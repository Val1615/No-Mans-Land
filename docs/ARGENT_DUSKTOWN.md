# Argent à Dusk-Town : branchements pour Développement

Statut : **proposition** (contenu dans `src/data/dialogues_argent.js`, export `DIALOGUES_ARGENT`, plus `ITEMS_ARGENT` et `FERRAILLE`). Aucun fichier de Développement modifié.

## Bilan en dollars
| Source | Gain max | Remarque |
|---|---|---|
| Quête A, l'eau du poste (Sol) | 12 $ | 8 $ si un bidon manque |
| Quête B, l'ardoise d'Ezequiel (Hector) | 15 $ | ou clés revendues 8 $, ou -15 $ et allié |
| Ferraille chez Anselme | 22 $ | 7 points, une fois chacun |
| **Total sans le jeu** | **49 $** | objectif ≥ 40 $ tenu |
| Les Trois Os (Teo) | +15 $ max | plafond pour **toute la partie** |

## Choix des PNJ
- **Quête A : Sol.** Elle tient la citerne des Sables (l'eau, c'est elle) et protège les gens cachés. Destinataires : trois personnes cachées au « poste du bord », derrière les sacs de sable du Transit (`dusk_q2`, x 44,5, z 13,2). Pas de sprite : scène `poste`, sur le modèle de la porte d'acier.
- **Quête B : Hector (créancier), Ezequiel (débiteur).** Ezequiel est le seul « mécanicien » de Dusk-Town (atelier, cric, outils). Hector fait déjà crédit (il nourrit Teo). Ni Nane ni Pic.
- **Ferraille : Anselme.** Commerçant qui « compte devant toi » ; Teo ne fait que vendre des nouvelles.
- **Les Trois Os : Teo.** 17 ans, veut des dollars pour une place sur une caravane ; le refus final au plafond découle de ce désir.

## Actions nouvelles (game.js, fonction `act`)
| Action | Effet |
|---|---|
| `gain:N` | `pl.money += N`, message `+N $` |
| `give:objet[:n]` | ajoute n (défaut 1) objets à `pl.inv` |
| `sell:objet:N` | si l'objet est dans l'inventaire : le retire, `+N $` ; sinon `{ ok:false }` |
| `os:mise:N` | Trois Os : vérifie `money >= N` (sinon nœud `pauvre`), retient la mise, lance 3d6 du joueur, remplit `{joueur}` |
| `os:relance` | relance les 3 dés du joueur (bluff réussi) |
| `os:maison` | lance 3d6 de Teo, remplit `{maison}` |
| `os:resout` | compare et renvoie `next` = `gagne` / `perd` / `egal` (règles plus bas) ; paie la mise si gagné, en respectant le plafond ; renvoie `plafond` si le plafond est atteint |
| `os:perd` | bluff raté : la mise est perdue |
| `os:finpartie` | efface `os_bluff_fait` (un bluff par partie) |
| `hook:combat_rodeur` | **déjà existant** (`hook:`), réservé au futur combat contre le rôdeur |

Le pré-contrôle d'argent de `choose` (regex `^(buy|pay:|heal)`) doit aussi couvrir `os:mise:N`.

## Conditions nouvelles (`cond1`)
- `inv:objet>=N` / `inv:objet<=N` : nombre d'objets dans `pl.inv`. Le regex actuel `^(\w+)(>=...)` ne prend pas le `:` ; ajouter un cas dédié.

## Substitutions dans le texte
- `{joueur}` et `{maison}` dans les nœuds de `trois_os` : afficher les dés et le total, par ex. « 4, 4, 2 (10) ». Stocker dans `state.os = { mise, joueur:[...], maison:[...] }`.

## Branchements de dialogues (options à ajouter aux arbres existants)
- `sol.start` : `{ label: 'Tu as du travail ?', next: 'sol_eau/start', if: '!a_debut' }` ; retour : `{ label: 'Le poste a eu son eau.', next: 'sol_eau/retour', if: 'a_fini' }`.
- `hector.start` : `{ label: 'Du travail pour moi ?', next: 'dette_hector/start', if: '!b_debut' }` ; retours selon drapeaux :
  `b_argent&!b_fini` → `dette_hector/paye` (rend les 15 d'Ezequiel, donne 15 : net +15 $) ; `b_outils&!b_fini` → `dette_hector/outils` ; `b_paye_moi&!b_fini` → `dette_hector/toi`.
- `ezequiel.start` : `{ label: 'Hector m\'envoie. Pour ton ardoise.', next: 'dette_ezequiel/start', if: 'b_debut&!b_regle' }`.
- `anselme.start` : `{ label: 'Tu achètes de la ferraille ?', next: 'ferraille/start' }`.
- `teo.start` : `{ label: 'Tu joues ?', next: 'trois_os/start' }`.
- Fusion : `DIALOGUES = { ...DIALOGUES, ...DIALOGUES_ARGENT }` et `ITEMS = { ...ITEMS, ...ITEMS_ARGENT }`.

## Scènes à déclencher (game.startScene, comme la porte d'acier)
- `rodeur` : première entrée dans `dusk_q1` ou `dusk_q2` avec `a_debut&!a_fini&!a_rodeur_fait`. Test `volonte:6` ; échec = `hurt:5`, fuite = `hurt:3` ; les deux posent `combat_rodeur` + `hook:combat_rodeur`. Céder un bidon pose `a_rodeur_paye`.
- `raid` (facultatif) : Service Militarisé, par ex. au premier passage dans `dusk_q2` si `a_debut&!a_fini&!a_raid_fait` et un tirage. Test `volonte:5` ; échec = `hurt:3` et un bidon perdu.
- `poste` : clic sur les sacs de sable de `dusk_q2` (44,5 ; 13,2) avec `a_debut&!a_fini`. Quatre bidons = 12 $ ; trois = 8 $ (qu'ils aient été perdus ou gardés).
  Garder un bidon : `give:water` + `a_garde` (Sol méfiante). Si le bidon gardé doit soigner, utiliser un objet `consumeNow` avec `heal` (proposé : +4 PV) à la place de `water`.

## Objets (`ITEMS_ARGENT`)
`bidon`, `cles` (8 $ chez Anselme), `piece` (2 $), `circuit` (4 $), `batterie` (6 $).

## Ferraille (`FERRAILLE`)
7 points, posés sur des props existants ; au clic : `give:item`, drapeau `ramasse_<id>`, texte affiché, plus rien ensuite.
| id | lieu | x ; z | objet |
|---|---|---|---|
| f_q1_epave | dusk_q1 | 45,5 ; 16,6 | circuit |
| f_q1_pneus | dusk_q1 | 38,6 ; 23,0 | pièce |
| f_q2_epave | dusk_q2 | 20,5 ; 19,6 | batterie |
| f_q2_caisse | dusk_q2 | 23,2 ; 23,2 | pièce |
| f_q3_caisse | dusk_q3 | 21,6 ; 10,8 | circuit |
| f_q3_pneus | dusk_q3 | 9,8 ; 22,6 | pièce |
| f_q4_charrette | dusk_q4 | 31,8 ; 11,8 | pièce |
Total : 4 × 2 + 2 × 4 + 6 = 22 $.

## Les Trois Os : règles
- Mise : 1, 3 ou 5 $ (boutons proposés ; une mise libre de 1 à 5 est possible).
- Chacun lance 3d6. Un brelan (trois dés égaux) bat tout total ; deux brelans : le plus haut gagne. Sinon le total le plus haut gagne. Égalité : mises rendues.
- Gain = mise (1 pour 1).
- Bluff, une fois par partie (`os_bluff_fait`, effacé par `os:finpartie`) : test `volonte:6`. Réussi : le joueur relance ses trois dés avant le lancer de Teo. Raté : mise perdue.
- **Plafond : 15 $ de gains nets sur toute la partie** (décision de Développement). Compteur `state.osGains` (sauvegardé). Un gain est tronqué pour ne pas dépasser 15. À 15, `os:resout` renvoie `plafond`, qui pose `os_plafond` : Teo refuse ensuite de rejouer.

## Drapeaux
`a_debut`, `a_fini`, `a_garde`, `a_rodeur_fait`, `a_rodeur_paye`, `a_raid_fait`, `combat_rodeur`, `b_debut`, `b_regle`, `b_argent`, `b_outils`, `b_paye_moi`, `b_echec`, `b_fini`, `ezequiel_rancune`, `ezequiel_allie`, `os_bluff_fait`, `os_plafond`, `ramasse_<id>`.

## Doutes
- Le test raté de la quête B (`b_echec`) clôt la négociation sans argent : Hector n'a pas de réplique dédiée (à écrire si voulu).
- Les actions commençant par `flag:` émettent « Journal : piste notée » ; les drapeaux techniques du jeu (`os_*`) pourraient être silencieux.
