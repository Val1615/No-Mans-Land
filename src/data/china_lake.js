// China Lake lot 3 (zone steel_china) : décor, accès, PNJ et services de base. SANS quêtes (« Le loyer de Mei » partie 2 non branchée).
// Sources : docs/villes/steel/quartiers/PLAN_IMPLEMENTATION.md §3 et lot 3 (la fiche CHINA_LAKE.md est perdue), DA d'Ocre (creation/quartiers, DA_QUARTIERS.md, China Lake).
// Sprites d'Ocre (creation/china-lake-sprites a301df7), emprises = footprint_m du manifeste. Positions : docs/villes/steel/quartiers/CHINA_LAKE_POSITIONS.md.
// Composition [décision Valentin] : grand marché illégal de contrefaçons, lac au centre (x 14-34, z 12-26, non praticable), stands sur les quatre quais,
// bâtiments au fond (bord nord, haut du cadre), ruelles. Une rive par marchandise [proposition] : nord implants et puces, est armes, sud faux papiers, ouest médicaments.
// Palette [DA] : noir pétrole, tôle verdie, ampoules ambre dominantes, rouge seulement dans les lanternes ; aucun néon.
const CHINA = { bg: '#060805', hemi: ['#c8b070', '#0c1208', 1.0], sun: ['#e8a860', 0.55], tint: '#cdb890', actor: '#e0c8a0' };
const AMBRE = '#e8a13a', ROUGE = '#c8322a', BILE = '#7a8a3a';
const B = (id, label, sprite, x, z, w, d, extra = {}) => ({ id, label, sprite, x, z, w, d, visitable: false, cue: null, named: true, ...extra });
const P = (id, sp, x, z, w, d, solid) => ({ id, label: '', sprite: sp, x, z, w, d, visitable: false, cue: null, named: false, ...(solid ? { solid } : {}) });
export const LAKE = { x: 14, z: 12, w: 20, d: 14 };
const STANDS = [ // [id, sprite, x, z, libellé] ; emprises du manifeste (implants/puces/papiers 2,5 x 1 ; médocs 2,5 x 1,5 ; armes 2,5 x 2)
  ['cl_s_implants', 'cl_stand_implants', 16, 10.6, 'Implants « garantis »'], ['cl_s_puces', 'cl_stand_puces', 19.5, 10.6, 'Puces et lecteurs'],
  ['cl_s_puces2', 'cl_stand_puces', 27.5, 10.6, ''], ['cl_s_implants2', 'cl_stand_implants', 31, 10.6, ''],
  ['cl_s_armes', 'cl_stand_armes', 37, 13, 'Armes sans numéro'], ['cl_s_armes2', 'cl_stand_armes', 37, 17, ''], ['cl_s_armes3', 'cl_stand_armes', 37, 21, ''],
  ['cl_s_papiers', 'cl_stand_papiers', 16, 28.5, 'Faux papiers'], ['cl_s_tech', 'cl_stand_implants', 22.75, 26.6, 'Établi du technicien'], ['cl_s_papiers2', 'cl_stand_papiers', 28, 28.5, ''],
  ['cl_s_medocs', 'cl_stand_medocs', 10.5, 13.6, 'Médicaments et stimulants'], ['cl_s_medocs2', 'cl_stand_medocs', 10.5, 22.6, ''] ];
const FP = { cl_stand_implants: [2.5, 1], cl_stand_puces: [2.5, 1], cl_stand_papiers: [2.5, 1], cl_stand_medocs: [2.5, 1.5], cl_stand_armes: [2.5, 2] };
export const BUILDINGS_CHINA = [
  // Fond (bord nord) : pilotis, Pavillon du Dragon, façades muettes, maison de thé (seul toit recourbé), la trouée du Barrage x 21,5-29,5 entre eux.
  B('cl_pilotis_no', '', 'cl_pilotis', 0.5, 0.5, 6, 6, { named: false }),
  B('cl_dragon', 'Pavillon du Dragon', 'cl_immeuble_fond', 8, 0.5, 7, 8, { visitable: true, sign: true }),
  B('cl_fond1', '', 'cl_immeuble_fond_b', 15.5, 0.5, 6, 8, { named: false }),
  B('cl_the', 'Maison de thé', 'cl_maison_the', 30, 0.5, 10, 5.5, { visitable: true, sign: true }),
  B('cl_fond2', '', 'cl_immeuble_fond_b', 41, 0.5, 6, 8, { named: false }),
  // Est : cabane des Filets (8 x 2), ruelle de l'angle vers Lower-Town (k_est, x 48, z 32) laissée libre ; sud-ouest : pilotis qui ferment l'angle
  B('cl_filets', 'Les Filets', 'cl_cabane', 40, 24, 8, 2, { visitable: true }),
  B('cl_pilotis_so', '', 'cl_pilotis', 0.5, 29.5, 6, 6, { named: false }),
  // Ponton de Shen (rive ouest), praticable
  B('cl_ponton', 'Ponton de Shen', 'cl_ponton', 9, 17, 5, 3, { solid: [], sign: true }),
  ...STANDS.map(([id, sp, x, z, label]) => B(id, label, sp, x, z, FP[sp][0], FP[sp][1], { named: !!label, sign: !!label })),
  // Props (emprises du manifeste ; solid [] = au-dessus de l'eau ou à hauteur de tête)
  P('cl_cable1', 'cl_cable_lanternes', 17, 14, 14, 0.5, []), P('cl_cable2', 'cl_cable_lanternes', 17, 22, 14, 0.5, []),
  P('cl_b_dragon', 'cl_ballon_dragon', 17, 15.5, 3, 1.5, []), P('cl_b_carpe', 'cl_ballon_carpe', 28, 15, 3, 1, []),
  P('cl_b_tigre', 'cl_ballon_tigre', 20.5, 22.8, 3, 1.2, []), P('cl_b_phenix', 'cl_ballon_phenix', 27.5, 19, 3, 1.5, []),
  P('cl_dech_a', 'cl_dechets_a', 19, 17.5, 2, 2, []), P('cl_dech_b', 'cl_dechets_b', 29.5, 22.5, 2, 2, []), P('cl_dech_c', 'cl_dechets_c', 15.5, 23, 2, 2, []),
  ...[[13.6, 11.6], [33.6, 11.6], [13.6, 25.6], [33.6, 25.6], [24, 25.6]].map(([x, z], i) => P(`cl_pieux${i}`, i % 2 ? 'cl_pieux_b' : 'cl_pieux', x, z, 0.8, 0.8)),
  P('cl_bache1', 'cl_bache', 21.4, 30.4, 3, 3, []), P('cl_bache2', 'cl_bache', 42, 12.4, 3, 3, []),
  P('cl_treteaux1', 'cl_treteaux', 31.5, 29.4, 2, 0.6), P('cl_treteaux2', 'cl_treteaux', 4, 14.2, 2, 0.6),
  P('cl_friture', 'cl_friture', 22.2, 9.6, 1, 0.7), P('cl_mahjong', 'cl_mahjong', 43.6, 18.4, 1.6, 1.6),
  P('cl_caisse_armes', 'cl_caisse_armes', 40.4, 15.6, 1.2, 0.6), P('cl_bac_puces', 'cl_bac_puces', 22.6, 11.4, 0.6, 0.4),
  P('cl_presse', 'cl_presse_papiers', 14.2, 30.8, 1, 0.6), P('cl_bocaux', 'cl_bocaux', 8.6, 14.2, 0.8, 0.4),
  P('cl_barriere', 'cl_barriere_caisses', 25.8, 2.4, 4, 0.8),
];
const CHINA_IN = { bg: '#070806', hemi: ['#e8c890', '#141a0e', 1.15], sun: ['#e8a860', 0.95] };
const IN = (id, name, w, d, floor, wall, props, glows) => ({ id, name, kind: 'interior', size: { w, d }, light: CHINA_IN,
  ground: { base: '#2a2a20', skin: floor, tileM: 2 }, wall: '#2a2a1c', wallSkin: wall, buildings: [], props, glows, city: 'steel' });
export const LOCATIONS_CHINA = {
  steel_china: { id: 'steel_china', name: 'Steel-Megalopolis · China Lake', kind: 'exterior', size: { w: 48, d: 36 }, light: CHINA,
    ground: { base: '#22241c', skin: 'g_sv', tileM: 5, clean: true, tint: 'rgba(8,12,4,.5)',
      water: [{ ...LAKE, tileM: 6, lanterns: [[16.5, 13.4], [21, 16.8], [25.5, 13.6], [31.5, 17.2], [18, 20.6], [24.6, 21.4], [30.6, 24.4], [15.6, 24.8], [27.2, 16.2]].map(([x, z]) => ({ x, z })) }],
      zones: [ { x: 0, z: 8.5, w: 48, d: 3.5, kind: 'plate', tint: 'rgba(30,26,14,.55)' }, { x: 0, z: 26, w: 48, d: 5, kind: 'plate', tint: 'rgba(30,26,14,.55)' } ] }, // quais en planches et béton
    buildings: BUILDINGS_CHINA, props: [],
    glows: [ // ampoules ambre des stands, lanternes rouges flottantes (reflets), une lueur bile au ras de l'eau
      ...STANDS.map(([, sp, x, z]) => ({ x: x + 1.25, z: z + FP[sp][1] + 0.4, rx: 1.8, rz: 1.2, color: AMBRE, i: 0.6, flicker: true })),
      ...[[16.5, 13.4], [21, 16.8], [25.5, 13.6], [31.5, 17.2], [18, 20.6], [24.6, 21.4], [30.6, 24.4], [15.6, 24.8], [27.2, 16.2]].map(([x, z], i) => ({ x, z, rx: 1.3, rz: 0.9, color: ROUGE, i: 0.45, flicker: i % 2 === 0 })),
      { x: 24, z: 19, rx: 9, rz: 6, color: BILE, i: 0.18 }, { x: 11.5, z: 9.6, rx: 2.4, rz: 1.4, color: AMBRE, i: 0.6 }, { x: 35, z: 7, rx: 3, rz: 1.6, color: ROUGE, i: 0.5 },
      { x: 44, z: 27, rx: 2, rz: 1.2, color: AMBRE, i: 0.45 }, { x: 24, z: 2, rx: 2.4, rz: 1.6, color: AMBRE, i: 0.45 }, { x: 46, z: 32, rx: 2, rz: 1.4, color: AMBRE, i: 0.35 } ],
    extras: [ ...[[18, 9.2], [25, 12.0], [35.4, 15.2], [35.2, 22.4], [20, 27.4], [26, 30.6], [8, 25], [6.5, 12.6], [44, 21]].map(([x, z], i) => ({ sprite: `st_civil${i % 6}`, x, z, face: i % 2 ? 1 : -1, role: 'client' })) ],
    walkers: [ { sprite: 'st_civil3', path: [[2, 10], [46, 10]], speed: 0.7, t0: 3 }, { sprite: 'st_civil5', path: [[35.5, 10], [35.5, 27.5], [8, 27.5]], speed: 0.6, t0: 9 },
      { sprite: 'st_civil1', path: [[7.5, 27], [7.5, 11]], speed: 0.6, t0: 17 } ],
    spawn: { player: { x: 24, z: 1 }, companion: { x: 23, z: 1.5 } }, city: 'steel',
    arrive: { from: 'steel_asia', text: 'China Lake. Le lac noir au milieu, et autour, des tables à perte de vue : implants, armes, papiers. Les ampoules ambre se reflètent dans le pétrole. On te dévisage.' } },
  // Intérieurs [plan §3] : style de l'extérieur (CHINA_IN), sortie au sud, seuil à 1 m. Mobilier = réemplois du manifeste d'intérieurs.
  the_in: IN('the_in', 'China Lake · Maison de thé', 12, 9, 'f_wood', 'w_planks', [
    { furn: 'home_curtain', x: 0.4, z: 0.2 }, { furn: 'home_curtain', x: 10.2, z: 0.2 }, { furn: 'bar_table_b', x: 2.2, z: 5.2 }, { furn: 'bar_table_b', x: 8.6, z: 5.2 },
    { furn: 'sv_cardtable_b', x: 5.2, z: 4.6 }, { furn: 'm_desk', x: 4.8, z: 0.3 }, { furn: 'bar_backshelf_b', x: 8.4, z: 0.2 } ],
    [{ x: 6, z: 2.4, rx: 3, rz: 1.8, color: ROUGE, i: 0.5 }, { x: 6, z: 6, rx: 4, rz: 2.4, color: AMBRE, i: 0.45 }]),
  dragon_in: IN('dragon_in', 'China Lake · Pavillon du Dragon', 12, 9, 'f_tiles', 'w_brick', [
    { furn: 'bar_counter_b', x: 0.4, z: 0.4 }, { sprite: 'stove', x: 3.4, z: 0.6 }, { furn: 'bar_table_b', x: 3.0, z: 5.0 }, { furn: 'bar_table_b', x: 6.6, z: 5.0 },
    { furn: 'bar_table_b', x: 9.4, z: 3.0 }, { furn: 'bar_backshelf_b', x: 9.0, z: 0.2 } ],
    [{ x: 2, z: 1.4, rx: 2.4, rz: 1.6, color: AMBRE, i: 0.6, flicker: true }, { x: 7, z: 5.4, rx: 4, rz: 2.4, color: ROUGE, i: 0.35 }]),
  filets_in: IN('filets_in', 'China Lake · Les Filets', 10, 8, 'f_sv_plates', 'w_sv_tin', [
    { furn: 'sv_workbench', x: 0.3, z: 0.3 }, { furn: 'sv_shelf', x: 3.8, z: 0.2 }, { furn: 'home_mattress_d', x: 7.6, z: 0.4 }, { sprite: 'barrel', x: 8.4, z: 5.6 },
    { sprite: 'rubble', x: 1.0, z: 5.6 }, { box: true, x: 5.6, z: 4.4, w: 1, d: 0.8, h: 0.08, color: '#2a2418' } ], // box = trappe de la cache sous le plancher (PROVISOIRE)
    [{ x: 4, z: 3, rx: 2.6, rz: 1.8, color: AMBRE, i: 0.5 }]),
};
const J = (id, loc, ox, oz, tx, tz, to, label, conditions = []) => ({ id, location: loc, junction: true, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: { doorId: to }, conditions });
const DOOR = (id, bid, ox, oz, to) => ({ id, buildingId: bid, location: 'steel_china', opening: { x: ox, z: oz, side: 'south' }, threshold: { x: ox, z: oz + 1 }, target: { doorId: to }, conditions: [] });
const OUT = (id, loc, w, d, to) => ({ id, location: loc, opening: { x: w / 2, z: d, side: 'south' }, threshold: { x: w / 2, z: d - 1 }, target: { doorId: to }, conditions: [] });
export const DOORS_CHINA = [
  J('k_nord', 'steel_china', 24, 0, 24, 1, 'a_sud', 'Le Barrage (Asia-Ground)'),           // [plan] sortie libre
  J('k_est', 'steel_china', 48, 32, 47, 32, 'l_sud_est', 'Ruelle (Lower-Town)'),            // [plan] libre
  DOOR('cl_dragon_door', 'cl_dragon', 11.5, 8.5, 'dragon_in_door'), OUT('dragon_in_door', 'dragon_in', 12, 9, 'cl_dragon_door'),
  DOOR('cl_the_door', 'cl_the', 35, 6, 'the_in_door'), OUT('the_in_door', 'the_in', 12, 9, 'cl_the_door'),
  DOOR('cl_filets_door', 'cl_filets', 44, 26, 'filets_in_door'), OUT('filets_in_door', 'filets_in', 10, 8, 'cl_filets_door'),
];
const behind = id => { const s = STANDS.find(q => q[0] === id); return { x: s[2] + 1.25, z: s[3] - 0.7 }; }; // marchand côté nord de l'étal [plan]
export const NPCS_CHINA = [ // positions corrigées d'après CHINA_LAKE.md (Régie 9a33b8c) : >= 1,5 m du centre des stands, jamais sur l'eau
  { id: 'cl_shen', name: 'Shen', sprite: 'gen_cl_shen', location: 'steel_china', x: 7.6, z: 18.6, faceTo: [12, 18.6], dialogue: 'cl_shen' },
  { id: 'cl_m_nord', name: 'Marchande d\u2019implants', sprite: 'gen_cl_m_nord', location: 'steel_china', x: 17.25, z: 9.5, faceTo: [17.25, 13], dialogue: 'cl_m_nord' },
  { id: 'cl_m_est', name: 'Armurier', sprite: 'gen_cl_m_est', location: 'steel_china', ...behind('cl_s_armes'), faceTo: [36, 14], dialogue: 'cl_m_est' },
  { id: 'cl_m_sud', name: 'Faussaire', sprite: 'gen_cl_m_sud', location: 'steel_china', x: 19.1, z: 28.6, faceTo: [17.25, 31], /* au bout de l'étal : derrière, le sprite du stand masquait le tap */ dialogue: 'cl_m_sud' },
  { id: 'cl_m_ouest', name: 'Apothicaire', sprite: 'gen_cl_m_ouest', location: 'steel_china', x: 11.75, z: 12.8, faceTo: [9, 15], dialogue: 'cl_m_ouest' },
  { id: 'cl_tech', name: 'Le technicien', sprite: 'gen_cl_tech', location: 'steel_china', x: 25.7, z: 27.1, faceTo: [24, 30], dialogue: 'cl_tech' },
  { id: 'cl_zhou', name: 'Madame Zhou', sprite: 'gen_cl_zhou', location: 'the_in', x: 6, z: 2, faceTo: [6, 9], dialogue: 'cl_zhou' },
  { id: 'cl_main1', name: 'Homme de main', sprite: 'gen_cl_main1', location: 'the_in', x: 2, z: 4, faceTo: [6, 9], dialogue: 'cl_main' },
  { id: 'cl_main2', name: 'Homme de main', sprite: 'gen_cl_main2', location: 'the_in', x: 10, z: 4, faceTo: [6, 9], dialogue: 'cl_main' },
  { id: 'cl_serveur', name: 'Serveur', sprite: 'gen_cl_serveur', location: 'dragon_in', x: 2.4, z: 3.2, faceTo: [6, 9], dialogue: 'cl_serveur' },
  { id: 'cl_lo', name: 'Vieux Lo', sprite: 'gen_cl_lo', location: 'dragon_in', x: 9, z: 6, faceTo: [6, 9], dialogue: 'cl_lo' },
  { id: 'cl_yu', name: 'Yu', sprite: 'gen_cl_yu', location: 'filets_in', x: 4, z: 3, faceTo: [5, 8], dialogue: 'cl_yu' },
];
// Répliques et services de base [inventé, d'après la DA : marchandage à voix basse, l'étranger dévisagé]. Prix en crédits. Aucune quête, aucun achat d'objet (lot 4).
const D = (t1, t2, svc = []) => ({ start: { text: t1, options: [ ...svc, { label: 'Et sinon ?', next: 'b' }, { label: 'Au revoir.', next: 'end' } ] },
  b: { text: t2, options: [ { label: 'Au revoir.', next: 'end' } ] },
  servi: { text: 'Mange. Et ne parle pas trop fort.', options: [ { label: 'Merci.', next: 'end' } ] },
  pauvre: { text: 'Pas de crédits, pas d\u2019affaire.', options: [ { label: 'Au revoir.', next: 'end' } ] } });
export const DIALOGUES_CHINA = {
  cl_shen: D('Shen. Je lis les puces que personne ne doit lire. Pas ce soir : j\u2019ai les mains dans l\u2019eau.', 'Le lac garde tout. Les puces, les armes, les types qui parlaient trop.'),
  cl_m_nord: D('Implants « garantis ». Garantis quoi ? Garantis vendus.', 'Les puces viennent d\u2019IO. Enfin, elles en venaient.'),
  cl_m_est: D('Tu regardes ou tu achètes ? Ici on ne regarde pas longtemps.', 'Sans numéro, sans histoire. Comme toi, on dirait.'),
  cl_m_sud: D('Un nom, une photo, un tampon. Le tampon, c\u2019est le plus cher.', 'Le Bureau des Emplacements vend des places. Moi je vends des gens.'),
  cl_m_ouest: D('Stimulants, calmants, antibiotiques coupés à peine. Tu as mal où ?', 'Chez Lau c\u2019est propre. Ici c\u2019est ouvert la nuit. Ici c\u2019est toujours la nuit.'),
  cl_tech: D('Pose ça là. Non, pas là, là. Tout ce qui a un circuit, je l\u2019ouvre.', 'Un jour je trouverai l\u2019ordinateur d\u2019avant. En attendant je répare des radios.'),
  cl_zhou: D('Assieds-toi. Le thé est offert. Le reste, rien ne l\u2019est.', 'Asia-Ground paie son loyer. China Lake garde ses comptes. Chacun sa place.'),
  cl_main: D('…', 'Madame Zhou parle. Nous, on écoute.'),
  cl_serveur: D('Une table ? Bol du jour, cinq crédits.', 'En haut, c\u2019est privé. Les marches aussi.', [{ label: 'Le bol du jour (5 cr).', action: 'paycr:5;give:meal', next: 'servi' }]),
  cl_lo: D('Les câbles, je les ai tendus moi-même, il y a trente ans. Les lanternes aussi.', 'Le lac était propre, avant. Personne ne me croit.'),
  cl_yu: D('Ferme la porte, l\u2019humidité rentre. Tu cherches quelque chose qu\u2019on a repêché ?', 'Tout ce qui tombe dans le lac finit chez moi. Presque tout.'),
};
