// v12 Steel-Megalopolis, lot L1 : la route et la douane (S0), puis Center-Town (S1). Voir docs/villes/STEEL_MEGALOPOLIS_PLAN.md.
// [décision] Valentin : entrée selon la race (augmenté / cyborg passent avec l'implant, humain refusé, mutant attaqué à vue) ;
// premier quartier = Center-Town ; la quête s'arrête une fois en ville. Le reste (PNJ, textes, plan, taux) = [proposition].
import { BUILDINGS_ROUTE, PAINTED_DOORS_ROUTE, BUILDINGS_CENTER, PAINTED_DOORS_CENTER } from './buildings_steel.js';

const named = list => list.map(b => ({ ...b, named: true }));
// v13 : nuit de Steel (concept art docs/villes/steel/ambiance/concept_center_town.jpg). light = éclairage du lieu (view.js),
// extras = figurants immobiles (file d'attente, soldats), walkers = passants, drones = drones en orbite, glows = lumières au sol.
const SOLDAT = 'gen_halloran';
const civ = i => `st_civil${i % 6}`;
const NIGHT_ROUTE = { bg: '#0c0f18', hemi: ['#8090b8', '#2a2430', 0.95], sun: ['#a8b8ff', 0.55], tint: '#c4c8d8', actor: '#c9cddc' };
const NIGHT_CITY = { bg: '#0b0a16', hemi: ['#aab4ff', '#4a2a5c', 1.35], sun: ['#c0b0ff', 0.7], tint: '#9092b8', actor: '#d4d4ea' };
const NEON_V = '#c247ff', NEON_C = '#2fd8ff', WARM = '#ffae55', FLOOD = '#d8ecff';
export const LOCATIONS = {
  // S0 : place forte d'IO devant le sarcophage [décision v13] : porte en haut à droite au bout de la route, poste de douane à gauche,
  // file d'attente, soldats, miradors, tourelles, barbelés, projecteurs, check-point sur la route.
  steel_route: { id: 'steel_route', name: 'Steel-Megalopolis · La douane', kind: 'exterior', size: { w: 48, d: 36 }, light: NIGHT_ROUTE,
    ground: { base: '#5d5446', skin: 'g_sand', tint: 'rgba(8,12,30,.45)', zones: [
      { x: 31, z: 8, w: 6, d: 28, kind: 'asphalt' }, { x: 17, z: 8, w: 30, d: 4, kind: 'plate', tint: 'rgba(0,0,0,.25)' }, { x: 2, z: 28, w: 35, d: 5, kind: 'plate', tint: 'rgba(0,0,0,.2)' } ] },
    buildings: named(BUILDINGS_ROUTE).map(b => b.id === 'r_service' ? b : { ...b, tint: '#ffffff' }), props: [
      // check-point : barricades de part et d'autre de la route, passage gardé au milieu
      { sprite: 'st_barricade', x: 29.4, z: 26.2, fp: [3.4, 0.8] }, { sprite: 'st_barricade', x: 39.0, z: 26.2, fp: [3.4, 0.8] },
      { sprite: 'st_barricade', x: 25.8, z: 26.2, fp: [3.4, 0.8] }, { sprite: 'st_barricade', x: 42.6, z: 26.2, fp: [3.4, 0.8] },
      { sprite: 'st_barricade', x: 19.5, z: 13.4, fp: [3.4, 0.8] }, { sprite: 'st_barricade', x: 23.1, z: 13.4, fp: [3.4, 0.8] }, { sprite: 'st_barricade', x: 44.6, z: 13.4, fp: [3.4, 0.8] },
      { sprite: 'st_barricade', x: 14.4, z: 34.6, fp: [3.4, 0.8] }, { sprite: 'st_barricade', x: 18.0, z: 34.6, fp: [3.4, 0.8] }, { sprite: 'st_barricade', x: 21.6, z: 34.6, fp: [3.4, 0.8] },
      { sprite: 'st_mirador', x: 15.2, z: 9.6, fp: [2.4, 2.4] }, { sprite: 'st_mirador', x: 45.4, z: 18.0, fp: [2.4, 2.4] }, { sprite: 'st_mirador', x: 1.6, z: 9.0, fp: [2.4, 2.4] }, { sprite: 'st_mirador', x: 2.0, z: 34.4, fp: [2.4, 2.4] },
      { sprite: 'st_tourelle', x: 27.6, z: 14.2, fp: [2.0, 2.0] }, { sprite: 'st_tourelle', x: 40.4, z: 14.2, fp: [2.0, 2.0] }, { sprite: 'st_tourelle', x: 14.2, z: 26.6, fp: [2.0, 2.0] },
      { sprite: 'st_projecteur', x: 24.6, z: 19.4, solid: 0.5 }, { sprite: 'st_projecteur', x: 43.2, z: 23.6, solid: 0.5 }, { sprite: 'st_projecteur', x: 29.2, z: 31.6, solid: 0.5 },
      { sprite: 'sandbags', x: 30.0, z: 23.4 }, { sprite: 'sandbags', x: 38.2, z: 23.4 }, { sprite: 'sandbags', x: 24.0, z: 26.4 },
      { sprite: 'barrel', x: 22.6, z: 23.6 }, { sprite: 'rubble', x: 46, z: 33 }, { sprite: 'tires', x: 24.5, z: 32.2 }, { sprite: 'wreck', x: 8, z: 5, fp: [4.6, 2.4] } ],
    glows: [ { x: 24.6, z: 21.5, rx: 4.5, rz: 4.5, color: FLOOD, i: 0.5 }, { x: 41.5, z: 24.5, rx: 4, rz: 4, color: FLOOD, i: 0.45 }, { x: 31, z: 31, rx: 4, rz: 4, color: FLOOD, i: 0.4 },
      { x: 34, z: 10.5, rx: 6, rz: 3, color: NEON_C, i: 0.35 }, { x: 9, z: 29.6, rx: 2.2, rz: 1.6, color: NEON_C, i: 0.55, flicker: true }, { x: 21, z: 10.4, rx: 3, rz: 1.6, color: NEON_V, i: 0.3 },
      { x: 44, z: 10.4, rx: 3, rz: 1.6, color: NEON_V, i: 0.3 } ],
    extras: [
      // file d'attente devant le guichet (vers l'est, le long de la place)
      ...[[10.4, 31.0], [11.5, 31.3], [12.7, 31.1], [13.9, 31.4], [15.1, 31.2], [16.3, 31.5], [17.5, 31.2], [18.7, 31.4]].map(([x, z], i) => ({ sprite: civ(i), x, z, face: -1, role: 'file' })),
      // soldats : porte, tourelles, check-point, poste
      ...[[29.6, 10.6, 1], [38.4, 10.6, -1], [26.4, 11.0, 1], [42.2, 11.2, -1], [31.4, 24.8, 1], [37.0, 24.8, -1], [7.2, 29.8, 1], [12.4, 29.2, -1], [20.6, 30.0, -1], [33.6, 15.6, 1]]
        .map(([x, z, f]) => ({ sprite: SOLDAT, x, z, face: f, role: 'soldat' })) ],
    walkers: [ { sprite: SOLDAT, path: [[18, 11.4], [46, 11.4]], speed: 0.9, role: 'soldat' } ],
    spawn: { player: { x: 34, z: 34 }, companion: { x: 35, z: 34 } }, city: null,
    arrive: { from: 'dusk_q2', text: 'Une journée de marche vers l\u2019est. Le dôme grandit pendant des heures, puis il n\u2019y a plus que lui.' } },
  // Poste de douane : intérieur IO (mobilier de la maquette io-interiors et générés, angle corrigé v4) [décision v13 : cohérent avec l'extérieur]
  douane_in: { id: 'douane_in', name: 'Steel-Megalopolis · Poste de douane', kind: 'interior', size: { w: 10, d: 7 },
    light: { bg: '#07090e', hemi: ['#dfe8ff', '#28303f', 1.25], sun: ['#bcd4ff', 1.15] },
    ground: { base: '#2a2c30', skin: 'f_io_grate', tileM: 2 }, wall: '#2a2e36', wallSkin: 'w_io_dark', doorSkin: 'door_io', buildings: [], props: [
      { furn: 'io_server', x: 0.2, z: 0.2 }, { furn: 'io_reception', x: 2.9, z: 0.6 }, { furn: 'io_console', x: 4.6, z: 0.2 },
      { furn: 'io_locker', x: 8.4, z: 0.2 }, { furn: 'io_scanner', x: 7.6, z: 2.3 }, { furn: 'io_sofa', x: 0.2, z: 3.6 } ], city: null },
  // S1 : Center-Town sous le dôme, la nuit (concept art) : chaussée mouillée, néons, hologrammes, échoppes, passants, drones.
  steel_center: { id: 'steel_center', name: 'Steel-Megalopolis · Center-Town', kind: 'exterior', size: { w: 48, d: 36 }, light: NIGHT_CITY,
    ground: { base: '#1b1b22', skin: 'g_wet', tileM: 6, clean: true, zones: [
      { x: 0, z: 13, w: 48, d: 1.6, kind: 'plate', tint: 'rgba(10,10,20,.55)' }, { x: 0, z: 21.6, w: 48, d: 1.8, kind: 'plate', tint: 'rgba(10,10,20,.55)' } ] },
    buildings: named(BUILDINGS_CENTER).map(b => ['c_tour', 'c_change', 'c_arcadius'].includes(b.id) ? { ...b, tint: '#ffffff' } : b), props: [
      { sprite: 'st_echoppe', x: 33.2, z: 14.0, fp: [2.6, 1.2] }, { sprite: 'st_kiosque', x: 14.2, z: 13.9, fp: [1.4, 1.0] }, { sprite: 'st_echoppe', x: 46.2, z: 22.6, fp: [2.6, 1.2] },
      { sprite: 'st_lampadaire', x: 9, z: 14.4, solid: 0.4 }, { sprite: 'st_lampadaire', x: 24, z: 14.4, solid: 0.4 }, { sprite: 'st_lampadaire', x: 40, z: 14.4, solid: 0.4 },
      { sprite: 'st_lampadaire', x: 15, z: 22.2, solid: 0.4 }, { sprite: 'st_lampadaire', x: 31, z: 22.2, solid: 0.4 },
      { sprite: 'st_holo', x: 27.6, z: 14.2, solid: 0.4, glow: 0.9 }, { sprite: 'st_holo', x: 20.2, z: 22.6, solid: 0.4, glow: 0.9, flip: true }, { sprite: 'st_holo', x: 44.8, z: 14.0, solid: 0.4, glow: 0.85 },
      { sprite: 'st_borne', x: 35.8, z: 22.6, fp: [0.8, 0.6] }, { sprite: 'st_banc', x: 26.0, z: 22.8, fp: [1.8, 0.6] }, { sprite: 'st_pylone', x: 2.6, z: 13.8, fp: [0.7, 0.7] },
      { sprite: 'st_voiture', x: 41.5, z: 20.4, fp: [4.4, 2.0] } ],
    glows: [
      { x: 10, z: 16, rx: 2.1, rz: 4.4, color: NEON_V, i: 0.8 }, { x: 14.6, z: 16.2, rx: 1.8, rz: 3.9, color: NEON_V, i: 0.85, flicker: true }, { x: 21, z: 15.6, rx: 3.1, rz: 4.2, color: NEON_C, i: 0.8 },
      { x: 27.6, z: 16.6, rx: 2.6, rz: 4.4, color: NEON_C, i: 0.95, flicker: true }, { x: 33.2, z: 15.8, rx: 2.9, rz: 3.1, color: WARM, i: 0.8 }, { x: 40, z: 16, rx: 2.3, rz: 3.9, color: NEON_C, i: 0.75 },
      { x: 44.8, z: 16.4, rx: 2.6, rz: 3.9, color: NEON_V, i: 0.85, flicker: true }, { x: 15, z: 20.2, rx: 2.3, rz: 3.9, color: NEON_C, i: 0.75 }, { x: 20.2, z: 20.4, rx: 2.6, rz: 4.2, color: NEON_V, i: 0.9, flicker: true },
      { x: 31, z: 20.2, rx: 2.3, rz: 3.9, color: NEON_C, i: 0.75 }, { x: 46, z: 20.6, rx: 2.6, rz: 3.1, color: WARM, i: 0.75 }, { x: 6, z: 18, rx: 3.4, rz: 4.4, color: NEON_V, i: 0.6 },
      { x: 24, z: 9, rx: 9.1, rz: 5.2, color: NEON_C, i: 0.45 }, { x: 39.5, z: 13.4, rx: 4.7, rz: 2.1, color: NEON_C, i: 0.8 }, { x: 9, z: 15.2, rx: 1.8, rz: 1.8, color: FLOOD, i: 0.6 }, { x: 24, z: 15.2, rx: 1.8, rz: 1.8, color: FLOOD, i: 0.6 }, { x: 40, z: 15.2, rx: 1.8, rz: 1.8, color: FLOOD, i: 0.6 },
      { x: 15, z: 21.4, rx: 1.8, rz: 1.8, color: FLOOD, i: 0.6 }, { x: 31, z: 21.4, rx: 1.8, rz: 1.8, color: FLOOD, i: 0.6 }, { x: 2.5, z: 18, rx: 2.4, rz: 3.6, color: NEON_C, i: 0.6, flicker: true },
      { x: 13.4, z: 9.2, rx: 2.1, rz: 2.9, color: WARM, i: 0.75 } ],
    extras: [ { sprite: SOLDAT, x: 34.0, z: 13.6, face: -1, role: 'soldat' }, { sprite: SOLDAT, x: 44.2, z: 12.9, face: -1, role: 'soldat' },
      { sprite: civ(2), x: 32.0, z: 15.4, face: 1, role: 'client' }, { sprite: civ(4), x: 34.6, z: 15.6, face: -1, role: 'client' } ],
    walkers: [ { sprite: civ(0), path: [[2, 14.2], [46, 14.2], [46, 14.8], [2, 14.8]], speed: 1.1, t0: 5 }, { sprite: civ(1), path: [[46, 22.4], [2, 22.4], [2, 23.0], [46, 23.0]], speed: 0.9, t0: 30 },
      { sprite: civ(3), path: [[2, 14.6], [46, 14.6], [46, 14.0], [2, 14.0]], speed: 1.0, t0: 60 }, { sprite: civ(5), path: [[46, 22.8], [2, 22.8], [2, 22.2], [46, 22.2]], speed: 1.2, t0: 12 },
      { sprite: civ(4), path: [[18, 15], [18, 21.5], [19, 21.5], [19, 15]], speed: 0.8 }, { sprite: civ(2), path: [[36.5, 15], [36.5, 21.5], [37.4, 21.5], [37.4, 15]], speed: 0.9, t0: 4 },
      { sprite: civ(1), path: [[4, 22.6], [44, 22.6], [44, 23.1], [4, 23.1]], speed: 1.05, t0: 50 } ],
    drones: [ { x: 22, z: 17, r: 7, y: 6, speed: 0.22 }, { x: 38, z: 18, r: 5, y: 5.2, speed: -0.3, ph: 2 }, { x: 10, z: 18, r: 4, y: 6.5, speed: 0.35, ph: 4 } ],
    spawn: { player: { x: 1, z: 18 }, companion: { x: 1, z: 19 } }, city: 'steel' },
  change_in: { id: 'change_in', name: 'Center-Town · Change de Teng', kind: 'interior', size: { w: 6, d: 5 },
    light: { bg: '#07090e', hemi: ['#ffd9b0', '#2a2030', 1.2], sun: ['#ffc890', 1.0] },
    ground: { base: '#22232a', skin: 'f_io_dark', tileM: 2 }, wall: '#2a2e36', wallSkin: 'w_io_dark', doorSkin: 'door_io', buildings: [], props: [
      { furn: 'io_console', x: 1.4, z: 0.3 }, { furn: 'io_locker', x: 4.3, z: 0.2 } ], city: 'steel' },
};
const painted = (list, loc, T) => list.map(d => ({ id: d.id, buildingId: d.buildingId, location: loc, opening: { x: d.opening[0], z: d.opening[1], side: d.face === 's' ? 'south' : 'east' },
  threshold: { x: d.threshold[0], z: d.threshold[1] }, target: { doorId: T[d.id] }, conditions: [] }));
const J = (id, loc, ox, oz, tx, tz, to, label, conditions = []) => ({ id, location: loc, junction: true, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: { doorId: to }, conditions });
const E = (id, loc, ox, oz, tx, tz, label, text) => ({ id, location: loc, edge: text, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: null, conditions: [] });
export const ROUTE_TEXT = 'La route file vers l\'est, celle des camions. Personne ne la prend à pied.';
export const DOORS = [
  // La route des patrouilles (bord est du Transit) s'ouvre quand la porte d'acier est derrière toi [proposition, plan §2]
  J('j_q2_est', 'dusk_q2', 48, 18, 47, 18, 'j_route_sud', 'Route des patrouilles', [{ test: s => !!s.flags.q_fin, reason: 'route', text: ROUTE_TEXT }]),
  J('j_route_sud', 'steel_route', 34, 36, 34, 35, 'j_q2_est', 'Vers Dusk-Town'),
  ...painted(PAINTED_DOORS_ROUTE, 'steel_route', { r_douane_door: 'douane_in_sud' }).map(d => ({ ...d,
    conditions: [{ test: s => !s.flags.race_mutant, reason: 'mutant', text: 'Le soldat lève son arme avant que tu touches la porte.' }] })),
  { id: 'douane_in_sud', location: 'douane_in', opening: { x: 2, z: 7, side: 'south' }, threshold: { x: 2, z: 6 }, target: { doorId: 'r_douane_door' }, conditions: [] },
  { id: 'douane_in_est', location: 'douane_in', label: 'Vers Center-Town', opening: { x: 10, z: 4, side: 'east' }, threshold: { x: 9, z: 4 }, target: { doorId: 'c_ouest' },
    conditions: [{ test: s => !!s.flags.steel_passe, reason: 'douane', text: 'La barrière reste baissée. Il faut d\u2019abord passer au guichet.' }] },
  J('c_ouest', 'steel_center', 0, 18, 1, 18, 'douane_in_est', 'Vers la douane'),
  ...painted(PAINTED_DOORS_CENTER, 'steel_center', { c_change_door: 'change_in_door' }),
  { id: 'change_in_door', location: 'change_in', opening: { x: 3, z: 5, side: 'south' }, threshold: { x: 3, z: 4 }, target: { doorId: 'c_change_door' }, conditions: [] },
  E('c_est', 'steel_center', 48, 18, 47, 18, 'Vers les autres quartiers', 'L\u2019avenue continue vers Lower-Town et Asia-Ground. Plus tard. D\u2019abord, apprendre celui-ci.'),
  E('r_ouest', 'steel_route', 0, 30, 1, 30, 'Désert', 'Du sable, et le mur du dôme qui ne finit pas.'),
];
export const NPCS = [
  { id: 'odile', name: 'Odile Varga', sprite: 'gen_odile', location: 'douane_in', x: 2.1, z: 2.0, faceTo: [6, 2.4], dialogue: 'odile' },
  { id: 'halloran', name: 'Sergent Halloran', sprite: 'gen_halloran', location: 'steel_route', x: 36.2, z: 23.0, faceTo: [34, 34], dialogue: 'halloran' },
  { id: 'teng', name: 'Teng', sprite: 'gen_teng', location: 'change_in', x: 2.9, z: 1.6, faceTo: [3, 5], dialogue: 'teng' },
  { id: 'patrouilleur', name: 'Patrouilleur', sprite: 'gen_halloran', location: 'steel_center', x: 30.5, z: 19.8, faceTo: [22, 18], dialogue: 'patrouilleur' },
];
export const CLOSED_TEXT = {
  r_porte: 'La route entre dans le noir entre deux battants grands comme des immeubles. Sans passer la douane, les tourelles s\u2019en chargent.',
  r_service: s => s.flags.sol_passage ? 'La trappe dont parlait Sol. Chaîne neuve, cadenas neuf. Celui qui passe par là ne passe pas par le dessus.' : 'Une trappe de service à moitié ensablée, chaîne et cadenas. Des traces de pas fraîches, qui n\u2019en reviennent pas.',
  c_tour: 'La Rotonde. Des écrans sur toute la façade, et pas une porte qui s\u2019ouvre pour toi.',
  c_arcadius: 'Arcadius Center. Les portes s\u2019ouvrent pour les implants qu\u2019elles reconnaissent, pas pour les autres.',
  c_blanc: 'Bureau des permis. Un écran annonce un délai d\u2019attente qui ne veut rien dire.',
  c_neon: 'Une galerie de néons. Tout y est à vendre, en crédits.',
};
// Crochet du futur combat [décision : mutant à la douane = premier combat ; fuite vers le désert ; 0 PV = capture, Sous-Ville].
// Le combat n'existe pas encore : la scène « halloran » le remplace par deux choix scriptés (provisoire, documenté).
// Le jour où le combat existe : l'action « hook:douane_mutant » lancera le combat, et ses deux issues remplaceront ces choix.
export const COMBAT_HOOKS = { douane_mutant: { status: 'provisoire', fuite: 'warp:steel_route:29:34', capture: 'warp:steel_route:42:34', note: 'L2 : la capture mènera dans la Sous-Ville' } };
export const DIALOGUES = {
  odile: {
    start: { text: 'Suivant. Motif ?', options: [
      { label: 'Entrer. Je cherche du travail.', next: 'lu', if: 'implant&!steel_passe' },
      { label: 'Entrer. Je cherche du travail.', next: 'refus', if: '!implant', action: 'flag:steel_refuse' },
      { label: 'Changer des dollars (20 $ contre 11 cr)', action: 'change:20:11', next: 'change', if: 'implant' },
      { label: 'Je repasse la barrière.', next: 'passe', if: 'steel_passe' },
      { label: 'Rien. Je regardais.', next: 'end' } ] },
    lu: { text: 'Poignet. Plus près. Voilà. Implant lu, aucune dette, aucun signalement. Entrée de transit, sept jours, renouvelable au bureau des permis. Le change est ici ou chez les changeurs de la place. Ici, au moins, on ne vous vole qu\u2019officiellement.', options: [
      { label: 'Merci.', action: 'flag:steel_passe;flag:q_douane', next: 'passe' } ] },
    passe: { text: 'Barrière à votre droite. Ne courez pas dans le couloir, les caméras n\u2019aiment pas ça.', options: [ { label: 'J\u2019y vais.', next: 'end' } ] },
    refus: { text: 'Je ne lis rien. Pas d\u2019implant, pas de fiche. Pour IO, vous n\u2019êtes personne, et personne ne passe cette barrière.', options: [
      { label: 'Je peux payer.', next: 'payer' }, { label: 'Et si je reviens demain ?', next: 'demain' }, { label: 'Je m\u2019en vais.', next: 'end' } ] },
    payer: { text: 'Je n\u2019ai rien entendu, et vous n\u2019avez rien dit. Suivant.', options: [ { label: 'Je m\u2019en vais.', next: 'end' } ] },
    demain: { text: 'Demain, je lirai la même chose. Moi ou une autre.', options: [ { label: 'Je m\u2019en vais.', next: 'end' } ] },
    change: { text: 'Vingt dollars, onze crédits. Le taux est affiché derrière moi. Personne ne le lit non plus.', options: [ { label: 'Merci.', next: 'start' } ] },
    pauvre: { text: 'Il manque des dollars. Le taux, lui, ne bouge pas.', options: [ { label: 'Tant pis.', next: 'end' } ] },
  },
  halloran: {
    start: { text: 'La douane, c\u2019est le guichet, là. Moi, je regarde.', alt: [
        { if: 'race_mutant&steel_fui', text: 'Encore toi. Tu as eu de la chance une fois. Le col.' },
        { if: 'race_mutant', text: 'Hé. Toi. Les mains où je les vois. Non. Le col. Baisse le col.' },
        { if: 'steel_refuse', text: 'Refoulé ? Alors la route, c\u2019est par là. Ne traîne pas sous les tourelles.' },
        { if: 'steel_passe', text: 'Implant lu, tu es en règle. Avance.' } ], options: [
      { label: 'Courir vers le désert.', if: 'race_mutant', action: 'hook:douane_mutant;hurt:9;flag:steel_attaque;flag:steel_fui;warp:steel_route:29:34', next: 'fui' },
      { label: 'Rester. Lever les mains.', if: 'race_mutant', next: 'insiste' },
      { label: 'Je passe juste.', if: '!race_mutant', next: 'end' } ] },
    fui: { text: 'Deux tirs. Le premier soulève le sable, le second t\u2019ouvre l\u2019épaule. Tu cours jusqu\u2019à n\u2019entendre plus que ton souffle.', options: [ { label: 'Reprendre mon souffle.', next: 'end' } ] },
    insiste: { text: 'Il ne tire pas. Il parle dans son col, et deux autres arrivent avec une cagoule et des liens.', options: [
      { label: 'Ne pas résister.', action: 'hook:douane_mutant;hurt:15;flag:steel_attaque;flag:steel_capture;reveal:r_service;warp:steel_route:42:34', next: 'capture' } ] },
    capture: { text: 'Le noir. Des marches. Une odeur d\u2019huile chaude et de machines. Puis on te jette dehors, à côté d\u2019une trappe enchaînée, avec une côte qui craque. Quelqu\u2019un a dit « Sous-Ville ». Ce sera pour une autre fois.', options: [ { label: 'Me relever.', next: 'end' } ] },
  },
  teng: {
    start: { text: 'Des dollars ? J\u2019adore les dollars. Personne n\u2019en veut ici, alors je les prends tous. Dix dollars, six crédits, et je souris en prime.', options: [
      { label: 'Changer 10 $ (6 cr)', action: 'change:10:6', next: 'merci' },
      { label: 'Ce bâtiment de verre, en face ?', action: 'reveal:c_arcadius', next: 'arcadius' },
      { label: 'Où on fait ses papiers ?', action: 'reveal:c_blanc', next: 'permis' },
      { label: 'Plus tard.', next: 'end' } ] },
    merci: { text: 'Six, sept... non, six. Un plaisir. Reviens quand tu veux, je ne ferme jamais, je dors debout.', options: [ { label: 'Autre chose.', next: 'start' }, { label: 'Au revoir.', next: 'end' } ] },
    arcadius: { text: 'Arcadius Center. Tout ce qui porte un implant y a une fiche. La tienne aussi. N\u2019y entre pas sans y être appelé.', options: [ { label: 'Autre chose.', next: 'start' } ] },
    permis: { text: 'Le bureau blanc, de l\u2019autre côté de l\u2019avenue. Ils ouvrent quand l\u2019écran le décide. Prends un livre.', options: [ { label: 'Autre chose.', next: 'start' } ] },
    pauvre: { text: 'Pas de dollars, pas de sourire. C\u2019est la règle, désolé.', options: [ { label: 'Tant pis.', next: 'end' } ] },
  },
  patrouilleur: {
    start: { text: 'Circulez. L\u2019avenue est à tout le monde, mais pas pour longtemps.', options: [
      { label: 'Il y a un change, par ici ?', action: 'reveal:c_change', next: 'change' }, { label: 'Je circule.', next: 'end' } ] },
    change: { text: 'Chez Teng, les boutiques en face. Compte ta monnaie deux fois.', options: [ { label: 'Merci.', next: 'end' } ] },
  },
};
