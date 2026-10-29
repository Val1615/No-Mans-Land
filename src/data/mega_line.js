// Mega-Line (zone steel_megaline, 48 x 24 m) et terminus de fret (zone steel_terminus, 30 x 20 m). Pack d'Ocre : docs/villes/steel/quartiers/mega_line/.
// [proposition] porte c_mega au nord de steel_center (8 ; 0) ; passerelle de service au fond de la ligne vers le terminus (à pied, aller-retour).
// [décision Valentin] terminus : portes massives pleines et fermées, aucune vue sur le désert ; panneau « Dernier arrêt avant No Man's Land » affiché par le code.
// Vibes et Tron : uniquement sur les écrans de quai. Budget mobile : ligne 5 au plus (écrans en groupe, horaires, logo, rame, lueurs), terminus 3.
const LIGNE = { bg: '#070910', hemi: ['#a890d8', '#1a1420', 1.2], sun: ['#f2b44a', 0.55], tint: '#b0a8c8', actor: '#dcd6e8' };
const FRET = { bg: '#0a0a0a', hemi: ['#c8b8a0', '#181410', 1.05], sun: ['#e8a040', 0.5], tint: '#c0b4a0', actor: '#dcd0c0' }; // béton, ambre ; ni ciel ni sable
const VIOLET = '#8a3cff', MAGENTA = '#e03ca8', CYAN = '#5fd3f0', AMBRE = '#f2b44a', ORANGE = '#ff8a2a', ROUGE = '#c8323c';
const B = (id, label, sprite, x, z, w, d, extra = {}) => ({ id, label, sprite, x, z, w, d, visitable: false, cue: null, named: !!label, ...extra });
const ENS = (id, sprite, x, z, y, extra = {}) => B(id, '', sprite, x - 0.1, z - 0.1, 0.2, 0.2, { y, solid: [], named: false, ...extra });
const LAMPS = [[4, 14], [44, 14], [12, 20.5], [36, 20.5]];
export const BUILDINGS_MEGA = [
  B('ml_viaduc0', '', 'ml_viaduc', 0, 4, 24, 3, { solid: [], named: false }), B('ml_viaduc1', 'Viaduc de la Mega-Line', 'ml_viaduc', 24, 4, 24, 3, { solid: [] }),
  B('ml_rame', '', 'ml_rame', 12, 4, 24, 3, { solid: [], named: false, y: 3.2, defile: { dx: 72, passage: 9, periode: 40 } }), // rame déplacée par le code, ne s'arrête pas (pas de billet)
  B('ml_station', 'Station de la Mega-Line', 'ml_station', 14, 7.5, 20, 6),
  B('ml_tableau', 'Tableau des départs', 'ml_tableau', 25, 14, 2.4, 0.4),
  B('ml_borne', 'Borne de billets', 'ml_borne', 38.6, 15, 0.8, 0.6),
  B('ml_banc0', '', 'ml_banc', 4, 16.4, 2, 0.6, { named: false }), B('ml_banc1', '', 'ml_banc', 30, 17, 2, 0.6, { named: false }),
  B('ml_poub0', '', 'ml_poubelle', 9, 15.4, 0.6, 0.6, { named: false }), B('ml_poub1', '', 'ml_poubelle', 41, 18, 0.6, 0.6, { named: false }),
  ...LAMPS.map(([x, z], i) => B(`ml_lamp${i}`, '', 'ml_lampadaire', x - 0.3, z - 0.3, 0.6, 0.6, { named: false })),
  ENS('ml_e_vibes', 'ml_ens_ecran_vibes', 19, 13.6, 3.4, { groupe: 'ecrans_quai', ph: 0 }), ENS('ml_e_tron', 'ml_ens_ecran_tron', 29, 13.6, 3.4, { groupe: 'ecrans_quai', ph: 0 }),
  ENS('ml_e_horaires', 'ml_ens_horaires', 26.2, 14.6, 2.2), ENS('ml_e_hc', 'ml_ens_human_corp', 8, 7.2, 1.6),
];
export const BUILDINGS_TERMINUS = [
  B('ml_sas', 'Les portes du sas', 'ml_sas', 6, 0, 18, 2),
  B('ml_panneau', 'Dernier arrêt avant No Man\u2019s Land', 'ml_panneau_terminus', 13.5, 3, 3, 0.5, { sign: true }), // phrase affichée par le code (libellé), panneau vierge
  B('ml_portique', 'Portique de levage', 'ml_portique', 11.5, 7, 7, 4, { solid: [] }),
  B('ml_bureau', 'Bureau de la gare de fret', 'ml_bureau_fret', 2, 8, 5, 4),
  B('ml_cont0', '', 'ml_conteneurs', 21, 6, 6, 2.5, { named: false }), B('ml_cont1', '', 'ml_conteneurs', 22, 11, 6, 2.5, { named: false }),
  ENS('ml_e_sas', 'ml_ens_sas', 15, 2.2, 5.2),
  ENS('ml_e_gyro0', 'ml_ens_gyrophare', 12, 11.2, 6.2, { groupe: 'gyrophares', ph: 0 }), ENS('ml_e_gyro1', 'ml_ens_gyrophare', 18.4, 11.2, 6.2, { groupe: 'gyrophares', ph: 2 }),
];
export const CLOSED_MEGA = {
  ml_station: 'La station. On monte au quai par les escaliers ; la rame ne s\u2019arrête pas pour qui n\u2019a pas de billet.',
  ml_viaduc1: 'Le viaduc de fer noir. Les piles ruissellent ; le fer transpire.',
  ml_tableau: 'Le tableau des départs, en pictogrammes. Une ligne change. Aucune ne dit « terminus ».',
  ml_borne: 'La borne de billets reconnaît les bracelets, et les visages.',
  ml_sas: 'Les portes du sas. Pleines, si hautes qu\u2019on les prend pour un mur. Fermées. Elles ne s\u2019ouvriront pas.',
  ml_panneau: '« Dernier arrêt avant No Man\u2019s Land. »',
  ml_bureau: 'Le bureau de la gare de fret. Une fenêtre ambrée, des bordereaux.',
  ml_portique: 'Le portique de levage jaune. Les conteneurs vont et viennent, toujours vers l\u2019intérieur.',
};
export const LOCATIONS_MEGA = {
  steel_megaline: { id: 'steel_megaline', name: 'Steel-Megalopolis · Mega-Line', kind: 'exterior', size: { w: 48, d: 24 }, light: LIGNE,
    ground: { base: '#12121a', skin: 'g_ml_pave', tileM: 4, clean: true, zones: [ { x: 14, z: 13.5, w: 20, d: 2, kind: 'plate', skin: 'g_ml_quai', tileM: 4 } ] },
    buildings: BUILDINGS_MEGA, props: [],
    glows: [ ...LAMPS.map(([x, z]) => ({ x, z: z + 0.6, rx: 2.4, rz: 1.8, color: AMBRE, i: 0.6, flicker: true })), // lueurs des lampadaires (code)
      { x: 19, z: 14.6, rx: 3, rz: 1.4, color: VIOLET, i: 0.7, flicker: true }, { x: 29, z: 14.6, rx: 3, rz: 1.4, color: CYAN, i: 0.65, flicker: true },
      { x: 8, z: 8, rx: 2.4, rz: 1.2, color: '#e8eef2', i: 0.45 }, { x: 24, z: 6, rx: 22, rz: 2, color: MAGENTA, i: 0.15 }, { x: 24, z: 15.2, rx: 2, rz: 1, color: AMBRE, i: 0.6 } ],
    extras: [ ...[[16, 15.4], [22, 15.6], [32, 15.2], [11, 18], [27, 19]].map(([x, z], i) => ({ sprite: i % 2 ? 'gen_ml_foule_b' : 'gen_ml_foule_a', x, z, face: i % 2 ? 1 : -1, role: 'voyageur' })) ],
    walkers: [ { sprite: 'gen_ml_foule_a', path: [[2, 19], [46, 19]], speed: 0.8, t0: 4 } ],
    spawn: { player: { x: 24, z: 23 }, companion: { x: 25, z: 23 } }, city: 'steel',
    arrive: { from: 'steel_center', text: 'La Mega-Line. Le viaduc de fer noir passe au-dessus des têtes ; la rame violette glisse sans bruit. Sur le quai, Vibes et Tron passent en boucle.' } },
  steel_terminus: { id: 'steel_terminus', name: 'Steel-Megalopolis · Terminus de fret', kind: 'exterior', size: { w: 30, d: 20 }, light: FRET,
    ground: { base: '#141210', skin: 'g_ml_fret', tileM: 4, clean: true },
    buildings: BUILDINGS_TERMINUS, props: [],
    glows: [ { x: 15, z: 3, rx: 9, rz: 1.6, color: ROUGE, i: 0.4, flicker: true }, { x: 15, z: 11.6, rx: 4, rz: 1.6, color: ORANGE, i: 0.5, flicker: true }, // lueurs de quai (code)
      { x: 4.5, z: 12.6, rx: 2.6, rz: 1.4, color: AMBRE, i: 0.6 }, { x: 15, z: 16, rx: 12, rz: 3, color: AMBRE, i: 0.2 } ],
    extras: [ { sprite: 'gen_ml_foule_a', x: 9, z: 15, face: -1, role: 'docker' }, { sprite: 'gen_ml_foule_b', x: 20, z: 15.6, face: 1, role: 'voyageur' } ],
    walkers: [], spawn: { player: { x: 15, z: 19 }, companion: { x: 16, z: 19 } }, city: 'steel',
    arrive: { from: 'steel_megaline', text: 'Le terminus de fret. Plus d\u2019écran, plus de pub. Au bout de la voie, des portes si grandes qu\u2019on les prend d\u2019abord pour un mur.' } },
};
const J = (id, loc, ox, oz, tx, tz, to, label, conditions = []) => ({ id, location: loc, junction: true, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: { doorId: to }, conditions });
export const DOORS_MEGA = [
  J('c_mega', 'steel_center', 8, 0, 8, 1, 'ml_sud', 'Mega-Line'),
  J('ml_sud', 'steel_megaline', 24, 24, 24, 23, 'c_mega', 'Vers Center-Town'),
  J('ml_passerelle', 'steel_megaline', 48, 2, 47, 2, 'tm_sud', 'Passerelle de service (terminus)'),
  J('tm_sud', 'steel_terminus', 15, 20, 15, 19, 'ml_passerelle', 'Passerelle de service (vers la ligne)'),
];
export const NPCS_MEGA = [ // aucun n'est Vibes ni Tron
  { id: 'ml_navetteur', name: 'Anselme Roque', sprite: 'gen_ml_navetteur', location: 'steel_megaline', x: 35, z: 14, faceTo: [30, 16], dialogue: 'ml_navetteur' },
  { id: 'ml_controleuse', name: 'Sabine', sprite: 'gen_ml_controleuse', location: 'steel_megaline', x: 13, z: 14, faceTo: [16, 18], dialogue: 'ml_controleuse' },
  { id: 'ml_etudiante', name: 'Lou', sprite: 'gen_ml_etudiante', location: 'steel_megaline', x: 5, z: 17.4, faceTo: [5, 20], dialogue: 'ml_etudiante' },
  { id: 'ml_entretien', name: 'Marcel', sprite: 'gen_ml_entretien', location: 'steel_megaline', x: 40, z: 7.8, faceTo: [36, 10], dialogue: 'ml_entretien' },
  { id: 'ml_nouilles', name: 'Mme Tran', sprite: 'gen_ml_nouilles', location: 'steel_megaline', x: 23, z: 15.2, faceTo: [23, 19], dialogue: 'ml_nouilles' },
  { id: 'ml_vigile', name: 'Kessler', sprite: 'gen_ml_vigile', location: 'steel_megaline', x: 40, z: 16, faceTo: [34, 18], dialogue: 'ml_vigile' },
  { id: 'ml_pancarte', name: 'Noé', sprite: 'gen_ml_pancarte', location: 'steel_megaline', x: 35.5, z: 16.6, faceTo: [30, 19], dialogue: 'ml_pancarte' },
  { id: 'ml_fan', name: 'Yuna', sprite: 'gen_ml_fan', location: 'steel_megaline', x: 19, z: 16, faceTo: [19, 13], dialogue: 'ml_fan' },
  { id: 'ml_cheffe', name: 'Odile Ferraz', sprite: 'gen_ml_cheffe_fret', location: 'steel_terminus', x: 5, z: 13, faceTo: [10, 15], dialogue: 'ml_cheffe' },
  { id: 'ml_docker', name: 'Bruno', sprite: 'gen_ml_docker', location: 'steel_terminus', x: 19.5, z: 12, faceTo: [15, 14], dialogue: 'ml_docker' },
];
const D = (t1, t2) => ({ start: { text: t1, options: [ { label: 'Et sinon ?', next: 'b' }, { label: 'Au revoir.', next: 'end' } ] }, b: { text: t2, options: [ { label: 'Au revoir.', next: 'end' } ] } });
export const DIALOGUES_MEGA = {
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
