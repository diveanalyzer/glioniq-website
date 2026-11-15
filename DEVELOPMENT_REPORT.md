# GlionIQ v2 local development report

Date: 2026-11-15. Branch: `development/glioniq-homepage-v2`.

## Scope and publication status

The complete 14-page corporate website is implemented locally. No push, merge, deployment or public preview was performed. Production `main` remains at `479a153aa9b767ad47b3f919dd7b55f3261f4ca2`. CNAME, DNS, HTTPS and GitHub Pages settings were not changed. Local preview: <http://127.0.0.1:8787/>.

## Files

Modified: `index.html`, `about-us/index.html`, `assets/site.css`, `scripts/build.py`, `scripts/verify.py`, `README.md`.

Created: generated pages under `science/`, `blog/`, `contact/`, `journey/`, `search/`, and `laboratories/`; `assets/site.js`; `assets/search-index.json`; `content/platforms.json`; `content/pages.json`; `content/articles.json`; `public/images/development/` artwork and provenance; `scripts/verify_interactions.js`; `scripts/verify_http.py`; `scripts/responsive-qa.html`; this report. The supplied `design/glioniq-homepage-approved.png` is preserved and included as the design source.

## Design and functionality

The homepage follows the approved composition: compact branding and navigation, side-by-side desktop hero, three illuminated platform cards, a separate native NeuroPath disclosure with four labs, four lower navigation blocks and Earth-horizon CTA. Mobile hero and cards stack. Typography and responsive spacing adapt to screen width; this is a functional interpretation, not a pixel-identical screenshot.

Actual approved product artwork is cropped from the supplied reference. Existing transparent GlionIQ hero artwork is reused. Text, buttons, navigation, laboratory links and search are HTML. All GlionIQ branding links Home. Product identity is retained without substituting generated logos. No removed Trampolina badge or fixed age restriction was introduced.

Pages describe development state honestly. Known signature activities remain in their approved labs. No games, fake store links, invented articles/authors, unverified contact details or data-collecting forms were added. Future approved articles support metadata, body sections and source links, and appear in the blog and search index after rebuilding.

## Local preview routes

| Page | URL |
| --- | --- |
| Home | http://127.0.0.1:8787/ |
| About Us | http://127.0.0.1:8787/about-us/ |
| Trampolina | http://127.0.0.1:8787/laboratories/trampolina/ |
| Dr. Quiz | http://127.0.0.1:8787/laboratories/dr-quiz/ |
| NeuroPath | http://127.0.0.1:8787/laboratories/neuropath/ |
| Memory Lab | http://127.0.0.1:8787/laboratories/neuropath/memory/ |
| Attention Lab | http://127.0.0.1:8787/laboratories/neuropath/attention/ |
| Logic Lab | http://127.0.0.1:8787/laboratories/neuropath/logic/ |
| Flexibility Lab | http://127.0.0.1:8787/laboratories/neuropath/flexibility/ |
| Science & Research | http://127.0.0.1:8787/science/ |
| Blog & Insights | http://127.0.0.1:8787/blog/ |
| Contact | http://127.0.0.1:8787/contact/ |
| Join Our Journey | http://127.0.0.1:8787/journey/ |
| Search | http://127.0.0.1:8787/search/ |

## Verification performed

- Static verification: 14 balanced English pages, one H1 per page, unique IDs, 398 valid internal references including fragments, shared navigation and consistent icon declarations.
- All 61 About Us story blocks match the approved source in order, including punctuation. All 16 pre-existing protected branding/story/domain/hosting files match the baseline bytes.
- Existing favicon PNG dimensions/alpha, ICO 16/32/48 frames, Apple 180px and Android 192/512px icons, manifest and derivative hashes pass.
- Local HTTP verification: 41 distinct page/asset/icon URLs return 200, with bodies identical to local files. This is local-server evidence, not a new production deployment.
- Safari viewport harness: all 14 pages at 320, 390, 768, 1024 and 1440px passed (70 combinations), with no horizontal overflow, clipped platform cards, missing HTML images or captured JavaScript/resource errors. Mobile navigation state matched the breakpoint. The complete viewport suite passed again after the final navigation, phone layout and Earth artwork refinements.
- Safari visual inspection: desktop hero/cards/lab tree/footer and mobile/tablet hero, laboratory and About Us layouts compared with the supplied reference. Three desktop cards align; original product artwork, navy/blue/gold identity and logo transparency are retained. A stray text fragment in the initial Earth crop was identified visually and removed from the derivative; the source remains unchanged. Phone laboratories use a readable two-column arrangement.
- Safari interactions: 320px menu opened with Space and closed with Escape, restoring focus; NeuroPath disclosure collapsed by click and reopened with Space without navigation; Logic Lab link opened the correct page and displayed NeuroWeave and CodeQuest. The mobile world CTA scrolled to Our Laboratories, and the About Us header brand returned Home.
- Safari search integration passed: a direct NeuroWeave query returned the correct Logic Lab URL, and no-result/blank states worked. Manual header search navigation, query submission and Enter-key submission were observed.
- Search tests passed: real indexed destinations, case/whitespace handling, all-term matching, approved activity lookup, empty and no-result queries, no index mutation. JavaScript syntax passed. Executed through the available Node runtime because a standalone `node` CLI is not installed locally.
- Future article generator passed using a temporary synthetic fixture outside the website output: body, metadata, sources, listing and search inclusion. No sample article remains in the website.
- Main text colors on the navy content panel have measured contrast ratios of 10.61:1 to 14.09:1. Reduced-motion CSS disables transitions, animations and smooth scrolling. Controls have keyboard focus styles; principal controls are at least 44px high.
- `git diff --check` passed.

## Remaining review items and limits

- Safari access was restored and all previously blocked browser checks were completed. Repeatable local viewport and search checks remain available at `/scripts/responsive-qa.html`. The normal homepage is left open for owner review.
- Viewport checks used Safari desktop frames at the specified CSS widths. Physical iPhone/Android touch behavior, Add to Home Screen installation, cross-browser behavior and a full screen-reader audit were not tested.
- Standalone high-resolution official Trampolina, Dr. Quiz and NeuroPath assets were not supplied. The approved reference crops preserve their appearance but can look softer when enlarged. Suggested asset names: `trampolina-logo-transparent.png`, `dr-quiz-logo-transparent.png`, `neuropath-logo-transparent.png`.
- Light Paths remains unassigned because this repository does not verify its laboratory category. No other project was modified or used to invent its placement.
- Product release availability, contact channels and approved editorial material still need owner-provided confirmation. Honest placeholders remain.
- Owner approval of the rendered local implementation is required before any publishing work.

## Browser automation note

During Safari recovery, a paste action unexpectedly placed previous clipboard text into the address bar. Navigation was canceled and subsequent addresses used direct field entry. The tool output does not establish whether Safari issued an external search request. No website content was published and no production settings were changed.

Development completed. Awaiting owner approval before publishing to GitHub Pages.
