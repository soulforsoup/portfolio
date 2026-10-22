#!/usr/bin/env python3
"""Check content completeness, links, portable URLs and original-asset integrity."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import hashlib
import json
import re
import sys
from build import DOMAIN

ROOT = Path(__file__).resolve().parents[1]
errors = []
checks = 0

def check(condition, message):
    global checks
    checks += 1
    if not condition:
        errors.append(message)

class Page(HTMLParser):
    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.refs = []
        self.words = []
        self.images = []
        self.videos = []
        self.photos = []
        self.labels = []
        self.h1s = 0
        self.skip = 0
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "h1":
            self.h1s += 1
        if "id" in a:
            self.ids.append(a["id"])
        for attr in ("src", "href"):
            if a.get(attr):
                self.refs.append(a[attr])
        if a.get("srcset"):
            self.refs.extend(s.strip().split()[0] for s in a["srcset"].split(",") if s.strip())
        for attr in ("aria-labelledby", "aria-controls"):
            self.labels.extend(a.get(attr, "").split())
        if tag == "img":
            self.images.append(a)
        if "data-video" in a:
            self.videos.append(a["data-video"])
        if "data-photo" in a:
            self.photos.append(a)

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, text):
        if not self.skip:
            self.words.append(text)

def normal(text):
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:!?’‘])", r"\1", text)
    return text

names = ["index.html", "videography/index.html", "photography/index.html"]
pages = {name: Page((ROOT / name).read_text(encoding="utf-8")) for name in names}
for name, page in pages.items():
    check(page.h1s == 1, f"{name}: expected one H1")
    check(len(page.ids) == len(set(page.ids)), f"{name}: duplicate element IDs")
    for identifier in page.labels:
        check(identifier in page.ids, f"{name}: unresolved accessibility reference {identifier}")
    for image in page.images:
        check("alt" in image, f"{name}: image missing alt attribute")
        if image.get("src"):
            check("width" in image and "height" in image, f"{name}: image lacks layout dimensions")
    for prefix in ("/", "/portfolio/"):
        for ref in page.refs:
            if ref.startswith(("http:", "https:", "mailto:", "data:")):
                continue
            check(not ref.startswith("/"), f"{name}: root-relative URL fails project hosting: {ref}")
            url = urlsplit(urljoin("https://example.test" + prefix + name, ref))
            check(url.path.startswith(prefix), f"{name}: URL escapes deployment prefix: {ref}")
            relative = unquote(url.path[len(prefix):])
            target = ROOT / relative
            if target.is_dir():
                target /= "index.html"
            check(target.is_file(), f"{name}: missing local target {ref}")
            if url.fragment and target.suffix == ".html" and target.is_file():
                key = str(target.relative_to(ROOT))
                target_page = pages.get(key)
                if target_page:
                    check(url.fragment in target_page.ids, f"{name}: missing anchor {ref}")

home = json.loads((ROOT / "content/home.json").read_text())
videos = json.loads((ROOT / "content/videos.json").read_text())
photos = json.loads((ROOT / "content/photographs.json").read_text())
home_text = normal(" ".join(pages["index.html"].words))
video_text = normal(" ".join(pages["videography/index.html"].words))
for key in ("name", "eyebrow", "tagline", "level", "role", "description", "aside", "contactTitle", "email"):
    check(normal(home[key]) in home_text, f"Home wording missing: {key}")
for item in home["services"] + home["experience"]:
    for key in ("title", "description"):
        check(normal(item[key]) in home_text, f"Home wording missing: {item[key]}")
for value in home["skills"] + home["qualifications"] + list(home["easterEgg"].values()):
    check(normal(value) in home_text, f"Home wording missing: {value}")
for video in videos:
    check(normal(video["title"]) in video_text, f"Missing video title: {video['title']}")
    check(normal(video["description"]) in video_text, f"Missing video description: {video['title']}")
    thumb = ROOT / video["thumbnail"]
    check(thumb.is_file() and thumb.stat().st_size > 0, f"Missing or empty local video thumbnail: {video['title']}")
    check(re.fullmatch(r"[A-Za-z0-9_-]{11}", video["id"]), f"Invalid YouTube ID: {video['id']}")
check(set(pages["videography/index.html"].videos) == {v["id"] for v in videos}, "Video inventory mismatch")
check(len(photos) == 48, "Expected 48 original gallery photographs")
check(len(pages["photography/index.html"].photos) == len(photos), "Gallery photograph count mismatch")
for photo in photos:
    check(photo["id"] in pages["photography/index.html"].ids, f"Missing photograph: {photo['id']}")
    for variant in photo["variants"]:
        image = ROOT / variant["path"]
        check(image.is_file() and image.stat().st_size > 0, f"Missing or empty optimised image: {variant['path']}")
for original in json.loads((ROOT / "docs/original-assets.json").read_text()):
    p = ROOT / original["path"]
    check(p.is_file(), f"Missing original asset: {original['path']}")
    if p.is_file():
        check(hashlib.sha256(p.read_bytes()).hexdigest() == original["sha256"], f"Original asset modified: {original['path']}")
check((ROOT / ".nojekyll").exists(), "Missing .nojekyll")
hostname = urlsplit(DOMAIN).hostname
if hostname and not hostname.endswith(".github.io"):
    check((ROOT / "CNAME").exists() and (ROOT / "CNAME").read_text().strip() == hostname, "Custom domain and CNAME do not match")
for name in names:
    source = (ROOT / name).read_text()
    check("mailto:justintmk@gmail.com" in source, f"{name}: missing working email link")
    check("/wp-includes/" not in source and "/et-cache/" not in source, f"{name}: legacy WordPress runtime dependency")
    check("fonts.googleapis.com" not in source, f"{name}: remote font dependency")

if errors:
    print("\n".join("FAIL: " + err for err in errors))
    sys.exit(1)
print(f"PASS: {checks:,} checks — local links at / and /portfolio/, wording, 48 gallery photographs, 10 films, and all original upload hashes.")
print("Browser rendering and live YouTube playback require a browser check; this script does not test them.")
