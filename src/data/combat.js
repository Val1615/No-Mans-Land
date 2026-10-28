// Combat, lot C1 (docs/design/COMBAT.md §14) : lancement combat:<id> + autosave, grille de 1 m affichée seulement en combat,
// déplacement avec aperçu et coût en PA, tours par initiative, fin de tour, 4 issues minimales ; rencontre du rôdeur.
// Toutes les valeurs de règle sont ici (COMBAT.md §0). Lot C2 : attaques mêlée / pistolet / fusil, recharge, chance bornée 5-95 %, couverture 0/1/2, ligne de vue.
export const COMBAT = {
  cell: 1,                       // cases de 1 m [décision]
  coutOrtho: 2, coutDiag: 3,     // en demi-PA : 1 PA orthogonal [décision], 1,5 PA diagonal [proposition], total arrondi au supérieur
  zoneRayon: 9,                  // zone de combat = carré de 19 x 19 cases centré sur le joueur ; ses cases de bord sont des sorties (fuite)
  coutSeRendre: 0, coutFinTour: 0,
  pvMinApres: 1,                 // §3 : PV remis à au moins 1 après le combat
  // lot C2 (§6 à §8)
  chanceMin: 5, chanceMax: 95,   // §7 [décision]
  malusParMetre: 4,              // §7 : − 4 % par mètre au-delà de la portée utile [proposition]
  couverture: [0, 20, 40],       // §8 : malus par niveau 0 / 1 / 2 [proposition]
  coutRecharger: 2,              // §6 [décision]
  pasLigneDeVue: 0.25,           // échantillonnage de la ligne de vue (m)
};
// §13 : 4 armes [proposition pour la liste] + mains nues. pa = coût d'une attaque (§6) ; portee = portée utile (m) ; mêlée = au contact (case voisine, diagonale comprise).
// degats [min, max] [proposition, point ouvert §15.3] ; chargeur = coups avant de recharger (réserve illimitée au lot C2).
export const ARMES = {
  mains:    { nom: 'Mains nues',   type: 'melee', pa: 3, portee: 1,  degats: [1, 3] },
  poignard: { nom: 'Poignard',     type: 'melee', pa: 3, portee: 1,  degats: [3, 5] },
  barre:    { nom: 'Barre de fer', type: 'melee', pa: 3, portee: 1,  degats: [4, 6] },
  pistolet: { nom: 'Pistolet',     type: 'tir',   pa: 3, portee: 8,  degats: [4, 7],  chargeur: 6 },
  fusil:    { nom: 'Fusil',        type: 'tir',   pa: 4, portee: 15, degats: [6, 10], chargeur: 5 },
};
// arme du joueur : la meilleure du Sac dans cet ordre, sinon les mains nues
export const ORDRE_ARMES = ['fusil', 'pistolet', 'barre', 'poignard'];
// Rencontres. ennemis : position relative à l'ancre (cases), pv, pa, initiative, arme (ARMES), competences { melee, armes } en %. fuitTour : l'ennemi s'enfuit au début de ce tour (rôdeur qui panique vite, §13) -> victoire.
// issues : chaînes d'actions de game.js (même format que les dialogues), drapeau combat_<id>_<issue> posé en plus.
export const ENCOUNTERS = {
  rodeur: {
    nom: 'Rôdeur du désert',
    // ancres : centre de la zone 19 x 19 par lieu (docs/villes/dusk/DUSK_TOWN_POSITIONS.md) ; toute la zone est sur la carte (aucune case dans le vide)
    ancres: { dusk_q1: { x: 22.5, z: 26.5 }, dusk_q2: { x: 32.5, z: 26.5 } },
    ennemis: [{ id: 'rodeur', nom: 'Rôdeur', sprite: 'gen_rodeur', dx: 4, dz: 2, pv: 14, pa: 6, initiative: 6, arme: 'barre', competences: { melee: 45, armes: 20 }, fuitTour: 3 }],
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
