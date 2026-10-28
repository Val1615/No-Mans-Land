# Combat C2 (docs/design/COMBAT.md §6 à §8, §14) : attaques mêlée / pistolet / fusil, recharge, chance bornée 5-95 %, malus de portée, couverture 0/1/2, ligne de vue ;
# combat réel du rôdeur (scène), positions posées par le test ; desktop 1280x800 et mobile 390x844. Port dédié 8862.


import sys, os, time, io, json, base64, re
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8862/'); OUT = os.environ.get('OUT', '/tmp/nml-test-out/combat_c2/'); os.makedirs(OUT, exist_ok=True)
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
CAP = os.environ.get('CAP', '/tmp/nml-test-out/combat_c2/'); os.makedirs(CAP, exist_ok=True)
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
    def hover_or_tap(i, j):  # aperçu : survol à la souris (desktop) ou premier tap (mobile)
        pt = cell_pt(i, j)
        if mob: gesture(pt['x'], pt['y'])
        else: pg.mouse.move(pt['x'] + 3, pt['y'] + 2); pg.mouse.move(pt['x'], pt['y'])
        time.sleep(0.35)
    def confirm(i, j): pt = cell_pt(i, j); gesture(pt['x'], pt['y']); time.sleep(0.35)  # desktop : clic sur la case survolée ; mobile : second tap
    def tap_cell(i, j): hover_or_tap(i, j)
    def fresh(hp=30, inv=None):  # combat neuf, par la vraie scène : rôdeur raté (Volonté 0, tirage forcé), « Ramasser les bidons. » -> combat:rodeur
        E(f"{C}=null"); d = E("window.__nml.game.doorById('j_q4_nord')"); t, o = d['threshold'], d['opening']; vx, vz = t['x'] - o['x'], t['z'] - o['z']; n = max(1e-6, np.hypot(vx, vz))
        place('dusk_q4', t['x'] + vx / n * 2.5, t['z'] + vz / n * 2.5, {'a_debut': True, 'a_rodeur_fait': False, 'a_fini': False}, dict({'bidon': 4}, **(inv or {})), hp=hp, vol=0)
        E("window.__q=[0,0,0,0];window.__nml.game.setRng(()=>window.__q.length?window.__q.shift():Math.random())")
        enter_door('j_q4_nord'); waitjs("window.__nml.state.dialogue && window.__nml.state.dialogue.npc==='rodeur'", 15)
        waitjs("[...document.querySelectorAll('#dlg-options button')].length>0", 8); option('Le regarder en face'); waitjs("window.__nml.state.dialogue && window.__nml.state.dialogue.node==='frappe'", 8)
        r = option('Ramasser'); ok = waitjs(f"!!{C}", 10) and my_turn()
        if not ok: print('DIAG fresh', r, st()['dialogue'], st()['location'], E("JSON.stringify(window.__nml.state.log.slice(-6))"), flush=True)
        return ok

    def tp(uid, i, j): E(f"(()=>{{const u=window.__nml.game.combat.unit('{uid}');Object.assign(u,{{i:{i},j:{j},x:{i}+0.5,z:{j}+0.5,path:[]}});if(u.joueur)Object.assign(window.__nml.state.player,{{x:u.x,z:u.z}})}})()"); time.sleep(0.25)
    def ev(): return E("window.__nml.game.combat.evaluer('rodeur')")
    def unit(uid): return E(f"JSON.parse(JSON.stringify(window.__nml.game.combat.unit('{uid}')))")
    def rng(v): E(f"window.__nml.game.setRng(()=>{v})")
    def foe_pt(): u = unit('rodeur'); return P(u['x'], 0.9, u['z'])
    def hover_foe():
        pt = foe_pt()
        if mob: gesture(pt['x'], pt['y'])
        else: pg.mouse.move(pt['x'] + 3, pt['y'] + 2); pg.mouse.move(pt['x'], pt['y'])
        time.sleep(0.35)
    def click_foe(): pt = foe_pt(); gesture(pt['x'], pt['y']); time.sleep(0.4)
    def base(k='armes'): return E(f"window.__nml.state.character.skills.{k}")
    def label(): return E("(()=>{const e=document.querySelector('.cbt-cost');return e&&!e.hidden?e.textContent:null})()")
    for prof in os.environ.get('PROFILES', 'desktop,mobile').split(','):
        mob = prof == 'mobile'
        if mob:
            ctx.close(); VW, VH = 390, 844; ctx = br.new_context(viewport={'width': VW, 'height': VH}, has_touch=True, is_mobile=True, device_scale_factor=2); pg = ctx.new_page()
            pg.on('pageerror', lambda e: errs.append(str(e))); gesture = pg.touchscreen.tap; E = pg.evaluate; P = lambda x, y, z: E(f'window.__nml.project({x},{y},{z})')
            onscreen = lambda pt: 20 < pt['x'] < VW - 20 and 130 < pt['y'] < VH - 120
            pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=60000); time.sleep(1.5)
            E("import('./src/core/path.js').then(m => window.__findPath = m.findPath)")
            press('#m-new', 0.6); press('[data-race="augmente"]'); press('#cr-next', 0.5); press('#cr-enter', 1.2)
        T = prof
        # --- pistolet : arme prise dans le Sac, aperçu, tir, raté, recharge, chargeur vide
        ok = fresh(inv={'pistolet': 1})
        pl = unit('joueur'); check(f'{T}: combat lancé, pistolet du Sac équipé (chargeur 6/6)', ok and pl['arme'] == 'pistolet' and pl['charge'] == 6 and 'Pistolet 6/6' in (E("document.getElementById('cbt-info').textContent") or ''), (ok, pl.get('arme'), pl.get('charge')))
        # configurations de visée trouvées sur la vraie carte (zone du rôdeur, dusk_q1) : couverture 0, 1, 2 et vue coupée, à 8 m au plus (pas de malus de portée)
        cfg = E("""(()=>{const g=window.__nml.game.combat,c=window.__nml.state.combat,z=c.zone,res={},free=[];
          for(let i=z.i0+1;i<z.i1;i++)for(let j=z.j0+1;j<z.j1;j++)if(g.cellFree(i,j))free.push({i,j});
          for(const t of free){for(const s of free){const d=Math.hypot(s.i-t.i,s.j-t.j);if(d<2.5||d>8)continue;const v=g.visee(s,t),k=v.vue?String(v.couverture):'x';if(!res[k])res[k]=[s.i,s.j,t.i,t.j,Math.round(d*100)/100];}if(Object.keys(res).length>=4)break;}return res})()""")
        check(f'{T}: la carte offre les 4 cas de visée (couverture 0, 1, 2, vue coupée)', all(k in cfg for k in ['0', '1', '2', 'x']), cfg)
        b = base(); exp = {'0': 0, '1': 20, '2': 40}
        for k in ['0', '1', '2']:
            if k not in cfg: continue
            si, sj, ti, tj, d = cfg[k]; tp('joueur', si, sj); tp('rodeur', ti, tj); e = ev()
            check(f'{T}: couverture {k} : chance = Armes ({b}) - {exp[k]} %, bornée 5-95', e['couverture'] == int(k) and e['chance'] == max(5, min(95, round(b - exp[k]))) and e['ok'], e)
            if k == '1':
                hover_foe(); cap(f'{T}-02_couverture_1')
                check(f'{T}: aperçu d\'attaque : chance, PA et couverture affichés près de la cible', label() and f"{e['chance']} %" in label() and '3 PA' in label() and 'couvert 1' in label(), label())
        if 'x' in cfg:
            si, sj, ti, tj, d = cfg['x']; tp('joueur', si, sj); tp('rodeur', ti, tj); e = ev(); pa0 = unit('joueur')['pa']
            r = E("window.__nml.game.combat.attack('rodeur')")
            check(f'{T}: vue coupée par un bâtiment : tir impossible, aucun PA dépensé', not e['ok'] and e['raison'] == 'pas_de_ligne_de_vue' and not r['ok'] and unit('joueur')['pa'] == pa0, (e, r))
            hover_foe(); cap(f'{T}-03_vue_coupee')
        # bornes 5 / 95 (compétence forcée) et malus de portée
        si, sj, ti, tj, d = cfg['0']; tp('joueur', si, sj); tp('rodeur', ti, tj)
        E("window.__nml.state.character.skills.armes=250"); hi = ev(); E("window.__nml.state.character.skills.armes=-40"); lo = ev(); E(f"window.__nml.state.character.skills.armes={b}")
        check(f'{T}: chance bornée : 95 % au plus, 5 % au moins', hi['chance'] == 95 and hi['brut'] > 95 and lo['chance'] == 5 and lo['brut'] < 5, (hi['chance'], hi['brut'], lo['chance'], lo['brut']))
        far = E("""(()=>{const g=window.__nml.game.combat,c=window.__nml.state.combat,z=c.zone;let best=null;
          for(let i=z.i0+1;i<z.i1;i++)for(let j=z.j0+1;j<z.j1;j++)for(let a=z.i0+1;a<z.i1;a++)for(const b of [j]){if(!g.cellFree(i,j)||!g.cellFree(a,b))continue;const d=Math.abs(a-i);if(d<11)continue;const v=g.visee({i,j},{i:a,j:b});if(v.vue&&v.couverture===0&&(!best||d>best[4]))best=[i,j,a,b,d];}return best})()""")
        if far:
            tp('joueur', far[0], far[1]); tp('rodeur', far[2], far[3]); e = ev()
            check(f'{T}: malus de portée : − 4 % par mètre au-delà de 8 m (pistolet, {far[4]} m)', e['malPortee'] == 4 * (far[4] - 8) and e['chance'] == max(5, min(95, b - 4 * (far[4] - 8))), e)
        else: check(f'{T}: malus de portée : ligne dégagée de 11 m trouvée', False, far)
        # tir réel à l'interface : survol / premier tap = aperçu, clic / second tap = tir ; tirage forcé (touché, dégâts min 4)
        si, sj, ti, tj, d = cfg['0']; tp('joueur', si, sj); tp('rodeur', ti, tj); pv0 = unit('rodeur')['pv']; pa0 = unit('joueur')['pa']
        rng(0); hover_foe(); pre = E("JSON.parse(JSON.stringify(window.__nml.state.combat.preview))")
        check(f'{T}: survol / premier tap sur l\'ennemi = aperçu de l\'attaque, rien ne part', pre and pre.get('type') == 'attaque' and unit('rodeur')['pv'] == pv0 and unit('joueur')['charge'] == 6, pre)
        click_foe(); u = unit('rodeur'); me = unit('joueur'); last = E("JSON.parse(JSON.stringify(window.__nml.state.combat.dernier||null))")
        check(f'{T}: tir au pistolet : 3 PA, une balle, touché (tirage 0 < chance) : − 4 PV', last and last['touche'] and u['pv'] == pv0 - 4 and me['pa'] == pa0 - 3 and me['charge'] == 5, (last, u['pv'], me['pa'], me['charge']))
        cap(f'{T}-04_tir_touche')
        rng(0.99); r = E("window.__nml.game.combat.attack('rodeur')"); u2 = unit('rodeur')
        check(f'{T}: tir raté (tirage 99 >= chance) : PV inchangés, balle et PA dépensés', r['ok'] and not r['touche'] and u2['pv'] == u['pv'] and unit('joueur')['charge'] == 4, r)
        press('#cbt-recharger', 0.3); me = unit('joueur')
        check(f'{T}: bouton Recharger : 2 PA, chargeur plein', me['charge'] == 6 and me['pa'] == pa0 - 3 - 3 - 2, (me['charge'], me['pa'], pa0))
        cap(f'{T}-05_recharge')
        E("window.__nml.game.combat.unit('joueur').charge=0"); e = ev()
        check(f'{T}: chargeur vide : tir refusé', not e['ok'] and e['raison'] == 'chargeur_vide', e)
        # mort de l'ennemi = victoire
        E("(()=>{const c=window.__nml.game.combat,u=c.unit('joueur');u.charge=6;u.pa=u.paMax;c.unit('rodeur').pv=2})()"); rng(0); r = E("window.__nml.game.combat.attack('rodeur')"); L = E("window.__nml.state.combatLast")
        check(f'{T}: ennemi à 0 PV : hors de combat, issue victoire', r['ok'] and r['touche'] and L and L['issue'] == 'victoire' and not E(f"!!{C}"), (r.get('degats'), L))
        # --- fusil : 4 PA, portée utile 15 m
        ok = fresh(inv={'fusil': 1, 'pistolet': 1}); si, sj, ti, tj, d = cfg['0']; tp('joueur', si, sj); tp('rodeur', ti, tj); e = ev(); pa0 = unit('joueur')['pa']; rng(0)
        r = E("window.__nml.game.combat.attack('rodeur')")
        check(f'{T}: fusil (préféré au pistolet) : 4 PA par tir, dégâts min 6, chargeur 5', ok and e['arme'] == 'fusil' and e['pa'] == 4 and r['touche'] and r['degats'] == 6 and unit('joueur')['pa'] == pa0 - 4 and unit('joueur')['charge'] == 4, (e.get('arme'), r))
        if far:
            tp('joueur', far[0], far[1]); tp('rodeur', far[2], far[3]); e = ev()
            check(f'{T}: fusil à {far[4]} m : aucun malus de portée (portée utile 15 m)', e['malPortee'] == max(0, 4 * (far[4] - 15)), e)
        E("window.__nml.game.combat.finish('fuite')")
        # --- mêlée : barre de fer, au contact seulement, 3 PA, compétence Corps à corps, aucune couverture
        ok = fresh(inv={'barre': 1}); si, sj, ti, tj, d = cfg['1']; tp('joueur', si, sj); tp('rodeur', ti, tj); e = ev()
        check(f'{T}: mêlée hors de contact : refusée (au contact seulement)', ok and e['arme'] == 'barre' and not e['ok'] and e['raison'] == 'hors_portee', e)
        hover_foe(); check(f'{T}: aperçu mêlée hors de contact : « au contact »', label() == 'au contact', label())
        nb = E(f"(()=>{{const g=window.__nml.game.combat;for(const [a,b] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]])if(g.cellFree({ti}+a,{tj}+b))return [{ti}+a,{tj}+b];return null}})()")
        tp('joueur', *nb); e = ev(); m = base('melee'); pa0 = unit('joueur')['pa']; pv0 = unit('rodeur')['pv']; rng(0)
        hover_foe(); click_foe(); u = unit('rodeur')
        check(f'{T}: mêlée au contact : chance = Corps à corps ({m}), couverture ignorée, 3 PA, − 4 PV (barre, dégâts min)', e['ok'] and e['chance'] == max(5, min(95, m)) and e['couverture'] == 0 and unit('joueur')['pa'] == pa0 - 3 and u['pv'] == pv0 - 4, (e, u['pv']))
        cap(f'{T}-06_melee')
        # --- l'ennemi attaque à son tour (barre, tirage forcé) : − 4 PV au joueur
        hp0 = st()['player']['hp']; press('#cbt-end', 0.3); my_turn(40); hp1 = st()['player']['hp']
        check(f'{T}: tour du rôdeur au contact : il frappe (barre, − 4 PV par coup touché)', hp1 < hp0 and (hp0 - hp1) % 4 == 0, (hp0, hp1, E("window.__nml.state.combat && window.__nml.state.combat.dernier")))
        mid = E("""(()=>{const W=innerWidth,H=innerHeight,q={l:W/3,r:2*W/3,t:H/3,b:2*H/3};return ['cbt-file','cbt-res','cbt-actions'].map(id=>{const r=document.getElementById(id).getBoundingClientRect();return [id, r.left<q.r&&r.right>q.l&&r.top<q.b&&r.bottom>q.t]})})()""")
        check(f'{T}: aucune interface de combat dans le tiers central', not any(x[1] for x in mid), mid)
        if mob:
            bs = E("[...document.querySelectorAll('#cbt-actions button')].map(b=>{const r=b.getBoundingClientRect();return [Math.round(r.width),Math.round(r.height)]})")
            check(f'{T}: boutons de combat >= 52 px, 4 au plus', len(bs) <= 4 and all(w >= 52 and h >= 52 for w, h in bs), bs)
        E("window.__nml.state.combat && window.__nml.game.combat.finish('fuite')")
        check(f'{T}: aucune erreur JS / 404', not errs, errs[:3])
    br.close()
json.dump(R, open(OUT + 'results.json', 'w'), ensure_ascii=False, indent=1)
bad = [r for r in R if not r['ok']]; print(f'{len(R) - len(bad)}/{len(R)} OK'); sys.exit(1 if bad else 0)
