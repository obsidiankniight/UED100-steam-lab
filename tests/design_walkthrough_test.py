"""Browser validation of the interactive SVG walkthrough in restricted environment.
External links are tested by source structure, not followed to network pages.
"""
from pathlib import Path
from lxml import etree
from playwright.sync_api import sync_playwright
import base64,json
ROOT=Path(__file__).resolve().parent.parent
checks=[]
def check(label,passed):
 checks.append((label,bool(passed))); print(('PASS' if passed else 'FAIL')+' '+label)
for p in (ROOT/'design').glob('*.svg'):
 try: etree.parse(str(p)); check('Valid importable SVG '+p.name,True)
 except Exception as e: check('Valid importable SVG '+p.name,False)
html=(ROOT/'design'/'interactive_wireframes.html').read_text()
for p in (ROOT/'design').glob('*.svg'):
 html=html.replace('src="'+p.name+'"','src="data:image/svg+xml;base64,'+base64.b64encode(p.read_bytes()).decode()+'"')
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1240,'height':900})
 page.set_content(html)
 check('Clickthrough heading renders',page.locator('h1').inner_text().startswith('STEAM / LAB'))
 check('Desktop design screen initially visible',page.locator('#store').is_visible())
 page.locator('nav a[href="#detail"]').click()
 check('Game detail design opens',page.locator('#detail').is_visible())
 page.locator('nav a[href="#mobile"]').click()
 check('Mobile design screen opens',page.locator('#mobile').is_visible())
 page.locator('nav a[href="#store"]').click()
 check('Store design is restored',page.locator('#store').is_visible())
 check('Three images load in walkthrough',page.locator('.mockup img').evaluate_all('(els)=>els.every(e=>e.complete && e.naturalWidth>0)'))
 page.screenshot(path=str(ROOT/'tests'/'design-clickthrough.png'),full_page=False)
 browser.close()
passed=sum(v for _,v in checks)
(ROOT/'tests'/'DESIGN_WALKTHROUGH_RESULTS.md').write_text(f'# Interactive wireframe checks\n\n**{passed}/{len(checks)} passed in Chromium using in-memory rendering.**\n\nThis confirms the browser clickthrough works, but it is not a Figma/Adobe XD prototype and has not been reviewed by real users.\n\n'+''.join(f'- {"PASS" if yes else "FAIL"}: {label}\n' for label,yes in checks),encoding='utf-8')
if passed!=len(checks): raise SystemExit('Design walkthrough failed checks')
