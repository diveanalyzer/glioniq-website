# GlionIQ validation — 2026-11-14

## Scope and assets

Work is limited to `/Users/igor/Documents/Repositories/glioniq-website`, repository `diveanalyzer/glioniq-website`, branch `main`. Starting tree was clean at `f190358`.

Both approved PNGs are unchanged and protected by SHA-256 assertions. The homepage reference is `public/images/glioniq-coming-soon.PNG`; the official logo is `public/images/glioniq-logo-official.PNG`. Home uses the approved image motifs with responsive HTML typography and functional navigation, preserving its composition and visual identity. This is a responsive reconstruction, not a claim of pixel-for-pixel equivalence. The separate official logo is shown in full without stretching or cropping.

`BOOST.md`, referenced by the session instructions, was absent from the checkout and checked parent directories. No BoostGraph index exists in this checkout.

## Content and static checks

- `python3 scripts/build.py` and `python3 scripts/verify.py` pass.
- All **61 story blocks** match the supplied updated narrative exactly, including punctuation and order. A separate comparison against the original user attachment also passed.
- Both HTML pages have balanced markup, English language, one H1, unique IDs, and valid local links/anchors. All 22 local references resolve. The CSS artwork reference resolves.
- Home copy, complete About Us narrative, Contact sections, correct domain metadata, and copyright are present.
- No unverified mailbox address/link is displayed. The untouched source reference image still contains its original embedded address, outside the regions displayed by CSS.
- Local HTTP 200 and exact served-byte checks pass for Home, both About Us URL forms, CSS, both images, and CNAME.
- No runtime JavaScript, external fonts, libraries, forms, analytics, or server dependencies. Safari's rendered documents report zero scripts; a separate developer-console inspection was not performed.

## Browser checks

Safari on macOS, with same-origin frames measuring actual layout viewport widths:

| Page | Widths in CSS pixels | Result |
| --- | --- | --- |
| Home | 320, 390, 768, 1024, 1440 | No horizontal overflow; all images loaded |
| About Us | 320, 390, 768, 1024, 1440 | No horizontal overflow; all images loaded |

Visually inspected Home's hero, Coming Soon panel, scientific cards, Our Vision and wave artwork, plus the About Us introduction and full logo. Narrow-screen cards stack in one column; desktop/tablet cards remain in three columns. The original reference was opened and compared with the implementation.

Verified by browser interaction:

- Home → About Us through the main navigation.
- Read Our Story → separate About Us page.
- About Us → Home via Home navigation and the logo.
- Contact on both pages → the real contact section, with focus moving to that section.
- About Us direct navigation and refresh.
- Option-Tab reveals the skip link with a visible blue focus ring; keyboard traversal and Return open About Us.

These are desktop Safari viewport tests, not physical iPhone, iPad, or Android device tests. Chrome/Android, a full assistive-technology audit, and OS-level reduced-motion emulation were not performed. The site has no entrance or looping animations; optional link transitions are limited to users allowing motion.

## Publication checks

Existing Pages configuration was verified through GitHub's API: `main`, `/`, legacy branch publishing. Root CNAME was corrected to `glioniq.tech` with explicit owner authorization; `.nojekyll` is retained. No workflow or DNS configuration changes are required.

Before publishing, `glioniq.tech` resolved to all four GitHub Pages IPv4 addresses, and `www.glioniq.tech` had CNAME `diveanalyzer.github.io`. HTTPS initially failed certificate hostname validation while GitHub still held the old domain; this resolved after the domain correction.

Implementation commit `d9c144eb340af2a0c812007383e2a4bf709fba3e` was pushed successfully. A concurrent remote CNAME correction (`1019c0c`) was preserved by rebasing the unpublished implementation; the only conflict was a trailing newline in the same approved domain value. No force push was used.

GitHub Pages reported `built` for the implementation commit, and [deployment run 43572596911](https://github.com/diveanalyzer/glioniq-website/actions/runs/43572596911) completed successfully. The Pages API confirms `glioniq.tech`, `main`, and `/`; domain health reports valid apex and www DNS.

Production checks over normally validated HTTPS returned HTTP 200 and exact local-file bytes for Home, `/about-us/`, `/about-us/index.html`, CSS, both original PNGs, and CNAME. The ordinary Home and About URLs also return HTTP 200. `https://www.glioniq.tech/` redirects to `https://glioniq.tech/`. GitHub reports an approved certificate covering both hostnames, expiring 2027-02-12.

HTTPS is active and verified. The existing `https_enforced: false` setting is unchanged: HTTP remains available without an automatic HTTPS redirect. No DNS/Namecheap settings were modified.

## Remaining verification limits

Physical-device/cross-browser acceptance remains unverified. Contact information must be supplied and verified before a real email destination or submission flow is enabled.
