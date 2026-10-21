import json, os
from playwright.sync_api import sync_playwright
G = '/workspace/nml/game'; D = os.getcwd(); OUT = '/workspace/nml/docs/systemes/maquettes/'; os.makedirs(OUT, exist_ok=True)
proj = json.load(open('proj.json'))
CSS = f"""
@font-face{{font-family:Plex;src:url(file://{G}/assets/fonts/IBMPlexMono-Regular.ttf)}}
@font-face{{font-family:Plex;font-weight:500;src:url(file://{G}/assets/fonts/IBMPlexMono-Medium.ttf)}}
@font-face{{font-family:VT;src:url(file://{G}/assets/fonts/VT323-Regular.ttf)}}
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--c:#f2b44a;--t:#fde9c2;--d:rgba(242,180,74,.5);--bg:rgba(10,7,4,.72)}}
body{{font-family:Plex;color:var(--t);font-size:13px;overflow:hidden;position:relative}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:center}}
.rp{{position:absolute;background:var(--bg);border:1px solid var(--d);backdrop-filter:blur(2px)}}
.rp::after{{content:'';position:absolute;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,rgba(0,0,0,.12) 0 1px,transparent 1px 3px)}}
.lbl{{font-size:10px;letter-spacing:.09em;color:var(--c);text-transform:uppercase}}
h1{{font-family:VT;font-weight:400;color:var(--c);letter-spacing:.06em}}
h2{{font-family:VT;font-weight:400;font-size:24px;color:var(--c);letter-spacing:.05em}}
.muted{{color:rgba(253,233,194,.62)}}
.btn{{display:inline-block;background:rgba(8,6,3,.8);border:1px solid var(--d);color:#fff2d8;padding:5px 10px;font-size:12.5px}}
.btn u{{color:var(--c);text-decoration:none;margin-right:4px}}
.on{{border-color:var(--c);color:var(--c)}}
.sel{{background:rgba(242,180,74,.14);border-color:var(--c)}}
"""
def page(name, w, h, body, dpr=1):
    open(f'{name}.html', 'w').write(f'<!doctype html><meta charset=utf-8><style>{CSS}</style><body style="width:{w}px;height:{h}px">{body}</body>')
    return name, w, h, dpr

screens = []
# 1. MENU PRINCIPAL
screens.append(page('menu', 1280, 800, f"""
<div class=bg style="background-image:url(file://{D}/menu-fond.jpg)"></div>
<div class=bg style="background:linear-gradient(90deg,rgba(6,4,2,.55),rgba(6,4,2,0) 45%)"></div>
<div class=rp style="left:56px;top:150px;width:360px;padding:26px 26px 22px">
 <h1 style="font-size:52px;line-height:.9">NO MAN'S LAND</h1>
 <div class=lbl style="margin:8px 0 22px">Dusk-Town · 2175</div>
 <div style="display:flex;flex-direction:column;gap:7px;font-size:15px">
  <div class="btn sel" style="font-size:15px;padding:8px 12px"><u>&gt;</u>Continuer<div class=muted style="font-size:11px;margin-top:3px">Auto · Le Scellé · 23:41</div></div>
  <div class=btn style="font-size:15px;padding:8px 12px">Nouveau jeu</div>
  <div class=btn style="font-size:15px;padding:8px 12px">Charger / Sauvegarder</div>
  <div class=btn style="font-size:15px;padding:8px 12px">Options</div>
  <div class=btn style="font-size:15px;padding:8px 12px">Codex</div>
  <div class=btn style="font-size:15px;padding:8px 12px">Crédits</div>
  <div class=btn style="font-size:15px;padding:8px 12px;opacity:.8">Quitter <span class=muted style="font-size:11px">(retour au titre)</span></div>
 </div>
</div>
<div class=rp style="right:16px;bottom:14px;padding:5px 10px;font-size:11px"><span class=lbl>Musique</span> Dusk-Town · <u style="color:var(--c);text-decoration:none">S</u> couper</div>
<div class=rp style="left:56px;bottom:14px;padding:4px 10px;font-size:11px" ><span class=lbl>Maquette</span> v10 · piste, non codée</div>
"""))
# 2. CREATION 1
races = [('Humain', 'Ni implant ni mutation. Refusé à la douane de Steel.', ''), ('Mutant', 'Changé par les radiations. Abattu à vue par le Service.', 'sel'),
         ('Augmenté', 'Implant d\'IO sous la peau. Passe la douane.', ''), ('Cyborg', 'Corps en partie mécanique, implant. Passe la douane.', '')]
ori = [('Né dans les Sables', 'Tu as grandi caché à Dusk-Town, sous un foulard. Sol te connaît depuis toujours.', 'sel'),
       ('Rescapé d\'une rafle', 'Ils t\'ont pris une fois. Tu as sauté du camion avant la capitale.', ''),
       ('Errant des terres brûlées', 'Tu viens de plus loin que la carte. L\'eau, tu la sens.', '')]
screens.append(page('creation-1-identite', 1280, 800, f"""
<div class=bg style="background-image:url(file://{D}/bg-q1-desktop.png);filter:blur(3px) brightness(.55)"></div>
<div class=rp style="left:24px;top:20px;right:24px;padding:8px 14px;display:flex;justify-content:space-between;align-items:center">
 <h2>CRÉATION · 1/2 · IDENTITÉ</h2><span class=muted>Échap : retour au menu</span></div>
<div class=rp style="left:24px;top:76px;width:300px;bottom:76px;padding:16px">
 <div class=lbl>Aperçu</div>
 <div style="margin:10px 0;border:1px solid var(--d);height:300px;background:url(file://{D}/portrait-player.webp) center/cover"></div>
 <div style="display:flex;justify-content:space-between"><span class=btn>&lt;</span><span class=muted>Visage 2/4</span><span class=btn>&gt;</span></div>
 <div class=lbl style="margin-top:18px">Nom</div>
 <div style="border:1px solid var(--c);padding:7px 9px;margin-top:5px;font-size:15px">Rafael Quintero<span style="color:var(--c)">_</span></div>
</div>
<div class=rp style="left:340px;top:76px;width:440px;bottom:76px;padding:16px">
 <div class=lbl>Race</div>
 <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px">
 {''.join(f'<div class="btn {c}" style="padding:10px;height:96px"><div style="font-size:15px;color:{"var(--c)" if c else "#fff2d8"}">{n}</div><div class=muted style="font-size:11.5px;margin-top:6px;white-space:normal">{t}</div></div>' for n,t,c in races)}
 </div>
 <div class=lbl style="margin-top:18px">Effets · Mutant</div>
 <ul style="list-style:none;margin-top:6px;line-height:1.7;font-size:12.5px">
  <li>Endurance +1 · résiste aux radiations</li><li>Pas d'implant : inconnu d'IO</li><li>Service Militarisé : tire à vue</li><li>À Dusk-Town, certains te parlent plus volontiers</li></ul>
</div>
<div class=rp style="left:796px;top:76px;right:24px;bottom:76px;padding:16px">
 <div class=lbl>Origine · Mutant</div>
 <div style="display:flex;flex-direction:column;gap:8px;margin-top:8px">
 {''.join(f'<div class="btn {c}" style="padding:10px;white-space:normal"><div style="font-size:14px;color:{"var(--c)" if c else "#fff2d8"}">{n}</div><div class=muted style="font-size:11.5px;margin-top:5px">{t}</div></div>' for n,t,c in ori)}
 </div>
 <div class=lbl style="margin-top:16px">Apporte</div>
 <div style="font-size:12.5px;line-height:1.7;margin-top:4px">Perception +1 · Discrétion favorite<br>Foulard de sable · 25 $</div>
</div>
<div class=rp style="left:24px;right:24px;bottom:20px;padding:8px 14px;display:flex;justify-content:space-between;align-items:center">
 <span class=btn>Profil prêt</span><span class=muted>Race et origine ne changent plus en cours de partie.</span><span class="btn on">Suivant &gt;</span></div>
"""))
# 3. CREATION 2
attrs = [('Force', 6, 'dégâts de mêlée, effraction'), ('Perception', 7, 'précision'), ('Endurance', 7, 'santé'), ('Charisme', 3, 'négociation'),
         ('Intelligence', 5, 'technologie, points de compétence'), ('Agilité', 6, 'PA et discrétion'), ('Volonté', 4, 'peur, douleur, intimidation')]
skills = [('Armes à feu', 32, 0), ('Corps à corps', 28, 0), ('Discrétion', 47, 1), ('Crochetage', 18, 0), ('Parole', 14, 0), ('Troc', 12, 0),
          ('Médecine', 20, 0), ('Mécanique', 22, 1), ('Survie', 41, 1), ('Électronique', 9, 0), ('Observation', 36, 0)]
def bar(v, m=10): return ''.join(f'<span style="display:inline-block;width:14px;height:10px;margin-right:2px;background:{"var(--c)" if i < v else "rgba(242,180,74,.15)"}"></span>' for i in range(m))
screens.append(page('creation-2-attributs', 1280, 800, f"""
<div class=bg style="background-image:url(file://{D}/bg-q1-desktop.png);filter:blur(3px) brightness(.55)"></div>
<div class=rp style="left:24px;top:20px;right:24px;padding:8px 14px;display:flex;justify-content:space-between;align-items:center">
 <h2>CRÉATION · 2/2 · ATTRIBUTS ET COMPÉTENCES</h2><span>Rafael Quintero · Mutant · Né dans les Sables</span></div>
<div class=rp style="left:24px;top:76px;width:470px;bottom:76px;padding:16px">
 <div style="display:flex;justify-content:space-between"><span class=lbl>Attributs</span><span>Points restants <b style="color:var(--c);font-size:16px">2</b> <span class=muted>/ 40</span></span></div>
 {''.join(f'<div style="display:grid;grid-template-columns:96px 26px 170px 26px 1fr;align-items:center;gap:6px;margin-top:11px"><span style="font-size:14px">{n}</span><span class=btn style="padding:2px 8px">-</span><span>{bar(v)} <b style="color:var(--c)">{v}</b></span><span class=btn style="padding:2px 7px">+</span><span class=muted style="font-size:11px">{t}</span></div>' for n,v,t in attrs)}
 <div class=lbl style="margin-top:16px">Traits · 0 à 2</div>
 <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px">
  <span class="btn sel">Pieds de sable</span><span class=btn>Pas de nerfs</span><span class=btn>Œil de pillard</span><span class=btn>Gueule cassée</span><span class=btn>Insomniaque</span></div>
 <div class=muted style="font-size:11.5px;margin-top:8px">Pieds de sable : le désert ne te fatigue pas. En ville, Discrétion −10.</div>
</div>
<div class=rp style="left:510px;top:76px;width:460px;bottom:76px;padding:16px">
 <div style="display:flex;justify-content:space-between"><span class=lbl>Compétences</span><span>Favorites <b style="color:var(--c)">3/3</b></span></div>
 {''.join(f'<div style="display:grid;grid-template-columns:22px 150px 1fr 40px;align-items:center;margin-top:9px"><span style="color:var(--c)">{"*" if f else ""}</span><span style="{"color:var(--c)" if f else ""}">{n}</span><span style="height:6px;background:rgba(242,180,74,.15)"><span style="display:block;height:6px;width:{v}%;background:{"var(--c)" if f else "rgba(253,233,194,.7)"}"></span></span><span style="text-align:right">{v}</span></div>' for n,v,f in skills)}
 <div class=muted style="font-size:11.5px;margin-top:14px">* favorite : +15 au départ, progresse plus vite.</div>
</div>
<div class=rp style="left:986px;top:76px;right:24px;bottom:76px;padding:16px;line-height:1.75">
 <div class=lbl>Fiche</div>
 <div style="margin:10px 0;border:1px solid var(--d);height:150px;background:url(file://{D}/portrait-player.webp) center 20%/cover"></div>
 PV <b style="color:var(--c)">38</b><br>PA <b style="color:var(--c)">8</b> · Initiative 7<br>Implant : aucun<br>Dollars : 25 $<br>
 <div class=lbl style="margin-top:10px">À Dusk-Town</div><span class=muted style="font-size:11.5px">Sol te reconnaît. Teo te prévient deux fois avant les camions.</span>
</div>
<div class=rp style="left:24px;right:24px;bottom:20px;padding:8px 14px;display:flex;justify-content:space-between;align-items:center">
 <span class=btn>&lt; Identité</span><span class=muted>Tu pourras monter tes compétences en jouant.</span><span class="btn on">Entrer dans Dusk-Town &gt;</span></div>
"""))
# 4. COMBAT bureau / mobile
def combat(prof, w, h):
    P = proj[prof]; pts = P['pts']; s = 1
    poly = ''.join(f'<polygon points="{" ".join(f"{c["x"]:.1f},{c["y"]:.1f}" for c in cell)}" fill="rgba(242,180,74,.22)" stroke="rgba(242,180,74,.8)" stroke-width="1"/>' for cell in P['cells'])
    sh = 46 if prof == 'desktop' else 30
    en = ''.join(f'<img src="file://{D}/soldat.webp" style="position:absolute;left:{pts[k]["x"]-sh*0.18:.0f}px;top:{pts[k]["y"]-sh:.0f}px;height:{sh}px">' for k in ('e1', 'e2', 'e3'))
    t = pts['e1']; pl = pts['player']
    ring = f'<ellipse cx="{t["x"]:.0f}" cy="{t["y"]:.0f}" rx="{14 if prof=="desktop" else 10}" ry="{7 if prof=="desktop" else 5}" fill="none" stroke="#e8553a" stroke-width="2"/>'
    los = f'<line x1="{pl["x"]:.0f}" y1="{pl["y"]-20 if prof=="desktop" else pl["y"]-12:.0f}" x2="{t["x"]:.0f}" y2="{t["y"]-25 if prof=="desktop" else t["y"]-16:.0f}" stroke="rgba(242,180,74,.85)" stroke-dasharray="5 4" stroke-width="1.5"/>'
    svg = f'<svg style="position:absolute;inset:0" width="{w}" height="{h}">{poly}{ring}{los}</svg>'
    frise = ''.join(f'<div style="width:{30 if prof=="desktop" else 24}px;height:{30 if prof=="desktop" else 24}px;border:1px solid {"var(--c)" if i==0 else "var(--d)"};background:{"url(file://"+D+"/portrait-player.webp) center 20%/cover" if i==0 else "rgba(232,85,58,.35)"};font-size:10px;text-align:center;line-height:28px">{"" if i==0 else "S"+str(i)}</div>' for i in range(4))
    if prof == 'desktop':
        ui = f"""
<div class=rp style="left:12px;top:12px;padding:8px 12px;display:flex;gap:18px">
 <div><div class=lbl>Points de vie</div><div style="font-family:VT;font-size:22px">38/38</div></div>
 <div><div class=lbl>Points d'action</div><div style="font-family:VT;font-size:22px;color:var(--c)">2 <span style="color:var(--t)">/ 6</span></div><div style="display:flex;gap:3px">{''.join(f'<span style="width:12px;height:6px;background:{"var(--c)" if i<2 else "rgba(242,180,74,.18)"}"></span>' for i in range(6))}</div></div>
 <div><div class=lbl>Arme</div><div style="font-size:12.5px;margin-top:3px">Pistolet · 5/8</div></div></div>
<div class=rp style="left:50%;transform:translateX(-50%);top:12px;padding:5px 10px;display:flex;gap:6px;align-items:center"><span class=lbl style="margin-right:6px">Combat · tour 2</span>{frise}</div>
<div class=rp style="left:{t['x']+24:.0f}px;top:{t['y']-118:.0f}px;width:230px;padding:9px 11px;font-size:12px;line-height:1.55">
 <div style="color:var(--c)">Soldat du Service</div><div class=muted>blessé · couvert partiel</div>
 <div style="margin-top:5px">Tir visé · <b style="color:var(--c)">4 PA</b> <span class=muted>(il t'en reste 2)</span></div>
 <div>Torse 58 % · Tête 27 %</div><div>Bras 41 % · Jambes 49 %</div><div class=muted>Dégâts 6 à 9</div></div>
<div class=rp style="left:{pts['player']['x']+60:.0f}px;top:{P['cells'][-1][2]['y']+6:.0f}px;padding:3px 8px;font-size:11.5px">Déplacer · <b style="color:var(--c)">4 m · 4 PA</b> → couvert</div>
<div class=rp style="left:12px;bottom:14px;padding:8px;display:flex;gap:6px;align-items:center">
 <span class="btn on"><u>1</u>Tir 3</span><span class=btn><u>2</u>Visé 4</span><span class=btn style="opacity:.5"><u>3</u>Rafale 5</span><span class=btn><u>4</u>Recharger 2</span><span class=btn><u>5</u>Se baisser 1</span><span class=btn><u>6</u>Objet 2</span>
 <span style="width:1px;height:24px;background:var(--d);margin:0 4px"></span><span class=btn><u>Espace</u>Fin du tour</span></div>
<div class=rp style="left:12px;bottom:62px;padding:6px 8px;display:flex;gap:6px;align-items:center"><span class=lbl style="margin-right:4px">Visée</span><span class="btn sel">Torse</span><span class=btn>Tête</span><span class=btn>Bras</span><span class=btn>Jambes</span></div>
<div class=rp style="right:12px;bottom:14px;padding:6px 10px;font-size:11.5px"><span class=lbl>Tours ennemis</span> ×2 · <u style="color:var(--c);text-decoration:none">Maj</u> accélère</div>
<div class=rp style="right:12px;top:12px;padding:5px 10px"><span style="font-family:VT;font-size:19px;color:var(--c)">DUSK-TOWN · LE TRANSIT</span></div>
<div style="position:absolute;inset:0;border:2px solid rgba(242,180,74,.45);pointer-events:none"></div>"""
    else:
        ui = f"""
<div class=rp style="left:8px;top:8px;right:8px;padding:6px 10px;display:flex;justify-content:space-between;align-items:center">
 <div><div class=lbl>PV</div><div style="font-family:VT;font-size:20px">38/38</div></div>
 <div><div class=lbl>PA</div><div style="font-family:VT;font-size:20px;color:var(--c)">2/6</div></div>
 <div style="display:flex;gap:4px">{frise}</div></div>
<div class=rp style="left:8px;right:8px;bottom:206px;padding:9px 11px;font-size:12.5px;line-height:1.5">
 <div style="display:flex;justify-content:space-between"><span style="color:var(--c)">Soldat du Service</span><span class=muted>couvert partiel</span></div>
 <div>Tir visé <b style="color:var(--c)">4 PA</b> · il t'en reste 2</div><div>Torse 58 % · Tête 27 % · Dégâts 6 à 9</div>
 <div class=muted style="font-size:11px;margin-top:3px">Touche encore la cible pour tirer.</div></div>
<div class=rp style="left:8px;right:8px;bottom:128px;padding:6px;display:grid;grid-template-columns:repeat(4,1fr);gap:5px">
 <span class="btn sel" style="text-align:center;padding:10px 0">Torse</span><span class=btn style="text-align:center;padding:10px 0">Tête</span><span class=btn style="text-align:center;padding:10px 0">Bras</span><span class=btn style="text-align:center;padding:10px 0">Jambes</span></div>
<div class=rp style="left:8px;right:8px;bottom:62px;padding:6px;display:grid;grid-template-columns:repeat(5,1fr);gap:5px">
 <span class="btn on" style="text-align:center;padding:11px 0">Tir 3</span><span class=btn style="text-align:center;padding:11px 0">Visé 4</span><span class=btn style="text-align:center;padding:11px 0">Rech. 2</span><span class=btn style="text-align:center;padding:11px 0">Baisser</span><span class=btn style="text-align:center;padding:11px 0">...</span></div>
<div class=rp style="left:8px;right:8px;bottom:12px;padding:6px;display:flex;gap:6px">
 <span class=btn style="flex:1;text-align:center;padding:10px 0">Fin du tour</span><span class=btn style="text-align:center;padding:10px 14px">×2</span></div>
<div style="position:absolute;inset:0;border:2px solid rgba(242,180,74,.45);pointer-events:none"></div>"""
    return page(f'combat-{prof}', w, h, f'<div class=bg style="background-image:url(file://{D}/bg-combat-{prof}.png)"></div>{svg}{en}{ui}', 1 if prof == 'desktop' else 2)
screens.append(combat('desktop', 1280, 800)); screens.append(combat('mobile', 390, 844))
# 5. OPTIONS
row = lambda n, v: f'<div style="display:grid;grid-template-columns:220px 1fr;align-items:center;margin-top:11px"><span>{n}</span><span>{v}</span></div>'
sl = lambda p: f'<span style="display:inline-block;width:180px;height:6px;background:rgba(242,180,74,.15);vertical-align:middle"><span style="display:block;height:6px;width:{p}%;background:var(--c)"></span></span> <span class=muted>{p}</span>'
seg = lambda opts, i: ' '.join(f'<span class="btn {"sel" if k==i else ""}" style="padding:3px 8px">{o}</span>' for k, o in enumerate(opts))
screens.append(page('options', 1280, 800, f"""
<div class=bg style="background-image:url(file://{D}/bg-q1-desktop.png);filter:brightness(.8)"></div>
<div class=rp style="left:24px;top:24px;width:640px;bottom:24px;padding:18px 22px">
 <h2>OPTIONS</h2>
 <div class=lbl style="margin-top:14px">Son</div>{row('Musique', sl(60))}{row('Effets', sl(80))}{row('Tout couper (S)', seg(['Non','Oui'],0))}
 <div class=lbl style="margin-top:22px">Interface</div>{row('Mode minimal au démarrage (H)', seg(['Non','Oui'],0))}{row('Taille du texte', seg(['100 %','115 %','130 %'],1))}{row('Contraste renforcé', seg(['Non','Oui'],0))}
 <div class=lbl style="margin-top:22px">Combat</div>{row('Vitesse des tours ennemis', seg(['×1','×2','×4'],1))}{row('Confirmer les actions', seg(['Double tap','Toujours','Jamais'],0))}{row('Chances au survol', seg(['Non','Oui'],1))}
 <div class=lbl style="margin-top:22px">Accessibilité</div>{row('Texte des dialogues', seg(['Instantané','Défilant'],0))}{row('Police', seg(['Radio (VT323)','Lisible (Plex)'],0))}{row('Réduire les animations', seg(['Non','Oui'],0))}
 <div class=lbl style="margin-top:22px">Langue</div>{row('Langue', seg(['Français'],0))}
 <div style="position:absolute;left:22px;right:22px;bottom:16px;display:flex;justify-content:space-between"><span class=btn><u>Échap</u>Retour</span><span class=muted style="font-size:11.5px">Réglages gardés sur cet appareil, hors sauvegardes.</span></div>
</div>"""))
# 6. CODEX
cats = [('Lieux', ['Dusk-Town', 'Le Scellé', 'Steel-Megalopolis', '???']), ('Factions', ['Human Corporation', 'Service Militarisé', '???', '???']), ('Peuples', ['Mutants', '???']), ('Objets', ['???'])]
screens.append(page('codex', 1280, 800, f"""
<div class=bg style="background-image:url(file://{D}/bg-q1-desktop.png);filter:brightness(.8)"></div>
<div class=rp style="left:24px;top:24px;width:300px;bottom:24px;padding:18px">
 <h2>CODEX</h2><div class=muted style="font-size:11.5px;margin:4px 0 6px">7 entrées sur 31</div>
 {''.join(f'<div class=lbl style="margin-top:14px">{c}</div>' + ''.join(f'<div class="btn {"sel" if e=="Human Corporation" else ""}" style="display:block;margin-top:5px;{"opacity:.45" if e=="???" else ""}">{e}</div>' for e in es) for c, es in cats)}
</div>
<div class=rp style="left:340px;top:24px;width:560px;padding:20px 22px;line-height:1.7;font-size:14px">
 <div class=lbl>Factions</div><h2 style="font-size:30px;margin:4px 0 12px">HUMAN CORPORATION</h2>
 <p>Une grande société pharmaceutique d'avant la guerre. Elle a laissé un laboratoire sous Dusk-Town.</p>
 <p style="margin-top:10px">L'accès est verrouillé. Beaucoup ont tenté de forcer les portes scellées. Personne n'est passé.</p>
 <p style="margin-top:10px">Quand deux bandes de récupérateurs arrivent le même jour devant la porte, ça finit en bain de sang.</p>
 <div class=muted style="font-size:11.5px;margin-top:18px;border-top:1px solid var(--d);padding-top:8px">Débloqué : la porte d'acier du Scellé · Sources : roman, Ch. I §75, §77</div>
</div>"""))
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome')
    for name, w, h, dpr in screens:
        pg = br.new_page(viewport={'width': w, 'height': h}, device_scale_factor=dpr)
        pg.goto(f'file://{D}/{name}.html'); pg.wait_for_timeout(700); pg.screenshot(path=OUT + f'{name}.png'); pg.close()
    br.close()
print('ok')
