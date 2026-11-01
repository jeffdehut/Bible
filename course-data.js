// The Complete Bible Story: its twelve parts, with the colors and hand-drawn icons of the
// outline, and the quarter each is taught in (the Son has two). The lessons themselves are in
// data/course/qNN.json (scripts/course_check.py checks them); course.html lists them, and
// lesson.html shows one.
window.COURSE = {
  sections: {
    plan:       { c: "#ec3024", ink: "#c41f15", en: "God Has a Plan: To Unify All Things in Christ", zh: "神有一個計劃：使萬有在基督裏同歸於一" },
    patriarchs: { c: "#f4901c", ink: "#b95f00", en: "God Calls the Patriarchs", zh: "神呼召列祖" },
    multiplies: { c: "#f0c828", ink: "#8a6a00", en: "God Multiplies His People", zh: "神使他的子民增多" },
    leads:      { c: "#98c838", ink: "#4f7a10", en: "God Leads His People", zh: "神帶領他的子民" },
    judges:     { c: "#68c080", ink: "#2f7d45", en: "God Provides Judges", zh: "神賜下士師" },
    kings:      { c: "#68ccdc", ink: "#1f7f8f", en: "God Anoints Kings", zh: "神膏立君王" },
    repent:     { c: "#448cc8", ink: "#2a6aa6", en: "God Calls His People to Repent", zh: "神呼喚他的子民悔改" },
    exile:      { c: "#3c58a4", ink: "#334b8f", en: "God Exiles His People", zh: "神使他的子民被擄" },
    home:       { c: "#7454a4", ink: "#634690", en: "God Brings His People Home", zh: "神領他的子民歸回" },
    son:        { c: "#bc60a4", ink: "#9a4585", en: "God Sends His Son", zh: "神差遣他的兒子" },
    church:     { c: "#ec3090", ink: "#c41a72", en: "Christ Establishes the Church", zh: "基督建立教會" },
    unifies:    { c: "#000000", ink: "#2a2a2a", en: "God Unifies All Things in Christ", zh: "神使萬有在基督裏同歸於一" },
  },
  order: ["plan", "patriarchs", "multiplies", "leads", "judges", "kings", "repent", "exile", "home", "son", "church", "unifies"],
  quarters: ["plan", "patriarchs", "multiplies", "leads", "judges", "kings", "repent", "exile", "home", "son", "son", "church"],
  // The last quarter closes with the last part of the story.
  lessonSection: (q, n) => (q === 12 && n >= 11 ? "unifies" : null),
  years: [
    { en: "Year one", zh: "第一年", span: { en: "Genesis to Joshua", zh: "創世記到約書亞記" } },
    { en: "Year two", zh: "第二年", span: { en: "Judges to the exile", zh: "士師記到被擄" } },
    { en: "Year three", zh: "第三年", span: { en: "The return, the Gospels and the church", zh: "歸回、福音書和教會" } },
  ],
  icon: id => "icons/story/" + String(window.COURSE.order.indexOf(id) + 1).padStart(2, "0") + "-" + id + ".png",
  zh: () => !!(window.I18N && /^zh/.test(window.I18N.lang || "")),
};
