// Dusk-Town, quartier 1 « La Pompe ». Définitions immuables, en mètres. Voir docs/quartiers/DUSK_TOWN_Q1.md.
// Bâtiments : volumes faits main (facade = texture peinte procéduralement, statut provisoire).
// faces : 'boarded' (porte condamnée), 'closed' (porte fermée), 'garage', 'service' (porte réelle).
const B = (o) => ({ storeys: 1, visitable: false, ...o });
export const LOCATIONS = {
  dusk_q1: {
    id: 'dusk_q1', name: 'Dusk-Town · La Pompe', size: { w: 48, d: 36 }, kind: 'exterior',
    ground: { base: '#8d7a5e', skin: 'g_sand', zones: [
      { x: 30, z: 30, w: 6, d: 5, kind: 'grass' }, { x: 0, z: 0, w: 6, d: 4, kind: 'grass' },
      { x: 0, z: 14, w: 48, d: 8, kind: 'asphalt' },
      { x: 0, z: 15, w: 4, d: 6, kind: 'track' },
      { x: 22, z: 2, w: 6, d: 12, kind: 'packed' }, { x: 20, z: 2, w: 10, d: 8, kind: 'packed' },
      { x: 22, z: 22, w: 6, d: 14, kind: 'packed' } ] },
    // Décision de Valentin : personne dans les rues. Façades d'abandon, entrées camouflées mais lisibles (cadre, seuil dégagé, traces).
    buildings: [
      B({ id: 'clinic', label: 'Clinique', x: 7, z: 5, w: 9, d: 8, height: 6, skin: { s: 'yellow_s', e: 'yellow_e' }, roof: 'roof_flat', visitable: true, color: '#a9a091', trim: '#5f6e6a', cue: 'cross', windows: 'boarded' }),
      B({ id: 'bar', label: 'Le Passage', x: 31, z: 4, w: 10, d: 9, height: 6.5, skin: { s: 'palazzo_s', e: 'palazzo_e' }, roof: 'roof_palazzo', visitable: true, color: '#8c6248', trim: '#3f2a1c', cue: 'bottle', windows: 'boarded', roofHoles: true }),
      B({ id: 'tower', label: 'Tour effondrée', x: 43, z: 8, w: 4, d: 5, height: 6.5, color: '#7a7064', trim: '#4a4038', door: 'none', windows: 'holes', ruin: 'partial', roofHoles: true }),
      B({ id: 'mara_house', label: 'Maison de Mara', x: 1, z: 5, w: 5, d: 7, height: 3.5, skin: { s: 'cottage_s', e: 'cottage_e' }, roof: 'roof_tiles', visitable: true, color: '#9a8a70', trim: '#5b4a36', cue: 'drop', windows: 'boarded' }),
      B({ id: 'grocery', label: 'Épicerie', x: 14, z: 24, w: 8, d: 7, height: 6, skin: { s: 'shop_s', e: 'shop_e', cover: { s: [[0.0, 0.6, 0.62, 0.4]] } }, roof: 'roof_tiles', visitable: true, color: '#b29672', trim: '#6a3b2a', cue: 'jar', windows: 'boarded', roofHoles: true }),
      B({ id: 'house_a', label: 'Maison', x: 4, z: 24, w: 4, d: 6, color: '#a48c70', trim: '#55606a', door: 'boarded', windows: 'holes' }),
      B({ id: 'house_b', label: 'Maison', x: 8, z: 24, w: 5, d: 6, storeys: 2, color: '#8e7f6d', trim: '#6a4b33', door: 'boarded', windows: 'boarded', roofHoles: true }),
      B({ id: 'ruin', label: 'Ruine', x: 30, z: 24, w: 7, d: 7, height: 3.5, skin: { s: 'ruin_s', e: 'ruin_e' }, roof: 'roof_ruin', color: '#7f7263', trim: '#5a5048', door: 'none', windows: 'none', ruin: true }),
      B({ id: 'workshop', label: 'Atelier', x: 39, z: 24, w: 8, d: 9, height: 3.5, skin: { s: 'garage_s', e: 'cottage_e' }, roof: 'roof_tiles', color: '#74746c', trim: '#7a5a2b', door: 'garage', windows: 'holes', roofHoles: true })
    ],
    props: [
      { sprite: 'gen_pump', x: 25, z: 6 }, { sprite: 'board', x: 21, z: 3.2 }, { sprite: 'barrel', x: 27.6, z: 4.2 },
      { sprite: 'lamp', x: 20, z: 14.3, solid: 0.3 },
      // sortie est : éboulis et épave (plus de barricade de milice)
      { sprite: 'wreck', x: 45.5, z: 17.2, fp: [4.6, 2.4] }, { sprite: 'rubble', x: 46.6, z: 20.4, fp: [2.6, 2.4] }, { sprite: 'rubble', x: 46.6, z: 14.9, fp: [2.6, 1.8] }, { sprite: 'rubble', x: 46.6, z: 22.8, fp: [2.6, 2.4] },
      { sprite: 'tires', x: 38.2, z: 25.5 }, { sprite: 'cart', x: 23.6, z: 33 }, { sprite: 'rubble', x: 33.5, z: 27.5 },
      { sprite: 'rubble', x: 18, z: 18.6 }, { sprite: 'rubble', x: 41, z: 6.5 }, { sprite: 'tires', x: 12.5, z: 20.8 },
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

export const DOORS = [
  { id: 'mara_door', buildingId: 'mara_house', location: 'dusk_q1', opening: { x: 4, z: 12, side: 'south' }, threshold: { x: 4, z: 13 }, target: { doorId: 'mara_in_door' }, conditions: [] },
  { id: 'mara_in_door', location: 'mara_in', opening: { x: 3.5, z: 7, side: 'south' }, threshold: { x: 3.5, z: 6 }, target: { doorId: 'mara_door' }, conditions: [] },
  { id: 'clinic_door', buildingId: 'clinic', location: 'dusk_q1', opening: { x: 13, z: 13, side: 'south' }, threshold: { x: 13, z: 14 }, target: { doorId: 'clinic_in_door' }, conditions: [] },
  { id: 'clinic_in_door', location: 'clinic_in', opening: { x: 5, z: 8, side: 'south' }, threshold: { x: 5, z: 7 }, target: { doorId: 'clinic_door' }, conditions: [] },
  { id: 'bar_door', buildingId: 'bar', location: 'dusk_q1', opening: { x: 39.5, z: 13, side: 'south' }, threshold: { x: 39.5, z: 14 }, target: { doorId: 'bar_in_door' }, conditions: [] },
  { id: 'bar_in_door', location: 'bar_in', opening: { x: 5, z: 9, side: 'south' }, threshold: { x: 5, z: 8 }, target: { doorId: 'bar_door' }, conditions: [] },
  { id: 'grocery_door', buildingId: 'grocery', location: 'dusk_q1', opening: { x: 22, z: 26.5, side: 'east' }, threshold: { x: 23, z: 26.5 }, target: { doorId: 'grocery_in_door' }, conditions: [] },
  { id: 'grocery_in_door', location: 'grocery_in', opening: { x: 8, z: 3.5, side: 'east' }, threshold: { x: 7, z: 3.5 }, target: { doorId: 'grocery_door' }, conditions: [] }
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
