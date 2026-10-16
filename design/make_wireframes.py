"""Original editable SVG wireframes; import SVGs into Figma/Adobe XD."""
from pathlib import Path
P=Path(__file__).parent
C={'bg':'#0d1721','panel':'#192936','panel2':'#263a48','line':'#587183','txt':'#e6f1f7','soft':'#96b2bf','lime':'#b6e983','art':'#126174'}
def rect(x,y,w,h,r=8,fill=None,stroke=None):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill or C["panel"]}" {f"stroke={chr(34)+stroke+chr(34)} stroke-width={chr(34)+str(1)+chr(34)}" if stroke else ""}/>'
def text(x,y,t,s=16,bold=False,color=None):return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{s}" font-weight="{700 if bold else 400}" fill="{color or C["txt"]}">{t}</text>'
def header(w):return rect(0,0,w,72,0,'#111e29')+text(25,44,'STEAM / LAB',21,True)+text(250,43,'Store       Explore       Library',15)
def frame(w,h,body):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{C["bg"]}"/>{body}</svg>'
def save(name,content): (P/name).write_text(content,encoding='utf-8')
# Desktop homepage
w,h=1440,1040
s=header(w)+rect(0,72,210,968,0,'#101d29')+text(24,128,'DISCOVER',12,True,C['soft'])
for i,t in enumerate(['Store home','Browse games','Wishlist','Library','Your cart']):s+=rect(15,150+i*55,177,42,8,'#1a2a37' if i==0 else '#12212e')+text(35,178+i*55,t,15)
s+=rect(1025,16,245,40,9,'#20313d')+text(1042,42,'Search games...',14)
s+=rect(250,105,1145,335,16,'#153144',C['line'])+text(288,145,'HERO / FEATURED GAME',13,True,C['lime'])+text(288,230,'PLAY BEYOND',47,True)+text(288,286,'THE ORDINARY.',47,True)+text(290,333,'Large visual feature + clear primary action',17)
s+=rect(287,355,202,50,10,C['lime'])+text(304,387,'View featured game',15,True,C['bg'])+rect(795,125,560,278,12,'#24586b')+text(930,278,'ORIGINAL ARTWORK',27,True)
s+=text(250,489,'Browse by genre',25,True)
for i,t in enumerate(['Action','Adventure','RPG','Strategy','Racing','Puzzle']):s+=rect(250+i*173,510,158,47,20,'#253846')+text(280+i*173,540,t,14)
s+=text(250,619,'Curated for you',27,True)+text(250,646,'Recommendations can be collapsed or hidden',14,color=C['soft'])
for i in range(4):
 x=250+i*288
 s+=rect(x,673,270,254,12,'#172634',C['line'])+rect(x+9,683,252,154,8,'#22576a')+text(x+26,771,'GAME COVER',18,True)+text(x+16,862,['Game A','Game B','Game C','Game D'][i],18,True)+text(x+16,900,'Price   ♡   Cart',14,color=C['soft'])
s+=rect(1170,981,235,43,10,'#274451')+text(1189,1008,'Friends & Chat   ↑',14,True)
save('desktop_home_wireframe.svg',frame(w,h,s))
# Mobile homepage
w,h=390,890
s=rect(0,0,390,60,0,'#101e2a')+text(14,38,'☰',24,True)+text(47,37,'STEAM / LAB',15,True)+text(306,36,'♡  Cart',14)
s+=rect(13,80,364,323,18,'#173e50')+text(32,110,'FEATURED GAME',12,True,C['lime'])+text(31,183,'PLAY BEYOND',35,True)+text(31,222,'THE ORDINARY',35,True)+text(32,263,'Art + headline + 1 primary action',13)
s+=rect(29,310,205,50,9,C['lime'])+text(51,341,'Explore featured',15,True,C['bg'])
s+=text(15,450,'Browse by genre',23,True)
for i,t in enumerate(['Action','Adventure','RPG','Strategy']):s+=rect(13+(i%2)*187,472+(i//2)*57,176,45,20,'#223848')+text(35+(i%2)*187,500+(i//2)*57,t,14)
s+=text(15,621,'Curated for you',24,True)+text(15,643,'Collapse / personalise this shelf',12,color=C['soft'])
for i in range(2):
 x=13+i*187
 s+=rect(x,663,176,190,11,'#1c2e3b')+rect(x+8,671,160,101,7,'#226073')+text(x+33,730,'ARTWORK',15,True)+text(x+12,799,f'Game {i+1}',15,True)+text(x+12,831,'Price   ♡',12,color=C['soft'])
save('mobile_home_wireframe.svg',frame(w,h,s))
# Desktop detail page
w,h=1440,930
s=header(w)+rect(0,72,210,858,0,'#101d29')+text(35,135,'DISCOVERY')+text(250,128,'← Back to discovery',17,color=C['lime'])
s+=rect(250,164,730,470,15,'#254d60')+text(460,405,'ORIGINAL GAME ARTWORK',27,True)
s+=rect(1005,164,370,470,15,'#1a2b39')+text(1028,220,'GAME TITLE',34,True)+text(1028,277,'Description, genres, ratings',15)+text(1028,326,'Price AUD',25,True)
s+=rect(1028,355,210,51,10,C['lime'])+text(1061,387,'Add to cart',16,True,C['bg'])+rect(1028,415,210,51,10,'#29485a')+text(1061,448,'Add to wishlist',15,True)
s+=text(250,690,'Concept media gallery',24,True)
for i in range(3):s+=rect(250+i*381,714,360,170,11,'#254b5e')+text(330+i*381,802,'MEDIA PREVIEW',21,True)
save('desktop_game_wireframe.svg',frame(w,h,s))
print('3 SVG wireframes created for Figma import')
