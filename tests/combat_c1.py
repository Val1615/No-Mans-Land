# Combat C1 (docs/design/COMBAT.md §14) : combat:rodeur depuis la scène du rôdeur, autosave avant, grille 1 m affichée seulement en combat, aperçu et coût (1 / 1,5 PA), tours, 4 issues ; desktop 1280x800 et mobile 390x844. Port dédié 8862.


import sys, os, time, io, json, base64, re
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8862/'); OUT = os.environ.get('OUT', '/tmp/nml-test-out/combat_c1/'); os.makedirs(OUT, exist_ok=True)
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
CAP = os.environ.get('CAP', '/tmp/nml-test-out/combat_c1/'); os.makedirs(CAP, exist_ok=True)
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
    C = "window.__nml.state.combat"
    def cst(): return E(f"{C} && JSON.parse(JSON.stringify({{phase:{C}.phase,tour:{C}.tour,actif:{C}.actif,units:{C}.units.map(u=>({{id:u.id,i:u.i,j:u.j,pa:u.pa,actif:u.actif,moving:u.path.length}})),preview:{C}.preview,zone:{C}.zone}}))")
    def my_turn(t=30): return waitjs(f"{C} && {C}.phase==='joueur' && {C}.units[{C}.actif].joueur && !{C}.units.some(u=>u.path.length)", t)
    def place(loc, x, z, flags, inv, hp=30, vol=None):
        E(f"""(()=>{{const g=window.__nml.game,s=g.snapshot();s.location='{loc}';s.player.x={x};s.player.z={z};s.player.hp={hp};s.player.inv={json.dumps(inv)};Object.assign(s.flags,{json.dumps(flags)});
          {'' if vol is None else f's.character.attrs.volonte={vol};'} g.restore(s,true)}})()"""); time.sleep(1.0)
    def cell_pt(i, j): return P(i + 0.5, 0, j + 0.5)
    def tap_cell(i, j): pt = cell_pt(i, j); gesture(pt['x'], pt['y']); time.sleep(0.35)
    def fresh(hp=30):  # combat neuf, par la vraie scène : rôdeur raté (Volonté 0, tirage forcé), « Ramasser les bidons. » -> combat:rodeur
        E(f"{C}=null"); d = E("window.__nml.game.doorById('j_q4_nord')"); t, o = d['threshold'], d['opening']; vx, vz = t['x'] - o['x'], t['z'] - o['z']; n = max(1e-6, np.hypot(vx, vz))
        place('dusk_q4', t['x'] + vx / n * 2.5, t['z'] + vz / n * 2.5, {'a_debut': True, 'a_rodeur_fait': False, 'a_fini': False}, {'bidon': 4}, hp=hp, vol=0)
        E("window.__q=[0,0,0,0];window.__nml.game.setRng(()=>window.__q.length?window.__q.shift():Math.random())")
        enter_door('j_q4_nord'); waitjs("window.__nml.state.dialogue && window.__nml.state.dialogue.npc==='rodeur'", 15)
        waitjs("[...document.querySelectorAll('#dlg-options button')].length>0", 8); option('Le regarder en face'); waitjs("window.__nml.state.dialogue && window.__nml.state.dialogue.node==='frappe'", 8)
        option('Ramasser'); return waitjs(f"!!{C}", 10) and my_turn()
    for prof in os.environ.get('PROFILES', 'desktop,mobile').split(','):
        mob = prof == 'mobile'
        if mob:
            br2 = br; ctx.close(); VW, VH = 390, 844; ctx = br.new_context(viewport={'width': VW, 'height': VH}, has_touch=True, is_mobile=True, device_scale_factor=2); pg = ctx.new_page(); errs2 = []
            pg.on('pageerror', lambda e: errs.append(str(e))); gesture = pg.touchscreen.tap; E = pg.evaluate; P = lambda x, y, z: E(f'window.__nml.project({x},{y},{z})')
            onscreen = lambda pt: 20 < pt['x'] < VW - 20 and 130 < pt['y'] < VH - 120
            pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=60000); time.sleep(1.5)
            E("import('./src/core/path.js').then(m => window.__findPath = m.findPath)")
            press('#m-new', 0.6); press('[data-race="augmente"]'); press('#cr-next', 0.5); press('#cr-enter', 1.2)
        T = prof
        E("localStorage.removeItem('nml_save_auto')")
        check(f'{T}: grille absente hors combat', E("!document.body.classList.contains('combat') && document.getElementById('cbt').hidden && !window.__nml.state.combat"))
        ok = fresh()
        check(f'{T}: combat:rodeur lancé par la scène (Ramasser les bidons.)', ok and E(f"{C}.id") == 'rodeur', cst())
        auto = E("(()=>{const r=localStorage.getItem('nml_save_auto');if(!r)return null;const o=JSON.parse(r);return {loc:o.state.location,combat:'combat' in o.state,hp:o.state.player.hp,flag:!!o.state.flags.combat_rodeur}})()")
        check(f'{T}: autosave écrite juste avant le combat (sans le combat en cours)', auto and auto['loc'] == 'dusk_q1' and not auto['combat'] and auto['flag'], auto)
        check(f'{T}: grille et interface de combat affichées', E("document.body.classList.contains('combat') && !document.getElementById('cbt').hidden"))
        time.sleep(0.8); cap(f'{T}-01_debut_combat')
        c = cst(); me = c['units'][[u['id'] for u in c['units']].index('joueur')]; i0, j0 = me['i'], me['j']
        costs = E(f"(()=>{{const g=window.__nml.game.combat,f=(i,j)=>{{const p=g.path(i,j);return p?p.pa:null}};return [f({i0}+1,{j0}),f({i0}+2,{j0}),f({i0}+1,{j0}+1),f({i0}+2,{j0}+2),f({i0}+3,{j0}+1)]}})()")
        check(f'{T}: coûts 1 case = 1 PA, 2 cases = 2, 1 diagonale = 2 (1,5 arrondi), 2 diagonales = 3, 2 droites + 1 diag = 4 (3,5 arrondi)', costs == [1, 2, 2, 3, 4], costs)
        pa0 = me['pa']; free2 = E(f"(()=>{{const g=window.__nml.game.combat;for(const [di,dj] of [[2,0],[-2,0],[0,2],[0,-2],[1,1],[-1,-1]])if(g.path({i0}+di,{j0}+dj))return [{i0}+di,{j0}+dj];return null}})()")
        tap_cell(*free2); pv = cst()['preview']
        check(f'{T}: premier tap = aperçu du chemin et de son coût (sans bouger)', pv and pv['i'] == free2[0] and pv['j'] == free2[1] and pv['ok'] and cst()['units'][0]['moving'] == 0 and E("document.querySelector('.cbt-cost') && !document.querySelector('.cbt-cost').hidden && document.querySelector('.cbt-cost').textContent"), (pv, E("document.querySelector('.cbt-cost')?.textContent")))
        cap(f'{T}-02_apercu_chemin')
        tap_cell(*free2); my_turn(10); me = [u for u in cst()['units'] if u['id'] == 'joueur'][0]
        check(f'{T}: second tap = déplacement, PA décomptés', (me['i'], me['j']) == tuple(free2) and me['pa'] == pa0 - pv['pa'], (me, pv['pa']))
        far = E(f"(()=>{{const g=window.__nml.game.combat,me=g.player();for(let d=12;d>6;d--)for(const [a,b] of [[d,0],[-d,0],[0,d],[0,-d]]){{const p=g.path(me.i+a,me.j+b);if(p&&p.pa>me.pa)return [me.i+a,me.j+b,p.pa]}}return null}})()")
        if far:
            tap_cell(far[0], far[1]); pv = cst()['preview']; tap_cell(far[0], far[1]); me2 = [u for u in cst()['units'] if u['id'] == 'joueur'][0]
            check(f'{T}: case trop loin : aperçu refusé, aucun déplacement', pv and not pv['ok'] and (me2['i'], me2['j']) == (me['i'], me['j']), (pv and pv['pa'], me2))
        press('#cbt-end', 0.3); ok = my_turn(40); c = cst()
        check(f'{T}: fin du tour -> tour du rôdeur -> retour au joueur (tour 2, PA rechargés)', ok and c['tour'] == 2 and [u for u in c['units'] if u['id'] == 'joueur'][0]['pa'] == E(f"{C}.units.find(u=>u.joueur).paMax"), c and (c['tour'], c['units']))
        cap(f'{T}-03_tour_2')
        mid = E("""(()=>{const W=innerWidth,H=innerHeight,q={l:W/3,r:2*W/3,t:H/3,b:2*H/3};return ['cbt-file','cbt-res','cbt-actions'].map(id=>{const r=document.getElementById(id).getBoundingClientRect();
          return [id, r.left<q.r&&r.right>q.l&&r.top<q.b&&r.bottom>q.t]})})()""")
        check(f'{T}: aucune interface de combat dans le tiers central', not any(x[1] for x in mid), mid)
        if mob:
            bs = E("[...document.querySelectorAll('#cbt-actions button')].map(b=>{const r=b.getBoundingClientRect();return [Math.round(r.width),Math.round(r.height)]})")
            check(f'{T}: boutons de combat >= 52 px', all(w >= 52 and h >= 52 for w, h in bs), bs)
        # issue 1 : victoire (le rôdeur panique et s'enfuit au tour 3)
        for _ in range(3):
            if not E(f"!!{C}"): break
            press('#cbt-end', 0.3); waitjs(f"!{C} || ({C}.phase==='joueur' && !{C}.units.some(u=>u.path.length))", 40)
        L = E("window.__nml.state.combatLast"); f = st()['flags']
        check(f'{T}: issue victoire (rôdeur en fuite au tour 3) : drapeau, retour à l\'exploration', L and L['issue'] == 'victoire' and f.get('combat_rodeur_victoire') and f.get('a_rodeur_fait') and not E(f"!!{C}") and E("!document.body.classList.contains('combat')"), (L, st()['player']['hp']))
        cap(f'{T}-04_victoire')
        # issue 2 : reddition (bouton « Se rendre », un bidon perdu)
        ok = fresh(); b0 = st()['player']['inv'].get('bidon', 0); press('#cbt-rendre', 0.6); L = E("window.__nml.state.combatLast")
        check(f'{T}: issue reddition : bouton Se rendre, un bidon perdu', ok and L['issue'] == 'reddition' and st()['flags'].get('combat_rodeur_reddition') and st()['player']['inv'].get('bidon', 0) == b0 - 1, (L, b0, st()['player']['inv']))
        # issue 3 : fuite (déplacements réels jusqu'à une case de bord de la zone)
        ok = fresh(); n = 0
        while E(f"!!{C}") and n < 8:
            n += 1; my_turn(40)
            tgt = E(f"(()=>{{const g=window.__nml.game.combat,c={C},z=c.zone;let best=null;for(const q of g.reachable()){{const d=Math.min(q.i-z.i0,z.i1-q.i,q.j-z.j0,z.j1-q.j);if(!best||d<best[2])best=[q.i,q.j,d]}}return best}})()")
            if tgt: tap_cell(tgt[0], tgt[1]); tap_cell(tgt[0], tgt[1]); waitjs(f"!{C} || !{C}.units.some(u=>u.path.length)", 15); time.sleep(0.3)
            if E(f"!!{C}") and E(f"{C}.phase==='joueur'"): press('#cbt-end', 0.3)
        L = E("window.__nml.state.combatLast")
        check(f'{T}: issue fuite : case de bord atteinte en marchant', L and L['issue'] == 'fuite' and st()['flags'].get('combat_rodeur_fuite'), (L, n))
        cap(f'{T}-05_fuite')
        # issue 4 : défaite (PV à 0 sous les coups fixes de C1) : jamais de mort, PV remis à 1, un bidon en moins
        ok = fresh(hp=8); n = 0
        while E(f"!!{C}") and n < 8: n += 1; my_turn(40); E(f"{C} && {C}.phase==='joueur'") and press('#cbt-end', 0.3); waitjs(f"!{C} || ({C}.phase==='joueur' && !{C}.units.some(u=>u.path.length))", 40)
        L = E("window.__nml.state.combatLast")
        check(f'{T}: issue défaite : PV 0 -> inconscient, PV remis à 1, pas d\'écran de fin', L and L['issue'] == 'defaite' and st()['player']['hp'] == 1 and st()['flags'].get('combat_rodeur_defaite'), (L, st()['player']['hp']))
        cap(f'{T}-06_defaite')
        check(f'{T}: aucune erreur JS / 404', not errs, errs[:3])
    br.close()
json.dump(R, open(OUT + 'results.json', 'w'), ensure_ascii=False, indent=1)
bad = [r for r in R if not r['ok']]; print(f'{len(R) - len(bad)}/{len(R)} OK'); sys.exit(1 if bad else 0)
