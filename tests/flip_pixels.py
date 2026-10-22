# Contrôle VISUEL du miroir : on compare les pixels rendus du sprite (pas l'état interne).
# Pour chaque personnage : image isolée (même pipeline de rendu, fond magenta) face à droite puis face à gauche ;
# les deux doivent être le miroir l'une de l'autre : écart(A, miroir(B)) nettement < écart(A, B).
import sys, time, json, base64, io
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765/'
OUT = sys.argv[2] if len(sys.argv) > 2 else '/tmp/nml-test-out/flip_pixels/'; __import__('os').makedirs(OUT, exist_ok=True)
R = []
def check(n, ok, d=''): R.append({'name': n, 'ok': bool(ok), 'detail': str(d)}); print(('OK   ' if ok else 'ECHEC ') + n, d)
def grab(pg, who, dpr):
    r = pg.evaluate(f"window.__nml.view.actorRect('{who}')"); url = pg.evaluate(f"window.__nml.view.isolate('{who}')")
    im = Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB')
    return im.crop((int(r['x'] * dpr) - 4, int(r['y'] * dpr) - 4, int((r['x'] + r['w']) * dpr) + 4, int((r['y'] + r['h']) * dpr) + 4))
def content(I):
    a = np.asarray(I).astype(int); m = np.abs(a - [255, 0, 255]).sum(2) > 60; ys, xs = np.nonzero(m)
    return I.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
def mirror_score(A, B):
    A = content(A); B = content(B).resize(A.size); a = np.asarray(A).astype(float); b = np.asarray(B).astype(float); bm = b[:, ::-1]
    mask = lambda x: np.abs(x - [255, 0, 255]).sum(2) > 60
    m1 = mask(a) | mask(b); m2 = mask(a) | mask(bm)
    same = np.abs(a - b).sum(2)[m1].mean(); mir = np.abs(a - bm).sum(2)[m2].mean(); return round(same, 1), round(mir, 1)
def aligned_score(A, B, r=4):
    # v12 : même seuil, mesure fiabilisée. Le PNJ respire (rebond) et son sprite tombe sur une grille de pixels différente
    # entre les deux instants : on compare au meilleur recalage (±r px), pour l'image directe COMME pour l'image miroir.
    A = content(A); B = content(B); W, H = max(A.width, B.width) + 2 * r, max(A.height, B.height) + 2 * r
    def pad(I, dx=0, dy=0):
        c = Image.new('RGB', (W, H), (255, 0, 255)); c.paste(I, (r + dx, r + dy)); return np.asarray(c).astype(float)
    a = pad(A); mask = lambda x: np.abs(x - [255, 0, 255]).sum(2) > 60
    def best(I):
        out = 1e9
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                b = pad(I, dx, dy); m = mask(a) | mask(b); out = min(out, np.abs(a - b).sum(2)[m].mean())
        return out
    return round(best(B), 1), round(best(B.transpose(Image.FLIP_LEFT_RIGHT)), 1)
def shot(pg, who, path, dpr):
    r = pg.evaluate(f"window.__nml.view.actorRect('{who}')"); pad = 30
    pg.screenshot(path='/tmp/_full.png'); im = Image.open('/tmp/_full.png')
    im.crop((int(r['x'] * dpr) - pad, int(r['y'] * dpr) - pad, int((r['x'] + r['w']) * dpr) + pad, int((r['y'] + r['h']) * dpr) + pad)).save(path)
def pair(a, b, path, la, lb):
    from PIL import ImageDraw
    A, B = Image.open(a), Image.open(b); W = Image.new('RGB', (A.width + B.width + 20, max(A.height, B.height) + 30), '#111')
    W.paste(A, (0, 30)); W.paste(B, (A.width + 20, 30)); d = ImageDraw.Draw(W); d.text((4, 8), la, fill='#fff'); d.text((A.width + 24, 8), lb, fill='#fff'); W.save(path)
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for prof in ['desktop', 'mobile']:
        dpr = 1 if prof == 'desktop' else 2
        ctx = br.new_context(viewport={'width': 1280, 'height': 800}) if prof == 'desktop' else br.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2)
        pg = ctx.new_page(); pg.goto(URL); pg.wait_for_function('window.__nml'); [(pg.locator(_s).tap if pg.evaluate('navigator.maxTouchPoints>0') else pg.locator(_s).click)() for _s in ('#m-new', '#cr-next', '#cr-enter')]; pg.wait_for_function('!document.body.classList.contains("menu-open")'); time.sleep(2.5)
        gesture = pg.touchscreen.tap if prof == 'mobile' else pg.mouse.click
        def walk(x, z):
            pt = pg.evaluate(f'window.__nml.project({x},0,{z})'); gesture(pt['x'], pt['y']); time.sleep(0.3)
            pg.wait_for_function('window.__nml.state.player.path.length===0', timeout=20000); time.sleep(0.8)
        s = pg.evaluate('window.__nml.state.player')
        walk(s['x'] + 5, s['z'])   # vers la droite de l'écran
        A = {w: grab(pg, w, dpr) for w in ['player']}; shot(pg, 'player', f'/tmp/{prof}_pR.png', dpr)
        walk(s['x'] + 1, s['z'])   # vers la gauche
        B = {w: grab(pg, w, dpr) for w in ['player']}; shot(pg, 'player', f'/tmp/{prof}_pL.png', dpr)
        check(f'{prof}: Nilo absent (0 pixel rendu)', (lambda u: 0 if not u else int((abs(__import__('numpy').asarray(__import__('PIL.Image',fromlist=['Image']).open(__import__('io').BytesIO(__import__('base64').b64decode(u.split(',')[1]))).convert('RGB')).astype(int)-[255,0,255]).sum(2)>90).sum()))(pg.evaluate("window.__nml.view.isolate('companion')")) == 0)
        for w in ['player']:
            same, mir = mirror_score(A[w], B[w]); check(f'{prof}: {w} image rendue en miroir (droite vs gauche)', mir < 0.6 * same, f'écart direct {same}, écart miroir {mir}')
        if prof == 'desktop':
            pair(f'/tmp/{prof}_pR.png', f'/tmp/{prof}_pL.png', OUT + 'joueur-droite-vs-gauche.png', 'marche vers la droite', 'marche vers la gauche')
            A['player'].save(OUT + 'isole-joueur-droite.png'); B['player'].save(OUT + 'isole-joueur-gauche.png')
        # PNJ : Vera regarde l'armoire (à droite) puis se tourne vers le joueur pendant le dialogue
        pg.evaluate("(()=>{const g=window.__nml.game,d=g.doorById('clinic_door');Object.assign(g.state.player,{x:d.threshold.x,z:d.threshold.z,path:[]});Object.assign(g.state.companion,{x:d.threshold.x+1,z:d.threshold.z,path:[]});g.useDoor('clinic_door')})()")
        pg.wait_for_function('window.__nml.state.location==="clinic_in"'); time.sleep(1.0)
        V0 = grab(pg, 'vera', dpr); f0 = pg.evaluate("window.__nml.view.facingOf('vera')"); shot(pg, 'vera', f'/tmp/{prof}_v0.png', dpr)
        pg.evaluate("window.__nml.game.talkTo('vera')"); pg.wait_for_function('window.__nml.state.dialogue', timeout=20000); time.sleep(0.8)
        V1 = grab(pg, 'vera', dpr); f1 = pg.evaluate("window.__nml.view.facingOf('vera')"); shot(pg, 'vera', f'/tmp/{prof}_v1.png', dpr)
        same, mir = aligned_score(V0, V1)
        check(f'{prof}: Vera tournée vers le joueur, image rendue en miroir', f0 != f1 and mir < 0.6 * same, f'sens {f0}->{f1}, écart direct {same}, écart miroir {mir}')
        if prof == 'desktop':
            pg.screenshot(path=OUT + 'desktop-pnj-face-au-joueur.png'); pair(f'/tmp/{prof}_v0.png', f'/tmp/{prof}_v1.png', OUT + 'vera-repos-vs-dialogue.png', 'Vera au repos', 'Vera face au joueur')
        # animation : le rendu bouge pendant la marche (rebond), pas d'à-coups excessifs
        pg.evaluate("window.__nml.game.closeDialogue()")
        ys = []
        pg.evaluate("window.__nml.game.moveTo(1.5,1.5)")
        for _ in range(12): ys.append(pg.evaluate("window.__nml.view.actorRect('player').y")); time.sleep(0.05)
        check(f'{prof}: rebond de marche visible et léger', 0 < max(ys) - min(ys) < 60, f'amplitude écran {round(max(ys)-min(ys),1)} px (inclut le déplacement)')
        ctx.close()
    br.close()
json.dump(R, open(OUT + 'resultats-miroir.json', 'w'), ensure_ascii=False, indent=1)
print(sum(r['ok'] for r in R), '/', len(R))
