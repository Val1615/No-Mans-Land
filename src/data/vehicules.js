// Vues des véhicules (une clé de sprite -> comment la montrer sur chaque axe de circulation). Lu par render/view.js (loc.vehicules).
// axe : axe de la vue livrée par Ocre ('x' : le véhicule roule le long de x ; 'z' : le long de z).
// Sens −axe : vue_dos (sprite dédié, natif). Sur l'autre axe : vue_axe2 si elle existe, sinon miroir horizontal
// de la vue avant ou dos (miroir_axe2, vrai par défaut) : l'échelle reste à ±1, seul le signe horizontal change
// (UV et ancre miroir). Les calques _fenetres / _neon / _hover suivent le miroir ; _texte et _texte_miroir
// se dessinent sans retournement (jamais_miroir). Un champ du manifeste d'Ocre prime sur cette table.
export const VUES_VEHICULES = {
  ct_veh_taxi_avant_v4_3q: { axe: 'x', vue_dos: 'ct_veh_taxi_dos_v4_3q', miroir_axe2: true },
  ct_veh_berline_avant_v4_3q: { axe: 'x', vue_dos: 'ct_veh_berline_dos_v4_3q', miroir_axe2: true },
  ct_veh_compacte_avant_v4_3q: { axe: 'x', vue_dos: 'ct_veh_compacte_dos_v4_3q', miroir_axe2: true },
  ct_veh_limo_avant_v4_3q: { axe: 'x', vue_dos: 'ct_veh_limo_dos_v4_3q', miroir_axe2: true },
  ct_veh_utilitaire_avant_v4_3q: { axe: 'x', vue_dos: 'ct_veh_utilitaire_dos_v4_3q', miroir_axe2: true },
  ct_veh_intercepteur_avant_v4_3q: { axe: 'x', vue_dos: 'ct_veh_intercepteur_dos_v4_3q', miroir_axe2: true },
  ct_veh_moto_avant_v4_3q: { axe: 'x', vue_dos: 'ct_veh_moto_dos_v4_3q', miroir_axe2: true },
  ct_veh_motolivr_avant_v4_3q: { axe: 'x', vue_dos: 'ct_veh_motolivr_dos_v4_3q', miroir_axe2: true },
  ct_veh_depanneuse_avant_v4_3q: { axe: 'x', vue_dos: 'ct_veh_depanneuse_dos_v4_3q', miroir_axe2: true },
  ct_veh_bus_avant_v5_3q: { axe: 'x', vue_dos: 'ct_veh_bus_dos_v5_3q', miroir_axe2: true }, // v5 d'Ocre (pente 0,33, §8R) : remplace ct_veh_bus_avant_v4_3q, clés v4 conservées au manifeste
  ct_veh_tram_avant_v4_3q: { axe: 'z', vue_dos: 'ct_veh_tram_dos_v4_3q', miroir_axe2: true },
  // clés v3 conservées pour d'éventuelles scènes non basculées
  ct_taxi_v3_3q: { axe: 'x', vue_axe2: 'ct_taxi_v3_axe2_3q' },
  ct_tram_v3_3q: { axe: 'z', miroir_axe2: false },
};
