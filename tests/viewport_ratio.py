# Test anti-étirement mobile / pliant (#view CSS vs WebGL buffer vs frustum vs pointer/labels) :
# - Viewports : 880x1024 (pliant portrait), 1024x880 (rotation paysage), 390x844 (mobile DPR 2), 1280x720 (desktop)
# - Écart simulé 100vh != innerHeight / visualViewport.height (880x1024 avec barre d'adresse -> innerHeight=854, +20 % sur 100vh)
# - Vérifie sur vraies captures compositeur (pg.screenshot) que le rapport h/l reste invariant partout :
#   * cercle écran -> h/l = 1,00 (avant correctif sous écart 100vh : ~1,20)
#   * Guichets Human Corp (c_neon, ct_bord_sud_c_3q) -> h/l corps = 1,21 / complet = 1,31 (identique partout)
#   * Taxi v2 (ct_taxi1, ct_taxi_v2_3q) -> h/l = 0,58-0,59 (avant correctif sous écart 100vh : ~0,70-0,71 ; identique partout après)
# - Vérifie que pointer.js / pick() / labels utilisent exactement les mêmes dimensions (viewW x viewH == getBoundingClientRect)
# - Mesure à ppm=30 (1280x720 zoom 1,0) la hauteur rendue en px : PNJ / passants vs ct_taxi_v2_3q
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from nml_boot import passer_boot  # menu Terminal : sauter l'allumage
import io, os, sys, time, json
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

URL = os.environ.get('URL', 'http://127.0.0.1:8915/')
if not URL.endswith('/'): URL += '/'
OUT = os.environ.get('OUT', '/tmp/nml-test-out/center_arcadius2/')
os.makedirs(OUT, exist_ok=True)

fails = []
n = 0
def ok(c, m, d=''):
    global n
    print(('OK   ' if c else 'ECHEC ') + m + ('' if c else f'  {d}'), flush=True)
    n += bool(c)
    if not c:
        fails.append({'test': m, 'detail': str(d)[:260]})

def measure_non_magenta(png_bytes, body_frac=0.0, crop_h=None):
    arr = np.array(Image.open(io.BytesIO(png_bytes)).convert('RGB'), dtype=np.int16)
    if crop_h:
        arr = arr[:crop_h, :, :]
    fg = ~((arr[:, :, 0] > 220) & (arr[:, :, 1] < 35) & (arr[:, :, 2] > 220))
    ys, xs = np.where(fg)
    w = int(xs.max() - xs.min() + 1)
    h = int(ys.max() - ys.min() + 1)
    res = {'w': w, 'h': h, 'ratio': round(h / w, 4)}
    if body_frac > 0:
        row_counts = fg.sum(axis=1)
        yb = np.where(row_counts >= max(3, int(w * body_frac)))[0]
        hb = int(yb.max() - yb.min() + 1)
        res['body_h'] = hb
        res['body_ratio'] = round(hb / w, 4)
    return res

def measure_circle_on_black(png_bytes, crop_h=None):
    arr = np.array(Image.open(io.BytesIO(png_bytes)).convert('RGB'), dtype=np.int16)
    if crop_h:
        arr = arr[:crop_h, :, :]
    lum = arr.max(axis=2)
    ys, xs = np.where(lum > 45)
    w = int(xs.max() - xs.min() + 1)
    h = int(ys.max() - ys.min() + 1)
    return {'w': w, 'h': h, 'ratio': round(h / w, 4)}

report = {'avant_100vh_bug': {}, 'apres': {}, 'echelle_ppm30': {}}

with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=[
        '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'
    ])

    def boot_to_center(ctx, mob):
        pg = ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.goto(URL)
        pg.wait_for_function('window.__nml && window.__nml.shell', timeout=60000)
        pg.evaluate("localStorage.removeItem('nml_save_auto'); localStorage.removeItem('nml_zoom')")
        time.sleep(0.4)
        gesture = pg.touchscreen.tap if mob else pg.mouse.click
        passer_boot(pg)
        for sel in ['#m-new', '[data-race="augmente"]', '#cr-next', '#cr-enter']:
            b = pg.locator(sel).first.bounding_box()
            gesture(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2)
            time.sleep(0.28)
        pg.wait_for_function('!document.body.classList.contains("menu-open")', timeout=15000)
        pg.evaluate("""() => {
          const g = window.__nml.game, s = g.snapshot();
          s.location = 'steel_center'; s.player.x = 24; s.player.z = 18;
          Object.assign(s.flags, { q_start: true, q_fin: true, steel_passe: true, q_steel: true });
          g.restore(s, true);
        }""")
        time.sleep(0.6)
        return pg, errs

    def capture_isolated(pg, mode, target_id=None, cx=24, cz=18, zoom=1.0, force_old_bug=False):
        pg.evaluate("""({ mode, targetId, cx, cz, zoom, forceOldBug }) => {
          const w = window.__nml.game.world, loc = w.LOCATIONS.steel_center, v = window.__nml.view, g = window.__nml.game;
          window.__savedLoc ||= {
            buildings: [...loc.buildings], glows: [...loc.glows], pulses: [...loc.pulses],
            enseignes: [...loc.enseignes], drones: [...loc.drones], extras: [...loc.extras],
            walkers: [...loc.walkers], light: { ...loc.light }, ground: { ...loc.ground }, doors: [...w.DOORS], npcs: [...w.NPCS],
          };
          const S = window.__savedLoc;
          document.body.style.background = mode === 'circle' ? '#000000' : '#ff00ff';
          for (const id of ['hud','locbox','obj','msg','dialogue','panel','keys','zoom','act','mini','labels']) {
            const el = document.getElementById(id); if (el) el.style.visibility = 'hidden';
          }
          loc.ground = { ...S.ground, marge: null }; w.DOORS = []; w.NPCS = [];
          if (mode === 'circle') {
            loc.light = { bg: '#000000', hemi: ['#ffffff', '#ffffff', 1], sun: ['#ffffff', 0], tint: '#ffffff' };
            loc.buildings = []; loc.pulses = []; loc.enseignes = []; loc.drones = []; loc.extras = []; loc.walkers = [];
            loc.glows = [{ x: cx, z: cz, y: 0, r: 2.8, color: '#ffffff', i: 1.0 }];
            w.editorLayers = { zone: { visible: false }, building: { visible: false }, prop: { visible: false }, actor: { visible: false } };
          } else if (mode === 'building') {
            loc.light = { bg: '#ff00ff', hemi: ['#ffffff', '#ffffff', 1], sun: ['#ffffff', 0], tint: '#ffffff' };
            loc.buildings = S.buildings.filter(b => b.id === targetId).map(b => ({ ...b, tint: '#ffffff' }));
            loc.glows = []; loc.pulses = []; loc.enseignes = []; loc.drones = []; loc.extras = []; loc.walkers = [];
            w.editorLayers = { zone: { visible: false }, building: { visible: true }, prop: { visible: false }, actor: { visible: false } };
          } else if (mode === 'actor') {
            loc.light = { bg: '#ff00ff', hemi: ['#ffffff', '#ffffff', 1], sun: ['#ffffff', 0], tint: '#ffffff', actor: '#ffffff' };
            loc.buildings = []; loc.glows = []; loc.pulses = []; loc.enseignes = []; loc.drones = []; loc.walkers = [];
            loc.extras = targetId === 'player' ? [] : [{ sprite: targetId, x: cx, z: cz, face: 1, role: 'test' }];
            w.editorLayers = { zone: { visible: false }, building: { visible: false }, prop: { visible: false }, actor: { visible: targetId === 'player' } };
          }
          const snap = g.snapshot(); snap.player.x = cx; snap.player.z = cz; g.restore(snap, true);
          v.setZoom(zoom, { user: false });
          v.invalidate();
          for (let i = 0; i < 4; i++) v.render();
          if (forceOldBug) {
            const c = document.getElementById('view');
            c.style.width = '100vw'; c.style.height = '100vh';
          }
        }""", {'mode': mode, 'targetId': target_id, 'cx': cx, 'cz': cz, 'zoom': zoom, 'forceOldBug': force_old_bug})
        time.sleep(0.1)
        if force_old_bug:
            pg.evaluate("const c = document.getElementById('view'); c.style.width = '100vw'; c.style.height = '100vh';")
        raw = pg.screenshot()
        pg.evaluate("""() => {
          const w = window.__nml.game.world, loc = w.LOCATIONS.steel_center, S = window.__savedLoc;
          if (S) Object.assign(loc, {
            buildings: [...S.buildings], glows: [...S.glows], pulses: [...S.pulses],
            enseignes: [...S.enseignes], drones: [...S.drones], extras: [...S.extras],
            walkers: [...S.walkers], light: { ...S.light }, ground: { ...S.ground },
          });
          document.body.style.background = '';
          if (S) { w.DOORS = [...S.doors]; w.NPCS = [...S.npcs]; } delete w.editorLayers;
          for (const id of ['hud','locbox','obj','msg','dialogue','panel','keys','zoom','act','mini','labels']) {
            const el = document.getElementById(id); if (el) el.style.visibility = '';
          }
          window.__nml.view.invalidate();
          window.dispatchEvent(new Event('resize'));
          window.__nml.view.render();
        }""")
        return raw

    # A. Contexte mobile DPR 2 : 880x1024 (adresse 854 + plein), 1024x880 (rotation), 390x844
    ctx_mob = br.new_context(viewport={'width': 880, 'height': 1024}, has_touch=True, is_mobile=True, device_scale_factor=2)
    pg_mob, errs_mob = boot_to_center(ctx_mob, True)

    # Simuler l'écart mobile 100vh=1024 vs innerHeight=854 (+19,9 %)
    pg_mob.evaluate("""() => {
      Object.defineProperty(window, 'innerHeight', { value: 854, configurable: true });
      if (window.visualViewport) {
        Object.defineProperty(window.visualViewport, 'height', { value: 854, configurable: true });
        window.visualViewport.dispatchEvent(new Event('resize'));
      }
      window.dispatchEvent(new Event('resize'));
      window.__nml.view.render();
    }""")
    time.sleep(0.12)

    # Captures scène témoin AVANT (étirée +20 %) vs APRÈS (corrigée)
    pg_mob.evaluate("""() => {
      const g = window.__nml.game, s = g.snapshot(); s.player.x = 24.5; s.player.z = 24.5; g.restore(s, true);
      window.__nml.view.setZoom(1.0, { user: false });
      for (let i = 0; i < 4; i++) window.__nml.view.render();
      const c = document.getElementById('view'); c.style.width = '100vw'; c.style.height = '100vh';
    }""")
    pg_mob.screenshot(path=OUT + 'pliable_880x1024_avant_etire20pct.png')
    pg_mob.evaluate("window.dispatchEvent(new Event('resize')); window.__nml.view.render();")
    pg_mob.screenshot(path=OUT + 'pliable_880x1024_apres_fix.png')

    b_circ = measure_circle_on_black(capture_isolated(pg_mob, 'circle', cx=24, cz=18, zoom=1.1, force_old_bug=True))
    b_guich = measure_non_magenta(capture_isolated(pg_mob, 'building', 'c_neon', cx=22, cz=32, zoom=1.0, force_old_bug=True), body_frac=0.06)
    b_taxi = measure_non_magenta(capture_isolated(pg_mob, 'building', 'ct_taxi1', cx=15.8, cz=18.0, zoom=1.2, force_old_bug=True))
    report['avant_100vh_bug'] = {'cercle': b_circ, 'guichet_hc': b_guich, 'taxi': b_taxi}
    print('Témoin AVANT (100vh=1024 vs innerHeight=854) :', report['avant_100vh_bug'], flush=True)
    ok(1.17 <= b_circ['ratio'] <= 1.23 and 0.68 <= b_taxi['ratio'] <= 0.74,
       f'témoin AVANT reproduit l étirement +20 % : cercle={b_circ["ratio"]:.3f}, taxi={b_taxi["ratio"]:.3f}, guichet={b_guich["body_ratio"]:.3f}/{b_guich["ratio"]:.3f}')

    def measure_suite(pg, label, dpr, crop_css_h=None, shot_scene=None):
        ch = crop_css_h * dpr if crop_css_h else None
        c = measure_circle_on_black(capture_isolated(pg, 'circle', cx=24, cz=18, zoom=1.1), crop_h=ch)
        g = measure_non_magenta(capture_isolated(pg, 'building', 'c_neon', cx=22, cz=32, zoom=1.0), body_frac=0.06, crop_h=ch)
        t = measure_non_magenta(capture_isolated(pg, 'building', 'ct_taxi1', cx=15.8, cz=18.0, zoom=1.2), crop_h=ch)
        dims = pg.evaluate("""() => {
          const g = window.__nml.game, s = g.snapshot(); s.player.x = 24.5; s.player.z = 24.5; g.restore(s, true);
          window.__nml.view.setZoom(1.0, { user: false });
          for (let i = 0; i < 4; i++) window.__nml.view.render();
          const c = document.getElementById('view'), r = c.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
          const pTaxi = window.__nml.view.project(15.8, 0, 18.0), hitTaxi = window.__nml.view.pick(pTaxi.x, pTaxi.y);
          const pNeon = window.__nml.view.project(22.5, 0.8, 33.5), hitNeon = window.__nml.view.pick(pNeon.x, pNeon.y);
          const badLabels = [...document.querySelectorAll('.wlabel')].filter(l => !l.hidden && l.style.visibility !== 'hidden').filter(l => {
            const q = l.getBoundingClientRect();
            return q.width > 0 && (q.left < -1 || q.right > r.width + 1 || q.top < -1 || q.bottom > r.height + 1);
          }).map(l => l.textContent);
          return {
            cssW: Math.round(r.width), cssH: Math.round(r.height),
            bufW: Math.round(c.width / dpr), bufH: Math.round(c.height / dpr),
            hitTaxi: hitTaxi?.buildingId, hitNeon: hitNeon?.buildingId, badLabels,
          };
        }""")
        if shot_scene:
            pg.screenshot(path=OUT + shot_scene)
        report['apres'][label] = {'cercle': c, 'guichet_hc': g, 'taxi': t, 'dims': dims}
        ok(abs(c['ratio'] - 1.0) <= 0.02, f'{label} cercle reste un cercle (h/l={c["ratio"]:.3f})', c)
        ok(dims['cssW'] == dims['bufW'] and dims['cssH'] == dims['bufH']
           and dims['hitTaxi'] == 'ct_taxi1' and dims['hitNeon'] == 'c_neon' and not dims['badLabels'],
           f'{label} CSS==buffer ({dims["cssW"]}x{dims["cssH"]}), pick(taxi/guichet) exact, labels bornés', dims)

    # 1) 880x1024 avec barre d'adresse simulée (innerHeight=854)
    measure_suite(pg_mob, '880x1024_adresse854', dpr=2, crop_css_h=854)

    # 2) 880x1024 plein
    pg_mob.evaluate("""() => {
      delete window.innerHeight;
      if (window.visualViewport) delete window.visualViewport.height;
      window.dispatchEvent(new Event('resize'));
      window.__nml.view.render();
    }""")
    time.sleep(0.1)
    measure_suite(pg_mob, '880x1024', dpr=2, shot_scene='ratio_880x1024.png')

    # 3) 1024x880 (rotation paysage)
    pg_mob.set_viewport_size({'width': 1024, 'height': 880})
    pg_mob.evaluate("window.dispatchEvent(new Event('orientationchange')); window.__nml.view.render();")
    time.sleep(0.15)
    measure_suite(pg_mob, '1024x880_rotation', dpr=2, shot_scene='ratio_1024x880.png')

    # 4) 390x844 (mobile classique)
    pg_mob.set_viewport_size({'width': 390, 'height': 844})
    pg_mob.evaluate("window.dispatchEvent(new Event('resize')); window.__nml.view.render();")
    time.sleep(0.15)
    measure_suite(pg_mob, '390x844', dpr=2, shot_scene='ratio_390x844.png')
    ok(not errs_mob, 'mobile (880x1024 / 1024x880 / 390x844) aucune erreur JS', errs_mob[:3])
    ctx_mob.close()

    # B. Desktop 1280x720 (DPR 1, ppm=30 à zoom 1,0) + mesures en px PNJ vs Taxi
    ctx_desk = br.new_context(viewport={'width': 1280, 'height': 720}, device_scale_factor=1)
    pg_desk, errs_desk = boot_to_center(ctx_desk, False)
    measure_suite(pg_desk, '1280x720', dpr=1, shot_scene='ratio_1280x720.png')

    r_guich_full = [v['guichet_hc']['ratio'] for v in report['apres'].values()]
    r_guich_body = [v['guichet_hc']['body_ratio'] for v in report['apres'].values()]
    r_taxi = [v['taxi']['ratio'] for v in report['apres'].values()]
    r_circ = [v['cercle']['ratio'] for v in report['apres'].values()]
    ok(max(r_guich_full) - min(r_guich_full) <= 0.02 and max(r_guich_body) - min(r_guich_body) <= 0.025,
       f'Guichets Human Corp invariant sur les 5 configs (corps={r_guich_body}, complet={r_guich_full})')
    ok(max(r_taxi) - min(r_taxi) <= 0.02 and max(r_circ) - min(r_circ) <= 0.02,
       f'Taxi v2 et cercle invariants sur les 5 configs (taxi={r_taxi}, cercle={r_circ})')

    # Mesures exactes en px à ppm=30 (1280x720, zoom 1,0) : taxi vs joueur / passants
    m_taxi_30 = measure_non_magenta(capture_isolated(pg_desk, 'building', 'ct_taxi1', cx=15.8, cz=18.0, zoom=1.0))
    m_kiosq_30 = measure_non_magenta(capture_isolated(pg_desk, 'building', 'ct_kiosque0', cx=14.0, cz=22.0, zoom=1.0))
    m_player_30 = measure_non_magenta(capture_isolated(pg_desk, 'actor', 'player', cx=24.0, cz=18.0, zoom=1.0))
    m_civ0_30 = measure_non_magenta(capture_isolated(pg_desk, 'actor', 'st_civil0', cx=24.0, cz=18.0, zoom=1.0))
    m_nav_30 = measure_non_magenta(capture_isolated(pg_desk, 'actor', 'gen_ml_navetteur', cx=24.0, cz=18.0, zoom=1.0))
    m_foule_30 = measure_non_magenta(capture_isolated(pg_desk, 'actor', 'gen_pp_foule_c', cx=24.0, cz=18.0, zoom=1.0))
    report['echelle_ppm30'] = {
        'ppm': pg_desk.evaluate("window.__nml.view.ppm()"),
        'ct_taxi_v2_3q': m_taxi_30,
        'ct_kiosque_info_3q': m_kiosq_30,
        'player_1m80': m_player_30,
        'st_civil0_1m84': m_civ0_30,
        'gen_ml_navetteur_1m76': m_nav_30,
        'gen_pp_foule_c_1m74': m_foule_30,
    }
    print('Mesures rendues à ppm=30 :', json.dumps(report['echelle_ppm30'], ensure_ascii=False), flush=True)
    ok(not errs_desk, '1280x720 aucune erreur JS', errs_desk[:3])
    ctx_desk.close()
    br.close()

json.dump(report, open(OUT + 'ratios_et_echelle.json', 'w'), indent=2, ensure_ascii=False)
print(f'{n}/{n + len(fails)} OK')
sys.exit(1 if fails else 0)
