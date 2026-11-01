// The Story Board's pieces, cut from felt: people, animals, things, nature, and the scenes behind
// them. Each piece is SVG markup in its own box (w x h, in board units: the board is 1600 x 1000)
// with a starting size (s). Faces, robes and the like are flat shapes in felt colours; the board
// gives them their felt edges and texture (storyboard.js).
//
//   window.SB_ART = { pieces: [{ id, name, cat, w, h, s, svg }], scenes: [{ id, name, svg }], cats }
(() => {
  const C = {
    red: "#b8403a", blue: "#2f5fa8", sky: "#5b8fd1", green: "#3d8a4a", leaf: "#5fa84a", brown: "#8a5a2b", tan: "#c9a46a",
    gold: "#e2b23c", purple: "#6f4a9e", cream: "#efe7d4", white: "#f7f4ec", orange: "#d9772b", grey: "#7c7f86",
    dark: "#3a3430", pink: "#e59a9a", teal: "#2f8c87", wine: "#7d2f3f", sand: "#d8bb84", stone: "#9a948a", wood: "#7a5232",
  };
  const SKIN = ["#e8bb94", "#c98e5f", "#a8703f", "#7e4f2c"];
  const HAIR = { black: "#2a1d16", brown: "#5a3720", grey: "#9b9690", white: "#ece8de", gold: "#d9a640", red: "#8c3a1c" };

  // A person, standing, in a 120 x 260 box.
  function person(o) {
    const skin = o.skin || SKIN[1], hair = o.hair || HAIR.black, robe = o.robe || C.blue, dk = shade(robe, -0.18);
    const p = [];
    if (o.wings) p.push(`<path d="M58 84C18 34-6 100 14 168c10-30 22-50 44-62Z" fill="${C.white}"/><path d="M62 84c40-50 64 16 44 84-10-30-22-50-44-62Z" fill="${C.white}"/><path d="M20 120c10-10 20-16 34-20M106 120c-10-10-20-16-34-20" stroke="#d8d2c4" stroke-width="3" fill="none"/>`);
    if (o.long) p.push(`<path d="M38 40c-6 30-4 58 4 72h36c8-14 10-42 4-72Z" fill="${hair}"/>`);
    p.push(`<rect x="53" y="54" width="14" height="18" fill="${skin}"/>`);
    p.push(`<path d="M38 72Q60 62 82 72L102 238Q60 250 18 238Z" fill="${robe}"/>`);
    p.push(`<path d="M22 222Q60 234 98 222L102 238Q60 250 18 238Z" fill="${dk}"/>`);
    if (o.mantle) p.push(`<path d="M38 72Q50 66 62 72L96 236Q84 241 72 242L46 112Z" fill="${o.mantle}"/>`);
    if (o.armor) p.push(`<path d="M40 76Q60 68 80 76L84 150Q60 158 36 150Z" fill="${o.armor}"/><path d="M40 104h44M38 126h46" stroke="${shade(o.armor, -0.25)}" stroke-width="3"/>`);
    if (o.breast) p.push(`<rect x="46" y="88" width="28" height="30" rx="3" fill="${C.gold}"/><g fill="${C.red}"><circle cx="53" cy="96" r="3"/><circle cx="67" cy="110" r="3"/></g><g fill="${C.teal}"><circle cx="67" cy="96" r="3"/><circle cx="53" cy="110" r="3"/></g>`);
    if (o.sash) p.push(`<path d="M34 128Q60 136 88 126L89 138Q60 148 33 140Z" fill="${o.sash}"/>`);
    // Arms and hands.
    p.push(`<path d="M40 76Q24 112 28 152h13Q40 114 50 88Z" fill="${dk}"/><path d="M80 76Q96 112 92 152H79Q80 114 70 88Z" fill="${dk}"/>`);
    p.push(`<circle cx="34" cy="156" r="7.5" fill="${skin}"/><circle cx="86" cy="156" r="7.5" fill="${skin}"/>`);
    if (o.staff) p.push(`<path d="M90 252V44Q90 20 74 22Q62 25 66 38" stroke="${C.wood}" stroke-width="6" fill="none" stroke-linecap="round"/><circle cx="86" cy="156" r="7.5" fill="${skin}"/>`);
    if (o.spear) p.push(`<path d="M92 254V20" stroke="${C.wood}" stroke-width="5" stroke-linecap="round"/><path d="M92 2l8 22H84Z" fill="${C.grey}"/><circle cx="86" cy="156" r="7.5" fill="${skin}"/>`);
    if (o.shield) p.push(`<ellipse cx="30" cy="150" rx="22" ry="30" fill="${o.shield}"/><ellipse cx="30" cy="150" rx="8" ry="10" fill="${C.gold}"/>`);
    if (o.gift) p.push(`<rect x="22" y="142" width="24" height="20" rx="3" fill="${C.gold}"/><path d="M22 150h24" stroke="${C.red}" stroke-width="3"/><circle cx="34" cy="156" r="7" fill="${skin}"/>`);
    if (o.scroll) p.push(`<rect x="24" y="140" width="16" height="30" rx="4" fill="${C.cream}"/><rect x="22" y="138" width="20" height="5" rx="2" fill="${C.wood}"/><rect x="22" y="167" width="20" height="5" rx="2" fill="${C.wood}"/>`);
    p.push(`<ellipse cx="47" cy="246" rx="10" ry="5" fill="#5a3a22"/><ellipse cx="73" cy="246" rx="10" ry="5" fill="#5a3a22"/>`);
    // Head.
    p.push(`<circle cx="60" cy="38" r="21" fill="${skin}"/>`);
    if (!o.head && !o.helmet) p.push(o.bald ? `<path d="M40 40Q40 30 44 26Q42 40 46 44Z M80 40Q80 30 76 26Q78 40 74 44Z" fill="${hair}"/>` : `<path d="M39 40Q38 15 60 15Q82 15 81 40Q76 26 60 26Q44 26 39 40Z" fill="${hair}"/>`);
    if (o.beard) p.push(`<path d="M41 43Q42 72 60 75Q78 72 79 43Q74 57 60 57Q46 57 41 43Z" fill="${o.beard}"/><path d="M52 49Q60 46 68 49" stroke="${shade(o.beard, -0.3)}" stroke-width="2" fill="none" stroke-linecap="round"/>`);
    p.push(`<circle cx="53" cy="38" r="2.4" fill="#2a1a10"/><circle cx="67" cy="38" r="2.4" fill="#2a1a10"/>`);
    if (!o.beard) p.push(`<path d="M54 47Q60 51 66 47" stroke="#7a3b2a" stroke-width="2" fill="none" stroke-linecap="round"/><circle cx="48" cy="45" r="4" fill="${C.pink}" opacity=".45"/><circle cx="72" cy="45" r="4" fill="${C.pink}" opacity=".45"/>`);
    if (o.head) p.push(o.veil
      ? `<path d="M35 46Q33 12 60 12Q87 12 85 46L94 120Q80 110 77 54Q72 28 60 28Q48 28 43 54Q40 110 26 120Z" fill="${o.head}"/>`
      : `<path d="M36 46Q34 13 60 13Q86 13 84 46L90 88Q77 80 75 52Q71 29 60 29Q49 29 45 52Q43 80 30 88Z" fill="${o.head}"/>` + (o.band ? `<rect x="40" y="21" width="40" height="6" rx="3" fill="${o.band}"/>` : ""));
    if (o.crown) p.push(`<path d="M42 22V6l9 9 9-13 9 13 9-9v16Z" fill="${C.gold}"/><circle cx="60" cy="14" r="3" fill="${C.red}"/>`);
    if (o.helmet) p.push(`<path d="M38 36Q38 12 60 12Q82 12 82 36Z" fill="${C.grey}"/><path d="M60 12Q60 0 74 2Q66 6 62 14" fill="${C.red}"/>`);
    if (o.turban) p.push(`<path d="M38 30Q36 8 60 8Q84 8 82 30Q60 22 38 30Z" fill="${o.turban}"/><circle cx="60" cy="16" r="4" fill="${C.gold}"/>`);
    return p.join("");
  }
  function shade(hex, k) {
    const n = parseInt(hex.slice(1), 16), f = c => Math.max(0, Math.min(255, Math.round(c + (k < 0 ? c : 255 - c) * k)));
    return "#" + [n >> 16, (n >> 8) & 255, n & 255].map(f).map(c => c.toString(16).padStart(2, "0")).join("");
  }

  const people = [
    ["jesus", "Jesus", { robe: C.white, mantle: C.red, hair: HAIR.brown, beard: HAIR.brown, skin: SKIN[1] }],
    ["mary", "Mary", { robe: C.cream, head: C.blue, veil: true, skin: SKIN[1] }],
    ["joseph", "Joseph", { robe: C.brown, mantle: C.tan, head: C.cream, band: C.blue, beard: HAIR.black, skin: SKIN[2] }],
    ["man", "Man", { robe: C.blue, mantle: C.brown, head: C.white, band: C.red, beard: HAIR.black, skin: SKIN[2] }],
    ["woman", "Woman", { robe: C.green, head: C.orange, veil: true, skin: SKIN[1] }],
    ["old-man", "Old man", { robe: C.tan, mantle: C.wine, head: C.cream, band: C.brown, beard: HAIR.white, skin: SKIN[1], staff: true }],
    ["old-woman", "Old woman", { robe: C.purple, head: C.grey, veil: true, skin: SKIN[2] }],
    ["boy", "Boy", { robe: C.orange, hair: HAIR.black, skin: SKIN[1], sash: C.brown }, 0.68],
    ["girl", "Girl", { robe: C.pink, hair: HAIR.brown, long: true, skin: SKIN[1], sash: C.white }, 0.66],
    ["shepherd", "Shepherd", { robe: C.tan, mantle: C.brown, head: C.red, band: C.white, beard: HAIR.black, staff: true, skin: SKIN[2] }],
    ["shepherd-boy", "Shepherd boy", { robe: C.leaf, head: C.cream, band: C.brown, staff: true, skin: SKIN[1] }, 0.7],
    ["king", "King", { robe: C.purple, mantle: C.red, crown: true, beard: HAIR.brown, sash: C.gold, skin: SKIN[1] }],
    ["queen", "Queen", { robe: C.purple, mantle: C.gold, crown: true, long: true, hair: HAIR.black, skin: SKIN[1] }],
    ["soldier", "Soldier", { robe: C.red, armor: C.grey, helmet: true, shield: C.wine, spear: true, skin: SKIN[1] }],
    ["angel", "Angel", { robe: C.white, sash: C.gold, wings: true, hair: HAIR.gold, skin: SKIN[0] }, 1.05],
    ["priest", "Priest", { robe: C.white, turban: C.white, breast: true, sash: C.blue, beard: HAIR.grey, skin: SKIN[1] }],
    ["wise-man", "Wise man", { robe: C.wine, mantle: C.gold, turban: C.teal, gift: true, beard: HAIR.black, skin: SKIN[3] }],
    ["fisherman", "Fisherman", { robe: C.sky, mantle: C.tan, beard: HAIR.grey, sash: C.brown, skin: SKIN[2] }],
    ["teacher", "Teacher", { robe: C.cream, mantle: C.blue, head: C.white, band: C.blue, beard: HAIR.grey, scroll: true, skin: SKIN[1] }],
    ["adam", "Adam", { robe: "#9b7b52", hair: HAIR.brown, beard: HAIR.brown, skin: SKIN[2] }],
    ["eve", "Eve", { robe: "#9b7b52", long: true, hair: HAIR.brown, skin: SKIN[1] }],
    ["noah", "Noah", { robe: C.green, mantle: C.tan, beard: HAIR.white, hair: HAIR.white, skin: SKIN[1] }],
    ["abraham", "Abraham", { robe: C.blue, mantle: C.tan, head: C.cream, band: C.red, beard: HAIR.white, staff: true, skin: SKIN[2] }],
    ["sarah", "Sarah", { robe: C.wine, head: C.cream, veil: true, skin: SKIN[2] }],
    ["moses", "Moses", { robe: C.brown, mantle: C.red, head: C.cream, band: C.brown, beard: HAIR.white, staff: true, skin: SKIN[2] }],
    ["david", "David", { robe: C.orange, hair: HAIR.red, sash: C.brown, skin: SKIN[0] }, 0.74],
    ["goliath", "Goliath", { robe: C.dark, armor: C.grey, helmet: true, shield: C.grey, spear: true, beard: HAIR.black, skin: SKIN[2] }, 1.5],
    ["daniel", "Daniel", { robe: C.teal, mantle: C.gold, head: C.white, band: C.teal, skin: SKIN[2] }],
    ["peter", "Peter", { robe: C.blue, mantle: C.brown, beard: HAIR.grey, hair: HAIR.grey, skin: SKIN[2] }],
    ["paul", "Paul", { robe: C.brown, mantle: C.red, beard: HAIR.black, bald: true, scroll: true, skin: SKIN[1] }],
    ["zacchaeus", "Zacchaeus", { robe: C.gold, mantle: C.wine, beard: HAIR.black, skin: SKIN[2] }, 0.78],
    ["pharisee", "Pharisee", { robe: C.cream, mantle: C.teal, head: C.white, band: C.gold, beard: HAIR.grey, scroll: true, skin: SKIN[1] }],
  ].map(([id, name, o, s = 1]) => ({ id, name, cat: "people", w: 120, h: 260, s, svg: person(o) }));
  people.push({ id: "baby", name: "Baby", cat: "people", w: 110, h: 60, s: 1, svg:
    `<ellipse cx="62" cy="34" rx="44" ry="20" fill="${C.cream}"/><path d="M30 26Q60 40 100 30M34 44Q66 52 98 40" stroke="#d6ccb4" stroke-width="3" fill="none"/><circle cx="22" cy="30" r="17" fill="${SKIN[1]}"/><path d="M8 26Q10 10 24 12Q36 14 38 26Q26 18 8 26Z" fill="${HAIR.brown}"/><path d="M16 32Q18 34 20 32M24 32Q26 34 28 32" stroke="#2a1a10" stroke-width="1.8" fill="none"/>` });

  const animals = [
    ["sheep", "Sheep", 170, 120, `<g fill="${C.dark}"><rect x="46" y="80" width="10" height="34" rx="4"/><rect x="66" y="84" width="10" height="32" rx="4"/><rect x="100" y="84" width="10" height="32" rx="4"/><rect x="118" y="80" width="10" height="34" rx="4"/></g><g fill="${C.white}"><circle cx="60" cy="62" r="26"/><circle cx="88" cy="50" r="28"/><circle cx="116" cy="60" r="26"/><circle cx="76" cy="78" r="24"/><circle cx="106" cy="80" r="24"/><circle cx="134" cy="72" r="20"/></g><ellipse cx="34" cy="58" rx="18" ry="22" fill="${C.dark}"/><ellipse cx="24" cy="44" rx="10" ry="5" fill="${C.dark}" transform="rotate(-30 24 44)"/><circle cx="29" cy="54" r="2.6" fill="#fff"/><circle cx="40" cy="54" r="2.6" fill="#fff"/>`],
    ["lamb", "Lamb", 170, 120, null, 0.62],
    ["donkey", "Donkey", 200, 170, `<g fill="#6f6a66"><rect x="52" y="100" width="12" height="60" rx="5"/><rect x="74" y="104" width="12" height="56" rx="5"/><rect x="126" y="104" width="12" height="56" rx="5"/><rect x="146" y="100" width="12" height="60" rx="5"/></g><ellipse cx="104" cy="96" rx="64" ry="36" fill="#8d8781"/><path d="M164 86q24 6 22 40" stroke="#6f6a66" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M56 82Q40 50 34 36L56 30Q66 54 76 74Z" fill="#8d8781"/><ellipse cx="34" cy="40" rx="18" ry="26" fill="#8d8781" transform="rotate(30 34 40)"/><ellipse cx="22" cy="56" rx="12" ry="9" fill="#cfc8bf"/><path d="M38 18L30-2 46 14ZM50 22L52 0 60 20Z" fill="#6f6a66"/><circle cx="38" cy="34" r="3" fill="#1d1a18"/><path d="M48 60Q62 70 80 76" stroke="#3a3430" stroke-width="5" fill="none"/>`],
    ["camel", "Camel", 230, 210, `<g fill="#a77b48"><rect x="62" y="120" width="12" height="84" rx="5"/><rect x="84" y="124" width="12" height="80" rx="5"/><rect x="152" y="124" width="12" height="80" rx="5"/><rect x="172" y="120" width="12" height="84" rx="5"/></g><path d="M58 128Q60 92 90 92Q100 44 124 64Q138 40 160 76Q196 86 192 130Q130 146 58 128Z" fill="#c69a63"/><path d="M66 112Q44 92 40 54L58 50Q62 84 80 100Z" fill="#c69a63"/><ellipse cx="40" cy="44" rx="24" ry="14" fill="#c69a63"/><circle cx="34" cy="40" r="3" fill="#1d1a18"/><path d="M48 32l4-8 6 8Z" fill="#a77b48"/><path d="M190 120q14 10 10 34" stroke="#a77b48" stroke-width="5" fill="none"/><path d="M96 92q30-6 58 0" stroke="${C.red}" stroke-width="8" fill="none"/>`],
    ["lion", "Lion", 220, 160, `<g fill="#c98a2e"><rect x="56" y="96" width="16" height="58" rx="7"/><rect x="80" y="100" width="16" height="54" rx="7"/><rect x="146" y="100" width="16" height="54" rx="7"/><rect x="168" y="96" width="16" height="58" rx="7"/></g><ellipse cx="124" cy="94" rx="70" ry="38" fill="#dda243"/><path d="M190 90q30-10 22-46" stroke="#c98a2e" stroke-width="7" fill="none" stroke-linecap="round"/><circle cx="210" cy="44" r="9" fill="#8a4e1c"/><circle cx="58" cy="72" r="52" fill="#a85e22"/><circle cx="58" cy="76" r="34" fill="#e7b25a"/><circle cx="46" cy="70" r="3.4" fill="#1d1a18"/><circle cx="70" cy="70" r="3.4" fill="#1d1a18"/><path d="M52 84h12l-6 7Z" fill="#5a3214"/><path d="M50 96Q58 102 66 96" stroke="#5a3214" stroke-width="2.4" fill="none"/>`],
    ["ox", "Ox", 220, 160, `<g fill="#5e3b22"><rect x="56" y="96" width="16" height="58" rx="6"/><rect x="78" y="100" width="16" height="54" rx="6"/><rect x="148" y="100" width="16" height="54" rx="6"/><rect x="170" y="96" width="16" height="58" rx="6"/></g><ellipse cx="122" cy="92" rx="76" ry="40" fill="#7a4e2c"/><path d="M196 86q18 10 12 40" stroke="#5e3b22" stroke-width="6" fill="none"/><ellipse cx="44" cy="80" rx="30" ry="36" fill="#7a4e2c"/><ellipse cx="40" cy="104" rx="20" ry="13" fill="#d9b48c"/><path d="M20 52Q0 44 6 26Q14 44 28 46ZM66 52Q86 44 80 26Q72 44 58 46Z" fill="${C.cream}"/><circle cx="32" cy="74" r="3.4" fill="#1d1a18"/><circle cx="56" cy="74" r="3.4" fill="#1d1a18"/>`],
    ["dove", "Dove", 140, 90, `<path d="M20 52Q40 20 80 38Q110 22 130 30Q112 46 104 62Q80 80 40 70Z" fill="${C.white}"/><path d="M70 40Q86 4 120 6Q104 26 92 46Z" fill="#e3ddd0"/><circle cx="30" cy="48" r="13" fill="${C.white}"/><circle cx="27" cy="45" r="2.4" fill="#1d1a18"/><path d="M17 49l-12 4 12 3Z" fill="${C.orange}"/><path d="M30 30q4-6 10-4" stroke="${C.leaf}" stroke-width="4" fill="none"/>`],
    ["fish", "Fish", 140, 70, `<path d="M10 35Q50 0 100 35Q50 70 10 35Z" fill="${C.sky}"/><path d="M98 35l36-24v48Z" fill="${C.sky}"/><path d="M40 20q-6 15 0 30M58 16q-6 19 0 38" stroke="#4a78b8" stroke-width="3" fill="none"/><circle cx="28" cy="31" r="4" fill="#1d1a18"/>`],
    ["great-fish", "Great fish", 420, 220, `<path d="M20 120Q60 30 220 40Q330 46 360 110L410 60 404 180 360 140Q330 200 210 204Q70 210 20 120Z" fill="#46617f"/><path d="M40 140Q120 190 250 180" stroke="#8aa3bd" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M30 126q40 10 70 0" stroke="#2c3e54" stroke-width="6" fill="none"/><circle cx="90" cy="96" r="9" fill="#1d1a18"/><circle cx="93" cy="93" r="3" fill="#fff"/>`],
    ["snake", "Serpent", 200, 140, `<path d="M20 120Q60 130 70 96Q80 60 120 74Q160 88 160 50Q160 24 186 26" stroke="${C.leaf}" stroke-width="20" fill="none" stroke-linecap="round"/><path d="M40 118q20 4 26-14M100 76q20 4 30 0" stroke="#3d7a32" stroke-width="5" fill="none" stroke-dasharray="3 8"/><ellipse cx="186" cy="24" rx="14" ry="11" fill="${C.leaf}"/><circle cx="190" cy="20" r="2.6" fill="#1d1a18"/><path d="M198 28l10 4-8 2 8 4" stroke="${C.red}" stroke-width="2.4" fill="none"/>`],
    ["raven", "Raven", 130, 100, `<path d="M18 60Q40 30 80 44Q112 36 126 50Q108 58 98 70Q72 92 34 76Z" fill="#26262e"/><path d="M60 48Q76 10 110 18Q94 36 84 56Z" fill="#3a3a44"/><circle cx="30" cy="54" r="14" fill="#26262e"/><circle cx="26" cy="50" r="2.4" fill="#fff"/><path d="M16 54L0 60l16 4Z" fill="#4a4a50"/>`],
    ["goat", "Goat", 180, 140, `<g fill="#6a5440"><rect x="48" y="84" width="10" height="50" rx="4"/><rect x="66" y="88" width="10" height="46" rx="4"/><rect x="118" y="88" width="10" height="46" rx="4"/><rect x="134" y="84" width="10" height="50" rx="4"/></g><ellipse cx="96" cy="80" rx="56" ry="28" fill="#8a7058"/><path d="M152 70l14-12-4 18Z" fill="#8a7058"/><ellipse cx="38" cy="58" rx="18" ry="24" fill="#8a7058"/><path d="M30 38Q20 10 40 4Q30 22 40 36Z" fill="#cfc4b0"/><path d="M34 80l4 18 6-16Z" fill="#cfc4b0"/><circle cx="32" cy="54" r="2.6" fill="#1d1a18"/>`],
  ].map(([id, name, w, h, svg, s = 1]) => ({ id, name, cat: "animals", w, h, s, svg }));
  animals.find(a => a.id === "lamb").svg = animals.find(a => a.id === "sheep").svg;

  const things = [
    ["ark", "Ark", 520, 300, `<path d="M20 170H500L460 270Q260 300 60 270Z" fill="${C.wood}"/><path d="M40 196H480M50 226H470M64 254H456" stroke="#5d3c22" stroke-width="5"/><rect x="120" y="90" width="280" height="84" fill="#9b6b3e"/><path d="M100 96L260 30 420 96Z" fill="#6a4426"/><rect x="170" y="112" width="40" height="34" fill="#3a2414"/><rect x="310" y="112" width="40" height="34" fill="#3a2414"/><rect x="240" y="118" width="40" height="56" fill="#3a2414"/>`],
    ["boat", "Fishing boat", 320, 260, `<path d="M150 20V180" stroke="${C.wood}" stroke-width="8"/><path d="M158 26Q250 90 250 170H158Z" fill="${C.cream}"/><path d="M142 40Q80 110 70 170H142Z" fill="#e2d6bd"/><path d="M10 176H310L272 240Q160 258 48 240Z" fill="${C.wood}"/><path d="M26 200H294" stroke="#5d3c22" stroke-width="5"/>`],
    ["tent", "Tent", 300, 200, `<path d="M150 10L290 190H10Z" fill="${C.brown}"/><path d="M150 10L80 190M150 10L220 190" stroke="#6a4426" stroke-width="6"/><path d="M150 70L120 190H180Z" fill="#3a2414"/><path d="M40 150L260 150" stroke="${C.cream}" stroke-width="8" opacity=".6"/>`],
    ["house", "House", 260, 220, `<rect x="20" y="60" width="220" height="150" fill="${C.sand}"/><rect x="10" y="44" width="240" height="22" fill="${C.tan}"/><rect x="104" y="120" width="52" height="90" rx="26" fill="#5d3c22"/><rect x="40" y="96" width="40" height="34" fill="#5d3c22"/><rect x="180" y="96" width="40" height="34" fill="#5d3c22"/><path d="M200 44V10h40v34" fill="none" stroke="${C.tan}" stroke-width="8"/>`],
    ["wall", "City wall", 420, 240, `<rect x="0" y="60" width="420" height="180" fill="${C.stone}"/><path d="M0 60V30h40v30h30V30h40v30h30V30h40v30h30V30h40v30h30V30h40v30h30V30h40v30" fill="${C.stone}"/><path d="M160 240V150Q210 100 260 150V240Z" fill="#3a2e24"/><path d="M0 110h420M0 160h160M260 160h160M0 210h160M260 210h160M60 60v50M140 110v50M300 60v50M380 110v50M80 160v50M340 160v50" stroke="#7a756c" stroke-width="4"/>`],
    ["well", "Well", 200, 200, `<path d="M30 20h140" stroke="${C.wood}" stroke-width="10" stroke-linecap="round"/><path d="M44 24v80M156 24v80" stroke="${C.wood}" stroke-width="8"/><path d="M100 24v50" stroke="${C.dark}" stroke-width="3"/><rect x="88" y="70" width="24" height="22" rx="3" fill="${C.wood}"/><path d="M20 100Q100 84 180 100V190Q100 206 20 190Z" fill="${C.stone}"/><path d="M20 130Q100 118 180 130M20 160Q100 150 180 160M70 100v90M130 100v90" stroke="#7a756c" stroke-width="4" fill="none"/>`],
    ["jar", "Water jar", 100, 150, `<path d="M30 10h40v18Q96 50 92 96Q88 140 50 146Q12 140 8 96Q4 50 30 28Z" fill="#b8653a"/><path d="M14 80q36 14 72 0" stroke="#8e4a28" stroke-width="5" fill="none"/><rect x="26" y="4" width="48" height="10" rx="5" fill="#9a5230"/>`],
    ["bread", "Loaves and fish", 220, 150, `<path d="M20 70H200L180 140H40Z" fill="#a8763f"/><path d="M30 90H190M36 112H184" stroke="#7d5428" stroke-width="5"/><ellipse cx="70" cy="62" rx="34" ry="20" fill="#e0a85a"/><ellipse cx="128" cy="58" rx="34" ry="20" fill="#d89a48"/><ellipse cx="100" cy="44" rx="30" ry="18" fill="#e8b468"/><path d="M150 40q20-16 40 0-20 16-40 0Zm40 0 14-10v20Z" fill="${C.sky}"/>`],
    ["tablets", "Stone tablets", 220, 180, `<path d="M10 176V50Q10 10 54 10Q100 10 100 50V176Z" fill="${C.stone}"/><path d="M120 176V50Q120 10 164 10Q210 10 210 50V176Z" fill="${C.stone}"/><g stroke="#5f5a52" stroke-width="5" stroke-linecap="round"><path d="M30 60h50M30 88h50M30 116h50M30 144h40M140 60h50M140 88h50M140 116h50M140 144h40"/></g>`],
    ["staff", "Staff", 70, 260, `<path d="M40 256V48Q40 12 18 16Q4 20 10 36" stroke="${C.wood}" stroke-width="9" fill="none" stroke-linecap="round"/>`],
    ["crown", "Crown", 140, 100, `<path d="M10 90V24l30 26 30-44 30 44 30-26v66Z" fill="${C.gold}"/><rect x="10" y="76" width="120" height="14" fill="#c9952a"/><circle cx="70" cy="56" r="8" fill="${C.red}"/><circle cx="34" cy="64" r="6" fill="${C.teal}"/><circle cx="106" cy="64" r="6" fill="${C.teal}"/>`],
    ["lamp", "Oil lamp", 160, 110, `<path d="M20 70Q20 40 80 40Q140 40 150 62L120 70Q100 96 60 96Q20 96 20 70Z" fill="#b8653a"/><path d="M60 40Q70 30 82 40" fill="#8e4a28"/><path d="M146 58Q130 30 146 6Q162 30 146 58Z" fill="${C.gold}"/><path d="M146 54Q138 38 146 24Q154 38 146 54Z" fill="${C.orange}"/>`],
    ["manger", "Manger", 220, 150, `<path d="M20 30H200L170 110H50Z" fill="${C.wood}"/><path d="M30 50H190M40 80H180" stroke="#5d3c22" stroke-width="5"/><path d="M50 110L30 146M170 110L190 146" stroke="${C.wood}" stroke-width="10" stroke-linecap="round"/><path d="M22 34Q60 6 100 26Q140 2 198 32" stroke="${C.gold}" stroke-width="10" fill="none" stroke-linecap="round"/>`],
    ["cross", "Cross", 160, 300, `<rect x="66" y="10" width="28" height="290" fill="${C.wood}"/><rect x="10" y="70" width="140" height="26" fill="${C.wood}"/><path d="M80 20v270M20 83h130" stroke="#5d3c22" stroke-width="3" opacity=".5"/>`],
    ["tomb", "Empty tomb", 300, 220, `<path d="M10 210Q20 30 150 20Q280 30 290 210Z" fill="${C.stone}"/><path d="M100 210V130Q140 90 180 130V210Z" fill="#2a2420"/><circle cx="236" cy="168" r="44" fill="#8a847a"/><circle cx="236" cy="168" r="30" fill="none" stroke="#6d675e" stroke-width="5"/>`],
    ["scroll", "Scroll", 180, 120, `<rect x="30" y="20" width="120" height="84" fill="${C.cream}"/><path d="M44 42h92M44 62h92M44 82h70" stroke="#b8a888" stroke-width="5" stroke-linecap="round"/><rect x="14" y="8" width="22" height="108" rx="10" fill="${C.wood}"/><rect x="144" y="8" width="22" height="108" rx="10" fill="${C.wood}"/>`],
    ["sling", "Sling and stones", 160, 120, `<path d="M20 20Q60 100 80 96Q100 92 140 20" stroke="${C.brown}" stroke-width="5" fill="none"/><ellipse cx="80" cy="94" rx="18" ry="12" fill="#6a4426"/><g fill="${C.stone}"><circle cx="30" cy="104" r="9"/><circle cx="52" cy="110" r="8"/><circle cx="118" cy="108" r="9"/></g>`],
    ["throne", "Throne", 200, 240, `<rect x="40" y="10" width="120" height="150" rx="16" fill="${C.wine}"/><rect x="56" y="26" width="88" height="120" rx="10" fill="${C.red}"/><rect x="20" y="140" width="160" height="40" rx="8" fill="${C.gold}"/><path d="M36 180v56M164 180v56" stroke="${C.gold}" stroke-width="14" stroke-linecap="round"/>`],
    ["altar", "Altar", 200, 180, `<rect x="20" y="70" width="160" height="106" fill="${C.stone}"/><path d="M20 106h160M20 142h160M70 70v36M130 106v36M100 142v34" stroke="#7a756c" stroke-width="4"/><path d="M60 72Q50 30 80 20Q74 44 92 50Q96 20 120 6Q112 40 138 46Q150 60 140 72Z" fill="${C.orange}"/><path d="M80 72Q78 50 96 40Q100 60 116 60Q124 66 120 72Z" fill="${C.gold}"/>`],
  ].map(([id, name, w, h, svg, s = 1]) => ({ id, name, cat: "things", w, h, s, svg }));

  const nature = [
    ["tree", "Tree", 240, 300, `<path d="M106 300V180Q100 150 80 136M134 300V180Q140 150 162 140" stroke="${C.wood}" stroke-width="26" stroke-linecap="round" fill="none"/><g fill="${C.green}"><circle cx="120" cy="96" r="72"/><circle cx="60" cy="130" r="50"/><circle cx="180" cy="130" r="50"/><circle cx="90" cy="60" r="46"/><circle cx="160" cy="62" r="46"/></g><g fill="${C.leaf}" opacity=".7"><circle cx="100" cy="80" r="26"/><circle cx="160" cy="116" r="22"/><circle cx="60" cy="122" r="18"/></g>`],
    ["fruit-tree", "Fruit tree", 240, 300, null],
    ["palm", "Palm tree", 220, 320, `<path d="M112 316Q104 200 118 100" stroke="#8a6a3e" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M104 300h20M104 260h20M106 220h18M108 180h18M112 140h14" stroke="#6d5230" stroke-width="5"/><g fill="${C.green}"><path d="M118 96Q60 40 6 90Q60 70 118 100Z"/><path d="M118 96Q180 40 214 92Q160 70 118 100Z"/><path d="M118 96Q110 20 150 0Q132 50 120 100Z"/><path d="M118 96Q70 10 30 30Q80 50 116 100Z"/><path d="M120 96Q168 120 190 170Q150 128 118 102Z"/><path d="M116 96Q70 120 46 168Q90 126 118 102Z"/></g><g fill="#7a4e2c"><circle cx="110" cy="108" r="8"/><circle cx="126" cy="110" r="8"/></g>`],
    ["bush", "Burning bush", 220, 200, `<g fill="${C.green}"><circle cx="70" cy="140" r="50"/><circle cx="150" cy="140" r="50"/><circle cx="110" cy="110" r="56"/></g><path d="M50 120Q30 60 70 30Q66 70 90 76Q86 30 120 4Q118 52 146 58Q164 30 180 50Q190 90 170 124Z" fill="${C.orange}" opacity=".95"/><path d="M80 120Q72 86 96 66Q100 92 116 92Q120 66 138 54Q148 90 140 120Z" fill="${C.gold}"/>`],
    ["rock", "Rock", 240, 150, `<path d="M10 146Q0 80 50 50Q90 6 150 20Q220 30 234 100Q240 140 230 146Z" fill="${C.stone}"/><path d="M60 70Q100 50 130 64M150 40Q190 60 200 100" stroke="#7a756c" stroke-width="5" fill="none"/>`],
    ["hill", "Hill", 520, 220, `<path d="M0 220Q120 20 260 30Q420 40 520 220Z" fill="${C.leaf}"/><path d="M120 120Q200 80 280 96" stroke="${C.green}" stroke-width="8" fill="none"/>`],
    ["mountain", "Mountain", 520, 360, `<path d="M0 360L210 20 300 140 360 80 520 360Z" fill="#8a8580"/><path d="M210 20L260 100 236 96 214 120 196 92 172 98Z" fill="${C.white}"/><path d="M360 80L392 140 372 134 356 150 340 120Z" fill="${C.white}"/>`],
    ["water", "Water", 600, 160, `<rect x="0" y="40" width="600" height="120" fill="#4f86c6"/><path d="M0 40Q50 10 100 40T200 40T300 40T400 40T500 40T600 40V60H0Z" fill="#6b9fd6"/><path d="M40 90Q70 76 100 90M240 110Q270 96 300 110M440 90Q470 76 500 90" stroke="#a6c8ec" stroke-width="5" fill="none"/>`],
    ["sun", "Sun", 200, 200, `<g stroke="${C.gold}" stroke-width="12" stroke-linecap="round"><path d="M100 6v30M100 164v30M6 100h30M164 100h30M34 34l20 20M146 146l20 20M34 166l20-20M146 54l20-20"/></g><circle cx="100" cy="100" r="54" fill="${C.gold}"/><circle cx="100" cy="100" r="40" fill="#f0c650"/>`],
    ["moon", "Moon", 140, 160, `<path d="M90 6Q20 20 20 80Q20 140 90 154Q40 126 40 80Q40 34 90 6Z" fill="#f2e7b8"/>`],
    ["star", "Star", 140, 140, `<path d="M70 4l17 46h48l-39 28 15 48-41-29-41 29 15-48L5 50h48Z" fill="${C.gold}"/>`],
    ["cloud", "Cloud", 260, 140, `<g fill="${C.white}"><circle cx="70" cy="86" r="46"/><circle cx="130" cy="64" r="56"/><circle cx="192" cy="88" r="44"/><rect x="40" y="88" width="180" height="44" rx="22"/></g>`],
    ["rainbow", "Rainbow", 500, 260, `<g fill="none" stroke-width="24"><path d="M30 260a220 220 0 0 1 440 0" stroke="#d64a3a"/><path d="M54 260a196 196 0 0 1 392 0" stroke="${C.orange}"/><path d="M78 260a172 172 0 0 1 344 0" stroke="${C.gold}"/><path d="M102 260a148 148 0 0 1 296 0" stroke="${C.leaf}"/><path d="M126 260a124 124 0 0 1 248 0" stroke="${C.sky}"/><path d="M150 260a100 100 0 0 1 200 0" stroke="${C.purple}"/></g>`],
    ["grass", "Grass", 300, 80, `<path d="M0 80Q20 20 30 80Q40 10 56 80Q70 30 84 80Q96 0 112 80Q126 26 140 80Q156 6 170 80Q184 30 196 80Q212 10 226 80Q240 26 252 80Q268 4 280 80Q290 30 300 80Z" fill="${C.leaf}"/>`],
    ["flowers", "Flowers", 200, 120, `<path d="M40 120V60M100 120V40M160 120V64" stroke="${C.green}" stroke-width="6"/><g fill="${C.pink}"><circle cx="40" cy="50" r="16"/><circle cx="160" cy="54" r="16"/></g><circle cx="100" cy="32" r="18" fill="${C.gold}"/><g fill="#f5e6a8"><circle cx="40" cy="50" r="6"/><circle cx="160" cy="54" r="6"/></g><circle cx="100" cy="32" r="7" fill="${C.orange}"/>`],
  ].map(([id, name, w, h, svg, s = 1]) => ({ id, name, cat: "nature", w, h, s, svg }));
  nature.find(a => a.id === "fruit-tree").svg = nature.find(a => a.id === "tree").svg + `<g fill="${C.red}"><circle cx="90" cy="100" r="10"/><circle cx="140" cy="80" r="10"/><circle cx="170" cy="130" r="10"/><circle cx="64" cy="140" r="10"/><circle cx="120" cy="140" r="10"/></g>`;

  // Scenes, behind everything: 1600 x 1000.
  const S = (sky, rest) => `<rect width="1600" height="1000" fill="${sky}"/>` + rest;
  // Light blue graph paper: a line every 40 units, a stronger one every 200.
  const gridLines = (step, every, out = "") => { for (let v = step; v < 1600; v += step) if (!every || v % every === 0) out += `M${v} 0V1000`; for (let v = step; v < 1000; v += step) if (!every || v % every === 0) out += `M0 ${v}H1600`; return out; };
  const GRID_SVG = `<path d="${gridLines(40)}" stroke="#d6e6f7" stroke-width="2" fill="none"/><path d="${gridLines(40, 200)}" stroke="#a9c9ec" stroke-width="2.5" fill="none"/>`;
  const scenes = [
    ["hills", "Green hills", S("#7fb2e5", `<path d="M0 560Q300 420 620 520Q980 380 1600 540V1000H0Z" fill="#6fae58"/><path d="M0 700Q420 600 820 700Q1200 620 1600 690V1000H0Z" fill="#4f9440"/>`)],
    ["desert", "Desert", S("#f2d7a2", `<path d="M0 600Q400 500 800 600Q1200 520 1600 590V1000H0Z" fill="#dcb874"/><path d="M0 760Q500 660 1000 760Q1300 700 1600 750V1000H0Z" fill="#c9a15c"/>`)],
    ["sea", "Sea", S("#8ec1ea", `<rect y="520" width="1600" height="480" fill="#3f78b8"/><path d="M0 520Q100 490 200 520T400 520T600 520T800 520T1000 520T1200 520T1400 520T1600 520V560H0Z" fill="#5a92cf"/><path d="M0 760Q120 730 240 760T480 760T720 760T960 760T1200 760T1440 760T1680 760V800H0Z" fill="#336aa6"/>`)],
    ["river", "River", S("#86bbe8", `<path d="M0 520Q400 440 800 520Q1200 460 1600 520V1000H0Z" fill="#66a654"/><path d="M560 1000Q700 800 820 700Q920 620 1080 560L1200 560Q1020 640 940 740Q840 880 800 1000Z" fill="#4f86c6"/>`)],
    ["garden", "Garden", S("#9ccbef", `<path d="M0 520Q800 440 1600 520V1000H0Z" fill="#5fa84a"/><g fill="#3d8a4a"><circle cx="160" cy="470" r="90"/><circle cx="280" cy="500" r="70"/><circle cx="1360" cy="470" r="96"/><circle cx="1480" cy="500" r="70"/></g><g fill="#e59a9a"><circle cx="400" cy="760" r="12"/><circle cx="1200" cy="820" r="12"/><circle cx="900" cy="700" r="12"/></g>`)],
    ["night", "Night", S("#1b2747", `<path d="M0 640Q400 560 800 640Q1200 580 1600 630V1000H0Z" fill="#26364f"/><g fill="#f5e6a8" opacity=".7"><circle cx="200" cy="120" r="4"/><circle cx="420" cy="220" r="3"/><circle cx="760" cy="90" r="4"/><circle cx="1100" cy="180" r="3"/><circle cx="1400" cy="100" r="4"/><circle cx="1250" cy="320" r="3"/><circle cx="560" cy="360" r="3"/></g>`)],
    ["town", "Town", S("#a9cdee", `<path d="M0 640H1600V1000H0Z" fill="#d8bb84"/><g fill="#c9a46a"><rect x="80" y="430" width="220" height="210"/><rect x="340" y="480" width="180" height="160"/><rect x="1080" y="450" width="200" height="190"/><rect x="1320" y="410" width="220" height="230"/></g><g fill="#7a5232"><rect x="160" y="540" width="60" height="100" rx="30"/><rect x="400" y="560" width="50" height="80" rx="25"/><rect x="1150" y="550" width="60" height="90" rx="30"/><rect x="1400" y="530" width="60" height="110" rx="30"/></g>`)],
    ["indoors", "Indoors", S("#d9c49b", `<rect y="700" width="1600" height="300" fill="#a8835a"/><path d="M0 700H1600" stroke="#8a6a44" stroke-width="10"/><rect x="620" y="180" width="360" height="260" fill="#8ec1ea"/><path d="M620 310H980M800 180V440" stroke="#7a5232" stroke-width="14"/><rect x="610" y="170" width="380" height="280" fill="none" stroke="#7a5232" stroke-width="18"/>`)],
    ["graph", "Graph paper", S("#fbfdff", GRID_SVG)],
    ["blue", "Blue felt", S("#2f5fa8", "")],
    ["green", "Green felt", S("#3d7a44", "")],
    ["tan", "Tan felt", S("#c9a874", "")],
    ["black", "Black felt", S("#22252b", "")],
  ].map(([id, name, svg]) => ({ id, name, svg, ...(id === "graph" ? { line: `<rect width="1600" height="1000" fill="#fff"/><path d="${gridLines(40)}" stroke="#dde3ea" stroke-width="2" fill="none"/>` } : {}) }));

  // How the pieces are found: a group within their drawer, words to search by, and the stories
  // they belong to. With hundreds of pieces, these keep any one easy to find.
  const SUBS = {
    people: [["ot", "Old Testament"], ["nt", "New Testament"], ["everyday", "Everyday people"], ["heaven", "Angels"]],
    animals: [["farm", "Farm animals"], ["wild", "Wild animals"], ["birds", "Birds"], ["water", "Fish and sea"]],
    things: [["home", "Home and town"], ["boats", "Boats"], ["worship", "Worship"], ["royal", "Kings and battles"], ["writing", "Writing"]],
    nature: [["plants", "Plants"], ["land", "Land and water"], ["sky", "Sky"]],
  };
  const META = {
    jesus: ["nt", "Christ Lord Messiah Son of God teacher"], mary: ["nt", "mother of Jesus"], joseph: ["nt", "carpenter husband of Mary"],
    man: ["everyday", "person adult crowd"], woman: ["everyday", "person adult crowd"], "old-man": ["everyday", "elder grandfather"],
    "old-woman": ["everyday", "elder grandmother widow"], boy: ["everyday", "child kid son"], girl: ["everyday", "child kid daughter"],
    shepherd: ["everyday", "flock sheep keeper"], "shepherd-boy": ["everyday", "child flock"], king: ["everyday", "ruler royal Saul Solomon Herod pharaoh"],
    queen: ["everyday", "royal Esther Sheba"], soldier: ["everyday", "army guard Roman warrior centurion"], angel: ["heaven", "Gabriel messenger"],
    priest: ["everyday", "Aaron temple high priest Levite"], "wise-man": ["nt", "magi king gift"], fisherman: ["nt", "disciple Andrew James John"],
    teacher: ["everyday", "rabbi scribe scroll"], adam: ["ot", "first man"], eve: ["ot", "first woman"], noah: ["ot", "ark flood"],
    abraham: ["ot", "Abram father patriarch"], sarah: ["ot", "Sarai wife"], moses: ["ot", "lawgiver prophet Exodus"], david: ["ot", "shepherd king boy"],
    goliath: ["ot", "giant Philistine"], daniel: ["ot", "prophet lions"], peter: ["nt", "Simon disciple apostle fisherman"], paul: ["nt", "Saul apostle missionary"],
    zacchaeus: ["nt", "tax collector short"], pharisee: ["nt", "religious leader scribe"], baby: ["nt", "infant Jesus newborn"],
    sheep: ["farm", "flock lamb wool ewe"], lamb: ["farm", "sheep young"], donkey: ["farm", "ass colt"], camel: ["farm", "desert caravan"], lion: ["wild", "den"],
    ox: ["farm", "cow cattle bull calf"], dove: ["birds", "Holy Spirit peace bird"], fish: ["water", "catch"], "great-fish": ["water", "whale Jonah big fish"],
    snake: ["wild", "serpent devil"], raven: ["birds", "bird black"], goat: ["farm", "kid scapegoat"],
    ark: ["boats", "flood boat"], boat: ["boats", "sail fishing"], tent: ["home", "tabernacle camp"], house: ["home", "home town"], wall: ["home", "Jericho gate city"],
    well: ["home", "water Samaritan"], jar: ["home", "water pot jug"], bread: ["home", "five loaves two fish feeding"], tablets: ["worship", "ten commandments law stone"],
    staff: ["home", "rod shepherd"], crown: ["royal", "king queen"], lamp: ["home", "light oil parable"], manger: ["home", "stable hay"], cross: ["worship", "crucifixion Calvary"],
    tomb: ["worship", "grave resurrection stone"], scroll: ["writing", "book Scripture law"], sling: ["royal", "stones David weapon"], throne: ["royal", "seat king"],
    altar: ["worship", "sacrifice offering fire"], tree: ["plants", "oak"], "fruit-tree": ["plants", "apple fig fruit"], palm: ["plants", "palm branches"],
    bush: ["plants", "burning bush fire"], rock: ["land", "stone"], hill: ["land", "hill mount"], mountain: ["land", "mount Sinai"], water: ["land", "river sea lake"],
    sun: ["sky", "day light"], moon: ["sky", "night"], star: ["sky", "Bethlehem night"], cloud: ["sky", "pillar"], rainbow: ["sky", "promise flood"], grass: ["plants", "field"],
    flowers: ["plants", "lilies field"],
  };
  const STORIES = [
    ["creation", "Creation", "Genesis 1–2", "adam eve tree fruit-tree sun moon star cloud water flowers grass fish dove sheep lion", "garden"],
    ["fall", "The garden and the serpent", "Genesis 3", "adam eve snake fruit-tree tree angel", "garden"],
    ["noah", "Noah and the flood", "Genesis 6–9", "noah ark dove raven rainbow cloud water sheep ox camel lion goat donkey", "sea hills"],
    ["abraham", "Abraham and Sarah", "Genesis 12–22", "abraham sarah tent star camel sheep goat altar", "desert night"],
    ["moses", "Moses and the Exodus", "Exodus 3–20", "moses bush staff tablets mountain water priest sheep", "desert sea"],
    ["david", "David and Goliath", "1 Samuel 17", "david goliath sling soldier king shepherd-boy sheep", "hills"],
    ["daniel", "Daniel and the lions", "Daniel 6", "daniel lion king soldier", "indoors"],
    ["jonah", "Jonah", "Jonah 1–4", "great-fish boat man cloud water", "sea"],
    ["nativity", "The birth of Jesus", "Luke 2; Matthew 2", "baby mary joseph angel shepherd sheep donkey ox manger star wise-man camel", "night town"],
    ["ministry", "Jesus' ministry", "The Gospels", "jesus peter fisherman boat fish bread zacchaeus tree pharisee man woman boy girl", "sea hills town"],
    ["resurrection", "Jesus' death and resurrection", "The Gospels", "jesus cross tomb soldier mary angel rock", "hills garden"],
    ["church", "The early church", "Acts", "peter paul scroll house man woman", "town"],
  ].map(([id, name, ref, pieces, scenes]) => ({ id, name, ref, pieces: pieces.split(" "), scenes: scenes.split(" ") }));
  for (const p of [...people, ...animals, ...things, ...nature]) {
    const m = META[p.id] || [];
    p.sub = m[0] || ""; p.tags = m[1] || "";
    p.stories = STORIES.filter(st => st.pieces.includes(p.id)).map(st => st.id);
  }

  window.SB_ART = {
    subs: SUBS, stories: STORIES,
    pieces: [...people, ...animals, ...things, ...nature],
    scenes,
    cats: [["recent", "Recent"], ["stories", "Stories"], ["people", "People"], ["animals", "Animals"], ["things", "Things"], ["nature", "Nature"], ["scenes", "Scenes"]],
  };
})();
