# GlionIQ website

Static HTML, CSS and lightweight JavaScript for `glioniq.tech`. The v2 website is developed **locally only** on `development/glioniq-homepage-v2`. Do not push, merge or deploy until the owner explicitly approves publication. The production `main` branch, GitHub Pages configuration, CNAME, DNS and HTTPS are unchanged.

## Build and preview

Python 3.9+ is sufficient; normal builds have no package dependencies:

```sh
python3 scripts/build.py
python3 scripts/verify.py
node scripts/verify_interactions.js
python3 -m http.server 8787 --bind 127.0.0.1
```

Open <http://127.0.0.1:8787/>. With the server running, `python3 scripts/verify_http.py` checks local HTTP responses. Open `/scripts/responsive-qa.html` for the browser viewport and search integration checks. Generated HTML is tracked so a future approved GitHub Pages release needs no Python build step. The search test uses Node's built-in modules; Node is not a website runtime dependency.

## Content and routes

- Home: `/`; approved composition from `design/glioniq-homepage-approved.png`.
- About: `/about-us/`; all 61 approved blocks come unchanged from `content/about-us.md`.
- Platforms and four NeuroPath laboratories: `content/platforms.json`.
- Science, Blog, Contact and Journey: `content/pages.json`.
- Search: `/search/`, generated `assets/search-index.json`, and `assets/site.js`.
- Future articles: `content/articles.json`. The approved article list is intentionally empty. Each article supports a unique slug, title, category, ISO publication date, optional author, summary, body sections and relevant source links. Adding an approved article creates its page, blog listing and search entry on the next build. Rebuilds do not automatically delete previously generated article directories; remove a withdrawn article's output deliberately during editorial review.

Search is case-insensitive, matches all query terms against the local website index, handles empty queries and no results, and links directly to matching pages. No external search provider or data collection is used. The mobile menu and NeuroPath disclosure use native HTML controls. JavaScript enhances mobile state, Escape handling and search; content/navigation remain usable without it. Reduced-motion preferences are respected.

## Artwork and preserved icons

The two original PNGs and approved design reference remain unchanged. Existing transparent GlionIQ hero/brain assets, favicon files, Apple touch icon, Android icons and `site.webmanifest` are preserved. Every generated page shares the existing icon cache version `20261114-2`.

`public/images/development/` contains crops of the supplied approved reference, plus a transparent compact header crop of the original coming-soon artwork. `provenance.json` records the source hash, crop boxes and limitations. The product cards use the actual approved artwork; headings, descriptions, navigation, buttons, tree and search are HTML, not a screenshot of the page. The Earth crop has its embedded button removed with alpha so the real CTA remains interactive.

Separate high-resolution transparent product masters were not supplied. For sharper exports, supply approved Trampolina, Dr. Quiz and NeuroPath logo/artwork files (suggested names: `trampolina-logo-transparent.png`, `dr-quiz-logo-transparent.png`, `neuropath-logo-transparent.png`). The current reference crops are faithful but limited by their source resolution. No substitute logos or missing brain anatomy were generated.

The existing `scripts/build_brand_assets.py` is an optional authoring tool using `scripts/branding-requirements.txt`. **Do not run it for routine v2 builds**: current favicon and home-screen icon files must remain unchanged. Their prior provenance is in `public/images/branding-provenance.json`.

## Content limits

Product availability is not independently verified in this website repository, so planned areas and development status are explicit. NeuroWeave and CodeQuest remain in Logic Lab; Memory Lab remains in Memory Lab. Light Paths is named only on the NeuroPath overview, with its category awaiting confirmation. No games, fake store links, invented publications, contact details or subscription forms are included.

See `DEVELOPMENT_REPORT.md` for local acceptance evidence and remaining review items. `VALIDATION.md` records earlier production work and is historical; it is not evidence that v2 has been deployed.
