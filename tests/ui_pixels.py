# v8 : recette de l'interface « radio de récupération » (direction A) AU PIXEL et par GESTES RÉELS, bureau 1280x800 et mobile 390x844.
# Contraste mesuré sur les pixels rendus (texte contre fond réel du panneau, posé sur sable clair), surface de scène couverte par l'UI,
# personnages visibles sous l'UI, tous les accès (Sac, Journal, Carte, Discret, dialogue, achat) actionnés par clic / tap.
import sys, os, time, io, base64, json
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8765/'); OUT = os.environ.get('OUT', '/workspace/nml/docs/captures/ui-v8/'); os.makedirs(OUT, exist_ok=True)
R = []
def check(n, ok, d=''): R.append({'test': n, 'ok': bool(ok), 'detail': str(d)}); print(('OK    ' if ok else 'ECHEC ') + n, d, flush=True)
def png(url): return np.asarray(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB')).astype(int)
def lum(rgb):
    c = np.asarray(rgb, float) / 255; c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4); return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]
UI = '#hud,#locbox,#keys,#msg,#mini,#actions,#dialogue,#panel,#labels'
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for prof in os.environ.get('PROFILES', 'desktop,mobile').split(','):
        dpr = 1 if prof == 'desktop' else 2
        ctx = br.new_context(viewport={'width': 1280, 'height': 800}) if prof == 'desktop' else br.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and 'Failed to load resource' not in m.text and errs.append(m.text))
        pg.on('response', lambda r: r.status >= 400 and errs.append(f'{r.status} {r.url}'))
        pg.goto(URL); pg.wait_for_function('window.__nml', timeout=60000); [(pg.locator(_s).tap if pg.evaluate('navigator.maxTouchPoints>0') else pg.locator(_s).click)() for _s in ('#m-new', '#cr-next', '#cr-enter')]; pg.wait_for_function('!document.body.classList.contains("menu-open")'); time.sleep(2.5)
        pg.evaluate("import('./src/core/path.js').then(m => window.__findPath = m.findPath)"); time.sleep(0.4)
        VW, VH = (1280, 800) if prof == 'desktop' else (390, 844)
        gesture = pg.touchscreen.tap if prof == 'mobile' else pg.mouse.click
        E = pg.evaluate; st = lambda: E('JSON.parse(JSON.stringify(window.__nml.state))')
        P = lambda x, y, z: E(f'window.__nml.project({x},{y},{z})')
        shot = lambda: np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert('RGB')).astype(int)
        def press(sel):
            bb = pg.locator(sel).first.bounding_box(); gesture(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2); time.sleep(0.45)
        def rect(sel): return E(f'(()=>{{const e=document.querySelector("{sel}"); if(!e||e.hidden||getComputedStyle(e).display==="none") return null; const r=e.getBoundingClientRect(); return r.width?[r.left,r.top,r.right,r.bottom]:null}})()')
        def scene_only():
            E(f'document.querySelectorAll("{UI}").forEach(e=>e.style.visibility="hidden")'); time.sleep(0.25); s = shot()
            E(f'document.querySelectorAll("{UI}").forEach(e=>e.style.visibility="")'); time.sleep(0.25); return s
        def crop(a, r): return a[int(r[1]*dpr):int(r[3]*dpr), int(r[0]*dpr):int(r[2]*dpr)]
        def contrast(sel, full, bare):
            # texte = 75e centile des pixels éclaircis par l'UI ; fond = médiane de luminance de tout le panneau (prudent)
            # le voile ne fait qu'assombrir : les pixels de texte sont ceux que l'UI ÉCLAIRCIT par rapport à la scène nue
            r = rect(sel); A, B = crop(full, r), crop(bare, r); L = lum(A); up = L > lum(B) + 0.08
            if up.sum() < 20: return 0.0, round(float(lum(B).mean()), 3)
            t = np.percentile(L[up], 75); back = np.median(L)
            return round(float((t + 0.05) / (back + 0.05)), 2), round(float(lum(B).mean()), 3)
        def cover(sels):
            m = np.zeros((VH, VW), bool)
            for s in sels:
                for r in E(f'[...document.querySelectorAll("{s}")].filter(e=>!e.hidden&&getComputedStyle(e).display!=="none"&&getComputedStyle(e).visibility!=="hidden").map(e=>{{const r=e.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]}})'):
                    m[max(0, int(r[1])):max(0, int(r[3])), max(0, int(r[0])):max(0, int(r[2]))] = True
            return round(float(m.mean()), 3)
        def vis(who):
            full = shot(); iso = png(E(f"window.__nml.view.isolate('{who}')")); m = np.abs(iso - [255, 0, 255]).sum(2) > 90
            return round(float(((np.abs(full - iso).sum(2) < 60) & m).sum() / max(1, m.sum())), 2)
        def idle(t=30):
            t0 = time.time()
            while time.time() - t0 < t:
                if E('(()=>{const s=window.__nml.state;return !s.player.path.length && !s.player.pending})()'): time.sleep(0.3); return
                time.sleep(0.1)
        def walk(x, z, tol=0.7):
            loc0 = st()['location']
            for _ in range(20):
                s = st(); pl = s['player']
                if s['location'] != loc0 or ((x - pl['x'])**2 + (z - pl['z'])**2) ** 0.5 < tol: return True
                path = E(f"window.__findPath(window.__nml.game.grids[window.__nml.state.location], window.__nml.state.player, {{x:{x},z:{z}}})")
                if not path: return False
                for q in reversed(path[1:]):
                    pt = P(q['x'], 0, q['z'])
                    if not (20 < pt['x'] < VW - 20 and 130 < pt['y'] < VH - 110): continue
                    k = E(f'window.__nml.pick({pt["x"]},{pt["y"]})')
                    if k and k['kind'] == 'ground' and ((k['x'] - q['x'])**2 + (k['z'] - q['z'])**2) ** 0.5 < 1: gesture(pt['x'], pt['y']); break
                else: return False
                idle()
            return False
        T = 'desktop' if prof == 'desktop' else 'mobile'
        # 1. Exploration : HUD lisible sur sable clair (vue caméra déplacée pour mettre du sable sous les panneaux), scène peu couverte
        # pour chaque panneau, on cherche une vue (caméra seule, le joueur ne bouge pas) qui met le sable le plus clair dessous
        CANDS = [(x, z) for x in (6, 14, 22, 30, 38, 44) for z in (2, 10, 18, 26, 32, 35)]
        best = {}
        for (x, z) in CANDS:  # (zones de texte mesurées : #hud .cell = PV / $ / Nilo hors portrait)
            E(f'window.__nml.setCamera({{x:{x},z:{z},ppm:50}})'); time.sleep(0.35); bare = scene_only()
            for sel in ['#hud .cell', '#locbox', '#k-sac']:
                u = float(lum(crop(bare, rect(sel))).mean())
                if u > best.get(sel, (0,))[0]: best[sel] = (u, x, z)
        for sel in ['#hud .cell', '#locbox', '#k-sac']:
            u, x, z = best[sel]; E(f'window.__nml.setCamera({{x:{x},z:{z},ppm:50}})'); time.sleep(0.6); full, bare = shot(), scene_only()
            c, under = contrast(sel, full, bare); check(f'{T}: contraste {sel} sur sable clair ≥ 4,5:1 (pixels)', c >= 4.5 and under > 0.15, f'contraste {c}, luminance du sable dessous {under} (vue {x},{z})')
            if sel == '#hud .cell': pg.screenshot(path=OUT + f'{prof}-contraste-sable.png'); fullH, bareH = full, bare
        full, bare = fullH, bareH
        # ambre limité au texte : dans les panneaux, la scène reste lisible (pixels non-texte proches de la scène assombrie, pas teintés)
        E(f'window.__nml.setCamera({{x:{best["#hud .cell"][1]},z:{best["#hud .cell"][2]},ppm:50}})'); time.sleep(0.4); r = rect('#hud'); A, B = crop(full, r), crop(bare, r); d = np.abs(A - B).sum(2); bgA, bgB = A[d <= 60], B[d <= 60]
        if bgA.size == 0: bgA, bgB = A.reshape(-1, 3), B.reshape(-1, 3)
        tint = float(np.abs((A.mean((0, 1)) / max(1, A.mean())) - (B.mean((0, 1)) / max(1, B.mean()))).max())
        check(f'{T}: fond de panneau non teinté en ambre (équilibre des couleurs conservé)', tint < 0.25, round(tint, 3))
        E('window.__nml.setCamera(null)'); time.sleep(0.8)
        cv = cover(['#hud', '#locbox', '#keys button', '#act']); check(f'{T}: exploration : UI ≤ {12 if prof == "desktop" else 22} % de l\'écran', cv <= (0.12 if prof == 'desktop' else 0.22), cv)
        check(f'{T}: exploration : joueur visible, Nilo non rendu (pixels)', vis('player') >= 0.6 and vis('companion') == 0, (vis('player'), vis('companion')))
        hud = E('[document.getElementById("hp").textContent, document.getElementById("money").textContent, document.getElementById("loc").textContent, getComputedStyle(document.getElementById("nilo").closest(".cell")).display==="none"]')
        check(f'{T}: HUD : PV, $, quartier ; case Nilo masquée', hud[0] == '27/40' and hud[1] == '40 $' and 'Pompe' in hud[2] and hud[3] is True, hud)
        pg.screenshot(path=OUT + f'{prof}-exploration.png')
        # 2. Minimal (bouton Discret / touche H)
        h0 = crop(shot(), rect('#hud'))
        r0 = rect('#hud'); press('#k-mini'); full = shot()
        check(f'{T}: interface minimale par {"tap" if prof == "mobile" else "clic"} : HUD retiré, scène rendue à la place (pixels)', rect('#hud') is None and rect('#mini') and np.abs(crop(full, [r0[0] + 200 if prof == 'desktop' else r0[0] + 150, r0[1], r0[2], r0[3]]) - crop(scene_only(), [r0[0] + 200 if prof == 'desktop' else r0[0] + 150, r0[1], r0[2], r0[3]])).mean() < 4, E('document.getElementById("mini").textContent'))
        cv = cover(['#mini', '#keys button', '#msg']); check(f'{T}: minimal : UI ≤ 4 % de l\'écran', cv <= 0.04, cv)
        pg.screenshot(path=OUT + f'{prof}-minimal.png')
        if prof == 'desktop': pg.keyboard.press('h'); time.sleep(0.3)
        else: press('#k-mini')
        check(f'{T}: retour à l\'interface complète ({"touche H" if prof == "desktop" else "tap"})', rect('#hud') is not None)
        # 3. Journal et carte (lieux, quartiers)
        press('#k-journal'); check(f'{T}: Journal ouvert par geste', rect('#panel') and 'JOURNAL' in E('document.getElementById("panel").textContent'))
        cv = cover(['#panel']); check(f'{T}: Journal sur un bord, scène visible (≤ {35 if prof == "desktop" else 45} %)', cv <= (0.35 if prof == 'desktop' else 0.45) and vis('player') >= 0.5, (cv, vis('player')))
        pg.screenshot(path=OUT + f'{prof}-journal.png')
        press('#k-carte'); txt = E('document.getElementById("panel").textContent'); check(f'{T}: Carte ouverte par geste, quartier courant marqué', 'CARTE' in txt and 'ici' in txt and 'La Pompe' in txt, txt[:60])
        pg.screenshot(path=OUT + f'{prof}-carte.png'); press('#panel-close'); check(f'{T}: fermeture du panneau par ×', rect('#panel') is None)
        # 4. Marche réelle jusqu'au bar, dialogue par geste sur Hector : en bas à gauche, jamais au centre
        d = E("window.__nml.game.doorById('bar_door')"); walk(d['threshold']['x'], d['threshold']['z'] + 2.2, 1.0)
        pt = P(d['opening']['x'], 1.0, d['opening']['z']); gesture(pt['x'], pt['y'])
        pg.wait_for_function('window.__nml.state.location==="bar_in"', timeout=25000); time.sleep(1)
        a = E("window.__nml.view.actorRect('hector')"); gesture(a['x'] + a['w'] / 2, a['y'] + a['h'] * 0.45)
        pg.wait_for_function('!!window.__nml.state.dialogue', timeout=20000); time.sleep(0.6)
        r = rect('#dialogue'); cx = (r[0] + r[2]) / 2
        check(f'{T}: dialogue ancré en bas{" à gauche" if prof == "desktop" else ""}, pas au centre', r[3] > VH - 70 and ((r[0] < 20 and cx < VW * 0.42) if prof == 'desktop' else r[1] > VH * 0.4), [round(v) for v in r])
        full, bare = shot(), scene_only(); c, _ = contrast('#dlg-text', full, bare); check(f'{T}: contraste du texte de dialogue ≥ 4,5:1 (pixels)', c >= 4.5, c)
        check(f'{T}: pendant le dialogue : Hector et le joueur visibles (pixels)', vis('hector') >= 0.5 and vis('player') >= 0.5, (vis('hector'), vis('player')))
        n = E('document.querySelectorAll("#dlg-options button").length'); check(f'{T}: choix numérotés (1> …)', n >= 3 and E('document.querySelector("#dlg-options button").dataset.n') == '1', n)
        pg.screenshot(path=OUT + f'{prof}-dialogue.png')
        # 5. Sac : achat existant depuis le panneau, pendant le dialogue
        m0 = st()['player']['money']; press('#k-sac')
        check(f'{T}: Sac ouvert, offres du marchand listées', 'ACHAT · HECTOR' in E('document.getElementById("panel").textContent'))
        if prof == 'mobile': check(f'{T}: mobile : un seul panneau à la fois (dialogue masqué sous le sac)', rect('#dialogue') is None)
        else:
            a, b = rect('#dialogue'), rect('#panel'); check(f'{T}: sac et dialogue sans chevauchement', a[2] <= b[0] or a[3] <= b[1], (a, b))
        pg.screenshot(path=OUT + f'{prof}-sac.png')
        press('#panel [data-buy]:last-child button') if False else press('#panel li:last-child [data-buy]')
        s = st(); check(f'{T}: achat par geste dans le sac (−3 $, HUD à jour)', s['player']['money'] == m0 - 3 and E('document.getElementById("money").textContent') == f'{m0 - 3} $', (m0, s['player']['money']))
        press('#panel-close')
        if prof == 'desktop':
            pg.keyboard.press('Escape'); time.sleep(0.3); a = E("window.__nml.view.actorRect('hector')"); gesture(a['x'] + a['w'] / 2, a['y'] + a['h'] * 0.45)
            pg.wait_for_function('!!window.__nml.state.dialogue', timeout=20000); time.sleep(0.4)
            pg.keyboard.press(str(E('document.querySelectorAll("#dlg-options button").length'))); time.sleep(0.4)
            check(f'{T}: choix au clavier (chiffre) ferme le dialogue', not st()['dialogue'])
            for k, w in [('i', 'SAC'), ('j', 'JOURNAL'), ('m', 'CARTE')]:
                pg.keyboard.press(k); time.sleep(0.3); check(f'{T}: touche {k.upper()} ouvre {w}', w in E('document.getElementById("panel").textContent'))
            pg.keyboard.press('Escape'); time.sleep(0.3); check(f'{T}: Échap ferme le panneau', rect('#panel') is None)
        else:
            if st()['dialogue']: press('#dlg-close')
        # 6. sortie par le bouton d'action (accessible, petit, bord bas)
        dd = E("window.__nml.game.doorById('bar_in_door')"); walk(dd['threshold']['x'], dd['threshold']['z'] - 0.2, 0.5)
        ok = E('!document.getElementById("act").hidden'); ar = rect('#act')
        check(f'{T}: bouton d\'action discret (≤ 56 px de haut, en bas)', ok and ar[3] - ar[1] <= 56 and ar[1] > VH * 0.75, ar)
        press('#act'); pg.wait_for_function('window.__nml.state.location==="dusk_q1"', timeout=20000)
        check(f'{T}: sortie par le bouton d\'action', st()['location'] == 'dusk_q1')
        check(f'{T}: aucune erreur console/réseau', not errs, errs[:3]); ctx.close()
    br.close()
ok = sum(r['ok'] for r in R); print(f'{ok}/{len(R)}'); json.dump(R, open(OUT + 'ui_pixels.json', 'w'), indent=1, ensure_ascii=False)
sys.exit(0 if ok == len(R) else 1)
