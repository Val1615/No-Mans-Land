# v14 Steel-Megalopolis L2 : la Sous-Ville. Parcours complet humain (refoulé) et mutant (desktop : fuite ; mobile : capture),
# de Dusk-Town (bout du Transit) à Center-Town par la trappe, les Poutres, la Cuve, l'atelier d'Elio et le monte-charge.
# Gestes réels (clic 1280x800, tap 390x844 dpr2), pixels rendus. Les allers-retours vers Sol et Bruno (Dusk-Town) sont posés par restore, comme steel_l1.
import sys, os, time, io, json, base64, re
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8765/'); OUT = os.environ.get('OUT', '/tmp/nml-test-out/steel_l2/'); os.makedirs(OUT, exist_ok=True)
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
RACES = os.environ.get('RACES', 'humain,mutant').split(',')
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for prof in os.environ.get('PROFILES', 'desktop,mobile').split(','):
      mob = prof == 'mobile'; dpr = 2 if mob else 1; VW, VH = (390, 844) if mob else (1280, 800)
      for race in RACES:
        T = f'{prof}/{race}'
        ctx = br.new_context(viewport={'width': VW, 'height': VH}, has_touch=True, is_mobile=True, device_scale_factor=2) if mob else br.new_context(viewport={'width': VW, 'height': VH})
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('response', lambda r: r.status >= 400 and errs.append(f'{r.status} {r.url}'))
        gesture = pg.touchscreen.tap if mob else pg.mouse.click
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
            b = loc.first.bounding_box(); gesture(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2); time.sleep(0.5); return True
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
        def journal():
            press('#k-journal', 0.5); h = E("document.getElementById('panel-body').innerText"); press('#panel-close', 0.3); return h
        # --- création : race choisie au geste ---
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=60000); time.sleep(1.5)
        E("import('./src/core/path.js').then(m => window.__findPath = m.findPath)")
        press('#m-new', 0.6); press(f'[data-race="{race}"]'); press('#cr-next', 0.5); press('#cr-enter', 1.2)
        c = st()['character']; check(f'{T}: perso créé ({race})', c and c['race'] == race and not E('document.body.classList.contains("menu-open")'))
        lbl = lambda b: E(f"(()=>{{const e=document.querySelector('.wlabel[data-building=\"{b}\"]');return !!e && !e.hidden && getComputedStyle(e).display!=='none'}})()")
        def warm(a):  # part de pixels éclairés chauds (orange) et rapport R/B des pixels visibles
            v, sat = hsv(a); r, g, b = a[..., 0], a[..., 1], a[..., 2]; lit = v > 0.25
            return {'warm': round(float(((r > g) & (g > b) & (sat > 0.35) & lit).mean()), 3), 'rb': round(float(r[lit].mean() / max(1, b[lit].mean())), 2), 'neon': mood(a)['neon']}
        E("(()=>{window.__msgs=[];const m=document.getElementById('msg');new MutationObserver(()=>window.__msgs.push(m.textContent)).observe(m,{childList:true,characterData:true,subtree:true})})()")
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='dusk_q2';s.player.x=42;s.player.z=18;Object.assign(s.flags,{q_start:true,q_cric:true,q_signal:true,q_fin:true});g.restore(s,true)})()"); time.sleep(1.2)
        j = E("window.__nml.game.doorById('j_q2_est').threshold"); walk(j['x'], j['z'], tol=0.5)
        # lot 3 interface : la route des patrouilles ouvre la carte des No Man's Land (Steel proposé) ; « Partir », voyage case par case
        check(f'{T}: carte NML ouverte à la sortie, Steel proposé', waitjs("!document.getElementById('nml').hidden && window.__nml.voyage.region().dest?.lieu==='steel'", 15)); press('#nml-partir', 0.3)
        check(f'{T}: Dusk-Town -> route de Steel à pied', waitjs("window.__nml.state.location==='steel_route'", 25)); time.sleep(1)
        r = E("window.__nml.game.useDoor('r_trappe')"); check(f'{T}: trappe fermée tant qu\'on ne connaît personne', r and r['ok'] is False and r['reason'] == 'trappe', r)
        capt = race == 'mutant' and mob
        if race == 'humain':
            enter_door('r_douane_door'); tap_npc('odile'); option('Entrer. Je cherche du travail.')
            check(f'{T}: refoulé à la douane', st()['flags'].get('steel_refuse')); close_dlg(); enter_door('douane_in_sud'); time.sleep(0.8)
        else:
            h = E("window.__nml.npcs.find(n=>n.id==='halloran')"); walk(h['x'] + 3, h['z'] + 5, tol=1.2)
            check(f'{T}: interpellé par le soldat', waitjs("window.__nml.state.dialogue && window.__nml.state.dialogue.npc==='halloran'", 15))
            if capt:
                hp0 = st()['player']['hp']; option('Rester. Lever les mains.'); option('Ne pas résister.'); s = st()
                check(f'{T}: capturé, jeté dans la Sous-Ville (crochet douane_mutant)', s['location'] == 'sv_poutres' and s['flags'].get('sv_jete') and 'douane_mutant' in (s.get('hooks') or []) and s['player']['hp'] == max(1, hp0 - 15), (s['location'], s['player']['hp']))
                close_dlg(); time.sleep(0.6)
                hj = journal(); check(f'{T}: journal : trouver Elio (sans passer par Sol)', 'Elio' in hj, hj[-160:])
            else:
                option('Courir vers le désert.'); close_dlg(); check(f'{T}: fuite (steel_fui)', st()['flags'].get('steel_fui'))
        if not capt:  # Sol puis Bruno, à Dusk-Town, au geste
            E("(()=>{const g=window.__nml.game,s=g.snapshot(),d=g.doorById('citerne_in_door');s.location='citerne_in';s.player.x=d.threshold.x-0.6;s.player.z=d.threshold.z;g.restore(s,true)})()"); time.sleep(1)
            tap_npc('sol'); option("Steel. Ils m'ont refoulé" if race == 'humain' else "Steel. Ils m'ont tiré dessus"); option('Merci, Sol.'); close_dlg()
            E("(()=>{const g=window.__nml.game,s=g.snapshot(),d=window.__nml.doors.find(d=>d.location==='mara_in');s.location='mara_in';s.player.x=d.threshold.x;s.player.z=d.threshold.z-0.6;g.restore(s,true)})()"); time.sleep(1)
            tap_npc('bruno'); option('Sol m'); option('Quatorze poutres'); close_dlg()
            check(f'{T}: Sol puis Bruno : le nom et le mot', st()['flags'].get('sol_passage') and st()['flags'].get('bruno_frere'))
            hj = journal(); check(f'{T}: journal : trouver Elio, plus de « prochain lot »', 'Trouver Elio' in hj and 'prochain lot' not in hj, hj[-160:])
            E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_route';s.player.x=38;s.player.z=34.4;g.restore(s,true)})()"); time.sleep(1)
            check(f'{T}: trappe nommée (Sortie de service)', lbl('r_service'))
            ok = enter_door('r_trappe'); time.sleep(1.2)
            check(f'{T}: trappe ouverte -> Sous-Ville (les Poutres)', ok and st()['location'] == 'sv_poutres', st()['location'])
            check(f'{T}: texte d\'arrivée en bas', waitjs("window.__msgs.some(t=>t.includes('tôle chaude'))", 6))
        # --- Les Poutres ---
        check(f'{T}: HUD : Sous-Ville, dollars', 'SOUS-VILLE' in E("document.getElementById('loc').textContent").upper() and E("document.getElementById('money').textContent").endswith('$'))
        check(f'{T}: lumière chaude des braseros (fond)', E("window.__nml.view.lightOf().bg") == '#0e0805')
        W = warm(crop_hud(shot())); check(f'{T}: ambiance orange chaude (pixels)', W['warm'] > 0.07 and W['rb'] > 1.4 and W['neon'] < 0.01, W)
        r = E("window.__nml.game.useDoor('v_est')"); check(f'{T}: passage vers la Cuve gardé sans le mot', r and r['ok'] is False and r['reason'] == 'guet', r)
        check(f'{T}: tripot non nommé avant découverte', not lbl('v_tripot'))
        n = E("window.__nml.npcs.find(n=>n.id==='guetteuse')"); walk(n['x'] + 2, n['z'] + 0.6, tol=1.0); time.sleep(0.4)
        f0 = E("window.__nml.view.facingOf('guetteuse')"); V0 = png(E("window.__nml.view.isolate('guetteuse')"))
        check(f'{T}: la guetteuse parle par geste', tap_npc('guetteuse')); time.sleep(0.8)
        f1 = E("window.__nml.view.facingOf('guetteuse')"); V1 = png(E("window.__nml.view.isolate('guetteuse')"))
        same, mir = aligned(V0, V1); check(f'{T}: guetteuse tournée vers le joueur (miroir, pixels)', f0 != f1 and mir < 0.6 * same, (f0, f1, same, mir))
        lab = 'Et maintenant' if capt else 'Quatorze poutres.'
        check(f'{T}: option « {lab} »', option(lab), opts()); t = dtext()
        check(f'{T}: la guetteuse envoie à la Cuve, chez Elio', 'Elio' in t and 'Cuve' in t, t[:80])
        if not mob: pg.screenshot(path=OUT + f'{prof}-{race}-guetteuse.png')
        close_dlg(); time.sleep(0.5); check(f'{T}: « Le Tripot » nommé une fois repéré', lbl('v_tripot'))
        if race == 'humain':  # le tripot : intérieur, dealer
            d = E("window.__nml.game.doorById('v_tripot_door').threshold"); walk(d['x'], d['z'] + 1.5, tol=1.0); time.sleep(0.4)
            v = bvis('v_tripot'); check(f'{T}: tripot rendu (pixels)', v[0] > 0.3 and v[1] > 1500 * dpr * dpr, v)
            o = E("window.__nml.game.doorById('v_tripot_door').opening"); pt = P(o['x'], 1.0, o['z']); iso = png(E("window.__nml.view.isolateBuilding('v_tripot')"))
            ex, ey = int(pt['x'] * dpr), int(pt['y'] * dpr); win = iso[max(0, ey - 6):ey + 6, max(0, ex - 6):ex + 6]
            check(f'{T}: porte du tripot sur le sprite (pixels)', MAG(win).mean() > 0.5, round(float(MAG(win).mean()), 2))
            check(f'{T}: entrée au tripot', enter_door('v_tripot_door') and st()['location'] == 'tripot_in')
            check(f'{T}: le dealer parle par geste', tap_npc('dealer'))
            check(f'{T}: trafic (puces, yeux de nuit)', 'œil' in dtext() or 'puce' in dtext(), dtext()[:60])
            if not mob: pg.screenshot(path=OUT + f'{prof}-tripot.png')
            close_dlg(); m = E("window.__nml.view.furnCount ? window.__nml.view.furnCount() : -1"); check(f'{T}: mobilier du tripot rendu', m != 0, m)
            enter_door('tripot_in_door'); time.sleep(0.8)
        if race == 'humain' and not mob:
            dec = E("window.__nml.view.decor()"); roles = {d['role'] for d in dec}
            check(f'{T}: figurants : gang, guetteur, et des marcheurs (gang, dealer)', {'gang', 'guetteur'} <= roles and sum(d['role'] == 'passant' for d in dec) >= 2, roles)
            E("window.__nml.view.setCamera({x:19,z:12,ppm:42})"); time.sleep(0.8); pg.screenshot(path=OUT + 'desktop-04-vue-concept.png')
            C = warm(crop_hud(shot())); A = warm(rgb_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../docs/villes/steel/ambiance/concept_sous_ville.jpg')))
            check(f'{T}: vue concept : ambiance proche du concept art (orange chaud, sans néon froid)', C['warm'] > 0.4 * A['warm'] and C['rb'] > 0.6 * A['rb'], (C, A))
            E("window.__nml.view.setCamera(null)"); time.sleep(0.5)
        ok = enter_door('v_est'); time.sleep(1); check(f'{T}: jonction à pied -> la Cuve', ok and st()['location'] == 'sv_cuve', st()['location'])
        # --- La Cuve ---
        r = E("window.__nml.game.useDoor('v_lift_door')"); check(f'{T}: monte-charge refusé sans Elio', r and r['ok'] is False and r['reason'] == 'lift', r)
        d = E("window.__nml.game.doorById('v_atelier_door').threshold"); walk(d['x'], d['z'] + 1.5, tol=1.0); time.sleep(0.4)
        v = bvis('v_atelier'); check(f'{T}: atelier d\'Elio rendu (pixels)', v[0] > 0.3 and v[1] > 1000 * dpr * dpr, v)
        if not mob: pg.screenshot(path=OUT + f'{prof}-{race}-cuve.png')
        check(f'{T}: entrée chez Elio', enter_door('v_atelier_door') and st()['location'] == 'elio_in')
        check(f'{T}: Elio parle par geste', tap_npc('elio')); option('Il faut que je monte'); t = dtext()
        check(f'{T}: Elio : un prix (20 $)', 'Vingt dollars' in t, t[:80])
        s0 = st()['player']
        if race == 'humain':
            option('Payer 20'); s = st()['player']; check(f'{T}: payé 20 $', s['money'] == s0['money'] - 20, (s0['money'], s['money']))
        else:
            option('Je n'); option('Porter la caisse.'); s = st()['player']; check(f'{T}: le risque : blessé (-6 PV)', s['hp'] == max(1, s0['hp'] - 6), (s0['hp'], s['hp']))
        check(f'{T}: passage accordé, monte-charge repéré', st()['flags'].get('sv_passage') and st()['discovered'].get('v_lift'))
        if not mob: pg.screenshot(path=OUT + f'{prof}-{race}-elio.png')
        close_dlg(); hj = journal(); check(f'{T}: journal : remonter par le monte-charge', 'monte-charge' in hj, hj[-160:])
        enter_door('elio_in_door'); time.sleep(0.8)
        v = bvis('v_lift'); check(f'{T}: monte-charge rendu (pixels, si dans le champ)', v[1] == 0 or v[0] > 0.25, v)
        ok = enter_door('v_lift_door'); time.sleep(1.5); s = st()
        check(f'{T}: monte-charge -> Center-Town (entre deux galeries)', ok and s['location'] == 'steel_center' and abs(s['player']['x'] - 19.5) < 2, (s['location'], s['player']['x'], s['player']['z']))
        check(f'{T}: quête terminée : arrivé à Steel (q_steel)', s['flags'].get('q_steel'))
        hj = journal(); check(f'{T}: journal : arrivé, la suite attend', 'Arrivé à Steel-Megalopolis' in hj, hj[-120:])
        pg.screenshot(path=OUT + f'{prof}-{race}-center.png')
        check(f'{T}: aucune erreur console / réseau', not errs, errs[:3])
        ctx.close()
    br.close()
ok = sum(r['ok'] for r in R); print(f'{ok}/{len(R)}'); json.dump(R, open(OUT + 'resultats.json', 'w'), ensure_ascii=False, indent=1); sys.exit(0 if ok == len(R) else 1)
