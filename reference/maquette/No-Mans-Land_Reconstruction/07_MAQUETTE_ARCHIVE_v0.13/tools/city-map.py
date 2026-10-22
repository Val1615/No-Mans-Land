from pathlib import Path
import html
out=Path(__file__).resolve().parents[1]/'dist/assets'
base='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 900"><defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#668da3" stroke-opacity=".1"/></pattern><pattern id="hazard" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><path d="M0 0V12" stroke="#d7876e" stroke-opacity=".18" stroke-width="4"/></pattern><radialGradient id="glow"><stop stop-color="#1c4054"/><stop offset="1" stop-color="#0b1723"/></radialGradient></defs><rect width="1100" height="900" fill="#08111b"/><rect x="20" y="20" width="1060" height="860" rx="12" fill="url(#glow)" stroke="#4b7488"/><rect x="20" y="20" width="1060" height="860" fill="url(#grid)"/><g fill="#7697a8" font-family="monospace" font-size="11" letter-spacing="2"><text x="46" y="57">IO / SERVICE DE CARTOGRAPHIE</text><text x="1040" y="57" text-anchor="end">2175</text><text x="46" y="851">SCHÉMA DE DESSERTE · POSITIONS INDICATIVES</text></g>'''
ends='</svg>'
levels={}
levels['perimeter']='''<path d="M80 335L148 350 230 270 208 170 282 101 331 65 400 159 480 125 520 192 574 191 643 108 709 167 770 145 840 179 832 247 908 280 912 373 1034 403 1050 464 980 486 920 556 924 660 835 685 783 755 705 731 668 827 577 779 518 831 455 784 426 700 356 669 363 600 288 632 243 685 172 691 134 657 139 577 184 544 149 484 92 478 46 410Z" fill="#23383e" stroke="#93a7a6" stroke-width="3"/>
<g fill="#683d3b" fill-opacity=".64" stroke="#a66d5b"><path d="M70 400L228 278 209 170 330 65 400 159 480 125 545 205 570 270 480 288 428 351 300 373 197 433 149 484 92 478Z"/><path d="M830 247L907 280 912 373 1034 403 1050 464 980 486 920 556 864 522 784 549 716 502 719 420Z"/><path d="M172 691L243 685 288 632 363 600 426 700 455 784 518 831 577 779 668 827 705 731 783 755 817 704 789 657 721 638 652 666 577 636 512 650 448 586 377 548 271 564 205 594Z"/></g>
<g stroke="#c2b481" stroke-width="9" opacity=".35" fill="none"><path d="M160 490Q280 430 450 430T770 155"/><path d="M550 440Q730 410 900 680"/><path d="M360 245Q415 355 550 440T530 750"/></g><path d="M815 130Q740 319 600 344T435 457 404 600 285 726" fill="none" stroke="#5c93ac" stroke-width="9" opacity=".5"/>
<circle cx="550" cy="445" r="145" fill="#0b1d2b" stroke="#9bb8c5" stroke-width="4"/><circle cx="550" cy="445" r="130" fill="none" stroke="#66bdcf" stroke-dasharray="4 8"/><ellipse cx="550" cy="445" rx="145" ry="48" fill="none" stroke="#476d83"/><ellipse cx="550" cy="445" rx="70" ry="145" fill="none" stroke="#476d83"/><text x="550" y="454" text-anchor="middle" fill="#c2e0e4" font-family="monospace" font-size="22" letter-spacing="3">SARCOPHAGE</text><text x="550" y="482" text-anchor="middle" fill="#74a2b7" font-family="monospace" font-size="12">PLAN DES NIVEAUX INTÉRIEURS</text>'''
levels['under']='''<rect x="110" y="115" width="880" height="655" rx="120" fill="#252c28" stroke="#6a7966" stroke-width="3"/><g stroke="#72806b" stroke-width="34" fill="none"><path d="M180 300H880V620H270V450H550V200M550 450H910"/></g><g stroke="#394b3c" stroke-width="19" fill="none"><path d="M180 300H880V620H270V450H550V200M550 450H910"/></g><g fill="#675f47" stroke="#91856a"><path d="M220 365h90v60h-90ZM330 330h65v90h-65ZM390 510h100v75H390ZM600 345h75v68h-75ZM690 510h83v70h-83ZM745 340h75v72h-75Z"/></g><g fill="#161e1b" stroke="#4d6050"><rect x="360" y="180" width="85" height="65"/><rect x="625" y="170" width="85" height="65"/><rect x="370" y="665" width="85" height="65"/><rect x="625" y="665" width="85" height="65"/></g><text x="550" y="104" text-anchor="middle" fill="#b2ba9f" font-family="monospace" font-size="18" letter-spacing="4">SOUS-VILLE · FONDATIONS ET CONDUITES</text><text x="550" y="805" text-anchor="middle" fill="#8b9d80" font-family="monospace" font-size="12">ACCÈS DE SERVICE / HABITAT INFORMEL</text>'''
for tier in ['lower','center','upper']:
 s='<rect x="110" y="115" width="880" height="655" rx="180" fill="#102635" stroke="#608fa3" stroke-width="3"/>'
 if tier!='upper':
  for row in range(6):
   for col in range(8):
    x=155+col*100;y=155+row*94
    if col in [3,4] or row==3:continue
    s+=f'<rect x="{x}" y="{y}" width="74" height="65" rx="{5 if tier=="lower" else 13}" fill="{"#284454" if tier=="lower" else "#345b70"}" stroke="#567b8a"/><path d="M{x+8} {y+12}H{x+65}M{x+8} {y+21}H{x+65}" stroke="#7aa3ad" stroke-opacity=".3"/>'
  s+='<g fill="none" stroke="#599cae" stroke-width="12" opacity=".35"><path d="M135 465H965M550 130V755M220 155L855 730"/></g><g fill="none" stroke="#70cbdb" stroke-width="3" stroke-dasharray="8 9"><path d="M260 300L520 430 760 300 790 680 260 660 260 300"/></g>'
  if tier=='lower':s+='<path d="M190 240Q245 180 325 220L360 305 300 370 210 345Z" fill="#39584b" stroke="#82906d" stroke-width="5"/><text x="270" y="390" text-anchor="middle" fill="#91a584" font-family="monospace" font-size="12">CHINA LAKE / EAU POLLUÉE</text>'
  if tier=='center':s+='<rect x="450" y="357" width="185" height="170" rx="50" fill="#284f52" stroke="#81b6a2"/><circle cx="542" cy="442" r="38" fill="#426f73" stroke="#a2d3d1"/>'
 else:
  s+='<ellipse cx="550" cy="445" rx="365" ry="240" fill="#274b43" stroke="#789a78" stroke-width="4"/>'
  for x,y in [(280,300),(350,500),(680,580),(810,400),(520,650),(470,250)]:s+=f'<circle cx="{x}" cy="{y}" r="52" fill="#3c6351"/><circle cx="{x}" cy="{y}" r="33" fill="#527963"/>'
  s+='<path d="M235 620Q340 410 690 310T870 480M340 700Q500 490 740 650" stroke="#b5b599" fill="none" stroke-width="22"/><ellipse cx="550" cy="460" rx="100" ry="75" fill="#437c8d" stroke="#c4c3a3" stroke-width="12"/><circle cx="690" cy="310" r="69" fill="#dddac4" stroke="#c1ae75" stroke-width="8"/><circle cx="690" cy="310" r="43" fill="#436779" stroke="#d7c995" stroke-width="4"/>'
 s+='<path d="M109 798H991" stroke="#4b7187" stroke-width="2"/>'
 s+=f'<text x="550" y="104" text-anchor="middle" fill="#acd3df" font-family="monospace" font-size="18" letter-spacing="5">{tier.upper()}-TOWN</text>' if tier!='upper' else '<text x="550" y="104" text-anchor="middle" fill="#d6d3b5" font-family="monospace" font-size="18" letter-spacing="5">UPPER-TOWN · CIEL ARTIFICIEL</text>'
 levels[tier]=s
for name,body in levels.items():
 (out/f'steel-{name}.svg').write_text(base+body+ends)
print('5 fonds de carte vectoriels créés.')
# A standalone labeled atlas is exported from the same district coordinates as the UI.
import json,subprocess,re
root=Path(__file__).resolve().parents[1]
nodes=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import {CITY_LOCATIONS} from './dist/city-data.js'; console.log(JSON.stringify(CITY_LOCATIONS.map(({name,cx,cy,cityLevel})=>({name,cx,cy,cityLevel}))));"],cwd=root))
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="2200" height="2820" viewBox="0 0 2200 2820"><rect width="2200" height="2820" fill="#08111b"/><text x="1100" y="53" text-anchor="middle" fill="#d3e6e8" font-family="monospace" font-size="30" letter-spacing="6">STEEL-MEGALOPOLIS</text><text x="1100" y="84" text-anchor="middle" fill="#93b6c5" font-family="monospace" font-size="14">PÉRIMÈTRE ET PROJECTIONS DES NIVEAUX HABITÉS · 2175</text>']
for i,tier in enumerate(['perimeter','under','lower','center','upper']):
 x=(i%2)*1100;y=110+(i//2)*900
 panel=base+levels[tier]
 panel=re.sub(r'id="([^"]+)"',lambda m:f'id="{tier}-{m[1]}"',panel)
 panel=re.sub(r'url\(#([^)]+)\)',lambda m:f'url(#{tier}-{m[1]})',panel)
 panel=panel.replace('viewBox="0 0 1100 900"',f'x="{x}" y="{y}" width="1100" height="900" viewBox="0 0 1100 900"')
 for n in [n for n in nodes if n['cityLevel']==tier]:
  label=html.escape(n['name']);w=min(240,len(n['name'])*7.2+20)
  panel+=f'<g><circle cx="{n["cx"]}" cy="{n["cy"]}" r="9" fill="#a7d9e3" stroke="#0c1d28" stroke-width="3"/><rect x="{n["cx"]-w/2}" y="{n["cy"]+17}" width="{w}" height="27" rx="3" fill="#0b1d2b" stroke="#6b8c9f"/><text x="{n["cx"]}" y="{n["cy"]+35}" text-anchor="middle" font-family="monospace" font-size="13" fill="#daebe8">{label}</text></g>'
 parts.append(panel+'</svg>')
parts.append('</svg>');(out/'steel-atlas.svg').write_text(''.join(parts))
print('Atlas autonome 5 planches étiquetées exporté.')
