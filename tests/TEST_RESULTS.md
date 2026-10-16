# Functional test results

**26/26 checks passed.**

- PASS: Homepage renders 3 game shelves
- PASS: All original game covers load
- PASS: Friends dock initially collapsed
- PASS: Friends panel expands upward on hover
- PASS: Friends panel can stay open on click
- PASS: Escape closes pinned friend panel
- PASS: Wishlist updates live count
- PASS: Cart updates live count
- PASS: Personalise shelves hides selected shelf
- PASS: No browser scripting errors on home
- PASS: Browse search filters results
- PASS: Genre filters return relevant results
- PASS: Clearing filters restores catalogue
- PASS: Game detail has artwork, price and buttons
- PASS: Empty cart shows actionable empty state
- PASS: Populated cart computes correct AUD total
- PASS: Checkout is explicitly demo-only
- PASS: Empty wishlist shows actionable empty state
- PASS: Non-Steam action exists only within Library secondary section
- PASS: User-supplied names render literally (no HTML injection)
- PASS: Mobile homepage does not overflow horizontally
- PASS: Mobile menu opens on tap
- PASS: Mobile menu closes with Escape
- PASS: Mobile friends panel opens with tap
- PASS: No mobile scripting errors
- PASS: Small 320px mobile does not overflow horizontally

## Testing method

Executed using Chromium and Playwright with locally injected HTML, CSS, JavaScript and concept art because the test environment restricts browser navigation. Tests verify visible interface states and interactions, not live Steam services. Screenshots are saved alongside this log. Real-device and cross-browser testing still require user verification.
