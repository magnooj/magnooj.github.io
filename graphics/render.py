"""Render the blog graphics, LinkedIn images, carousel PDF and Open Graph images.

Usage: python3 graphics/render.py [--linkedin-dir DIR]

Needs Google Chrome and Pillow. Blog images (1080x1350) and Open Graph images
(1200x627) are written into src/assets/img/. The 2x LinkedIn images and the
carousel PDF go to --linkedin-dir (default graphics/out/linkedin, not committed).
"""
import argparse
import pathlib
import re
import subprocess
import tempfile

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
GFX = ROOT / "graphics"
OUT = GFX / "out"
BLOG_IMG = ROOT / "src/assets/img/blog/model-not-hard-part"
SITE_IMG = ROOT / "src/assets/img"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">'


def foot(right="magnooj.github.io", swipe=False):
    r = '<span class="swipe">Swipe →</span>' if swipe else f'<span class="url">{right}</span>'
    return f'<div class="foot"><span class="who"><span class="mark">AG</span>Ali Ganjizadeh, MD, MBA</span>{r}</div>'


def card(kicker, title, fig, source="", sub="", title_cls="", swipe=False):
    sub_html = f'<p class="sub">{sub}</p>' if sub else ""
    src_html = f'<p class="source">{source}</p>' if source else ""
    return (f'<section class="card"><p class="kicker">{kicker}</p><h1 class="{title_cls}">{title}</h1>{sub_html}'
            f'<div class="fig">{fig}</div>{src_html}{foot(swipe=swipe)}</section>')


def pill(n):
    return f'<span class="num">{n}</span>'


PILLARS = [
    ("Data provenance", "Where did the data come from?"),
    ("Label definition", "What exactly does it predict?"),
    ("Evaluation", "What evidence beyond accuracy?"),
    ("After go-live", "Who watches it once it’s in use?"),
]

CARDS = {}

CARDS["00-cover"] = card(
    "Talk notes · MedAI Summit 2026",
    "The model is not the hard part.",
    '<div class="pillars">' + "".join(
        f'<div class="pillar">{pill(i)}<div>{name}<small>{q}</small></div></div>'
        for i, (name, q) in enumerate(PILLARS, 1)) + "</div>",
    sub="Four questions for any medical AI tool, and why they’re clinical questions.",
    title_cls="xl", swipe=True)

CARDS["01-small-box"] = card(
    "The big idea",
    "The model is the small box.",
    '<div class="sys">'
    '<div class="box edge" style="left:0;top:0;width:440px;height:200px"><div>Data provenance<span>Why the image exists</span></div></div>'
    '<div class="box ops" style="left:460px;top:0;width:444px;height:95px">Data pipelines</div>'
    '<div class="box ops" style="left:460px;top:105px;width:444px;height:95px">Infrastructure</div>'
    '<div class="box edge" style="left:0;top:220px;width:300px;height:200px"><div>Label definition<span>Which outcome matters</span></div></div>'
    '<div class="box model" style="left:322px;top:290px;width:108px;height:58px">Model</div>'
    '<div class="box ops" style="left:452px;top:220px;width:452px;height:95px">Integration</div>'
    '<div class="box ops" style="left:452px;top:325px;width:452px;height:95px">Monitoring</div>'
    '<div class="box edge" style="left:0;top:440px;width:560px;height:200px"><div>Evaluation<span>What a PPV means at the bedside</span></div></div>'
    '<div class="box ops" style="left:580px;top:440px;width:324px;height:200px">Governance</div>'
    '</div>'
    '<div class="legend"><span><i style="background:var(--accent)"></i>Where a physician has the edge</span>'
    '<span><i style="background:var(--ink)"></i>The algorithm</span></div>',
    sub="Three of the big boxes are where a physician has the edge over a computer-science graduate.",
    source="After Sculley D et al. Hidden technical debt in machine learning systems. NeurIPS 2015. Clinical labels are mine.")

CARDS["02-ink"] = card(
    f"{pill(1)} Data provenance",
    "The AI learned the surgeon’s worry, not the disease.",
    '<div class="bars">'
    '<div><p class="bar-label">Specificity on the same benign moles</p>'
    '<div class="bar-row"><div class="bar ink" style="width:588px"></div><span class="bar-val">84%</span></div>'
    '<p class="axis-note">Unmarked</p></div>'
    '<div><div class="bar-row"><div class="bar acc" style="width:322px"></div><span class="bar-val acc">46%</span></div>'
    '<p class="axis-note">Marked with surgical ink</p></div>'
    '</div>'
    '<div class="callbox">False alarms more than tripled, from 16% to 54%, and the heat maps lit up on the ink. <b>Surgeons mark the lesions that worry them.</b></div>',
    sub="A commercial melanoma AI saw the same benign moles twice: clean, and marked with surgical ink.",
    source="Winkler JK et al. JAMA Dermatol 2019;155:1135-41. 130 lesions: 107 benign moles, 23 melanomas.")

CARDS["03-cost"] = card(
    f"{pill(2)} Label definition",
    "Accurate at predicting cost. Wrong question.",
    '<div class="flow">'
    '<div class="step"><p class="tag">The goal</p><p>Find patients who need extra care</p></div>'
    '<div class="step bad"><p class="tag">What it predicted</p><p>Next year’s healthcare cost</p></div>'
    '<div class="step"><p class="tag">The result</p><p>At the same risk score, Black patients were considerably sicker</p></div>'
    '</div>'
    '<div class="bigstat"><span class="from">17.7%</span><span class="arr">→</span><span class="to">46.5%</span></div>'
    '<p class="statnote">Black patients’ share of the extra help if the bias were removed (authors’ estimate)</p>'
    '<div class="callbox">Changing only the label, to a mix of health and cost, cut one measure of the bias by <b>84%</b>.</div>',
    source="Obermeyer Z, Powers B, Vogeli C, Mullainathan S. Science 2019;366:447-53. A commercial algorithm used by US health systems.")

CARDS["04-ppv"] = card(
    f"{pill(3)} Evaluation",
    "Five of every six alerts are false.",
    '<div class="alerts">' + '<div class="alert t">true</div>' + '<div class="alert f">false</div>' * 5 + '</div>'
    '<table class="tbl"><tr><th>10,000 inpatients</th><th>AI flags</th><th>AI is quiet</th></tr>'
    '<tr><td><b>100</b><span>have the reaction</span></td><td><b>95</b><span>true alerts</span></td><td><b>5</b><span>missed</span></td></tr>'
    '<tr><td><b>9,900</b><span>don’t</span></td><td class="acc"><b>495</b><span>false alarms</span></td><td><b>9,405</b><span>correctly quiet</span></td></tr></table>'
    '<div class="ppv"><span class="eq">95 ÷ (95 + 495) =</span><span class="res">≈ 16%</span></div>'
    '<p class="ward">On a ward where 1 in 10 react, the same tool gives ≈ 68%. Same tool, different value.</p>',
    sub="An AI that is 95% sensitive and 95% specific flags inpatients at risk of a drug reaction that 1 in 100 will have.",
    source="Worked example: positive predictive value at 1% prevalence.")

CARDS["05-drift"] = card(
    f"{pill(4)} After go-live",
    "Same code. Different patients.",
    '<div class="bars">'
    '<div><p class="bar-label">Hospitalized patients triggering a sepsis alert each day</p>'
    '<div class="bar-row"><div class="bar ink" style="width:257px"></div><span class="bar-val">9%</span></div>'
    '<p class="axis-note">3 weeks before each hospital’s first COVID-19 case</p></div>'
    '<div><div class="bar-row"><div class="bar acc" style="width:600px"></div><span class="bar-val acc">21%</span></div>'
    '<p class="axis-note">3 weeks after</p></div>'
    '</div>'
    '<div class="callbox">Michigan paused its sepsis alerts. Nothing in the code changed; the patients did. <b>That’s why drugs have Phase&nbsp;IV.</b></div>',
    sub="The Epic Sepsis Model across 24 US hospitals, as COVID-19 arrived.",
    source="Wong A et al. JAMA Netw Open 2021;4:e2135286. The study measured alert volume, not accuracy.")

CARDS["06-package-insert"] = card(
    f"{pill(4)} After go-live",
    "Every model needs a package insert.",
    '<div class="insert">'
    '<div class="drug"><h3>Drug insert</h3><ul>'
    '<li>Indications and usage</li><li>Dosage</li><li>Contraindications</li><li class="w">Warnings</li>'
    '<li>Clinical studies</li><li>Post-marketing experience</li></ul></div>'
    '<div class="facts"><h3>Model Facts</h3><p class="mname">Deep Sepsis · Duke University Hospital · v1.0</p>'
    '<div class="row"><b>Summary</b>Probability of meeting sepsis criteria in the next 4 hours, from EHR data</div>'
    '<div class="row"><b>For whom, when</b>Adults in the emergency department; a new score every hour</div>'
    '<div class="row"><b>Validation</b>Past Duke data: AUC 0.88 · later Duke data: 0.94 · live use: <span class="tbd">TBD</span> · other hospitals: <span class="tbd">TBD</span></div>'
    '<div class="row warn"><b>Warnings</b>Without further evaluation, do not use in the ICU, after a first sepsis episode, or at other hospitals · Not a diagnosis</div>'
    '</div></div>',
    source="Adapted from Sendak MP, Gao M, Brajer N, Balu S. npj Digit Med 2020;3:41, Fig. 1 (CC BY 4.0).")

QUESTIONS = [
    ("Data provenance", "Where did the data come from, and do those patients look like mine?", "Like a drug’s ingredients and trial population"),
    ("Label definition", "What exactly does it predict, and who acts on it, when?", "Like a drug’s indication and endpoint"),
    ("Evaluation", "What evidence is there beyond accuracy, at my prevalence?", "Like a drug’s trial phases"),
    ("After go-live", "Who watches it once it’s in use?", "Like a package insert and pharmacovigilance"),
]
CARDS["07-four-questions"] = card(
    "Take-home",
    "Four questions for any medical AI tool",
    '<div class="qs">' + "".join(
        f'<div class="q">{pill(i)}<div><p class="name">{n}</p><p>{q}</p><small>{a}</small></div></div>'
        for i, (n, q, a) in enumerate(QUESTIONS, 1)) + '</div>'
    '<p class="closing">None of them is about the model. <span>They’re clinical questions.</span></p>',
    source="One-page checklist and reading list: magnooj.github.io/medai-summit-2026")

def ppv(p, sens=0.95, spec=0.95):
    return sens * p / (sens * p + (1 - spec) * (1 - p))


OG_ROWS = "".join(
    f'<div class="r{" hot" if p == 0.01 else ""}"><span>{label}</span><div class="tr"><div style="width:{ppv(p) * 100:.1f}%"></div></div>'
    f'<span class="v">{ppv(p) * 100:.0f}%</span></div>'
    for p, label in ((0.01, "1 in 100"), (0.05, "1 in 20"), (0.10, "1 in 10"), (0.30, "3 in 10")))

OG_POST = (
    '<section class="og"><p class="kicker">Writing · Evaluating medical AI</p>'
    '<div class="ogwrap"><div class="left"><h1>The model is not the hard part</h1>'
    '<p class="sub">Four questions for any medical AI tool, and why answering them takes clinical training more than code.</p></div>'
    '<div class="ogchart"><p class="ct">How often an alert is right</p>'
    '<p class="cs">95% sensitive, 95% specific tool, by how many patients have the condition</p>'
    f'{OG_ROWS}</div></div>'
    '<div class="ogfoot"><span class="who"><span class="mark">AG</span>Ali Ganjizadeh, MD, MBA</span><span class="url">magnooj.github.io</span></div></section>')

OG_DEFAULT = (
    '<section class="og"><div class="ogwrap" style="grid-template-columns:1fr 150px"><div class="left">'
    '<p class="kicker">Physician-scientist · Medical imaging AI</p>'
    '<h1>Ali Ganjizadeh</h1>'
    '<p class="sub">I work on the data, labels and evaluation that decide whether a medical AI model can be trusted.</p></div>'
    f'<img class="photo" src="{(ROOT / "src/assets/img/ali.jpg").as_uri()}" alt=""></div>'
    '<div class="ogfoot"><span class="who"><span class="mark">AG</span>magnooj.github.io</span><span class="url">MD, MBA · LinkedIn · X @magnooj</span></div></section>')


def page(body, w, h):
    css = (GFX / "cards.css").read_text()
    check = ("<script>document.fonts.ready.then(() => document.querySelectorAll('.card').forEach((c, i) => {"
             "if (c.scrollHeight > c.clientHeight + 1) document.body.insertAdjacentHTML('beforeend',"
             "`<i data-overflow='${i}:${c.scrollHeight - c.clientHeight}px'></i>`); }));</script>")
    return (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{css}'
            f'@page {{ size: {w}px {h}px; margin: 0; }} html, body {{ width: {w}px; }}</style></head><body>{body}{check}</body></html>')


def chrome(args, profile):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                    "--virtual-time-budget=10000", f"--user-data-dir={profile}", *args],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def shot(html_path, png_path, w, h, profile):
    chrome([f"--window-size={w},{h}", "--force-device-scale-factor=2", f"--screenshot={png_path}",
            html_path.as_uri()], profile)


def downscale(src, dst, w, h):
    im = Image.open(src).convert("RGB")
    im = im.resize((w, h), Image.LANCZOS)
    im.save(dst, optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--linkedin-dir", default=str(OUT / "linkedin"))
    a = ap.parse_args()
    li = pathlib.Path(a.linkedin_dir)
    for d in (OUT / "html", li, BLOG_IMG):
        d.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as profile:
        for name, body in CARDS.items():
            html = OUT / "html" / f"{name}.html"
            html.write_text(page(body, 1080, 1350))
            big = li / f"{name}.png"
            shot(html, big, 1080, 1350, profile)
            if name != "00-cover":
                downscale(big, BLOG_IMG / f"{name}.png", 1080, 1350)
            print("rendered", name, Image.open(big).size)
        deck = OUT / "html" / "carousel.html"
        deck.write_text(page("".join(CARDS.values()), 1080, 1350))
        dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=10000",
                              f"--user-data-dir={profile}", "--window-size=1080,1350", "--dump-dom", deck.as_uri()],
                             capture_output=True, text=True).stdout
        overflow = re.findall(r'data-overflow="(\d+):(\d+)px"', dom)
        names = list(CARDS)
        for i, px in overflow:
            print(f"WARNING: card {names[int(i)]} overflows by {px}px")
        if not overflow:
            print("overflow check: all cards fit")
        chrome(["--no-pdf-header-footer", f"--print-to-pdf={li / 'carousel.pdf'}", deck.as_uri()], profile)
        print("carousel", li / "carousel.pdf")
        for name, body, dst in (("og-post", OG_POST, BLOG_IMG / "og.png"), ("og-default", OG_DEFAULT, SITE_IMG / "og-default.png")):
            html = OUT / "html" / f"{name}.html"
            html.write_text(page(body, 1200, 627))
            big = OUT / f"{name}@2x.png"
            shot(html, big, 1200, 627, profile)
            downscale(big, dst, 1200, 627)
            print("rendered", name, Image.open(dst).size)


if __name__ == "__main__":
    main()
