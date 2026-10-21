// Définition immuable de la scène d'étalonnage. Le rendu, la collision et l'interaction lisent CES données.
export const LOCATIONS = {
  street: {
    id: 'street', name: 'Rue (étalonnage)', size: { w: 24, d: 20 }, ground: '#6b6256',
    buildings: [
      { id: 'shop', label: 'Boutique (placeholder)', x: 4, z: 4, w: 8, d: 6, storeys: 1, visitable: true, color: '#9a7b55' },
      { id: 'tower', label: 'Volume occultant (placeholder)', x: 14, z: 3, w: 4, d: 4, storeys: 3, visitable: false, color: '#5d6a74' }
    ],
    props: [ { id: 'crate', label: 'Caisse', x: 9, z: 14, w: 1, d: 1, h: 1, color: '#7a5a32' } ],
    spawn: { player: { x: 6, z: 16 }, companion: { x: 7.5, z: 17 } }
  },
  shop_interior: {
    id: 'shop_interior', name: 'Intérieur boutique (étalonnage)', size: { w: 8, d: 6 }, ground: '#8a7458',
    walls: true, buildings: [],
    props: [ { id: 'counter', label: 'Comptoir', x: 1, z: 1, w: 4, d: 1, h: 1.1, color: '#5a3d22' } ],
    spawn: null
  }
};

// Contrat de porte unique : ouverture, seuil, cible, retour, conditions. Pas d'autre définition ailleurs.
export const DOORS = [
  {
    id: 'shop_door', buildingId: 'shop', location: 'street',
    // ouverture sur la façade sud (z = 4 + 6 = 10), centrée en x = 8
    opening: { x: 8, z: 10, facing: 'south' },
    threshold: { x: 8, z: 11 },            // case praticable devant l'ouverture
    target: { location: 'shop_interior', doorId: 'shop_door_in' },
    conditions: []
  },
  {
    id: 'shop_door_in', buildingId: null, location: 'shop_interior',
    opening: { x: 4, z: 6, facing: 'south' },
    threshold: { x: 4, z: 5 },
    target: { location: 'street', doorId: 'shop_door' },
    conditions: []
  }
];
