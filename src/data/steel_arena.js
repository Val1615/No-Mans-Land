// Steel Arena (zone steel_arena, 56 x 40 m, quartier de Center-Town). Pack d'Ocre : docs/villes/steel/quartiers/steel_arena/ (STEEL_ARENA.md, ASSETS.md).
// [décision] entrée ouest par la grille du bout est du Fréquence Strip (aller-retour) ; le parvis se visite, le dôme reste fermé (réplique au clic).
// Vibes et Tron n'apparaissent que sur les écrans du dôme (ar_ens_ecran_vibes, ar_ens_ecran_tron). Aucun nom civil.
// Animations : les 4 faisceaux = un groupe synchronisé (une seule place dans le plafond mobile de 8), décalés d'une image ; un seul cœur animé dans la file.
const ARENA = { bg: '#060a10', hemi: ['#7a90ff', '#1a1030', 1.2], sun: ['#5fd3f0', 0.6], tint: '#a0a8d0', actor: '#d8dcf0' };
const VIOLET = '#8a3cff', CYAN = '#5fd3f0', MAGENTA = '#e03ca8', BLANC = '#e8eef2', ROUGE = '#c8323c';
const B = (id, label, sprite, x, z, w, d, extra = {}) => ({ id, label, sprite, x, z, w, d, visitable: false, cue: null, named: !!label, ...extra });
const ENS = (id, sprite, x, z, y, extra = {}) => B(id, '', sprite, x - 0.1, z - 0.1, 0.2, 0.2, { y, solid: [], named: false, ...extra });
const PROJ = [[2, 0], [52, 0], [2, 10], [52, 10]], LAMP = [[9, 15], [47, 15], [9, 27], [49, 27]];
export const BUILDINGS_ARENA = [
  B('ar_arena', 'Steel Arena', 'ar_arena', 4, 0, 48, 12, { tint: '#ffffff' }),
  B('ar_entree', 'Entrée de l\u2019Arena', 'ar_entree', 22, 12, 8, 2),
  ...[22, 24, 26, 28].map((x, i) => B(`ar_portique${i}`, i === 1 ? 'Portiques Human Corp' : '', 'ar_portique', x, 14, 2, 1, { named: i === 1, tint: '#ffffff' })), // portiques blancs, lisibles
  B('ar_bar0', '', 'ar_barriere', 22, 17, 4, 0.5, { named: false }), B('ar_bar1', '', 'ar_barriere', 26, 20, 4, 0.5, { named: false }), B('ar_bar2', '', 'ar_barriere', 22, 23, 4, 0.5, { named: false }),
  ...PROJ.map(([x, z], i) => B(`ar_proj${i}`, '', 'ar_projecteur', x, z, 2, 2, { named: false })),
  ...LAMP.map(([x, z], i) => B(`ar_lamp${i}`, '', 'ar_lampadaire', x - 0.3, z - 0.3, 0.6, 0.6, { named: false })),
  B('ar_guichets', 'Guichets', 'ar_guichets', 6, 20, 4, 4),
  B('ar_merch', 'Merch officiel', 'ar_merch', 46, 20, 4, 4),
  B('ar_securite', 'Poste Human Corp', 'ar_securite', 14, 26, 4, 4),
  B('ar_regie', 'Camion régie', 'ar_regie', 44, 26, 6, 4),
  B('ar_panneau', 'Panneau', 'ar_panneau_nml', 50, 36, 2, 0.5),
  B('ar_cam', '', 'pp_camera', 26.8, 28.8, 0.4, 0.4, { named: false }),
  // enseignes animées (7 places au plus dans le plafond mobile)
  ENS('ar_e_vibes', 'ar_ens_ecran_vibes', 14, 12.2, 5), ENS('ar_e_tron', 'ar_ens_ecran_tron', 42, 12.2, 5),
  ENS('ar_e_fronton', 'ar_ens_fronton', 29.6, 14.2, 4.4), ENS('ar_e_hc', 'ar_ens_human_corp', 17.6, 30.2, 2.6),
  ENS('ar_e_guichet', 'ar_ens_guichet', 9.6, 24.2, 2.0),
  ...PROJ.map(([x, z], i) => ENS(`ar_e_faisceau${i}`, 'ar_ens_faisceau', x + 1.9, z + 2.1, 3.6, { groupe: 'faisceaux', ph: i })),
  ...[[24, 18.3], [28, 18.8], [24.5, 21.6], [29, 22.4]].map(([x, z], i) => ENS(`ar_e_coeur${i}`, 'ar_ens_coeurs', x, z, 1.5, { fige: i > 0, ph: 0 })),
];
export const CLOSED_ARENA = {
  ar_arena: 'Le dôme de la Steel Arena. « Live tonight. » Une basse sourde fait vibrer les barrières. Les portes ne s\u2019ouvrent pas pour toi ce soir.',
  ar_entree: 'L\u2019entrée vitrée. « Human Corp sponsorise le sourire. » Derrière, une clameur monte et s\u2019arrête net.',
  ar_portique1: 'Les portiques blancs de Human Corp. « Building a better tomorrow. Tous les rythmes appartiennent à Human Corp. »',
  ar_guichets: 'Les guichets. L\u2019écran annonce le Festival Pulse of Steel, le 14/11. Complet.',
  ar_merch: 'Merch officiel Human Corp. Les prix s\u2019affichent selon ton score d\u2019engagement.',
  ar_securite: 'Le poste de sécurité Human Corp. Une vitre teintée qui te regarde.',
  ar_regie: 'Le camion régie. Des câbles partent vers le dôme comme des racines.',
  ar_panneau: '« Au-delà de ce point : pas de droits, pas de loi, pas de retour. »',
};
export const LOCATIONS_ARENA = {
  steel_arena: { id: 'steel_arena', name: 'Steel-Megalopolis · Steel Arena', kind: 'exterior', size: { w: 56, d: 40 }, light: ARENA,
    ground: { base: '#10121a', skin: 'g_ar_parvis_mouille', tileM: 4, clean: true, zones: [
      { x: 0, z: 14, w: 56, d: 26, kind: 'plate', skin: 'g_ar_parvis', tileM: 4 }, { x: 0, z: 32, w: 30, d: 8, kind: 'plate', skin: 'g_ar_parvis_mouille', tileM: 4 },
      { x: 22, z: 15, w: 8, d: 9, kind: 'plate', skin: 'g_ar_ligne_file', tileM: 4 } ] },
    buildings: BUILDINGS_ARENA, props: [],
    glows: [
      { x: 14, z: 13, rx: 5, rz: 2, color: VIOLET, i: 0.85, flicker: true }, { x: 42, z: 13, rx: 5, rz: 2, color: CYAN, i: 0.8, flicker: true },
      { x: 26, z: 15, rx: 5, rz: 1.6, color: BLANC, i: 0.55 }, { x: 26, z: 19.5, rx: 4.5, rz: 5, color: CYAN, i: 0.35 },
      ...PROJ.map(([x, z]) => ({ x: x + 1, z: z + 2.2, rx: 2.4, rz: 1.6, color: CYAN, i: 0.6, flicker: true })),
      ...LAMP.map(([x, z]) => ({ x, z: z + 0.6, rx: 2.4, rz: 1.8, color: VIOLET, i: 0.7 })),
      { x: 26, z: 21, rx: 3, rz: 3, color: MAGENTA, i: 0.4, flicker: true }, { x: 16, z: 30.6, rx: 2.2, rz: 1.2, color: BLANC, i: 0.5 },
      { x: 27, z: 29.4, rx: 0.6, rz: 0.4, color: ROUGE, i: 0.5 }, { x: 51, z: 37, rx: 2, rz: 1.4, color: ROUGE, i: 0.3 } ],
    extras: [ ...[[23, 15.6], [27.6, 15.6], [29, 18.4], [23, 19.2], [27, 21.8], [23.4, 22.5], [29.4, 23.2], [12, 25], [38, 18]].map(([x, z], i) => ({ sprite: i % 2 ? 'gen_ar_foule_b' : 'gen_ar_foule_a', x, z, face: i % 3 ? 1 : -1, role: 'foule' })) ],
    walkers: [ { sprite: 'gen_ar_foule_a', path: [[2, 21], [20, 21], [20, 30], [2, 30]], speed: 0.6, t0: 3 }, { sprite: 'gen_ar_foule_b', path: [[34, 18], [52, 18], [52, 32], [34, 32]], speed: 0.6, t0: 10 } ],
    spawn: { player: { x: 1, z: 21 }, companion: { x: 1, z: 22 } }, city: 'steel',
    arrive: { from: 'steel_strip', text: 'La Steel Arena. Le dôme noir mange tout le nord ; quatre faisceaux cyan balaient le plafond du sarcophage. « Human Corp sponsorise le sourire. »' } },
};
const J = (id, loc, ox, oz, tx, tz, to, label, conditions = []) => ({ id, location: loc, junction: true, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: { doorId: to }, conditions });
export const DOORS_ARENA = [
  J('ar_ouest', 'steel_arena', 0, 21, 1, 21, 'fs_est', 'Fréquence Strip'),
  J('fs_est', 'steel_strip', 64, 13, 63, 13, 'ar_ouest', 'La grille de l\u2019Arena'),
];
export const NPCS_ARENA = [ // positions de la fiche (m), décalées hors des portiques et des projecteurs ; aucun n'est Vibes ni Tron
  { id: 'ar_ferrand', name: 'Ferrand', sprite: 'gen_ar_ferrand', location: 'steel_arena', x: 31, z: 14.6, faceTo: [26, 18], dialogue: 'ar_ferrand' },
  { id: 'ar_anouk', name: 'Anouk', sprite: 'gen_ar_anouk', location: 'steel_arena', x: 8, z: 24.8, faceTo: [8, 28], dialogue: 'ar_anouk' },
  { id: 'ar_zelie', name: 'Zélie', sprite: 'gen_ar_zelie', location: 'steel_arena', x: 9, z: 28.4, faceTo: [14, 24], dialogue: 'ar_zelie' },
  { id: 'ar_malik', name: 'Malik', sprite: 'gen_ar_malik', location: 'steel_arena', x: 45, z: 31, faceTo: [40, 26], dialogue: 'ar_malik' },
  { id: 'ar_ines', name: 'Inès', sprite: 'gen_ar_ines', location: 'steel_arena', x: 24, z: 18.6, faceTo: [26, 14], dialogue: 'ar_ines' },
  { id: 'ar_clem', name: 'Clém', sprite: 'gen_ar_clem', location: 'steel_arena', x: 32, z: 16, faceTo: [26, 20], dialogue: 'ar_clem' },
  { id: 'ar_garnier', name: 'Agent Garnier', sprite: 'gen_ar_garnier', location: 'steel_arena', x: 19, z: 28, faceTo: [24, 28], dialogue: 'ar_garnier' },
  { id: 'ar_bastien', name: 'Bastien', sprite: 'gen_ar_bastien', location: 'steel_arena', x: 51, z: 13, faceTo: [46, 16], dialogue: 'ar_bastien' },
  { id: 'ar_laure', name: 'Madame Laure', sprite: 'gen_ar_laure', location: 'steel_arena', x: 49, z: 37.4, faceTo: [44, 34], dialogue: 'ar_laure' },
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
};
