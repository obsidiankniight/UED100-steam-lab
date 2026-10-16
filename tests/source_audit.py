"""Lightweight static project integrity checks (does not replace browser testing)."""
from pathlib import Path
from html.parser import HTMLParser
import json,re
p=Path(__file__).resolve().parent.parent
pages=['index.html','browse.html','game.html','wishlist.html','cart.html','library.html']
required=['css/styles.css','js/data.js','js/app.js','assets/icons/sprite.svg']
missing=[f for f in pages+required if not (p/f).is_file()]
for f in pages:
 t=(p/f).read_text()
 for tag in ['<html lang="en-AU">','<main class="page-main"','id="friends-toggle"','id="menu-toggle"','href="css/styles.css"']:
  if tag not in t:missing.append(f'{f}: {tag}')
 for href in re.findall(r'(?:src|href)="([^"]+)"',t):
  if href.startswith(('https:','http:','#','mailto:')):continue
  if '?' in href:href=href.split('?',1)[0]
  if href.startswith('docs/') and href=='docs/README.md':pass
  if href and not (p/href).is_file():missing.append(f'{f}: missing linked {href}')
covers=list((p/'assets/covers').glob('*.svg'))
assert len(covers)==10, len(covers)
assert not missing, '\n'.join(missing)
assert len(list((p/'design').glob('*_wireframe.svg')))==3
print('PASS: 6 linked HTML pages, 4 shared essentials, 10 original illustrations, 3 wireframes, no missing local links.')
print('Total asset sizes:',sum(x.stat().st_size for x in covers),'bytes for 10 SVG covers')
