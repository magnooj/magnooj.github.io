import { isLive, now, publishAt, showDrafts } from "./lib/publish.js";

export default function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });
  eleventyConfig.amendLibrary("md", (md) => {
    md.set({ typographer: true });
    // Heading anchors: "## Title {#id}" sets the id; other headings get a slug.
    md.core.ruler.push("heading_ids", (state) => {
      const toks = state.tokens;
      for (let i = 0; i < toks.length - 1; i++) {
        if (toks[i].type !== "heading_open") continue;
        const inline = toks[i + 1];
        const m = inline.content.match(/\s*\{#([\w-]+)\}\s*$/);
        let id;
        if (m) {
          id = m[1];
          inline.content = inline.content.slice(0, m.index);
          const last = inline.children[inline.children.length - 1];
          last.content = last.content.replace(/\s*\{#[\w-]+\}\s*$/, "");
        } else {
          id = inline.content.replace(/<[^>]+>/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
        }
        toks[i].attrSet("id", id);
      }
    });
  });
  eleventyConfig.addPassthroughCopy({ "src/.nojekyll": ".nojekyll" });

  // Only live posts are listed (see lib/publish.js). DRAFTS=1 (npm run preview) lists drafts and
  // scheduled posts too, for review; deploys never do.
  const live = new Set(); // slugs of live posts
  const scheduled = new Map(); // slug -> date, for approved posts that go live later
  eleventyConfig.addCollection("posts", (api) => {
    const all = api.getFilteredByGlob("src/blog/*.md");
    live.clear();
    scheduled.clear();
    for (const p of all) {
      if (isLive(p.data)) live.add(p.page.fileSlug);
      else if (!p.data.draft) scheduled.set(p.page.fileSlug, p.date);
    }
    return all.filter((p) => live.has(p.page.fileSlug)).reverse();
  });
  // Posts in a series, in reading order (part 0 is the overview). Scheduled parts are included
  // without a link, so readers see what comes next; drafts are left out.
  eleventyConfig.addCollection("series", (api) =>
    api.getFilteredByGlob("src/blog/*.md")
      .filter((p) => p.data.series && (showDrafts || !p.data.draft))
      .sort((a, b) => a.data.part - b.data.part)
  );
  eleventyConfig.addFilter("seriesNext", (items, url) => {
    const i = items.findIndex((p) => p.url === url);
    return i < 0 ? null : items[i + 1] || null;
  });
  // A link to a post that is not live yet becomes plain text until the post goes live,
  // so a post can mention later parts without sending readers to a missing page.
  eleventyConfig.addTransform("pending-links", function (content) {
    if (!this.page.outputPath || !this.page.outputPath.endsWith(".html")) return content;
    return content.replace(/<a href="\/blog\/([a-z0-9-]+)\/[^"]*"[^>]*>([\s\S]*?)<\/a>/g, (m, slug, text) => {
      if (live.has(slug)) return m;
      const when = scheduled.has(slug) ? `Coming ${dayMonth(scheduled.get(slug))}` : "Coming soon";
      return `<span class="pending-link" title="${when}">${text}</span>`;
    });
  });

  const months = ["January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December"];
  const dayMonth = (d) => `${d.getUTCDate()} ${months[d.getUTCMonth()]}`;
  eleventyConfig.addFilter("dayMonth", dayMonth);
  // "10 November" while a post is scheduled for later, "" once it is live.
  eleventyConfig.addFilter("goesLive", (d) => (publishAt(d) > now ? dayMonth(d) : ""));
  eleventyConfig.addFilter("longDate", (d) =>
    `${d.getUTCDate()} ${months[d.getUTCMonth()]} ${d.getUTCFullYear()}`);
  eleventyConfig.addFilter("isoDate", (d) => d.toISOString());
  const mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  eleventyConfig.addFilter("shortDate", (d) => `${d.getUTCDate()} ${mon[d.getUTCMonth()]} ${d.getUTCFullYear()}`);
  eleventyConfig.addFilter("head", (arr, n) => arr.slice(0, n));
  eleventyConfig.addFilter("allLabels", (posts) => {
    const counts = new Map();
    for (const p of posts) for (const l of p.data.labels || []) counts.set(l, (counts.get(l) || 0) + 1);
    return [...counts].map(([name, count]) => ({ name, count }));
  });
  eleventyConfig.addShortcode("year", () => String(new Date().getFullYear()));
  eleventyConfig.addFilter("absoluteUrl", (path, base) => new URL(path, base).href);
  eleventyConfig.addFilter("readingTime", (html) => {
    const words = String(html).replace(/<[^>]+>/g, " ").split(/\s+/).filter(Boolean).length;
    return `${Math.max(1, Math.round(words / 230))} min read`;
  });

  return {
    dir: { input: "src", includes: "_includes", data: "_data", output: "_site" },
    markdownTemplateEngine: false,
    htmlTemplateEngine: "njk",
  };
}
