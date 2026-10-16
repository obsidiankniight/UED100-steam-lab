from pathlib import Path
import random, math, html
p=Path(__file__).parent/'assets'/'covers'
p.mkdir(parents=True,exist_ok=True)
GAMES=[
('neon-drift','NEON / DRIFT','#061c33','#10d5f2','#ec52bf','city'),
('last-grove','THE LAST GROVE','#112a2a','#baf28a','#f6cc74','forest'),
('deep-signal','DEEP SIGNAL','#091a3e','#46c5ea','#ff906b','space'),
('aetherfall','AETHERFALL','#1d1737','#aa8dfd','#f5d87e','fantasy'),
('orbit-assembly','ORBIT ASSEMBLY','#082e35','#58e0b4','#fd8a59','space'),
('emberline','EMBERLINE','#3b1921','#ffa45a','#fe5175','mountains'),
('paper-kingdom','PAPER KINGDOM','#354052','#f4dca0','#adc3ea','forest'),
('glaciera','GLACIERA','#12263b','#91dcff','#e3fbff','mountains'),
('nexus-circuit','NEXUS CIRCUIT','#0d2130','#b5f756','#28b6e7','city'),
('echoes-of-arc','ECHOES OF ARC','#2b183d','#ff8dd2','#bc9cfd','fantasy'),
]
for idx,(slug,name,bg,accent,accent2,kind) in enumerate(GAMES):
    rng=random.Random(idx*107+13)
    w,h=1200,750
    stars=''.join(f'<circle cx="{rng.randint(10,w-10)}" cy="{rng.randint(5,470)}" r="{rng.choice([1,1,2,3])}" fill="white" opacity="{rng.uniform(.1,.6):.2f}"/>' for _ in range(65))
    streaks=''.join(f'<path d="M {rng.randint(-200,1100)} {rng.randint(20,600)} l {rng.randint(100,500)} -{rng.randint(30,140)}" stroke="{accent2}" stroke-width="{rng.choice([1,2,3])}" opacity=".11"/>' for _ in range(23))
    if kind=='city':
        skyline=''.join(f'<rect x="{x}" y="{y}" width="{wd}" height="{h-y}" fill="{rng.choice(["#030b18","#071626","#0b2132"])}" opacity=".9"/><path d="M {x+wd//3} {y+35} v 25" stroke="{accent}" stroke-width="3" opacity=".65"/>' for x,wd,y in [(x,rng.randint(35,88),rng.randint(230,490)) for x in range(0,1200,70)])
        scene=f'<ellipse cx="810" cy="235" rx="235" ry="235" fill="url(#glow)"/><circle cx="835" cy="270" r="175" stroke="{accent}" stroke-width="12" fill="none" opacity=".72"/><path d="M 0 610 L 1200 530 1200 750 0 750Z" fill="#040d1b" opacity=".75"/>{skyline}<path d="M 0 675 L 1200 610" stroke="{accent2}" stroke-width="5" opacity=".7"/>'
    elif kind=='forest':
        trees=''.join(f'<path d="M {x} {y} l -{s} {s*1.7} h {s*2}Z" fill="{rng.choice(["#142a31","#1a3e39","#225243"])}" opacity=".98"/>' for x,y,s in [(x,rng.randrange(200,470),rng.randrange(70,190)) for x in range(-100,1300,110)])
        scene=f'<circle cx="770" cy="285" r="205" fill="url(#glow)"/><circle cx="755" cy="255" r="125" fill="{accent2}" opacity=".6"/><path d="M0 480 Q350 350 620 500 T1200 420 V750 H0Z" fill="#163b36"/>{trees}<path d="M0 650 Q650 520 1200 640 V750 H0Z" fill="#071d25"/>'
    elif kind=='mountains':
        scene=f'<circle cx="865" cy="245" r="215" fill="url(#glow)"/><circle cx="860" cy="230" r="108" fill="{accent2}" opacity=".75"/><path d="M-100 660 340 230 610 620 840 310 1300 700Z" fill="#273044" opacity=".92"/><path d="M-70 750 440 300 680 690 980 350 1400 750Z" fill="#121e35"/><path d="M 340 230 l -70 78 70 -30 50 35Z M 840 310 l -55 74 55 -23 50 42Z" fill="{accent}" opacity=".75"/>'
    elif kind=='space':
        scene=f'<circle cx="850" cy="310" r="270" fill="url(#glow)"/><circle cx="850" cy="310" r="165" stroke="{accent}" stroke-width="20" fill="none" opacity=".62"/><circle cx="850" cy="310" r="130" stroke="{accent2}" stroke-width="5" fill="none" opacity=".3"/><ellipse cx="855" cy="300" rx="340" ry="70" transform="rotate(-25 855 300)" stroke="{accent2}" stroke-width="11" fill="none" opacity=".75"/><circle cx="850" cy="310" r="55" fill="#030b17"/>'
    else:
        scene=f'<circle cx="795" cy="260" r="255" fill="url(#glow)"/><path d="M 600 520 Q 560 180 800 90 Q 1040 210 950 525 L 810 610Z" fill="{accent}" opacity=".33"/><path d="M 800 70 L 1100 400 820 670 540 405Z" fill="none" stroke="{accent2}" stroke-width="24" opacity=".56"/><circle cx="800" cy="350" r="126" fill="#0b1b30" opacity=".8"/><path d="M 600 350H1000 M 800 150V560" stroke="{accent2}" stroke-width="9" opacity=".7"/>'
    title=html.escape(name)
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="750" viewBox="0 0 1200 750" role="img" aria-label="Original illustrated artwork for {title}">
<defs><linearGradient id="sky" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="{bg}"/><stop offset="100%" stop-color="#040b17"/></linearGradient><radialGradient id="glow"><stop offset="0%" stop-color="{accent}" stop-opacity=".65"/><stop offset="100%" stop-color="{accent}" stop-opacity="0"/></radialGradient><linearGradient id="shade" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#061321" stop-opacity="0"/><stop offset="100%" stop-color="#020611" stop-opacity=".8"/></linearGradient></defs>
<rect width="1200" height="750" fill="url(#sky)"/>{stars}{streaks}{scene}<rect width="1200" height="750" fill="url(#shade)"/><rect x="38" y="38" width="6" height="50" rx="3" fill="{accent}"/><text x="60" y="70" font-family="Arial,sans-serif" font-size="24" fill="#e5f2fc" letter-spacing="7" opacity=".74">PLAY MORE / DISCOVER MORE</text><text x="60" y="654" font-family="Arial,sans-serif" font-weight="800" font-size="65" fill="white" letter-spacing="2">{title}</text><rect x="61" y="674" width="140" height="5" rx="3" fill="{accent}"/><text x="60" y="715" font-family="Arial,sans-serif" font-size="17" fill="#e9e9fa" letter-spacing="6" opacity=".7">ORIGINAL CONCEPT ART</text></svg>'''
    (p/f'{slug}.svg').write_text(svg,encoding='utf-8')
print('generated',len(GAMES),'unique concept art SVGs')
