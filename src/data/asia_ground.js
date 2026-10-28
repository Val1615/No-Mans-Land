// Asia-Ground lot 2 (zone steel_asia) : décor, accès, PNJ et services de base. SANS quêtes (« Le loyer de Mei » non branché).
// Fiches de Régie : docs/villes/steel/quartiers/ASIA_GROUND.md et PLAN_IMPLEMENTATION.md §2. Positions : docs/villes/steel/quartiers/ASIA_GROUND_POSITIONS.md.
// Sprites d'Ocre (creation/asia-ground-sprites 99f6759), emprises = footprint_m du manifeste. [fiche] = repris de la fiche ; [inventé] = choix de ce lot.
// Géographie [décision] : Asia-Ground au sud de Lower-Town. a_nord au bord nord (x 8, z 0) comme le plan (la fiche dit x 0, z 18 : point ouvert du plan §5.1).
// Palette [fiche §2] : rouge laque, or terni, vapeur ; un seul néon cyan (ag_neon_io).
const ASIA = { bg: '#0c0607', hemi: ['#f0a070', '#1a0f10', 1.1], sun: ['#ff9a6a', 0.65], tint: '#e0b48e', actor: '#ecc8a8' };
const LAQUE = '#d0402a', LAMPE = '#f0b060', WOK = '#e86a22', CYAN = '#38d8ff';
const B = (id, label, sprite, x, z, w, d, extra = {}) => ({ id, label, sprite, x, z, w, d, visitable: false, cue: null, named: true, ...extra });
const P = (sp, x, z, w, d, solid) => ({ label: '', sprite: sp, x, z, w, d, visitable: false, cue: null, named: false, ...(solid ? { solid } : {}) });
export const BUILDINGS_ASIA = [
  // Rue des Lanternes (nord) [fiche] : restaurants à étages 8 x 6 m. ag_restaurant = « Chez Lin 林记 » (nom définitif d'Ocre, 99f6759).
  B('ag_lin', 'Chez Lin 林记', 'ag_restaurant', 13, 0.5, 8, 6, { sign: true }) // enseigne : libellé visible dès l'arrivée (sans porte, il n'était jamais « découvert »),
  B('ag_resto2', 'Restaurant', 'ag_restaurant_b', 23, 0.5, 8, 6, { named: false }),
  // Mille Marches (nord-est) [fiche] : escalier 8 x 14 m, décor praticable (pas de collision), haut de l'escalier = a_escalier (x 43, z 0).
  B('ag_escalier', 'Mille Marches', 'ag_escalier', 39, 0, 8, 14, { named: false, solid: [{ x: 39, z: 0, w: 0.6, d: 14 }, { x: 46.4, z: 0, w: 0.6, d: 14 }] }),
  // Marché couvert [fiche] x 12-36, z 10-26 : trois modules de halle 8 x 16 m, h 3, ouverts (seuls les poteaux d'angle sont pleins).
  ...[12, 20, 28].map((x, i) => B(`ag_halle${i}`, 'Marché couvert', 'ag_halle_module', x, 10, 8, 16, { named: i === 1, sign: i === 1,
    solid: [[x, 10], [x + 7.6, 10], [x, 25.6], [x + 7.6, 25.6]].map(([a, b]) => ({ x: a, z: b, w: 0.4, d: 0.4 })) })),
  // Boutiques-ateliers 6 x 5 m (ouest) et Bureau des Emplacements (est)
  B('ag_lau', 'Pharmacie Lau', 'ag_boutique', 2, 13, 6, 5, { visitable: true }),
  B('ag_okafor', 'Électronique Okafor', 'ag_boutique_b', 2, 23, 6, 5, { visitable: true }),
  B('ag_bureau', 'Bureau des Emplacements', 'ag_bureau', 39, 18, 6, 5, { visitable: true }),
  // Cour des Porteurs (sud-est) : monte-charge de quai 4 x 4 m, h 9 (a_quai : lot 4, non posé)
  B('ag_monte_charge', 'Monte-charge', 'ag_monte_charge', 42, 28, 4, 4, { named: false }),
  // Stands [fiche §7] (emprises réelles du manifeste) : nouilles 2,5 x 1,5 ; poisson 3,5 x 3 ; pièces 4 x 2
  B('ag_mei', 'Les Nouilles de Mei', 'ag_stand_nouilles', 14, 12, 2.5, 1.5),
  { id: 'ag_p0', ...P('ag_stand_poisson', 20.5, 14, 3.5, 3) }, { id: 'ag_p1', ...P('ag_stand_pieces', 29, 14.5, 4, 2) },
  { id: 'ag_p2', ...P('ag_stand_poisson', 22, 20.5, 3.5, 3) }, { id: 'ag_p3', ...P('ag_stand_nouilles', 30, 20.5, 2.5, 1.5) },
  ...[['ag_wok', 17, 12.2, 1, 1], ['ag_caisses_legumes', 18.6, 18.4, 1.2, 0.8], ['ag_caisses_legumes', 26.5, 18.6, 1.2, 0.8], ['ag_glaciere', 24.4, 14.6, 1, 0.6],
    ['ag_glaciere', 33.6, 22, 1, 0.6], ['ag_chariot', 38, 30.6, 1.8, 0.9], ['ag_chariot', 9.5, 31, 1.8, 0.9], ['ag_caisses_legumes', 40.4, 32.4, 1.2, 0.8],
    ['ag_auvent', 2.5, 18.2, 5, 2.5, []], ['ag_hautparleur_io', 35.4, 8.6, 0.6, 0.6], ['ag_neon_io', 22.4, 9.4, 1.2, 0.3, []],
    ['ag_lanterne_cable', 13, 7.2, 5, 1, []], ['ag_lanterne_cable', 24, 7.2, 5, 1, []], ['ag_lanterne_cable', 31.5, 7.2, 5, 1, []]]
    .map(([sp, x, z, w, d, solid], i) => ({ id: `ag_prop${i}`, ...P(sp, x, z, w, d, solid) })),
  // Barrage de gang (bord sud, a_sud) : caisses et chariot en travers, décor [inventé]
  ...[[21.5, 33.6], [23, 34], [25.4, 33.8]].map(([x, z], i) => ({ id: `ag_barrage${i}`, ...P('ag_caisses_legumes', x, z, 1.2, 0.8) })),
];
const ASIA_IN = { bg: '#0b0606', hemi: ['#ffb890', '#2a1410', 1.2], sun: ['#ffaa70', 1.0] };
const IN = (id, name, w, d, floor, wall, props, glows) => ({ id, name, kind: 'interior', size: { w, d }, light: ASIA_IN,
  ground: { base: '#3a2e2a', skin: floor, tileM: 2 }, wall: '#3a2018', wallSkin: wall, buildings: [], props, glows, city: 'steel' });
export const LOCATIONS_ASIA = {
  steel_asia: { id: 'steel_asia', name: 'Steel-Megalopolis · Asia-Ground', kind: 'exterior', size: { w: 48, d: 36 }, light: ASIA,
    ground: { base: '#2c2422', skin: 'g_sv', tileM: 5, clean: true, tint: 'rgba(14,6,6,.45)', zones: [
      { x: 0, z: 6.5, w: 48, d: 3.5, kind: 'asphalt', tint: 'rgba(24,10,8,.45)' },         // Rue des Lanternes [fiche]
      { x: 12, z: 10, w: 24, d: 16, kind: 'plate', tint: 'rgba(40,20,14,.3)' },            // Marché couvert : carrelage ancien [fiche]
      { x: 36, z: 26, w: 12, d: 10, kind: 'plate', tint: 'rgba(20,16,14,.4)' } ] },        // Cour des Porteurs [fiche]
    buildings: BUILDINGS_ASIA, props: [],
    glows: [ { x: 15.5, z: 8, rx: 3, rz: 1.6, color: LAQUE, i: 0.7, flicker: true }, { x: 26.5, z: 8, rx: 3, rz: 1.6, color: LAQUE, i: 0.7, flicker: true }, { x: 34, z: 8, rx: 3, rz: 1.6, color: LAQUE, i: 0.6 },
      { x: 17.5, z: 13, rx: 2, rz: 1.6, color: WOK, i: 0.8, flicker: true }, { x: 22, z: 16, rx: 2.4, rz: 2, color: LAMPE, i: 0.55 }, { x: 31, z: 16, rx: 2.4, rz: 2, color: LAMPE, i: 0.55 },
      { x: 24, z: 22, rx: 3, rz: 2.4, color: LAMPE, i: 0.5 }, { x: 5, z: 19.5, rx: 2.4, rz: 1.4, color: LAMPE, i: 0.5 }, { x: 5, z: 29, rx: 2.4, rz: 1.4, color: LAMPE, i: 0.45 },
      { x: 42, z: 24, rx: 2.4, rz: 1.4, color: LAMPE, i: 0.45 }, { x: 23, z: 10, rx: 1.6, rz: 0.8, color: CYAN, i: 0.5 }, { x: 44, z: 33, rx: 2.4, rz: 2, color: LAMPE, i: 0.35 } ],
    extras: [ ...[[16, 17], [19, 23], [27, 23.6], [33, 17.6], [10, 8.4]].map(([x, z], i) => ({ sprite: `st_civil${(i + 2) % 6}`, x, z, face: i % 2 ? 1 : -1, role: 'client' })) ],
    walkers: [ { sprite: 'st_civil1', path: [[2, 8.4], [46, 8.4]], speed: 0.8, t0: 4 }, { sprite: 'st_civil4', path: [[19, 18.6], [33, 18.6]], speed: 0.6, t0: 12 },
      { sprite: 'st_civil2', path: [[37, 33], [37, 26], [46, 26]], speed: 0.7, t0: 22 } ],
    spawn: { player: { x: 8, z: 1 }, companion: { x: 9, z: 1.5 } }, city: 'steel',
    arrive: { from: 'steel_lower', text: 'Asia-Ground. L\u2019odeur arrive avant les lanternes : huile chaude, épices, poisson. On marchande dans trois langues.' } },
  // Intérieurs [plan §2] : 10 x 8 m, style de l'extérieur, ASIA_IN ; sortie au sud, seuil à 1 m. Mobilier = réemplois du manifeste d'intérieurs.
  lau_in: IN('lau_in', 'Asia-Ground · Pharmacie Lau', 10, 8, 'f_concrete', 'w_brick', [
    { furn: 'shop_counter', x: 2.4, z: 3.0 }, { furn: 'm_archive_shelf', x: 0.3, z: 0.2 }, { furn: 'sv_shelf', x: 2.6, z: 0.2 }, { furn: 'home_curtain', x: 7.0, z: 0.2 }, { furn: 'home_mattress_d', x: 7.8, z: 1.4 } ],
    [{ x: 4, z: 3, rx: 2.6, rz: 1.8, color: LAMPE, i: 0.55 }]),
  okafor_in: IN('okafor_in', 'Asia-Ground · Électronique Okafor', 10, 8, 'f_sv_plates', 'w_sv_tin', [
    { furn: 'sv_workbench', x: 3.6, z: 0.3 }, { furn: 'sv_workbench', x: 0.3, z: 0.3 }, { furn: 'sv_shelf', x: 8.2, z: 0.2 }, { furn: 'm_desk', x: 7.2, z: 4.6 }, { sprite: 'rubble', x: 0.8, z: 5.4 } ],
    [{ x: 6, z: 2.4, rx: 2.4, rz: 1.6, color: LAMPE, i: 0.55 }]),
  emplacements_in: IN('emplacements_in', 'Asia-Ground · Bureau des Emplacements', 10, 8, 'f_concrete', 'w_sv_planks', [
    { furn: 'm_desk', x: 4.0, z: 3.0 }, { furn: 'm_archive_shelf', x: 0.3, z: 0.2 }, { furn: 'm_archive_shelf', x: 1.9, z: 0.2 }, { furn: 'io_locker', x: 8.6, z: 0.3 } ],
    [{ x: 5, z: 3.2, rx: 2.6, rz: 1.8, color: LAMPE, i: 0.5 }]),
  mei_in: IN('mei_in', 'Asia-Ground · Arrière du stand de Mei', 10, 8, 'f_sv_concrete', 'w_brick', [
    { sprite: 'stove', x: 0.6, z: 0.6 }, { furn: 'home_table', x: 2.6, z: 3.6 }, { furn: 'home_water', x: 5.0, z: 0.3 }, { furn: 'home_mattress_d', x: 8.0, z: 0.3 }, { sprite: 'barrel', x: 8.6, z: 6.4 } ],
    [{ x: 1.2, z: 1.2, rx: 2, rz: 2, color: WOK, i: 0.6, flicker: true }, { x: 5, z: 4, rx: 3, rz: 2.4, color: LAMPE, i: 0.35 }]),
};
const J = (id, loc, ox, oz, tx, tz, to, label, conditions = []) => ({ id, location: loc, junction: true, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: { doorId: to }, conditions });
const E = (id, loc, ox, oz, tx, tz, label, text) => ({ id, location: loc, edge: text, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: null, conditions: [] });
const DOOR = (id, bid, ox, oz, to) => ({ id, buildingId: bid, location: 'steel_asia', opening: { x: ox, z: oz, side: 'south' }, threshold: { x: ox, z: oz + 1 }, target: { doorId: to }, conditions: [] });
const OUT = (id, loc, w, d, to) => ({ id, location: loc, opening: { x: w / 2, z: d, side: 'south' }, threshold: { x: w / 2, z: d - 1 }, target: { doorId: to }, conditions: [] });
export const DOORS_ASIA = [
  J('a_nord', 'steel_asia', 8, 0, 8, 1, 'l_sud', 'Vers Lower-Town'),                       // [plan] a_nord ↔ l_sud, aucune condition
  J('a_escalier', 'steel_asia', 43, 0, 43, 1, 'c_sud_est', 'Mille Marches (Center-Town)'),  // [plan] a_escalier ↔ c_sud_est ; Repérage +1 : système absent, non branché
  J('c_sud_est', 'steel_center', 38, 36, 38, 35, 'a_escalier', 'Mille Marches (Asia-Ground)'),
  E('a_sud', 'steel_asia', 24, 36, 24, 35, 'Barrage (China Lake)', 'Des caisses en travers de la rue, trois types assis dessus. China Lake est derrière. Pas ce soir.'), // [plan] lot 3
  DOOR('ag_lau_door', 'ag_lau', 5, 18, 'lau_in_door'), OUT('lau_in_door', 'lau_in', 10, 8, 'ag_lau_door'),
  DOOR('ag_okafor_door', 'ag_okafor', 5, 28, 'okafor_in_door'), OUT('okafor_in_door', 'okafor_in', 10, 8, 'ag_okafor_door'),
  DOOR('ag_bureau_door', 'ag_bureau', 42, 23, 'emplacements_in_door'), OUT('emplacements_in_door', 'emplacements_in', 10, 8, 'ag_bureau_door'),
  DOOR('ag_mei_door', 'ag_mei', 15.25, 13.5, 'mei_in_door'), OUT('mei_in_door', 'mei_in', 10, 8, 'ag_mei_door'), // arrière du stand (sert à la quête plus tard)
];
export const NPCS_ASIA = [ // sprites PROVISOIRES (réemplois) ; positions intérieures du plan §2
  { id: 'ag_mei', name: 'Mei Tran', sprite: 'gen_vera', location: 'steel_asia', x: 15.2, z: 11.2, faceTo: [15.2, 16], dialogue: 'ag_mei' },     // derrière son stand, côté nord [plan]
  { id: 'ag_lau', name: 'Hana Lau', sprite: 'gen_odile', location: 'lau_in', x: 4, z: 2, faceTo: [5, 8], dialogue: 'ag_lau' },
  { id: 'ag_okafor', name: 'Okafor', sprite: 'gen_ezequiel', location: 'okafor_in', x: 6, z: 2, faceTo: [5, 8], dialogue: 'ag_okafor' },
  { id: 'ag_seng', name: 'Victor Seng', sprite: 'gen_teng', location: 'emplacements_in', x: 5, z: 2, faceTo: [5, 8], dialogue: 'ag_seng' },
  { id: 'ag_kim', name: 'Kim Tran', sprite: 'gen_sv_guetteuse', location: 'mei_in', x: 8, z: 5, faceTo: [5, 8], dialogue: 'ag_kim' },
];
// Répliques et services [inventé, d'après envie / peur / voix de la fiche §5]. Prix en crédits [fiche §1]. Aucune quête.
const D = (t1, t2, t3, svc = []) => ({ start: { text: t1, options: [ ...svc, { label: 'Continuer.', next: 'b' }, { label: 'Au revoir.', next: 'end' } ] },
  b: { text: t2, options: [ { label: 'Et alors ?', next: 'c' }, { label: 'Au revoir.', next: 'end' } ] }, c: { text: t3, options: [ { label: 'Au revoir.', next: 'end' } ] },
  servi: { text: 'Voilà. Mange chaud, ça tient au corps.', options: [ { label: 'Merci.', next: 'end' } ] },
  pauvre: { text: 'Pas assez de crédits. Reviens quand tu en as.', options: [ { label: 'Au revoir.', next: 'end' } ] } });
export const DIALOGUES_ASIA = {
  ag_mei: D('Assieds-toi, assieds-toi ! Nouilles, bouillon, trois crédits. Ni hao, tu as faim, ça se voit.', 'Ici tout le monde loue. Le stand, le coin de trottoir, même l\u2019air au-dessus du wok.',
    'Mon fils porte des caisses pour qui le paie. Il croit que je ne vois rien. Mange, va.', [{ label: 'Un bol de nouilles (3 cr).', action: 'paycr:3;give:meal', next: 'servi' }]),
  ag_lau: D('Fermez la porte. Qu\u2019est-ce qui fait mal ?', 'Je soigne. Je ne demande pas d\u2019où viennent les plaies.', 'Les patrouilles ont une lampe qui voit sous la peau. On dit. Moi je ne dis rien.'),
  ag_okafor: D('Ah, un client ! Pile, fusible, carte mère d\u2019avant-guerre ? Non ? Dommage, j\u2019adore les cartes mères.', 'Tout passe par ici : les radios, les lecteurs, même les implants quand ça grésille. Licence IO au mur, voyez ?',
    'Un jour je trouverai une vraie pièce d\u2019avant. Pas une copie. Une vraie, avec la poussière d\u2019origine.'),
  ag_seng: D('Bienvenue. Vous cherchez un emplacement ? Le marché est complet, mais tout se négocie.', 'Quinze pour cent sur le chiffre, plus l\u2019entretien du toit, plus l\u2019éclairage. C\u2019est raisonnable.',
    'Les comptes sont tenus, rassurez-vous. Personne n\u2019a besoin de les relire.'),
  ag_kim: D('T\u2019es qui, toi ? Ma mère t\u2019a fait entrer ?', 'Je porte des caisses. Je cours vite. Je gagne plus qu\u2019elle en une nuit, des fois.', 'Parle pas de China Lake devant elle. Jamais.'),
};
