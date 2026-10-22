# v12 Steel-Megalopolis L1 : route depuis Dusk-Town, douane selon la race, Center-Town. Gestes réels (clic 1280x800, tap 390x844 dpr2), pixels rendus.
# Pour chaque profil, les 4 races : perso créé par l'écran de création (gestes), puis mise en place « porte d'acier forcée » (q_fin),
# placé au bout du Transit ; ensuite tout se fait au geste : jonction, douane, dialogues, portes, change, journal.
import sys, os, time, io, json, base64, re
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8765/'); OUT = os.environ.get('OUT', '/tmp/nml-test-out/steel_l1/'); os.makedirs(OUT, exist_ok=True)
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
REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../docs/captures/steel-l1-v12/live/')
def rgb_file(p): return np.asarray(Image.open(p).convert('RGB')).astype(int)
def centroid(u):
    a = png(u); m = MAG(a); ys, xs = np.nonzero(m); return (float(xs.mean()), float(ys.mean()), int(m.sum())) if len(xs) else (0, 0, 0)
RACES = os.environ.get('RACES', 'augmente,cyborg,humain,mutant').split(',')
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
        # --- mise en place : la porte d'acier est forcée (quête v9 testée ailleurs), on est au bout du Transit ---
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='dusk_q2';s.player.x=42;s.player.z=18;Object.assign(s.flags,{q_start:true,q_cric:true,q_signal:true,q_fin:true});g.restore(s,true)})()"); time.sleep(1.2)
        # 1. jonction à pied vers la route de Steel
        j = E("window.__nml.game.doorById('j_q2_est').threshold"); walk(j['x'], j['z'], tol=0.5)
        ok = waitjs("window.__nml.state.location==='steel_route'", 15); time.sleep(1.2)
        check(f'{T}: jonction à pied Transit -> route de Steel', ok, st()['location'])
        check(f'{T}: texte d\'arrivée (une journée de marche)', 'journée de marche' in E("document.getElementById('msg').textContent"))
        ROUTE_MOOD = mood(crop_hud(shot()))
        check(f'{T}: HUD : lieu, dollars hors de la ville', 'LA DOUANE' in E("document.getElementById('loc').textContent").upper() and E("document.getElementById('money').textContent").endswith('$'))
        for b in (['r_porte'] if mob else ['r_porte', 'r_douane']):  # mobile : vue étroite, le poste (à gauche) est mesuré dans la vue d'ensemble
            v = bvis(b); check(f'{T}: {b} rendu à l\'écran (pixels)', v[0] > 0.3 and v[1] > 4000 * dpr * dpr * 0.25, v)
        a = st(); check(f'{T}: autosave à l\'arrivée', E("JSON.parse(localStorage.getItem('nml_save_auto')).state.location") == 'steel_route')
        if race == 'augmente' and not mob: pg.screenshot(path=OUT + f'{prof}-01-route.png')
        if race == 'augmente':
            # v13 : disposition de la place forte, vue d'ensemble (caméra de contrôle), mesurée sur les pixels rendus
            ppm = 15 if not mob else 7.5
            E(f"window.__nml.view.setCamera({{x:24,z:18,ppm:{ppm}}})"); time.sleep(0.6)
            pg.screenshot(path=OUT + f'{prof}-02-place-forte.png')
            c0 = P(24, 0, 18); cx, cy_ = c0['x'] * dpr, c0['y'] * dpr
            gx, gy, gn = centroid(E("window.__nml.view.isolateBuilding('r_porte')")); px_, py_, pn = centroid(E("window.__nml.view.isolateBuilding('r_douane')"))
            check(f'{T}: porte du sarcophage en haut à droite de la place', gn > 0 and gx > cx and gy < cy_, (round(gx), round(gy), round(cx), round(cy_)))
            check(f'{T}: poste de douane à gauche', pn > 0 and px_ < cx - 0.25 * VW * dpr / 2, (round(px_), round(cx)))
            # la route mène à la porte : chemin marchable depuis l'arrivée jusqu'au pied de la porte, chaussée continue, et le bout de route tombe sur le sprite de la porte
            path = E("(()=>{const g=window.__nml.game; return window.__findPath(g.grids['steel_route'], {x:34,z:34}, {x:34,z:9})})()")
            W = E("window.__nml.game.world.LOCATIONS.steel_route")
            road = [z for z in W['ground']['zones'] if z['kind'] == 'asphalt' and z['x'] <= 34 <= z['x'] + z['w']]
            check(f'{T}: route reliée à la porte (chemin + chaussée continue)', path and len(path) > 2 and road and road[0]['z'] <= 8 and road[0]['z'] + road[0]['d'] >= 36, (len(path or []), road))
            end = P(34, 0.6, 8.0); gate = png(E("window.__nml.view.isolateBuilding('r_porte')"))
            ex, ey = int(end['x'] * dpr), int(end['y'] * dpr); win = gate[max(0, ey - 6):ey + 6, max(0, ex - 6):ex + 6]
            check(f'{T}: le bout de la route entre dans la porte (pixels du sprite)', MAG(win).mean() > 0.5, round(float(MAG(win).mean()), 2))
            dec = E("window.__nml.view.decor()")
            def seen(i):
                a = png(E(f'window.__nml.view.isolateDecor({i})')); return int(MAG(a).sum())
            sold = [d for d in dec if d['role'] == 'soldat']; queue = [d for d in dec if d['role'] == 'file']
            ns = sum(seen(d['i']) > 40 for d in sold) + 1  # + Halloran ; > 40 px d'écran = personnage effectivement rendu dans le champ
            nq = sum(seen(d['i']) > 40 for d in queue)
            check(f'{T}: beaucoup de soldats visibles (>= 10)', ns >= 10, ns)
            dz = E("window.__nml.game.doorById('r_douane_door').threshold")
            first = min(queue, key=lambda d: np.hypot(d['x'] - dz['x'], d['z'] - dz['z']))
            xs = sorted(d['x'] for d in queue); zs = [d['z'] for d in queue]
            check(f'{T}: file d\'attente visible devant le poste (>= 6, alignée)', nq >= 6 and np.hypot(first['x'] - dz['x'], first['z'] - dz['z']) < 3.5 and max(zs) - min(zs) < 1.0 and max(np.diff(xs)) < 1.6, (nq, first, round(max(zs) - min(zs), 2)))
            props = [p.get('sprite') for p in W['props']]
            cnt = {k: props.count(k) for k in ['st_mirador', 'st_tourelle', 'st_barricade', 'st_projecteur', 'sandbags']}
            check(f'{T}: fortifications (miradors, tourelles, barbelés, projecteurs, sacs)', cnt['st_mirador'] >= 3 and cnt['st_tourelle'] >= 3 and cnt['st_barricade'] >= 6 and cnt['st_projecteur'] >= 3 and cnt['sandbags'] >= 2, cnt)
            E("window.__nml.view.setCamera(null)"); time.sleep(0.5)
            check(f'{T}: nuit sur la place (fond et éclairage du lieu)', E("window.__nml.view.lightOf().bg") == '#0c0f18')
        if race == 'mutant':
            # 2m. attaqué à vue : le soldat interpelle dès qu'on approche (scène provisoire, crochet du futur combat)
            h = E("window.__nml.npcs.find(n=>n.id==='halloran')"); walk(h['x'] + 3, h['z'] + 5, tol=1.2)
            ok = waitjs("window.__nml.state.dialogue && window.__nml.state.dialogue.npc==='halloran'", 15)
            check(f'{T}: mutant repéré à vue par le soldat', ok and 'col' in dtext(), dtext() if ok else st()['player'])
            check(f'{T}: choix fuir / se rendre, pas de passage', opts()[:2] == ['Courir vers le désert.', 'Rester. Lever les mains.'], opts())
            pg.screenshot(path=OUT + f'{prof}-mutant-interpelle.png')
            hp0 = st()['player']['hp']
            if not mob:
                option('Courir vers le désert.'); s = st()
                check(f'{T}: fuite vers le désert : blessé, renvoyé loin de la douane', s['player']['hp'] == max(1, hp0 - 9) and s['player']['z'] > 30 and s['flags'].get('steel_fui'), (s['player']['hp'], s['player']['z']))
            else:
                option('Rester. Lever les mains.'); option('Ne pas résister.'); s = st()
                check(f'{T}: capture : blessé, jeté près de la trappe (Sous-Ville = L2)', s['player']['hp'] == max(1, hp0 - 15) and s['flags'].get('steel_capture') and s['player']['x'] > 38, (s['player']['hp'], s['player']['x']))
                check(f'{T}: texte de capture sans mécanique', 'Sous-Ville' in dtext())
            check(f'{T}: crochet combat signalé (hook douane_mutant)', 'douane_mutant' in (st().get('hooks') or []))
            close_dlg(); time.sleep(0.4)
            r = E("window.__nml.game.useDoor('r_douane_door')"); check(f'{T}: la porte de la douane reste interdite', r and r.get('ok') is False and r.get('reason') == 'mutant', (r, st()['location'], st()['player']))
            pg.screenshot(path=OUT + f'{prof}-mutant-apres.png')
        else:
            # 2. douane : entrer par la porte peinte, parler à Odile au geste
            ok = enter_door('r_douane_door'); check(f'{T}: entrée dans le poste de douane', ok and st()['location'] == 'douane_in', st()['location'])
            check(f'{T}: lieu « Douane » repéré, nommé dehors ensuite', st()['discovered'].get('r_douane'))
            if race == 'augmente':
                # v13 : intérieur cohérent avec l'extérieur (IO) : mobilier io_*, murs/sol IO, porte IO ; palette froide, aucun ton sable
                L = E("window.__nml.game.world.LOCATIONS.douane_in"); fur = [p['furn'] for p in L['props']]
                check(f'{T}: intérieur douane : mobilier IO seulement (>= 5, dont scanner)', all(f.startswith('io_') for f in fur) and len(fur) >= 5 and 'io_scanner' in fur, fur)
                check(f'{T}: intérieur douane : murs, sol et porte IO', L['wallSkin'] == 'w_io_dark' and L['ground']['skin'].startswith('f_io') and L['doorSkin'] == 'door_io')
                time.sleep(0.6); a = png(E("window.__nml.view.envShot()")); v, sat = hsv(a); r_, g_, b_ = a[..., 0], a[..., 1], a[..., 2]
                lit = v > 0.15; warm = lit & (r_ - b_ > 35) & (g_ - b_ > 15); cool = lit & (b_ >= r_)
                check(f'{T}: intérieur douane : palette froide, pas de sable (pixels)', warm.sum() / max(1, lit.sum()) < 0.08 and cool.sum() / max(1, lit.sum()) > 0.5, (round(float(warm.sum() / max(1, lit.sum())), 3), round(float(cool.sum() / max(1, lit.sum())), 3)))
                vis = 0
                for k in range(E("window.__nml.view.furnCount()")):
                    vis += MAG(png(E(f'window.__nml.view.isolateFurn({k})'))).sum() > 400 * dpr * dpr
                check(f'{T}: intérieur douane : chaque meuble IO rendu à l\'écran', vis == len(fur), (vis, len(fur)))
                pg.screenshot(path=OUT + f'{prof}-03-douane-interieur.png')
            check(f'{T}: Odile parle par geste', tap_npc('odile') and 'Motif' in dtext())
            option('Entrer. Je cherche du travail.')
            if race in ('augmente', 'cyborg'):
                check(f'{T}: implant lu, passage accordé', 'Implant lu' in dtext(), dtext()[:60])
                pg.screenshot(path=OUT + f'{prof}-{race}-douane.png')
                option('Merci.'); close_dlg()
                check(f'{T}: drapeau steel_passe', st()['flags'].get('steel_passe'))
                tap_npc('odile'); m0 = st()['player']['money']; option('Changer des dollars'); s = st()
                check(f'{T}: change à la douane 20 $ -> 11 cr', s['player']['money'] == m0 - 20 and s['player']['credits'] == 11, (s['player']['money'], s['player']['credits']))
                close_dlg()
                ok = enter_door('douane_in_est'); time.sleep(1.5); s = st()
                check(f'{T}: barrière franchie -> Center-Town', ok and s['location'] == 'steel_center', s['location'])
                check(f'{T}: quête : arrivé en ville (q_steel)', s['flags'].get('q_steel'))
                check(f'{T}: HUD en crédits dans Steel', E("document.getElementById('money').textContent") == '11 cr' and E("document.getElementById('money-lbl').textContent") == 'Crédits')
                lbl = lambda b: E(f"(()=>{{const e=document.querySelector('.wlabel[data-building=\"{b}\"]');return !!e && !e.hidden && getComputedStyle(e).display!=='none'}})()")
                check(f'{T}: services non nommés avant découverte', not lbl('c_change') and not lbl('c_arcadius'))
                pg.screenshot(path=OUT + f'{prof}-{race}-center.png')
                if race == 'augmente':
                    # v13 : Center-Town vivant, mesuré sur les pixels : saturation, néons, zones éclairées, contre la v12 et contre l'approche
                    time.sleep(0.5); M = mood(crop_hud(shot())); ref = REF + f'{prof}-augmente-center.png'  # écran réel, à l'arrivée (même cadrage que la capture v12)
                    R12 = mood(crop_hud(rgb_file(ref))) if os.path.exists(ref) else None
                    check(f'{T}: Center-Town : saturation et néons nettement supérieurs à la v12', R12 and M['sat'] > 1.4 * R12['sat'] and M['neon'] > 2 * max(R12['neon'], 0.002), (M, R12))
                    check(f'{T}: Center-Town : lumières (p95) et néons nettement au-dessus de l\'approche', M['v95'] > 1.3 * ROUTE_MOOD['v95'] and M['neon'] > 3 * max(ROUTE_MOOD['neon'], 0.002) and M['sat'] > 1.1 * ROUTE_MOOD['sat'], (M, ROUTE_MOOD))
                    check(f'{T}: Center-Town : sol mouillé, nuit', E("window.__nml.game.world.LOCATIONS.steel_center.ground.skin") == 'g_wet' and E("window.__nml.view.lightOf().bg") == '#0b0a16')
                    d0 = {d['i']: d for d in E("window.__nml.view.decor()")}; time.sleep(1.2); d1 = E("window.__nml.view.decor()")
                    moved = [d for d in d1 if d['role'] == 'passant' and np.hypot(d['x'] - d0[d['i']]['x'], d['z'] - d0[d['i']]['z']) > 0.4]
                    drones = [d for d in d1 if d['role'] == 'drone' and np.hypot(d['x'] - d0[d['i']]['x'], d['z'] - d0[d['i']]['z']) > 0.1]
                    check(f'{T}: passants qui marchent (>= 5) et drones en vol (>= 3)', len(moved) >= 5 and len(drones) >= 3, (len(moved), len(drones)))
                    ok_f, sides = 0, set()
                    for d in d1:
                        if d['role'] != 'passant': continue
                        a0 = d0[d['i']]; sr = E(f"window.__nml.view.screenRightOf({d['x'] - a0['x']},{d['z'] - a0['z']})")
                        if abs(sr) > 0.2: ok_f += (sr > 0) == (d['facing'] > 0); sides.add(d['facing'])
                    check(f'{T}: passants tournés dans leur sens de marche (miroir), dans les deux sens', ok_f >= 4 and sides == {1, -1}, (ok_f, sides))
                    W = E("window.__nml.game.world.LOCATIONS.steel_center"); sp = [p.get('sprite') for p in W['props']]
                    check(f'{T}: échoppes, hologrammes, lampadaires néon, reflets au sol', sp.count('st_echoppe') >= 2 and sp.count('st_holo') >= 3 and sp.count('st_lampadaire') >= 4 and len(W['glows']) >= 10, (sp.count('st_echoppe'), sp.count('st_holo'), len(W['glows'])))
                    fps = E("new Promise(r=>{let n=0;const t=performance.now();(function f(){n++;if(performance.now()-t<2000)requestAnimationFrame(f);else r(n/2)})()})")
                    check(f'{T}: perf Center-Town (rendu logiciel SwiftShader) >= 8 i/s', fps >= 8, fps)
                    if not mob:  # vue comparable au concept art : la rotonde, la rue mouillée, les néons
                        E("window.__nml.view.setCamera({x:24,z:13.5,ppm:38})"); time.sleep(0.8); pg.screenshot(path=OUT + 'desktop-04-vue-concept.png')
                        C = mood(crop_hud(shot())); A = mood(rgb_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../docs/villes/steel/ambiance/concept_center_town.jpg')))
                        check(f'{T}: vue concept : ambiance proche du concept art (néons et saturation du même ordre)', 0.5 * A['sat'] < C['sat'] < 2.2 * A['sat'] and C['neon'] > 0.3 * A['neon'], (C, A))
                        E("window.__nml.view.setCamera(null)"); time.sleep(0.5)
                # PNJ animé / miroir : le patrouilleur regarde l'avenue, puis se tourne vers le joueur
                n = E("window.__nml.npcs.find(n=>n.id==='patrouilleur')"); walk(n['x'] + 1.8, n['z'] + 0.6, tol=1.2); time.sleep(0.5)
                f0 = E("window.__nml.view.facingOf('patrouilleur')"); V0 = png(E("window.__nml.view.isolate('patrouilleur')"))
                check(f'{T}: patrouilleur parle par geste', tap_npc('patrouilleur')); time.sleep(0.8)
                f1 = E("window.__nml.view.facingOf('patrouilleur')"); V1 = png(E("window.__nml.view.isolate('patrouilleur')"))
                same, mir = aligned(V0, V1); check(f'{T}: patrouilleur tourné vers le joueur, image en miroir', f0 != f1 and mir < 0.6 * same, (f0, f1, same, mir))
                option('Il y a un change'); check(f'{T}: le change est repéré par la conversation', st()['discovered'].get('c_change')); close_dlg(); time.sleep(0.6)
                check(f'{T}: « Change de Teng » nommé une fois repéré', lbl('c_change'))
                d = E("window.__nml.game.doorById('c_change_door').threshold"); walk(d['x'], d['z'] + 1.5, tol=1.0); time.sleep(0.5)
                v = bvis('c_change'); check(f'{T}: c_change rendu devant le joueur (pixels)', v[0] > 0.25 and v[1] > 500 * dpr * dpr, v)
                ok = enter_door('c_change_door'); check(f'{T}: entrée chez Teng', ok and st()['location'] == 'change_in')
                check(f'{T}: Teng parle par geste', tap_npc('teng')); m0 = st()['player']['money']; option('Changer 10'); s = st()
                check(f'{T}: change chez Teng 10 $ -> 6 cr', s['player']['money'] == m0 - 10 and s['player']['credits'] == 17, (s['player']['money'], s['player']['credits']))
                option('Autre chose.'); option('Ce bâtiment de verre'); check(f'{T}: Arcadius repéré par Teng', st()['discovered'].get('c_arcadius'))
                pg.screenshot(path=OUT + f'{prof}-{race}-teng.png'); close_dlg()
                enter_door('change_in_door'); time.sleep(1)
                for b in ['c_arcadius', 'c_neon', 'c_tour']:
                    v = bvis(b); check(f'{T}: {b} rendu (pixels, si dans le champ)', v[1] == 0 and (mob or b != 'c_arcadius') or v[0] > 0.25, v)
                check(f'{T}: Arcadius Center nommé dehors', st()['location'] == 'steel_center' and lbl('c_arcadius'))
                h = journal(); check(f'{T}: journal : arrivé à Steel, la suite attend', 'Arrivé à Steel-Megalopolis' in h, h[-160:])
            else:  # humain
                check(f'{T}: humain refusé (pas d\'implant)', 'Pas d\u2019implant' in dtext() and st()['flags'].get('steel_refuse'), dtext()[:60])
                pg.screenshot(path=OUT + f'{prof}-humain-refuse.png'); close_dlg()
                r = E("window.__nml.game.useDoor('douane_in_est')"); check(f'{T}: barrière refusée', r and r['ok'] is False and r['reason'] == 'douane', r)
        if race in ('humain', 'mutant'):
            # 3. Dusk-Town : Sol oriente vers la Sous-Ville, Bruno donne le nom (provisoire) de son frère
            h = journal(); check(f'{T}: journal : demander à Sol', 'Sol' in h, h[-150:])
            E("(()=>{const g=window.__nml.game,s=g.snapshot(),d=g.doorById('citerne_in_door');s.location='citerne_in';s.player.x=d.threshold.x-0.6;s.player.z=d.threshold.z;g.restore(s,true)})()"); time.sleep(1)
            check(f'{T}: Sol parle par geste', tap_npc('sol'))
            lab = "Steel. Ils m'ont refoulé" if race == 'humain' else "Steel. Ils m'ont tiré dessus"
            check(f'{T}: option Steel chez Sol', option(lab), opts()); check(f'{T}: Sol indique une autre porte et Bruno', 'Bruno' in dtext() and 'sable' in dtext())
            option('Merci, Sol.'); check(f'{T}: trappe repérée, drapeau sol_passage', st()['flags'].get('sol_passage') and st()['discovered'].get('r_service'))
            E("(()=>{const g=window.__nml.game,s=g.snapshot(),d=g.doorById('mara_in_door')||window.__nml.doors.find(d=>d.location==='mara_in');s.location='mara_in';s.player.x=d.threshold.x;s.player.z=d.threshold.z-0.6;g.restore(s,true)})()"); time.sleep(1)
            check(f'{T}: Bruno parle par geste', tap_npc('bruno')); option('Sol m'); t = dtext()
            check(f'{T}: Bruno donne le nom de son frère (Elio, provisoire) et un mot', 'Elio' in t and 'quatorze poutres' in t, t[:80]); option('Quatorze poutres'); close_dlg()
            h = journal(); check(f'{T}: journal : Elio, Sous-Ville au prochain lot', 'Elio' in h and 'prochain lot' in h, h[-200:])
            pg.screenshot(path=OUT + f'{prof}-{race}-journal.png')
        check(f'{T}: aucune erreur console / réseau', not errs, errs[:3])
        ctx.close()
    br.close()
ok = sum(r['ok'] for r in R); print(f'{ok}/{len(R)}'); json.dump(R, open(OUT + 'resultats.json', 'w'), ensure_ascii=False, indent=1); sys.exit(0 if ok == len(R) else 1)
