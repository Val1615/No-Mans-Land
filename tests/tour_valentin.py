# Tour de Valentin (mobile, 28/10/2026) : Pia (Lower-Town), marché couvert d'Asia-Ground (ordre de rendu, transparence),
# passage praticable >= 2 m autour du stand d'implants (China Lake), message « : fermé. » sans libellé.
# PHASE=avant : captures seules (état d'origine) ; PHASE=apres (défaut) : captures + assertions.
import os, time, json, io, base64
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8862/'); PHASE = os.environ.get('PHASE', 'apres')
OUT = os.environ.get('OUT', '/tmp/nml-test-out/tour_valentin/'); os.makedirs(OUT, exist_ok=True)
R = []
def check(n, ok, d=''): R.append({'test': n, 'ok': bool(ok), 'detail': str(d)}); print(('OK    ' if ok else 'ECHEC ') + n, d, flush=True)
SET = "(()=>{const g=window.__nml.game,s=g.snapshot();s.location='%s';s.player.x=%s;s.player.z=%s;Object.assign(s.flags,{q_start:true,q_fin:true,steel_passe:true,q_steel:true,cl_barrage:true});g.restore(s,true)})()"
def run(T, VW, VH, mob):
    ctx = br.new_context(viewport={'width': VW, 'height': VH}, is_mobile=mob, has_touch=mob, device_scale_factor=1); pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    E = pg.evaluate
    def press(sel, wait=0.4):
        E(f'(()=>{{const e=document.querySelector({json.dumps(sel)}); if(e) e.scrollIntoView({{block:"center"}})}})()'); time.sleep(0.1)
        b = pg.locator(sel).first.bounding_box(); assert b, sel; pg.mouse.click(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2); time.sleep(wait)
    def go(loc, x, z, w=1.6): E(SET % (loc, x, z)); time.sleep(w)
    def cap(name): pg.screenshot(path=f'{OUT}{PHASE}_{T}_{name}.png'); time.sleep(0.1)
    pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=60000); time.sleep(1.5)
    E("import('./src/core/path.js').then(m => window.__findPath = m.findPath)"); E("import('./src/core/grid.js').then(m => window.__grid = m)")
    press('#m-new', 0.6); press('[data-race="augmente"]'); press('#cr-next', 0.5); press('#cr-enter', 1.2)
    # Livrables d'Ocre (retours tour 1) : Chez Moss, Maison de thé, lac
    go('steel_lower', 38, 32); cap('2_chez_moss'); go('steel_china', 35, 9.5); cap('3_maison_the'); go('steel_china', 24, 29); cap('6_lac')
    if os.environ.get('ONLY') == 'ocre': ctx.close(); return
    # 1. Pia, Allée du Foyer
    go('steel_lower', 14.4, 28.5); cap('1_pia')
    # 4-5. Marché couvert
    go('steel_asia', 24, 29); cap('4_marche_dehors')
    go('steel_asia', 24, 26.8); cap('5_marche_bord_sud')
    go('steel_asia', 17.5, 24.5); cap('5_marche_entree')
    # 6. Stand d'implants (quai nord de China Lake)
    go('steel_china', 18, 9.7); cap('6_implants')
    # 7. clic sur un étal sans libellé
    go('steel_china', 30, 30); E("document.getElementById('msg').textContent=''")
    sp = E("(()=>{const b=window.__nml.world.LOCATIONS.steel_china.buildings.find(b=>b.id==='cl_s_papiers2');return window.__nml.project(b.x+b.w/2,0.6,b.z+b.d/2)})()")
    pk = E(f"window.__nml.pick({sp['x']},{sp['y']})"); pg.mouse.click(sp['x'], sp['y']); time.sleep(0.4); msg = E("document.getElementById('msg').textContent"); cap('7_etal_sans_libelle')
    if PHASE == 'apres':
        # 1. Pia : au sol, aucune boîte vide (props « box ») sous ou à côté d'elle
        pia = E("window.__nml.npcs.find(n=>n.id==='lt_pia')"); L = E("window.__nml.world.LOCATIONS.steel_lower")
        boxes = [p for p in L['props'] if p.get('box') and p['x'] - 1 < pia['x'] < p['x'] + p['w'] + 1 and p['z'] - 1 < pia['z'] < p['z'] + p['d'] + 1]
        check(f'{T} 1. Pia au sol, sans volume vide à moins d\u20191 m', not boxes and not pia.get('y'), boxes)
        # 4. ordre de rendu : chaque stand sous une halle est dessiné avant elle (la halle couvre les stands)
        go('steel_asia', 24, 33); od = E("""(()=>{const v=window.__nml.view,A=window.__nml.world.LOCATIONS.steel_asia.buildings,H=A.filter(b=>b.cover),out=[];window.__nml.game.state.player.x=24;window.__nml.game.state.player.z=33;v.render();v.render();
          for(const s of A.filter(b=>!b.cover&&b.x>=12&&b.x<36&&b.z>=10&&b.z<26)){const h=H.find(h=>s.x<h.x+h.w&&s.x+s.w>h.x&&s.z<h.z+h.d&&s.z+s.d>h.z);if(h)out.push([s.id,h.id,v.orderOf(s.id),v.orderOf(h.id)])}return out})()""")
        check(f'{T} 4. stands du marché dessinés sous la halle ({len(od)} stands)', len(od) >= 8 and all(a[2] < a[3] for a in od), [a for a in od if not a[2] < a[3]])
        # 5. transparence dès l'emprise ou son abord (<= 1,5 m), opaque loin
        def op(x, z):
            go('steel_asia', x, z, 0.2)
            for _ in range(15): E("window.__nml.view.render()")
            return [round(E(f"window.__nml.opacityOf('ag_halle{i}')"), 2) for i in range(3)]
        res = {k: op(*k) for k in [(16, 25), (24, 27.2), (13, 11), (34.5, 24.5), (24, 32)]}
        check(f'{T} 5. halle transparente à l\u2019entrée (coin sud-ouest)', res[(16, 25)][0] < 0.5, res[(16, 25)])
        check(f'{T} 5. halle transparente à l\u2019abord (1,2 m au sud)', res[(24, 27.2)][1] < 0.5, res[(24, 27.2)])
        check(f'{T} 5. halle transparente au coin nord-ouest', res[(13, 11)][0] < 0.5, res[(13, 11)])
        check(f'{T} 5. halle transparente au coin sud-est', res[(34.5, 24.5)][2] < 0.5, res[(34.5, 24.5)])
        check(f'{T} 5. halle opaque loin (6 m au sud)', min(res[(24, 32)]) > 0.9, res[(24, 32)])
        # 6. passage >= 2 m le long du stand d'implants : pathfinding sur une grille gonflée de 1 m (demi-largeur), PNJ compris
        pw = E("""(()=>{const n=window.__nml,G=n.__g||null,loc=n.world.LOCATIONS.steel_china,sp=n.view?null:null;
          const npc=n.npcs.filter(q=>q.location==='steel_china').map(q=>({x:q.x-0.3,z:q.z-0.3,w:0.6,d:0.6}));
          const S=window.__grid.solidsOf(loc,n.doors,window.__nml.game.sprites||{}).concat(npc),C=0.5,r=1.0,w=Math.round(loc.size.w/C)+1,d=Math.round(loc.size.d/C)+1,bl=new Uint8Array(w*d);
          for(let j=0;j<d;j++)for(let i=0;i<w;i++){const x=i*C,z=j*C;for(const s of S)if(x>s.x-r&&x<s.x+s.w+r&&z>s.z-r&&z<s.z+s.d+r){bl[j*w+i]=1;break}}
          const g={w,d,blocked:bl,toCell:(x,z)=>[Math.round(x/C),Math.round(z/C)],toWorld:(i,j)=>({x:i*C,z:j*C}),free(i,j){return i>=0&&j>=0&&i<w&&j<d&&!bl[j*w+i]}};
          const p=window.__findPath(g,{x:12,z:9.75},{x:26,z:9.75});return p?{n:p.length,zmax:Math.max(...p.map(q=>q.z)),zmin:Math.min(...p.map(q=>q.z))}:null})()""")
        check(f'{T} 6. passage de 2 m le long du stand d\u2019implants (pathfinding, dégagement 1 m de chaque côté)', pw and pw['n'] > 5, pw)
        real = E("(()=>{const g=window.__nml.game;return window.__findPath(g.grids.steel_china,{x:12,z:9.75},{x:26,z:9.75})})()")
        check(f'{T} 6. passage praticable avec la grille du jeu', bool(real))
        # 7. message de bâtiment fermé jamais sans libellé
        check(f'{T} 7. clic sur un étal sans libellé : message complet, jamais « : fermé. » coupé', pk and pk.get('kind') == 'closed' and msg and not msg.lstrip().startswith(':'), [pk, msg])
        anon = E("Object.values(window.__nml.world.LOCATIONS).filter(l=>l.id==='steel_china').flatMap(l=>l.buildings).filter(b=>b.id.startsWith('cl_s_')&&!(b.label||'').trim()).map(b=>b.id)")
        check(f'{T} 7. tous les étaux de China Lake ont un libellé', not anon, anon)
        # Livrables d'Ocre : lac en polygone (eau rétrécie de 0,6 m), quai marchable, PNJ hors de l'eau, Moss et maison de thé compacts
        lac = E("""(async()=>{const m=await import('./src/data/china_lake.js'),G=await import('./src/core/grid.js'),g=window.__nml.game.grids.steel_china;
          const fr=(x,z)=>{const [i,j]=g.toCell(x,z);return g.free(i,j)};const quai=m.LAC_POLY.map((p,k)=>[(p[0]+m.EAU_POLY[k][0])/2,(p[1]+m.EAU_POLY[k][1])/2]);
          const qok=quai.filter(([x,z])=>{const [i,j]=g.toCell(x,z),q=g.toWorld(i,j);return !G.inPoly(m.EAU_POLY,q.x,q.z)});
          return {eau:fr(24,18),eau2:fr(20,20),quai:[quai[7],fr(quai[7][0],quai[7][1])],quaiLibres:qok.filter(([x,z])=>fr(x,z)).length,quaiN:qok.length,
            wet:window.__nml.npcs.filter(n=>n.location==='steel_china'&&G.inPoly(m.EAU_POLY,n.x,n.z)).map(n=>n.id),
            lant:window.__nml.world.LOCATIONS.steel_china.ground.water[0].lanterns.filter(l=>!G.inPoly(m.EAU_POLY,l.x,l.z)).length,img:window.__nml.world.LOCATIONS.steel_china.ground.water[0].image}})()""")
        check(f'{T} lac : un point dans l’eau (24 ; 18) non marchable', not lac['eau'] and not lac['eau2'], lac)
        check(f'{T} lac : un point sur le quai marchable, et tout le quai marchable', lac['quai'][1] and lac['quaiLibres'] == lac['quaiN'] and lac['quaiN'] > 20, (lac['quai'], lac['quaiLibres'], lac['quaiN']))
        check(f'{T} lac : aucun PNJ de China Lake dans l’eau ; lanternes sur l’eau ; image g_cl_lac', not lac['wet'] and lac['lant'] == 0 and lac['img'] == 'g_cl_lac', lac)
        hs = E("[window.__nml.world.LOCATIONS.steel_lower.buildings.find(b=>b.id==='lt_moss').ph.h]")
        check(f'{T} Chez Moss h 4,5 (sprite d’origine 389 x 669 tassé par sy 0,584)', hs == [4.5], hs)
        # Régie (28/10) : depuis (24 ; 34), Mei sous la halle reste visible (silhouette), étiquette lisible, sélectionnable
        go('steel_asia', 24, 34)
        for _ in range(15): E("window.__nml.view.render()")
        cap('8_mei_de_loin')
        mei = E("""(()=>{const n=window.__nml.npcs.find(n=>n.id==='ag_mei'||n.name==='Mei Tran'),v=window.__nml.view,p=window.__nml.project(n.x,1.0,n.z);
          const lab=[...document.querySelectorAll('.wlabel.npc')].find(e=>e.textContent==='Mei Tran');const r=lab&&lab.getBoundingClientRect();
          const hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
          return {id:n.id,g:v.ghostOf(n.id),halle:v.opacityOf('ag_halle0'),lab:!!lab&&!lab.hidden&&r.width>0&&r.x>=0&&r.right<=innerWidth&&r.y>=0&&r.bottom<=innerHeight,labTop:hit===lab||lab.contains(hit),pick:window.__nml.pick(p.x,p.y),hOrd:v.orderOf('ag_halle0'),sOrd:v.orderOf('ag_mei')}})()""")
        check(f'{T} Régie : depuis (24 ; 34), Mei visible à travers la halle opaque (silhouette 45 %)', mei['g'] and mei['g']['visible'] and abs(mei['g']['opacity'] - 0.45) < 0.01 and mei['halle'] > 0.9, mei)
        check(f'{T} Régie : étiquette de Mei visible à l’écran et au premier plan', mei['lab'], mei)
        check(f'{T} Régie : Mei sélectionnable (pick = npc)', mei['pick'] and mei['pick'].get('kind') == 'npc' and mei['pick'].get('npcId') == mei['id'], mei['pick'])
        check(f'{T} Régie : halle toujours dessinée au-dessus du stand de Mei', mei['hOrd'] > mei['sOrd'], (mei['hOrd'], mei['sOrd']))
        go('steel_asia', 16, 25, 0.2)
        for _ in range(15): E("window.__nml.view.render()")
        g2 = E(f"window.__nml.view.ghostOf('{mei['id']}')"); check(f'{T} Régie : à l’approche, halle transparente et silhouette masquée', E("window.__nml.opacityOf('ag_halle0')") < 0.5 and not g2['visible'], g2)
        # bord du quai de China Lake, côté eau, caméra rapprochée (capture seule, pour juger le débord ~0,3 m)
        import math
        q = E("import('./src/data/china_lake.js').then(m=>{const k=0,a=m.LAC_POLY[k],b=m.EAU_POLY[k];return [a,b]})")
        qx, qz = q[1][0] + (q[0][0] - q[1][0]) * 0.1, q[1][1] + (q[0][1] - q[1][1]) * 0.1
        go('steel_china', qx, qz, 1.0); E(f"(()=>{{const p=window.__nml.game.state.player;p.x={qx};p.z={qz};p.path=[];window.__nml.view.setCamera({{x:{qx},z:{qz},ppm:150}})}})()"); time.sleep(0.8)
        pg.screenshot(path=f'{OUT}quai_bord_{T}.png'); E("window.__nml.view.setCamera(null)"); go('steel_china', 24, 28.5); pg.screenshot(path=f'{OUT}lac_v3_{T}.png'); print('quai', T, round(qx, 2), round(qz, 2), E("[window.__nml.game.state.player.x,window.__nml.game.state.player.z]"))
    check(f'{T} aucune erreur JS', not errs, errs[:3]); ctx.close()
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    run('desktop', 1280, 800, False); run('mobile', 390, 844, True); br.close()
json.dump(R, open(OUT + f'resultats_{PHASE}.json', 'w'), ensure_ascii=False, indent=1)
bad = [r for r in R if not r['ok']]; print(f'{len(R) - len(bad)}/{len(R)} OK'); raise SystemExit(1 if bad else 0)
