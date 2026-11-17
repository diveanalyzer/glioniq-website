# Dr. Quiz catalogue source audit — 17 November 2026

The active iOS source is `DrQuiz/experiments/IQuiz-Expansion`, as identified by that repository's `AGENTS.md` and README. It was inspected read-only. No mobile source, data, simulator or device was modified or tested for this website task.

The inspected app HEAD is `ff1869340e9b5658a57cea47914426b7c0904e31`, with existing local edits. Catalogue **483**, revision `2026-11-17-inventions-sports-five-disciplines`, is a **preview** containing 1,271 fact–question pairs, 28 categories and 20 subcategories. Do not attribute this whole snapshot to the app HEAD: the website JSON records hashes of the actual inspected working files. Every fact and question has seven locale records: English, Hebrew, Russian, French, German, Spanish and Italian. This does not establish public release, translation acceptance or editorial approval of every record.

## Website inventory

`content/catalogue/dr-quiz.json` contains 52 stable entries: one platform, three existing experience routes, 28 canonical knowledge-topic pages and 20 actual subcategory pages. Topic pages are canonical under Discover & Learn and can be linked from other experiences without duplicating all categories. Parent paths follow actual subcategory parent IDs, including Italy → Piedmont → Barolo and Neuroscience → its child topics. The app's subcategory search includes descendant content (`Features/CategoryBrowser.swift:27–44`), so the two empty direct wine groupings still have meaningful descendant content.

No individual fact was invented as a new game. Favorites and My Mix remain collection controls, not invented content categories. Detailed topic descriptions were checked against current category content. Topic counts describe this source snapshot, not a promise of public availability.

## Mechanics evidence

- **Challenge Me:** four shuffled answers, one submission per question, explanations, correct/answered score, a chosen session limit or unlimited play, and score-preserving review. `Core/Models.swift:406–432,459–480,603–630`; `Features/SessionView.swift:390–440,481–490`; `Features/SettingsView.swift:338–371`.
- **Party Quiz:** one-device moderator flow, 2–12 players, category or wheel mode, 3/5/10 rounds or free play. Correct scores are 5/10 for category/wheel, reduced to 3/5 with a hint; incorrect scores 0. Hint gives four choices and one attempt. `Core/PartyQuiz.swift:3–18,31–43,135–180,206–252`; `Features/PartyQuizView.swift:437–519`; `Resources/strings.json:4917`.
- **Discover & Learn:** fact/context/illustration, Source, Quiz Me, independent Favorites, explicit Next acknowledgement and finite unseen rounds. `Features/SessionView.swift:238–265,289–319,481–487`; `Core/Models.swift:290–339,518–567,648–670`.
- **Like discrepancy:** the owner-approved direction says Like influences recurrence. Current inspected code stores Like as a reaction but no weighting is present in selection. Dislike filters automatic learning; explicit Favorites and search can still reveal a hidden fact. Website copy identifies recurrence personalization as unverified, and no app implementation was added. `Core/AppStore.swift:39–68,277–305`.
- **Difficulty/age:** no fixed easy/medium/hard field or numerical age rating was found. Topic difficulty is described in terms of prior knowledge; no unsupported rating, certification or developmental guarantee is asserted.
- **Sound:** optional game feedback is verified. General spoken fact/question narration is not verified; Party Quiz speech comes from its moderator and participants.

## Explicit exclusion: inactive Sailing course

The retained Sailing signal-card code is historical recovery material. The owner removed separate Sailing learning/practice/exam navigation. Current `App/IQuizBoosterApp.swift:23–30` has no such route; `Docs/ContentExpansion/SAILING-STANDARD-CATEGORY349-2026-10-29.md` documents the removal. The website therefore represents the current ordinary Yachting & Sailing facts/quiz category, not an invented playable signal course.

## Artwork provenance and review

The existing website's official character and three experience artworks remain unchanged. Two app atlases were copied byte-for-byte to `public/images/laboratories/dr-quiz/catalogue/originals/`:

- `owner-category-atlas.png`: owner-supplied 1206×785 reference, provenance `Docs/Design/OwnerMascot-2026-10-19/DISCOVERY-PROMPTS.md:3,8`.
- `prior-generated-extra-atlas.png`: previous 1254×1254 generated illustration sheet. Specific final owner approval is unverified.

`content/catalogue/dr-quiz-assets.json` records source hashes, original dimensions, 28 derivative hashes, exact crop rectangles and usage. Twenty-five topic crops use the owner atlas. Three existing illustration crops (Diving, Yachting & Sailing, Mythology & Ancient Cultures) remain provisional and require owner visual review. No new image generation occurred in this subtask. The retired “amazing” atlas quadrant does not create a new category.

The app's native 96px crop coordinates are retained in metadata as identity evidence (`App/Theme.swift:343–394`). Visual inspection found some native viewports cut object edges or caught a border. Website crops were therefore individually bounded against the unchanged original atlas, excluding Russian labels and unrelated card UI. These are compact category images, not new official logos; `artwork_compact` and a separate experience `hero_artwork_route` prevent enlarging small icons into a large hero. Subcategories explicitly reuse their parent's topic artwork, with missing dedicated illustrations recorded.

No genuine gameplay screenshots were imported in this subtask. Their absence is recorded without broken placeholders or fabricated screenshots. The 28 final crop derivatives were inspected together against the source atlas; this is artwork review, not rendered-page or device acceptance.

## Local checks

JSON parsing, 52 unique IDs/routes, valid parent relationships, all related-route targets, 28 derivative hashes and source/original hash equality were checked. No build, staging, commit, push or deployment was performed by this subtask. Website integration and rendered-page QA belong to the root task.
