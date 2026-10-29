// Lot 3 interface : carte des No Man's Land et voyage case par case (à la Fallout 1 et 2).
// Fond, grille (22 x 20, 167 cases terrestres, biomes) et grands lieux : assets/ui/maps/manifest.json (Ocre, docs/assets/CARTES.md).
// Fiche : docs/design/INTERFACE.md §3 (Régie). [proposition] = décision provisoire, facile à changer ici.
// UNE seule table de terrains (validée par Valentin le 29/10) : h = heures pour entrer dans la case, p = probabilité d'événement.
// La piste passe par-dessus n'importe quel terrain. Mer : bloquée (seules les 167 cases terrestres du manifest existent).
export const TERRAINS = {
  cote:   { nom: 'Côte', h: 2, p: 0.05 },
  desert: { nom: 'Désert', h: 2, p: 0.10 },
  foret:  { nom: 'Forêt', h: 3, p: 0.10 },
  rocher: { nom: 'Rocher', h: 3, p: 0.15 },
  verre:  { nom: 'Verre vitrifié', h: 3, p: 0.20 },
  piste:  { nom: 'Piste', h: 1, p: 0.05 },
};
export const BIOME_TERRAIN = { coast: 'cote', desert: 'desert', forest: 'foret', rock: 'rocher', glass: 'verre' }; // biomes de la maquette v0.13 (manifest)
// Table d'événements de route : VIDE pour l'instant (aucun événement réel). Forme prévue : { id, terrains?: [...], si?: etat => bool, poids?: n, effet(etat) }.
export const EVENEMENTS_ROUTE = [];
// Pistes de la maquette v0.13 (tools/map.py, reprises par tools_cartes.py d'Ocre) : polylignes en unités maquette (50 par case).
export const PISTES_MAQUETTE = [
  [[234, 143], [367, 180], [499, 268], [622, 290], [879, 271]],
  [[367, 180], [464, 108], [715, 184], [622, 290], [740, 442], [762, 749]],
  [[499, 268], [478, 426], [302, 432]],
  [[478, 426], [568, 621], [762, 749], [907, 924]],
  [[580, 238], [622, 290], [602, 333], [478, 426]],
];
// Grands lieux jouables : clé du manifest -> porte d'arrivée (le joueur apparaît sur son seuil) et sorties régionales du lieu.
// Les autres grands lieux du manifest s'affichent une fois découverts (brouillard sinon) mais n'ont pas encore de terrain : on y fait halte.
export const LIEUX_JEU = {
  dusk: { entree: 'j_q2_est', sorties: ['j_q2_est'], prefixe: 'dusk_' },
  steel: { entree: 'j_route_sud', sorties: ['j_route_sud'] }, // [proposition] la douane de Steel est sur la case de Steel-Megalopolis
};
export const LIEUX_CONNUS_DEPART = ['dusk', 'steel']; // [proposition] Dusk-Town (chez soi) et le dôme de Steel, visible de loin
// Brouillard de guerre [décision Valentin, 29/10] : cases voilées tant qu'elles ne sont ni traversées ni vues (rayon d'une case autour du trajet).
export const RAYON_VUE = 1;
export const HEURE_DEPART = 8; // jour 1, 8 h
export const VOYAGE_PAS_MS = 380; // durée de l'animation d'une case (ms)
