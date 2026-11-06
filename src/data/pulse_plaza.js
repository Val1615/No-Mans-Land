// Pulse Plaza (zone steel_pulse, quartier de Center-Town). Pack d'Ocre : docs/villes/steel/quartiers/pulse_plaza/PULSE_PLAZA.md et ASSETS.md.
// [décision Valentin] zone à part, porte vers Center-Town (comme Lower-Town), sortie sud vers la grille c_sud. Groovy Vibes et Groovy-Tron
// n'apparaissent que sur les écrans et les médias (écran du feed, billboard, hologramme) : jamais rencontrés, aucun sosie qui parle.
// Le nom civil de Vibes n'apparaît nulle part. Bâtiments festifs *_v2_3q (b3bd9a6 + 769c16d, guérite conservée en pp_guerite_3q), props rythmiques et sync ostCentre.
const PULSE = { bg: '#060a10', hemi: ['#b8a0f0', '#2e2034', 1.3], sun: ['#e6c8a8', 0.6], tint: '#b8aec4', actor: '#ddd4e8' };
const VIOLET = '#8a3cff', MAGENTA = '#e03ca8', CYAN = '#a9d2e6', CHAUD = '#ffae55', ROUGE = '#c8323c';
const B = (id, label, sprite, x, z, w, d, extra = {}) => ({ id, label, sprite, x, z, w, d, visitable: false, cue: null, named: !!label, ...extra });
const CAMS = [[9, 7], [35, 7], [17, 25], [35, 25]];
// Bords de la place sur trame de 4 m : nord en *_v2_3q (fronts z 0, emprises z -4 -> 0), ouest en *_v2_3q (fronts x 0, emprises x -4 -> 0, accès ouest z 12-16 libre),
// sud et est fermés par les murets de 1,2 m et le support d'écran e2 (accès escalier sud x 20-28 et jonction Strip z 12-16 libres).
const FACADES = [ // [id, sprite, x, z, w, d]
  ['pp_fac_n1', 'pp_nord_c2_v2_3q', 0, -4, 12, 4], ['pp_fac_n2', 'pp_nord_a_v2_3q', 12, -4, 16, 4], ['pp_fac_n4', 'pp_nord_b_v2_3q', 28, -4, 8, 4], ['pp_fac_n3', 'pp_nord_c3_v2_3q', 36, -4, 12, 4],
  ['pp_fac_o1', 'pp_ouest_a_v2_3q', -4, 0, 4, 12], ['pp_fac_o2', 'pp_ouest_b_v2_3q', -4, 16, 4, 8], ['pp_fac_o3', 'pp_ouest_b_v2_3q', -4, 24, 4, 8], ['pp_mur_o4', 'pp_muret_4_o', -0.4, 32, 0.4, 4],
  ['pp_mur_s1', 'pp_muret', 0, 36, 8, 0.4], ['pp_mur_s2', 'pp_muret', 8, 36, 8, 0.4], ['pp_mur_s3', 'pp_muret_4', 16, 36, 4, 0.4],
  ['pp_mur_s4', 'pp_muret_4', 28, 36, 4, 0.4], ['pp_mur_s5', 'pp_muret', 32, 36, 8, 0.4], ['pp_mur_s6', 'pp_muret', 40, 36, 8, 0.4],
  ['pp_mur_e0', 'pp_muret_o', 48, 0, 0.4, 8], ['pp_mur_e1', 'pp_muret_4_o', 48, 8, 0.4, 4], ['pp_mur_e3', 'pp_muret_4_o', 48, 16, 0.4, 4], ['pp_mur_e4', 'pp_support_ecran_o', 48, 20, 0.4, 4],
  ['pp_mur_e5', 'pp_muret_4_o', 48, 24, 0.4, 4], ['pp_mur_e2', 'pp_muret_o', 48, 28, 0.4, 8],
];
// Écrans en hauteur d'Ocre (accrochés devant leur façade nord en z 0..0.6 ou sur leur support est, non-solides, contenu dessiné par le code).
const ECRANS_HAUTS = [ ['pp_ecran_n1', 'pp_ecran_haut_n1', 39, 0, 8, 0.6], ['pp_ecran_n2', 'pp_ecran_haut_n2', 3, 0, 4, 0.6], ['pp_ecran_e2', 'pp_ecran_haut_e2', 48.3, 20, 0.1, 4] ];
const GARDE_CORPS = [];
// Bandes de grille assombrie au pied des façades et des stands 4x4
const PIEDS = [
  [0, 0, 48, 1], [0, 1, 0.8, 7], [0, 16, 0.8, 12], [0, 35.2, 20, 0.8], [28, 35.2, 20, 0.8],
  [44, 12, 4, 0.6], [0, 12, 4, 0.6], [40, 24, 4, 0.6], [0, 32, 4, 0.6], [8, 32, 4, 0.6], [36, 32, 4, 0.6], [44, 32, 4, 0.6],
];
const LAMPES = [[8, 14], [8, 26], [40, 14], [34.5, 31]], BORNES = [[11, 11.8], [33.5, 11.8]];
const MOBILIER = [
  ...LAMPES.map(([x, z], i) => [`pp_lampe${i}`, 'pp_lampadaire', x, z, 0.6, 0.6]),
  ...[[13, 19], [14.5, 26], [33, 25]].map(([x, z], i) => [`pp_statue${i}`, 'pp_statue', x, z, 2, 2]),
  ...BORNES.map(([x, z], i) => [`pp_borne${i}`, 'pp_borne_neon', x, z, 0.5, 0.5]),
  ...[[4, 21.5], [39.2, 24]].map(([x, z], i) => [`pp_jard${i}`, 'pp_jardiniere', x, z, 1.6, 1.6]),
  ['pp_banc3', 'pp_banc_bois', 38, 21, 2, 0.6], ['pp_banc4', 'pp_banc_beton_o', 46.8, 20, 0.6, 2],
];
// Écran du Feed v2 3/4 (pp_ecran_feed_v2_3q, 941 x 623, ancre [826, 621]) : dalle noire mesurée sur la face avant x [132..755], pente 0,331, hauteur 274 px.
const ECRAN_FEED = { coins: [[132, 37], [755, 242], [755, 516], [132, 311]], periode: 9, beat: true, pages: [
  { fond: ['#3a1470', '#7a2cc8'], image: 'pp_billboard', crop: [40, 175, 128, 240], titre: 'GROOVY VIBES', sous: 'Clip officiel · Feed 24/7', bandeau: '100% connection stable. Jusqu’à la prochaine alerte.' },
  { fond: ['#200a40', '#5a1c9a'], titre: 'L’IDOLE DÉMASQUÉE', sous: 'Qui est vraiment Groovy Vibes ?', bandeau: '100% connection stable. Jusqu’à la prochaine alerte.' },
  { fond: ['#081a2c', '#2a5a8a'], image: 'pp_holo_tron', crop: [0, 0, 81, 180], titre: 'GROOVY-TRON.EXE', sous: 'Démarrage…', bandeau: 'Status : Optimum. Le sourire est une mise à jour.' },
  { fond: ['#3a0a2a', '#b02a7a'], titre: 'AUDIENCE SYNC', sous: 'Applaudissez maintenant', bandeau: '100% connection stable. Jusqu’à la prochaine alerte.' },
] };
export const BUILDINGS_PULSE = [
  // Dalles lumineuses de l'allée centrale (b3bd9a6, fond: true, praticables sans solide)
  B('pp_dalle_pa0', '', 'pp_dalle_pulse_a_3q', 22, 12, 4, 4, { solid: [], named: false, fond: true }),
  B('pp_dalle_pb0', '', 'pp_dalle_pulse_b_3q', 26, 12, 4, 4, { solid: [], named: false, fond: true }),
  B('pp_portique', 'Portique IO', 'pp_portique_v2_3q', 20, 0, 4, 4),
  B('pp_arche0', '', 'pp_arche_holo_3q', 21, 4, 6, 2, { solid: [], named: false, cover: true }),
  B('pp_ecran_feed', 'Écran du Feed 24/7', 'pp_ecran_feed_v2_3q', 12, 8, 20, 4, { sign: true, ecran: ECRAN_FEED }),
  B('pp_holo', 'Projection Holo-Tron', 'pp_holo_socle', 20, 14, 8, 8),
  B('pp_holo_tron', '', 'pp_holo_tron', 23.7, 17.7, 0.6, 0.6, { solid: [], named: false, cover: true }),
  B('pp_totem0', '', 'pp_totem_pulse_3q', 18, 18, 2, 2, { named: false }),
  B('pp_ence0', '', 'pp_enceinte_pulse_3q', 16, 22, 2, 2, { named: false }),
  B('pp_pont0', '', 'pp_pont_projecteurs_v2_3q', 10, 20, 8, 2, { solid: [], named: false, cover: true }),
  B('pp_billboard', 'Billboard HCM-88X', 'pp_billboard_v2_3q', 0, 8, 4, 4),
  B('pp_kiosque', 'Kiosque merch officiel', 'pp_kiosque_v2_3q', 44, 8, 4, 4),
  B('pp_guerite', 'Guérite SMPD', 'pp_guerite_3q', 0, 28, 4, 4),
  B('pp_nouilles', 'Stand de nouilles', 'pp_nouilles_v2_3q', 44, 28, 4, 4),
  B('pp_distrib', 'Distributeur « sourire calibré »', 'pp_distrib_v2_3q', 40, 20, 4, 4),
  B('pp_kiosque_presse', 'Kiosque presse', 'pp_kiosque_presse_v2_3q', 8, 28, 4, 4),
  B('pp_kiosque_boissons', 'Kiosque boissons', 'pp_kiosque_boissons_v2_3q', 36, 28, 4, 4),
  B('pp_banc1', '', 'pp_banc', 4, 20, 2, 1, { named: false }), B('pp_banc2', '', 'pp_banc', 4, 23, 2, 1, { named: false }),
  ...CAMS.map(([x, z], i) => B(`pp_cam${i}`, '', 'pp_camera', x - 0.2, z - 0.2, 0.4, 0.4, { named: false })),
  B('pp_escalier', '', 'pp_escalier', 22, 28, 4, 4, { solid: [], named: false }),
  ...FACADES.map(([id, sprite, x, z, w, d]) => B(id, '', sprite, x, z, w, d, { named: false })),
  ...ECRANS_HAUTS.map(([id, sprite, x, z, w, d], i) => B(id, '', sprite, x, z, w, d, { named: false, solid: [], ecran: { periode: 11 + i * 2, decale: i + 1, beat: true, pages: ECRAN_FEED.pages } })),
  ...MOBILIER.map(([id, sprite, ax, az, w, d]) => B(id, '', sprite, ax - w, az - d, w, d, { named: false })),
];
export const CLOSED_PULSE = { // textes des écrans, stands et façades (aucun nom civil)
  pp_portique: 'Le portique d’IO. Il lit les implants de ceux qui passent. Le tien, il le lit un peu trop longtemps.',
  pp_ecran_feed: '« L’idole démasquée. Qui est vraiment Groovy Vibes ? » Puis le bandeau : « 100% connection stable. Jusqu’à la prochaine alerte. » Puis « Audience sync » : la place applaudit d’un seul coup, et s’arrête net.',
  pp_holo: 'Groovy-Tron, en hologramme à taille double, tourne lentement sur son socle chromé. C’est une image. Il ne te voit pas.',
  pp_billboard: 'Billboard HCM-88X. Groovy Vibes, sourire figé : « Status : Optimum. Le sourire est une mise à jour. »',
  pp_guerite: 'La guérite du SMPD. Une vitre, une lampe, et quelqu’un derrière qui te regarde déjà.',
  pp_distrib: 'Une borne violette : passes pour la soirée Next Drop du Club Neon-7. Paiement en crédits, sourire conseillé.',
  pp_kiosque: 'Kiosque Human Corp : casquette pixel, stickers holo, pack EXE, poster Error 404.',
  pp_nouilles: 'Le stand de l’oncle Pham. Le seul coin de la place sans écran.',
  pp_kiosque_presse: 'Holo-presse validée par IO : éditions du soir, programmes du Feed et portrait officiel de la tournée.',
  pp_kiosque_boissons: 'Hydratation synthétique, électrolytes chromés et canettes à l’effigie du groupe. En crédits seulement.',
};
export const LOCATIONS_PULSE = {
  steel_pulse: { id: 'steel_pulse', name: 'Steel-Megalopolis · Pulse Plaza', kind: 'exterior', size: { w: 48, d: 36 }, light: PULSE,
    ground: { base: '#141826', skin: 'g_pp_dalle_sombre', tileM: 4, clean: true, zones: [
      { x: 20, z: 30, w: 8, d: 6, kind: 'plate', tint: 'rgba(10,12,22,.55)' },
      { x: 12, z: 12, w: 20, d: 2, kind: 'wet', skin: 'g_pp_dalle_mouillee', tint: 'rgba(10,10,20,.35)' }, { x: 19, z: 22, w: 10, d: 1.5, kind: 'wet', skin: 'g_pp_dalle_mouillee', tint: 'rgba(10,10,20,.35)' },
      ...PIEDS.map(([x, z, w, d]) => ({ x, z, w, d, kind: 'plate', skin: 'g_pp_grille', tint: 'rgba(6,6,12,.55)' })) ],
      paint: [ { x: 22, z: 4, w: 4, d: 24, skin: 'g_pp_allee' }, { x: 0, z: 15, w: 22, d: 2, skin: 'g_pp_allee_ew' }, { x: 26, z: 15, w: 22, d: 2, skin: 'g_pp_allee_ew' } ] },
    gardeCorps: GARDE_CORPS, labelsProches: { ids: ['pp_ecran_feed', 'pp_vasseur', 'pp_isaure', 'pp_maelle'], r: 3 },
    accessLabels: false,
    buildings: BUILDINGS_PULSE, props: [],
    // Enseignes _neon : pp_billboard_v2_3q_neon sur le billboard v2, pulse sur PULSE et le distributeur, léger grésillement sur les nouilles ; les autres restent fixes auto.
    enseignes: [
      { id: 'pp_n_billboard', building: 'pp_billboard', neon: 'pp_billboard_v2_3q_neon', effet: 'pulse', periode: 3.6, intensite: 0.95 },
      { id: 'pp_n_nord_a', building: 'pp_fac_n2', effet: 'pulse', periode: 2.8, intensite: 0.95 },
      { id: 'pp_n_distrib', building: 'pp_distrib', effet: 'pulse', periode: 3.2, intensite: 0.9, decale: 0.6 },
      { id: 'pp_n_nouilles', building: 'pp_nouilles', effet: 'gresille', intensite: 0.85, decale: 0.5 },
    ],
    // Calques rythmiques *_ecran, *_pulse (kick), *_faisceau (kick) et *_pulse_b (mid / aigus) branchés sur ostCentre (~170 BPM, kick ≈ 0,35 s).
    // Priorité mobile (plafond 8) : Feed (pulse + ecran) + Nord_A (pulse + ecran) + Billboard (pulse + ecran) + Pont v2 faisceau + Dalle A.
    pulses: [
      { building: 'pp_ecran_feed', calque: 'pulse', mode: 'kick', intensite: 1.0, punch: 0.022, priorite: 8 },
      { building: 'pp_ecran_feed', calque: 'ecran', mode: 'mid', intensite: 0.92, punch: 0.012, priorite: 5 },
      { building: 'pp_ecran_feed', calque: 'pulse_b', mode: 'high', intensite: 0.92, decale: 0.12 },
      { building: 'pp_fac_n2', calque: 'pulse', mode: 'kick', intensite: 1.0, decale: 0.05, punch: 0.020, priorite: 7 },
      { building: 'pp_fac_n2', calque: 'ecran', mode: 'mid', intensite: 0.90, decale: 0.08, priorite: 3 },
      { building: 'pp_fac_n2', calque: 'pulse_b', mode: 'mid', intensite: 0.88, decale: 0.5 },
      { building: 'pp_billboard', calque: 'pulse', mode: 'kick', intensite: 1.0, decale: 0.10, punch: 0.022, priorite: 6 },
      { building: 'pp_billboard', calque: 'ecran', mode: 'mid', intensite: 0.92, decale: 0.14, priorite: 4 },
      { building: 'pp_billboard', calque: 'pulse_b', mode: 'high', intensite: 0.90, decale: 0.25 },
      { building: 'pp_pont0', calque: 'faisceau', mode: 'kick', intensite: 1.0, decale: 0.04, punch: 0.024, priorite: 2 },
      { building: 'pp_pont0', calque: 'pulse', mode: 'kick', intensite: 0.98, decale: 0.04, punch: 0.020 },
      { building: 'pp_pont0', calque: 'pulse_b', mode: 'high', intensite: 0.95, decale: 0.18 },
      { building: 'pp_dalle_pa0', calque: 'pulse', mode: 'kick', intensite: 1.0, punch: 0.024, priorite: 1 },
      { building: 'pp_dalle_pa0', calque: 'pulse_b', mode: 'mid', intensite: 0.90, decale: 0.25 },
      { building: 'pp_dalle_pb0', calque: 'pulse', mode: 'kick', intensite: 0.96, decale: 0.5, punch: 0.022 },
      { building: 'pp_dalle_pb0', calque: 'pulse_b', mode: 'mid', intensite: 0.92, decale: 0.15 },
      { building: 'pp_arche0', calque: 'pulse', mode: 'kick', intensite: 0.95, decale: 0.08 },
      { building: 'pp_arche0', calque: 'pulse_b', mode: 'mid', intensite: 0.90, decale: 0.30 },
      { building: 'pp_totem0', calque: 'pulse', mode: 'kick', intensite: 0.96, decale: 0.12 },
      { building: 'pp_totem0', calque: 'pulse_b', mode: 'high', intensite: 0.94, decale: 0.22 },
      { building: 'pp_ence0', calque: 'pulse', mode: 'kick', intensite: 0.98, punch: 0.024 },
      { building: 'pp_ence0', calque: 'pulse_b', mode: 'mid', intensite: 0.88, decale: 0.16 },
      { building: 'pp_fac_n1', calque: 'pulse', mode: 'kick', intensite: 0.95, decale: 0.18 },
      { building: 'pp_fac_n1', calque: 'ecran', mode: 'mid', intensite: 0.86, decale: 0.20 },
      { building: 'pp_fac_n1', calque: 'pulse_b', mode: 'mid', intensite: 0.85, decale: 0.42 },
      { building: 'pp_fac_n3', calque: 'pulse', mode: 'kick', intensite: 0.95, decale: 0.32 },
      { building: 'pp_fac_n3', calque: 'ecran', mode: 'high', intensite: 0.88, decale: 0.36 },
      { building: 'pp_fac_n3', calque: 'pulse_b', mode: 'high', intensite: 0.85, decale: 0.55 },
      { building: 'pp_fac_n4', calque: 'pulse', mode: 'demi_kick', intensite: 0.92, decale: 0.28 },
      { building: 'pp_fac_n4', calque: 'pulse_b', mode: 'mid', intensite: 0.84, decale: 0.48 },
      { building: 'pp_fac_o1', calque: 'pulse', mode: 'kick', intensite: 0.95, decale: 0.24 },
      { building: 'pp_fac_o1', calque: 'ecran', mode: 'mid', intensite: 0.88, decale: 0.30 },
      { building: 'pp_fac_o1', calque: 'pulse_b', mode: 'mid', intensite: 0.84, decale: 0.52 },
      { building: 'pp_fac_o2', calque: 'pulse', mode: 'demi_kick', intensite: 0.88, decale: 0.16 },
      { building: 'pp_fac_o2', calque: 'pulse_b', mode: 'high', intensite: 0.84, decale: 0.38 },
      { building: 'pp_fac_o3', calque: 'pulse', mode: 'demi_kick', intensite: 0.88, decale: 0.66 },
      { building: 'pp_fac_o3', calque: 'pulse_b', mode: 'mid', intensite: 0.84, decale: 0.72 },
      { building: 'pp_portique', calque: 'pulse', mode: 'kick', intensite: 0.94, decale: 0.14 },
      { building: 'pp_portique', calque: 'pulse_b', mode: 'high', intensite: 0.86, decale: 0.34 },
      { building: 'pp_distrib', calque: 'pulse', mode: 'kick', intensite: 0.94, decale: 0.10 },
      { building: 'pp_distrib', calque: 'ecran', mode: 'mid', intensite: 0.88, decale: 0.20 },
      { building: 'pp_distrib', calque: 'pulse_b', mode: 'high', intensite: 0.86, decale: 0.44 },
      { building: 'pp_kiosque', calque: 'pulse', mode: 'kick', intensite: 0.90, decale: 0.22 },
      { building: 'pp_kiosque', calque: 'pulse_b', mode: 'mid', intensite: 0.85, decale: 0.46 },
      { building: 'pp_kiosque_presse', calque: 'pulse', mode: 'kick', intensite: 0.90, decale: 0.18 },
      { building: 'pp_kiosque_presse', calque: 'ecran', mode: 'mesure', periode: 11, intensite: 0.82, decale: 0.3 },
      { building: 'pp_kiosque_presse', calque: 'pulse_b', mode: 'high', intensite: 0.86, decale: 0.40 },
      { building: 'pp_kiosque_boissons', calque: 'pulse', mode: 'kick', intensite: 0.90, decale: 0.30 },
      { building: 'pp_kiosque_boissons', calque: 'pulse_b', mode: 'mid', intensite: 0.85, decale: 0.56 },
      { building: 'pp_guerite', calque: 'pulse', mode: 'balise', periode: 2.8, intensite: 0.82 },
    ],
    projecteurs: [
      { building: 'pp_pont0', y: 4.4, couleur: CYAN, longueur: 26, ouverture: 4.2, inclinaison: 32, cap: 135, balayage: 28, periode: 7.5, decale: 0, intensite: 0.30 },
      { building: 'pp_ecran_feed', y: 6.8, couleur: MAGENTA, longueur: 24, ouverture: 3.8, inclinaison: 28, cap: 180, balayage: 24, periode: 9.0, decale: 2.5, intensite: 0.26 },
    ],
    glows: [
      { x: 22, z: 13, rx: 11, rz: 4, color: VIOLET, i: 0.88, flicker: true, beat: 'kick' }, { x: 22, z: 13.5, rx: 6.5, rz: 2.6, color: MAGENTA, i: 0.62, flicker: true, beat: 'kick' },
      { x: 24, z: 14, rx: 3.4, rz: 2.4, color: MAGENTA, i: 0.65, beat: 'kick' }, { x: 28, z: 14, rx: 3.4, rz: 2.4, color: CHAUD, i: 0.58, beat: 'mid' },
      { x: 24, z: 18, rx: 4.8, rz: 4.8, color: CYAN, i: 0.66, flicker: true, beat: 'mid' }, { x: 2.2, z: 12.6, rx: 3.2, rz: 2.4, color: MAGENTA, i: 0.76, beat: 'kick' },
      { x: 14, z: 21, rx: 3.8, rz: 2.0, color: CYAN, i: 0.55, beat: 'kick' }, { x: 18, z: 20, rx: 2.2, rz: 1.6, color: MAGENTA, i: 0.58, beat: 'kick' },
      { x: 46, z: 12.6, rx: 2.4, rz: 1.8, color: CHAUD, i: 0.55 }, { x: 42, z: 24.5, rx: 2.4, rz: 1.6, color: VIOLET, i: 0.65, flicker: true, beat: 'kick' },
      { x: 22, z: 4.8, rx: 3.4, rz: 1.8, color: CYAN, i: 0.55, beat: 'mid' }, { x: 46, z: 32.6, rx: 2.6, rz: 1.8, color: CHAUD, i: 0.85, flicker: true }, { x: 2, z: 32.6, rx: 2.2, rz: 1.5, color: '#e8eef2', i: 0.45 },
      { x: 10, z: 32.5, rx: 2.2, rz: 1.4, color: CYAN, i: 0.48 }, { x: 38, z: 32.5, rx: 2.2, rz: 1.4, color: CYAN, i: 0.48 },
      ...CAMS.map(([x, z]) => ({ x: x + 0.2, z: z + 0.2, rx: 0.6, rz: 0.4, color: ROUGE, i: 0.5 })),
      ...LAMPES.map(([x, z]) => ({ x, z, rx: 2.2, rz: 1.6, color: CYAN, i: 0.55 })), ...BORNES.map(([x, z]) => ({ x, z, rx: 1.4, rz: 1.1, color: MAGENTA, i: 0.65, flicker: true, beat: 'kick' })),
      ...[[2, 1.2], [6, 1.2], [10, 1.2], [14.5, 1.2], [20, 1.2], [26, 1.2], [31, 1.2], [38.5, 1.2], [42.5, 1.2], [46, 1.2], [1.2, 4.5], [1.2, 18], [1.2, 22], [1.2, 26]].map(([x, z], idx) => ({ x, z, rx: 1.8, rz: 1.2, color: idx % 3 === 1 ? MAGENTA : CHAUD, i: 0.5, beat: idx % 2 === 0 ? 'kick' : 'mid' })) ],
    extras: [ ...[['c', 15, 14.5], ['d', 19, 13.6], ['e', 29, 15], ['f', 14, 16.6], ['g', 26, 23.4], ['h', 19.6, 24.4], ['i', 30.5, 16.8], ['j', 27, 13.8]].map(([k, x, z]) => ({ sprite: 'gen_pp_foule_' + k, x, z, face: x < 24 ? 1 : -1, role: 'foule' })) ],
    walkers: [ { sprite: 'gen_pp_foule_a', path: [[2, 16], [44, 16]], speed: 0.7, t0: 4 }, { sprite: 'gen_pp_foule_b', path: [[13.5, 33.2], [13.5, 26.8], [34.5, 26.8]], speed: 0.6, t0: 11 } ],
    spawn: { player: { x: 1, z: 14 }, companion: { x: 1, z: 15 } }, city: 'steel',
    arrive: { from: 'steel_center', text: 'Pulse Plaza. Les écrans éclairent tout ; la nuit n’a plus le droit de tomber ici. La foule applaudit en même temps, puis se tait en même temps.' } },
};
const J = (id, loc, ox, oz, tx, tz, to, label, conditions = []) => ({ id, location: loc, junction: true, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: { doorId: to }, conditions });
export const DOORS_PULSE = [
  J('pp_ouest', 'steel_pulse', 0, 14, 1, 14, 'c_nord', 'Vers Center-Town (rue d’arrivée)'),
  J('pp_sud', 'steel_pulse', 24, 36, 24, 35, 'c_pp_sud', 'Escalier de service (vers Center-Town)'),
  J('c_pp_sud', 'steel_center', 26, 36, 26, 35, 'pp_sud', 'Escalier de Pulse Plaza'),
  J('c_nord', 'steel_center', 33, 0, 33, 1, 'pp_ouest', 'Pulse Plaza'),
];
export const NPCS_PULSE = [ // positions recalées autour des emprises 4x4 des bâtiments *_v2_3q et props rythmiques (view.masques() vide) ; aucun n'est Vibes ni Tron
  { id: 'pp_maelle', name: 'Maëlle', sprite: 'gen_pp_maelle', location: 'steel_pulse', x: 17.2, z: 13.4, faceTo: [22, 10], dialogue: 'pp_maelle' },
  { id: 'pp_dorian', name: 'Dorian', sprite: 'gen_pp_dorian', location: 'steel_pulse', x: 41.0, z: 8.4, faceTo: [46, 10], dialogue: 'pp_dorian' },
  { id: 'pp_brisset', name: 'Agente Brisset', sprite: 'gen_pp_brisset', location: 'steel_pulse', x: 5.4, z: 32.4, faceTo: [2, 30], dialogue: 'pp_brisset' },
  { id: 'pp_pham', name: 'Oncle Pham', sprite: 'gen_pp_pham', location: 'steel_pulse', x: 43.2, z: 32.6, faceTo: [46, 30], dialogue: 'pp_pham' },
  { id: 'pp_isaure', name: 'Isaure', sprite: 'gen_pp_isaure', location: 'steel_pulse', x: 22.5, z: 23.4, faceTo: [24, 18], dialogue: 'pp_isaure' },
  { id: 'pp_clone', name: 'Le Clone 7', sprite: 'gen_pp_clone_gt', location: 'steel_pulse', x: 19.6, z: 23.2, faceTo: [14, 24], dialogue: 'pp_clone' },
  { id: 'pp_gaspard', name: 'Gaspard', sprite: 'gen_pp_gaspard', location: 'steel_pulse', x: 7, z: 22, faceTo: [12, 22], dialogue: 'pp_gaspard' },
  { id: 'pp_noor', name: 'Noor', sprite: 'gen_pp_noor', location: 'steel_pulse', x: 27, z: 31, faceTo: [24, 31], dialogue: 'pp_noor' },
  { id: 'pp_vasseur', name: 'Monsieur Vasseur', sprite: 'gen_pp_vasseur', location: 'steel_pulse', x: 34.5, z: 8.5, faceTo: [28, 10], dialogue: 'pp_vasseur' },
];
const D = (t1, t2) => ({ start: { text: t1, options: [ { label: 'Et sinon ?', next: 'b' }, { label: 'Au revoir.', next: 'end' } ] }, b: { text: t2, options: [ { label: 'Au revoir.', next: 'end' } ] } });
export const DIALOGUES_PULSE = {
  pp_maelle: D('Tu l’as vue hier, sur le feed ? Elle a regardé la caméra une demi-seconde de trop. Moi j’appelle ça un message.', 'Personne ne sait qui elle est vraiment. Et franchement, je préfère. Si on savait, elle serait comme nous.'),
  pp_dorian: D('Pack EXE, la clé chrome est vide, mais c’est la vraie. C’est écrit sur la boîte.', 'Le poster Error 404 part mieux que tout le reste. Les gens aiment bien qu’on leur dise qu’ils sont introuvables.'),
  pp_brisset: D('Implant, s’il vous plaît. Simple routine. Ici, tout est simple routine.', 'Ne restez pas sur la place trop longtemps, d’accord ?'),
  pp_pham: D('Assieds-toi de ce côté. La caméra du coin voit tout sauf mes casseroles.', 'Moi, la musique, je ne l’entends plus. Je ne remarque que quand elle s’arrête. Là, je regarde l’écran.'),
  pp_isaure: D('L’audience sync, c’est un signal. Il part de l’écran et les implants font le reste. Les mains suivent.', 'Tu crois qu’ils applaudissent parce qu’ils veulent ? Moi, ça fait trois ans que je ne pose plus la question.'),
  pp_clone: D('Bonsoir. Je suis un modèle de démonstration. On me pose ici pour que vous voyiez à quoi ressemble un modèle réussi.', 'Question non prévue. Je vous renvoie au refrain.'),
  pp_gaspard: D('Chaque semaine quelqu’un jure avoir trouvé qui elle est. Chaque semaine le feed passe à autre chose. Drôle de hasard.', 'Si un jour tu entends son vrai nom, garde-le pour toi. Les gens qui le disent trop fort ne reviennent plus sur la place.'),
  pp_noor: D('Pas d’implant, pas d’applaudissement. Du coup on me regarde. C’est bête, non ?', 'Si tu veux descendre sans passer devant la guérite, l’escalier de service ne ferme jamais vraiment.'),
  pp_vasseur: D('Je travaille juste là. Non, je ne sais pas ce qu’on y fait. Je sais seulement ce que je fais, moi.', 'L’écran ? C’est nous qui louons la place. Le groupe chante, nous on comptera les mains.'),
};
