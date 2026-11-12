# Optimisation du lancement (12/11, demande de Valentin) : plus d'écran noir à l'ouverture, un seul visage du menu, chargement visible
# à l'ouverture d'une partie, catalogue chargé par lieu.
# 1. première image : ligne d'attente ambre du Terminal (cadre retenu), jamais le repli plein cadre comme état d'attente
# 2. menu complet sans attendre le catalogue (images du jeu retenues) : cadre, titre, choix
# 3. CONTINUER renseigné depuis localStorage avant main.js (main.js retenu), même format que shell.js ; sauvegardes DEV séparées
# 4. musique du menu au premier geste, avant main.js ; pas de préchargement du mp3 (preload none)
# 5. ouverture d'une partie (Continuer -> Center-Town, images de Center-Town retenues) : Terminal visible, monogramme NML
#    avec progression (anneau = vrai %), jamais de menu caché sur du vide ; puis le jeu ; aucun échantillon « silencieux »
# 6. Nouvelle partie : création puis Dusk-Town, sans silence
# 7. en jeu : lieu pas encore chargé -> monogramme NML en badge, puis le lieu ; les autres quartiers se chargent à l'arrivée
# 8. un seul visage au repos : cadre + musique + progression, 1280 et 390 ; mouvement réduit
# 9. (12/11, choix de Valentin : proposition B d'Ocre) monogramme NML à la place de la ligne, dans le Terminal et sur l'overlay en jeu,
#    à 1280, 390 et fold (plié 412, déplié 884) : une seule unité (canvas net + légende Plex sur une ligne), dans l'écran, sans recouvrir
#    de texte du Terminal, légende « SECTEUR   n % » (ou « n % » en petit format), texte lu (secteur + %), anneau sur le vrai progrès ;
#    mouvement réduit : hexagone et lettres déjà là
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

# monogramme NML : canvas net (devicePixelRatio) et dessiné, légende sur une seule ligne (nowrap), unité dans la fenêtre (et dans l'écran
# du Terminal), anneau visible (hors halo) sans croiser de texte du Terminal ; texte lu dans l'élément role=status ; plus de barre [###---]
SCEAU = """sel => { const e = document.querySelector(sel); const r = e && e.querySelector('.nml-sceau'); if (!r) return { ok: false, raison: 'absent' };
  const cv = r.querySelector('canvas'), leg = r.querySelector('.nml-sceau-leg'), lu = e.querySelector('.nml-sceau-lu'), s = e._sceau;
  const b = r.getBoundingClientRect(), cb = cv.getBoundingClientRect(), dpr = devicePixelRatio, ech = parseFloat(r.style.getPropertyValue('--sceau-e'));
  const g = cv.getContext('2d'), d = g.getImageData(0, 0, cv.width, cv.height).data; let enc = 0; for (let i = 3; i < d.length; i += 16) if (d[i] > 40) enc++;
  const c = g.getImageData(Math.round(cv.width * .38), Math.round(cv.height * .44), Math.round(cv.width * .24), Math.round(cv.height * .12)).data; let lettres = 0; for (let i = 3; i < c.length; i += 4) if (c[i] > 120) lettres++;
  const rg = document.createRange(); rg.selectNodeContents(leg); const tops = [...new Set([...rg.getClientRects()].filter(x => x.width > 0).map(x => Math.round(x.top)))];
  const lc = leg.getBoundingClientRect(), cs = getComputedStyle(leg);
  const m = (132 - 121) * ech, anneau = { left: cb.left + m, right: cb.right - m, top: cb.top + m, bottom: cb.bottom - m };
  const vis = { left: Math.min(anneau.left, lc.left), right: Math.max(anneau.right, lc.right), top: anneau.top, bottom: lc.bottom };
  const ecr = document.getElementById('t-screen'), er = e.closest('#menu') ? ecr.getBoundingClientRect() : { left: 0, top: 0, right: innerWidth, bottom: innerHeight };
  const dedans = vis.left >= er.left - 1 && vis.right <= er.right + 1 && vis.top >= er.top - 1 && vis.bottom <= er.bottom + 1;
  let croise = [];
  if (e.closest('#menu')) { const M = e.closest('#menu'), T = el => { const q = document.createRange(); q.selectNodeContents(el); return [...q.getClientRects()].filter(x => x.width > 0); };
    const els = [M.querySelector('h1'), ...M.querySelectorAll('.t-list .btn:not([hidden])'), M.querySelector('#m-exec'), ...M.querySelectorAll('.t-status span'), M.querySelector('#m-version')];
    for (const el of els) for (const x of T(el)) if (x.left < vis.right && x.right > vis.left && x.top < vis.bottom && x.bottom > vis.top) croise.push(el.id || el.className || el.tagName);
    const tk = M.querySelector('.t-ticker').getBoundingClientRect(); if (tk.top < vis.bottom && tk.bottom > vis.top) croise.push('ticker'); }
  const ok = cv.width === Math.round(parseFloat(cv.style.width) * dpr) && enc > 30 && tops.length === 1 && cs.whiteSpace === 'pre' && leg.textContent.includes('%') && dedans && !croise.length
    && /\d+ %/.test(lu.textContent) && !/\[[#-]+\]/.test(e.textContent);
  return { ok, leg: leg.textContent.replace(/\u00a0/g, ' '), lu: lu.textContent, forme: leg.dataset.forme, ech: +ech.toFixed(3), w: Math.round(b.width), h: Math.round(b.height), cvw: cv.width, dpr, enc, lettres,
    lignes: tops.length, fs: parseFloat(cs.fontSize), dedans, croise, cx: Math.round((anneau.left + anneau.right) / 2), cy: Math.round((anneau.top + anneau.bottom) / 2), vw: innerWidth, vh: innerHeight,
    cible: s ? +s.cible.toFixed(3) : null, vu: s ? +s.vu.toFixed(3) : null, op: +getComputedStyle(e).opacity }; }"""

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
        sc = pg.evaluate(SCEAU, '#menu-note')
        ok(s['menu'] and s['charge'] and sc['ok'] and 'CENTER-TOWN' in sc['lu'] and '%' in sc['leg'],
           f'{nom} ouverture de partie : le Terminal reste, monogramme NML (CENTER-TOWN, %) à la place de la ligne', sc)
        if nom == '1280': ok(sc['forme'] == 'longue' and 'CENTER-TOWN' in sc['leg'], '1280 : légende longue « CENTER-TOWN   n % » (place suffisante)', sc['leg'])
        ok(sc['fs'] >= 11, f'{nom} la légende du sceau est lisible (≥ 11 px, Plex)', sc['fs'])
        # anneau = vrai progrès : on lâche une partie des images retenues, l'anneau avance d'autant
        p0 = pg.evaluate("document.getElementById('menu-note')._sceau.cible"); n0 = len(hold.held)
        for r in hold.held[:n0 // 2]:
            try: r.continue_()
            except Exception: pass
        hold.held = hold.held[n0 // 2:]; time.sleep(1.5)
        s1 = pg.evaluate(SCEAU, '#menu-note')
        ok(s1['cible'] > p0 and s1['vu'] > 0 and abs(s1['vu'] - s1['cible']) < 0.2 and str(round(100 * s1['cible'])) in s1['leg'],
           f'{nom} l\'anneau suit le vrai chargement (images lâchées : {p0:.2f} -> {s1["cible"]:.2f}), le % de la légende aussi', s1)
        time.sleep(0.5); hold.relache()
        vides = []; fin = None
        while time.time() - t0 < 120:
            s = pg.evaluate(SONDE)
            signe = (s['menu'] and s['charge']) or s['chargeJeu']
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
        if not (s['creation'] or (s['menu'] and s['charge']) or s['chargeJeu']): vides.append(round(time.time() - t0, 2))
        time.sleep(0.2)
    ok(not s['menu'] and not s['creation'] and s['pret'], 'Nouvelle partie : en jeu après la création', {'s': s, 'boutons': done[:8]})
    ok(len(vides) <= 1, 'Nouvelle partie : pas de silence entre la création et le jeu', vides[:8])
    # 7. téléportation vers Pulse Plaza (images retenues) : monogramme NML en jeu, puis le lieu
    pg.evaluate("window.__nml.game.state.location = 'steel_pulse'"); time.sleep(0.8)
    s = pg.evaluate(SONDE); pg.screenshot(path=f'{OUT}1280_7_chargement_en_jeu.png')
    ok(s['chargeJeu'] and 'PULSE PLAZA' in s['ligneJeu'] and not s['pret'], 'en jeu : lieu pas encore chargé -> monogramme NML (PULSE PLAZA), monde figé', s)
    l1 = pg.evaluate(SCEAU, '#chargement'); ok(l1['ok'] and 'PULSE PLAZA' in l1['leg'] and 0.66 <= l1['cy'] / l1['vh'] <= 0.84 and abs(l1['cx'] - l1['vw'] / 2) <= 2 and 0.9 <= l1['op'] < 1,
       '1280 en jeu (Pulse Plaza) : badge NML en bas, centré, discret (opacité ~0,96), légende « PULSE PLAZA   n % »', l1)
    hold.relache()
    pg.wait_for_function("window.__nml.lieuPret('steel_pulse') && document.getElementById('chargement').hidden", timeout=120000); time.sleep(0.5)
    n = pg.evaluate("window.__nml.chargeur.cles('steel_pulse').filter(k => !window.__nml.chargeur.charge(k)).length")
    ok(n == 0, 'en jeu : Pulse Plaza chargé à l\'arrivée, toutes ses images présentes', n)
    pg.screenshot(path=f'{OUT}1280_8_pulse_charge.png')
    ok(not [e for e in errs if 'JS' in e], 'Nouvelle partie / passage : aucune erreur JS', errs[:3]); ctx.close()

    # 9. monogramme NML, Terminal et overlay en jeu, 1280 / 390 / fold plié / fold déplié
    for nom, w, h, mob in [('1280', 1280, 800, False), ('390', 390, 844, True), ('fold_plie_412', 412, 915, True), ('fold_deplie_884', 884, 1104, True)]:
        ctx, pg, errs = contexte(br, w, h, mob, save=SAVE)
        hc = Retenue(pg, re.compile(r'.*/assets/steel/center_town/.*\.(webp|png)$')); hp = Retenue(pg, re.compile(r'.*/assets/steel/pulse_plaza/.*\.(webp|png)$'))
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=120000)
        saute(pg); pg.evaluate("window.__nml.shell.terminal.saute()"); time.sleep(0.3)
        pg.click('#m-continue'); time.sleep(1.0)
        l = pg.evaluate(SCEAU, '#menu-note'); pg.screenshot(path=f'{OUT}{nom}_9_sceau_terminal.png')
        ok(pg.evaluate(SONDE)['charge'] and l['ok'] and l['lettres'] > 10, f'{nom} Terminal : monogramme NML net, dans l\'écran, sans recouvrir de texte, légende sur une ligne', l)
        hc.relache(); pg.wait_for_function("window.__nml.lieuPret('steel_center') && document.getElementById('menu').hidden", timeout=120000); time.sleep(0.3)
        pg.evaluate("window.__nml.game.state.location = 'steel_pulse'")  # la ligne paraît à l'image suivante (Center-Town : images lentes en swiftshader)
        pg.wait_for_function("!document.getElementById('chargement').hidden", timeout=20000); time.sleep(0.4)
        l = pg.evaluate(SCEAU, '#chargement'); pg.screenshot(path=f'{OUT}{nom}_9_sceau_en_jeu.png')
        ok(pg.evaluate(SONDE)['chargeJeu'] and l['ok'] and l['lettres'] > 10 and 0.66 <= l['cy'] / l['vh'] <= 0.84 and l['forme'] == 'longue',
           f'{nom} en jeu (Pulse Plaza) : badge NML en bas, dans la fenêtre, légende « PULSE PLAZA   n % » sur une ligne', l)
        hp.relache(); pg.wait_for_function("window.__nml.lieuPret('steel_pulse') && document.getElementById('chargement').hidden", timeout=120000)
        ok(not [e for e in errs if 'JS' in e], f'{nom} monogramme : aucune erreur JS', errs[:3]); ctx.close()

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
    # mouvement réduit + images retenues : le monogramme (hexagone + lettres) est là d'emblée, seul l'anneau avance
    ctx, pg, errs = contexte(br, save=SAVE, reduit=True); hold = Retenue(pg, re.compile(r'.*/assets/steel/center_town/.*\.(webp|png)$'))
    pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=120000); time.sleep(0.3)
    pg.click('#m-continue'); pg.wait_for_function("!!document.querySelector('#menu-note .nml-sceau')", timeout=10000)
    pg.evaluate('() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))')
    l = pg.evaluate(SCEAU, '#menu-note'); pg.screenshot(path=f'{OUT}1280_8_reduit_sceau.png')
    ok(l['ok'] and l['lettres'] > 10 and l['vu'] == l['cible'], 'mouvement réduit : hexagone et lettres déjà là dès la première image, l\'anneau sur le % sans glissement', l)
    hold.relache(); ctx.close()
    br.close()
bons = sum(1 for c, _ in R if c)
print(f'{bons}/{len(R)} OK'); print('ECHECS', len(R) - bons)
sys.exit(0 if bons == len(R) else 1)
