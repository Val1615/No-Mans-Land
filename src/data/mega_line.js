// Mega-Line v2 (zone steel_megaline, 64 x 40 m) et terminus v2 (zone steel_terminus, 40 x 28 m) : refonte du 17/11/2026 sur les planches d'Ocre
// (nml-shots/concepts_megaline/NOTES.md). Plan, zones cotées, clés d'assets attendues : docs/villes/steel/quartiers/mega_line/MEGALINE_V2_IMPL.md.
// Ligne : z0 = nord (bâti, passerelle de service vers le terminus), z40 = sud (parvis, porte c_mega vers Center-Town). Terminus : z0 = sas, z28 = passerelle.
// [décision Valentin] terminus : portes massives pleines et fermées pour toujours, aucune vue sur le désert ; panneau vierge, phrase affichée par le code.
// Vibes (écran ouest) et Tron (écran est) : uniquement en image sur les écrans du quai, aucun nom civil. Violet réservé à la rame et aux écrans.
// Gabarits : chaque pièce a sa clé d'Ocre (attente { cle, h }) ; tant qu'elle n'est pas livrée, un volume à la bonne emprise et hauteur (b.ph, view.placeholder).
// Quai à +6 m : le moteur n'a qu'un niveau de marche par point ; loc.niveaux donne la hauteur du sol (quai, escaliers) au rendu, et les solides
// (garde-corps, bords de quai, côtés des escaliers) font que le quai ne s'atteint que par les deux escaliers (src/core/niveaux.js).
const LIGNE = { bg: '#070910', hemi: ['#b4a894', '#16141a', 1.2], sun: ['#f2b44a', 0.55], tint: '#c8beb0', actor: '#e0d8cc' }; // fer, laiton, béton, ambre ; plus de lumière violette générale
const FRET = { bg: '#0a0b0c', hemi: ['#b8c4cc', '#1a1c1e', 1.6], sun: ['#e8a040', 0.45], tint: '#b8bcc0', actor: '#d4d6d8' }; // palette froide, sodium ponctuel ; ni ciel ni sable
const VIOLET = '#8a3cff', CYAN = '#5fd3f0', AMBRE = '#f2b44a', ORANGE = '#ff8a2a', ROUGE = '#e03030', SODIUM = '#f0a040';
const B = (id, label, sprite, x, z, w, d, extra = {}) => ({ id, label, sprite, x, z, w, d, visitable: false, cue: null, named: !!label, ...extra });
const ENS = (id, sprite, x, z, y, extra = {}) => B(id, '', sprite, x - 0.1, z - 0.1, 0.2, 0.2, { y, solid: [], named: false, ...extra });
// gabarit en attente du module d'Ocre : clé = sprite attendu ; ph = volume de repli (h, y0, couleur, fenêtres, kind tablier|escalier|viaduc|portique)
const G = (id, cle, x, z, w, d, ph, extra = {}) => ({ id, label: '', sprite: cle, x, z, w, d, visitable: false, cue: null, named: false, tint: '#ffffff',
  attente: { cle, h: ph.h ?? ph.monte ?? ph.sol }, ph, ...extra, ...(extra.label ? { named: true } : {}) });
// fenêtres ambrées (face sud, et face est si de) : rangées tous les 3 m, une sur quatre éteinte (motif fixe, pas d'aléa)
const FEN = (w, h, seed = 0, de = 0) => ({
  lights: Array.from({ length: Math.max(1, Math.floor((w - 1) / 3)) }, (_, i) => Array.from({ length: Math.max(1, Math.floor((h - 1.2) / 3)) }, (_, k) => ((i * 7 + k * 5 + seed) % 4) ? { x: 1.5 + i * 3, y: 2.2 + k * 3, w: 1.4, h: 1.1, c: (i + k + seed) % 3 ? '#e8a13a' : '#c98a3a' } : null)).flat().filter(Boolean),
  lightsE: de ? Array.from({ length: Math.floor((de - 1) / 3) }, (_, i) => Array.from({ length: Math.max(1, Math.floor((h - 1.2) / 3)) }, (_, k) => ((i * 5 + k * 3 + seed) % 4) ? { z: 1.5 + i * 3, y: 2.2 + k * 3, w: 1.4, h: 1.1, c: '#e8a13a' } : null)).flat().filter(Boolean) : [] });
const FER = '#1b1d22', LAITON = '#3a332a', BETON = '#4a4844';
const PILES = [2, 14, 26, 38, 50, 62]; // centres des piles du viaduc (tous les 12 m), passage libre 10,4 m
const LAMPS = [[6, 33.6], [22, 33.6], [42, 33.6], [58, 33.6], [14, 20], [50, 20]];
const TERR = [[22.5, 24], [26, 27.5], [22.5, 29], [37.5, 24], [40.5, 27.5], [36.5, 29]];
const QUAI = 6; // plancher du quai (m)
// bords du quai et côtés des escaliers (solides) : le quai ne se rejoint que par les deux escaliers ; bande d'embarquement fermée par les barrières et le portique
const BORDS_QUAI = [{ x: 18, z: 13.6, w: 28, d: 0.4 }, { x: 17.6, z: 14, w: 0.4, d: 8 }, { x: 46, z: 14, w: 0.4, d: 8 }, { x: 21, z: 21.8, w: 22, d: 0.4 }];
const COTES_ESC = x => [{ x: x - 0.4, z: 22, w: 0.4, d: 9.5 }, { x: x + 3, z: 22, w: 0.4, d: 9.5 }];
export const BUILDINGS_MEGA = [
  // Lot 2 · bâti nord, passerelle de service (sortie nord vers le terminus)
  G('ml2_n1', 'ml_bati_n1_v2_3q', 0, 0, 24, 8, { h: 12, color: '#211f22', ...FEN(24, 12, 1) }),
  G('ml2_n2', 'ml_bati_n2_v2_3q', 24, 0, 20, 8, { h: 16, color: '#1e1d21', ...FEN(20, 16, 2) }),
  G('ml2_pass', 'ml_passerelle_nord_v2_3q', 44, 0, 0.4, 8, { h: 1.1, color: LAITON }),
  G('ml2_pass_e', 'ml_passerelle_nord_v2_3q', 47.6, 0, 0.4, 8, { h: 1.1, color: LAITON }, { repliDe: 'ml2_pass' }),
  G('ml2_n3', 'ml_bati_n3_v2_3q', 48, 0, 16, 8, { h: 10, color: '#221f20', ...FEN(16, 10, 3) }),
  // Lot 2 · ruelle de service (z8-14)
  G('ml2_benne0', 'ml_ruelle_benne_v2_3q', 5, 8.3, 2, 1.2, { h: 1.4, color: '#2c3328' }), G('ml2_benne1', 'ml_ruelle_benne_v2_3q', 53, 8.3, 2, 1.2, { h: 1.4, color: '#2c3328' }),
  G('ml2_caisses0', 'ml_ruelle_caisses_v2_3q', 19, 8.3, 1.6, 1.2, { h: 1.2, color: '#3a2e22' }), G('ml2_caisses1', 'ml_ruelle_caisses_v2_3q', 56, 12.2, 1.6, 1.2, { h: 1.2, color: '#3a2e22' }),
  // Lot 1 · viaduc (z10-14, sous-poutre 6 m, rails à 6,8 m), piles tous les 12 m, rame qui passe sans s'arrêter
  G('ml2_viaduc0', 'ml_viaduc_seg24_v2_3q', 0, 10, 24, 4, { kind: 'viaduc', y0: 6, dessus: 6.8, h: 6.8 }, { solid: [], etage: 1 }),
  G('ml2_viaduc1', 'ml_viaduc_seg24_v2_3q', 24, 10, 24, 4, { kind: 'viaduc', y0: 6, dessus: 6.8, h: 6.8 }, { solid: [], etage: 1 }),
  G('ml2_viaduc2', 'ml_viaduc_seg16_v2_3q', 48, 10, 16, 4, { kind: 'viaduc', y0: 6, dessus: 6.8, h: 6.8 }, { solid: [], etage: 1 }),
  ...PILES.map((cx, i) => G(`ml2_pile${i}`, 'ml_viaduc_pile_v2_3q', cx - 0.8, 11.2, 1.6, 1.6, { h: 6, color: '#17181c' })),
  // repli : l'ancienne rame (24 m, déjà livrée) défile tant que la rame 3 voitures (28 m) n'est pas livrée ; déplacée par le code, ne s'arrête pas
  B('ml_rame', '', 'ml_rame', 14, 10.5, 28, 3, { solid: [], named: false, y: 6.8, etage: 2, attente: { cle: 'ml_rame_3v_v2_3q', h: 3.6 }, defile: { dx: 110, passage: 10, periode: 40 } }),
  // Lot 2 · rez sous le quai (z14-20, sous le tablier ; galerie couverte z20-22 au pied des poteaux)
  G('ml2_tran', 'ml_echoppe_tran_v2_3q', 18, 14, 6, 6, { h: 5.4, color: '#2a1d1a', lights: [{ x: 1.6, y: 1.5, w: 2.2, h: 1.6, c: '#c9541e' }, { x: 4.4, y: 1.5, w: 2, h: 1.6, c: '#e8a13a' }] }, { solid: [], label: 'Nouilles de Mme Tran' }),
  G('ml2_cables', 'ml_echoppe_cables_v2_3q', 24, 14, 6, 6, { h: 5.4, color: '#1f2124', lights: [{ x: 3, y: 1.5, w: 4.4, h: 1.5, c: '#c98a3a' }] }, { solid: [], label: 'Câbles et réparations' }),
  G('ml2_hc', 'ml_facade_humancorp_v2_3q', 30, 14, 8, 6, { h: 5.4, color: '#1c2230', lights: [{ x: 1.5, y: 1.4, w: 2, h: 2.2, c: '#e8a13a' }, { x: 6.5, y: 1.4, w: 2, h: 2.2, c: '#e8a13a' }] }, { solid: [], label: 'Human Corp' }),
  G('ml2_atelier', 'ml_atelier_rivet_v2_3q', 38, 14, 8, 6, { h: 5.4, color: '#24211c', lights: [{ x: 2, y: 1.4, w: 2.6, h: 1.4, c: '#e8a13a' }, { x: 6, y: 1.3, w: 1.6, h: 2.2, c: '#c98a3a' }] }, { solid: [], label: 'Atelier de Rivet' }),
  ENS('ml_e_hc', 'ml_ens_human_corp', 34, 20.1, 1.8), // logo Human Corp (triangle, sans lettrage) qui respire, sous la galerie
  // Lot 1 · quai à +6 m (x18-46, z14-22) : tablier, bande d'embarquement (z14-17,5, ligne jaune z15,2), barrières, portique à implant, deux escaliers vers la rue
  G('ml2_quai', 'ml_quai_tablier_v2_3q', 18, 14, 28, 8, { kind: 'tablier', sol: QUAI, ep: 0.6, h: QUAI + 1.1, ligne: 15.2, bande: [14, 17.5], pas: 4,
    gc: [[0, 0.2, 0.06, 8], [27.94, 0.2, 28, 8], [3, 7.94, 25, 8]] }, { solid: BORDS_QUAI, etage: 1 }),
  G('ml2_esc_o', 'ml_escalier_v2_3q', 18, 22, 3, 10, { kind: 'escalier', monte: QUAI }, { solid: COTES_ESC(18), etage: 1 }),
  G('ml2_esc_e', 'ml_escalier_v2_3q', 43, 22, 3, 10, { kind: 'escalier', monte: QUAI }, { solid: COTES_ESC(43), etage: 1 }),
  G('ml2_barr_o', 'ml_quai_barriere_v2_3q', 18.4, 17.35, 12.6, 0.3, { h: 1.1, y0: QUAI, color: LAITON }, { y: QUAI, solid: [{ x: 18, z: 17.35, w: 13, d: 0.3 }], etage: 2 }),
  G('ml2_barr_e', 'ml_quai_barriere_v2_3q', 32.6, 17.35, 12.6, 0.3, { h: 1.1, y0: QUAI, color: LAITON }, { y: QUAI, solid: [{ x: 32.6, z: 17.35, w: 13.4, d: 0.3 }], etage: 2 }),
  B('ml_portique_implant', 'Portique à implant', 'ml_portique_implant', 31, 17, 1.6, 1, { y: QUAI, etage: 2, solid: [{ x: 31, z: 17, w: 1.6, d: 1 }] }), // éteint ; planches jouées une fois au passage (main.js)
  B('ml_tableau', 'Tableau des départs', 'ml_tableau', 26.4, 19.6, 2.4, 0.4, { y: QUAI, etage: 2 }), ENS('ml_e_horaires', 'ml_ens_horaires', 27.6, 20.2, QUAI + 2.2, { etage: 3 }),
  B('ml_borne', 'Borne de billets', 'ml_borne', 34.4, 18.4, 0.8, 0.6, { y: QUAI, etage: 2 }),
  B('ml_banc0', '', 'ml_banc', 24, 19.2, 2, 0.6, { named: false, y: QUAI, etage: 2 }), B('ml_banc1', '', 'ml_banc', 37, 20.4, 2, 0.6, { named: false, y: QUAI, etage: 2 }),
  B('ml_poub0', '', 'ml_poubelle', 29.6, 20.6, 0.6, 0.6, { named: false, y: QUAI, etage: 2 }), B('ml_poub1', '', 'ml_poubelle', 41, 18.2, 0.6, 0.6, { named: false, y: QUAI, etage: 2 }),
  // Lot 1 · écrans du quai, en hauteur sur le flanc sud du viaduc : Vibes à l'ouest, Tron à l'est (planches déjà livrées, 5,12 m)
  G('ml2_ecran_o', 'ml_ecran_cadre_v2_3q', 19.9, 13.6, 5.2, 0.4, { h: 3, y0: 7.2, color: '#141418' }, { y: 7.2, solid: [], etage: 2 }),
  G('ml2_ecran_e', 'ml_ecran_cadre_v2_3q', 36.9, 13.6, 5.2, 0.4, { h: 3, y0: 7.2, color: '#141418' }, { y: 7.2, solid: [], etage: 2 }),
  ENS('ml_e_vibes', 'ml_ens_ecran_vibes', 22.5, 13.95, 7.26, { groupe: 'ecrans_quai', ph: 0, etage: 3 }), ENS('ml_e_tron', 'ml_ens_ecran_tron', 39.5, 13.95, 7.26, { groupe: 'ecrans_quai', ph: 0, etage: 3 }),
  // Lot 2 · rue piétonne et terrasses (x21-43, z22-32), atelier de Rivet : établi et café froid
  ...TERR.map(([x, z], i) => G(`ml2_terr${i}`, 'ml_terrasse_v2_3q', x, z, 2, 2, { h: 1, color: '#3a2e24' })),
  G('ml2_etabli', 'ml_etabli_v2_3q', 39.2, 22.5, 1.6, 0.6, { h: 0.9, color: '#4a3a28' }),
  B('ml_cafe_froid', '', 'ml_cafe_froid', 39.9, 22.7, 0.2, 0.2, { solid: [], named: false, y: 0.9 }), // café froid de Rivet, sur l'établi (hauteur de plan de travail)
  // Lot 2 · bâti ouest et est (z14-32), rez actifs sur les rues latérales (x10-18, x46-54)
  G('ml2_w', 'ml_bati_w_v2_3q', 0, 14, 10, 18, { h: 12, color: '#1f1e22', ...FEN(10, 12, 4, 18) }),
  G('ml2_e', 'ml_bati_e_v2_3q', 54, 14, 10, 18, { h: 10, color: '#201e21', ...FEN(10, 10, 5, 18) }),
  // parvis sud (z32-40) : lampadaires à ampoule visible, bancs
  ...LAMPS.map(([x, z], i) => B(`ml_lamp${i}`, '', 'ml_lampadaire', x - 0.3, z - 0.3, 0.6, 0.6, { named: false })),
  B('ml_banc2', '', 'ml_banc', 11, 36.6, 2, 0.6, { named: false }), B('ml_banc3', '', 'ml_banc', 51, 36.6, 2, 0.6, { named: false }),
];
const CONT = [[24.5, 9.5, 2], [30.5, 9.5, 2], [24.5, 13, 3], [30.5, 13, 2], [24.5, 16.5, 2], [30.5, 16.5, 3]]; // 3 rangées de 2 piles (allées de 1 m), 2 ou 3 niveaux
export const BUILDINGS_TERMINUS = [
  // Lot 3 · voûte (fond), mur et portes du sas (z0-2) : pleines, fermées, sans lumière de dehors
  G('tm2_voute', 'ml_tm_voute_v2_3q', 0, 0, 40, 2, { h: 18, color: '#33373b' }, { solid: [], fond: true }),
  G('tm2_mur_o', 'ml_tm_sas_mur_o_v2_3q', 0, 0, 10, 2, { h: 13, color: '#585d62' }),
  B('ml_sas', 'Les portes du sas', 'ml_tm_sas_portes_v2_3q', 10, 0, 20, 2, { attente: { cle: 'ml_tm_sas_portes_v2_3q', h: 13 }, tint: '#ffffff',
    ph: { h: 13, color: '#4c545c', lights: [{ x: 10, y: 6.5, w: 0.14, h: 13, c: '#121416' }, { x: 10, y: 0.7, w: 19.6, h: 0.6, c: '#b8962a' }, { x: 10, y: 12.2, w: 19.6, h: 0.4, c: '#b8962a' }] } }),
  G('tm2_mur_e', 'ml_tm_sas_mur_e_v2_3q', 30, 0, 10, 2, { h: 13, color: '#585d62' }),
  ENS('ml_e_sas0', 'ml_ens_sas', 13.5, 2.15, 12.4, { groupe: 'sas', ph: 0 }), ENS('ml_e_sas1', 'ml_ens_sas', 26.5, 2.15, 12.4, { groupe: 'sas', ph: 2 }), // lampes d'alerte rouges qui clignotent (planche existante)
  // voie, heurtoir, quai à l'est de la voie (+1,1 m), voiture d'accès à la rame
  G('tm2_voie', 'ml_tm_voie_v2_3q', 14, 3.4, 3, 24.6, { h: 0.2, color: '#2b2a28' }, { solid: [], fond: true }),
  G('tm2_heurtoir', 'ml_tm_heurtoir_v2_3q', 14, 2, 3, 1.4, { h: 1.2, color: '#8a2a24' }),
  G('tm2_quai', 'ml_tm_quai_v2_3q', 17, 3, 6, 21, { h: 1.1, color: '#55585a' }, { solid: [], etage: 1 }),
  G('tm2_voiture', 'ml_tm_voiture_v2_3q', 14, 20, 3, 8, { h: 3.6, color: '#34383d', lightsE: [{ z: 5, y: 1.3, w: 1.2, h: 2, c: '#c9541e' }] }),
  B('ml_panneau', 'Dernier arrêt avant No Man\u2019s Land', 'ml_panneau_terminus', 18.5, 3.4, 3, 0.5, { sign: true, y: 1.1, etage: 2 }), // phrase affichée par le code (libellé), panneau vierge
  // bureau de la gare de fret et son dock (allée de 3 m jusqu'à la voie), hangar, locaux techniques
  G('ml_bureau', 'ml_tm_bureau_fret_v2_3q', 2, 9, 7, 5, { h: 4, color: '#535960', lights: [{ x: 2.2, y: 2, w: 1.8, h: 1.1, c: '#e8a13a' }, { x: 5.4, y: 1.1, w: 1.2, h: 2.1, c: '#c98a3a' }] }, { label: 'Bureau de la gare de fret' }),
  G('tm2_dock', 'ml_tm_dock_v2_3q', 9, 9, 2, 5, { h: 1.2, color: '#44474a' }),
  G('tm2_hangar', 'ml_tm_hangar_v2_3q', 0, 2, 9, 5, { h: 6, color: '#50565b', roof: 'pitched', roofColor: '#3a3f43', lights: [{ x: 6.5, y: 1.6, w: 3, h: 3, c: '#c98a3a' }] }),
  G('tm2_loc_so', 'ml_tm_locaux_so_v2_3q', 0, 17, 8, 11, { h: 5, color: '#4a5055', lights: [{ x: 2, y: 2.2, w: 1.4, h: 1, c: '#e8a13a' }], lightsE: [{ z: 3, y: 1.2, w: 1.1, h: 2.1, c: '#c98a3a' }] }),
  G('tm2_loc_e', 'ml_tm_locaux_e_v2_3q', 37, 2, 3, 26, { h: 6, color: '#4a5055', lights: [{ x: 1.5, y: 2.2, w: 1.4, h: 1, c: '#e8a13a' }] }),
  // portique de levage jaune (13 x 13 m, seuls les pieds sont pleins) et cour de conteneurs (piles de 2 : ml_conteneurs existant ; piles de 3 : gabarit)
  B('ml_portique', 'Portique de levage', 'ml_tm_portique_levage_v2_3q', 24, 8, 13, 13, { attente: { cle: 'ml_tm_portique_levage_v2_3q', h: 13 }, tint: '#ffffff', etage: 1, ph: { kind: 'portique', h: 13, color: '#c9a227' },
    solid: [{ x: 24, z: 8, w: 1, d: 1 }, { x: 36, z: 8, w: 1, d: 1 }, { x: 24, z: 20, w: 1, d: 1 }, { x: 36, z: 20, w: 1, d: 1 }] }),
  ...CONT.map(([x, z, n], i) => n === 2 ? B(`ml_cont${i}`, '', 'ml_conteneurs', x, z, 6, 2.5, { named: false })
    : G(`ml_cont${i}`, 'ml_tm_conteneurs_x3_v2_3q', x, z, 6, 2.5, { h: 7.8, color: i % 2 ? '#2a3f66' : '#7a2a26' })),
  ENS('ml_e_gyro0', 'ml_ens_gyrophare', 24.5, 8.6, 13.1, { groupe: 'gyrophares', ph: 0, etage: 2 }), ENS('ml_e_gyro1', 'ml_ens_gyrophare', 36.5, 8.6, 13.1, { groupe: 'gyrophares', ph: 2, etage: 2 }),
  // passerelle de service (arrivée de la ligne, sud-ouest)
  G('tm2_pass', 'ml_tm_passerelle_v2_3q', 8, 24, 0.3, 4, { h: 1.1, color: '#3d4246' }), G('tm2_pass_e', 'ml_tm_passerelle_v2_3q', 11.7, 24, 0.3, 4, { h: 1.1, color: '#3d4246' }, { repliDe: 'tm2_pass' }),
];
export const CLOSED_MEGA = {
  ml_portique_implant: 'Le portique à implant. Deux piliers, deux volets vitrés, un lecteur éteint. Il lit la nuque des gens.',
  ml2_viaduc1: 'Le viaduc de fer noir. Les piles ruissellent ; le fer transpire.',
  ml2_quai: 'Le quai, six mètres au-dessus de la rue. On y monte par les escaliers ; la rame ne s\u2019arrête pas pour qui n\u2019a pas de billet.',
  ml_tableau: 'Le tableau des départs, en pictogrammes. Une ligne change. Aucune ne dit « terminus ».',
  ml_borne: 'La borne de billets reconnaît les bracelets, et les visages.',
  ml_sas: 'Les portes du sas. Pleines, si hautes qu\u2019on les prend pour un mur. Fermées. Elles ne s\u2019ouvriront pas.',
  ml_panneau: '« Dernier arrêt avant No Man\u2019s Land. »',
  ml_bureau: 'Le bureau de la gare de fret. Une fenêtre ambrée, des bordereaux.',
  ml_portique: 'Le portique de levage jaune. Les conteneurs vont et viennent, toujours vers l\u2019intérieur.',
};
export const LOCATIONS_MEGA = {
  steel_megaline: { id: 'steel_megaline', name: 'Steel-Megalopolis · Mega-Line', kind: 'exterior', size: { w: 64, d: 40 }, light: LIGNE, plan: 2,
    gabaritsSeuls: true, // lots 1 et 2 d'Ocre (structure, rez et bâti) publiés pendant la pose du plan (ef04794, a203f03) : câblé au lot suivant, après lecture de sa fiche de poses (ASSETS.md)
    cadre: { desktop: { x: [21, 43], z: [16, 24] }, mobile: { x: [8, 56], z: [10, 30] } }, // le cadre reste sur le lieu (pas de vide au sud à l'arrivée)
    ground: { base: '#12121a', skin: 'g_ml_pave', tileM: 4, clean: true },
    // quai à +6 m et escaliers (montée vers le nord) : hauteur de sol au rendu ; l'accès est fait par les solides (BORDS_QUAI, COTES_ESC)
    niveaux: [{ x: 18, z: 14, w: 28, d: 8, y: QUAI }, { x: 18, z: 22, w: 3, d: 10, y0: QUAI, y1: 0, axe: 'z' }, { x: 43, z: 22, w: 3, d: 10, y0: QUAI, y1: 0, axe: 'z' }],
    buildings: BUILDINGS_MEGA, props: [],
    glows: [ ...LAMPS.map(([x, z]) => ({ x, z: z + 0.6, rx: 2.6, rz: 1.9, color: AMBRE, i: 0.55, flicker: true })), // lampadaires (code)
      { x: 22.5, z: 15.6, rx: 3, rz: 1.4, color: VIOLET, i: 0.6, flicker: true, sol: true }, { x: 39.5, z: 15.6, rx: 3, rz: 1.4, color: CYAN, i: 0.55, flicker: true, sol: true }, // reflets des écrans sur le quai
      { x: 21, z: 23.2, rx: 3, rz: 1.2, color: '#e0603a', i: 0.5, flicker: true }, { x: 27, z: 23, rx: 2.6, rz: 1, color: AMBRE, i: 0.35 }, { x: 34, z: 23, rx: 3, rz: 1.1, color: '#6aa8e0', i: 0.3 },
      { x: 42, z: 23.2, rx: 2.6, rz: 1.1, color: AMBRE, i: 0.5 }, { x: 32, z: 19.6, rx: 12, rz: 2, color: AMBRE, i: 0.18, sol: true }, { x: 31.8, z: 18.3, rx: 1.4, rz: 0.8, color: AMBRE, i: 0.5, sol: true } ],
    extras: [ ...[[20.5, 15.8], [26.5, 16.2], [29, 15.6], [36, 15.7], [43.5, 16.1]].map(([x, z], i) => ({ sprite: i % 2 ? 'gen_ml_foule_b' : 'gen_ml_foule_a', x, z, face: i % 2 ? 1 : -1, role: 'voyageur' })), // bande d'embarquement
      ...[[30.6, 21], [14.4, 26], [25.2, 30.6], [38.8, 31], [8, 36.4], [55, 37.2], [24.6, 26.6], [41.4, 25.4]].map(([x, z], i) => ({ sprite: i % 2 ? 'gen_ml_foule_a' : 'gen_ml_foule_b', x, z, face: i % 2 ? -1 : 1, role: 'passant', dense: i > 5 })) ],
    walkers: [ { sprite: 'gen_ml_foule_a', path: [[32, 36], [19.5, 33], [19.5, 22.6], [30, 19.6], [44.5, 22.6], [44.5, 33]], speed: 0.9, t0: 4 }, // monte l'escalier ouest, traverse le quai, redescend à l'est
      { sprite: 'gen_ml_foule_b', path: [[3, 37.5], [61, 37.5]], speed: 0.8, t0: 10 }, { sprite: 'gen_ml_foule_a', path: [[13.5, 33], [13.5, 9.2], [50, 9.2], [50.5, 33]], speed: 0.85, t0: 30 } ],
    spawn: { player: { x: 32, z: 38.2 }, companion: { x: 33, z: 38.2 } }, city: 'steel',
    arrive: { from: 'steel_center', text: 'La Mega-Line. Le viaduc de fer noir passe à six mètres au-dessus de la rue ; la rame violette glisse sans s\u2019arrêter. Sur le quai, Vibes et Tron passent en boucle.' } },
  steel_terminus: { id: 'steel_terminus', name: 'Steel-Megalopolis · Terminus de fret', kind: 'exterior', size: { w: 40, d: 28 }, light: FRET, plan: 2,
    cadre: { desktop: { x: [17, 23], z: [6, 16] }, mobile: { x: [8, 32], z: [4, 22] } }, // z min bas : on voit les portes du sas (13 m) en s'en approchant
    ground: { base: '#141414', skin: 'g_ml_fret', tileM: 4, clean: true },
    niveaux: [{ x: 17, z: 3, w: 6, d: 19, y: 1.1 }, { x: 17, z: 22, w: 6, d: 2, y0: 1.1, y1: 0, axe: 'z' }, { x: 16.4, z: 3, w: 0.6, d: 19, y0: 0, y1: 1.1, axe: 'x' }, { x: 23, z: 3, w: 0.6, d: 19, y0: 1.1, y1: 0, axe: 'x' }], // quai bas (+1,1 m) : bords en pente douce
    buildings: BUILDINGS_TERMINUS, props: [],
    glows: [ { x: 20, z: 2.8, rx: 11, rz: 1.6, color: ROUGE, i: 0.4, flicker: true }, // lampes d'alerte du sas : reflet rouge au sol (code)
      { x: 13.5, y: 12.6, z: 2.3, r: 1.1, color: ROUGE, i: 0.75, flicker: true }, { x: 26.5, y: 12.6, z: 2.3, r: 1.1, color: ROUGE, i: 0.75, flicker: true },
      { x: 24.5, y: 13.4, z: 8.8, r: 0.9, color: ORANGE, i: 0.7, flicker: true }, { x: 36.5, y: 13.4, z: 8.8, r: 0.9, color: ORANGE, i: 0.7, flicker: true }, // gyrophares
      { x: 8, y: 13, z: 14, r: 1.2, color: SODIUM, i: 0.6 }, { x: 20, y: 15, z: 12, r: 1.2, color: SODIUM, i: 0.6 }, { x: 31, y: 15, z: 22, r: 1.2, color: SODIUM, i: 0.55 }, // suspensions sodium
      { x: 8, z: 14.6, rx: 4, rz: 2, color: SODIUM, i: 0.3 }, { x: 20, z: 12, rx: 4, rz: 3, color: SODIUM, i: 0.22, sol: true }, { x: 30.5, z: 22, rx: 5, rz: 2, color: SODIUM, i: 0.25 },
      { x: 18.4, z: 25, rx: 1.8, rz: 1.2, color: ORANGE, i: 0.5 }, { x: 10, z: 14.4, rx: 2.4, rz: 1.2, color: AMBRE, i: 0.45 } ],
    extras: [ { sprite: 'gen_ml_foule_a', x: 12.4, z: 12.6, face: -1, role: 'docker' }, { sprite: 'gen_ml_foule_b', x: 21, z: 16, face: 1, role: 'voyageur' }, { sprite: 'gen_ml_foule_a', x: 27.6, z: 22.4, face: 1, role: 'docker' } ],
    walkers: [ { sprite: 'gen_ml_foule_b', path: [[11.6, 15.4], [13.4, 15.4], [13.4, 7.8], [11.6, 7.8]], speed: 0.7, t0: 3 } ],
    spawn: { player: { x: 10, z: 26.4 }, companion: { x: 11, z: 26.4 } }, city: 'steel',
    arrive: { from: 'steel_megaline', text: 'Le terminus de fret, sous une voûte de béton. Plus d\u2019écran, plus de pub. Au bout de la voie, des portes si grandes qu\u2019on les prend d\u2019abord pour un mur.' } },
};
const J = (id, loc, ox, oz, tx, tz, to, label, conditions = []) => ({ id, location: loc, junction: true, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: { doorId: to }, conditions });
// [décision Valentin] rame jouable : billet lié à l'implant. Augmenté et cyborg embarquent ; humain et mutant refusés (conseil : la passerelle), sauf avec le Pique-Puce.
// Espèce : state.character.race, et les drapeaux race_* posés à la création (character.js, raceFlags) ; on lit les drapeaux, comme la douane.
// Valeurs non canon (fiche d'Ocre, MEGA_LINE.md) : proposé, non validé.
export const PIQUE_PUCE_PRIX = 600;              // proposé, non validé : prix chez Fusible, en crédits (actif)
export const PIQUE_PUCE_ZONES = ['steel_megaline', 'steel_terminus']; // proposé, non validé : ne sert que sur la Mega-Line (actif)
export const PIQUE_PUCE_P_REPERE = 0;            // proposé, non validé : 0.1 (1 sur 10 d'être repéré) ; désactivé par défaut
export const PIQUE_PUCE_P_GRILLE = 0;            // proposé, non validé : 0.05 (1 sur 20 de griller) ; désactivé par défaut
export const ITEMS_MEGA = { pirate_implant: { name: 'Pique-Puce', icon: 'steel/mega_line/icone_pique_puce_64.webp', icon128: 'steel/mega_line/icone_pique_puce_128.webp',
  desc: 'Un boîtier rafistolé au ruban adhésif, un écran fendu et une pastille de contact au bout d\u2019un fil. On le colle contre la peau, il fait croire au portique qu\u2019il y a un implant. Ça pique un peu.' } };
export const aImplant = s => !!(s.flags.race_augmente || s.flags.race_cyborg);
export const aBillet = s => aImplant(s) || (!!s.player.inv?.pirate_implant && PIQUE_PUCE_ZONES.includes(s.location));
export const VALIDATION = s => aImplant(s)
  ? 'Ton implant vibre une fois. « Titre validé. Bon voyage sur la Mega-Line. »'
  : (s.flags.race_mutant ? 'Le Pique-Puce te mord la nuque, une décharge sèche. ' : 'Le Pique-Puce grésille contre ta nuque. ') + '« Titre… validé. Bon voyage. » Personne ne regarde.';
// Refus du portique (fiche d'Ocre) : communes + catégorie, tirées au hasard ; 3 insistances de suite : Kessler se retourne
export const REFUS = { commun: ['« Aucun implant détecté. Accès refusé. »', '« Lecture impossible. Veuillez présenter un implant valide. »', '« Titre de transport absent. Le personnel est informé. »', '« Accès refusé. La passerelle piétonne est à votre disposition. »'],
  humain: ['« Profil non augmenté. Ce service ne vous est pas destiné. »', '« Aucun implant. Pensez à consulter un centre Human Corp. »', '« Erreur : passager organique. »'],
  mutant: ['« Signature biologique non conforme. Accès refusé. »', '« Profil non reconnu. Merci de vous éloigner du portique. »', '« Lecture interrompue. Anomalie corporelle détectée. »'],
  insiste: ['« Tentatives répétées enregistrées. »', '« Merci de libérer le passage. »'] };
export const CONSEIL = 'Sans implant, la rame n\u2019est pas pour toi : pour le terminus, prends la passerelle de service, au bout du viaduc.';
const AU_PORTIQUE = [{ test: s => !!s.flags.ml_valide, reason: 'billet', text: '' }]; // le portique (main.js) valide puis relance le passage
const BILLET_RETOUR = [{ test: aBillet, reason: 'billet_retour', text: 'Le lecteur du quai reste rouge. Pour la ligne, la passerelle de service.' }];
export const DOORS_MEGA = [
  J('ml_rame_quai', 'steel_megaline', 31.8, 17.5, 31.8, 18.6, 'tm_rame_quai', 'Portique : monter dans la rame (terminus)', AU_PORTIQUE), // sur le quai (+6 m), devant le portique
  J('tm_rame_quai', 'steel_terminus', 17, 25.2, 18.2, 25.2, 'ml_rame_quai', 'Monter dans la rame (vers la ligne)', BILLET_RETOUR), // porte est de la voiture d'accès
  J('c_mega', 'steel_center', 0, 50, 1, 50, 'ml_sud', 'Mega-Line', [], { labelPos: [3, 50] }), // Center-Town v2 : bout ouest du trottoir nord de l'av. E-O, au pied du viaduc
  J('ml_sud', 'steel_megaline', 32, 40, 32, 39, 'c_mega', 'Vers Center-Town'), // centre du bord sud (parvis)
  J('ml_passerelle', 'steel_megaline', 46, 0, 46, 1, 'tm_sud', 'Passerelle de service (terminus)'), // bord nord, entre N2 et N3
  J('tm_sud', 'steel_terminus', 10, 28, 10, 27, 'ml_passerelle', 'Passerelle de service (vers la ligne)'), // sud-ouest du terminus
];
export const NPCS_MEGA = [ // aucun n'est Vibes ni Tron ; places : planche 01 (ligne) et 02 (terminus) d'Ocre
  { id: 'ml_navetteur', name: 'Anselme Roque', sprite: 'gen_ml_navetteur', location: 'steel_megaline', x: 44.6, z: 19.4, faceTo: [40, 16], dialogue: 'ml_navetteur' }, // bout du quai (est)
  { id: 'ml_controleuse', name: 'Sabine', sprite: 'gen_ml_controleuse', location: 'steel_megaline', x: 22, z: 20.8, faceTo: [19.5, 23], dialogue: 'ml_controleuse' }, // haut de l'escalier ouest
  { id: 'ml_etudiante', name: 'Lou', sprite: 'gen_ml_etudiante', location: 'steel_megaline', x: 25, z: 20.1, faceTo: [25, 24], dialogue: 'ml_etudiante' }, // sur le banc du quai
  { id: 'ml_entretien', name: 'Marcel', sprite: 'gen_ml_entretien', location: 'steel_megaline', x: 32, z: 11.8, faceTo: [26, 12], dialogue: 'ml_entretien' }, // ruelle, sous le viaduc
  { id: 'ml_nouilles', name: 'Mme Tran', sprite: 'gen_ml_nouilles', location: 'steel_megaline', x: 22.6, z: 22.9, faceTo: [22.6, 26], dialogue: 'ml_nouilles' }, // devant son échoppe, sous le quai
  { id: 'ml_vigile', name: 'Kessler', sprite: 'gen_ml_vigile', location: 'steel_megaline', x: 33.6, z: 18.7, faceTo: [31.8, 18.6], dialogue: 'ml_vigile' }, // au portique
  { id: 'ml_pancarte', name: 'Noé', sprite: 'gen_ml_pancarte', location: 'steel_megaline', x: 42, z: 33, faceTo: [36, 34], dialogue: 'ml_pancarte' }, // pied de l'escalier est
  { id: 'ml_fan', name: 'Yuna', sprite: 'gen_ml_fan', location: 'steel_megaline', x: 22.5, z: 18.5, faceTo: [22.5, 14], dialogue: 'ml_fan' }, // sous l'écran de Vibes
  { id: 'ml_rivet', name: 'Rivet', sprite: 'gen_ml_rivet', location: 'steel_megaline', x: 41.2, z: 23.1, faceTo: [39.9, 22.7], dialogue: 'ml_rivet' }, // caméo : devant son atelier, sous le quai
  { id: 'ml_regie', name: 'Régie', sprite: 'gen_ml_regie', location: 'steel_terminus', x: 18.6, z: 5.6, faceTo: [15, 5.6], dialogue: 'ml_regie' }, // caméo : quai, côté sas, face à la voie
  { id: 'ml_cheffe', name: 'Odile Ferraz', sprite: 'gen_ml_cheffe_fret', location: 'steel_terminus', x: 6.5, z: 15.4, faceTo: [10, 17], dialogue: 'ml_cheffe' }, // devant le bureau de fret
  { id: 'ml_docker', name: 'Bruno', sprite: 'gen_ml_docker', location: 'steel_terminus', x: 30.5, z: 22.2, faceTo: [30.5, 18], dialogue: 'ml_docker' }, // au pied du portique, au sud
];
const D = (t1, t2) => ({ start: { text: t1, options: [ { label: 'Et sinon ?', next: 'b' }, { label: 'Au revoir.', next: 'end' } ] }, b: { text: t2, options: [ { label: 'Au revoir.', next: 'end' } ] } });
const D3 = (a, b, c) => ({ start: { text: a, options: [ { label: 'Et sinon ?', next: 'b' }, { label: 'Au revoir.', next: 'end' } ] }, b: { text: b, options: [ { label: 'Et sinon ?', next: 'c' }, { label: 'Au revoir.', next: 'end' } ] }, c: { text: c, options: [ { label: 'Au revoir.', next: 'end' } ] } });
export const DIALOGUES_MEGA = {
  ml_rivet: D3('Ça fonctionne ? Bien. Maintenant, voyons comment ça casse.', 'Si la rame t\u2019a refusé, c\u2019est le portique. Si elle t\u2019a accepté, c\u2019est aussi le portique. Moi, je répare.', 'Le café est froid. Il l\u2019est toujours. Ne me demande pas pourquoi, j\u2019ai arrêté de déboguer ça.'),
  ml_regie: D3('Dernier arrêt. Au-delà, ce ne sont plus mes horaires.', 'Je sais qui monte, qui descend, et qui n\u2019aurait pas dû. Toi, je n\u2019ai pas encore décidé.', 'Ces portes ne s\u2019ouvrent pas. Enfin, pas pour toi. Pas encore.'),
  ml_navetteur: D('Trente-huit minutes de trajet, tous les jours. J\u2019ai fini par connaître les écrans mieux que mes enfants.', 'La rame n\u2019est jamais en retard. C\u2019est nous qui sommes en avance, d\u2019après eux.'),
  ml_controleuse: D('Billet, s\u2019il vous plaît. Ou votre bracelet. Ou votre visage, la borne sait faire.', 'Le terminus ? Il n\u2019y a rien là-bas, que du fret. Personne n\u2019achète de billet pour le terminus.'),
  ml_etudiante: D('Je révise dans la rame. C\u2019est le seul endroit où le réseau me laisse tranquille.', 'Le prof dit que la ligne allait jusqu\u2019au désert, avant. Maintenant elle s\u2019arrête contre une porte.'),
  ml_entretien: D('Ça goutte du viaduc toute l\u2019année. Il ne pleut jamais, ici, mais le fer transpire.', 'Au terminus, on nettoie les portes une fois par mois. Elles n\u2019ont pas bougé depuis que je travaille.'),
  ml_nouilles: D('Un bol avant la rame, un bol après. Entre les deux, on attend.', 'Mon mari conduisait le fret. Il disait que derrière la porte, ça sent le sable. Je ne sais pas comment il savait.'),
  ml_vigile: D('Circulez. Le quai est fait pour attendre, pas pour rester.', 'Vous avez pris les escaliers trois fois. La borne aime bien qu\u2019on prenne la rame.'),
  ml_pancarte: D('Je n\u2019écris rien dessus. Quand j\u2019écrivais, on me l\u2019enlevait.', 'Tout le monde sait ce qu\u2019il y a derrière la dernière porte. Personne n\u2019a le droit de le dire.'),
  ml_fan: D('Je filme l\u2019écran pour mon fil. Oui, je sais, c\u2019est déjà une vidéo.', 'Tron bégaie toujours au même endroit. Je crois que c\u2019est fait exprès.'),
  ml_cheffe: D('Ici on charge, on décharge, on signe. Les portes, ce n\u2019est pas mon service.', 'Le panneau, c\u2019est la seule blague qu\u2019ils aient laissée. Dernier arrêt. Comme si on pouvait aller plus loin.'),
  ml_docker: D('Les conteneurs arrivent pleins de l\u2019intérieur et repartent vers l\u2019intérieur. Rien ne vient de dehors. Officiellement.', 'Pose ta main sur la porte, un jour de grand vent. Tu sentiras qu\u2019elle tremble.'),
};
