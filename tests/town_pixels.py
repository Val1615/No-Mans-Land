# v7 : recette de la ville entière (4 quartiers) AU PIXEL et par GESTES RÉELS. Chrome headless, WebGL logiciel.
# Chaque jonction est franchie dans les deux sens par une vraie marche (clics souris 1280x800 / taps 390x844 sur le sol),
# jamais par téléportation. Contrôles visuels : capture d'écran comparée au rendu isolé (même pipeline) du bâtiment,
# du joueur et de Nilo. État conservé entre quartiers : argent, PV, lieux découverts (vérifiés dans le HUD et les étiquettes).
import sys, os, time, io, base64, json
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8765/'); OUT = os.environ.get('OUT', '/workspace/nml/docs/captures/dusk-v7/'); os.makedirs(OUT, exist_ok=True)
GIF = os.environ.get('GIF', '1') == '1'
R = []
def check(n, ok, d=''): R.append({'test': n, 'ok': bool(ok), 'detail': str(d)}); print(('OK    ' if ok else 'ECHEC ') + n, d, flush=True)
def png(url): return np.asarray(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB')).astype(int)
def mask(iso): return np.abs(iso - [255, 0, 255]).sum(2) > 90
def vis(full, iso, ui=None):
    m = mask(iso)
    if ui is not None: m &= ~ui
    if m.sum() == 0: return 0, 0
    return round(((np.abs(full - iso).sum(2) < 60) & m).sum() / m.sum(), 2), int(m.sum())
def content(I):
    a = np.asarray(I).astype(int); m = np.abs(a - [255, 0, 255]).sum(2) > 60; ys, xs = np.nonzero(m)
    return I.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
def mirror_score(A, B):
    A = content(A); B = content(B).resize(A.size); a = np.asarray(A).astype(float); b = np.asarray(B).astype(float); bm = b[:, ::-1]
    mk = lambda x: np.abs(x - [255, 0, 255]).sum(2) > 60
    return round(np.abs(a - b).sum(2)[mk(a) | mk(b)].mean(), 1), round(np.abs(a - bm).sum(2)[mk(a) | mk(bm)].mean(), 1)
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for prof in os.environ.get('PROFILES', 'desktop,mobile').split(','):
        dpr = 1 if prof == 'desktop' else 2
        ctx = br.new_context(viewport={'width': 1280, 'height': 800}) if prof == 'desktop' else br.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and 'Failed to load resource' not in m.text and errs.append(m.text))
        pg.on('response', lambda r: r.status >= 400 and errs.append(f'{r.status} {r.url}'))
        pg.goto(URL); pg.wait_for_function('window.__nml', timeout=60000); time.sleep(2.5)
        VW, VH = (1280, 800) if prof == 'desktop' else (390, 844)
        gesture = pg.touchscreen.tap if prof == 'mobile' else pg.mouse.click
        E = pg.evaluate
        st = lambda: E('JSON.parse(JSON.stringify(window.__nml.state))')
        P = lambda x, y, z: E(f'window.__nml.project({x},{y},{z})')
        def shot(): return np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert('RGB')).astype(int)
        def ui_mask():
            m = np.zeros((VH * dpr, VW * dpr), bool)
            for r in E('[...document.querySelectorAll(".wlabel:not([hidden]),#hud,#locbox,#keys button,#mini:not([hidden]),#act:not([hidden]),#msg")].map(e=>e.getBoundingClientRect()).filter(r=>r.width>0).map(r=>[r.left,r.top,r.right,r.bottom])'):
                m[max(0, int(r[1]*dpr)):max(0, int(r[3]*dpr)+1), max(0, int(r[0]*dpr)):max(0, int(r[2]*dpr)+1)] = True  # bornes négatives (étiquette hors écran) écrêtées
            return m
        def waitjs(js, t=25):
            t0 = time.time()
            while time.time() - t0 < t:
                if E(js): return True
                time.sleep(0.1)
            return False
        def settle(): waitjs('(()=>{const s=window.__nml.state;return !s.player.path.length && !s.player.pending})()', 30); time.sleep(0.35)
        def onscreen(pt): return 20 < pt['x'] < VW - 20 and 110 < pt['y'] < VH - 90
        frames = []
        def walk(x, z, loc_change=None, rec=False):
            """Marche par gestes réels vers (x, z) ; si la cible est hors écran, tap au point le plus lointain visible du segment."""
            loc0 = st()['location']
            for _ in range(14):
                s = st()
                if s['location'] != loc0: break
                pl = s['player']; d = np.hypot(x - pl['x'], z - pl['z'])
                if d < 0.6: break
                done = False
                for f in [1.0, 0.8, 0.6, 0.45, 0.3, 0.2, 0.12]:
                    tx, tz = pl['x'] + (x - pl['x']) * f, pl['z'] + (z - pl['z']) * f; pt = P(tx, 0, tz)
                    if not onscreen(pt): continue
                    k = E(f'window.__nml.pick({pt["x"]},{pt["y"]})')
                    if not k or k['kind'] not in ('ground', 'door'): continue
                    if k['kind'] == 'door' and not E(f"(window.__nml.doors.find(d=>d.id==='{k['doorId']}')||{{}}).junction || (window.__nml.doors.find(d=>d.id==='{k['doorId']}')||{{}}).edge"): continue
                    gesture(pt['x'], pt['y']); done = True; break
                if not done: return False
                t0 = time.time()
                while time.time() - t0 < 25:
                    if rec: frames.append(Image.open(io.BytesIO(pg.screenshot())).convert('RGB').resize((640, 400)))
                    s = st()
                    if s['location'] != loc0 or (not s['player']['path'] and not s['player']['pending']): break
                    time.sleep(0.12 if rec else 0.1)
                time.sleep(0.3)
            if loc_change: return waitjs(f'window.__nml.state.location==="{loc_change}"', 5)
            return True
        def bvis(bid):
            u = E(f"window.__nml.view.isolateBuilding('{bid}')")
            if not u: return 0, 0
            return vis(shot(), png(u), ui_mask())
        def actors_visible():
            full = shot(); um = ui_mask()
            return [vis(full, png(E(f"window.__nml.view.isolate('{w}')")), um)[0] for w in ('player', 'companion')]
        def crossing(name, wps, dest, door_arrive, bid, rec=False):
            for (x, z) in wps[:-1]: walk(x, z)
            ok = walk(*wps[-1], loc_change=dest, rec=rec); s = st(); time.sleep(0.9)
            arr = E(f"window.__nml.game.doorById('{door_arrive}').threshold")
            check(f'{prof}: {name} : arrivée dans {dest} par la marche', ok and s['location'] == dest, s['location'])
            s = st(); pl, c = s['player'], s['companion']
            check(f'{prof}: {name} : joueur au bout de rue correspondant', np.hypot(pl['x'] - arr['x'], pl['z'] - arr['z']) < 1.3, (round(pl['x'], 1), round(pl['z'], 1), arr))
            check(f'{prof}: {name} : Nilo suit', c['location'] == dest and c['mode'] == 'follow' and np.hypot(c['x'] - pl['x'], c['z'] - pl['z']) < 3.5, (c['location'], c['mode']))
            v = bvis(bid); check(f'{prof}: {name} : bâtiment {bid} rendu à l\'écran (pixels)', v[0] >= 0.35 and v[1] > 3000 * dpr * dpr * 0.3, v)
            a = actors_visible(); check(f'{prof}: {name} : joueur et Nilo visibles (pixels)', a[0] >= 0.5 and a[1] >= 0.4, a)
            hud = E('document.getElementById("loc").textContent'); check(f'{prof}: {name} : HUD = quartier', E(f'window.__nml.game.world.LOCATIONS["{dest}"].name') == hud, hud)
            for pd in E(f"window.__nml.doors.filter(d=>d.painted && d.location==='{dest}' && !['dusk_q1'].includes(d.location)).map(d=>d.id)"):
                e = E(f"window.__nml.view.paintedDoorError('{pd}')"); check(f'{prof}: {pd} : porte peinte alignée sur l\'ouverture (< 0,8 m)', e < 0.8, f'{e} m')
            time.sleep(1.5); check(f'{prof}: {name} : pas de rebond sur la jonction d\'arrivée', st()['location'] == dest)
            pg.screenshot(path=OUT + f'{prof}-{name.replace(" ", "_").replace(">", "")}.png')
        def money_hud(): return E('document.getElementById("money").textContent')
        def talk(npc, labels):
            pt = E(f"window.__nml.view.actorRect('{npc}')"); gesture(pt['x'] + pt['w'] / 2, pt['y'] + pt['h'] * 0.45)
            ok = waitjs('!!window.__nml.state.dialogue', 20); check(f'{prof}: dialogue {npc} ouvert par geste', ok)
            for lab in labels:
                b = pg.locator('#dlg-options button', has_text=lab).first
                b.wait_for(timeout=5000); bb = b.bounding_box(); gesture(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2); time.sleep(0.4)
            if E('!!window.__nml.state.dialogue'):
                bb = pg.locator('#dlg-close').bounding_box(); gesture(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2); time.sleep(0.3)
        def enter_painted(door, inside):
            d = E(f"window.__nml.game.doorById('{door}')"); pt = P(d['opening']['x'], 1.0, d['opening']['z']); gesture(pt['x'], pt['y'])
            ok = waitjs(f'window.__nml.state.location==="{inside}"', 25); time.sleep(1.0); return ok
        def exit_room(inside):
            d = E(f"window.__nml.game.doorById('{inside}_door')"); pt = P(d['opening']['x'], 1.0, d['opening']['z']); gesture(pt['x'], pt['y'])
            return waitjs(f'window.__nml.state.location!=="{inside}"', 25)

        s0 = st(); check(f'{prof}: départ La Pompe, 40 $, 27 PV', s0['location'] == 'dusk_q1' and s0['player']['money'] == 40 and s0['player']['hp'] == 27)
        # 1. La Pompe -> Le Transit (est) : passage dans les éboulis
        crossing('Q1>Q2 est', [(9, 18), (17, 17.4), (25, 17.5), (33, 17.6), (41, 19.6), (47, 20)], 'dusk_q2', 'j_q2_ouest', 't_guet', rec=GIF and prof == 'desktop')
        if frames: frames[0].save(OUT + 'jonction-q1-q2.gif', save_all=True, append_images=frames[1:] + [frames[-1]] * 6, duration=110, loop=0); frames.clear()
        # miroir et marche dans le nouveau quartier (pixels)
        walk(7, 18); time.sleep(0.2); E("window.__nml.state.player.heading=Math.PI/2"); time.sleep(0.3); A = content(Image.fromarray(png(E("window.__nml.view.isolate('player')")).astype('uint8')))
        E("window.__nml.state.player.heading=-Math.PI/2"); time.sleep(0.3); B = content(Image.fromarray(png(E("window.__nml.view.isolate('player')")).astype('uint8')))
        ms = mirror_score(A, B); check(f'{prof}: Q2 : sprite joueur retourné en miroir selon le sens (pixels)', ms[1] < ms[0], ms)
        # Le guet : entrée camouflée, Teo vend un tuyau (5 $) qui révèle L'atelier au Scellé
        walk(4.5, 15.5); ok = enter_painted('t_guet_door', 'guet_in'); check(f'{prof}: Q2 : entrée camouflée du guet par geste sur la porte peinte', ok, st()['location'])
        n = E('window.__nml.view.furnCount()'); full = shot(); um = ui_mask(); low = [i for i in range(n) if vis(full, png(E(f'window.__nml.view.isolateFurn({i})')), um)[0] < 0.4]
        check(f'{prof}: guet_in : mobilier réel visible (pixels)', n >= 3 and not low, (n, low))
        talk('teo', ['Tu vends des nouvelles', 'Marché conclu', 'Noté'])
        s = st(); check(f'{prof}: Teo : 5 $ payés, L\'atelier découvert par dialogue', s['player']['money'] == 35 and s['discovered'].get('s_atelier'), (s['player']['money'], s['discovered']))
        ok = exit_room('guet_in'); time.sleep(0.8); check(f'{prof}: sortie du guet', ok and st()['location'] == 'dusk_q2')
        # bord de ville est : annoncé, aucun passage
        if prof == 'desktop':
            for wp in [(12, 18), (20, 17), (28, 17), (36, 17.5), (43, 18)]: walk(*wp)
            walk(47, 18); time.sleep(0.4); msg = E('document.getElementById("msg").textContent')
            check(f'{prof}: Q2 : bout est = route des patrouilles, annoncée, sans passage', st()['location'] == 'dusk_q2' and 'route' in msg, msg)
            for wp in [(40, 18), (32, 17.5), (24, 17.5), (16, 17.5), (8, 19)]: walk(*wp)
        else: walk(7, 19)
        # 2. Le Transit -> La Pompe (retour, même rue)
        crossing('Q2>Q1 ouest', [(4, 20), (1, 20)], 'dusk_q1', 'j_q1_est', 'halle')
        check(f'{prof}: argent conservé entre quartiers (HUD)', money_hud() == '35 $', money_hud())
        # 3. La Pompe -> Le Scellé (nord, par la ruelle de la pompe)
        crossing('Q1>Q3 nord', [(40, 18), (32, 16), (30.5, 14.5), (30.4, 9), (28.5, 5.5), (28, 1)], 'dusk_q3', 'j_q3_sud', 's_garages')
        walk(28, 28); walk(28, 20); walk(28, 13); walk(28, 9)
        v = bvis('s_lab'); check(f'{prof}: Q3 : accès Human Corporation rendu (pixels)', v[0] >= 0.35, v)
        lab = E('[...document.querySelectorAll(".wlabel.service")].filter(e=>e.dataset.building==="s_atelier").map(e=>!e.hidden && e.getBoundingClientRect().width>0)[0]')
        check(f'{prof}: Q3 : « L\'atelier » affiché (découvert au Transit)', lab, lab)
        pt = P(28.5, 1.6, 5.4); gesture(pt['x'], pt['y']); time.sleep(0.5); msg = E('document.getElementById("msg").textContent')
        check(f'{prof}: Q3 : porte scellée : message, pas d\'entrée', 'soudée' in msg and st()['location'] == 'dusk_q3', msg)
        pg.screenshot(path=OUT + f'{prof}-Q3-acces-scelle.png')
        # 4. Le Scellé -> La Pompe
        crossing('Q3>Q1 sud', [(28, 20), (28, 28), (28, 35)], 'dusk_q1', 'j_q1_nord', 'grocery')
        # 5. La Pompe -> Les Sables (sud, entre la ruine et les garages)
        crossing('Q1>Q4 sud', [(28.5, 5.5), (30.4, 9), (30.5, 15), (28, 21), (28, 27), (28, 31), (28, 35)], 'dusk_q4', 'j_q4_nord', 'd_citerne')
        walk(28.5, 8.5); ok = enter_painted('d_citerne_door', 'citerne_in'); check(f'{prof}: Q4 : entrée camouflée de la citerne (porte latérale est)', ok, st()['location'])
        hp0 = st()['player']['hp']
        talk('sol', ["De l'eau"])
        s = st(); check(f'{prof}: Sol : eau achetée 3 $, inventaire', s['player']['money'] == 32 and s['player']['inv'].get('water') == 1, (s['player']['money'], s['player']['inv']))
        ok = exit_room('citerne_in'); time.sleep(0.8); check(f'{prof}: sortie de la citerne', ok and st()['location'] == 'dusk_q4')
        lab = E('[...document.querySelectorAll(".wlabel.service")].filter(e=>e.dataset.building==="d_citerne").map(e=>!e.hidden)[0]'); check(f'{prof}: Q4 : « La citerne » nommée après découverte', lab)
        for wp in [(28, 16), (28, 24), (28, 31)]: walk(*wp)
        walk(28, 35); time.sleep(0.4); msg = E('document.getElementById("msg").textContent')
        check(f'{prof}: Q4 : bout sud = terres dévastées, annoncé, sans passage', st()['location'] == 'dusk_q4' and 'dévastées' in msg, msg)
        pg.screenshot(path=OUT + f'{prof}-Q4-bord-sud.png')
        # 6. Les Sables -> La Pompe
        crossing('Q4>Q1 nord', [(28, 28), (28, 20), (28, 12), (28, 5), (28, 1)], 'dusk_q1', 'j_q1_sud', 'garages')
        s = st(); check(f'{prof}: état conservé au retour (32 $, PV {hp0}, eau, lieux)', s['player']['money'] == 32 and s['player']['hp'] == hp0 and money_hud() == '32 $' and all(s['discovered'].get(k) for k in ('t_guet', 's_atelier', 'd_citerne')), (money_hud(), s['player']['hp'], s['discovered']))
        check(f'{prof}: aucune erreur console/réseau', not errs, errs[:3])
        ctx.close()
    br.close()
ok = sum(r['ok'] for r in R); print(f'{ok}/{len(R)}')
json.dump(R, open(OUT + 'town_pixels.json', 'w'), indent=1, ensure_ascii=False)
sys.exit(0 if ok == len(R) else 1)
