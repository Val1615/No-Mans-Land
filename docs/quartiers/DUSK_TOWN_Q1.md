# Dusk-Town, quartier 1 : « La Pompe » (v2)

Rédigé le 21 octobre 2026 (heure de Paris). Le jeu se passe en 2175 ; le roman décrit Dusk-Town en 2202.

## 0. Ce que dit le roman (canon) et ce qui en découle

| Fait du roman | Citation | Lecture pour 2175 |
|---|---|---|
| Une ville d'apparence abandonnée | « une ville laissée à l'abandon [...] Dusk-Town, la cité fantôme » (Ch. I §61) | L'apparence est voulue, elle n'est pas un état définitif |
| Les habitants se cachent | « Dusk Town n'est pas la ville fantôme qu'elle veut laisser paraitre. » (Ch. I §93) | Base canon de l'habitat discret : volets, accès latéraux, vie en arrière-cour |
| Accès par une piste | « le long du tracé de terre battu menant à Dusk-Town » (Ch. I §69) | Une entrée ouest en terre battue |
| État des lieux | « Les murs sont délabrés, les routes recouvertes de sable et d'herbes mortes. » (Ch. I §71) ; « croulant sous le temps et les dégâts du passé » (§61) | État de 2202. En 2175, le délabrement est moindre et entretenu par endroits (**ambiguïté temporelle**) |
| Avenue principale, bitume | « un son strident dans l'avenue principale » (Ch. I §107) ; « regardant le bitume » (§145) | Un axe asphalté, ensablé sur les bords |
| Bâtiments à étage | « fouiller le bâtiment et prendre de la hauteur » (Ch. I §83), un couloir (§85) | Plusieurs bâtiments ont un ou deux étages |
| Laboratoire scellé sous la ville | « Un ancien laboratoire de Human Corporation est situé sous cette ville, mais l'accès est verrouillé » (Ch. I §75) | Scellé en 2202, donc vraisemblablement scellé en 2175. Il est absent du quartier 1 et ne fait l'objet que d'une rumeur |
| Violence des récupérateurs | « importants bains de sang quand les différentes troupes de récupérateurs se croisent » (Ch. I §77) | Danger extérieur. **Pas de milice** (décision de Valentin, 21/10/2026) |
| IO tire sur les mutants | un mutant abattu « sans sommation » (Ch. I §99-105) | Cohérent avec les rafles du Service Militarisé (**décision de Valentin**) |

**Décisions de Valentin (21/10/2026), qui remplacent la v1**
- **Personne dans les rues.** Les habitants vivent cachés dans les bâtiments en ruine.
- **Pas de vraie milice** en ville.
- **Des mutants vivent cachés** parmi les villageois.
- **Quelques membres isolés des Los Invictos**, sans importance collective.
- **Pourquoi ils se cachent** : Dusk-Town est un point de passage important des soldats du Service Militarisé de Steel-Megalopolis. Ceux-ci y mènent souvent des rafles anti-mutants, qui font aussi de nombreuses victimes humaines. Les habitants ont donc choisi une vie retirée et camouflée.
- Cette histoire s'apprend en jeu par les personnages, sans exposition.
- Une communauté relativement accueillante, une fois à l'intérieur.

## 1. Fonction du quartier
C'est l'entrée de la ville et un passage forcé des patrouilles. Le quartier abrite, cachés derrière des façades mortes :
- l'eau (la pompe, actionnée la nuit) ;
- les soins (la clinique) ;
- le ravitaillement (l'épicerie) ;
- le lieu de parole (le bar) ;
- des logements (dont celui de Mara, où vit aussi Bruno).

## 2. Habitants et activités
- Des humains et des mutants cachés, plus Ileana, une Invicta isolée de passage.
- Le jour, rien ne bouge dehors. La pompe sert la nuit (pas de cycle jour-nuit en Q1).
- Règles de camouflage, apprises par les dialogues :
  - rien dehors (ni linge, ni pot de fleurs, ni fumée le jour) ;
  - longer les murs ;
  - entrer par l'arrière quand c'est possible.

## 3. Plan (grille de 1 m, origine au nord-ouest, x vers l'est, z vers le sud) : zone de 48 × 36 m

```
x:0     6        16    20  22   28 30 31        41 43  47 48
z:0 +------------------------------------------------------+
    |                  [ Place de la pompe ]               |
  2 |                  x20-30 z2-10   P=pompe(25,6)        |
  4 |  M     +---------+      |  ruelle |  +-----------+    |
    | (MARA) | CLINIQUE|      |  6 m    |  |  BAR      | T  |
    | x1-5   | x6-16   |      | x22-28  |  | x31-41    |(N3)|
    | z6-12  | z5-13   |      |         |  | z4-13 2ét.|x43-47
 13 |        +---D-----+      |         |  +----D------+z8-13
 14 |====== AVENUE PRINCIPALE (bitume ensablé) 8 m, z14-22 ==|
 22 |=========================================================|
 24 | S2a S2b    +-------+   | ruelle  |  ruine    atelier   |
    | x4-8 x8-13 |EPICERIE D  | sud 6 m |  x30-37   x39-47   |
    | habitées   | x14-22 |   | x22-28  |  z24-31   z24-33   |
 31 |            | z24-31 |   |         |                    |
 36 +------------------------------------------------------+
Entrée : piste de terre battue à l'ouest (x0-4, z15-21).
```

- **Avenue principale** : 8 m (z 14-22), sur toute la largeur. Bitume, sable sur les bords.
- **Ruelle de la pompe** : 6 m (x 22-28, z 2-14). Elle mène à la place (x 20-30, z 2-10).
- **Ruelle sud** : 6 m (x 22-28, z 22-36). Elle dessert l'épicerie par son flanc est.
- **Sortie est** : barrée par des sacs de sable et la milice (x 46-48). C'est la route des récupérateurs, fermée en Q1.

## 4. Bâtiments visitables, à entrée camouflée (contrat de porte unique)

| Id | Bâtiment | Volume | Porte (ouverture, côté) | Seuil | Intérieur | Personnes |
|---|---|---|---|---|---|---|
| mara_house | Maison de Mara | 5 × 7 × 6 m | (4,5 ; 12), sud | (4,5 ; 13) | mara_in 5 × 7, porte (3,5 ; 7) | Mara, Bruno (mutant) |
| clinic | Clinique | 9 × 8 × 3 m | (11 ; 13), sud | (11 ; 14) | clinic_in 9 × 8, porte (5 ; 8) | Vera : soins payants |
| bar | Le Passage | 10 × 9 × 6 m | (36 ; 13), sud | (36 ; 14) | bar_in 10 × 9, porte (5 ; 9) | Hector : repas, verre ; Ileana (Invicta) |
| grocery | Épicerie | 8 × 7 × 3 m | (22 ; 27,5), est | (23 ; 27,5) | grocery_in 8 × 7, porte (8 ; 3,5) | Anselme : eau, rations |

**Ce qui rend une entrée camouflée lisible** (contrat de porte, sans faux marqueur)
1. **Indice sur la façade** : la porte est en planches clouées, avec un filet de lumière en bas, et un petit symbole gravé à côté (croix, bouteille, goutte, bocal).
2. **Seuil praticable** dégagé du sable, avec des traces de pas.
3. **Anneau discret** au seuil, présent seulement sur les vraies entrées.
4. **Interaction** : clic ou tap sur la façade ou la porte, puis trajet jusqu'au seuil et entrée. Près du seuil, le bouton « Entrer » apparaît.

Les enseignes de la v1 sont supprimées. Aucune fenêtre n'est éclairée de l'extérieur.

## 5. Bâtiments non visitables (aucun marqueur)
- Tour effondrée : 4 × 5 × 6,5 m, toit percé. Elle remplace le poste de milice.
- Maisons S2a et S2b : portes condamnées.
- Ruine S3 : 7 × 7 × 1,6 m.
- Atelier : porte de garage fermée.

Un clic dessus donne « fermé ».

## 6. Accès et restrictions
- Entrée par la piste ouest.
- La sortie est est bloquée par des éboulis et une épave de voiture (plus de barricade de milice).

## 7. Décor : l'abandon visible, la vie cachée
- **Dehors** :
  - sable en congères au pied des murs ;
  - herbes mortes en nombre ;
  - enduits tombés, briques à nu, fissures, coulures ;
  - toits percés, fenêtres condamnées ou crevées ;
  - éboulis, pneus, buissons morts, épave.
- **Dedans** : linge, bacs de culture, paillasse, rideau derrière lequel se tient Bruno. (v6 : paillasse et rideau réalisés ; linge et bacs à produire, voir « Intérieurs ».)

## 8. Accroches de quête (**propositions**)
- **La pompe** : son joint siffle et trahit le pompage nocturne. Il faut trouver du caoutchouc pour Nilo.
- **Les rafles** :
  - Bruno a perdu son frère au nord ;
  - deux hommes d'ici, sans mutation, ont aussi été emmenés ;
  - Vera garde une civière derrière la porte.
- **Ileana** : elle attend une caravane qui ne vient pas.

## 9. Personnages clés

Tous ces personnages sont des **propositions réutilisables** : Mara, Vera et Nilo viennent de la maquette ; Hector, Anselme, Bruno et Ileana sont nouveaux. Ruth (milice) est supprimée. Aucun n'est canon.

### Mara (chez elle, pompe la nuit)

| Rubrique | Contenu |
|---|---|
| Veut | Que la pompe tienne jusqu'aux pluies |
| Craint | Que le sifflement de la pompe attire une patrouille la nuit ; que l'on découvre Bruno |
| Sait | L'état exact de la pompe, qui a de l'eau en réserve |
| Cache | Elle héberge Bruno, un mutant |
| Relation au joueur | Méfiante, mais pragmatique |
| Vocabulaire et rythme | Phrases courtes, mots de métier (joint, piston, seau) |
| Esquive | Parle de la quantité restante au lieu de répondre |
| Limites | Ne vend pas l'eau de la pompe |
| Ce qui la change | Une aide concrète à la pompe |

### Vera (clinique)

| Rubrique | Contenu |
|---|---|
| Veut | Des médicaments, et du calme dans sa salle |
| Craint | Une épidémie qu'elle ne pourrait pas contenir |
| Sait | Qui est malade, qui se bat |
| Cache | Elle soigne parfois des blessés des récupérateurs |
| Relation au joueur | Polie, distante. Le paiement passe d'abord |
| Vocabulaire et rythme | Précis, un peu sec, de l'humour noir rare |
| Esquive | « Ça regarde mes patients. » |
| Limites | Pas de soin à crédit en Q1 |
| Ce qui la change | Ramener des fournitures (plus tard) |

### Hector (bar)

| Rubrique | Contenu |
|---|---|
| Veut | Que le bar reste le seul endroit neutre de la ville |
| Craint | La milice dans sa salle, les armes sorties |
| Sait | Les rumeurs, les dettes |
| Cache | Il achète au marché des récupérateurs |
| Relation au joueur | Commercial, curieux |
| Vocabulaire et rythme | Phrases qui tournent, questions en retour |
| Esquive | Sert un verre et change de sujet |
| Limites | Pas de bagarre chez lui |
| Ce qui le change | Une information qui vaut quelque chose |

### Bruno (mutant caché chez Mara, nouveau, proposition)

| Rubrique | Contenu |
|---|---|
| Veut | Rester invisible, se rendre utile la nuit |
| Craint | Les lampes des soldats, d'être vu de la fenêtre |
| Sait | Comment s'est passée la rafle au nord, qui a été pris |
| Cache | Il pense parfois à se rendre pour qu'on cesse de chercher chez Mara |
| Relation au joueur | Méfiant, puis franc, sans se plaindre |
| Vocabulaire et rythme | Phrases courtes, silences (« ... »), détails concrets (les poutres, les lampes) |
| Esquive | « Personne ne pose la question deux fois. » |
| Limites | Ne sort pas le jour |
| Ce qui le change | Une preuve que quelqu'un d'autre prend des risques pour la maison |

### Ileana (Invicta isolée, nouvelle, proposition)

| Rubrique | Contenu |
|---|---|
| Veut | Repartir, mais pas vers le ranch |
| Craint | De devoir choisir un camp |
| Sait | Les routes et les caravanes, comment on parle de Dusk-Town au Ranch Liberté |
| Cache | Pourquoi elle a quitté les Invictos |
| Relation au joueur | Sèche, observatrice |
| Vocabulaire et rythme | Ironie froide, réponses brèves |
| Esquive | « Ça ne te regarde pas. Bois ton verre. » |
| Limites | Ne parle pas du ranch en détail |
| Ce qui la change | Une caravane, un service sans contrepartie |

### Anselme (épicerie, secondaire)
Vieux, lent, compte tout à voix haute. Il vend l'eau en bouteille qu'il filtre lui-même. Il cache un stock de rations pour la saison sèche.

### Nilo (compagnon, proposition reprise de la maquette)
Mécanicien de Dusk-Town. Il suit le joueur et commente peu.

## Noms des lieux (décision de Valentin)
Aucun nom n'est affiché au-dessus d'une façade tant que le lieu n'est pas découvert. Un lieu est découvert quand le joueur y est entré, ou quand un personnage l'a nommé explicitement en dialogue (exemple : Mara parle de Vera et de la porte à la croix, la Clinique est alors nommée). Pas d'affichage à l'approche. Une fois découvert, le nom reste affiché.

## Intérieurs (v6, 21/10/2026) : réalisés en assets réels
Grille en mètres, origine au coin nord-ouest de la pièce. Murs du fond (nord, ouest) à 3 m, murs avant (sud, est) en coupe à 0,9 m. Mobilier posé par son emprise ; objets longs le long de l'axe x (seule orientation dessinée).

| Intérieur | Taille | Sol / murs | Mobilier (coin min x, z) | Personnes | Porte(s) |
|---|---|---|---|---|---|
| Clinique (Vera) | 9 × 8 | carrelage fissuré / chaux écaillée | 2 lits de camp (0,4 ; 0,4) et (0,4 ; 2,1) ; étagère métallique (3 ; 0,25) ; armoire à pharmacie (7,4 ; 0,25) ; table de soins (4,4 ; 2,6) ; bureau (7 ; 3,7) ; **civière derrière la porte** (6,1 ; 6,7) | Vera (6,2 ; 1,6) | sud (5 ; 8) |
| Le Passage (Hector) | 10 × 9 | planches (maquette) / brique à nu | étagère basse et radio (3 ; 0,25) ; comptoir 3,8 m (2,1 ; 2) ; 2 tables à tabourets (6,4 ; 4,6) et (1,2 ; 5,4) ; étagère métallique (7,6 ; 0,25) | Hector derrière le comptoir (4 ; 1,4), Ileana (8,9 ; 3,6) | sud (5 ; 9) |
| Épicerie (Anselme) | 8 × 7 | béton (maquette) / planches et tôle | 2 étagères de conserves (0,4 ; 0,25) et (2,6 ; 0,25) ; étagère métallique (5,2 ; 0,25) ; comptoir et balance (1,2 ; 4,9) ; seaux et jerrican (5,6 ; 1,6) | Anselme (2,2 ; 4,2) | sud (5,5 ; 7) et est (8 ; 3,5) |
| Chez Mara | 5 × 7 | terre battue / enduit d'argile | paillasse (0,3 ; 0,3) ; **rideau** (2,5 ; 2,7) devant Bruno ; table et deux chaises (0,3 ; 3,4) ; seaux et jerrican (3,4 ; 4) | Mara (1 ; 2), Bruno derrière le rideau (3,8 ; 1,6) | sud (3,5 ; 7) |

Écarts au §7 : le linge et les bacs de culture ne sont plus chez Mara (aucun sprite à l'angle v4) ; les sacs de rations d'Anselme et son filtre à eau sont à produire. Toutes les entrées camouflées existantes (5 portes peintes, 4 bâtiments) mènent à un intérieur réalisé ; les autres façades restent fermées par décision (§5).
