# Rencontres aléatoires et exploration régionale : suivi

Point d'entrée unique du chantier. L'architecture est dans `ARCHI.md` (Rivet). Il n'y a pas d'autre fichier de suivi.

Document de reprise. Il est tenu à jour à chaque lot publié, pour qu'un agent (Rivet, Ocre, Régie, ChatGPT ou autre) puisse reprendre le chantier sans relire les conversations.

Consigne d'origine : Valentin, 17 novembre 2026 (heure de Paris), « CONSIGNE WORK : rencontres aléatoires et exploration régionale ».

## Règle non négociable
Toute rencontre se joue dans une vraie scène isométrique, où l'on peut se déplacer, examiner, parler, combattre, fouiller et partir. Jamais une simple fenêtre de texte sur la carte du monde. Les dialogues ont lieu dans la scène.

## Rôles
- **Rivet (développement)** : le gestionnaire de rencontres, le branchement sur `onCaseEntree()` (`src/core/voyage.js`), le chargement des scènes à la demande, les transitions carte ⇄ scène, la sauvegarde en plein trajet et la réutilisation des moteurs existants (déplacement, dialogues, inventaire, combat). Pas de second moteur.
- **Ocre (création)** : les décors qui racontent quelque chose, les PNJ, les créatures, les dialogues, les issues et l'identité de chaque biome. Elle signale à Valentin toute décision qui touche au lore ou aux factions.
- **Régie (production)** : le découpage, les priorités, le contrôle de chaque jalon sur captures et la tenue de ce document.

## Points techniques connus
- `EVENEMENTS_ROUTE` (`src/data/nml.js`) est vide au départ, et `onCaseEntree()` existe déjà comme crochet remplaçable.
- Les grilles des lieux sont construites au démarrage (`src/core/game.js`) : une scène ne s'injecte pas à chaud sans adapter l'architecture. L'architecture est décrite dans `docs/rencontres/ARCHI.md` (Rivet).
- Les probabilités de base de `nml.js` ne changent pas. Pour tester, on utilise le mode DEV, avec une fonction « forcer une rencontre ».
- La maquette v0.13 (`reference/maquette/.../07_MAQUETTE_ARCHIVE_v0.13/`) est une réserve d'idées, pas du code à reprendre.

## Jalons
| Jalon | Contenu | État |
|---|---|---|
| 1 | **Une rencontre complète de bout en bout** : embuscade de pillards sur une route sèche. Arrêt du marqueur, pause du temps, sauvegarde de la position et de l'itinéraire, scène jouable (contourner, parler, combattre, fouiller, fuir), retour et reprise du voyage. Fonction DEV « forcer une rencontre ». Validé sur Pages, à 1280 et en 390. | En cours |
| 2 | Quatre familles de rencontres : caravane marchande (échange), créatures mutantes, survivant blessé (choix), événement environnemental ou découverte. Variantes par biome. | À faire |
| 3 | Patrouilles de factions, convoi en difficulté, négociant itinérant, voyageur isolé, lieu insolite. Probabilités selon la région, les factions, le scénario et les rencontres récentes. | À faire |

On ne passe pas au jalon suivant tant que le précédent n'est pas jouable sur Pages.

## Jalon 1 : embuscade (pilote)
Décor (Ocre) : pick-up en panne au milieu de la route, capot ouvert, qui sert d'appât ; caisses éventrées ; guetteurs sur les talus et derrière une carcasse, qui ne se montrent pas tous à l'arrivée ; traces qui trahissent le piège pour le joueur attentif.

Fiche complète : [PILOTE.md](PILOTE.md) (plan coté provisoire, PNJ et dialogues, combat, butin, clés d'assets, accroches pour Rivet). À aligner sur `ARCHI.md` dès sa publication.

## Journal des lots
Une ligne par lot publié : date, commit, ce qui marche en jeu, ce qui reste.

- 2026-11-17 : chantier ouvert, document créé (Régie).
- 2026-11-17 : `ff499ea` (Ocre) — [PILOTE.md](PILOTE.md), embuscade « L'appât de la piste » : décor, plan coté 30 × 24 m, dialogues, combat, butin, 20 clés d'assets. Rien en jeu encore. Reste : aligner le format sur `ARCHI.md`, validation des décisions DA/lore par Valentin, puis production des sprites.

## Décisions de DA et de lore (Ocre)
_À compléter à chaque lot._
- Jalon 1 : voir [PILOTE.md §13](PILOTE.md#13-décisions-de-da-et-de-lore-à-valider-par-valentin) (bande sans faction, noms nouveaux, lien avec Anselme, biome désert).

## Questions ouvertes pour Valentin
- La consigne reçue s'arrête au milieu de l'étape 5 (« retour au voyage ») : il manque la suite.
