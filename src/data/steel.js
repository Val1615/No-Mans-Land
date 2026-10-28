// v12 Steel-Megalopolis, lot L1 : la route et la douane (S0), puis Center-Town (S1). Voir docs/villes/STEEL_MEGALOPOLIS_PLAN.md.
// [décision] Valentin : entrée selon la race (augmenté / cyborg passent avec l'implant, humain refusé, mutant attaqué à vue) ;
// premier quartier = Center-Town ; la quête s'arrête une fois en ville. Le reste (PNJ, textes, plan, taux) = [proposition].
import { LOCATIONS_LOWER, DOORS_LOWER, NPCS_LOWER, DIALOGUES_LOWER } from './lower_town.js';
import { LOCATIONS_ASIA, DOORS_ASIA, NPCS_ASIA, DIALOGUES_ASIA } from './asia_ground.js';
import { BUILDINGS_ROUTE, PAINTED_DOORS_ROUTE, BUILDINGS_CENTER, PAINTED_DOORS_CENTER, BUILDINGS_SV1, PAINTED_DOORS_SV1, BUILDINGS_SV2, PAINTED_DOORS_SV2 } from './buildings_steel.js';

const named = list => list.map(b => ({ ...b, named: true }));
// v13 : nuit de Steel (concept art docs/villes/steel/ambiance/concept_center_town.jpg). light = éclairage du lieu (view.js),
// extras = figurants immobiles (file d'attente, soldats), walkers = passants, drones = drones en orbite, glows = lumières au sol.
const SOLDAT = 'gen_halloran';
const civ = i => `st_civil${i % 6}`;
const NIGHT_ROUTE = { bg: '#0c0f18', hemi: ['#8090b8', '#2a2430', 0.95], sun: ['#a8b8ff', 0.55], tint: '#c4c8d8', actor: '#c9cddc' };
const NIGHT_CITY = { bg: '#0b0a16', hemi: ['#aab4ff', '#4a2a5c', 1.35], sun: ['#c0b0ff', 0.7], tint: '#9092b8', actor: '#d4d4ea' };
// v14 : Sous-Ville (concept docs/villes/steel/ambiance/concept_sous_ville.jpg) : lumière orange des braseros, fumée, tôle rouillée.
const UNDER = { bg: '#0e0805', hemi: ['#ffb27a', '#2a1408', 1.05], sun: ['#ff9c55', 0.62], tint: '#dcae86', actor: '#e6c4a2' };
const FIRE = '#ff8a2a';
const NEON_V = '#c247ff', NEON_C = '#2fd8ff', WARM = '#ffae55', FLOOD = '#d8ecff';
export const LOCATIONS = {
  // S0 : place forte d'IO devant le sarcophage [décision v13] : porte en haut à droite au bout de la route, poste de douane à gauche,
  // file d'attente, soldats, miradors, tourelles, barbelés, projecteurs, check-point sur la route.
  steel_route: { id: 'steel_route', name: 'Steel-Megalopolis · La douane', kind: 'exterior', size: { w: 48, d: 36 }, light: NIGHT_ROUTE,
    ground: { base: '#5d5446', skin: 'g_sand', tint: 'rgba(8,12,30,.45)', zones: [
      { x: 31, z: 8, w: 6, d: 28, kind: 'asphalt' }, { x: 17, z: 8, w: 30, d: 4, kind: 'plate', tint: 'rgba(0,0,0,.25)' }, { x: 2, z: 28, w: 35, d: 5, kind: 'plate', tint: 'rgba(0,0,0,.2)' } ] },
    buildings: named(BUILDINGS_ROUTE).map(b => b.id === 'r_service' ? { ...b, visitable: true } : { ...b, tint: '#ffffff' }), props: [
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
  // v14 [proposition] Sous-Ville, quartier des Poutres : arrivée par la trappe (échelle à l'ouest), guetteuse, cabanes, tripot.
  sv_poutres: { id: 'sv_poutres', name: 'Sous-Ville · Les Poutres', kind: 'exterior', size: { w: 36, d: 28 }, light: UNDER,
    ground: { base: '#3a2c20', skin: 'g_sv', tileM: 5, clean: true, zones: [ { x: 0, z: 11, w: 36, d: 7, kind: 'plate', tint: 'rgba(20,10,0,.35)' } ] },
    buildings: named(BUILDINGS_SV1), props: [
      { sprite: 'sv_tuyau', x: 6, z: 9.6, fp: [4.2, 1.2] }, { sprite: 'sv_tuyau', x: 31, z: 9.4, fp: [4.2, 1.2] }, { sprite: 'sv_tuyau', x: 12, z: 19.4, fp: [4.2, 1.2], flip: true },
      { sprite: 'sv_ecrans', x: 33.4, z: 2.4, fp: [2.6, 1.2], glow: 0.35 }, { sprite: 'sv_linge', x: 10.4, z: 8.2, fp: [3.0, 0.3] }, { sprite: 'sv_linge', x: 28.6, z: 19.6, fp: [3.0, 0.3], flip: true },
      { sprite: 'sv_brasero', x: 8.2, z: 15.6, fp: [0.8, 0.8] }, { sprite: 'sv_brasero', x: 20.6, z: 11.4, fp: [0.8, 0.8] }, { sprite: 'sv_brasero', x: 27.4, z: 16.8, fp: [0.8, 0.8] },
      { sprite: 'sv_panneau', x: 14.8, z: 10.6, solid: 0.3 }, { sprite: 'sv_armes', x: 30.8, z: 12.2, fp: [1.4, 1.0] }, { sprite: 'sv_pneus', x: 2.2, z: 18.4, fp: [2.0, 1.6] },
      { sprite: 'sv_implants', x: 11.2, z: 17.6, fp: [1.8, 0.9] } ],
    glows: [ { x: 8.6, z: 16, rx: 3.4, rz: 3.4, color: FIRE, i: 0.85, flicker: true }, { x: 21, z: 11.8, rx: 3.4, rz: 3.4, color: FIRE, i: 0.85, flicker: true },
      { x: 27.8, z: 17.2, rx: 3.4, rz: 3.4, color: FIRE, i: 0.8, flicker: true }, { x: 22.7, z: 10.4, rx: 2, rz: 1.4, color: WARM, i: 0.7 }, { x: 34.6, z: 4.4, rx: 2.4, rz: 1.6, color: '#c8d4ff', i: 0.35, flicker: true },
      { x: 18, z: 14, rx: 14, rz: 6, color: WARM, i: 0.3 } ],
    extras: [ { sprite: 'gen_sv_gang', x: 29.6, z: 13.0, face: -1, role: 'gang' }, { sprite: 'gen_sv_gang', x: 25.0, z: 10.6, face: 1, role: 'gang' }, { sprite: 'gen_sv_guetteuse', x: 33.8, z: 18.2, face: -1, role: 'guetteur' } ],
    walkers: [ { sprite: 'gen_sv_gang', path: [[4, 13], [34, 13], [34, 15.5], [4, 15.5]], speed: 0.7, role: 'gang' }, { sprite: 'gen_sv_dealer', path: [[16, 16], [24, 16]], speed: 0.5, t0: 8, role: 'dealer' } ],
    spawn: { player: { x: 2, z: 13 }, companion: { x: 2, z: 14 } }, city: null,
    arrive: { from: 'steel_route', text: 'En bas, ça sent la tôle chaude et la friture. Personne ne lève les yeux.' } },
  tripot_in: { id: 'tripot_in', name: 'Sous-Ville · Le Tripot', kind: 'interior', size: { w: 8, d: 6 },
    light: { bg: '#0a0604', hemi: ['#ffb070', '#2a1208', 1.15], sun: ['#ff9a50', 0.95] },
    ground: { base: '#3a3028', skin: 'f_sv_plates', tileM: 2 }, wall: '#3a2a20', wallSkin: 'w_sv_tin', buildings: [], props: [
      { furn: 'sv_bar', x: 0.3, z: 0.3 }, { furn: 'sv_shelf', x: 5.8, z: 0.2 }, { furn: 'sv_cardtable_b', x: 5.0, z: 2.6 } ],
    glows: [{ x: 5.6, z: 3.2, rx: 1.4, rz: 1.4, color: WARM, i: 0.6 }], city: null },
  // v14 [proposition] la Cuve : atelier d'Elio, monte-charge vers Center-Town (au nord-est).
  sv_cuve: { id: 'sv_cuve', name: 'Sous-Ville · La Cuve', kind: 'exterior', size: { w: 36, d: 28 }, light: UNDER,
    ground: { base: '#3a2c20', skin: 'g_sv', tileM: 5, clean: true, zones: [ { x: 0, z: 11, w: 36, d: 7, kind: 'plate', tint: 'rgba(20,10,0,.35)' } ] },
    buildings: named(BUILDINGS_SV2).map(b => b.id === 'v_lift' ? { ...b, visitable: true } : b), props: [
      { sprite: 'sv_tuyau', x: 22, z: 9.4, fp: [4.2, 1.2] }, { sprite: 'sv_tuyau', x: 26, z: 19.8, fp: [4.2, 1.2], flip: true }, { sprite: 'sv_ecrans', x: 3.0, z: 9.0, fp: [2.6, 1.2], glow: 0.35 },
      { sprite: 'sv_linge', x: 24.6, z: 5.4, fp: [3.0, 0.3] }, { sprite: 'sv_brasero', x: 18.4, z: 14.8, fp: [0.8, 0.8] }, { sprite: 'sv_brasero', x: 6.6, z: 17.0, fp: [0.8, 0.8] },
      { sprite: 'sv_panneau', x: 34.4, z: 9.4, solid: 0.3 }, { sprite: 'sv_pneus', x: 12.4, z: 19.6, fp: [2.0, 1.6] }, { sprite: 'sv_armes', x: 24.4, z: 16.2, fp: [1.4, 1.0] } ],
    glows: [ { x: 18.8, z: 15.2, rx: 3.4, rz: 3.4, color: FIRE, i: 0.85, flicker: true }, { x: 7, z: 17.4, rx: 3.4, rz: 3.4, color: FIRE, i: 0.8, flicker: true },
      { x: 14.6, z: 9.2, rx: 2.2, rz: 1.4, color: WARM, i: 0.7 }, { x: 32, z: 8.4, rx: 2.2, rz: 1.6, color: WARM, i: 0.6, flicker: true }, { x: 18, z: 14, rx: 14, rz: 6, color: WARM, i: 0.3 } ],
    extras: [ { sprite: 'gen_sv_gang', x: 31.0, z: 9.8, face: -1, role: 'gang' }, { sprite: 'gen_sv_dealer', x: 20.4, z: 16.6, face: 1, role: 'dealer' } ],
    walkers: [ { sprite: 'gen_sv_guetteuse', path: [[2, 15], [30, 15]], speed: 0.6, role: 'guetteur' } ],
    spawn: { player: { x: 1, z: 14 }, companion: { x: 1, z: 15 } }, city: null },
  elio_in: { id: 'elio_in', name: 'Sous-Ville · Atelier d\u2019Elio', kind: 'interior', size: { w: 7, d: 5 },
    light: { bg: '#0a0604', hemi: ['#ffc080', '#2a1408', 1.2], sun: ['#ffa860', 1.0] },
    ground: { base: '#3a3430', skin: 'f_sv_concrete', tileM: 2 }, wall: '#3a2a20', wallSkin: 'w_sv_planks', buildings: [], props: [
      { furn: 'sv_workbench', x: 0.3, z: 0.3 }, { furn: 'sv_shelf', x: 4.9, z: 0.2 } ], city: null },
  ...LOCATIONS_ASIA, // Asia-Ground lot 2 (asia_ground.js)
  ...LOCATIONS_LOWER, // Lower-Town v1 (lower_town.js)
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
    interrupt: { npc: 'odile', tree: 'odile_volonte', if: s => !!(s.flags.race_augmente || s.flags.race_cyborg) && !s.flags.odile_tenu && !s.flags.odile_signe && !s.flags.odile_payee },
    conditions: [{ test: s => !!s.flags.steel_passe, reason: 'douane', text: 'La barrière reste baissée. Il faut d\u2019abord passer au guichet.' }] },
  J('c_ouest', 'steel_center', 0, 18, 1, 18, 'douane_in_est', 'Vers la douane'),
  ...painted(PAINTED_DOORS_CENTER, 'steel_center', { c_change_door: 'change_in_door' }),
  { id: 'change_in_door', location: 'change_in', opening: { x: 3, z: 5, side: 'south' }, threshold: { x: 3, z: 4 }, target: { doorId: 'c_change_door' }, conditions: [] },
  // Lower-Town v1 : La Descente. c_est vérifié libre (aucun bâtiment ni prop sur x 47-48, z 18 ; test lower_town.py).
  J('c_est', 'steel_center', 48, 18, 47, 18, 'l_ouest', 'La Descente (Lower-Town)'),
  ...DOORS_LOWER,
  ...DOORS_ASIA,
  // v14 : la trappe de service ouvre sur la Sous-Ville pour qui connaît Elio (ou qu'on y a jeté)
  { id: 'r_trappe', buildingId: 'r_service', location: 'steel_route', opening: { x: 42.2, z: 32.5, side: 'south' }, threshold: { x: 42.2, z: 33.5 }, target: { doorId: 'v_trappe' },
    conditions: [{ test: s => !!(s.flags.bruno_frere || s.flags.sv_jete), reason: 'trappe', text: s => CLOSED_TEXT.r_service(s) }] },
  J('v_trappe', 'sv_poutres', 0, 13, 1, 13, 'r_trappe', 'Échelle vers la surface'),
  J('v_est', 'sv_poutres', 36, 14, 35, 14, 'v_ouest', 'Vers la Cuve', [{ test: s => !!s.flags.sv_mot, reason: 'guet', text: 'Deux types se lèvent quand tu approches du passage. Ils ne disent rien. Ils attendent que tu repartes.' }]),
  J('v_ouest', 'sv_cuve', 0, 14, 1, 14, 'v_est', 'Vers les Poutres'),
  ...painted(PAINTED_DOORS_SV1, 'sv_poutres', { v_tripot_door: 'tripot_in_door' }),
  { id: 'tripot_in_door', location: 'tripot_in', opening: { x: 4, z: 6, side: 'south' }, threshold: { x: 4, z: 5 }, target: { doorId: 'v_tripot_door' }, conditions: [] },
  ...painted(PAINTED_DOORS_SV2, 'sv_cuve', { v_atelier_door: 'elio_in_door' }),
  { id: 'elio_in_door', location: 'elio_in', opening: { x: 3.5, z: 5, side: 'south' }, threshold: { x: 3.5, z: 4 }, target: { doorId: 'v_atelier_door' }, conditions: [] },
  { id: 'v_lift_door', buildingId: 'v_lift', location: 'sv_cuve', opening: { x: 32, z: 7.5, side: 'south' }, threshold: { x: 32, z: 8.5 }, target: { doorId: 'c_sud' },
    conditions: [{ test: s => !!s.flags.sv_passage, reason: 'lift', text: 'Le monte-charge. Un boîtier à clé, et un type assis dessus qui ne bougera pas pour toi.' }] },
  J('c_sud', 'steel_center', 19.5, 36, 19.5, 35, 'v_lift_door', 'Vers la Sous-Ville', [{ test: s => !!s.flags.sv_passage, reason: 'grille', text: 'Une grille entre deux galeries. Fermée de l’intérieur.' }]),
  E('r_ouest', 'steel_route', 0, 30, 1, 30, 'Désert', 'Du sable, et le mur du dôme qui ne finit pas.'),
];
export const NPCS = [
  { id: 'odile', name: 'Odile Varga', sprite: 'gen_odile', location: 'douane_in', x: 2.1, z: 2.0, faceTo: [6, 2.4], dialogue: 'odile' },
  { id: 'halloran', name: 'Sergent Halloran', sprite: 'gen_halloran', location: 'steel_route', x: 36.2, z: 23.0, faceTo: [34, 34], dialogue: 'halloran' },
  { id: 'teng', name: 'Teng', sprite: 'gen_teng', location: 'change_in', x: 2.9, z: 1.6, faceTo: [3, 5], dialogue: 'teng' },
  { id: 'guetteuse', name: 'Nane', sprite: 'gen_sv_guetteuse', location: 'sv_poutres', x: 33.2, z: 15.2, faceTo: [28, 14], dialogue: 'guetteuse' },
  { id: 'receleur', name: 'Le receleur', sprite: 'gen_sv_receleur', location: 'sv_poutres', x: 31.6, z: 11.6, faceTo: [28, 14], dialogue: 'receleur' },
  { id: 'dealer', name: 'Pic', sprite: 'gen_sv_dealer', location: 'tripot_in', x: 3.2, z: 2.2, faceTo: [4, 6], dialogue: 'dealer' },
  { id: 'elio', name: 'Elio', sprite: 'gen_elio', location: 'elio_in', x: 2.6, z: 1.9, faceTo: [3.5, 5], dialogue: 'elio' },
  { id: 'patrouilleur', name: 'Patrouilleur', sprite: 'gen_halloran', location: 'steel_center', x: 30.5, z: 19.8, faceTo: [22, 18], dialogue: 'patrouilleur' },
  ...NPCS_LOWER,
  ...NPCS_ASIA,
];
export const CLOSED_TEXT = {
  r_porte: 'La route entre dans le noir entre deux battants grands comme des immeubles. Sans passer la douane, les tourelles s\u2019en chargent.',
  r_service: s => s.flags.sol_passage ? 'La trappe dont parlait Sol. Chaîne neuve, cadenas neuf. Celui qui passe par là ne passe pas par le dessus.' : 'Une trappe de service à moitié ensablée, chaîne et cadenas. Des traces de pas fraîches, qui n\u2019en reviennent pas.',
  c_tour: 'La Rotonde. Des écrans sur toute la façade, et pas une porte qui s\u2019ouvre pour toi.',
  c_arcadius: 'Arcadius Center. Les portes s\u2019ouvrent pour les implants qu\u2019elles reconnaissent, pas pour les autres.',
  c_blanc: 'Bureau des permis. Un écran annonce un délai d\u2019attente qui ne veut rien dire.',
  c_neon: 'Une galerie de néons. Tout y est à vendre, en crédits.',
  v_cab_a: 'Une cabane de tôle. Quelqu’un tousse derrière le rideau.', v_cab_b: 'Rideau tiré. Une radio grésille un match qui date.', v_cab_c: 'Des chiens grognent derrière la porte.',
  v_cab_d: 'Cadenas. Sur la tôle, une croix à la craie.', v_cab_e: 'Une odeur de soudure. On ne t’ouvre pas.', v_cab_f: 'Un gamin te regarde par une fente, puis plus rien.',
  v_cab_g: 'Rideau tiré.', v_cab_h: 'On dort, là-dedans. Ou on fait semblant.', v_cab_i: 'Une cabane vide. Vide depuis peu.', v_cab_j: 'Quelqu’un compte des billets à voix basse.',
};
// Crochet du futur combat [décision : mutant à la douane = premier combat ; fuite vers le désert ; 0 PV = capture, Sous-Ville].
// Le combat n'existe pas encore : la scène « halloran » le remplace par deux choix scriptés (provisoire, documenté).
// Le jour où le combat existe : l'action « hook:douane_mutant » lancera le combat, et ses deux issues remplaceront ces choix.
export const COMBAT_HOOKS = { douane_mutant: { status: 'provisoire', fuite: 'warp:steel_route:29:34', capture: 'warp:sv_poutres:3:13', note: 'v14 : capture = jeté dans la Sous-Ville (Les Poutres)' } };
export const DIALOGUES = {
  ...DIALOGUES_LOWER,
  ...DIALOGUES_ASIA,
  odile: {
    start: { text: 'Suivant. Motif ?', options: [
      { label: 'Je repasse. Il paraît que mon implant a sonné.', next: 'odile_volonte/start', if: 'steel_passe&!race_humain&!race_mutant&!odile_tenu&!odile_signe&!odile_payee' },
      { label: 'Entrer. Je cherche du travail.', next: 'lu', if: 'implant&!steel_passe' },
      { label: 'Entrer. Je cherche du travail.', next: 'refus', if: '!implant', action: 'flag:steel_refuse' },
      { label: 'Changer des dollars (20 $ contre 11 cr)', action: 'change:20:11', next: 'change', if: 'implant' },
      { label: 'Changer moins (10 $ contre 5 cr)', action: 'change:10:5', next: 'change', if: 'implant' },
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
      { label: 'La guichetière a l\u2019air de bien vous connaître.', if: '!race_mutant&!info_cousin_odile', next: 'halloran_cousin/start' },
      { label: 'Je passe juste.', if: '!race_mutant', next: 'end' } ] },
    fui: { text: 'Deux tirs. Le premier soulève le sable, le second t\u2019ouvre l\u2019épaule. Tu cours jusqu\u2019à n\u2019entendre plus que ton souffle.', options: [ { label: 'Reprendre mon souffle.', next: 'end' } ] },
    insiste: { text: 'Il ne tire pas. Il parle dans son col, et deux autres arrivent avec une cagoule et des liens.', options: [
      { label: 'Ne pas résister.', action: 'hook:douane_mutant;hurt:15;flag:steel_attaque;flag:steel_capture;flag:sv_jete;reveal:r_service;warp:sv_poutres:3:13', next: 'capture' } ] },
    capture: { text: 'Le noir. Des marches, longtemps. On t\u2019enlève la cagoule au bord d\u2019un trou et on te pousse. Tu tombes sur de la tôle, une côte craque. Là-haut, quelqu\u2019un rigole : « Bienvenue en bas. »', options: [ { label: 'Me relever.', next: 'end' } ] },
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
  // v14 [proposition] Sous-Ville. Monnaie : le dollar, comme dans les No Man's Land (city: null).
  guetteuse: {
    start: { text: 'T\u2019es perdu, ou tu cherches quelqu\u2019un ?', alt: [
        { if: 'sv_mot', text: 'Tu connais le chemin. La Cuve, après le passage.' },
        { if: 'sv_jete', text: 'Les soldats t\u2019ont balancé par le trou, hein. Ils font ça quand ils ont la flemme de remplir des papiers.' } ], options: [
      { label: 'Tu me regardes depuis tout à l\u2019heure.', next: 'guetteuse_volonte/start', if: 'sv_passage&!nane_tenu&!nane_paie&!nane_cede' },
      { label: 'Quatorze poutres.', if: 'bruno_frere&!sv_mot', action: 'flag:sv_mot;reveal:v_tripot', next: 'mot' },
      { label: 'Et maintenant, je vais où ?', if: 'sv_jete&!sv_mot', action: 'flag:sv_mot;reveal:v_tripot', next: 'jete' },
      { label: 'Je cherche Elio.', if: '!sv_mot', next: 'qui' },
      { label: 'Rien. Je passe.', next: 'end' } ] },
    mot: { text: 'Bruno t\u2019envoie. Ça fait longtemps qu\u2019il n\u2019a envoyé personne. Elio bosse à la Cuve, l\u2019atelier sous les tuyaux. Passe, les garçons te laisseront tranquille.', options: [ { label: 'Merci.', next: 'end' } ] },
    jete: { text: 'Va voir Elio, au fond, à la Cuve. Il fait remonter les gens, pas gratuitement. Et évite le tripot si tu tiens à ce qui te reste.', options: [ { label: 'Merci.', next: 'end' } ] },
    qui: { text: 'Plein de gens cherchent plein de gens. Tu as un mot, ou juste un prénom ?', options: [ { label: 'Juste un prénom.', next: 'end' } ] },
  },
  receleur: {
    start: { text: 'Montres, implants, papiers de transit. Tout est d\u2019occasion, surtout les papiers.', options: [
      { label: 'Des papiers de transit ?', next: 'papiers' }, { label: 'Pas aujourd\u2019hui.', next: 'end' } ] },
    papiers: { text: 'Trois cents dollars, et ils passent une fois sur deux. L\u2019autre fois, tu n\u2019as jamais acheté chez moi.', options: [ { label: 'Je repasserai.', next: 'end' } ] },
  },
  dealer: {
    start: { text: 'Une puce de mémoire, un œil qui voit la nuit, un truc pour dormir. Ici on ne demande pas d\u2019où ça sort.', options: [
      { label: 'Tu voulais me voir ?', next: 'dealer_volonte/start', if: '!pic_tenu&!pic_paie&!pic_cede' },
      { label: 'Ça sort d\u2019où ?', next: 'ou' }, { label: 'Non merci.', next: 'end' } ] },
    ou: { text: 'De gens qui n\u2019en avaient plus besoin. Tu veux une table, ou tu veux partir ?', options: [ { label: 'Partir.', next: 'end' } ] },
  },
  elio: {
    start: { text: 'Ferme derrière toi. Qui t\u2019envoie ?', alt: [
        { if: 'sv_passage', text: 'Le monte-charge est au fond à droite. Dis à Bruno que je mange.' },
        { if: 'bruno_frere', text: 'Quatorze poutres, hein. Mon frère vend encore de l\u2019eau tiède à La Pompe ?' } ], options: [
      { label: 'Il faut que je monte à Center-Town.', if: '!sv_passage', next: 'monter' },
      { label: 'Merci, Elio.', if: 'sv_passage', next: 'end' },
      { label: 'Plus tard.', if: '!sv_passage', next: 'end' } ] },
    monter: { text: 'Tout le monde veut monter. Le monte-charge sert aux livraisons du marché, la nuit. Tu montes dans une caisse, tu ne bouges pas, tu ne parles pas. Vingt dollars.', options: [
      { label: 'Payer 20 $.', action: 'pay:20;flag:sv_passage;reveal:v_lift', next: 'ok' },
      { label: 'Je n\u2019ai pas vingt dollars.', next: 'risque' } ] },
    risque: { text: 'Alors tu portes. Une caisse pour la Cuve d\u2019en face, chez des gens qui n\u2019aiment pas qu\u2019on les regarde. S\u2019ils sont de mauvaise humeur, tu le sauras.', options: [
      { label: 'Porter la caisse.', action: 'hurt:6;flag:sv_passage;reveal:v_lift', next: 'porte' }, { label: 'Je reviendrai avec l\u2019argent.', next: 'end' } ] },
    ok: { text: 'Le monte-charge est au fond à droite. Le gars dessus sait. En haut, tu sors entre deux galeries, et tu ne m\u2019as jamais vu.', options: [ { label: 'Merci.', next: 'end' } ] },
    porte: { text: 'Ils étaient de mauvaise humeur. Tu reviens avec une lèvre ouverte et la caisse livrée. Elio hoche la tête : le monte-charge, au fond à droite.', options: [ { label: 'J\u2019y vais.', next: 'end' } ] },
    pauvre: { text: 'Il te manque des billets, et je ne fais pas crédit. Par contre, j\u2019ai une caisse à porter à la Cuve. Tu la livres, tu montes. Les gens là-bas sont nerveux, je te préviens.', options: [
      { label: 'D\u2019accord, je porte la caisse.', action: 'hurt:6;flag:sv_passage;reveal:v_lift', next: 'porte' }, { label: 'Je reviendrai avec l\u2019argent.', next: 'end' } ] },
  },
  patrouilleur: {
    start: { text: 'Circulez. L\u2019avenue est à tout le monde, mais pas pour longtemps.', options: [
      { label: 'Il y a un change, par ici ?', action: 'reveal:c_change', next: 'change' }, { label: 'Je circule.', next: 'end' } ] },
    change: { text: 'Chez Teng, les boutiques en face. Compte ta monnaie deux fois.', options: [ { label: 'Merci.', next: 'end' } ] },
  },
};
