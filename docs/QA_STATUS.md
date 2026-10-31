# UED100 — QA and validation status

Date: 31 October 2026.

**Verified inside the working environment:**

- `python tests/source_audit.py`: passed local links, artwork and project structure audit.
- `python tests/browser_test.py`: **26/26** offline Chromium UI checks passed; this harness injects the real source into browser pages and simulates local storage because navigation is blocked.
- `python tests/design_walkthrough_test.py`: **9/9** validation checks passed, including parsing all three SVGs and switching between clickable design screens.
- Microsoft Word rationale rendered to a **clean single page**, with 208 words (excluding references).

**Not verified / still to do:**

- `python tests/live_site_test.py` runs a true local HTTP server and navigates browser pages, but **this cloud environment blocks all URL navigation**, including localhost, and returned `ERR_BLOCKED_BY_ADMINISTRATOR`. The script is provided for execution on the student's own computer. Do not claim those integration tests passed yet.
- Real participants have **not** tested usability. Use `tests/USABILITY_TEST_PLAN.md` and blank CSVs.
- Firefox, Safari and Edge have **not** been confirmed.
- Figma/Adobe XD project file and published prototype link have **not** been created. The SVG files and browser clickthrough are ready, but the required design-tool step remains.
- A public GitHub repository is **not** created. Local commits are real; publication requires the student's GitHub connection or credentials.

### Evidence that affected design

1. Desktop wireframe SVG contained an unescaped ampersand. XML validation failed; the SVG was repaired and all three designs now validate.
2. Mobile topbar hid the large desktop search field; a clearly labelled mobile search shortcut was added. It links to the working Browse view, where users can search and filter.
3. An unintended `$` was present in the Library add button's HTML; it was removed.

**Do not present automated test outputs as interviews or human-user feedback.**
