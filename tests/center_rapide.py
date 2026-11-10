# Test rapide Center-Town · Carrefour Arcadius (lot v3 f6dbb6b + swap poses) :
# - 7 sols g_ct_* + vraie nuit noire (#05070d), 26 bâtiments ct_*_v3_3q (0 clé obsolète, ct_taxi_v3_3q vérifié sur ct_taxi0/ct_taxi1)
# - Étiquettes « Fréquence Strip » et « Pulse Plaza » calées sur les débouchés des sorties (labelPos), hors Dôme Fréquence, QG Arcadius et HUD
# - Foule densifiée sur trottoirs, parvis et passages piétons (51 figurants + 8 passants <= 8 anims mobile), hors solids, view.masques() == []
# - 10 portes joignables (findPath), c_change_door ([451, 1444] -> change_in), c_dome ([22, 12] -> steel_dome intact), fondu 30 % auto de Teng vers c_mega
# - Calques _pulse des 5 tours battant sur 01_center_town.mp3, pulsesOn <= 8 sur mobile, captures 1280/390 sous /tmp/nml-test-out/center_arcadius2/
import os, sys, time, json, re, urllib.request
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

DOORS_10 = ['c_ouest', 'c_est', 'c_mega', 'c_strip', 'c_nord', 'c_sud', 'c_pp_sud', 'c_sud_est', 'c_change_door', 'c_dome']
EXPECTED_SPRITES = {
    'ct_arcadius_qg_v3_3q', 'ct_dome_frequence_v3_3q', 'ct_bureau_permis_v3_3q',
    'ct_tour_teng_v3_3q', 'ct_tour_archeon_v3_3q', 'ct_tour_orc_v3_3q', 'ct_tour_humancorp_v3_3q', 'ct_tour_nexus_v3_3q',
    'ct_bord_sud_a_v3_3q', 'ct_bord_sud_b_v3_3q', 'ct_bord_sud_c_v3_3q',
    'ct_monorail_viaduc_v3_3q', 'ct_monorail_rame_v3_3q', 'ct_holo_suspendu_v3_3q',
    'ct_arret_tram_v3_3q', 'ct_tram_v3_3q', 'ct_taxi_v3_3q',
    'ct_echoppe_vapeur_v3_3q', 'ct_kiosque_info_v3_3q',
    'ct_lampadaire_io_v3_3q', 'ct_banniere_io_v3_3q', 'ct_cerisier_bac_v3_3q',
}
OBSOLETE_V1 = {
    'ct_cerisier_bac_3q', 'ct_taxi_3q',
    'ct_tour_teng_3q', 'ct_tour_archeon_3q', 'ct_tour_orc_3q', 'ct_tour_humancorp_3q', 'ct_tour_nexus_3q',
    'b_st_ct_tower', 'b_st_ct_dome', 'b_st_ct_shop', 'b_st_blanc',
    'b_st_immeuble', 'b_st_galerie', 'b_st_neon', 'b_st_jumelles',
    'df_ens_facade_vibes', 'df_ens_facade_tron',
    'ct_arcadius_qg_3q', 'ct_dome_frequence_3q', 'ct_bureau_permis_3q',
    'ct_tour_teng_v2_3q', 'ct_tour_archeon_v2_3q', 'ct_tour_orc_v2_3q', 'ct_tour_humancorp_v2_3q', 'ct_tour_nexus_v2_3q',
    'ct_bord_sud_a_3q', 'ct_bord_sud_b_3q', 'ct_bord_sud_c_3q',
    'ct_monorail_viaduc_3q', 'ct_monorail_rame_3q', 'ct_holo_suspendu_3q',
    'ct_arret_tram_3q', 'ct_tram_3q', 'ct_taxi_v2_3q',
    'ct_echoppe_vapeur_3q', 'ct_kiosque_info_3q',
    'ct_lampadaire_io_3q', 'ct_banniere_io_3q', 'ct_cerisier_bac_v2_3q',
}
EXPECTED_SOLS = {
    'g_ct_trottoir_dalles', 'g_ct_asphalte_mouille', 'g_ct_rails_tram_ew',
    'g_ct_rails_tram_ns', 'g_ct_passage_pieton_ns', 'g_ct_passage_pieton_ew', 'g_ct_carrefour_jaune',
}

with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=[
        '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'
    ])
    for name, vp, mob in [('desktop', (1280, 800), False), ('mobile', (390, 844), True)]:
        errs = []
        ctx = (br.new_context(viewport={'width': vp[0], 'height': vp[1]}, has_touch=True, is_mobile=True, device_scale_factor=2)
               if mob else br.new_context(viewport={'width': vp[0], 'height': vp[1]}))
        pg = ctx.new_page()
        E = pg.evaluate
        gesture = pg.touchscreen.tap if mob else pg.mouse.click
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.on('response', lambda r: r.status >= 400 and errs.append(f'{r.status} {r.url}'))

        pg.goto(URL)
        pg.wait_for_function('window.__nml && window.__nml.shell && window.__nml.ostCentre', timeout=60000)
        E("localStorage.removeItem('nml_muted'); localStorage.removeItem('nml_save_auto'); localStorage.removeItem('nml_zoom')")
        E("import('./src/core/path.js').then(m => window.__findPath = m.findPath)")
        time.sleep(0.6)

        def tapel(sel):
            b = pg.locator(sel).first.bounding_box()
            gesture(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2)
            time.sleep(0.35)

        tapel('#m-new'); tapel('[data-race="augmente"]'); tapel('#cr-next'); tapel('#cr-enter')
        pg.wait_for_function('!document.body.classList.contains("menu-open")', timeout=15000)
        time.sleep(0.6)

        E("""() => {
          const g = window.__nml.game, s = g.snapshot();
          s.location = 'steel_center'; s.player.x = 24; s.player.z = 18;
          Object.assign(s.flags, { q_start: true, q_fin: true, steel_passe: true, q_steel: true });
          g.restore(s, true);
        }""")
        pg.wait_for_function("window.__nml.state.location === 'steel_center' && !window.__nml.music.paused && Math.abs(window.__nml.music.volume - 0.55) < 0.06", timeout=12000)
        time.sleep(0.6)

        # 1. Sols, lumière nuit, clés v3 (dont ct_taxi_v3_3q), foule densifiée et absence d'obsolètes
        info = E("""() => {
          const l = window.__nml.world.LOCATIONS.steel_center;
          return {
            bg: window.__nml.view.lightOf().bg,
            skin: l.ground.skin,
            marge: l.ground.marge?.skin,
            paint: (l.ground.paint || []).map(r => r.skin),
            props: l.props.length,
            bs: l.buildings.map(b => [b.id, b.sprite, b.x, b.z, b.w, b.d]),
            taxis: l.buildings.filter(b => b.id.startsWith('ct_taxi')).map(b => [b.id, b.sprite, b.x, b.z, b.w, b.d]),
            extras: l.extras.map(e => [e.sprite, e.x, e.z]),
            walkers: l.walkers.map(w => [w.sprite, w.path.length]),
            invalid: !!document.getElementById('editor-map-invalid'),
          };
        }""")
        sprites_used = {b[1] for b in info['bs']}
        sols_used = {info['skin'], info['marge'], *info['paint']}
        ok(info['bg'] == '#05070d' and sols_used == EXPECTED_SOLS and info['props'] == 0 and not info['invalid'],
           f'{name} nuit #05070d + 7 sols g_ct_* + props vides + schéma valide', (info['bg'], sorted(EXPECTED_SOLS ^ sols_used), info['props']))
        ok(sprites_used == EXPECTED_SPRITES and not (sprites_used & OBSOLETE_V1) and len(info['bs']) == 26,
           f'{name} 22 clés ct_*_v3_3q (26 instances, 0 clé obsolète, sans jumelles ni FACADE_DOME)', sorted(EXPECTED_SPRITES ^ sprites_used))
        ok(len(info['taxis']) == 2 and all(t[1] == 'ct_taxi_v3_3q' and t[4] == 4.5 and t[5] == 1.8 for t in info['taxis']),
           f'{name} ct_taxi0 et ct_taxi1 posent bien ct_taxi_v3_3q (4,5x1,8 m)', info['taxis'])
        crowd_sprites = {e[0] for e in info['extras']} | {w[0] for w in info['walkers']}
        ok(len(info['extras']) >= 40 and 5 <= len(info['walkers']) <= 8 and len(crowd_sprites) >= 14,
           f'{name} foule densifiée ({len(info["extras"])} figurants + {len(info["walkers"])} passants <= 8, {len(crowd_sprites)} sprites distincts)',
           (len(info['extras']), len(info['walkers']), len(crowd_sprites)))

        # 2. Collisions solides, figurants/passants hors solids, stabilité profondeur (x0,6..x1,5) et masques == []
        SOL = E("window.__nml.world.LOCATIONS.steel_center.buildings.flatMap(b=>(b.solid??[{x:b.x,z:b.z,w:b.w,d:b.d}]).map(s=>[b.id,s.x,s.z,s.x+s.w,s.z+s.d]))")
        chev_sol = [(a[0], b[0]) for i, a in enumerate(SOL) for b in SOL[i + 1:]
                    if a[0] != b[0] and a[1] < b[3] - 1e-6 and b[1] < a[3] - 1e-6 and a[2] < b[4] - 1e-6 and b[2] < a[4] - 1e-6]
        ok(not chev_sol, f'{name} 0 chevauchement de sous-rectangles solides', chev_sol)

        stab = E("""() => {
          const loc = window.__nml.world.LOCATIONS.steel_center, v = window.__nml.view, g = window.__nml.game, s = g.state, gr = g.grids.steel_center;
          v.render();
          const B = loc.buildings.map(b => ({ id: b.id, o0: v.orderOf(b.id) }));
          const rel = {};
          for (let i = 0; i < B.length; i++) for (let j = i + 1; j < B.length; j++) rel[B[i].id + '/' + B[j].id] = B[i].o0 < B[j].o0;
          const flips = [], mq = [], inSol = [], snap = g.snapshot();
          for (const [idx, e] of loc.extras.entries()) {
            const [ci, cj] = gr.toCell(e.x, e.z);
            if (!gr.free(ci, cj)) inSol.push('extra' + idx);
          }
          for (const z of [0.6, 1.0, 1.5]) {
            v.setZoom(z, { user: false });
            for (const [px, pz] of [[2.5, 18], [13.5, 9.5], [22, 14], [30, 18], [44, 18], [26, 33]]) {
              s.player.x = px; s.player.z = pz; g.step(0.6); v.render();
              for (const m of v.masques()) mq.push(m.join(':'));
              for (let i = 0; i < B.length; i++) for (let j = i + 1; j < B.length; j++) {
                const k = B[i].id + '/' + B[j].id;
                if ((v.orderOf(B[i].id) < v.orderOf(B[j].id)) !== rel[k]) flips.push(k);
              }
            }
          }
          v.setZoom(1.0, { user: false }); g.restore(snap, true); v.render();
          for (const [wi, w] of loc.walkers.entries()) {
            const P = w.path;
            for (let i = 0; i < P.length; i++) {
              const a = P[i], b = P[(i + 1) % P.length], len = Math.hypot(b[0] - a[0], b[1] - a[1]), n = Math.max(4, Math.ceil(len * 4));
              for (let k = 0; k <= n; k++) {
                const x = a[0] + (b[0] - a[0]) * k / n, z = a[1] + (b[1] - a[1]) * k / n;
                const [ci, cj] = gr.toCell(x, z);
                if (!gr.free(ci, cj)) inSol.push('walker' + wi + ':' + x.toFixed(1) + ',' + z.toFixed(1));
                for (const bid of v.masqueEn(x, z)) mq.push(bid + '@walker' + wi);
              }
            }
          }
          return { flips: [...new Set(flips)], mq: [...new Set(mq)], inSol: [...new Set(inSol)] };
        }""")
        ok(not stab['flips'] and not stab['mq'] and not stab['inSol'],
           f'{name} 0 inversion de profondeur, 0 figurant/passant en solid et view.masques() == [] (×0,6..×1,5)', stab)

        # 3. Calques additifs + rythme kick sur 01_center_town.mp3 + plafond mobile <= 8
        samples = []
        max_bass = max_energy = 0.0
        # l'OST peut mettre ~1,5 s à se charger (Pages, mobile) : on attend qu'elle joue vraiment, puis on mesure sur ~4 s
        for _ in range(60):
            if E("(() => { const m = window.__nml.music; return !!window.__nml.ostCentre.playing && !m.paused && m.currentTime > 0.5 && m.readyState >= 3; })()"): break
            time.sleep(0.1)
        for _ in range(60):
            time.sleep(0.06)
            E("window.__nml.view.render()"); samples.append(E("Object.fromEntries(window.__nml.view.pulses().map(p => [p.key, p.opacity]))"))
            ost = E("({ mode: window.__nml.ostCentre.mode, active: window.__nml.ostCentre.active, playing: window.__nml.ostCentre.playing, bass: window.__nml.ostCentre.bass, energy: window.__nml.ostCentre.energy })")
            max_bass = max(max_bass, ost['bass'])
            max_energy = max(max_energy, ost['energy'])
        st = E("({...window.__nml.view.animStats, walkers: window.__nml.world.LOCATIONS.steel_center.walkers.length})")
        tower_pulse_keys = [f'ct_tour_{t}_v3_3q_pulse' for t in ('teng', 'orc', 'archeon', 'nexus', 'humancorp')]
        spans = {k: round(max(s.get(k, 0) for s in samples) - min(s.get(k, 0) for s in samples), 3) for k in tower_pulse_keys}
        ok(st['enseignes'] == 24 and st['fenetres'] == 26 and st['pulses'] == 19 and st['on'] <= 8 and st['walkers'] <= 8
           and st['pulsesOn'] <= (8 if mob else 48) and st['pulsesOn'] >= (8 if mob else 12),
           f'{name} calques additifs & plafond mobile <= 8 : on={st["on"]}, walkers={st["walkers"]}, pulsesOn={st["pulsesOn"]}', st)
        ok(ost['mode'] == 'ost_center_town' and not ost['active'] and ost['playing'] and max_bass > 0.05 and max_energy > 0.04 and all(v > 0.12 for v in spans.values()),
           f'{name} OST Center-Town pilote les 5 _pulse des tours v3 sur le kick (bass={max_bass:.2f}, spans={spans})', (ost, spans))

        # 4. 10 portes joignables depuis l'entrée (1, 18) et depuis le carrefour (30, 18)
        reach = E(f"""() => {{
          const g = window.__nml.game, gr = g.grids.steel_center, out = {{}};
          for (const id of {json.dumps(DOORS_10)}) {{
            const d = g.doorById(id);
            const [ci, cj] = gr.toCell(d.threshold.x, d.threshold.z);
            const p1 = window.__findPath(gr, {{ x: 1, z: 18 }}, d.threshold);
            const p2 = window.__findPath(gr, {{ x: 30, z: 18 }}, d.threshold);
            out[id] = {{ free: gr.free(ci, cj), p1: p1 ? p1.length : 0, p2: p2 ? p2.length : 0, th: d.threshold }};
          }}
          return out;
        }}""")
        ok(len(reach) == 10 and all(v['free'] and v['p1'] >= 1 and v['p2'] >= 2 for v in reach.values()),
           f'{name} 10/10 portes libres et joignables depuis (1;18) et (30;18)', reach)

        # 5. Fondu auto 30 % de Tour Teng v3 (~29 m) vers c_mega (8 ; 1)
        if not mob:
            E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=8;s.player.z=1.2;g.restore(s,true)})()")
            for _ in range(18):
                E("window.__nml.view.render()"); time.sleep(0.03)
            op_teng = E("window.__nml.view.opacityOf('c_change')")
            ok(op_teng is not None and op_teng < 0.35, f'desktop fondu 30 % auto de Tour Teng v3 devant c_mega (opacity={op_teng:.2f})', op_teng)
            pg.screenshot(path=OUT + 'teng_fondu_mega_1280.png')

        # 6. Transitions intérieures : c_change_door -> change_in et c_dome -> steel_dome (non reconstruit, 10 PNJ)
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=13;s.player.z=8.5;g.restore(s,true);g.useDoor('c_change_door')})()")
        pg.wait_for_function("window.__nml.state.location === 'change_in'", timeout=8000)
        ok(E("window.__nml.state.location") == 'change_in', f'{name} porte c_change_door ([451, 1444]) -> change_in')
        E("window.__nml.game.useDoor('change_in_door')")
        pg.wait_for_function("window.__nml.state.location === 'steel_center'", timeout=8000)

        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=22;s.player.z=13;s.flags.dome_ouvert=true;g.restore(s,true);g.useDoor('c_dome')})()")
        pg.wait_for_function("window.__nml.state.location === 'steel_dome'", timeout=8000)
        dome_ok = E("window.__nml.state.location === 'steel_dome' && window.__nml.world.NPCS.filter(n=>n.location==='steel_dome').length === 10 && window.__nml.world.LOCATIONS.steel_dome.buildings.length >= 20")
        ok(dome_ok, f'{name} porte c_dome (22;12) -> zone steel_dome existante intacte')
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=15;s.player.z=29;g.restore(s,true);g.useDoor('df_sortie')})()")
        pg.wait_for_function("window.__nml.state.location === 'steel_center'", timeout=8000)

        # 7. Étiquettes des sorties hors monuments/HUD + Captures 1280 et 390 sous /tmp/nml-test-out/center_arcadius2/
        wtag = str(vp[0])
        def check_labels_and_shot(fname, px, pz, zoom):
            E(f"""() => {{
              const g = window.__nml.game, s = g.snapshot();
              s.location = 'steel_center'; s.player.x = {px}; s.player.z = {pz};
              s.discovered = {{}}; delete s.flags.dome_ouvert;
              g.restore(s, true);
              window.__nml.view.setZoom({zoom}, {{ user: false }});
              document.getElementById('msg').textContent = '';
            }}""")
            for _ in range(8):
                E("window.__nml.view.render(); document.getElementById('msg').textContent = ''")
                time.sleep(0.05)
            pg.screenshot(path=OUT + fname)
            return E("""() => {
              const ids = ['hud','locbox','obj','msg','dialogue','panel','keys','zoom','act','mini'];
              const H = ids.map(i => document.getElementById(i)).filter(e => e && !e.hidden && e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden').map(e => e.getBoundingClientRect());
              const out = { hud: [], rects: {} };
              for (const l of document.querySelectorAll('.wlabel')) {
                if (l.hidden || l.style.visibility === 'hidden') continue;
                const a = l.getBoundingClientRect();
                if (!a.width) continue;
                if (H.some(q => a.left < q.right && a.right > q.left && a.top < q.bottom && a.bottom > q.top)) out.hud.push(l.textContent);
                if (l.dataset.door) out.rects[l.dataset.door] = [Math.round(a.left), Math.round(a.top), Math.round(a.right), Math.round(a.bottom)];
              }
              const dDome = window.__nml.view.project(22, 7, 12), dQg = window.__nml.view.project(42, 8, 12);
              out.monuments = { dome: [Math.round(dDome.x), Math.round(dDome.y)], qg: [Math.round(dQg.x), Math.round(dQg.y)] };
              return out;
            }""")

        r_ens = check_labels_and_shot(f'carrefour_ensemble_{wtag}.png', 27, 18, 0.6)
        r_ctr = check_labels_and_shot(f'carrefour_centre_{wtag}.png', 28, 17.5, 1.0)
        r_qgd = check_labels_and_shot(f'qg_dome_bureau_{wtag}.png', 35, 18, 0.75)
        r_ech = check_labels_and_shot(f'echelle_teng_cerisier_taxi_{wtag}.png', 13.2, 16.2, 1.0)

        hud_ov = r_ens['hud'] + r_ctr['hud'] + r_qgd['hud'] + r_ech['hud']
        # Ni c_strip ni c_nord ne recouvrent le cœur façade du Dôme (22,7,12) ou du QG Arcadius (42,8,12)
        def hits_pt(rect, pt):
            return rect and rect[0] - 8 <= pt[0] <= rect[2] + 8 and rect[1] - 8 <= pt[1] <= rect[3] + 8
        mon_ov = []
        for tag, r in [('ens', r_ens), ('ctr', r_ctr), ('qgd', r_qgd), ('ech', r_ech)]:
            for did in ('c_strip', 'c_nord'):
                rc = r['rects'].get(did)
                if hits_pt(rc, r['monuments']['dome']): mon_ov.append(f'{tag}:{did}@dome')
                if hits_pt(rc, r['monuments']['qg']): mon_ov.append(f'{tag}:{did}@qg')
        ok(not hud_ov and not mon_ov,
           f'{name} étiquettes « Fréquence Strip » et « Pulse Plaza » sur les sorties, hors Dôme / QG / HUD',
           {'hud': hud_ov, 'mon': mon_ov, 'ens': r_ens['rects'], 'ctr': r_ctr['rects']})

        ok(not errs, f'{name} aucune erreur JS / console / réseau', errs[:3])
        ctx.close()
    br.close()

print(f'{n}/{n + len(fails)} OK')
json.dump({'ok': n, 'fails': fails}, open(OUT + 'resultats.json', 'w'), indent=1, ensure_ascii=False)
sys.exit(1 if fails else 0)
