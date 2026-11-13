# Cinématique d'ouverture + OST du menu (13/11, demande de Valentin) : séquence cinématique -> Terminal.
# La cinématique est sautée pour un navigateur piloté (tous les autres tests) ; ici on la force avec ?intro=1.
# 1. fichiers servis identiques à l'octet (sha256) : assets/video/cinematique_ouverture.mp4, assets/audio/ost_menu/01_ost_menu.mp3
# 2. autoplay refusé : première image noire (pas de Terminal, pas d'invite tant que play() n'a pas répondu), invite « TOUCHER POUR COMMENCER »,
#    rien ne joue ; le geste lance la vidéo AVEC son ; « PASSER » ; Échap / Entrée / Espace / clic / tap passent ; fondu noir ; Terminal allumé depuis le noir ;
#    OST du menu en boucle, volume et muet respectés ; aucun geste de la cinématique ne traverse vers le menu
# 3. autoplay permis : pas d'invite, fin naturelle, voile noir sur les 0,6 dernières secondes, puis Terminal + OST
# 4. vidéo en échec (404) : Terminal tout de suite, OST au premier geste
# 5. pas de rejeu en session : Continuer -> jeu -> pause -> QUITTER : pas de cinématique, OST du menu reprend ; rechargement : la cinématique revient
# 6. mouvement réduit : cinématique gardée, passable
# 7. bandes noires (contain) et captures 1280 / 390 / fold plié 412 / déplié 884 : invite, lecture, transition, Terminal
# Captures : OUT (défaut /tmp/nml-test-out/cinematique/), sélection 1x légère dans OUT/livraison/.
import os, sys, time, json, re, hashlib, urllib.request
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8915/')
if not URL.endswith('/') and '?' not in URL: URL += '/'
OUT = os.environ.get('OUT', '/tmp/nml-test-out/cinematique/'); os.makedirs(OUT + 'livraison/', exist_ok=True)
SHA = {'assets/video/cinematique_ouverture.mp4': 'd3ba44185f2e213a03f6bd312c7fc34f306a93669ccae755e167e42bda33de66',
       'assets/audio/ost_menu/01_ost_menu.mp3': '2fb43a976c5fb21e451de9f25a62d43783e42edf992d5543752b29f2532287db'}
R = []
def ok(c, n, d=''): R.append((bool(c), n)); print(('OK   ' if c else 'ECHEC ') + n + ('' if c else f'  {str(d)[:400]}'), flush=True)
BASE = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']
GESTE_REQUIS, AUTOPLAY = BASE + ['--autoplay-policy=user-gesture-required'], BASE + ['--autoplay-policy=no-user-gesture-required']
QI = ('&' if '?' in URL else '?') + 'intro=1'
FORMATS = [('1280x800', 1280, 800, False), ('390x844', 390, 844, True), ('fold_plie_412x915', 412, 915, True), ('fold_deplie_884x1104', 884, 1104, True)]
if os.environ.get('FORMATS'): FORMATS = [f for f in FORMATS if f[0] in os.environ['FORMATS'].split(',')]
ETAT = """() => { const v = document.getElementById('intro-video'), a = document.getElementById('music'), I = document.getElementById('intro'), M = document.getElementById('menu');
  const vis = s => { const e = document.querySelector(s); if (!e) return false; const cs = getComputedStyle(e), r = e.getBoundingClientRect(); return !e.hidden && cs.display !== 'none' && cs.visibility !== 'hidden' && +cs.opacity > 0.05 && r.width > 0; };
  return { intro: Object.assign({}, window.__nmlIntro || {}), present: !!I, cls: I ? I.className : null, vis: document.visibilityState, introVis: vis('#intro'), invite: vis('#intro-invite'), passer: vis('#intro-passer'),
    voile: I ? +getComputedStyle(document.getElementById('intro-voile')).opacity : null, actif: !!window.__nmlIntroActive,
    v: v ? { t: v.currentTime, paused: v.paused, muted: v.muted, vol: v.volume, d: v.duration, vw: v.videoWidth, vh: v.videoHeight, fit: getComputedStyle(v).objectFit, inline: v.playsInline,
      r: (r => [r.left, r.top, r.width, r.height].map(Math.round))(v.getBoundingClientRect()) } : null,
    a: { src: a.currentSrc || a.src, paused: a.paused, loop: a.loop, muted: a.muted, vol: +a.volume.toFixed(3), t: a.currentTime },
    menuPret: !!window.__nmlMenuPret, boot: M.dataset.boot || 'repos', booting: M.classList.contains('booting'), menuVis: !M.hidden,
    creation: !document.getElementById('creation').hidden, shell: !!(window.__nml && window.__nml.shell), mode: window.__nml && window.__nml.musique ? window.__nml.musique.mode : null }; }"""

def ctx_de(br, w, h, mob, reduit=False, init=None):
    ctx = br.new_context(viewport={'width': w, 'height': h}, has_touch=mob, is_mobile=mob, device_scale_factor=2 if mob else 1, reduced_motion='reduce' if reduit else 'no-preference')
    if init: ctx.add_init_script(init)
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append('JS ' + str(e)))
    pg.on('response', lambda r: r.status >= 400 and '/cinematique_ouverture.mp4' not in r.url and errs.append(f'{r.status} {r.url}'))
    return ctx, pg, errs

def attendre(pg, js, t=20):
    try: pg.wait_for_function(js, timeout=t * 1000, polling=100); return True
    except Exception: return False

def geste(pg, mob, x=None, y=None):
    vp = pg.viewport_size; x = vp['width'] / 2 if x is None else x; y = vp['height'] / 2 if y is None else y
    (pg.touchscreen.tap if mob else pg.mouse.click)(x, y)

def bandes(path, w, h, vw=1280, vh=720):
    """Vérifie la mise en contain sur la capture : bandes noires hors du rectangle vidéo attendu, image claire dedans."""
    from PIL import Image
    im = Image.open(path).convert('L'); sx = im.width / w
    k = min(w / vw, h / vh); dw, dh = vw * k, vh * k; x0, y0 = (w - dw) / 2, (h - dh) / 2
    def moy(box): c = im.crop(tuple(int(v * sx) for v in box)); px = list(c.get_flattened_data() if hasattr(c, 'get_flattened_data') else c.getdata()); return sum(px) / max(1, len(px))
    hors = []
    if y0 > 6: hors += [moy((0, 0, w, y0 - 3)), moy((0, y0 + dh + 3, w, h))]
    if x0 > 6: hors += [moy((0, 0, x0 - 3, h)), moy((x0 + dw + 3, 0, w, h))]
    dedans = moy((x0 + dw * .1, y0 + dh * .1, x0 + dw * .9, y0 + dh * .9))
    return {'rect': [round(x0), round(y0), round(dw), round(dh)], 'hors': [round(v, 1) for v in hors], 'dedans': round(dedans, 1),
            'ok': all(v < 12 for v in hors) and dedans > 40}

def livrer(src, nom):
    from PIL import Image
    im = Image.open(src).convert('RGB'); vp = im.size
    if im.width > 1400: im = im.resize((im.width // 2, im.height // 2))
    elif im.width >= 700 and im.height > 1500: im = im.resize((im.width // 2, im.height // 2))
    im.save(OUT + 'livraison/' + nom.replace('.png', '.jpg'), quality=84)

# 1. hash des fichiers servis (processus parent seulement)
for chemin, h in ([] if os.environ.get('SCEN') else SHA.items()):
    try: got = hashlib.sha256(urllib.request.urlopen(URL.split('?')[0] + chemin, timeout=120).read()).hexdigest()
    except Exception as e: got = str(e)
    ok(got == h, f'servi identique à l\'octet : {chemin}', got)

def sc_formats(p):
    # 2. autoplay refusé, par format : invite, geste, lecture avec son, passage, Terminal, OST
    br = p.chromium.launch(channel='chrome', args=GESTE_REQUIS)
    for i, (nom, w, h, mob) in enumerate(FORMATS):
        P = f'[{nom}]'
        ctx, pg, errs = ctx_de(br, w, h, mob, init="window.__premier = new Promise(r => requestAnimationFrame(() => { const M = document.getElementById('menu'), I = document.getElementById('intro'); r({ intro: !!I && getComputedStyle(I).display !== 'none', z: I ? +getComputedStyle(I).zIndex : 0, fond: I ? getComputedStyle(I).backgroundColor : '' }); }));" if nom == '1280x800' else None)
        pg.goto(URL + QI, wait_until='domcontentloaded')
        if nom == '1280x800':
            pr = pg.evaluate('window.__premier'); ok(pr['intro'] and pr['z'] >= 90 and pr['fond'] in ('rgb(0, 0, 0)',), f'{P} première image : calque noir de la cinématique au-dessus de tout (pas de Terminal)', pr)
        ok(attendre(pg, "window.__nmlIntro && window.__nmlIntro.etat === 'invite'", 15), f'{P} autoplay refusé : invite affichée', pg.evaluate(ETAT))
        time.sleep(1.2); e = pg.evaluate(ETAT); pg.screenshot(path=f'{OUT}{nom}_1_invite.png')
        ok(e['invite'] and not e['passer'] and e['v']['paused'] and e['a']['paused'] and not e['menuPret'] and e['actif'], f'{P} invite seule sur noir : vidéo et musique arrêtées, Terminal pas encore allumé', e)
        if nom == '1280x800':  # une touche quelconque sans activation n'affiche rien d'autre ; le menu ne voit rien
            pg.keyboard.press('x'); time.sleep(0.3)
        geste(pg, mob)
        ok(attendre(pg, "window.__nmlIntro.etat === 'lecture' && document.getElementById('intro-video').currentTime > 0.3", 20), f'{P} le premier geste lance la vidéo', pg.evaluate(ETAT))
        time.sleep(0.3); e = pg.evaluate(ETAT)
        ok(not e['v']['muted'] and e['v']['vol'] == 1 and not e['v']['paused'] and e['intro'].get('mode') == 'geste' and e['v']['inline'], f'{P} lecture avec son (muted=false, volume 1), inline', e['v'])
        ok(e['passer'] and not e['invite'] and e['voile'] < 0.05, f'{P} « PASSER » visible, voile d\'entrée levé', e)
        ok(e['a']['paused'], f'{P} pas d\'OST pendant la cinématique', e['a'])
        ok(e['v']['fit'] == 'contain' and e['v']['r'] == [0, 0, w, h] and e['v']['vw'] == 1280 and e['v']['vh'] == 720, f'{P} vidéo plein écran en contain, 1280×720 natif', e['v'])
        while pg.evaluate("document.getElementById('intro-video').currentTime") < 4.0: time.sleep(0.05)
        pg.screenshot(path=f'{OUT}{nom}_2_lecture.png'); b = bandes(f'{OUT}{nom}_2_lecture.png', w, h)
        ok(b['ok'], f'{P} bandes noires correctes autour de l\'image (jamais d\'étirement)', b)
        e = pg.evaluate(ETAT); x = pg.evaluate("[document.getElementById('m-exec').textContent, document.getElementById('menu').classList.contains('t-charge'), document.getElementById('menu').dataset.boot || '']")
        ok(not e['creation'] and not x[0] and not x[1] and x[2] in ('', 'b-off'), f'{P} aucun geste de la cinématique n\'a traversé vers le menu (pas de choix, allumage pas commencé)', [e, x])
        # passage : touche (bureau : Échap ; fold déplié : Espace ; 390 : tap ; fold plié : Entrée)
        how = {'1280x800': 'Escape', '390x844': 'tap', 'fold_plie_412x915': 'Enter', 'fold_deplie_884x1104': 'Space'}.get(nom, 'tap')
        t0 = time.time()
        if how == 'tap': geste(pg, mob)
        else: pg.keyboard.press(how)
        time.sleep(0.2); pg.screenshot(path=f'{OUT}{nom}_3_fondu.png'); e = pg.evaluate(ETAT)
        ok(e['intro'].get('etat') in ('fondu', 'fini') and e['intro'].get('fin') == 'passee', f'{P} {how} passe la cinématique (fondu au noir)', e['intro'])
        ok(attendre(pg, "!document.getElementById('intro') && window.__nmlMenuPret === true", 5), f'{P} fondu puis Terminal (calque retiré)', pg.evaluate(ETAT))
        dt = time.time() - t0; time.sleep(0.25); pg.screenshot(path=f'{OUT}{nom}_4_terminal_depuis_noir.png'); e = pg.evaluate(ETAT)
        ok(dt < 1.6 and (e['booting'] or e['boot'] != 'repos'), f'{P} le Terminal s\'allume depuis le noir ({dt:.2f} s après le geste)', e)
        ok(attendre(pg, "!document.getElementById('music').paused && document.getElementById('music').currentTime > 0.2", 10), f'{P} l\'OST du menu démarre après le fondu', pg.evaluate(ETAT))
        e = pg.evaluate(ETAT)
        ok('/assets/audio/ost_menu/01_ost_menu.mp3' in e['a']['src'] and e['a']['loop'] and abs(e['a']['vol'] - 0.55) < 0.06 and not e['a']['muted'], f'{P} OST du menu : bon fichier, en boucle, volume 0,55', e['a'])
        ok(not e['creation'], f'{P} le geste qui passe ne choisit rien dans le menu', e)
        time.sleep(2.2); pg.screenshot(path=f'{OUT}{nom}_5_terminal.png')
        ok(not errs, f'{P} aucune erreur JS / réseau', errs[:3]); ctx.close()
    br.close()

def sc_reglages(p):
    br = p.chromium.launch(channel='chrome', args=GESTE_REQUIS)
    # 2b. réglages son : musique à 40 % et muet mémorisé, OST qui reboucle
    ctx, pg, errs = ctx_de(br, 1280, 800, False, init="localStorage.setItem('nml_options', JSON.stringify({ v: 1, music: 40 })); localStorage.setItem('nml_muted', '1');")
    pg.goto(URL + QI); attendre(pg, "window.__nmlIntro && window.__nmlIntro.etat === 'invite'", 15); time.sleep(1.0); geste(pg, False)
    attendre(pg, "window.__nmlIntro.etat === 'lecture'", 20); time.sleep(0.8); pg.keyboard.press('Enter')
    attendre(pg, "!document.getElementById('intro') && !document.getElementById('music').paused", 10); time.sleep(0.6); e = pg.evaluate(ETAT)
    ok(e['a']['muted'] and abs(e['a']['vol'] - 0.22) < 0.04, 'réglages respectés : muet mémorisé, musique à 40 % (0,22)', e['a'])
    attendre(pg, 'window.__nml && window.__nml.shell', 120)
    attendre(pg, 'isFinite(window.__nml.music.duration) && window.__nml.music.duration > 60', 30)
    pg.evaluate("localStorage.setItem('nml_muted', '0'); document.getElementById('music').muted = false; window.__nml.music.currentTime = window.__nml.music.duration - 1.2")
    time.sleep(2.6); e = pg.evaluate(ETAT)
    ok(not e['a']['paused'] and e['a']['t'] < 5 and e['a']['loop'] and e['mode'] == 'menu', 'OST du menu en boucle (reprend au début après la fin)', e)
    ok(not errs, 'réglages : aucune erreur', errs[:3]); ctx.close()
    br.close()

def sc_echec(p):
    br = p.chromium.launch(channel='chrome', args=GESTE_REQUIS)
    # 4. vidéo en échec : Terminal tout de suite, OST au premier geste
    ctx, pg, errs = ctx_de(br, 1280, 800, False)
    pg.route(re.compile(r'.*/cinematique_ouverture\.mp4.*'), lambda r: r.fulfill(status=404, body='absent'))
    t0 = time.time(); pg.goto(URL + QI)
    ok(attendre(pg, "!document.getElementById('intro') && window.__nmlIntro.fin === 'erreur'", 10), 'vidéo en échec (404) : on saute au Terminal', pg.evaluate(ETAT))
    ok(attendre(pg, 'window.__nmlMenuPret === true', 30), f'vidéo en échec : Terminal prêt ({time.time() - t0:.1f} s)', pg.evaluate(ETAT))
    time.sleep(0.5); pg.mouse.click(5, 5); time.sleep(0.8); e = pg.evaluate(ETAT)
    ok(not e['a']['paused'] and 'ost_menu' in e['a']['src'], 'vidéo en échec : OST du menu au premier geste', e['a'])
    ok(not errs, 'vidéo en échec : aucune autre erreur', errs[:3]); ctx.close()
    br.close()

def sc_reduit(p):
    br = p.chromium.launch(channel='chrome', args=GESTE_REQUIS)
    # 6. mouvement réduit : gardée, passable (Espace)
    ctx, pg, errs = ctx_de(br, 390, 844, True, reduit=True)
    pg.goto(URL + QI); ok(attendre(pg, "window.__nmlIntro && window.__nmlIntro.etat === 'invite'", 15), 'mouvement réduit : cinématique gardée (invite)')
    time.sleep(1.0); geste(pg, True); ok(attendre(pg, "window.__nmlIntro.etat === 'lecture'", 20), 'mouvement réduit : lecture au geste')
    time.sleep(0.8); pg.keyboard.press(' ')
    ok(attendre(pg, "!document.getElementById('intro') && window.__nmlMenuPret === true", 5), 'mouvement réduit : Espace passe, Terminal (allumage sauté par le mode réduit)', pg.evaluate(ETAT))
    ok(not errs, 'mouvement réduit : aucune erreur', errs[:3]); ctx.close()
    br.close()

def sc_autoplay(p):
    # 3. autoplay permis : pas d'invite, fin naturelle avec voile noir sur la fin, puis Terminal + OST
    br = p.chromium.launch(channel='chrome', args=AUTOPLAY)
    ctx, pg, errs = ctx_de(br, 1280, 800, False)
    pg.goto(URL + QI)
    ok(attendre(pg, "window.__nmlIntro && window.__nmlIntro.etat === 'lecture'", 20), 'autoplay permis : lecture directe, sans invite', pg.evaluate(ETAT))
    e = pg.evaluate(ETAT); ok(not e['intro'].get('invite') and e['intro'].get('mode') == 'autoplay' and not e['v']['muted'], 'autoplay permis : mode autoplay, avec son', e)
    voile = []
    while True:
        e = pg.evaluate(ETAT)
        if not e['present']: break
        if e['v'] and e['v']['d'] and e['v']['t'] > 1: voile.append((round(e['v']['t'], 2), round(e['voile'], 2)))
        if e['v'] and e['v']['t'] > 12.45 and not os.path.exists(OUT + 'autoplay_fondu_fin.png'): pg.screenshot(path=OUT + 'autoplay_fondu_fin.png')
        time.sleep(0.05)
        if len(voile) > 600: break
    avant = [o for t, o in voile if 2 <= t < 12.1]; fin = [o for t, o in voile if t >= 12.6]
    ok(avant and max(avant) < 0.05 and fin and max(fin) > 0.6, 'fin naturelle : image nette jusqu\'à ~12,2 s, voile noir sur les 0,6 dernières secondes', voile[-12:])
    e = pg.evaluate(ETAT); ok(e['intro'].get('fin') == 'naturelle', 'fin naturelle consignée', e['intro'])
    ok(attendre(pg, "window.__nmlMenuPret === true && !document.getElementById('music').paused", 10), 'fin naturelle : Terminal puis OST du menu', pg.evaluate(ETAT))
    time.sleep(0.2); pg.screenshot(path=OUT + 'autoplay_terminal_apres_fin.png')
    ok(not errs, 'autoplay : aucune erreur', errs[:3]); ctx.close()
    br.close()

def sc_session(p):
    # 5. pas de rejeu en session ; rejeu au rechargement (vraie partie : sauvegarde Center-Town écrite par le jeu, Continuer)
    br = p.chromium.launch(channel='chrome', args=GESTE_REQUIS)
    ctx, pg, errs = ctx_de(br, 1280, 800, False)
    pg.goto(URL); attendre(pg, 'window.__nml && window.__nml.shell', 120)  # sans ?intro=1 : navigateur piloté, cinématique sautée
    etat = pg.evaluate("""() => { const N = window.__nml, d = N.doors.find(d => d.id === 'c_ouest'), s = JSON.parse(JSON.stringify(N.game.snapshot()));
      s.location = 'steel_center'; Object.assign(s.player, { x: d.threshold.x + 3, z: d.threshold.z, path: [], pending: null }); return s; }""")
    ok(pg.evaluate("window.__nmlIntro && window.__nmlIntro.fin === 'absente' && !document.getElementById('intro')"), 'navigateur piloté sans ?intro=1 : cinématique sautée (autres suites inchangées)')
    ctx.close()
    save = {'v': 2, 't': int(time.time() * 1000), 'label': 'Steel-Megalopolis · Center-Town', 'state': etat}
    ctx, pg, errs = ctx_de(br, 1280, 800, False, init="if (!sessionStorage.getItem('_seed')) { localStorage.setItem('nml_save_auto', %s); sessionStorage.setItem('_seed', '1'); }" % json.dumps(json.dumps(save)))
    pg.goto(URL + QI); attendre(pg, "window.__nmlIntro && window.__nmlIntro.etat === 'invite'", 15); time.sleep(1.0); geste(pg, False); attendre(pg, "window.__nmlIntro.etat === 'lecture'", 20)
    time.sleep(0.8); pg.keyboard.press('Escape')  # > anti-rebond de 450 ms après le geste qui a lancé la vidéo
    ok(attendre(pg, '!document.getElementById("intro") && window.__nmlMenuPret === true', 5), 'session : Échap passe la cinématique', pg.evaluate(ETAT)['intro'])
    attendre(pg, 'window.__nml && window.__nml.shell', 120); pg.evaluate('window.__nml.shell.terminal.saute()'); time.sleep(0.4)  # allumage sauté (comme passer_boot)
    t0 = time.time(); bb = pg.locator('#m-continue').bounding_box()
    pg.mouse.click(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2)
    ok(attendre(pg, "window.__nml && window.__nml.shell && !window.__nml.shell.isOpen() && window.__nml.state.location === 'steel_center'", 120),
       f'Continuer rapide après la cinématique : en jeu à Center-Town ({time.time() - t0:.1f} s)', pg.evaluate("[window.__nml.shell.mode, window.__nml.state.location, document.getElementById('menu').className, document.getElementById('m-continue').disabled, (window.__nmlRaf = 0, requestAnimationFrame(() => window.__nmlRaf = 1), 0)]"))
    ok(attendre(pg, "window.__nml.musique.mode === 'ost_center_town' && !window.__nml.music.paused", 15), 'en jeu : la musique du lieu reprend la main (OST Center-Town)', pg.evaluate(ETAT)['mode'])
    pg.keyboard.press('Escape'); time.sleep(0.6)
    ok(pg.evaluate("window.__nml.shell.mode") == 'pause' and pg.evaluate(ETAT)['mode'] == 'ost_center_town', 'menu pause : musique du lieu gardée', pg.evaluate(ETAT)['mode'])
    pg.evaluate("document.getElementById('m-quit').click()"); time.sleep(1.2); e = pg.evaluate(ETAT)
    ok(not e['present'] and e['intro'].get('fin') == 'passee' and e['menuVis'] and pg.evaluate("window.__nml.shell.mode") == 'title', 'QUITTER -> écran titre : pas de cinématique rejouée', e)
    ok(attendre(pg, "window.__nml.musique.mode === 'menu' && /ost_menu/.test(window.__nml.music.currentSrc) && !window.__nml.music.paused", 10), 'écran titre : l\'OST du menu reprend', pg.evaluate(ETAT)['a'])
    pg.reload(); ok(attendre(pg, "window.__nmlIntro && window.__nmlIntro.etat === 'invite' && !!document.getElementById('intro')", 15), 'nouveau lancement de la page : la cinématique revient')
    ok(not errs, 'session : aucune erreur', errs[:3]); ctx.close()
    br.close()

SCENARIOS = ['formats', 'reglages', 'echec', 'reduit', 'autoplay', 'session']
if os.environ.get('SCEN'):  # un scénario, dans ce processus
    with sync_playwright() as p:
        for n in os.environ['SCEN'].split(','): globals()['sc_' + n](p)
    print('RES', json.dumps(R)); sys.exit(0)
# Chaque scénario dans son propre processus et son propre navigateur (enchaîner les navigateurs dans un même pilote Playwright
# finit par figer les rendus sous swiftshader ; isolé, chaque scénario est déterministe).
import subprocess
for n in SCENARIOS:
    if os.environ.get('SAUF') and n in os.environ['SAUF'].split(','): continue
    for f in ([x[0] for x in FORMATS] if n == 'formats' else [None]):
        env = {**os.environ, 'SCEN': n, **({'FORMATS': f} if f else {})}
        r = subprocess.run([sys.executable, __file__], env=env, capture_output=True, text=True, timeout=900)
        sys.stdout.write(''.join(l + '\n' for l in r.stdout.splitlines() if not l.startswith('RES '))); sys.stdout.flush()
        res = [l for l in r.stdout.splitlines() if l.startswith('RES ')]
        if res: R.extend(tuple(x) for x in json.loads(res[-1][4:]))
        else: ok(False, f'scénario {n} {f or ""} : terminé sans résultat', r.stderr[-800:])

# sélection livrable 1x
if os.environ.get('SCEN'): sys.exit(0)
for nom, w, h, mob in FORMATS:
    for k in ('1_invite', '2_lecture', '3_fondu', '4_terminal_depuis_noir'):
        f = f'{OUT}{nom}_{k}.png'
        if os.path.exists(f): livrer(f, f'{nom}_{k}.png')
for f in ('autoplay_fondu_fin.png',):
    if os.path.exists(OUT + f): livrer(OUT + f, f)
n = sum(1 for c, _ in R if c); print(f'{n}/{len(R)} OK'); print('ECHECS', len(R) - n); sys.exit(0 if n == len(R) else 1)
