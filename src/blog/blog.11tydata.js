export default {
  layout: "layouts/post.njk",
  // Drafts (draft: true) are not written to the site.
  permalink: (data) => (data.draft ? false : `/blog/${data.page.fileSlug}/`),
};
