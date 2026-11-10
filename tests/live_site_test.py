"""Optional live local HTTP smoke tests for the student's computer.
Run from project root: python tests/live_site_test.py
Requires Playwright, a working Chromium installation, and permission to navigate to
127.0.0.1. The restricted evaluation environment may block browser URL navigation, even
loopback, so this script was NOT successfully executed here. Results are not claimed.
This test is NOT a substitute for real-user testing.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from functools import partial
from playwright.sync_api import sync_playwright
import json, datetime, traceback, shutil

ROOT=Path(__file__).resolve().parent.parent
checks=[]
def check(name,value):
    checks.append({'check':name,'passed':bool(value)})
    print(('PASS' if value else 'FAIL')+' '+name)
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
port=server.server_address[1]
Thread(target=server.serve_forever, daemon=True).start()
base=f'http://127.0.0.1:{port}/'
console_errors=[]
request_failures=[]
try:
 with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,**({'executable_path':shutil.which('chromium')} if shutil.which('chromium') else {}))
    desktop=browser.new_context(viewport={'width':1366,'height':900})
    page=desktop.new_page()
    page.on('pageerror',lambda err:console_errors.append(str(err)))
    page.on('response',lambda r:request_failures.append(f'{r.status} {r.url}') if r.status>=400 and 'favicon' not in r.url else None)
    page.goto(base+'index.html',wait_until='load')
    check('Home loads over real HTTP', page.get_by_role('heading',name='PLAY BEYOND THE ORDINARY.').count()==1)
    check('Home has three product shelves',page.locator('.shelf').count()==3)
    check('Original covers load over HTTP',page.locator('img').evaluate_all('(els)=>els.every(e=>e.complete && e.naturalWidth > 0)'))
    check('Desktop header search is visible',page.locator('#global-search').is_visible())
    check('Mobile search shortcut hidden on desktop',not page.locator('.mobile-search-link').is_visible())
    page.locator('button[data-action="wishlist"]').first.click()
    check('Wishlist count changes on home',page.locator('.wishlist-count').first.inner_text()=='1')
    page.get_by_role('link',name='Wishlist, 1 games').click()
    check('Wishlist persists between real pages',page.url.endswith('wishlist.html') and page.locator('.list-item').count()==1)
    page.goto(base+'browse.html')
    page.locator('#browse-query').fill('Neon')
    check('Browse live search filters actual data',page.locator('.game-card').count()==1)
    page.goto(base+'game.html?id=neon-drift')
    check('Game details open from URL',page.locator('.detail-hero').count()==1)
    page.goto(base+'library.html')
    check('Non-Steam action is Library-only',page.get_by_role('button',name='Add a non-Steam game').count()==1)
    page.get_by_role('button',name='Add a non-Steam game').click()
    page.locator('#nonsteam-title').fill('<img src=x onerror=alert(1)>')
    page.locator('#nonsteam-form button[type="submit"]').click()
    check('Entered Library name displayed safely as literal text',page.locator('.nonsteam-entry img').count()==0 and '<img src=x' in page.locator('.nonsteam-entry').first.inner_text())
    page.goto(base+'design/interactive_wireframes.html')
    check('Clickable design walkthrough loads',page.get_by_role('heading',name='STEAM / LAB — design walkthrough').count()==1)
    page.locator('a[href="#detail"].hotspot').first.click(force=True)
    check('Wireframe hotspot navigates to detail design',page.url.endswith('#detail'))
    page.locator('a[href="#store"].hotspot').click(force=True)
    check('Wireframe back link returns to Store design',page.url.endswith('#store'))
    page.screenshot(path=str(ROOT/'tests'/'live-wireframe.png'),full_page=False)
    page.goto(base+'index.html')
    page.screenshot(path=str(ROOT/'tests'/'live-desktop.png'),full_page=False)
    check('Desktop has no failed local HTTP requests',not request_failures)
    check('Desktop has no unhandled JS errors',not console_errors)
    desktop.close()
    for width in [390,320,768]:
      mobile=browser.new_context(viewport={'width':width,'height':844},is_mobile=width<600,has_touch=width<600)
      mp=mobile.new_page()
      mp.on('pageerror',lambda err:console_errors.append(str(err)))
      mp.goto(base+'index.html',wait_until='load')
      sizes=mp.evaluate('({w:window.innerWidth,scroll:document.documentElement.scrollWidth})')
      check(f'No horizontal overflow at {width}px',sizes['scroll']<=sizes['w']+2)
      if width<=390:
        check(f'Mobile search shortcut is visible at {width}px',mp.locator('.mobile-search-link').is_visible())
        mp.locator('.mobile-search-link').click()
        check(f'Mobile search shortcut opens Browse at {width}px',mp.url.endswith('browse.html'))
        mp.goto(base+'index.html')
        mp.locator('#menu-toggle').click()
        check(f'Mobile menu opens at {width}px',mp.locator('#menu-toggle').get_attribute('aria-expanded')=='true')
        mp.keyboard.press('Escape')
        check(f'Mobile menu closes by Escape at {width}px',mp.locator('#menu-toggle').get_attribute('aria-expanded')=='false')
      if width==390: mp.screenshot(path=str(ROOT/'tests'/'live-mobile.png'),full_page=True)
      mobile.close()
    check('All live-site pages have no JS errors',not console_errors)
    browser.close()
finally:
 server.shutdown()

results={'run_date':datetime.date.today().isoformat(),'browser':'Chromium system binary on Linux','method':'local HTTP server with live navigation, no mocks','checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'console_errors':console_errors,'http_errors':request_failures}
(ROOT/'tests'/'LIVE_SITE_RESULTS.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
(ROOT/'tests'/'LIVE_SITE_RESULTS.md').write_text('# Real HTTP browser verification\n\n**'+str(results['passed'])+'/'+str(results['total'])+' tests passed in Linux Chromium.**\n\nTests used a local HTTP server and real page loads, not an injected DOM. They do not replace cross-browser tests on Safari/Firefox/Edge or real user feedback.\n\n'+''.join('- '+('PASS' if c['passed'] else 'FAIL')+': '+c['check']+'\n' for c in checks)+'\nSee `LIVE_SITE_RESULTS.json` for machine-readable results and `live-*.png` for screenshots.\n',encoding='utf-8')
if results['passed']!=results['total']:
 raise SystemExit(f"{results['passed']}/{results['total']} passed")
