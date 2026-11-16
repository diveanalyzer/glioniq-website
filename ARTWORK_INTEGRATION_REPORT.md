# GlionIQ official artwork integration — local review

Date: 16 November 2026. Branch: `development/glioniq-homepage-v2`. Starting HEAD: `c289642`. Local working changes only; no commit, push, merge, deployment, publication or DNS change in this task.

Preview: [local homepage](http://127.0.0.1:8787/). The loopback preview is running with publication disabled.

27 supplied images were inspected across all four directories and every nested directory: Trampolina 10, Dr. Quiz 4, NeuroPath 12, NeuroBreath 1. Three `.DS_Store` files are Finder metadata, not artwork. Existing GlionIQ branding and the approved homepage reference were also inspected.

The integration maps all 30 existing platform/laboratory/activity pages to 27 visual assets. It replaces generic category SVGs with supplied artwork or four explicitly unapproved illustration proposals. No games, mechanics or routes were added.

## Preservation and display decisions

- The homepage Hero, existing main product logos, typography, backgrounds, card borders, navigation, search and approved copy remain intact. Main card logos come from the authoritative approved homepage reference; they are not replaced by a new character illustration or the opaque checkerboard NeuroPath logo reference.
- The standalone supplied Trampolina logo and Dr. Quiz character appear on their platform pages. NeuroPath uses a clean logo region from its supplied home screenshot; the new NeuroBreath file is byte-identical to the existing approved orb.
- Source files are untouched. Separate PNG extraction masters retain exact source RGB pixels. Documented alpha masks remove neutral background areas and small unrelated screenshot text/control fragments; they never repaint the artwork. The full Trampolina brand retains its white background to preserve the dark slogan contrast.
- Separate lossless WebP card exports are limited to 640 pixels, retaining full composition and aspect ratio. CSS uses `object-fit: contain`; artwork is not stretched or cover-cropped. All 27 served exports total approximately 7.70 MiB, versus 29.40 MiB for the extraction masters.
- NeuroWeave and CodeQuest retain embedded English wordmarks without repeating a visible card heading. Their names remain accessible. Trampolina Hebrew lettering is preserved; English headings are translations for the English website.
- NeuroBreath methods share the approved neural orb. Their existing route diagrams remain explanatory content, not substitute product artwork. The Memory Lab activity uses its own cube tile from the approved daily-training screenshot; the parent Memory Lab retains the brain-and-memory-cards illustration.

## Verification

| Check | Result | Evidence |
|---|---|---|
| Build | PASS | 37 pages generated; 36 content pages indexed |
| Existing static verification | PASS | 37 balanced pages, 1,104 local references, 61 exact About Us blocks, 6 protected source checks |
| Asset inventory and integrity | PASS | 27 supplied originals; 27 source/extraction/web hash sets; all 30 destinations mapped |
| Original-file preservation | PASS | All 51 image, provenance and design-reference files present at start remain byte-identical |
| Extraction integrity | PASS | Every extraction master retains the exact source RGB values, including JPEG-decoded crops; only documented alpha changes occur |
| Local HTTP | PASS | 88 unique referenced URLs return 200 and match repository bytes |
| Search verification | PASS | Existing Node verification and Safari query/result/no-results/blank-query checks |
| Editorial regression | PASS | 8 existing isolated test groups; no live draft modifications |
| Safari responsive checks | PASS | All 37 pages at 320, 390, 768, 1024 and 1440 px: 185/185; no missing images, horizontal overflow or captured JavaScript/resource errors |
| Visual inspection | PASS | Supplied originals, proposed illustrations, selected crop outputs, desktop NeuroPath game cards and 320px expanded Trampolina tree inspected |
| Physical devices / other browsers / full assistive-technology audit | NOT VERIFIED | Safari desktop with responsive iframes is not physical-device certification |
| Production | NOT VERIFIED in this task | No deployment or live-state changes; this report covers the local implementation |

## Mapping by destination

Each asset key resolves to the exact original, crop coordinates, alpha method, dimensions and SHA-256 values in [artwork-map.json](content/artwork-map.json). All served paths below are relative to the repository root.

| Platform / laboratory / activity | Local route | Asset key | Approval status |
|---|---|---|---|
| Trampolina | [/laboratories/trampolina/](http://127.0.0.1:8787/laboratories/trampolina/) | `trampolina-brand` | Approved source, separate derivative |
| Dr. Quiz | [/laboratories/dr-quiz/](http://127.0.0.1:8787/laboratories/dr-quiz/) | `dr-quiz-character` | Approved source, separate derivative |
| NeuroPath | [/laboratories/neuropath/](http://127.0.0.1:8787/laboratories/neuropath/) | `neuropath-brand` | Approved source, separate derivative |
| Memory Lab | [/laboratories/neuropath/memory/](http://127.0.0.1:8787/laboratories/neuropath/memory/) | `memory` | Approved source, separate derivative |
| Attention Lab | [/laboratories/neuropath/attention/](http://127.0.0.1:8787/laboratories/neuropath/attention/) | `attention` | Approved source, separate derivative |
| Logic Lab | [/laboratories/neuropath/logic/](http://127.0.0.1:8787/laboratories/neuropath/logic/) | `logic` | Approved source, separate derivative |
| Flexibility Lab | [/laboratories/neuropath/flexibility/](http://127.0.0.1:8787/laboratories/neuropath/flexibility/) | `flexibility` | Approved source, separate derivative |
| Colors | [/laboratories/trampolina/colors/](http://127.0.0.1:8787/laboratories/trampolina/colors/) | `colors` | Owner review required — generated illustration |
| Numbers | [/laboratories/trampolina/numbers/](http://127.0.0.1:8787/laboratories/trampolina/numbers/) | `numbers` | Owner review required — generated illustration |
| Shapes | [/laboratories/trampolina/shapes/](http://127.0.0.1:8787/laboratories/trampolina/shapes/) | `shapes` | Owner review required — generated illustration |
| Letters | [/laboratories/trampolina/letters/](http://127.0.0.1:8787/laboratories/trampolina/letters/) | `letters` | Owner review required — generated illustration |
| Memory & Perception | [/laboratories/trampolina/memory-perception/](http://127.0.0.1:8787/laboratories/trampolina/memory-perception/) | `memory-perception` | Approved source, separate derivative |
| Thinking & Logic | [/laboratories/trampolina/thinking-logic/](http://127.0.0.1:8787/laboratories/trampolina/thinking-logic/) | `thinking-logic` | Approved source, separate derivative |
| Challenge Me | [/laboratories/dr-quiz/challenge-me/](http://127.0.0.1:8787/laboratories/dr-quiz/challenge-me/) | `challenge-me` | Approved source, separate derivative |
| Party Quiz | [/laboratories/dr-quiz/party-quiz/](http://127.0.0.1:8787/laboratories/dr-quiz/party-quiz/) | `party-quiz` | Approved source, separate derivative |
| Discover & Learn | [/laboratories/dr-quiz/discover-learn/](http://127.0.0.1:8787/laboratories/dr-quiz/discover-learn/) | `discover-learn` | Approved source, separate derivative |
| NeuroBreath | [/laboratories/neurobreath/](http://127.0.0.1:8787/laboratories/neurobreath/) | `neurobreath` | Approved source, separate derivative |
| Square Focus | [/laboratories/neurobreath/square-focus/](http://127.0.0.1:8787/laboratories/neurobreath/square-focus/) | `neurobreath` | Approved source, separate derivative |
| Sleep Calm | [/laboratories/neurobreath/sleep-calm/](http://127.0.0.1:8787/laboratories/neurobreath/sleep-calm/) | `neurobreath` | Approved source, separate derivative |
| Neural Wave | [/laboratories/neurobreath/neural-wave/](http://127.0.0.1:8787/laboratories/neurobreath/neural-wave/) | `neurobreath` | Approved source, separate derivative |
| Memory Lab | [/laboratories/neuropath/memory/memory-activity/](http://127.0.0.1:8787/laboratories/neuropath/memory/memory-activity/) | `memory-activity` | Approved source, separate derivative |
| NeuroWeave | [/laboratories/neuropath/logic/neuroweave/](http://127.0.0.1:8787/laboratories/neuropath/logic/neuroweave/) | `neuroweave` | Approved source, separate derivative |
| CodeQuest | [/laboratories/neuropath/logic/codequest/](http://127.0.0.1:8787/laboratories/neuropath/logic/codequest/) | `codequest` | Approved source, separate derivative |
| Memory Game | [/laboratories/trampolina/memory-perception/memory-game/](http://127.0.0.1:8787/laboratories/trampolina/memory-perception/memory-game/) | `memory-game` | Approved source, separate derivative |
| Picture Puzzle | [/laboratories/trampolina/memory-perception/picture-puzzle/](http://127.0.0.1:8787/laboratories/trampolina/memory-perception/picture-puzzle/) | `picture-puzzle` | Approved source, separate derivative |
| Spot the Differences | [/laboratories/trampolina/memory-perception/spot-differences/](http://127.0.0.1:8787/laboratories/trampolina/memory-perception/spot-differences/) | `spot-differences` | Approved source, separate derivative |
| Continue the Pattern | [/laboratories/trampolina/thinking-logic/continue-pattern/](http://127.0.0.1:8787/laboratories/trampolina/thinking-logic/continue-pattern/) | `continue-pattern` | Approved source, separate derivative |
| Sorting Categories | [/laboratories/trampolina/thinking-logic/sorting-categories/](http://127.0.0.1:8787/laboratories/trampolina/thinking-logic/sorting-categories/) | `sorting-categories` | Approved source, separate derivative |
| First & Next | [/laboratories/trampolina/thinking-logic/first-next/](http://127.0.0.1:8787/laboratories/trampolina/thinking-logic/first-next/) | `first-next` | Approved source, separate derivative |
| Odd One Out | [/laboratories/trampolina/thinking-logic/odd-one-out/](http://127.0.0.1:8787/laboratories/trampolina/thinking-logic/odd-one-out/) | `odd-one-out` | Approved source, separate derivative |

## Exact source mapping

| Asset key | Supplied original or generated proposal | Extraction |
|---|---|---|
| `trampolina-brand` | [526CFEED-567B-4C82-A7E9-21B7CDF1ACF2 3.png](<public/images/laboratories/trampolina/526CFEED-567B-4C82-A7E9-21B7CDF1ACF2 3.png>) | Full frame |
| `memory-perception` | [78612329-716C-4B2E-A379-5969D6209669.png](<public/images/laboratories/trampolina/78612329-716C-4B2E-A379-5969D6209669.png>) | Full frame; neutral-background alpha extraction; enclosed background seeds [[750, 440]] |
| `thinking-logic` | [56D2556C-E502-49F1-90F3-A1D30C4F1621.png](<public/images/laboratories/trampolina/56D2556C-E502-49F1-90F3-A1D30C4F1621.png>) | Full frame; neutral-background alpha extraction; enclosed background seeds [[980, 455], [1085, 560], [900, 80], [955, 80]] |
| `memory-game` | [6F105743-02F3-479E-BDDB-7EC1908DC771 2.png](<public/images/laboratories/trampolina/6F105743-02F3-479E-BDDB-7EC1908DC771 2.png>) | Full frame; neutral-background alpha extraction |
| `picture-puzzle` | [08471A48-DD4B-41BC-8A0D-5F843D58737B.png](<public/images/laboratories/trampolina/08471A48-DD4B-41BC-8A0D-5F843D58737B.png>) | Full frame; neutral-background alpha extraction |
| `spot-differences` | [DFBEE128-E301-44F3-9316-092A7B7E2713.png](<public/images/laboratories/trampolina/DFBEE128-E301-44F3-9316-092A7B7E2713.png>) | Full frame; neutral-background alpha extraction |
| `continue-pattern` | [AAB54338-01FE-46AB-8BF5-3A39FD3F9786.png](<public/images/laboratories/trampolina/AAB54338-01FE-46AB-8BF5-3A39FD3F9786.png>) | Full frame; neutral-background alpha extraction |
| `sorting-categories` | [A357F62F-4375-4B51-A261-5163FF7ADB06.png](<public/images/laboratories/trampolina/A357F62F-4375-4B51-A261-5163FF7ADB06.png>) | Full frame; neutral-background alpha extraction |
| `first-next` | [FEB9898E-F8C1-4B0E-837D-3C3A3814FF77.png](<public/images/laboratories/trampolina/FEB9898E-F8C1-4B0E-837D-3C3A3814FF77.png>) | Full frame; neutral-background alpha extraction |
| `odd-one-out` | [1B2081EC-7484-4C5A-BF82-8B3721C02205.png](<public/images/laboratories/trampolina/1B2081EC-7484-4C5A-BF82-8B3721C02205.png>) | Full frame; neutral-background alpha extraction |
| `colors` | [trampolina-colors-3d-review.png](<public/images/laboratories/generated-review/trampolina-colors-3d-review.png>) | Full frame |
| `numbers` | [trampolina-numbers-3d-review.png](<public/images/laboratories/generated-review/trampolina-numbers-3d-review.png>) | Full frame |
| `shapes` | [trampolina-shapes-3d-review.png](<public/images/laboratories/generated-review/trampolina-shapes-3d-review.png>) | Full frame |
| `letters` | [trampolina-letters-3d-review.png](<public/images/laboratories/generated-review/trampolina-letters-3d-review.png>) | Full frame |
| `dr-quiz-character` | [C514A1B2-697F-4527-BF9E-E3BA8FBA2368.png](<public/images/laboratories/dr-quiz/C514A1B2-697F-4527-BF9E-E3BA8FBA2368.png>) | Full frame |
| `challenge-me` | [challenge-me.png](<public/images/laboratories/dr-quiz/challenge-me.png>) | Crop [80, 16, 579, 351] (left, top, right, bottom) |
| `discover-learn` | [discover-and-learn.png](<public/images/laboratories/dr-quiz/discover-and-learn.png>) | Crop [32, 20, 545, 412] (left, top, right, bottom) |
| `party-quiz` | [party-quiz.png](<public/images/laboratories/dr-quiz/party-quiz.png>) | Crop [70, 20, 625, 389] (left, top, right, bottom) |
| `memory` | [game_selection.jpeg](<public/images/laboratories/neuropath/06_games/game_selection.jpeg>) | Crop [58, 309, 352, 508] (left, top, right, bottom); clear unrelated UI region [260, 0, 294, 75] |
| `attention` | [game_selection.jpeg](<public/images/laboratories/neuropath/06_games/game_selection.jpeg>) | Crop [630, 305, 881, 511] (left, top, right, bottom) |
| `logic` | [game_selection.jpeg](<public/images/laboratories/neuropath/06_games/game_selection.jpeg>) | Crop [632, 555, 866, 753] (left, top, right, bottom) |
| `flexibility` | [game_selection.jpeg](<public/images/laboratories/neuropath/06_games/game_selection.jpeg>) | Crop [62, 556, 307, 754] (left, top, right, bottom) |
| `neuroweave` | [game_selection.jpeg](<public/images/laboratories/neuropath/06_games/game_selection.jpeg>) | Crop [719, 884, 895, 1059] (left, top, right, bottom) |
| `codequest` | [game_selection.jpeg](<public/images/laboratories/neuropath/06_games/game_selection.jpeg>) | Crop [923, 884, 1098, 1060] (left, top, right, bottom) |
| `memory-activity` | [training_duration.jpeg](<public/images/laboratories/neuropath/05_daily_training/training_duration.jpeg>) | Crop [995, 654, 1125, 747] (left, top, right, bottom) |
| `neuropath-brand` | [home.jpeg](<public/images/laboratories/neuropath/03_home/home.jpeg>) | Crop [205, 70, 815, 508] (left, top, right, bottom); clear unrelated UI region [565, 0, 610, 18] |
| `neurobreath` | [IMG_0020 3.JPG](<public/images/laboratories/neurobreath/IMG_0020 3.JPG>) | Full frame |

## Reference-only files

These supplied images were inspected and preserved. They are not flattened into website cards or treated as instructions to implement additional features.

| File | Reference role |
|---|---|
| [approved_logo_reference.jpeg](<public/images/laboratories/neuropath/01_brand_logo/approved_logo_reference.jpeg>) | Approved brand reference with opaque baked checkerboard; retained unchanged, not used as a transparent logo |
| [registration_login_flow.jpeg](<public/images/laboratories/neuropath/02_onboarding/registration_login_flow.jpeg>) | NeuroPath visual reference for registration login flow |
| [profile_dashboard.jpeg](<public/images/laboratories/neuropath/04_profile/profile_dashboard.jpeg>) | NeuroPath visual reference for profile dashboard |
| [profile_setup_flow.jpeg](<public/images/laboratories/neuropath/04_profile/profile_setup_flow.jpeg>) | NeuroPath visual reference for profile setup flow |
| [daily_training_progress.jpeg](<public/images/laboratories/neuropath/05_daily_training/daily_training_progress.jpeg>) | NeuroPath visual reference for daily training progress |
| [logic_lab_reference.jpeg](<public/images/laboratories/neuropath/06_games/logic_lab_reference.jpeg>) | NeuroPath visual reference for logic lab reference |
| [achievements.jpeg](<public/images/laboratories/neuropath/07_rewards/achievements.jpeg>) | NeuroPath visual reference for achievements |
| [progress.jpeg](<public/images/laboratories/neuropath/08_progress/progress.jpeg>) | NeuroPath visual reference for progress |
| [settings.jpeg](<public/images/laboratories/neuropath/09_settings/settings.jpeg>) | NeuroPath visual reference for settings |

## Additional games visible in references

| Referenced game | Source | Website integration |
|---|---|---|
| Synapse Forge, OrbitMind, EchoShift | `neuropath/06_games/game_selection.jpeg` | Inventoried only; no existing destination |
| PatternGrid, LogicFlow | `neuropath/06_games/logic_lab_reference.jpeg` | Inventoried only; no existing destination |
| Target Hunt, Rule Shift | `neuropath/05_daily_training/training_duration.jpeg` and `daily_training_progress.jpeg` | Inventoried only; no existing destination |
| Light Paths | No matching supplied artwork identified | No route or laboratory assignment added |

## Owner review and source limitations

The separate [artwork review list](ARTWORK_REVIEW.md) contains the four generated proposals. None is an officially approved logo. Exact prompts and reference roles are recorded in [artwork-generation.json](content/artwork-generation.json); the built-in image generation tool was used.

For a later high-resolution brand release, clean transparent master exports would improve the two checkerboard-backed Trampolina category sources and the NeuroPath standalone logo. Dr. Quiz category inputs are photographed/cropped references with source texture; NeuroPath game tiles are small screenshot crops; the Memory Lab activity tile is only 130×93 px and its display is limited to 160 px. Higher-resolution masters are still desirable. These limitations are preserved and disclosed, not concealed by redrawing approved graphics. Current local cards use the best available supplied artwork.

Publication remains pending explicit owner approval. Approval of the four illustrations and the final visual integration is still outstanding.

## Reproduction

Build and checks: `python3 -B scripts/build.py`, `python3 -B scripts/verify.py`, `python3 -B scripts/verify_artwork.py`, `python3 -B scripts/verify_http.py http://127.0.0.1:8787`, and `python3 -B scripts/verify_editorial.py`. Search uses the existing `scripts/verify_interactions.js`.

Asset extraction is optional authoring work: run `scripts/prepare_laboratory_artwork.py` with Pillow 10.4.0. It writes only named derivatives and the mapping, retaining original assets. Normal builds have no Pillow dependency.
