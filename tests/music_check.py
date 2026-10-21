# v9 : musique d'ambiance de Dusk-Town. Lecture réelle après le premier geste, boucle, coupure mémorisée, continuité entre quartiers,
# atténuation en intérieur, fichier livré octet-identique (SHA-256) à celui fourni par Valentin.
import sys, os, time, json, hashlib, urllib.request
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8765/'); OUT = os.environ.get('OUT', '/workspace/nml/docs/captures/quete-v9/'); os.makedirs(OUT, exist_ok=True)
REF = 'ae1d8ee965840781fa5c5ed46f8489d34bdf70a10ec461ffb1ec0788ca166b12'
R = []
def check(n, ok, d=''): R.append({'test': n, 'ok': bool(ok), 'detail': str(d)[:200]}); print(('OK    ' if ok else 'ECHEC ') + n, str(d)[:200], flush=True)
h = hashlib.sha256(urllib.request.urlopen(URL + 'assets/audio/dusk_town_ambiance.mp3').read()).hexdigest()
check('fichier servi octet-identique à l\'original (SHA-256)', h == REF, h)
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=user-gesture-required'])
    for prof in ('desktop', 'mobile'):
        ctx = br.new_context(viewport={'width': 1280, 'height': 800}) if prof == 'desktop' else br.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2)
        pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(URL); pg.wait_for_function('window.__nml', timeout=60000); (pg.locator('#m-new').tap if pg.evaluate('navigator.maxTouchPoints>0') else pg.locator('#m-new').click)(); pg.wait_for_function('!document.body.classList.contains("menu-open")'); time.sleep(2)
        E = pg.evaluate; gesture = pg.touchscreen.tap if prof == 'mobile' else pg.mouse.click
        M = lambda: E('(()=>{const a=window.__nml.music;return {paused:a.paused,t:a.currentTime,loop:a.loop,muted:a.muted,vol:a.volume,src:a.currentSrc,dur:a.duration,n:document.querySelectorAll("audio").length}})()')
        P = lambda x, z: E(f'window.__nml.project({x},0,{z})')
        def tapel(sel): b = pg.locator(sel).bounding_box(); gesture(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2); time.sleep(0.3)
        m = M(); check(f'{prof}: muette avant tout geste (règle autoplay)', m['paused'], m)
        pl = E('window.__nml.state.player'); pt = P(pl['x'] + 1.5, pl['z']); gesture(pt['x'], pt['y']); time.sleep(2.5)
        m1 = M(); time.sleep(1.5); m2 = M()
        check(f'{prof}: lecture effective après le premier geste (le temps avance)', not m1['paused'] and m2['t'] - m1['t'] > 1.0, (m1['t'], m2['t']))
        check(f'{prof}: activée par défaut (non coupée), en boucle, un seul lecteur', not m2['muted'] and m2['loop'] and m2['n'] == 1, m2)
        check(f'{prof}: volume extérieur', abs(m2['vol'] - 0.55) < 0.05, m2['vol'])
        # boucle : on place la tête à 1,5 s de la fin, elle doit repartir du début sans s'arrêter
        E('window.__nml.music.currentTime = window.__nml.music.duration - 1.5'); time.sleep(3.5); m3 = M()
        check(f'{prof}: boucle : repart au début après la fin, toujours en lecture', not m3['paused'] and m3['t'] < 5, (m3['t'], m3['dur']))
        # continuité entre quartiers : marche réelle jusqu'à la jonction est (Q1 -> Q2)
        E('window.__nml.music.dataset.mark = "x"'); t_before = M()['t']
        for _ in range(12):
            if E('window.__nml.state.location') == 'dusk_q2': break
            pl = E('window.__nml.state.player'); tx = min(47, pl['x'] + 6); tz = 20
            pt = P(tx, tz)
            if not (10 < pt['x'] < (1270 if prof == 'desktop' else 380) and 140 < pt['y'] < (700 if prof == 'desktop' else 740)): tx = pl['x'] + 3; pt = P(tx, tz)
            gesture(pt['x'], pt['y']); time.sleep(2.2)
        m4 = M(); same = E('window.__nml.music.dataset.mark === "x"')
        check(f'{prof}: changement de quartier par la marche : pas de coupure (même lecteur, temps continu)', E('window.__nml.state.location') == 'dusk_q2' and same and not m4['paused'] and m4['t'] > t_before, (E('window.__nml.state.location'), t_before, m4['t']))
        # coupure : bouton du style v8 (geste) ; mémorisée au rechargement
        tapel('#k-son'); m5 = M()
        check(f'{prof}: bouton Son : coupe (muted), libellé « Muet »', m5['muted'] and 'Muet' in pg.locator('#k-son').inner_text() and E("localStorage.getItem('nml_muted')") == '1', m5['muted'])
        pg.screenshot(path=OUT + f'{prof}-son-coupe.png')
        pg.reload(); pg.wait_for_function('window.__nml', timeout=60000); (pg.locator('#m-new').tap if pg.evaluate('navigator.maxTouchPoints>0') else pg.locator('#m-new').click)(); pg.wait_for_function('!document.body.classList.contains("menu-open")'); time.sleep(1.5)
        check(f'{prof}: réglage mémorisé après rechargement', M()['muted'] and 'Muet' in pg.locator('#k-son').inner_text())
        tapel('#k-son'); time.sleep(1.5); m6 = M()
        check(f'{prof}: rétabli par geste, lecture (le geste démarre la musique)', not m6['muted'] and not m6['paused'] and E("localStorage.getItem('nml_muted')") == '0', m6)
        if prof == 'desktop':
            pg.keyboard.press('s'); check('desktop: touche S coupe', M()['muted']); pg.keyboard.press('s'); check('desktop: touche S rétablit', not M()['muted'])
        # intérieur : atténuée (entrée par geste sur la porte de chez Mara)
        d = E("window.__nml.game.doorById('mara_house_door')"); pl = E('window.__nml.state.player')
        for _ in range(8):
            if E('window.__nml.game.location.kind') == 'interior': break
            pt = E(f"window.__nml.project({d['opening']['x']},1.0,{d['opening']['z']})"); gesture(pt['x'], pt['y']); time.sleep(3)
        time.sleep(3); m7 = M()
        check(f'{prof}: intérieur : musique continue et atténuée', E('window.__nml.game.location.kind') == 'interior' and not m7['paused'] and m7['vol'] < 0.3, (E('window.__nml.state.location'), m7['vol']))
        check(f'{prof}: aucune erreur page', not errs, errs[:2]); ctx.close()
    br.close()
ok = sum(r['ok'] for r in R); print(f'{ok}/{len(R)}'); json.dump(R, open(OUT + 'music_check.json', 'w'), indent=1, ensure_ascii=False)
sys.exit(0 if ok == len(R) else 1)
