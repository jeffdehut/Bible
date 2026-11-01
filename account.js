// Accounts: an optional sign-in that keeps highlights, notes and the reading plan the same on
// every device.
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
  //   last: when this device last synced, planDirty: the plan changed here and isn't sent yet,
  //   planSeen: this device has synced its plan with the account at least once }
  let state = {};
  try { state = JSON.parse(localStorage.getItem(STORE)) || {}; } catch (e) { /* storage unavailable */ }
  state.dirty = state.dirty || {};
  // Signed in before plans were kept in the account: send this device's plan once.
  if (state.session && !state.planSeen && R.plan.get().plan) state.planDirty = true;
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
    state.planDirty = !!R.plan.get().plan;
    state.planSeen = false;
    state.prefsSeen = {}; state.prefsDirty = {};
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
  // Email and password: the usual way in. A new account is confirmed by one email; a forgotten
  // password is reset by an emailed link that signs in and asks for a new one.
  async function passwordSignIn(email, password) {
    const s = await call("/auth/v1/token?grant_type=password", { method: "POST", auth: false, body: { email, password } });
    keep(s);
    signedIn();
  }
  // Returns "in" (signed in at once), "confirm" (an email to confirm), or "exists".
  async function signUp(email, password) {
    const back = encodeURIComponent(location.origin + location.pathname);
    const s = await call("/auth/v1/signup?redirect_to=" + back, { method: "POST", auth: false, body: { email, password } });
    if (s && s.access_token) { keep(s); signedIn(); return "in"; }
    const u = (s && (s.user || s)) || {};
    if (Array.isArray(u.identities) && !u.identities.length) return "exists";
    return "confirm";
  }
  async function recover(email) {
    const back = encodeURIComponent(location.origin + location.pathname);
    await call("/auth/v1/recover?redirect_to=" + back, { method: "POST", auth: false, body: { email } });
  }
  async function setPassword(password) {
    await call("/auth/v1/user", { method: "PUT", body: { password } });
  }
  // What the account service's answers mean, in plain words.
  const said = (e, what) => {
    if (navigator.onLine === false) return "You're offline. Try again when you're connected.";
    const m = (e && e.message) || "";
    if (/invalid login credentials/i.test(m)) return "That email and password don't match. Try again, or choose “Forgot your password?”. (If you've only signed in with emailed links, use it to set a password.)";
    if (/email not confirmed/i.test(m)) return "Confirm your email first: open the link we sent you, then sign in.";
    if (/password.*(at least|short|characters)/i.test(m)) return "Choose a longer password: at least 8 characters.";
    if (/rate limit|too many|security purposes/i.test(m)) return "Too many tries for now. Wait a minute and try again.";
    return what + ": " + m;
  };
  // A magic link brings the reader back with the session in the address; index.html sets it
  // aside before the reader reads the address. A password reset link does the same, and then
  // asks for the new password.
  async function fromLink() {
    let raw = null;
    try { raw = sessionStorage.getItem("pe.authHash"); sessionStorage.removeItem("pe.authHash"); } catch (e) { /* storage unavailable */ }
    if (!raw) return false;
    const p = new URLSearchParams(raw);
    if (p.get("error")) { problem = (p.get("error_description") || "That sign-in link didn't work").replace(/\+/g, " ") + ". Ask for a new link."; return true; }
    if (!p.get("access_token")) return false;
    if (p.get("type") === "recovery") step.reset = true;
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
        await syncPlan();
        await syncPrefs();
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
      // An account that keeps only the first five whole-verse colors (before supabase/schema.sql
      // was run again) refuses the others; then those verses go without their color there, and
      // everything else is still sent.
      try { await call("/rest/v1/rpc/push_annotations", { method: "POST", body: { rows } }); }
      catch (e) {
        if (!/highlight_check/.test(e.message)) throw e;
        const OLD = ["yellow", "green", "blue", "pink", "orange"];
        await call("/rest/v1/rpc/push_annotations", { method: "POST", body: { rows: rows.map(r => (r.highlight && !OLD.includes(r.highlight) ? { ...r, highlight: null } : r)) } });
      }
      for (const r of rows) if (state.dirty[r.verse] === sent[r.verse]) delete state.dirty[r.verse];
      save();
    }
  }
  // The reading plan: one record, the newer winning. The first time a device meets the account's
  // plan, if both follow the same plan, the days marked on either are kept.
  async function syncPlan() {
    const rows = await call("/rest/v1/plans?select=plan,updated_at");
    const theirs = rows && rows[0], mine = R.plan.get();
    if (theirs && theirs.updated_at > mine.t) {
      let p = theirs.plan, t = theirs.updated_at;
      if (!state.planSeen && p && mine.plan && p.id === mine.plan.id) {
        p = { ...p, start: Math.min(p.start, mine.plan.start), done: [...new Set([...p.done, ...mine.plan.done])].sort((a, b) => a - b) };
        if (p.done.length !== theirs.plan.done.length || p.start !== theirs.plan.start) { t = Date.now(); state.planDirty = true; }
      } else state.planDirty = false;
      R.plan.apply(p, t);
    } else if (theirs && theirs.updated_at === mine.t) state.planDirty = false;
    else if (!theirs && mine.plan) state.planDirty = true;
    if (state.planDirty) {
      const sent = R.plan.get();
      await call("/rest/v1/rpc/push_plan", { method: "POST", body: { plan: sent.plan, updated_at: sent.t } });
      if (R.plan.get().t === sent.t) state.planDirty = false;
    }
    state.planSeen = true;
    save();
  }
  // Other things kept by key (reader.prefs: your markings): the newer wins, and the first time a
  // device meets the account's, the two are joined.
  async function syncPrefs() {
    const P = R.prefs;
    if (!P) return;
    state.prefsDirty = state.prefsDirty || {};
    state.prefsSeen = state.prefsSeen || {};
    const rows = await call("/rest/v1/prefs?select=key,value,updated_at");
    for (const key of P.keys) {
      const theirs = (rows || []).find(r => r.key === key), mine = P.get(key);
      if (theirs && theirs.updated_at > mine.t) {
        if (!state.prefsSeen[key] && mine.t && theirs.value) {
          P.apply(key, P.merge(key, mine.v, theirs.value), Date.now());
          state.prefsDirty[key] = true;
        } else { P.apply(key, theirs.value, theirs.updated_at); delete state.prefsDirty[key]; }
      } else if (theirs && theirs.updated_at === mine.t) delete state.prefsDirty[key];
      else if (!theirs && mine.t) state.prefsDirty[key] = true;
      if (state.prefsDirty[key]) {
        const sent = P.get(key);
        await call("/rest/v1/rpc/push_pref", { method: "POST", body: { key, value: sent.v, updated_at: sent.t } });
        if (P.get(key).t === sent.t) delete state.prefsDirty[key];
      }
      state.prefsSeen[key] = true;
    }
    save();
  }
  let soon = 0;
  if (R.prefs) R.prefs.onChange = key => {
    if (!state.session) return;
    state.prefsDirty = state.prefsDirty || {};
    state.prefsDirty[key] = true;
    save();
    clearTimeout(soon);
    soon = setTimeout(sync, 2000);
  };
  R.plan.onChange = () => {
    if (!state.session) return;
    state.planDirty = true;
    save();
    clearTimeout(soon);
    soon = setTimeout(sync, 2000);
  };
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
  let step = { email: "", sent: false, busy: false, confirmDelete: false, mode: "in" };
  // The quieter choices under the sign-in form, as links.
  if (!document.getElementById("account-style")) {
    const st = document.createElement("style"); st.id = "account-style";
    st.textContent = `.account-alt { display: flex; flex-wrap: wrap; gap: 6px 16px; margin: 12px 0 4px; }
.account-alt .linkish { border: 0; background: none; padding: 4px 0; color: var(--lapis); font: 500 14px/1.3 var(--sans); cursor: pointer; text-decoration: underline; text-decoration-color: color-mix(in srgb, currentColor 35%, transparent); text-underline-offset: 3px; }
.account-alt .linkish:hover { text-decoration-color: currentColor; }
#account-body input[type="password"] { width: 100%; font: 400 16px/1.4 var(--sans); padding: 10px 12px; border: 1px solid var(--line); border-radius: 12px; background: var(--surface); color: var(--ink); }
#account-body input[type="password"]:focus { outline: 2px solid var(--lapis); outline-offset: 1px; border-color: transparent; }`;
    document.head.append(st);
  }
  // Signed in: set a password (after a reset link, or for an account made by emailed links), or change it.
  function passwordSection() {
    const open = step.reset || step.pwOpen;
    const box = el("div", { class: "section" }, el("h3", { text: step.reset ? "Choose a new password" : "Password" }));
    if (!open) {
      box.append(el("p", { class: "hint", text: "Sign in on any device with your email and a password." }),
        el("div", { class: "actions" }, el("button", { class: "btn line", type: "button", onclick: () => { step.pwOpen = true; render(); } }, "Set or change your password")));
      if (step.pwDone) box.append(el("p", { class: "account-sent", role: "status", text: "Your password is saved." }));
      return box;
    }
    const pw = el("input", { type: "password", id: "account-newpass", autocomplete: "new-password", required: true, minlength: "8" });
    box.append(el("form", { class: "account-form", onsubmit: async ev => {
      ev.preventDefault();
      if (pw.value.length < 8) { problem = "Choose a longer password: at least 8 characters."; render(); return; }
      step.busy = true; problem = ""; render();
      try { await setPassword(pw.value); step.reset = false; step.pwOpen = false; step.pwDone = true; }
      catch (e) { problem = said(e, "Couldn't save the password"); }
      step.busy = false; render();
    } },
      el("label", { for: "account-newpass", text: "New password (at least 8 characters)" }), pw,
      el("div", { class: "actions" },
        el("button", { class: "btn solid", type: "submit", disabled: step.busy }, step.busy ? "Saving…" : "Save password"),
        step.reset ? null : el("button", { class: "btn line", type: "button", onclick: () => { step.pwOpen = false; render(); } }, "Cancel"))));
    return box;
  }
  const privacy = () => el("p", { class: "hint" }, "Your account holds your email address, your highlights, notes and markings, and your reading plan, nothing else. ",
    el("a", { href: "privacy.html", text: "Privacy" }));
  function render() {
    $("open-account").hidden = false;
    const ab = $("acct-btn");
    if (ab) {
      ab.hidden = false;
      ab.classList.toggle("in", !!state.session);
      const tip = state.session ? state.session.user.email : "Sign in to sync across devices";
      ab.title = tip; ab.setAttribute("aria-label", state.session ? "Your account: " + state.session.user.email : tip);
    }
    R.signedIn = !!state.session;
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
        passwordSection(),
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
      if (step.mode !== "link") {
        // Email and password: sign in, or make an account.
        const pw = el("input", { type: "password", id: "account-password", autocomplete: step.mode === "new" ? "new-password" : "current-password", required: true, minlength: step.mode === "new" ? "8" : "1" });
        const fresh = step.mode === "new";
        kids.push(
          el("p", {}, fresh ? "Make an account to keep your highlights, notes and reading plan on every device you use." : "Sign in to keep your highlights, notes and reading plan on every device you use."),
          el("p", { class: "hint", text: "Reading never needs an account, and what you've saved on this device stays here either way." }),
          el("form", { class: "account-form", onsubmit: async ev => {
            ev.preventDefault();
            step.email = email.value.trim();
            if (fresh && pw.value.length < 8) { problem = "Choose a longer password: at least 8 characters."; render(); return; }
            step.busy = true; problem = ""; render();
            try {
              if (fresh) {
                const r = await signUp(step.email, pw.value);
                if (r === "confirm") { step.confirm = true; }
                else if (r === "exists") { step.mode = "in"; problem = "This email already has an account. Sign in with its password, or choose “Forgot your password?”."; }
              } else await passwordSignIn(step.email, pw.value);
            } catch (e) { problem = said(e, fresh ? "Couldn't make the account" : "Couldn't sign in"); }
            step.busy = false; render();
          } },
            el("label", { for: "account-email", text: "Email" }), email,
            el("label", { for: "account-password", text: fresh ? "Choose a password (at least 8 characters)" : "Password" }), pw,
            el("div", { class: "actions" },
              el("button", { class: "btn solid", type: "submit", disabled: step.busy }, step.busy ? (fresh ? "Making it…" : "Signing in…") : fresh ? "Make my account" : "Sign in"))),
          step.confirm ? el("p", { class: "account-sent", role: "status" }, el("strong", { text: "Check your email." }), " Open the link we sent to confirm your account, and you'll be signed in.") : null,
          el("p", { class: "account-alt" },
            el("button", { class: "linkish", type: "button", onclick: () => { step.mode = fresh ? "in" : "new"; step.confirm = false; problem = ""; render(); } }, fresh ? "I have an account: sign in" : "New here? Make an account"),
            fresh ? null : el("button", { class: "linkish", type: "button", onclick: async () => {
              step.email = email.value.trim();
              if (!step.email) { problem = "Type your email first, then choose “Forgot your password?”."; render(); return; }
              step.busy = true; problem = ""; render();
              try { await recover(step.email); step.mode = "link"; step.sent = true; step.resetSent = true; }
              catch (e) { problem = said(e, "Couldn't send the link"); }
              step.busy = false; render();
            } }, "Forgot your password?"),
            el("button", { class: "linkish", type: "button", onclick: () => { step.email = email.value.trim(); step.mode = "link"; problem = ""; render(); } }, "Email me a sign-in link instead")),
          privacy());
        body.replaceChildren(...kids.filter(Boolean));
        return;
      }
      kids.push(
        el("p", {}, "We'll email you a link to sign in with, no password needed."),
        el("p", { class: "account-alt" }, el("button", { class: "linkish", type: "button", onclick: () => { step.mode = "in"; problem = ""; render(); } }, "Sign in with a password instead")),
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
        el("p", {}, step.resetSent ? "We sent a link to reset your password to " : "We sent a sign-in link to ", el("strong", { text: step.email }), step.resetSent ? ". Open it on this device, in this browser: you'll be signed in and asked for a new password." : ". Open it on this device, in this browser, and you'll be signed in."),
        el("p", { class: "hint", text: step.resent ? "We sent another link: use the newest one, as each link works once." : "It can take a minute to arrive; if it doesn't, look in your spam folder. The link works once." }),
        el("div", { class: "actions" },
          el("button", { class: "btn solid", type: "button", disabled: step.busy, onclick: async () => {
            step.busy = true; problem = ""; render();
            try { await sendLink(step.email); step.resent = true; }
            catch (e) { problem = navigator.onLine === false ? "You're offline. Try again when you're connected." : "Couldn't send the link: " + e.message; }
            step.busy = false; render();
          } }, step.busy ? "Sending…" : "Send another link"),
          el("button", { class: "btn line", type: "button", onclick: () => { step.sent = false; step.resent = false; step.resetSent = false; step.mode = "in"; problem = ""; render(); } }, "Back to sign in")),
        privacy());
    }
    body.replaceChildren(...kids);
  }
  $("open-account").onclick = () => { render(); R.openSheet("account"); };

  // Signed in on another page (Felt Stories): adopt the session as a new sign-in, so what this
  // device has saved is sent to the account too.
  if (state.session && state.fresh) { delete state.fresh; signedIn(); }
  render();
  fromLink().then(opened => {
    if (opened) { render(); R.openSheet("account"); }
    else if (state.session) sync();
  });
})();
