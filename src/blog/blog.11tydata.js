import { isLive } from "../../lib/publish.js";

export default {
  layout: "layouts/post.njk",
  // Drafts and posts dated in the future are not written to the site until they go live (see lib/publish.js).
  permalink: (data) => (isLive(data) ? `/blog/${data.page.fileSlug}/` : false),
};
