// When a blog post goes live.
// A post is live once it is not a draft (no `draft: true`) and its publish time has passed.
// Publish time is 11:00 UTC on the post's `date`: 6 am New York time in winter, 7 am in summer.
// The site rebuilds every morning (.github/workflows/deploy.yml), so a scheduled post appears on its date by itself.
//   DRAFTS=1  shows drafts and scheduled posts (npm run preview, for review only).
//   NOW=...   pretends the build runs at another time, e.g. NOW=2026-11-17T12:00Z npm run build.
export const showDrafts = process.env.DRAFTS === "1";
export const now = process.env.NOW ? new Date(process.env.NOW) : new Date();

export function publishAt(date) {
  const d = new Date(date);
  d.setUTCHours(11, 0, 0, 0);
  return d;
}

export function isLive(data) {
  if (showDrafts) return true;
  return !data.draft && publishAt(data.page.date) <= now;
}
