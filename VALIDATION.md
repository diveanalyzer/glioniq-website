# GlionIQ branding validation — 2026-11-14

## Scope and preservation

Work is limited to `/Users/igor/Documents/Repositories/glioniq-website`, repository `diveanalyzer/glioniq-website`, branch `main`. This branding revision started from clean commit `e78fb12e433512ef898ef280b0217a894ac0eb71`, after the initial site was published successfully.

Both original PNGs, the approved story Markdown, and CNAME are byte-for-byte unchanged, protected by SHA-256 assertions. CNAME contains exactly `glioniq.tech`. No DNS/Namecheap settings were changed. The homepage copy, scientific imagery, panels, cards, vision, navigation, and contact content are retained. Only branding, icon metadata, and the redundant About Us logo change.

`BOOST.md`, referenced by the session instructions, was absent from the checkout and checked parent directories. No BoostGraph index exists in this checkout.

## Artwork and icons

- True-alpha derivatives preserve the existing Home hero composition and provide the full official logo including its slogan and emblem as a separate asset. The full derivative is not redundantly displayed on the pages.
- Header and footer branding uses the approved compact brain symbol. About Us retains its title and entire story without a large story logo.
- Every displayed brand is an ordinary keyboard-accessible anchor targeting `/`, labelled “GlionIQ — Home”.
- Browser icons: transparent 16/32-pixel PNGs and a 16/32/48-pixel ICO.
- Home-screen icons: centered brain on deep navy, at 180, 192, and 512 pixels. Both pages reference the Apple icon and web manifest.
- `public/images/branding-provenance.json` records source crops, hashes, processing method, and derivative hashes. No artwork was generated, redrawn, or substituted.

Matting uses measured background samples. Bright source surfaces and protected brain interiors retain their source RGB; edge/glow pixels are unmatted. A flattened PNG cannot establish the exact original alpha channel. The only unobscured brain symbol in the supplied artwork is a **74 × 60** reference crop. Larger exports are resampled and softer than a dedicated high-resolution symbol master; lettering-overlapped anatomy is not reconstructed.

## Automated and HTTP checks

- `python3 scripts/build.py`, `python3 scripts/verify.py`, and `git diff --check` pass.
- All **61 story blocks** match the approved narrative, including punctuation and order.
- Both pages have balanced HTML, English language, one H1, unique IDs, accessible brand links, correct icon metadata, and valid local links/anchors. All **35 local references** resolve; the CSS artwork path also resolves.
- PNG dimensions, real alpha with transparent corners and antialiased edges, ICO entries, navy app-icon backgrounds, manifest icon paths, and derivative hashes pass.
- Local HTTP 200 and exact served-byte checks pass for Home, About Us, all six root icon files, the manifest, and all three transparent derivatives.
- No runtime JavaScript, unverified email destination, external fonts, analytics, forms, or server dependencies were introduced. The temporary browser QA harness is excluded from publication.

## Browser evidence for this branding revision

Safari on macOS:

- Visually inspected the Home hero and compact header, with no visible rectangular logo background on the navy page; About Us opens without its redundant large logo.
- Visually inspected the exported artwork on navy and light backgrounds and the browser/app icon contact sheet.
- The blue brain favicon was visible in Safari's active About Us tab and on a fresh Home URL (`/?branding=bb104b6`). Safari retained its old generic cached favicon on the previously visited bare Home URL, including after a normal reload; existing favicon caches can lag the published files.
- Home hero click returns to `/`; Home Contact navigates to the contact section and its footer brain returns to `/`.
- Main navigation opens About Us; its header brain returns to `/`.
- Home and About Us rendered in same-origin frames with measured viewport widths **320, 390, 768, 1024, and 1440 CSS pixels**: no horizontal overflow, all images loaded, all brand links target `/`, and all icon metadata is present. About Us reports zero story images at every width.
- The 320-pixel About Us header brain opens Home. At 390 pixels, About Us Contact moves focus to the contact section, and its footer brain opens Home.
- Published Home and About Us were visually inspected over HTTPS. Option-Tab focuses the About Us header brain with a visible blue ring; Return opens Home. Keyboard traversal also reaches the Home hero and Return activates its `/` link.

Safari access was temporarily interrupted. After the user reopened its window, the outstanding viewport, mobile interaction, and keyboard checks above were completed against this revision.

These are desktop Safari viewport checks, not physical iPhone/Android home-screen installation tests. Cross-browser/device acceptance and a full assistive-technology audit remain unverified. No offline capability is claimed.

## Publication

Implementation commit `bb104b68e3538ab381872392d33ba28bf3cf97cb` was committed and pushed to the existing `main` branch. GitHub Pages reported `built` for that exact commit; [deployment run 43576413670](https://github.com/diveanalyzer/glioniq-website/actions/runs/43576413670) completed successfully. Existing `main` + `/` publishing, `.nojekyll`, and the `glioniq.tech` CNAME are retained.

Production HTTP 200 and exact local-file byte comparisons pass for **17 resources**: Home, both About Us URL forms, CSS, six root icon files, the manifest, CNAME, both original PNGs, and three transparent derivatives. Requests use normal TLS certificate validation. The manifest is served as `application/manifest+json`; image MIME types are correct. Ordinary Home and About Us URLs also return HTTP 200 without a release query parameter.

GitHub reports an approved certificate for `glioniq.tech` and `www.glioniq.tech`, expiring 2027-02-12. **HTTPS works; enforcement remains disabled (`https_enforced: false`).** A direct HTTP request returns HTTP 200 without redirecting to HTTPS. No Pages setting or DNS/Namecheap configuration was changed by this branding revision.

## Favicon cache revision — 2026-11-14

Starting commit: `25bcee3b895af1887f9439a6036553b25fe37f35`. The existing six icon files were regenerated from the same approved brain crop; their bytes are unchanged. All three ICO frames (16, 32, 48) decode as RGBA, both browser PNGs have transparency, and the 180/192/512-pixel home-screen icons have the intended navy background. No higher-resolution unobscured source was available in the repository.

Both HTML heads now explicitly reference root-relative favicon, Apple touch icon, and manifest URLs with `?v=20261114-2`. Manifest icons use the same version. The ICO has an explicit image MIME type, and the 32-pixel PNG follows the 16-pixel entry. GlionIQ name, start URL, scope, and navy colors are retained.

`scripts/verify.py` passes, including all versioned paths, icon dimensions, alpha, hashes, manifest branding, and all 61 story blocks. Independent Pillow decoding confirms all ICO frames and PNG dimensions. A comparison against the starting commit confirms both complete HTML bodies, CSS, all displayed logo derivatives, original PNGs, story Markdown, and CNAME are byte-for-byte unchanged. `git diff --check` passes. DNS and HTTPS settings are outside this revision; physical iPhone Add to Home Screen has not been tested.
