# GlionIQ

Official static company website for **glioniq.tech**, published from the existing `main` branch and repository root on GitHub Pages.

- `/` — responsive implementation of the approved Home reference, with real text, scientific artwork, three cards, Our Vision, and Contact.
- `/about-us/` — the complete updated company story, generated from `content/about-us.md`.
- Both pages include Home, About Us, Contact, accessible keyboard navigation, and linked branding.

## Build and validate

Python 3.9 or later; no package manager or third-party dependencies:

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

Home retains the reference composition, blue/gold palette, brain and wordmark, neural imagery, illuminated panel, cards, separators, and footer waves. CSS displays the relevant original reference motifs, while readable HTML supplies the text and controls. No replacement artwork or logo is generated. The full separate official logo is displayed proportionally, without cropping, on About Us and in both footers. On narrow screens the navigation wraps and the cards stack vertically.

The reference PNG contains an email address. That part is not displayed on the site, and no email link is published because the mailbox is unverified. Contact navigates to a real section explaining that contact details will be shared when ready; it does not claim to send messages.

## GitHub Pages

The existing `main` + `/` branch publishing configuration and `.nojekyll` are retained. All internal links are relative, including direct About Us access. The root `CNAME` is `glioniq.tech`, corrected from `glionic.tech` with explicit owner authorization on 2026-11-14. Canonical and social metadata use the corrected domain. DNS/Namecheap settings are not changed.

See `VALIDATION.md` for verification evidence and limits.
