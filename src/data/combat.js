// Combat, lot C1 (docs/design/COMBAT.md §14) : lancement combat:<id> + autosave, grille de 1 m affichée seulement en combat,
// déplacement avec aperçu et coût en PA, tours par initiative, fin de tour, 4 issues minimales ; rencontre du rôdeur.
// Toutes les valeurs de règle sont ici (COMBAT.md §0). Les attaques réelles (chance de toucher, couverture) sont le lot C2.
export const COMBAT = {
  cell: 1,                       // cases de 1 m [décision]
  coutOrtho: 2, coutDiag: 3,     // en demi-PA : 1 PA orthogonal [décision], 1,5 PA diagonal [proposition], total arrondi au supérieur
  zoneRayon: 9,                  // zone de combat = carré de 19 x 19 cases centré sur le joueur ; ses cases de bord sont des sorties (fuite)
  coutSeRendre: 0, coutFinTour: 0,
  pvMinApres: 1,                 // §3 : PV remis à au moins 1 après le combat
};
// Rencontres. ennemis : position relative au joueur (cases), pv, pa, initiative ; frappe = coup fixe de C1 (au contact, coût, dégâts),
// remplacé au lot C2 par la chance de toucher. fuitTour : l'ennemi s'enfuit au début de ce tour (rôdeur qui panique vite, §13) -> victoire.
// issues : chaînes d'actions de game.js (même format que les dialogues), drapeau combat_<id>_<issue> posé en plus.
export const ENCOUNTERS = {
  rodeur: {
    nom: 'Rôdeur du désert',
    // ancres : centre de la zone 19 x 19 par lieu (docs/villes/dusk/DUSK_TOWN_POSITIONS.md) ; toute la zone est sur la carte (aucune case dans le vide)
    ancres: { dusk_q1: { x: 27.5, z: 23.5 }, dusk_q2: { x: 32.5, z: 23.5 } },
    ennemis: [{ id: 'rodeur', nom: 'Rôdeur', sprite: 'gen_sv_dealer', dx: 4, dz: -2, pv: 14, pa: 6, initiative: 6, frappe: { pa: 3, degats: 3 }, fuitTour: 3 }],
    issues: {
      victoire: 'flag:a_rodeur_fait',                // il détale ; les bidons restent
      fuite: 'flag:a_rodeur_fait',                   // tu as couru jusqu'au bout de la rue
      reddition: 'take:bidon;flag:a_rodeur_fait',    // tu lâches un bidon
      defaite: 'take:bidon;flag:a_rodeur_fait',      // tu te réveilles dans le sable, un bidon en moins (jamais de mort au lot C1)
    },
    textes: {
      debut: 'Le rôdeur revient, la barre levée. COMBAT.',
      victoire: 'Il recule, crache, et file vers les ruines.',
      fuite: 'Tu cours jusqu\u2019au bout de la rue. Il ne suit pas.',
      reddition: 'Tu poses un bidon par terre. Il le ramasse et s\u2019en va.',
      defaite: 'Le sable. Le ciel. Il manque un bidon.',
    },
  },
};
