# Vérification navigateur réelle (Chrome headless, WebGL logiciel). Clics/taps réels via Playwright.
import json, sys, time
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8765/'
OUT = '/workspace/nml/docs/captures/'
results = []
def check(name, ok, detail=''):
    results.append({'test': name, 'ok': bool(ok), 'detail': detail}); print(('OK  ' if ok else 'ECHEC ') + name, detail)
def st(page): return page.evaluate('JSON.parse(JSON.stringify(window.__nml.state))')
def wait_for(page, js, timeout=15):
    t = time.time()
    while time.time() - t < timeout:
        if page.evaluate(js): return True
        time.sleep(0.1)
    return False
def inside_shop(s): return 4 < s['player']['x'] < 12 and 4 < s['player']['z'] < 10 and s['location'] == 'street'

with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for profile in ['desktop', 'mobile']:
        if profile == 'desktop':
            ctx = b.new_context(viewport={'width': 1280, 'height': 800})
        else:
            ctx = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2)
        page = ctx.new_page(); errors = []
        page.on('pageerror', lambda e: errors.append(str(e))); page.on('console', lambda m: m.type == 'error' and errors.append(m.text))
        page.goto(URL); page.wait_for_function('window.__nml'); time.sleep(1)
        page.screenshot(path=f'{OUT}{profile}-01-rue.png')
        tap = (lambda x, y: page.touchscreen.tap(x, y)) if profile == 'mobile' else (lambda x, y: page.mouse.click(x, y))
        # 1. Geste sur la façade (desktop) ou sur la porte (mobile)
        pt = page.evaluate('window.__nml.project(8.0, 1.6, 10.0)' if profile == 'mobile' else 'window.__nml.project(6.0, 1.5, 10.0)')
        tap(pt['x'], pt['y'])
        samples = []
        entered = False; t0 = time.time()
        while time.time() - t0 < 15:
            s = st(page); samples.append(s)
            if s['location'] == 'shop_interior': entered = True; break
            time.sleep(0.05)
        check(f'{profile}: {"clic façade" if profile=="desktop" else "tap porte"} -> trajet au seuil puis entrée', entered, f"lieu={s['location']}")
        check(f'{profile}: aucun point du trajet dans l\'emprise du bâtiment', not any(inside_shop(x) for x in samples), f'{len(samples)} échantillons')
        s = st(page); c = s['companion']; d = ((c['x']-s['player']['x'])**2 + (c['z']-s['player']['z'])**2) ** .5
        check(f'{profile}: compagnon entré avec le joueur', c['mode'] == 'follow' and c.get('location') == 'shop_interior' and d < 2, f"mode={c['mode']} dist={d:.2f}m")
        time.sleep(0.8); page.screenshot(path=f'{OUT}{profile}-02-interieur.png')
        # 2. Sortie : desktop clic sur la porte intérieure, mobile bouton "Sortir"
        if profile == 'desktop':
            pt = page.evaluate('window.__nml.project(4.0, 1.2, 6.0)'); tap(pt['x'], pt['y'])
        else:
            page.locator('#act').tap()
        ok = wait_for(page, "window.__nml.state.location==='street'")
        s = st(page); c = s['companion']; d = ((c['x']-s['player']['x'])**2 + (c['z']-s['player']['z'])**2) ** .5
        check(f'{profile}: sortie vers la rue au seuil extérieur', ok and abs(s['player']['x']-8) < .05 and abs(s['player']['z']-11) < .05, f"pos=({s['player']['x']},{s['player']['z']})")
        check(f'{profile}: compagnon ressorti avec le joueur', c['mode']=='follow' and c.get('location')=='street' and d < 2, f'dist={d:.2f}m')
        # 3. Réentrée immédiate (régression du bug historique de compagnon replacé loin)
        pt = page.evaluate('window.__nml.project(8.0, 1.6, 10.0)'); tap(pt['x'], pt['y'])
        check(f'{profile}: réentrée immédiate après sortie', wait_for(page, "window.__nml.state.location==='shop_interior'"))
        page.evaluate("window.__nml.game.useDoor('shop_door_in')"); wait_for(page, "window.__nml.state.location==='street'")
        # 4. Suivi du compagnon en extérieur via clic sol réel
        pt = page.evaluate('window.__nml.project(4.0, 0, 15.0)'); tap(pt['x'], pt['y'])
        wait_for(page, "Math.hypot(window.__nml.state.player.x-4, window.__nml.state.player.z-15)<0.6"); time.sleep(1.5)
        s = st(page); c = s['companion']; d = ((c['x']-s['player']['x'])**2 + (c['z']-s['player']['z'])**2) ** .5
        check(f'{profile}: compagnon suit après déplacement au sol (clic réel)', d < 2.2, f'dist={d:.2f}m')
        # 5. Collision : destination dans le bâtiment refusée explicitement
        r = page.evaluate("window.__nml.game.moveTo(8, 7)")
        check(f'{profile}: destination dans l\'emprise refusée (commande)', r.get('ok') is False and r.get('reason') == 'chemin_bloque', json.dumps(r))
        # 6. Occlusion : joueur derrière le volume occultant (déplacement par commande)
        page.evaluate("window.__nml.game.moveTo(16, 1.5)")
        wait_for(page, "Math.hypot(window.__nml.state.player.x-16, window.__nml.state.player.z-1.5)<0.3", 20); time.sleep(1.2)
        op = page.evaluate("window.__nml.opacityOf('tower')")
        check(f'{profile}: volume occultant transparent quand le joueur est derrière', op is not None and op < 0.5, f'opacité={op:.2f}')
        page.screenshot(path=f'{OUT}{profile}-03-occultation.png')
        page.evaluate("window.__nml.game.moveTo(20, 16)"); wait_for(page, "window.__nml.state.player.z>15", 20); time.sleep(1.2)
        op = page.evaluate("window.__nml.opacityOf('tower')")
        check(f'{profile}: volume redevenu opaque quand le joueur est devant', op > 0.9, f'opacité={op:.2f}')
        check(f'{profile}: aucune erreur console', not errors, '; '.join(errors)[:300])
        ctx.close()
    b.close()
json.dump(results, open(OUT + 'resultats-verification.json', 'w'), ensure_ascii=False, indent=1)
print(sum(r['ok'] for r in results), '/', len(results))
