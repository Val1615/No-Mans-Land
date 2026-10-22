# Steel-Megalopolis · Plan d'implémentation des quartiers bas (Lower-Town, Asia-Ground, China Lake)

Légende : **[décision]** Valentin · **[proposition]** à valider · **[fiche]** repris de LOWER_TOWN.md, ASIA_GROUND.md, CHINA_LAKE.md.
Planches validées par Valentin le 2026-10-22. Rien n'est codé au-delà de ce qui est en cours chez Rivet (Lower-Town, sans quêtes).

## 0. Règles communes
- Géographie [décision] : Center-Town au centre, surélevé au-dessus de Lower-Town ; Sous-Ville souterraine et séparée ; Asia-Ground au sud de Lower-Town ; China Lake au sud d'Asia-Ground, derrière le barrage de gang.
- Quartiers composés à la main [décision] : aucun placement procédural, chaque sprite a ses coordonnées dans `src/data/steel.js`.
- Format [proposition, d'après `src/data/steel.js`] :
  - extérieurs `kind: 'exterior'`, `size: { w: 48, d: 36 }`, `light`, `ground`, `props`, `walkers`, `glows` ;
  - jonctions de bord avec `J(id, loc, ox, oz, tx, tz, to, label, conditions)` ;
  - portes peintes via `painted(PAINTED_DOORS_X, loc, table)` et bâtiments dans `buildings_steel.js` (`BUILDINGS_LOWER`, `BUILDINGS_ASIA`, `BUILDINGS_CHINA`) ;
  - intérieurs `kind: 'interior'`, porte de sortie au sud avec seuil à 1 m dans la pièce ;
  - PNJ dans la liste des acteurs (`id, name, sprite, location, x, z, faceTo, dialogue`).
- Caméra v4, 50 px/m, nuit sous le sarcophage. Un `light` propre à chaque quartier : `LOWER` (sodium et four), `ASIA` (rouge laque, vapeur, un seul néon cyan IO), `CHINA` (vert bile, reflets d'eau, rouge en points).
- **Intérieurs** (pour corriger les défauts connus) :
  - Taille minimale 10 × 8 m, 12 × 9 m pour les pièces principales. Les 6 × 5 m actuels laissent trop de noir à l'écran.
  - Le sol et les murs remplissent le cadre de la caméra v4, sans grande marge noire. Si la pièce reste plus petite que le cadre, on ajoute un fond de mur ou une arrière-salle visible plutôt que du vide.
  - Le style de l'intérieur reprend celui de l'extérieur [décision] : mêmes matériaux, même palette, même `light` en version intérieure (`LOWER_IN`, `ASIA_IN`, `CHINA_IN`).
- **PNJ et libellés** : un PNJ se place à 1,5 m au moins d'une porte, d'une jonction ou d'un objet à libellé, et jamais sur la ligne entre le libellé et la caméra (donc pas au sud de l'objet). Vérification sur capture pour chaque zone.
- **Combat** : il n'existe pas encore. Toute issue qui demande un combat est un simple point d'accroche (drapeau et réplique), sans mécanique.

## 1. Lower-Town (lot 1, en cours chez Rivet)
### Zones
| Zone | Taille | Rôle |
|---|---|---|
| `steel_lower` | 48 × 36 m | rue industrielle, usine, foyer, accès vers Center-Town, la Sous-Ville et Asia-Ground |

### Jonctions
| Id ici | Position | Vers | Id en face | Condition |
|---|---|---|---|---|
| `l_ouest` | x 0, z 18 (La Descente) | Center-Town | `c_est` (x 48, z 18) | portique : Repérage +1 en montée |
| `l_fosse` | x 42, z 34 (Escalier de la Fosse) | Sous-Ville | `v_fosse` (aux Poutres, à créer) | clé de Mère Ruiz, ou ouvert depuis le bas |
| `l_sud` | x 8, z 36 | Asia-Ground | `a_nord` | aucune |
| `l_sud_est` | x 30, z 36 (ruelle) | China Lake | `k_est` | fermé jusqu'au lot 3, puis libre depuis China Lake |

### Bâtiments
| Bâtiment | Sprite | État |
|---|---|---|
| Usine 7 (14 × 10 m) | `lt_atelier_usine` | existant |
| Atelier Bastide (version réduite) | `lt_atelier_usine` à l'échelle 0,6 ou variante `lt_atelier_petit` | variante à produire |
| Immeuble ouvrier × 3 (8 × 6 m) | `lt_immeuble_ouvrier` (avec `flip` pour varier) | existant |
| Foyer Ruiz (10 × 7 m) | `lt_foyer_ruiz` | existant |
| Portique de La Descente | `lt_portique_io` | existant |
| Comptoir de Moss (rez d'immeuble) | `lt_comptoir_moss` | à produire |
Props à produire : `lt_tuyau` (droit, coude), `lt_sodium`, `lt_horloge_pointage`, `lt_voiture_panne`, `lt_bidons`, `lt_ferraille`, `lt_palettes`, `lt_grille_fosse`, `lt_flaque`, `lt_passerelle`.

### Intérieurs
| Intérieur | Taille | Contenu | PNJ |
|---|---|---|---|
| `foyer_in` (Le Foyer Ruiz) | 12 × 9 m | réfectoire, longues tables, poêle, dortoir visible au fond, trappe de cave fermée (lit = soin et sauvegarde) | Mère Ruiz (x 3, z 2), Pia (x 9, z 6) |
| `bastide_in` (Atelier Bastide) | 10 × 8 m | établi, palan, tas de ferraille, four | Joaquim Bastide (x 7, z 2) |
| `moss_in` (Chez Moss) | 10 × 8 m | comptoir, quatre tables, arrière-salle entrouverte | Moss (x 5, z 2, derrière le comptoir) |
| `pointage_in` (Pointage Usine 7) | 10 × 8 m | guichet grillagé, horloge, file de casiers, vue sur l'atelier par une vitre | Ilse Raack (x 5, z 2) |
La cave du foyer n'est pas un intérieur au lot 1 : la trappe reste fermée jusqu'au lot 4.

### PNJ extérieurs
- Agent Dorn : il patrouille sur la Rue des Fours, entre x 12 et x 36 à z 18, avec des arrêts loin des portes.
- Pia : la nuit, elle se tient près de l'Allée du Foyer (x 6, z 26).
- Passants (`walkers`) : des ouvriers sur la Place de la Relève.

### Quêtes rattachées
« Contrôle de nuit » [fiche] : trois issues, toutes sans combat (faire sortir la famille par la Fosse, acheter Dorn avec ce que Moss sait, le retenir ailleurs). Une seule accroche de combat : `hook_dorn_combat`, si le joueur frappe Dorn, avec un drapeau et une réplique.

## 2. Asia-Ground
### Zones
| Zone | Taille | Rôle |
|---|---|---|
| `steel_asia` | 48 × 36 m | marché couvert, Rue des Lanternes, Mille Marches, Cour des Porteurs |

### Jonctions
| Id ici | Position | Vers | Id en face | Condition |
|---|---|---|---|---|
| `a_nord` | x 8, z 0 [proposition : la fiche dit « bout de rue ouest, x 0, z 18 », à aligner car Asia-Ground est au sud] | Lower-Town | `l_sud` | aucune |
| `a_escalier` | x 43, z 0 (Mille Marches) | Center-Town | `c_sud_est` (x 38, z 36) | caméra en haut : Repérage +1 en montée |
| `a_sud` | x 24, z 36 | China Lake | `k_nord` | barrage de gang : fermé jusqu'au lot 3, puis condition de la quête |
| `a_quai` | x 46, z 30 (monte-charge, Cour des Porteurs) | Lower-Town (arrière de l'Usine 7) | `l_usine_arriere` | [proposition, facultatif] lot 4 |

### Bâtiments
| Bâtiment | Sprite | État |
|---|---|---|
| Restaurant à étages × 3 (8 × 6 m, 3 niveaux) | `ag_restaurant` (2 variantes de façade) | à produire |
| Halle du marché (24 × 16 m, 3 modules) | `ag_halle_module` | à produire |
| Boutique-atelier (6 × 5 m) : Pharmacie Lau et Électronique Okafor | `ag_boutique` (2 variantes) | à produire |
| Bureau des Emplacements (étage au-dessus d'une boutique) | `ag_bureau` | à produire |
| Mille Marches | `ag_escalier` | à produire |
| Monte-charge de quai | `ag_monte_charge` | à produire |
Props à produire : `ag_stand_nouilles`, `ag_stand_poisson`, `ag_stand_pieces`, `ag_lanterne_cable`, `ag_auvent`, `ag_caisses_legumes`, `ag_glaciere`, `ag_wok`, `ag_chariot`, `ag_hautparleur_io`, `ag_neon_io` (le seul cyan du quartier).

### Intérieurs
| Intérieur | Taille | Contenu | PNJ |
|---|---|---|---|
| `lau_in` (Pharmacie Lau) | 10 × 8 m | comptoir, étagères de boîtes, arrière-boutique avec lit de soin visible | Hana Lau (x 4, z 2) |
| `okafor_in` (Électronique Okafor) | 10 × 8 m | établi, bacs de pièces, écrans, fauteuil de réparation d'implant | Okafor (x 6, z 2) |
| `emplacements_in` (Bureau des Emplacements) | 10 × 8 m | bureau, coffre, registres, fenêtre sur le marché ; le faux registre se cherche la nuit | Victor Seng (x 5, z 2, en journée seulement) |
| `mei_in` (arrière du stand de Mei) | 10 × 8 m | cuisine, réserve, lit de Kim, coffre à loyers | Mei Tran (x 3, z 2), Kim Tran (x 8, z 5, quand il n'est pas en course) |
Le stand des Nouilles de Mei reste un service extérieur (comptoir) ; `mei_in` sert seulement à la quête.

### PNJ extérieurs
- Mei Tran : derrière son stand, côté nord de la halle. Elle sert depuis la rue, son libellé reste au-dessus du stand.
- Kim Tran : il circule entre la Cour des Porteurs et le bord sud.
- Le passeur (frère de Bruno), selon le plan : il n'est pas placé ici.

### Quêtes rattachées
« Le loyer de Mei » partie 1 [fiche] : la hausse, le faux registre, le paiement en crédits, ou la filature de Kim jusqu'au barrage. Pas de combat requis. Accroche de combat `hook_barrage_force` : forcer le barrage est refusé par une réplique et laisse un drapeau.

## 3. China Lake
### Zones
| Zone | Taille | Rôle |
|---|---|---|
| `steel_china` | 48 × 36 m | marché illégal [décision] : lac au centre, ceinture de stands sur les quais, bâtiments au fond, ruelles |
Une seule zone suffit : le lac (x 14-34, z 12-26) est vide et non praticable, il agrandit la vue sans demander de contenu. Une seconde zone (arrière-cour de la maison de thé) reste en réserve et n'est pas planifiée.

### Jonctions
| Id ici | Position | Vers | Id en face | Condition |
|---|---|---|---|---|
| `k_nord` | x 24, z 0 (Le Barrage) | Asia-Ground | `a_sud` | entrée : quête de Mei active, laissez-passer, ou 20 cr à Ah-Lam [proposition] ; sortie libre |
| `k_est` | x 48, z 32 (ruelle de l'angle) | Lower-Town | `l_sud_est` | libre depuis China Lake ; dans l'autre sens, ouvert seulement après une première visite |

### Bâtiments
| Bâtiment | Sprite | État |
|---|---|---|
| Maison de thé (10 × 8 m, 2 niveaux, au fond sur l'axe x 24), seul toit recourbé | `cl_maison_the` | à produire |
| Immeuble de fond à étages × 3 (8 × 6 m, 2 façades) : Pavillon du Dragon et façades muettes | `cl_immeuble_fond` | à produire |
| Structures sur pilotis (module 6 m) | `cl_pilotis` | à produire |
| Cabane des Filets | `cl_cabane` | à produire |
| Ponton de Shen | `cl_ponton` | à produire |
| Stand illégal (2 × 2 m, en ligne) | `cl_stand_puces`, `cl_stand_armes`, `cl_stand_papiers`, `cl_stand_medocs` | à produire (4 variantes) |
| Lac | sol `g_cl_eau` (eau sombre, reflets rouges) | à produire |
Props à produire : `cl_cable_lanternes` (12 à 20 m), `cl_ballon` (dragon, carpe, tigre, phénix), `cl_bache`, `cl_treteaux`, `cl_caisse_armes`, `cl_bac_puces`, `cl_presse_papiers`, `cl_bocaux`, `cl_dechets` (3 variantes), `cl_barriere_caisses`, `cl_pieux`, `cl_friture`, `cl_mahjong`.

### Intérieurs
| Intérieur | Taille | Contenu | PNJ |
|---|---|---|---|
| `the_in` (Maison de thé) | 12 × 9 m | salle à paravents, tables basses, estrade au fond, porte gardée vers un bureau (décor seul) | Madame Zhou (x 6, z 2), deux hommes de main (x 2, z 4 et x 10, z 4) |
| `dragon_in` (Pavillon du Dragon) | 12 × 9 m | salle de restaurant, cuisine ouverte, escalier vers la salle de jeu (décor) ; repas 5 cr | serveur (figurant), Vieux Lo le soir (x 9, z 6) |
| `filets_in` (Les Filets) | 10 × 8 m | cabane humide, filets, objets repêchés, cache sous le plancher | Yu (x 4, z 3) |
Les stands, le ponton de Shen et le barrage sont des services extérieurs, sans intérieur.

### PNJ extérieurs
- Shen : sur son ponton, rive ouest (x 4, z 16).
- Ah-Lam : au barrage, décalé à x 27, z 2, pour ne pas masquer le libellé de la jonction.
- Les marchands des stands sont des figurants, un par rive, placés derrière leur table (côté nord de l'étal) pour que le libellé du stand reste visible.
- Le Vieux Lo : il marche le long des câbles, sur le quai nord.

### Quêtes rattachées
« Le loyer de Mei » partie 2 [fiche] : remonter l'argent de Kim (Ah-Lam, puis Zhou) et découvrir la fraude de Seng. Trois issues sans combat : preuve à Zhou (registre et lecture de puce chez Shen), rachat de Kim, ou prise de la place de Seng. Accroches de combat : `hook_hommes_de_main`, si le joueur menace Zhou, et `hook_ah_lam`, si le joueur le confronte seul. Ce sont des drapeaux et des répliques, sans mécanique.

## 4. Lots ordonnés
### Lot 1 : Lower-Town, extérieur et intérieurs, sans quête (en cours)
- **Rivet** : `steel_lower` et `LOWER` ; placement des sprites existants ; jonctions `l_ouest` ↔ `c_est` et `l_fosse` ↔ `v_fosse` (avec `v_fosse` aux Poutres) ; `l_sud` et `l_sud_est` posées en bord « fermé » (`E(...)`) avec un texte ; les 4 intérieurs ; PNJ placés avec leurs dialogues de base (services seulement) ; tests de réciprocité des jonctions.
- **Ocre** : `lt_atelier_petit`, `lt_comptoir_moss`, props `lt_*` ; décor des 4 intérieurs dans le style de l'extérieur ; textes des services et dialogues de base (Ruiz, Bastide, Moss, Raack, Dorn, Pia).
- **Vérification** :
  - aller-retour Center-Town ↔ Lower-Town ↔ Sous-Ville sans blocage, avec le Repérage +1 en montée seulement ;
  - les 4 intérieurs font au moins 10 × 8 m et la capture ne montre pas de grande zone noire ;
  - aucun PNJ ne masque de libellé (capture de chaque porte) ;
  - les sprites reprennent l'angle v4 à 50 px/m ;
  - les tests existants passent.

### Lot 2 : Asia-Ground, extérieur et intérieurs
- **Rivet** : `steel_asia` et `ASIA` ; jonctions `a_nord` ↔ `l_sud` et `a_escalier` ↔ `c_sud_est` (côté Center-Town) ; `a_sud` en bord fermé (barrage visible) ; les 4 intérieurs ; PNJ et services (nouilles, pharmacie, électronique, bureau).
- **Ocre** : les bâtiments `ag_*` (6) et les props (11), les décors des 4 intérieurs, les textes de services et dialogues de base ; validation de palette face à Lower-Town et China Lake.
- **Vérification** :
  - la boucle Center-Town → Lower-Town → Asia-Ground → Center-Town par les Mille Marches fonctionne ;
  - un seul néon cyan dans la zone ;
  - pas de pagode ;
  - mêmes contrôles d'intérieurs et de libellés qu'au lot 1.

### Lot 3 : China Lake, extérieur et intérieurs
- **Rivet** : `steel_china` et `CHINA` ; le sol d'eau non praticable avec un test de connexité des quais (comme `scenes.test.js` de la maquette) ; jonctions `k_nord` ↔ `a_sud` (condition du barrage) et `k_est` ↔ `l_sud_est` (Lower-Town s'ouvre après la première visite) ; les 3 intérieurs ; services des 4 stands, du ponton et des Filets.
- **Ocre** : les bâtiments `cl_*` (7 types, dont les 4 stands), le sol d'eau, les props (13), les décors des 3 intérieurs ; textes des stands (marchandises illégales [décision]) et dialogues de base.
- **Vérification** :
  - on fait le tour complet du lac par les quais, sans passage dans l'eau ;
  - la maison de thé est le seul toit recourbé et se voit depuis le barrage ;
  - la palette reste distincte d'Asia-Ground (comparaison de captures côte à côte) ;
  - la boucle Asia-Ground → China Lake → Lower-Town fonctionne ;
  - mêmes contrôles d'intérieurs et de libellés.

### Lot 4 : quêtes
- **Rivet** :
  - drapeaux et étapes de « Contrôle de nuit » (la trappe du foyer s'ouvre vers la Fosse) ;
  - « Le loyer de Mei » parties 1 et 2 (faux registre de nuit, filature de Kim, condition du barrage, preuves chez Zhou, trois issues) ;
  - accroches de combat sous forme de drapeaux ;
  - jonction facultative `a_quai` ↔ `l_usine_arriere`.
- **Ocre** : tous les dialogues de quête (Ruiz, Pia, Dorn, Moss ; Mei, Kim, Seng ; Ah-Lam, Zhou, Shen, Yu), les objets de quête (`obj_faux_registre`, `obj_puce`), et les répliques des accroches de combat.
- **Vérification** :
  - chaque issue des deux quêtes se termine par une partie scriptée de tests (comme `city.test.js`) ;
  - aucune issue ne demande de combat ;
  - les drapeaux d'accroche sont posés et sans effet bloquant.

## 5. Points à trancher avant ou pendant les lots [proposition]
1. Position de `a_nord` : la fiche Asia-Ground la place au bord ouest (x 0, z 18). Comme Asia-Ground est au sud de Lower-Town, ce plan la met au bord nord (x 8, z 0). Il faut corriger la fiche si c'est validé.
2. `k_est` ↔ `l_sud_est` : une ruelle de China Lake qui rejoint Lower-Town en contournant Asia-Ground. À confirmer, sinon China Lake n'a qu'une entrée.
3. Prix du barrage (20 cr) et règle de réouverture de `l_sud_est`.
4. `v_fosse` : la sortie aux Poutres est à ajouter dans la Sous-Ville (fichier `steel.js`, lot 1).
