# Rencontre pilote : « L'appât de la piste » (embuscade de pillards)

Jalon 1 du chantier (voir [README.md](README.md)). Création : Ocre, 17/11/2026 (heure de Paris).

> **Format provisoire, à aligner sur `docs/rencontres/ARCHI.md` (Rivet).** La note d'architecture n'était pas publiée au moment de la rédaction. Le plan coté, les champs et les identifiants ci-dessous sont en mètres et restent simples ; ils seront recalés sur ce que le moteur sait charger (taille de scène, sorties, PNJ, butin, adversaires). Aucun sprite n'est produit tant que ce format n'a pas tenu en jeu.

Planche concept (MAQUETTE, pas une capture) : `/workspace/nml-shots/rencontres/pilote_concept.png` sur la machine d'Ocre (vue iso d'ambiance + vue de dessus cotée). Le plan coté de ce document fait foi ; la vue iso est une ambiance.

## 1. Fiche
| Champ | Valeur |
|---|---|
| id | `embuscade_piste` [proposition] |
| Famille | Pillards et embuscades |
| Terrains | `piste` (p = 0,05) et `desert` (p = 0,10) de `src/data/nml.js` ; taux inchangés |
| Biome | désert (`desert` du manifest) |
| Cases de référence | la piste Dusk-Town → Steel-Megalopolis : I05 (8,4), K06 (10,5), L06 (11,5). Pour le test : forcée par le mode DEV |
| Moment | jour (la variante de nuit viendra après le jalon 1) |
| Emprise | 30 × 24 m (x vers l'est, z vers le sud, origine au coin nord-ouest), un seul niveau de marche |
| Faction | aucune : bande indépendante (voir §11) |
| Rejouable | non : une fois réglée, la case ne relance pas cette rencontre (idée reprise de la maquette v0.13, pas son code) |

## 2. La situation
Une bande de quatre pillards tient la piste entre Dusk-Town et la douane ouest. Il y a trois jours, ils ont arrêté un pick-up qui livrait de l'eau filtrée à Dusk-Town. Le chauffeur est reparti à pied ; les bidons et le pick-up sont restés. La bande a crevé les pneus, ouvert le capot et assis contre la portière un mannequin de chiffons coiffé d'un chapeau de paille, « Don Trapo ». De loin, on croit voir un chauffeur blessé. Les voyageurs s'arrêtent, par bon cœur ou par appétit. La cheffe, Quilla, sort alors de l'ombre des rochers et annonce le péage, pendant que les deux guetteurs couvrent la piste depuis le talus et depuis l'épave, et que le cogneur ferme le lit asséché.

## 3. Ce que le décor raconte (et les traces du piège)
Tout ce qui suit est examinable (bouton Examiner, ou survol à 4 m sur mobile). Les traces marquées ★ révèlent un guetteur caché et posent un drapeau qui débloque des répliques.

| Où (x ; z) | Ce qu'on voit | Texte d'examen | Effet |
|---|---|---|---|
| Pick-up (12-17,2 ; 11-13,2) | capot ouvert, pneus lacérés, bouchon de réservoir arraché | « Les quatre pneus sont tranchés net, au couteau. Capot ouvert, mais pas un outil par terre : personne n'a essayé de réparer. » | — |
| Don Trapo (13,5 ; 13,7) | silhouette affalée contre la portière sud | de loin : « Un homme affalé contre la portière. Il ne bouge pas. » ; à 2 m : « Des chiffons bourrés de paille, une chemise cousue sur un sac. Le chapeau est vissé sur un manche à balai. » | `flag:emb_mannequin_vu` |
| Caisses C1, C3 | caisses éventrées, couvercles arrachés | « Vides. Le sable a déjà fait une petite dune au fond : pillées depuis des jours, pas aujourd'hui. » | — |
| ★ Traces de pas (11-12,5 ; 6-9,6) | empreintes qui montent dans la pente | « Des empreintes fraîches montent vers la crête. Aucune ne redescend. » (Observation 4 pour la seconde phrase) | `flag:emb_vu_talus` |
| ★ Miroir (20 ; 3,2) | petit miroir de poche sur un piquet, un éclat de soleil | « Un éclat sur la crête, toujours au même endroit. Un miroir, posé pour faire signe. » | `flag:emb_vu_talus` |
| ★ Traînées (18,4 ; 15,9) → (26,6 ; 21,5) | sillons de caisses tirées vers le lit | « Quelque chose de lourd a été traîné vers le lit asséché. Les sillons passent au pied de l'épave. » | `flag:emb_vu_epave` |
| ★ Épave (17-26 ; 18-20,8) | camion bâché du Service, ensablé, pneus crevés | « Un camion du Service, ensablé depuis des années. Sur le plateau, des mégots récents, et une forme qui ne bouge pas assez pour être un sac. » (Observation 5) | `flag:emb_vu_epave` |
| Fil à boîtes (x 21 ; z 10-16) | fil tendu au ras du sol, quatre boîtes de conserve | « Un fil de fer tendu en travers de la piste, quatre boîtes de conserve dessus. Un piège à bruit. » (Observation 3 pour le voir avant de marcher dessus) | `flag:emb_vu_fil` (on l'enjambe sans bruit) |
| Panneau (3,5 ; 9,3) | vieux panneau routier UFSA, criblé | texte affiché par le code : « Le panneau a perdu ses lettres. Il reste les trous des balles, en forme de flèche vers l'est. » | — |
| Tas de pneus (5-7,5 ; 19-21) | pneus et gravats dans le lit | « Un tas de pneus. Derrière, quelqu'un a tassé le sable pour s'asseoir. » | `flag:emb_vu_lit` |

Lecture à 1280 et en 390 : les silhouettes de Quilla (assise à l'ombre) et de Don Trapo sont lisibles dès l'arrivée ; Pibe, Morsa et Tuerto ne le sont pas. Le miroir est la seule « lumière » de la scène : un éclat ponctuel posé sur un objet visible, jamais un halo seul.

## 4. Plan coté (provisoire)
Vue de dessus, 1 caractère = 1 m. Légende : `=` piste (6 m), `t` talus nord (pente solide z 5-8,5, crête praticable z 0-5 à +2,5 m), `/` sente vers la crête, `R` rochers, `~` lit asséché (z 17-24, visuel à -0,8 m, même niveau de marche), `P` pick-up, `c` caisses, `|` fil à boîtes, `E` épave, `B` bâche (cache), `O` pneus, `.` traces de pas, `,` bas-côté sableux, `S` panneau, `m` miroir, `@` apparition, `d` Don Trapo, `1` Quilla, `2` Pibe, `3` Morsa, `4` Tuerto. `O>` sortie ouest, `<E` sortie est route, `<L` sortie est lit.

```text
      0         1         2         
      012345678901234567890123456789
  0   ,,,,,ttttttttttttttttttttttttt
  1   ,,,,,ttttttttttttttttttttttRRR
  2   ,,,,,ttttttttttRRRttttRRRttRRR
  3   ,,///tttttttttttttttmtRRRttttt
  4   ,,///ttttttttttt2ttttttttttttt
  5   ,,///ttttttttttttttttttttttttt
  6   ,,///ttttttt.ttttttttttttttttt
  7   ,,///ttttttt.ttttttttttttttttt
  8   ,,///,,,,,,,.,,,,,,,,,,,,,,,,,
  9   ,,/S/,,,,,,.,,,,,,,,,,,,1,,,,,
 10 O>=====================|========<E
 11 O>============PPPPP====|========<E
 12 O>============PPPPP====|========<E
 13 O>=@===========d=======|========<E
 14 O>=====================|========<E
 15 O>========cc========c==|========<E
 16   ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
 17   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<L
 18   ~~~~~~~~~~~~~~~~~EEEEEEEEE~~~~<L
 19   ~~~~~OO~~~~~~~~~~EEEE3EEEE~~~~<L
 20   ~~~~~OO~~~~~~~~~~EEEEEEEEEBBBB<L
 21   ~~~~~~~~~~~~~~~~~~~~~~~~~~BBBB
 22   ~~~~~~4~~~~~~~~~~~~~~~~~~~BBBB
 23   ~~~~~~~~~~~~~~~~~~~~~~~~~~BBBB
```

### Éléments et solides
| id | Élément | x0-x1 | z0-z1 | Haut. (m) | Solide | Couverture combat |
|---|---|---|---|---|---|---|
| sol_piste | piste damée, ornières | 0-30 | 10-16 | 0 | non | 0 |
| sol_sable | bas-côtés | 0-30 | 8,5-10 et 16-17 | 0 | non | 0 |
| talus | pente du talus | 5-30 | 5-8,5 | 0 → 2,5 | oui (sauf la sente) | 2 pour qui est derrière la crête |
| crete | plateau de crête | 5-30 | 0-5 | 2,5 (rendu) | non | — |
| sente | rampe ouest vers la crête | 2-5 | 3-10 | 0 → 2,5 | non | 0 |
| rochers ×3 | blocs de crête | 15-18 / 22-25 / 27-30 | 2-3,5 / 2,5-4 / 1,5-3 | 1,6 | oui | 1 |
| pickup | pick-up appât | 12-17,2 | 11-13,2 | 2,0 | oui | 1 |
| caisses ×3 | C1, C2 (double fond), C3 | 8,5-9,7 / 10,2-11,4 / 17,8-19 | 14,8-15,6 / 15,6-16,4 / 15-15,8 | 0,7 | oui | 1 |
| fil | fil à boîtes | 20,9-21,1 | 10-16 | 0,3 | non (déclencheur T2) | 0 |
| lit | lit asséché | 0-30 | 17-24 | -0,8 (rendu) | non | 0 |
| epave | camion du Service ensablé | 17-26 | 18-20,8 | 3,0 (plateau à 2,0) | oui | 2 |
| pneus | tas de pneus et gravats | 5-7,5 | 19-21 | 1,2 | oui | 1 |
| bache | bâche tendue, cache | 26,5-30 | 20,5-24 | 1,6 | oui (bords), fouille par le côté ouest | 1 |
| panneau | panneau UFSA | 3,4-3,6 | 9,2-9,4 | 3,0 | oui | 0 |
| miroir | miroir sur piquet | 20 ; 3,2 | — | 1,2 au-dessus de la crête | non | — |

Le moteur n'a qu'un niveau de marche par point (voir `src/core/niveaux.js`) : la crête et le plateau de l'épave sont des hauteurs de rendu. Le talus est solide sauf par la sente ; le plateau de l'épave n'est pas praticable pour le joueur (Morsa y est posé, `y = 2,0`).

### Apparition, sorties, déclencheurs
| id | Type | Position (m) | Rôle |
|---|---|---|---|
| spawn | apparition | (1,5 ; 13), regard vers l'est | on arrive par l'ouest, la piste devant soi ; Don Trapo et Quilla sont lisibles, le reste non |
| S_O | sortie | x = 0, z 10-16 | demi-tour : retour à la carte, voyage en halte sur la case, itinéraire conservé |
| S_E_route | sortie | x = 30, z 10-16 | reprise du voyage. **Gardée** : tant que l'embuscade n'est pas réglée (péage, bluff, intimidation, victoire), franchir x = 23 sur la piste lance Quilla (si déjà parlé : `combat:embuscade_piste`) |
| S_E_lit | sortie | x = 30, z 17-20,5 | reprise du voyage par le contournement |
| T1 | déclencheur | x ≥ 10, z 9-17 | Quilla se lève, marche jusqu'à (19 ; 12) et parle (§6.1, nœud `start`) |
| T2 | déclencheur | fil, x 20,9-21,1 | si `!emb_vu_fil` : bruit de boîtes, Pibe et Morsa se montrent, Quilla parle en nœud `alerte` (péage +5 $) |
| T3 | déclencheur | x 4-10, z 17-24 | Tuerto se lève (§6.4) |
| fuite | combat | bords de la zone 19 × 19 | issue « fuite » : retour à la carte comme S_O |

### Zone de combat
Ancre (18 ; 13), zone 19 × 19 (x 8,5-27,5, z 3,5-22,5), entièrement dans l'emprise : aucune case dans le vide.

## 5. Mise en scène échelonnée (découverte progressive)
1. **Arrivée** (x 1,5) : piste vide, pick-up à 11 m, « chauffeur » affalé, caisses éventrées. Au loin, une silhouette assise à l'ombre des rochers (Quilla), qu'on prend pour un autre voyageur. Rien n'impose d'avancer.
2. **Approche** (T1) : Quilla se lève et vient au-devant. Elle reste à 6 m.
3. **Les guetteurs** : Pibe (crête) et Morsa (épave) restent cachés tant qu'aucune trace ★ n'a été lue, qu'on n'est pas à moins de 6 m d'eux, que le fil n'a pas sonné ou que le combat n'a pas commencé.
4. **Le cogneur** : Tuerto reste derrière les pneus jusqu'à T3 ou jusqu'au tour 2 du combat (renfort).

## 6. PNJ : fiches et dialogues
Format des dialogues : celui de `src/data/dialogues_*.js` (nœuds `text` + `options` ; `next`, `action` avec `pay:`, `take:`, `give:`, `gain:`, `flag:`, `combat:` ; `test`, `pass`, `fail`, `partial`/`partialAt`, `opposed` ; `if`). Les identifiants sont des propositions.

### 6.1 Quilla, cheffe de la bande
- Femme d'une cinquantaine d'années, lunettes de soudeur relevées sur le front, poncho couleur sable, pistolet à la ceinture. Ancienne mécanicienne de convois. Polie, lasse, jamais pressée. Elle tient au péage plus qu'au sang : un mort ne repasse pas payer.
- Stats proposées : PV 18, PA 7, initiative 7, `pistolet`, mêlée 40 %, armes 55 %, Volonté 6.
- Sprite : `gen_rc_quilla` (à produire) + portrait.

```text
start   « Doucement, voyageur. Tu ne poses rien, tu ne lèves rien. Tu marches sur ma route. »
  - « Ta route ? »                                             → route
  - « Je veux juste passer. »                                  → peage
  - [si emb_mannequin_vu] « Ton chauffeur est en chiffons. »   → trapo
  - [si !emb_mannequin_vu] « Le chauffeur du pick-up a besoin d'aide. » → trapo_naif
  - [si emb_vu_talus & emb_vu_epave] « Le gamin sur la crête, celui sur l'épave. Ça fait deux. Il t'en reste combien ? » → compte
  - « Je fais demi-tour. »                                     → demi
  - [Attaquer] « Dégaine. »                     action combat:embuscade_piste

alerte  (T2, fil déclenché) « Tu as marché sur la sonnette. Ça arrive. Mais maintenant, tout le monde est réveillé, et le prix aussi : vingt. »
  - suite des options de peage, péage à 20 $

route   « Celle-là, oui. La poussière est à tout le monde. La piste est à qui la tient, et aujourd'hui c'est moi. Péage : quinze dollars. Ou deux bidons d'eau, je ne suis pas difficile. »
  → peage

trapo_naif « Il a surtout besoin qu'on le laisse tranquille. Il s'appelle Don Trapo. Il ne boit pas, il ne parle pas, et il arrête tout le monde. Le meilleur employé que j'aie jamais eu. » → peage
trapo   « Bien vu. Ça te fait un point. Les gens ont bon cœur, c'est ça qui les perd. Toi, tu es juste curieux. » → peage

peage   « Quinze dollars, et la piste est à toi jusqu'à la douane. »
  - « Voilà quinze dollars. »             action pay:15;flag:emb_regle;flag:emb_paye → paye
  - [si inv:water>=2] « Deux bidons d'eau. »  action take:water;take:water;flag:emb_regle;flag:emb_paye → paye
  - « Quinze, pour un bout de sable ? Parlons-en. »   test parole:5, partialAt 4 → pass neg_ok, partial neg_moitie, fail neg_rate
  - « Un convoi du Service roule une heure derrière moi. »   test parole:6 → pass bluff_ok, fail bluff_rate
  - [si inv:plaque>=1] Montrer la plaque de camion du Service. « Ce convoi-là. »   test parole:4 → pass bluff_ok, fail bluff_rate
  - « Recule. Maintenant. »                test intimider:6, opposed → pass peur_ok, fail peur_rate
  - « Non. »                               → refus

paye    « Voilà un voyageur qui veut vieillir. Passe. Et ne touche pas au pick-up : il travaille. »
  - « D'où il vient, ce pick-up ? »        → appat
  - « Je passe. »                          → end

appat   « De Dusk-Town, avec douze bidons et un gars qui roulait trop vite. Le gars est reparti à pied, sans ses bidons. Le pick-up, je l'ai gardé. Un camion en panne, ça arrête tout le monde. »
  - « Et le gars ? »   → appat2
  - « Je vois. »       → end
appat2  « Vivant. Je ne suis pas le Service. Moi, je ne ramasse que ce qui roule. » → end

neg_ok     « Huit. Parce que tu parles bien et que la journée est longue. »
  - « Huit, d'accord. »  action pay:8;flag:emb_regle;flag:emb_paye → paye
  - « Toujours trop. »   → refus
neg_moitie « Douze. Et je n'ai pas envie de compter plus loin. »
  - « Douze. »           action pay:12;flag:emb_regle;flag:emb_paye → paye
  - « Non. »             → refus
neg_rate   « Tu parles trop. Vingt, maintenant. »
  - « Vingt… Tiens. »    action pay:20;flag:emb_regle;flag:emb_paye → paye
  - « Non. »             → refus

bluff_ok   (Elle lève les yeux vers le miroir.) « Pibe ! Tu vois quelque chose ? » — Pibe, de la crête : « De la poussière, Quilla ! » — « De la poussière. Ça peut être n'importe quoi. Passe. Vite. »
  action flag:emb_regle;flag:emb_bluff → end
bluff_rate « Le Service, ça s'entend à dix kilomètres. Là, je n'entends que toi. Le prix vient de monter : vingt. » → neg_rate

peur_ok    (Elle recule d'un pas.) « Tu as les yeux de quelqu'un qui a déjà enterré du monde. Passe. On n'a rien vu, tu n'as rien vu. »
  action flag:emb_regle;flag:emb_intimide → end
peur_rate  « Ah. Tu veux jouer. Pibe ! » action combat:embuscade_piste

refus      « Comme tu veux. Le désert est plein de gens qui ont dit non. » 
  - « J'ai changé d'avis. »  → peage
  - [Attaquer]               action combat:embuscade_piste
  - « Je fais demi-tour. »   → demi

compte     (Un silence.) « Personne ne compte jamais jusqu'à deux. »
  - « Tout le monde repart entier. Je passe, gratis. »    test parole:4 → pass compte_ok, fail peage
  - « Et c'est vous qui payez. Dix dollars, et vous changez de route. »   test intimider:5, opposed → pass racket_ok, fail peur_rate
compte_ok  « Gratis. Ne le répète pas, ça me ferait une mauvaise réputation. » action flag:emb_regle;flag:emb_bluff → end
racket_ok  (Elle jette quelques billets dans le sable.) « Garde-les. Et ne reviens pas sur cette piste. » action gain:10;flag:emb_regle;flag:emb_racket → end

demi       « Sage. La piste sera encore là demain. Moi aussi. » action flag:emb_demi → end   (le joueur repart par S_O)
```

### 6.2 Pibe, guetteur de la crête
- Seize ans « presque », fusil trop grand pour lui, foulard sur le nez. Il panique vite.
- Stats : PV 10, PA 6, initiative 8, `fusil`, armes 35 %, Volonté 3, `fuitTour: 2`.
- Sprite : `gen_rc_pibe` (à produire) + portrait. Position (16,5 ; 4,2), rendu à +2,5 m, derrière le rocher R1, regard au sud.
- Parlable seulement si on l'atteint par la sente avant le combat.

```text
start   « Bouge pas ! Bouge pas, je… je tire ! » (Le canon tremble.)
  - « Tu as quel âge ? »                         → age
  - « Lâche ce fusil et rentre chez toi. »       test intimider:3, opposed → pass pibe_fuit, fail crie
  - « Cinq dollars, et tu n'as rien vu. »        action pay:5;flag:emb_pibe_achete → achete
  - Le désarmer d'un coup sec.                   test melee:4 → pass pibe_ko, fail crie
age     « Seize. Presque. Quilla dit que l'âge, ça ne compte pas sur la piste. » → start
pibe_fuit « Je… d'accord. D'accord ! » (Il lâche le fusil et dévale la sente.) action give:fusil;flag:emb_pibe_parti → end
achete  « J'ai rien vu. J'ai jamais rien vu, moi. » → end
pibe_ko (Il s'assoit dans la poussière, le souffle coupé.) action give:fusil;flag:emb_pibe_ko → end
crie    « QUILLA ! » action combat:embuscade_piste
```

### 6.3 Morsa, guetteur de l'épave
- La quarantaine, lourd, moustache tombante, chapeau sur les yeux. Couché sur le plateau du camion, fusil sur le ventre ; il somnole dans la chaleur, le regard tourné vers la piste (dos au lit).
- Stats : PV 14, PA 6, initiative 5, `fusil`, armes 50 %, Volonté 5.
- Sprite : `gen_rc_morsa` (à produire) + portrait. Position (21,5 ; 19,4), rendu à +2,0 m.
- Abordable depuis le lit (côté sud de l'épave), avant le combat.

```text
start   (Morsa ronfle doucement, le fusil sur le ventre.)
  - Prendre son fusil sans le réveiller.   test discretion:5 → pass vol_ok, fail reveil
  - Le réveiller doucement.                → reveil
  - L'assommer.                            test melee:3 → pass morsa_ko, fail reveil
vol_ok  (Le fusil glisse. Morsa grogne et se retourne.) action give:fusil;flag:emb_morsa_desarme → end
morsa_ko action flag:emb_morsa_ko → end
reveil  « Mmh. Si tu es là, c'est que le gamin dort aussi. »
  - « Combien Quilla te paie ? »           → paie
  - [Attaquer]                             action combat:embuscade_piste
paie    « Une part sur quatre. Une part de rien, ça fait rien. »
  - « Je double. Dix dollars, et tu regardes la piste. »  action pay:10;flag:emb_morsa_achete → achete
  - « Dommage pour toi. »                  → end
achete « La piste. Je regarde la piste. Elle est très jolie aujourd'hui. » → end
```

### 6.4 Tuerto, le cogneur du lit
- Borgne, bras épais, barre de fer. C'est le profil du rôdeur existant.
- Stats : celles du `rodeur` de `src/data/combat.js` (PV 14, PA 6, initiative 6, `barre`, mêlée 45 %, armes 20 %), sans `fuitTour`.
- Sprite : `gen_rodeur` réutilisé (aucun sprite neuf). Position (6 ; 22), caché derrière les pneus.

```text
start   (T3) « Tiens. Le lit, c'est aussi ma route. »
  - « Je ne fais que passer. »             → retour
  - « Un dollar par pas, et tu me montres le chemin ? »   test troc:5 → pass guide, fail retour
  - [Attaquer]                             action combat:embuscade_piste
retour  « Alors passe par la piste, comme tout le monde. Quilla t'attend. » (Il te raccompagne jusqu'à la berge, en (10 ; 16,5).) action flag:emb_tuerto_vu → end
guide   « Six dollars. Et tu ne m'as jamais vu. » action pay:6;flag:emb_tuerto_achete → end   (il se rassoit ; le lit est libre)
```

## 7. Manières d'agir et conséquences
| Approche | Comment | Conséquence |
|---|---|---|
| Contourner par le lit | entrer dans le lit après le tas de pneus (x ≥ 10), longer z 21-23 sous l'épave : test Discrétion 4 (Morsa somnole dos au lit), Discrétion 6 si `emb_vu_fil` a sonné | sortie S_E_lit, rien payé ; échec = Morsa crie, combat |
| Contourner par la crête | sente, crête : neutraliser ou acheter Pibe, redescendre derrière Quilla | Quilla seule devant un joueur armé : option intimider à 4 au lieu de 6 [proposition] |
| Payer | 15 $ ou 2 eaux (8 à 20 $ selon la négociation) | passage, `emb_paye` ; Quilla raconte l'appât |
| Bluffer | « convoi du Service », mieux avec la plaque | passage gratuit, `emb_bluff` |
| Intimider | Charisme ou Force contre Volonté 6 | passage gratuit, `emb_intimide` ; échec = combat |
| Retourner le piège | avoir repéré les deux guetteurs (`emb_vu_talus` + `emb_vu_epave`) | passage gratuit, ou racket de la bande (+10 $) |
| Combattre | à tout moment, ou après un échec | voir §8 |
| Voler | la cache sous la bâche, depuis le lit par Discrétion 6 avant que la bande soit réglée, ou librement après une victoire ou un racket ; le fusil de Morsa pendant qu'il somnole | butin de la cache ; échec = combat |
| Partir | S_O (demi-tour) à tout moment avant le combat ; fuite pendant | voyage en halte sur la case ; la bande reste |

Drapeaux posés : `emb_regle`, `emb_paye`, `emb_bluff`, `emb_intimide`, `emb_racket`, `emb_demi`, `emb_vu_*`, `emb_pibe_*`, `emb_morsa_*`, `emb_tuerto_*`, `combat_embuscade_piste_<issue>` (posé par le moteur).

## 8. Combat optionnel
Reprise du système existant (`src/core/combat.js`, `src/data/combat.js`) : une entrée `ENCOUNTERS.embuscade_piste` au format du `rodeur`. Positions relatives à l'ancre (18 ; 13), en cases de 1 m.

| id | Sprite | dx ; dz | Position | PV | PA | Init. | Arme | Mêlée / armes | Particularité |
|---|---|---|---|---|---|---|---|---|---|
| quilla | gen_rc_quilla | 1 ; -1 | (19 ; 12) près du pick-up | 18 | 7 | 7 | pistolet | 40 / 55 | se rend sous 25 % de PV (reddition de la bande) |
| pibe | gen_rc_pibe | -2 ; -9 | (16 ; 4) crête, derrière R1 | 10 | 6 | 8 | fusil | 10 / 35 | `fuitTour: 2` ; absent si `emb_pibe_parti`/`_ko` ; ne tire pas si `emb_pibe_achete` |
| morsa | gen_rc_morsa | 4 ; 6 | (22 ; 19) plateau de l'épave | 14 | 6 | 5 | fusil | 30 / 50 | mains nues si `emb_morsa_desarme` ; absent si `_ko` ; ne tire pas si `_achete` |
| tuerto | gen_rodeur | -8 ; 7 | (10 ; 20) entre au tour 2 depuis les pneus | 14 | 6 | 6 | barre | 45 / 20 | renfort tour 2 (comme la douane), absent si `emb_tuerto_achete` |

Couverture : pick-up, caisses, rochers, pneus = 1 ; épave, crête vue d'en bas = 2.

Issues (format `issues` existant, jamais de mort au lot C1) :
- **victoire** : la bande s'enfuit vers l'est par le lit ; la cache et le corps du pick-up sont fouillables. `flag:emb_regle;flag:emb_vaincue`. Texte : « Quilla crache dans le sable. "Garde la piste, alors. Elle ne te gardera pas." Ils s'en vont par le lit. »
- **fuite** : le joueur sort par un bord de la zone ; retour à la carte, halte sur la case. Texte : « Tu cours jusqu'à ne plus entendre les boîtes de conserve. »
- **reddition** : le joueur paie 20 $ (ou tout ce qu'il a) ; `emb_regle`. Texte : « Tu jettes les billets dans le sable. Quilla les compte sans se presser. »
- **defaite** : 1 PV, on se réveille à l'apparition, délesté de 20 $ au plus et d'une eau ; `emb_regle`. Texte : « Le ciel. Le sable. Don Trapo, qui te regarde. »

## 9. Objets à fouiller (butin)
Objets existants (`ITEMS`, armes du combat) sauf mention.

| Où | Condition | Contenu |
|---|---|---|
| Boîte à gants du pick-up (côté ouest du pick-up) | libre | 4 $ (`gain:4`) + **carnet du chauffeur** (`carnet_chauffeur`, objet de lore, [proposition]) : « Livraison Anselme, Dusk-Town : 12 bidons filtrés. Ne pas s'arrêter avant la douane. Ne s'arrêter pour personne. » |
| Caisse C2 (double fond) | Observation 4 ou trait Œil de pillard | 1 `ration`, 1 `water` |
| Caisses C1, C3 | libre | vides (texte d'examen) |
| Cache sous la bâche | bande réglée par victoire, `emb_racket`, ou Discrétion 6 depuis le lit (échec = combat) | 3 `water` (les bidons volés), 1 `ration`, 22 $, 1 `poignard` |
| Plateau de l'épave (par le flanc sud) | Morsa absent ou neutralisé | son `fusil` s'il ne l'a plus pris, gourde vide, mégots (texte) |
| Réservoir du pick-up | libre | vide : « Percé. Même le sable n'y reste pas. » |

## 10. Clés d'assets à produire (_3q) et réutilisations
Rien n'est produit avant la validation du format. Préfixe proposé `rc_` (rencontres), `rc_ds_` pour les modules du désert réutilisables, `rc_emb_` pour ceux propres à l'embuscade. Ancre et échelle comme les autres lots : sprite à l'échelle 1, 50 px/m, ancre au coin avant sud-est.

| Clé | Rôle | Emprise L × P × H (m) | Notes |
|---|---|---|---|
| `g_rc_piste` | sol piste damée, ornières | tuile 4 × 4 | + variante `_b` (ornière croisée) ; ocre clair |
| `g_rc_sable` | sol sable des bas-côtés et du talus | tuile 4 × 4 | + `_b` (cailloux, touffes sèches) ; jamais une dalle vide |
| `g_rc_lit` | sol du lit asséché, galets et craquelures | tuile 4 × 4 | plus sombre et plus froid que la piste |
| `rc_ds_talus_pente_3q` | pente du talus, module | 10 × 3,5 × 2,5 | ×3 en x (5-30) ; éboulis, racines mortes |
| `rc_ds_talus_crete_3q` | plateau de crête | 10 × 5 × 0,3 | sur la pente, mêmes x |
| `rc_ds_sente_3q` | rampe vers la crête | 3 × 7 × 2,5 | |
| `rc_ds_rochers_3q` | blocs de crête | 3 × 1,5 × 1,6 | + `_b` (3 × 1,5) |
| `rc_ds_berge_3q` | rebord du lit (visuel) | 10 × 1 × 0,8 | ×3 |
| `rc_emb_pickup_appat_3q` | pick-up, capot ouvert, pneus lacérés | 5,2 × 2,2 × 2,0 | gris-bleu délavé et rouille ; boîte à gants ouverte côté ouest |
| `rc_emb_trapo_3q` | Don Trapo, mannequin | 0,8 × 0,6 × 1,3 | assis contre la portière sud, chapeau de paille |
| `rc_emb_caisses_eventrees_3q` | caisse ouverte pleine de sable | 1,2 × 0,8 × 0,7 | + `_b` (couvercle à côté) ; la C2 utilise `_b` |
| `rc_emb_fil_boites_3q` | fil tendu et boîtes de conserve | 0,2 × 6 × 0,3 | piquets aux deux bouts |
| `rc_emb_miroir_3q` + `_neon` | miroir de poche sur piquet | 0,3 × 0,3 × 1,2 | `_neon` = un seul éclat sur le verre, pas de halo au sol |
| `rc_emb_epave_service_3q` | camion bâché du Service ensablé | 9 × 2,8 × 3,0 | ridelles cassées, pneus crevés ; plateau à 2,0 m |
| `rc_emb_bache_cache_3q` | bâche tendue, sacs, bidons | 3,5 × 3,5 × 1,6 | bidons bleus de Dusk-Town (lien avec le carnet) |
| `rc_emb_traces_3q` | décalques au sol : empreintes, traînées, mégots | 2 × 1 | calque sol, plusieurs poses |
| `rc_ds_panneau_ufsa_3q` | panneau routier UFSA criblé | 0,6 × 0,2 × 3,0 | sans texte lisible |
| `gen_rc_quilla` | PNJ + portrait `portrait-gen_rc_quilla` | 1,8 m | lunettes de soudeur, poncho sable |
| `gen_rc_pibe` | PNJ + portrait | 1,65 m | fusil trop grand, foulard |
| `gen_rc_morsa` | PNJ couché + debout + portrait | 1,8 m | pose couchée pour le plateau |

Réutilisé tel quel : `gen_rodeur` (Tuerto), `assets/reused/tires.webp` et `rubble.webp` (tas du lit), `bush.webp` (touffes), `barrel.webp` (bidon près de la bâche), `assets/generated/sv_pneus.webp` en secours. Ces modules `rc_ds_*` et `g_rc_*` serviront de base au biome désert des jalons 2 et 3.

## 11. Identité du biome désert (pour cette scène)
- **Palette** : ocre et sable ambre (`#d9b47a`, `#c9a46a`), rouille, bois blanchi, gris-bleu délavé des tôles ; ombres brun chaud. L'ambre reste la couleur des No Man's Land (comme la carte NML), en opposition au bleu acier de Steel.
- **Lumière** : soleil haut, ombres courtes, aucune source artificielle. Le seul point brillant est le miroir, sur un objet visible. Proposition de réglage : `bg '#1a1510'`, `hemi ['#f0dcb0', '#3a2a18', 1.3]`, `sun ['#ffd890', 0.9]`, `tint '#e8d0a0'`.
- **Sol** : jamais uni. Ornières, cailloux, touffes sèches et décalques de traces cassent les tuiles ; le lit est plus froid et plus sombre que la piste.
- **À éviter** : terrain plat avec trois ennemis au milieu, halo sans source, dalles vides, violet et cyan (réservés à Steel), végétation verte.

## 12. Points d'accroche pour Rivet
1. `EVENEMENTS_ROUTE` : une entrée `{ id: 'embuscade_piste', terrains: ['piste', 'desert'], si: etat => !etat.flags?.emb_regle_<case>, poids: 1 }` [proposition] ; taux de `TERRAINS` inchangés.
2. Scène construite à la demande (§4) : sol, éléments, solides, apparition, sorties (S_O = halte, S_E_* = reprise), déclencheurs T1-T3.
3. Visibilité différée : `cache: true` sur Pibe, Morsa, Tuerto, levée par drapeau (`emb_vu_*`), par distance (< 6 m), par T2/T3 ou au début du combat.
4. Hauteurs de rendu sans niveau de marche : crête +2,5, plateau de l'épave +2,0, lit -0,8 (optionnel, sinon 0).
5. Sortie est gardée tant que `!emb_regle` (franchir x = 23 sur la piste).
6. Combat : `ENCOUNTERS.embuscade_piste` (§8), ancre (18 ; 13) par scène de rencontre, renfort au tour 2, effets des drapeaux sur la liste des ennemis.
7. Persistance par case : la rencontre réglée ne se relance pas ; la cache vidée reste vide.
8. Tests DEV : « forcer une rencontre » `embuscade_piste` ; scénarios payer, bluffer, intimider, contourner, combattre (4 issues), fouiller.
9. Nouvel objet proposé : `carnet_chauffeur` (lisible, sans valeur marchande).

## 13. Décisions de DA et de lore (à valider par Valentin)
Rien n'est imposé ; tout est [proposition].
1. **Faction : aucune.** La bande de Quilla est indépendante. Je n'ai pas pris les Los Invictos (canon, mais présentés à Dusk-Town comme des isolés « sans importance », et liés au Ranch Liberté par Ileana) ni les Rakkens (canon, mais leur nature n'est pas décrite dans nos docs) pour ne pas fixer leur caractère sans toi. À rattacher plus tard si tu le souhaites.
2. **Nouveaux noms** : Quilla, Pibe, Morsa, Tuerto, Don Trapo (le mannequin). Noms à saveur argentine, cohérents avec Buenos Aires et Novo Córdoba.
3. **Lien avec Dusk-Town** : le pick-up livrait de l'eau filtrée à **Anselme** (l'épicier de Dusk-Town, Q1). C'est un crochet de quête possible (rapporter le carnet ou les bidons), hors jalon 1.
4. **Le Service Militarisé sur la piste** : le bluff s'appuie sur le canon (le Service passe par Dusk-Town). L'épave est un ancien camion du Service, sans date précise.
5. **Mutants et humains** : la bande traite toutes les races de la même façon (« ici, tout le monde paie »), à l'inverse de Steel. Pas de réplique propre à la race au jalon 1.
6. **Monnaie** : dollars (canon des No Man's Land). Péage 15 $, à comparer aux prix de Dusk-Town (eau 4 $, repas 6 $).
7. **DA** : désert ambre, lumière du seul soleil, un seul éclat (le miroir) avec sa source visible ; aucun violet ni cyan hors de Steel.
