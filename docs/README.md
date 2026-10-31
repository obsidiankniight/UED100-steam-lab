# Steam / Lab — UED100 Assessment 2 Prototype

A functional, independent **Steam Store UX redesign demonstration** based on the UED100 Assessment 1 analysis. **It is not an official Steam site, does not connect to Valve/Steam services, and cannot sell or launch real games.** All ten games, price figures, rating figures, friend names and artwork are fictional.

## Run on your computer

1. Extract the entire ZIP (retain the folder structure).
2. Open `index.html` in Chrome, Edge or Firefox, or preferably run a local server from the project folder:
   ```powershell
   python -m http.server 5500
   ```
   Then visit `http://localhost:5500` in your browser. This also allows SVG icon sprites to work reliably across browsers.
3. Use the top navigation or side navigation to move among **Store, Browse, Library, Wishlist, Cart**, and any game detail.

The project uses vanilla HTML, CSS and JavaScript with no build step, no external dependency, and no network/API access.

## Working prototype features

- Six interlinked HTML pages; responsive desktop/tablet/mobile layout.
- Steam-like visual identity with *original* SVG art for ten entirely fictional games.
- Search suggestions in the header; functional search, genre filters and sorting on Browse.
- Game details, individual wishlisting/cart controls, displayed AUD prices and live counts.
- Cart summary and a clearly labelled **simulated** checkout dialogue (no payment inputs).
- Collapsible homepage recommendation shelves; custom shelf visibility preferences.
- Wishlist, cart, shelf preferences and optional Library names saved locally through `localStorage`.
- Friends list that expands *upward* on hover, keyboard focus and by click/tap; Escape closes pinned view.
- **Add a non-Steam game** intentionally moved into the *bottom of the Library*, as a small secondary action (not prominent on Store pages). It stores a display name only and never executes an app.
- Basic accessible markup, meaningful labels/landmarks, keyboard focus, reduced motion preferences, local input validation, safe rendering of entered Library names via `textContent`.

## Source map

- `index.html` — Store; `browse.html` — filtered catalogue; `game.html?id=...` — dynamic game details.
- `wishlist.html` — saved games; `cart.html` — shopping cart/demo checkout; `library.html` — owned games and optional non-Steam names.
- `css/styles.css` — design system, responsive layout and focus states.
- `js/data.js` — fictional game catalogue, prices and tags.
- `js/app.js` — view rendering, state, navigation, dialogs, localStorage.
- `assets/covers/` — 10 self-authored SVG concept illustrations.
- `assets/icons/sprite.svg` — original local SVG icon sprite.
- `design/` — desktop/mobile wireframes, import instructions and user journeys.
- `tests/` — automated interaction checks, captured screenshots and test results.
- `docs/` — rationale, submission notes and supporting material.

## Technical choices and design rationale

Semantic HTML supports landmark-based navigation and accessibility. CSS Grid, Flexbox and media queries provide responsive layout without a third-party framework. JavaScript adds interactive filtering and shopping state, while `localStorage` avoids requiring a server. Demo inputs use DOM `textContent` and length/duplicate validation rather than injecting HTML; the project collects no passwords or payments. All SVG game artwork is local and scalable, with lazy loading for noncritical cards. Users control recommendation density; publishers retain discovery space instead of removing shelves.

## Verification and boundaries

Chromium automation checked interactions and a 390px mobile layout; the results are in `tests/TEST_RESULTS.md`. **Cross-browser real-device checks, genuine external user testing and Figma clickable-prototype publication are still to be completed by the student.** This is not a production security audit or real Steam integration.

## Git repository

Use this source folder as a local Git repository and make further meaningful commits while improving the project. Set up a remote repository (GitHub is fine), push the source, and include the real link in the UED100 assessment submission. A genuine initial commit history and captured results appear in `docs/COMMIT_HISTORY.txt` (generated locally). Do not invent a public repository URL.

## Original assets and license

All game names/art, descriptions, dummy prices, user avatars and mock friend names were authored for this assessment. Icons are original simple stroke vectors. Text 'Steam' refers to the subject of this student comparative UX exercise. Valve owns its trademarks; no affiliation or endorsement is implied.


## Updates completed after Assessment 1 mark (31 October 2026)

Assessment 1 received **91/100**, with no written feedback. New evidence: `docs/ASSESSMENT_1_TO_DESIGN_MATRIX.md`, repaired importable SVGs, an interactive browser design walkthrough (`design/interactive_wireframes.html`), and a mobile search entry point. See `docs/QA_STATUS.md` for exact test claims and limitations, and `tests/USABILITY_TEST_PLAN.md` for the actual participant-testing plan.

**Design tool and GitHub:** Figma and GitHub accounts must be connected by the student if the designs or source are to be published directly. Do not substitute the browser clickthrough for the brief's Figma/Adobe XD requirement.
