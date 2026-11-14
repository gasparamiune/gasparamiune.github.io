#!/usr/bin/env python3
"""Builds the static portfolio from content.py: index.html, projects/<slug>.html and play/micromouse.html.
Run from anywhere:  python3 _src/build.py"""
import html, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import (PERSON, SKILLS, CATS, PROJECTS, SHORT, FEATURE, HERO_SLIDES, PAGE_HERO, PAGE_HERO_CAP,
                     PLAYS, TIMELINE, LANGS)
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
REV = "2026-11"
N = len(PROJECTS)
SHEETS = N + 1                      # home + one sheet per project
NO = {p["slug"]: i + 1 for i, p in enumerate(PROJECTS)}
ICON = {
 "live": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>',
 "code": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m16 18 6-6-6-6M8 6l-6 6 6 6"/></svg>',
 "play": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>',
 "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
}
_dims = {}
def dims(f):
    if f not in _dims:
        with Image.open(os.path.join(ROOT, "assets/img", f)) as im:
            _dims[f] = im.size
    return _dims[f]

def img(f, alt, up, cls="", lazy=True, extra=""):
    w, h = dims(f)
    return (f'<img src="{up}assets/img/{f}" alt="{E(alt)}" width="{w}" height="{h}"'
            f'{" class=" + chr(34) + cls + chr(34) if cls else ""}{" loading=lazy" if lazy else ""}{extra}>')

def head(title, desc, depth):
    up = "/" if depth is None else "../" * depth
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="https://gasparamiune.github.io/assets/img/og.jpg"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#efece4">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{up}assets/fonts/barlow-condensed-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{up}assets/site.css">
<script>(function(d){{d.classList.add('js');try{{if(localStorage.getItem('theme')==='dark')d.dataset.theme='dark'}}catch(e){{}}setTimeout(function(){{d.classList.add('ready')}},2500)}})(document.documentElement)</script>
</head><body>"""

def top(depth):
    up = "/" if depth is None else "../" * depth
    return f"""<header class="top"><div class="wrap"><a class="brand" href="{up}index.html"><i></i>Gaspar Amiune</a>
<nav aria-label="Main"><a class="opt" href="{up}index.html#work">Work</a><a class="opt" href="{up}index.html#play">Play</a><a class="opt" href="{up}index.html#skills">Skills</a><a class="opt" href="{up}index.html#about">About</a>
<a href="{PERSON['github']}" target="_blank" rel="noopener">GitHub</a><button class="theme-btn" aria-label="Switch between light and dark"><svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg></button></nav></div></header>"""

def foot(depth, scripts=("site.js",)):
    up = "/" if depth is None else "../" * depth
    s = "".join(f'<script src="{up}assets/{f}"></script>' for f in scripts)
    return f"""<footer><div class="wrap"><div><b>Gaspar Amiune</b>{E(PERSON['role'])}<br>{E(PERSON['location'])}</div>
<div><b>Note on the figures</b>Every image on this site is a real render, simulation, screenshot or photo from the project itself. Work that is designed or simulated but not built is labelled that way.</div>
<div><b>Rev {REV}</b><a href="{PERSON['github']}" target="_blank" rel="noopener">GitHub</a> · <a href="{up}index.html#work">Index</a></div></div></footer>
{s}</body></html>"""

# ---------------------------------------------------------------- diagrams (true system maps)
def box(x, y, w, h, t, sub="", col="var(--ink)", sw=1.2, fs=14):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="var(--sheet)" stroke="{col}" stroke-width="{sw}"/>'
    s += f'<text x="{x+w/2}" y="{y+h/2-(6 if sub else -5)}" text-anchor="middle" font-size="{fs}" font-weight="600">{E(t)}</text>'
    if sub:
        s += f'<text x="{x+w/2}" y="{y+h/2+13}" text-anchor="middle" font-size="11.5" style="fill:var(--ink-2)">{E(sub)}</text>'
    return s

def cbox(x, y, w, h, t, sub="", col="var(--accent)", fs=14):
    """Box with a coloured edge: marks a group (accent = core, blue = data, green = safety, violet = AI)."""
    return box(x, y, w, h, t, sub, col, 2, fs) + f'<rect x="{x}" y="{y}" width="5" height="{h}" fill="{col}"/>'

def arrow(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="var(--ink-2)" stroke-width="1.4" marker-end="url(#ah)"/>'

DEFS = '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10z" fill="var(--ink-2)"/></marker></defs>'

def diagram(kind):
    A, C, G, V = "var(--accent)", "var(--blue)", "var(--green)", "var(--violet)"
    if kind == "hedge":
        s = DEFS + '<text class="lbl" x="20" y="22">EXTERNAL DATA</text>'
        for i, t in enumerate(["Prices", "SEC filings", "Patents", "News", "Macro feeds"]):
            s += box(20 + i*150, 32, 136, 40, t)
        s += '<text class="lbl" x="20" y="108">SCORING AGENTS · DAILY DEEP CYCLE</text>'
        ag = ["AI capex", "Catalysts", "Fundamentals", "Inst. flow", "LLM thesis", "Moat", "Quantum", "Valuation"]
        for i, t in enumerate(ag):
            s += (cbox(20 + i*92, 118, 84, 40, t, col=V, fs=12) if t == "LLM thesis" else box(20 + i*92, 118, 84, 40, t, fs=12))
        s += cbox(780, 118, 150, 40, "Context: watcher", col=C)
        s += cbox(780, 166, 150, 40, "Macro regime", col=C)
        s += arrow(380, 72, 380, 116)
        s += cbox(240, 210, 280, 50, "Scoring engine", "normalised weighted sum", col=A)
        s += arrow(380, 158, 380, 208) + arrow(855, 206, 522, 236)
        s += box(240, 290, 280, 50, "Conviction tiers", "HIGH needs agreement + fresh LLM read")
        s += arrow(380, 260, 380, 288)
        s += box(240, 370, 280, 50, "Planner + exits", "BUY · TRIM · CLOSE · hold")
        s += arrow(380, 340, 380, 368)
        s += cbox(600, 290, 330, 50, "Safety layer", "kill switch · daily limit · heartbeat · halt", col=G)
        s += cbox(600, 370, 330, 50, "LLM router", "budget caps + retry, one choke point", col=V)
        s += arrow(522, 395, 598, 320) + arrow(380, 420, 380, 452)
        s += box(240, 454, 280, 40, "Telegram alerts + dashboard")
        return f'<svg viewBox="0 0 950 510" role="img" aria-label="Hedge agents architecture">{s}</svg>'
    if kind == "pourstock":
        s = DEFS
        s += box(20, 30, 200, 56, "Staff & managers", "phone, tablet, kitchen screen")
        s += box(20, 120, 200, 56, "Telegram / in-app", "problem reports")
        s += cbox(290, 30, 230, 56, "React app", "floor · kitchen · bar · rooms · stock", col=A)
        s += cbox(290, 120, 230, 56, "Claude support agent", "triage + answer", col=V)
        s += cbox(590, 30, 200, 56, "Supabase Postgres", "row-level security per venue", col=C)
        s += cbox(590, 120, 200, 56, "Edge functions", "server logic + Claude calls", col=C)
        s += cbox(590, 210, 200, 56, "Forecast service", "Python in Docker", col=C)
        s += cbox(290, 210, 230, 56, "Coding agent fix", "must pass the quality gate", col=V)
        s += cbox(290, 300, 500, 52, "Quality gate on Linux CI", "unit tests · end-to-end tests · AI constitution rule checks", col=G)
        s += arrow(220, 58, 288, 58) + arrow(520, 58, 588, 58) + arrow(220, 148, 288, 148) + arrow(520, 148, 588, 148)
        s += arrow(405, 176, 405, 208) + arrow(405, 266, 405, 298) + arrow(690, 210, 690, 178)
        s += arrow(690, 120, 690, 88)
        return f'<svg viewBox="0 0 810 370" role="img" aria-label="PourStock architecture">{s}</svg>'
    if kind == "coolbench":
        s = DEFS
        s += cbox(20, 40, 210, 60, "Sensor-simulation circuits", "temperature · pressure", col=C)
        s += cbox(20, 130, 210, 60, "Switches", "defrost demand · sensor fault", col=C)
        s += cbox(310, 70, 230, 90, "Refrigeration controller", "superheat · valve · defrost · alarms", col=A)
        s += box(620, 40, 210, 60, "Stepper pointer", "shows valve position")
        s += cbox(620, 130, 210, 60, "Validation tool", "scenarios → traceable results", col=G)
        s += arrow(230, 70, 308, 100) + arrow(230, 160, 308, 130) + arrow(540, 100, 618, 72) + arrow(540, 130, 618, 160)
        return f'<svg viewBox="0 0 850 220" role="img" aria-label="COOL-BENCH system">{s}</svg>'
    if kind == "interstellar":
        s = DEFS
        steps = [("Webcam", "OpenCV capture"), ("Hand landmarks", "MediaPipe"), ("Gesture", "open = move · fist = click"), ("Game", "Pygame loop")]
        for i, (t, sub) in enumerate(steps):
            s += cbox(20 + i*205, 50, 180, 64, t, sub, col=[C, V, A, G][i])
            if i: s += arrow(20 + i*205 - 23, 82, 20 + i*205 - 2, 82)
        s += '<text x="420" y="160" text-anchor="middle" font-size="13" style="fill:var(--ink-2)">Catch astronauts for points · avoid black holes</text>'
        return f'<svg viewBox="0 0 840 180" role="img" aria-label="Interstellar game pipeline">{s}</svg>'
    return ""

# ---------------------------------------------------------------- tiny syntax highlighter
KW = r"\b(void|int|for|if|while|return|continue|auto|def|not|and|or|is|in|else|import|True|False|None|std|queue)\b"
def hl(code, lang):
    out = []
    for line in code.split("\n"):
        cm = "//" if lang == "cpp" else "#"
        i = line.find(cm)
        body, com = (line[:i], line[i:]) if i >= 0 else (line, "")
        b = E(body)
        b = re.sub(r"(?<![\w#&])(\d+(?:\.\d+)?(?:e-?\d+)?)\b", r'<span class="tok-n">\1</span>', b)
        b = re.sub(KW, r'<span class="tok-k">\1</span>', b)
        b = re.sub(r"\b([A-Za-z_]\w*)(?=\()", r'<span class="tok-f">\1</span>', b)
        out.append(b + (f'<span class="tok-c">{E(com)}</span>' if com else ""))
    return "\n".join(out)

def status(p):
    lab, kind = p["status"]; return f'<span class="st {kind}">{E(lab)}</span>'

def ext(url):
    return ' target="_blank" rel="noopener"' if url.startswith("http") else ""

def link_btn(label, url, kind, cls="", depth=1):
    if depth == 0 and url.startswith("../"): url = url[3:]
    c = {"live": "hot", "play": "hot"}.get(kind, "")
    return f'<a class="btn {c} {cls}" href="{E(url)}"{ext(url)}>{ICON.get(kind,"")}{E(label)}</a>'

SCREENS = {"quantum/home.webp", "aibubble/home.webp", "pourstock/cover.webp"}
MAZE = '<canvas data-mini aria-label="Floodfill maze simulation, running live"></canvas>'

def thumb(p, up):
    if p.get("cover"):
        return img(p["cover"], p["title"], up, cls="top" if p["cover"] in SCREENS else "")
    return f'<div class="art">{diagram(p["diagram"])}</div>'

# ---------------------------------------------------------------- index
def build_index():
    cat_n = {k: sum(p["cat"] == k for p in PROJECTS) for k in CATS}
    counts = {k: sum(k in p["skills"] for p in PROJECTS) for k in SKILLS}
    n_open = sum(any(l[2] in ("live", "play") for l in p["links"]) for p in PROJECTS)
    out = [head("Gaspar Amiune · Mechatronics engineer and AI-native builder",
                "Portfolio of Gaspar Amiune: PourStock, the ARGUS lunar rover, a rocket engine and a waterjet design, robots, drones and AI agents. Real renders, simulations and things you can try.", 0), top(0)]
    # hero
    slides = "".join(img(f, cap, "", cls=("on " if i == 0 else "") + fit, lazy=i > 0,
                         extra=f' data-cap="{E(cap)}" data-href="projects/{slug}.html"')
                     for i, (f, slug, cap, fit) in enumerate(HERO_SLIDES))
    ticks = "".join(f'<i{" class=on" if i == 0 else ""}></i>' for i in range(len(HERO_SLIDES)))
    out.append(f"""<main><section class="hero"><div class="wrap">
<div class="hero-meta"><span class="ann"><b>■</b> Portfolio · Rev {REV}</span><span class="ann opt">{E(PERSON['location'])} · 54.91° N 9.79° E</span><span class="ann">Sheet 01 / {SHEETS}</span></div>
<h1 class="name">Gaspar Amiune</h1>
<div class="hero-grid"><div>
<p class="lead">{E(PERSON['tagline'])}</p><p class="sub">{E(PERSON['intro'])}</p>
<div class="row"><a class="btn solid" href="#work">See the work {ICON['arrow']}</a><a class="btn hot" href="#play">{ICON['play']}Try something live</a></div></div>
<figure class="fig plate"><a class="media" href="projects/{HERO_SLIDES[0][1]}.html">{slides}</a>
<figcaption><b>FIG. 01</b><span class="pc">{E(HERO_SLIDES[0][2])}</span><span class="ticks" aria-hidden="true">{ticks}</span></figcaption></figure></div>
<div class="tb"><div><small>Role</small><span>{E(PERSON['role'])}</span></div>
<div><small>Now</small><span>Compressor failure analysis at Danfoss · Founder of PourStock</span></div>
<div><small>Degree</small><span>BSc Mechatronics Engineering, SDU Sønderborg · June 2027</span></div>
<div><small>On this site</small><span>{N} projects · {n_open} you can open and try</span></div></div>
</div></section>""")
    # work
    tabs = f'<button class="on" data-f="all">All<em>{N}</em></button>' + "".join(
        f'<button data-f="{k}">{E(v)}<em>{cat_n[k]}</em></button>' for k, v in CATS.items())
    feats, cards, fno = [], [], 1
    for p in PROJECTS:
        no = f"GA-{NO[p['slug']]:02d}"
        href = f'projects/{p["slug"]}.html'
        data = f'data-cat="{p["cat"]}" data-skills="{" ".join(p["skills"])}"'
        first = p["links"][0] if p["links"] else None
        if p["slug"] in FEATURE:
            f = FEATURE[p["slug"]]; m = f["media"]; fno += 1
            if m[0] == "video":
                media = (f'<video data-auto muted loop playsinline preload="none" poster="assets/img/{m[2]}" aria-label="{E(f["cap"])}">'
                         f'<source src="assets/video/{m[1]}" type="video/mp4"></video>')
            elif m[0] == "img":
                media = img(m[1], f["cap"], "", cls=m[2] if len(m) > 2 else "")
            elif m[0] == "maze":
                media = MAZE
            else:
                media = f'<div class="art full">{diagram(p["diagram"])}</div>'
            keys = "".join(f"<li>{E(k)}</li>" for k in f["keys"])
            tags = "".join(f"<span>{E(SKILLS[s][0])}</span>" for s in p["skills"][:5])
            acts = f'<a class="btn solid" href="{href}">Read more {ICON["arrow"]}</a>'
            if first: acts += link_btn(first[0], first[1], first[2], depth=0)
            feats.append(f"""<article class="feat rv{' flip' if len(feats) % 2 else ''}" {data}>
<figure class="fig"><a class="media" href="{href}" aria-label="{E(p['title'])}">{media}</a><figcaption><b>FIG. {fno:02d}</b><span>{E(f['cap'])}</span></figcaption></figure>
<div><div class="row"><span class="ann"><b>{no}</b> · {p['year']} · {E(CATS[p['cat']])}</span>{status(p)}</div>
<h3><a href="{href}">{E(p['title'])}</a></h3><p>{E(p['short'])}</p><ul class="keys">{keys}</ul><div class="tags">{tags}</div>
<div class="row">{acts}</div></div></article>""")
        else:
            acts = f'<a class="btn sm" href="{href}">Read more {ICON["arrow"]}</a>'
            if first:
                lab = {"live": "Live preview", "play": "Play", "code": "Source"}[first[2]]
                acts += f'<a class="lnk" href="{E(first[1])}"{ext(first[1])}>{lab} ↗</a>'
            cards.append(f"""<article class="card rv" {data}>
<figure class="fig"><a class="media" href="{href}" aria-label="{E(p['title'])}">{thumb(p, '')}</a><figcaption><b>{no}</b>{status(p)}</figcaption></figure>
<h3><a href="{href}">{E(p['title'])}</a></h3><p>{E(p['short'])}</p><div class="row">{acts}</div></article>""")
    out.append(f"""<section class="zone" id="work"><div class="wrap"><div class="sec rv"><span class="no">01</span><h2>Work</h2>
<div class="filters" role="group" aria-label="Filter projects">{tabs}</div></div><p class="fnote" aria-live="polite"></p>
{''.join(feats)}<div class="cards">{''.join(cards)}</div></div></section>""")
    # play band
    pl = []
    for url, m, tag, title, text in PLAYS:
        media = MAZE if m[0] == "maze" else img(m[1], "", "")
        where = "Opens in a new tab ↗" if url.startswith("http") else "On this site"
        pl.append(f"""<a class="playc rv" href="{E(url)}"{ext(url)}><figure class="fig"><div class="media">{media}<span class="go">{ICON['arrow']}</span></div>
<figcaption><b>{E(tag)}</b><span>{E(where)}</span></figcaption></figure><h3>{E(title)}</h3><p>{E(text)}</p></a>""")
    out.append(f"""<section class="band" id="play"><div class="wrap"><div class="sec rv"><span class="no">02</span><h2>Do not read about it. Try it.</h2>
<p>Three things you can use right now, in your browser.</p></div><div class="plays">{''.join(pl)}</div></div></section>""")
    # skills matrix
    cols = "".join(f'<th scope="col"><a href="projects/{p["slug"]}.html">{E(SHORT[p["slug"]])}</a></th>' for p in PROJECTS)
    groups = {}
    for k, (lab, g) in SKILLS.items():
        groups.setdefault(g, []).append(k)
    rows = []
    for g, ks in groups.items():
        rows.append(f'<tr class="grp"><th scope="colgroup">{E(g)}</th><td colspan="{N + 1}"></td></tr>')
        for k in ks:
            cells = "".join("<td><i></i></td>" if k in p["skills"] else "<td></td>" for p in PROJECTS)
            rows.append(f'<tr data-row="{k}"><th class="sk" scope="row"><button type="button" data-skill="{k}" data-label="{E(SKILLS[k][0])}">{E(SKILLS[k][0])}</button></th>{cells}<td class="n">{counts[k]}</td></tr>')
    out.append(f"""<section class="zone" id="skills"><div class="wrap"><div class="sec rv"><span class="no">03</span><h2>Skills, with proof</h2>
<p>One row per skill, one column per project. A mark means the project used it. Click a skill to see those projects.</p></div>
<div class="mx-wrap rv"><table class="mx"><thead><tr><th class="sk" scope="col">Skill</th>{cols}<th scope="col" class="n" aria-label="Projects"></th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></div></section>""")
    # about
    tl = "".join(f"<tr><td>{E(a)}</td><td><b>{E(b)}</b><span>{E(c)}</span></td></tr>" for a, b, c in TIMELINE)
    lg = "".join(f'<div>{E(n)}<u style="--w:{round(100 * v / 6, 1)}%"></u><span>{E(l)}</span></div>' for n, v, l in LANGS)
    out.append(f"""<section class="zone" id="about"><div class="wrap"><div class="sec rv"><span class="no">04</span><h2>About</h2><p>Engineer first, AI-native by habit.</p></div>
<div class="about"><div class="rv"><p class="big">I grew up in Argentina, moved to Italy and then to Denmark, and I study Mechatronics at SDU while working. I like projects where mechanics, electronics and software have to agree, and I like shipping them.</p>
<p>I use Claude every day to build. What I care about most is the system around the code: clear requirements, one source of truth for every number, automatic checks, and honest labels on what is simulated and what is real.</p>
<div class="row" style="margin-top:24px"><a class="btn solid" href="{PERSON['github']}" target="_blank" rel="noopener">{ICON['code']}GitHub</a><a class="btn" href="https://www.pourstock.com" target="_blank" rel="noopener">{ICON['live']}pourstock.com</a></div></div>
<div class="rv"><table class="tl"><tbody>{tl}</tbody></table><div class="langs" aria-label="Languages">{lg}</div></div></div></div></section></main>""")
    out.append(foot(0, ("maze.js", "site.js")))
    return "\n".join(out)

# ---------------------------------------------------------------- project page
def build_project(i):
    p = PROJECTS[i]; up = "../"; slug = p["slug"]
    no = f"GA-{NO[slug]:02d}"
    links = "".join(link_btn(*l) for l in p["links"])
    if not links:
        links = '<span class="ann">No public link: the code is private or the work is a report. The figures below are from the project itself.</span>'
    hm = PAGE_HERO[slug]; cap = PAGE_HERO_CAP[slug]; needs_maze = bool(p.get("play")) or hm[0] == "maze"
    if hm[0] == "diagram":
        hero = f'<div class="diagram">{diagram(p["diagram"])}</div>'
    elif hm[0] == "maze":
        hero = f'<a class="media" href="{p["play"][0]}" aria-label="Open the interactive demo">{MAZE}</a>'
    elif hm[0] == "pair":
        hero = f'<div class="media pair">{img(hm[1], p["title"] + ", photo", up, lazy=False)}{img(hm[2], p["title"] + ", render", up, lazy=False)}</div>'
    else:
        hero = f'<div class="media {hm[0]}">{img(hm[1], cap, up, lazy=False)}</div>'
    secs = []          # (id, title, html)
    secs.append(("project", "The project", '<div class="prose">' + "".join(f"<p>{E(t)}</p>" for t in p["intro"]) + "</div>"))
    if p.get("play") and hm[0] != "maze":
        u, c = p["play"]
        secs.append(("try", "Try it", f'<a href="{u}"><figure class="fig"><div class="media" style="aspect-ratio:16/9">{MAZE}</div><figcaption><b>LIVE</b><span>{E(c)}</span></figcaption></figure></a>'))
    elif p.get("play"):
        u, c = p["play"]
        secs.append(("try", "Try it", f'<div class="prose"><p>{E(c)} You control the speed, step through it one move at a time, and can reveal the walls the mouse has not seen yet.</p></div><div class="row"><a class="btn hot" href="{u}">{ICON["play"]}Open the interactive demo</a></div>'))
    secs.append(("did", "What I did", '<ul class="did">' + "".join(f"<li><span>{d}</span></li>" for d in p["did"]) + "</ul>"))
    if p.get("diagram") and hm[0] != "diagram":
        secs.append(("map", "How it fits together", f'<figure class="fig"><div class="diagram">{diagram(p["diagram"])}</div><figcaption><b>MAP</b><span>Accent = core, blue = data, violet = AI, green = checks.</span></figcaption></figure>'))
    how = "".join(f"<div><b>{E(a)}</b><span>{E(b)}</span></div>" for a, b in p["how"])
    code = ""
    if p.get("code"):
        lang, title, src, note = p["code"]
        code = f'<div class="code"><header><span>{E(title)}</span><b>{ {"cpp": "C++", "py": "Python", "python": "Python"}.get(lang, lang) }</b></header><pre><code>{hl(src, lang)}</code></pre><div class="note">{E(note)}</div></div>'
    secs.append(("hood", "Under the hood", f'<div class="stack">{how}</div>{code}'))
    if p.get("embed"):
        u, c = p["embed"]
        bg = img(p["cover"], "", up) if p.get("cover") else ""
        secs.append(("live", "Live preview", f'<figure class="fig embed"><div class="stage">{bg}<button class="btn hot" data-src="{E(u)}">{ICON["play"]}Load the live preview here</button></div>'
                     f'<figcaption><b>LIVE</b><span>{E(c)}</span><a class="lnk" href="{E(u)}" target="_blank" rel="noopener">New tab ↗</a></figcaption></figure>'))
    fn = 1
    if p.get("videos"):
        v = ""
        for f, c, po in p["videos"]:
            v += (f'<figure class="fig"><div class="media"><video data-auto muted loop playsinline preload="none" poster="{up}assets/img/{po}" aria-label="{E(c)}">'
                  f'<source src="{up}assets/video/{f}" type="video/mp4"></video></div><figcaption><b>FIG. {fn:02d}</b><span>{E(c)}</span></figcaption></figure>'); fn += 1
        secs.append(("motion", "In motion", f'<div class="vids{" one" if len(p["videos"]) == 1 else ""}">{v}</div>'))
    if p.get("gallery"):
        g = ""
        for f, c in p["gallery"]:
            g += f'<figure class="fig" tabindex="0">{img(f, c, up)}<figcaption><b>FIG. {fn:02d}</b><span>{E(c)}</span></figcaption></figure>'; fn += 1
        secs.append(("figures", "Figures", f'<div class="figs">{g}</div>'))
    toc = "".join(f'<li><a href="#{sid}">{E(t)}</a></li>' for sid, t, _ in secs)
    body = "".join(f'<section id="{sid}" class="rv"><h2><small>{k:02d}</small>{E(t)}</h2>{h}</section>' for k, (sid, t, h) in enumerate(secs, 1))
    tags = "".join(f"<span>{E(SKILLS[s][0])}</span>" for s in p["skills"])
    prv, nxt = PROJECTS[i-1], PROJECTS[(i+1) % N]
    long = " class=\"long\"" if len(p["title"]) > 16 else ""
    page = f"""<main><div class="wrap"><section class="ph">
<div class="hero-meta"><a class="ann" href="../index.html#work">← Index</a><span class="ann"><b>{no}</b> · {E(CATS[p['cat']])} · {p['year']}</span><span class="ann">Sheet {NO[slug]+1:02d} / {SHEETS}</span></div>
<h1{long}>{E(p['title'])}</h1><p class="one">{E(p['short'])}</p>
<div class="tb"><div><small>Year</small><span>{p['year']}</span></div><div><small>Role</small><span>{E(p['role'])}</span></div>
<div><small>Team</small><span>{E(p['team'])}</span></div><div><small>Status</small>{status(p)}</div></div>
<div class="row acts">{links}</div></section>
<figure class="fig pfig">{hero}<figcaption><b>FIG. 00</b><span>{E(cap)}</span></figcaption></figure>
<div class="pb"><aside class="rail"><div><h4>On this sheet</h4><ol class="toc">{toc}</ol></div><div><h4>Skills shown</h4><div class="tags">{tags}</div></div></aside>
<div class="pmain">{body}</div></div>
<nav class="pnav" aria-label="More projects"><a href="{prv['slug']}.html"><span class="ann">← Previous · GA-{NO[prv['slug']]:02d}</span><b>{E(prv['title'])}</b></a>
<a href="{nxt['slug']}.html"><span class="ann">Next · GA-{NO[nxt['slug']]:02d} →</span><b>{E(nxt['title'])}</b></a></nav></div></main>"""
    return (head(f"{p['title']} · Gaspar Amiune", p["short"], 1) + top(1) + page
            + foot(1, ("maze.js", "site.js") if needs_maze else ("site.js",)))

# ---------------------------------------------------------------- play page
FLOOD_SNIPPET = """void Flood() {
  std::queue<pii> q;
  // every cell starts "infinitely" far
  ...
  // the 4 centre cells are distance 0
  for (goal : goals) { dist = 0; q.push(goal); }
  while (!q.empty()) {
    auto [x, y] = q.front(); q.pop();
    for (int d = 0; d < 4; d++) {
      if (wall[x][y][d] == 1) continue; // known wall
      if (dist[nx][ny] > dist[x][y] + 1) {
        dist[nx][ny] = dist[x][y] + 1;
        q.push({nx, ny});
      }
    }
  }
}"""

def build_play():
    return head("Micromouse floodfill, live · Gaspar Amiune",
                "Watch the floodfill algorithm from my Micromouse firmware explore a random 16x16 maze, then race the shortest path.", 1) + top(1) + f"""<main><div class="wrap"><section class="ph">
<div class="hero-meta"><a class="ann" href="../projects/micromouse.html">← Micromouse maze robot</a><span class="ann"><b>GA-{NO['micromouse']:02d}</b> · Interactive</span><span class="ann">Runs in your browser</span></div>
<h1 class="long">Floodfill, live</h1>
<p class="one">The mouse starts in the bottom-left corner and knows nothing about the maze. In each new cell it senses the walls, re-runs <span class="mono">Flood()</span> on what it knows and steps to the lowest-numbered open neighbour.</p></section>
<div class="simlay"><figure class="fig board"><canvas id="cv" aria-label="Maze simulation"></canvas>
<div class="ctrl"><button class="btn hot" id="play">▶ Run</button><button class="btn" id="stepb">Step</button><button class="btn" id="newb">New maze</button>
<label><input type="checkbox" id="reveal"> Hidden walls</label><label><input type="checkbox" id="nums" checked> Distances</label>
<label>Speed <input type="range" id="speed" min="1" max="60" value="18"></label></div>
<div class="tb" style="margin:0;border-width:1px 0 0;grid-template-columns:repeat(3,1fr)"><div><small>Phase</small><span id="phase">Exploring</span></div><div><small>Exploration steps</small><span id="steps">0</span></div><div><small>Speed-run cells</small><span id="run">–</span></div></div></figure>
<aside><div class="rail" style="position:static"><div><h4>What you see</h4><ul class="legend">
<li><i style="background:var(--ink)"></i>Walls the mouse has sensed</li>
<li><i style="background:var(--ink-3);height:2px"></i>Hidden walls (tick the box)</li>
<li><i style="background:var(--blue)"></i>Path explored so far</li>
<li><i style="background:var(--accent)"></i>Final speed-run path</li>
<li><i style="background:linear-gradient(90deg,color-mix(in srgb,var(--ink) 24%,transparent),color-mix(in srgb,var(--ink) 3%,transparent))"></i>Distance map: darker is closer to the target</li></ul></div>
<div><h4>How a run goes</h4><ol class="toc"><li><a>Explore until the centre is reached</a></li><li><a>Explore back to the start</a></li><li><a>Race the shortest path it has proven</a></li></ol></div></div>
<div class="code"><header><span>The same logic in my firmware</span><b>C++</b></header><pre><code>{hl(FLOOD_SNIPPET, "cpp")}</code></pre><div class="note">On the robot this runs on an STM32H743 in well under a millisecond.</div></div>
</aside></div></div></main>""" + foot(1, ("maze.js", "site.js")).replace("</body>", """<script>
(function(){
  const cv=document.getElementById('cv'),ctx=cv.getContext('2d');let sim=new Micromouse.Sim(Date.now()%1e9),running=false,acc=0,last=0;
  const $=id=>document.getElementById(id);
  const size=()=>{const r=cv.getBoundingClientRect(),d=Math.min(2,devicePixelRatio||1);cv.width=cv.height=Math.round(r.width*d);render()};
  const render=()=>{Micromouse.draw(ctx,sim,cv.width,{reveal:$('reveal').checked,numbers:$('nums').checked});
    $('steps').textContent=sim.steps;$('run').textContent=sim.runPath?sim.runPath.length-1:'–';
    $('phase').textContent={explore:'Exploring',return:'Returning home',run:'Speed run',done:'Done'}[sim.phase]};
  const tick=t=>{if(running){acc+=(t-last)*$('speed').value/1000;while(acc>=1){acc--;if(!sim.step()){running=false;$('play').textContent='▶ Run';break}}render()}last=t;requestAnimationFrame(tick)};
  $('play').onclick=()=>{if(sim.phase==='done')sim=new Micromouse.Sim(Date.now()%1e9);running=!running;$('play').textContent=running?'❚❚ Pause':'▶ Run'};
  $('stepb').onclick=()=>{running=false;$('play').textContent='▶ Run';sim.step();render()};
  $('newb').onclick=()=>{sim=new Micromouse.Sim(Date.now()%1e9);render()};
  $('reveal').onchange=render;$('nums').onchange=render;addEventListener('resize',size);
  document.querySelectorAll('.theme-btn').forEach(b=>b.addEventListener('click',()=>setTimeout(render,0)));
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(render);
  size();requestAnimationFrame(tick);
})();
</script></body>""")

def build_404():
    return head("Sheet not found · Gaspar Amiune", "This page does not exist.", None) + top(None) + f"""<main><div class="wrap"><section class="ph" style="min-height:56vh">
<div class="hero-meta"><a class="ann" href="/index.html#work">← Index</a><span class="ann"><b>404</b> · Not in the drawing set</span><span class="ann">Sheet ?? / {SHEETS}</span></div>
<h1>Sheet not found</h1><p class="one">This page does not exist. The index has all {N} projects.</p>
<div class="row acts"><a class="btn solid" href="/index.html#work">Back to the index {ICON['arrow']}</a></div></section></div></main>""" + foot(None)

def main():
    os.makedirs(os.path.join(ROOT, "projects"), exist_ok=True)
    for p in PROJECTS:
        used = [p.get("cover"), p.get("hero")] + [g[0] for g in p.get("gallery", [])] + [v[2] for v in p.get("videos", [])] + list(PAGE_HERO[p["slug"]][1:])
        for f in used:
            if f: assert os.path.exists(os.path.join(ROOT, "assets/img", f)), f"missing image {f}"
        for v in p.get("videos", []):
            assert os.path.exists(os.path.join(ROOT, "assets/video", v[0])), f"missing video {v[0]}"
    open(os.path.join(ROOT, "index.html"), "w").write(build_index())
    for i, p in enumerate(PROJECTS):
        open(os.path.join(ROOT, "projects", p["slug"] + ".html"), "w").write(build_project(i))
    open(os.path.join(ROOT, "play", "micromouse.html"), "w").write(build_play())
    open(os.path.join(ROOT, "404.html"), "w").write(build_404())
    base = "https://gasparamiune.github.io/"
    urls = ["", "play/micromouse.html"] + [f"projects/{p['slug']}.html" for p in PROJECTS]
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{base}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n")
    print(f"built index + {N} project pages + play page + 404")

if __name__ == "__main__":
    main()
