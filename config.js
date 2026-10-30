// Settings for this copy of the site.
//
// Accounts (an optional sign-in that keeps highlights and notes the same on every device) stay
// off until a Supabase project is set up for them: see DEPLOY.md, "Accounts". Then put the
// project's address and its publishable (anon) key here. The key is meant to be public: the
// database's own rules (supabase/schema.sql) keep each person's notes to themselves.
window.SITE_CONFIG = {
  supabase: {
    url: "https://uqxubaiazcjemwvskzoo.supabase.co",   // the "Plain Bible" project
    key: "sb_publishable_yatPH_LbBSWflCRESEjIIQ_q1H7gJqM",   // its publishable key: public by design
  },
  // Where people can write about their data, shown on privacy.html. Needed before accounts go on.
  contact: "privacy@bibledata.org",   // a Porkbun email forward to the owner's inbox
  // Where readers send questions and suggestions: the "Send feedback" buttons.
  feedback: "info@bibledata.org",
  // A page where people can support the project financially (a donation page). Leave empty to
  // hide the "Support this project" section.
  support: "",
};
