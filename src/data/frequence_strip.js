import { PIQUE_PUCE_PRIX } from './mega_line.js';
// Fréquence Strip (zone steel_strip, 80 x 24 m, quartier de Center-Town). Pack d'Ocre : docs/villes/steel/quartiers/frequence_strip/ (FREQUENCE_STRIP.md, ASSETS.md, compléments 1 et 2).
// [décision] ouverte à l'ouest sur la sortie est de Pulse Plaza ; bout est : grille ouverte vers la Steel Arena (fs_est). Neon-7 et Core Stack fermés pour l'instant.
// Groovy-Tron et Groovy Vibes n'apparaissent que sur des écrans (enseignes fs_ens_tron, fs_ens_vibes) : jamais rencontrés. Aucun nom civil.
// Enseignes animées : planches du manifeste (frames, frame_px, fps), lues par view.js ; au plus 8 animations visibles à la fois sur mobile.
// [décision Valentin] quartier rouge : rue sombre, chaque tache de lumière vient d'une enseigne ou d'une vitrine ; rouges et roses dominants,
// ambre en touche (bar, stand), violet en accent seulement (Core Stack, Vibes). Ambiance plus sombre qu'avant (hemi, soleil et teinte baissés en luminance ; la teinte sans bleu tire les fenêtres violettes des façades vers le rose).
const STRIP = { bg: '#060a10', hemi: ['#e05870', '#2a0c16', 1.3], sun: ['#f2a04a', 0.5], tint: '#d4907e', actor: '#ecd0d4' };
const ROUGE = '#ff2a48', ROSE = '#ff5a8c', VIOLET = '#8a3cff', AMBRE = '#f2a04a', VELOURS = '#7a1428';
const B = (id, label, sprite, x, z, w, d, extra = {}) => ({ id, label, sprite, x, z, w, d, visitable: false, cue: null, named: !!label, ...extra });
const ENS = (id, sprite, x, z, y) => B(id, '', sprite, x - 0.1, z - 0.1, 0.2, 0.2, { y, solid: [], named: false }); // enseigne : point de pose (x, z) au pied de la façade, hauteur y (m)
// Pose 3/4 (0602bea) : bâtiments complets en 3/4 isométrique (*_3q, calques *_3q_neon et *_3q_fenetres), ancrés au pied du coin avant sud-est (x+W ; z+D).
// Nord : front aligné sur le trottoir (z 6), profondeur 4 ou 8 m (z 2 ou -2) ; ruelle Fusible fermée en z 0-3 (z 3-6 libre).
// Sud : front au bord de la zone (z 24), profondeur 4 m (z 20-24, alignée sur Le Retour et l'hôtel capsule) ; aucun personnage dans leur ombre d'écran (view.masques() vide).
export const BUILDINGS_STRIP = [
  // façade nord, d'ouest en est (rue de 80 m, front z 6 ; volumes legacy à ancre centrale recalés dans leur parcelle via ancre/k)
  B('fs_fn0', '', 'fs_facade_nord', 0, 0, 8, 6, { named: false, ancre: [-2.4, 0], k: 1.32 }),
  B('fs_bouche0', '', 'fs_bouche_nord_3q', 8, 0, 2, 3, { ancre: [1, 0], named: false }), // ferme la ruelle x 8-10 bord à bord (z 3-6 libre autour de Fusible)
  B('fs_neon7', 'Club Neon-7', 'fs_neon7', 10, 0, 12, 6, { ancre: [-3.2, 0], k: 1.24 }),
  B('fs_sexshop', 'Jouets calibrés', 'fs_sexshop_3q', 22, -2, 8, 8), B('fs_peep', '3 secondes', 'fs_peep_3q', 30, 2, 4, 4), B('fs_salon', 'Tombé de rideau', 'fs_salon_3q', 34, 2, 4, 4),
  B('fs_corestack', 'Core Stack', 'fs_corestack', 38, 0, 12, 6, { ancre: [-3.4, 0], k: 1.28 }),
  B('fs_bouche1', '', 'fs_bouche_nord_3q', 50, 2, 4, 4, { named: false }),
  B('fs_club', 'L\u2019Effeuillée', 'fs_club_3q', 54, -2, 10, 8), B('fs_lovehotel', 'L\u2019Heure exquise', 'fs_lovehotel_3q', 64, -2, 8, 8), B('fs_clubprive', 'Club 404', 'fs_clubprive_3q', 72, -2, 8, 8),
  // côté sud, premier plan (front z 24, emprises 3/4 z 20-24)
  B('fs_nouilles', 'Nouilles de minuit', 'fs_bas_nouilles_3q', 0, 20, 8, 4), B('fs_fleurs', 'Excuses', 'fs_bas_fleurs_3q', 8, 20, 4, 4), B('fs_tabac', 'À crédit', 'fs_bas_tabac_3q', 12, 20, 4, 4),
  B('fs_retour', 'Le Retour', 'fs_retour', 16, 18, 8, 6, { ancre: [-1.2, 0] }),
  B('fs_couvert', 'Bien couvert', 'fs_bas_preservatifs_3q', 24, 20, 4, 4),
  B('fs_fresque_vibes', 'Fresque inachevée', 'fs_fresque_vibes', 28, 23.4, 6, 0.6), // caméo Ocre : mur de fresque au bord sud (x 28-34), média de Vibes, aucune animation
  B('fs_shots', 'Shot de grâce', 'fs_bas_shots_3q', 34, 20, 4, 4),
  B('fs_cabines', 'Cabines sans C.A.G.E.', 'fs_cabines_3q', 38, 20, 8, 4),
  B('fs_billets', 'Billets doux', 'fs_bas_distributeur_3q', 46, 20, 4, 4), B('fs_massages', 'Mains de fée', 'fs_bas_massages_3q', 50, 20, 4, 4),
  B('fs_capsules', 'Hôtel capsule', 'fs_capsules', 54, 18, 6, 6, { ancre: [-1.2, 0] }),
  B('fs_laverie', 'Blanchiment', 'fs_bas_laverie_3q', 60, 20, 8, 4), B('fs_gage', 'Mont-de-piété', 'fs_bas_gage_3q', 68, 20, 4, 4), B('fs_perruques', 'Faux-semblants', 'fs_bas_perruques_3q', 72, 20, 4, 4), B('fs_implants', 'Rechromage', 'fs_bas_implants_3q', 76, 20, 4, 4),
  // rue
  B('fs_tapis', '', 'fs_tapis', 14, 6, 4, 2, { solid: [], named: false, ancre: [-1.4, 0] }),
  B('fs_stand_brochettes', 'Brochettes de Yun', 'fs_stand_brochettes', 8, 14, 4, 4),
  B('fs_stand_merch', 'Merch « pas tout à fait officiel »', 'fs_stand_merch', 46, 14, 4, 4),
  B('fs_cam', '', 'pp_camera', 24.8, 14.8, 0.4, 0.4, { named: false }),
  B('fs_grille_est', 'Grille de l\u2019Arena', 'fs_grille_est', 76, 11, 4, 1, { solid: [] }), // ouverte : mène à la Steel Arena (fs_est)
  // enseignes animées (planches d'Ocre, 9 au total, au plus 8 visibles sur mobile) : Neon-7, Core Stack, cœur, Retour, capsules ; Vibes et Tron face à face sur le mur aveugle x 50-54 ; 2 panaches de vapeur
  ENS('fs_e_neon7', 'fs_ens_neon7', 16.8, 6.2, 4.0), ENS('fs_e_core', 'fs_ens_corestack', 44.6, 6.2, 3.8),
  ENS('fs_e_vibes', 'fs_ens_vibes', 51.4, 6.2, 1.2), ENS('fs_e_coeur', 'fs_ens_coeur', 4.2, 6.2, 2.8),
  ENS('fs_e_tron', 'fs_ens_tron', 53.8, 6.2, 1.2),
  ENS('fs_e_retour', 'fs_ens_retour', 18.4, 24.2, 3.4), ENS('fs_e_capsules', 'fs_ens_capsules', 55.8, 24.2, 2.4),
  ENS('fs_vap0', 'fs_vapeur', 5, 11, 0), ENS('fs_vap1', 'fs_vapeur', 69, 11, 0),
];
export const CLOSED_STRIP = {
  fs_fresque_vibes: 'Une fresque inachevée de Groovy Vibes, une échelle, des pots. La peinture est encore fraîche.',
  fs_neon7: 'Club Neon-7. « Next Drop. Entrée : sourire calibré. » Le portique au-dessus de la porte te scanne et ne s\u2019ouvre pas.',
  fs_corestack: 'Core Stack. Une affiche : 31/10. Les baies ronronnent derrière la porte, fermée.',
  fs_retour: 'Le Retour. Lumière ambre, musique basse. Fermé pour l\u2019instant.',
  fs_capsules: 'Hôtel capsule. Des cases empilées, quelques hublots allumés. Complet.',
  fs_grille_est: 'La grille du bout de la rue, ouverte. Derrière, le dôme de l\u2019Arena et une foule qui gronde.',
  fs_sexshop: 'Jouets calibrés. En vitrine, des objets aux formes vagues et aux couleurs franches. « Satisfaction mesurée ou remboursée. »',
  fs_peep: '3 secondes. Une fente à crédits, un rideau. « Trois secondes pour m\u2019aimer. Au-delà, c\u2019est un abonnement. »',
  fs_salon: 'Tombé de rideau. Velours rouge, hôtesses au bar. Une pancarte : « On ne réveille pas les rideaux. »',
  fs_club: 'L\u2019Effeuillée. Une basse lente derrière la porte capitonnée. Le videur te fait comprendre que ce n\u2019est pas encore ton heure.',
  fs_lovehotel: 'L\u2019Heure exquise. Chambres à l\u2019heure, tarif dégressif après minuit. Le rideau de lanières cache une alcôve, pas une entrée.',
  fs_clubprive: 'Club 404. « Membre introuvable. » La double porte reste fermée, même pour ceux qui ont la carte.',
  fs_cabines: 'Cabines sans C.A.G.E. Pas de caméra, pas de garde, pas d\u2019engagement. Un rideau, et c\u2019est complet.',
  fs_nouilles: 'Nouilles de minuit. Le bouillon fume, le comptoir donne sur la rue. Rien à payer tant que tu ne t\u2019assois pas.',
  fs_fleurs: 'Excuses. Des fleurs pour ceux qui sortent d\u2019ici et rentrent chez eux. Les bouquets les plus chers sont les plus petits.',
  fs_couvert: 'Bien couvert. Préservatifs et « tonifiants » au comptoir. Le vendeur te souhaite bonne chance sans lever les yeux.',
  fs_shots: 'Shot de grâce. Trois verres alignés, un seul a une étiquette. Le barman dit que c\u2019est la surprise.',
  fs_billets: 'Billets doux. Un distributeur rafistolé au ruban rose. Il donne des billets, ou il les garde, selon son humeur.',
  fs_massages: 'Mains de fée. Un rideau de perles et une lampe tamisée. « Tarif à la minute, pourboire à la conscience. »',
  fs_laverie: 'Blanchiment. Laverie ouverte toute la nuit. Personne ne vient pour le linge.',
  fs_gage: 'Mont-de-piété. Montres, implants, alliances. Le prêteur pèse tout, même les excuses.',
  fs_perruques: 'Faux-semblants. Perruques et costumes. On ressort quelqu\u2019un d\u2019autre, au même prix.',
  fs_implants: 'Rechromage. Réparateur d\u2019implants. « Danse, sois plus chrome. » La garantie tient jusqu\u2019au trottoir.',
  fs_tabac: 'À crédit. Tabac, recharges, tickets. Le guichet sert depuis la rue et ne rend jamais la monnaie exacte.',
};
// Sol : chaussée sombre g_fs_asphalte en grandes tuiles (10,24 m, aucun damier lisible), trottoirs étroits g_fs_trottoir_etroit (tuile 2,56 x 6,4 m gardée),
// caniveaux, plaques d'égout, détritus et cartons peints dans le sol (ground.decals) ; mouillé et reflets au moteur : lueurs étirées sous chaque enseigne.
const CANIVEAUX = [...Array.from({ length: 20 }, (_, i) => ({ image: 'fs_caniveau', x: 2 + i * 4, z: 8.3, a: 0.6 })), ...Array.from({ length: 20 }, (_, i) => ({ image: 'fs_caniveau', x: 2 + i * 4, z: 15.7, a: 0.6 }))];
const PIECES = [ { image: 'fs_plaque_egout', x: 20, z: 12 }, { image: 'fs_plaque_egout', x: 44, z: 10 }, { image: 'fs_plaque_egout', x: 64, z: 13 }, { image: 'fs_plaque_egout', x: 74, z: 9.6 },
  { image: 'fs_detritus', x: 37.4, z: 6.6 }, { image: 'fs_detritus', x: 50.6, z: 6.7, rot: 30 }, { image: 'fs_detritus', x: 63.4, z: 6.6, rot: -20 }, { image: 'fs_detritus', x: 26, z: 19.3, rot: 60 }, { image: 'fs_detritus', x: 71, z: 19.2 },
  { image: 'fs_carton', x: 61.2, z: 19.4, rot: 15 }, { image: 'fs_carton', x: 9.2, z: 5.2, rot: -10 } ];
export const LOCATIONS_STRIP = {
  steel_strip: { id: 'steel_strip', name: 'Steel-Megalopolis · Fréquence Strip', kind: 'exterior', size: { w: 80, d: 24 }, light: STRIP,
    ground: { base: '#0c0a0e', skin: 'g_fs_asphalte', tileM: 10.24, clean: true, marge: { skin: 'g_fs_asphalte', tileM: 10.24, m: 60, voile: 'rgba(8,4,10,.62)' }, decals: [...CANIVEAUX, ...PIECES], zones: [
      { x: 0, z: 6, w: 80, d: 2, kind: 'plate', skin: 'g_fs_trottoir_etroit', tileM: 2.56 }, { x: 0, z: 16, w: 80, d: 8, kind: 'plate', skin: 'g_fs_trottoir_etroit', tileM: 2.56 },
      { x: 8, z: 3, w: 2, d: 3, kind: 'plate', skin: 'g_fs_trottoir_etroit', tileM: 2.56 }, // ruelle de Fusible
      // grilles vapeur : plaques isolées, une tuile chacune (jamais en motif)
      { x: 4, z: 10, w: 2, d: 2, kind: 'plate', skin: 'g_fs_grille_vapeur', tileM: 2 }, { x: 68, z: 10, w: 2, d: 2, kind: 'plate', skin: 'g_fs_grille_vapeur', tileM: 2 },
      { x: 35, z: 13, w: 2, d: 2, kind: 'plate', skin: 'g_fs_grille_vapeur', tileM: 2 } ] },
    buildings: BUILDINGS_STRIP, props: [],
    // une lueur = une enseigne ou une vitrine (reflet sur le mouillé) : rouges et roses dominants, ambre en touche (Retour, brochettes, nouilles, tabac), violet en accent (Core Stack, Vibes)
    glows: [
      { x: 16, z: 7.5, rx: 6, rz: 2.4, color: ROSE, i: 0.85, flicker: true }, { x: 16, z: 7, rx: 2.2, rz: 1, color: VELOURS, i: 0.7 },
      { x: 44, z: 7.5, rx: 5, rz: 2, color: VIOLET, i: 0.6, flicker: true }, { x: 52.6, z: 7.4, rx: 2.4, rz: 1.4, color: VIOLET, i: 0.55, flicker: true },
      { x: 4, z: 7.4, rx: 2.2, rz: 1.4, color: ROUGE, i: 0.75, flicker: true },
      { x: 26, z: 7.4, rx: 3.6, rz: 1.6, color: ROSE, i: 0.7 }, { x: 32, z: 7.2, rx: 1.8, rz: 1.2, color: ROUGE, i: 0.6, flicker: true }, { x: 36, z: 7.2, rx: 1.8, rz: 1.2, color: ROUGE, i: 0.55 },
      { x: 59, z: 7.6, rx: 4.4, rz: 1.8, color: ROSE, i: 0.8, flicker: true }, { x: 68, z: 7.4, rx: 3.6, rz: 1.6, color: ROUGE, i: 0.7 }, { x: 76, z: 7.4, rx: 3.4, rz: 1.6, color: ROSE, i: 0.65, flicker: true },
      { x: 20, z: 16.6, rx: 3.6, rz: 1.6, color: AMBRE, i: 0.7 }, { x: 10, z: 13.4, rx: 2.4, rz: 1.4, color: AMBRE, i: 0.6, flicker: true },
      { x: 4, z: 19.2, rx: 3.2, rz: 1.4, color: AMBRE, i: 0.55 }, { x: 10, z: 19.2, rx: 1.8, rz: 1.1, color: ROSE, i: 0.5 }, { x: 14, z: 19.2, rx: 1.8, rz: 1.1, color: AMBRE, i: 0.45, flicker: true },
      { x: 42, z: 19.0, rx: 3.4, rz: 1.6, color: ROSE, i: 0.6, flicker: true },
      { x: 48, z: 13.4, rx: 2.4, rz: 1.4, color: ROUGE, i: 0.6 }, { x: 57, z: 16.6, rx: 2, rz: 1.2, color: ROSE, i: 0.45 },
      { x: 40, z: 12, rx: 38, rz: 4, color: ROUGE, i: 0.12 }, { x: 25, z: 15.4, rx: 0.6, rz: 0.4, color: '#c8323c', i: 0.5 } ],
    // enseignes _neon : effets poussés avec parcimonie (hors animStats.on) ; fleures/tabac/laverie/gage/perruques restent fixes
    enseignes: [
      { id: 'fs_n_sexshop', building: 'fs_sexshop', effet: 'pulse', intensite: 0.85, periode: 4.2 },
      { id: 'fs_n_peep', building: 'fs_peep', effet: 'gresille', intensite: 0.9 },
      { id: 'fs_n_salon', building: 'fs_salon', effet: 'gresille', intensite: 0.75, decale: 0.7 },
      { id: 'fs_n_club', building: 'fs_club', effet: 'saute', saute: [0.334, 0.36], intensite: 0.95, periode: 3 },
      { id: 'fs_n_lovehotel', building: 'fs_lovehotel', effet: 'pulse', intensite: 0.85, periode: 5 },
      { id: 'fs_n_clubprive', building: 'fs_clubprive', effet: 'clignote', intensite: 0.9, periode: 4.04 }, // « 404 » qui s'éteint par moments
      { id: 'fs_n_cabines', building: 'fs_cabines', effet: 'gresille', intensite: 0.8, decale: 0.4 },
      { id: 'fs_n_nouilles', building: 'fs_nouilles', effet: 'pulse', intensite: 0.7, periode: 6 },
      { id: 'fs_n_couvert', building: 'fs_couvert', effet: 'gresille', intensite: 0.7, decale: 1.1 },
      { id: 'fs_n_shots', building: 'fs_shots', effet: 'clignote', intensite: 0.85, periode: 2.8 },
      { id: 'fs_billets_n', building: 'fs_billets', effet: 'gresille' },
      { id: 'fs_n_massages', building: 'fs_massages', effet: 'pulse', intensite: 0.75, periode: 5.5, decale: 0.3 },
      { id: 'fs_implants_n', building: 'fs_implants', effet: 'clignote', periode: 3.3 },
      // démo du contour par le même fichier (sans calque _neon), derrière ?dev=1
      { id: 'fs_n_neon7', building: 'fs_neon7', effet: 'saute', saute: [0.42, 0.58], couleur: ROSE, intensite: 0.28, periode: 3, dev: true },
      { id: 'fs_n_retour', building: 'fs_retour', effet: 'pulse', couleur: AMBRE, intensite: 0.25, periode: 4, decale: 0.5, dev: true } ],
    // passants sur des couloirs hors de toute ombre d'écran (vérifiés avec view.masqueEn) ; figurants densifiés : grappes aux seuils du quartier chaud, clients hésitants ; miroir (face ±1) ; accès ouest/est et ruelle Fusible libres
    extras: [
      // Neon-7 / sexshop (trottoir nord)
      { sprite: 'gen_fs_foule_a', x: 12, z: 8.6, face: -1, role: 'foule' }, { sprite: 'gen_fs_foule_b', x: 13.2, z: 9.4, face: 1, role: 'foule' },
      { sprite: 'gen_fs_foule_a', x: 14.4, z: 7.4, face: 1, role: 'foule' }, { sprite: 'gen_fs_client_imper', x: 18.6, z: 7.3, face: -1, role: 'client' },
      { sprite: 'gen_fs_foule_b', x: 23.4, z: 7.5, face: 1, role: 'foule' }, { sprite: 'gen_fs_passante', x: 25.2, z: 8.1, face: -1, role: 'foule' },
      // peep / salon / Core Stack
      { sprite: 'gen_fs_client_costume', x: 32.6, z: 7.9, face: -1, role: 'client' },
      { sprite: 'gen_fs_foule_a', x: 35.2, z: 7.4, face: 1, role: 'foule' }, { sprite: 'gen_fs_foule_b', x: 36.8, z: 8.0, face: -1, role: 'foule' },
      { sprite: 'gen_fs_foule_a', x: 42.4, z: 7.6, face: 1, role: 'foule' }, { sprite: 'gen_fs_foule_b', x: 45.6, z: 7.4, face: -1, role: 'foule' },
      { sprite: 'gen_fs_passant_canne', x: 47.2, z: 8.2, face: 1, role: 'client' },
      // L'Effeuillée / lovehotel / Club 404 (hors grappe des PNJ nommés)
      { sprite: 'gen_fs_foule_b', x: 61.2, z: 7.3, face: -1, role: 'foule' }, { sprite: 'gen_fs_client_costume', x: 66.8, z: 7.2, face: 1, role: 'client' },
      { sprite: 'gen_fs_foule_a', x: 69.6, z: 8.4, face: -1, role: 'foule' }, { sprite: 'gen_fs_foule_b', x: 73.2, z: 8.6, face: 1, role: 'foule' },
      { sprite: 'gen_fs_client_imper', x: 75.0, z: 9.2, face: -1, role: 'client' },
      { sprite: 'gen_fs_videur_prive', x: 78, z: 7.1, face: -1, role: 'videur' },
      // cabines (position historique sûre) + quelques clients en pleine rue (z 12-14, hors ombres sud)
      { sprite: 'gen_fs_client_imper', x: 42.8, z: 14.8, face: 1, role: 'client' },
      { sprite: 'gen_fs_foule_b', x: 10.2, z: 12.8, face: 1, role: 'foule' }, { sprite: 'gen_fs_client_costume', x: 48.4, z: 12.6, face: -1, role: 'client' },
      { sprite: 'gen_fs_foule_a', x: 28.8, z: 13.2, face: -1, role: 'foule' }, { sprite: 'gen_fs_passante', x: 38.4, z: 12.4, face: 1, role: 'foule' },
      { sprite: 'gen_fs_foule_b', x: 58.2, z: 13.4, face: -1, role: 'foule' }, { sprite: 'gen_fs_client_imper', x: 6.8, z: 12.6, face: 1, role: 'client' } ],
    walkers: [ { sprite: 'gen_fs_foule_a', path: [[4, 9.75], [67, 9.75]], speed: 0.8, t0: 2 }, { sprite: 'gen_fs_foule_b', path: [[66, 8.75], [5, 8.75]], speed: 0.7, t0: 8 },
      { sprite: 'gen_fs_passante', path: [[21, 8.2], [27, 11.6]], speed: 0.9, t0: 1 }, { sprite: 'gen_fs_passant_canne', path: [[40, 7.4], [52.6, 7.4]], speed: 0.35, t0: 4 },
      { sprite: 'gen_fs_foule_a', path: [[8, 11.2], [48, 11.2]], speed: 0.7, t0: 11 } ],
    spawn: { player: { x: 1, z: 10 }, companion: { x: 1, z: 11 } }, city: 'steel',
    // revue Régie : cadre borné sur la rue (arrivées ouest et est sans vide) ; étiquettes des groupes serrés à l'approche (3 m), comme Pulse Plaza
    cadre: { mobile: { x: [9, 71], z: [9, 10] }, desktop: { x: [17, 63], z: [12, 14] } },
    labelsProches: { ids: ['fs_rouge', 'fs_rubis', 'fs_fourrure', 'fs_racoleur', 'fs_flic_a', 'fs_flic_b', 'fs_racoleuse', 'fs_mac'], r: 3 },
    arrive: { from: 'steel_arena', text: 'Fréquence Strip. Néons mouillés, publicités qui chantent plus fort que les gens. Deux basses se battent au milieu de la rue.' } },
};
const J = (id, loc, ox, oz, tx, tz, to, label, conditions = []) => ({ id, location: loc, junction: true, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: { doorId: to }, conditions });
export const DOORS_STRIP = [
  J('fs_ouest', 'steel_strip', 0, 10, 1, 10, 'c_strip', 'Vers Center-Town'),
  J('c_strip', 'steel_center', 14, 0, 14, 1, 'fs_ouest', 'Fréquence Strip'),
];
const P = (id, name, sprite, x, z, faceTo) => ({ id, name, sprite, location: 'steel_strip', x, z, faceTo, dialogue: id });
export const NPCS_STRIP = [ // aucun n'est Vibes ni Tron ; positions hors de l'ombre d'écran des façades sud (view.masques() vide)
  P('fs_rocco', 'Rocco', 'gen_fs_rocco', 16, 9, [16, 14]),
  P('fs_lila', 'Lila', 'gen_fs_lila', 22.5, 8, [20, 12]),
  P('fs_hugo', 'Hugo', 'gen_fs_hugo', 44, 8.4, [42, 12]),
  P('fs_sacha', 'Sacha', 'gen_fs_sacha', 49.6, 8, [48, 12]),
  P('fs_okoro', 'Mme Okoro', 'gen_fs_okoro', 14.2, 14.4, [20, 14]),
  P('fs_tibo', 'Tibo', 'gen_fs_tibo', 52, 10.5, [48, 14]),
  P('fs_yun', 'Yun', 'gen_fs_yun', 12.6, 15.6, [10, 12]),
  P('fs_gt', 'GT de promotion', 'gen_fs_gt_promo', 32, 12, [28, 12]),
  // Fusible (fiche Mega-Line d'Ocre) : vendeur du Pique-Puce, au fond de la ruelle noire x 8-10 fermée par fs_bouche_nord (aucune enseigne ni lueur), loin du merch et de la caméra
  P('fs_fusible', 'Fusible', 'gen_ml_fusible', 9, 5.4, [9, 9]),
  P('fs_ocre', 'Ocre', 'gen_fs_ocre', 27.4, 18.6, [30, 23.4]), // caméo du studio, sans mécanique, devant sa fresque
  P('fs_marius', 'Vieux Marius', 'gen_fs_marius', 61.4, 16.4, [56, 12]),
  // compléments d'Ocre : grappe devant L'Effeuillée (étalée le long de l'horizontale de l'écran : étiquettes côte à côte), rabatteuse des cabines et son patron un peu en retrait, patrouille qui regarde ailleurs
  P('fs_rouge', 'Rouge', 'gen_fs_rouge', 53.6, 9.4, [57, 12]),
  P('fs_rubis', 'Rubis', 'gen_fs_rubis', 59.4, 6.9, [55, 12]),
  P('fs_fourrure', 'Zibeline', 'gen_fs_fourrure', 56.4, 7.6, [58, 13]),
  P('fs_racoleur', 'Le rabatteur', 'gen_fs_racoleur', 64, 8, [60, 12]),
  P('fs_racoleuse', 'La rabatteuse', 'gen_fs_racoleuse', 43.8, 16, [41, 13]),
  P('fs_mac', 'Monsieur Velours', 'gen_fs_mac', 45.2, 15.6, [43.8, 16]),
  P('fs_flic_a', 'Agente Brehm', 'gen_fs_flic_a', 65, 12.2, [74, 16]),
  P('fs_flic_b', 'Agent Kessler', 'gen_fs_flic_b', 69.4, 12.4, [74, 17]),
];
const D = (t1, t2) => ({ start: { text: t1, options: [ { label: 'Et sinon ?', next: 'b' }, { label: 'Au revoir.', next: 'end' } ] }, b: { text: t2, options: [ { label: 'Au revoir.', next: 'end' } ] } });
const D4 = (...t) => Object.fromEntries(t.map((x, i) => [i ? 'r' + i : 'start', { text: x, options: [ ...(i < t.length - 1 ? [{ label: 'Et sinon ?', next: 'r' + (i + 1) }] : []), { label: 'Au revoir.', next: 'end' } ] }]));
export const DIALOGUES_STRIP = {
  fs_ocre: D4('Recule un peu, tu me fais de l\u2019ombre. Et ton ombre n\u2019a aucun talent.', 'Non, elle n\u2019a pas posé pour moi. Personne ne l\u2019a jamais vue poser. J\u2019ai mieux que ça, j\u2019ai de la mémoire.',
    'Les vigiles ? Ils adorent la fresque. Ils font semblant de ne pas me voir depuis trois nuits.', 'Toi, je te mettrais bien dans un coin du mur. Tout petit. Personne ne regarde jamais les coins, et c\u2019est là que je cache les meilleurs.'),
  // Fusible : 7 répliques de la fiche d'Ocre ; vend le Pique-Puce (prix proposé, non validé : PIQUE_PUCE_PRIX), un seul exemplaire à la fois
  fs_fusible: {
    start: { text: 'Tu cherches la rame sans la puce ? Parle moins fort, le néon d\u2019à côté a des oreilles.', alt: [
        { if: 'race_augmente', text: 'Toi, tu as déjà ce qu\u2019il faut sous la peau. Qu\u2019est-ce que tu viens faire dans ma ruelle ?' },
        { if: 'race_cyborg', text: 'Toi, tu as déjà ce qu\u2019il faut sous la peau. Qu\u2019est-ce que tu viens faire dans ma ruelle ?' },
        { if: 'fusible_vendu', text: 'Tu ne m\u2019as jamais vu. Et moi je n\u2019ai jamais rien vendu.' } ], options: [
      { label: 'Combien, la boîte ?', next: 'prix', if: 'pirate_implant<1' },
      { label: 'Ça marche à tous les coups ?', next: 'fiable' },
      { label: 'Au revoir.', next: 'end' } ] },
    prix: { text: 'Six cents. C\u2019est le prix d\u2019un aller simple pour avoir l\u2019air de quelqu\u2019un d\u2019autre.', alt: [
        { if: 'race_mutant', text: 'Six cents. Elle va te mordre un peu au contact. Les portiques n\u2019aiment pas les gens comme nous, et la boîte non plus.' } ], options: [
      { label: `Je la prends (${PIQUE_PUCE_PRIX} cr).`, action: `paycr:${PIQUE_PUCE_PRIX};give:pirate_implant;flag:fusible_vendu`, next: 'vendu', poor: 'pauvre' },
      { label: 'Trop cher.', next: 'end' } ] },
    vendu: { text: 'Si ça chauffe dans ta poche, jette-la. Ne me rapporte pas les morceaux.', options: [ { label: 'Au revoir.', next: 'end' } ] },
    fiable: { text: 'Ça ne marche pas à tous les coups. Neuf fois sur dix, ce qui est mieux que la plupart des gens.', options: [ { label: 'Combien ?', next: 'prix', if: 'pirate_implant<1' }, { label: 'Au revoir.', next: 'end' } ] },
    pauvre: { text: 'Reviens avec six cents crédits. Je ne fais pas crédit, justement.', options: [ { label: 'Au revoir.', next: 'end' } ] },
  },
  fs_rocco: D('Le scanner dit que ton sourire est à soixante pour cent. Il faut quatre-vingts. Reviens quand tu seras content.', 'Moi je ne choisis personne. C\u2019est la machine. Je me contente d\u2019être grand.'),
  fs_lila: D('Douze sets cette semaine. Dans le contrat, il y a une clause sur le sourire. Je l\u2019ai lue deux fois pour être sûre.', 'Ils passent « Danse, sois plus chrome » toutes les heures. Je crois qu\u2019au bout d\u2019un moment, plus personne n\u2019entend les paroles.'),
  fs_hugo: D('J\u2019attends depuis six heures. Le concert du 31, c\u2019est ce soir ou dans un an, personne n\u2019est sûr.', 'Si elle passe en vrai, tu crois qu\u2019on la reconnaîtra ? Personne ne sait à quoi elle ressemble sans le chapeau.'),
  fs_okoro: D('Ici on baisse le son. Les gens viennent pour s\u2019entendre penser, et ça, la rue ne le fait plus.', 'Les caméras du Strip ne marchent pas, c\u2019est écrit dessus. Moi, je fais comme si elles marchaient.'),
  fs_tibo: D('La casquette officielle coûte trois fois plus et elle déteint pareil.', 'Tu peux t\u2019éloigner un peu ? Tu attires les drones, et moi je n\u2019ai pas de licence.'),
  fs_yun: D('Brochettes de quoi ? De protéines. C\u2019est marqué sur le carton, et le carton, je ne l\u2019ai pas écrit.', 'À l\u2019heure où le Neon-7 ferme, je vends trois fois plus. Les gens sortent avec faim et sans sourire.'),
  fs_gt: D('Bonsoir. Je suis ici pour vous rappeler qu\u2019il y a un concert. Il y a toujours un concert.', 'Je n\u2019ai pas d\u2019avis. Mon modèle n\u2019en avait pas en option.'),
  fs_sacha: D('Tron chante en direct, enfin c\u2019est ce qu\u2019on dit. Moi je règle le son, je ne vérifie rien.', 'La salle tient mille personnes. Le soir où le système de sync a planté, il en restait trois cents qui applaudissaient.'),
  fs_marius: D('Avant les écrans, le Strip s\u2019appelait autrement. Je ne me souviens plus comment. C\u2019est peut-être ça, le but.', 'Un conseil : la nuit, ne regarde pas les pubs dans les yeux. Elles te reconnaissent.'),
  fs_rouge: D4('Je m\u2019appelle Rouge. Comme les néons, comme le feu, comme toi quand tu me regardes trop longtemps.', 'Ici on vend du temps, mon chou. Le reste, c\u2019est toi qui l\u2019imagines.', 'Les caméras ne marchent pas. Moi si, mais pas pour toi ce soir.'),
  fs_rubis: D4('Rubis. Un vrai, pas un synthétique. Enfin, c\u2019est ce que dit l\u2019étiquette.', 'Au Neon-7 ils paient le sourire. Ici aussi, sauf qu\u2019on sait le faire semblant.'),
  fs_fourrure: D4('C\u2019est de la fausse fourrure. Tout est faux ici, c\u2019est pour ça que c\u2019est honnête.', 'Tu hésites ? Ceux qui hésitent sont ceux qui reviennent.', 'Garde tes crédits pour le taxi. On rentre toujours plus léger qu\u2019on est venu.'),
  fs_racoleur: D4('Entrée libre, sortie payante ! Je plaisante. À moitié.', 'L\u2019Effeuillée, spectacle de minuit. Les fauteuils du fond sont réservés aux timides.'),
  fs_racoleuse: D4('Cabines sans C.A.G.E. : pas de caméra, pas de garde, pas d\u2019engagement. Juste un rideau.', 'Trois minutes, c\u2019est le tarif de base. Au-delà, c\u2019est toi qui comptes.', 'Si tu cherches quelqu\u2019un, tu ne le trouveras pas ici. Si tu cherches à oublier quelqu\u2019un, entre.'),
  fs_mac: D4('Je ne vends rien. Je loue de la tranquillité, au quart d\u2019heure.', 'Ici, chacun choisit ses clients. Moi, je choisis les flics.', 'Tu poses beaucoup de questions pour quelqu\u2019un qui garde les mains dans les poches.'),
  fs_flic_a: D4('Circulez. Il n\u2019y a rien à voir, et je suis payée pour ne pas le voir.', 'Le Strip ? Zone calme. C\u2019est dans le rapport. Je l\u2019ai écrit moi-même.'),
  fs_flic_b: D4('Ma collègue surveille la rue, moi je surveille ma collègue. Comme ça, personne ne surveille rien.', 'Une enveloppe ? Quelle enveloppe ? Ah, celle-là. Elle est tombée toute seule.'),
};
