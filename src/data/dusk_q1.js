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
      { sprite: 'gen_pump', x: 28.2, z: 11.6 }, { sprite: 'board', x: 29.6, z: 9 }, { sprite: 'barrel', x: 27, z: 9.6 },
      { sprite: 'lamp', x: 20, z: 14.3, solid: 0.3 },
      // sortie est : éboulis et épave (plus de barricade de milice)
      { sprite: 'wreck', x: 45.5, z: 17.2, fp: [4.6, 2.4] }, { sprite: 'rubble', x: 46.6, z: 20.4, fp: [2.6, 2.4] }, { sprite: 'rubble', x: 46.6, z: 14.9, fp: [2.6, 1.8] }, { sprite: 'rubble', x: 46.6, z: 22.8, fp: [2.6, 2.4] },
      { sprite: 'tires', x: 38.6, z: 23 }, { sprite: 'cart', x: 23.6, z: 33 }, { sprite: 'rubble', x: 33.5, z: 31 },
      { sprite: 'rubble', x: 18, z: 18.6 }, { sprite: 'rubble', x: 39, z: 4 }, { sprite: 'tires', x: 12.5, z: 20.8 },
      { sprite: 'bush', x: 2, z: 33 }, { sprite: 'bush', x: 45.5, z: 3 }, { sprite: 'bush', x: 12, z: 2 }, { sprite: 'bush', x: 29, z: 16 }, { sprite: 'bush', x: 8, z: 15.3 },
      { sprite: 'bush', x: 36, z: 34 }, { sprite: 'crate', x: 22.8, z: 30 }, { sprite: 'barrel', x: 39.3, z: 21.4 }
    ],
    spawn: { player: { x: 2.5, z: 18 }, companion: { x: 2.5, z: 19.5 } }
  },
  clinic_in: { id: 'clinic_in', name: 'Clinique', kind: 'interior', size: { w: 9, d: 8 }, ground: { base: '#a39a88', tiles: true, skin: 'g_concrete' },
    wall: '#cfc6b4', buildings: [], props: [
      { box: true, label: 'Lit', x: 0.6, z: 0.6, w: 2.2, d: 1.0, h: 0.6, color: '#d8d4ca' },
      { box: true, label: 'Lit', x: 0.6, z: 2.6, w: 2.2, d: 1.0, h: 0.6, color: '#d8d4ca' },
      { box: true, label: 'Armoire', x: 6.6, z: 0.3, w: 2.0, d: 0.6, h: 2.0, color: '#7d8f8c' },
      { box: true, label: 'Table', x: 5.4, z: 2.4, w: 1.6, d: 0.9, h: 0.9, color: '#8b7356' },
      { sprite: 'crate', x: 8.2, z: 6.8 } ] },
  bar_in: { id: 'bar_in', name: 'Le Passage', kind: 'interior', size: { w: 10, d: 9 }, ground: { base: '#6e5039', planks: true, skin: 'g_wood' },
    wall: '#8d6446', buildings: [], props: [
      { box: true, label: 'Comptoir', x: 1.5, z: 2.0, w: 5.0, d: 0.8, h: 1.1, color: '#4a2f1d' },
      { sprite: 'stove', x: 8.6, z: 0.9 }, { sprite: 'kitchen', x: 4.0, z: 0.6 },
      { box: true, label: 'Table', x: 6.8, z: 4.8, w: 1.2, d: 1.2, h: 0.75, color: '#5c3d27' },
      { box: true, label: 'Table', x: 1.6, z: 5.6, w: 1.2, d: 1.2, h: 0.75, color: '#5c3d27' },
      { sprite: 'barrel', x: 9.3, z: 7.5 }, { box: true, label: 'Table', x: 8.4, z: 2.2, w: 1.0, d: 1.0, h: 0.75, color: '#5c3d27' } ] },
  mara_in: { id: 'mara_in', name: 'Chez Mara', kind: 'interior', size: { w: 5, d: 7 }, ground: { base: '#7d6a52', planks: true, skin: 'g_wood' },
    wall: '#9a8466', buildings: [], props: [
      { box: true, label: 'Rideau', x: 2.6, z: 0.2, w: 0.1, d: 2.6, h: 2.0, color: '#6b4a3a' },
      { box: true, label: 'Paillasse', x: 3.0, z: 0.3, w: 1.8, d: 0.9, h: 0.3, color: '#8a7a5c' },
      { box: true, label: 'Table', x: 0.4, z: 3.2, w: 1.2, d: 0.9, h: 0.75, color: '#5c3d27' },
      { sprite: 'laundry', x: 1.4, z: 0.4 }, { sprite: 'barrel', x: 4.4, z: 6.4 }, { sprite: 'planters', x: 1.0, z: 6.3 } ] },
  grocery_in: { id: 'grocery_in', name: 'Épicerie d\'Anselme', kind: 'interior', size: { w: 8, d: 7 }, ground: { base: '#857055', planks: true, skin: 'g_wood' },
    wall: '#b89c74', buildings: [], props: [
      { sprite: 'shelves', x: 1.6, z: 0.6 }, { sprite: 'shelves', x: 4.0, z: 0.6 },
      { box: true, label: 'Comptoir', x: 3.0, z: 3.0, w: 0.8, d: 2.6, h: 1.0, color: '#6b4a2c' },
      { sprite: 'crate', x: 0.8, z: 5.8 }, { sprite: 'barrel', x: 1.8, z: 6.2 } ] }
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
export const COMPANION = { id: 'nilo', name: 'Nilo', sprite: 'nilo' };
