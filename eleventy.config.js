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
          id = inline.content.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
        }
        toks[i].attrSet("id", id);
      }
    });
  });
  eleventyConfig.addPassthroughCopy({ "src/.nojekyll": ".nojekyll" });

  eleventyConfig.addCollection("posts", (api) =>
    api.getFilteredByGlob("src/blog/*.md").filter((p) => !p.data.draft).reverse()
  );

  const months = ["January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December"];
  eleventyConfig.addFilter("longDate", (d) =>
    `${d.getUTCDate()} ${months[d.getUTCMonth()]} ${d.getUTCFullYear()}`);
  eleventyConfig.addFilter("isoDate", (d) => d.toISOString());
  eleventyConfig.addFilter("head", (arr, n) => arr.slice(0, n));
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
