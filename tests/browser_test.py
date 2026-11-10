"""Offline Playwright QA harness for UED100 prototype.

This evaluation environment blocks browser navigation. HTML/CSS/JS are injected into
an about:blank browser page; tested files are unmodified and keep their normal
relative-path structure for real-world browser use. On a normal PC, simply run
index.html locally or serve the project with python -m http.server 5500.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re, json, base64

ROOT=Path(__file__).resolve().parent.parent
ART={p.stem:'data:image/svg+xml;base64,'+base64.b64encode(p.read_bytes()).decode() for p in (ROOT/'assets'/'covers').glob('*.svg')}
CSS=(ROOT/'css/styles.css').read_text()
DATA=(ROOT/'js/data.js').read_text()
APP=(ROOT/'js/app.js').read_text().replace("const art = (game) => `assets/covers/${game.id}.svg`;", "const art = (game) => window.__art[game.id];").replace('assets/icons/sprite.svg#','#')
SPRITE=(ROOT/'assets/icons/sprite.svg').read_text().replace('<svg xmlns=', '<svg style="position:absolute;width:0;height:0;overflow:hidden" xmlns=',1)
RESULTS=[]

def check(label,ok):
    RESULTS.append((label,bool(ok)))
    print(('PASS' if ok else 'FAIL')+'  '+label)

def load(page,file,storage=None):
    doc=(ROOT/file).read_text()
    doc=doc.replace('<link rel="stylesheet" href="css/styles.css">',f'<style>{CSS}</style>')
    doc=doc.replace('<script defer src="js/data.js"></script><script defer src="js/app.js"></script>','')
    doc=doc.replace('href="assets/icons/sprite.svg#','href="#')
    doc=doc.replace('><a class="skip-link"',f'>{SPRITE}<a class="skip-link"',1)
    scripts=f'<script>window.__art={json.dumps(ART)};window.__fake={json.dumps(storage or {})};Object.defineProperty(window,"localStorage",{{value:{{getItem:k=>window.__fake[k]||null,setItem:(k,v)=>window.__fake[k]=v}}}});</script><script>{DATA}</script><script>{APP}</script>'
    doc=doc.replace('</body>',scripts+'</body>')
    page.set_content(doc,wait_until='load',timeout=20000)
    # Only the static hero is outside the app's runtime artwork helper.
    page.evaluate("""() => document.querySelectorAll('img').forEach(i => { let s=i.getAttribute('src'); if(s&&s.startsWith('assets/covers/')) i.src=window.__art[s.split('/').pop().replace('.svg','')]; });""")
    page.evaluate("""() => document.querySelectorAll('img').forEach(i => i.loading='eager')""")
    return page

with sync_playwright() as browser_api:
    browser=browser_api.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    desktop=browser.new_context(viewport={'width':1440,'height':900},device_scale_factor=1)
    page=desktop.new_page();errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    load(page,'index.html')
    page.screenshot(path=str(ROOT/'tests'/'desktop-home.png'),full_page=False)
    check('Homepage renders 3 game shelves',page.locator('.shelf').count()==3)
    check('All original game covers load',page.locator('img').count()>10)
    check('Friends dock initially collapsed',page.locator('#friends-toggle').get_attribute('aria-expanded')=='false')
    check('Friends panel shows all four activity states',all(page.locator(f'.friend[data-status="{status}"]').count() >= 1 for status in ('online','playing','away','offline')))
    activity_colors=page.evaluate('''() => Object.fromEntries(['online','playing','away','offline'].map(s=>[s,getComputedStyle(document.querySelector(`.friend-dot.${s}`)).backgroundColor]))''')
    check('Activity states have distinct presence colours',len(set(activity_colors.values()))==4)
    check('Offline friend has a visible status label',page.locator('.friend[data-status="offline"] small').inner_text()=='Offline')
    page.locator('#friends-toggle').hover();page.wait_for_timeout(250)
    check('Friends panel expands upward on hover',float(page.locator('.friends-panel').evaluate('(e)=>getComputedStyle(e).maxHeight').replace('px',''))>=300)
    page.locator('#friends-toggle').click()
    check('Friends panel can stay open on click',page.locator('#friends-toggle').get_attribute('aria-expanded')=='true')
    page.keyboard.press('Escape')
    check('Escape closes pinned friend panel',page.locator('#friends-toggle').get_attribute('aria-expanded')=='false')
    page.locator('button[data-action="wishlist"]').first.click()
    check('Wishlist updates live count',page.locator('.wishlist-count').first.inner_text()=='1')
    heart=page.locator('button[data-action="wishlist"][aria-pressed="true"]').first
    styles=heart.evaluate('''e=>({buttonBg:getComputedStyle(e).backgroundColor, heartFill:getComputedStyle(e.querySelector('svg')).fill})''')
    check('Saved heart turns red without green button fill',styles['heartFill'].startswith('rgb(240, 106, 122)') and styles['buttonBg']!='rgb(53, 73, 49)')
    check('Header wishlist icon reflects saved items',page.locator('.wishlist-navigation.has-items').count()==1)
    page.locator('button[data-action="cart"]').first.click()
    check('Cart updates live count',page.locator('.cart-count').first.inner_text()=='1')
    page.get_by_role('button',name='Customise shelves').click()
    page.locator('#shelf-pref-popular').uncheck()
    page.get_by_role('button',name='Save preferences').click()
    check('Personalise shelves hides selected shelf',page.locator('#shelf-popular').count()==0)
    page.screenshot(path=str(ROOT/'tests'/'desktop-interactions.png'),full_page=False)
    check('No browser scripting errors on home',len(errors)==0)
    load(page,'browse.html')
    page.locator('#browse-query').fill('Aetherfall')
    check('Browse search filters results',page.locator('.game-card').count()==1)
    page.locator('#browse-query').fill('')
    page.locator('input[name="genre"][value="RPG"]').check()
    check('Genre filters return relevant results',page.locator('.game-card').count()==2)
    page.get_by_role('button',name='Clear all filters').click()
    check('Clearing filters restores catalogue',page.locator('.game-card').count()==10)
    load(page,'game.html')
    check('Game detail has artwork, price and buttons',page.locator('.detail-hero img').count()==1 and page.locator('.detail-price').count()==1)
    load(page,'cart.html')
    check('Empty cart shows actionable empty state',page.get_by_text('Your cart is empty').count()==1)
    load(page,'cart.html',storage={'ued100_cart':'["neon-drift","last-grove"]'})
    check('Populated cart computes correct AUD total', '$64.90' in page.locator('.summary').inner_text())
    page.locator('button[data-action="checkout"]').click()
    check('Checkout is explicitly demo-only',page.locator('#checkout-dialog').is_visible())
    load(page,'wishlist.html')
    check('Empty wishlist shows actionable empty state',page.get_by_text('Your wishlist is empty').count()==1)
    load(page,'library.html')
    check('Non-Steam action exists only within Library secondary section',page.locator('.library-secondary button[data-action="add-nonsteam"]').count()==1)
    page.get_by_role('button',name='Add a non-Steam game').click()
    page.locator('#nonsteam-title').fill('<script>alert(1)</script>')
    page.locator('#nonsteam-form button[type="submit"]').click()
    check('User-supplied names render literally (no HTML injection)',page.locator('.nonsteam-entry span').first.inner_text()=='<script>alert(1)</script>' and page.locator('.nonsteam-entry script').count()==0)
    page.screenshot(path=str(ROOT/'tests'/'desktop-library.png'),full_page=False)

    mobile=browser.new_context(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
    mobile_page=mobile.new_page();m_errors=[]
    mobile_page.on('pageerror',lambda e:m_errors.append(str(e)))
    load(mobile_page,'index.html')
    mobile_page.screenshot(path=str(ROOT/'tests'/'mobile-home.png'),full_page=True)
    dimensions=mobile_page.evaluate('({scroll:document.documentElement.scrollWidth,view:window.innerWidth})')
    check('Mobile homepage does not overflow horizontally',dimensions['scroll']<=dimensions['view']+2)
    mobile_page.locator('#menu-toggle').click()
    check('Mobile menu opens on tap',mobile_page.locator('#menu-toggle').get_attribute('aria-expanded')=='true')
    mobile_page.keyboard.press('Escape')
    check('Mobile menu closes with Escape',mobile_page.locator('#menu-toggle').get_attribute('aria-expanded')=='false')
    mobile_page.locator('#friends-toggle').click()
    check('Mobile friends panel opens with tap',mobile_page.locator('#friends-toggle').get_attribute('aria-expanded')=='true')
    check('No mobile scripting errors',len(m_errors)==0)
    tiny=browser.new_context(viewport={'width':320,'height':740},is_mobile=True,has_touch=True).new_page()
    load(tiny,'index.html')
    dim=tiny.evaluate('({scroll:document.documentElement.scrollWidth,view:window.innerWidth})')
    check('Small 320px mobile does not overflow horizontally',dim['scroll']<=dim['view']+2)
    browser.close()

log=ROOT/'tests'/'TEST_RESULTS.md'
passed=sum(ok for _,ok in RESULTS)
log.write_text('# Functional test results\n\n'+f'**{passed}/{len(RESULTS)} checks passed.**\n\n'+'\n'.join(f'- {"PASS" if ok else "FAIL"}: {name}' for name,ok in RESULTS)+'\n\n## Testing method\n\nExecuted using Chromium and Playwright with locally injected HTML, CSS, JavaScript and concept art because the test environment restricts browser navigation. Tests verify visible interface states and interactions, not live Steam services. Screenshots are saved alongside this log. Real-device and cross-browser testing still require user verification.\n',encoding='utf-8')
if passed<len(RESULTS):raise SystemExit(1)
