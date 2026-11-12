# Optimisation du lancement (12/11, demande de Valentin) : plus d'écran noir à l'ouverture, un seul visage du menu, chargement visible
# à l'ouverture d'une partie, catalogue chargé par lieu.
# 1. première image : ligne d'attente ambre du Terminal (cadre retenu), jamais le repli plein cadre comme état d'attente
# 2. menu complet sans attendre le catalogue (images du jeu retenues) : cadre, titre, choix
# 3. CONTINUER renseigné depuis localStorage avant main.js (main.js retenu), même format que shell.js ; sauvegardes DEV séparées
# 4. musique du menu au premier geste, avant main.js ; pas de préchargement du mp3 (preload none)
# 5. ouverture d'une partie (Continuer -> Center-Town, images de Center-Town retenues) : Terminal visible, ligne CHARGEMENT DU SECTEUR
#    avec progression, jamais de menu caché sur du vide ; puis le jeu ; aucun échantillon « silencieux »
# 6. Nouvelle partie : création puis Dusk-Town, sans silence
# 7. en jeu : lieu pas encore chargé -> ligne de chargement, puis le lieu ; les autres quartiers se chargent à l'arrivée
# 8. un seul visage au repos : cadre + musique + progression, 1280 et 390 ; mouvement réduit
# 9. (12/11, Ocre) ligne de chargement sur UNE SEULE LIGNE (barre et « % » ensemble), dans le Terminal et sur l'overlay en jeu,
#    à 1280, 390 et fold (plié 412, déplié 884) ; lisible (≥ 17 px), dans la largeur utile
# 10. calques WebP (Ocre, 197def3) : tampon, cadre et fond servis en .webp ; PNG seulement en repli (WebP en échec), une seule fois
# Captures : OUT (défaut /tmp/nml-test-out/menu_chargement/).
import os, sys, time, json, re
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8921/')
if not URL.endswith('/') and '?' not in URL: URL += '/'
OUT = os.environ.get('OUT', '/tmp/nml-test-out/menu_chargement/'); os.makedirs(OUT, exist_ok=True)
R = []
def ok(c, n, d=''): R.append((bool(c), n)); print(('OK   ' if c else 'ECHEC ') + n + ('' if c else f'  {str(d)[:400]}'), flush=True)
SAVE = {'v': 2, 't': 1794486164670, 'label': 'Steel-Megalopolis · Center-Town', 'state': None}
ARGS = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=user-gesture-required']
VIS = """sel => { const e = document.querySelector(sel); if (!e) return false; const cs = getComputedStyle(e), r = e.getBoundingClientRect();
  return !e.hidden && cs.display !== 'none' && cs.visibility !== 'hidden' && +cs.opacity > 0.05 && r.width > 0 && r.height > 0; }"""
SONDE = """() => { const M = document.getElementById('menu'), v = s => (""" + VIS + """)(s), ch = document.getElementById('chargement');
  return { menu: !M.hidden && v('#menu'), attente: v('#t-attente'), ecran: v('#t-screen'), cadre: v('#t-cadre'), plein: M.dataset.cadre === 'plein' && v('#t-screen'),
    charge: M.classList.contains('t-charge'), note: (document.getElementById('menu-note') || {}).textContent || '', creation: v('#creation'),
    chargeJeu: !!ch && !ch.hidden, ligneJeu: ch ? ch.textContent : '', loc: window.__nml && window.__nml.state ? window.__nml.state.location : null,
    pret: !!(window.__nml && window.__nml.lieuPret && window.__nml.state && window.__nml.lieuPret(window.__nml.state.location)),
    musique: !document.getElementById('music').paused, shell: !!(window.__nml && window.__nml.shell) }; }"""

def contexte(br, w=1280, h=800, mob=False, save=None, cle='nml_save_auto', reduit=False):
    ctx = br.new_context(viewport={'width': w, 'height': h}, has_touch=mob, is_mobile=mob, device_scale_factor=2 if mob else 1, reduced_motion='reduce' if reduit else 'no-preference')
    if save: ctx.add_init_script("if (!sessionStorage.getItem('_seed')) { localStorage.setItem(%s, %s); sessionStorage.setItem('_seed', '1'); }" % (json.dumps(cle), json.dumps(json.dumps(save))))
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append('JS ' + str(e)))
    pg.on('response', lambda r: r.status >= 400 and errs.append(f'{r.status} {r.url}'))
    return ctx, pg, errs

class Retenue:
    """Retient les requêtes d'un motif jusqu'à relâche()."""
    def __init__(self, pg, motif): self.pg, self.motif, self.held, self.libre = pg, motif, [], False; pg.route(motif, self._h)
    def _h(self, route):
        if self.libre: return route.continue_()
        self.held.append(route)
    def relache(self):
        self.libre = True
        for r in self.held:
            try: r.continue_()
            except Exception: pass
        self.held = []
        try: self.pg.unroute(self.motif, self._h)
        except Exception: pass

# une seule ligne : une seule rangée de boîtes de texte (Range), hauteur d'une ligne, rien qui déborde ; police lisible
UNE_LIGNE = """sel => { const e = document.querySelector(sel); if (!e || !e.firstChild) return { une: false, raison: 'vide' };
  const cs = getComputedStyle(e), lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.2, r = e.getBoundingClientRect();
  const rg = document.createRange(); rg.selectNodeContents(e); const rs = [...rg.getClientRects()].filter(x => x.width > 0);
  const tops = [...new Set(rs.map(x => Math.round(x.top)))], txt = e.textContent;
  const pad = parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom) + parseFloat(cs.borderTopWidth) + parseFloat(cs.borderBottomWidth);
  const vw = innerWidth, dedans = r.left >= -1 && r.right <= vw + 1;
  const une = tops.length === 1 && r.height - pad <= lh * 1.5 && e.scrollWidth <= e.clientWidth + 1 && dedans && /\\[[#-]+\\]/.test(txt) && txt.includes('%') && parseFloat(cs.fontSize) >= 17;
  return { une, txt, tops: tops.length, h: Math.round(r.height - pad), lh, sw: e.scrollWidth, cw: e.clientWidth, fs: cs.fontSize, ws: cs.whiteSpace, l: Math.round(r.left), rt: Math.round(r.right), vw }; }"""

def saute(pg):  # saute l'allumage (geste : aussi le premier geste pour la musique)
    pg.mouse.click(6, 6); time.sleep(0.25)

with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=ARGS)
    # sauvegarde Center-Town réelle (état de départ déplacé sur Center-Town), écrite par le jeu lui-même
    ctx, pg, errs = contexte(br)
    pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=120000)
    etat = pg.evaluate("""() => { const N = window.__nml, d = N.doors.find(d => d.id === 'c_ouest'), s = JSON.parse(JSON.stringify(N.game.snapshot()));
      s.location = 'steel_center'; Object.assign(s.player, { x: d.threshold.x + 3, z: d.threshold.z, path: [], pending: null }); return s; }""")
    SAVE['state'] = etat; ctx.close()
    ATTENDU = f"Auto · {SAVE['label']} · " + time.strftime('%d/%m %H:%M', time.localtime(SAVE['t'] / 1000))

    # 1. première image : cadre retenu -> ligne d'attente ambre, pas de plein cadre ; puis le cadre se pose (transition unique)
    for nom, w, h, mob, variante in [('1280', 1280, 800, False, 'paysage'), ('390', 390, 844, True, 'portrait')]:
        ctx, pg, errs = contexte(br, w, h, mob, save=SAVE)
        hold = Retenue(pg, re.compile(r'.*/assets/ui/menu_terminal/(cadre|fond).*\.(webp|png)$'))
        pg.goto(URL, wait_until='commit'); pg.wait_for_selector('#t-attente', state='attached'); time.sleep(0.6)
        s = pg.evaluate(SONDE); pg.screenshot(path=f'{OUT}{nom}_1_premiere_image.png')
        ok(s['attente'] and not s['plein'] and not s['ecran'] and not s['cadre'], f'{nom} première image : ligne d\'attente du Terminal visible, pas d\'écran noir, pas de repli plein cadre', s)
        txt = pg.evaluate("document.getElementById('t-attente').innerText")
        ok('HUMAN CORP' in txt and 'TERMINAL' in txt, f'{nom} première image : texte du Terminal (phosphore ambre)', txt)
        vus = set()
        hold.relache()
        t0 = time.time()
        while time.time() - t0 < 30:
            s = pg.evaluate(SONDE); vus.add('attente' if s['attente'] else 'plein' if s['plein'] else 'cadre' if s['cadre'] else 'autre')
            if pg.evaluate('!!window.__nmlMenuPret') and s['cadre']: break
            time.sleep(0.03)
        et = pg.evaluate('window.__nmlMenu.terminal.etat()')
        ok(et['mode'] == variante and 'plein' not in vus, f'{nom} le cadre se pose dès qu\'il est prêt, sans passer par le plein cadre', {'vus': sorted(vus), 'etat': et})
        ok(not [e for e in errs if 'JS' in e], f'{nom} aucune erreur JS', errs[:3]); ctx.close()

    # 2 + 3 + 4. main.js retenu : menu complet, Continuer renseigné depuis localStorage, musique au premier geste
    for nom, w, h, mob in [('1280', 1280, 800, False), ('390', 390, 844, True)]:
        ctx, pg, errs = contexte(br, w, h, mob, save=SAVE)
        hold = Retenue(pg, '**/src/main.js')
        imgs = []; pg.on('request', lambda r: r.resource_type == 'image' and imgs.append(r.url))
        pg.goto(URL); pg.wait_for_function('window.__nmlMenuPret === true', timeout=30000)
        info = pg.evaluate("document.getElementById('m-continue-info').textContent"); dis = pg.evaluate("document.getElementById('m-continue').disabled")
        ok(info == ATTENDU and not dis, f'{nom} CONTINUER renseigné depuis localStorage avant main.js (même format que le shell)', {'info': info, 'attendu': ATTENDU})
        ok(not pg.evaluate("!!(window.__nml && window.__nml.shell)"), f'{nom} main.js bien retenu pendant le contrôle')
        audio = pg.evaluate("(() => { const a = document.getElementById('music'); return { preload: a.getAttribute('preload'), paused: a.paused }; })()")
        ok(audio['preload'] == 'none' and audio['paused'], f'{nom} pas de préchargement du mp3 avant le geste (preload none), silence avant le geste', audio)
        jeu = [u for u in imgs if re.search(r'/assets/(buildings|interiors|steel|mockup|generated)/', u)]
        ok(not jeu, f'{nom} aucune image du jeu demandée avant le menu (main.js retenu)', jeu[:5])
        if mob: pg.tap('#menu', position={'x': 10, 'y': 10})
        else: saute(pg)
        time.sleep(0.5)
        ok(pg.evaluate("!document.getElementById('music').paused"), f'{nom} musique du menu au premier geste, sans attendre main.js')
        pg.evaluate("window.__nmlMenu.terminal.saute()"); time.sleep(0.4)
        pg.screenshot(path=f'{OUT}{nom}_2_menu_complet_avant_main.png')
        vis = pg.evaluate("(() => { const v = " + VIS + "; return { cadre: v('#t-cadre'), titre: v('#menu h1'), cont: v('#m-continue'), neuf: v('#m-new') }; })()")
        ok(all(vis.values()) or (not mob and False), f'{nom} menu complet sans main.js ni catalogue : cadre, titre, choix', vis)
        hold.relache(); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=120000); time.sleep(0.3)
        info2 = pg.evaluate("document.getElementById('m-continue-info').textContent")
        ok(info2 == info, f'{nom} une fois le shell prêt, la ligne sous CONTINUER ne change pas (un seul visage)', {'avant': info, 'apres': info2})
        ok(not pg.evaluate("document.getElementById('music').paused"), f'{nom} la musique continue quand main.js prend la main')
        ok(not [e for e in errs if 'JS' in e], f'{nom} aucune erreur JS', errs[:3]); ctx.close()
    # DEV : sauvegardes séparées (une sauvegarde joueur n'apparaît pas en ?dev=1)
    ctx, pg, errs = contexte(br, save=SAVE); hold = Retenue(pg, '**/src/main.js')
    pg.goto(URL + ('&' if '?' in URL else '?') + 'dev=1'); pg.wait_for_function('window.__nmlMenuPret === true', timeout=30000)
    i = pg.evaluate("document.getElementById('m-continue-info').textContent")
    ok(i == 'AUCUNE SESSION ANTERIEURE' and pg.evaluate("document.getElementById('m-continue').disabled"), 'DEV : la sauvegarde du joueur n\'est pas lue (préfixe nml_dev_save_)', i)
    hold.relache(); ctx.close()

    # 5. Continuer -> Center-Town, images de Center-Town retenues : chargement visible, jamais de vide
    for nom, w, h, mob in [('1280', 1280, 800, False), ('390', 390, 844, True)]:
        ctx, pg, errs = contexte(br, w, h, mob, save=SAVE)
        hold = Retenue(pg, re.compile(r'.*/assets/steel/center_town/.*\.(webp|png)$'))
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=120000)
        saute(pg); pg.evaluate("window.__nml.shell.terminal.saute()"); time.sleep(0.3)
        pg.screenshot(path=f'{OUT}{nom}_3_menu_complet.png')
        repos = pg.evaluate(SONDE)
        ok(repos['cadre'] and repos['musique'] and pg.evaluate("document.getElementById('m-continue-info').textContent") == ATTENDU,
           f'{nom} repos : un seul visage, cadre + musique + progression sous CONTINUER', repos)
        pg.click('#m-continue'); t0 = time.time(); time.sleep(1.0)
        s = pg.evaluate(SONDE); pg.screenshot(path=f'{OUT}{nom}_4_chargement_partie.png')
        ok(s['menu'] and s['charge'] and 'CHARGEMENT' in s['note'] and 'CENTER-TOWN' in s['note'] and '%' in s['note'] and '[' in s['note'],
           f'{nom} ouverture de partie : le Terminal reste, ligne CHARGEMENT · CENTER-TOWN avec progression', s)
        if nom == '1280': ok('CHARGEMENT DU SECTEUR' in s['note'], '1280 : forme longue « CHARGEMENT DU SECTEUR » (place suffisante)', s['note'])
        taille = pg.evaluate("(() => { const n = document.getElementById('menu-note'); return parseFloat(getComputedStyle(n).fontSize); })()")
        ok(taille >= 17, f'{nom} la ligne de chargement est lisible (≥ 17 px, phosphore vif)', taille)
        time.sleep(2.0); hold.relache()
        vides = []; fin = None
        while time.time() - t0 < 120:
            s = pg.evaluate(SONDE)
            signe = (s['menu'] and ('CHARGEMENT' in s['note'] or s['charge'])) or s['chargeJeu']
            jouable = not s['menu'] and s['loc'] == 'steel_center' and s['pret'] and not s['chargeJeu']
            if jouable: fin = time.time() - t0; break
            if not signe: vides.append(round(time.time() - t0, 2))
            time.sleep(0.2)
        pg.evaluate('() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))'); time.sleep(0.8)
        pg.screenshot(path=f'{OUT}{nom}_5_entree_en_jeu.png')
        ok(fin is not None, f'{nom} entrée en jeu à Center-Town une fois ses images là', fin)
        ok(len(vides) <= 1, f'{nom} pas de silence : à chaque instant, chargement visible ou partie jouable', vides[:10])
        ok(pg.evaluate("window.__nml.view && document.getElementById('menu').hidden"), f'{nom} menu fermé en jeu')
        ok(not [e for e in errs if 'JS' in e], f'{nom} aucune erreur JS', errs[:3]); ctx.close()

    # 6. Nouvelle partie : création, puis Dusk-Town ; 7. passage vers un lieu non chargé (Pulse Plaza retenu)
    ctx, pg, errs = contexte(br)
    hold = Retenue(pg, re.compile(r'.*/assets/steel/pulse_plaza/.*\.(webp|png)$'))
    pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=120000)
    saute(pg); pg.evaluate("window.__nml.shell.terminal.saute()"); time.sleep(0.2)
    pg.click('#m-new'); time.sleep(0.4)
    ok(pg.evaluate(SONDE)['creation'], 'Nouvelle partie : la création s\'ouvre tout de suite')
    done = []
    t0 = time.time()
    for sel in ['[data-race="augmente"]', '#cr-next', '#cr-enter']:  # même parcours que menu_rapide
        pg.click(sel); time.sleep(0.3)
    vides = []
    while time.time() - t0 < 60:
        s = pg.evaluate(SONDE)
        if not s['menu'] and not s['creation'] and s['pret'] and s['loc'] and not s['chargeJeu']: break
        if not (s['creation'] or (s['menu'] and ('CHARGEMENT' in s['note'] or s['charge'])) or s['chargeJeu']): vides.append(round(time.time() - t0, 2))
        time.sleep(0.2)
    ok(not s['menu'] and not s['creation'] and s['pret'], 'Nouvelle partie : en jeu après la création', {'s': s, 'boutons': done[:8]})
    ok(len(vides) <= 1, 'Nouvelle partie : pas de silence entre la création et le jeu', vides[:8])
    # 7. téléportation vers Pulse Plaza (images retenues) : ligne de chargement en jeu, puis le lieu
    pg.evaluate("window.__nml.game.state.location = 'steel_pulse'"); time.sleep(0.8)
    s = pg.evaluate(SONDE); pg.screenshot(path=f'{OUT}1280_7_chargement_en_jeu.png')
    ok(s['chargeJeu'] and 'CHARGEMENT DU SECTEUR' in s['ligneJeu'] and not s['pret'], 'en jeu : lieu pas encore chargé -> ligne CHARGEMENT DU SECTEUR, monde figé', s)
    l1 = pg.evaluate(UNE_LIGNE, '#chargement'); ok(l1['une'], '1280 en jeu (Pulse Plaza) : overlay de chargement sur une seule ligne, « % » compris', l1)
    hold.relache()
    pg.wait_for_function("window.__nml.lieuPret('steel_pulse') && document.getElementById('chargement').hidden", timeout=120000); time.sleep(0.5)
    n = pg.evaluate("window.__nml.chargeur.cles('steel_pulse').filter(k => !window.__nml.chargeur.charge(k)).length")
    ok(n == 0, 'en jeu : Pulse Plaza chargé à l\'arrivée, toutes ses images présentes', n)
    pg.screenshot(path=f'{OUT}1280_8_pulse_charge.png')
    ok(not [e for e in errs if 'JS' in e], 'Nouvelle partie / passage : aucune erreur JS', errs[:3]); ctx.close()

    # 9. une seule ligne, Terminal et overlay en jeu, 1280 / 390 / fold plié / fold déplié
    for nom, w, h, mob in [('1280', 1280, 800, False), ('390', 390, 844, True), ('fold_plie_412', 412, 915, True), ('fold_deplie_884', 884, 1104, True)]:
        ctx, pg, errs = contexte(br, w, h, mob, save=SAVE)
        hc = Retenue(pg, re.compile(r'.*/assets/steel/center_town/.*\.(webp|png)$')); hp = Retenue(pg, re.compile(r'.*/assets/steel/pulse_plaza/.*\.(webp|png)$'))
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=120000)
        saute(pg); pg.evaluate("window.__nml.shell.terminal.saute()"); time.sleep(0.3)
        pg.click('#m-continue'); time.sleep(1.0)
        l = pg.evaluate(UNE_LIGNE, '#menu-note'); pg.screenshot(path=f'{OUT}{nom}_9_ligne_terminal.png')
        ok(pg.evaluate(SONDE)['charge'] and l['une'], f'{nom} Terminal : ligne de chargement sur une seule ligne (barre et « % » ensemble, ≥ 17 px)', l)
        hc.relache(); pg.wait_for_function("window.__nml.lieuPret('steel_center') && document.getElementById('menu').hidden", timeout=120000); time.sleep(0.3)
        pg.evaluate("window.__nml.game.state.location = 'steel_pulse'")  # la ligne paraît à l'image suivante (Center-Town : images lentes en swiftshader)
        pg.wait_for_function("!document.getElementById('chargement').hidden", timeout=20000); time.sleep(0.4)
        l = pg.evaluate(UNE_LIGNE, '#chargement'); pg.screenshot(path=f'{OUT}{nom}_9_ligne_en_jeu.png')
        ok(pg.evaluate(SONDE)['chargeJeu'] and l['une'], f'{nom} en jeu (Pulse Plaza) : overlay de chargement sur une seule ligne, « % » compris', l)
        hp.relache(); pg.wait_for_function("window.__nml.lieuPret('steel_pulse') && document.getElementById('chargement').hidden", timeout=120000)
        ok(not [e for e in errs if 'JS' in e], f'{nom} ligne unique : aucune erreur JS', errs[:3]); ctx.close()

    # 10. calques WebP : tampon (et cadre, fond) en .webp ; PNG seulement en repli
    ctx, pg, errs = contexte(br); vus = []
    pg.on('request', lambda r: '/assets/ui/menu_terminal/' in r.url and vus.append(r.url.split('/')[-1]))
    pg.goto(URL); pg.wait_for_function('window.__nmlMenuPret === true', timeout=30000)
    pg.wait_for_function("document.getElementById('t-tampon').complete && document.getElementById('t-tampon').naturalWidth > 0", timeout=30000)
    t = pg.evaluate("(() => { const t = document.getElementById('t-tampon'), c = document.getElementById('t-cadre'); return { tampon: t.currentSrc.split('/').pop(), w: t.naturalWidth, h: t.naturalHeight, data: t.dataset.src.split('/').pop(), cadre: c.currentSrc.split('/').pop(), fond: getComputedStyle(document.querySelector('.t-fond')).backgroundImage.split('/').pop() }; })()")
    ok(t['tampon'] == 'tampon_acces_non_autorise.webp' and t['data'].endswith('.webp') and t['w'] > 0, 'tampon servi en .webp (data-src et image chargée)', t)
    ok(t['cadre'] == 'cadre.webp' and 'fond_ecran.webp' in t['fond'], 'cadre et fond du manifeste pris en .webp par le code', t)
    ok(not [u for u in vus if u.endswith('.png') and not u.startswith('ecran_masque')], 'aucun PNG de calque demandé quand le WebP passe (PNG = repli)', vus)
    ctx.close()
    for nom, w, h, mob in [('1280', 1280, 800, False), ('390', 390, 844, True)]:
        ctx, pg, errs = contexte(br, w, h, mob); vus = []
        pg.route(re.compile(r'.*/assets/ui/menu_terminal/.*\.webp$'), lambda r: r.abort())
        pg.on('request', lambda r: '/assets/ui/menu_terminal/' in r.url and vus.append(r.url.split('/')[-1]))
        pg.goto(URL); pg.wait_for_function('window.__nmlMenuPret === true', timeout=30000)
        pg.wait_for_function("document.getElementById('t-tampon').complete && document.getElementById('t-tampon').naturalWidth > 0", timeout=30000); time.sleep(0.5)
        t = pg.evaluate("(() => { const t = document.getElementById('t-tampon'), c = document.getElementById('t-cadre'); return { tampon: t.currentSrc.split('/').pop(), cadre: c.currentSrc.split('/').pop(), mode: document.getElementById('menu').dataset.cadre }; })()")
        nt = len([u for u in vus if u.startswith('tampon_acces_non_autorise.png')])
        ok(t['tampon'] == 'tampon_acces_non_autorise.png' and nt == 1, f'{nom} WebP en échec : tampon en PNG de repli, une seule requête (pas de boucle)', {'t': t, 'png': nt})
        ok(t['cadre'].endswith('.png') and t['mode'] != 'plein', f'{nom} WebP en échec : cadre en PNG de repli, cadre posé (pas de plein cadre)', t)
        pg.screenshot(path=f'{OUT}{nom}_10_repli_png.png'); ctx.close()

    # 8. mouvement réduit : la ligne d'attente et le chargement restent (sans animation), menu identique
    ctx, pg, errs = contexte(br, save=SAVE, reduit=True)
    pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=120000); time.sleep(0.3)
    et = pg.evaluate('window.__nml.shell.terminal.etat()')
    ok(et['reduit'] and not et['booting'] and et['mode'] == 'paysage', 'mouvement réduit : pas d\'allumage, cadre posé', et)
    ok(pg.evaluate("document.getElementById('m-continue-info').textContent") == ATTENDU, 'mouvement réduit : progression sous CONTINUER')
    ctx.close()
    br.close()
bons = sum(1 for c, _ in R if c)
print(f'{bons}/{len(R)} OK'); print('ECHECS', len(R) - bons)
sys.exit(0 if bons == len(R) else 1)
