# Assessment 1 → Assessment 2 design traceability

**Assessment 1: Steam Store UX and UI requirements analysis.** Report mark: **91/100 (High Distinction)**. No written marker feedback was provided, so there are no specific marker comments to quote or apply. The following traceability uses the **recommendations actually written in Assessment 1**, not invented feedback.

| Assessment 1 finding or recommendation | Design decision in prototype | Implementation evidence | Test/evidence |
|---|---|---|---|
| Homepage information density may overwhelm new customers | Clear featured action and user-controlled recommendation shelves | `index.html`, `js/app.js`: `gameShelf`, `renderHome`, custom shelf state | Browser checks: personalisation; user task U3 pending |
| Novice users need understandable navigation and discovery | Genre chips, prominent search, Browse filtering; mobile search shortcut | `browse.html`, `js/app.js` and `css/styles.css` | Browser search/filter checks; mobile user task U1 pending |
| Returning customers value recommendations and wishlists | Preserve shelves, wishlist controls and local session persistence | `wishlist.html`, `js/app.js`: state collection | Browser count checks; real-user U1 pending |
| Publishers need discovery visibility | Preserve game thumbnails/tags and featured placement; do not remove all carousels | Home game shelves and details cards | Visual inspection, rationale; no real publisher testing claimed |
| Layout must adapt to mobile/tablet/desktop | Grid/Flexbox media queries, mobile navigation, touch controls | `css/styles.css`, mobile shortcut | 320px/390px automated overflow tests; cross-browser pending |
| Accessible semantic HTML and feedback | Landmarks, button labels, focus styles, live feedback, Escape close | HTML templates, CSS and JS | Keyboard/UI checks, further assistive-tech evaluation pending |
| Performance affected by artwork and trailers | Use original small SVG assets and lazy-loaded card images | `assets/covers/*.svg`, `js/app.js` | Local asset audit; no Core Web Vitals benchmark claimed |
| Secure interaction requires clear controls | Demo-only checkout, local input length checks, text-only user input | JS, library demo dialog | Automated literal-text injection test; not a production security audit |
| Avoid giving low-priority non-Steam actions prominence in shopping | Place the secondary control **only** at bottom of Library | `library.html`, Library renderer | Automated check; user task U5 pending |

**Technical limitations:** This is a client-side demo, not a real marketplace. There is no external authentication or server-side validation. In a production system, transaction data and user input would require server-side controls and HTTPS.
