// The icons of the Bible's themes, for the pages that set out a book's types and topics
// (psalms.html, proverbs.html). Each is drawn on a 24-unit square in strokes, like the site's
// other icons, and takes the color of the text around it.
//   Themes.svg(name, extraClass) -> an <svg> string;  Themes.el(name) -> an <svg> element
(() => {
  const I = {
    /* ---------- Psalms: the types ---------- */
    lament: '<path d="M12 3.5c3 4.2 6 7.4 6 10.9a6 6 0 0 1-12 0C6 10.9 9 7.7 12 3.5Z"/><path d="M9.5 15a2.6 2.6 0 0 0 2.5 2.4"/>',
    praise: '<circle cx="12" cy="12" r="3.8"/><path d="M12 2.5v2.6M12 18.9v2.6M2.5 12h2.6M18.9 12h2.6M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M5.3 18.7l1.8-1.8M16.9 7.1l1.8-1.8"/>',
    thanksgiving: '<path d="M6 3.5h12l-.8 5.6a5.2 5.2 0 0 1-10.4 0Z"/><path d="M12 14.4V19M8 20.5h8"/><path d="M8.5 6.5h7"/>',
    trust: '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8 7.5 9.5 4.3-1.5 7.5-4.9 7.5-9.5V6Z"/><path d="m9 12 2.2 2.2L15.5 10"/>',
    royal: '<path d="M3.5 8.5l4.2 3.6L12 5.5l4.3 6.6 4.2-3.6-1.8 9.5H5.3Z"/><path d="M5.5 20.5h13"/>',
    wisdom: '<path d="M12 21v-6.5"/><path d="M12 14.5c-4 0-6.5-2.2-6.5-5.2 0-2.6 2.1-4.6 4.3-4.6C10.4 3.4 11.4 3 12 3s1.6.4 2.2 1.7c2.2 0 4.3 2 4.3 4.6 0 3-2.5 5.2-6.5 5.2Z"/><path d="M4 21h16"/><path d="M12 11.5l-2-1.8M12 13l2.4-2"/>',
    history: '<path d="M7.5 3.5H18a2 2 0 0 1 2 2V7h-3"/><path d="M17 5.5v13a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V17h10.5"/><path d="M7.5 3.5a2 2 0 0 0-2 2V17"/><path d="M8.5 8.5h5.5M8.5 12h5.5"/>',
    /* ---------- Psalms: the groups ---------- */
    ascents: '<path d="M3 20.5h4.5V16H12v-4.5h4.5V7H21"/><path d="M15.5 3.5H21V9"/>',
    hallel: '<path d="M9 18V5.5l10.5-2v12.5"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="17" cy="16" r="2.5"/><path d="M9 9l10.5-2"/>',
    "final-hallel": '<path d="M12 2.5v4M12 17.5v4M2.5 12h4M17.5 12h4M5.3 5.3l2.8 2.8M15.9 15.9l2.8 2.8M5.3 18.7l2.8-2.8M15.9 8.1l2.8-2.8"/><circle cx="12" cy="12" r="1.6"/>',
    kingship: '<path d="M7.5 17V5.5A1.5 1.5 0 0 1 9 4h6a1.5 1.5 0 0 1 1.5 1.5V17"/><path d="M5.5 12.5h13V17h-13Z"/><path d="M7 17v4M17 17v4"/>',
    zion: '<path d="M3 20.5h18"/><path d="M4.5 20.5V10.5l2.5-2 2.5 2v10M14.5 20.5v-10l2.5-2 2.5 2v10"/><path d="M9.5 20.5V14h5v6.5"/><path d="M9.5 14a2.5 2.5 0 0 1 5 0"/>',
    creation: '<path d="M2.5 20 9 10.5l4 5.8 2.6-3.6 5.9 7.3Z"/><circle cx="16.5" cy="6" r="2.6"/>',
    torah: '<path d="M4.5 20.5V7.5a3.5 3.5 0 0 1 7 0v13ZM12.5 20.5V7.5a3.5 3.5 0 0 1 7 0v13Z"/><path d="M6.5 10.5h3M6.5 14h3M14.5 10.5h3M14.5 14h3"/>',
    messianic: '<path d="M12 3.2 14.6 8.8l6 .7-4.5 4.1 1.2 6L12 16.6l-5.3 3 1.2-6-4.5-4.1 6-.7Z"/>',
    penitential: '<path d="M12 20s-8-4.7-8-10.5A4.4 4.4 0 0 1 12 7a4.4 4.4 0 0 1 8 2.5C20 15.3 12 20 12 20Z"/><path d="M12 7l-1.8 4.2 3.2 2-1.4 3.8"/>',
    acrostic: '<path d="M3 18.5 6.6 6.5l3.6 12M4.3 14.5h4.6"/><path d="M13.5 6.5h4.2a2.8 2.8 0 0 1 0 5.6h-4.2Zm0 5.6h4.8a3.2 3.2 0 0 1 0 6.4h-4.8Z"/>',
    imprecatory: '<path d="M13.5 2.5 5 13.5h6.2l-1.2 8 8.5-11.2h-6.3Z"/>',
    entrance: '<path d="M5 21V10a7 7 0 0 1 14 0v11"/><path d="M3 21h18M12 21V8.5"/><path d="M10 15.5v.1M14 15.5v.1"/>',
    prophetic: '<path d="M4.5 5h15a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H10l-5.5 4v-4h0a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Z"/><path d="M12 8v3.5M12 13.6v.1"/>',
    story: '<path d="M2.5 20.5c1-7.5 4.5-13 9.5-13s8.5 5.5 9.5 13"/><path d="M8 20.5c0-4 1.8-7 4-7s4 3 4 7"/><path d="M1.5 20.5h21"/>',
    /* ---------- Psalms: who wrote them ---------- */
    David: '<path d="M6.5 4c-2 3.5-1.6 9.6 1.5 14h8c3.1-4.4 3.5-10.5 1.5-14"/><path d="M6.5 4c1.6 1.1 3.4 1.6 5.5 1.6s3.9-.5 5.5-1.6"/><path d="M9.5 6.5V18M12 7v11M14.5 6.5V18"/><path d="M8 21h8"/>',
    Asaph: '<path d="M2.5 10c2.2-2.6 6-2.6 8.2 0-2.2 2.6-6 2.6-8.2 0ZM13.3 10c2.2-2.6 6-2.6 8.2 0-2.2 2.6-6 2.6-8.2 0Z"/><path d="M6.6 7.8V5M17.4 7.8V5"/><path d="M9.5 16l-1.5 2.5M12 16.5V19M14.5 16l1.5 2.5"/>',
    "Sons of Korah": '<path d="M6 21V4.5h12V21"/><path d="M3.5 21h17"/><path d="M14.5 13v.1"/><path d="M9 4.5v16.5"/>',
    Solomon: '<path d="M3 9.5 12 4l9 5.5"/><path d="M5 9.5v9M9.5 9.5v9M14.5 9.5v9M19 9.5v9"/><path d="M3 20.5h18M4 9.5h16"/>',
    Moses: '<path d="M7 21 14.5 4.5"/><path d="M14.5 4.5c2.3-.6 4 1 3.6 3.2-.3 1.6-2 2.2-3 1.4"/><path d="M4 21h7"/>',
    Heman: '<path d="M10 18V4l7.5 3"/><circle cx="7.5" cy="18" r="2.5"/>',
    Ethan: '<path d="M6 20.5C6 12.5 9 7 14 4"/><path d="M14 4c3 2.2 4 6.5 4 16.5"/><path d="M4.5 20.5h15"/><path d="M8.4 11h8.8M7.3 15.5h10.5"/>',
    "No name": '<circle cx="12" cy="12" r="8" stroke-dasharray="2.2 3"/>',
    /* ---------- Proverbs: the topics ---------- */
    speech: '<path d="M5 4.5h14a1.5 1.5 0 0 1 1.5 1.5v8.5A1.5 1.5 0 0 1 19 16h-8.5L5.5 20v-4H5a1.5 1.5 0 0 1-1.5-1.5V6A1.5 1.5 0 0 1 5 4.5Z"/><path d="M8 9h8M8 12h5"/>',
    honesty: '<path d="M12 3.5v16.5M8 20.5h8M4.5 7h15"/><path d="M4.5 7 2 13a2.5 2.5 0 0 0 5 0ZM19.5 7 17 13a2.5 2.5 0 0 0 5 0Z"/><circle cx="12" cy="4" r=".6"/>',
    wealth: '<ellipse cx="9" cy="7" rx="5.5" ry="2.5"/><path d="M3.5 7v4c0 1.4 2.5 2.5 5.5 2.5s5.5-1.1 5.5-2.5V7"/><path d="M14.5 9c3 0 5.5 1.1 5.5 2.5v5c0 1.4-2.5 2.5-5.5 2.5S9 17.9 9 16.5v-3"/><path d="M9 13.5c0 1.4 2.5 2.5 5.5 2.5s5.5-1.1 5.5-2.5"/>',
    work: '<circle cx="5.5" cy="12.5" r="2.2"/><ellipse cx="10.5" cy="12.5" rx="1.8" ry="1.5"/><ellipse cx="16.8" cy="12.5" rx="3.7" ry="2.6"/><path d="M10.5 14 8 18.5M10.5 14v5M10.5 14l2.5 4.5M10.5 11 8 6.5M10.5 11V6M10.5 11l2.5-4.5"/><path d="M4.6 10.5 3.2 7.5M6.4 10.5l1-3"/>',
    anger: '<path d="M12 2.5c1 3.6 5.5 5.6 5.5 10.6a5.5 5.5 0 0 1-11 0c0-2.8 1.5-4.4 2.7-6 .4 1.8 1.4 2.8 2.6 3.1-.5-2.8-.8-5.2.2-7.7Z"/>',
    pride: '<path d="M6.5 21V8.5h11V21"/><path d="M6.5 8.5V4h2.2v2h2.2V4h2.2v2h2.2V4h2.2v4.5"/><path d="M4.5 21h15"/><path d="M12.5 10.5 11 13.5l2 1.5-1.5 3"/>',
    friends: '<circle cx="8.5" cy="8" r="3"/><circle cx="16.2" cy="9" r="2.5"/><path d="M3 20c0-3.6 2.5-6 5.5-6s5.5 2.4 5.5 6"/><path d="M14.7 14.3c3.4-.6 6.3 1.8 6.3 5.7"/>',
    family: '<circle cx="8" cy="6" r="2.6"/><path d="M4 21v-5.5a4 4 0 0 1 8 0V21"/><circle cx="17" cy="11" r="2"/><path d="M14 21v-3a3 3 0 0 1 6 0v3"/>',
    marriage: '<circle cx="9" cy="13.5" r="5.5"/><circle cx="15" cy="13.5" r="5.5"/><path d="M13.5 5.5 15 3.5h2l1.5 2-2.5 2.5Z"/>',
    kings: '<path d="M3.5 8.5l4.2 3.6L12 5.5l4.3 6.6 4.2-3.6-1.8 9.5H5.3Z"/><path d="M5.5 20.5h13"/>',
    justice: '<path d="M10.2 3.8l6 6M7.8 6.2l6 6M9 5l3.6 3.6"/><path d="M11.8 10.6 4 18.4l1.6 1.6 7.8-7.8"/><path d="M13 21h8"/>',
    fools: '<path d="M4 18c0-5.5 1.8-9.6 5-11-1 3 0 6 3 8 3-2 4-5 3-8 3.2 1.4 5 5.5 5 11Z"/><circle cx="8.6" cy="4.8" r="1.4"/><circle cx="15.4" cy="4.8" r="1.4"/><path d="M3.5 18h17v2.5h-17Z"/>',
    wisdom_lamp: '<path d="M3.5 13.5h17c0 3-3.6 5-8.5 5s-8.5-2-8.5-5Z"/><path d="M20.5 13.5c1-.7 1.3-1.6 1.2-2.7"/><path d="M8.5 18.5 7.5 21h9l-1-2.5"/><path d="M12 4c1.2 1.6 2 2.6 2 4a2 2 0 0 1-4 0c0-1.4.8-2.4 2-4Z"/>',
    lord: '<path d="M2.5 20.5 9.5 9l3.5 5.5 2.5-3.5 6 9.5Z"/><path d="M12 2.5v2.5M7 4l1.4 2M17 4l-1.4 2M4 7.5l2 1M20 7.5l-2 1"/>',
    righteous: '<path d="M12 21v-7"/><path d="M12 14 6.5 5M12 14l5.5-9"/><path d="M4.5 6.5 6.5 4.5l2 2M15.5 6.5l2-2 2 2"/>',
    drink: '<path d="M7 3.5h10l-.6 5a4.4 4.4 0 0 1-8.8 0Z"/><path d="M12 13v5.5M8.5 20.5h7"/><path d="M7.4 7h9.2"/>',
    life: '<path d="M12 21v-9"/><path d="M12 12c0-4 2.5-6.5 7-6.5 0 4-2.5 6.5-7 6.5Z"/><path d="M12 15c0-3-2-5-6-5 0 3 2 5 6 5Z"/><path d="M8 21h8"/>',
    heart: '<path d="M12 20s-8-4.7-8-10.5A4.4 4.4 0 0 1 12 7a4.4 4.4 0 0 1 8 2.5C20 15.3 12 20 12 20Z"/>',
    but: '<path d="M4 8h15M15.5 4.5 19 8l-3.5 3.5"/><path d="M20 16H5M8.5 12.5 5 16l3.5 3.5"/>',
    /* ---------- Proverbs: the collections ---------- */
    pillars: '<path d="M3 8.5 12 4l9 4.5"/><path d="M4 8.5h16"/><path d="M5.5 8.5V19M9 8.5V19M12.5 8.5V19M16 8.5V19M19 8.5V19"/><path d="M3 20.5h18"/>',
    scroll: '<path d="M7.5 3.5H18a2 2 0 0 1 2 2V7h-3"/><path d="M17 5.5v13a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V17h10.5"/><path d="M7.5 3.5a2 2 0 0 0-2 2V17"/><path d="M8.5 8.5h5.5M8.5 12h5.5"/>',
    ear: '<path d="M6.5 9a5.5 5.5 0 0 1 11 0c0 3.2-2.6 4.3-3.6 5.9-.8 1.4-.6 3.1-2.4 4.6-1.6 1.3-3.8.9-4.5-.7"/><path d="M9.5 9.2a2.5 2.5 0 0 1 5 0c0 1.6-1.6 2-1.6 3.3"/>',
    wall: '<path d="M2.5 20.5h19"/><path d="M3.5 20.5V16h5.5v4.5M9 16v-4.5h5.5V16M14.5 20.5V16H20v4.5"/><path d="M3.5 16v-3.5H7"/><path d="M17 11.5l1.5-1.5 1 2"/>',
    quill: '<path d="M20 3.5C12.5 4.5 7.5 9.5 5.5 18.5"/><path d="M20 3.5c-1 6.2-5.3 10.2-11.5 11.2"/><path d="M12 9.5l-2.5 1"/><path d="M4 21l1.5-2.5"/>',
    question: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 0 1 5 .4c0 1.8-2.5 2.1-2.5 3.7M12 16.8v.1"/>',
    spindle: '<path d="M12 2.5v19"/><path d="M8 8.5c0-1.4 1.8-2.4 4-2.4s4 1 4 2.4v6.5c0 1.4-1.8 2.4-4 2.4s-4-1-4-2.4Z"/><path d="M8 10.5l8 2.2M8 13.3l8 2.2"/>',
  };
  const svg = (name, cls = "") => I[name] ? `<svg class="ti${cls ? " " + cls : ""}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${I[name]}</svg>` : "";
  const el = (name, cls) => { const t = document.createElement("template"); t.innerHTML = svg(name, cls); return t.content.firstChild; };
  window.Themes = { icons: I, svg, el };
})();
