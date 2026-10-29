// Le Dôme Fréquence (zone steel_dome, 30 x 30 m) : intérieur de c_tour (Center-Town). Pack d'Ocre : docs/villes/steel/quartiers/dome_frequence/.
// Entrée : porte de façade de c_tour vers (23,5 ; 13), fermée tant que le drapeau dome_ouvert n'est pas posé (comme les grilles conditionnelles).
// Accès de debug : ?dome=1 dans l'URL, ou window.__nml.ouvrirDome(). Vibes et Tron : uniquement sur les écrans de scène et de façade.
// Écrans de scène : 213 x 120 (2,4 m, ancre [106, 119]), posés à y 3,9 au-dessus de la herse (y 2,6) : sommet à 6,3 m comme avant, bas dégagé ; un groupe, une seule horloge. Herse de lumières : enseigne df_ens_lumieres + lueurs posées par le code (rien de peint).
const DOME = { bg: '#07060c', hemi: ['#c8a0ff', '#2a1420', 1.15], sun: ['#f2b44a', 0.55], tint: '#c8b4d0', actor: '#e8dcea' };
const VIOLET = '#8a3cff', MAGENTA = '#e03ca8', CYAN = '#5fd3f0', AMBRE = '#f2b44a', LAITON = '#c8a050';
const B = (id, label, sprite, x, z, w, d, extra = {}) => ({ id, label, sprite, x, z, w, d, visitable: false, cue: null, named: !!label, ...extra });
const ENS = (id, sprite, x, z, y, extra = {}) => B(id, '', sprite, x - 0.1, z - 0.1, 0.2, 0.2, { y, solid: [], named: false, ...extra });
export const BUILDINGS_DOME = [
  B('df_cadre_v', '', 'df_ecran_cadre', 8, 1.2, 6, 0.5, { named: false }), B('df_cadre_t', '', 'df_ecran_cadre', 14, 1.2, 6, 0.5, { named: false }),
  B('df_scene', 'Scène', 'df_scene', 6, 2, 18, 4),
  B('df_enc0', '', 'df_enceinte', 4, 6, 1, 1, { named: false }), B('df_enc1', '', 'df_enceinte', 25, 6, 1, 1, { named: false }),
  ...[8, 10.5, 13, 15.5].flatMap((z, i) => [B(`df_gr${i}a`, '', 'df_gradin', 6, z, 6, 2, { named: false }), B(`df_gr${i}b`, '', 'df_gradin', 19, z, 6, 2, { named: false })]),
  B('df_regie', 'Régie', 'df_regie', 13, 14, 4, 4),
  B('df_col0', '', 'df_colonne', 2, 18, 1, 1, { named: false }), B('df_col1', '', 'df_colonne', 27, 18, 1, 1, { named: false }),
  B('df_cl0', '', 'df_cloison', 0, 20.5, 6, 0.5, { named: false }), B('df_cl1', '', 'df_cloison', 6, 20.5, 6, 0.5, { named: false }),
  B('df_cl2', '', 'df_cloison', 18, 20.5, 6, 0.5, { named: false }), B('df_cl3', '', 'df_cloison', 24, 20.5, 6, 0.5, { named: false }),
  B('df_bar', 'Bar du foyer', 'df_bar', 4, 22, 6, 2), B('df_vestiaire', 'Vestiaire', 'df_vestiaire', 20, 22, 6, 2),
  B('df_ban0', '', 'df_banquette', 6, 26, 2, 1, { named: false }), B('df_ban1', '', 'df_banquette', 22, 26, 2, 1, { named: false }),
  B('df_borne', 'Borne de billets', 'df_borne', 14, 26, 1, 1),
  B('df_porte', '', 'df_porte', 12, 29.5, 6, 0.5, { solid: [], named: false }),
  // enseignes : écrans de scène (groupe synchronisé), herse de lumières, vumètres, néon du bar
  ENS('df_e_vibes', 'df_ens_ecran_vibes', 11, 1.8, 3.9, { groupe: 'ecrans_scene', ph: 0 }), ENS('df_e_tron', 'df_ens_ecran_tron', 17, 1.8, 3.9, { groupe: 'ecrans_scene', ph: 0 }),
  ENS('df_e_herse', 'df_ens_lumieres', 15, 6.2, 2.6), ENS('df_e_vu', 'df_ens_vu', 16.8, 18.2, 1.4), ENS('df_e_bar', 'df_ens_bar', 8, 24.2, 2.2),
];
export const CLOSED_DOME = {
  df_scene: 'La scène, plateau noir à bord laiton. Au-dessus, Vibes et Tron jouent sur les écrans, en parfaite synchronisation.',
  df_regie: 'La console de la régie. Des centaines de curseurs, et un seul marqué « applaudissements ».',
  df_borne: 'La borne Human Corp lit les billets. Et un peu plus que les billets.',
  df_bar: 'Le bar du foyer, laiton et ambre. Le cocktail du moment s\u2019appelle HeartSync.', df_vestiaire: 'Le vestiaire. Un ticket par manteau.',
};
export const LOCATIONS_DOME = {
  steel_dome: { id: 'steel_dome', name: 'Steel-Megalopolis · Le Dôme Fréquence', kind: 'exterior', size: { w: 30, d: 30 }, light: DOME,
    ground: { base: '#120c14', skin: 'g_df_marbre', tileM: 4, clean: true, zones: [
      { x: 6, z: 2, w: 18, d: 4, kind: 'plate', skin: 'g_df_scene', tileM: 4 }, { x: 4, z: 7, w: 22, d: 13, kind: 'plate', skin: 'g_df_moquette', tileM: 4 } ] },
    buildings: BUILDINGS_DOME, props: [],
    glows: [ // herse de projecteurs allumée par le code : lueurs magenta et cyan au-dessus de la scène, qui scintillent
      ...[7, 10, 13, 16, 19, 22].map((x, i) => ({ x, z: 4.2, rx: 1.6, rz: 1.2, color: i % 2 ? CYAN : MAGENTA, i: 0.75, flicker: true })),
      { x: 15, z: 4, rx: 10, rz: 2.6, color: VIOLET, i: 0.5 }, { x: 15, z: 12, rx: 10, rz: 6, color: VIOLET, i: 0.22 },
      { x: 15, z: 16, rx: 2.4, rz: 2, color: CYAN, i: 0.4 }, { x: 7, z: 24.6, rx: 3.6, rz: 1.6, color: AMBRE, i: 0.7 }, { x: 23, z: 24.6, rx: 3, rz: 1.4, color: LAITON, i: 0.45 },
      { x: 15, z: 27, rx: 3, rz: 2, color: '#e8eef2', i: 0.35 }, { x: 15, z: 25, rx: 13, rz: 4, color: AMBRE, i: 0.18 } ],
    extras: [ ...[[21, 9.6], [23, 12.2], [8.5, 17.4], [22, 17.4], [12, 25.6], [18, 27]].map(([x, z], i) => ({ sprite: i % 2 ? 'gen_df_foule_b' : 'gen_df_foule_a', x, z, face: x < 15 ? 1 : -1, role: 'public' })) ],
    walkers: [ { sprite: 'gen_df_foule_a', path: [[3, 25], [27, 25]], speed: 0.5, t0: 5 } ],
    spawn: { player: { x: 15, z: 28.5 }, companion: { x: 16, z: 28.5 } }, city: 'steel',
    arrive: { from: 'steel_center', text: 'Le Dôme Fréquence. Marbre, laiton et velours. Sur les deux écrans de scène, Vibes et Tron jouent pour une salle presque vide.' } },
};
const J = (id, loc, ox, oz, tx, tz, to, label, conditions = []) => ({ id, location: loc, junction: true, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: { doorId: to }, conditions });
export const DOORS_DOME = [
  { id: 'c_dome', buildingId: 'c_tour', location: 'steel_center', label: 'Le Dôme Fréquence', opening: { x: 23.5, z: 13, side: 'south' }, threshold: { x: 23.5, z: 14 }, target: { doorId: 'df_sortie' },
    conditions: [{ test: s => !!s.flags.dome_ouvert, reason: 'dome', text: 'Le Dôme Fréquence. Des écrans sur toute la façade, et une porte qui ne s\u2019ouvre pas pour toi. Pas ce soir.' }] },
  J('df_sortie', 'steel_dome', 15, 30, 15, 29, 'c_dome', 'Sortie (Center-Town)'),
];
export const NPCS_DOME = [ // positions de la fiche, décalées hors du mobilier ; aucun n'est Vibes ni Tron
  { id: 'df_varenne', name: 'Mme Varenne', sprite: 'gen_df_varenne', location: 'steel_dome', x: 15, z: 24, faceTo: [15, 28], dialogue: 'df_varenne' },
  { id: 'df_octave', name: 'Octave', sprite: 'gen_df_octave', location: 'steel_dome', x: 17.8, z: 16.4, faceTo: [15, 4], dialogue: 'df_octave' },
  { id: 'df_jade', name: 'Jade', sprite: 'gen_df_jade', location: 'steel_dome', x: 7, z: 24.8, faceTo: [7, 28], dialogue: 'df_jade' },
  { id: 'df_nils', name: 'Nils', sprite: 'gen_df_nils', location: 'steel_dome', x: 23, z: 24.8, faceTo: [23, 28], dialogue: 'df_nils' },
  { id: 'df_pia', name: 'Pia', sprite: 'gen_df_pia', location: 'steel_dome', x: 22, z: 7, faceTo: [15, 4], dialogue: 'df_pia' },
  { id: 'df_ruben', name: 'Ruben', sprite: 'gen_df_ruben', location: 'steel_dome', x: 15.8, z: 27.2, faceTo: [15, 30], dialogue: 'df_ruben' },
  { id: 'df_helene', name: 'Hélène', sprite: 'gen_df_helene', location: 'steel_dome', x: 8.6, z: 27.4, faceTo: [12, 27], dialogue: 'df_helene' },
  { id: 'df_theo', name: 'Théo', sprite: 'gen_df_foule_a', location: 'steel_dome', x: 8, z: 9.6, faceTo: [15, 4], dialogue: 'df_theo' },
  { id: 'df_maelle', name: 'Maëlle', sprite: 'gen_df_foule_b', location: 'steel_dome', x: 10, z: 12, faceTo: [15, 4], dialogue: 'df_maelle' },
  { id: 'df_gardien', name: 'Le Gardien des balcons', sprite: 'gen_df_gardien', location: 'steel_dome', x: 3.6, z: 19.6, faceTo: [10, 14], dialogue: 'df_gardien' },
];
const D = (t1, t2) => ({ start: { text: t1, options: [ { label: 'Et sinon ?', next: 'b' }, { label: 'Au revoir.', next: 'end' } ] }, b: { text: t2, options: [ { label: 'Au revoir.', next: 'end' } ] } });
const D1 = t1 => ({ start: { text: t1, options: [ { label: 'Au revoir.', next: 'end' } ] } });
export const DIALOGUES_DOME = {
  df_varenne: D('Ici, nous ne faisons pas de bruit. Nous faisons de la musique validée.', 'Le 11, la salle était pleine à cent deux pour cent. Les deux pour cent restants, c\u2019était la sécurité qui chantait.'),
  df_octave: D('On refait les balances tous les soirs, même quand il n\u2019y a personne. La salle doit sonner comme sur l\u2019enregistrement.', 'Les voix sur l\u2019écran sont parfaites. Ce sont les applaudissements qui me demandent le plus de travail.'),
  df_jade: D('Le cocktail du moment s\u2019appelle HeartSync. Il a le même goût que le précédent, mais en violet.', 'Les gens viennent ici pour dire qu\u2019ils sont venus. Ils regardent l\u2019écran plus que la scène.'),
  df_nils: D('J\u2019ai un ticket pour chaque manteau. Pour les gens, on n\u2019a pas de ticket.', 'Une fois, quelqu\u2019un a oublié une veste ici, avec un badge du groupe dedans. Le lendemain, la veste avait disparu, et le badge aussi.'),
  df_pia: D1('Je règle les lumières pour une scène qui joue surtout sur écran. Mes projecteurs éclairent des gens qui ne sont pas là.'),
  df_ruben: D('Le Dôme est fermé ce soir. Il est fermé presque tous les soirs. C\u2019est ce qui le rend désirable.', 'Vous étiez déjà venu hier. La borne s\u2019en souvient, moi aussi.'),
  df_helene: D('J\u2019écris sur leurs disques depuis le début. Je n\u2019ai jamais réussi à savoir qui écrit vraiment les paroles.', 'Le meilleur morceau de l\u2019album, c\u2019est celui qu\u2019on ne passe jamais ici. Devine lequel.'),
  df_theo: D('J\u2019ai pris une place au premier rang. Je regarde quand même l\u2019écran, on voit mieux leurs visages.', 'Tous les soirs, le même concert, à la seconde près. Moi, c\u2019est ça qui me rassure.'),
  df_maelle: D('Ma robe est assortie à l\u2019écran de Tron. Si la caméra de la salle passe par ici, je serai prête.', 'On dit qu\u2019ils ne viennent jamais en vrai. Moi, je garde mon billet au cas où.'),
  df_gardien: D('Avant, ça s\u2019appelait la Rotonde. On y jouait de l\u2019orgue. L\u2019orgue est toujours sous la scène, personne n\u2019a pensé à l\u2019enlever.', 'Le dôme ne laisse pas passer le ciel. Il le montre. Ce n\u2019est pas pareil.'),
};
// Écrans de façade sur c_tour (steel_center) : comptent dans le budget mobile de Center-Town
export const FACADE_DOME = [ENS('c_e_vibes', 'df_ens_facade_vibes', 19.5, 13.2, 3.2), ENS('c_e_tron', 'df_ens_facade_tron', 28.5, 13.2, 3.2)];
