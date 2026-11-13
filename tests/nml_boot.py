# Aide commune des tests : sauter la séquence d'allumage du menu Terminal (un geste pendant l'allumage ne fait que la sauter).
# Usage : passer_boot(pg) ou passer_boot(E) juste avant le premier clic sur #m-new.
# Contrôle aussi le lancement : dès la première image, pas d'ancien HUD ; le Terminal s'ouvre
# dès que son code est prêt, sans attendre le rendu de Center-Town.
# (13/11) Cinématique d'ouverture : sautée pour un navigateur piloté (sauf ?intro=1) ; passer_boot la passe aussi si elle est là.
# Section 3 : ?intro=1 -> première image = calque noir de la cinématique (pas de vestige, Terminal retenu), passage -> Terminal allumé ;
# ?intro=0 -> Terminal direct.
import os, sys, time

SAUTE_JS = """async () => {
  if (window.__nmlIntroActive) { dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' })); for (let i = 0; i < 100 && window.__nmlIntroActive; i++) await new Promise(r => setTimeout(r, 50)); }
  for (let i = 0; i < 1200 && !(window.__nml && window.__nml.shell && window.__nml.shell.terminal); i++) await new Promise(r => setTimeout(r, 50));
  const t = window.__nml && window.__nml.shell && window.__nml.shell.terminal; if (t) t.saute(); return !!t; }"""

def passer_boot(pg_ou_E):
    ev = pg_ou_E.evaluate if hasattr(pg_ou_E, 'evaluate') else pg_ou_E
    ok = ev(SAUTE_JS); time.sleep(0.15); return ok

# --- premier affichage : aucun vestige d'interface, le monde est caché ---
ETAT_AFFICHAGE_JS = """() => {
  const vis = id => { const e = document.getElementById(id); if (!e) return { existe: false }; const cs = getComputedStyle(e), r = e.getBoundingClientRect();
    const cache = e.hidden || cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0 || r.width === 0 || r.height === 0;
    return { existe: true, cache, vis: !cache, display: cs.display, visibility: cs.visibility, w: Math.round(r.width), h: Math.round(r.height) }; };
  const hud = vis('hud'), keys = vis('keys'), zoom = vis('zoom'), view = vis('view'), loc = vis('locbox'), menu = vis('menu');
  const txt = (document.body && document.body.innerText) || '';
  const texteHud = /POINTS DE VIE|DOLLARS|COMPAGNON/.test(txt) && hud.vis;
  const proto = /\\bPROTO\\b/.test(txt) && loc.vis;
  const dusk = /Dusk-Town|DUSK-TOWN/.test(txt) && (loc.vis || view.vis);
  const nilo = !!(document.getElementById('nilo-portrait') && !hud.cache);
  return { hud, keys, zoom, view, loc, menu, texteHud, proto, dusk, nilo,
    menuOpen: document.body.classList.contains('menu-open'),
    menuPret: !!window.__nmlMenuPret, cartePrete: !!window.__nmlCartePrete,
    boot: (document.getElementById('menu') || {}).dataset ? document.getElementById('menu').dataset.boot : '',
    booting: document.getElementById('menu') ? document.getElementById('menu').classList.contains('booting') : false };
}"""

def etat_affichage(pg):
    return pg.evaluate(ETAT_AFFICHAGE_JS)

def vestige_absent(etat):
    """Vrai si l'ancienne page (HUD, Dollars, Nilo, Dusk-Town, barre d'icônes, monde) n'est pas visible."""
    return (etat['menuOpen'] and not etat['hud']['vis'] and not etat['keys']['vis'] and not etat['zoom']['vis']
            and not etat['view']['vis'] and not etat['loc']['vis'] and not etat['texteHud'] and not etat['proto']
            and not etat['dusk'] and not etat['nilo'])

# Script de premier cadre : s'exécute avant tout module de la page.
INIT_PREMIER_CADRE = """
window.__nmlPremierCadre = new Promise(resolve => {
  const lire = () => {
    const vis = id => { const e = document.getElementById(id); if (!e) return { vis: false, cache: true }; const cs = getComputedStyle(e);
      const cache = e.hidden || cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0; return { vis: !cache, cache, visibility: cs.visibility }; };
    resolve({ hud: vis('hud'), keys: vis('keys'), zoom: vis('zoom'), view: vis('view'), loc: vis('locbox'), menu: vis('menu'),
      menuOpen: !!(document.body && document.body.classList.contains('menu-open')),
      classesMenu: (document.getElementById('menu') && document.getElementById('menu').className) || '' });
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => requestAnimationFrame(lire));
  else requestAnimationFrame(lire);
});
"""

def controler_lancement(pg, hold_carte=True, timeout=30000):
    """Vérifie : premier cadre sans vestige ; Terminal visible dès que son code est prêt, carte éventuellement encore en cours."""
    R = {}
    if hold_carte:
        # on retient les textures Center-Town jusqu'à ce que le menu soit prêt
        held = []
        def hold(route):
            held.append(route)
        pg.route('**/assets/steel/center_town/**', hold)
        R['held'] = held
    pg.add_init_script(INIT_PREMIER_CADRE)
    pg.goto(os.environ.get('URL', 'http://127.0.0.1:8921/'), wait_until='domcontentloaded')
    premier = pg.evaluate('() => window.__nmlPremierCadre')
    R['premier'] = premier
    R['premier_ok'] = (premier.get('menuOpen') and not premier['hud']['vis'] and not premier['keys']['vis']
                       and not premier['zoom']['vis'] and not premier['view']['vis'] and not premier['loc']['vis']
                       and premier['menu']['vis'])
    pg.wait_for_function('window.__nmlMenuPret === true', timeout=timeout)
    etat = etat_affichage(pg)
    R['menu'] = etat
    R['menu_ok'] = vestige_absent(etat) and etat['menu']['vis'] and etat['menuPret']
    # indépendance : le menu est là alors que la carte n'est pas encore signalée prête
    R['avant_carte'] = not etat['cartePrete']
    R['independant_ok'] = R['menu_ok'] and (not hold_carte or not etat['cartePrete'])
    if hold_carte:
        for route in R.get('held') or []:
            try: route.continue_()
            except Exception: pass
        try: pg.unroute('**/assets/steel/center_town/**')
        except Exception: pass
    return R

if __name__ == '__main__':
    from playwright.sync_api import sync_playwright
    URL = os.environ.get('URL', 'http://127.0.0.1:8921/')
    OUT = os.environ.get('OUT', '/tmp/nml-test-out/boot_menu_direct/')
    os.makedirs(OUT, exist_ok=True)
    FORMATS = [('1280x800', 1280, 800, False), ('390x844', 390, 844, True), ('fold_plie_412x915', 412, 915, True)]
    if os.environ.get('FORMATS'):
        FORMATS = [f for f in FORMATS if f[0] in os.environ['FORMATS'].split(',')]
    R = []
    def ok(c, n, d=''):
        R.append((bool(c), n)); print(('OK   ' if c else 'ECHEC ') + n + ('' if c else f'  {d}'), flush=True)
    with sync_playwright() as p:
        br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        # 1. indépendance menu / carte (Center-Town retenu)
        ctx = br.new_context(viewport={'width': 1280, 'height': 800})
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append('JS ' + str(e)))
        r = controler_lancement(pg, hold_carte=True)
        ok(r['premier_ok'], 'premier cadre : pas de HUD / barre / zoom / monde / PROTO, menu déjà là', r['premier'])
        ok(r['menu_ok'], 'Terminal ouvert dès que son code est prêt, vestige absent', r['menu'])
        ok(r['independant_ok'], 'Terminal ouvert sans attendre le rendu de Center-Town', {'cartePrete': r['menu'].get('cartePrete'), 'held': len(r.get('held') or [])})
        ok(not errs, 'aucune erreur JS pendant le lancement anticipé', errs[:3])
        pg.screenshot(path=OUT + 'independance_menu_avant_carte.png')
        # laisser la carte se terminer pour passer_boot
        try:
            pg.wait_for_function('window.__nml && window.__nml.shell && window.__nml.shell.terminal', timeout=90000)
            ok(passer_boot(pg), 'passer_boot saute l\'allumage une fois le shell prêt')
        except Exception as e:
            ok(False, 'shell disponible après relâchement de Center-Town', str(e))
        ctx.close()
        # 2. séquence de lancement 1280 / 390 / fold à t=0, 0,5 s, 2 s
        for nom, w, h, mob in FORMATS:
            ctx = br.new_context(viewport={'width': w, 'height': h}, has_touch=mob, is_mobile=mob, device_scale_factor=2 if mob else 1)
            pg = ctx.new_page(); pg.add_init_script(INIT_PREMIER_CADRE)
            t0 = time.time()
            pg.goto(URL, wait_until='domcontentloaded')
            premier = pg.evaluate('() => window.__nmlPremierCadre')
            pg.screenshot(path=f'{OUT}{nom}_t0.png')
            et0 = etat_affichage(pg)
            ok(r_ok := (premier.get('menuOpen') and not premier['hud']['vis'] and not premier['keys']['vis'] and not premier['view']['vis'] and not et0['texteHud'] and not et0['nilo'] and not et0['dusk']),
               f'{nom} t=0 : pas de vestige (HUD / Dollars / Nilo / Dusk-Town / barre / monde)', {'premier': premier, 'etat': et0})
            while time.time() - t0 < 0.5: time.sleep(0.01)
            pg.screenshot(path=f'{OUT}{nom}_t500ms.png')
            try:
                pg.wait_for_function('window.__nmlMenuPret === true', timeout=20000)
                menu_a_05 = True
            except Exception:
                menu_a_05 = bool(etat_affichage(pg)['menuPret'])
            et5 = etat_affichage(pg)
            ok(vestige_absent(et5) and et5['menu']['vis'], f'{nom} t=0,5 s : Terminal visible, vestige absent', et5)
            while time.time() - t0 < 2.0: time.sleep(0.01)
            pg.screenshot(path=f'{OUT}{nom}_t2000ms.png')
            et2 = etat_affichage(pg)
            ok(vestige_absent(et2) and et2['menu']['vis'] and (et2['booting'] or et2['boot'] in ('repos', 'b-log', 'b-line', 'b-open', 'b-warm', 'b-off', 'b-logout', 'b-title', 'b-items', 'b-status', 'b-stamp')),
               f'{nom} t=2 s : Terminal en allumage (ou repos), pas de vestige', et2)
            ctx.close()
        br.close()
        # 3. cinématique d'ouverture : première image noire, Terminal retenu, passage, ?intro=0 (un navigateur neuf par format)
        for nom, w, h, mob in FORMATS:
            br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=user-gesture-required'])
            ctx = br.new_context(viewport={'width': w, 'height': h}, has_touch=mob, is_mobile=mob, device_scale_factor=2 if mob else 1)
            pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append('JS ' + str(e)))
            pg.add_init_script("window.__p = new Promise(r => { const f = () => { const I = document.getElementById('intro'); r({ intro: !!I && getComputedStyle(I).display !== 'none', fond: I ? getComputedStyle(I).backgroundColor : '' }); }; if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => requestAnimationFrame(f)); else requestAnimationFrame(f); });")
            pg.goto(URL + ('&' if '?' in URL else '?') + 'intro=1', wait_until='domcontentloaded')
            pr = pg.evaluate('window.__p'); et = etat_affichage(pg)
            ok(pr['intro'] and pr['fond'] == 'rgb(0, 0, 0)' and not et['hud']['vis'] and not et['texteHud'] and not et['nilo'], f'{nom} ?intro=1 : première image = calque noir de la cinématique, aucun vestige', [pr, et])
            pg.wait_for_function("window.__nmlIntro && window.__nmlIntro.etat === 'invite'", timeout=20000, polling=100); time.sleep(1.5)
            ok(not pg.evaluate('!!window.__nmlMenuPret') and pg.evaluate("(document.getElementById('menu').dataset.boot || '') === ''"), f'{nom} pendant la cinématique : allumage du Terminal retenu')
            pg.screenshot(path=f'{OUT}{nom}_cinematique_invite.png')
            (pg.touchscreen.tap if mob else pg.mouse.click)(w / 2, h / 2); pg.wait_for_function("window.__nmlIntro.etat === 'lecture'", timeout=20000, polling=100)
            time.sleep(1.0); ok(passer_boot(pg) and not pg.evaluate('!!document.getElementById("intro")'), f'{nom} passer_boot passe la cinématique puis l\'allumage')
            et = etat_affichage(pg); ok(vestige_absent(et) and et['menu']['vis'] and et['menuPret'], f'{nom} après la cinématique : Terminal visible, vestige absent', et)
            ok(not errs, f'{nom} cinématique : aucune erreur JS', errs[:3]); ctx.close()
            ctx = br.new_context(viewport={'width': w, 'height': h}); pg = ctx.new_page()
            pg.goto(URL + ('&' if '?' in URL else '?') + 'intro=0'); pg.wait_for_function('window.__nmlMenuPret === true', timeout=30000, polling=100)
            ok(not pg.evaluate('!!document.getElementById("intro")') and pg.evaluate("window.__nmlIntro.fin") == 'absente', f'{nom} ?intro=0 : Terminal direct, sans cinématique')
            ctx.close(); br.close()
    n = sum(1 for c, _ in R if c); print(f'{n}/{len(R)} OK'); print('ECHECS', len(R) - n); sys.exit(0 if n == len(R) else 1)
