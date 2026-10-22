# Argent minimal : pour chaque race, origine Errant (15 $) ou, à défaut, l'origine au plus faible argent ; aucun gain d'argent.
# De la route de Steel à Center-Town par le seul chemin de la race : implant -> douane (change réduit 10 $ -> 5 cr, Odile : « Bon. Je signe. ») ;
# sans implant -> Sol, Bruno, trappe, Sous-Ville, Elio « Je n'ai pas vingt dollars » -> porter la caisse -> monte-charge. Mise en place reprise de steel_l1/l2.
import sys, os, time, io, json, base64, re
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8799/'); OUT = os.environ.get('OUT', '/tmp/nml-test-out/lower_town/'); os.makedirs(OUT, exist_ok=True)
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
CAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../docs/captures/lower-town-v1/'); os.makedirs(CAP, exist_ok=True)
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
    E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_center';s.player.x=30;s.player.z=17;Object.assign(s.flags,{q_start:true,q_fin:true,steel_passe:true,q_steel:true});g.restore(s,true)})()"); time.sleep(1.5)
    free = E("(()=>{const g=window.__nml.game.grids.steel_center,[i,j]=g.toCell(47,18);return g.free(i,j)})()")
    check('c_est (47,18) hors bâtiment : case libre', free)
    cap('01_center_avant_descente')
    ok = enter_door('c_est'); time.sleep(1.5)
    check('Center-Town -> Lower-Town par La Descente', ok and st()['location'] == 'steel_lower', st()['location'])
    time.sleep(3); cap('02_arrivee_descente')
    a = crop_hud(shot()); m = mood(a); check('palette : pas de néon violet/cyan (part < 0,3 %)', m['neon'] < 0.003, m)
    def talk(nid, capname=None):
        close_dlg(); n0 = E(f"window.__nml.npcs.find(n=>n.id==='{nid}')"); walk(n0['x'], n0['z'] + 1.8, tol=1.6)
        ok = tap_npc(nid); t1 = dtext() if ok else ''
        if capname: cap(capname)
        n = 1
        while option('Continuer.') or option('Et alors ?'): n += 1
        check(f'dialogue {nid} ({n} répliques)', ok and n >= 3 and t1, t1[:50]); close_dlg()
    # PNJ à >= 1,5 m de toute porte/jonction/libellé de bâtiment du même lieu [plan §0]
    near = E("""(()=>{const w=window.__nml.world,out=[];for(const n of window.__nml.npcs.filter(n=>n.id.startsWith('lt_'))){
      const pts=[...w.DOORS.filter(d=>d.location===n.location).flatMap(d=>[d.opening,d.threshold]),...(w.LOCATIONS[n.location].buildings||[]).filter(b=>b.named).map(b=>({x:b.x+b.w/2,z:b.z+b.d}))];
      const m=Math.min(...pts.map(p=>Math.hypot(p.x-n.x,p.z-n.z)));out.push([n.id,+m.toFixed(2)])}return out})()""")
    check('PNJ à >= 1,5 m des portes et libellés', all(m >= 1.5 for _, m in near), near)
    sizes = E("['foyer_in','bastide_in','moss_in','pointage_in'].map(k=>window.__nml.world.LOCATIONS[k].size)")
    check('4 intérieurs >= 10 x 8 m', all(z['w'] >= 10 and z['d'] >= 8 for z in sizes), sizes)
    for did in ['l_sud', 'l_sud_est', 'l_fosse']:
        E("window.__msgs=[]"); n0 = E(f"window.__nml.game.doorById('{did}').threshold"); walk(n0['x'], n0['z'] - 1.2, tol=1.0)
        E(f"window.__nml.game.useDoor('{did}')"); idle(); time.sleep(0.5)
        check(f'sortie {did} fermée', st()['location'] == 'steel_lower', st()['location'])
    cap('03_sud_sorties_fermees')
    talk('lt_dorn', '04_rue_des_fours_dorn'); talk('lt_pia', '05_allee_foyer_pia')
    for door, inn, nid in [('lt_foyer_door', 'foyer_in', 'lt_ruiz'), ('lt_bastide_door', 'bastide_in', 'lt_bastide'), ('lt_moss_door', 'moss_in', 'lt_moss'), ('lt_usine7_door', 'pointage_in', 'lt_raack')]:
        ok = enter_door(door); time.sleep(1.2); check(f'entrée {inn}', ok and st()['location'] == inn, st()['location'])
        talk(nid, f'06_{inn}')
        ok = enter_door(f'{inn}_door'); time.sleep(1.2); check(f'sortie {inn}', st()['location'] == 'steel_lower', st()['location'])
    # Fosse : clé (lot 4) simulée par drapeau, descente aux Poutres et remontée
    E("window.__nml.state.flags.lt_cle_ruiz=true")
    ok = enter_door('l_fosse'); time.sleep(1.2); check('Fosse : Lower-Town -> Sous-Ville (v_fosse)', ok and st()['location'] == 'sv_poutres', st()['location'])
    cap('07_poutres_v_fosse')
    E("window.__nml.state.flags.lt_cle_ruiz=false")
    ok = enter_door('v_fosse'); time.sleep(1.2); check('Fosse : Sous-Ville -> Lower-Town, ouverte depuis le bas', ok and st()['location'] == 'steel_lower' and st()['flags'].get('lt_fosse_ouverte'), (st()['location'], st()['flags'].get('lt_fosse_ouverte')))
    walk(24, 18); cap('08_rue_des_fours')
    ok = enter_door('l_ouest'); time.sleep(1.5)
    check('Lower-Town -> Center-Town (retour)', ok and st()['location'] == 'steel_center' and st()['player']['x'] > 44, (st()['location'], st()['player']['x']))
    # smoke Center-Town : patrouilleur, change de Teng
    ok = tap_npc('patrouilleur'); check('smoke Center-Town : patrouilleur parle', ok and 'Circulez' in dtext()); close_dlg()
    ok = enter_door('c_change_door'); check('smoke Center-Town : entrée chez Teng', ok and st()['location'] == 'change_in', st()['location'])
    check('aucune erreur JS / 404', not errs, errs[:3])
    br.close()
json.dump(R, open(OUT + 'results.json', 'w'), ensure_ascii=False, indent=1)
bad = [r for r in R if not r['ok']]; print(f'{len(R) - len(bad)}/{len(R)} OK'); sys.exit(1 if bad else 0)
