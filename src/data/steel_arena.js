// Steel Arena (zone steel_arena, 96 x 64 m, quartier de Center-Town). Pack d'Ocre : docs/villes/steel/quartiers/steel_arena/ (STEEL_ARENA.md, ASSETS.md, compléments 1 et 2).
// [décision] entrée ouest par la grille du bout est du Fréquence Strip (aller-retour) ; le parvis se visite, l'enceinte reste fermée (réplique au clic).
// Vibes et Tron n'apparaissent que sur les écrans géants dessinés par le code (pages tournantes). Aucun nom civil.
// Enceinte basse ar2_ (moitié nord, x 0 à 92, z 0 à 30) : façades 15 m et dôme 23 m en six morceaux ; parvis et bord ouest en bâtiments complets 3/4 (*_3q), calques rythmiques *_pulse2, *_faisceau et *_pulse/_pulse_b (b3bd9a6 + 769c16d).
// Animations au code (anime_par_code du manifeste) : faisceaux des 4 pylônes (pulsant sur le kick), écrans géants et fronton (pages + beat), enseignes _neon, fenêtres _fenetres et calques rythmiques pilotés par ostCentre.
// Planches peintes restantes : guichet, Human Corp, un cœur dans la file (les 4 ar_ens_faisceau, Vibes, Tron et le fronton peints sont retirés).
export const ARENA_TAILLE_PROPOSEE = { w: 96, d: 64 };
const ARENA = { bg: '#07080b', hemi: ['#9a96b0', '#1c1612', 1.15], sun: ['#e8b078', 0.45], tint: '#b4aeb0', actor: '#e6ded6' };
const VIOLET = '#8a3cff', CYAN = '#5fd3f0', MAGENTA = '#e03ca8', BLANC = '#e8eef2', ROUGE = '#c8323c', AMBRE = '#ffa040', ORANGE = '#ff7a30';
const B = (id, label, sprite, x, z, w, d, extra = {}) => ({ id, label, sprite, x, z, w, d, visitable: false, cue: null, named: !!label, ...extra });
const ENS = (id, sprite, x, z, y, extra = {}) => B(id, '', sprite, x - 0.1, z - 0.1, 0.2, 0.2, { y, solid: [], named: false, ...extra });
const AP = (id, sprite, ax, az, w, d, extra = {}) => B(id, '', sprite, ax - w, az - d, w, d, { named: false, ...extra });
const BATTLE = [
  { fond: ['#2a0c4a', '#6a24b0'], image: 'ar_ens_ecran_vibes', crop: [0, 0, 256, 144], titre: 'GROOVY VIBES', sous: 'Battle du 31 · côté gauche', bandeau: 'Votez avec vos applaudissements. Ils sont mesurés.' },
  { fond: ['#061a2a', '#1a6a9a'], image: 'ar_ens_ecran_tron', crop: [0, 0, 256, 144], titre: 'GROOVY-TRON', sous: 'Battle du 31 · côté droit', bandeau: 'Statut : invaincu. Statut : mis à jour.' },
  { fond: ['#300818', '#a0203a'], titre: 'ROUND 3', sous: 'Vibes 48 % · Tron 52 %', bandeau: 'Le public décide. Human Corp arbitre.' },
  { fond: ['#101018', '#3a3a5a'], titre: 'PULSE OF STEEL', sous: 'Festival · 14/11 · complet', bandeau: 'Human Corp sponsorise le sourire.' },
  { fond: ['#1a0828', '#7a2ab0'], titre: 'EN DIRECT', sous: 'Caméra 7 · gradins ouest', bandeau: 'Ne regardez pas les écrans. Ils vous regardent.' },
  { fond: ['#081820', '#1a5a7a'], titre: 'SCORE LIVE', sous: 'Vibes 51 % · Tron 49 %', bandeau: 'Écart sous la marge d\u2019erreur Human Corp.' },
  { fond: ['#281008', '#8a4020'], titre: 'MERCH OFFICIEL', sous: 'Stand B · parvis sud', bandeau: 'Casquettes qui déteignent. Sourires calibrés.' },
];
const FRONTON = [ { fond: ['#0a0a14', '#20204a'], titre: 'STEEL ARENA', sous: 'Live tonight', bandeau: 'Portiques ouverts' },
  { fond: ['#2a0c4a', '#5a1c9a'], titre: 'VIBES × TRON', sous: 'Battle du 31', bandeau: 'Billet, implant, sourire' },
  { fond: ['#180a20', '#4a1860'], titre: 'FILE ACTIVE', sous: 'Attente estimée 42 min', bandeau: 'Le serpentin est une forme d\u2019art' },
  { fond: ['#0a1418', '#184858'], titre: 'HUMAN CORP', sous: 'Sponsor officiel', bandeau: 'Souriez. C\u2019est mesuré.' } ];
const PYL = [[10, 40], [86, 40], [24, 58], [72, 58]], LAMP = [[4, 40], [92, 34], [36, 60], [60, 60]];
const POOL = ['gen_ar_foule_a', 'gen_pp_foule_a', 'gen_fs_foule_a', 'gen_pp_foule_c', 'gen_ml_fan', 'gen_ar_foule_b', 'gen_pp_foule_e', 'gen_df_foule_a', 'gen_fs_passante', 'gen_pp_foule_g', 'gen_ml_foule_a', 'gen_pp_foule_b', 'gen_fs_foule_b', 'gen_pp_foule_i', 'gen_df_foule_b', 'gen_pp_foule_d', 'gen_ml_foule_b', 'gen_pp_foule_f', 'gen_fs_client_imper', 'gen_pp_foule_h', 'gen_pp_foule_j', 'gen_fs_client_costume'];
const FIG = (pts, k0, role) => pts.map(([x, z, f], i) => ({ sprite: POOL[(k0 + i * 5) % POOL.length], x, z, face: f ?? ((k0 + i) % 2 ? -1 : 1), role }));
export const BUILDINGS_ARENA = [
  // dôme en six morceaux peints avant tout (fond), d'ouest en est puis ar2_toit_z avant l'angle ; le premier porte le solide de toute l'enceinte (z < 29)
  B('ar_toit_so', '', 'ar2_toit_angle_so', 0, 0, 20, 30, { named: false, fond: true, solid: [{ x: 0, z: 0, w: 96, d: 29 }] }),
  ...[20, 36, 52].map((x, i) => B(`ar_toit_x${i}`, '', 'ar2_toit_x', x, 0, 16, 30, { named: false, fond: true, solid: [] })),
  B('ar_toit_z', '', 'ar2_toit_z', 68, 0, 24, 14, { named: false, fond: true, solid: [] }),
  B('ar_toit_se', '', 'ar2_toit_angle_se', 68, 14, 24, 16, { named: false, fond: true, solid: [] }),
  // façades : est, sud d'ouest en est, retour ouest, angle ; écrans en dernier
  AP('ar_f_est', 'ar2_facade_courbe_z', 92, 22, 1, 16, { solid: [] }),
  AP('ar_f_s0', 'ar2_facade_courbe_x', 20, 30, 16, 1), AP('ar_f_s1', 'ar2_facade_courbe_x', 36, 30, 16, 1),
  AP('ar_entree', 'ar2_facade_entree', 52, 30, 16, 1, { label: 'Entrée de l\u2019Arena', named: true, ecran: { coins: [[93, 414], [685, 609], [685, 705], [93, 510]], periode: 5.5, beat: true, flash: '#ffd28a', marque: 'STEEL ARENA', pages: FRONTON } }),
  AP('ar_f_s2', 'ar2_facade_courbe_x', 68, 30, 16, 1), AP('ar_f_s3', 'ar2_facade_courbe_x', 84, 30, 16, 1),
  B('ar_f_retour', '', 'ar2_facade_retour_ouest', 0, 26, 4, 4, { named: false, solid: [{ x: 0, z: 29, w: 4, d: 1 }] }),
  B('ar_f_angle', '', 'ar2_facade_angle', 84, 22, 8, 8, { named: false, ancre: [-8, 0] }),
  B('ar_ecran_s', '', 'ar2_ecran_geant_x', 8.4, 30.0, 9.6, 0.2, { ancre: [0, 0.8], solid: [], named: false, ecran: { periode: 7, beat: true, flash: '#ffd898', marque: 'ARENA LIVE', pages: BATTLE } }),
  B('ar_ecran_e', '', 'ar2_ecran_geant_z', 92.0, 11, 0.2, 8, { ancre: [0.8, 0], solid: [], named: false, ecran: { periode: 8.5, decale: 2, beat: true, flash: '#98ebff', marque: 'ARENA LIVE', pages: BATTLE } }),
  // bord ouest : blocs techniques complets 3/4 d'Ocre (7e5478b) le long de x 0, arrivée ar_ouest libre (z 38 à 46)
  B('ar_tech_a', 'Technique ouest', 'ar_tech_ouest_a_3q', 0, 30, 8, 8),
  B('ar_tech_b', '', 'ar_tech_ouest_b_3q', 0, 46, 4, 8, { named: false }), B('ar_tech_c', '', 'ar_tech_ouest_c_3q', 0, 54, 4, 8, { named: false }),
  // bord sud : barrières de police le long de la rue (z 59,6), passages en x 32-40 et 56-64 (lampadaires)
  ...[4, 8, 12, 16, 20, 24, 28, 40, 44, 48, 52, 64, 68, 72, 76, 80, 84, 88].map((x, i) => B(`ar_police${i}`, '', 'ar_barriere_file', x, 59.6, 4, 0.4, { named: false })),
  // parvis : serpentin de file devant l'entrée
  B('ar_bar_l1', '', 'ar_barriere_file', 36, 34, 4, 0.4, { named: false }), B('ar_bar_l2', '', 'ar_barriere_file', 40, 34, 4, 0.4, { named: false }), B('ar_bar_l3', '', 'ar_barriere_file', 44, 34, 4, 0.4, { named: false }),
  B('ar_bar_m1', '', 'ar_barriere_file', 40, 37, 4, 0.4, { named: false }), B('ar_bar_m2', '', 'ar_barriere_file', 44, 37, 4, 0.4, { named: false }), B('ar_bar_m3', '', 'ar_barriere_file', 48, 37, 4, 0.4, { named: false }),
  B('ar_bar_s1', '', 'ar_barriere_file', 36, 40, 4, 0.4, { named: false }), B('ar_bar_s2', '', 'ar_barriere_file', 40, 40, 4, 0.4, { named: false }), B('ar_bar_s3', '', 'ar_barriere_file', 44, 40, 4, 0.4, { named: false }),
  B('ar_bar_e', '', 'ar_barriere_file_o', 51.6, 33, 0.4, 4, { named: false }), B('ar_bar_o', '', 'ar_barriere_file_o', 36, 36, 0.4, 4, { named: false }),
  B('ar_bar_n1', '', 'ar_barriere_file', 40, 43, 4, 0.4, { named: false }), B('ar_bar_n2', '', 'ar_barriere_file', 44, 43, 4, 0.4, { named: false }), B('ar_bar_n3', '', 'ar_barriere_file', 48, 43, 4, 0.4, { named: false }),
  B('ar_bar_t1', '', 'ar_barriere_file', 36, 46, 4, 0.4, { named: false }), B('ar_bar_t2', '', 'ar_barriere_file', 40, 46, 4, 0.4, { named: false }), B('ar_bar_t3', '', 'ar_barriere_file', 44, 46, 4, 0.4, { named: false }),
  B('ar_bar_e2', '', 'ar_barriere_file_o', 51.6, 39, 0.4, 4, { named: false }), B('ar_bar_o2', '', 'ar_barriere_file_o', 36, 42, 0.4, 4, { named: false }),
  // bâtiments complets 3/4 du parvis (7e5478b)
  B('ar_tribunes', 'Tribunes', 'ar_tribunes_3q', 20, 32, 12, 8),
  B('ar_merch_b', 'Merch officiel', 'ar_stand_merch_b_3q', 26, 40, 4, 4), B('ar_merch_c', 'Chariot de merch', 'ar_stand_merch_c_3q', 54, 40, 4, 4),
  B('ar_truck_n', 'Nouilles du parvis', 'ar_foodtruck_nouilles_3q', 16, 46, 8, 4), B('ar_truck_b', 'Boissons', 'ar_foodtruck_boissons_3q', 68, 46, 8, 4),
  // props rythmiques du parvis (b3bd9a6 + 769c16d) : posés hors serpentin et hors ombres de foule (0 chevauchement solide/emprise, view.masques() vide)
  B('ar_mat_p0', '', 'ar_mat_projecteur_pulse_3q', 60, 31, 2, 2, { named: false }),
  B('ar_mat_p1', '', 'ar_mat_projecteur_pulse_3q', 78, 34, 2, 2, { named: false }),
  B('ar_ence_p0', '', 'ar_enceinte_pulse_3q', 60, 36, 3, 2, { named: false }),
  B('ar_ence_p1', '', 'ar_enceinte_pulse_3q', 64, 40, 3, 2, { named: false }),
  B('ar_gantry0', '', 'ar_gantry_led_pulse_3q', 66, 32, 2.5, 7.6, { solid: [], named: false, cover: true, ancre: [2.25, -3.36] }),
  B('ar_strobe0', '', 'ar_strobe_pulse_3q', 56, 36, 1.5, 1.5, { named: false }),
  B('ar_strobe1', '', 'ar_strobe_pulse_3q', 32.5, 34, 1.5, 1.5, { named: false }),
  ...PYL.map(([x, z], i) => AP(`ar_pyl${i}`, 'ar_pylone_projecteur', x + 0.75, z + 0.75, 1.5, 1.5)),
  ...LAMP.map(([x, z], i) => B(`ar_lamp${i}`, '', 'ar_lampadaire', x - 0.3, z - 0.3, 0.6, 0.6, { named: false })),
  B('ar_guichets', 'Guichets', 'ar_guichets_3q', 6, 44, 4, 4),
  B('ar_booking', 'Booking', 'ar_booking_3q', 10, 44, 4, 4),
  B('ar_securite', 'Poste Human Corp', 'ar_securite_3q', 14, 52, 4, 4),
  B('ar_regie', 'Camion régie', 'ar_regie_3q', 76, 50, 8, 4),
  B('ar_panneau', 'Panneau', 'ar_panneau_nml', 90, 60, 2, 0.5),
  B('ar_cam', '', 'pp_camera', 33.8, 31.8, 0.4, 0.4, { named: false }),
  ENS('ar_e_hc', 'ar_ens_human_corp', 17.6, 56.2, 2.6), ENS('ar_e_guichet', 'ar_ens_guichet', 8.2, 48.2, 2.0),
  ...[[35.4, 40.8], [35.4, 33.6]].map(([x, z], i) => ENS(`ar_e_coeur${i}`, 'ar_ens_coeurs', x, z, 1.5, { fige: i > 0, ph: 0 })),
];
export const CLOSED_ARENA = {
  ar_entree: 'L\u2019entrée vitrée et ses six portiques blancs de Human Corp. « Building a better tomorrow. » Derrière, une clameur monte et s\u2019arrête net.',
  ar_guichets: 'Les guichets. L\u2019écran annonce le Festival Pulse of Steel, le 14/11. Complet.',
  ar_booking: 'Le comptoir Booking. Accréditations presse, bracelets artistes et listes d\u2019invités déjà closes.',
  ar_merch_b: 'Merch officiel Human Corp. Les prix s\u2019affichent selon ton score d\u2019engagement.',
  ar_merch_c: 'Un chariot de merch qui roule là où va la file. Les t-shirts sont unis : le motif se télécharge après paiement.',
  ar_truck_n: 'Nouilles du parvis. Le bouillon a le goût de la file : long, tiède, et on y revient.',
  ar_truck_b: 'Boissons. « Hydratation sponsorisée. » La paille est en option, le logo non.',
  ar_securite: 'Le poste de sécurité Human Corp. Une vitre teintée qui te regarde.',
  ar_regie: 'Le camion régie. Des câbles partent vers le dôme comme des racines.',
  ar_tribunes: 'Des gradins de parvis tournés vers les écrans géants, pour ceux qui paient le bruit sans voir la scène.',
  ar_tech_a: 'Bloc technique ouest. Groupes froids, treuils et gaines haute tension qui alimentent l\u2019enceinte.',
  ar_panneau: '« Au-delà de ce point : pas de droits, pas de loi, pas de retour. »',
};
const GRILLES = [[34, 36], [58, 36], [30, 48], [44, 49], [58, 48], [12, 38], [80, 38], [44, 58], [20, 31.4], [68, 31.4]].map(([x, z]) => ({ image: 'ar_grille_evacuation', x, z }));
export const LOCATIONS_ARENA = {
  steel_arena: { id: 'steel_arena', name: 'Steel-Megalopolis · Steel Arena', kind: 'exterior', size: { ...ARENA_TAILLE_PROPOSEE }, light: ARENA,
    ground: { base: '#101012', skin: 'g_ar_dalles_neutre', tileM: 10.24, clean: true, decals: GRILLES,
      marge: { skin: 'g_fs_asphalte', tileM: 10.24, m: 90 },
      zones: [ { x: 36, z: 31.6, w: 16, d: 10.24, kind: 'plate', skin: 'g_ar_parvis_marquages', tileM: 10.24 },
        ...[[24, 39, 9, 9], [52, 39, 10, 9], [6, 45, 20, 9], [66, 45, 20, 11], [8, 38, 5, 5], [84, 38, 5, 5], [21.5, 55.5, 5, 4], [69.5, 55.5, 5, 4]].map(([x, z, w, d]) => ({ x, z, w, d, kind: 'plate', skin: 'g_ar_parvis_use', tileM: 10.24 })),
        { x: 0, z: 60, w: 96, d: 4, kind: 'plate', skin: 'g_fs_asphalte', tileM: 10.24 } ] },
    buildings: BUILDINGS_ARENA, props: [],
    glows: [
      ...[38.5, 41.5, 44, 46.5, 49.5].map(x => ({ x, z: 31, rx: 1.9, rz: 1.2, color: AMBRE, i: 0.90, beat: 'kick' })),
      ...[38.5, 44, 49.5].map(x => ({ x, z: 30.4, y: 2.4, r: 0.78, color: AMBRE, i: 0.95, building: 'ar_entree', beat: 'kick' })),
      { x: 44, z: 30.2, y: 6.2, r: 2.5, color: AMBRE, i: 0.72, building: 'ar_entree', beat: 'kick' },
      { x: 13.2, z: 31.8, rx: 7.4, rz: 2.8, color: VIOLET, i: 0.92, beat: 'kick' }, { x: 13.2, z: 30.8, y: 9.8, r: 2.6, color: AMBRE, i: 0.72, building: 'ar_ecran_s', beat: 'kick' },
      { x: 93.4, z: 14, rx: 2.8, rz: 7.0, color: CYAN, i: 0.92, beat: 'kick' }, { x: 92.8, z: 15, y: 9.5, r: 2.4, color: CYAN, i: 0.72, building: 'ar_ecran_e', beat: 'kick' },
      ...PYL.map(([x, z]) => ({ x: x + 0.75, z: z + 0.85, rx: 2.5, rz: 1.5, color: CYAN, i: 0.56, beat: 'kick' })),
      ...LAMP.map(([x, z]) => ({ x: x + 0.3, z: z + 0.4, rx: 1.9, rz: 1.3, color: VIOLET, i: 0.35 })),
      { x: 25, z: 40.8, rx: 4.4, rz: 1.5, color: AMBRE, i: 0.58, beat: 'kick' },
      { x: 62, z: 33.2, rx: 2.2, rz: 1.4, color: AMBRE, i: 0.58, beat: 'kick' }, { x: 80, z: 36.2, rx: 2.2, rz: 1.4, color: AMBRE, i: 0.58, beat: 'kick' },
      { x: 67.2, z: 35.8, rx: 2.0, rz: 3.8, color: AMBRE, i: 0.52, beat: 'mid' },
      { x: 57.5, z: 37.6, rx: 1.8, rz: 1.2, color: AMBRE, i: 0.65, beat: 'kick' }, { x: 34.0, z: 35.6, rx: 1.8, rz: 1.2, color: AMBRE, i: 0.65, beat: 'kick' },
      { x: 28, z: 44.8, rx: 2.8, rz: 1.3, color: AMBRE, i: 0.6, flicker: true }, { x: 28, z: 43.8, y: 2.1, r: 0.55, color: AMBRE, i: 0.75, building: 'ar_merch_b', flicker: true },
      { x: 56, z: 44.8, rx: 2.8, rz: 1.3, color: AMBRE, i: 0.6, flicker: true }, { x: 56, z: 43.8, y: 2.1, r: 0.5, color: AMBRE, i: 0.75, building: 'ar_merch_c', flicker: true },
      { x: 20, z: 51, rx: 4.2, rz: 1.5, color: ORANGE, i: 0.6, flicker: true }, { x: 20, z: 49.9, y: 2.4, r: 0.6, color: ORANGE, i: 0.8, building: 'ar_truck_n', flicker: true },
      { x: 72, z: 51, rx: 4.2, rz: 1.5, color: AMBRE, i: 0.6, flicker: true }, { x: 72, z: 49.9, y: 2.4, r: 0.6, color: AMBRE, i: 0.8, building: 'ar_truck_b', flicker: true },
      { x: 8, z: 48.7, rx: 2.4, rz: 1, color: AMBRE, i: 0.45, flicker: true }, { x: 12, z: 48.7, rx: 2.4, rz: 1, color: AMBRE, i: 0.45, flicker: true },
      { x: 35.4, z: 41.4, rx: 1.4, rz: 1, color: MAGENTA, i: 0.3 },
      { x: 16, z: 56.7, rx: 2.4, rz: 1.1, color: AMBRE, i: 0.45 }, { x: 80, z: 54.8, rx: 3.8, rz: 1.3, color: AMBRE, i: 0.55, flicker: true, beat: 'mid' },
      { x: 34, z: 32.4, rx: 0.6, rz: 0.4, color: ROUGE, i: 0.5 }, { x: 91, z: 61, rx: 1.6, rz: 1.2, color: ROUGE, i: 0.3 } ],
    enseignes: [
      { id: 'ar_n_tribunes', building: 'ar_tribunes', effet: 'pulse', intensite: 0.95, periode: 2.8 },
      { id: 'ar_n_booking', building: 'ar_booking', effet: 'pulse', intensite: 0.9, periode: 4.2 },
      { id: 'ar_n_merch_b', building: 'ar_merch_b', effet: 'pulse', intensite: 0.9, periode: 3.2, decale: 0.2 },
      { id: 'ar_n_merch_c', building: 'ar_merch_c', effet: 'pulse', intensite: 0.9, periode: 3.6, decale: 0.6 },
      { id: 'ar_n_truck_n', building: 'ar_truck_n', effet: 'gresille', intensite: 0.85, decale: 0.4 },
      { id: 'ar_n_regie', building: 'ar_regie', effet: 'pulse', intensite: 0.9, periode: 4.8, decale: 0.5 } ],
    // calques rythmiques pulse2 + faisceau (769c16d) et props *_pulse/_pulse_b (b3bd9a6) branchés sur ostCentre.
    // Priorité mobile (plafond 8) : les 2 écrans géants (ar2_ecran_geant_*_pulse2) + projecteurs/faisceaux (entrée, dôme, mâts) + rubans entrée/tribunes.
    pulses: [
      { building: 'ar_ecran_s', calque: 'pulse2', mode: 'kick', veille: 0.02, intensite: 1.0, gain: 2.35, decale: 0, punch: 0.052, priorite: 8 },
      { building: 'ar_ecran_e', calque: 'pulse2', mode: 'kick', veille: 0.02, intensite: 1.0, gain: 2.35, decale: 0, punch: 0.052, priorite: 7 },
      { building: 'ar_entree', calque: 'faisceau', mode: 'kick', veille: 0.02, intensite: 0.92, gain: 1.85, decale: 0, punch: 0.032, priorite: 6 },
      { building: 'ar_entree', calque: 'pulse2', mode: 'kick', veille: 0.02, intensite: 1.0, gain: 2.95, decale: 0, punch: 0.045, priorite: 5 },
      { building: 'ar_mat_p0', calque: 'faisceau', mode: 'kick', veille: 0.02, intensite: 1.0, gain: 1.65, decale: 0, punch: 0.032, priorite: 4 },
      { building: 'ar_toit_x1', calque: 'faisceau', mode: 'kick', veille: 0.02, intensite: 1.0, gain: 1.60, decale: 0, priorite: 3 },
      { building: 'ar_toit_se', calque: 'faisceau', mode: 'kick', veille: 0.02, intensite: 1.0, gain: 1.60, decale: 0.04, priorite: 2 },
      { building: 'ar_tribunes', calque: 'pulse2', mode: 'kick', veille: 0.03, intensite: 1.0, gain: 1.75, decale: 0.04, punch: 0.030, priorite: 1 },
      // Autres faisceaux et rubans pulse2 du dôme et de l'enceinte
      { building: 'ar_toit_so', calque: 'faisceau', mode: 'kick', veille: 0.02, intensite: 1.0, gain: 1.55, decale: 0.08 },
      { building: 'ar_toit_x0', calque: 'faisceau', mode: 'kick', veille: 0.02, intensite: 1.0, gain: 1.55, decale: 0.04 },
      { building: 'ar_toit_x2', calque: 'faisceau', mode: 'kick', veille: 0.02, intensite: 1.0, gain: 1.55, decale: 0.04 },
      { building: 'ar_toit_z', calque: 'faisceau', mode: 'kick', veille: 0.02, intensite: 1.0, gain: 1.55, decale: 0.08 },
      { building: 'ar_toit_so', calque: 'pulse2', mode: 'kick', veille: 0.03, intensite: 1.0, gain: 1.60, decale: 0.08 },
      { building: 'ar_toit_x0', calque: 'pulse2', mode: 'kick', veille: 0.03, intensite: 1.0, gain: 1.60, decale: 0.04 },
      { building: 'ar_toit_x1', calque: 'pulse2', mode: 'kick', veille: 0.03, intensite: 1.0, gain: 1.65, decale: 0 },
      { building: 'ar_toit_x2', calque: 'pulse2', mode: 'kick', veille: 0.03, intensite: 1.0, gain: 1.60, decale: 0.04 },
      { building: 'ar_toit_z', calque: 'pulse2', mode: 'kick', veille: 0.03, intensite: 1.0, gain: 1.60, decale: 0.08 },
      { building: 'ar_toit_se', calque: 'pulse2', mode: 'kick', veille: 0.03, intensite: 1.0, gain: 1.60, decale: 0.05 },
      { building: 'ar_f_s0', calque: 'pulse2', mode: 'kick', veille: 0.03, intensite: 1.0, gain: 1.55, decale: 0.06 },
      { building: 'ar_f_s1', calque: 'pulse2', mode: 'kick', veille: 0.03, intensite: 1.0, gain: 1.60, decale: 0.04 },
      { building: 'ar_f_s2', calque: 'pulse2', mode: 'kick', veille: 0.03, intensite: 1.0, gain: 1.60, decale: 0.04 },
      { building: 'ar_f_s3', calque: 'pulse2', mode: 'kick', veille: 0.03, intensite: 1.0, gain: 1.55, decale: 0.08 },
      { building: 'ar_f_angle', calque: 'pulse2', mode: 'kick', veille: 0.03, intensite: 1.0, gain: 1.60, decale: 0.08 },
      { building: 'ar_f_est', calque: 'pulse2', mode: 'kick', veille: 0.03, intensite: 0.98, gain: 1.55, decale: 0.06 },
      { building: 'ar_f_retour', calque: 'pulse2', mode: 'kick', veille: 0.03, intensite: 0.98, gain: 1.55, decale: 0.12 },
      // Faisceaux des 4 pylônes + props rythmiques + bâtiments 3/4 du parvis
      ...PYL.map((_, i) => ({ building: `ar_pyl${i}`, calque: 'faisceau', mode: 'kick', veille: 0.02, intensite: 1.0, gain: 1.55, decale: i * 0.04, punch: 0.028 })),
      { building: 'ar_mat_p0', calque: 'pulse', mode: 'kick', veille: 0.03, intensite: 1.0, gain: 1.60, punch: 0.028 },
      { building: 'ar_mat_p0', calque: 'pulse_b', mode: 'high', veille: 0.04, intensite: 0.72, decale: 0.20 },
      { building: 'ar_mat_p1', calque: 'faisceau', mode: 'kick', veille: 0.02, intensite: 1.0, gain: 1.65, decale: 0.06, punch: 0.032 },
      { building: 'ar_mat_p1', calque: 'pulse', mode: 'kick', veille: 0.03, intensite: 1.0, gain: 1.60, decale: 0.06, punch: 0.028 },
      { building: 'ar_mat_p1', calque: 'pulse_b', mode: 'high', veille: 0.04, intensite: 0.72, decale: 0.36 },
      { building: 'ar_gantry0', calque: 'pulse', mode: 'kick', veille: 0.03, intensite: 1.0, gain: 1.65, decale: 0.03, punch: 0.028 },
      { building: 'ar_gantry0', calque: 'pulse_b', mode: 'mid', veille: 0.04, intensite: 0.72, decale: 0.25 },
      { building: 'ar_ence_p0', calque: 'pulse', mode: 'kick', veille: 0.03, intensite: 1.0, gain: 1.65, punch: 0.030 },
      { building: 'ar_ence_p0', calque: 'pulse_b', mode: 'mid', veille: 0.04, intensite: 0.70, decale: 0.18 },
      { building: 'ar_ence_p1', calque: 'pulse', mode: 'kick', veille: 0.03, intensite: 1.0, gain: 1.65, decale: 0.06, punch: 0.030 },
      { building: 'ar_ence_p1', calque: 'pulse_b', mode: 'mid', veille: 0.04, intensite: 0.70, decale: 0.28 },
      { building: 'ar_strobe0', calque: 'pulse', mode: 'kick', veille: 0.02, intensite: 1.0, gain: 1.85, punch: 0.034 },
      { building: 'ar_strobe0', calque: 'pulse_b', mode: 'high', veille: 0.03, intensite: 0.72, decale: 0.25 },
      { building: 'ar_strobe1', calque: 'pulse', mode: 'kick', veille: 0.02, intensite: 1.0, gain: 1.85, decale: 0.5, punch: 0.034 },
      { building: 'ar_strobe1', calque: 'pulse_b', mode: 'high', veille: 0.03, intensite: 0.72, decale: 0.75 },
      { building: 'ar_regie', calque: 'pulse2', mode: 'kick', veille: 0.03, intensite: 0.98, gain: 1.55, decale: 0.08 },
      { building: 'ar_guichets', calque: 'pulse', mode: 'high', veille: 0.04, intensite: 0.85, decale: 0.22 },
      { building: 'ar_booking', calque: 'pulse', mode: 'mid', veille: 0.04, intensite: 0.85, decale: 0.30 },
      { building: 'ar_securite', calque: 'pulse', mode: 'kick', veille: 0.03, intensite: 0.95, gain: 1.45, decale: 0.08 },
      { building: 'ar_tech_a', calque: 'pulse', mode: 'mid', veille: 0.04, intensite: 0.85, decale: 0.40 },
      { building: 'ar_merch_b', calque: 'pulse', mode: 'high', veille: 0.04, intensite: 0.85, decale: 0.26 },
      { building: 'ar_truck_n', calque: 'pulse', mode: 'mid', veille: 0.04, intensite: 0.85, decale: 0.38 },
    ],
    projecteurs: PYL.map((_, i) => ({ building: `ar_pyl${i}`, couleur: CYAN, longueur: 32, ouverture: [2.8, 3.1, 2.9, 3.0][i], inclinaison: [22, 25, 24, 23][i],
      cap: [24, -24, 10, -10][i], balayage: [34, 24, 38, 30][i], periode: [11, 14, 9.5, 12.5][i], decale: [0, 3.5, 7, 1.8][i], intensite: 0.20 })),
    extras: [ { sprite: 'gen_ar_fan_chignons', x: 40.4, z: 38.9, face: 1, role: 'fan' }, { sprite: 'gen_ar_techwear', x: 46, z: 35.9, face: -1, role: 'fan' },
      { sprite: 'gen_ar_manteau', x: 62, z: 48, face: -1, role: 'fan' }, { sprite: 'gen_ar_cuir', x: 25.6, z: 56.4, face: 1, role: 'fan' },
      { sprite: 'gen_ar_fan_echarpe', x: 34, z: 38.5, face: 1, role: 'fan' }, { sprite: 'gen_ar_fan_pancarte', x: 54, z: 33, face: -1, role: 'fan' },
      { sprite: 'gen_ar_fan_batons', x: 53, z: 47.6, face: -1, role: 'fan' }, { sprite: 'gen_ar_fans_duo', x: 26, z: 47, face: 1, role: 'fan' },
      ...FIG([[38.2, 31.2], [39.8, 30.9, -1], [41, 31.6], [42.4, 31], [43.4, 31.8, -1], [45.4, 31.1], [46.6, 31.7], [47.8, 30.9, -1], [49, 31.5], [36.6, 31.4], [38.8, 32.9, -1], [37.4, 32.4], [40.6, 32.6], [47.2, 32.7, -1], [50.2, 32.6]], 0, 'foule'),
      ...FIG([[39.2, 35.7], [42.2, 35.2], [44.6, 35.8, -1], [48.2, 35.2], [41.8, 38.9], [44.2, 38.2, -1], [47.6, 38.8], [38.8, 41.7], [41.4, 41.2], [45.6, 41.8, -1], [47.8, 41.3], [39.6, 44.8], [42.8, 44.2, -1], [45.2, 44.9], [47.4, 44.3]], 3, 'attente'),
      ...FIG([[18.2, 36.6, -1], [8.8, 32.6, -1], [9.8, 33.8, -1], [11.2, 32.9, -1], [12.6, 34.2, -1], [14.2, 33.1, -1], [15.8, 34.4, -1], [8.8, 35.6, -1], [12, 36, -1], [16.2, 35.4, -1]], 19, 'ecran'),
      ...FIG([[26.6, 44.9], [28.0, 45.4, -1], [29.6, 44.8], [31.2, 44.6, -1], [24.8, 44.8], [27.4, 46.4, -1], [30.4, 46.0], [29.0, 45.8, -1]], 7, 'grappe'),
      ...FIG([[55.4, 44.9], [56.8, 45.5, -1], [59.0, 44.6, -1], [55.0, 46.1], [58.0, 45.2, -1]], 11, 'grappe'),
      ...FIG([[18.6, 51.8], [19.4, 53.0, -1], [21.8, 51.2], [23.0, 52.3, -1], [24.6, 51.1], [23.8, 50.8, -1]], 13, 'grappe'),
      ...FIG([[68.8, 50.9], [70.2, 51.8, -1], [71.6, 51.0], [72.8, 52.2, -1], [73.6, 51.3], [69.6, 52.6, -1], [77.4, 54.9], [81.4, 55.2, -1]], 17, 'grappe'),
      ...FIG([[10.8, 49.0], [11.8, 50.2, -1], [21.6, 41.4, -1], [23.4, 41.8, -1]], 5, 'grappe'),
      ...FIG([[36.2, 33.4], [51.4, 33.2, -1], [37.8, 34.6], [50.2, 34.8, -1], [35.4, 36.2], [48.6, 33.8, -1]], 21, 'foule') ],
    walkers: [ ...[0, 8, 16, 24, 32, 40, 48].map((t0, i) => ({ sprite: ['gen_ar_foule_a', 'gen_pp_foule_b', 'gen_ar_foule_b', 'gen_fs_foule_a', 'gen_ml_fan', 'gen_pp_foule_h', 'gen_df_foule_a'][i], path: [[50, 49], [50, 44.6], [38, 44.6], [38, 41.6], [49.4, 41.6], [49.4, 38.6], [38, 38.6], [38, 35.6], [49.4, 35.6], [49.4, 32.9], [44, 32.9]], speed: 0.3, t0, aller: true, role: 'file' })),
      { sprite: 'gen_ar_foule_a', path: [[3, 62.2], [94, 62.2]], speed: 0.6, t0: 3 }, { sprite: 'gen_pp_foule_c', path: [[93, 63.2], [3, 63.2]], speed: 0.6, t0: 10 } ],
    spawn: { player: { x: 1, z: 44 }, companion: { x: 1, z: 45 } }, city: 'steel',
    cadre: { arrivee: { mobile: { ppm: 4, avance: 12, u: [26, 30] }, desktop: { ppm: 12, avance: 10, u: [26, 30] } } },
    arrive: { from: 'steel_pulse', text: 'La Steel Arena. L\u2019enceinte noire mange tout le nord ; quatre faisceaux cyan balaient le plafond du sarcophage. « Human Corp sponsorise le sourire. »' } },
};
const J = (id, loc, ox, oz, tx, tz, to, label, conditions = []) => ({ id, location: loc, junction: true, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: { doorId: to }, conditions });
export const DOORS_ARENA = [
  J('ar_ouest', 'steel_arena', 0, 44, 1, 44, 'pp_est', 'Pulse Plaza'),
  J('ar_est', 'steel_arena', 96, 44, 95, 44, 'fs_est', 'Fréquence Strip'),
  J('fs_est', 'steel_strip', 80, 13, 79, 13, 'ar_est', 'La grille de l\u2019Arena'),
];
export const NPCS_ARENA = [
  { id: 'ar_ferrand', name: 'Ferrand', sprite: 'gen_ar_ferrand', location: 'steel_arena', x: 53.4, z: 32.2, faceTo: [44, 34], dialogue: 'ar_ferrand' },
  { id: 'ar_anouk', name: 'Anouk', sprite: 'gen_ar_anouk', location: 'steel_arena', x: 8, z: 48.8, faceTo: [8, 52], dialogue: 'ar_anouk' },
  { id: 'ar_zelie', name: 'Zélie', sprite: 'gen_ar_zelie', location: 'steel_arena', x: 9, z: 52.4, faceTo: [14, 48], dialogue: 'ar_zelie' },
  { id: 'ar_malik', name: 'Malik', sprite: 'gen_ar_malik', location: 'steel_arena', x: 79, z: 55, faceTo: [74, 50], dialogue: 'ar_malik' },
  { id: 'ar_ines', name: 'Inès', sprite: 'gen_ar_ines', location: 'steel_arena', x: 39, z: 31.9, faceTo: [44, 31], dialogue: 'ar_ines' },
  { id: 'ar_clem', name: 'Clém', sprite: 'gen_ar_clem', location: 'steel_arena', x: 53.6, z: 45, faceTo: [49, 41], dialogue: 'ar_clem' },
  { id: 'ar_garnier', name: 'Agent Garnier', sprite: 'gen_ar_garnier', location: 'steel_arena', x: 19, z: 57, faceTo: [24, 54], dialogue: 'ar_garnier' },
  { id: 'ar_bastien', name: 'Bastien', sprite: 'gen_ar_bastien', location: 'steel_arena', x: 84.4, z: 42.4, faceTo: [86, 40], dialogue: 'ar_bastien' },
  { id: 'ar_laure', name: 'Madame Laure', sprite: 'gen_ar_laure', location: 'steel_arena', x: 89, z: 61.6, faceTo: [84, 58], dialogue: 'ar_laure' },
  { id: 'ar_revendeur', name: 'Le revendeur', sprite: 'gen_ar_revendeur', location: 'steel_arena', x: 33, z: 44, faceTo: [40, 40], dialogue: 'ar_revendeur' },
  { id: 'ar_revendeuse', name: 'La revendeuse', sprite: 'gen_ar_revendeuse', location: 'steel_arena', x: 60, z: 46.4, faceTo: [56, 42], dialogue: 'ar_revendeuse' },
];
const D = (t1, t2) => ({ start: { text: t1, options: [ { label: 'Et sinon ?', next: 'b' }, { label: 'Au revoir.', next: 'end' } ] }, b: { text: t2, options: [ { label: 'Au revoir.', next: 'end' } ] } });
const D1 = t1 => ({ start: { text: t1, options: [ { label: 'Au revoir.', next: 'end' } ] } });
export const DIALOGUES_ARENA = {
  ar_ferrand: D('Billet, implant, sourire. Dans cet ordre, s\u2019il vous plaît.', 'Vous n\u2019êtes pas dans la liste. Personne n\u2019est pas dans la liste. Reculez.'),
  ar_anouk: D('Ce soir c\u2019est complet. Demain aussi. Pour le Festival du 14, il reste des places debout derrière les places debout.', 'Le prix change selon votre score d\u2019engagement. Ne me demandez pas comment, c\u2019est l\u2019écran qui calcule.'),
  ar_zelie: D('Vrai billet, vraie puce, faux nom. Ça passe neuf fois sur dix. La dixième, tu cours.', 'Tu es grillé, toi. Je ne te connais pas.'),
  ar_malik: D('Trois mille personnes à l\u2019intérieur, et le show tient sur une seule console. Si elle plante, je deviens célèbre.', 'Les cris du public sont mixés, comme le reste. Ce soir, on en a ajouté vingt pour cent.'),
  ar_ines: D('Je n\u2019ai pas de billet. Je viens pour la file. Ici, au moins, on est ensemble.', 'Personne ne sait qui elle est sous le chapeau. Moi je dis qu\u2019elle est comme nous, et qu\u2019elle a juste eu de la chance. Ou pas.'),
  ar_clem: D('Je fais le direct de la file. Les gens adorent regarder d\u2019autres gens attendre.', 'On m\u2019a demandé de ne pas filmer le panneau du fond. Alors évidemment, tout le monde le filme.'),
  ar_garnier: D('Ici c\u2019est Human Corp qui garde la porte. Nous, on garde ceux qui restent dehors.', 'Le panneau là-bas ? Une blague de mauvais goût. Ou un avertissement. Je ne suis pas payé pour choisir.'),
  ar_bastien: D1('Quatre faisceaux, et ils doivent rester synchrones avec la musique. Le jour où ils se décalent, ça fait une prière ratée.'),
  ar_laure: D('J\u2019ai placé des gens ici pendant trente ans. Avant, on voyait les visages des chanteurs. Maintenant on voit les écrans.', 'Ce panneau était là avant l\u2019Arena. On a construit autour, et on n\u2019a jamais osé l\u2019enlever.'),
  ar_revendeur: D('Places debout, places assises, places imaginaires. Les dernières sont les moins chères.', 'Le billet est vrai. C\u2019est la date qui est approximative.'),
  ar_revendeuse: D('Tu veux entrer, ou tu veux pouvoir dire que tu étais là ? La deuxième option coûte moins cher.', 'Je ne rembourse pas. Les concerts non plus.'),
};
