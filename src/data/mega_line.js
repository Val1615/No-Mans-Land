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
const TERR = [[22, 24], [26, 27.5], [30, 24], [34, 28], [37.5, 24], [40.5, 28]]; // fiche de poses d'Ocre (lot 2)
const QUAI = 6; // plancher du quai (m)
// bords du quai (solides) : le quai ne se rejoint que par les deux escaliers ; bande d'embarquement fermée par les barrières et le portique
const BORDS_QUAI = [{ x: 18, z: 13.6, w: 28, d: 0.4 }, { x: 17.6, z: 14, w: 0.4, d: 8 }, { x: 46, z: 14, w: 0.4, d: 8 }, { x: 21, z: 21.8, w: 22, d: 0.4 }];
// côtés des escaliers : limons de la fiche d'Ocre (0,15 m), passage libre 2,7 m
const COTES_ESC = x => [{ x, z: 22, w: 0.15, d: 10 }, { x: x + 2.85, z: 22, w: 0.15, d: 10 }];
// Poses des lots 1 (ef04794) et 2 (a203f03) d'Ocre, d'après ses fiches (docs/villes/steel/quartiers/mega_line/ASSETS.md) : sprites à l'échelle 1,
// ancre au coin avant sud-est, base_y -> y. Ordre de dessin : tri du peintre par emprise + étage (rez 0 < viaduc et tablier 1 < rame et ce qui
// est posé sur le quai 2 < poutres _avant du viaduc 3). Le rez sous le tablier n'est pas praticable (un seul niveau de marche : le quai à +6).
export const BUILDINGS_MEGA = [
  // Lot 2 · bâti nord, passerelle de service (sortie nord vers le terminus)
  B('ml_n1', '', 'ml_bati_n1_v2_3q', 0, 0, 24, 8, { named: false, solid: [{ x: 0, z: 0, w: 24, d: 8 }] }),
  B('ml_n2', '', 'ml_bati_n2_v2_3q', 24, 0, 20, 8, { named: false, solid: [{ x: 24, z: 0, w: 20, d: 8 }] }),
  B('ml_pass_n', '', 'ml_passerelle_nord_v2_3q', 44, 0, 4, 8, { named: false, solid: [{ x: 44, z: 0, w: 0.3, d: 8 }, { x: 47.7, z: 0, w: 0.3, d: 8 }, { x: 44.2, z: 6.4, w: 0.4, d: 0.6 }] }), // libre x44,3-47,7
  B('ml_n3', '', 'ml_bati_n3_v2_3q', 48, 0, 16, 8, { named: false, solid: [{ x: 48, z: 0, w: 16, d: 8 }] }),
  // Lot 2 · ruelle de service (z8-10) et pied de l'escalier ouest
  ...[[3, 8.4], [37, 8.4]].map(([x, z], i) => B('ml_benne' + i, '', 'ml_ruelle_benne_v2_3q', x, z, 2, 1.2, { named: false, solid: [{ x, z, w: 2, d: 1.2 }] })),
  ...[[5.6, 8.6], [52, 8.6], [16.5, 30.5]].map(([x, z], i) => B('ml_caisses' + i, '', 'ml_ruelle_caisses_v2_3q', x, z, 1.6, 1.2, { named: false, solid: [{ x, z, w: 1.6, d: 1.2 }] })),
  // Lot 1 · viaduc (z10-14, sous-poutre 6 m, rails à 6,8 m) sans solide, piles tous les 12 m
  ...PILES.map((cx, i) => B('ml_v_pile' + i, '', 'ml_viaduc_pile_v2_3q', cx - 0.8, 11.2, 1.6, 1.6, { zone: 'viaduc', named: false, solid: [{ x: cx - 0.8, z: 11.2, w: 1.6, d: 1.6 }] })),
  B('ml_v_seg0', '', 'ml_viaduc_seg24_v2_3q', 0, 10, 24, 4, { zone: 'viaduc', named: false, solid: [], etage: 1 }),
  B('ml_v_seg1', '', 'ml_viaduc_seg24_v2_3q', 24, 10, 24, 4, { zone: 'viaduc', named: false, solid: [], etage: 1 }),
  B('ml_v_seg2', '', 'ml_viaduc_seg16_v2_3q', 48, 10, 16, 4, { zone: 'viaduc', named: false, solid: [], etage: 1 }),
  // rame 3 voitures (base y 6,8, z10,5-13,5) : passe sans s'arrêter, vue avant vers +x, vue dos vers −x (view.js, rame) ; boîte de tri = tout le viaduc
  B('ml_rame', '', 'ml_rame_3v_v2_3q', 0, 10.5, 64, 3, { zone: 'viaduc', named: false, solid: [], y: 6.8, etage: 2, rame: { passage: 12, periode: 30, ph: 4 } }),
  // poutres sud du viaduc (calques _avant) : APRÈS la rame, elles masquent ses bogies
  B('ml_v_av0', '', 'ml_viaduc_seg24_v2_3q_avant', 0, 10, 24, 4, { zone: 'viaduc', named: false, solid: [], etage: 3 }),
  B('ml_v_av1', '', 'ml_viaduc_seg24_v2_3q_avant', 24, 10, 24, 4, { zone: 'viaduc', named: false, solid: [], etage: 3 }),
  B('ml_v_av2', '', 'ml_viaduc_seg16_v2_3q_avant', 48, 10, 16, 4, { zone: 'viaduc', named: false, solid: [], etage: 3 }),
  // Lot 2 · échoppes sous le quai (z14-20, dessus à +5,4 caché par le tablier) : rez non praticable, solides de la fiche non posés (le sol y est le quai)
  B('ml_ech_tran', 'Nouilles de Mme Tran', 'ml_echoppe_tran_v2_3q', 18, 14, 6, 6, { zone: 'quai', solid: [] }),
  B('ml_ech_cables', 'Câbles et réparations', 'ml_echoppe_cables_v2_3q', 24, 14, 6, 6, { zone: 'quai', solid: [] }),
  B('ml_hc', 'Human Corp', 'ml_facade_humancorp_v2_3q', 30, 14, 8, 6, { zone: 'quai', solid: [], dalles: [{ champ: 'logo', image: 'ml_ens_human_corp' }] }), // logo qui respire dans le caisson noir
  B('ml_atelier', 'Atelier de Rivet', 'ml_atelier_rivet_v2_3q', 38, 14, 8, 6, { zone: 'quai', solid: [] }),
  B('ml_cafe_froid', '', 'ml_cafe_froid', 39.7, 20, 0.2, 0.2, { zone: 'quai', solid: [], named: false, y: 0.98 }), // café froid de Rivet, sur l'établi de l'atelier (fiche : x≈39,8 z≈20,1 y 0,98)
  // Lot 1 · quai à +6 m (x18-46, z14-22) : tablier, barrières, portique à implant, écrans ; deux escaliers vers la rue
  B('ml_quai', '', 'ml_quai_tablier_v2_3q', 18, 14, 28, 8, { zone: 'quai', named: false, solid: BORDS_QUAI, etage: 1 }),
  B('ml_esc_o', '', 'ml_escalier_v2_3q', 18, 22, 3, 10, { named: false, solid: COTES_ESC(18), etage: 1 }),
  B('ml_esc_e', '', 'ml_escalier_v2_3q', 43, 22, 3, 10, { named: false, solid: COTES_ESC(43), etage: 1 }),
  // barrières de la fiche (z17,4) + deux bouts de 0,4 et 0,8 m jusqu'aux garde-corps (sinon la bande d'embarquement s'ouvre aux extrémités)
  B('ml_barr_o', '', 'ml_quai_barriere_v2_3q', 18.4, 17.35, 12.6, 0.3, { zone: 'quai', named: false, y: QUAI, etage: 2, solid: [{ x: 18.4, z: 17.4, w: 12.6, d: 0.2 }, { x: 18, z: 17.4, w: 0.4, d: 0.2 }] }),
  B('ml_barr_e', '', 'ml_quai_barriere_v2_3q', 32.6, 17.35, 12.6, 0.3, { zone: 'quai', named: false, y: QUAI, etage: 2, solid: [{ x: 32.6, z: 17.4, w: 12.6, d: 0.2 }, { x: 45.2, z: 17.4, w: 0.8, d: 0.2 }] }),
  B('ml_portique_implant', 'Portique à implant', 'ml_portique_implant', 31, 17, 1.6, 1, { zone: 'quai', y: QUAI, etage: 2, solid: [{ x: 31, z: 17, w: 1.6, d: 1 }] }), // éteint ; planches jouées une fois au passage (main.js)
  B('ml_tableau', 'Tableau des départs', 'ml_tableau', 26.4, 19.6, 2.4, 0.4, { zone: 'quai', y: QUAI, etage: 2 }), ENS('ml_e_horaires', 'ml_ens_horaires', 27.6, 20.2, QUAI + 2.2, { zone: 'quai', etage: 3 }),
  B('ml_borne', 'Borne de billets', 'ml_borne', 34.4, 18.4, 0.8, 0.6, { zone: 'quai', y: QUAI, etage: 2 }),
  B('ml_banc0', '', 'ml_banc', 24, 19.2, 2, 0.6, { zone: 'quai', named: false, y: QUAI, etage: 2 }), B('ml_banc1', '', 'ml_banc', 37, 20.4, 2, 0.6, { zone: 'quai', named: false, y: QUAI, etage: 2 }),
  B('ml_poub0', '', 'ml_poubelle', 29.6, 20.6, 0.6, 0.6, { zone: 'quai', named: false, y: QUAI, etage: 2 }), B('ml_poub1', '', 'ml_poubelle', 41, 18.2, 0.6, 0.6, { zone: 'quai', named: false, y: QUAI, etage: 2 }),
  // écrans du quai (cadres vierges, mâts depuis le quai, dalle +10,5-13,38 au-dessus du toit de la rame) : Vibes à l'ouest, Tron à l'est, posés dans ecran.quad_px
  B('ml_ecran_vibes', '', 'ml_ecran_cadre_v2_3q', 19.8, 14, 5.4, 0.4, { zone: 'quai', named: false, y: QUAI, etage: 2, solid: [{ x: 19.8, z: 14, w: 0.3, d: 0.2 }, { x: 24.9, z: 14, w: 0.3, d: 0.2 }], dalles: [{ champ: 'ecran', image: 'ml_ens_ecran_vibes', groupe: 'ecrans_quai' }] }),
  B('ml_ecran_tron', '', 'ml_ecran_cadre_v2_3q', 36.8, 14, 5.4, 0.4, { zone: 'quai', named: false, y: QUAI, etage: 2, solid: [{ x: 36.8, z: 14, w: 0.3, d: 0.2 }, { x: 41.9, z: 14, w: 0.3, d: 0.2 }], dalles: [{ champ: 'ecran', image: 'ml_ens_ecran_tron', groupe: 'ecrans_quai' }] }),
  // Lot 2 · rue piétonne et terrasses (x21-43, z22-32)
  ...TERR.map(([x, z], i) => B('ml_ter' + i, '', 'ml_terrasse_v2_3q', x, z, 2, 2, { named: false, solid: [{ x: x + 0.6, z: z + 0.6, w: 0.8, d: 0.8 }] })),
  // Lot 2 · bâti ouest et est (z14-32), rez actifs sur les rues latérales (x10-18, x46-54)
  B('ml_bw', '', 'ml_bati_w_v2_3q', 0, 14, 10, 18, { named: false, solid: [{ x: 0, z: 14, w: 10, d: 18 }] }),
  B('ml_be', '', 'ml_bati_e_v2_3q', 54, 14, 10, 18, { named: false, solid: [{ x: 54, z: 14, w: 10, d: 18 }] }),
  // parvis sud (z32-40) : lampadaires à ampoule visible, bancs
  ...LAMPS.map(([x, z], i) => B(`ml_lamp${i}`, '', 'ml_lampadaire', x - 0.3, z - 0.3, 0.6, 0.6, { named: false })),
  B('ml_banc2', '', 'ml_banc', 11, 36.6, 2, 0.6, { named: false }), B('ml_banc3', '', 'ml_banc', 51, 36.6, 2, 0.6, { named: false }),
  // bord sud (z40, Régie) : garde-corps bas d'acier sombre de Center-Town (ct_mob_barriere_x_v4_3q, 2 m, 1 m de haut, 50 px/m, échelle 1), ouvert sur 4 m
  // au centre (x30-34) pour la porte c_mega ; au-delà, le parvis continue dans la marge sombre (ground.marge) au lieu du noir
  ...[...Array(15).keys()].flatMap(i => [2 * i, 34 + 2 * i])
    .map(x => B('ml_sud_gc' + x, '', 'ct_mob_barriere_x_v4_3q', x, 39.6, 2, 0.2, { named: false, solid: [{ x, z: 39.6, w: 2, d: 0.2 }] })),
];
const CONT = [[24.5, 9.5, 2], [30.5, 9.5, 2], [24.5, 13, 3], [30.5, 13, 2], [24.5, 16.5, 2], [30.5, 16.5, 3]]; // 3 rangées de 2 piles (allées de 1 m), 2 ou 3 niveaux
// Lot 3 d'Ocre (f86e5ec), poses de sa fiche (ASSETS.md, lot 3) : échelle 1, ancre au coin avant sud-est, base y 0 (quai et rame portent leur hauteur).
// Tri : zone 'cour' (portique 0 < conteneurs 1 < poutres _avant du portique 2 < gyrophares 3), zone 'quai' (quai 1 < panneau 2, personnages sur le quai).
export const BUILDINGS_TERMINUS = [
  // voûte (fond), murs et portes du sas (z0-2) : pleines, fermées, joint plein, sans lumière de dehors
  B('tm2_voute', '', 'ml_tm_voute_v2_3q', 0, 0, 40, 2, { named: false, solid: [], fond: true }),
  B('tm2_mur_o', '', 'ml_tm_sas_mur_o_v2_3q', 0, 0, 10, 2, { named: false }),
  B('ml_sas', 'Les portes du sas', 'ml_tm_sas_portes_v2_3q', 10, 0, 20, 2, {}), // boîtiers éteints en x13,5 / 26,5 : les lampes ml_ens_sas tombent dessus
  B('tm2_mur_e', '', 'ml_tm_sas_mur_e_v2_3q', 30, 0, 10, 2, { named: false }),
  ENS('ml_e_sas0', 'ml_ens_sas', 13.5, 2.15, 12.4, { groupe: 'sas', ph: 0 }), ENS('ml_e_sas1', 'ml_ens_sas', 26.5, 2.15, 12.4, { groupe: 'sas', ph: 2 }), // lampes d'alerte rouges qui clignotent
  // hangar, heurtoir, voie (fond), quai à l'est de la voie (+1,1 m sur z3-22, rampe z22-24)
  B('tm2_hangar', '', 'ml_tm_hangar_v2_3q', 0, 2, 9, 5, { named: false }),
  B('tm2_heurtoir', '', 'ml_tm_heurtoir_v2_3q', 14, 2, 3, 1.4, { named: false }),
  B('tm2_voie', '', 'ml_tm_voie_v2_3q', 14, 3.4, 3, 24.6, { named: false, solid: [], fond: true }),
  B('tm2_quai', '', 'ml_tm_quai_v2_3q', 17, 3, 6, 21, { zone: 'quai', named: false, solid: [], etage: 1 }),
  // la vraie rame à quai (violette, exception au terminus) : deux voitures tête au nord, puis la voiture d'accès (porte est z25-26, jonction tm_rame_quai)
  B('tm2_rame_nord', '', 'ml_tm_rame_nord_v2_3q', 14, 3.4, 3, 16.6, { named: false, solid: [{ x: 14, z: 3.4, w: 3, d: 16.6 }] }),
  // la rame occupe toute la voie (z3,4-28) : on traverse par le vestibule de la voiture d'accès (portes ouvertes, z25-26), sinon le quai et la cour
  // seraient coupés de l'arrivée (passerelle SO) ; la jonction tm_rame_quai reste sur le quai, au seuil (18,2 ; 25,2)
  B('tm2_voiture', '', 'ml_tm_voiture_v2_3q', 14, 20, 3, 8, { named: false, solid: [{ x: 14, z: 20, w: 3, d: 5 }, { x: 14, z: 26, w: 3, d: 2 }] }),
  B('ml_panneau', 'Dernier arrêt avant No Man\u2019s Land', 'ml_panneau_terminus', 18.5, 3.4, 3, 0.5, { zone: 'quai', sign: true, y: 1.1, etage: 2 }), // phrase affichée par le code (libellé), panneau vierge
  // bureau de la gare de fret et son dock
  B('ml_bureau', 'Bureau de la gare de fret', 'ml_tm_bureau_fret_v2_3q', 2, 9, 7, 5, {}),
  B('tm2_dock', '', 'ml_tm_dock_v2_3q', 9, 9, 2, 5, { named: false }),
  // portique de levage (seuls les pieds sont pleins), conteneurs (piles de 2 et de 3, z croissant), puis poutres _avant du portique
  B('ml_portique', 'Portique de levage', 'ml_tm_portique_levage_v2_3q', 24, 8, 13, 13, { zone: 'cour', etage: 0,
    solid: [{ x: 24, z: 8, w: 1, d: 1 }, { x: 36, z: 8, w: 1, d: 1 }, { x: 24, z: 20, w: 1, d: 1 }, { x: 36, z: 20, w: 1, d: 1 }] }),
  ...CONT.map(([x, z, n], i) => B(`ml_cont${i}`, '', n === 2 ? 'ml_tm_conteneurs_x2_v2_3q' : 'ml_tm_conteneurs_x3_v2_3q', x, z, 6, 2.5, { zone: 'cour', etage: 1, named: false })),
  B('tm2_portique_avant', '', 'ml_tm_portique_levage_v2_3q_avant', 24, 8, 13, 13, { zone: 'cour', etage: 2, named: false, solid: [] }),
  ENS('ml_e_gyro0', 'ml_ens_gyrophare', 24.5, 8.6, 13.1, { zone: 'cour', groupe: 'gyrophares', ph: 0, etage: 3 }), ENS('ml_e_gyro1', 'ml_ens_gyrophare', 36.5, 8.6, 13.1, { zone: 'cour', groupe: 'gyrophares', ph: 2, etage: 3 }),
  // locaux techniques, passerelle de service (arrivée de la ligne, sud-ouest) : une pose 4 x 4, garde-corps pleins
  B('tm2_loc_e', '', 'ml_tm_locaux_e_v2_3q', 37, 2, 3, 26, { named: false }),
  B('tm2_loc_so', '', 'ml_tm_locaux_so_v2_3q', 0, 17, 8, 11, { named: false }),
  B('tm2_pass', '', 'ml_tm_passerelle_v2_3q', 8, 24, 4, 4, { named: false, solid: [{ x: 8, z: 24, w: 0.3, d: 4 }, { x: 11.7, z: 24, w: 0.3, d: 4 }] }),
];
export const CLOSED_MEGA = {
  ml_portique_implant: 'Le portique à implant. Deux piliers, deux volets vitrés, un lecteur éteint. Il lit la nuque des gens.',
  ml_v_seg1: 'Le viaduc de fer noir. Les piles ruissellent ; le fer transpire.',
  ml_quai: 'Le quai, six mètres au-dessus de la rue. On y monte par les escaliers ; la rame ne s\u2019arrête pas pour qui n\u2019a pas de billet.',
  ml_tableau: 'Le tableau des départs, en pictogrammes. Une ligne change. Aucune ne dit « terminus ».',
  ml_borne: 'La borne de billets reconnaît les bracelets, et les visages.',
  ml_sas: 'Les portes du sas. Pleines, si hautes qu\u2019on les prend pour un mur. Fermées. Elles ne s\u2019ouvriront pas.',
  ml_panneau: '« Dernier arrêt avant No Man\u2019s Land. »',
  ml_bureau: 'Le bureau de la gare de fret. Une fenêtre ambrée, des bordereaux.',
  ml_portique: 'Le portique de levage jaune. Les conteneurs vont et viennent, toujours vers l\u2019intérieur.',
};
// Sol de la ligne : dalle g_ml_parvis_v2 (4 m) + variantes _b/_c/_d semées sur la grille de 4 m (ASSETS.md, « sol du parvis et de la rue »).
// Les 11 carreaux de la fiche d'Ocre sont gardés ; le reste est un tirage déterministe (hachage de x, z), ~40 % de variantes,
// jamais la même variante sur deux carreaux voisins (O, N, NO, NE) : pas de motif répété visible, même rendu à chaque chargement.
const PARVIS = (() => {
  const V = ['_b', '_c', '_d'], fiche = { '12,24': '_c', '24,24': '_b', '36,28': '_d', '48,24': '_c', '28,32': '_c', '8,36': '_b', '20,36': '_d', '40,36': '_b', '56,36': '_c', '12,8': '_b', '32,8': '_c' };
  const h = (x, z) => { let n = Math.imul(x * 374761 + z * 668265 + 1013, 2246822519) >>> 0; n = Math.imul(n ^ (n >>> 13), 3266489917) >>> 0; return (n ^ (n >>> 16)) >>> 0; };
  const g = {};
  for (let z = 0; z < 40; z += 4) for (let x = 0; x < 64; x += 4) {
    const k = x + ',' + z; if (fiche[k]) { g[k] = fiche[k]; continue; }
    const r = h(x, z); if (r % 10 >= 4) continue; // ~60 % de dalle de base
    const voisins = [[-4, 0], [0, -4], [-4, -4], [4, -4], [4, 0], [0, 4], [-4, 4], [4, 4]].map(([a, b]) => g[(x + a) + ',' + (z + b)] || fiche[(x + a) + ',' + (z + b)]);
    for (let i = 0; i < 3; i++) { const v = V[(r + i) % 3]; if (!voisins.includes(v)) { g[k] = v; break; } }
  }
  return Object.entries(g).map(([k, v]) => { const [x, z] = k.split(',').map(Number); return { x, z, w: 4, d: 4, skin: 'g_ml_parvis_v2' + v }; });
})();
export const LOCATIONS_MEGA = {
  steel_megaline: { id: 'steel_megaline', name: 'Steel-Megalopolis · Mega-Line', kind: 'exterior', size: { w: 64, d: 40 }, light: LIGNE, plan: 2, zoneNiveau: 'quai', // personnage sur le quai ou l'escalier : trié avec le quai (devant son rez)
    cadre: { desktop: { x: [21, 43], z: [16, 24] }, mobile: { x: [8, 56], z: [10, 30] } }, // le cadre reste sur le lieu (pas de vide au sud à l'arrivée)
    ground: { base: '#12121a', skin: 'g_ml_parvis_v2', tileM: 4, clean: true, paint: PARVIS, // dalle mate d'Ocre (27a0fd3) à la place de g_ml_pave (halos peints)
      marge: { skin: 'g_ml_parvis_v2', tileM: 4, m: 48, voile: 'rgba(6,6,10,.62)' } }, // hors carte : le parvis continue vers Center-Town, voilé, au lieu du noir
    labelsProches: { ids: ['ml_navetteur', 'ml_controleuse', 'ml_etudiante', 'ml_entretien', 'ml_nouilles', 'ml_vigile', 'ml_pancarte', 'ml_fan', 'ml_rivet', 'ml_rame_quai', 'ml_passerelle'], r: 4, petits: true }, // 390 (Régie) : noms des PNJ, du portique et de la passerelle à 4 m du joueur ou au toucher ; desktop inchangé
    // quai à +6 m et escaliers (montée vers le nord) : hauteur de sol au rendu ; l'accès est fait par les solides (BORDS_QUAI, COTES_ESC)
    niveaux: [{ x: 18, z: 14, w: 28, d: 8, y: QUAI }, ...[18, 43].flatMap(x => [{ x, z: 22, w: 3, d: 1, y: QUAI }, { x, z: 23, w: 3, d: 9, y0: QUAI, y1: 0, axe: 'z' }])], // fiche d'Ocre : palier z22-23 à +6, 36 marches jusqu'à z32
    buildings: BUILDINGS_MEGA, props: [],
    glows: [ ...LAMPS.map(([x, z]) => ({ x, z: z + 0.6, rx: 2.6, rz: 1.9, color: AMBRE, i: 0.55, flicker: true })), // lampadaires (code)
      { x: 22.5, z: 15.6, rx: 3, rz: 1.4, color: VIOLET, i: 0.6, flicker: true, sol: true }, { x: 39.5, z: 15.6, rx: 3, rz: 1.4, color: CYAN, i: 0.55, flicker: true, sol: true }, // reflets des écrans sur le quai
      { x: 21, z: 23.2, rx: 3, rz: 1.2, color: '#e0603a', i: 0.5, flicker: true }, { x: 27, z: 23, rx: 2.6, rz: 1, color: AMBRE, i: 0.35 }, { x: 34, z: 23, rx: 3, rz: 1.1, color: '#6aa8e0', i: 0.3 },
      { x: 42, z: 23.2, rx: 2.6, rz: 1.1, color: AMBRE, i: 0.5 }, { x: 32, z: 19.6, rx: 12, rz: 2, color: AMBRE, i: 0.18, sol: true }, { x: 31.8, z: 18.3, rx: 1.4, rz: 0.8, color: AMBRE, i: 0.5, sol: true } ],
    extras: [ ...[[20.5, 15.8], [26.5, 16.2], [29, 15.6], [36, 15.7], [43.5, 16.1]].map(([x, z], i) => ({ sprite: i % 2 ? 'gen_ml_foule_b' : 'gen_ml_foule_a', x, z, face: i % 2 ? 1 : -1, role: 'voyageur' })), // bande d'embarquement
      ...[[30.6, 21], [14.4, 26], [25.2, 30.6], [38.8, 31], [8, 36.4], [55, 37.2], [24.6, 26.6], [41.4, 25.4]].map(([x, z], i) => ({ sprite: i % 2 ? 'gen_ml_foule_a' : 'gen_ml_foule_b', x, z, face: i % 2 ? -1 : 1, role: 'passant', dense: i > 5 })) ],
    walkers: [ { sprite: 'gen_ml_foule_a', path: [[32, 36], [19.5, 33], [19.5, 21.2], [30, 19.6], [44.5, 21.2], [44.5, 33]], speed: 0.9, t0: 4 }, // monte l'escalier ouest, traverse le quai, redescend à l'est
      { sprite: 'gen_ml_foule_b', path: [[3, 37.5], [61, 37.5]], speed: 0.8, t0: 10 }, { sprite: 'gen_ml_foule_a', path: [[13.5, 33], [13.5, 10.2], [50, 10.2], [50.5, 33]], speed: 0.85, t0: 30 } ],
    spawn: { player: { x: 32, z: 38.2 }, companion: { x: 33, z: 38.2 } }, city: 'steel',
    arrive: { from: 'steel_center', text: 'La Mega-Line. Le viaduc de fer noir passe à six mètres au-dessus de la rue ; la rame violette glisse sans s\u2019arrêter. Sur le quai, Vibes et Tron passent en boucle.' } },
  steel_terminus: { id: 'steel_terminus', name: 'Steel-Megalopolis · Terminus de fret', kind: 'exterior', size: { w: 40, d: 28 }, light: FRET, plan: 2, zoneNiveau: 'quai',
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
