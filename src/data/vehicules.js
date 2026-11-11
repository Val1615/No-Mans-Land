// Vues des véhicules (une clé de sprite -> comment la montrer sur chaque axe de circulation). Lu par render/view.js (loc.vehicules).
// axe : axe de la vue livrée par Ocre ('x' : le véhicule roule le long de x ; 'z' : le long de z).
// Sur l'autre axe : vue_axe2 (clé d'un sprite dédié) si elle existe, sinon miroir horizontal (miroir_axe2, vrai par défaut), comme les PNJ :
// l'échelle reste à ±1, seul le signe horizontal change (scale.x = -1, appliqué par les UV car THREE.Sprite ignore ce signe). Jamais d'étirement.
// Un champ axe / vue_axe2 / miroir_axe2 posé dans le manifeste d'Ocre prime sur cette table.
export const VUES_VEHICULES = {
  ct_taxi_v3_3q: { axe: 'x', vue_axe2: 'ct_taxi_v3_axe2_3q' }, // axe E-O ; axe N-S : vraie deuxième vue d'Ocre (§8F), « TAXI » à l'endroit, pas de miroir
  ct_tram_v3_3q: { axe: 'z', miroir_axe2: false }, // reste sur sa ligne N-S ; « CENTER-TOWN » au flanc : jamais en miroir
};
