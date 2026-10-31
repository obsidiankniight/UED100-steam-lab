# Figma / Adobe XD design handoff — still requires student account

**Important:** This folder contains valid editable SVG wireframes and a working browser click-through (`interactive_wireframes.html`). These are **not** a completed Figma/Adobe XD project. The UED100 brief explicitly specifies using one of those tools to create wireframes and interactive mockups.

## Import the frames

1. In Figma, start a new design file. Import (drag/drop or Place image) `desktop_home_wireframe.svg`, `desktop_game_wireframe.svg`, and `mobile_home_wireframe.svg`.
2. Verify shapes and text after import; convert/group SVG elements into named frames as needed. Native editable Figma layers may require ungrouping imported vectors; not all SVG text edits behave identically to native Figma text.
3. Name frames **D1 — Store Desktop (1440)**, **D2 — Game Detail (1440)**, and **M1 — Store Mobile (390)**.
4. In Prototype mode, set D1 as desktop flow starting point and M1 as mobile flow starting point. Connect links as below. Use a local fictional game name and original art.
5. Run Preview / Present and verify each navigation link. Add screenshot(s) and the **actual share URL** to `docs/SUBMISSION_CHECKLIST.md`. Do not list a placeholder URL as completed.

## Required click connections

| From | Interactive component | To | Behaviour |
|---|---|---|---|
| D1 Store | Featured game artwork / CTA | D2 Game Detail | Navigate on click |
| D2 Game Detail | Back to discovery | D1 Store | Navigate on click |
| M1 Mobile Store | Featured game CTA | Mobile details (duplicate/rescale D2) | Navigate on click |
| D1 Store | Friends & Chat | Open overlay with upward positioning | On hover if supported; also click/tap |
| D1 Store | Browse | Browse screen (can create a simplified extra frame) | Navigate on click |

Use `interactive_wireframes.html` as a reference for hotspot placement and flow design; the working HTML prototype remains the functional implementation.

## Visual design and scope

Use the existing original game artwork in `assets/covers/` and the palette from `css/styles.css`. Document that the simplified navigation and collapsible content address novice discovery, while the wishlist, featured shelf and tags preserve returning-user and publisher needs from Assessment 1. The **Add a non-Steam game** action belongs as a small secondary control at the bottom of Library; do not add it to the Store.

**Evidence to submit:** Figma/Adobe XD project URL or exported design proof, screenshots of interaction connections, and a one-line statement that the clickable flows were tested. Never claim this step is complete until verified.
