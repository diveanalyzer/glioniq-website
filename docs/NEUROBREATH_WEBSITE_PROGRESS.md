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
| 1 — approved NeuroBreath wordmark | Complete | Recorded in the next checkpoint |
| 2 — central laboratory trees | Pending | — |
| 3 — living orb | Pending | — |
| 4 — breathing activities | Pending | — |
| 5 — responsive verification | Pending | — |
| 6 — complete testing / screenshots | Pending | — |
| 7 — verified GitHub backup | Pending | — |

## Current state

GitHub Backup: INCOMPLETE — implementation has just started; no push attempted.

Next step: build four central exploration routes using existing laboratory and activity data.

Publication is not authorized. Never merge into main, change DNS/hosting, or trigger production deployment.

## Phase 1 — approved branding

Extracted the exact 539 × 83 wordmark from the supplied approved reference, with reproducible crop coordinates and SHA-256 provenance. Both original NeuroBreath files and all other approved logos remain unchanged. The original orb is larger within the existing artwork area. The subtitle, descriptions, card sizing and both actions are retained.

Safari visual review: desktop and a 320 CSS-pixel iframe show the full wordmark, original orb, readable text and reachable controls. Build: 37 pages. The crop retains a thin blue reference glow and navy background; this is not a redrawn or newly approved logo. The reference's lung-orb differs from the explicitly required original neural orb, which is preserved. Final screenshots and responsive sweep follow in phase 6.
