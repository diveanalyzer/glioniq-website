# Local Safari evidence — 17 November 2026

Local server: `http://127.0.0.1:8787/`. Captures were made through native Safari UI, after the recovery audit. Top 180 image pixels containing browser chrome/unrelated tabs are cropped; website pixels are otherwise unchanged. Raw captures remain in the local temporary evidence folder. SHA-256 hashes are in `manifest.json`.

| Evidence | View |
|---|---|
| [Homepage four cards](homepage-four-cards.png) | Existing homepage grid, Safari 50% zoom to fit the four cards. |
| [Homepage Hero](homepage-hero.png) | Normal Safari scale, original full-width Hero. |
| [NeuroBreath tree](tree-neurobreath.png) | All three timing nodes at 50% zoom. |
| [Dr. Quiz tree](tree-dr-quiz.png) | Three existing laboratories, 50% zoom. |
| [NeuroPath tree](tree-neuropath.png) | Existing branches and child activities, 50% zoom. |
| [Trampolina tree](tree-trampolina.png), [lower portion](tree-trampolina-lower.png) | Existing branches and child activities, 50% zoom. |
| [Square Focus](activity-square-focus.png) | Active 4–4–4–4 guide at normal scale. |
| [Sleep Calm](activity-sleep-calm.png) | Active 4–2–6 guide at normal scale. |
| [Neural Wave](activity-neural-wave.png) | Active 4–6 guide at normal scale. |
| [Mobile homepage](mobile-homepage.png) | 390 CSS-pixel iframe, normal Safari scale. |
| [Mobile NeuroBreath tree](mobile-neurobreath-tree.png), [lower portion](mobile-neurobreath-tree-lower.png) | 390px iframe; scrolled to inspect connected nodes. |
| [Mobile Sleep Calm](mobile-sleep-calm.png) | Opened by clicking the tree node inside the 390px iframe. |
| [Responsive result](responsive-results.png) | 205/205 PASS; all 41 pages at 320/390/768/1024/1440px, search integration passed. |
| [Interaction checks](browser-results.png) | Scrolled excerpt from the passing interaction run. The final status was read in Safari accessibility state: “153 PASS · 0 failures.” |

QA frames are development-only tools. Some visual captures show the responsive sweep in progress; `responsive-results.png` records the completed sweep. Activity screenshots show one moment in an animation; timing and controls were verified by the real-time browser suite and separate clock assertions. Native toolbar Back/Forward was also tested manually.

The wordmark's source glow remains visible; masked neural-arm overlays are an approximation. Four earlier Trampolina illustrations still require owner approval. See the full [progress and recovery report](../../NEUROBREATH_WEBSITE_PROGRESS.md) for limitations, provenance, remaining approvals and exact test coverage. No physical-device, multi-browser or complete accessibility acceptance is claimed.
