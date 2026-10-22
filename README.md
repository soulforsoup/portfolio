# Justin Tan — portfolio

A complete static portfolio for [justintan.work](https://justintan.work/), rebuilt from the original site and [soulforsoup/portfolio](https://github.com/soulforsoup/portfolio).

Warm paper, charcoal and orange; large photography; a video collection; a filterable photo gallery; and the original personal copy. Plain HTML, CSS and JavaScript. **No npm install, framework, WordPress, server or build service is required.**

## Publish on GitHub Pages

1. Put the contents of this folder in the root of the `soulforsoup/portfolio` repository. Replace the three existing HTML pages and add the new folders and files. Keep the included `.nojekyll` file.
2. Commit to the branch you want to publish.
3. In **Settings → Pages → Build and deployment**, choose **Deploy from a branch**, select the branch and **/(root)**, then **Save**. If the repository already publishes that branch and folder, the existing setup can be retained.
4. Keep `CNAME` containing `justintan.work` when retaining the current custom domain. Existing DNS settings are not changed by these files. Check the Pages settings and HTTPS state after publishing.

See GitHub's official [publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) and [site-creation instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

### Use the default GitHub Pages address instead

All normal page, image, stylesheet and script links are relative and support `https://soulforsoup.github.io/portfolio/`. To intentionally move away from the existing custom domain, remove `CNAME`, change `DOMAIN` in `scripts/build.py` to `https://soulforsoup.github.io/portfolio` and regenerate the pages. This updates canonical URLs, social-image URLs, the sitemap and robots file too. Do not change domain settings just to review the redesign.

## Preview locally

From this folder, run:

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000/`. The site is already built. For a no-server review, use the separate self-contained `justin-tan-preview.html` deliverable. That preview is not the deployment source; its photographs are reduced in size to keep it portable.

YouTube playback needs an internet connection and a browser that can reach YouTube. Video files were never stored in the original repository; the existing YouTube videos are preserved as embeds, with local thumbnails and direct YouTube links.

## Edit the site

| What to change | Where |
| --- | --- |
| Bio, services, experience, qualifications, email, socials | `content/home.json` |
| Video titles, descriptions, YouTube IDs and categories | `content/videos.json` |
| Photo sequence, alt text, categories and image paths | `content/photographs.json` |
| Colours, typography, spacing and responsive layouts | `assets/site.css` |
| Mobile navigation, filters, video player and photo viewer | `assets/site.js` |
| Shared HTML, page composition and metadata | `scripts/build.py` |

After changing content or templates:

```sh
python3 scripts/build.py
python3 scripts/check.py
node --check assets/site.js
```

Commit the generated `index.html`, `videography/index.html` and `photography/index.html` too. The Python generator uses only the standard library. Node is only used by the optional JavaScript syntax check, not by the site.

The photo totals and the content-preservation checks describe this migration. Update those intentional expectations when adding or removing work in future.

## Included

- Home, Videography and Photography at the existing routes, plus a custom 404 page.
- All 48 gallery photographs and both original homepage photographs.
- All **198 original upload files**, unchanged, including the original responsive JPEG variants. Their original paths still work.
- Responsive WebP copies for the redesigned pages, with original JPEG fallbacks.
- All 10 original video titles, descriptions and YouTube IDs; 10 downloaded local video thumbnails.
- Original biography, experience, qualifications, service descriptions, email address, social links and the Side Character easter egg.
- Photo and film filters, a full-resolution photo viewer, arrow-key/swipe navigation, and an on-demand video player.
- Visible focus states, a skip link, labelled dialogs, reduced-motion support and useful behaviour without JavaScript.
- Existing `CNAME`, `.nojekyll`, canonical/social metadata, a sitemap and robots file.

## Content notes

The original wording is intentionally retained, including “an amalgation”, “commisioned”, “it’s relations”, the playful service descriptions and “Lv. 28”. The level is not a newly verified statement of age. Review these if you want a copy-editing pass.

The original broken `mailto:/#` has been corrected to `mailto:justintmk@gmail.com`. Redundant WordPress interface labels and plugin branding have been removed. The design adds short navigation and section labels; it does not invent clients, job titles, awards or project outcomes.

## Verification

`scripts/check.py` verifies local references at both root and project-path deployments, content coverage, media counts, original file hashes, accessible ID references and basic page structure. `node --check` verifies JavaScript syntax. All downloaded thumbnails and optimised images were decoded and inspected during preparation.

**An interactive browser and live video playback were not tested in the preparation environment.** Before switching the live site, check the preview on a desktop and a phone, try the filters and dialogs, and play a video from an HTTP/HTTPS origin. YouTube may reject playback when a preview is opened directly as a local file; the direct YouTube links remain available.

The source files are prepared for review and publication. No remote branch, repository settings, DNS or live site was changed.

## Media rights

Original portfolio photographs and writing remain the property of their respective owners. The repository does not grant a general reuse licence for the media.
