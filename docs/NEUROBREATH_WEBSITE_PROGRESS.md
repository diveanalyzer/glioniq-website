# NeuroBreath website progress and recovery

Repository: `/Users/igor/Documents/Repositories/glioniq-website`.
Remote: `https://github.com/diveanalyzer/glioniq-website.git` (public repository).
Feature branch: `feature/neurobreath-central-trees-20261116`.
Preserved development branch: `development/glioniq-homepage-v2`, starting HEAD `c289642`.

## Phase 0 — complete

Verified cwd, Git root, status, recent history, remote and actual website sources before editing. The site uses dependency-free Python static generation, JSON content, shared CSS/JavaScript and a loopback Python preview server. No package-manager lint command is configured. No applicable `BOOST.md` or repository `AGENTS.md` file exists at the supplied locations.

All prior uncommitted artwork work is preserved on the dedicated feature branch. A local starting snapshot is at `/private/tmp/glioniq-before-neurobreath-20261116.tar.gz`; starting hashes are in `/private/tmp/glioniq-neurobreath-starting-hashes.json`.

Read-only GitHub verification on 16 November 2026 confirmed Pages uses legacy deployment from `main:/`, custom domain `glioniq.tech`. Only the dynamic `pages-build-deployment` workflow exists; repository webhooks are empty; the ten latest deployments are from main. The GitHub connector could verify repository identity but did not expose the workflow endpoint, so authenticated read-only REST checks used the existing Git credential without printing it. No hosting setting changed. Recheck before the final push.

The supplied `neuropath/04_profile/profile_setup_flow.jpeg` contains a personal-profile example with a portrait and name. It is unused by the website and is preserved locally, excluded from this public backup. Its hash/path may remain in the inventory, but the image itself must never be staged.

Per the owner's no-build-artifacts requirement, new commits include source, necessary artwork and verification evidence; regenerated HTML and generated search/route indexes are not staged. Previously tracked build outputs remain in history. A clean clone must run `python3 -B scripts/build.py` to reproduce the current preview.

## Phases and checkpoints

| Phase | Status | Local checkpoint |
|---|---|---|
| 0 — safety / preserve existing artwork | Complete | `1542123` |
| 1 — approved NeuroBreath wordmark | Complete | `9c44096` |
| 2 — central laboratory trees | Complete | `f7b9528` |
| 3 — living orb | Complete | `5c33c70` |
| 4 — breathing activities | Complete | `67e8932` |
| 5 — responsive verification | Complete | `dbecbfe` |
| 6 — complete testing / screenshots | Complete locally; visual limitations below | `2e1baab` |
| 7 — verified GitHub backup | INCOMPLETE — awaiting owner approval | No push attempted |

## Current state

GitHub Backup: INCOMPLETE — owner approval required by the newer recovery directive dated 17 November 2026. No push attempted.

Next step: owner review of the local preview and approval for a normal push of this feature branch to the existing GlionIQ GitHub remote. No publication is proposed.

Publication is not authorized. Never merge into main, change DNS/hosting, or trigger production deployment.

## Phase 1 — approved branding

Extracted the exact 539 × 83 wordmark from the supplied approved reference, with reproducible crop coordinates and SHA-256 provenance. Both original NeuroBreath files and all other approved logos remain unchanged. The original orb is larger within the existing artwork area. The subtitle, descriptions, card sizing and both actions are retained.

Safari visual review: desktop and a 320 CSS-pixel iframe show the full wordmark, original orb, readable text and reachable controls. Build: 37 pages. The crop retains a thin blue reference glow and navy background; this is not a redrawn or newly approved logo. The reference's lung-orb differs from the explicitly required original neural orb, which is preserved. Final screenshots and responsive sweep follow in phase 6.

## Phase 2 — central exploration

Four native, directly addressable `/laboratories/{platform}/explore/` pages replace the homepage expansion. Each uses its approved logo, existing branches, and the ten existing child-activity links. Luminous connectors preserve the approved palette. Unimplemented products are explicitly described as in development. NeuroBreath's three nodes show their names, exact timing sequences and links.

Validation: build 41 pages; static verification 1,239 local references, original branding and 61 About Us blocks pass; artwork verification passes. Safari local QA: **118 checks PASS**, including all four Discover and Back to Home actions at 320, 390, 768, 1024 and 1440px, equal card heights and no tree overflow. Actual Safari toolbar Back and Forward returned between the NeuroBreath tree and homepage correctly. Direct NeuroBreath tree visually inspected. Editorial-writing browser tests are now opt-in (`?editorial=1`); this navigation run did not write drafts.

## Phase 3 — living orb

The unchanged original image is rendered as a base and two soft masked outer-arm overlays. Idle expansion/light and slight asymmetric arm movement use CSS. IntersectionObserver and page visibility stop offscreen idle work. Active rendering uses the monotonic clock and cosine easing: expand on inhale, hold the corresponding size, contract on exhale. A shared frame renderer maps cycle progress onto square / ח / wave paths. Frame highlights and arm expansion approximate contact with the square edges.

Limit: the JPG has no separate arm geometry. The two masked overlays are a faithful non-destructive approximation, not independently rigged individual neurons. Reduced-motion CSS removes all orb animation/transforms; the renderer also keeps its scale fixed.

Node timing tests passed: exact boundaries for all three patterns, continuous sizes, pause/resume with fractional elapsed time, restart/reset and 100-cycle frame gaps. Safari **125 checks PASS**, including moving idle animations, explicit active-renderer phase sizes and reduced-motion renderer behavior. End-to-end user controls are phase 4; OS-level reduced-motion preference has not been changed.

## Phase 4 — breathing activities

Three existing URLs now contain working guides: Square Focus 4/4/4/4, Sleep Calm 4/2/6 and Neural Wave 4/6. Start, Pause, Resume, Restart and Exit are functional; phase, countdown, cycle, highlighted steps and frame trace derive from the same elapsed-time snapshot. Hidden pages, leaving the activity and scrolling the guide out of view pause the clock; return requires explicit Resume. No saved data, backend or permissions are required. Existing comfort guidance remains.

Safari **149 checks PASS**: actual full 16s, 12s and 10s cycles, phase order, controls, paused countdown/animation, resume, restart and Exit destinations. Also manually activated and paused Square Focus with focus moving to the next available control. Static build and links passed; artwork verification was updated from the retired flat activity-thumbnail contract to the original orb image and passed. Node timing and search tests passed.

## Phase 5 — homepage and responsive design

Preserved the original grid dimensions/order, Explore destinations, subtitle/descriptions, shared header/footer and complete approved Hero HTML/CSS prefix (compared with `c289642`). The exact cropped wordmark is blended against navy; its thin reference glow remains visible. Tree connectors now follow measured node positions, including wrapped rows and mobile, without changing homepage layout.

Safari **205/205 page-width combinations PASS** (41 pages × 320/390/768/1024/1440 CSS pixels): no horizontal overflow, no clipped main cards, all images decoded, navigation breakpoint correct, zero captured JavaScript/resource errors. Browser search direct-query/result/no-results/blank-query checks also passed. Mobile NeuroBreath tree was visually inspected. These are desktop Safari viewport tests, not physical-device acceptance. HTTP verification: **93 unique URLs PASS**, all 200 and byte-matched.

## Recovery audit — 17 November 2026

Latest owner directive supersedes automatic push authorization: finish local work and request approval before pushing or publishing. Existing feature branch and all prior development work remain intact. Phase 5 (`dbecbfe`) was the last completed checkpoint. Phase 6 stopped with three source changes awaiting final verification: Exit/Back ready-state reset, lifecycle/reduced-motion browser QA, and exclusion of the private reference image from static packaging. Generated HTML/search/route files remain unstaged by design. No staged files were present.

Read-only audit ran cwd/root, branch/status/remote/log, full diff (saved in the recovery snapshot), staged/untracked/ignored inventory, source diff inspection and integrity verification. Main and remote main remain `479a153aa9b767ad47b3f919dd7b55f3261f4ca2`; the remote contains only main. There are 13 local commits above main at the audit checkpoint. Development branch remains `c289642`. No missing protected source assets or approved story blocks were found. Four local editor files remain present; hashes are recorded privately in the snapshot.

New snapshot: `/private/tmp/glioniq-recovery-20261117-193355/`. Its `working-tree.tar.gz` contains 205 relevant tracked/untracked/generated-route files, all reopened and SHA-256 verified; `history.bundle` was verified by Git. `working-tree.diff`, `staged.diff` and a manifest preserve the exact audited changes. Local editor contents, the unused personal-profile reference, caches and credentials are not in the shareable tree archive; they are preserved in place. The local editor hash manifest is local-only. No existing backup was overwritten.

Earlier temporary screenshot/authoring folders and the previous preview process disappeared across the environment restart. These were temporary artifacts, not website source. Earlier visual test results are conversation evidence; final screenshot files will be recaptured into the repository. Safari reconnects successfully; its error page was caused by the stopped loopback server.

Read-only production check: HTTPS 200 for Home, About Us and CNAME; all three byte-match main. GitHub Pages uses legacy `main:/`, only the dynamic Pages workflow is active, no webhooks exist, and the latest deployment is main `479a153`. No publication or hosting setting changed.

## Phase 6 — completed local validation, 17 November 2026

Resumed the three preserved fixes: Exit now resets the rendered guide and controls before navigation, the browser QA covers visibility and reduced motion, and local static packaging excludes the unused personal-profile reference. Native Safari Start → Exit → toolbar Back returned to “Ready when you are” with Start enabled and Pause/Restart disabled. No approved art, other product repository, CMS content or live setting was changed during recovery.

Final Safari interaction run: **153 PASS, 0 failures**. It includes all four laboratory trees at five widths, complete real-time breathing cycles, pause/resume/restart/exit, synthetic visibility events and forced reduced-motion stylesheet rules. The forced-rule test supplements the reduced-motion renderer test; it does not claim actual OS preference testing. Browser history was checked manually because iframe history is not equivalent to native navigation.

Final responsive run: **205/205 PASS**, 41 pages at 320, 390, 768, 1024 and 1440 CSS pixels. Images decoded, no horizontal overflow or clipped main cards, expected navigation breakpoint, no captured JavaScript/resource errors. Search query, linked result, no-results and empty-query states passed. Mobile tree → Sleep Calm navigation was also activated manually in a 390px iframe.

Other validation: **3,847** breathing timing assertions; search unit checks; **8** editorial tests using isolated temporary storage; static build **41 pages / 40 search entries**; **1,263** local references; **93** HTTP URLs returned 200 and byte-matched; **27** supplied original assets and their mapping passed integrity checks; six original protected branding pins and all **61** approved About Us story blocks passed. Local packaging produced **160** files with all 41 routes and the exact CNAME, without the private reference image. No standalone lint command is configured; `git diff --check` passes.

Screenshots: [evidence index](evidence/neurobreath-20261117/README.md). All final files were recaptured after the environment restart. Browser chrome is cropped from saved evidence. These are Safari desktop captures and CSS-width iframe tests, not physical-device certification or a full accessibility audit.

### Remaining differences and acceptance boundaries

- The NeuroBreath wordmark is an exact crop of the supplied reference. Its blue glow/navy strip remains faintly visible. The original neural orb is retained as explicitly requested; the reference's different lung-like orb was not substituted.
- Neural-arm motion uses two masked overlays of the original image, an approximation rather than separately rigged neurons. No original image bytes were changed.
- Four earlier Trampolina illustrations (Colors, Numbers, Shapes, Letters) still require owner visual approval; see [artwork review](../ARTWORK_REVIEW.md). No new illustrations were generated during this recovery.
- Physical mobile devices, other browsers, a full screen-reader audit, actual OS reduced-motion switching and production deployment acceptance remain **NOT VERIFIED**. No remaining functional failure was observed in the completed local suites.
- GitHub backup is **INCOMPLETE** until the owner approves the push and the remote SHA is verified. The local source checkout intentionally retains unstaged generated HTML/search/route outputs; they were not reset or included in new source checkpoints.

## Recovery report A–K

| Item | Verified result |
|---|---|
| A — Repository / branch | Existing `glioniq-website`; `feature/neurobreath-central-trees-20261116`; correct `diveanalyzer/glioniq-website` origin. |
| B — Integrity / backup | Protected assets, story, source history and local editor files preserved. Read-back-verified recovery snapshot and Git bundle recorded above; final checkpoint bundle recorded below. |
| C — Last task before recovery | Phase 5 responsive/layout preservation, commit `dbecbfe`. |
| D — Stop point | Phase 6 final lifecycle/package fixes and screenshot evidence. The reported older CSS-only stop preceded the actual current state; `assets/site.css` was already committed. |
| E — Unfinished changes recovered | Exit/Back ready reset, lifecycle/reduced-motion QA, private-reference package exclusion; generated outputs retained. |
| F — Completed on resume | Recovery audit, new snapshot, Safari reconnection, final fixes/QA, replacement screenshots and local checkpoint preparation. |
| G — Remaining | Owner visual acceptance, device/accessibility checks noted above, approval and verification of GitHub backup. |
| H — Tests | Final results and precise coverage above. |
| I — GitHub sync | Remote main remains `479a153`; feature commits are local only. No push attempted. |
| J — Publication | No publish, merge, hosting or DNS changes. Live Home/About/CNAME byte-match main. |
| K — Next action | Review local preview at `http://127.0.0.1:8787/`, approve feature-branch backup; after approval recheck deployment coupling, normal push, verify exact remote SHA. Publication requires separate approval. |

Proposed push after approval: `git push -u origin feature/neurobreath-central-trees-20261116`. Never force-push. Source-only checkpoints require `python3 -B scripts/build.py` after a fresh checkout to regenerate the current site.

## Final local checkpoint and recovery package

Phase 6 commit: `2e1baab` — source fixes, verification scripts, progress and 16 reviewed screenshots with SHA-256 manifest. Staging review covered 23 files; known credential-pattern checks found no matches. No generated HTML/index, local editor content, cache or private profile image was staged.

A fresh `git archive HEAD` extraction at `/private/tmp/glioniq-source-restore-qoup5ft2` rebuilt all 41 pages and passed both `verify.py` and `verify_artwork.py`. This verifies the committed source can reproduce the site without the original working tree or the local-only profile reference.

Durable local recovery destination outside the repository: `/Users/igor/Documents/GlionIQ-Recovery/glioniq-20261117-195527/`. The final Git bundle, source snapshot including unstaged generated outputs, per-file integrity manifest and exact final HEAD are recorded there. The original audit snapshot is preserved separately. The final documentation-only checkpoint follows `2e1baab`; the recovery manifest and `git log -1` identify its exact SHA.

Final remote read: only `main`, still `479a153aa9b767ad47b3f919dd7b55f3261f4ca2`. GitHub Backup: **INCOMPLETE — owner approval required**, not an authentication failure. All feature work remains local. No publication action is proposed or performed.
