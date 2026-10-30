// Accounts: an optional sign-in that keeps highlights and notes the same on every device.
//
// Reading, highlighting and notes never need an account: they are saved in the browser first.
// Signing in, with a link sent by email (no password), adds what this device has saved to the
// account and brings in what the account holds, verse by verse, the newest change winning.
// After that each change is sent a few seconds after it is made, and the account is checked
// for changes from other devices when the reader opens or comes back into view.
//
// The service is Supabase (see supabase/schema.sql), reached through its REST interface with
// fetch, so nothing else is loaded. config.js turns it on; without it this file does nothing
// and the reader looks as it always has.
(() => {
  const C = (window.SITE_CONFIG || {}).supabase || {};
  const R = window.reader;
  if (!C.url || !C.key || !R) return;
  const BASE = C.url.replace(/\/+$/, "");
  const STORE = "pe.account";
  const $ = id => document.getElementById(id);

  // { session: {access_token, refresh_token, expires_at, user: {id, email}},
  //   pulled: the server time of the newest change fetched, dirty: {verse: time changed},
  //   last: when this device last synced }
  let state = {};
  try { state = JSON.parse(localStorage.getItem(STORE)) || {}; } catch (e) { /* storage unavailable */ }
  state.dirty = state.dirty || {};
  const save = () => { try { localStorage.setItem(STORE, JSON.stringify(state)); } catch (e) { /* storage unavailable */ } };
  let status = "", problem = "";

  /* ---------- Talking to Supabase ---------- */
  async function call(path, { method = "GET", body, auth = true, retry = true } = {}) {
    const headers = { apikey: C.key };
    if (body !== undefined) headers["Content-Type"] = "application/json";
    if (auth) {
      await fresh();
      headers.Authorization = "Bearer " + state.session.access_token;
    }
    const res = await fetch(BASE + path, { method, headers, body: body === undefined ? undefined : JSON.stringify(body) });
    if (res.status === 401 && auth && retry) {
      await refresh();
      return call(path, { method, body, auth, retry: false });
    }
    if (!res.ok) {
      let msg = "";
      try { const j = await res.json(); msg = j.msg || j.message || j.error_description || j.error || ""; } catch (e) { /* not JSON */ }
      const err = new Error(msg || `The account service answered ${res.status}`);
      err.status = res.status;
      throw err;
    }
    const text = await res.text();
    return text ? JSON.parse(text) : null;
  }
  async function fresh() {
    if (!state.session) throw new Error("Not signed in");
    if (state.session.expires_at - 60 < Date.now() / 1000) await refresh();
  }
  let refreshing = null;
  function refresh() {
    if (!refreshing) refreshing = (async () => {
      try {
        const s = await call("/auth/v1/token?grant_type=refresh_token", { method: "POST", auth: false, body: { refresh_token: state.session.refresh_token } });
        keep(s);
      } catch (e) {
        if (e.status === 400 || e.status === 401) signedOut("Your sign-in has ended. Sign in again to keep syncing.");
        throw e;
      } finally { refreshing = null; }
    })();
    return refreshing;
  }
  function keep(s, user) {
    const u = s.user || user || (state.session && state.session.user);
    state.session = {
      access_token: s.access_token, refresh_token: s.refresh_token,
      expires_at: s.expires_at || Math.floor(Date.now() / 1000) + (+s.expires_in || 3600),
      user: { id: u.id, email: u.email },
    };
    save();
  }

  /* ---------- Signing in and out ---------- */
  function signedIn() {
    // Send everything saved here and fetch everything the account holds; the newer of each
    // verse wins, so this is safe however often it happens.
    state.pulled = null;
    state.dirty = {};
    for (const [id, a] of Object.entries(R.annotations.all())) state.dirty[id] = a.t || Date.now();
    save();
    render();
    sync();
  }
  function signedOut(message) {
    state = { dirty: {} };
    save();
    problem = message || "";
    render();
  }
  async function sendLink(email) {
    // The email's link brings the reader back to this page (the live site or a preview),
    // provided Supabase's Redirect URLs allow it.
    const back = encodeURIComponent(location.origin + location.pathname);
    await call("/auth/v1/otp?redirect_to=" + back, { method: "POST", auth: false, body: { email, create_user: true } });
  }
  // A magic link brings the reader back with the session in the address; index.html sets it
  // aside before the reader reads the address.
  async function fromLink() {
    let raw = null;
    try { raw = sessionStorage.getItem("pe.authHash"); sessionStorage.removeItem("pe.authHash"); } catch (e) { /* storage unavailable */ }
    if (!raw) return false;
    const p = new URLSearchParams(raw);
    if (p.get("error")) { problem = (p.get("error_description") || "That sign-in link didn't work").replace(/\+/g, " ") + ". Ask for a new link."; return true; }
    if (!p.get("access_token")) return false;
    state.session = { access_token: p.get("access_token"), refresh_token: p.get("refresh_token"), expires_at: +p.get("expires_at") || Math.floor(Date.now() / 1000) + (+p.get("expires_in") || 3600), user: { id: "", email: "" } };
    try {
      const user = await call("/auth/v1/user");
      state.session.user = { id: user.id, email: user.email };
      signedIn();
    } catch (e) {
      state.session = null;
      problem = "That sign-in link didn't work. Ask for a new link.";
      save();
    }
    return true;
  }
  async function signOut() {
    try { await call("/auth/v1/logout", { method: "POST" }); } catch (e) { /* ended already, or offline */ }
    signedOut("Signed out. Your highlights and notes stay on this device.");
  }
  async function deleteAccount() {
    await call("/rest/v1/rpc/delete_account", { method: "POST", body: {} });
    signedOut("Your account and everything in it are deleted. Your highlights and notes stay on this device.");
  }

  /* ---------- Sync ---------- */
  let syncing = null, again = false;
  function sync() {
    if (!state.session) return Promise.resolve();
    if (syncing) { again = true; return syncing; }
    syncing = (async () => {
      status = "syncing"; render();
      try {
        await pull();
        await push();
        state.last = Date.now(); save();
        status = "ok"; problem = "";
      } catch (e) {
        status = navigator.onLine === false ? "offline" : "error";
        problem = status === "offline" ? "" : e.message;
      } finally {
        syncing = null;
        render();
        if (again) { again = false; sync(); }
      }
    })();
    return syncing;
  }
  // Fetch what changed since the last look, a minute back to be sure of nothing missed (a
  // change seen twice does no harm), and keep each newer than this device's own.
  async function pull() {
    const since = state.pulled ? new Date(Date.parse(state.pulled) - 60000).toISOString() : null;
    for (let offset = 0; ; offset += 1000) {
      const rows = await call("/rest/v1/annotations?select=verse,highlight,ranges,note,bookmark,updated_at,deleted,synced_at" +
        (since ? "&synced_at=gt." + encodeURIComponent(since) : "") + "&order=synced_at.asc,verse.asc&limit=1000&offset=" + offset);
      const notes = R.annotations.all(), changes = [];
      for (const r of rows) {
        const mine = state.dirty[r.verse] ?? (notes[r.verse] ? notes[r.verse].t || 0 : 0);
        if (r.updated_at > mine) {
          changes.push([r.verse, r.deleted ? null : { h: r.highlight || undefined, r: r.ranges || undefined, n: r.note || undefined, b: r.bookmark || undefined, t: r.updated_at }]);
          delete state.dirty[r.verse];
        } else if (r.updated_at === mine) delete state.dirty[r.verse];
        if (!state.pulled || Date.parse(r.synced_at) > Date.parse(state.pulled)) state.pulled = r.synced_at;
      }
      if (changes.length) R.annotations.apply(changes);
      save();
      if (rows.length < 1000) break;
    }
  }
  // Send this device's changes; the account keeps each only if it is newer than its own.
  async function push() {
    const sent = { ...state.dirty }, ids = Object.keys(sent);
    const notes = R.annotations.all();
    for (let k = 0; k < ids.length; k += 500) {
      const rows = ids.slice(k, k + 500).map(id => notes[id]
        ? { verse: id, highlight: notes[id].h || null, ranges: notes[id].r || null, note: notes[id].n || null, bookmark: notes[id].b || null, updated_at: notes[id].t || sent[id], deleted: false }
        : { verse: id, highlight: null, ranges: null, note: null, bookmark: null, updated_at: sent[id], deleted: true });
      await call("/rest/v1/rpc/push_annotations", { method: "POST", body: { rows } });
      for (const r of rows) if (state.dirty[r.verse] === sent[r.verse]) delete state.dirty[r.verse];
      save();
    }
  }
  let soon = 0;
  R.annotations.onChange = ids => {
    if (!state.session) return;
    const notes = R.annotations.all();
    for (const id of ids) state.dirty[id] = notes[id] ? notes[id].t || Date.now() : Date.now();
    save();
    clearTimeout(soon);
    soon = setTimeout(sync, 2000);
  };
  document.addEventListener("visibilitychange", () => { if (document.visibilityState === "visible") sync(); });
  // Signed in or out in another tab (as when the emailed link opens in a new one): follow it.
  addEventListener("storage", e => {
    if (e.key !== STORE) return;
    let next = {};
    try { next = JSON.parse(e.newValue) || {}; } catch (err) { /* unreadable */ }
    if (!!next.session === !!state.session) return;
    state = next; state.dirty = state.dirty || {};
    step = { email: "", sent: false, busy: false, confirmDelete: false };
    problem = "";
    render();
    if (state.session) sync();
  });
  addEventListener("online", () => sync());
  setInterval(() => { if (document.visibilityState === "visible") sync(); }, 5 * 60 * 1000);

  /* ---------- The account sheet ---------- */
  const body = $("account-body");
  const el = (tag, attrs = {}, ...kids) => {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v == null || v === false) continue;
      if (k === "class") n.className = v; else if (k === "text") n.textContent = v;
      else if (k.startsWith("on")) n.addEventListener(k.slice(2), v); else n.setAttribute(k, v === true ? "" : v);
    }
    for (const c of kids) if (c != null) n.append(c);
    return n;
  };
  const ago = t => {
    const s = Math.round((Date.now() - t) / 1000);
    return s < 45 ? "just now" : s < 90 ? "a minute ago" : s < 3600 ? `${Math.round(s / 60)} minutes ago` : s < 5400 ? "an hour ago"
      : s < 86400 ? `${Math.round(s / 3600)} hours ago` : new Date(t).toLocaleDateString();
  };
  const statusText = () => status === "syncing" ? "Syncing…" : status === "offline" ? "Offline: changes will sync when you're back online"
    : status === "error" ? "Couldn't sync just now. It will try again." : state.last ? `Synced ${ago(state.last)}` : "Not synced yet";
  let step = { email: "", sent: false, busy: false, confirmDelete: false };
  const privacy = () => el("p", { class: "hint" }, "Your account holds your email address and your highlights and notes, nothing else. ",
    el("a", { href: "privacy.html", text: "Privacy" }));
  function render() {
    $("open-account").hidden = false;
    $("account-sub").textContent = state.session ? statusText() : "";
    $("mine-account").textContent = state.session ? `Also kept in your account, ${state.session.user.email}. ${statusText()}.`
      : "Sign in to keep them in an account and on every device you use.";
    if (!body) return;
    const kids = [];
    if (problem) kids.push(el("p", { class: "notice", role: "status", text: problem }));
    if (state.session) {
      kids.push(
        el("p", {}, "Signed in as ", el("strong", { text: state.session.user.email }), "."),
        el("p", { class: "hint", role: "status", text: statusText() }),
        el("div", { class: "actions" },
          el("button", { class: "btn solid", type: "button", onclick: () => sync(), disabled: status === "syncing" }, "Sync now"),
          el("button", { class: "btn line", type: "button", onclick: () => signOut() }, "Sign out")),
        el("p", { class: "hint", text: "Signing out leaves your highlights and notes on this device, and in your account." }),
        el("div", { class: "section" },
          el("h3", { text: "Delete your account" }),
          el("p", { class: "hint", text: "This deletes your account and every highlight and note in it, for good. What is saved on this device stays here." }),
          el("div", { class: "actions" }, el("button", { class: "btn line danger", type: "button", onclick: async ev => {
            if (!step.confirmDelete) { step.confirmDelete = true; render(); return; }
            ev.target.disabled = true;
            try { await deleteAccount(); } catch (e) { problem = "Couldn't delete the account: " + e.message; render(); }
            step.confirmDelete = false;
          } }, step.confirmDelete ? "Delete it: tap again to confirm" : "Delete my account"))),
        privacy());
    } else if (!step.sent) {
      const email = el("input", { type: "email", id: "account-email", autocomplete: "email", inputmode: "email", placeholder: "you@example.com", required: true, value: step.email });
      kids.push(
        el("p", {}, "Sign in with your email to keep your highlights and notes on every device you use. We'll email you a link to sign in with: there's no password."),
        el("p", { class: "hint", text: "Reading never needs an account, and what you've saved on this device stays here either way." }),
        el("form", { class: "account-form", onsubmit: async ev => {
          ev.preventDefault();
          step.email = email.value.trim();
          step.busy = true; problem = ""; render();
          try { await sendLink(step.email); step.sent = true; }
          catch (e) { problem = navigator.onLine === false ? "You're offline. Try again when you're connected." : "Couldn't send the link: " + e.message; }
          step.busy = false; render();
        } },
          el("label", { for: "account-email", text: "Email" }), email,
          el("div", { class: "actions" }, el("button", { class: "btn solid", type: "submit", disabled: step.busy }, step.busy ? "Sending…" : "Email me a sign-in link"))),
        privacy());
    } else {
      // The link signs in whichever tab it opens in; this one follows (see the storage listener).
      kids.push(
        el("p", { class: "account-sent" }, el("strong", { text: "Check your email." })),
        el("p", {}, "We sent a sign-in link to ", el("strong", { text: step.email }), ". Open it on this device, in this browser, and you'll be signed in."),
        el("p", { class: "hint", text: step.resent ? "We sent another link: use the newest one, as each link works once." : "It can take a minute to arrive; if it doesn't, look in your spam folder. The link works once." }),
        el("div", { class: "actions" },
          el("button", { class: "btn solid", type: "button", disabled: step.busy, onclick: async () => {
            step.busy = true; problem = ""; render();
            try { await sendLink(step.email); step.resent = true; }
            catch (e) { problem = navigator.onLine === false ? "You're offline. Try again when you're connected." : "Couldn't send the link: " + e.message; }
            step.busy = false; render();
          } }, step.busy ? "Sending…" : "Send another link"),
          el("button", { class: "btn line", type: "button", onclick: () => { step.sent = false; step.resent = false; problem = ""; render(); } }, "Use a different email")),
        privacy());
    }
    body.replaceChildren(...kids);
  }
  $("open-account").onclick = () => { render(); R.openSheet("account"); };

  render();
  fromLink().then(opened => {
    if (opened) { render(); R.openSheet("account"); }
    else if (state.session) sync();
  });
})();
