"""Render the "Clinical foundations of medical AI" series graphics.

Usage: python3 graphics/series.py [--linkedin-dir DIR]

LinkedIn cards (1080x1350, saved at 2x) go to --linkedin-dir (default
graphics/out/linkedin/series, not committed). Each post's Open Graph image
(1200x627) goes to src/assets/img/blog/<slug>/og.png. The cards themselves
are not published on the site: the posts draw their figures in HTML.
Card text lives in series_cards.py.
"""
import argparse
import pathlib
import tempfile

from PIL import Image

from render import OUT, ROOT, downscale, overflow, page, shot
from series_cards import CARDS, OG


def og_html(slug):
    part, title, sub, mini = OG[slug]
    return (
        '<section class="og"><div class="ogwrap"><div class="left">'
        '<p class="kicker"><span class="part">PART ' + str(part) + '</span>Clinical foundations of medical AI</p>'
        '<h1>' + title + '</h1><p class="sub">' + sub + '</p></div>'
        '<div class="mini mini-' + str(part) + '"><div>' + mini + '</div></div></div>'
        '<div class="ogfoot"><span class="who"><span class="mark">AG</span>Ali Ganjizadeh, MD, MBA</span>'
        '<span class="url">magnooj.github.io</span></div></section>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--linkedin-dir", default=str(OUT / "linkedin" / "series"))
    a = ap.parse_args()
    li = pathlib.Path(a.linkedin_dir)
    html_dir = OUT / "html" / "series"
    for d in (html_dir, li):
        d.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as profile:
        for name, body in CARDS.items():
            path = html_dir / f"{name}.html"
            path.write_text(page(body, 1080, 1350))
            shot(path, li / f"{name}.png", 1080, 1350, profile)
            print("rendered", name, Image.open(li / f"{name}.png").size)
        # Overflow check: every card must fit its 1080x1350 frame, and every OG image its 1200x627 frame
        # with the scaled figure inside its panel.
        allc = html_dir / "all.html"
        allc.write_text(page("".join(CARDS.values()), 1080, 1350))
        problems = overflow(allc, list(CARDS), 1080, 1350, profile)
        allog = html_dir / "og-all.html"
        allog.write_text(page("".join(og_html(slug) for slug in OG), 1200, 627))
        problems += overflow(allog, [f"og {slug}" for slug in OG], 1200, 627, profile)
        for p in problems:
            print("WARNING: overflow in", p)
        if not problems:
            print("overflow check: all cards and Open Graph images fit")
        for slug in OG:
            path = html_dir / f"og-{slug}.html"
            path.write_text(page(og_html(slug), 1200, 627))
            big = OUT / f"og-{slug}@2x.png"
            shot(path, big, 1200, 627, profile)
            dst = ROOT / "src/assets/img/blog" / slug / "og.png"
            dst.parent.mkdir(parents=True, exist_ok=True)
            downscale(big, dst, 1200, 627)
            print("rendered og", slug, Image.open(dst).size)


if __name__ == "__main__":
    main()
