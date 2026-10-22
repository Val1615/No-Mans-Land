# v6 : recette AU PIXEL des intérieurs (clinique, bar, épicerie, maison de Mara). Chrome headless, WebGL logiciel.
# Gestes réels : clic souris 1280x800, tap tactile 390x844. Tout contrôle visuel lit les pixels rendus (capture d'écran
# comparée au rendu isolé du même objet par le même pipeline), jamais seulement l'état interne.
import sys, os, time, json, base64, io
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
def content(I):
    a = np.asarray(I).astype(int); m = np.abs(a - [255, 0, 255]).sum(2) > 60; ys, xs = np.nonzero(m)
    return I.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
def mirror_score(A, B):  # même mesure que tests/flip_pixels.py
    A = content(A); B = content(B).resize(A.size); a = np.asarray(A).astype(float); b = np.asarray(B).astype(float); bm = b[:, ::-1]
    mask_ = lambda x: np.abs(x - [255, 0, 255]).sum(2) > 60
    m1 = mask_(a) | mask_(b); m2 = mask_(a) | mask_(bm)
    return round(np.abs(a - b).sum(2)[m1].mean(), 1), round(np.abs(a - bm).sum(2)[m2].mean(), 1)
URL = os.environ.get('URL', 'http://127.0.0.1:8765/'); OUT = os.environ.get('OUT', '/workspace/nml/docs/captures/dusk-q1-v6/'); os.makedirs(OUT, exist_ok=True)
GIF = os.environ.get('GIF', '1') == '1'
R = []
def check(n, ok, d=''): R.append({'test': n, 'ok': bool(ok), 'detail': str(d)}); print(('OK    ' if ok else 'ECHEC ') + n, d)
def png(url): return np.asarray(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB')).astype(int)
def shot(pg): return np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert('RGB')).astype(int)
def mask(iso): return np.abs(iso - [255, 0, 255]).sum(2) > 90
def visible_fraction(full, iso):
    m = mask(iso); m[:, :] &= True
    if m.sum() == 0: return 0, 0
    same = (np.abs(full - iso).sum(2) < 60) & m; return round(same.sum() / m.sum(), 2), int(m.sum())
def patch_std(full, x, y, r=14):
    x, y = int(x), int(y); p = full[max(0, y-r):y+r, max(0, x-r):x+r].mean(2); return round(float(p.std()), 1)
INTERIORS = [('clinic', 'clinic_door', 'clinic_in', ['vera']), ('bar', 'bar_door', 'bar_in', ['hector', 'ileana']),
             ('grocery', 'grocery_door', 'grocery_in', ['anselme']), ('mara_house', 'mara_house_door', 'mara_in', ['mara', 'bruno']),
             ('grocery', 'grocery_door2', 'grocery_in', ['anselme'])]  # 2e entrée camouflée de l'épicerie (porte latérale est)
NAMES = {'clinic': 'clinique-vera', 'bar': 'bar-le-passage-hector', 'grocery': 'epicerie-anselme', 'mara_house': 'maison-mara'}
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for prof in os.environ.get('PROFILES', 'desktop,mobile').split(','):
        dpr = 1 if prof == 'desktop' else 2
        ctx = br.new_context(viewport={'width': 1280, 'height': 800}) if prof == 'desktop' else br.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and 'Failed to load resource' not in m.text and errs.append(m.text))
        pg.on('response', lambda r: r.status >= 400 and errs.append(f'{r.status} {r.url}'))
        pg.goto(URL); pg.wait_for_function('window.__nml', timeout=60000); [(pg.locator(_s).tap if pg.evaluate('navigator.maxTouchPoints>0') else pg.locator(_s).click)() for _s in ('#m-new', '#cr-next', '#cr-enter')]; pg.wait_for_function('!document.body.classList.contains("menu-open")'); time.sleep(2.5)
        gesture = pg.touchscreen.tap if prof == 'mobile' else pg.mouse.click
        P = lambda x, y, z: pg.evaluate(f'window.__nml.project({x},{y},{z})')
        def tap_world(x, y, z): pt = P(x, y, z); gesture(pt['x'], pt['y'])
        st = lambda: pg.evaluate('JSON.parse(JSON.stringify(window.__nml.state))')
        def waitjs(js, t=25):
            t0 = time.time()
            while time.time() - t0 < t:
                if pg.evaluate(js): return True
                time.sleep(0.1)
            return False
        for bid, door, inside, npcs in INTERIORS:
            d = pg.evaluate(f"window.__nml.game.doorById('{door}')")
            # placement devant la façade par commande (le trajet de rue est couvert par dusk_q1_check.py), puis GESTE sur la porte peinte
            pg.evaluate(f"(()=>{{const g=window.__nml.game;const e={'1' if d['opening']['side']=='east' else '0'};Object.assign(g.state.player,{{x:{d['threshold']['x']}+1.5*e,z:{d['threshold']['z']}+1.5*(1-e),path:[]}});Object.assign(g.state.companion,{{x:{d['threshold']['x']}+1+e,z:{d['threshold']['z']}+2-e,path:[]}})}})()")
            time.sleep(0.6); frames = []
            tap_world(d['opening']['x'], 1.0, d['opening']['z'])
            t0 = time.time()
            while GIF and prof == 'desktop' and bid == 'clinic' and time.time() - t0 < 2.5: frames.append(Image.open(io.BytesIO(pg.screenshot())).convert('RGB').resize((640, 400))); time.sleep(0.12)
            ok = waitjs(f'window.__nml.state.location==="{inside}"'); check(f'{prof}: {bid} entrée par {"tap" if prof=="mobile" else "clic"} sur la porte peinte', ok, st()['location'])
            time.sleep(1.2)
            for _ in range(4 if GIF and prof == 'desktop' and bid == 'clinic' else 0): frames.append(Image.open(io.BytesIO(pg.screenshot())).convert('RGB').resize((640, 400))); time.sleep(0.15)
            full = shot(pg)
            # 1. mobilier rendu et visible au pixel
            n = pg.evaluate('window.__nml.view.furnCount()'); check(f'{prof}: {bid} mobilier en sprites présent', n >= 4, f'{n} meubles')
            furn = pg.evaluate('window.__nml.view.furnitureOf()'); low = []
            # pixels légitimement couverts par un personnage (joueur, Nilo, PNJ devant le meuble) : exclus du compte
            actors = np.zeros(full.shape[:2], bool)
            for w in ['player', 'companion'] + npcs: actors |= mask(png(pg.evaluate(f"window.__nml.view.isolate('{w}')")))
            # ... et pixels sous l'interface HTML (étiquettes, HUD, bouton) : ce n'est pas le rendu 3D
            for r in pg.evaluate('[...document.querySelectorAll(".wlabel:not([hidden]),#hud,#locbox,#keys button,#msg,#mini:not([hidden]),#act:not([hidden])")].map(e=>e.getBoundingClientRect()).filter(r=>r.width>0).map(r=>[r.left,r.top,r.right,r.bottom])'):
                actors[max(0, int(r[1]*dpr)):int(r[3]*dpr)+1, max(0, int(r[0]*dpr)):int(r[2]*dpr)+1] = True
            for i in range(n):
                iso = png(pg.evaluate(f'window.__nml.view.isolateFurn({i})')); iso[actors] = [255, 0, 255]; vf, area = visible_fraction(full, iso)
                if area < 400 * dpr * dpr * (0.35 if prof == 'mobile' else 1) or vf < 0.5: low.append((furn[i]['id'], vf, area))
            check(f'{prof}: {bid} chaque meuble est visible au pixel (>= 50 % de son image à l écran)', not low, low or f'{n}/{n}')
            # 2. murs et sol texturés : variance locale des pixels (une couleur unie donnerait ~0)
            L = pg.evaluate('window.__nml.game.location'); W, D = L['size']['w'], L['size']['d']
            pts = {'mur nord': (W * 0.62, 2.2, 0.12), 'mur ouest': (0.12, 2.2, D * 0.62), 'sol': (W * 0.5, 0, D * 0.55)}
            stds = {k: patch_std(full, P(*v)['x'] * dpr, P(*v)['y'] * dpr) for k, v in pts.items()}
            check(f'{prof}: {bid} murs et sol texturés (écart-type local des pixels > 3 ; une couleur unie éclairée donne < 1)', all(v > 3 for v in stds.values()), stds)
            # 3. PNJ de service à l'intérieur, visibles au pixel
            for npc in npcs:
                loc = pg.evaluate(f"window.__nml.npcs.find(n=>n.id==='{npc}').location"); iso = png(pg.evaluate(f"window.__nml.view.isolate('{npc}')")); vf, area = visible_fraction(full, iso)
                # Bruno se tient derrière le rideau (DUSK_TOWN_Q1 §7), Hector derrière son comptoir : partiellement cachés par conception
                need = {'bruno': 0.25, 'hector': 0.4}.get(npc, 0.6)
                check(f'{prof}: {npc} dans {inside} et visible au pixel', loc == inside and vf >= need, f'{loc}, visible {vf} (seuil {need})')
            # 4. joueur visible au seuil (porte de sortie et mur bas en occultation)
            iso = png(pg.evaluate("window.__nml.view.isolate('player')")); vf, _ = visible_fraction(shot(pg), iso)
            check(f'{prof}: {bid} joueur visible au seuil malgré la porte et le mur avant', vf >= 0.6, f'visible {vf}, opacité porte {pg.evaluate("window.__nml.view.leafOpacity()")}')
            # 5. nom du service : affiché une fois découvert (entrée)
            check(f'{prof}: {bid} découvert en entrant', st()['discovered'].get(bid) is True)
            if door == 'grocery_door2': pass
            elif prof == 'desktop' or bid in ('clinic', 'bar'):
                pg.screenshot(path=f'{OUT}{prof}-interieur-{NAMES[bid]}.png')
            # 6. marche et miroir EN INTÉRIEUR, sur les pixels
            WALK = {'clinic': ((1.0, 5.0), (4.0, 5.0), (1.8, 5.0)), 'grocery': ((3.6, 6.0), (6.6, 6.0), (4.0, 6.0))}
            if bid in WALK and door != 'grocery_door2':
                (ax, az), (bx, bz), (cx, cz) = WALK[bid]
                def iso_player():
                    I = Image.fromarray(png(pg.evaluate("window.__nml.view.isolate('player')")).astype('uint8')); r = pg.evaluate("window.__nml.view.actorRect('player')")
                    return I.crop((int(r['x']*dpr)-6, int(r['y']*dpr)-10, int((r['x']+r['w'])*dpr)+6, int((r['y']+r['h'])*dpr)+6))
                def bbox_h(I):
                    m = mask(np.asarray(I).astype(int)); ys = np.nonzero(m.any(1))[0]; return int(ys.max() - ys.min()) if len(ys) else 0
                pg.evaluate(f'window.__nml.game.moveTo({ax},{az})'); waitjs('window.__nml.state.player.path.length===0'); time.sleep(0.5)
                tap_world(bx, 0, bz); time.sleep(0.15); hs = []
                for _ in range(7): hs.append(bbox_h(iso_player())); time.sleep(0.04)
                walking = len(st()['player']['path']) > 0 or True
                waitjs('window.__nml.state.player.path.length===0'); time.sleep(0.6); A = iso_player(); h_rest = bbox_h(A)
                tap_world(cx, 0, cz); time.sleep(0.3); waitjs('window.__nml.state.player.path.length===0'); time.sleep(0.6); B = iso_player()
                same, mir = mirror_score(A, B); check(f'{prof}: {bid} miroir du joueur rendu en intérieur (geste vers la droite puis la gauche)', mir < 0.6 * same, f'écart direct {same}, écart miroir {mir}')
                check(f'{prof}: {bid} animation de marche en intérieur (hauteur rendue du sprite varie au pas)', max(hs) - min(hs) >= 1, f'hauteurs rendues pendant la marche {hs} px, au repos {h_rest} px')
                if prof == 'desktop': A.save(f'{OUT}desktop-interieur-{bid}-marche-droite.png'); B.save(f'{OUT}desktop-interieur-{bid}-marche-gauche.png')
            # 7. occultation par un meuble (bar : joueur derrière le comptoir)
            if bid == 'bar':
                pg.evaluate('window.__nml.game.moveTo(2.4,1.4)'); waitjs('window.__nml.state.player.path.length===0'); time.sleep(1.2)
                f = [x for x in pg.evaluate('window.__nml.view.furnitureOf()') if x['id'] == 'bar_counter_b'][0]
                iso = png(pg.evaluate("window.__nml.view.isolate('player')")); vf, _ = visible_fraction(shot(pg), iso)
                check(f'{prof}: comptoir du bar transparent quand le joueur est derrière, joueur visible au pixel', f['opacity'] < 0.5 and vf >= 0.5, f"opacité comptoir {f['opacity']}, joueur visible {vf}")
                if prof == 'desktop': pg.screenshot(path=f'{OUT}desktop-occultation-comptoir.png')
            # sortie par geste : clic sur la porte intérieure (bureau) / bouton Sortir (mobile)
            di = pg.evaluate(f'window.__nml.doors.find(d=>d.location==="{inside}" && d.target.doorId==="{door}")')
            if prof == 'mobile':
                ex, ez = (0.5, 0) if di['opening']['side'] == 'east' else (0, 0.5)
                pg.evaluate(f"window.__nml.game.moveTo({di['threshold']['x']-ex},{di['threshold']['z']-ez})"); waitjs('window.__nml.state.player.path.length===0'); time.sleep(0.3)
                waitjs('!document.getElementById("act").hidden', 5); pg.locator('#act').tap()
            else:
                ex, ez = (1, 0) if di['opening']['side'] == 'east' else (0, 1)
                pg.evaluate(f"window.__nml.game.moveTo({di['threshold']['x']-ex},{di['threshold']['z']-ez})"); waitjs('window.__nml.state.player.path.length===0'); time.sleep(0.4)
                tap_world(di['opening']['x'], 1.0, di['opening']['z'])
            t0 = time.time()
            while GIF and prof == 'desktop' and bid == 'clinic' and time.time() - t0 < 2.5: frames.append(Image.open(io.BytesIO(pg.screenshot())).convert('RGB').resize((640, 400))); time.sleep(0.12)
            ok = waitjs('window.__nml.state.location==="dusk_q1"'); s = st()
            check(f'{prof}: {bid} sortie par {"bouton Sortir (tap)" if prof=="mobile" else "clic sur la porte"}, arrivée au seuil devant la porte peinte', ok and abs(s['player']['x'] - d['threshold']['x']) < 0.05 and abs(s['player']['z'] - d['threshold']['z']) < 0.05, (s['player']['x'], s['player']['z']) if ok else (s['location'], s['player']['x'], s['player']['z'], s['dialogue'], [e.get('text') or e.get('type') for e in s['log'][-4:]]))
            time.sleep(1.0)
            lab = pg.evaluate(f'[...document.querySelectorAll(".wlabel.service")].filter(e=>!e.hidden).map(e=>e.dataset.building)')
            check(f'{prof}: {bid} nom du service affiché dehors après découverte', bid in lab, lab)
            for _ in range(5 if GIF and prof == 'desktop' and bid == 'clinic' else 0): frames.append(Image.open(io.BytesIO(pg.screenshot())).convert('RGB').resize((640, 400))); time.sleep(0.15)
            if frames: frames[0].save(f'{OUT}entree-sortie-clinique.gif', save_all=True, append_images=frames[1:], duration=140, loop=0); check(f'{prof}: gif entrée/sortie écrit', len(frames) > 8, f'{len(frames)} images')
        check(f'{prof}: aucune erreur console (intérieurs)', not errs, '; '.join(errs)[:300])
        ctx.close()
    br.close()
json.dump(R, open(OUT + 'resultats-interieurs.json', 'w'), ensure_ascii=False, indent=1)
print(sum(r['ok'] for r in R), '/', len(R))
