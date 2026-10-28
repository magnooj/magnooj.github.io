# magnooj.github.io

Personal site and blog of Ali Ganjizadeh, MD, MBA: https://magnooj.github.io

Built with [Eleventy](https://www.11ty.dev/). `main` holds the source; the built site is published to the `gh-pages` branch, which GitHub Pages serves.

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
   draft: true                           # optional; drafts are not published
   ---
   ```

   Wrap each part in `<section id="...">` with a blank line after the opening tag and before `</section>`, and write the heading as `## <span class="n">01</span>Title`. Stat tiles, the TL;DR box, callouts and the figure styles (`hbars`, `flow`, `sysmap`, `insert`, `table.data`) are plain HTML classes from `src/assets/css/site.css`.

3. Put images in `src/assets/img/blog/<post>/` and use them with `<figure><img src="..." alt="..."><figcaption>...</figcaption></figure>`.
4. Run `npm run deploy` to build and publish (it needs the GitHub CLI, `gh`, logged in). Commit and push `main` too, so the source stays in sync.

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
