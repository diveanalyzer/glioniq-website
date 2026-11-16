# GlionIQ — local development phase two

Verification date: 2026-11-16. Repository: `/Users/igor/Documents/Repositories/glioniq-website`. Branch: `development/glioniq-homepage-v2`. Nothing was pushed, merged or published.

The local implementation adds four platform cards, a shared laboratory explorer, thirteen missing platform/branch routes, NeuroBreath product information and a local editorial workspace. The public release remains unchanged. Production CMS authentication, role enforcement and publishing are intentionally incomplete pending external infrastructure and owner activation.

**Local review URLs — server confirmed on loopback port 8787**

- [Homepage and four platforms](http://127.0.0.1:8787/)
- [NeuroBreath](http://127.0.0.1:8787/laboratories/neurobreath/)
- [Blog destination](http://127.0.0.1:8787/blog/) and [Science destination](http://127.0.0.1:8787/science/)
- [Local Editorial Studio](http://127.0.0.1:8787/admin/)
- After opening the Studio: [Blog article template](http://127.0.0.1:8787/preview/blog/) and [Science article template](http://127.0.0.1:8787/preview/science/)
- [Full route/width QA](http://127.0.0.1:8787/scripts/responsive-qa.html?v=resume-20261116) and [Explorer/editor browser QA](http://127.0.0.1:8787/scripts/phase2-qa.html?v=phase2-final)

The preview binds only `127.0.0.1`; it is not a public preview deployment. If it is stopped, run `python3 -B scripts/serve.py --port 8787`. Open `/admin/` again after a restart to establish a new local session. One clearly labelled browser QA draft is retained in the ignored `.local-cms/` folder; it is not in public content or Git.

**Preservation and Git evidence**

- `903d901` — local checkpoint retaining the owner's existing approved full-width Hero CSS.
- `e3a7058` — local four-platform explorer and editorial workspace implementation, 51 files.
- Prior local development commit `b0889f1` remains intact.
- Local and remote `main` both remain `479a153aa9b767ad47b3f919dd7b55f3261f4ca2`.
- Hero section HTML is byte-identical to the checkpoint. Existing CSS is retained as an unchanged prefix; new rules target laboratories/editorial components. No official artwork was edited or regenerated.
- Original PNGs, approved design reference, CNAME and About Us Markdown match their existing protected hashes. All 61 approved story blocks match exactly, including order and punctuation. About Us generated HTML changes only CSS/JS cache-version URLs.
- CNAME remains exactly `glioniq.tech` plus its existing newline. No obsolete `glionic.tech` occurrence was found in active configuration/content/assets checked.
- Generated pages now use content-hashed CSS/JS URLs. Search requests revalidate the index. This prevents old browser cache entries from mixing the previous three-platform interface with the new local pages.

**Implemented platform and tree structure**

| Platform | Branches | Evidence / qualification |
|---|---|---|
| Trampolina | Colors; Numbers; Shapes; Letters; Memory & Perception; Thinking & Logic | Preserves the actual sibling project's curricula and cognitive worlds. Six real areas replace the proposed speculative grouping. No public release is claimed. |
| Dr. Quiz | Challenge Me; Party Quiz; Discover & Learn | Exactly the three owner-confirmed experiences. |
| NeuroPath | Memory Lab; Attention Lab; Logic Lab; Flexibility Lab | Signature Memory Lab remains in Memory; NeuroWeave and CodeQuest remain in Logic. Light Paths remains unassigned. |
| NeuroBreath | Square Focus; Sleep Calm; Neural Wave | Custom Breathing is a future configuration feature, not a fourth branch. |

Detailed content provenance is in [content/laboratories.sources.md](content/laboratories.sources.md). Existing NeuroPath activity text and route organization were preserved. New pages include purpose, audience, development status and return navigation. No fake download links or invented released games were added.

The homepage uses a 2×2 desktop grid and one-column narrow mobile layout in the specified order. The exact approved four-platform subtitle is present. One platform at a time expands into the desktop section's center; the other three remain visible as secondary cards. The connected branches use blue/gold nodes and lines. Hover dwell is 300 ms, region-leave delay 500 ms and transitions 500 ms. Leaving a single card does not close the tree. Focused keyboard interactions are retained rather than dismissed by pointer exit. A separate Explore link navigates, while the disclosure/tap opens branches. Close and Escape restore the disclosure focus. Native details provide a no-JavaScript fallback. Reduced-motion CSS and JavaScript guards are implemented; OS-level reduced-motion emulation was not performed.

NeuroBreath introduces three labelled illustrative routes: Square Focus inhale/hold/exhale/hold 4/4/4/4 seconds; Sleep Calm inhale/hold/exhale 4/2/6 seconds on a Hebrew ח-shaped path; Neural Wave inhale/exhale 4/6 seconds on a wave. Coming Soon, future Custom Breathing, comfortable breathing, no forced holds, stopping for dizziness/discomfort and non-medical expectations are explicit. The site does not run a breathing exercise or make clinical efficacy claims.

**Editorial workspace, architecture and permissions**

The local Studio supports title, subtitle, summary, author, Blog/Science destination, category, tags, dates, draft/review preparation, Markdown/rich-text paste conversion, headings, bold/italic, links, images/captions, featured image, structured research references, PDF attachments and SEO fields. The shared template generates branded responsive article pages; approved published entries feed their destination listing and search. An isolated test also verifies unpublishing removes a generated article route and search entry.

There are no invented public articles. Template demonstrations are labelled local/unpublished and require the local editor session. Source content uses maintainable JSON with Markdown in `body`. Future approved entries in `content/editorial/` are Git-backed; local working drafts and snapshot history in `.local-cms/` are deliberately not automatically committed or synced. Export is available for local backup.

The local API is a single trusted-workstation tool. It has no login screen, Owner/Editor labels pretending to enforce roles, production credentials or publish endpoint. It requires a local session and exact same-origin writes, validates Host/path boundaries, rejects unsafe content URLs, escapes HTML, limits uploads to PNG/JPEG/WebP/PDF with 5 MB limits and signature checks, and serves PDFs as downloads. Snapshot revisions and conflict detection preserve local draft history. Public static packaging excludes admin code, drafts, scripts, source content and Git metadata.

Owner/Editor identity, assigned-draft permissions, owner-only approval/merge, public publish/unpublish and authenticated remote upload enforcement are NOT VERIFIED and NOT ACTIVE. The local magic-byte checks are not malware scanning. The documented production plan requires a trusted OAuth service or managed provider, protected Git rules/owner reviews, a content-only authorizing service or suitably restricted content repository, secure media processing and an authenticated preview environment. GitHub Pages alone cannot provide these services. No live rules or credentials were configured.

Decap was evaluated against its current official documentation and release/security information. Latest release resolved to 3.17.3, with the file-preview SVG issue patched in that release. The future integration is an inactive configuration example, not an installed or authenticated Decap deployment. See [cms/SETUP.md](cms/SETUP.md) for activation, role limitations, backup and rollback details, and [cms/decap-config.example.yml](cms/decap-config.example.yml) for the content model. Primary sources: [GitHub backend](https://decapcms.org/docs/github-backend/), [editorial workflow](https://decapcms.org/docs/editorial-workflows/), [release](https://github.com/decaporg/decap-cms/releases/tag/decap-cms@3.17.3), [security advisory](https://github.com/decaporg/decap-cms/security/advisories/GHSA-qf66-gqh8-qvrh).

**Requested QA matrix**

PASS means the stated local scope was verified; it does not imply production readiness or physical-device acceptance.

| # | Check | Result | Evidence / remaining requirement |
|---|---|---|---|
| 1 | Homepage Hero preservation | PASS | Byte-identical Hero HTML, unchanged original CSS prefix and protected assets; native Safari visual inspection. |
| 2 | Four platform cards | PASS | Approved order and 2×2/mobile grid verified in browser checks at all five widths; original three artwork bytes preserved. |
| 3 | Desktop laboratory explorer | PASS | Native activation plus browser tests for centered selection, single active tree, timed hover and delayed region exit. Human motion acceptance remains owner review. |
| 4 | Touch laboratory explorer | NOT VERIFIED | Tap-equivalent click paths, close controls and touch-pointer hover suppression passed in browser tests. Physical touchscreen gestures were not tested. |
| 5 | Trampolina tree | PASS | Six source-verified areas; browser expansion and all route/reference checks pass. |
| 6 | Dr. Quiz tree | PASS | Exactly three approved branches; browser expansion and destinations pass. |
| 7 | NeuroPath tree | PASS | Exactly four labs; existing signature placements and routes retained. |
| 8 | NeuroBreath tree | PASS | Exactly three methods; no Custom fourth branch; browser expansion passes. |
| 9 | All branch navigation | PASS | Static targets and local HTTP responses verified; each branch has a dedicated page. |
| 10 | NeuroBreath product page | PASS | Generated page, diagrams, durations, safety text and HTTP verified. Native Safari visual inspection confirmed the three routes and readable content; neutral development artwork remains pending approval/integration of the newly present asset. |
| 11 | Search | PASS | 26 indexed destinations; existing search assertions pass including NeuroWeave, Party Quiz and Neural Wave. Fresh Safari integration passed direct query, result URL, no-results and blank-query checks. |
| 12 | About Us preservation | PASS | All 61 blocks match; protected Markdown hash unchanged. |
| 13 | Blog layout | PASS | Local branded template and five-width browser fit checks passed; native Safari visual inspection confirmed typography and the unpublished banner. Fixture generation/listing/search tested in isolation. No public article invented. |
| 14 | Science & Research layout | PASS | Shared branded template and five-width browser fit checks passed; native Safari visual inspection confirmed readable typography and the unpublished banner. Structured references supported. |
| 15 | CMS article editor | PASS | Browser create/edit/review sequence passed; all editor form fields and local safe-paste implementation present. Production roles excluded. |
| 16 | Article preview | PASS | Browser preview displays edited title, emphasis and unpublished banner; script text does not execute. Server image/caption preview test passes. |
| 17 | Draft storage | PASS | Browser save/reopen passed; server revision/history/conflict tests pass. Local drafts are not remotely backed up. |
| 18 | Publishing architecture | NOT VERIFIED | Design, inactive Decap schema and isolated build/package/unpublish tests complete. Real OAuth, protected branch rules, roles and release flow not activated or tested. |
| 19 | CMS security boundaries | PASS | Local API denial, Origin/Host checks, private-path/traversal denial, safe rendering, type/size/signature checks and disabled publishing tested. Production auth/RBAC remains item 18. |
| 20 | Responsive layouts | PASS | Fresh native Safari harness: 135/135 combinations passed across 27 pages at 320/390/768/1024/1440px; no horizontal overflow, missing images or captured JavaScript/resource errors, and navigation breakpoints correct. Explorer plus Studio/Blog/Science width checks also passed. Desktop browser viewport coverage; physical-device acceptance remains item 4. |

**Verification runs and limits**

- Baseline `python3 -B scripts/verify.py`: 14 pages and 398 references passed before changes.
- Final `python3 -B scripts/build.py`: 27 pages generated, 26 indexed; no publication.
- Final `python3 -B scripts/verify.py`: 27 balanced pages, 779 local references, shared navigation/icons, all 61 story blocks, approved hashes and PNG/ICO checks pass.
- Existing `scripts/verify_interactions.js` executed through the available Node runtime: search assertions pass. Site/editor JavaScript parses successfully. No Node CLI installation was needed.
- `python3 -B scripts/verify_http.py http://127.0.0.1:8787`: 50 unique page/asset URLs return 200 and match repository bytes, including versioned asset requests.
- `python3 -B scripts/verify_editorial.py`: 8 test groups pass. Tests use temporary isolated drafts/media and a temporary build copy; synthetic published fixtures never enter public source.
- Native Safari `scripts/phase2-qa.html`: 160 assertions passed, zero failures, covering all four expansions at five widths, single active selection, centering, close/Escape, 300/500 ms pointer timing, touch-pointer suppression, local draft create/edit/review/reopen, safe preview and Studio/Blog/Science width checks. Pointer/tap simulations are not physical-device testing.
- Native keyboard Enter, Space and Escape were observed on the Dr. Quiz disclosure. The active desktop card and secondary cards were visually inspected.
- The older responsive harness displayed 70/70 using cached old harness/index data; that result is excluded from phase-two coverage. After updating the harness for dynamic route counts/no-store fetches and using content-hashed CSS/JS URLs, a fresh Safari run at `scripts/responsive-qa.html?v=resume-20261116` completed **135/135 PASS; 0 failures; 0 JavaScript/resource errors**. All 27 pages passed at 320, 390, 768, 1024 and 1440px with no horizontal overflow, all images loaded and correct navigation breakpoints. Fresh browser search integration also passed direct query, result URL, no-results and blank-query checks.
- Browser access initially failed with `Computer Use server error -10005: cgWindowNotFound`. After the owner restored Safari availability, control recovered and the full responsive result was observed. Native screenshots additionally confirmed the NeuroBreath diagrams/phase labels and Blog/Science template typography. These checks use desktop Safari and iframe viewport widths; they do not establish physical touchscreen, assistive-technology or OS reduced-motion acceptance.
- During the resumed QA, the new untracked file `public/images/neurobreath-logo-official.jpg` was present (228,197 bytes; SHA-256 `6866c599f679a561dbe5aa78e7ed4dcaeb5fd19246c7f17790d7882ba065ac4b`). It was preserved without modification, staging or integration. Its correspondence to the approved neural orb was not verified in this browser-only follow-up.
- Static artifact test: 59 allowlisted files; new routes present; no admin/drafts/source/scripts/Git metadata included. This artifact was temporary and was not uploaded.
- `git diff --check` and Python syntax checks pass. Shared site JavaScript is 6,975 bytes with no third-party runtime dependency. No network-performance or Lighthouse score is claimed.

**Production unchanged**

Read-only HTTPS checks found production `/`, `/about-us/`, `/assets/site.css`, `/CNAME` and `/site.webmanifest` byte-identical to unchanged `main`. Certificate/hostname verification succeeded using TLS; certificate expiry was February 12, 2027. `git ls-remote` confirmed remote main at `479a153aa9b767ad47b3f919dd7b55f3261f4ca2`; the connected GitHub branch listing showed only main. Supplementary probes initially returned HTTP 503 for `/admin/` and `/laboratories/neurobreath/`. A repeat returned 404 for NeuroBreath, confirming that new route is absent, while `/admin/` still returned 503. The live admin route status therefore remains NOT VERIFIED; the unchanged main ref and matched live core-file bytes are the production-preservation evidence. CNAME, DNS, HTTPS and Namecheap configuration were not changed. No push, merge, Actions trigger or public hosting request was performed.

**Remaining owner review / activation work**

1. Verify the newly present NeuroBreath asset against the approved orb, then integrate the approved artwork and assess the requested motion. Neutral development placeholders remain; orb/energy-arm motion is not yet implemented.
2. Test real mobile tap/scroll, OS reduced motion and assistive technology. Fix any resulting issue before release approval. The fresh 135 route-width checks and native NeuroBreath/article visual inspection are complete.
3. Review the expanded card motion and six source-backed Trampolina areas.
4. Select/configure authentication and protected Git permissions, then test distinct real Owner and Editor identities. Complete production upload processing and authenticated preview infrastructure.
5. Approve content and a future publication separately. This report grants no release permission.

**Files created and modified**

The implementation commit contains the following files. Existing informational HTML files outside the laboratories change only their asset-cache URLs. The report itself is an additional local documentation file.

```text
M	.gitignore
M	about-us/index.html
A	assets/generated-routes.json
M	assets/search-index.json
M	assets/site.css
M	assets/site.js
M	blog/index.html
A	cms/SETUP.md
A	cms/decap-config.example.yml
A	cms/editor.css
A	cms/editor.html
A	cms/editor.js
M	contact/index.html
A	content/editorial/README.md
A	content/laboratories.json
A	content/laboratories.sources.md
M	content/platforms.json
M	index.html
M	journey/index.html
A	laboratories/dr-quiz/challenge-me/index.html
A	laboratories/dr-quiz/discover-learn/index.html
M	laboratories/dr-quiz/index.html
A	laboratories/dr-quiz/party-quiz/index.html
A	laboratories/neurobreath/index.html
A	laboratories/neurobreath/neural-wave/index.html
A	laboratories/neurobreath/sleep-calm/index.html
A	laboratories/neurobreath/square-focus/index.html
M	laboratories/neuropath/attention/index.html
M	laboratories/neuropath/flexibility/index.html
M	laboratories/neuropath/index.html
M	laboratories/neuropath/logic/index.html
M	laboratories/neuropath/memory/index.html
A	laboratories/trampolina/colors/index.html
M	laboratories/trampolina/index.html
A	laboratories/trampolina/letters/index.html
A	laboratories/trampolina/memory-perception/index.html
A	laboratories/trampolina/numbers/index.html
A	laboratories/trampolina/shapes/index.html
A	laboratories/trampolina/thinking-logic/index.html
M	science/index.html
M	scripts/build.py
A	scripts/editorial.py
A	scripts/laboratories.py
A	scripts/package_site.py
A	scripts/phase2-qa.html
M	scripts/responsive-qa.html
A	scripts/serve.py
M	scripts/verify.py
A	scripts/verify_editorial.py
M	scripts/verify_interactions.js
M	search/index.html
```

GlionIQ development phase completed locally. Awaiting owner review and explicit approval before any publication.
