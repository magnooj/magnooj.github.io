# magnooj.github.io

Personal site and blog of Ali Ganjizadeh, MD, MBA: https://magnooj.github.io

Built with [Eleventy](https://www.11ty.dev/). `main` holds the source; the built site is published to the `gh-pages` branch, which GitHub Pages serves.

## Write a new post

1. Add a Markdown file to `src/blog/`, for example `src/blog/what-a-benchmark-cant-tell-you.md`. The file name becomes the URL.
2. Start it with front matter:

   ```yaml
   ---
   title: What a benchmark can't tell you
   description: One sentence that appears in the post list and in link previews.
   date: 2026-11-15
   kicker: Essay
   ogImage: /assets/img/blog/your-post/og.png   # optional, 1200 x 627
   disclosure: I work at HOPPR, which builds AI for medical imaging. The views are my own.
   draft: true                                  # optional; drafts are not published
   ---
   ```

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
