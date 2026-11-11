#!/usr/bin/env python3
"""Builds the static portfolio from content.py: index.html + projects/<slug>.html.
Run from anywhere:  python3 _src/build.py"""
import html, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import PERSON, SKILLS, CATS, PROJECTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">')
ICON = {
 "live": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17 17 7M8 7h9v9"/></svg>',
 "code": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m16 18 6-6-6-6M8 6l-6 6 6 6"/></svg>',
 "play": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>',
 "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
}

def head(title, desc, depth):
    up = "../" * depth
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="https://gasparamiune.github.io/assets/img/og.webp">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
{FONTS}<link rel="stylesheet" href="{up}assets/site.css">
<script>try{{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head><body><div class="grid-bg"></div>"""

def nav(depth):
    up = "../" * depth
    return f"""<header class="nav"><div class="wrap"><a class="brand" href="{up}index.html"><i></i>Gaspar Amiune</a>
<nav><a class="hide-sm" href="{up}index.html#projects">Projects</a><a class="hide-sm" href="{up}index.html#play">Play</a><a class="hide-sm" href="{up}index.html#skills">Skills</a><a class="hide-sm" href="{up}index.html#about">About</a>
<a href="{PERSON['github']}" target="_blank" rel="noopener">GitHub</a><button class="theme-btn" aria-label="Toggle light and dark theme">◐</button></nav></div></header>"""

def foot(depth):
    up = "../" * depth
    return f"""<footer><div class="wrap"><span>© 2026 Gaspar Amiune · {E(PERSON['location'])}</span>
<span>Every image on this site is a real render, simulation, screenshot or photo from the project itself.</span></div></footer>
<script src="{up}assets/site.js"></script></body></html>"""

# ---------------------------------------------------------------- diagrams (true system maps)
def box(x, y, w, h, t, sub="", col="var(--line2)", fill="var(--bg2)"):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{col}" stroke-width="1.5"/>'
    s += f'<text x="{x+w/2}" y="{y+h/2-(6 if sub else -5)}" text-anchor="middle" font-size="14" font-weight="600">{E(t)}</text>'
    if sub:
        s += f'<text x="{x+w/2}" y="{y+h/2+13}" text-anchor="middle" font-size="11.5" style="fill:var(--muted)">{E(sub)}</text>'
    return s

def arrow(x1, y1, x2, y2, col="var(--dim)"):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="1.6" marker-end="url(#ah)"/>'

DEFS = '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10z" fill="var(--dim)"/></marker></defs>'

def diagram(kind):
    A, C, G, V = "var(--amber)", "var(--cyan)", "var(--green)", "var(--violet)"
    if kind == "hedge":
        s = DEFS + '<text class="lbl" x="20" y="22">EXTERNAL DATA</text>'
        for i, t in enumerate(["Prices", "SEC filings", "Patents", "News", "Macro feeds"]):
            s += box(20 + i*150, 32, 136, 40, t)
        s += '<text class="lbl" x="20" y="108">SCORING AGENTS · DAILY DEEP CYCLE</text>'
        ag = ["AI capex", "Catalysts", "Fundamentals", "Inst. flow", "LLM thesis", "Moat", "Quantum", "Valuation"]
        for i, t in enumerate(ag):
            s += box(20 + i*92, 118, 84, 40, t, col=(A if t == "LLM thesis" else "var(--line2)"))
        s += box(780, 118, 150, 40, "Context: watcher", col=C)
        s += box(780, 166, 150, 40, "Macro regime", col=C)
        s += arrow(380, 72, 380, 116)
        s += box(240, 210, 280, 50, "Scoring engine", "normalised weighted sum", col=A)
        s += arrow(380, 158, 380, 208) + arrow(855, 206, 522, 236)
        s += box(240, 290, 280, 50, "Conviction tiers", "HIGH needs agreement + fresh LLM read")
        s += arrow(380, 260, 380, 288)
        s += box(240, 370, 280, 50, "Planner + exits", "BUY · TRIM · CLOSE · hold")
        s += arrow(380, 340, 380, 368)
        s += box(600, 290, 330, 50, "Safety layer", "kill switch · daily limit · heartbeat · halt", col=G)
        s += box(600, 370, 330, 50, "LLM router", "budget caps + retry, one choke point", col=V)
        s += arrow(522, 395, 598, 320) + arrow(380, 420, 380, 452)
        s += box(240, 454, 280, 40, "Telegram alerts + dashboard")
        return f'<svg viewBox="0 0 950 510" role="img" aria-label="Hedge agents architecture">{s}</svg>'
    if kind == "pourstock":
        s = DEFS
        s += box(20, 30, 200, 56, "Staff & managers", "phone, tablet, kitchen screen")
        s += box(20, 120, 200, 56, "Telegram / in-app", "problem reports")
        s += box(290, 30, 230, 56, "React app", "floor · kitchen · bar · rooms · stock", col=A)
        s += box(290, 120, 230, 56, "Claude support agent", "triage + answer", col=V)
        s += box(590, 30, 200, 56, "Supabase Postgres", "row-level security per venue", col=C)
        s += box(590, 120, 200, 56, "Edge functions", "server logic + Claude calls", col=C)
        s += box(590, 210, 200, 56, "Forecast service", "Python in Docker", col=C)
        s += box(290, 210, 230, 56, "Coding agent fix", "must pass the quality gate", col=V)
        s += box(290, 300, 500, 52, "Quality gate on Linux CI", "unit tests · end-to-end tests · AI constitution rule checks", col=G)
        s += arrow(220, 58, 288, 58) + arrow(520, 58, 588, 58) + arrow(220, 148, 288, 148) + arrow(520, 148, 588, 148)
        s += arrow(405, 176, 405, 208) + arrow(405, 266, 405, 298) + arrow(690, 210, 690, 88)
        s += arrow(690, 120, 690, 88)
        return f'<svg viewBox="0 0 810 370" role="img" aria-label="PourStock architecture">{s}</svg>'
    if kind == "coolbench":
        s = DEFS
        s += box(20, 40, 210, 60, "Sensor-simulation circuits", "temperature · pressure", col=C)
        s += box(20, 130, 210, 60, "Switches", "defrost demand · sensor fault", col=C)
        s += box(310, 70, 230, 90, "Refrigeration controller", "superheat · valve · defrost · alarms", col=A)
        s += box(620, 40, 210, 60, "Stepper pointer", "shows valve position")
        s += box(620, 130, 210, 60, "Validation tool", "scenarios → traceable results", col=G)
        s += arrow(230, 70, 308, 100) + arrow(230, 160, 308, 130) + arrow(540, 100, 618, 72) + arrow(540, 130, 618, 160)
        return f'<svg viewBox="0 0 850 220" role="img" aria-label="COOL-BENCH system">{s}</svg>'
    if kind == "interstellar":
        s = DEFS
        steps = [("Webcam", "OpenCV capture"), ("Hand landmarks", "MediaPipe"), ("Gesture", "open = move · fist = click"), ("Game", "Pygame loop")]
        for i, (t, sub) in enumerate(steps):
            s += box(20 + i*205, 50, 180, 64, t, sub, col=[C, V, A, G][i])
            if i: s += arrow(20 + i*205 - 23, 82, 20 + i*205 - 2, 82)
        s += '<text x="420" y="160" text-anchor="middle" font-size="13" style="fill:var(--muted)">Catch astronauts for points · avoid black holes</text>'
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
        b = re.sub(r"(\d+(?:\.\d+)?(?:e-?\d+)?)", r'<span class="tok-n">\1</span>', b)
        b = re.sub(KW, r'<span class="tok-k">\1</span>', b)
        b = re.sub(r"\b([A-Za-z_]\w*)(?=\()", r'<span class="tok-f">\1</span>', b)
        out.append(b + (f'<span class="tok-c">{E(com)}</span>' if com else ""))
    return "\n".join(out)

def badge(p):
    lab, kind = p["status"]; return f'<span class="badge {kind}">{E(lab)}</span>'

def thumb_html(p, depth):
    up = "../" * depth
    if p.get("cover"):
        return f'<img src="{up}assets/img/{p["cover"]}" alt="{E(p["title"])}" loading="lazy">'
    if p.get("code"):
        return f'<div class="art"><pre>{hl(p["code"][2], p["code"][0])}</pre></div>'
    return f'<div class="art">{diagram(p["diagram"])}</div>'

def link_btn(label, url, kind, cls=""):
    ext = url.startswith("http")
    c = {"live": "primary", "play": "cyan", "code": ""}.get(kind, "")
    return f'<a class="btn {c} {cls}" href="{E(url)}"{" target=_blank rel=noopener" if ext else ""}>{ICON.get(kind,"")}{E(label)}</a>'

# ---------------------------------------------------------------- index
def build_index():
    by_slug = {p["slug"]: p for p in PROJECTS}
    counts = {k: sum(k in p["skills"] for p in PROJECTS) for k in SKILLS}
    n_live = sum(any(l[2] in ("live", "play") and l[1].startswith("http") for l in p["links"]) for p in PROJECTS)
    n_built = sum(p["status"][1] in ("built", "live") for p in PROJECTS)
    out = [head("Gaspar Amiune · Mechatronics engineer & AI-native builder",
                "Portfolio of Gaspar Amiune: PourStock, the ARGUS lunar rover, rocket engine and waterjet design, robots, drones and AI agents.", 0), nav(0)]
    m = [("argus/01_deployed_driving.webp", "ARGUS", "argus", "tall"), ("engine/plume_artistic_side.webp", "ARGOS-H1", "argos-h1", ""),
         ("pourstock/shifts.webp", "PourStock", "pourstock", ""), ("drone/d_000.webp", "Drone", "flood-drone", ""), ("robotdog/g_090.webp", "Robot dog", "robot-dog", "")]
    mosaic = "".join(f'<a class="{c}" href="projects/{s}.html"><img src="assets/img/{f}" alt="{E(t)}"><span>{E(t)}</span></a>' for f, t, s, c in m)
    out.append(f"""<main><section class="hero"><div class="wrap">
<div><div class="kicker">Portfolio · {E(PERSON['location'])}</div>
<h1>Gaspar Amiune<br><span>builds real systems.</span></h1>
<p class="lead">{E(PERSON['tagline'])}</p><p class="sub">{E(PERSON['intro'])}</p>
<div class="cta"><a class="btn primary" href="#projects">{ICON['arrow']}See the projects</a><a class="btn cyan" href="#play">{ICON['play']}Try something live</a></div></div>
<div class="mosaic rv">{mosaic}</div></div>
<div class="wrap"><div class="stats rv"><div><b>{len(PROJECTS)}</b><small>projects, personal and university</small></div>
<div><b>{n_live}</b><small>with a live preview you can open</small></div><div><b>{n_built}</b><small>built, shipped or tested</small></div>
<div><b>1</b><small>startup live in production</small></div></div></div></section>""")
    # play
    out.append(f"""<section class="block" id="play"><div class="wrap"><div class="sec-head rv"><div><div class="kicker">Play</div><h2>Don't read about it. Try it.</h2></div>
<p>Three things you can use right now, in your browser.</p></div><div class="play rv">
<a href="https://gasparamiune.github.io/ARGus/surface-test/" target="_blank" rel="noopener"><img src="assets/img/argus/03_at_station_APXS_down.webp" alt=""><span class="tag">GAME · 3D</span><h3>Drive ARGUS on the Moon</h3><p>The real rover CAD in three.js: drive it, switch design revisions, open every part.</p></a>
<a href="play/micromouse.html"><canvas class="mini-maze" data-mini></canvas><span class="tag">SIMULATION</span><h3>Micromouse floodfill</h3><p>My maze-solving algorithm exploring a random maze, step by step.</p></a>
<a href="https://gasparamiune.github.io/quantum-physics-book/" target="_blank" rel="noopener"><img src="assets/img/quantum/home.webp" alt=""><span class="tag">INTERACTIVE BOOK</span><h3>Beat the quantum bosses</h3><p>Simulations, hint ladders and four final bosses for the exam.</p></a>
</div></div></section>""")
    # projects
    tabs = '<button class="on" data-f="all">All</button>' + "".join(f'<button data-f="{k}">{E(v)}</button>' for k, v in CATS.items())
    cards = []
    for p in PROJECTS:
        chips = "".join(f'<span class="chip">{E(SKILLS[s][0])}</span>' for s in p["skills"][:4])
        acts = "".join(link_btn(l[0], l[1] if l[1].startswith("http") else l[1].replace("../", ""), l[2]) for l in p["links"][:1])
        acts += f'<a class="btn" href="projects/{p["slug"]}.html">Read more {ICON["arrow"]}</a>'
        cards.append(f"""<article class="card rv" data-cat="{p['cat']}" data-skills="{' '.join(p['skills'])}">
<a class="thumb" href="projects/{p['slug']}.html">{thumb_html(p,0)}<span class="badge-wrap" style="position:absolute;top:12px;left:12px">{badge(p)}</span></a>
<div class="body"><div class="meta"><span>{p['year']}</span><span>·</span><span>{E(CATS[p['cat']])}</span></div>
<h3><a href="projects/{p['slug']}.html">{E(p['title'])}</a></h3><p>{E(p['short'])}</p><div class="chips">{chips}</div>
<div class="actions">{acts}</div></div></article>""")
    out.append(f"""<section class="block" id="projects"><div class="wrap"><div class="sec-head rv"><div><div class="kicker">Work</div><h2>All projects</h2></div>
<div class="filters">{tabs}</div></div><div class="filter-note"></div><div class="cards">{''.join(cards)}</div></div></section>""")
    # skills
    groups = {}
    for k, (lab, g) in SKILLS.items():
        groups.setdefault(g, []).append(k)
    sg = "".join(f'<div class="skill-group rv"><h4>{E(g)}</h4><div class="chips">' +
                 "".join(f'<button class="chip" data-skill="{k}" data-label="{E(SKILLS[k][0])}">{E(SKILLS[k][0])}<em>{counts[k]}</em></button>' for k in ks) +
                 '</div></div>' for g, ks in groups.items())
    out.append(f"""<section class="block" id="skills"><div class="wrap"><div class="sec-head rv"><div><div class="kicker">Skills</div><h2>What I bring, with proof</h2></div>
<p>Each number is how many projects on this page use that skill. Click one to see them.</p></div><div class="skills">{sg}</div></div></section>""")
    # about
    tl = [("2026 –", "Danfoss, compressor failure analysis", "Disassembling compressors and tracing mechanical, electrical and electronic faults"),
          ("2026 –", "Founder, PourStock", "Operations software for restaurants and hotels, live at pourstock.com"),
          ("2023 – 2027", "BSc Mechatronics Engineering, SDU Sønderborg", "Graduating June 2027"),
          ("2015 – 2026", "11 years in restaurants and hotels", "Where PourStock comes from"),
          ("2011 – 2017", "Programming Technician (Java)", "Technical high school, Alta Gracia, Argentina")]
    tlh = "".join(f'<li><small>{a}</small><b>{E(b)}</b><span style="color:var(--muted);font-size:14px">{E(c)}</span></li>' for a, b, c in tl)
    out.append(f"""<section class="block" id="about"><div class="wrap"><div class="sec-head rv"><div><div class="kicker">About</div><h2>Engineer first, AI-native by habit</h2></div></div>
<div class="about"><div class="panel rv"><p style="margin-top:0;font-size:17px">I grew up in Argentina, moved to Italy and then to Denmark, and I study Mechatronics at SDU while working. I like projects where mechanics, electronics and software have to agree, and I like shipping them.</p>
<p style="font-size:17px">I use Claude every day to build. What I care about most is the system around the code: clear requirements, one source of truth for every number, automatic checks, and honest labels on what is simulated and what is real.</p>
<p style="color:var(--muted)">Languages: Spanish (native), English (C1), Italian (C1), Danish (B1), Russian (A1).</p>
<div class="cta" style="display:flex;gap:10px;flex-wrap:wrap;margin-top:18px"><a class="btn primary" href="{PERSON['github']}" target="_blank" rel="noopener">{ICON['code']}GitHub</a><a class="btn" href="https://www.pourstock.com" target="_blank" rel="noopener">{ICON['live']}pourstock.com</a></div></div>
<div class="panel rv"><ul class="tl">{tlh}</ul></div></div></div></section></main>""")
    out.append(foot(0).replace('<script src', '<script src="assets/maze.js"></script><script src', 1))
    return "\n".join(out)

# ---------------------------------------------------------------- project page
def build_project(i):
    p = PROJECTS[i]; up = "../"
    hero = (f'<img src="{up}assets/img/{p["hero"]}" alt="{E(p["title"])}">' if p.get("hero")
            else f'<div class="hero-art" style="display:grid;place-items:center;padding:80px 40px 140px;opacity:.55">{diagram(p["diagram"])}</div>')
    links = "".join(link_btn(*l) for l in p["links"])
    meta = f"""<div class="metarow"><div><b>Year</b><span>{p['year']}</span></div><div><b>Role</b><span>{E(p['role'])}</span></div>
<div><b>Team</b><span>{E(p['team'])}</span></div><div><b>Status</b><span>{badge(p)}</span></div></div>"""
    secs = [f'<section class="prose rv"><h2>The project</h2>' + "".join(f"<p>{E(t)}</p>" for t in p["intro"]) + "</section>"]
    if p.get("play"):
        u, cap = p["play"]
        secs.append(f'<section class="rv"><h2>Try it</h2><a class="embed" href="{u}" style="display:block"><div class="stage"><canvas class="mini-maze" data-mini style="position:absolute;inset:0;width:100%;height:100%"></canvas><span class="btn primary">{ICON["play"]}Open the interactive demo</span></div><p>{E(cap)}</p></a></section>')
    secs.append('<section class="rv"><h2>What I did</h2><ul class="did">' + "".join(f"<li>{d}</li>" for d in p["did"]) + "</ul></section>")
    if p.get("diagram"):
        secs.append(f'<section class="rv"><h2>How it fits together</h2><div class="diagram">{diagram(p["diagram"])}</div></section>')
    how = "".join(f"<div><b>{E(a)}</b><span>{E(b)}</span></div>" for a, b in p["how"])
    code = ""
    if p.get("code"):
        lang, title, src, note = p["code"]
        code = f'<div class="code"><header><i></i><i></i><i></i>&nbsp;{E(title)}</header><pre><code>{hl(src, lang)}</code></pre><div class="note">{E(note)}</div></div>'
    secs.append(f'<section class="rv"><h2>Under the hood</h2><div class="stack">{how}</div>{code}</section>')
    if p.get("embed"):
        u, cap = p["embed"]
        bg = f'<img src="{up}assets/img/{p["cover"]}" alt="">' if p.get("cover") else ""
        secs.append(f'<section class="rv"><h2>Live preview</h2><div class="embed"><div class="bar"><i></i><i></i><i></i>{E(u.replace("https://",""))}<a href="{E(u)}" target="_blank" rel="noopener">Open in a new tab ↗</a></div>'
                    f'<div class="stage">{bg}<button class="btn primary" data-src="{E(u)}">{ICON["play"]}Load the live preview here</button></div><p>{E(cap)}</p></div></section>')
    if p.get("videos"):
        v = "".join(f'<figure><video data-auto muted loop playsinline preload="none" poster="{up}assets/img/{po}"><source src="{up}assets/video/{f}" type="video/mp4"></video><figcaption>{E(c)}</figcaption></figure>' for f, c, po in p["videos"])
        secs.append(f'<section class="rv"><h2>In motion</h2><div class="videos">{v}</div></section>')
    if p.get("gallery"):
        g = "".join(f'<figure><img src="{up}assets/img/{f}" alt="{E(c)}" loading="lazy"><figcaption>{E(c)}</figcaption></figure>' for f, c in p["gallery"])
        secs.append(f'<section class="rv"><h2>Renders, results and photos</h2><div class="gallery">{g}</div></section>')
    chips = "".join(f'<a class="chip" href="../index.html#projects">{E(SKILLS[s][0])}</a>' for s in p["skills"])
    side = f'<aside class="side">' + (f'<div class="panel"><h4>Links</h4><div class="links">{links}</div></div>' if links else
                                      '<div class="panel"><h4>Links</h4><p style="margin:0;color:var(--muted);font-size:14px">The code is private or the work is a report, so there is no public link. The visuals here are from the project itself.</p></div>')
    side += f'<div class="panel"><h4>Skills shown</h4><div class="chips">{chips}</div></div></aside>'
    prv, nxt = PROJECTS[i-1], PROJECTS[(i+1) % len(PROJECTS)]
    pn = f'<div class="wrap pnav"><a href="{prv["slug"]}.html"><small>← Previous</small><b>{E(prv["title"])}</b></a><a class="next" href="{nxt["slug"]}.html"><small>Next →</small><b>{E(nxt["title"])}</b></a></div>'
    body = f"""<main><div class="p-hero">{hero}<div class="wrap"><a class="crumb" href="../index.html#projects">← All projects</a><div class="kicker">{E(CATS[p['cat']])}</div>
<h1>{E(p['title'])}</h1><p class="one">{E(p['short'])}</p>{meta}<div class="cta" style="display:flex;gap:10px;flex-wrap:wrap">{links}</div></div></div>
<div class="wrap p-body"><div>{''.join(secs)}</div>{side}</div>{pn}</main>"""
    extra = '<script src="../assets/maze.js"></script>' if p.get("play") else ""
    return head(f"{p['title']} · Gaspar Amiune", p["short"], 1) + nav(1) + body + foot(1).replace('<script src', extra + '<script src', 1)

def main():
    os.makedirs(os.path.join(ROOT, "projects"), exist_ok=True)
    open(os.path.join(ROOT, "index.html"), "w").write(build_index())
    for i, p in enumerate(PROJECTS):
        for f in [p.get("cover"), p.get("hero")] + [g[0] for g in p.get("gallery", [])] + [v[2] for v in p.get("videos", [])]:
            if f: assert os.path.exists(os.path.join(ROOT, "assets/img", f)), f"missing image {f}"
        for v in p.get("videos", []):
            assert os.path.exists(os.path.join(ROOT, "assets/video", v[0])), f"missing video {v[0]}"
        open(os.path.join(ROOT, "projects", p["slug"] + ".html"), "w").write(build_project(i))
    print(f"built index + {len(PROJECTS)} project pages")

if __name__ == "__main__":
    main()
