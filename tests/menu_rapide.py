# Menu principal « Terminal Human Corp » (docs/ui/MENU_TERMINAL.md, docs/ui/MENU_TERMINAL_IMPL.md) : contrôle rapide multi-formats.
# Chargement sans erreur JS ni 404, allumage joué puis sauté (touche / tap), six choix visibles et non recouverts, navigation clavier,
# nouvelle partie jusqu'en jeu (menu en pause, aucune animation), prefers-reduced-motion, onglet caché. Captures + séquence GIF du boot (1280).
import os, sys, time, json
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8921/'); OUT = os.environ.get('OUT', '/tmp/nml-test-out/menu_terminal/'); os.makedirs(OUT, exist_ok=True)
FORMATS = [  # (nom, largeur, hauteur, mobile, mode attendu)
    ('1920x1080', 1920, 1080, False, 'paysage'), ('1280x800', 1280, 800, False, 'paysage'), ('390x844', 390, 844, True, 'portrait'),
    ('360x780', 360, 780, True, 'plein'), ('fold_plie_412x915', 412, 915, True, 'portrait'), ('fold_deplie_884x1104', 884, 1104, True, 'portrait')]
if os.environ.get('FORMATS'): FORMATS = [f for f in FORMATS if f[0] in os.environ['FORMATS'].split(',')]
SIX = ['m-continue', 'm-new', 'm-load', 'm-options', 'm-credits', 'm-quit']
R = []; R_TAMPON = {}
def ok(c, n, d=''): R.append((bool(c), n)); print(('OK   ' if c else 'ECHEC ') + n + ('' if c else f'  {d}'), flush=True)
ETAT = "window.__nml.shell.terminal.etat()"
ANIMS = "document.getAnimations().filter(a => a.playState === 'running' && a.effect && a.effect.target && a.effect.target.closest && a.effect.target.closest('#menu')).length"
CHOIX = """(ids) => { const t = document.getElementById('t-tampon'), tr = t.getBoundingClientRect(), tv = getComputedStyle(t).opacity > 0.05 && !t.classList.contains('t-cache');
  const sc = document.getElementById('t-screen').getBoundingClientRect(), tk = document.querySelector('#menu .t-ticker').getBoundingClientRect(), st = document.querySelector('#menu .t-status').getBoundingClientRect();
  const inter = (a, b) => a.left < b.right - 0.5 && a.right > b.left + 0.5 && a.top < b.bottom - 0.5 && a.bottom > b.top + 0.5;
  return ids.map(id => { const e = document.getElementById(id), r = e.getBoundingClientRect(), cs = getComputedStyle(e);
    const pts = [[.5, .5], [.15, .5], [.85, .5], [.5, .2], [.5, .8]].map(([fx, fy]) => { const el = document.elementFromPoint(r.left + r.width * fx, r.top + r.height * fy); return !!el && (el === e || e.contains(el)); });
    return { id, w: r.width, h: r.height, vis: !e.hidden && cs.display !== 'none' && cs.visibility !== 'hidden' && +cs.opacity > 0.4,
      dansEcran: r.left >= sc.left - 1 && r.right <= sc.right + 1 && r.top >= sc.top - 1 && r.bottom <= sc.bottom + 1 && r.top >= 0 && r.bottom <= innerHeight,
      dessus: pts.every(Boolean), tampon: tv && inter(r, tr), ticker: inter(r, tk), statut: inter(r, st), z: [cs.zIndex] }; }); }"""
# Tampon : jamais sur un choix, le bandeau, la version ni le statut, avec 24 px de marge (canevas de base × échelle --k)
MARGE = """() => { const t = document.getElementById('t-tampon'), tr = t.getBoundingClientRect(), cs = getComputedStyle(t);
  const vis = +cs.opacity > 0.05 && !t.classList.contains('t-cache') && tr.width > 0, k = +getComputedStyle(document.getElementById('menu')).getPropertyValue('--k') || 1, m = 24 * k;
  const cibles = [...document.querySelectorAll('#menu .t-list button:not([hidden])'), document.querySelector('#menu .t-ticker'), document.getElementById('m-version'), ...document.querySelectorAll('#menu .t-status span')];
  const touche = cibles.filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && r.left - m < tr.right && r.right + m > tr.left && r.top - m < tr.bottom && r.bottom + m > tr.top; }).map(e => e.id || e.className || e.textContent.slice(0, 20));
  return { vis, echelle: t.dataset.echelle, w: Math.round(tr.width), h: Math.round(tr.height), x: Math.round(tr.left), y: Math.round(tr.top), marge: +m.toFixed(1), touche }; }"""
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    def ouvre(w, h, mob, reduit=False):
        ctx = br.new_context(viewport={'width': w, 'height': h}, has_touch=mob, is_mobile=mob, device_scale_factor=2 if mob else 1, reduced_motion='reduce' if reduit else 'no-preference')
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append('JS ' + str(e))); pg.on('response', lambda r: r.status >= 400 and errs.append(f'{r.status} {r.url}'))
        pg.on('console', lambda m: m.type == 'error' and errs.append('console ' + m.text))
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell && window.__nml.shell.terminal', timeout=90000)
        return ctx, pg, errs
    for nom, w, h, mob, attendu in FORMATS:
        ctx, pg, errs = ouvre(w, h, mob); E = pg.evaluate; P = f'{nom} :'
        E("window.__nml.shell.terminal.pret"); time.sleep(0.3)
        et = E(ETAT); ok(et['mode'] == attendu, f'{P} variante de cadre « {attendu} »', et)
        if attendu != 'plein':
            g = E("(()=>{const c=document.getElementById('t-cadre').getBoundingClientRect();return {w:c.width,h:c.height}})()")
            ratio = (1920 / 1080) if attendu == 'paysage' else (1080 / 1920)
            ok(abs(g['w'] / g['h'] - ratio) < 0.01 and (abs(g['w'] - w) < 1 or abs(g['h'] - h) < 1), f'{P} cadre en contain uniforme (aucun étirement)', g)
        else:
            ok(E("document.getElementById('t-cadre').hidden") and E("(()=>{const r=document.getElementById('t-screen').getBoundingClientRect();return r.width>=innerWidth-1&&r.height>=innerHeight-1})()"), f'{P} repli : pas de cadre métal, écran plein cadre')
        # 1. l'allumage se joue
        if not E(ETAT)['booting']: E("window.__nml.shell.terminal.rejouer()")
        time.sleep(2.6); b = E("[document.getElementById('t-boot').textContent, window.__nml.shell.terminal.etat()]")
        ok(b[1]['booting'] and len(b[0]) > 10 and b[0].startswith('HUMAN CORP'), f'{P} allumage en cours (journal tapé)', b)
        pg.screenshot(path=f'{OUT}{nom}_1_boot.png')
        # 2. un geste pendant l'allumage ne fait que le sauter : clic / tap sur la position de NOUVELLE PARTIE -> pas de partie
        if not mob:  # bureau : une touche saute aussi, puis on rejoue l'allumage pour le test du clic
            pg.keyboard.press('x'); time.sleep(0.4); et = E(ETAT)
            ok(not et['booting'] and et['boot'] == 'repos' and E("document.getElementById('creation').hidden"), f'{P} allumage sauté par une touche, sans action', et)
            E("window.__nml.shell.terminal.rejouer()"); time.sleep(2.6)
        bb = pg.locator('#m-new').bounding_box(); geste = pg.touchscreen.tap if mob else pg.mouse.click
        ok(E(ETAT)['booting'] and E("getComputedStyle(document.querySelector('#menu .t-list')).pointerEvents") == 'none', f'{P} pendant l\'allumage, la liste ne reçoit aucun geste')
        geste(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2); time.sleep(0.8); et = E(ETAT)
        ok(not et['booting'] and et['boot'] == 'repos' and E("document.getElementById('creation').hidden") and E("document.body.classList.contains('menu-open') && !document.getElementById('menu').hidden"),
           f'{P} {"tap" if mob else "clic"} sur NOUVELLE PARTIE pendant l\'allumage : séquence sautée, aucune partie lancée', et)
        E("window.__nml.shell.terminal.rejouer()"); time.sleep(1.0); E("document.getElementById('m-new').click()"); time.sleep(0.3)
        ok(E("document.getElementById('creation').hidden") and not E(ETAT)['booting'], f'{P} clic programmatique pendant l\'allumage : ignoré (séquence sautée)')
        geste(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2); time.sleep(0.6)
        ok(not E("document.getElementById('creation').hidden"), f'{P} le geste suivant choisit : NOUVELLE PARTIE ouvre la création')
        E("document.getElementById('cr-menu').click()"); time.sleep(0.6)
        ok(E("document.getElementById('creation').hidden && !document.getElementById('menu').hidden") and not E(ETAT)['booting'], f'{P} retour au menu depuis la création, sans rallumage')
        time.sleep(0.4)
        # 3. six choix visibles, non recouverts, cibles >= 44 px
        c = E(CHOIX, SIX)
        bad = [x for x in c if not (x['vis'] and x['dansEcran'] and x['dessus'] and not x['tampon'] and not x['ticker'] and not x['statut'] and x['h'] >= 44 and x['w'] >= 44)]
        ok(not bad, f'{P} six choix visibles, dans l\'écran, au premier plan, hors tampon / bandeau / statut, cibles >= 44 px', bad)
        ok(E("['m-continue','m-new','m-load','m-options','m-credits','m-quit'].map(i=>document.getElementById(i).textContent.trim().split(/\\s{2,}|\\n/)[0])").__len__() == 6
           and E("[...document.querySelectorAll('#menu .t-list button:not([hidden])')].map(b=>b.querySelector('span').textContent).join('|')") == 'CONTINUER|NOUVELLE PARTIE|CHARGER|OPTIONS|CRÉDITS|QUITTER',
           f'{P} libellés et ordre de la fiche', E("[...document.querySelectorAll('#menu .t-list button:not([hidden])')].map(b=>b.querySelector('span').textContent).join('|')"))
        ok(E("document.getElementById('m-continue').disabled && document.getElementById('m-quit').disabled"), f'{P} CONTINUER (sans sauvegarde) et QUITTER (écran titre) désactivés proprement')
        tk = E("(()=>{const t=document.getElementById('t-ticker-track');return [t.textContent.includes('HUMAN CORP'), getComputedStyle(t).animationName]})()")
        ok(tk[0] and tk[1] == 't-ticker', f'{P} bandeau de surveillance défilant', tk)
        mg = E(MARGE); R_TAMPON[nom] = mg
        ok(not mg['vis'] or not mg['touche'], f'{P} tampon : 24 px de marge (base) avec choix, bandeau, version et statut (échelle {mg["echelle"]}, {mg["w"]}x{mg["h"]} px)', mg)
        pg.screenshot(path=f'{OUT}{nom}_2_menu.png')
        # 4. navigation clavier (flèches, Début / Fin) puis survol / sélection
        E("document.activeElement && document.activeElement.blur(); document.querySelectorAll('#menu .cur').forEach(b => b.classList.remove('cur'))")
        pg.keyboard.press('ArrowDown'); f1 = E("document.activeElement.id")
        pg.keyboard.press('ArrowDown'); f2 = E("document.activeElement.id")
        pg.keyboard.press('ArrowUp'); f3 = E("document.activeElement.id")
        pg.keyboard.press('End'); f4 = E("document.activeElement.id")
        pg.keyboard.press('Home'); f5 = E("document.activeElement.id")
        ok([f1, f2, f3, f4, f5] == ['m-new', 'm-load', 'm-new', 'm-credits', 'm-new'], f'{P} navigation clavier (choix grisés sautés)', [f1, f2, f3, f4, f5])
        inv = E("(()=>{const s=getComputedStyle(document.getElementById('m-new'));return [s.backgroundColor,s.color]})()")
        ok(inv[0] == 'rgb(242, 180, 74)' and inv[1] == 'rgb(10, 8, 4)', f'{P} sélection en vidéo inverse', inv)
        if not mob: bb = pg.locator('#m-options').bounding_box(); pg.mouse.move(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2); time.sleep(0.3)
        pg.screenshot(path=f'{OUT}{nom}_3_selection.png')
        # 5. sous-panneau (Options) ouvert puis fermé par Échap
        pg.keyboard.press('Home'); pg.keyboard.press('ArrowDown'); pg.keyboard.press('ArrowDown'); pg.keyboard.press('Enter'); time.sleep(0.5)
        so = E("[!document.getElementById('menu-sub').hidden, document.getElementById('menu-sub').textContent.includes('OPTIONS'), document.getElementById('m-exec').textContent]")
        pg.screenshot(path=f'{OUT}{nom}_4_options.png')
        pg.keyboard.press('Escape'); time.sleep(0.3)
        ok(so[0] and so[1] and E("document.getElementById('menu-sub').hidden"), f'{P} Entrée ouvre OPTIONS, Échap referme', so)
        # 6. nouvelle partie jusqu'en jeu (Entrée sur NOUVELLE PARTIE, puis création par gestes)
        pg.keyboard.press('Home'); pg.keyboard.press('Enter'); time.sleep(0.6)
        ok(not E("document.getElementById('creation').hidden"), f'{P} Entrée sur NOUVELLE PARTIE ouvre la création')
        for s in ['[data-race="augmente"]', '#cr-next', '#cr-enter']:
            bb = pg.locator(s).first.bounding_box(); (pg.touchscreen.tap if mob else pg.mouse.click)(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2); time.sleep(0.5)
        try: pg.wait_for_function('!document.body.classList.contains("menu-open")', timeout=15000); enjeu = True
        except Exception: enjeu = False
        time.sleep(1.0); et = E(ETAT)
        ok(enjeu and E("window.__nml.state.location") == 'dusk_q1', f'{P} nouvelle partie : en jeu (Dusk-Town)', E("window.__nml.state.location"))
        ok(et['paused'] and not et['glitch'] and not et['booting'] and E(ANIMS) == 0, f'{P} en jeu : menu démonté / en pause, 0 animation du menu', (et, E(ANIMS)))
        # 7. pause (Échap / bouton Menu) : même terminal, sans rallumage ; onglet caché : pause
        if mob: pg.locator('#k-menu').tap()
        else: pg.keyboard.press('Escape')
        time.sleep(0.6); et = E(ETAT)
        ok(E("document.body.classList.contains('menu-open')") and not et['booting'] and not E("document.getElementById('m-resume').hidden") and not E("document.getElementById('m-quit').disabled"), f'{P} pause : terminal sans rallumage, REPRENDRE et QUITTER actifs', et)
        E("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))"); time.sleep(0.2)
        ok(E(ETAT)['paused'] and not E(ETAT)['glitch'] and E(ANIMS) == 0, f'{P} onglet caché : aucune animation, aucun minuteur de glitch', E(ETAT))
        E("Object.defineProperty(document,'hidden',{configurable:true,get:()=>false});document.dispatchEvent(new Event('visibilitychange'))")
        ok(not errs, f'{P} aucune erreur JS, aucune requête en échec (404)', errs[:4])
        ctx.close()
        # 8. prefers-reduced-motion : pas d'allumage, rien ne bouge, bandeau en messages alternés
        ctx, pg, errs = ouvre(w, h, mob, reduit=True); E = pg.evaluate
        E("window.__nml.shell.terminal.pret"); time.sleep(1.2); et = E(ETAT)
        rm = E("(()=>{const t=document.getElementById('t-ticker-track');return [getComputedStyle(t).animationName, t.children.length]})()")
        ok(et['reduit'] and not et['booting'] and et['boot'] == 'repos' and not et['glitch'] and E(ANIMS) == 0 and rm == ['none', 1], f'{P} prefers-reduced-motion : état de repos direct, 0 animation, bandeau sans défilement', (et, E(ANIMS), rm))
        c = E(CHOIX, SIX); ok(all(x['vis'] and x['dessus'] for x in c), f'{P} prefers-reduced-motion : six choix visibles d\'office', [x for x in c if not (x['vis'] and x['dessus'])])
        mg = E(MARGE); ok(not mg['vis'] or not mg['touche'], f'{P} prefers-reduced-motion : tampon avec marge', mg)
        pg.screenshot(path=f'{OUT}{nom}_5_mouvement_reduit.png')
        ok(not errs, f'{P} mouvement réduit : aucune erreur', errs[:3]); ctx.close()
    # 9. séquence de 6 images de l'allumage + GIF (1280 × 800)
    if any(f[0] == '1280x800' for f in FORMATS) and not os.environ.get('NOGIF'):
        ctx, pg, errs = ouvre(1280, 800, False); E = pg.evaluate; E("window.__nml.shell.terminal.pret"); time.sleep(0.5)
        E("window.__nml.shell.terminal.rejouer()"); t0 = time.time(); frames = []
        for i, t in enumerate([0.2, 0.55, 1.2, 5.0, 16.6, 18.6]):
            while time.time() - t0 < t: time.sleep(0.01)
            f = f'{OUT}boot_seq_{i + 1}_{int(t * 1000)}ms.png'; pg.screenshot(path=f); frames.append(f)
        from PIL import Image
        ims = [Image.open(f).convert('RGB').resize((640, 400)) for f in frames]
        ims[0].save(OUT + 'boot_1280.gif', save_all=True, append_images=ims[1:], duration=[400, 400, 700, 900, 900, 1600], loop=0)
        ok(len(frames) == 6, 'séquence GIF de l\'allumage (6 images, 1280)', OUT + 'boot_1280.gif'); ctx.close()
    br.close()
print('TAMPON', json.dumps(R_TAMPON)); n = sum(1 for c, _ in R if c); print(f'{n}/{len(R)} OK'); print('ECHECS', len(R) - n); sys.exit(0 if n == len(R) else 1)
