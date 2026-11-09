# magnooj.github.io

Personal site and blog of Ali Ganjizadeh, MD, MBA: https://magnooj.github.io

Built with [Eleventy](https://www.11ty.dev/). `main` holds the source. GitHub Actions (`.github/workflows/deploy.yml`) builds it and publishes it to GitHub Pages on every push to `main` and every morning, so scheduled posts go live on their date.

## Write a new post

1. Add a Markdown file to `src/blog/`, for example `src/blog/what-a-benchmark-cant-tell-you.md`. The file name becomes the URL.
2. Start it with front matter (see `src/blog/the-model-is-not-the-hard-part.md` for a full example):

   ```yaml
   ---
   title: What a benchmark can't tell you
   description: One sentence for search results and link previews.
   dek: The longer standfirst under the title.
   summary: Two sentences for the post card on the home and Writing pages.
   date: 2026-11-15
   topic: Evaluating medical AI          # small caps line on the post card
   labels: ["Evaluation"]                # tag pills; the Writing page filters on them
   ogImage: /assets/img/blog/your-post/og.png   # 1200 x 627; also the post card thumbnail
   disclosure: I work at HOPPR, which builds AI for medical imaging. The views are my own.
   toc:                                  # optional left-hand contents; ids match <section id="...">
     - { id: "intro", n: "01", label: "Introduction" }
   draft: true                           # optional; drafts are never published
   ---
   ```

   Wrap each part in `<section id="...">` with a blank line after the opening tag and before `</section>`, and write the heading as `## <span class="n">01</span>Title`. Stat tiles, the TL;DR box, callouts and the figure styles (`hbars`, `flow`, `sysmap`, `insert`, `table.data`) are plain HTML classes from `src/assets/css/site.css`.

3. Put images in `src/assets/img/blog/<post>/` and use them with `<figure><img src="..." alt="..."><figcaption>...</figcaption></figure>`.
4. Commit and push to `main`. GitHub Actions publishes the site in about two minutes.

## Schedule a post

A post goes live at 05:00 UTC (midnight New York time in winter) on its `date`. GitHub often starts scheduled builds hours late, so the workflow runs four times each morning and a post is usually up by 7 am New York time. Give it a future `date`, remove `draft: true`, then commit and push: it stays hidden until that day, when the first morning build publishes it. Until then, links to it from other posts show as plain text, and the series box lists it as "coming 17 November".

- `npm run preview` shows drafts and scheduled posts at http://localhost:8090, for review only.
- `NOW=2026-11-17T12:00Z npm run build` builds the site as it will look at that time.
- `npm run deploy` starts the publish workflow by hand (needs the GitHub CLI, `gh`), for example if a scheduled run is late. It publishes what is on `main`.

Note that the source of a scheduled post is readable in this public repository before it goes live. Keep unapproved drafts out of `main`.

## Run it locally

```sh
npm install
npm start          # http://localhost:8080, reloads on save
```

## Graphics

`graphics/render.py` draws the post's figures with headless Chrome and writes the blog images (1080 x 1350) and Open Graph images (1200 x 627) into `src/assets/img/`. It needs Google Chrome and Pillow:

```sh
python3 graphics/render.py --linkedin-dir ~/Desktop/linkedin   # also writes 2x LinkedIn images and a carousel PDF
```

The card text lives in `graphics/render.py` and the styles in `graphics/cards.css`.
