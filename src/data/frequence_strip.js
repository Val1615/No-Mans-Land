// Fréquence Strip (zone steel_strip, 64 x 24 m, quartier de Center-Town). Pack d'Ocre : docs/villes/steel/quartiers/frequence_strip/ (FREQUENCE_STRIP.md, ASSETS.md).
// [décision] ouverte à l'ouest sur la sortie est de Pulse Plaza ; bout est : grille ouverte vers la Steel Arena (fs_est). Neon-7 et Core Stack fermés pour l'instant.
// Groovy-Tron et Groovy Vibes n'apparaissent que sur des écrans (enseignes fs_ens_tron, fs_ens_vibes) : jamais rencontrés. Aucun nom civil.
// Enseignes animées : planches du manifeste (frames, frame_px, fps), lues par view.js ; au plus 8 animations visibles à la fois sur mobile.
const STRIP = { bg: '#060a10', hemi: ['#e070c0', '#2a1030', 1.3], sun: ['#f2b44a', 0.55], tint: '#c8a0c0', actor: '#e8d0e0' }; // plus chaud que Pulse Plaza : magenta et ambre
const MAGENTA = '#e03ca8', VIOLET = '#8a3cff', CYAN = '#a9d2e6', AMBRE = '#f2b44a', VELOURS = '#7a1428';
const B = (id, label, sprite, x, z, w, d, extra = {}) => ({ id, label, sprite, x, z, w, d, visitable: false, cue: null, named: !!label, ...extra });
const ENS = (id, sprite, x, z, y) => B(id, '', sprite, x - 0.1, z - 0.1, 0.2, 0.2, { y, solid: [], named: false }); // enseigne : point de pose (x, z) au pied de la façade, hauteur y (m)
export const BUILDINGS_STRIP = [
  // façades nord (z 0-6) : la rue court d'ouest en est
  B('fs_fn0', '', 'fs_facade_nord', 0, 0, 8, 6, { named: false }),
  B('fs_neon7', 'Club Neon-7', 'fs_neon7', 10, 0, 12, 6),
  B('fs_fn1', '', 'fs_facade_nord', 22, 0, 8, 6, { named: false }), B('fs_fn2', '', 'fs_facade_nord', 30, 0, 8, 6, { named: false }),
  B('fs_corestack', 'Core Stack', 'fs_corestack', 38, 0, 12, 6),
  B('fs_fn3', '', 'fs_facade_nord', 50, 0, 8, 6, { named: false }), B('fs_fn4', '', 'fs_facade_nord', 58, 0, 6, 6, { named: false }),
  // façades sud (z 18-24)
  B('fs_fs0', '', 'fs_facade_sud', 0, 18, 8, 6, { named: false }), B('fs_fs1', '', 'fs_facade_sud', 8, 18, 8, 6, { named: false }),
  B('fs_retour', 'Le Retour', 'fs_retour', 16, 18, 8, 6),
  B('fs_fs2', '', 'fs_facade_sud', 24, 18, 8, 6, { named: false }), B('fs_fs3', '', 'fs_facade_sud', 32, 18, 8, 6, { named: false }),
  B('fs_fs4', '', 'fs_facade_sud', 40, 18, 8, 6, { named: false }), B('fs_fs5', '', 'fs_facade_sud', 48, 18, 6, 6, { named: false }),
  B('fs_capsules', 'Hôtel capsule', 'fs_capsules', 54, 18, 6, 6),
  B('fs_fs6', '', 'fs_facade_sud', 60, 18, 4, 6, { named: false }),
  // rue
  B('fs_tapis', '', 'fs_tapis', 14, 6, 4, 2, { solid: [], named: false }),
  B('fs_stand_brochettes', 'Brochettes de Yun', 'fs_stand_brochettes', 8, 14, 4, 4),
  B('fs_stand_merch', 'Merch « pas tout à fait officiel »', 'fs_stand_merch', 46, 14, 4, 4),
  B('fs_cam', '', 'pp_camera', 24.8, 14.8, 0.4, 0.4, { named: false }),
  B('fs_grille_est', 'Grille de l\u2019Arena', 'fs_grille_est', 60, 11, 4, 1, { solid: [] }), // ouverte : mène à la Steel Arena (fs_est)
  // enseignes animées : 4 en façade nord (Neon-7, Core Stack, Vibes, cœur), Tron au milieu, 2 côté sud (Retour, capsules), 2 panaches de vapeur
  ENS('fs_e_neon7', 'fs_ens_neon7', 20, 6.2, 3.6), ENS('fs_e_core', 'fs_ens_corestack', 48, 6.2, 3.4),
  ENS('fs_e_vibes', 'fs_ens_vibes', 28.4, 6.2, 1.2), ENS('fs_e_coeur', 'fs_ens_coeur', 6.4, 6.2, 2.6),
  ENS('fs_e_tron', 'fs_ens_tron', 36.4, 6.2, 1.2),
  ENS('fs_e_retour', 'fs_ens_retour', 20, 24.2, 3.4), ENS('fs_e_capsules', 'fs_ens_capsules', 57, 24.2, 2.4),
  ENS('fs_vap0', 'fs_vapeur', 5, 11, 0), ENS('fs_vap1', 'fs_vapeur', 57, 11, 0),
];
export const CLOSED_STRIP = {
  fs_neon7: 'Club Neon-7. « Next Drop. Entrée : sourire calibré. » Le portique au-dessus de la porte te scanne et ne s\u2019ouvre pas.',
  fs_corestack: 'Core Stack. Une affiche : 31/10. Les baies ronronnent derrière la porte, fermée.',
  fs_retour: 'Le Retour. Lumière ambre, musique basse. Fermé pour l\u2019instant.',
  fs_capsules: 'Hôtel capsule. Des cases empilées, quelques hublots allumés. Complet.',
  fs_grille_est: 'La grille du bout de la rue, ouverte. Derrière, le dôme de l\u2019Arena et une foule qui gronde.',
};
export const LOCATIONS_STRIP = {
  steel_strip: { id: 'steel_strip', name: 'Steel-Megalopolis · Fréquence Strip', kind: 'exterior', size: { w: 64, d: 24 }, light: STRIP,
    ground: { base: '#140e16', skin: 'g_fs_asphalte_mouille', tileM: 4, clean: true, zones: [
      { x: 0, z: 6, w: 64, d: 2, kind: 'plate', skin: 'g_fs_trottoir', tileM: 4 }, { x: 0, z: 16, w: 64, d: 2, kind: 'plate', skin: 'g_fs_trottoir', tileM: 4 },
      // grilles vapeur : trois plaques isolées, une tuile chacune (jamais en motif)
      { x: 4, z: 10, w: 2, d: 2, kind: 'plate', skin: 'g_fs_grille_vapeur', tileM: 2 }, { x: 56, z: 10, w: 2, d: 2, kind: 'plate', skin: 'g_fs_grille_vapeur', tileM: 2 },
      { x: 35, z: 13, w: 2, d: 2, kind: 'plate', skin: 'g_fs_grille_vapeur', tileM: 2 } ] },
    buildings: BUILDINGS_STRIP, props: [],
    glows: [
      { x: 16, z: 7.5, rx: 6, rz: 2.4, color: MAGENTA, i: 0.9, flicker: true }, { x: 16, z: 7, rx: 2.2, rz: 1, color: VELOURS, i: 0.7 },
      { x: 44, z: 7.5, rx: 6, rz: 2.4, color: CYAN, i: 0.75, flicker: true }, { x: 26, z: 7.4, rx: 2.4, rz: 1.6, color: VIOLET, i: 0.8, flicker: true },
      { x: 34, z: 7.4, rx: 2.4, rz: 1.6, color: VIOLET, i: 0.8, flicker: true }, { x: 4, z: 7.4, rx: 2.2, rz: 1.4, color: MAGENTA, i: 0.75, flicker: true },
      { x: 20, z: 16.6, rx: 3.6, rz: 1.6, color: AMBRE, i: 0.75 }, { x: 10, z: 13.4, rx: 2.4, rz: 1.4, color: AMBRE, i: 0.7, flicker: true },
      { x: 48, z: 13.4, rx: 2.4, rz: 1.4, color: MAGENTA, i: 0.6 }, { x: 57, z: 16.6, rx: 2, rz: 1.2, color: CYAN, i: 0.5 },
      { x: 32, z: 12, rx: 30, rz: 4, color: MAGENTA, i: 0.18 }, { x: 25, z: 15.4, rx: 0.6, rz: 0.4, color: '#c8323c', i: 0.5 } ],
    extras: [ ...[[12, 8.6], [13, 9.4], [19.5, 8.8], [42, 7.4], [43, 7.6], [45, 7.2], [46.5, 7.6], [30, 15], [53, 12.6]].map(([x, z], i) => ({ sprite: i % 2 ? 'gen_fs_foule_b' : 'gen_fs_foule_a', x, z, face: i % 3 ? 1 : -1, role: 'foule' })) ],
    walkers: [ { sprite: 'gen_fs_foule_a', path: [[2, 12], [58, 12]], speed: 0.8, t0: 2 }, { sprite: 'gen_fs_foule_b', path: [[58, 9.5], [3, 9.5]], speed: 0.7, t0: 8 } ],
    spawn: { player: { x: 1, z: 10 }, companion: { x: 1, z: 11 } }, city: 'steel',
    arrive: { from: 'steel_pulse', text: 'Fréquence Strip. Néons mouillés, publicités qui chantent plus fort que les gens. Deux basses se battent au milieu de la rue.' } },
};
const J = (id, loc, ox, oz, tx, tz, to, label, conditions = []) => ({ id, location: loc, junction: true, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: { doorId: to }, conditions });
export const DOORS_STRIP = [
  J('fs_ouest', 'steel_strip', 0, 10, 1, 10, 'pp_est', 'Pulse Plaza'),
  J('pp_est', 'steel_pulse', 48, 13, 47, 13, 'fs_ouest', 'Fréquence Strip'),
];
export const NPCS_STRIP = [ // positions de la fiche (m) ; aucun n'est Vibes ni Tron
  { id: 'fs_rocco', name: 'Rocco', sprite: 'gen_fs_rocco', location: 'steel_strip', x: 16, z: 9, faceTo: [16, 14], dialogue: 'fs_rocco' },
  { id: 'fs_lila', name: 'Lila', sprite: 'gen_fs_lila', location: 'steel_strip', x: 22.5, z: 8, faceTo: [20, 12], dialogue: 'fs_lila' },
  { id: 'fs_hugo', name: 'Hugo', sprite: 'gen_fs_hugo', location: 'steel_strip', x: 44, z: 8.4, faceTo: [42, 12], dialogue: 'fs_hugo' },
  { id: 'fs_sacha', name: 'Sacha', sprite: 'gen_fs_sacha', location: 'steel_strip', x: 50.5, z: 8, faceTo: [48, 12], dialogue: 'fs_sacha' },
  { id: 'fs_okoro', name: 'Mme Okoro', sprite: 'gen_fs_okoro', location: 'steel_strip', x: 20, z: 16.8, faceTo: [20, 12], dialogue: 'fs_okoro' },
  { id: 'fs_tibo', name: 'Tibo', sprite: 'gen_fs_tibo', location: 'steel_strip', x: 48, z: 13.2, faceTo: [48, 10], dialogue: 'fs_tibo' },
  { id: 'fs_yun', name: 'Yun', sprite: 'gen_fs_yun', location: 'steel_strip', x: 10, z: 13.2, faceTo: [10, 10], dialogue: 'fs_yun' },
  { id: 'fs_gt', name: 'GT de promotion', sprite: 'gen_fs_gt_promo', location: 'steel_strip', x: 32, z: 12, faceTo: [28, 12], dialogue: 'fs_gt' },
  { id: 'fs_marius', name: 'Vieux Marius', sprite: 'gen_fs_marius', location: 'steel_strip', x: 58, z: 16.6, faceTo: [56, 12], dialogue: 'fs_marius' },
];
const D = (t1, t2) => ({ start: { text: t1, options: [ { label: 'Et sinon ?', next: 'b' }, { label: 'Au revoir.', next: 'end' } ] }, b: { text: t2, options: [ { label: 'Au revoir.', next: 'end' } ] } });
export const DIALOGUES_STRIP = {
  fs_rocco: D('Le scanner dit que ton sourire est à soixante pour cent. Il faut quatre-vingts. Reviens quand tu seras content.', 'Moi je ne choisis personne. C\u2019est la machine. Je me contente d\u2019être grand.'),
  fs_lila: D('Douze sets cette semaine. Dans le contrat, il y a une clause sur le sourire. Je l\u2019ai lue deux fois pour être sûre.', 'Ils passent « Danse, sois plus chrome » toutes les heures. Je crois qu\u2019au bout d\u2019un moment, plus personne n\u2019entend les paroles.'),
  fs_hugo: D('J\u2019attends depuis six heures. Le concert du 31, c\u2019est ce soir ou dans un an, personne n\u2019est sûr.', 'Si elle passe en vrai, tu crois qu\u2019on la reconnaîtra ? Personne ne sait à quoi elle ressemble sans le chapeau.'),
  fs_okoro: D('Ici on baisse le son. Les gens viennent pour s\u2019entendre penser, et ça, la rue ne le fait plus.', 'Les caméras du Strip ne marchent pas, c\u2019est écrit dessus. Moi, je fais comme si elles marchaient.'),
  fs_tibo: D('La casquette officielle coûte trois fois plus et elle déteint pareil.', 'Tu peux t\u2019éloigner un peu ? Tu attires les drones, et moi je n\u2019ai pas de licence.'),
  fs_yun: D('Brochettes de quoi ? De protéines. C\u2019est marqué sur le carton, et le carton, je ne l\u2019ai pas écrit.', 'À l\u2019heure où le Neon-7 ferme, je vends trois fois plus. Les gens sortent avec faim et sans sourire.'),
  fs_gt: D('Bonsoir. Je suis ici pour vous rappeler qu\u2019il y a un concert. Il y a toujours un concert.', 'Je n\u2019ai pas d\u2019avis. Mon modèle n\u2019en avait pas en option.'),
  fs_sacha: D('Tron chante en direct, enfin c\u2019est ce qu\u2019on dit. Moi je règle le son, je ne vérifie rien.', 'La salle tient mille personnes. Le soir où le système de sync a planté, il en restait trois cents qui applaudissaient.'),
  fs_marius: D('Avant les écrans, le Strip s\u2019appelait autrement. Je ne me souviens plus comment. C\u2019est peut-être ça, le but.', 'Un conseil : la nuit, ne regarde pas les pubs dans les yeux. Elles te reconnaissent.'),
};
