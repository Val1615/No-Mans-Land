# Test rapide Pulse Plaza (lot « centre désengorgé + marge sombre », dans le style de center_rapide.py) :
# - la zone se charge depuis Center-Town (porte c_nord), 9 PNJ, schéma valide, dalle sombre + allées, marge hors carte assombrie (voile >= 0,85)
# - 0 chevauchement d'emprises solides, 0 inversion d'ordre de profondeur (×0,6..×1,5, positions variées), view.masques() == [] (PNJ, figurants, passants),
#   0 figurant / passant / PNJ dans un solide, passants jamais masqués le long de leur trajet
# - props du centre lisibles : boîtes écran projetées (alpha du sprite, ancre comprise) sans recouvrement important (<= 25 % de la plus petite)
# - allée centrale (x 22-26, hors socle holo), accès ouest / est (z 12-16) et escalier sud (x 20-28) sans prop posé ; portes pp_ouest, pp_est, pp_sud joignables (findPath)
# - budget d'animations mobile (on <= 8), 45 calques rythmiques, aucune erreur JS / console / réseau
# - captures 1280x800 et 390x844 : vue d'ensemble ×0,6, centre de la place ×1,0, bord sud avec la marge ×1,0 (OUT, préfixe TAG)
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from nml_boot import passer_boot  # menu Terminal : sauter l'allumage
import os, sys, time, json, re, io, math, urllib.request
from PIL import Image
from playwright.sync_api import sync_playwright

URL = os.environ.get('URL', 'http://127.0.0.1:8916/')
if not URL.endswith('/'): URL += '/'
OUT = os.environ.get('OUT', '/tmp/nml-test-out/pulse_v4/')
TAG = os.environ.get('TAG', 'apres')
os.makedirs(OUT, exist_ok=True)

fails = []
n = 0
def ok(c, m, d=''):
    global n
    print(('OK   ' if c else 'ECHEC ') + m + ('' if c else f'  {d}'), flush=True)
    n += bool(c)
    if not c:
        fails.append({'test': m, 'detail': str(d)[:400]})

# Boîtes écran des sprites (repère caméra du jeu : yaw 34,5°, pitch 28,8°, 50 px d'image par mètre), découpées sur l'alpha réel de l'image servie
MAN = json.load(urllib.request.urlopen(URL + 'assets/steel/pulse_plaza/manifest.json'))
yaw, pitch = math.radians(34.5), math.radians(28.8)
dv = (-math.sin(yaw) * math.cos(pitch), -math.sin(pitch), -math.cos(yaw) * math.cos(pitch))
cr = lambda a, b: (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
nz = lambda a: tuple(x / math.sqrt(sum(y * y for y in a)) for x in a)
RIGHT = nz(cr(dv, (0, 1, 0))); UP = nz(cr(RIGHT, dv))
_bb = {}
def alpha_box(key):
    if key not in _bb:
        im = Image.open(io.BytesIO(urllib.request.urlopen(URL + 'assets/' + MAN[key]['file']).read())).convert('RGBA')
        _bb[key] = im.split()[3].point(lambda v: 255 if v > 40 else 0).getbbox()
    return _bb[key]
def screen_box(b):
    e = MAN.get(b['sprite'])
    if not e: return None
    an = b.get('ancre') or [0, 0]; ax, az = b['x'] + b['w'] + an[0], b['z'] + b['d'] + an[1]; k = b.get('k') or 1
    sx, sy = ax * RIGHT[0] + az * RIGHT[2], -(ax * UP[0] + az * UP[2]); x0, y0, x1, y1 = alpha_box(b['sprite'])
    return (sx + (x0 - e['anchor'][0]) / 50 * k, sy + (y0 - e['anchor'][1]) / 50 * k, sx + (x1 - e['anchor'][0]) / 50 * k, sy + (y1 - e['anchor'][1]) / 50 * k)
PROPS = re.compile(r'^pp_(holo|holo_tron|totem\d|ence\d|pont\d|arche\d|escalier|statue\d|jard\d|banc\d|lampe\d|borne\d)$')
SEULS_OK = {('pp_holo', 'pp_holo_tron')}  # l'hologramme est posé sur son socle

with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for name, vp, mob in [('desktop', (1280, 800), False), ('mobile', (390, 844), True)]:
        errs = []
        ctx = (br.new_context(viewport={'width': vp[0], 'height': vp[1]}, has_touch=True, is_mobile=True, device_scale_factor=2)
               if mob else br.new_context(viewport={'width': vp[0], 'height': vp[1]}))
        pg = ctx.new_page(); E = pg.evaluate
        gesture = pg.touchscreen.tap if mob else pg.mouse.click
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.on('response', lambda r: r.status >= 400 and errs.append(f'{r.status} {r.url}'))
        pg.goto(URL)
        pg.wait_for_function('window.__nml && window.__nml.shell', timeout=60000)
        E("localStorage.removeItem('nml_save_auto'); localStorage.removeItem('nml_zoom')")
        E("import('./src/core/path.js').then(m => window.__findPath = m.findPath)")
        time.sleep(0.6)
        def tapel(sel):
            b = pg.locator(sel).first.bounding_box(); gesture(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2); time.sleep(0.35)
        passer_boot(pg); tapel('#m-new'); tapel('[data-race="augmente"]'); tapel('#cr-next'); tapel('#cr-enter')
        pg.wait_for_function('!document.body.classList.contains("menu-open")', timeout=15000); time.sleep(0.6)
        E("""() => { const g = window.__nml.game, s = g.snapshot(); s.location = 'steel_center'; s.player.x = 33; s.player.z = 2;
          Object.assign(s.flags, { q_start: true, q_fin: true, steel_passe: true }); g.restore(s, true); }""")
        time.sleep(1.0)
        E("window.__nml.game.useDoor('c_nord')")
        try: pg.wait_for_function("window.__nml.state.location === 'steel_pulse'", timeout=15000)
        except Exception: pass
        time.sleep(1.5)
        ok(E("window.__nml.state.location") == 'steel_pulse', f'{name} porte Center-Town (c_nord) -> Pulse Plaza', E("window.__nml.state.location"))

        # 1. Données : PNJ, sol, marge
        L = E("""() => { const l = window.__nml.world.LOCATIONS.steel_pulse;
          return { npcs: window.__nml.world.NPCS.filter(n => n.location === 'steel_pulse').map(n => [n.id, n.x, n.z]), skin: l.ground.skin, marge: l.ground.marge,
            paint: (l.ground.paint || []).map(r => r.skin), b: l.buildings.map(b => ({ id: b.id, sprite: b.sprite, x: b.x, z: b.z, w: b.w, d: b.d, ancre: b.ancre || null, k: b.k || null, cover: !!b.cover, fond: !!b.fond, solid: b.solid ?? null })),
            ex: l.extras.length, wk: l.walkers.length, invalid: !!document.getElementById('editor-map-invalid') }; }""")
        ok(len(L['npcs']) == 9 and not L['invalid'] and L['skin'] == 'g_pp_dalle_sombre' and 'g_pp_allee' in L['paint'] and L['ex'] >= 30 and L['wk'] >= 4,
           f'{name} 9 PNJ, schéma valide, dalle sombre + allées, foule ({L["ex"]} figurants + {L["wk"]} passants)', L['npcs'])
        mg = L['marge'] or {}; va = re.match(r'rgba\(\s*(\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)', mg.get('voile', ''))
        ok(mg and va and float(va.group(4)) >= 0.85 and max(int(va.group(i)) for i in (1, 2, 3)) <= 24,
           f'{name} marge hors carte assombrie (voile {mg.get("voile")}, m {mg.get("m")})', mg)

        # 2. Boîtes écran : props du centre lisibles
        boxes = [(b['id'], screen_box(b)) for b in L['b'] if PROPS.match(b['id'])]
        ovl = []
        for i, (ia, ra) in enumerate(boxes):
            for ib, rb in boxes[i + 1:]:
                if not ra or not rb or (ia, ib) in SEULS_OK or (ib, ia) in SEULS_OK: continue
                ix, iy = min(ra[2], rb[2]) - max(ra[0], rb[0]), min(ra[3], rb[3]) - max(ra[1], rb[1])
                if ix > 0 and iy > 0:
                    r = ix * iy / min((ra[2] - ra[0]) * (ra[3] - ra[1]), (rb[2] - rb[0]) * (rb[3] - rb[1]))
                    if r > 0.25: ovl.append((ia, ib, round(r, 2)))
        ok(not ovl, f'{name} props du centre lisibles : aucun recouvrement écran > 25 % ({len(boxes)} props, holo + Holo-Tron exceptés)', ovl)

        # 3. Allée et accès libres (aucun prop posé), portes joignables
        bad = []
        for b in L['b']:
            if not PROPS.match(b['id']) or b['id'] in ('pp_holo', 'pp_holo_tron', 'pp_escalier'): continue
            x0, x1, z0, z1 = b['x'], b['x'] + b['w'], b['z'], b['z'] + b['d']
            if x0 < 26 and x1 > 22 and z1 > 4 and z0 < 28 and not (z0 >= 14 and z1 <= 22): bad.append(b['id'] + '@allée')
            if x0 < 4 and z0 < 16 and z1 > 12: bad.append(b['id'] + '@ouest')
            if x1 > 44 and z0 < 16 and z1 > 12: bad.append(b['id'] + '@est')
            if x0 < 28 and x1 > 20 and z1 > 28: bad.append(b['id'] + '@sud')
        ok(not bad, f'{name} allée centrale, accès ouest / est et escalier sud sans prop', bad)
        reach = E("""() => { const g = window.__nml.game, gr = g.grids.steel_pulse, out = {};
          for (const id of ['pp_ouest', 'pp_est', 'pp_sud']) { const d = g.doorById(id), [ci, cj] = gr.toCell(d.threshold.x, d.threshold.z);
            const a = window.__findPath(gr, { x: 1, z: 14 }, d.threshold), b = window.__findPath(gr, { x: 24, z: 30 }, d.threshold), c = window.__findPath(gr, { x: 40, z: 16 }, d.threshold);
            out[id] = { free: gr.free(ci, cj), a: a ? a.length : 0, b: b ? b.length : 0, c: c ? c.length : 0 }; } return out; }""")
        ok(all(v['free'] and v['a'] >= 1 and v['b'] >= 1 and v['c'] >= 1 for v in reach.values()), f'{name} portes pp_ouest / pp_est / pp_sud libres et joignables', reach)

        # 4. Solides, profondeur, masques, figurants / passants / PNJ hors solides
        SOL = [(b['id'], s['x'], s['z'], s['x'] + s['w'], s['z'] + s['d']) for b in L['b'] for s in (b['solid'] if b['solid'] is not None else [b])]
        chev = [(a[0], b[0]) for i, a in enumerate(SOL) for b in SOL[i + 1:] if a[0] != b[0] and a[1] < b[3] - 1e-6 and b[1] < a[3] - 1e-6 and a[2] < b[4] - 1e-6 and b[2] < a[4] - 1e-6]
        ok(not chev, f'{name} 0 chevauchement d emprises solides', chev)
        stab = E("""() => {
          const loc = window.__nml.world.LOCATIONS.steel_pulse, v = window.__nml.view, g = window.__nml.game, s = g.state, gr = g.grids.steel_pulse;
          v.render(); const B = loc.buildings.map(b => ({ id: b.id, o0: v.orderOf(b.id) })), rel = {};
          for (let i = 0; i < B.length; i++) for (let j = i + 1; j < B.length; j++) rel[B[i].id + '/' + B[j].id] = B[i].o0 < B[j].o0;
          const flips = [], mq = [], inSol = [], snap = g.snapshot();
          for (const [idx, e] of loc.extras.entries()) { const [ci, cj] = gr.toCell(e.x, e.z); if (!gr.free(ci, cj)) inSol.push('extra' + idx + '@' + e.x + ',' + e.z); }
          const SOL = loc.buildings.flatMap(b => b.solid ?? [{ x: b.x, z: b.z, w: b.w, d: b.d }]); // la case d'un PNJ est bloquée par le PNJ lui-même : on teste les emprises
          for (const n of window.__nml.world.NPCS.filter(n => n.location === 'steel_pulse')) if (SOL.some(q => n.x > q.x - 0.3 && n.x < q.x + q.w + 0.3 && n.z > q.z - 0.3 && n.z < q.z + q.d + 0.3)) inSol.push(n.id);
          for (const z of [0.6, 1.0, 1.5]) { v.setZoom(z, { user: false });
            for (const [px, pz] of [[2, 14], [12, 16], [24, 25], [34, 16], [40, 16], [24, 33], [8, 26], [38, 26]]) {
              s.player.x = px; s.player.z = pz; g.step(0.6); v.render();
              for (const m of v.masques()) mq.push(m.join(':'));
              for (let i = 0; i < B.length; i++) for (let j = i + 1; j < B.length; j++) { const k = B[i].id + '/' + B[j].id; if ((v.orderOf(B[i].id) < v.orderOf(B[j].id)) !== rel[k]) flips.push(k); } } }
          v.setZoom(1.0, { user: false }); g.restore(snap, true); v.render();
          for (const [wi, w] of loc.walkers.entries()) { const P = w.path;
            for (let i = 0; i < P.length; i++) { const a = P[i], b = P[(i + 1) % P.length], len = Math.hypot(b[0] - a[0], b[1] - a[1]), n = Math.max(4, Math.ceil(len * 4));
              for (let k = 0; k <= n; k++) { const x = a[0] + (b[0] - a[0]) * k / n, z = a[1] + (b[1] - a[1]) * k / n, [ci, cj] = gr.toCell(x, z);
                if (!gr.free(ci, cj)) inSol.push('walker' + wi + ':' + x.toFixed(1) + ',' + z.toFixed(1));
                for (const bid of v.masqueEn(x, z)) mq.push(bid + '@walker' + wi); } } }
          return { flips: [...new Set(flips)], mq: [...new Set(mq)], inSol: [...new Set(inSol)] }; }""")
        ok(not stab['flips'], f'{name} 0 inversion d ordre de profondeur entre bâtiments (×0,6..×1,5)', stab['flips'][:12])
        ok(not stab['mq'], f'{name} view.masques() == [] et passants jamais masqués (×0,6..×1,5)', stab['mq'][:20])
        ok(not stab['inSol'], f'{name} 0 figurant / passant / PNJ dans un solide', stab['inSol'][:20])

        # 5. Budget d'animations
        time.sleep(1.0); st = E("window.__nml.view.animStats")
        ok(st.get('on', 0) <= (8 if mob else 16) and st.get('pulses') == 45 and st.get('pulsesOn', 0) <= (8 if mob else 48),
           f'{name} budget animations (on={st.get("on")}, pulses={st.get("pulses")}, pulsesOn={st.get("pulsesOn")})', st)

        # 6. Captures (vue d'ensemble ×0,6, centre ×1,0, bord sud + marge ×1,0)
        def shot(fname, px, pz, zoom):
            E(f"""() => {{ const g = window.__nml.game, s = g.snapshot(); s.location = 'steel_pulse'; s.player.x = {px}; s.player.z = {pz}; g.restore(s, true);
              window.__nml.view.setZoom({zoom}, {{ user: false }}); const m = document.getElementById('msg'); if (m) m.textContent = ''; }}""")
            for _ in range(10): E("window.__nml.view.render()"); time.sleep(0.08)
            time.sleep(0.6); pg.screenshot(path=OUT + fname)
        w = vp[0]
        shot(f'{TAG}_ensemble_x06_{w}.png', 24, 25, 0.6)
        shot(f'{TAG}_centre_x10_{w}.png', 22, 25, 1.0)
        shot(f'{TAG}_bord_sud_marge_x10_{w}.png', 24, 34, 1.0)
        # 7. Gros plans : Feed v4 (écran animé dans le cadre peint, ECRAN_FEED.coins) et stand de nouilles
        dsf = 2 if mob else 1
        def closeup(fname, cx, cz, ppm):
            E(f"window.__nml.view.setCamera({{x:{cx},z:{cz},ppm:{ppm}}})")
            for _ in range(10): E("window.__nml.view.render()"); time.sleep(0.08)
            time.sleep(1.2); img = pg.screenshot(path=OUT + fname); return Image.open(io.BytesIO(img)).convert('RGB')
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=24;s.player.z=27;g.restore(s,true)})()"); time.sleep(0.8)
        ppm = 14 if mob else 26
        im = closeup(f'{TAG}_gros_plan_feed_{w}.png', 22, 9, ppm)
        coins = E("window.__nml.world.LOCATIONS.steel_pulse.buildings.find(b => b.id === 'pp_ecran_feed').ecran.coins")
        an = E("window.__nml.project(32, 0, 12)")
        scr = lambda u, v: ((an['x'] + (u - 828) / 50 * ppm) * dsf, (an['y'] + (v - 861) / 50 * ppm) * dsf)
        def lum(u, v, r=3):
            x0, y0 = scr(u, v); px = [im.getpixel((int(x0) + i, int(y0) + j)) for i in range(-r, r + 1) for j in range(-r, r + 1)
                                       if 0 <= int(x0) + i < im.width and 0 <= int(y0) + j < im.height]
            return sum(sum(c) for c in px) / max(1, len(px)) / 3
        (tl, tr, br_, bl) = coins
        inside = [lum(tl[0] + 40, tl[1] + 60), lum(tr[0] - 40, tr[1] + 60), lum(br_[0] - 40, br_[1] - 60), lum(bl[0] + 40, bl[1] - 60), lum((tl[0] + br_[0]) / 2, (tl[1] + br_[1]) / 2)]
        ok(coins == [[96, 18], [801, 251], [801, 706], [96, 472]] and min(inside) > 12 and max(inside) > 40,  # pages sombres du Feed possibles ; la dalle noire nue reste < 10
           f'{name} écran animé du Feed v4 dans le cadre peint (coins {coins}, luminance intérieure {[round(v) for v in inside]})', inside)
        E("window.__nml.view.setCamera(null)"); time.sleep(0.5)
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=38;s.player.z=27;g.restore(s,true)})()"); time.sleep(0.8)
        closeup(f'{TAG}_gros_plan_nouilles_{w}.png', 44, 28, 30 if mob else 48)
        E("window.__nml.view.setCamera(null)"); time.sleep(0.5)
        ok(not errs, f'{name} aucune erreur JS / console / réseau', errs[:3])
        ctx.close()
    br.close()

print(f'{n}/{n + len(fails)} OK')
json.dump({'ok': n, 'fails': fails}, open(OUT + f'resultats_{TAG}.json', 'w'), indent=1, ensure_ascii=False)
sys.exit(1 if fails else 0)
