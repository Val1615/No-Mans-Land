// Lower-Town v1 (zone steel_lower) : décor, accès, PNJ d'ambiance. SANS quêtes. Fiche : docs/villes/steel/quartiers/LOWER_TOWN.md (Production),
// DA : docs/DA_QUARTIERS.md d'Ocre (branche creation/quartiers). [fiche] = repris de la fiche ; [inventé] = choix de Volonté pour ce lot.
// Géographie [décision Valentin, 22/10/2026] : Lower-Town au sol, même secteur que Center-Town ; Center-Town = dalle haute visible au nord.
// Palette [fiche §2, DA §3] : suie, gris acier, rouille, sodium et four. Ni violet ni cyan.
const LOWER = { bg: '#0d0a07', hemi: ['#e8b070', '#16130f', 1.05], sun: ['#ffb060', 0.6], tint: '#d6b48a', actor: '#e4c9a6' };
const SODIUM = '#e8a13a', FOUR = '#c9541e';
// Bâtiments : sprites d'Ocre (creation/lower-town-sprites da01a62) ; `ph` = volume de repli si un sprite manque. Pour passer au sprite d'Ocre, il suffit que la clé `sprite` existe dans
// assets/buildings/manifest.json (view.js n'utilise le volume `ph` que si le sprite est absent). Emprise x, z, w, d = mètres.
const B = (id, label, sprite, x, z, w, d, ph, extra = {}) => ({ id, label, sprite, x, z, w, d, visitable: false, cue: null, named: true, ph, ...extra });
export const BUILDINGS_LOWER = [
  // [décision] la dalle de Center-Town au-dessus des toits : dessous, pylônes, feux ambrés. Seuls les pylônes sont pleins. sprite Ocre lt_dalle_center (d02551d)
  B('lt_dalle', 'Dalle de Center-Town', 'lt_dalle_center', 0, 0, 48, 2.5, { kind: 'dalle', h: 15 }, { named: false, solid: [0, 1, 2, 3, 4].map(i => ({ x: 1 + i * 10.5, z: 0, w: 3.4, d: 2.5 })) }), // socles des pylônes mesurés sur le sprite (≈ 244 px = 3,5 m ; centres alignés à 2,7 + 10,5 i)
  B('lt_usine7', 'Pointage Usine 7', 'lt_atelier_usine', 25, 1, 7, 14, { h: 9, color: '#3d3a36', roof: 'sheds', chimney: [2, 2] }, { visitable: true }), // sprite Ocre da01a62
  B('lt_bastide', 'Atelier Bastide', 'lt_atelier_petit', 36, 7, 8, 6, { h: 4.5, color: '#43362c', roof: 'sheds' }, { visitable: true }),
  B('lt_immeuble', 'Immeuble ouvrier', 'lt_immeuble_ouvrier', 5, 5, 8, 6.5, { h: 13, floors: 4 }),                    // sprite Ocre da01a62
  B('lt_immeuble3', 'Immeuble ouvrier', 'lt_immeuble_ouvrier', 14.5, 5, 8, 6.5, { h: 13, floors: 4 }),                // idem (flip non géré pour les bâtiments)
  B('lt_moss', 'Chez Moss', 'lt_comptoir_moss', 37, 24.5, 6, 5, { h: 7 }, { visitable: true }),                         // sprite Ocre 711de0a
  // Props d'Ocre (lot 2, 711de0a) : sprites ancrés du manifeste des bâtiments, posés comme bâtiments anonymes (x, z = coin min, emprise du manifeste).
  ...[['lt_tuyau', 18.5, 13, 3, 2], ['lt_tuyau', 33, 13, 3, 2], ['lt_sodium', 9.6, 14.8, 0.8, 0.8], ['lt_sodium', 25.6, 15.6, 0.8, 0.8], ['lt_sodium', 39.6, 20.6, 0.8, 0.8],
    ['lt_sodium', 20.6, 28.2, 0.8, 0.8], ['lt_horloge_pointage', 24, 20.9, 1, 1], ['lt_voiture_panne', 30, 19.4, 4, 2], ['lt_voiture_panne', 1.5, 32.5, 4, 2],
    ['lt_bidons', 33.3, 15.4, 0.6, 0.6], ['lt_bidons', 34.1, 15.6, 0.6, 0.6], ['lt_ferraille', 44.6, 13.4, 1.5, 1], ['lt_palettes', 46.5, 11, 1, 1], ['lt_palettes', 17.6, 30, 1, 1],
    ['lt_grille_fosse', 44.5, 33.6, 2, 2, []], ['lt_flaque', 11, 20.6, 2.5, 1.5, []], ['lt_flaque', 34, 21.6, 2.5, 1.5, []], ['lt_tuyau_coude', 32.5, 3, 2.5, 2.5], ['lt_passerelle', 23.4, 2.5, 1.5, 6]]
    .map(([sp, x, z, w, d, solid], i) => ({ id: `lt_prop${i}`, label: '', sprite: sp, x, z, w, d, visitable: false, cue: null, ...(solid ? { solid } : {}) })),
  // lt_tuyau_coude et lt_passerelle : version corrigée d'Ocre (37d3cbb) ; passerelle = Passerelle haute [fiche], décor (pas d'étage praticable)
  B('lt_foyer', 'Le Foyer Ruiz', 'lt_foyer_ruiz', 3, 24, 10, 7, { h: 5.5, roof: 'pitched' }, { visitable: true }),     // sprite Ocre da01a62
  // Portique de La Descente : sprite 7 x 2,5 m (arche ouverte vers le sud) ; posé au nord du bas de rampe, la rampe (z 16-20) passe devant.
  B('lt_portique', 'Portique de contrôle', 'lt_portique_io', 1.5, 13.5, 7, 2.5, { kind: 'arch', h: 7 }, { named: false }), // sprite Ocre da01a62
];
const LOWER_IN = { bg: '#0a0705', hemi: ['#ffc080', '#2a1a10', 1.2], sun: ['#ffae60', 1.0] };
const IN = (id, name, w, d, floor, wall, props, glows) => ({ id, name, kind: 'interior', size: { w, d }, light: LOWER_IN,
  ground: { base: '#3a3430', skin: floor, tileM: 2 }, wall: '#3a2a20', wallSkin: wall, buildings: [], props, glows, city: 'steel' });
export const LOCATIONS_LOWER = {
  steel_lower: { id: 'steel_lower', name: 'Steel-Megalopolis · Lower-Town', kind: 'exterior', size: { w: 48, d: 36 }, light: LOWER,
    ground: { base: '#2e2b27', skin: 'g_sv', tileM: 5, clean: true, tint: 'rgba(10,8,6,.45)', zones: [
      { x: 0, z: 15, w: 48, d: 6, kind: 'asphalt', tint: 'rgba(20,14,8,.45)' },            // Rue des Fours [fiche]
      { x: 0, z: 16, w: 9, d: 4, kind: 'plate', tint: 'rgba(40,30,20,.35)' },              // La Descente (bas de rampe) [fiche]
      { x: 20, z: 21, w: 10, d: 8, kind: 'plate', tint: 'rgba(30,24,18,.3)' },             // Place de la Relève [fiche]
      { x: 13.4, z: 21, w: 2, d: 12, kind: 'plate', tint: 'rgba(0,0,0,.45)' } ] },         // Allée du Foyer, 2 m [fiche]
    buildings: BUILDINGS_LOWER, props: [
      { sprite: 'rubble', x: 45, z: 9, fp: [2.0, 1.6] }, { sprite: 'tires', x: 16, z: 31, fp: [1.2, 1.0] }, { sprite: 'sv_brasero', x: 31, z: 24, fp: [0.8, 0.8] },
      { box: true, x: 15.4, z: 22, w: 2.2, d: 11, h: 2.6, color: '#2f2a25' },        // palissade de tôle : ferme l'Allée du Foyer à l'est [inventé]
    ],
    glows: [ { x: 10, z: 16.6, rx: 3, rz: 3, color: SODIUM, i: 0.7 }, { x: 26, z: 16.6, rx: 3, rz: 3, color: SODIUM, i: 0.7 }, { x: 40, z: 22.4, rx: 3, rz: 3, color: SODIUM, i: 0.65 },
      { x: 21, z: 30, rx: 3, rz: 3, color: SODIUM, i: 0.6 }, { x: 28.5, z: 15.6, rx: 3, rz: 2.2, color: FOUR, i: 0.85, flicker: true }, { x: 39, z: 14, rx: 2.2, rz: 1.6, color: FOUR, i: 0.75, flicker: true },
      { x: 31.4, z: 24.4, rx: 2.4, rz: 2.4, color: FOUR, i: 0.6, flicker: true }, { x: 6.4, z: 32, rx: 2, rz: 1.2, color: SODIUM, i: 0.45 }, { x: 4.5, z: 18, rx: 1.4, rz: 3, color: SODIUM, i: 0.5, flicker: true },
      { x: 24, z: 4, rx: 20, rz: 3, color: SODIUM, i: 0.18 } ],
    extras: [ ...[[23.5, 22.5], [24.4, 22.8], [25.3, 22.6], [26.2, 22.9], [27.1, 22.7]].map(([x, z], i) => ({ sprite: `st_civil${(i + 1) % 6}`, x, z, face: -1, role: 'relève' })) ], // file de la relève [fiche]
    walkers: [ { sprite: 'st_civil3', path: [[21, 26], [29, 26], [29, 27.5], [21, 27.5]], speed: 0.7, t0: 3 }, { sprite: 'st_civil0', path: [[29, 24.5], [21, 24.5]], speed: 0.8, t0: 20 }, // ouvriers, Place de la Relève [plan]
      { sprite: 'st_civil5', path: [[46, 19.2], [3, 19.2]], speed: 0.9, t0: 10 } ],
    spawn: { player: { x: 1, z: 18 }, companion: { x: 1, z: 19 } }, city: 'steel',
    arrive: { from: 'steel_center', text: 'La Descente. L\u2019air épaissit à chaque pas ; au-dessus, la dalle de Center-Town ferme le ciel. Ici, c\u2019est la nuit pour de bon.' } },
  // Intérieurs [plan §1] : style de l'extérieur (tôle, béton, sodium), LOWER_IN ; sortie au sud, seuil à 1 m. Mobilier = réemplois tels quels du manifeste d'intérieurs.
  foyer_in: IN('foyer_in', 'Lower-Town · Le Foyer Ruiz', 12, 9, 'f_sv_concrete', 'w_brick', [
    { furn: 'shop_counter', x: 0.4, z: 0.3 }, { furn: 'home_water', x: 3.2, z: 0.3 }, { furn: 'home_table', x: 2.0, z: 4.0 }, { furn: 'home_table', x: 5.2, z: 4.0 }, { furn: 'home_table', x: 2.0, z: 6.4 },
    { furn: 'home_curtain', x: 7.4, z: 2.8 }, { furn: 'home_mattress_d', x: 7.6, z: 0.3 }, { furn: 'home_mattress_d', x: 9.8, z: 0.3 }, { furn: 'home_mattress_d', x: 9.8, z: 1.6 },
    { sprite: 'stove', x: 11.2, z: 4.6 }, { box: true, x: 10.2, z: 7.4, w: 1.2, d: 0.9, h: 0.12, color: '#2a2016' } ], // box = trappe de cave fermée (PROVISOIRE)
    [{ x: 11.2, z: 5, rx: 2, rz: 2, color: FOUR, i: 0.6, flicker: true }, { x: 4, z: 5, rx: 4, rz: 3, color: SODIUM, i: 0.35 }]),
  bastide_in: IN('bastide_in', 'Lower-Town · Atelier Bastide', 10, 8, 'f_sv_plates', 'w_sv_tin', [
    { furn: 'sv_workbench', x: 0.3, z: 0.3 }, { furn: 'sv_workbench', x: 2.6, z: 0.3 }, { furn: 'sv_shelf', x: 8.2, z: 0.2 }, { sprite: 'rubble', x: 8.4, z: 5.2 },
    { sprite: 'barrel', x: 0.8, z: 5.6 }, { sprite: 'tires', x: 1.4, z: 3.6 }, { sprite: 'sv_brasero', x: 5.8, z: 0.8 } ], // brasero = four ; palan non disponible
    [{ x: 5.8, z: 1.4, rx: 2, rz: 2, color: FOUR, i: 0.7, flicker: true }]),
  moss_in: IN('moss_in', 'Lower-Town · Chez Moss', 10, 8, 'f_concrete', 'w_sv_planks', [
    { furn: 'sv_bar', x: 3.9, z: 2.6 }, { furn: 'bar_backshelf_b', x: 3.9, z: 0.2 }, { furn: 'home_curtain', x: 7.2, z: 0.2 },
    { furn: 'bar_table_b', x: 0.6, z: 4.6 }, { furn: 'bar_table_b', x: 3.0, z: 5.8 }, { furn: 'bar_table_b', x: 7.2, z: 4.4 }, { furn: 'sv_cardtable_b', x: 7.8, z: 6.4 } ],
    [{ x: 5, z: 3.5, rx: 2.4, rz: 1.6, color: SODIUM, i: 0.55 }]),
  pointage_in: IN('pointage_in', 'Lower-Town · Pointage Usine 7', 10, 8, 'f_sv_concrete', 'w_sv_tin', [
    { furn: 'shop_counter', x: 3.9, z: 2.6 }, { furn: 'm_desk', x: 4.2, z: 0.4 }, { furn: 'io_locker', x: 0.3, z: 0.2 }, { furn: 'io_locker', x: 0.3, z: 1.4 },
    { furn: 'io_locker', x: 0.3, z: 2.6 }, { furn: 'm_archive_shelf', x: 8.0, z: 0.2 }, { box: true, x: 5.9, z: 2.7, w: 0.4, d: 0.4, h: 1.9, color: '#4a4f53' } ], // box = horloge (PROVISOIRE: lt_horloge_pointage)
    [{ x: 5, z: 3.4, rx: 2.6, rz: 1.6, color: SODIUM, i: 0.5 }]),
};
const J = (id, loc, ox, oz, tx, tz, to, label, conditions = []) => ({ id, location: loc, junction: true, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: { doorId: to }, conditions });
const E = (id, loc, ox, oz, tx, tz, label, text) => ({ id, location: loc, edge: text, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: null, conditions: [] });
const DOOR = (id, bid, ox, oz, to) => ({ id, buildingId: bid, location: 'steel_lower', opening: { x: ox, z: oz, side: 'south' }, threshold: { x: ox, z: oz + 1 }, target: { doorId: to }, conditions: [] });
const OUT = (id, loc, w, d, to) => ({ id, location: loc, opening: { x: w / 2, z: d, side: 'south' }, threshold: { x: w / 2, z: d - 1 }, target: { doorId: to }, conditions: [] });
export const DOORS_LOWER = [
  J('l_ouest', 'steel_lower', 0, 18, 1, 18, 'c_est', 'La Descente (vers Center-Town)'), // [plan] c_est ↔ l_ouest ; Repérage +1 : système absent, non branché
  // [plan] l_fosse ↔ v_fosse : clé de Mère Ruiz (lt_cle_ruiz, lot 4) ou ouvert depuis le bas (lt_fosse_ouverte, posé en remontant)
  J('l_fosse', 'steel_lower', 42, 36, 42, 35, 'v_fosse', 'Escalier de la Fosse', [{ test: s => !!(s.flags.lt_cle_ruiz || s.flags.lt_fosse_ouverte), reason: 'fosse',
    text: 'Un escalier grillagé qui plonge vers la Sous-Ville. Cadenas neuf, chaîne neuve.' }]),
  J('v_fosse', 'sv_poutres', 18, 28, 18, 27, 'l_fosse', 'Escalier de la Fosse (vers Lower-Town)'),
  J('l_sud', 'steel_lower', 8, 36, 8, 35, 'a_nord', 'Vers Asia-Ground'),                                  // [plan] l_sud ↔ a_nord (lot 2), aucune condition
  J('l_sud_est', 'steel_lower', 30, 36, 30, 35, 'k_est', 'Ruelle (China Lake)'),                          // [plan] l_sud_est ↔ k_est (lot 3), libre dans les deux sens [décision du lot]
  DOOR('lt_foyer_door', 'lt_foyer', 9.5, 31, 'foyer_in_door'), OUT('foyer_in_door', 'foyer_in', 12, 9, 'lt_foyer_door'),
  DOOR('lt_bastide_door', 'lt_bastide', 40.5, 13, 'bastide_in_door'), OUT('bastide_in_door', 'bastide_in', 10, 8, 'lt_bastide_door'),
  DOOR('lt_moss_door', 'lt_moss', 41, 29.5, 'moss_in_door'), OUT('moss_in_door', 'moss_in', 10, 8, 'lt_moss_door'),
  DOOR('lt_usine7_door', 'lt_usine7', 28.5, 15, 'pointage_in_door'), OUT('pointage_in_door', 'pointage_in', 10, 8, 'lt_usine7_door'),
];
export const NPCS_LOWER = [ // sprites PROVISOIRES (réemplois), voir rapport ; positions intérieures du plan §1
  { id: 'lt_ruiz', name: 'Mère Ruiz', sprite: 'gen_vera', location: 'foyer_in', x: 3, z: 2, faceTo: [6, 9], dialogue: 'lt_ruiz' },
  { id: 'lt_pia', name: 'Pia', sprite: 'gen_sv_guetteuse', location: 'steel_lower', x: 14.4, z: 25.5, faceTo: [14.4, 20], dialogue: 'lt_pia' }, // Allée du Foyer
  { id: 'lt_bastide', name: 'Joaquim Bastide', sprite: 'gen_ezequiel', location: 'bastide_in', x: 7, z: 2, faceTo: [5, 8], dialogue: 'lt_bastide' },
  { id: 'lt_moss', name: 'Moss', sprite: 'gen_sv_receleur', location: 'moss_in', x: 5, z: 2, faceTo: [5, 8], dialogue: 'lt_moss' },
  { id: 'lt_raack', name: 'Ilse Raack', sprite: 'gen_odile', location: 'pointage_in', x: 5, z: 2, faceTo: [5, 8], dialogue: 'lt_raack' },
  { id: 'lt_dorn', name: 'Agent Dorn', sprite: 'gen_halloran', location: 'steel_lower', x: 20, z: 18, faceTo: [12, 18], dialogue: 'lt_dorn' }, // arrêt fixe sur la Rue des Fours (patrouille non gérée)
];
// Répliques d'ambiance [inventé, d'après envie / peur / voix de la fiche §5]. Aucune quête ; « Contrôle de nuit » (§6) non branché.
const D = (t1, t2, t3) => ({ start: { text: t1, options: [ { label: 'Continuer.', next: 'b' }, { label: 'Au revoir.', next: 'end' } ] },
  b: { text: t2, options: [ { label: 'Et alors ?', next: 'c' }, { label: 'Au revoir.', next: 'end' } ] }, c: { text: t3, options: [ { label: 'Au revoir.', next: 'end' } ] } });
export const DIALOGUES_LOWER = {
  lt_ruiz: D('Entre pas comme ça dans l\u2019allée, toi. Tu as faim ? Ça se voit.', 'Ici c\u2019est le foyer. Un lit, une soupe, quatre crédits la nuit. Tu payes quand tu peux, mais tu payes.',
    'Et tu ne poses pas de questions sur la cave. Personne n\u2019en pose. C\u2019est pour ça que tout le monde dort au chaud.'),
  lt_bastide: D('Attends. Elle tousse.', 'La presse. Pas toi. Elle a vingt ans de plus que l\u2019atelier, et l\u2019atelier appartient à l\u2019Usine.',
    'Un jour je le rachète. Ferraille au poids, pièces au détail. Ne demande pas d\u2019où.'),
  lt_raack: D('Équipe de nuit : quarante-deux pointés. Quarante-deux payés. Suivant.', 'Le guichet ouvre à la sirène. Implant au lecteur, pas au visage. Je ne regarde pas les visages.',
    'Les quotas, c\u2019est la seule chose qui tient l\u2019équipe en place. Les machines d\u2019IO n\u2019ont pas de quotas.'),
  lt_dorn: D('Alors, copain, on se promène ? Rue des Fours, la nuit, c\u2019est une drôle d\u2019idée.', 'Moi je fais ma ronde, les commerçants font leur petit geste, et tout le monde dort.',
    'La Sous-Ville ? Ils envoient là-bas ceux qui posent trop de questions. Tu en poses beaucoup ?'),
  lt_moss: D('Tu bois quoi ? Ou tu cherches quoi ?', 'Ici on change, on écoute, on oublie. Les dollars aussi, sous le comptoir. Qui t\u2019a parlé de moi ?',
    'China Lake ? Pourquoi tu dis ce nom-là ici ? Tu veux que je baisse la voix, ou que tu sortes ?'),
  lt_pia: D('Hé, t\u2019es d\u2019en haut, toi ? T\u2019as vu le ciel ? Le vrai ?', 'Moi je porte des lettres. Vite. Je dis pas à qui, sinon c\u2019est plus des lettres, c\u2019est des ennuis !',
    'Et quand la sirène gueule, je cours. Tout le monde court. Ah ah ! T\u2019as sursauté !'),
};
