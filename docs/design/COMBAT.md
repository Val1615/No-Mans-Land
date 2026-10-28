# Combat : conception (rien n'est codé)

Légende : **[canon]** roman tome 1 · **[décision]** Valentin · **[proposition]** à valider · **[existant]** déjà dans `src/`.
Document réécrit le 2026-10-28 après perte de la version précédente. Il remplace `docs/systemes/MENU_CREATION_COMBAT.md` §6 partout où les deux divergent (notamment le déplacement, désormais sur grille).

## 0. Principe
- Combat tactique au tour par tour façon vieux Fallout, plus fluide et moins lent [décision, MENU_CREATION_COMBAT §0].
- Même scène, même caméra v4, sans changement d'écran : liseré ambre et bandeau « COMBAT » à l'entrée ; tout s'efface à la sortie [proposition, MENU_CREATION_COMBAT §6].
- Toutes les valeurs de règle vivent dans un fichier de données unique, `src/data/combat.js`, sur le modèle de `src/data/volonte.js` [proposition].

## 1. Lancement et sauvegarde [décision]
- Un combat se lance par l'action de dialogue ou de scène **`combat:<id>`** (format `action` de `game.js`, actions séparées par `;`).
- **Autosave juste avant** le combat (`nml_save_<n>`, emplacement automatique). Le combat en cours n'est jamais sauvegardé ; on recharge l'autosave d'avant combat [existant dans la conception de la sauvegarde].
- Les crochets actuels `hook:douane_mutant` (`src/data/steel.js`, `COMBAT_HOOKS`) et `hook:combat_rodeur` (`src/data/dialogues_argent.js`) seront remplacés par `combat:douane_mutant` et `combat:rodeur` au lot C1 ; leurs issues scriptées actuelles (`warp`, `hurt`, drapeaux) deviennent les issues du combat [proposition].

## 2. Issues (4) [décision]
| Issue | Déclencheur | Effet |
|---|---|---|
| **Victoire** | plus d'ennemi actif (mort, en fuite ou rendu) | drapeau `combat_<id>_victoire`, butin, retour à l'exploration |
| **Fuite** | le joueur atteint une case de sortie de la zone de combat | drapeau `combat_<id>_fuite` ; action de fuite propre au combat (par exemple `warp:steel_route:29:34` pour la douane) |
| **Reddition** | action « Se rendre », ou ennemi qui se rend en panique | drapeau `combat_<id>_reddition` ; suite scriptée (capture, rançon, dialogue) |
| **Défaite** | PV du joueur à 0 | voir §3 |
Chaque combat déclare ses 4 issues dans sa définition (`issues: { victoire, fuite, reddition, defaite }`, chaînes d'actions), même si l'une est impossible [proposition].

## 3. Pas de mort du joueur au premier lot [décision]
- À 0 PV, le joueur tombe inconscient : c'est l'issue **défaite**, avec une suite scriptée (capture, dépouillé, réveil ailleurs), jamais un écran de fin.
- Douane : défaite = capture et chute dans la Sous-Ville (`warp:sv_poutres:3:13`, déjà écrit) [décision, MENU_CREATION_COMBAT §0].
- Après le combat, PV remis à au moins 1 [proposition, comme `hurt` qui ne descend pas sous 1].
- La mort définitive (et le mode qui l'active) est hors premier lot.

## 4. Ressources [décision]
- **PA = 5 + Agilité / 2** (arrondi bas, plus les traits) [existant : `src/data/character.js`, `derive()`].
- **PV = 25 + 3 × Endurance** (plus race et traits) [existant : `character.js`].
- Les PA se rechargent à chaque tour ; les PA non dépensés sont perdus [proposition].
- Initiative = (Agilité + Perception) / 2 [existant : `character.js`] ; ordre des tours par initiative décroissante [proposition].

## 5. Déplacement sur grille [décision]
- **Cases de 1 m**, alignées sur les mètres des zones (case (i, j) = carré x ∈ [i, i+1[, z ∈ [j, j+1[). La grille de navigation existante (`UNITS.cell = 0,5`, `src/core/grid.js`) reste celle de l'exploration ; la grille de combat en dérive : une case de 1 m est libre si ses 4 sous-cases de 0,5 m sont libres [proposition].
- **1 PA par case** orthogonale [décision] ; **diagonale 1,5 PA** [proposition]. Sur un chemin, les demi-PA s'additionnent et le total est arrondi au supérieur [proposition].
- Chemin : A* 8 directions sans couper les coins, comme `src/core/path.js` [existant], avec ce coût (1 / 1,5) au lieu de la distance euclidienne.
- Les cases occupées par une unité sont bloquées ; on ne traverse pas un allié [proposition].
- **Grille affichée seulement en combat**, semi-transparente, avec **aperçu du chemin** et de son coût en PA avant confirmation [décision]. Cases atteignables teintées, case cible marquée, coût affiché au bout du chemin [proposition].
- Le déplacement reste animé de case en case à vitesse de marche (`UNITS.walkSpeed`), sans pas à pas saccadé [proposition].

## 6. Coûts des actions [décision]
| Action | Coût (PA) |
|---|---|
| Déplacement | 1 par case, 1,5 en diagonale [proposition pour la diagonale] |
| Attaque en mêlée | 3 |
| Tir au pistolet | 3 |
| Tir au fusil | 4 |
| Tir visé (zone choisie) | +1 |
| Recharger | 2 |
| Intimider | 3 [proposition] |
| Utiliser un objet | 2 [proposition, MENU_CREATION_COMBAT §6] |
| Se rendre, passer le tour | 0 [proposition] |

## 7. Chance de toucher [décision pour les bornes]
- Résultat **borné entre 5 % et 95 %** [décision].
- Formule de départ [proposition] : base = compétence (`armes` à distance, `melee` au contact) ; − 4 % par mètre au-delà de la portée utile de l'arme ; − couverture (§8) ; − zone visée (§9) ; − malus de blessure (§9) ; puis bornage 5-95.
- Chance affichée au survol ou à l'appui long, par zone [proposition].

## 8. Couverture 0 / 1 / 2 [décision]
| Niveau | Exemple | Effet [proposition] |
|---|---|---|
| 0 | à découvert | aucun |
| 1 | partielle : caisses, tréteaux, épave, barrière basse | − 20 % à la chance de toucher |
| 2 | forte : mur, pilier, bâtiment, angle | − 40 %, ou tir impossible si la ligne de vue est entièrement coupée |
- Calcul : on lance la ligne de vue sur la grille de collision existante ; le niveau vient de la hauteur du solide traversé près de la cible (props bas = 1, bâtiments et murs = 2) [proposition].

## 9. Blessures localisées [décision]
- Zones : tête, torse, bras, jambes [proposition, MENU_CREATION_COMBAT §6].
- Effets [proposition] : tête − 30 % pour toucher, critique ; bras touché = l'arme peut tomber, − 15 % au tir ; jambe touchée = + 1 PA par case ; torse = aucun malus, dégâts pleins.
- Les malus des blessures graves sont réduits par la Volonté : `VOLONTE.blessures` (− 15 % par point au-dessus de 5, plafond 75 %) [existant : `src/data/volonte.js`].

## 10. Volonté, panique et Intimider [décision]
- La Volonté est la résistance à la **peur**, à la **douleur** et à l'**intimidation** [décision].
- **Panique** : `VOLONTE.panique` [existant] : test quand les PV passent sous 25 % ou qu'un allié meurt ; jet `rollVolonte(volonte, 6)` ; échec = − 2 PA au tour suivant. Un ennemi en panique peut fuir ou se rendre [proposition].
- **Intimider** : action de combat [décision]. Test opposé [proposition] : Charisme ou Force de l'auteur contre `rollVolonte` de la cible ; réussite = test de panique immédiat de la cible. L'effet subi par le joueur est réduit par `VOLONTE.intimidation` (− 10 % par point au-dessus de 5, plafond 60 %) [existant].
- Le trait « Gueule cassée » donne un bonus à Intimider [proposition, trait stocké sans effet aujourd'hui].

## 11. Vitesse et rythme [décision]
- Vitesse des tours ennemis **×1 / ×2 / ×4**, réglable dans les options et par maintien d'une touche [décision, option déjà prévue dans les options de MENU_CREATION_COMBAT].
- Tours ennemis en simultané visuel quand ils n'interagissent pas [proposition].

## 12. Interface [décision]
- Aucune UI dans le **tiers central** de l'écran : l'action reste visible.
- UI **discrète et semi-transparente** : barre de PA et PV en bas à gauche, file d'initiative en haut, actions en bas à droite [proposition pour les emplacements].
- **Mobile : 4 boutons de 52 px** [décision] ; contenu proposé : Attaquer, Viser, Recharger, Fin du tour ; Intimider, Objet et Se rendre dans un menu « plus » [proposition]. Premier tap = aperçu, second tap = confirmer [proposition].

## 13. Premier lot de contenu [décision]
- **4 armes** [proposition pour la liste] : poignard (mêlée), barre de fer (mêlée), pistolet, fusil.
- **3 ennemis** dans **2 rencontres** : douane-mutant (2 soldats + 1 renfort) et rôdeur (1 rôdeur du désert, lien avec `dialogues_argent.js`).
- **Douane** [décision] : 2 soldats du Service au départ, **1 renfort au tour 3**. Gagnable mais **très dur** ; la fuite vers le désert reste l'issue attendue. Réglage [proposition] : soldats au fusil, couverture 1 aux barrières, renfort arrivant par la guérite.
- **Rôdeur** [proposition] : un seul adversaire, mêlée, qui panique vite ; sert de tutoriel.

## 14. Lots C1 à C5 [décision pour le découpage]
| Lot | Contenu [proposition pour le détail] | Vérification |
|---|---|---|
| **C1** | `combat:<id>` et autosave, grille de 1 m affichée, déplacement avec aperçu et coût, tours, fin de tour, 4 issues en version minimale ; rencontre rôdeur | tests de coûts (1 / 1,5), autosave présente, 4 issues atteignables par test scripté |
| **C2** | attaques mêlée, pistolet, fusil, recharge, chance bornée 5-95 %, couverture 0/1/2, ligne de vue | tests de bornes et de couverture |
| **C3** | blessures localisées, tir visé + 1, panique (`volonte.js`), Intimider | tests de panique et d'Intimider avec graine fixée |
| **C4** | rencontre douane (2 + 1 renfort au tour 3), IA simple (avancer, se couvrir, tirer, fuir), défaite = Sous-Ville | partie scriptée de victoire, de fuite et de défaite |
| **C5** | UI finale (hors tiers central, semi-transparente), mobile 4 boutons de 52 px, vitesses ×1/×2/×4, captures desktop et 390 × 844 | captures, aucun élément dans le tiers central |

## 15. Points ouverts
1. Diagonale à 1,5 PA et arrondi des demi-PA.
2. Valeurs de couverture (− 20 % / − 40 %) et de zones.
3. Liste exacte des 4 armes et leurs dégâts.
4. Coût d'Intimider (3 PA proposé).
5. Accroches de China Lake (`hook_hommes_de_main`, `hook_ah_lam`) : à convertir en `combat:` après C4 ou à laisser en drapeaux.
