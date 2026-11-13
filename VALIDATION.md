# GlionIQ validation — 2026-11-13

## Implementation

- Repository: existing `diveanalyzer/glioniq-website`, branch `main`.
- Static root Home and `/about-us/` pages, shared CSS, canonical approved Markdown, and standard-library Python generator/verifier.
- Existing `CNAME` and original asset bytes preserved. No pre-existing workflow or application code was present.
- `BOOST.md` referenced in the session instructions was absent from the checkout and checked parent locations.
- Full supplied company story preserved, including its cautious scientific wording.

## Local verification

- Production HTML generated successfully with `python3 scripts/build.py`.
- Automated checks: approved story checksum, both image checksums, exact story block wording/punctuation/order, balanced HTML, English language, one H1 per page, unique IDs, relative links, file and anchor targets.
- Local HTTP checks cover both direct page URLs, the CSS and both PNGs.
- Safari desktop: visually inspected the full Home artwork, About introduction, scientific sections, three life-stage columns, closing slogan, and footer. No clipping observed in inspected views.
- Responsive Safari frames: Home at 320 × 700; About at 320 × 700, 390 × 844, and 768 × 900. Inspected narrow headers, readable paragraphs, stacked mobile life stages, and tablet columns. These are desktop Safari frames, not physical iPhone/iPad verification.
- Home → About, logo → Home, About refresh, and expandable launch-message interaction verified in Safari.
- Keyboard: Option-Tab revealed the visible skip-link focus ring; Option-Tab navigation and Return successfully opened About. Semantic headings and accessible link names were visible in Safari's accessibility tree.
- Reduced-motion support reviewed in CSS: entrance animation applies only for `prefers-reduced-motion: no-preference`. OS-level reduced-motion emulation was not performed.
- No runtime JavaScript or external font/library requests. Browser developer-console inspection and a full automated accessibility audit were not performed.

## Known limitations

- The immutable launch image contains small raster text, which becomes small on phones. Accessible navigation, an expandable readable launch message, and the full text About page supplement it without changing the artwork.
- Embedded email `info@glioniq.tech` is supplied in the artwork; mailbox existence and delivery were not tested.
- Before deployment, the existing custom domain `glionic.tech` failed DNS resolution and GitHub's DNS validation. HTTPS enforcement was already unavailable. Public accessibility requires resolution of that existing domain configuration by the domain owner; no DNS or domain setting was changed.
