# NeuroPath catalogue source audit

Read-only inspection: 17 November 2026. Application repository: `NeuroPath`, inspected revision `c9b4ac3a044a16cb242411caf9839cd284fed6f2`. No application file, user record, simulator or application build was changed or executed for this audit.

## Inventory and placement

The actual `lib/core/models.dart:15–42` enum and approved `NeuroPath_MASTER_PRD.md:25–38` specify exactly nine cognitive games in four laboratories:

| Laboratory | Games, in catalogue order |
|---|---|
| Memory Lab | Memory Lab (signature), Light Paths 2.0, EchoShift |
| Attention Lab | Target Hunt, OrbitMind |
| Logic Lab | NeuroWeave (signature), CodeQuest (signature) |
| Flexibility Lab | Rule Shift, Synapse Forge |

EchoShift belongs to Memory Lab, despite the website directive's tentative flexibility example. Memory Lab is also a signature game. No separate signature category, duplicated game, PatternGrid, LogicFlow or Sound & Connection entry was created. Existing Memory Lab, NeuroWeave and CodeQuest website URLs are preserved.

`content/catalogue/neuropath.json` contains fourteen entries: one platform, four laboratories and nine game destinations. Each records parent, purpose, audience guidance, difficulty, interaction details, tutorials, related destinations and precise source references.

## Current mechanics and content limits

- Memory Lab uses real Spanish words and selected-language meanings, followed by typed recall and recognition; optional pronunciation recordings are absent.
- New Light Paths sessions use V2 (`lib/core/controller.dart:270–290`), with six tiers, direction/color/pulse recall, correction and ten lessons. The legacy V1 screenshot and simpler old rules are not presented as V2.
- CodeQuest supports solo, three AI strengths and local two-player play. Feedback is aggregate within each row. Online play remains future work.
- NeuroWeave uses connected directed routes, no numerical-order requirement, energy and exact objectives. No revisits is the current rule. Recovery retains challenge outcomes and counts as assistance.
- The four remaining games follow `lib/games/cognitive.dart` and the actual tutorial text in `lib/core/coaching.dart`. No additional mechanics were inferred from decorative images.
- English, Hebrew and Russian UI are present in source. No numeric age rating was established; the website's reading/puzzle-familiarity guidance is editorial.
- All nine games are application experiences in development. The catalogue is information, not new browser gameplay or a product-release claim.
- No product-specific efficacy study was found in the inspected material. General cognitive research must not be presented as proof of NeuroPath effectiveness or illness prevention.

## Artwork and screenshot decisions

Existing approved platform/laboratory artwork and all three signature crops remain the priority. Six missing dedicated game illustrations reuse the application's existing generated scenes, copied byte-for-byte into `public/images/laboratories/neuropath/catalogue/`. Their original generation provenance is `NeuroPath/docs/GENERATED_ART.md`. They are **provisional game illustrations awaiting owner review**, not official logos or approved screenshots. No new image generation was needed.

Nine genuine development UI images are included. Eight are game-only host-test captures with synthetic puzzle state from `docs/evidence/recovery-20261117/host-ui/`; Light Paths uses the actual native V2 tutorial capture from `docs/evidence/welcome-neurobreath/all-native/device-ui/lp2-tutorial.png`. Each was visually inspected for private data before copying. None contains private profile information. Captures may show one viewport of a scrollable screen; no claim of complete-screen coverage is made.

The V2 tutorial capture retains the older application's checkerboard-backed logo treatment. It is explicitly captioned development UI and is not used as the website logo. The legacy V1 Light Paths capture and a separate debug/clipped V2 host capture are excluded. Screenshots were not cropped, retouched or otherwise changed.

`content/catalogue/neuropath-assets.json` records the fifteen copied assets, source paths, dimensions, matching SHA-256 hashes, approval status, use and mapping confidence. It also identifies excluded captures and the approved routes preserved.

## Local content checks

Fourteen unique IDs/routes, three signature flags, explicit parent destinations, all related destinations, mandatory interaction fields, fifteen exact-copy hashes and referenced image existence were checked. These are catalogue/data checks only. Rendered website QA and the final whole-site validation belong to the main development workflow. No new application test result or physical-device acceptance is claimed.
