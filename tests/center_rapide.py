# Test rapide Center-Town v2 · Carrefour Arcadius 132 x 116 m (plan cible d'Ocre validé par Valentin le 11/11/2026) :
# - sols g_ct_* (dont le carrefour v4 : bordures, angles, tirets, lignes d'arrêt, case jaune 12 m) + vraie nuit noire ; 0 clé obsolète, AUCUNE échelle de sprite différente de 1
# - Arcadius v4 (3 sprites d'emprise) et 10 façades de remplissage v4 + porche/segment NE (ct_remplissage_*) posés à l'échelle 1 sur leurs emprises, sans repli ni silhouette
# - tram à l'arrêt sur la voie tram N-S ; circulation mixte (taxi, berline, compacte, utilitaire, moto, limo, intercepteur, dépanneuse, bus) sur la chaussée, un seul véhicule au carrefour ; figurants du carrefour et des trois coins (marché, jardin, cour NE) et 12 passants, jamais sur un solide ni sur la chaussée hors passages
# - 8 sorties et seuils du plan v2 (portes miroir), portes Dôme (50;96) et Teng (8;44.5), 10/10 portes atteignables, temps de traversée à 3 m/s, A* en tas binaire
# - plan large d'arrivée (12 ppm ordinateur, 6-8 ppm téléphone, foule allégée) terminé par un geste ; budget d'effets tactile (Fold) ; sorties hors écran empilées en 390
# - captures 1280 et 390, échelle de jeu et plan large, sous /tmp/nml-test-out/ct_132/
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from nml_boot import passer_boot; from vue_rendue import vue_rendue  # menu Terminal : sauter l'allumage
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
    'ct_arcadius_aile_est_v4_3q', 'ct_arcadius_arriere_v4_3q', 'ct_arcadius_facade_v4_3q',
    'ct_arcadius_grille_e1_v4_3q', 'ct_arcadius_grille_e2_v4_3q', 'ct_arcadius_grille_e3_v4_3q',
    'ct_arcadius_grille_s1_17m_v4_3q', 'ct_arcadius_grille_s2_6m_v4_3q', 'ct_arcadius_grille_s3_v4_3q',
    'ct_arcadius_portail_io_v4_3q', 'ct_arret_tram_v3_3q', 'ct_banniere_io_v3_3q',
    'ct_bord_sud_a_v3_3q', 'ct_bord_sud_b_v3_3q', 'ct_bord_sud_c_v3_3q',
    'ct_bureau_permis_v3_3q', 'ct_cerisier_bac_v3_3q', 'ct_dome_frequence_v3_3q',
    'ct_echoppe_vapeur_v3_3q', 'ct_holo_suspendu_v3_3q', 'ct_kiosque_info_v3_3q',
    'ct_lampadaire_io_v3_3q', 'ct_mob_banc_x_v4_3q', 'ct_mob_banc_z_v4_3q',
    'ct_mob_barriere_x_v4_3q', 'ct_mob_borne_info_v4_3q', 'ct_mob_bornes_recharge_v4_3q',
    'ct_mob_distributeurs_v4_3q', 'ct_mob_feu_pieton_e_v4_3q', 'ct_mob_feu_pieton_v4_3q',
    'ct_mob_feu_tricolore_e_v4_3q', 'ct_mob_feu_tricolore_v4_3q', 'ct_mob_gba_z_v4_3q',
    'ct_mob_jardiniere_arbre_v4_3q', 'ct_mob_jardiniere_arbustes_v4_3q', 'ct_mob_lampadaire_ambre_v4_3q',
    'ct_mob_panneau_holo_v4_3q', 'ct_mob_plots_v4_3q', 'ct_mob_poubelles_x_v4_3q',
    'ct_mob_poubelles_z_v4_3q', 'ct_mob_stand_streetfood_v4_3q', 'ct_mob_table_haute_v4_3q',
    'ct_monorail_rame_v3_3q', 'ct_monorail_viaduc_v3_3q', 'ct_ne_bureaux_a1_8x6_v4_3q',
    'ct_ne_bureaux_a2_8x6_v4_3q', 'ct_ne_bureaux_a3_8x6_v4_3q', 'ct_ne_bureaux_b1_12x6_v4_3q',
    'ct_ne_bureaux_b2_12x6_v4_3q', 'ct_ne_bureaux_c_10x8_v4_3q', 'ct_ne_bureaux_d_10x6_v4_3q',
    'ct_ne_bureaux_e1_8x8_v4_3q', 'ct_ne_bureaux_e2_8x8_v4_3q', 'ct_ne_bureaux_f_7x6_v4_3q',
    'ct_ne_porche_8x4_v4_3q', 'ct_ne_segment_8x4_v4_3q', 'ct_se_arriere_8x10_v4_3q',
    'ct_se_ateliers_12x10_v4_3q', 'ct_se_echoppes_9x6_v4_3q', 'ct_se_etals_couverts_v4_3q',
    'ct_se_kiosque_nouilles_v4_3q', 'ct_se_maison_the_v4_3q', 'ct_so_arbre_jardin_v4_3q',
    'ct_so_fontaine_v4_3q', 'ct_so_kiosque_jardin_v4_3q', 'ct_so_muret_haie_x_v4_3q',
    'ct_so_muret_haie_z_v4_3q', 'ct_so_stand_concert_v4_3q', 'ct_tour_archeon_v4_3q',
    'ct_tour_humancorp_v4_3q', 'ct_tour_nexus_v4_3q', 'ct_tour_orc_v4_3q',
    'ct_tour_teng_v4_3q', 'ct_veh_berline_avant_v4_3q', 'ct_veh_berline_dos_v4_3q',
    'ct_veh_bus_avant_v5_3q', 'ct_veh_bus_dos_v5_3q', 'ct_veh_compacte_avant_v4_3q',
    'ct_veh_compacte_dos_v4_3q', 'ct_veh_depanneuse_avant_v4_3q', 'ct_veh_intercepteur_avant_v4_3q',
    'ct_veh_limo_avant_v4_3q', 'ct_veh_limo_dos_v4_3q', 'ct_veh_moto_avant_v4_3q', 'ct_veh_motolivr_dos_v4_3q',
    'ct_veh_taxi_avant_v4_3q', 'ct_veh_tram_avant_v4_3q', 'ct_veh_utilitaire_avant_v4_3q',
}
# façades de remplissage v4 d'Ocre (CENTER_TOWN.md §8C) : id -> (clé, x, z, w, d, h cible)
REMPL = {
    'ct_rempl0': ('ct_remplissage_8x8_c', 92, 0, 8, 8, 20),
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
    'ct_veh_bus_avant_v4_3q', 'ct_veh_bus_dos_v4_3q',  # bus v4 (plongeon 0,45-0,48) : plus posé, remplacé par le v5 (§8R)
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
    'g_ct_jardin_pelouse', 'g_ct_jardin_allee',
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
               f'{name} {len(EXPECTED_SPRITES)} clés posées (lot mobilier §8J, véhicules §8K, porche §8L), 0 clé obsolète', sorted(EXPECTED_SPRITES ^ sprites_used))
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
                if (m.footprint_m && !((m.footprint_m[0] === b.w && m.footprint_m[1] === b.d) || (m.footprint_m[0] === b.d && m.footprint_m[1] === b.w && !!b.miroir))) out.push([b.id, b.sprite, [b.w, b.d], m.footprint_m, b.miroir || false]);
                if (m.px_par_m && m.px_par_m !== 50) out.push([b.id, b.sprite, 'px_par_m', m.px_par_m]); }
              return { out, H }; }""")
            TOURS = {'c_change': 39, 'ct_archeon': 43, 'ct_orc': 45, 'ct_nexus': 46, 'ct_humancorp': 48, 'c_arcadius_n': 60}
            ok(not emp['out'] and all(emp['H'].get(k) is not None and abs(emp['H'][k] - h) < 1.0 for k, h in TOURS.items()),
               f'{name} emprises posées = footprint_m du manifeste ; tours v4 Teng 39, Archeon 43, Orc 45, Nexus 46, Human Corp 48, Arcadius 60 m', (emp['out'], {k: emp['H'].get(k) for k in TOURS}))
            tram = next(b for b in info['bs'] if b['id'] == 'ct_tram1')
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
            texte_ok = all(v.get('texte') and v['texte']['repeat'] == 1 and v['texte']['sx'] == 1 for v in flat if v.get('texte'))
            typ = lambda cle: re.sub(r'_(avant|dos)_v[45]_3q$', '', (cle or '').replace('ct_veh_', ''))  # bus en v5 (§8R), les autres en v4
            types = sorted({typ(v['cle']) for v in VS[0]})
            want = {'taxi', 'berline', 'compacte', 'utilitaire', 'moto', 'limo', 'intercepteur', 'depanneuse', 'bus'}
            dos_ouest = any(v['axe'] == 'x' and v['sx'] == 1 and v['key'] and re.search(r'_dos_v[45]_3q$', v['key']) for v in flat)
            avant_est = any(v['axe'] == 'x' and v['sx'] == 1 and v['key'] and re.search(r'_avant_v[45]_3q$', v['key']) for v in flat)
            miroir_ns = any(v['axe'] == 'z' and v['sx'] == -1 and v['key'] and re.search(r'_(avant|dos)_v[45]_3q', v['key']) for v in flat)
            tram_mobile = any('tram' in typ(v['sprite']) for v in info['vehicules'])
            ok(tram['sprite'] == 'ct_veh_tram_avant_v4_3q' and abs(tram['x'] - 72.68) < 0.02 and abs(tram['z'] - 18) < 0.02 and abs(tram['w'] - 2.65) < 0.02 and abs(tram['d'] - 33.8) < 0.02
               and all(v['sprite'] != 'ct_tram_v3_3q' for v in info['vehicules']) and tram['z'] + tram['d'] <= 52.01 and not tram_mobile,
               f'{name} tram v2 à l\'arrêt sur sa voie N-S (x72-76, z18-51,8), hors des véhicules qui roulent, tête avant le passage nord', tram)
            ok(len(info['vehicules']) >= 8 and want <= set(types) and not hors_voie and len(tourne) >= 2 and not echV and texte_ok and dos_ouest and avant_est and miroir_ns
               and 'tram' not in types,
               f'{name} {len(info["vehicules"])} véhicules ({", ".join(types)}) sur les deux axes ({len(tourne)} tournent au carrefour), voies de chaussée, hors garés ; +x avant / −x dos / N-S miroir, texte non retourné, |échelle| = 1',
               {'hors_voie': hors_voie, 'axes': sorted(axes), 'tourne': len(tourne), 'etire': echV[:2], 'texte': texte_ok, 'vues': (dos_ouest, avant_est, miroir_ns), 'types': types})
            sim = E("window.__nml.view.simVehicules(60, 1 / 30, { pietons: false })")
            sim2 = E("window.__nml.view.simVehicules(60, 1 / 30)")
            ok(not sim['hits'] and not sim2['hits'] and sim['minEcart'] >= 0 and min(sim['parcouru']) > 150
               and sim.get('maxCarrefour', 99) <= 1 and sim2.get('maxCarrefour', 99) <= 1,
               f'{name} 60 s simulées (x2, avec et sans piétons) : les emprises de deux véhicules ne se recouvrent jamais (écart mini {min(sim["minEcart"], sim2["minEcart"])} m), carrefour à un seul véhicule (max {max(sim.get("maxCarrefour", -1), sim2.get("maxCarrefour", -1))}), tous roulent (≥ {min(sim["parcouru"]):.0f} m)',
               {'hits': (sim['hits'] + sim2['hits'])[:3], 'parcouru': sim['parcouru'], 'maxCarrefour': (sim.get('maxCarrefour'), sim2.get('maxCarrefour'))})
            # 1b. Correctifs du 12/11 (Valentin) : (a) plus de marche arrière, (b) une seule plaque de lettrage, qui suit l'orientation
            # (a) chaque véhicule posé tous les 1,5 m de son trajet (4 caps, juste avant / après chaque virage, début et fin = wrap) : la vue suit le
            #     déplacement réel (+x avant natif, −x dos natif, +z avant miroir, −z dos miroir) et aucun calque d'une autre vue n'est laissé visible
            cap = E("""() => { const v = window.__nml.view, L = window.__nml.world.LOCATIONS.steel_center, bad = [], caps = {}; let n = 0; v.figerVehicules(true); const t0 = v.calquesVehicules().map(c => [c.cle, c.t]);
              const attendu = (dx, dz) => Math.abs(dx) >= Math.abs(dz) ? { dos: dx < 0, sx: 1, cap: dx < 0 ? '-x' : '+x' } : { dos: dz < 0, sx: -1, cap: dz < 0 ? '-z' : '+z' };
              for (const veh of L.vehicules) { const r0 = v.placerVehicule(veh.sprite, 0), Lt = r0.L, ts = [];
                for (let t = 0; t < Lt; t += 1.5) ts.push(t); let acc = 0; for (let k = 0; k + 1 < veh.path.length; k++) { const a = veh.path[k], b = veh.path[k + 1]; acc += Math.hypot(b[0] - a[0], b[1] - a[1]); ts.push(acc - 0.3, acc + 0.3); } ts.push(Lt - 0.01);
                for (const t of ts) { if (t < 0 || t > Lt) continue; const a = v.placerVehicule(veh.sprite, t), b = v.placerVehicule(veh.sprite, Math.min(Lt - 0.001, t + 0.25)); v.placerVehicule(veh.sprite, t);
                  const dx = b.x - a.x, dz = b.z - a.z; if (Math.hypot(dx, dz) < 1e-4) continue; const e = attendu(dx, dz), dos = String(a.key).endsWith('_dos_v4_3q'); n++;
                  (caps[e.cap] = caps[e.cap] || new Set()).add(veh.sprite.replace('ct_veh_', '').replace('_avant_v4_3q', ''));
                  const c = v.calquesVehicules().find(q => q.cle === veh.sprite), etr = c.calques.filter(q => q.visible && !q.vue && !String(q.img).startsWith(a.key + '_'));
                  const tx = c.calques.filter(q => q.visible && q.vue);
                  if (dos !== e.dos || a.sx !== e.sx || etr.length || tx.some(q => (q.vue === 'miroir') !== (a.sx < 0) || q.repeat !== 1 || !String(q.img).startsWith(a.key + '_'))) bad.push([veh.sprite, +t.toFixed(1), e.cap, a.key, a.sx, etr.map(q => q.img)]); } }
              for (const [c, t] of t0) v.placerVehicule(c, t); v.figerVehicules(false); return { n, bad: bad.slice(0, 6), nbad: bad.length, caps: Object.fromEntries(Object.entries(caps).map(([k, s]) => [k, [...s]])) }; }""")
            ok(cap['n'] > 300 and not cap['nbad'] and all(len(cap['caps'].get(k, [])) >= 1 for k in ('+x', '-x', '+z', '-z')),
               f'{name} plus de marche arrière : {cap["n"]} poses sur les trajets (4 caps, avant / après virage, début / fin de trajet), la vue suit toujours le déplacement et aucun calque d\'une autre vue ne reste affiché', cap)
            # (b) une seule plaque : en roulant (images successives) et pour chaque cap posé, au plus un calque texte visible, et exactement un quand la vue en a ;
            #     garés (taxis, bus, tram) : une seule plaque, celle du miroir de la caisse ; _texte / _texte_miroir jamais retournés
            pl = E("""async () => { const v = window.__nml.view, w = ms => new Promise(r => setTimeout(r, ms)), bad = [], vus = new Set(); let n = 0;
              const chk = (lab, c, sx) => { const tx = c.calques.filter(q => q.vue), vis = tx.filter(q => q.visible); if (!tx.length) return; n++;
                if (vis.length !== 1 || (vis[0].vue === 'miroir') !== (sx < 0) || vis[0].repeat !== 1) bad.push([lab, vis.map(q => q.lay)]); else vus.add(lab.split(':')[0] + ':' + vis[0].vue); };
              for (let k = 0; k < 24; k++) { v.render(); for (const c of v.calquesVehicules()) chk(c.cle.replace('ct_veh_', '') + ':roule', c, c.sx); await w(60); }
              v.figerVehicules(true); const t0 = v.calquesVehicules().map(c => [c.cle, c.t]);
              for (const [cle, pts] of [['ct_veh_taxi_avant_v4_3q', [[70, 20], [40, 61]]], ['ct_veh_bus_avant_v5_3q', [[40, 70]]]]) for (const pt of pts) { const r = v.placerVehicule(cle, pt); v.render();
                chk(cle.replace('ct_veh_', '') + ':' + r.key.replace(/^.*_(avant|dos)_.*$/, '$1') + (r.sx < 0 ? '_miroir' : '_natif'), v.calquesVehicules().find(q => q.cle === cle), r.sx); }
              for (const [c, t] of t0) v.placerVehicule(c, t); v.figerVehicules(false); v.render();
              const gares = v.calquesGares(), gbad = gares.filter(g => { const tx = g.calques.filter(q => q.vue); if (!tx.length) return false; const vis = tx.filter(q => q.visible);
                return vis.length !== 1 || (vis[0].vue === 'miroir') !== (g.repeat < 0) || vis[0].repeat !== 1; }).map(g => g.id);
              return { n, bad: bad.slice(0, 6), vus: [...vus], gares: gares.filter(g => g.calques.some(q => q.vue)).map(g => g.id), gbad }; }""")
            ok(pl['n'] > 50 and not pl['bad'] and not pl['gbad'] and len(pl['gares']) >= 4,
               f'{name} lettrage : une seule plaque à la fois ({pl["n"]} contrôles en roulant et posés, {len(pl["gares"])} véhicules garés), celle de l\'orientation (native / miroir), jamais retournée', pl)
            # (a bis) au pixel : rendu isolé du corps, comparé aux 4 vues d'Ocre ; poses enchaînées comme en roulant (taxi sud puis ouest, compacte nord puis est,
            #     limo ouest puis nord) : l'image affichée par la carte graphique doit être celle du cap (avant l'ancienne image restait après un virage)
            POSES_PIX = [('ct_veh_taxi_avant_v4_3q', [70, 20]), ('ct_veh_taxi_avant_v4_3q', [30, 61]), ('ct_veh_compacte_avant_v4_3q', [78, 100]), ('ct_veh_compacte_avant_v4_3q', [110, 70]),
                         ('ct_veh_limo_avant_v4_3q', [110, 61]), ('ct_veh_limo_avant_v4_3q', [78, 30]), ('ct_veh_bus_avant_v5_3q', [40, 70]), ('ct_veh_berline_avant_v4_3q', [40, 61]),
                         ('ct_veh_moto_avant_v4_3q', [78, 90]), ('ct_veh_utilitaire_avant_v4_3q', [70, 90]), ('ct_veh_taxi_avant_v4_3q', [70, 30])]
            t0p = E("window.__nml.view.figerVehicules(true) && window.__nml.view.calquesVehicules().map(c => [c.cle, c.t])"); pix_bad, pix_n = [], 0
            for cle, pt in POSES_PIX:
                r = E(f"window.__nml.view.placerVehicule('{cle}', {json.dumps(pt)})")
                E(f"window.__nml.view.setCamera({{ x: {r['x']}, z: {r['z']}, ppm: {14 if '_bus_' in cle else 40} }})")  # bus 18 m : entier dans les 390 px (à 40 ppm, l'écran coupait l'avant et l'arrière)
                best, sc = vue_rendue(E(f"window.__nml.view.isolerVehicule('{cle}')"), cle); pix_n += 1
                if best != (r['key'], r['sx']): pix_bad.append([cle[7:-12], pt, r['key'][7:], r['sx'], best and (best[0][7:], best[1])])
            E(f"(() => {{ const v = window.__nml.view; for (const [c, t] of {json.dumps(t0p)}) v.placerVehicule(c, t); v.figerVehicules(false); v.setCamera(null); }})()")
            ok(pix_n == len(POSES_PIX) and not pix_bad, f'{name} au pixel : {pix_n} poses (4 caps, après virage) affichent bien la vue du cap (avant / dos, natif / miroir), pas l\'image du cap précédent', pix_bad)
            # bus v5 (pente 0,33, 12/11) : le bus 18 m qui roule (z 70) longe le bus garé ct_vbus0 (z 73,15) ; les deux sont le v5 d'Ocre (824 x 451, échelle 1),
            #     le mobile, plus loin de la caméra, est peint avant le garé, et à chaque pose du passage côte à côte (x 84 à 126)
            cc = E("""() => { const v = window.__nml.view; v.figerVehicules(true); const t0 = v.calquesVehicules().map(c => [c.cle, c.t]), bad = []; let n = 0, g0 = null;
              for (let x = 84; x <= 126; x += 3) { v.placerVehicule('ct_veh_bus_avant_v5_3q', [x, 70]); v.render(); n++;
                const b = v.vehicules().find(q => q.cle === 'ct_veh_bus_avant_v5_3q'), g = v.calquesGares().find(q => q.id === 'ct_vbus0'); g0 = g;
                if (!b || !g || b.key !== 'ct_veh_bus_avant_v5_3q' || g.img !== 'ct_veh_bus_dos_v5_3q' || b.px[0] !== 824 || b.px[1] !== 451 || Math.abs(b.repeat) !== 1 || Math.abs(g.repeat) !== 1 || !(b.ordre < g.ordre))
                  bad.push([x, b && b.key, b && b.ordre, g && g.img, g && g.ordre]); }
              for (const [c, t] of t0) v.placerVehicule(c, t); v.figerVehicules(false); v.render(); return { n, bad, g: g0 && { img: g0.img, repeat: g0.repeat } }; }""")
            ok(cc['n'] >= 14 and not cc['bad'], f'{name} bus v5 côte à côte : {cc["n"]} poses du bus 18 m le long du bus garé ct_vbus0, v5 des deux côtés, échelle 1, le mobile (z 70) peint derrière le garé (z 73,15)', cc)
            # ordre de dessin des véhicules qui roulent (capture de Valentin, 12/11 : le bus mobile peint par-dessus le bus garé) : sur 40 images de circulation,
            #     chaque véhicule est peint après tout ce qui est derrière lui et avant tout ce qui est devant, quand leurs rectangles écran se recouvrent
            ov = E("""async () => { const v = window.__nml.view, w = ms => new Promise(r => setTimeout(r, ms)), bad = []; let n = 0;
              for (let k = 0; k < 40; k++) { const o = v.ordreVehicules(); n += o.n; bad.push(...o.bad); await w(80); } return { n, nbad: bad.length, bad: bad.slice(0, 6) }; }""")
            ok(ov['n'] > 200 and not ov['nbad'], f'{name} ordre de dessin des véhicules : {ov["n"]} recouvrements écran contrôlés sur 40 images (garés, bâtiments, passants), aucun véhicule peint par-dessus ce qui est devant lui', ov)
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
              const bloque = [[14, 46], [20, 46], [26, 46], [29.5, 46], [36.4, 46], [40, 46], [42, 46], [50, 46], [54, 10], [54, 25], [54, 40]].map(([x, z]) => f(x, z));
              const trous = [], libres = [];
              for (let x = 12; x <= 53.5; x += 0.5) { const libre = f(x, 46); if (x >= 30.5 && x <= 35.5) { if (!libre) libres.push(+x.toFixed(2)); } else if (libre) trous.push(+x.toFixed(2)); }
              const p = window.__findPath(gr, { x: 33, z: 49 }, { x: 33, z: 40 });
              const segs = Object.fromEntries(L.buildings.filter(b => /^c_arc_(grille|portail)/.test(b.id)).map(b => [b.id, { sprite: b.sprite, x: b.x, z: b.z, w: b.w, d: b.d }]));
              const want = { c_arc_grille_s1: ['ct_arcadius_grille_s1_17m_v4_3q', 12, 17], c_arc_portail_io: ['ct_arcadius_portail_io_v4_3q', 29, 8],
                c_arc_grille_s2: ['ct_arcadius_grille_s2_6m_v4_3q', 37, 6], c_arc_grille_s3: ['ct_arcadius_grille_s3_v4_3q', 43, 10.55] };
              const poses = Object.entries(want).filter(([id, [sp, x, w]]) => { const s = segs[id]; return !s || s.sprite !== sp || s.x !== x || s.w !== w; }).map(([id]) => id);
              const about = [segs.c_arc_grille_s1?.x + segs.c_arc_grille_s1?.w, segs.c_arc_portail_io?.x, segs.c_arc_portail_io?.x + segs.c_arc_portail_io?.w, segs.c_arc_grille_s2?.x, segs.c_arc_grille_s2?.x + segs.c_arc_grille_s2?.w, segs.c_arc_grille_s3?.x];
              const etire = [];
              for (const id of ['c_arc_grille_s1', 'c_arc_grille_s2', 'c_arc_grille_s3', 'c_arc_portail_io']) {
                const s = segs[id], m = window.__nml.bman[s.sprite], ppmA = m.px_par_m || K;
                const rendu = s.w * Math.abs(sr.x) + s.d * Math.abs(sr.z), natif = m.px[0] / ppmA, ratio = rendu / natif;
                if (Math.abs(ratio - 1) > 0.08) etire.push({ id, rendu: +rendu.toFixed(3), natif: +natif.toFixed(3), ratio: +ratio.toFixed(3) });
              }
              return { passage, bloque, trous, passageBouche: libres, chemin: p ? +p.reduce((s, q, i) => i ? s + Math.hypot(q.x - p[i - 1].x, q.z - p[i - 1].z) : 0, 0).toFixed(1) : null,
                n: Object.keys(segs).length, pas: man?.passage, fenceX: +fenceX.toFixed(2), gateMid: +gateMid.toFixed(2),
                dWorld: +Math.abs(gateMid - fenceX).toFixed(3), dEcranM: +(Math.abs(scrFoot.x - scrGate.x) / ppm).toFixed(3),
                painted_px: px, port: [port.x, port.z, port.w, port.d], poses, about, etire }; }""")
            ok(grille['n'] == 7 and all(grille['passage']) and not any(grille['bloque']) and not grille['trous'] and not grille['passageBouche']
               and not grille['poses'] and grille['about'] == [29, 29, 37, 37, 43, 43] and not grille['etire']
               and grille['chemin'] and grille['chemin'] < 10.5
               and grille['pas'] and abs((grille['pas']['x'][0] + grille['pas']['x'][1]) / 2 - grille['gateMid']) < 0.05
               and grille['dWorld'] <= 0.5 and grille['dEcranM'] <= 0.5,
               f'{name} clôture IO continue x12-53,55 (0 trou, 0 chevauchement, s1 17 m + portail + s2 6 m + s3), passage x30,5-35,5 franchissable ({grille["chemin"]} m), axé sur le pied d\'escalier peint (x={grille.get("fenceX")} sur z46, écart monde {grille.get("dWorld")} m, écran {grille.get("dEcranM")} m)', grille)
            porche = E("""() => {
              const gr = window.__nml.game.grids.steel_center, L = window.__nml.world.LOCATIONS.steel_center;
              const f = (x, z) => { const [i, j] = gr.toCell(x, z); return gr.free(i, j); };
              const seg = L.buildings.find(b => b.id === 'ct_ne_seg0'), po = L.buildings.find(b => b.id === 'ct_ne_porche0'), nx = L.buildings.find(b => b.id === 'ct_nexus');
              const passage = []; for (let x = 84.5; x <= 100.5; x += 0.5) for (const z of [21, 22, 23]) passage.push([x, z, f(x, z)]);
              const bloq = [[96, 16.5], [96, 18], [96, 19.5], [96, 20.2], [96, 23.8], [96, 25], [96, 28]].map(([x, z]) => [x, z, f(x, z)]);
              const p = window.__findPath(gr, { x: 88, z: 22 }, { x: 102, z: 22 });
              return { seg: seg && [seg.sprite, seg.x, seg.z, seg.w, seg.d], po: po && [po.sprite, po.x, po.z, po.w, po.d, po.solid],
                nx: nx && [nx.x, nx.z, nx.w, nx.d], passageLibres: passage.filter(q => !q[2] && q[0] >= 92 && q[0] <= 100).map(q => q.slice(0, 2)),
                trottoir: passage.filter(q => q[0] < 92 && !q[2]),
                bloq, chemin: p ? +p.reduce((s, q, i) => i ? s + Math.hypot(q.x - p[i - 1].x, q.z - p[i - 1].z) : 0, 0).toFixed(1) : null };
            }""")
            ok(porche['seg'] == ['ct_ne_segment_8x4_v4_3q', 92, 16, 8, 4] and porche['po'] and porche['po'][0] == 'ct_ne_porche_8x4_v4_3q'
               and porche['po'][1:5] == [92, 20, 8, 4] and porche['nx'] == [92, 24, 8, 8] and not porche['passageLibres']
               and porche['chemin'] and porche['chemin'] < 20 and all(not q[2] for q in porche['bloq']),
               f'{name} porche NE franchissable z20-24 (trottoir avenue → cour x100+), segment z16-20, Nexus intact z24-32', porche)
            mob_chaussee = E("""() => {
              const L = window.__nml.world.LOCATIONS.steel_center, out = [];
              for (const b of L.buildings) {
                if (b.sprite.startsWith('ct_veh_') || b.id === 'ct_tram1') continue; // véhicules garés : poses d'Ocre sur les bordures
                const boxes = b.solid || [{ x: b.x, z: b.z, w: b.w, d: b.d }];
                for (const s of boxes) if (s.x + s.w > 64 && s.x < 84 && s.z + s.d > 56 && s.z < 76) out.push([b.id, b.sprite, s]);
              }
              return out;
            }""")
            ok(not mob_chaussee, f'{name} mobilier hors chaussée 20 m (x64-84 / z56-76), véhicules garés exceptés (poses d\'Ocre)', mob_chaussee)
            coins = E("""() => {
              const L = window.__nml.world.LOCATIONS.steel_center, gr = window.__nml.game.grids.steel_center, bman = window.__nml.world.bman || window.__nml.data?.bman;
              const B = id => L.buildings.find(b => b.id === id);
              const f = (x, z) => { const [i, j] = gr.toCell(x, z); return gr.free(i, j); };
              const len = p => p ? +p.reduce((s, q, i) => i ? s + Math.hypot(q.x - p[i - 1].x, q.z - p[i - 1].z) : 0, 0).toFixed(1) : null;
              const se = ['ct_p_se_kiosque_nouilles','ct_p_se_echoppes_9x6','ct_p_se_maison_the','ct_p_se_ateliers_12x10','ct_p_se_arriere_8x10','ct_p_se_etals_couverts'].map(id => { const b=B(id); return b && [b.id, b.sprite, b.x, b.z, b.w, b.d]; });
              const ruelleN = [], ruelleEW = [], ruelleNS = [];
              for (let x = 100.5; x <= 123.5; x += 1) ruelleN.push([x, 93.5, f(x, 93.5)]);
              for (let x = 112.5; x <= 114.5; x += 0.5) for (let z = 101.5; z <= 105.5; z += 1) ruelleNS.push([x, z, f(x, z)]);
              for (let x = 101; x <= 111; x += 1) ruelleEW.push([x, 103.5, f(x, 103.5)]);
              const pSe = window.__findPath(gr, { x: 98, z: 88 }, { x: 113, z: 103 });
              const soK = B('ct_so_kiosque0'), soF = B('ct_so_fontaine0');
              const domePass = []; for (let x = 44.5; x <= 55.5; x += 1) for (const z of [96.5, 97, 98, 99.5]) domePass.push([x, z, f(x, z)]);
              const pDome = window.__findPath(gr, { x: 26, z: 90 }, { x: 50, z: 97 });
              const pJard = window.__findPath(gr, { x: 26, z: 90 }, { x: 18, z: 108 });
              const xGe44 = L.buildings.filter(b => b.x >= 44 && b.id.startsWith('ct_so_')).map(b => b.id);
              const c = B('ct_ne_bur_c'), d1 = B('ct_ne_bur_d1'), d2 = B('ct_ne_bur_d2'), e1 = B('ct_ne_bur_e1'), e2 = B('ct_ne_bur_e2'), e3 = B('ct_ne_bur_e3');
              const fcount = L.buildings.filter(b => b.sprite === 'ct_ne_bureaux_f_7x6_v4_3q').length;
              const dcount = L.buildings.filter(b => b.sprite === 'ct_ne_bureaux_d_10x6_v4_3q').length;
              const e1count = L.buildings.filter(b => b.sprite === 'ct_ne_bureaux_e1_8x8_v4_3q').length;
              const hc = L.buildings.find(b => b.sprite === 'ct_tour_humancorp_v4_3q');
              const neH = L.buildings.filter(b => (b.sprite||'').startsWith('ct_ne_bureaux_')).map(b => [b.id, (window.__nml.world.BUILDING_MANIFEST || window.__nml.assets || {})[b.sprite]]);
              const man = window.__nml.world.manifest || window.__nml.catalogue?.buildings;
              const hs = L.buildings.filter(b => (b.sprite||'').startsWith('ct_ne_bureaux_')).map(b => {
                const m = (window.__nml.bman || window.__nml.view && 0);
                return b.sprite;
              });
              const alley = []; for (let x = 100.5; x <= 109.5; x += 1) for (const z of [21, 22, 23]) if (!(x >= 103.6 && x <= 105.2 && z >= 21.6 && z <= 23.4)) alley.push([x, z, f(x, z)]);
              const pNe = window.__findPath(gr, { x: 88, z: 22 }, { x: 111, z: 26 });
              const frontSud = ['c_galerie','ct_rempl7','ct_rempl8','ct_rempl9','c_tour','ct_rempl4','ct_rempl5','ct_archeon','c_immeuble'].map(id => { const b=B(id); return b && [b.id, b.x, b.z, b.w, b.d]; });
              const seH = L.buildings.filter(b => (b.sprite||'').startsWith('ct_se_') && b.sprite.includes('v4')).length;
              const fouleSe = L.extras.filter(e => e.x >= 100 && e.z >= 95).length;
              const fouleSo = L.extras.filter(e => e.x < 44 && e.z >= 92).length;
              const fouleNe = L.extras.filter(e => e.x >= 100 && e.z >= 12 && e.z <= 50).length;
              const fouleBloq = L.extras.filter(e =>
                (e.x >= 44 && e.x <= 56 && e.z >= 96 && e.z <= 100) ||
                (e.x >= 100 && e.z >= 92 && e.z <= 95) ||
                (e.x >= 96 && e.x <= 100 && e.z >= 84 && e.z <= 92) ||
                (e.x >= 100 && e.x <= 108 && e.z >= 88 && e.z <= 92) ||
                (e.x >= 92 && e.z >= 20 && e.z <= 24) ||
                (e.x >= 100 && e.x <= 110 && e.z > 20 && e.z <= 28) ||
                (e.x >= 115 && e.x <= 120 && e.z >= 0 && e.z <= 12)
              ).map(e => [e.x, e.z]);
              return { se, seOk: se.every(Boolean) && se[0][2]===100 && se[2][2]===124 && se[3][3]===106,
                ruelleNbloq: ruelleN.filter(q => !q[2]), ruelleNSok: ruelleNS.every(q => q[2]), pSe: len(pSe),
                soK: soK && [soK.sprite, soK.x, soK.z, soK.w, soK.d], soF: soF && [soF.x, soF.z],
                domeBloq: domePass.filter(q => !q[2]), pDome: len(pDome), pJard: len(pJard), xGe44,
                c: c && [c.sprite, c.x, c.z, c.w, c.d], d1: d1 && [d1.x, d1.z], d2: d2 && [d2.x, d2.z],
                e1: e1 && [e1.sprite, e1.x, e1.z], e2: e2 && [e2.sprite, e2.z], e3: e3 && [e3.sprite, e3.z],
                fcount, dcount, e1count, hc: hc && [hc.x, hc.z, hc.w, hc.d],
                alleyBloq: alley.filter(q => !q[2]), pNe: len(pNe),
                frontSud, porche: [B('ct_ne_porche0')&&B('ct_ne_porche0').x, B('ct_ne_seg0')&&B('ct_ne_seg0').z, B('ct_nexus')&&B('ct_nexus').z],
                fouleSe, fouleSo, fouleNe, fouleBloq };
            }""")
            ok(coins['seOk'] and not coins['ruelleNbloq'] and coins['pSe'] and coins['pSe'] < 40
               and coins['frontSud'][0] == ['c_galerie', 100, 84, 8, 4]
               and coins['fouleSe'] >= 4 and not coins['fouleBloq'],
               f'{name} marché SE §8M posé (6 bâtiments), ruelle z92-95 libre, accès depuis le trottoir, vitrines sud intactes, figurants hors passages', coins)
            ok(coins['soK'] == ['ct_so_kiosque_jardin_v4_3q', 3, 107, 6, 6] and coins['soF'] == [18, 101]
               and not coins['domeBloq'] and coins['pDome'] and coins['pDome'] < 40 and not coins['xGe44']
               and coins['pJard'] and coins['fouleSo'] >= 8 and not coins['fouleBloq'],
               f'{name} jardin SO §8N posé, passage Dôme x44-56 z96-100 libre (seuil 50;97 atteignable), rien en x≥44, figurants dans le jardin', coins)
            ok(coins['c'] == ['ct_ne_bureaux_c_10x8_v4_3q', 100, 12, 10, 8] and coins['d1'] == [100, 28] and coins['d2'] == [100, 34]
               and coins['e1'] == ['ct_ne_bureaux_e1_8x8_v4_3q', 124, 16] and coins['e2'][0] == 'ct_ne_bureaux_e2_8x8_v4_3q' and coins['e3'][0] == 'ct_ne_bureaux_e1_8x8_v4_3q'
               and coins['fcount'] == 3 and coins['dcount'] == 2 and coins['e1count'] == 2
               and coins['hc'] == [104, 40, 8, 8] and coins['porche'] == [92, 16, 24]
               and not coins['alleyBloq'] and coins['pNe'] and coins['pNe'] < 40
               and coins['fouleNe'] >= 3 and not coins['fouleBloq'],
               f'{name} bureaux NE §8P posés (C x100 z12-20, ruelle z20-24, D/E/F, d×2 e1×2 f×3), porche/segment/Nexus et Human Corp intacts, cour joignable, figurants hors ruelles', coins)


            cede = E("""async () => { const v = window.__nml.view, g = window.__nml.game, s = g.state, L = v.vehicules(); const i = L.findIndex(q => q.axe === 'z' && q.z > 5 && q.z < 100);
              if (i < 0) return null; const q = L[i], x0 = s.player.x, z0 = s.player.z; s.player.x = q.x; s.player.z = q.z + (q.path[1][1] > q.path[0][1] ? 3 : -3); s.player.path = [];
              const w = ms => new Promise(r => setTimeout(r, ms)); await w(250); v.render(); const a = v.vehicules()[i]; const t0 = [a.x, a.z]; await w(400); v.render(); const b = v.vehicules()[i]; s.player.x = x0; s.player.z = z0;
              return { attend: b.attend, bouge: Math.hypot(b.x - t0[0], b.z - t0[1]) }; }""")
            ok(cede and cede['attend'] and cede['bouge'] < 0.05, f'{name} un véhicule cède le passage à un piéton devant lui', cede)
            crowd_sprites = {e[0] for e in info['extras']} | {w[0] for w in info['walkers']}
            ok(130 <= len(info['extras']) <= 170 and 8 <= len(info['walkers']) <= 12 and len(crowd_sprites) >= 14,
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
                        if a[0] != b[0] and not (a[0].startswith('ct_so_muret_') and b[0].startswith('ct_so_muret_'))
                        and a[1] < b[3] - 1e-6 and b[1] < a[3] - 1e-6 and a[2] < b[4] - 1e-6 and b[2] < a[4] - 1e-6]
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
            ok(st['enseignes'] == 75 and st['fenetres'] == 105 and st['pulses'] == 34 and st['on'] <= 8 and st['walkers'] <= 12
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
              for (const [k, a, b] of [['O-E', [0.5, 52], [131.5, 52]], ['N-S', [74, 0.5], [74, 115.5]], ['diag', [55, 0.5], [131.5, 93.5]], ['entree-dome', [1, 82], [50, 97]], ['entree-est', [1, 82], [131, 50]]]) {
                const t0 = performance.now(), p = window.__findPath(gr, { x: a[0], z: a[1] }, { x: b[0], z: b[1] }), ms = performance.now() - t0;
                out[k] = p ? { m: +len(p).toFixed(1), s: +(len(p) / 3).toFixed(1), ms: +ms.toFixed(1) } : null; }
              return out; }""")
            tr_ok = all(tr.values()) and tr.get('O-E') and tr['O-E']['s'] <= 46 and tr['N-S']['s'] <= 41 and tr['diag']['s'] <= 70 and max(v['ms'] for v in tr.values() if v) < 60
            ok(tr_ok,
               f'{name} temps de traversée à 3 m/s : O-E {tr.get("O-E") and tr["O-E"]["s"]} s, N-S {tr.get("N-S") and tr["N-S"]["s"]} s, diagonale {tr.get("diag") and tr["diag"]["s"]} s ; A* max {max((v["ms"] for v in tr.values() if v), default=-1)} ms', tr)

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
        r4 = labels_at(88, 22, 1.0, f'jeu_porche_{wtag}.png')
        E("window.__nml.view.setCamera({ x: 88, z: 22, ppm: 28 });")
        for _ in range(4): E("window.__nml.view.render()"); time.sleep(0.05)
        pg.screenshot(path=OUT + f'jeu_porche_axe_{wtag}.png')
        E("window.__nml.view.setCamera(null);")
        labels_at(116, 98, 1.0, f'jeu_se_marche_{wtag}.png')
        labels_at(22, 104, 1.0, f'jeu_so_jardin_{wtag}.png')
        labels_at(50, 97, 1.0, f'jeu_entree_dome_{wtag}.png')
        labels_at(116, 20, 1.0, f'jeu_ne_bureaux_{wtag}.png')
        E("window.__nml.view.setCamera({ x: 118, z: 38, ppm: 26 });")
        for _ in range(4): E("window.__nml.view.render()"); time.sleep(0.05)
        pg.screenshot(path=OUT + f'jeu_ne_ciel_{wtag}.png')
        E("window.__nml.view.setCamera({ x: 116, z: 24, ppm: 26 });")
        for _ in range(4): E("window.__nml.view.render()"); time.sleep(0.05)
        pg.screenshot(path=OUT + f'jeu_ne_cour_{wtag}.png')
        E("window.__nml.view.setCamera(null);")
        labels_at(109, 76, 1.0, f'jeu_bus_{wtag}.png')
        labels_at(78, 48, 1.0, f'jeu_tram_{wtag}.png')
        def shot_cam(fname, x, z, ppm):
            E(f"window.__nml.view.setCamera({{ x: {x}, z: {z}, ppm: {ppm} }});")
            for _ in range(4): E("window.__nml.view.render(); document.getElementById('msg').textContent = ''"); time.sleep(0.05)
            pg.screenshot(path=OUT + fname)
        shot_cam(f'lettrage_taxi_ew_{wtag}.png', 43, 58, 56)
        shot_cam(f'lettrage_taxi_ns_{wtag}.png', 66, 43, 56)
        shot_cam(f'lettrage_bus_{wtag}.png', 116, 75, 48)
        shot_cam(f'lettrage_tram_{wtag}.png', 78, 50, 48)
        dos = None
        for _ in range(40):
            dos = E("() => { const L = window.__nml.view.vehicules() || []; const t = L.find(q => q.key && String(q.key).includes('taxi') && String(q.key).includes('dos') && q.x > 16 && q.x < 120 && q.z > 16 && q.z < 100); return t ? { x: t.x, z: t.z, key: t.key, axe: t.axe } : null; }")
            if dos: break
            E("window.__nml.view.render()"); time.sleep(0.2)
        if dos:
            shot_cam(f'lettrage_taxi_dos_{wtag}.png', round(dos['x'], 1), round(dos['z'], 1), 56)
        # gros plans circulation figée (correctifs 12/11) : un véhicule dans chaque cap, après virage, lettrage avant / dos sur les deux axes, bus 18 m le long du bus garé
        GROS = [('cap_sud_taxi', 'ct_veh_taxi_avant_v4_3q', [70, 9], 56), ('cap_ouest_taxi_dos', 'ct_veh_taxi_avant_v4_3q', [40, 61], 56),
                ('cap_nord_compacte', 'ct_veh_compacte_avant_v4_3q', [78, 96], 56), ('cap_est_compacte_apres_virage', 'ct_veh_compacte_avant_v4_3q', [96, 70], 56),
                ('cap_ouest_berline', 'ct_veh_berline_avant_v4_3q', [110, 61], 56), ('cap_nord_limo_apres_virage', 'ct_veh_limo_avant_v4_3q', [78, 40], 56),
                ('cap_ouest_limo_avant_virage', 'ct_veh_limo_avant_v4_3q', [100, 61], 56), ('cap_nord_moto', 'ct_veh_moto_avant_v4_3q', [78, 100], 64),
                ('cap_sud_utilitaire', 'ct_veh_utilitaire_avant_v4_3q', [70, 96], 56), ('cap_ouest_depanneuse', 'ct_veh_depanneuse_avant_v4_3q', [116, 61], 48),
                ('lettrage_bus_avant_est', 'ct_veh_bus_avant_v5_3q', [40, 70], 44), ('bus_le_long_du_bus_gare', 'ct_veh_bus_avant_v5_3q', [109, 70], 40)]
        t0v = E("window.__nml.view.figerVehicules(true) && window.__nml.view.calquesVehicules().map(c => [c.cle, c.t])")
        for fname, cle, pt, ppm in GROS:
            r = E(f"(() => {{ const v = window.__nml.view; for (const [c, t] of {json.dumps(t0v)}) v.placerVehicule(c, t); return v.placerVehicule('{cle}', {json.dumps(pt)}); }})()")
            if r: shot_cam(f'{fname}_{wtag}.png', round(r['x'], 1), round(r['z'], 1), ppm)
        shot_cam(f'lettrage_bus_gare_dos_{wtag}.png', 109, 74, 44)
        shot_cam(f'lettrage_taxis_gares_{wtag}.png', 45, 58, 60)
        shot_cam(f'lettrage_taxi_gare_ns_miroir_{wtag}.png', 65, 43, 60)
        E(f"(() => {{ const v = window.__nml.view; for (const [c, t] of {json.dumps(t0v)}) v.placerVehicule(c, t); v.figerVehicules(false); }})()")
        E("window.__nml.view.setCamera(null);")
        lab_bad = r1['hud'] + r1['over'] + r2['hud'] + r2['over'] + r3['hud'] + r3['over']
        cap = vp[0] >= 700 or all(len(r['fleches']) <= 3 for r in (r1, r2, r3))
        ok(not lab_bad and cap and r1['fleches'], f'{name} étiquettes de sortie hors HUD, sans chevauchement, flèches au bord (entrée : {len(r1["fleches"])} hors écran)', {'bad': lab_bad, 'r1': r1['fleches'], 'r2': r2['fleches']})

        ok(not errs, f'{name} aucune erreur JS / console / réseau', errs[:3])
        ctx.close()
    br.close()

print(f'{n}/{n + len(fails)} OK')
json.dump({'ok': n, 'fails': fails}, open(OUT + 'resultats.json', 'w'), indent=1, ensure_ascii=False)
sys.exit(1 if fails else 0)
