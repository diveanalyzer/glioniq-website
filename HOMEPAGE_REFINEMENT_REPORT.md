# GlionIQ — local homepage refinement

Verified 2026-11-16 in `/Users/igor/Documents/Repositories/glioniq-website`.

- Branch: `development/glioniq-homepage-v2`.
- Starting commit: `d2771d3d6a10e4caba49a2686e646b4ae02e10f6`.
- Ending implementation commit: `2d66550` (the following documentation commit contains this report).
- The only starting untracked file was the owner-supplied NeuroBreath JPG. It is now tracked without changing its bytes. All previous commits were retained.
- No push, merge, deployment, production configuration change, CMS activation or DigitalOcean action was performed.

This report supersedes the explorer, artwork and responsive-coverage status in `DEVELOPMENT_PHASE_2_REPORT.md`; the earlier report remains a historical record.

## Working preview

- [Homepage](http://127.0.0.1:8787/?v=refinement-final)
- [Laboratory explorer](http://127.0.0.1:8787/?v=refinement-final#laboratories)
- [NeuroBreath](http://127.0.0.1:8787/laboratories/neurobreath/)
- [Search](http://127.0.0.1:8787/search/)
- [Logic Lab activity cards](http://127.0.0.1:8787/laboratories/neuropath/logic/)
- [Trampolina activity cards](http://127.0.0.1:8787/laboratories/trampolina/memory-perception/)
- [Local Editorial Studio](http://127.0.0.1:8787/admin/)

The existing loopback-only preview server on port 8787 was reused and verified with HTTP requests. If it is stopped, run `python3 -B scripts/serve.py --port 8787`. Local preview is not a public deployment.

## Implemented refinements

The four platform cards retain their approved order, descriptions and existing artwork. Desktop uses two columns and two rows; narrow screens use one column. Grid rows keep equal main-card heights. Opening a tree does not resize, reorder or move the cards.

All pointer-enter, pointer-move, pointer-leave and delayed hover expansion logic was removed. Hover changes only the visual highlight. The gold Explore links navigate independently. Native secondary buttons toggle between **Discover Laboratories +** and **Close Laboratories ×**, with platform-specific accessible names, `aria-expanded` and `aria-controls`.

A single shared panel below the entire grid displays one selected tree. Selecting another platform replaces its contents. The selected card has a gold highlight and a restrained connector that runs outside the desktop cards. The panel has an explicit close button. Escape closes within the explorer, and close restores focus to the original trigger. On narrow screens, activation focuses the panel heading and scrolls it into view when needed. Reduced-motion CSS disables transitions and JavaScript selects immediate scrolling. No popup or modal is used. Platform navigation remains available without JavaScript.

All 16 internal branch cards now have distinct appropriate visuals, descriptions and real destinations:

| Platform | Preserved branches | Visual source |
|---|---|---|
| Trampolina | Colors; Numbers; Shapes; Letters; Memory & Perception; Thinking & Logic | Colorful category SVG illustrations, labelled as category illustrations |
| Dr. Quiz | Challenge Me; Party Quiz; Discover & Learn | Distinct question, trophy and discovery illustrations; official character unchanged |
| NeuroPath | Memory Lab; Attention Lab; Logic Lab; Flexibility Lab | Existing approved reference-derived laboratory symbols, unchanged |
| NeuroBreath | Square Focus; Sleep Calm; Neural Wave | Square, Hebrew ח-shaped route and wave illustrations; exact existing timing descriptions retained |

Ten already named activities receive visual cards with their existing laboratory, development status and dedicated information routes. The three NeuroPath signature cards retain gold emphasis: Memory Lab stays in Memory, and NeuroWeave/CodeQuest stay in Logic. Trampolina cards cover Memory Game, Picture Puzzle, Spot the Differences, Continue the Pattern, Sorting Categories, First & Next and Odd One Out. Their information pages introduce only confirmed organization and development status; no mechanics, clinical benefits or public downloads were invented. Light Paths remains unassigned. Custom Breathing remains a feature rather than a fourth branch.

## Official NeuroBreath artwork

`public/images/neurobreath-logo-official.jpg` is a real opaque JPEG, 1206 × 640, 228,197 bytes. SHA-256 remains:

`6866c599f679a561dbe5aa78e7ed4dcaeb5fd19246c7f17790d7882ba065ac4b`

The original is used on the main card and dedicated platform page. Placeholder copy and spinner markup were removed. CSS containment preserves the aspect ratio; an elliptical edge fade blends the opaque background into navy. Native Safari visual inspection confirmed the treatment. No image pixels were edited, no official art was regenerated and no transparent derivative is claimed. The edge fade intentionally softens the peripheral background/outermost filaments; the central orb remains intact. A clean cutout would require an approved transparent source to preserve fine filaments reliably.

Separate official activity logos were not present in this website repository for Memory Lab (signature activity), NeuroWeave, CodeQuest, Memory Game, Picture Puzzle, Spot the Differences, Continue the Pattern, Sorting Categories, First & Next or Odd One Out. These cards use clearly labelled category illustrations. Separate official marks for the six Trampolina categories and three Dr. Quiz branches were also absent; the permitted category-symbol fallback is used. Existing platform artwork and all four NeuroPath laboratory symbols are reused.

## Search corrections

The generator now emits the exact placeholder:

> Search GlionIQ laboratories, platforms and research…

Both generated HTML and the JavaScript blank-query state use:

> Discover our platforms, laboratories and scientific insights.

The index contains all four platforms and their pages: 36 indexed destinations across 37 generated pages. Search remains directly accessible outside the collapsible mobile menu and follows Contact on desktop. A native click on the homepage search icon opened the working search page with both corrected strings.

## Requested verification matrix

PASS describes the explicitly tested local scope. Desktop Safari viewport tests are not physical iPhone/Android tests.

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Approved Hero unchanged | PASS | Hero HTML and all CSS preceding the explorer block match the starting commit; original artwork hashes preserved. |
| 2 | Four main cards | PASS | Approved order, 2×2/vertical layouts and equal heights at all five widths. |
| 3 | No hover expansion | PASS | Pointer/timer handlers removed; mouse/touch pointer traversal tests leave trees closed. Pointer exit leaves an open tree open. |
| 4 | Click opens correct tree | PASS | All four controls tested at all five widths; native Safari click observed. |
| 5 | Click closes tree | PASS | Repeated secondary click and panel close tested; focus returns to trigger. |
| 6 | Switching trees | PASS | One visible tree and one expanded control after each switch; native Trampolina → NeuroPath switch observed. |
| 7 | Shared panel | PASS | Panel remains below all four cards; card positions/heights unchanged while switching. Native desktop and 320px visual checks. |
| 8 | Internal visuals | PASS | All 16 branch cards contain appropriate visuals; all 10 activity cards include distinct category illustrations, description, lab/status and working routes. |
| 9 | Trampolina tree | PASS | Six retained categories; tested expansion and all route targets. |
| 10 | Dr. Quiz tree | PASS | Exactly three retained branches; tested expansion and all route targets. |
| 11 | NeuroPath tree | PASS | Four retained labs; native Logic Lab → CodeQuest navigation observed; signature placement preserved. |
| 12 | NeuroBreath tree | PASS | Exactly three methods; expansion/route checks; existing phase patterns preserved. |
| 13 | Official NeuroBreath image | PASS | Original JPEG/hash/dimensions checked; loads in all-width tests and visually blends into the dedicated page. |
| 14 | Search placeholder | PASS | Exact string verified in generator, output, fresh browser harness and native Safari field. |
| 15 | Search helper text | PASS | Exact initial and JavaScript blank-query strings verified in browser. |
| 16 | Search operation | PASS | Existing Node assertions plus browser direct-query/result-link/no-result/blank-query tests. |
| 17 | Navigation | PASS | 1,065 local references resolve; 65 unique HTTP page/asset responses match files; homepage search and laboratory/activity click paths observed. |
| 18 | Responsive layout | PASS | Final 185/185 page-width combinations across 37 pages at 320/390/768/1024/1440px. Expanded explorer checks also pass. |
| 19 | Broken images | PASS | All images loaded in final 185-case browser run; HTTP byte comparisons pass. |
| 20 | JavaScript errors | PASS | Zero captured JavaScript/resource errors in full browser sweep; runtime/harness syntax checked. |
| 21 | About Us | PASS | All 61 blocks match, including order and punctuation; source hash unchanged; generated page differs only by CSS/JS cache versions. |
| 22 | Existing CMS | PASS | CMS files/server/editorial module byte-identical; 8 isolated regression groups and browser draft/edit/review/preview/reopen tests pass. No production publishing activated. |

Additional accessibility evidence: native Safari Space and Enter activated the control; Escape closed it and restored focus. The accessibility tree exposed collapsed/expanded buttons, platform names and the selected heading. Full VoiceOver/screen-reader acceptance, OS-level reduced-motion testing and physical touchscreen gestures remain **NOT VERIFIED**. CSS/JavaScript reduced-motion handling is implemented and inspected.

## Test execution and limits

- `python3 -B scripts/build.py`: 37 pages generated, 36 indexed; no publication.
- `python3 -B scripts/verify.py`: protected originals 6/6, 61 story blocks, 37 balanced pages, 1,065 local references, icons, shared navigation and domain checks pass.
- `scripts/verify_interactions.js`: executed successfully in the normal available Node module context against all 36 destinations. An attempted isolated-VM wrapper produced a cross-realm array assertion mismatch; the unmodified test passed in its intended module context.
- `python3 -B scripts/verify_http.py http://127.0.0.1:8787`: 65 unique URLs returned 200 and matched current file bytes.
- `python3 -B scripts/verify_editorial.py`: all 8 isolated test groups passed; test content/media remained in temporary test storage.
- Fresh Safari `scripts/phase2-qa.html?v=click-refinement-3`: **268 PASS, 0 failures**, covering the click-only explorer at five widths, mobile panel focus/scroll, no hover changes, navigation distinction, corrected search text and existing CMS workflow/template fitting. One labelled QA draft was added to ignored local storage during this run; existing drafts were retained.
- Final Safari `scripts/responsive-qa.html?v=refinement-final&view=tree`: **185/185 PASS; 0 failures; 0 JavaScript/resource errors**. All images loaded, no horizontal overflow and navigation breakpoints correct. Browser search integration passed.
- The interaction harness now eagerly loads offscreen images and uses fresh per-navigation URLs. An initial run stalled on an offscreen lazy image; another encountered stale search HTML. Neither incomplete run is counted as a pass. The fresh run verified the exact requested wording.
- Native visual checks included the desktop grid, shared panel, 320px expanded panel, gold signature cards and the final NeuroBreath image treatment.
- Sandbox loopback restrictions initially prevented HTTP/CMS tests; the same checks passed after the required local network permission was granted.
- No physical device, Lighthouse score or cross-browser acceptance is claimed. No known functional failures remain in the tested scope.

## Preservation and production

The approved Hero HTML, pre-explorer CSS, original artwork, About Us source, icons, manifest and CNAME are unchanged. Blog, Science, Contact and About Us generated documents differ only in stylesheet/script cache-version URLs. CMS files, server and editorial module are byte-identical to the starting commit. The existing authentication/role/publishing limitations remain documented in `cms/SETUP.md`; this task does not activate them.

Read-only, certificate-validated HTTPS downloads of production `/`, `/about-us/`, `/assets/site.css`, `/CNAME` and `/site.webmanifest` matched `main` byte-for-byte. Remote main remains `479a153aa9b767ad47b3f919dd7b55f3261f4ca2`, also the unchanged local main. The web browsing gateway could not open the domain, so the direct validated HTTPS comparisons provide the live evidence. No production-write operation was performed.

## Files changed

Implementation commit `2d66550` contains 48 files. Most pre-existing generated pages only receive current CSS/JS cache URLs. The substantive sources are `assets/site.css`, `assets/site.js`, `content/platforms.json`, `scripts/build.py`, `scripts/laboratories.py` and the verification harnesses. The supplied JPG is newly tracked. Ten new activity pages provide real navigation destinations.

```text
M	about-us/index.html
M	assets/generated-routes.json
M	assets/search-index.json
M	assets/site.css
M	assets/site.js
M	blog/index.html
M	contact/index.html
M	content/platforms.json
M	index.html
M	journey/index.html
M	laboratories/dr-quiz/challenge-me/index.html
M	laboratories/dr-quiz/discover-learn/index.html
M	laboratories/dr-quiz/index.html
M	laboratories/dr-quiz/party-quiz/index.html
M	laboratories/neurobreath/index.html
M	laboratories/neurobreath/neural-wave/index.html
M	laboratories/neurobreath/sleep-calm/index.html
M	laboratories/neurobreath/square-focus/index.html
M	laboratories/neuropath/attention/index.html
M	laboratories/neuropath/flexibility/index.html
M	laboratories/neuropath/index.html
A	laboratories/neuropath/logic/codequest/index.html
M	laboratories/neuropath/logic/index.html
A	laboratories/neuropath/logic/neuroweave/index.html
M	laboratories/neuropath/memory/index.html
A	laboratories/neuropath/memory/memory-activity/index.html
M	laboratories/trampolina/colors/index.html
M	laboratories/trampolina/index.html
M	laboratories/trampolina/letters/index.html
M	laboratories/trampolina/memory-perception/index.html
A	laboratories/trampolina/memory-perception/memory-game/index.html
A	laboratories/trampolina/memory-perception/picture-puzzle/index.html
A	laboratories/trampolina/memory-perception/spot-differences/index.html
M	laboratories/trampolina/numbers/index.html
M	laboratories/trampolina/shapes/index.html
A	laboratories/trampolina/thinking-logic/continue-pattern/index.html
A	laboratories/trampolina/thinking-logic/first-next/index.html
M	laboratories/trampolina/thinking-logic/index.html
A	laboratories/trampolina/thinking-logic/odd-one-out/index.html
A	laboratories/trampolina/thinking-logic/sorting-categories/index.html
A	public/images/neurobreath-logo-official.jpg
M	science/index.html
M	scripts/build.py
M	scripts/laboratories.py
M	scripts/phase2-qa.html
M	scripts/responsive-qa.html
M	scripts/verify.py
M	search/index.html
```

GlionIQ homepage refinement completed locally. Awaiting owner approval before publication.
