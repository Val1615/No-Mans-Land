// v12 Steel-Megalopolis, lot L1 : la route et la douane (S0), puis Center-Town (S1). Voir docs/villes/STEEL_MEGALOPOLIS_PLAN.md.
// [décision] Valentin : entrée selon la race (augmenté / cyborg passent avec l'implant, humain refusé, mutant attaqué à vue) ;
// premier quartier = Center-Town ; la quête s'arrête une fois en ville. Le reste (PNJ, textes, plan, taux) = [proposition].
import { LOCATIONS_LOWER, DOORS_LOWER, NPCS_LOWER, DIALOGUES_LOWER } from './lower_town.js';
import { LOCATIONS_ASIA, DOORS_ASIA, NPCS_ASIA, DIALOGUES_ASIA } from './asia_ground.js';
import { LOCATIONS_MEGA, DOORS_MEGA, NPCS_MEGA, DIALOGUES_MEGA, CLOSED_MEGA } from './mega_line.js';
import { LOCATIONS_DOME, DOORS_DOME, NPCS_DOME, DIALOGUES_DOME, CLOSED_DOME } from './dome_frequence.js';
import { LOCATIONS_ARENA, DOORS_ARENA, NPCS_ARENA, DIALOGUES_ARENA, CLOSED_ARENA } from './steel_arena.js';
import { LOCATIONS_STRIP, DOORS_STRIP, NPCS_STRIP, DIALOGUES_STRIP, CLOSED_STRIP } from './frequence_strip.js';
import { LOCATIONS_PULSE, DOORS_PULSE, NPCS_PULSE, DIALOGUES_PULSE, CLOSED_PULSE } from './pulse_plaza.js';
import { LOCATIONS_CHINA, DOORS_CHINA, NPCS_CHINA, DIALOGUES_CHINA } from './china_lake.js';
import { CT_FOULE } from './center_foule.js';
import { BUILDINGS_ROUTE, PAINTED_DOORS_ROUTE, BUILDINGS_CENTER, PAINTED_DOORS_CENTER, BUILDINGS_SV1, PAINTED_DOORS_SV1, BUILDINGS_SV2, PAINTED_DOORS_SV2 } from './buildings_steel.js';

const named = list => list.map(b => ({ ...b, named: true }));
// v13 : nuit de Steel (concept art docs/villes/steel/ambiance/concept_center_town.jpg). light = éclairage du lieu (view.js),
// extras = figurants immobiles (file d'attente, soldats), walkers = passants, drones = drones en orbite, glows = lumières au sol.
const SOLDAT = 'gen_halloran';
const civ = i => `st_civil${i % 6}`;
const NIGHT_ROUTE = { bg: '#0c0f18', hemi: ['#8090b8', '#2a2430', 0.95], sun: ['#a8b8ff', 0.55], tint: '#c4c8d8', actor: '#c9cddc' };
const NIGHT_CITY = { bg: '#05070d', hemi: ['#9ab0d4', '#141824', 1.08], sun: ['#dce4f5', 0.55], tint: '#d8dce8', actor: '#e2dee8' };
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
  // S1 : Center-Town · Carrefour Arcadius (docs/villes/steel/quartiers/center_town/CENTER_TOWN.md) : vraie nuit noire (#05070d),
  // dalles anthracite humides, rails tram, case jaune, QG Arcadius IO, silhouette extérieure du Dôme Fréquence (zone steel_dome à part),
  // Bureau des permis, 5 tours à pubs distinctes, viaduc Mega-Line, hologramme suspendu NEXUS, mobilier ct_*_3q.
  // Center-Town v2 (plan cible d'Ocre validé le 11/11/2026, docs : /workspace/nml-shots/center_town_plan_cible.md) : 132 x 116 m.
  // Av. N-S : trottoir x56-64 | voies x64-72 | tram x72-76 | voies x76-84 | trottoir x84-92. Av. E-O : trottoir z48-56 | voies z56-64 | tram z64-68 | voies z68-76 | trottoir z76-84.
  steel_center: { id: 'steel_center', name: 'Steel-Megalopolis · Center-Town', kind: 'exterior', size: { w: 132, d: 116 }, light: NIGHT_CITY,
    ground: { base: '#12151d', skin: 'g_ct_trottoir_dalles', tileM: 4, clean: true,
      marge: { skin: 'g_ct_asphalte_mouille', tileM: 4, m: 48, voile: 'rgba(4,6,12,.64)' },
      zones: [],
      // sol du carrefour v4 d'Ocre (128 px/m, CENTER_TOWN.md §8D) : bordures + angles R 2 m sur la dernière rangée de trottoir, tirets de voie,
      // lignes d'arrêt avant chaque passage piéton (circulation à droite), case jaune 12 m d'un seul tenant
      paint: [
        { x: 64, z: 0, w: 8, d: 116, skin: 'g_ct_asphalte_mouille' }, { x: 76, z: 0, w: 8, d: 116, skin: 'g_ct_asphalte_mouille' },
        { x: 0, z: 56, w: 132, d: 8, skin: 'g_ct_asphalte_mouille' }, { x: 0, z: 68, w: 132, d: 8, skin: 'g_ct_asphalte_mouille' },
        { x: 72, z: 0, w: 4, d: 116, skin: 'g_ct_rails_tram_ns' },
        { x: 0, z: 64, w: 64, d: 4, skin: 'g_ct_rails_tram_ew' }, { x: 84, z: 64, w: 48, d: 4, skin: 'g_ct_rails_tram_ew' },
        { x: 64, z: 52, w: 20, d: 4, skin: 'g_ct_passage_pieton_ew' }, { x: 64, z: 76, w: 20, d: 4, skin: 'g_ct_passage_pieton_ew' },
        { x: 60, z: 56, w: 4, d: 20, skin: 'g_ct_passage_pieton_ns' }, { x: 84, z: 56, w: 4, d: 20, skin: 'g_ct_passage_pieton_ns' },
        // bordures : trottoirs de l'av. N-S (x60-64 / x84-88) et de l'av. E-O (z52-56 / z76-80), angles aux 4 coins du carrefour
        { x: 60, z: 0, w: 4, d: 52, skin: 'g_ct_bordure_e' }, { x: 60, z: 80, w: 4, d: 36, skin: 'g_ct_bordure_e' },
        { x: 84, z: 0, w: 4, d: 52, skin: 'g_ct_bordure_o' }, { x: 84, z: 80, w: 4, d: 36, skin: 'g_ct_bordure_o' },
        { x: 0, z: 52, w: 60, d: 4, skin: 'g_ct_bordure_s' }, { x: 88, z: 52, w: 44, d: 4, skin: 'g_ct_bordure_s' },
        { x: 0, z: 76, w: 60, d: 4, skin: 'g_ct_bordure_n' }, { x: 88, z: 76, w: 44, d: 4, skin: 'g_ct_bordure_n' },
        { x: 60, z: 52, w: 4, d: 4, skin: 'g_ct_bordure_angle_se' }, { x: 84, z: 52, w: 4, d: 4, skin: 'g_ct_bordure_angle_so' },
        { x: 60, z: 76, w: 4, d: 4, skin: 'g_ct_bordure_angle_ne' }, { x: 84, z: 76, w: 4, d: 4, skin: 'g_ct_bordure_angle_no' },
        // tirets de séparation des voies (x68, x80 ; z60, z72), hors carrefour et passages
        { x: 66, z: 0, w: 4, d: 52, skin: 'g_ct_voie_tirets_ns' }, { x: 78, z: 0, w: 4, d: 52, skin: 'g_ct_voie_tirets_ns' },
        { x: 66, z: 80, w: 4, d: 36, skin: 'g_ct_voie_tirets_ns' }, { x: 78, z: 80, w: 4, d: 36, skin: 'g_ct_voie_tirets_ns' },
        { x: 0, z: 58, w: 60, d: 4, skin: 'g_ct_voie_tirets_ew', tileM: 12 }, { x: 0, z: 70, w: 60, d: 4, skin: 'g_ct_voie_tirets_ew', tileM: 12 },
        { x: 88, z: 58, w: 44, d: 4, skin: 'g_ct_voie_tirets_ew', tileM: 12 }, { x: 88, z: 70, w: 44, d: 4, skin: 'g_ct_voie_tirets_ew', tileM: 12 },
        // lignes d'arrêt : sens sud x64-72 avant le passage nord, sens nord x76-84 avant le passage sud, sens est z68-76 avant le passage ouest, sens ouest z56-64 avant le passage est
        { x: 64, z: 48, w: 8, d: 4, skin: 'g_ct_ligne_arret_ns' }, { x: 76, z: 80, w: 8, d: 4, skin: 'g_ct_ligne_arret_ns' },
        { x: 56, z: 68, w: 4, d: 8, skin: 'g_ct_ligne_arret_ew' }, { x: 88, z: 56, w: 4, d: 8, skin: 'g_ct_ligne_arret_ew' },
        { x: 68, z: 60, w: 12, d: 12, skin: 'g_ct_case_jaune_12m', tileM: 12 },
        // jardin du Dôme §8N (pelouse, puis allées par-dessus, trottoir nord en dernier)
        { x: 0, z: 92, w: 44, d: 24, skin: 'g_ct_jardin_pelouse' },
        { x: 0, z: 104, w: 32, d: 4, skin: 'g_ct_jardin_allee' },
        { x: 12, z: 92, w: 4, d: 24, skin: 'g_ct_jardin_allee' },
        { x: 28, z: 96, w: 16, d: 4, skin: 'g_ct_jardin_allee' },
        { x: 32, z: 100, w: 12, d: 8, skin: 'g_ct_jardin_allee' },
        { x: 16, z: 100, w: 8, d: 8, skin: 'g_ct_jardin_allee' },
        { x: 0, z: 92, w: 44, d: 2, skin: 'g_ct_trottoir_dalles' },
        // cour des bureaux NE §8P (dalles, pelouse de cour, asphalte de la ruelle de service)
        { x: 100, z: 12, w: 32, d: 22, skin: 'g_ct_trottoir_dalles' },
        { x: 111, z: 21, w: 12, d: 10, skin: 'g_ct_jardin_pelouse' },
        { x: 115, z: 0, w: 5, d: 12, skin: 'g_ct_asphalte_mouille' },
      ] },
    buildings: BUILDINGS_CENTER, props: [],
    // taxis qui roulent sur les deux avenues (circulation à droite, voies de 4 m : E-O vers l'ouest z58, vers l'est z70/z74 ; N-S vers le sud x66/x70, vers le nord x82) ;
    // sur l'axe N-S, vue miroir du sprite x (data/vehicules.js) ; deux tournent à droite au carrefour. Entrée et sortie dans la marge sombre, hors carte.
    carrefourVehicules: { x: 64, z: 56, w: 20, d: 20 }, // boîte du carrefour : un seul véhicule à la fois (view.js, rouler)
    // taxis v2 : trajectoires reculées des véhicules garés d'Ocre (ouest z61, est z70, sud x70, nord x78)
    vehicules: [
      { sprite: 'ct_veh_taxi_avant_v4_3q', path: [[-8, 70], [70, 70], [70, 124]], speed: 7, t0: 40 },   // vers l'est puis à droite vers le sud
      { sprite: 'ct_veh_taxi_avant_v4_3q', path: [[140, 61], [-8, 61]], speed: 7.5, t0: 30 },           // vers l'ouest, tout droit
      { sprite: 'ct_veh_taxi_avant_v4_3q', path: [[78, 124], [78, 70], [140, 70]], speed: 6.5, t0: 20 }, // vers le nord puis à droite vers l'est
      { sprite: 'ct_veh_taxi_avant_v4_3q', path: [[70, -8], [70, 124]], speed: 7, t0: 50 },             // vers le sud, tout droit
      { sprite: 'ct_veh_taxi_avant_v4_3q', path: [[-8, 70], [140, 70]], speed: 8, t0: 20 },             // vers l'est, tout droit
    ],
    enseignes: [
      { id: 'ct_n_arcadius', building: 'c_arcadius', effet: 'fixe', intensite: 0.92 },
      { id: 'ct_n_dome', building: 'c_tour', effet: 'fixe', intensite: 0.92 },
      { id: 'ct_n_teng', building: 'c_change', effet: 'fixe', intensite: 0.90 },
      { id: 'ct_n_archeon', building: 'ct_archeon', effet: 'fixe', intensite: 0.92 },
      { id: 'ct_n_orc', building: 'ct_orc', effet: 'fixe', intensite: 0.92 },
      { id: 'ct_n_humancorp', building: 'ct_humancorp', effet: 'fixe', intensite: 0.92 },
      { id: 'ct_n_nexus', building: 'ct_nexus', effet: 'fixe', intensite: 0.92 },
      { id: 'ct_n_holo', building: 'ct_holo0', effet: 'fixe', intensite: 0.95 },
      { id: 'ct_n_arret', building: 'ct_arret0', effet: 'fixe', intensite: 0.88 },
      { id: 'ct_n_echoppe', building: 'ct_echoppe0', effet: 'gresille', intensite: 0.85, decale: 0.4 },
    ],
    // tours v4 : calques <clé>_pulse d'Ocre (§8H) sur le kick de l'OST ; enseignes _neon fixes
    pulses: [
      { building: 'c_change', calque: 'pulse', mode: 'kick', veille: 0.04, intensite: 1.0, gain: 2.2, punch: 0.030, decale: 0, priorite: 8 },
      { building: 'ct_orc', calque: 'pulse', mode: 'kick', veille: 0.04, intensite: 1.0, gain: 2.2, punch: 0.030, decale: 0.04, priorite: 7 },
      { building: 'ct_archeon', calque: 'pulse', mode: 'kick', veille: 0.04, intensite: 1.0, gain: 2.2, punch: 0.030, decale: 0.08, priorite: 6 },
      { building: 'ct_nexus', calque: 'pulse', mode: 'kick', veille: 0.04, intensite: 1.0, gain: 2.1, punch: 0.028, decale: 0.12, priorite: 5 },
      { building: 'ct_humancorp', calque: 'pulse', mode: 'kick', veille: 0.04, intensite: 1.0, gain: 2.1, punch: 0.028, decale: 0.16, priorite: 4 },
      { building: 'c_arcadius', calque: 'ecran', mode: 'balise', periode: 2.6, intensite: 0.95, veille: 0.35, priorite: 3 },
      { building: 'c_tour', calque: 'ecran', mode: 'mesure', periode: 8.0, intensite: 1.15, veille: 0.55, priorite: 2 },
      { building: 'ct_holo0', calque: 'ecran', mode: 'mesure', periode: 6.5, intensite: 1.20, veille: 0.60, priorite: 1 },
      { building: 'ct_orc', calque: 'ecran', mode: 'mesure', periode: 9.0, intensite: 1.15, veille: 0.55 },
      { building: 'ct_archeon', calque: 'ecran', mode: 'mesure', periode: 10.0, intensite: 1.15, veille: 0.55 },
      { building: 'ct_nexus', calque: 'ecran', mode: 'mesure', periode: 8.5, intensite: 1.15, veille: 0.55 },
      { building: 'ct_humancorp', calque: 'ecran', mode: 'mesure', periode: 9.5, intensite: 1.15, veille: 0.55 },
      { building: 'c_change', calque: 'ecran', mode: 'mesure', periode: 10.5, intensite: 1.15, veille: 0.55 },
      { building: 'c_blanc', calque: 'ecran', mode: 'fixe', intensite: 2.75, veille: 0.26 },
      { building: 'c_immeuble', calque: 'ecran', mode: 'fixe', intensite: 2.75, veille: 0.26 },
      { building: 'c_galerie', calque: 'ecran', mode: 'fixe', intensite: 2.75, veille: 0.26 },
      { building: 'c_neon', calque: 'ecran', mode: 'fixe', intensite: 2.75, veille: 0.26 },
      { building: 'ct_arret0', calque: 'ecran', mode: 'fixe', intensite: 2.75, veille: 0.26 },
      { building: 'ct_kiosque0', calque: 'ecran', mode: 'fixe', intensite: 2.75, veille: 0.26 },
    ],
    glows: [
      { x: 74, z: 66, rx: 7, rz: 7, color: NEON_C, i: 0.55, flicker: true },
      { x: 28, z: 42, rx: 9, rz: 3.6, color: '#c8323c', i: 0.45 },
      { x: 50, z: 22, rx: 3, rz: 8, color: '#c8323c', i: 0.36 },
      { x: 50, z: 98.5, rx: 3.6, rz: 2.2, color: WARM, i: 0.55 },
      { x: 20, z: 50.5, rx: 4.6, rz: 2.2, color: NEON_C, i: 0.5 },
      { x: 38, z: 80, rx: 2.8, rz: 2.2, color: WARM, i: 0.58, flicker: true },
      { x: 86.5, z: 40, rx: 2.6, rz: 2.2, color: '#e042a8', i: 0.5 },
      { x: 62, z: 42, rx: 2.6, rz: 2.2, color: WARM, i: 0.55 },
      { x: 86, z: 90, rx: 2.6, rz: 2.2, color: WARM, i: 0.55 },
      { x: 9.5, z: 44.5, rx: 2.4, rz: 2.4, color: WARM, i: 0.5 },
      { x: 96, z: 50, rx: 3.6, rz: 2.2, color: FLOOD, i: 0.42 },
      { x: 2.4, z: 82, rx: 2.6, rz: 2.6, color: NEON_C, i: 0.46 },
    ],
    // Foule (environ 140 figurants) concentrée sur les angles du carrefour, les passages piétons et le parvis de l'Arcadius,
    // tirée par tools_center132.py hors solides, hors seuils et hors masques ; dense: true = masqué en plan large d'arrivée (version allégée).
    extras: CT_FOULE,
    // Passants : boucles sur les trottoirs, les passages piétons et le parvis uniquement (jamais sur une case solide ni derrière un sprite qui les masquerait,
    // portions libres relevées dans le jeu ; contrôlé par tests/center_rapide.py)
    walkers: [
      { sprite: civ(0), path: [[64.6, 53.2], [82, 53.2], [82, 54.8], [64.6, 54.8]], speed: 1.15, t0: 2 },
      { sprite: 'gen_ml_navetteur', path: [[64.5, 77.4], [75.8, 77.4], [75.8, 78.6], [64.5, 78.6]], speed: 1.05, t0: 9 },
      { sprite: 'gen_fs_passante', path: [[61.2, 56.6], [61.2, 70], [62.8, 70], [62.8, 56.6]], speed: 1.1, t0: 1.5 },
      { sprite: civ(5), path: [[85.2, 56.6], [85.2, 75.4], [86.8, 75.4], [86.8, 56.6]], speed: 1.2, t0: 4 },
      { sprite: 'gen_fs_client_imper', path: [[40, 48.4], [44, 48.4], [44, 49.6], [40, 49.6]], speed: 1.0, t0: 3 },
      { sprite: 'gen_pp_foule_c', path: [[32.5, 50.6], [38.5, 50.6], [38.5, 51.8], [32.5, 51.8]], speed: 1.15, t0: 8 },
      { sprite: 'gen_fs_client_costume', path: [[49.4, 20], [49.4, 26], [50.6, 26], [50.6, 20]], speed: 1.1, t0: 5 },
      { sprite: 'gen_df_foule_a', path: [[58.4, 13], [58.4, 23.5], [59.6, 23.5], [59.6, 13]], speed: 0.95, t0: 6.5 },
      { sprite: civ(2), path: [[124, 48.4], [131, 48.4], [131, 49.6], [124, 49.6]], speed: 1.1, t0: 7 },
      { sprite: 'gen_ml_foule_a', path: [[124, 52.8], [131, 52.8], [131, 54], [124, 54]], speed: 1.05, t0: 2.5 },
      { sprite: civ(3), path: [[57.6, 110.2], [57.6, 113], [58.8, 113], [58.8, 110.2]], speed: 1.0, t0: 4.5 },
      { sprite: civ(4), path: [[49.4, 32], [49.4, 38], [50.6, 38], [50.6, 32]], speed: 1.1, t0: 6 },
    ],
    drones: [ { x: 74, z: 66, r: 9, y: 7, speed: 0.2 }, { x: 34, z: 46, r: 6, y: 6, speed: -0.28, ph: 2 }, { x: 104, z: 62, r: 5, y: 6.5, speed: 0.32, ph: 4 } ],
    // Plan large d'arrivée (view.js, loc.cadre.arrivee) : cadré sur le carrefour et le parvis de l'Arcadius (libre : plan d'ensemble, le joueur peut être hors cadre) ;
    // tenu jusqu'au premier pas, geste ou zoom, puis retour en douceur à l'échelle de jeu (30 ppm ordinateur, 24 ppm téléphone).
    cadre: { arrivee: { desktop: { ppm: 12, cible: [48, 38], libre: true }, mobile: { ppm: 7, cible: [52, 42], libre: true } } },
    spawn: { player: { x: 1, z: 82 }, companion: { x: 1, z: 83 } }, city: 'steel' },
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
  ...LOCATIONS_MEGA, // Mega-Line et terminus (mega_line.js)
  ...LOCATIONS_DOME, // Dôme Fréquence (dome_frequence.js)
  ...LOCATIONS_ARENA, // Steel Arena (steel_arena.js)
  ...LOCATIONS_STRIP, // Fréquence Strip (frequence_strip.js)
  ...LOCATIONS_PULSE, // Pulse Plaza (pulse_plaza.js)
  ...LOCATIONS_CHINA, // China Lake lot 3 (china_lake.js)
  ...LOCATIONS_LOWER, // Lower-Town v1 (lower_town.js)
};
const painted = (list, loc, T) => list.map(d => ({ id: d.id, buildingId: d.buildingId, location: loc, opening: { x: d.opening[0], z: d.opening[1], side: d.face === 's' ? 'south' : 'east' },
  threshold: { x: d.threshold[0], z: d.threshold[1] }, target: { doorId: T[d.id] }, conditions: [] }));
const J = (id, loc, ox, oz, tx, tz, to, label, conditions = [], extra = {}) => ({ id, location: loc, junction: true, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: { doorId: to }, conditions, ...extra });
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
  J('c_ouest', 'steel_center', 0, 82, 1, 82, 'douane_in_est', 'Vers la douane'), // Center-Town v2 : bout ouest du trottoir sud de l'av. E-O
  ...painted(PAINTED_DOORS_CENTER, 'steel_center', { c_change_door: 'change_in_door' }),
  { id: 'change_in_door', location: 'change_in', opening: { x: 3, z: 5, side: 'south' }, threshold: { x: 3, z: 4 }, target: { doorId: 'c_change_door' }, conditions: [] },
  // Lower-Town v1 : La Descente. c_est vérifié libre (aucun bâtiment ni prop sur x 47-48, z 18 ; test lower_town.py).
  J('c_est', 'steel_center', 132, 50, 131, 50, 'l_ouest', 'La Descente (Lower-Town)'), // Center-Town v2 : bout est du trottoir nord de l'av. E-O
  ...DOORS_LOWER,
  ...DOORS_ASIA,
  ...DOORS_CHINA,
  ...DOORS_PULSE,
  ...DOORS_STRIP,
  ...DOORS_ARENA,
  ...DOORS_DOME,
  ...DOORS_MEGA,
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
  J('c_sud', 'steel_center', 58, 116, 58, 115, 'v_lift_door', 'Vers la Sous-Ville', [{ test: s => !!s.flags.sv_passage, reason: 'grille', text: 'Une grille entre deux galeries. Fermée de l’intérieur.' }], { labelPos: [58, 113] }), // Center-Town v2 : bout sud du trottoir ouest de l'av. N-S
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
  { id: 'patrouilleur', name: 'Patrouilleur', sprite: 'gen_halloran', location: 'steel_center', x: 61, z: 50.5, faceTo: [74, 66], dialogue: 'patrouilleur' },
  ...NPCS_LOWER,
  ...NPCS_ASIA,
  ...NPCS_CHINA,
  ...NPCS_PULSE,
  ...NPCS_STRIP,
  ...NPCS_ARENA,
  ...NPCS_DOME,
  ...NPCS_MEGA,
];
export const CLOSED_TEXT = {
  ...CLOSED_PULSE,
  ...CLOSED_STRIP,
  ...CLOSED_ARENA,
  ...CLOSED_DOME,
  ...CLOSED_MEGA,
  r_porte: 'La route entre dans le noir entre deux battants grands comme des immeubles. Sans passer la douane, les tourelles s\u2019en chargent.',
  r_service: s => s.flags.sol_passage ? 'La trappe dont parlait Sol. Chaîne neuve, cadenas neuf. Celui qui passe par là ne passe pas par le dessus.' : 'Une trappe de service à moitié ensablée, chaîne et cadenas. Des traces de pas fraîches, qui n\u2019en reviennent pas.',
  c_tour: 'Le Dôme Fréquence. Des écrans sur toute la façade, et pas une porte qui s\u2019ouvre pour toi.',
  c_arcadius: 'Arcadius Center. Les portes s\u2019ouvrent pour les implants qu\u2019elles reconnaissent, pas pour les autres.',
  c_blanc: 'Bureau des permis. Un écran annonce un délai d\u2019attente qui ne veut rien dire.',
  c_neon: 'Les guichets Human Corp. Tout y est à vendre, en crédits.',
  c_immeuble: 'Immeuble Nexus Transit. Derrière les vitres ambre, les tourniquets demandent un badge résident.',
  c_galerie: 'La galerie du carrefour. Une affiche annonce Groovy Crew en concert ; les grilles de nuit sont déjà baissées.',
  ct_archeon: 'Tour Archeon Industries. Un panneau ambre haut de dix étages, et aucun interphone au rez-de-chaussée.',
  ct_orc: 'Tour Orc Énergie. Les conduites ronflent derrière le marbre noir.',
  ct_humancorp: 'Tour Human Corp. Des étages de bureaux identiques et une affiche de tournée qui éclaire tout le trottoir.',
  ct_nexus: 'Tour Nexus. Le réseau tourne sans personne derrière la vitre.',
  ct_arret0: 'Arrêt Tram Central. Le prochain passage s\u2019affiche en ambre, sans heure.',
  ct_tram0: 'Une rame du tramway de Center-Town, portes verrouillées à l\u2019arrêt.',
  ct_tram1: 'Une rame du tramway de Center-Town, portes verrouillées à l\u2019arrêt.',
  ct_p_se_maison_the: 'Maison de thé. L\u2019odeur du jasmin passe sous la porte, le rideau est déjà baissé.',
  ct_so_kiosque0: 'Kiosque du jardin. Programmes du Dôme, eau et tickets, le stock d\u2019après-concert.',
  ct_echoppe0: 'Nouilles et vapeur. Le bouillon fume derrière le comptoir en laiton ; paiement par implant uniquement.',
  ct_kiosque0: 'Kiosque Presse & Médias. Les éditions validées par IO tournent en boucle sur l\u2019écran latéral.',
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
  ...DIALOGUES_CHINA,
  ...DIALOGUES_PULSE,
  ...DIALOGUES_STRIP,
  ...DIALOGUES_ARENA,
  ...DIALOGUES_DOME,
  ...DIALOGUES_MEGA,
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
