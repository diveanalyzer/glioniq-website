# glioniq-website
Official GlionIQ company website

Two static pages, with no runtime JavaScript, package manager, or third-party dependencies:

- `/` — the complete approved Coming Soon artwork, accessible navigation, and an expandable launch message.
- `/about-us/` — the complete approved company story, rendered from `content/about-us.md`.

## Build and validate

Python 3.9 or later is sufficient:

```sh
python3 scripts/build.py
python3 scripts/verify.py
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/`. The generated HTML is committed, so GitHub Pages does not need to run Python. If approved content changes, regenerate both pages and update the approved checksum only after reviewing the new source.

## Approved artwork

- `public/images/glioniq-coming-soon.PNG` — PNG, 1221 × 1288.
- `public/images/glioniq-logo-official.PNG` — PNG, 1536 × 1024.

Both originals are used byte-for-byte, with proportional sizing and no crop. The supplied logo actually embeds “Grow Your Mind. Enrich Your Life.”; its pixels take precedence over the different tagline described in the build brief. The launch artwork includes navigation and contact text: transparent, keyboard-accessible links make those existing controls functional. The email destination comes from the artwork; mailbox delivery is unverified. Small raster text cannot reflow, so the launch message is also available in an expandable text disclosure and the story has a fully responsive text page.

## Publishing

The existing Pages settings were verified on 2026-11-13: deploy from `main`, `/` (root), legacy branch publishing. `.nojekyll` serves the static files directly. No workflow or publishing-source change is needed. All local links are relative and `/about-us/index.html` supports direct access and refresh.

The existing `CNAME` is `glionic.tech` and is preserved verbatim. At inspection, GitHub reported `InvalidDNSError` and HTTPS enforcement was unavailable because the custom domain's DNS was not configured correctly. The GitHub project URL redirected to that domain. DNS and HTTPS settings were not changed. This domain spelling differs from the email domain embedded in the supplied artwork; neither was silently corrected.

See `VALIDATION.md` for completed checks and verification limits.
