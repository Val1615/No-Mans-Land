# Rencontre pilote : « L'appât de la piste » (embuscade de pillards)

Jalon 1 du chantier (voir [README.md](README.md)). Création : Ocre, 17/11/2026 (heure de Paris).

> **Aligné sur [`ARCHI.md`](ARCHI.md) (Rivet, 8576eaa) le 17/11/2026.** Les 7 points de son §6 sont intégrés (lit au niveau 0, guetteur acheté absent du combat, journal par case, pas de trait Œil de pillard, examen au toucher sur mobile, reddition de Quilla = victoire, couverture 1 sur la crête). L'entrée au format de son §4 est au §14. Toutes les positions sont absolues, en mètres, et chaque ennemi est sur une case libre.

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
| Rejouable | non : le gestionnaire tient un journal par case (`region.rencontres['col,row'] = { id, regle }`) ; une case réglée ne relance pas la rencontre. Les drapeaux `emb_*` sont locaux à la scène et **remis à zéro à la sortie** (une autre embuscade, sur une autre case, n'hérite pas des traces vues) |

## 2. La situation
Une bande de quatre pillards tient la piste entre Dusk-Town et la douane ouest. Il y a trois jours, ils ont arrêté un pick-up qui livrait de l'eau filtrée à Dusk-Town. Le chauffeur est reparti à pied ; les bidons et le pick-up sont restés. La bande a crevé les pneus, ouvert le capot et assis contre la portière un mannequin de chiffons coiffé d'un chapeau de paille, « Don Trapo ». De loin, on croit voir un chauffeur blessé. Les voyageurs s'arrêtent, par bon cœur ou par appétit. La cheffe, Quilla, sort alors de l'ombre des rochers et annonce le péage, pendant que les deux guetteurs couvrent la piste depuis le talus et depuis l'épave, et que le cogneur ferme le lit asséché.

## 3. Ce que le décor raconte (et les traces du piège)
Tout ce qui suit est examinable (clic sur ordinateur, appui sur le point d'examen sur mobile, avec un anneau comme les portes ; pas d'examen au survol). Les traces marquées ★ révèlent un guetteur caché et posent un drapeau qui débloque des répliques.

| Où (x ; z) | Ce qu'on voit | Texte d'examen | Effet |
|---|---|---|---|
| Pick-up (12-17,2 ; 11-13,2) | capot ouvert, pneus lacérés, bouchon de réservoir arraché | « Les quatre pneus sont tranchés net, au couteau. Capot ouvert, mais pas un outil par terre : personne n'a essayé de réparer. » | — |
| Don Trapo (13,5 ; 13,7) | silhouette affalée contre la portière sud | de loin : « Un homme affalé contre la portière. Il ne bouge pas. » ; à 2 m : « Des chiffons bourrés de paille, une chemise cousue sur un sac. Le chapeau est vissé sur un manche à balai. » | `flag:emb_mannequin_vu` |
| Caisses C1, C3 | caisses éventrées, couvercles arrachés | « Vides. Le sable a déjà fait une petite dune au fond : pillées depuis des jours, pas aujourd'hui. » | — |
| ★ Traces de pas (11-12,5 ; 6-9,6) | empreintes qui montent dans la pente | « Des empreintes fraîches montent vers la crête. Aucune ne redescend. » (Observation 4 pour la seconde phrase) | `flag:emb_vu_talus` |
| ★ Miroir (20 ; 3,2) | petit miroir de poche sur un piquet, un éclat de soleil | « Un éclat sur la crête, toujours au même endroit. Un miroir, posé pour faire signe. » | `flag:emb_vu_talus` |
| ★ Traînées (18,4 ; 15,9) → (26,6 ; 21,5) | sillons de caisses tirées vers le lit | « Quelque chose de lourd a été traîné vers le lit asséché. Les sillons passent au pied de l'épave. » | `flag:emb_vu_epave` |
| ★ Épave (17-26 ; 18-20,8) | camion bâché du Service, ensablé jusqu'aux essieux, sans roues | « Un camion du Service, ensablé depuis des années. Sur le plateau, des mégots récents, et une forme qui ne bouge pas assez pour être un sac. » (Observation 5) | `flag:emb_vu_epave` |
| Fil à boîtes (x 21 ; z 10-16) | fil tendu au ras du sol, quatre boîtes de conserve | « Un fil de fer tendu en travers de la piste, quatre boîtes de conserve dessus. Un piège à bruit. » (Observation 3 pour le voir avant de marcher dessus) | `flag:emb_vu_fil` (on l'enjambe sans bruit) |
| Panneau (3,5 ; 9,3) | vieux panneau routier UFSA, criblé | texte affiché par le code : « Le panneau a perdu ses lettres. Il reste les trous des balles, en forme de flèche vers l'est. » | — |
| Tas de pneus (5-7,5 ; 19-21) | pneus et gravats dans le lit | « Un tas de pneus. Derrière, quelqu'un a tassé le sable pour s'asseoir. » | `flag:emb_vu_lit` |

Lecture à 1280 et en 390 : les silhouettes de Quilla (assise à l'ombre) et de Don Trapo sont lisibles dès l'arrivée ; Pibe, Morsa et Tuerto ne le sont pas. Le miroir est la seule « lumière » de la scène : un éclat ponctuel posé sur un objet visible, jamais un halo seul.

## 4. Plan coté (provisoire)
Vue de dessus, 1 caractère = 1 m. Légende : `=` piste (6 m), `t` talus nord (pente solide z 5-8,5, crête praticable z 0-5 à +2,5 m), `/` sente vers la crête, `R` rochers, `~` lit asséché (z 17-24, **au niveau 0** : le creux est rendu par le sol `g_rc_lit` et les berges peintes `rc_ds_berge_3q`), `P` pick-up, `c` caisses, `|` fil à boîtes, `E` épave, `B` bâche (cache), `O` pneus, `.` traces de pas, `,` bas-côté sableux, `S` panneau, `m` miroir, `@` apparition, `d` Don Trapo, `1` Quilla, `2` Pibe, `3` Morsa, `4` Tuerto. `O>` sortie ouest, `<E` sortie est route, `<L` sortie est lit.

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
| talus | pente du talus | 5-30 | 5-8,5 | 0 → 2,5 | oui (sauf la sente), champ `couv: 1` | **1** (la pente ne coupe pas la vue crête ⇄ piste) |
| crete | plateau de crête, `loc.niveaux` `{ x 5, z 0, w 25, d 5, y 2.5 }` | 5-30 | 0-5 | 2,5 | non | — (aucun avantage de hauteur) |
| sente | rampe ouest, `loc.niveaux` `{ x 2, z 3, w 3, d 7, y0 2.5, y1 0, axe 'z' }` | 2-5 | 3-10 | 0 → 2,5 | côtés en solides | 0 |
| rochers ×3 | blocs de crête | 15-18 / 22-25 / 27-30 | 2-3,5 / 2,5-4 / 1,5-3 | 1,6 | oui | 1 |
| pickup | pick-up appât | 12-17,2 | 11-13,2 | 2,0 | oui | 1 |
| caisses ×3 | C1, C2 (double fond), C3 | 8,5-9,7 / 10,2-11,4 / 17,8-19 | 14,8-15,6 / 15,6-16,4 / 15-15,8 | 0,7 | oui | 1 |
| fil | fil à boîtes | 20,9-21,1 | 10-16 | 0,3 | non (déclencheur T2) | 0 |
| lit | lit asséché (sol `g_rc_lit`, berges peintes) | 0-30 | 17-24 | 0 | non | 0 |
| epave | camion du Service ensablé, sans roues | 17-26 | 18-20,8 | 3,0 (plateau à 2,0) | oui, **sauf la niche de Morsa** x 21-22,5 ; z 19-20,8 (ouverte au sud, sur le lit) | 2 |
| pneus | tas de pneus et gravats | 5-7,5 | 19-21 | 1,2 | oui | 1 |
| bache | bâche tendue, cache | 26,5-30 | 20,5-24 | 1,6 | oui (bords), fouille par le côté ouest | 1 |
| panneau | panneau UFSA | 3,4-3,6 | 9,2-9,4 | 3,0 | oui | 0 |
| miroir | miroir sur piquet | 20 ; 3,2 | — | 1,2 au-dessus de la crête | non | — |

Un seul niveau de marche par point, comme sur la Mega-Line : la crête et la sente passent par `loc.niveaux` + solides (la pente en `couv: 1`). Le lit reste au niveau 0. Morsa est rendu à `y: 2.0` sur le PNJ (pas par `niveaux`) et sa case, dans la niche de l'épave, reste libre ; on l'approche par le lit. **Repli si le test 390 casse** : crête en décor plein, Pibe dans une niche praticable fermée de 2 × 2 m autour de (16,5 ; 4,2), hors d'atteinte en mêlée (il peut tirer et être visé), sente retirée ; on perd seulement « prendre la crête à revers ».

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
- Sprite : `gen_rc_pibe` (à produire) + portrait. Position (16,5 ; 4,5) sur le plateau de crête (`loc.niveaux`, +2,5 m), au sud du rocher R1, regard au sud.
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
- Sprite : `gen_rc_morsa` (à produire) + portrait. Position (21,75 ; 19,9), dans la niche de l'épave (case libre), rendu à `y: 2.0`.
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
- Sprite : `gen_rc_tuerto` (nouveau, silhouette distincte du rôdeur : borgne, épaules massives, gilet de cuir). Position (6 ; 22), caché derrière les pneus.

```text
start   (T3) « Tiens. Le lit, c'est aussi ma route. »
  - « Je ne fais que passer. »             → retour
  - « Un dollar par pas, et tu me montres le chemin ? »   test troc:5 → pass guide, fail retour
  - [Attaquer]                             action combat:embuscade_piste
retour  « Alors passe par la piste, comme tout le monde. Quilla t'attend. » action flag:emb_tuerto_vu;warp:rc_embuscade_piste:10:16.5 → end   (il te raccompagne sur la berge)
guide   « Six dollars. Et tu ne m'as jamais vu. » action pay:6;flag:emb_tuerto_achete → end   (il se rassoit ; le lit est libre)
```

## 7. Manières d'agir et conséquences
| Approche | Comment | Conséquence |
|---|---|---|
| Contourner par le lit | entrer dans le lit après le tas de pneus (x ≥ 10), longer z 21-23 sous l'épave : test Discrétion 4 (Morsa somnole dos au lit), Discrétion 6 si `emb_vu_fil` a sonné | sortie S_E_lit, rien payé ; échec = Morsa crie, combat |
| Contourner par la crête | sente, crête : neutraliser, chasser ou acheter Pibe (dans tous les cas, il est absent du combat), redescendre derrière Quilla | Quilla seule devant un joueur armé : option intimider à 4 au lieu de 6 [proposition] |
| Payer | 15 $ ou 2 eaux (8 à 20 $ selon la négociation) | passage, `emb_paye` ; Quilla raconte l'appât |
| Bluffer | « convoi du Service », mieux avec la plaque | passage gratuit, `emb_bluff` |
| Intimider | Charisme ou Force contre Volonté 6 | passage gratuit, `emb_intimide` ; échec = combat |
| Retourner le piège | avoir repéré les deux guetteurs (`emb_vu_talus` + `emb_vu_epave`) | passage gratuit, ou racket de la bande (+10 $) |
| Combattre | à tout moment, ou après un échec | voir §8 |
| Voler | la cache sous la bâche, depuis le lit par Discrétion 6 avant que la bande soit réglée, ou librement après une victoire ou un racket ; le fusil de Morsa pendant qu'il somnole | butin de la cache ; échec = combat |
| Partir | S_O (demi-tour) à tout moment avant le combat ; fuite pendant | voyage en halte sur la case ; la bande reste |

Drapeaux posés : `emb_regle`, `emb_paye`, `emb_bluff`, `emb_intimide`, `emb_racket`, `emb_demi`, `emb_vu_*`, `emb_pibe_*`, `emb_morsa_*`, `emb_tuerto_*`, `combat_embuscade_piste_<issue>` (posé par le moteur).

## 8. Combat optionnel
Reprise du système existant (`src/core/combat.js`, `src/data/combat.js`) : une entrée `ENCOUNTERS.embuscade_piste`, avec les extensions d'ARCHI.md : positions **absolues**, `centre: { x: 18, z: 13 }` sans téléporter le joueur, `si` par ennemi, `entreTour`, `rendSous`.

| id | Sprite | Position absolue (x ; z) | Case | PV | PA | Init. | Arme | Mêlée / armes | Particularité |
|---|---|---|---|---|---|---|---|---|---|
| quilla | gen_rc_quilla | (19 ; 12), à l'est du pick-up | libre (piste) | 18 | 7 | 7 | pistolet | 40 / 55 | `rendSous: 0.25` : quand elle se rend, la bande lâche la piste → **issue victoire** |
| pibe | gen_rc_pibe | (16,5 ; 4,5), crête, au sud du rocher R1 | libre (plateau) | 10 | 6 | 8 | fusil | 10 / 35 | `fuitTour: 2` ; couverture 1 (R1) ; **absent** si `emb_pibe_parti`, `_ko` ou `_achete` |
| morsa | gen_rc_morsa | (21,75 ; 19,9), niche de l'épave, rendu `y: 2.0` | libre (niche) | 14 | 6 | 5 | fusil | 30 / 50 | couverture 2 (épave) ; mains nues si `emb_morsa_desarme` ; **absent** si `_ko` ou `_achete` |
| tuerto | gen_rc_tuerto | (10 ; 20,5), lit, à l'est des pneus | libre (lit) | 14 | 6 | 6 | barre | 45 / 20 | `entreTour: 2` (renfort) ; **absent** si `emb_tuerto_achete` |

Pas d'ennemi neutre : un guetteur acheté, chassé ou assommé n'est pas dans la liste du combat (`si` par ennemi). Distances à l'entrée (1,5 ; 13) : Quilla 17,5 m, Pibe 17,3 m, Morsa 21,4 m, Tuerto 11,3 m (toutes ≥ 8 m). 

Couverture : pick-up, caisses, rochers (dont R1 pour Pibe), pneus, pente du talus = 1 ; épave = 2. Aucun avantage de hauteur sur la crête.

Issues (format `issues` existant, jamais de mort au lot C1) :
- **victoire** (dont la reddition de Quilla sous 25 % de PV) : la bande s'enfuit vers l'est par le lit ; la cache et le corps du pick-up sont fouillables. `flag:emb_regle;flag:emb_vaincue`. Texte : « Quilla crache dans le sable. "Garde la piste, alors. Elle ne te gardera pas." Ils s'en vont par le lit. »
- **fuite** : `rencontre:quitter` ; retour à la carte, halte sur la case. Texte : « Tu cours jusqu'à ne plus entendre les boîtes de conserve. »
- **reddition** (du joueur) : `payMax:20` (prend au plus 20 $) ; `emb_regle`. Texte : « Tu jettes les billets dans le sable. Quilla les compte sans se presser. »
- **defaite** : `payMax:20;take:water;warp:<entrée>` + 1 PV (existe) ; `emb_regle`. Texte : « Le ciel. Le sable. Don Trapo, qui te regarde. »

## 9. Objets à fouiller (butin)
Objets existants (`ITEMS`, armes du combat) sauf mention.

| Où | Condition | Contenu |
|---|---|---|
| Boîte à gants du pick-up (côté ouest du pick-up) | libre | 4 $ (`gain:4`) + **carnet du chauffeur** (`carnet_chauffeur`, objet de lore, [proposition]) : « Livraison Anselme, Dusk-Town : 12 bidons filtrés. Ne pas s'arrêter avant la douane. Ne s'arrêter pour personne. » |
| Caisse C2 (double fond) | `observation>=4` (compétence, lue par la condition étendue d'ARCHI) | 1 `ration`, 1 `water` |
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
| `rc_ds_berge_3q` | rebord peint du lit (le lit reste au niveau 0) | 10 × 1 × 0,4 | ×3 |
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
1. Catalogue `src/data/rencontres.js` (ARCHI §3) : entrée `embuscade_piste` du §14, `terrains: ['piste']`, `biomes: ['desert', 'rock']` ; `si(etat, case)` refuse une case déjà réglée dans `region.rencontres` ; taux de `TERRAINS` inchangés.
2. Scène construite à la demande (§4) : sol, éléments, solides, apparition, sorties (S_O = halte, S_E_* = reprise), déclencheurs T1-T3.
3. Visibilité différée : `si: '<drapeau>'` sur Pibe (`emb_vu_talus`), Morsa (`emb_vu_epave`), Tuerto (`emb_t3`) ; les zones < 6 m passent par des déclencheurs (`emb_pres_pibe`, `emb_pres_morsa`) ; le début du combat pose tous les drapeaux. Quilla : deux poses, `gen_rc_quilla_assise` si `!emb_t1`, debout si `emb_t1`.
4. Hauteurs : crête +2,5 et sente par `loc.niveaux` ; Morsa par `y: 2.0` sur le PNJ ; lit au niveau 0.
5. Sortie est gardée tant que `!emb_regle` (franchir x = 23 sur la piste).
6. Combat : `ENCOUNTERS.embuscade_piste` (§8), ancre (18 ; 13) par scène de rencontre, renfort au tour 2, effets des drapeaux sur la liste des ennemis.
7. Persistance : journal par case `region.rencontres` (réglée, cache vidée, morts) ; drapeaux `emb_*` remis à zéro par `retirerLieu` à la sortie.
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
8. **Lit asséché au niveau 0** (ARCHI) : le creux se lit par le sol `g_rc_lit` (galets, craquelures, plus froid) et les berges peintes `rc_ds_berge_3q`, pas par une vraie descente.
9. **Sols propres au pilote** plutôt que `g_sand` seul : `g_sand` est le sable de rue de Dusk-Town ; la scène a besoin de trois lectures distinctes (piste damée à ornières, sable des bas-côtés, lit de galets) pour que le joueur voie la route, le contournement et le creux. Variantes `_b`/`_c` contre la répétition.
10. **Tuerto a son propre sprite** (`gen_rc_tuerto`) au lieu de réutiliser `gen_rodeur` (ARCHI le permettait) : quatre silhouettes distinctes, pas de clone dans la même scène. Ses stats restent celles du rôdeur.
11. **Quilla a deux poses** (assise à l'ombre, debout près du pick-up) et Morsa une pose couchée : pas de PNJ qui marche, la scène change de pose au déclencheur T1.

## 14. Entrée au format d'ARCHI.md §4
Les poses des sprites (`buildings`, `props`, sols) sont dans le §15, avec la table des poses.

```js
embuscade_piste: {
  nom: "L'appât de la piste", famille: 'pillards',
  terrains: ['piste'], biomes: ['desert', 'rock'], poids: 1, duree: 1,
  scene: { size: { w: 30, d: 24 },
    ground: { skin: 'g_rc_sable', tint: null, paint: [ /* §15 : bande g_rc_piste z 10-16, bande g_rc_lit z 17-24, variantes _b/_c semées */ ] },
    light: { bg: '#1a1510', hemi: ['#f0dcb0', '#3a2a18', 1.3], sun: ['#ffd890', 0.9], tint: '#e8d0a0', actor: '#f2e6cc' },
    niveaux: [ { x: 5, z: 0, w: 25, d: 5, y: 2.5 }, { x: 2, z: 3, w: 3, d: 7, y0: 2.5, y1: 0, axe: 'z' } ],
    buildings: [ /* §15 */ ], props: [ /* §15 */ ],
    entree: { x: 1.5, z: 13, side: 'west' },
    sorties: [ { id: 'ouest', x: 0, z: 13, side: 'west', w: 6, effet: 'halte' },
               { id: 'est_route', x: 30, z: 13, side: 'east', w: 6, effet: 'reprise', si: 'emb_regle' },
               { id: 'est_lit', x: 30, z: 18.75, side: 'east', w: 3.5, effet: 'reprise' } ] },
  declencheurs: [ { id: 'T1', zone: { x: 10, z: 9, w: 13, d: 8 }, enter: 'flag:emb_t1', dialogue: 'rc_quilla' },
                  { id: 'T2', zone: { x: 20.9, z: 10, w: 0.2, d: 6 }, si: '!emb_vu_fil&!emb_regle', enter: 'flag:emb_alerte;flag:emb_vu_talus;flag:emb_vu_epave', dialogue: 'rc_quilla:alerte' },
                  { id: 'T3', zone: { x: 4, z: 17, w: 6, d: 7 }, enter: 'flag:emb_t3', dialogue: 'rc_tuerto' },
                  { id: 'garde', zone: { x: 23, z: 10, w: 1, d: 6 }, si: '!emb_regle', dialogue: 'rc_quilla:refus' },
                  { id: 'pres_pibe', zone: { x: 10.5, z: 0, w: 12, d: 9 }, enter: 'flag:emb_vu_talus' },
                  { id: 'pres_morsa', zone: { x: 15.75, z: 17, w: 12, d: 7 }, enter: 'flag:emb_vu_epave' } ],
  pnj: [ { id: 'rc_quilla_assise', name: 'Quilla', sprite: 'gen_rc_quilla_assise', x: 24.5, z: 9.0, faceTo: [1.5, 13], si: '!emb_t1' },
         { id: 'rc_quilla', name: 'Quilla', sprite: 'gen_rc_quilla', x: 19, z: 12, faceTo: [1.5, 13], dialogue: 'rc_quilla', si: 'emb_t1' },
         { id: 'rc_pibe', name: 'Pibe', sprite: 'gen_rc_pibe', x: 16.5, z: 4.5, faceTo: [16.5, 13], dialogue: 'rc_pibe', si: 'emb_vu_talus' },
         { id: 'rc_morsa', name: 'Morsa', sprite: 'gen_rc_morsa_couche', x: 21.75, z: 19.9, y: 2.0, faceTo: [21.75, 13], dialogue: 'rc_morsa', si: 'emb_vu_epave' },
         { id: 'rc_tuerto', name: 'Tuerto', sprite: 'gen_rc_tuerto', x: 6, z: 22, faceTo: [12, 22], dialogue: 'rc_tuerto', si: 'emb_t3' },
         { id: 'rc_trapo', name: 'Don Trapo', sprite: 'gen_rc_trapo', x: 13.5, z: 13.7, faceTo: [1.5, 13], examen: 'rc_trapo' } ],
  dialogues: { /* §6 : rc_quilla, rc_pibe, rc_morsa, rc_tuerto */ },
  fouilles: [ { id: 'rc_boite_gants', x: 12.2, z: 12.1, enter: 'gain:4;give:carnet_chauffeur' },
              { id: 'rc_caisse2', x: 10.8, z: 16.0, si: 'observation>=4', enter: 'give:ration;give:water', empty: 'Vide. Le sable a déjà fait une petite dune au fond.' },
              { id: 'rc_cache', x: 26.3, z: 22.2, si: 'emb_regle&!emb_paye&!emb_bluff&!emb_intimide', enter: 'gain:22;give:water:3;give:ration;give:poignard' }, // après victoire ou racket
              { id: 'rc_cache_vol', x: 26.3, z: 22.2, si: '!emb_regle', test: 'discretion:6', pass: 'gain:22;give:water:3;give:ration;give:poignard;flag:emb_vole', fail: 'combat:embuscade_piste' },
              { id: 'rc_plateau', x: 21.75, z: 20.9, si: '!rc_morsa_present', enter: 'give:fusil' } ],
  examens: [ /* §3 : rc_pickup, rc_trapo, rc_caisse1, rc_caisse3, rc_traces, rc_miroir, rc_trainees, rc_epave, rc_fil, rc_panneau, rc_pneus */ ],
  combat: { centre: { x: 18, z: 13 },
    ennemis: [ { id: 'quilla', nom: 'Quilla', sprite: 'gen_rc_quilla', x: 19, z: 12, pv: 18, pa: 7, initiative: 7, arme: 'pistolet', competences: { melee: 40, armes: 55 }, rendSous: 0.25 },
               { id: 'pibe', nom: 'Pibe', sprite: 'gen_rc_pibe', x: 16.5, z: 4.5, pv: 10, pa: 6, initiative: 8, arme: 'fusil', competences: { melee: 10, armes: 35 }, fuitTour: 2, si: '!emb_pibe_parti&!emb_pibe_ko&!emb_pibe_achete' },
               { id: 'morsa', nom: 'Morsa', sprite: 'gen_rc_morsa', x: 21.75, z: 19.9, pv: 14, pa: 6, initiative: 5, arme: 'fusil', competences: { melee: 30, armes: 50 }, si: '!emb_morsa_ko&!emb_morsa_achete' },
               { id: 'tuerto', nom: 'Tuerto', sprite: 'gen_rc_tuerto', x: 10, z: 20.5, pv: 14, pa: 6, initiative: 6, arme: 'barre', competences: { melee: 45, armes: 20 }, entreTour: 2, si: '!emb_tuerto_achete' } ],
    issues: { victoire: 'flag:emb_regle;flag:emb_vaincue', fuite: 'rencontre:quitter', reddition: 'payMax:20;flag:emb_regle', defaite: 'payMax:20;take:water;flag:emb_regle;warp:rc_embuscade_piste:1.5:13' },
    textes: { /* §8 */ } },
}
```
Morsa désarmé (`emb_morsa_desarme`) combat à mains nues : le moteur prend l'arme dans `arme`, donc Rivet pose `arme: 'mains'` quand le drapeau est levé (ou une deuxième entrée `morsa_desarme` à `si` inverse).
