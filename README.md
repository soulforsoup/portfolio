# justintan.work

Personal portfolio of Justin Tan — videography, photography and web design. Plain HTML, CSS and a little JavaScript; no build step, hosted on GitHub Pages at [justintan.work](https://justintan.work).

## Structure

```
index.html               Home: intro, services, selected work, character sheet, contact
videography/index.html   Video portfolio (YouTube, click-to-play)
photography/index.html   Photo gallery with filters and lightbox
404.html                 Not-found page
assets/css/style.css     All styles
assets/js/main.js        Header, reveals, video players, filters, lightbox, level counter
assets/img/photos/       Gallery photos, each at 480 / 980 / 1280 / 1920 px wide
assets/img/site/         Portrait, hero image, favicon
CNAME, .nojekyll         GitHub Pages config
```

## Common edits

- **Add a photo** – export it at 480, 980, 1280 and 1920 px wide as `assets/img/photos/NAME-480.jpg` etc. Copy any `<figure class="shot">` block in `photography/index.html`, update the file names, `width`/`height` (of the 480 version), `data-w`/`data-h` (of the 1920 version), the `alt` text and `data-cat` (`people`, `events`, `food` or `places`). Update the count in the matching filter button.
- **Add a video** – copy an `<article class="video-card">` in `videography/index.html` and change the YouTube ID in `data-yt` and the thumbnail URL.
- **Level** – the “Lv.” badge on the home page is worked out from `data-born` on page load, so it goes up on each birthday automatically.

## Run locally

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploy

GitHub → Settings → Pages → *Deploy from a branch* → `main` / root. The `CNAME` file keeps the custom domain.
