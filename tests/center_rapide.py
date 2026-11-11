# Test rapide Center-Town v2 · Carrefour Arcadius 132 x 116 m (plan cible d'Ocre validé par Valentin le 11/11/2026) :
# - sols g_ct_* (dont le carrefour v4 : bordures, angles, tirets, lignes d'arrêt, case jaune 12 m) + vraie nuit noire ; 0 clé obsolète, AUCUNE échelle de sprite différente de 1
# - Arcadius v4 (3 sprites d'emprise) et 11 façades de remplissage v4 (ct_remplissage_*) posés à l'échelle 1 sur leurs emprises, sans repli ni silhouette
# - tram sur la voie tram N-S, taxis sur l'av. E-O ; environ 140 figurants (carrefour + parvis) et 12 passants, jamais sur un solide ni sur la chaussée hors passages
# - 8 sorties et seuils du plan v2 (portes miroir), portes Dôme (50;96) et Teng (8;44.5), 10/10 portes atteignables, temps de traversée à 3 m/s, A* en tas binaire
# - plan large d'arrivée (12 ppm ordinateur, 6-8 ppm téléphone, foule allégée) terminé par un geste ; budget d'effets tactile (Fold) ; sorties hors écran empilées en 390
# - captures 1280 et 390, échelle de jeu et plan large, sous /tmp/nml-test-out/ct_132/
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from nml_boot import passer_boot  # menu Terminal : sauter l'allumage
import os, sys, time, json, re, urllib.request
from playwright.sync_api import sync_playwright

URL = os.environ.get('URL', 'http://127.0.0.1:8915/')
if not URL.endswith('/'): URL += '/'
OUT = os.environ.get('OUT', '/tmp/nml-test-out/ct_132/')
os.makedirs(OUT, exist_ok=True)

fails = []
n = 0
def ok(c, m, d=''):
    global n
    print(('OK   ' if c else 'ECHEC ') + m + ('' if c else f'  {d}'), flush=True)
    n += bool(c)
    if not c:
        fails.append({'test': m, 'detail': str(d)[:300]})

DOORS_10 = ['c_ouest', 'c_est', 'c_mega', 'c_strip', 'c_nord', 'c_sud', 'c_pp_sud', 'c_sud_est', 'c_change_door', 'c_dome']
# plan v2 (center_town_plan_cible.md, « Sorties de bord ») : ouverture -> seuil
SORTIES_V2 = {'c_strip': [58, 0, 58, 1], 'c_nord': [90, 0, 90, 1], 'c_mega': [0, 50, 1, 50], 'c_ouest': [0, 82, 1, 82],
              'c_est': [132, 50, 131, 50], 'c_sud_est': [132, 82, 131, 82], 'c_sud': [58, 116, 58, 115], 'c_pp_sud': [90, 116, 90, 115],
              'c_dome': [50, 96, 50, 97], 'c_change_door': [8, 44.5, 9, 44.5]}
EXPECTED_SPRITES = {
    'ct_arcadius_arriere_v4_3q', 'ct_arcadius_aile_est_v4_3q', 'ct_arcadius_facade_v4_3q', 'ct_dome_frequence_v3_3q', 'ct_bureau_permis_v3_3q',
    'ct_tour_teng_v4_3q', 'ct_tour_archeon_v4_3q', 'ct_tour_orc_v4_3q', 'ct_tour_humancorp_v4_3q', 'ct_tour_nexus_v4_3q',
    'ct_arcadius_grille_s1_v4_3q', 'ct_arcadius_grille_s2_v4_3q', 'ct_arcadius_grille_s3_v4_3q', 'ct_arcadius_portail_io_v4_3q',
    'ct_arcadius_grille_e1_v4_3q', 'ct_arcadius_grille_e2_v4_3q', 'ct_arcadius_grille_e3_v4_3q',
    'ct_bord_sud_a_v3_3q', 'ct_bord_sud_b_v3_3q', 'ct_bord_sud_c_v3_3q',
    'ct_monorail_viaduc_v3_3q', 'ct_monorail_rame_v3_3q', 'ct_holo_suspendu_v3_3q',
    'ct_arret_tram_v3_3q', 'ct_tram_v3_3q', 'ct_taxi_v3_3q',
    'ct_echoppe_vapeur_v3_3q', 'ct_kiosque_info_v3_3q',
    'ct_lampadaire_io_v3_3q', 'ct_banniere_io_v3_3q', 'ct_cerisier_bac_v3_3q',
}
# façades de remplissage v4 d'Ocre (CENTER_TOWN.md §8C) : id -> (clé, x, z, w, d, h cible)
REMPL = {
    'ct_rempl0': ('ct_remplissage_8x8_c', 92, 0, 8, 8, 20), 'ct_rempl1': ('ct_remplissage_8x8_a', 92, 16, 8, 8, 12),
    'ct_rempl2': ('ct_remplissage_8x8_b', 92, 32, 8, 8, 16), 'ct_rempl3': ('ct_remplissage_16x8_b', 112, 40, 16, 8, 18),
    'ct_rempl4': ('ct_remplissage_16x8_a', 0, 84, 16, 8, 14), 'ct_rempl5': ('ct_remplissage_8x8_a', 36, 84, 8, 8, 12),
    'ct_rempl6': ('ct_remplissage_8x16_bas_b', 48, 100, 8, 16, 6), 'ct_rempl7': ('ct_remplissage_16x8_bas_a', 108, 84, 16, 8, 6),
    'ct_rempl8': ('ct_remplissage_8x8_bas_a', 124, 84, 8, 8, 5), 'ct_rempl9': ('ct_remplissage_8x16_bas_a', 92, 92, 8, 16, 6),
    'ct_rempl10': ('ct_remplissage_8x8_bas_b', 92, 108, 8, 8, 6),
}
OBSOLETE_V1 = {
    'ct_cerisier_bac_3q', 'ct_taxi_3q',
    'ct_tour_teng_3q', 'ct_tour_archeon_3q', 'ct_tour_orc_3q', 'ct_tour_humancorp_3q', 'ct_tour_nexus_3q',
    'b_st_ct_tower', 'b_st_ct_dome', 'b_st_ct_shop', 'b_st_blanc',
    'b_st_immeuble', 'b_st_galerie', 'b_st_neon', 'b_st_jumelles',
    'df_ens_facade_vibes', 'df_ens_facade_tron',
    'ct_arcadius_qg_v3_3q', 'ct_arcadius_qg_3q', 'ct_dome_frequence_3q', 'ct_bureau_permis_3q',
    'ct_tour_teng_v3_3q', 'ct_tour_archeon_v3_3q', 'ct_tour_orc_v3_3q', 'ct_tour_humancorp_v3_3q', 'ct_tour_nexus_v3_3q',
    'ct_tour_teng_v2_3q', 'ct_tour_archeon_v2_3q', 'ct_tour_orc_v2_3q', 'ct_tour_humancorp_v2_3q', 'ct_tour_nexus_v2_3q',
    'ct_bord_sud_a_3q', 'ct_bord_sud_b_3q', 'ct_bord_sud_c_3q',
    'ct_monorail_viaduc_3q', 'ct_monorail_rame_3q', 'ct_holo_suspendu_3q',
    'ct_arret_tram_3q', 'ct_tram_3q', 'ct_taxi_v2_3q',
    'ct_echoppe_vapeur_3q', 'ct_kiosque_info_3q',
    'ct_lampadaire_io_3q', 'ct_banniere_io_3q', 'ct_cerisier_bac_v2_3q',
}
EXPECTED_SOLS = {
    'g_ct_trottoir_dalles', 'g_ct_asphalte_mouille', 'g_ct_rails_tram_ew',
    'g_ct_rails_tram_ns', 'g_ct_passage_pieton_ns', 'g_ct_passage_pieton_ew', 'g_ct_case_jaune_12m',
    'g_ct_voie_tirets_ns', 'g_ct_voie_tirets_ew', 'g_ct_ligne_arret_ns', 'g_ct_ligne_arret_ew',
    'g_ct_bordure_n', 'g_ct_bordure_s', 'g_ct_bordure_e', 'g_ct_bordure_o',
    'g_ct_bordure_angle_se', 'g_ct_bordure_angle_so', 'g_ct_bordure_angle_ne', 'g_ct_bordure_angle_no',
}
OBSOLETE_SOLS = {'g_ct_carrefour_jaune'}
# chaussée (hors passages piétons) : on n'y pose ni figurant ni passant
ROUTE_JS = "const route=(x,z)=>{const pp=[[64,52,84,56],[64,76,84,80],[60,56,64,76],[84,56,88,76]];if(pp.some(r=>x>=r[0]&&x<=r[2]&&z>=r[1]&&z<=r[3]))return false;return (x>64&&x<84)||(z>56&&z<76)};"

with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=[
        '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'
    ])
    for name, vp, mob in [('desktop', (1280, 800), False), ('mobile', (390, 844), True), ('fold', (823, 617), True)]:
        errs = []
        ctx = (br.new_context(viewport={'width': vp[0], 'height': vp[1]}, has_touch=True, is_mobile=True, device_scale_factor=2.625 if name == 'fold' else 2)
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

        passer_boot(pg); tapel('#m-new'); tapel('[data-race="augmente"]'); tapel('#cr-next'); tapel('#cr-enter')
        pg.wait_for_function('!document.body.classList.contains("menu-open")', timeout=15000)
        time.sleep(0.6)

        E("""() => {
          const g = window.__nml.game, s = g.snapshot();
          s.location = 'steel_center'; s.player.x = 1; s.player.z = 82;
          Object.assign(s.flags, { q_start: true, q_fin: true, steel_passe: true, q_steel: true });
          g.restore(s, true);
        }""")
        pg.wait_for_function("window.__nml.state.location === 'steel_center' && !window.__nml.music.paused && Math.abs(window.__nml.music.volume - 0.55) < 0.06", timeout=12000)
        time.sleep(0.6)
        wtag = {'desktop': '1280', 'mobile': '390', 'fold': 'fold'}[name]

        # 0. Plan large d'arrivée : présent, 12 ppm (ordinateur) / 6-8 ppm (téléphone), cadré sur le carrefour et le parvis, foule allégée, fin au geste
        E("window.__nml.view.rejouerArrivee()")
        for _ in range(10): E("window.__nml.view.render(); document.getElementById('msg').textContent = ''"); time.sleep(0.1)
        pa = E("""() => { const v = window.__nml.view, L = window.__nml.world.LOCATIONS.steel_center, c = L.cadre?.arrivee;
          const dense = L.extras.filter(e => e.dense).length; return { cadre: c, ppm: v.ppm(), cible: v.camCible(), etat: v.planArrivee(), dense, extras: L.extras.length }; }""")
        want = (6, 8) if mob else (11.5, 12.5)
        ok(pa['cadre'] and pa['etat']['planLarge'] and want[0] <= pa['ppm'] <= want[1] and pa['cible'] and 40 <= pa['cible'][0] <= 70 and 36 <= pa['cible'][1] <= 66,
           f'{name} plan large d\'arrivée présent : {pa["ppm"]:.1f} ppm, cadré en {pa["cible"]} (carrefour + parvis Arcadius)', pa)
        ok(pa['dense'] >= 40 and pa['extras'] - pa['dense'] >= 40, f'{name} foule allégée en plan large : {pa["extras"] - pa["dense"]} figurants visibles sur {pa["extras"]}', pa)
        pg.screenshot(path=OUT + f'plan_large_{wtag}.png')
        # un geste (appui sur la scène) termine le plan large, retour à l'échelle de jeu
        gesture(vp[0] * 0.5, vp[1] * 0.45); time.sleep(1.6)
        for _ in range(4): E("window.__nml.view.render()"); time.sleep(0.1)
        fin = E("[window.__nml.view.ppm(), window.__nml.view.planArrivee()]")
        jeu = 24 if vp[0] < 700 else 30
        ok(abs(fin[0] - jeu) < 0.6 and not fin[1]['planLarge'] and fin[1]['sorti'], f'{name} un geste termine le plan large : retour à {fin[0]:.0f} ppm (échelle de jeu)', fin)
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=62;s.player.z=52;s.player.path=[];g.restore(s,true)})()"); time.sleep(0.4)

        # budget d'effets tactile : pulsesOn <= 8 sur téléphone ET sur le Fold déplié (823 px)
        for _ in range(12): E("window.__nml.view.render()"); time.sleep(0.06)
        st0 = E("({...window.__nml.view.animStats, tactile: window.__nml.view.tactile()})")
        ok((st0['tactile'] == mob) and st0['pulsesMax'] == (8 if mob else 48) and st0['pulsesOn'] <= st0['pulsesMax'] and st0['on'] <= (8 if mob else 16),
           f'{name} budget d\'effets selon l\'écran tactile : tactile={st0["tactile"]}, pulses {st0["pulsesOn"]}/{st0["pulsesMax"]}, anims={st0["on"]}', st0)

        if name != 'fold':
            # 1. Sols, lumière nuit, clés v3, aucune échelle de sprite, emplacements en attente
            info = E("""() => {
              const l = window.__nml.world.LOCATIONS.steel_center;
              return {
                size: l.size, bg: window.__nml.view.lightOf().bg, skin: l.ground.skin, marge: l.ground.marge?.skin,
                paint: (l.ground.paint || []).map(r => r.skin), props: l.props.length,
                bs: l.buildings.map(b => ({ id: b.id, sprite: b.sprite, ph: !!b.ph, inMan: !!window.__nml.bman?.[b.sprite], obs: !!window.__nml.bman?.[b.sprite]?.obsolete, x: b.x, z: b.z, w: b.w, d: b.d, k: b.k ?? null, sy: b.sy ?? null, ancre: b.ancre ?? null, attente: b.attente ?? null, solid: b.solid ?? null })),
                extras: l.extras.map(e => [e.sprite, e.x, e.z, e.h || null]), walkers: l.walkers.map(w => [w.sprite, w.path.length]),
                invalid: !!document.getElementById('editor-map-invalid'), vehicules: (l.vehicules || []).map(v => ({ sprite: v.sprite, path: v.path })),
              };
            }""")
            sprites_used = {b['sprite'] for b in info['bs'] if b['id'] not in REMPL} | {v['sprite'] for v in info['vehicules']}
            sols_used = {info['skin'], info['marge'], *info['paint']}
            ok(info['size'] == {'w': 132, 'd': 116} and info['bg'] == '#05070d' and sols_used == EXPECTED_SOLS and not (sols_used & OBSOLETE_SOLS) and info['props'] == 0 and not info['invalid'],
               f'{name} carte 132 x 116 m, nuit #05070d, {len(EXPECTED_SOLS)} sols g_ct_* (carrefour v4 compris), schéma valide', (info['size'], sorted(EXPECTED_SOLS ^ sols_used)))
            ok(sprites_used == EXPECTED_SPRITES and not (sprites_used & OBSOLETE_V1),
               f'{name} 31 clés posées au plan v2 (Arcadius v4 x3 + clôture et portail IO x7, 5 tours v4, 16 v3 à l\'échelle), 0 clé obsolète', sorted(EXPECTED_SPRITES ^ sprites_used))
            echelles = [b['id'] for b in info['bs'] if (b['k'] not in (None, 1)) or (b['sy'] not in (None, 1))] + [f'extra@{e[1]},{e[2]}' for e in info['extras'] if e[3]]
            ok(not echelles, f'{name} aucune échelle de sprite différente de 1 en valeur absolue (ni b.k, ni b.sy, ni hauteur forcée ; miroir -1 admis)', echelles)
            bad = []
            for bid, (cle, x, z, w, d, h) in REMPL.items():
                b = next((b for b in info['bs'] if b['id'] == bid), None)
                if not b or b['sprite'] != cle or [b['x'], b['z'], b['w'], b['d']] != [x, z, w, d] or b['attente'] or b['ph'] or not b['inMan'] or b['ancre']: bad.append((bid, b and [b['sprite'], b['x'], b['z'], b['w'], b['d']]))
            sans_sprite = [b['id'] for b in info['bs'] if b['ph'] or b['attente'] or not b['inMan'] or b['obs']]
            arc = {b['id']: [b['sprite'], b['x'], b['z'], b['w'], b['d'], b['ancre']] for b in info['bs'] if b['id'].startswith('c_arcadius')}
            ok(not bad, f'{name} 11 façades de remplissage v4 (ct_remplissage_*) posées à l\'échelle 1 sur leurs emprises du plan v2', bad)
            ok(not sans_sprite, f'{name} 0 emplacement en attente : chaque bâtiment a un sprite livré, non obsolète, sans silhouette de repli', sans_sprite)
            ok(arc == {'c_arcadius_n': ['ct_arcadius_arriere_v4_3q', 12, 4, 24, 22, None], 'c_arcadius_e': ['ct_arcadius_aile_est_v4_3q', 36, 4, 8, 22, None],
                       'c_arcadius': ['ct_arcadius_facade_v4_3q', 12, 26, 32, 10, None]},
               f'{name} Arcadius v4 d\'Ocre posé aux emprises du §8 (socle 32x32, tour 60 m), sans ancre ni échelle', arc)
            emp = E("""() => { const l = window.__nml.world.LOCATIONS.steel_center, M = window.__nml.bman, out = [], H = {};
              for (const b of l.buildings) { const m = M[b.sprite]; if (!m) continue; H[b.id] = m.height_m ?? null;
                if (m.footprint_m && (m.footprint_m[0] !== b.w || m.footprint_m[1] !== b.d)) out.push([b.id, b.sprite, [b.w, b.d], m.footprint_m]);
                if (m.px_par_m && m.px_par_m !== 50) out.push([b.id, b.sprite, 'px_par_m', m.px_par_m]); }
              return { out, H }; }""")
            TOURS = {'c_change': 39, 'ct_archeon': 43, 'ct_orc': 45, 'ct_nexus': 46, 'ct_humancorp': 48, 'c_arcadius_n': 60}
            ok(not emp['out'] and all(emp['H'].get(k) is not None and abs(emp['H'][k] - h) < 1.0 for k, h in TOURS.items()),
               f'{name} emprises posées = footprint_m du manifeste ; tours v4 Teng 39, Archeon 43, Orc 45, Nexus 46, Human Corp 48, Arcadius 60 m', (emp['out'], {k: emp['H'].get(k) for k in TOURS}))
            tram = next(b for b in info['bs'] if b['id'] == 'ct_tram0')
            VS = []
            for _ in range(40):
                E("window.__nml.view.render()"); VS.append(E("window.__nml.view.vehicules()")); time.sleep(0.12)
            flat = [v for f in VS for v in f]
            echV = [v for v in flat if abs(v['sx']) != 1 or abs(v['repeat']) != 1 or abs(v['scale'][0] - v['px'][0] / v['K']) > 1e-3 or abs(v['scale'][1] - v['px'][1] / v['K']) > 1e-3]
            axes = {(v['axe'], v['sx']) for v in flat}
            tourne = [v['path'] for v in VS[0] if len({('x' if abs(b[0] - a[0]) > abs(b[1] - a[1]) else 'z') for a, b in zip(v['path'], v['path'][1:])}) > 1]
            hors_voie = E("""() => { const l = window.__nml.world.LOCATIONS.steel_center, gr = window.__nml.game.grids.steel_center, out = [];
              const voie = (x, z) => ((x > 64 && x < 72) || (x > 76 && x < 84)) || ((z > 56 && z < 64) || (z > 68 && z < 76));
              for (const [i, v] of (l.vehicules || []).entries()) { const P = v.path;
                for (let k = 0; k + 1 < P.length; k++) { const a = P[k], b = P[k + 1], n = Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1]) * 2);
                  for (let j = 0; j <= n; j++) { const x = a[0] + (b[0] - a[0]) * j / n, z = a[1] + (b[1] - a[1]) * j / n; if (x <= 0.5 || z <= 0.5 || x >= l.size.w - 0.5 || z >= l.size.d - 0.5) continue;
                    const [ci, cj] = gr.toCell(x, z); if (!voie(x, z) || !gr.free(ci, cj)) out.push(i + ':' + x.toFixed(1) + ',' + z.toFixed(1)); } } }
              return out.slice(0, 10); }""")
            ok(tram['x'] == 72 and tram['w'] == 4 and tram['sprite'] == 'ct_tram_v3_3q' and all(v['sprite'] != 'ct_tram_v3_3q' for v in info['vehicules']),
               f'{name} tram à l\'arrêt sur sa voie N-S (x72-76), hors des véhicules qui roulent', tram)
            ok(len(info['vehicules']) >= 4 and not hors_voie and len(tourne) >= 2 and axes == {('x', 1), ('z', 1)} and all(v['key'] == ('ct_taxi_v3_axe2_3q' if v['axe'] == 'z' else 'ct_taxi_v3_3q') for v in flat) and not echV,
               f'{name} {len(info["vehicules"])} taxis sur les deux axes ({len(tourne)} tournent au carrefour), voies de chaussée seulement ; axe N-S sur la vraie vue ct_taxi_v3_axe2_3q, sans miroir (scale.x = +1), |échelle| = 1, aucun étirement',
               {'hors_voie': hors_voie, 'axes': sorted(axes), 'tourne': len(tourne), 'etire': echV[:2]})
            sim = E("window.__nml.view.simVehicules(60, 1 / 30, { pietons: false })")
            sim2 = E("window.__nml.view.simVehicules(60, 1 / 30)")
            ok(not sim['hits'] and not sim2['hits'] and sim['minEcart'] >= 0 and min(sim['parcouru']) > 150,
               f'{name} 60 s simulées (x2, avec et sans piétons) : les emprises de deux véhicules ne se recouvrent jamais (écart mini {min(sim["minEcart"], sim2["minEcart"])} m), carrefour réservé à un véhicule, tous roulent (≥ {min(sim["parcouru"]):.0f} m)',
               {'hits': (sim['hits'] + sim2['hits'])[:3], 'parcouru': sim['parcouru']})
            grille = E("""() => {
              const v = window.__nml.view, gr = window.__nml.game.grids.steel_center, L = window.__nml.world.LOCATIONS.steel_center;
              const f = (x, z) => { const [i, j] = gr.toCell(x, z); return gr.free(i, j); };
              const fac = L.buildings.find(b => b.sprite === 'ct_arcadius_facade_v4_3q');
              const port = L.buildings.find(b => b.id === 'c_arc_portail_io');
              const mf = window.__nml.bman['ct_arcadius_facade_v4_3q'], man = window.__nml.bman['ct_arcadius_portail_io_v4_3q'];
              const px = mf.escalier_peint.painted_px, K = 50, yaw = 34.5 * Math.PI / 180, pitch = 28.8 * Math.PI / 180;
              const cy = Math.cos(yaw), sy = Math.sin(yaw), sp = Math.sin(pitch), cp = Math.cos(pitch);
              const sr = { x: cy, y: 0, z: -sy }, cu = { x: -sy * sp, y: cp, z: -cy * sp };
              const Ax = fac.x + fac.w, Az = fac.z + fac.d, sx = (px[0] - mf.anchor[0]) / K, syv = (mf.anchor[1] - px[1]) / K;
              const Bx = Ax + sr.x * sx + cu.x * syv, By = cu.y * syv, Bz = Az + sr.z * sx + cu.z * syv, zf = 46;
              const fenceX = (Bx * cy - Bz * sy + zf * sy) / cy, gateMid = port.x + port.w / 2;
              v.render();
              const scrFoot = v.project(Bx, By, Bz), scrGate = v.project(gateMid, 0, zf), ppm = v.ppm();
              const passage = []; for (let x = 30.5; x <= 35.5; x += 0.5) passage.push(f(x, 46));
              const bloque = [[14, 46], [20, 46], [29.5, 46], [36.4, 46], [40, 46], [50, 46], [54, 10], [54, 25], [54, 40]].map(([x, z]) => f(x, z));
              const p = window.__findPath(gr, { x: 33, z: 49 }, { x: 33, z: 40 });
              const b = Object.fromEntries(L.buildings.filter(b => /^c_arc_(grille|portail)/.test(b.id)).map(b => [b.id, b.sprite]));
              return { passage, bloque, chemin: p ? +p.reduce((s, q, i) => i ? s + Math.hypot(q.x - p[i - 1].x, q.z - p[i - 1].z) : 0, 0).toFixed(1) : null,
                n: Object.keys(b).length, pas: man?.passage, fenceX: +fenceX.toFixed(2), gateMid: +gateMid.toFixed(2),
                dWorld: +Math.abs(gateMid - fenceX).toFixed(3), dEcranM: +(Math.abs(scrFoot.x - scrGate.x) / ppm).toFixed(3),
                painted_px: px, port: [port.x, port.z, port.w, port.d] }; }""")
            ok(grille['n'] == 7 and all(grille['passage']) and not any(grille['bloque']) and grille['chemin'] and grille['chemin'] < 10.5
               and grille['pas'] and abs((grille['pas']['x'][0] + grille['pas']['x'][1]) / 2 - grille['gateMid']) < 0.05
               and grille['dWorld'] <= 0.5 and grille['dEcranM'] <= 0.5,
               f'{name} clôture et portail IO : 7 sprites, passage x30,5-35,5 franchissable ({grille["chemin"]} m), axé sur le pied d\'escalier peint (x={grille.get("fenceX")} sur z46, écart monde {grille.get("dWorld")} m, écran {grille.get("dEcranM")} m)', grille)
            cede = E("""async () => { const v = window.__nml.view, g = window.__nml.game, s = g.state, L = v.vehicules(); const i = L.findIndex(q => q.axe === 'z' && q.z > 5 && q.z < 100);
              if (i < 0) return null; const q = L[i], x0 = s.player.x, z0 = s.player.z; s.player.x = q.x; s.player.z = q.z + (q.path[1][1] > q.path[0][1] ? 3 : -3); s.player.path = [];
              const w = ms => new Promise(r => setTimeout(r, ms)); await w(250); v.render(); const a = v.vehicules()[i]; const t0 = [a.x, a.z]; await w(400); v.render(); const b = v.vehicules()[i]; s.player.x = x0; s.player.z = z0;
              return { attend: b.attend, bouge: Math.hypot(b.x - t0[0], b.z - t0[1]) }; }""")
            ok(cede and cede['attend'] and cede['bouge'] < 0.05, f'{name} un taxi cède le passage à un piéton devant lui', cede)
            crowd_sprites = {e[0] for e in info['extras']} | {w[0] for w in info['walkers']}
            ok(130 <= len(info['extras']) <= 150 and 8 <= len(info['walkers']) <= 12 and len(crowd_sprites) >= 14,
               f'{name} foule : {len(info["extras"])} figurants + {len(info["walkers"])} passants, {len(crowd_sprites)} sprites distincts', (len(info['extras']), len(info['walkers'])))
            rep = E("""() => { const X = window.__nml.world.LOCATIONS.steel_center.extras, G = {}, out = { paquets: [], proches: [], petits: 0, denses: 0, tailles: {} };
              for (const e of X) if (e.groupe) (G[e.groupe] ||= []).push(e);
              for (const [g, m] of Object.entries(G)) { const dense = m.some(e => e.role === 'attente' || e.role === 'porte'); if (dense) out.denses += m.length; else { out.petits += m.length; out.tailles[m.length] = (out.tailles[m.length] || 0) + 1; if (m.length > 3) out.paquets.push(g); } }
              for (const e of X) { if (e.role === 'attente' || e.role === 'porte' || e.role === 'soldat') continue;
                const n = X.filter(o => o !== e && Math.hypot(o.x - e.x, o.z - e.z) < 1.6).length; if (n > 2) out.paquets.push(e.x + ',' + e.z); }
              for (let i = 0; i < X.length; i++) for (let j = i + 1; j < X.length; j++) if (Math.hypot(X[i].x - X[j].x, X[i].z - X[j].z) < 0.74) out.proches.push(X[i].x + ',' + X[i].z);
              out.paquets = [...new Set(out.paquets)].slice(0, 8); return out; }""")
            ok(not rep['paquets'] and not rep['proches'] and rep['petits'] >= 0.6 * len(info['extras']) and rep['denses'] <= 45,
               f'{name} foule le long des trottoirs : {rep["petits"]} en petits groupes de 1 à 3 {rep["tailles"]}, {rep["denses"]} en groupes denses (passages, portes), 0 paquet, espacement ≥ 0,75 m', rep)

            # 2. Solides, foule hors solides et hors chaussée, profondeur stable, masques == []
            SOL = E("window.__nml.world.LOCATIONS.steel_center.buildings.flatMap(b=>(b.solid??[{x:b.x,z:b.z,w:b.w,d:b.d}]).map(s=>[b.id,s.x,s.z,s.x+s.w,s.z+s.d]))")
            chev_sol = [(a[0], b[0]) for i, a in enumerate(SOL) for b in SOL[i + 1:]
                        if a[0] != b[0] and a[1] < b[3] - 1e-6 and b[1] < a[3] - 1e-6 and a[2] < b[4] - 1e-6 and b[2] < a[4] - 1e-6]
            ok(not chev_sol, f'{name} 0 chevauchement de solides', chev_sol)
            stab = E("""() => { """ + ROUTE_JS + """
              const loc = window.__nml.world.LOCATIONS.steel_center, v = window.__nml.view, g = window.__nml.game, s = g.state, gr = g.grids.steel_center;
              v.render();
              const B = loc.buildings.map(b => ({ id: b.id, o0: v.orderOf(b.id) })).filter(b => b.o0 != null);
              const rel = {};
              for (let i = 0; i < B.length; i++) for (let j = i + 1; j < B.length; j++) rel[B[i].id + '/' + B[j].id] = B[i].o0 < B[j].o0;
              const flips = [], mq = [], inSol = [], surRoute = [], snap = g.snapshot();
              for (const [idx, e] of loc.extras.entries()) { const [ci, cj] = gr.toCell(e.x, e.z); if (!gr.free(ci, cj)) inSol.push('extra' + idx); if (route(e.x, e.z)) surRoute.push('extra' + idx); }
              for (const z of [0.6, 1.0, 1.5]) {
                v.setZoom(z, { user: false });
                for (const [px, pz] of [[2, 82], [9.5, 44.5], [30, 44], [62, 52], [74, 66], [88, 80], [50, 98], [120, 50]]) {
                  s.player.x = px; s.player.z = pz; g.step(0.6); v.render();
                  for (const m of v.masques()) mq.push(m.join(':'));
                  for (let i = 0; i < B.length; i++) for (let j = i + 1; j < B.length; j++) {
                    const k = B[i].id + '/' + B[j].id; if ((v.orderOf(B[i].id) < v.orderOf(B[j].id)) !== rel[k]) flips.push(k); }
                }
              }
              v.setZoom(1.0, { user: false }); g.restore(snap, true); v.render();
              for (const [wi, w] of loc.walkers.entries()) { const P = w.path;
                for (let i = 0; i < P.length; i++) { const a = P[i], b = P[(i + 1) % P.length], len = Math.hypot(b[0] - a[0], b[1] - a[1]), n = Math.max(4, Math.ceil(len * 4));
                  for (let k = 0; k <= n; k++) { const x = a[0] + (b[0] - a[0]) * k / n, z = a[1] + (b[1] - a[1]) * k / n, [ci, cj] = gr.toCell(x, z);
                    if (!gr.free(ci, cj)) inSol.push('walker' + wi + ':' + x.toFixed(1) + ',' + z.toFixed(1));
                    if (route(x, z)) surRoute.push('walker' + wi + ':' + x.toFixed(1) + ',' + z.toFixed(1));
                    for (const bid of v.masqueEn(x, z)) mq.push(bid + '@walker' + wi); } } }
              return { flips: [...new Set(flips)], mq: [...new Set(mq)], inSol: [...new Set(inSol)], surRoute: [...new Set(surRoute)].slice(0, 12) };
            }""")
            ok(not stab['inSol'] and not stab['surRoute'], f'{name} aucun figurant ni trajet de passant dans un solide ou sur la chaussée (hors passages piétons)', stab)
            ok(not stab['flips'] and not stab['mq'], f'{name} 0 inversion de profondeur et view.masques() == [] (x0,6..x1,5)', {'flips': stab['flips'][:8], 'mq': stab['mq'][:8]})

            # 3. Calques additifs + kick de l'OST
            samples = []; max_bass = max_energy = 0.0
            for _ in range(60):
                if E("(() => { const m = window.__nml.music; return !!window.__nml.ostCentre.playing && !m.paused && m.currentTime > 0.5 && m.readyState >= 3; })()"): break
                time.sleep(0.1)
            E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=88;s.player.z=52;g.restore(s,true)})()")
            for _ in range(60):
                time.sleep(0.06)
                E("window.__nml.view.render()"); samples.append(E("Object.fromEntries(window.__nml.view.pulses().map(p => [p.key, p.opacity]))"))
                ost = E("({ mode: window.__nml.ostCentre.mode, active: window.__nml.ostCentre.active, playing: window.__nml.ostCentre.playing, bass: window.__nml.ostCentre.bass, energy: window.__nml.ostCentre.energy })")
                max_bass = max(max_bass, ost['bass']); max_energy = max(max_energy, ost['energy'])
            st = E("({...window.__nml.view.animStats, walkers: window.__nml.world.LOCATIONS.steel_center.walkers.length})")
            tower_pulse_keys = [f'ct_tour_{t}_v4_3q_pulse' for t in ('teng', 'orc', 'archeon', 'nexus', 'humancorp')]
            spans = {k: round(max(s.get(k, 0) for s in samples) - min(s.get(k, 0) for s in samples), 3) for k in tower_pulse_keys}
            ok(st['enseignes'] == 42 and st['fenetres'] == 44 and st['pulses'] == 32 and st['on'] <= 8 and st['walkers'] <= 12
               and st['pulsesOn'] <= (8 if mob else 48) and st['pulsesOn'] >= (6 if mob else 8),
               f'{name} calques additifs & plafonds : on={st["on"]}, walkers={st["walkers"]}, pulsesOn={st["pulsesOn"]}', st)
            ok(ost['mode'] == 'ost_center_town' and not ost['active'] and ost['playing'] and max_bass > 0.05 and max_energy > 0.04 and all(v > 0.12 for v in spans.values()),
               f'{name} OST Center-Town pilote les 5 _pulse des tours v4 sur le kick (bass={max_bass:.2f})', (ost, spans))

            # 4. Sorties et portes du plan v2, libres et atteignables ; temps de traversée et coût de l'A*
            reach = E(f"""() => {{
              const g = window.__nml.game, gr = g.grids.steel_center, out = {{}};
              for (const id of {json.dumps(DOORS_10)}) {{
                const d = g.doorById(id), [ci, cj] = gr.toCell(d.threshold.x, d.threshold.z);
                const p1 = window.__findPath(gr, {{ x: 1, z: 82 }}, d.threshold), p2 = window.__findPath(gr, {{ x: 62, z: 52 }}, d.threshold);
                out[id] = {{ ow: [d.opening.x, d.opening.z, d.threshold.x, d.threshold.z], free: gr.free(ci, cj), p1: p1 ? p1.length : 0, p2: p2 ? p2.length : 0 }};
              }}
              return out;
            }}""")
            ecarts = {k: v['ow'] for k, v in reach.items() if v['ow'] != SORTIES_V2[k]}
            ok(not ecarts, f'{name} 8 sorties + portes Dôme et Teng aux coordonnées du plan v2', ecarts)
            ok(len(reach) == 10 and all(v['free'] and v['p1'] >= 1 and v['p2'] >= 2 for v in reach.values()),
               f'{name} 10/10 portes libres et atteignables depuis l\'entrée (1;82) et le carrefour (62;52)', {k: v for k, v in reach.items() if not (v['free'] and v['p1'] >= 1 and v['p2'] >= 2)})
            tr = E("""() => { const gr = window.__nml.game.grids.steel_center, len = p => p.reduce((s, q, i) => i ? s + Math.hypot(q.x - p[i - 1].x, q.z - p[i - 1].z) : 0, 0), out = {};
              for (const [k, a, b] of [['O-E', [0.5, 52], [131.5, 52]], ['N-S', [74, 0.5], [74, 115.5]], ['diag', [55, 0.5], [131.5, 115.5]], ['entree-dome', [1, 82], [50, 97]], ['entree-est', [1, 82], [131, 50]]]) {
                const t0 = performance.now(), p = window.__findPath(gr, { x: a[0], z: a[1] }, { x: b[0], z: b[1] }), ms = performance.now() - t0;
                out[k] = p ? { m: +len(p).toFixed(1), s: +(len(p) / 3).toFixed(1), ms: +ms.toFixed(1) } : null; }
              return out; }""")
            ok(all(tr.values()) and tr['O-E']['s'] <= 46 and tr['N-S']['s'] <= 41 and tr['diag']['s'] <= 70 and max(v['ms'] for v in tr.values()) < 60,
               f'{name} temps de traversée à 3 m/s : O-E {tr["O-E"]["s"]} s, N-S {tr["N-S"]["s"]} s, diagonale {tr["diag"]["s"]} s ; A* max {max(v["ms"] for v in tr.values())} ms', tr)

            # 5. Transitions : Teng (porte face est) et Dôme (face sud)
            E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=9.5;s.player.z=44.5;g.restore(s,true);g.useDoor('c_change_door')})()")
            pg.wait_for_function("window.__nml.state.location === 'change_in'", timeout=8000)
            ok(E("window.__nml.state.location") == 'change_in', f'{name} porte Teng c_change_door (8;44.5) -> change_in')
            E("window.__nml.game.useDoor('change_in_door')")
            pg.wait_for_function("window.__nml.state.location === 'steel_center'", timeout=8000)
            back = E("[window.__nml.state.player.x, window.__nml.state.player.z]")
            ok(abs(back[0] - 9) < 1.2 and abs(back[1] - 44.5) < 1.2, f'{name} retour de Teng sur son seuil (9;44.5)', back)
            E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=50;s.player.z=97.5;s.flags.dome_ouvert=true;g.restore(s,true);g.useDoor('c_dome')})()")
            pg.wait_for_function("window.__nml.state.location === 'steel_dome'", timeout=8000)
            dome_ok = E("window.__nml.state.location === 'steel_dome' && window.__nml.world.NPCS.filter(n=>n.location==='steel_dome').length === 10")
            ok(dome_ok, f'{name} porte Dôme c_dome (50;96, face sud) -> steel_dome intact')
            E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=15;s.player.z=29;g.restore(s,true);g.useDoor('df_sortie')})()")
            pg.wait_for_function("window.__nml.state.location === 'steel_center'", timeout=8000)

        # 6. Étiquettes : hors HUD, sans chevauchement ; en 390, au plus 3 sorties hors écran, avec leur flèche
        def labels_at(px, pz, zoom, fname):
            E(f"""() => {{ const g = window.__nml.game, s = g.snapshot(); s.location = 'steel_center'; s.player.x = {px}; s.player.z = {pz}; s.player.path = [];
              s.discovered = {{}}; delete s.flags.dome_ouvert; g.restore(s, true); window.__nml.view.setZoom({zoom}, {{ user: false }}); document.getElementById('msg').textContent = ''; }}""")
            E("window.__nml.state.player.path=[{x:%s,z:%s}]" % (px + 0.3, pz)); time.sleep(2.2)
            for _ in range(8): E("window.__nml.view.render(); document.getElementById('msg').textContent = ''"); time.sleep(0.05)
            pg.screenshot(path=OUT + fname)
            return E("""() => {
              const ids = ['hud','locbox','obj','msg','dialogue','panel','keys','zoom','act','mini'];
              const H = ids.map(i => document.getElementById(i)).filter(e => e && !e.hidden && e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden').map(e => e.getBoundingClientRect());
              const out = { hud: [], over: [], fleches: [], sorties: 0 }, R = [];
              for (const l of document.querySelectorAll('.wlabel')) { if (l.hidden || l.style.visibility === 'hidden') continue; const a = l.getBoundingClientRect(); if (!a.width) continue;
                if (H.some(q => a.left < q.right && a.right > q.left && a.top < q.bottom && a.bottom > q.top)) out.hud.push(l.textContent);
                for (const [t, b] of R) if (a.left < b.right - 1 && a.right > b.left + 1 && a.top < b.bottom - 1 && a.bottom > b.top + 1) out.over.push(t + ' / ' + l.textContent);
                R.push([l.textContent, a]); if (l.dataset.door) { out.sorties++; if (l.dataset.fleche) out.fleches.push(l.dataset.fleche + ' ' + l.textContent); } }
              return out; }""")
        r1 = labels_at(4, 82, 1.0, f'jeu_entree_ouest_{wtag}.png')
        r2 = labels_at(62, 52, 1.0, f'jeu_carrefour_{wtag}.png')
        r3 = labels_at(30, 45, 1.0, f'jeu_parvis_arcadius_{wtag}.png')
        lab_bad = r1['hud'] + r1['over'] + r2['hud'] + r2['over'] + r3['hud'] + r3['over']
        cap = vp[0] >= 700 or all(len(r['fleches']) <= 3 for r in (r1, r2, r3))
        ok(not lab_bad and cap and r1['fleches'], f'{name} étiquettes de sortie hors HUD, sans chevauchement, flèches au bord (entrée : {len(r1["fleches"])} hors écran)', {'bad': lab_bad, 'r1': r1['fleches'], 'r2': r2['fleches']})

        ok(not errs, f'{name} aucune erreur JS / console / réseau', errs[:3])
        ctx.close()
    br.close()

print(f'{n}/{n + len(fails)} OK')
json.dump({'ok': n, 'fails': fails}, open(OUT + 'resultats.json', 'w'), indent=1, ensure_ascii=False)
sys.exit(1 if fails else 0)
