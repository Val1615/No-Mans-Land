// Lots 2 et 3 interface : données des cartes. Fonds et positions (px) : assets/ui/maps/manifest.json (Ocre, docs/assets/CARTES.md).
// Fiche : docs/design/INTERFACE.md (Régie, branche docs/regie-interface). [proposition] = décision provisoire, facile à changer ici.

// ---------- Lot 2 : Steel-Megalopolis, 4 couches empilées (1 en bas, 4 en haut) ----------
// Repère : key = clé de reperes_px_proposition du manifest (ou px donné ici quand le manifest n'en a pas), type lieu | sortie | lien | verrou,
// loc = lieu du jeu représenté (marqueur du joueur), connu(s) = découvert ? (sinon silhouette et nom « ? »), vers = couche reliée.
const vu = (...ids) => s => ids.some(i => s.seen[i]);
export const STEEL_COUCHES = [
  { n: 1, id: 'sous_ville', nom: 'Sous-Ville', court: 'Sous-Ville', reperes: [
    { key: 'sv_poutres', nom: 'Les Poutres', type: 'lieu', loc: 'sv_poutres' },
    { key: 'sv_cuve', nom: 'La Cuve', type: 'lieu', loc: 'sv_cuve' },
    { key: 'sv_trappe', nom: 'Échelle vers la douane', type: 'lien', vers: 3, connu: vu('sv_poutres') },
    { key: 'sv_monte_charge', nom: 'Grille vers Center-Town', type: 'lien', vers: 3, connu: vu('sv_cuve') },
    { key: 'sv_fosse', px: [1000, 880], nom: 'Escalier de la Fosse (Lower-Town)', type: 'lien', vers: 2, connu: vu('sv_poutres', 'steel_lower') }, // même x, y que lt_acces_sous_ville
    { key: 'sv_sortie_sud', nom: 'Route de sortie sud', type: 'sortie', connu: () => false }, // [proposition] routes connues par rumeur seulement : silhouettes
    { key: 'sv_sortie_ouest', nom: 'Route de sortie ouest', type: 'sortie', connu: () => false } ] },
  { n: 2, id: 'lower_town', nom: 'Lower-Town', court: 'Lower', reperes: [
    { key: 'steel_lower', nom: 'Lower-Town', type: 'lieu', loc: 'steel_lower' },
    { key: 'steel_asia', nom: 'Asia-Ground', type: 'lieu', loc: 'steel_asia' },
    { key: 'steel_china', nom: 'China Lake', type: 'lieu', loc: 'steel_china' },
    { key: 'lac_lower_street', nom: 'Lac de Lower Street', type: 'lieu', connu: vu('steel_lower') },
    { key: 'lt_descente', nom: 'La Descente (Center-Town)', type: 'lien', vers: 3, connu: vu('steel_lower', 'steel_center') },
    { key: 'lt_acces_sous_ville', nom: 'Escalier de la Fosse (Sous-Ville)', type: 'lien', vers: 1, connu: vu('steel_lower', 'sv_poutres') },
    { key: 'lt_mille_marches', px: [980, 690], nom: 'Mille Marches (Center-Town)', type: 'lien', vers: 3, connu: vu('steel_asia') } ] }, // [proposition] repère ajouté par le code
  { n: 3, id: 'center_town', nom: 'Center-Town', court: 'Center', reperes: [
    { key: 'steel_center', nom: 'Center-Town', type: 'lieu', loc: 'steel_center' },
    { key: 'arcadius_center', nom: 'Arcadius Center', type: 'lieu', connu: s => !!(s.seen.steel_center || s.discovered.c_arcadius) },
    { key: 'cz_rotonde', nom: 'La Rotonde', type: 'lieu', connu: s => !!(s.seen.steel_center || s.discovered.c_tour) },
    { key: 'steel_route', nom: 'La douane (sortie vers les No Man\u2019s Land)', type: 'sortie', loc: 'steel_route', region: true },
    { key: 'ct_descente', nom: 'La Descente (Lower-Town)', type: 'lien', vers: 2, connu: vu('steel_lower', 'steel_center') },
    { key: 'ct_monte_charge', nom: 'Grille de la Sous-Ville', type: 'lien', vers: 1, connu: vu('steel_center', 'sv_cuve') },
    { key: 'ct_mille_marches', px: [980, 690], nom: 'Mille Marches (Asia-Ground)', type: 'lien', vers: 2, connu: vu('steel_center', 'steel_asia') },
    { key: 'ct_ascenseur_upper', nom: 'Ascenseur d\u2019Upper-Town', type: 'lien', vers: 4, connu: vu('steel_center') } ] },
  { n: 4, id: 'upper_town', nom: 'Upper-Town', court: 'Upper', verrou: true, reperes: [
    { key: 'ut_ascenseur', nom: 'Accès refusé', type: 'verrou' } ] },
];
// Lieu du jeu -> couche (les intérieurs prennent la couche du quartier par lequel on y entre ; la douane intérieure : la douane).
export const STEEL_LOC = { sv_poutres: 1, sv_cuve: 1, steel_lower: 2, steel_asia: 2, steel_china: 2, steel_center: 3, steel_route: 3, douane_in: 3 };
export const STEEL_ALIAS = { douane_in: 'steel_route' };
