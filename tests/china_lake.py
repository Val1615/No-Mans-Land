# China Lake lot 3 (steel_china), sans quêtes : accès sans argent par Lower-Town (l_sud_est <-> k_est), Barrage payant (20 cr), tour du lac par les quais, eau non praticable, 3 intérieurs, PNJ, emprises d Ocre, captures réelles.


import sys, os, time, io, json, base64, re
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8799/'); OUT = os.environ.get('OUT', '/tmp/nml-test-out/china_lake/'); os.makedirs(OUT, exist_ok=True)
R = []
def check(n, ok, d=''): R.append({'test': n, 'ok': bool(ok), 'detail': str(d)}); print(('OK    ' if ok else 'ECHEC ') + n, d, flush=True)
def png(u): return np.asarray(Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB')).astype(int)
MAG = lambda a: np.abs(a - [255, 0, 255]).sum(2) > 90
def content(a):
    m = MAG(a); ys, xs = np.nonzero(m); return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
def aligned(A, B, r=4):  # même mesure que flip_pixels (recalage ±r px), pour direct et miroir
    A, B = content(A), content(B); H, W = max(len(A), len(B)) + 2 * r, max(A.shape[1], B.shape[1]) + 2 * r
    def pad(I, dx=0, dy=0): c = np.zeros((H, W, 3)) + [255, 0, 255]; c[r + dy:r + dy + len(I), r + dx:r + dx + I.shape[1]] = I; return c
    a = pad(A)
    def best(I): return min(np.abs(a - pad(I, dx, dy)).sum(2)[MAG(a) | MAG(pad(I, dx, dy))].mean() for dx in range(-r, r + 1) for dy in range(-r, r + 1))
    return round(best(B), 1), round(best(B[:, ::-1]), 1)
# v13 : mesures d'image (canvas rendu, bandeaux HUD exclus) : saturation moyenne, part de pixels néon, luminance des zones éclairées
def hsv(a):
    a = a / 255.0; mx, mn = a.max(2), a.min(2); return mx, np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
def mood(a):
    v, sat = hsv(a); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    neon = (sat > 0.45) & (v > 0.45) & ((b > r + 10) | ((b > g) & (r > g + 10)))  # néons froids : cyan, bleu, violet (le sable orangé n'en est pas)
    return {'sat': round(float(sat.mean()), 3), 'neon': round(float(neon.mean()), 4), 'v95': round(float(np.percentile(v, 95)), 3), 'v': round(float(v.mean()), 3)}
def crop_hud(a): h = a.shape[0]; return a[int(h * 0.1):int(h * 0.9)]
REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../docs/captures/steel-l1-v12/live/')
def rgb_file(p): return np.asarray(Image.open(p).convert('RGB')).astype(int)
def centroid(u):
    a = png(u); m = MAG(a); ys, xs = np.nonzero(m); return (float(xs.mean()), float(ys.mean()), int(m.sum())) if len(xs) else (0, 0, 0)
CAP = os.environ.get('CAP', '/tmp/nml-test-out/china_lake/'); os.makedirs(CAP, exist_ok=True)
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    mob = False; VW, VH = 1280, 800; T = 'desktop'
    ctx = br.new_context(viewport={'width': VW, 'height': VH}); pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('response', lambda r: r.status >= 400 and errs.append(f'{r.status} {r.url}'))
    gesture = pg.mouse.click
    E = pg.evaluate; st = lambda: E('JSON.parse(JSON.stringify(window.__nml.state))'); P = lambda x, y, z: E(f'window.__nml.project({x},{y},{z})')
    onscreen = lambda pt: 20 < pt['x'] < VW - 20 and 130 < pt['y'] < VH - 120
    shot = lambda: np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert('RGB')).astype(int)
    def waitjs(js, t=25):
        t0 = time.time()
        while time.time() - t0 < t:
            if E(js): return True
            time.sleep(0.1)
        return False
    def idle(): waitjs('(()=>{const s=window.__nml.state;return !s.player.path.length && !s.player.pending})()', 30); time.sleep(0.3)
    def press(sel, wait=0.4):
        E(f'(()=>{{const e=document.querySelector({json.dumps(sel)}); if(e&&e.closest("#creation")&&!e.closest(".cr-foot")) e.scrollIntoView({{block:"center"}})}})()'); time.sleep(0.1)
        b = pg.locator(sel).first.bounding_box(); assert b, sel; gesture(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2); time.sleep(wait)
    def option(label):
        loc = pg.locator('#dlg-options button', has_text=label)
        if not loc.count(): return False
        b = loc.first.bounding_box()
        if not b: return False
        gesture(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2); time.sleep(0.5); return True
    def opts(): return E("[...document.querySelectorAll('#dlg-options button')].map(b=>b.textContent)")
    def dtext(): return E("document.getElementById('dlg-text').textContent")
    def close_dlg():
        for _ in range(6):
            if not st()['dialogue']: return
            press('#dlg-close', 0.3)
    def walk(x, z, tol=0.8):  # marche par taps successifs sur le sol visible, le long du chemin
        loc0 = st()['location']
        for _ in range(25):
            s = st()
            if s['location'] != loc0 or s['dialogue']: return True
            if np.hypot(x - s['player']['x'], z - s['player']['z']) < tol: return True
            path = E(f"(()=>{{const g=window.__nml.game; return window.__findPath(g.grids[g.state.location], g.state.player, {{x:{x},z:{z}}})}})()")
            if not path: return False
            tapped = False
            for q in reversed(path[1:]):
                pt = P(q['x'], 0, q['z'])
                if not onscreen(pt): continue
                k = E(f'window.__nml.pick({pt["x"]},{pt["y"]})')
                if not k or k['kind'] != 'ground' or np.hypot(k['x'] - q['x'], k['z'] - q['z']) > 1.0: continue
                gesture(pt['x'], pt['y']); tapped = True; break
            if not tapped: return False
            idle()
        return False
    def tap_npc(nid):
        n = E(f"window.__nml.npcs.find(n=>n.id==='{nid}')"); pt = P(n['x'], 1.0, n['z']); gesture(pt['x'], pt['y'])
        return waitjs(f"window.__nml.state.dialogue && window.__nml.state.dialogue.npc==='{nid}' && !document.getElementById('dialogue').hidden", 20)
    def enter_door(did):  # marcher près du seuil puis le bouton d'action (« Entrer », « Sortir », « Vers... ») au geste
        d = E(f"window.__nml.game.doorById('{did}')"); loc0 = st()['location']
        walk(d['threshold']['x'], d['threshold']['z'], tol=1.6)
        if st()['location'] != loc0: return True
        if E("!document.getElementById('act').hidden"): press('#act', 0.3)
        return waitjs(f"window.__nml.state.location !== '{loc0}'", 20)
    def bvis(bid):  # part du sprite du bâtiment réellement visible à l'écran
        u = E(f"window.__nml.view.isolateBuilding('{bid}')")
        if not u: return 0, 0
        iso = png(u); m = MAG(iso); full = shot(); return round(float(((np.abs(full - iso).sum(2) < 60) & m).sum() / max(1, m.sum())), 2), int(m.sum())
    def cap(name): pg.screenshot(path=CAP + name + '.png'); time.sleep(0.1)
    pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=60000); time.sleep(1.5)
    E("import('./src/core/path.js').then(m => window.__findPath = m.findPath)")
    press('#m-new', 0.6); press('[data-race="augmente"]'); press('#cr-next', 0.5); press('#cr-enter', 1.2)
    check('perso créé', st().get('character'))
    def talk(nid, capname=None, mn=2):
        close_dlg(); n0 = E(f"window.__nml.npcs.find(n=>n.id==='{nid}')"); walk(n0['x'], n0['z'] + 1.8, tol=1.6)
        ok = tap_npc(nid); t1 = dtext() if ok else ''
        if capname: cap(capname)
        n = 1
        while option('Et sinon ?'): n += 1
        check(f'dialogue {nid} ({n} répliques)', ok and n >= mn and t1, t1[:50]); close_dlg()
    W = "window.__nml.world.LOCATIONS.steel_china"
    man = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../assets/buildings/manifest.json')))
    bl = E(f"{W}.buildings.map(b=>[b.id,b.sprite,b.w,b.d])")
    bad = [b for b in bl if b[1] in man and [b[2], b[3]] != man[b[1]]['footprint_m']]
    check('emprises = footprint_m du manifeste (maison de thé 10 x 5,5, fond 7 x 8 / 6 x 8, cabane 8 x 2, stands 2,5 x 1-2)', not bad and len(bl) > 30, bad[:4])
    check('pivots stands implants / puces : y 168 / 167', [man['cl_stand_implants']['anchor'][1], man['cl_stand_puces']['anchor'][1]] == [168, 167])
    check('maison de thé : seul toit recourbé (1 seul cl_maison_the)', sum(1 for b in bl if b[1] == 'cl_maison_the') == 1)
    check('Pavillon du Dragon à China Lake', any(b[0] == 'cl_dragon' for b in bl) and E("window.__nml.world.LOCATIONS.dragon_in.name").endswith('Pavillon du Dragon'))
    check('aucun néon (DA : ni cyan ni violet)', not any('neon' in b[1] for b in bl))
    # Lower-Town -> China Lake sans un crédit (ruelle l_sud_est, libre)
    E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_lower';s.player.x=30;s.player.z=33;s.player.credits=0;s.player.money=0;Object.assign(s.flags,{q_start:true,q_fin:true,steel_passe:true,q_steel:true});g.restore(s,true)})()"); time.sleep(1.5)
    free = E("['l_sud_est','k_est','k_nord'].every(id=>!(window.__nml.game.doorById(id).conditions||[]).length)")
    check('l_sud_est / k_est / k_nord sans condition (China Lake joignable sans argent)', free)
    ok = enter_door('l_sud_est'); time.sleep(2)
    check('Lower-Town -> China Lake (l_sud_est -> k_est) à 0 cr / 0 $', ok and st()['location'] == 'steel_china' and st()['player']['x'] > 45, (st()['location'], st()['player']['x']))
    cap('01_arrivee_ruelle_k_est')
    # le lac n'est pas praticable ; le tour complet se fait par les quais
    wet = E("""(async()=>{const m=await import('./src/data/china_lake.js'),G=await import('./src/core/grid.js'),g=window.__nml.game.grids.steel_china;let n=0,b=0;for(let j=0;j<g.d;j++)for(let i=0;i<g.w;i++){const p=g.toWorld(i,j);
      if(G.inPoly(m.EAU_POLY,p.x,p.z)){n++;if(!g.free(i,j))b++}}return [n,b]})()""")  # retours tour 1 : eau = polygone d'Ocre rétréci de 0,6 m
    check('eau : toutes les cases du lac bloquées', wet[0] > 100 and wet[0] == wet[1], wet)
    loop = [(24, 10), (36, 19), (24, 29), (8, 21), (24, 10)]
    paths = [E(f"(()=>{{const g=window.__nml.game; const p=window.__findPath(g.grids.steel_china, {{x:{a[0]},z:{a[1]}}}, {{x:{b[0]},z:{b[1]}}}); return p?p.length:0}})()") for a, b in zip(loop, loop[1:])]
    check('connexité des quais : tour complet du lac (N -> E -> S -> O -> N)', all(paths), paths)
    for (x, z), name in [((36, 19), '02_quai_est_armes'), ((24, 29.6), '03_quai_sud_papiers'), ((8, 21), '04_quai_ouest_ponton')]:
        ok = walk(x, z, tol=1.2); time.sleep(1); s = st()
        check(f'marche réelle {name}', ok and np.hypot(s['player']['x'] - x, s['player']['z'] - z) < 1.6, (round(s['player']['x'], 1), round(s['player']['z'], 1)))
        cap(name)
    talk('cl_shen', '05_shen')
    walk(24, 10, tol=1.2); time.sleep(1); cap('06_quai_nord_barrage')
    for nid in ['cl_m_nord', 'cl_m_est', 'cl_m_sud', 'cl_m_ouest', 'cl_tech']: talk(nid)
    sizes = E("['the_in','dragon_in','filets_in'].map(k=>window.__nml.world.LOCATIONS[k].size)")
    check('3 intérieurs >= 10 x 8 m', all(z['w'] >= 10 and z['d'] >= 8 for z in sizes), sizes)
    near = E("""(()=>{const w=window.__nml.world,out=[];for(const n of window.__nml.npcs.filter(n=>n.id.startsWith('cl_'))){
      const pts=[...w.DOORS.filter(d=>d.location===n.location).flatMap(d=>[d.opening,d.threshold]),...(w.LOCATIONS[n.location].buildings||[]).filter(b=>b.named).map(b=>({x:b.x+b.w/2,z:b.z+b.d}))];
      const m=Math.min(...pts.map(p=>Math.hypot(p.x-n.x,p.z-n.z)));out.push([n.id,+m.toFixed(2)])}return out})()""")
    check('PNJ à >= 1,5 m des portes et libellés', all(m >= 1.5 for _, m in near), near)
    near2 = E("""(()=>{const w=window.__nml.world,out=[];for(const n of window.__nml.npcs.filter(n=>n.location==='steel_china')){
      const pts=w.LOCATIONS.steel_china.buildings.filter(b=>b.named).flatMap(b=>[{x:b.x+b.w/2,z:b.z+b.d},{x:b.x+b.w/2,z:b.z+b.d/2}]);
      out.push([n.id,+Math.min(...pts.map(p=>Math.hypot(p.x-n.x,p.z-n.z))).toFixed(2)])}return out})()""")
    check('PNJ de China Lake à >= 1,5 m des libellés et du centre des stands (mesure de Régie)', all(m >= 1.5 for _, m in near2), near2)
    wetn = E("""(()=>{const w=window.__nml.world,out=[];for(const n of window.__nml.npcs){const W=((w.LOCATIONS[n.location]||{}).ground||{}).water||[];
      if(W.some(q=>n.x>=q.x&&n.x<=q.x+q.w&&n.z>=q.z&&n.z<=q.z+q.d))out.push(n.id)}return out})()""")
    check('aucun PNJ sur l\'eau', not wetn, wetn)
    E("window.__nml.state.player.credits=6")
    for door, inn, nid in [('cl_dragon_door', 'dragon_in', 'cl_lo'), ('cl_the_door', 'the_in', 'cl_zhou'), ('cl_filets_door', 'filets_in', 'cl_yu')]:
        ok = enter_door(door); time.sleep(1.2); check(f'entrée {inn}', ok and st()['location'] == inn, st()['location'])
        talk(nid, f'07_{inn}')
        if inn == 'dragon_in':
            tap_npc('cl_serveur'); option('Le bol du jour'); check('Pavillon du Dragon : bol du jour 5 cr', st()['player']['credits'] == 1, st()['player']['credits']); close_dlg()
        ok = enter_door(f'{inn}_door'); time.sleep(1.2); check(f'sortie {inn}', st()['location'] == 'steel_china', st()['location'])
    # eau : la répétition du carreau 512 px est cassée (corrélation entre deux zones du lac distantes d'un carreau)
    E("window.__nml.view.setCamera({x:24,z:19,ppm:30})"); time.sleep(1.2); cap('08_lac_eau')
    a = shot().mean(2); pa, pb = P(17, 0, 15), P(23, 0, 15)
    A = a[int(pa['y']) - 30:int(pa['y']) + 30, int(pa['x']) - 30:int(pa['x']) + 30]; Bq = a[int(pb['y']) - 30:int(pb['y']) + 30, int(pb['x']) - 30:int(pb['x']) + 30]
    cc = float(np.corrcoef(A.ravel(), Bq.ravel())[0, 1]) if A.shape == Bq.shape and A.size else 1
    check('eau : deux carreaux voisins ne se ressemblent pas (corrélation < 0,8)', cc < 0.8, round(cc, 3))
    E("window.__nml.view.setCamera(null)"); time.sleep(0.5)
    # boucle China Lake -> Lower-Town (k_est) puis China Lake -> Asia-Ground (k_nord, sortie libre)
    ok = enter_door('k_est'); time.sleep(1.5)
    check('China Lake -> Lower-Town (k_est -> l_sud_est)', ok and st()['location'] == 'steel_lower' and st()['player']['z'] > 33, (st()['location'], st()['player']['z']))
    ok = enter_door('l_sud_est'); time.sleep(1.5); ok = ok and enter_door('k_nord'); time.sleep(1.5)
    check('China Lake -> Asia-Ground (k_nord -> a_sud) sans payer', ok and st()['location'] == 'steel_asia' and st()['player']['z'] > 33, (st()['location'], st()['player']['z']))
    cap('09_retour_asia_barrage')
    check('aucune erreur JS / 404', not errs, errs[:3])
    br.close()
json.dump(R, open(OUT + 'results.json', 'w'), ensure_ascii=False, indent=1)
bad = [r for r in R if not r['ok']]; print(f'{len(R) - len(bad)}/{len(R)} OK'); sys.exit(1 if bad else 0)
