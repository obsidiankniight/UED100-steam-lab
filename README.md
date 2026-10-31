# UED100 — Steam / Lab

This is a responsive, interactive student UX prototype redesign of the Steam Store, using original concept artwork and fictional game data.

**Start:** open `index.html`, or for full local icon support open a terminal in this folder and run `python -m http.server 5500`, then go to `http://localhost:5500`.

**Full instructions:** see [docs/README.md](docs/README.md).

**Still required for the assessment:** import wireframes into Figma/Adobe XD, carry out real-user and cross-browser tests, add your Assessment 1 marker feedback when received, publish the Git repo, and include the link in your submission.


## Assessment 2 review update

Open `design/interactive_wireframes.html` for the **clickable design walkthrough**, or `index.html` for the functional store. `docs/ASSESSMENT_1_TO_DESIGN_MATRIX.md` traces each requirement to implemented evidence. `docs/QA_STATUS.md` distinguishes passed automated checks from outstanding human and external tests. The 208-word technical rationale lives in `docs/Technical_Rationale.docx`.

For local navigation smoke tests on your PC: `pip install playwright`, `python -m playwright install chromium`, then `python tests/live_site_test.py` from this project directory. (This was blocked in the cloud environment, not reported as passed.)
