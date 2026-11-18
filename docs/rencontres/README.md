# Rencontres aléatoires et exploration régionale : suivi

Point d'entrée unique du chantier. L'architecture est dans [`ARCHI.md`](ARCHI.md) (Rivet). Il n'y a pas d'autre fichier de suivi.

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
- 2026-11-17 : `8576eaa` (Rivet) — [ARCHI.md](ARCHI.md) : architecture (catalogue `src/data/rencontres.js`, `game.ajouterLieu`, gestionnaire `src/core/rencontres.js`, sortie de bord, sauvegarde dans la scène, combat existant étendu, DEV « forcer une rencontre ») et verdict sur le pilote (§6) : la sente reste (niveaux + solides, talus en couverture 1) ; ne rentrent pas : lit à −0,8 m, guetteur acheté neutre en combat, drapeau par case, trait « Œil de pillard », examen au survol. Technique : rien de codé encore, aucun fichier `src/` touché. Reste : jalon 1 (≈ 2 j de dev). Tester : rien à tester en jeu pour l'instant ; au jalon 1, `?dev=1` → DEV « Rencontre » → forcer `embuscade_piste`, puis `tests/rencontres_rapide.py` (URL, OUT ; 1280 et 390).
- 2026-11-17 : `2b2013c` (Ocre) — PILOTE.md aligné sur ARCHI.md : les 7 points de Rivet intégrés, sente gardée (repli 390 noté), ennemis en positions absolues sur cases libres, §14 entrée au format ARCHI §4. Planche concept corrigée (Don Trapo contre la portière, épave sans roues), hors dépôt. Rien en jeu. Reste : sprites du pilote (en cours), puis câblage Rivet.
- 2026-11-17 : `0f15e0c` + `333215b` + docs (Ocre) — sprites du pilote dans `assets/rencontres/` (manifeste `assets/rencontres/manifest.json`) : lot 1 = 8 sols `g_rc_*` (512 px = 4 m) et 18 modules `_3q` (talus a/b/fin + sente, rochers, berges, panneau, pick-up, caisses, fil, miroir + `_neon`, épave, bâche, décalques) au pipeline Mega-Line, 50 px/m ; lot 2 = 5 PNJ en face + dos (+ Quilla assise, Morsa couché) et 4 portraits. Table des poses pour Rivet : [PILOTE.md §15](PILOTE.md#15-table-des-poses-pour-rivet). Rien en jeu (aucun `src/` touché). Planche et maquette (MAQUETTE) hors dépôt : `nml-shots/rencontres/`. Reste : câblage Rivet (`depth` +1 crête/Morsa, `vue_dos`, surélévation par `ancre`), défauts connus (joints doux entre talus, miroir non repeint, Morsa couché vu de profil).
- 2026-11-18 : `f3903a0` (Rivet) — **jalon 1 jouable, sprites d'Ocre câblés** (pas de lot gabarits séparé : les sprites étaient sur main avant le premier push). Marche en jeu : rencontre tirée à l'entrée d'une case (taux de `nml.js` inchangés, piste 5 %) ou forcée (DEV « Rencontres » → « Forcer une rencontre » / « Entrer maintenant », ou `?rencontre=embuscade_piste`) ; la carte se ferme, la scène 30 × 24 m se charge à chaud (`game.ajouterLieu`, statut de voyage `rencontre`) ; déclencheurs T1 (Quilla se lève), T2 (fil), T3 (Tuerto), garde, discrétion sous l'épave ; dialogues des 5 PNJ (péage, marchandage, bluff, intimidation, Pibe, Morsa, Tuerto, Don Trapo) ; 15 points de fouille/examen (anneaux sable) ; combat `embuscade_piste` sur zone fixe (centre 18 ; 13), positions absolues, Tuerto en renfort au tour 2, reddition de Quilla sous 25 % ; fuite ou porte ouest → carte en halte, portes est (péage réglé) et lit → trajet repris là où il s'était arrêté ; journal par case (`region.rencontres`) : pas de nouveau tirage, butin pris et morts gardés, sortie est bloquée tant que la bande tient la piste ; sauvegarde dans la scène (recréée au chargement) et en route. Sprites (§15 + 6 points) : crête surélevée par `ancre` et `etage: 1`, décalques et berges en couche sol, PNJ pivot 0 avec `vue_dos` (dos quand le PNJ regarde vers le fond) et miroir, Morsa couché à `y: 1.3` sans miroir (tête à l'ouest), Pibe à 2,5 par le niveau de crête, niche libre. Reste : Morsa en combat passe sur la case libre la plus proche (19 ; 17), la niche n'a aucune case de 1 m libre ; défauts connus d'Ocre (joints des talus, miroir/fil, Morsa de profil) ; IA de combat basique (C2). Tester : `?dev=1`, panneau DEV → Rencontres ; `python3 tests/rencontres_rapide.py` (URL, OUT ; 1280 et 390, 71 vérifications) ; captures `/tmp/nml-test-out/rencontres_j1/livraison/`.
- 2026-11-18 : CARAVANE (Ocre) — [CARAVANE.md](CARAVANE.md), jalon 2, famille caravane marchande : « La citerne qui respire » (`caravane_relais`, préfixe `car_`), caravane de Doña Remedios en panne au relais UFSA du puits sec, piste Douane ouest → Station de répartition (J07, J08). Scène 35 × 26 m sans niveaux, zone de combat 19 × 19 centrée (22 ; 16,5), 4 PNJ (Remedios, Fierro, Ciro, Lena) avec dialogues complets ; issues : passer, commerce à stock limité, troc, nouvelles, réparation (quête courte), escorte, secret de la passagère, rançon (issue tendue), vol, combat optionnel (3 ennemis, reddition de Remedios = victoire), fuite. Réutilise talus, rochers, panneau, bâche et sols `g_rc_*` ; 9 décors et 4 PNJ nouveaux listés (CARAVANE §10), **aucun sprite produit** (consigne Régie : après vérification du cadrage du jalon 1). Maquette concept (MAQUETTE) hors dépôt : `nml-shots/rencontres/caravane_concept.png`. Rien en jeu, aucun `src/` touché. Reste : validation des décisions de lore (CARAVANE §13), puis sprites, puis câblage Rivet (extension « escorte » à décider, CARAVANE §12).

## Décisions de DA et de lore (Ocre)
_À compléter à chaque lot._
- Jalon 1 : voir [PILOTE.md §13](PILOTE.md#13-décisions-de-da-et-de-lore-à-valider-par-valentin) (bande sans faction, noms nouveaux, lien avec Anselme, biome désert ; depuis l'alignement sur ARCHI : lit au niveau 0 rendu par le sol et les berges, sols `g_rc_*` propres au pilote, Tuerto avec son propre sprite, Quilla en deux poses).
- Sprites (PILOTE §13 points 12-13) : pick-up **rouge délavé** au lieu de gris-bleu (l'appât se lit en premier, palette chaude conservée) ; plancher de l'épave à **1,3 m** au lieu de 2,0 (Morsa `y: 1.3` ; ARCHI.md cite encore 2,0) ; bidons de la bâche restés bleus (lien Dusk-Town) ; Don Trapo produit comme PNJ `gen_rc_trapo` plutôt que décor.
- Jalon 2, caravane : voir [CARAVANE.md §13](CARAVANE.md#13-décisions-de-da-et-de-lore-à-signaler-à-valentin). **À valider en priorité** : une filière de passeurs qui cache des mutants dans une fausse citerne (réseau nouveau, ou cas isolé) ; c'est la caravane qu'attend Ileana (Dusk-Town Q1) et où Teo veut une place, avec drapeaux de monde `monde_remedios_*` pour Dusk-Town plus tard ; Lena, mutante en route vers la Sous-Ville (apparence mutante proposée : plaques sombres sur les avant-bras). Aussi : relais UFSA aux traits gravés, caravane sans faction, circuit Novo Córdoba → Dusk-Town, prix de piste (eau 6 $), même soleil que le pilote, accents garance / ocre jaune / olive, clins d'œil au pilote (péage de Quilla, carnet du chauffeur, cric d'Anselme).

## Questions ouvertes pour Valentin
- La consigne reçue s'arrête au milieu de l'étape 5 (« retour au voyage ») : il manque la suite.
