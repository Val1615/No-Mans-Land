// Dusk-Town, quartier 1 « La Pompe ». Définitions immuables, en mètres. Voir docs/quartiers/DUSK_TOWN_Q1.md.
import { BUILDINGS_Q1, PAINTED_DOORS_Q1 } from './buildings_q1.js';
// Bâtiments : sprites entiers de la maquette posés tels quels ; la collision est l'emprise déclarée.
export const LOCATIONS = {
  dusk_q1: {
    id: 'dusk_q1', name: 'Dusk-Town · La Pompe', size: { w: 48, d: 36 }, kind: 'exterior',
    ground: { base: '#8d7a5e', skin: 'g_sand', zones: [
      { x: 30, z: 30, w: 6, d: 5, kind: 'grass' }, { x: 0, z: 0, w: 6, d: 4, kind: 'grass' },
      { x: 0, z: 14, w: 48, d: 8, kind: 'asphalt' },
      { x: 0, z: 15, w: 4, d: 6, kind: 'track' },
      { x: 25.5, z: 8, w: 5.5, d: 6, kind: 'packed' }, { x: 26, z: 29, w: 4, d: 7, kind: 'packed' } ] },
    // Décision de Valentin : personne dans les rues. Façades d'abandon, entrées camouflées mais lisibles (cadre, seuil dégagé, traces).
    // v4 : sprites entiers de la maquette ; emprise, ancre et portes mesurées sur l'image (tools_buildings.py).
    buildings: BUILDINGS_Q1,
    props: [
      { sprite: 'gen_pump', x: 28.2, z: 11.6 }, { sprite: 'board', x: 29.6, z: 9 }, { sprite: 'barrel', x: 27.6, z: 7.4 },
      { sprite: 'lamp', x: 20, z: 14.3, solid: 0.3 },
      // sortie est : éboulis et épave ; v7 : un passage à pied reste ouvert côté sud de l'avenue (jonction vers Le Transit, z 20)
      { sprite: 'wreck', x: 45.5, z: 16.6, fp: [4.6, 2.4] }, { sprite: 'rubble', x: 46.6, z: 14.6, fp: [2.6, 1.4] }, { sprite: 'rubble', x: 46.6, z: 23.0, fp: [2.6, 2.0] },
      { sprite: 'tires', x: 38.6, z: 23 }, { sprite: 'cart', x: 23.6, z: 33 }, { sprite: 'rubble', x: 33.5, z: 31 },
      { sprite: 'rubble', x: 18, z: 18.6 }, { sprite: 'rubble', x: 39, z: 4 }, { sprite: 'tires', x: 12.5, z: 20.8 },
      { sprite: 'bush', x: 2, z: 33 }, { sprite: 'bush', x: 45.5, z: 3 }, { sprite: 'bush', x: 12, z: 2 }, { sprite: 'bush', x: 29, z: 16 }, { sprite: 'bush', x: 8, z: 15.3 },
      { sprite: 'bush', x: 36, z: 34 }, { sprite: 'crate', x: 22.8, z: 30 }, { sprite: 'barrel', x: 39.3, z: 21.4 }
    ],
    spawn: { player: { x: 2.5, z: 18 }, companion: { x: 2.5, z: 19.5 } }
  },
  // v6 : intérieurs en assets réels. Sols et murs = textures (maquette ou générées) sur la géométrie en mètres ;
  // mobilier = sprites dont l'angle a été contrôlé (tools_interiors.py), posés par leur emprise (x, z = coin min, en m).
  // Les objets longs sont tous orientés le long de l'axe x : c'est la seule orientation que les sprites montrent.
  clinic_in: { id: 'clinic_in', name: 'Clinique', kind: 'interior', size: { w: 9, d: 8 }, ground: { base: '#a39a88', skin: 'f_tiles', tileM: 2 },
    wall: '#cfc6b4', wallSkin: 'w_plaster', buildings: [], props: [
      { furn: 'clinic_cot_b', x: 0.4, z: 0.4 }, { furn: 'clinic_cot_b', x: 0.4, z: 2.1 },
      { furn: 'm_archive_shelf', x: 3.0, z: 0.25 }, { furn: 'clinic_cabinet', x: 7.4, z: 0.25 },
      { furn: 'clinic_table', x: 4.4, z: 2.6 }, { furn: 'm_desk', x: 7.0, z: 3.7 },
      { furn: 'clinic_stretcher_b', x: 6.1, z: 6.7 } ] },
  bar_in: { id: 'bar_in', name: 'Le Passage', kind: 'interior', size: { w: 10, d: 9 }, ground: { base: '#6e5039', skin: 'f_wood', tileM: 2.5 },
    wall: '#8d6446', wallSkin: 'w_brick', buildings: [], props: [
      { furn: 'bar_backshelf_b', x: 3.0, z: 0.25 }, { furn: 'bar_counter_b', x: 2.1, z: 2.0 },
      { furn: 'bar_table_b', x: 6.4, z: 4.6 }, { furn: 'bar_table_b', x: 1.2, z: 5.4 }, { furn: 'm_archive_shelf', x: 7.6, z: 0.25 } ] },
  mara_in: { id: 'mara_in', name: 'Chez Mara', kind: 'interior', size: { w: 5, d: 7 }, ground: { base: '#7d6a52', skin: 'f_earth', tileM: 2 },
    wall: '#9a8466', wallSkin: 'w_clay', buildings: [], props: [
      { furn: 'home_mattress_d', x: 0.3, z: 0.3 }, { furn: 'home_curtain', x: 2.5, z: 2.7 },
      { furn: 'home_table', x: 0.3, z: 3.4 }, { furn: 'home_water', x: 3.4, z: 4.0 } ] },
  grocery_in: { id: 'grocery_in', name: 'Épicerie d\'Anselme', kind: 'interior', size: { w: 8, d: 7 }, ground: { base: '#857055', skin: 'f_concrete', tileM: 3 },
    wall: '#b89c74', wallSkin: 'w_planks', buildings: [], props: [
      { furn: 'shop_shelf', x: 0.4, z: 0.25 }, { furn: 'shop_shelf', x: 2.6, z: 0.25 }, { furn: 'm_archive_shelf', x: 5.2, z: 0.25 },
      { furn: 'shop_counter', x: 1.2, z: 4.9 }, { furn: 'home_water', x: 5.6, z: 1.6 } ] }
};

const T = { mara_house_door: 'mara_in_door', clinic_door: 'clinic_in_door', bar_door: 'bar_in_door', grocery_door: 'grocery_in_door2', grocery_door2: 'grocery_in_door' };
export const DOORS = [
  ...PAINTED_DOORS_Q1.map(d => ({ id: d.id, buildingId: d.buildingId, location: 'dusk_q1', opening: { x: d.opening[0], z: d.opening[1], side: d.face === 's' ? 'south' : 'east' }, threshold: { x: d.threshold[0], z: d.threshold[1] }, target: { doorId: T[d.id] }, conditions: [], painted: d.painted_px })),
  { id: 'mara_in_door', location: 'mara_in', opening: { x: 3.5, z: 7, side: 'south' }, threshold: { x: 3.5, z: 6 }, target: { doorId: 'mara_house_door' }, conditions: [] },
  { id: 'clinic_in_door', location: 'clinic_in', opening: { x: 5, z: 8, side: 'south' }, threshold: { x: 5, z: 7 }, target: { doorId: 'clinic_door' }, conditions: [] },
  { id: 'bar_in_door', location: 'bar_in', opening: { x: 5, z: 9, side: 'south' }, threshold: { x: 5, z: 8 }, target: { doorId: 'bar_door' }, conditions: [] },
  { id: 'grocery_in_door2', location: 'grocery_in', opening: { x: 5.5, z: 7, side: 'south' }, threshold: { x: 5.5, z: 6 }, target: { doorId: 'grocery_door' }, conditions: [] },
  { id: 'grocery_in_door', location: 'grocery_in', opening: { x: 8, z: 3.5, side: 'east' }, threshold: { x: 7, z: 3.5 }, target: { doorId: 'grocery_door2' }, conditions: [] }
];

// Personne dehors : tous les PNJ sont à l'intérieur.
export const NPCS = [
  { id: 'mara', name: 'Mara', sprite: 'gen_mara', location: 'mara_in', x: 1.0, z: 2.0, faceTo: [3.5, 7], dialogue: 'mara' },
  { id: 'bruno', name: 'Bruno', sprite: 'bruno', location: 'mara_in', x: 3.8, z: 1.6, faceTo: [1.0, 3.6], dialogue: 'bruno' },
  { id: 'vera', name: 'Vera', sprite: 'gen_vera', location: 'clinic_in', x: 6.2, z: 1.6, faceTo: [7.6, 0.6], dialogue: 'vera' },
  { id: 'hector', name: 'Hector', sprite: 'gen_hector', location: 'bar_in', x: 4.0, z: 1.4, faceTo: [4.0, 2.4], dialogue: 'hector' },
  { id: 'ileana', name: 'Ileana', sprite: 'ileana', location: 'bar_in', x: 8.9, z: 3.6, faceTo: [5, 9], dialogue: 'ileana' },
  { id: 'anselme', name: 'Anselme', sprite: 'anselme', location: 'grocery_in', x: 2.2, z: 4.2, faceTo: [7, 3.5], dialogue: 'anselme' }
];

export const START = { location: 'dusk_q1', hp: 27, maxHp: 40, money: 40 };
export const COMPANION = { id: 'nilo', name: 'Nilo', sprite: 'nilo', enabled: false }; // v10 : retiré du début, débloqué plus tard par une quête
