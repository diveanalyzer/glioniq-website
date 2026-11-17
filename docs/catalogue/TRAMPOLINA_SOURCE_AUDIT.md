# Trampolina catalogue source audit — 17 November 2026

Application repository: `/Users/igor/Documents/Repositories/trampolina`. Read-only inspection and final source refresh used HEAD `ba461a85f47d7c0e428612edca06dfeb0e4e9127`. The repository already contains local changes. Of the 24 files fingerprinted below, 23 are byte-identical to HEAD; `lib/app/app_controller.dart` contains pre-existing working changes. Its inspected working-file hash, rather than HEAD alone, identifies the challenge-mode evidence.

No application file, user record, device, simulator or application build was changed or executed for this website audit. Source implementation is not a claim of public availability, runtime acceptance or product-specific scientific efficacy.

## Website inventory

`content/catalogue/trampolina.json` contains **32 entries: one platform, six laboratories and 25 activity-information destinations**. All 14 previous routes remain: the platform, six laboratories and seven cognitive games. The additional 18 destinations explain existing stages or selectable modes; they are not presented as 18 new standalone games.

| Laboratory | Destinations beneath it |
|---|---|
| Colors | Visual Color Recognition; Find All Matching Colors; Listening-Based Color Recognition |
| Numbers & Mathematics | Number Recognition; Guided Counting; Quantities and Matching Groups; Number Writing; Addition; Subtraction; Number Challenge |
| Shapes | Learn Shapes; Shapes and Real-World Objects; Shapes and Matching Holes; Mixed Shape Practice |
| Letters | Letter Recognition; Letters, Objects and Words; Letter Writing; Letter Challenge |
| Memory & Perception | Memory Game; Picture Puzzle; Spot the Differences |
| Thinking & Logic | Continue the Pattern; Sorting Categories; First & Next; Odd One Out |

Every destination has an explicit parent, purpose, audience guidance, interaction details, tutorial, related links, artwork mapping and source evidence. The website provides explanatory guides; it does not launch these mobile activities as browser games.

## Implemented mechanics and stage boundaries

- **Colors:** six colors across five stages: one visible match, all visible matches, then three listening decisions. The latter are represented together by the listening guide. Difficulty changes choice density. A listening task requires its real approved target recording; a visible substitute cannot unlock it. `lib/features/colors/color_journey.dart:172–257`; `lib/features/colors/color_journey_screen.dart:166–174,350–440`.
- **Numbers:** current curriculum V6 runs demonstration → tracing → drawing → identification → counting → matching groups → quantity recognition. Number selections cover 1–5, 6–10 and 11–20. **Letters V3** runs demonstration → identification → object/word association → tracing → drawing. English, Hebrew and Russian alphabets use language-specific content; Russian Ъ, Ы and Ь use letter-in-word examples. **Shapes** uses demonstration → identification → matching → tracing, plus object matching and matching-hole activities. A separately selectable free-drawing Shapes game was not verified. `lib/app/trampolina_app.dart:704–715`; `lib/core/learning/curriculum_session.dart:110–163`; `lib/core/learning/curriculum_catalog.dart:1–18`; `lib/features/learning/curriculum_entry_screen.dart:55–70,110–145`; `lib/features/learning/curriculum_learning_screen.dart:536–551,758–1057`.
- **Actual selectable practice modes:** Number Challenge, Letter Challenge and Mixed Shape Practice each use five questions. Numbers alternates recognition and quantity; Letters and Shapes use recognition. Shapes mixed practice uses the four base shapes; focused learning uses the selected pool. These are modes within their laboratory, not new apps. `lib/app/app_controller.dart:1671–1684`; `lib/core/learning/curriculum_session.dart:153–163`; `lib/features/learning/shapes_category_screen.dart:294–378`.
- **Shape matching:** objects progress from one match to all matches; matching holes accepts a piece in the matching outline. Harder pools add shapes and board complexity. `lib/features/learning/shape_game.dart:73–80,148–227`.
- **Addition/Subtraction:** apples visibly join or move away; quantities remain within ten, with ranges up to five, up to ten or both. Manual practice targets four independent successes; Smart progression considers two successes at the hard level. Show me again, Another game, Back to Numbers World and supported endings are preserved as existing mechanics. No approved hint was changed. `lib/features/math/math_session.dart:6–9,47–115,131–145`; `lib/features/math/math_screens.dart:295–415`.

The seven cognitive identities and laboratory assignments come from `lib/features/cognitive/cognitive_catalog.dart:5–23`. Their current content version is four (`cognitive_session.dart:20–31`):

| Game | Verified mechanics | Principal source |
|---|---|---|
| Memory Game | 2 / 3–4 / 5–6 pairs; preview 3.6 / 2.4 / 1.5 seconds. Smart mode uses three levels; manual mode one board. Help preserves found pairs and marks assistance. | `cognitive_generator.dart:40–99`; `cognitive_session.dart:90–106,670–689` |
| Picture Puzzle | Reassemble real pieces from the same reference image; 2–4 / 6–8 / 9–12 pieces by difficulty. | `cognitive_generator.dart:149–177`; `cognitive_session.dart:733–752` |
| Spot the Differences | Find 1–2 / 3–4 / 5–6 changed details against a shared scene; missing, size and position variants. | `cognitive_generator.dart:251–300` |
| Continue the Pattern | Five boards with AB/AAB, ABC/AABB and harder AABC/ABBC/ABCD repeating units. | `cognitive_generator.dart:100–148` |
| Sorting Categories | Sort 4 / 6–8 / 9 objects by supported properties; harder boards combine shape and color. | `cognitive_session.dart:308–397` |
| First & Next | Order 3 / 4 / 5 frames from 15 authored stories. Completed stories can replay; captions and reading time remain when recordings are missing. | `cognitive_generator.dart:178–201`; `cognitive_game_screen.dart:625–718` |
| Odd One Out | Choose among 4 / 4 / 5 items; harder rounds include a reason choice; five boards. | `cognitive_generator.dart:202–250`; `cognitive_session.dart:704–728` |

Paths in this table are relative to `lib/features/cognitive/`. Help and replay behavior is additionally supported by `cognitive_game_screen.dart:92–111,625–718` and `cognitive_session.dart:664–752`.

## Audio, parent access and age limits

The audio inventory records **5,220 required full-instruction slots, all missing**, including 360 five-stage Colors slots. The 216 supplied MP3 feedback mappings remain praise/retry recordings; they are not full instructions. Only approved bundled recordings for the selected language and voice may be used, with no synthesized or cross-language fallback. Listening-based Colors remains unavailable until the appropriate recording is supplied and successfully played. `docs/MISSING_INSTRUCTION_AUDIO_INVENTORY.md:3–28`; `lib/core/audio/instruction_catalog.dart:12–44`.

The parent gate generates a random three-digit challenge and accepts the reversed sequence. It is **not a persistent PIN**. Parent settings expose language/voice, voice samples, optional reminders and daily/session limits. English/Hebrew/Russian interfaces and Noa/Mia/Niko/Leo voice identities do not establish availability of instructional recordings. Completion-based star rewards are recorded separately from individual taps. `lib/features/parent/parent_gate.dart:21–37`; `parent_settings_screen.dart:125–159,237–294`; `lib/core/audio/voice_catalog.dart:1–11`; `lib/features/rewards/reward_completion.dart:459–479`.

Ages 2–6, with selected harder activities potentially relevant at 7–8, are flexible editorial/product starting suggestions. They are not validated developmental norms, mandatory age gates, clinical assessments or efficacy claims. `docs/RESEARCH_EVIDENCE_REGISTER.md:27–44`.

## Artwork and final content review

Existing approved branding, cognitive-laboratory artwork and seven cognitive-game artworks remain unchanged. Colors, Numbers, Shapes and Letters reuse their existing proposal illustrations with `owner-review-required` status; no proposal is promoted to an official logo. No new artwork or gameplay screenshot was copied or generated for Trampolina. Dedicated stage/mode illustrations and approved website tutorial screenshots remain missing, with explicit laboratory-art fallbacks and empty screenshot lists.

Final sanity review reconfirmed 32 unique entries, the seven actual cognitive games, the three five-question modes, source-backed stage order, explicit narration gaps and the parent challenge/PIN distinction. The integrating pass narrowed Memory & Perception's age, screen and Help descriptions to its own memory boards, picture puzzles and visual differences; story playback is described only where applicable.

Whole-catalogue source/rendered verification previously passed with 102 entries, 113 generated pages and 112 search entries. That evidence does not establish app runtime, device acceptance, artwork approval or a production release. No data, build or Git changes were made during this final audit pass.

## Inspected working-file SHA-256 fingerprints

These hashes identify actual inspected application bytes. All match HEAD except the explicitly marked controller. Original files were preserved.

| File relative to the application root | SHA-256 |
|---|---|
| `assets/content/instruction_audio_manifest.json` | `5ba33ceb11a5a016756cd2d3c461587c308c7c448b6656206390c869fb16ccd8` |
| `docs/MISSING_INSTRUCTION_AUDIO_INVENTORY.md` | `b38351632fd75d3e6d4661de16cd42f0daa9693754bf20b03181bc167a6805c3` |
| `docs/RESEARCH_EVIDENCE_REGISTER.md` | `cf7eeb1a4f4fc7fd0cf6f95795bc1882c0e8adc874f1c959c53066100df9a60f` |
| `lib/app/app_controller.dart` — existing working changes | `b4431c6f0529d2075766eebfc5c7ec4ccb39d59b63b7e31424b053437b1521b9` |
| `lib/app/trampolina_app.dart` | `0372a7bfe623c98c73d02fb8d8a5c0a6769bb963fc9efe8b20d8197720570884` |
| `lib/core/audio/instruction_catalog.dart` | `a0cc7d6da6a81fed713e675a6828d4f00b5441e5ea37c239d8d13dd8285bac31` |
| `lib/core/audio/voice_catalog.dart` | `b7328f35261aea4437d066cae5677df572e0c516abce4763fabd3fd1db11cdbb` |
| `lib/core/learning/curriculum_catalog.dart` | `14ce234d700ae5f4ca4a41476370df37652a765dc1bbe0d06891484370303e12` |
| `lib/core/learning/curriculum_session.dart` | `cb19764e107398c45a452d9f02c1b677e6ffa9331876b32b57aba06756c745ac` |
| `lib/features/cognitive/cognitive_catalog.dart` | `736f3b4b26a80a55ae28d8b7901bbc20e8383f75c8d0ee9ab460c2d9368d0729` |
| `lib/features/cognitive/cognitive_game_screen.dart` | `f70fb1e0299b420cfc137171776ef487ce94f593b8e5e4e12d40dddade1f7d04` |
| `lib/features/cognitive/cognitive_generator.dart` | `ca96fded511a8bf7de943120e16bb05d54918543e58babe72a16990a254aeb42` |
| `lib/features/cognitive/cognitive_session.dart` | `d6647a0a0756e7e8b342f854e59cd39a8c5c75c1e9415a214eb8f28a76ffcd17` |
| `lib/features/colors/color_journey.dart` | `2c0f62a02b46c05fd34c698252fee30481f2d37ac0ec9230afe1320cadbc81bd` |
| `lib/features/colors/color_journey_screen.dart` | `a155541dfd6318deb901fe9cc9a14cd2230a00f04a728f4c57e0cd0c0468a01b` |
| `lib/features/learning/curriculum_entry_screen.dart` | `7c6cc85afddaf783a889763c9e7a8aff2398ae166b1533c7aa81e13c88e3a1a3` |
| `lib/features/learning/curriculum_learning_screen.dart` | `1eac25e7179cd53b8783b14e4df4ef52871ea858379824092a2ff7ec96a5677e` |
| `lib/features/learning/shape_game.dart` | `6ca0b62c87ba8be2a97a52f36374b7d86c00846a55832bf110c614fde93b7b5c` |
| `lib/features/learning/shapes_category_screen.dart` | `e507ad865a3e7edee744416c3fe679950e3c650e9c25cf02a531266cf86cd0b7` |
| `lib/features/math/math_screens.dart` | `a4413fcf9d073c00f28b42f9db8ccf9dab10085d9186209f98d426e45338fc46` |
| `lib/features/math/math_session.dart` | `4105f34542540c5a56cae7d7a9f9353528c82afe28e2bc72ab95d1f02c24ee8f` |
| `lib/features/parent/parent_gate.dart` | `245fb2798e98479ec51b5c30290b335e3ddee350cdf76ff247999341e92a55d2` |
| `lib/features/parent/parent_settings_screen.dart` | `9d9f9ad5ebefcb6e9661bb71c9050ea5ffb2580b36178fa6a4554ce07d036f4b` |
| `lib/features/rewards/reward_completion.dart` | `62524240547d6d8e0caf655a11d8047dec30f73c8be2b89cc64e578678b7a127` |
