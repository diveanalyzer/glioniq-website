# GlionIQ

Official static company website for **glioniq.tech**, published from the existing `main` branch and repository root on GitHub Pages.

- `/` — responsive implementation of the approved Home reference, with real text, scientific artwork, three cards, Our Vision, and Contact.
- `/about-us/` — the complete updated company story, generated from `content/about-us.md`.
- Both pages include Home, About Us, Contact, accessible keyboard navigation, and linked branding.

## Build and validate

Python 3.9 or later; normal HTML builds and validation have no third-party dependencies:

```sh
python3 scripts/build.py
python3 scripts/verify.py
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/`. Generated HTML is committed; GitHub Pages needs no Python build step. After reviewing approved content changes, update its checksum in the verifier and regenerate the HTML.

## Approved artwork

Originals remain byte-for-byte unchanged:

- `public/images/glioniq-coming-soon.PNG` — 1221 × 1288, the approved homepage reference.
- `public/images/glioniq-logo-official.PNG` — 1536 × 1024, the complete official logo.

Home retains the reference composition, blue/gold palette, brain and wordmark, neural imagery, illuminated panel, cards, separators, and footer waves. The hero uses a true-alpha derivative of its existing approved reference crop. Headers and footers use the compact brain symbol; About Us has no redundant story logo. Every displayed brand links to `/` with an accessible label. On narrow screens the navigation wraps and the cards stack vertically.

`scripts/build_brand_assets.py` removes the measured navy background without generating or redrawing artwork. It creates transparent full-logo, hero, and brain derivatives, transparent browser favicons, and navy home-screen icons. `public/images/branding-provenance.json` records source hashes, crop coordinates, output hashes, and limitations. Bright surfaces and protected brain interiors retain source RGB; edge/glow colors are unmatted. Exact recovery of an original alpha channel from flattened PNGs is not claimed.

The unobscured approved brain symbol is a **74 × 60** crop from the reference. The larger brains overlap lettering, so hidden anatomy is not reconstructed. Larger icon exports are resampled and can look softer than a dedicated high-resolution symbol master. For optional asset regeneration, install `scripts/branding-requirements.txt` into an isolated virtual environment and run `scripts/build_brand_assets.py`. These packages are not needed by the site or GitHub Pages.

Both pages reference the 16/32-pixel PNG favicons, multi-size ICO, 180-pixel Apple touch icon, and `site.webmanifest` with 192/512-pixel Android icons. The manifest supplies home-screen presentation metadata; no service worker or offline capability is provided.

The reference PNG contains an email address. That part is not displayed on the site, and no email link is published because the mailbox is unverified. Contact navigates to a real section explaining that contact details will be shared when ready; it does not claim to send messages.

## GitHub Pages

The existing `main` + `/` branch publishing configuration and `.nojekyll` are retained. Brand links target the custom-domain root `/`; other internal navigation and asset references are relative. The root `CNAME` remains exactly `glioniq.tech`, following the earlier owner-authorized correction. Canonical and social metadata use this domain. DNS/Namecheap settings are not changed.

See `VALIDATION.md` for verification evidence and limits.
