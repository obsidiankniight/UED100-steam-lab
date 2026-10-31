# UED100 — Usability testing protocol (uncompleted)

**Status: awaiting real participants.** Do not report any findings or fixes as participant feedback until testing actually occurs. This exercise is separate from the existing browser automation, which checks functionality but cannot establish whether real users understand the interface.

## Purpose and approach

Assessment 1 identified two user groups: new/casual shoppers (need simpler discovery and clearer navigation) and returning customers (value recommendations and wishlist features). Test with **at least one person who is new to Steam and one familiar with Steam**, ideally 3 participants. Record only anonymous labels such as T1/T2/T3; do not collect names, emails, account details, or payment information. Participation should be voluntary.

Explain: “This is a fictional shopping prototype for university. No purchase is real. I am testing the interface, not you. Please think aloud; you can stop at any time.” Give the participant 60 seconds to explore. Do not tell them where the controls are during tasks. Record whether they finish unassisted (yes/no), approximate task time, errors/confusion, and direct feedback.

## Tasks (same order for every participant)

| ID | Task prompt (read aloud) | Target evidence |
|---|---|---|
| U1 | Find a role-playing game and add it to your wishlist. | Navigation/search/genre filter and wishlist count |
| U2 | Find Neon Drift, put it in the shopping cart, and view the total. Do not enter payment details. | Game details → cart → total |
| U3 | Hide a recommendation shelf on the homepage. Refresh the page. Is your preference remembered? | Customise shelves, persistence |
| U4 | Open Friends & Chat and close it. If possible, repeat using keyboard only. | Hover/click/keyboard access and Escape |
| U5 | Go to Library and find the option to add a game from outside Steam. | Secondary action discoverability (expected: findable without dominating Store) |

## Follow-up questions

1. What was the easiest part of the website to understand?
2. Where were you unsure what to do next?
3. Did anything feel like it took too many clicks or was visually crowded?
4. Was the Friends control or non-Steam option where you expected it?
5. What is **one improvement** that would help you most?

## Measures and decisions

Use `USABILITY_RESULTS_TEMPLATE.csv`. After the sessions, summarise task-success percentages, median approximate task time (when recorded), recurrent confusions, and the top two fixes. Make at least one justified change, test the changed functionality again, and record a before/after entry in `ITERATION_LOG_TEMPLATE.csv` or a new Markdown log. If a participant fails a task, describe what happened, not a judgement about them. Do **not** invent participant quotes or change logs.

## Cross-browser/device testing to complete on a normal computer

Chrome, Edge, Firefox, and Safari (where available): verify home, search, wishlist, cart, dialogs, keyboard navigation, 320px/390px mobile viewport and desktop layout. Record browser, OS, version, pass/fail, screenshots and fixes in `CROSS_BROWSER_TEMPLATE.csv`. Automated Chromium checks do **not** establish Safari/Firefox/Edge compatibility.
