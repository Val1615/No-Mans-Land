from pathlib import Path
import random,html
random.seed(2175)
import json,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
points=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import {CONTINENT} from './dist/world.js';console.log(JSON.stringify(CONTINENT));"],cwd=root))
continent='M'+' L'.join(' '.join(map(str,p)) for p in points)+' Z'
s=['''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="1000" viewBox="0 0 1100 1000"><defs><pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse"><path d="M50 0H0V50" fill="none" stroke="#789276" stroke-opacity=".12" stroke-width=".7"/></pattern><pattern id="grain" width="7" height="9" patternUnits="userSpaceOnUse"><circle cx="1" cy="2" r=".7" fill="#d3c497" opacity=".07"/></pattern><pattern id="hatch" width="9" height="9" patternUnits="userSpaceOnUse"><path d="m0 9 9-9" stroke="#ac745b" stroke-width="2" opacity=".25"/></pattern><radialGradient id="earth"><stop stop-color="#596247"/><stop offset="1" stop-color="#344e3d"/></radialGradient><radialGradient id="blast"><stop stop-color="#8a7150"/><stop offset=".65" stop-color="#8d795245"/><stop offset="1" stop-color="#786d4d00"/></radialGradient><clipPath id="land"><path d="'''+continent+'''"/></clipPath></defs><rect width="1100" height="1000" fill="#172e2b"/><rect width="1100" height="1000" fill="url(#grid)"/><path d="'''+continent+'''" fill="url(#earth)" stroke="#94a27a" stroke-opacity=".45" stroke-width="2"/><g clip-path="url(#land)">''']
s.append('<path d="M50 50H1100V400Q600 500 180 340Z" fill="#b39c5a" opacity=".15"/><path d="M440 600Q630 500 840 520L940 950 600 800Z" fill="#8ea070" opacity=".10"/>')
for i in range(1500):
 x=random.randint(80,1000);y=random.randint(45,965)
 s.append(f'<path d="m{x} {y} 2 -1 3 1" fill="none" stroke="#{random.choice(["8b9b71","a2aa7a","18382d"])}" stroke-width=".6" opacity=".30"/>')
s.append('<g fill="none" stroke="#819a8d" stroke-width="2" opacity=".42"><path d="M180 160Q400 80 510 210T720 390Q620 520 740 610T780 790Q700 870 880 915"/><path d="M280 260Q390 320 600 290T880 200"/><path d="M350 390Q570 340 740 442"/><path d="M500 575Q680 510 785 520"/></g>')
for i in range(65):
 t=i/64;x=240+t*615+random.randint(-12,10);y=280+t*650;w=random.randint(10,21);h=random.randint(16,30)
 s.append(f'<path d="M{x-w} {y+8} {x} {y-h} {x+w} {y+8}Z" fill="#9da88a" fill-opacity=".35" stroke="#bbc3a2" stroke-opacity=".18"/><path d="m{x-6} {y-h+12} 6 -12 6 12-6-4Z" fill="#cad1b1" fill-opacity=".35"/>')
s.append('<circle cx="464" cy="108" r="85" fill="url(#blast)"/><circle cx="464" cy="108" r="56" fill="url(#hatch)" stroke="#ab8660" stroke-dasharray="4 4" opacity=".6"/><circle cx="464" cy="108" r="25" fill="#3b4231" stroke="#a18454"/><path d="M520 240 561 210 646 223 704 260 705 319 668 357 583 357 524 315Z" fill="#74928c" opacity=".16" stroke="#8aaba2" stroke-dasharray="3 3"/><circle cx="622" cy="290" r="24" fill="#1a3832" stroke="#86b1a8" stroke-width="2"/><circle cx="622" cy="290" r="32" fill="none" stroke="#93b2a2" stroke-opacity=".28"/><path d="M682 144 743 129 790 169 774 208 717 222 674 196Z" fill="url(#hatch)" stroke="#97a47b" stroke-opacity=".35"/>')
s.append('<g fill="none" stroke="#c0b583" stroke-width="1.5" stroke-opacity=".44" stroke-dasharray="4 5"><path d="M234 143 367 180 499 268 622 290 879 271"/><path d="M367 180 464 108 715 184 622 290 740 442 762 749"/><path d="M499 268 478 426 302 432M478 426 568 621 762 749 907 924"/><path d="M580 238 622 290 602 333 478 426"/></g>')
s.append('</g><path d="'+continent+'" fill="url(#grain)"/>')
labels=[(337,75,'LAWLESS AREA',14,-7),(555,157,'LES TERRES GRISES',12,0),(890,345,'BAZARS DE L’EST',11,-23),(385,440,'CORDILLÈRE',13,50),(615,565,'TERRITOIRES UFSA',15,0),(809,738,'WASTE COAST',12,65),(165,651,'OCÉAN PACIFIQUE',13,-63),(978,527,'ATLANTIQUE SUD',13,90)]
for x,y,t,size,rot in labels:s.append(f'<text x="{x}" y="{y}" fill="#c1c5a0" fill-opacity=".40" font-family="monospace" font-size="{size}" letter-spacing="3" transform="rotate({rot} {x} {y})">{html.escape(t)}</text>')
s.append('<g fill="#b7bf99" font-family="monospace" font-size="9" opacity=".6"><text x="23" y="27">ATLAS DES TERRES / SECTEUR SUD</text><text x="23" y="976">RELEVÉS PARTIELS · 2175</text><text x="830" y="968">SIÈGE UFSA →</text></g><g transform="translate(1000 845)" stroke="#aab999" fill="none" opacity=".7"><path d="M0-28V28M-22 0H22M0-28l-5 13 5-3 5 3Z"/><text y="-38" x="-4" font-family="monospace" font-size="11" fill="#aab999" stroke="none">N</text><circle r="17" stroke-opacity=".4"/></g><rect x="12" y="12" width="1076" height="976" fill="none" stroke="#7f9774" stroke-opacity=".30"/><path d="M12 42V12h30M1058 12h30v30M12 958v30h30M1058 988h30v-30" stroke="#b1b68c" fill="none" stroke-width="2"/></svg>')
svg=''.join(s)
(root/'dist/assets/world-map.svg').write_text(svg)
nodes=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import {WORLD_LOCATIONS} from './dist/city-data.js';console.log(JSON.stringify(WORLD_LOCATIONS));"],cwd=root))
labels=''
for n in nodes:
 x,y=n['x'],n['y'];label=html.escape(n['name'])
 labels+=f'<g><circle cx="{x}" cy="{y}" r="5" fill="#e2d49f" stroke="#132c22"/><text x="{x+9}" y="{y-8}" font-family="monospace" font-size="12" fill="#e1dec2" stroke="#172e2b" stroke-width="3" paint-order="stroke">{label}</text></g>'
(root/'dist/assets/world-map-labeled.svg').write_text(svg.replace('</svg>',labels+'</svg>'))
