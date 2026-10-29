// Settings for this copy of the site.
//
// Accounts (an optional sign-in that keeps highlights and notes the same on every device) stay
// off until a Supabase project is set up for them: see DEPLOY.md, "Accounts". Then put the
// project's address and its publishable (anon) key here. The key is meant to be public: the
// database's own rules (supabase/schema.sql) keep each person's notes to themselves.
window.SITE_CONFIG = {
  supabase: {
    url: "",   // for example "https://abcdefghijklmnop.supabase.co"
    key: "",   // the project's publishable key ("sb_publishable_…") or legacy anon key
  },
  // Where people can write about their data, shown on privacy.html. Needed before accounts go on.
  contact: "",   // for example "privacy@example.org"
};
