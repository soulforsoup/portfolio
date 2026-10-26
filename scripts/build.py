#!/usr/bin/env python3
"""Regenerate the committed static pages. Python 3 only; no packages or build step needed to host."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
HOME = json.loads((ROOT / "content/home.json").read_text(encoding="utf-8"))
PHOTOS = json.loads((ROOT / "content/photographs.json").read_text(encoding="utf-8"))
VIDEOS = json.loads((ROOT / "content/videos.json").read_text(encoding="utf-8"))
DOMAIN = "https://justintan.work"

def e(value):
    return escape(str(value), quote=True)

def service_copy(value):
    # The strikethrough is part of the original joke, not a service claim.
    return e(value).replace("multi-level marketing scams", "<s>multi-level marketing scams</s>")

def icon(name="arrow", size=20):
    paths = {
        "arrow": '<path d="M5 19 19 5M5 5h14v14"/>',
        "right": '<path d="M4 12h16m-6-6 6 6-6 6"/>',
        "left": '<path d="M20 12H4m6-6-6 6 6 6"/>',
        "down": '<path d="M12 4v16m-6-6 6 6 6-6"/>',
        "close": '<path d="m6 6 12 12M6 18 18 6"/>',
        "plus": '<path d="M12 4v16M4 12h16"/>',
        "play": '<path d="m8 5 11 7-11 7Z" fill="currentColor" stroke="none"/>',
    }
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">{paths[name]}</svg>'

def photo_image(photo, base="", sizes="(max-width:600px) 46vw, (max-width:800px) 46vw, 30vw", eager=False):
    srcset = ", ".join(base + v["path"] + " " + str(v["width"]) + "w" for v in photo["variants"])
    source = photo["variants"][1]["path"] if len(photo["variants"]) > 1 else photo["variants"][0]["path"]
    priority = ' fetchpriority="high"' if eager else ""
    return (
        f'<picture><source type="image/webp" srcset="{e(srcset)}" sizes="{e(sizes)}">'
        f'<img src="{e(base + photo["original"])}" width="{photo["width"]}" height="{photo["height"]}" '
        f'alt="{e(photo["alt"])}" loading="{"eager" if eager else "lazy"}" decoding="async"{priority}></picture>'
    )

def nav(base, current):
    links = [("Home", base + "index.html", "home"), ("Videography", base + "videography/", "video"), ("Photography", base + "photography/", "photo")]
    items = "".join(f'<a href="{url}"{" aria-current=" + chr(34) + "page" + chr(34) if key == current else ""}>{name}</a>' for name, url, key in links)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="container nav-wrap">
<a class="brand" href="{base}index.html" aria-label="Justin Tan — home"><span class="brand-mark" aria-hidden="true">jt</span><span class="brand-label">justin <span class="brand-separator">/</span> creator</span></a>
<button class="menu-toggle" aria-controls="site-navigation" aria-expanded="false"><span>Menu</span>{icon("plus", 15)}</button>
<nav id="site-navigation" class="nav-links" aria-label="Main navigation">{items}<a class="nav-contact" href="#contact">Let’s talk {icon("arrow", 14)}</a></nav>
</div></header>'''

def footer():
    social = "".join(f'<a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["title"])} ↗</a>' for s in HOME["socials"])
    return f'''<section id="contact" class="contact" aria-labelledby="contact-heading"><div class="container">
<div class="contact-top"><p class="eyebrow">Have something in mind?</p><p class="micro">A conversation is a good place to start.</p></div>
<h2 id="contact-heading"><a class="contact-title" href="mailto:{e(HOME["email"])}"><span>{e(HOME["contactTitle"])}</span>{icon("arrow", 100)}</a></h2>
<div class="contact-bottom"><a class="email-link" href="mailto:{e(HOME["email"])}">{e(HOME["email"])}</a><nav class="social-links" aria-label="Social profiles">{social}</nav></div>
</div></section>
<footer class="container site-footer"><span>© Justin Tan · Photos, films &amp; everything between.</span><a href="#top">Back to top ↑</a></footer>'''

def video_dialog():
    return f'''<dialog class="viewer" id="video-viewer" aria-labelledby="video-title">
<div class="viewer-header"><h2 id="video-title">Video</h2><button class="viewer-close" data-close aria-label="Close video" autofocus><span>Close</span>{icon("close", 18)}</button></div>
<div class="viewer-stage video-stage"><p class="video-caption" id="video-description"></p></div>
<div class="viewer-footer"><span>Videography / Justin Tan</span><a id="video-external" href="https://www.youtube.com/" target="_blank" rel="noopener noreferrer">Watch on YouTube ↗</a></div>
</dialog>'''

def photo_dialog():
    return f'''<dialog class="viewer" id="photo-viewer" aria-labelledby="photo-title">
<div class="viewer-header"><h2 id="photo-title">Photograph</h2><button class="viewer-close" data-close aria-label="Close photograph" autofocus><span>Close</span>{icon("close", 18)}</button></div>
<div class="viewer-stage"><button class="viewer-arrow prev" data-prev aria-label="Previous photograph">{icon("left")}</button>
<img class="viewer-image" alt="" decoding="async">
<button class="viewer-arrow next" data-next aria-label="Next photograph">{icon("right")}</button></div>
<div class="viewer-footer"><span id="photo-position" role="status" aria-live="polite"></span><span class="viewer-help">← → to explore · Esc to close</span><a id="photo-original" href="#" target="_blank" rel="noopener noreferrer">Open original ↗</a></div>
</dialog>'''

def shell(title, description, body, page="home", path="", dialogs=""):
    base = "../" if path else ""
    canonical = DOMAIN + "/" + path
    person = {
        "@context": "https://schema.org", "@type": "Person", "name": "Justin Tan",
        "url": DOMAIN + "/", "jobTitle": HOME["role"],
        "sameAs": [s["url"] for s in HOME["socials"]]
    }
    return f'''<!doctype html>
<html lang="en-GB" id="top">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description)}">
<meta name="theme-color" content="#f5f3ed"><link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Justin Tan">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{DOMAIN}/wp-content/uploads/2022/07/JTN04824-1920x1280.jpg">
<meta property="og:image:alt" content="The setting sun beyond a dirt road and open fields, photographed by Justin Tan">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="{base}assets/favicon.svg">
<link rel="stylesheet" href="{base}assets/site.css">
<script src="{base}assets/site.js" defer></script>
<script type="application/ld+json">{json.dumps(person, ensure_ascii=False)}</script>
</head>
<body class="{page}-page">{nav(base, page)}
<main id="main">{body}</main>{footer()}{dialogs}
</body></html>
'''

def video_card(video, base="", compact=False):
    title = video["title"]
    attrs = f'data-video="{e(video["id"])}" data-title="{e(title)}" data-description="{e(video["description"])}"'
    url = "https://www.youtube.com/watch?v=" + video["id"]
    thumb = ROOT / video["thumbnail"]
    image = f'<img src="{e(base + video["thumbnail"])}" width="1280" height="720" alt="" loading="lazy" decoding="async">' if thumb.exists() else ""
    description = e(video["description"]).replace("Chope‘s", '<a href="https://www.chope.co/">Chope</a>‘s')
    full = "" if compact else f'<p class="project-description">{description}</p><p class="project-footer"><a href="{url}" target="_blank" rel="noopener noreferrer">Open on YouTube ↗</a></p>'
    return f'''<article class="project-card" data-category="{e(video["category"])}" id="film-{video["index"]:02d}">
<a class="project-cover" href="{url}" {attrs} aria-label="Play {e(title)}">
<span class="cover-lettering" aria-hidden="true"><span class="micro">{e(video["label"])}</span><span class="cover-title">{e(title)}</span><span class="cover-index">{video["index"]:02d}</span></span>{image}
<span class="play-circle">{icon("play", 21)}</span><span class="play-caption">Play film ↗</span></a>
<div class="project-copy"><div class="project-meta"><span>{e(video["label"])}</span><span>{video["index"]:02d} / 10</span></div>
<h3><a href="{url}" {attrs}>{e(title)}</a></h3>{full}</div></article>'''

def home_page():
    role_words = HOME["role"].rsplit(" ", 1)
    role_heading = (e(role_words[0]) + "<br> <em>" + e(role_words[1]) + ".</em>") if len(role_words) == 2 else e(HOME["role"]) + "."
    aside = e(HOME["aside"]).replace(" love ", " <em>love</em> ")
    frame_items = [(47, "Places", "01"), (1, "People", "02"), (30, "Details", "03")]
    frames = "".join(
        f'<a class="hero-frame" href="photography/#{PHOTOS[n-1]["id"]}" aria-label="Explore photography: {label.lower()}">'
        + photo_image(PHOTOS[n-1], sizes="(max-width:600px) 92vw, (max-width:800px) 58vw, 48vw", eager=(i == 0))
        + f'<span class="hero-frame-label"><span>{num} / {label}</span><span class="arrow-circle">{icon("arrow", 14)}</span></span></a>'
        for i, (n, label, num) in enumerate(frame_items)
    )
    services = "".join(
        f'<a class="service-row" href="{s["href"]}"><span class="micro">{i:02d}</span><div><h3>{e(s["title"])}</h3><p>{service_copy(s["description"])}</p></div><span class="arrow-circle">{icon("arrow", 18)}</span></a>'
        for i, s in enumerate(HOME["services"], 1)
    )
    skills = "".join(f'<li>{e(s)}</li>' for s in HOME["skills"])
    quals = "".join(f'<li>{e(q)}</li>' for q in HOME["qualifications"])
    experiences = []
    for i, exp in enumerate(HOME["experience"], 1):
        extras = ""
        if "url" in exp:
            extras += f'<a class="text-link" href="{e(exp["url"])}" target="_blank" rel="noopener noreferrer">Visit their site {icon("arrow", 13)}</a>'
        if "clients" in exp:
            clients = [f'<a href="{e(c["url"])}" target="_blank" rel="noopener noreferrer">{e(c["title"])}</a>' for c in exp["clients"]]
            extras += f'<p>Some of my past clients include {clients[0]}, {clients[1]} and {clients[2]}.</p>'
        experiences.append(f'<article class="experience-row"><span class="micro">{i:02d}</span><h3>{e(exp["title"])}</h3><div class="experience-body"><p>{e(exp["description"])}</p>{extras}</div></article>')
    content = f'''<section class="container hero" aria-labelledby="hero-heading">
<div class="hero-topline"><p class="eyebrow">{e(HOME["eyebrow"])}</p><span class="micro muted">An independent collection of work</span></div>
<div class="hero-heading"><h1 id="hero-heading">{e(HOME["name"])}<span class="dot" aria-hidden="true">.</span></h1><div class="hero-intro"><p>{e(HOME["tagline"])}</p><a class="text-link" href="#work">Explore my work {icon("down", 17)}</a></div></div>
<div class="hero-collage">{frames}</div><div class="hero-foot"><span class="caption">A few things I’ve seen along the way.</span><span class="caption">Photos / films / stories</span></div>
</section>
<section class="container section" id="work" aria-labelledby="work-title"><div class="section-label"><p class="eyebrow">The things I do</p><span class="index-label">01 / Practice</span></div>
<div class="services-layout"><div class="services-intro"><h2 id="work-title" class="section-title">A little bit of<br><em>everything.</em></h2><p class="micro">Different mediums. Same curiosity.</p></div><div>{services}</div></div></section>
<section class="films-section section" aria-labelledby="films-title"><div class="container"><div class="section-label"><p class="eyebrow">Videography</p><span class="index-label">02 / In motion</span></div>
<div class="section-intro"><h2 class="section-title" id="films-title">A couple of <em>the picks.</em></h2><a class="text-link" href="videography/">All 10 films {icon("arrow", 18)}</a></div>
<div class="project-grid">{video_card(VIDEOS[0], compact=True)}{video_card(VIDEOS[4], compact=True)}</div></div></section>
<section class="container section" id="about" aria-labelledby="about-title"><div class="section-label"><p class="eyebrow">The person behind the work</p><span class="index-label">03 / About</span></div>
<div class="about-grid"><div><div class="about-images"><picture><source type="image/webp" srcset="assets/images/justin-portrait-480.webp 480w, assets/images/justin-portrait-960.webp 960w" sizes="(max-width:600px) 85vw, 35vw"><img class="portrait" src="wp-content/uploads/2022/07/20220716221551_JTN06180-scaled.jpg" width="1707" height="2560" alt="Portrait of Justin Tan wearing a dark shirt" loading="lazy" decoding="async"></picture><picture><source type="image/webp" srcset="assets/images/coast-480.webp"><img class="coast-inset" src="wp-content/uploads/2022/07/photography-8.jpg" width="500" height="735" alt="Black and white photograph of waves breaking on a rocky coastline" loading="lazy" decoding="async"></picture></div><div class="about-caption"><span class="micro">Justin Tan</span><span class="micro muted">{e(HOME["level"])}</span></div></div>
<div class="about-body"><p class="eyebrow">A work in progress</p><h2 class="section-title" id="about-title">{role_heading}</h2>
<p class="description">{e(HOME["description"])}</p><p class="cheese-line">{aside}</p>
<div class="about-stats"><section aria-labelledby="skill-title"><h3 id="skill-title">Skill Points (SP)</h3><ul class="skill-list">{skills}</ul></section><section aria-labelledby="qual-title"><h3 id="qual-title">Qualifications</h3><ul class="qualifications">{quals}</ul></section></div>
</div></div></section>
<section class="container section experience-section" aria-labelledby="experience-title"><div class="section-label"><h2 id="experience-title" class="eyebrow">Experience (EXP)</h2><span class="index-label">04 / Along the way</span></div>
{"".join(experiences)}
<details class="easter-egg"><summary>{e(HOME["easterEgg"]["title"])}</summary><p>{e(HOME["easterEgg"]["description"])}</p></details></section>'''
    return shell("Justin Tan — Creator, Videographer & Photographer", HOME["tagline"], content, dialogs=video_dialog())

def filter_bar(grid_id, categories, items, noun):
    counts = {c: sum(1 for i in items if i["category"] == c) for c in categories}
    buttons = f'<button class="filter" data-filter="all" aria-pressed="true">All <sup>{len(items)}</sup></button>'
    buttons += "".join(f'<button class="filter" data-filter="{e(c)}" aria-pressed="false">{e(c.title() if c.islower() else c)} <sup>{counts[c]}</sup></button>' for c in categories)
    return f'''<div class="filter-bar" data-filters="{grid_id}" data-count="{grid_id}-count" data-noun="{noun}" hidden><div class="filters" role="group" aria-label="Filter {noun}">{buttons}</div><p class="result-count" id="{grid_id}-count" aria-live="polite" role="status">{len(items):02d} {noun}</p></div>'''

def video_page():
    body = f'''<section class="container page-hero" aria-labelledby="page-title"><p class="eyebrow">Videography / 10 selected films</p>
<div class="page-title-row"><h1 class="page-title" id="page-title">the <span class="serif">picks</span><span style="color:var(--orange)">.</span></h1><p class="page-note">{service_copy(HOME["services"][0]["description"])}</p></div></section>
<section class="container portfolio-section" aria-label="Video portfolio">
{filter_bar("video-grid", ["Brand & social", "People & stories", "Personal films"], VIDEOS, "films")}
<noscript><p class="nojs-note">Choose a film to watch it on YouTube.</p></noscript>
<div class="project-grid" id="video-grid">{"".join(video_card(v, "../") for v in VIDEOS)}</div>
</section>'''
    return shell("Videography — Justin Tan", "The picks: 10 films by Justin Tan, from brand campaigns and event teasers to personal stories, travel and documentaries.", body, "video", "videography/", video_dialog())

def photo_page():
    cards = []
    for photo in PHOTOS:
        cards.append(
            f'<figure class="photo-card" id="{photo["id"]}" data-category="{photo["category"]}">'
            f'<a class="photo-link" href="../{e(photo["original"])}" data-photo aria-label="View photograph {photo["index"]:02d}: {e(photo["alt"])}" style="--ratio:{photo["width"]}/{photo["height"]}">'
            + photo_image(photo, "../", eager=(photo["index"] == 1))
            + f'<span class="photo-zoom">{icon("plus", 18)}</span></a>'
            f'<figcaption class="photo-caption"><span>{photo["index"]:02d} / {e(photo["category"])}</span><span>Justin Tan</span></figcaption></figure>'
        )
    body = f'''<section class="container page-hero" aria-labelledby="page-title"><p class="eyebrow">Photography / 48 photographs</p>
<div class="page-title-row"><h1 class="page-title" id="page-title">a mish <span class="serif">mash</span><span style="color:var(--orange)">.</span></h1><p class="page-note">My relatives keep asking me to take passport photos</p></div></section>
<section class="container portfolio-section" aria-label="Photography portfolio">
{filter_bar("photo-grid", ["people", "places", "food"], PHOTOS, "photographs")}
<noscript><p class="nojs-note">Choose any photograph to open the original image.</p></noscript>
<div class="photo-grid" id="photo-grid">{"".join(cards)}</div>
<div class="gallery-bottom"><span>People, places and the details in between.</span><a href="#top">Back to the beginning ↑</a></div></section>'''
    return shell("Photography — Justin Tan", "A mish mash: 48 photographs of people, places, food and everyday moments, by Justin Tan.", body, "photo", "photography/", photo_dialog())

def build():
    pages = {"index.html": home_page(), "videography/index.html": video_page(), "photography/index.html": photo_page()}
    for name, markup in pages.items():
        path = ROOT / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markup, encoding="utf-8")
        print(f"Wrote {name} ({len(markup):,} characters)")
    notfound = f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found — Justin Tan</title><style>body{{margin:0;background:#f5f3ed;color:#20221f;font:17px/1.6 Arial,sans-serif}}main{{padding:15vh 8vw}}small{{color:#bc361c}}h1{{font-size:clamp(60px,10vw,140px);line-height:1;letter-spacing:-.07em;font-weight:500;max-width:900px}}a{{color:inherit;text-underline-offset:6px}}</style></head><body><main><small>JUSTIN / CREATOR · 404</small><h1>A little off the beaten path.</h1><p>That page isn’t here. There’s plenty to explore back at the beginning.</p><a id="home-link" href="{DOMAIN}/">Back to the portfolio ↗</a></main><script>if(location.hostname.endsWith('.github.io')){{document.getElementById('home-link').href=location.pathname.startsWith('/portfolio/')?'/portfolio/':'/';}}</script></body></html>'''
    (ROOT / "404.html").write_text(notfound, encoding="utf-8")
    (ROOT / ".nojekyll").touch()
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f'<url><loc>{DOMAIN}/{p}</loc></url>' for p in ["", "videography/", "photography/"]) + "</urlset>\n", encoding="utf-8")

if __name__ == "__main__":
    build()
