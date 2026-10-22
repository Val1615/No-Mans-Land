# Catalogue d'assets : Dusk-Town Q1 (v2)

Rédigé le 21 octobre 2026 (heure de Paris).

**Statuts**
- **concept** : idée non produite.
- **provisoire** : intégré et fonctionnel, qualité ou cohérence à revoir.
- **intégré** : en jeu, contrôlé dans le référentiel.
- **vérifié** : contrôlé en jeu par Valentin. **Aucun asset n'a ce statut.**

**Sources**
- **fait** : produit pour ce projet (géométrie en mètres et textures peintes par code dans `game/src/render/textures.js`).
- **repris** : copié depuis `src/a/No-Mans-Land_Reconstruction/07_MAQUETTE_ARCHIVE_v0.13/dist/assets/`, rogné au canal alpha et redimensionné vers `game/assets/reused/`. Les originaux ne sont pas modifiés.

**Règle d'échelle.** Un sprite repris est dimensionné par sa **hauteur en mètres** déclarée dans `assets/reused/manifest.json`, jamais par sa taille en pixels. La collision utilise l'emprise déclarée, ou une emprise surchargée `fp` dans les données du quartier.

**Évaluation des sprites de la maquette**
- Bonne qualité picturale.
- Vue 3/4 proche de notre caméra iso (lacet 45°).
- Une seule orientation : on ne les retourne pas en miroir, conformément à la règle.
- Ils fonctionnent comme panneaux face caméra.

**Limites des sprites repris**
- Pas d'animation de marche : les personnages glissent.
- L'éclairage peint ne suit pas la lumière de la scène.
- Le pied du sprite est approximatif (bas de la boîte alpha).

## Bâtiments et sols (faits)

| Asset | Dimensions (m) | Source | Statut |
|---|---|---|---|
| Clinique | 9 × 8 × 3 | fait : façade d'abandon, porte camouflée, symbole gravé | provisoire |
| Bar Le Passage | 10 × 9 × 6 (2 étages) | fait | provisoire |
| Épicerie | 8 × 7 × 3 | fait | provisoire |
| Tour effondrée (ex-poste de milice) | 4 × 5 × 6,5 | fait, toit percé | provisoire |
| Maison de Mara (visitable) | 5 × 7 × 6 | fait, porte camouflée | provisoire |
| Maisons mitoyennes S2a / S2b | 4 × 6 × 3 et 5 × 6 × 6 | fait | provisoire |
| Ruine | 7 × 7 × 1,2 | fait. Trop proche d'une dalle : à refaire avec des pans de murs | provisoire, faible |
| Atelier (porte de garage) | 8 × 9 × 3,5 | fait | provisoire |
| Portes réelles (cadre et vantail) | 1,0 × 2,2 | fait, cliquable, contrat `DOORS` | intégré |
| Murs d'intérieur | épaisseur 0,2 ; 3 m au nord et à l'ouest, 0,9 m au sud et à l'est (vue en coupe) | fait | intégré |
| Mobilier en boîtes (lits, comptoirs, tables, armoire) | voir `dusk_q1.js` | fait, volumes unis | provisoire, à remplacer |
| Sol de quartier (bitume fissuré, sable, terre battue, herbes mortes) | 48 × 36 | fait, canvas à 24 px/m | provisoire |
| Sols intérieurs (carrelage, planches) | taille de la pièce | fait | provisoire |

## Personnages (repris, sprites)

| Id | Fichier source | Hauteur (m) | Statut |
|---|---|---|---|
| Joueur | actors-v2-0.webp | 1,80 | provisoire |
| Nilo | actors-v2-4.webp | 1,75 | provisoire |
| Mara | actor-1.webp | 1,68 | provisoire. Porte encore une arme à l'épaule : sprite civil à produire |
| Vera | city-people-v3-2.webp (blouse blanche) | 1,70 | provisoire. Trop propre pour Dusk-Town (style IO) : à salir ou à refaire |
| Hector | actors-v2-2.webp | 1,85 | provisoire, fusil (tenancier sur une route de rafles) |
| Bruno (mutant) | actor-2.webp | 1,90 | intégré, sans arme |
| Ileana (Invicta) | actors-v2-5.webp | 1,72 | provisoire, fusil cohérent pour une voyageuse |
| Anselme | actor-4.webp | 1,70 | provisoire |

Portraits de dialogue : portrait-1 (Mara), portrait-2 (Bruno), city-portrait-v3-2 (Vera), portraits-v2-0/2/4/5, portrait-4. Statut provisoire.

Civils sans arme longue en v2 : Bruno, Anselme, Vera. **Mara porte encore une arme** sur le seul sprite civil féminin disponible. **À produire** : des sprites civils sans arme.

## Accessoires (repris)

| Id | Fichier | Hauteur (m) | Emprise (m) | Statut |
|---|---|---|---|---|
| pump | props-detail-v4-2.webp | 1,6 | 1,6 × 1,2 | provisoire. Machinerie de pompage plausible, mais pas une pompe de puits à bras : à produire |
| board | props-detail-v4-4.webp | 1,9 | 1,4 × 0,3 | intégré |
| barrel | props-v2-2.webp | 0,95 | 0,6 × 0,6 | intégré |
| crate | props-v2-1.webp | 0,7 | 1,0 × 0,6 | intégré |
| bench | street-detail-v9-0.webp | 0,9 | 1,6 × 0,6 | intégré |
| lamp | street-detail-v9-4.webp | 3,2 | 0,3 (collision) | intégré |
| stall | street-detail-v9-5.webp | 2,3 | 2,0 × 1,2 | intégré |
| laundry | props-v9-0.webp | 1,9 | 2,4 × 0,3 | intégré |
| planters | props-v9-5.webp | 0,6 | 1,6 × 1,0 | intégré |
| wreck (épave) | props-v2-5.webp | 1,5 | 4,6 × 2,4 (surcharge `fp`) | provisoire, paraît petite |
| sandbags | props-v9-10.webp | retiré en v2 (plus de milice) | | retiré |
| workbench | props-v2-0.webp | 1,2 | 1,8 × 0,8 | intégré |
| tires | props-v9-20.webp | 0,8 | 1,2 × 1,0 | intégré |
| firewood | props-v9-2.webp | 1,4 | 1,8 × 0,8 | intégré |
| cart | props-v9-1.webp | 1,1 | 1,8 × 0,9 | intégré |
| rubble | props-v9-9.webp | 0,7 | 2,0 × 1,6 | intégré |
| bush | props-v9-19.webp | 1,1 | 1,0 × 1,0 | intégré |
| stove | props-v9-3.webp | 1,3 | 0,9 × 0,7 | intégré |
| kitchen | props-v6-3.webp | 1,0 | 1,6 × 0,7 | intégré |
| shelves | street-detail-v9-3.webp | 1,9 | 1,8 × 0,6 | intégré |

**Non repris** : les décors urbains IO (`city-props-v3`, bancs lumineux, voitures) sont hors sujet pour Dusk-Town. Les bâtiments raster (`settlement-v9`, `buildings-v6`) ne sont pas repris : leur échelle, leur angle et leurs portes sont incompatibles avec le contrat de porte unique.

## À produire (priorité)
1. Sprites civils marchant en 8 directions (joueur, compagnon, PNJ).
2. Pompe à bras de puits.
3. Kit de façades modulaire avec vraies menuiseries (remplace les textures peintes par code).
4. Mobilier intérieur (lits de clinique, comptoir, tables).
5. Ruine en pans de murs.
6. Sacs de sable orientés.

## Ajouts v2 (faits)
- **Porte camouflée** : planches clouées, filet de lumière, sable au pied (`hiddenDoorTexture`).
- **Symboles gravés** près des entrées : croix, bouteille, goutte, bocal.
- **Décrépitude** : briques à nu, fissures, coulures, congères de sable, toits percés, fenêtres condamnées ou crevées.
- **Sol** : 700 touffes d'herbe morte, traces de pas devant les seules vraies entrées.
- **Retirés de l'extérieur** : étal, linge, bacs, banc, deuxième réverbère, sacs de sable. Le linge et les bacs sont déplacés chez Mara.

## v3 (2026-10-21) : assets réels de la maquette et sprites générés

Règle : la géométrie reste le volume mesuré (data/dusk_q1.js, en mètres). Les images ne servent que de texture appliquée sur ses faces ; elles ne définissent jamais la taille, la collision ni la porte. Les sources restent intactes : `game/tools_assets.py` lit `src/a/.../art-source/` et écrit dans `game/assets/mockup/` et `game/assets/generated/` (reproductible).

### Inventaire des planches pertinentes (src/a/No-Mans-Land_Reconstruction/07_MAQUETTE_ARCHIVE_v0.13/art-source/)
| Fichier | Contenu | Retenu ? | Pourquoi |
|---|---|---|---|
| terrain-v4.png (3x2 tuiles 512 px) | sable, asphalte, mousse ; panneaux bleus, marbre, grille | sable, asphalte | les 2 premiers collent à Dusk-Town ; panneaux, marbre et grille sont de style IO / ville |
| terrain-nature-v4.png | terre craquelée, gravier, herbe sèche ; béton moussu, béton, pierre | terre, gravier, herbe sèche, béton | sols de ruine à échelle humaine |
| settlement-v9-dusk.png | 6 maisons de village (tuiles, enduit ocre), dont boutique à store, maison à garages, ruine en brique | maison basse, boutique, maison à garages, ruine | planche faite pour Dusk ; maison à escalier et atelier ouvert écartés (portes ouvertes peintes = faux accès) |
| buildings-v6.png | 6 bâtiments anciens en ruine (palazzo rose, halle, entrepôt, maison jaune, marché, cinéma) | palazzo rose, maison jaune | bonne patine de ruine ; halle, marché et cinéma trop monumentaux pour le quartier |
| exterior-buildings-v4.png, buildings.png | serre, cabanes, temple, bloc néon | non | style IO / néon, ou hors échelle |
| interior-wood-v10.png | parquet | oui | sol intérieur bar, Mara, épicerie |
| props-v9-*, service-v10-* | mobilier, étals | déjà utilisés en v2 (reused/) | inchangé |

### Façades redressées (vue iso -> rectangle par transformation de quadrilatère), assets/mockup/
| Asset | Source | Appliqué à | Volume mesuré (l x p x h) |
|---|---|---|---|
| cottage_s / cottage_e | settlement-v9-dusk, maison basse | Maison de Mara | 5 x 7 x 3,5 m |
| yellow_s / yellow_e | buildings-v6, maison jaune | Clinique | 9 x 8 x 6 m |
| palazzo_s / palazzo_e | buildings-v6, palazzo rose | Le Passage (bar) | 10 x 9 x 6,5 m |
| shop_s / shop_e | settlement-v9-dusk, boutique à store | Épicerie (vitrine sud condamnée par des planches peintes) | 8 x 7 x 6 m |
| ruin_s / ruin_e | settlement-v9-dusk, ruine en brique | Ruine | 7 x 7 x 3,5 m |
| garage_s | settlement-v9-dusk, maison à garages (garages condamnés) | Atelier (face sud) | 8 x 9 x 3,5 m |
| roof_tiles, roof_palazzo, roof_flat, roof_ruin | recadrages des toits des mêmes planches | toits plats des volumes | |
| g_sand, g_asphalt, g_dirt, g_gravel, g_grass, g_concrete, g_wood | tuiles de sol (1 tuile = 4 m) | sols extérieurs et intérieurs | |

Portes : les portes réelles (cadre, battant, seuil) sont posées sur la porte peinte de la façade (Mara x=4, Clinique x=13, Bar x=39,5, Épicerie z=26,5). Pas de porte peinte ailleurs sans planches.
Restent en texture procédurale : Maison A, Maison B, Tour effondrée, face est de l'Atelier reprise de cottage_e, murs intérieurs (couleur unie). Aucun bâtiment identique répété.

### Générés (GenerateImage), assets/generated/ : ce sont des assets, pas des captures du jeu
| Asset | Remplace | Hauteur | Statut |
|---|---|---|---|
| gen_mara (+ portrait) | mara (maquette) | 1,66 m | civile sans arme, seau ; provisoire |
| gen_vera (+ portrait) | vera (blouse de labo, trop IO) | 1,68 m | infirmière de terrain, tablier, sacoche à croix ; provisoire |
| gen_hector (+ portrait) | hector (fusil) | 1,82 m | barman sans arme ; provisoire |
| gen_pump | pump (machine industrielle) | 1,5 m | pompe à bras sur socle ; provisoire |
Écarts connus : angle de caméra des sprites générés un peu plus bas que celui de la maquette ; liseré rose léger possible sur les cheveux (détourage d'un fond uni).

## v4 (2026-10-21) : bâtiments = sprites entiers de la maquette (décision de Valentin)

Les volumes texturés de la v3 sont retirés. Chaque bâtiment est l'image complète de la planche, posée en billboard dans la scène 3D orthographique.
Règles (contre les défauts racines de la maquette) :
- Caméra accordée aux planches : lacet 34,5°, tangage 28,8°, mesurés sur les pentes des arêtes de base (pente face gauche ≈ 0,33, face droite ≈ 0,70). Les planches ne sont pas en 2:1 symétrique.
- Une seule échelle pour tous les bâtiments : K = 50 px d'image par mètre à l'écran (tirée de la hauteur de la porte de la maison basse, environ 2,1 m). Personnages et accessoires : hauteur réelle × cos(tangage).
- Ancre = coin de base avant (pixel opaque le plus bas), posée sur le coin monde (x+w, z+d).
- Emprise = mesurée sur l'image (extrêmes gauche/droite de la base / K), puis réduite tant qu'un coin (rentré de 0,4 m) ne tombe pas sur un pixel opaque : la collision ne dépasse jamais la base visible. Collision = cette emprise.
- Porte = pixel de la porte peinte, ramené au point monde sur la façade ; seuil à 1 m devant. Indice discret (pictogramme) posé sur la porte peinte.
- Ordre de dessin : peintre topologique par emprise (séparés sur x ou z : le plus grand est devant), seulement entre objets qui se recouvrent à l'écran.
- Occultation : un bâtiment passe à 30 % d'opacité quand un acteur est derrière lui et qu'un point de son corps (0,3, 0,9 ou 1,5 m) tombe sur un pixel opaque du sprite ; un bâtiment transparent laisse passer le clic.
- Planche exterior-buildings-v4.png écartée : projection différente (emprises réduites à 2 m sur 11 m, incohérentes).
- Reproductible : game/tools_buildings.py (lit les planches, écrit assets/buildings/ et src/data/buildings_q1.js).

| Bâtiment | Sprite (planche) | Recadrage source (px) | Ancre dans le recadrage (px) | Emprise w x d (m) | Coin min (x, z) | Porte(s) : pixel peint -> ouverture monde (seuil) |
|---|---|---|---|---|---|---|
| Maison de Mara | assets/buildings/b_mara_house.webp (settlement-v9-dusk.png) | [47, 118, 480, 482] | [287, 363] | 7.0 x 5.0 | (1.0, 8.0) | [210, 418] -> (4.99, 13.0) face sud (seuil 4.99, 14.0) |
| Clinique | assets/buildings/b_clinic.webp (buildings-v6.png) | [16, 540, 498, 970] | [324, 429] | 8.0 x 5.5 | (10.0, 7.5) | [170, 890] -> (13.87, 13.0) face sud (seuil 13.87, 14.0) |
| Épicerie | assets/buildings/b_grocery.webp (settlement-v9-dusk.png) | [566, 17, 940, 493] | [231, 475] | 5.5 x 5.0 | (20.0, 8.0) | [718, 450] -> (23.58, 13.0) face sud (seuil 23.58, 14.0); [893, 440] -> (25.5, 9.61) face est (seuil 26.5, 9.61) |
| Le Passage | assets/buildings/b_bar.webp (buildings-v6.png) | [23, 36, 475, 493] | [270, 456] | 6.5 x 6.5 | (31.0, 6.5) | [225, 460] -> (35.85, 13.0) face sud (seuil 35.85, 14.0) |
| Halle effondrée | assets/buildings/b_halle.webp (buildings-v6.png) | [514, 33, 1018, 479] | [309, 445] | 7.5 x 7.0 | (40.0, 6.0) | aucune (non visitable) |
| Maison à escalier | assets/buildings/b_house_a.webp (settlement-v9-dusk.png) | [638, 529, 1036, 981] | [201, 451] | 4.0 x 7.0 | (3.0, 24.0) | aucune (non visitable) |
| Marché couvert | assets/buildings/b_marche.webp (buildings-v6.png) | [507, 515, 1045, 981] | [345, 465] | 8.5 x 6.5 | (9.0, 24.0) | aucune (non visitable) |
| Ruine | assets/buildings/b_ruin.webp (settlement-v9-dusk.png) | [1092, 535, 1520, 984] | [324, 448] | 8.0 x 3.5 | (19.0, 25.0) | aucune (non visitable) |
| Maison aux garages | assets/buildings/b_garages.webp (settlement-v9-dusk.png) | [1041, 7, 1515, 522] | [368, 514] | 9.0 x 3.5 | (29.0, 25.0) | aucune (non visitable) |
| Entrepôt éventré | assets/buildings/b_entrepot.webp (buildings-v6.png) | [1049, 47, 1521, 489] | [323, 441] | 8.0 x 4.5 | (39.5, 25.0) | aucune (non visitable) |

Épicerie : deux portes peintes (boutique au sud, porte latérale à l'est), toutes deux réelles et menant au même intérieur (deux ouvertures dans grocery_in).
Non retenus : maison à garages ouverte (workshop), halle-entrepôt aux portes ouvertes réutilisée seulement comme Entrepôt éventré (non visitable, clic = fermé). Sols : tuiles de la maquette (inchangées depuis v3).


## v6 (2026-10-21) : intérieurs en assets réels (clinique, bar, épicerie, maison de Mara)

Exigence de Valentin : pas de volumes ni de couleurs en code dans les intérieurs. Sols et murs portent des textures réelles ; le mobilier est en sprites.
Ordre des sources : maquette (`src/a/.../art-source/`, jamais modifiée) d'abord, génération (GenerateImage) sinon. Tout est reproductible par `game/tools_interiors.py`
(lit `art-source/` et `game/art-gen/`, écrit `game/assets/interiors/` + `manifest.json` + `rapport_angles.json`). Les générations brutes sont gardées dans `game/art-gen/`
(avec `guide_v4.png`, la grille de boîtes filaires à l'angle v4 donnée en référence au générateur).

**Contrôle d'angle (rejet automatique).** Caméra v4 : l'axe x monde apparaît avec une pente de 0,33 (vers le bas-droite), l'axe z avec 0,70. Pour chaque sprite :
Hough sur les contours ; accepté si la pente dominante est dans [0,25 ; 0,42] (bande mesurée sur les 10 planches de bâtiments v4 : 0,30 à 0,40) et si moins de 12 %
des arêtes opposées sont à 0,45-0,55 (signature de la projection 2:1 classique). **Contrôle d'échelle** : la largeur écran est imposée par l'emprise en mètres
(w·0,824 + d·0,566) ; la hauteur qui en découle doit rester à ± (30 % + 0,15 m) de la hauteur réelle attendue. Un sprite « miroir » (axe long vers le bas-gauche)
est retourné pour revenir à l'orientation canonique ; son éclairage vient alors de la droite (noté). Les objets longs ne peuvent être posés que le long de l'axe x.
Limite : mesure statistique sur les contours ; elle a départagé correctement la planche témoin (meubles 2:1 de la maquette rejetés), mais reste sensible au détourage.

**Pose en jeu** (`view.js`, `furniture`) : sprite posé par son emprise (x, z = coin min, en m) ; largeur = largeur projetée de l'emprise, bas de l'image sur le coin avant.
Collision = emprise (`grid.js`). Ordre du peintre par emprise (comme dehors) ; un meuble qui cache un personnage (joueur, Nilo, PNJ en dialogue) passe à 35 %.
Murs : la texture couvre 3 m × 3 m de mur et se répète selon la taille de chaque face. Sols : texture seule, sans bruit peint.

### Retenus en jeu
| Asset | Provenance | Emprise (m) | Hauteur (m) | Où |
|---|---|---|---|---|
| f_wood | **maquette** art-source/interior-wood-v10.png | tuile 2,5 m | | sol du bar |
| f_concrete | **maquette** art-source/terrain-nature-v4.png (tuile béton) | tuile 3 m | | sol de l'épicerie |
| m_archive_shelf | **maquette** art-source/interiors-v2.png, n° 2 (étagère métallique) | 1,6 × 0,5 | 1,9 | clinique, bar, épicerie |
| m_desk | **maquette** art-source/service-v10-B.png, n° 3 (bureau métallique) | 1,5 × 0,7 | 1,0 | clinique (bureau de Vera) |
| f_tiles | généré (gen_floors_sheet, carrelage fissuré) | tuile 2 m | | sol de la clinique |
| f_earth | généré (gen_floors_sheet, terre battue) | tuile 2 m | | sol chez Mara |
| w_plaster / w_brick / w_clay / w_planks | généré (gen_walls_sheet : chaux écaillée, brique à nu, enduit d'argile, planches et tôle) | 3 m × 3 m | | murs clinique / bar / Mara / épicerie |
| door_in | généré (gen_door_in : planches clouées, écharpe, verrou, filet de lumière) | 1,0 × 2,2 | | porte de sortie des 4 intérieurs (5 ouvertures) |
| clinic_cot_b | généré (gen_sheet2) | 2,0 × 0,9 | 0,95 | clinique × 2 |
| clinic_stretcher_b | généré (gen_sheet2) | 2,0 × 0,6 | 0,6 | civière derrière la porte (accroche « rafles ») |
| clinic_cabinet | généré (gen_clinic_sheet), retourné | 0,9 × 0,5 | 1,8 | armoire à pharmacie (Vera la regarde) |
| clinic_table | généré (gen_clinic_sheet) | 1,3 × 0,7 | 1,15 | table de soins |
| bar_counter_b | généré (gen_sheet2) | 3,8 × 0,8 | 1,4 (bouteilles comprises) | comptoir d'Hector |
| bar_backshelf_b | généré (gen_sheet2) | 2,0 × 0,6 | 1,05 | étagère basse et radio derrière Hector |
| bar_table_b | généré (gen_sheet3) | 1,6 × 1,2 | 0,9 | 2 tables à tabourets |
| shop_shelf | généré (gen_grocery_sheet), retourné | 1,9 × 0,5 | 1,9 | épicerie × 2 |
| shop_counter | généré (gen_grocery_sheet) | 2,2 × 0,7 | 1,6 | comptoir et balance d'Anselme |
| home_water | généré (gen_home_sheet) | 1,3 × 0,8 | 0,75 | seaux et jerrican (Mara, épicerie) |
| home_mattress_d | généré (gen_mattress_d, objet seul) | 1,9 × 0,9 | 0,45 | paillasse chez Mara |
| home_curtain | généré (gen_home_sheet) | 2,4 × 0,15 | 2,1 | rideau derrière lequel se tient Bruno |
| home_table | généré (gen_home_sheet) | 1,7 × 1,0 | 1,0 | table et deux chaises chez Mara |

Retirés des intérieurs (mesurés et rejetés à l'angle v4, ou non mesurables) : lits, comptoirs, cuisinière, étagères et tables de la maquette (2:1),
`reused/` laundry, planters, stove, kitchen, shelves (rejetés), barrel (cylindre, angle non mesurable), toutes les boîtes de couleur (`box`) de v2-v5.
Conséquence : le linge et les bacs de culture de Mara ne sont plus à l'intérieur (aucune variante à l'angle v4) ; les sacs de rations d'Anselme et son filtre à eau
ont été rejetés trois fois chacun (générateur resté en 2:1).

### Rapport d'angle complet (`assets/interiors/rapport_angles.json`)
| Id | Source | Pente dominante | Part 2:1 opposée | Hauteur implicite / attendue (m) | Verdict |
|---|---|---|---|---|---|
| clinic_cot | généré art-gen/gen_clinic_sheet.jpg #0 | 0.5 (direct) | 0.08 | 1.47 / 0.95 | REJETÉ |
| clinic_stretcher | généré art-gen/gen_clinic_sheet.jpg #1 | 0.45 (direct) | 0 | 0.68 / 0.6 | REJETÉ |
| clinic_cabinet | généré art-gen/gen_clinic_sheet.jpg #2 | 0.25 (miroir) | 0 | 1.58 / 1.8 | accepté |
| clinic_table | généré art-gen/gen_clinic_sheet.jpg #3 | 0.35 (direct) | 0 | 0.92 / 1.15 | accepté |
| bar_counter | généré art-gen/gen_bar_sheet.jpg #0 | 0.5 (direct) | 0.03 | 2.12 / 1.35 | REJETÉ |
| bar_backshelf | généré art-gen/gen_bar_sheet.jpg #1 | 0.4 (direct) | 0 | 1.46 / 2.1 | **non exporté** : pan de mur en ruine peint avec l étagère : double le vrai mur, remplacé par bar_backshelf_b |
| bar_table | généré art-gen/gen_bar_sheet.jpg #2 | 0.5 (direct) | 0.25 | 0.65 / 0.9 | REJETÉ |
| bar_reel | généré art-gen/gen_bar_sheet.jpg #3 | 0.6 (miroir) | 0.04 | 0.65 / 0.85 | REJETÉ |
| shop_shelf | généré art-gen/gen_grocery_sheet.jpg #0 | 0.35 (miroir) | 0.02 | 1.93 / 1.9 | accepté |
| shop_counter | généré art-gen/gen_grocery_sheet.jpg #1 | 0.35 (direct) | 0.02 | 1.35 / 1.6 | accepté |
| shop_filter | généré art-gen/gen_grocery_sheet.jpg #2 | 0.5 (miroir) | 0.15 | 1.56 / 1.4 | REJETÉ |
| shop_sacks | généré art-gen/gen_grocery_sheet.jpg #3 | 0.5 (direct) | 0.29 | 0.88 / 1.1 | REJETÉ |
| home_mattress | généré art-gen/gen_home_sheet.jpg #0 | 0.5 (direct) | 0 | 0.47 / 0.35 | REJETÉ |
| home_curtain | généré art-gen/gen_home_sheet.jpg #1 | 0.4 (direct) | 0 | 2.05 / 2.1 | accepté |
| home_table | généré art-gen/gen_home_sheet.jpg #2 | 0.4 (direct) | 0 | 0.62 / 1.0 | accepté |
| home_water | généré art-gen/gen_home_sheet.jpg #3 | 0.35 (direct) | 0 | 0.66 / 0.75 | accepté |
| bar_counter_b | généré art-gen/gen_sheet2.jpg #0 | 0.3 (direct) | 0.11 | 1.73 / 1.4 | accepté |
| bar_backshelf_b | généré art-gen/gen_sheet2.jpg #1 | 0.35 (direct) | 0 | 0.96 / 1.05 | accepté |
| clinic_cot_b | généré art-gen/gen_sheet2.jpg #2 | 0.4 (direct) | 0 | 0.73 / 0.95 | accepté |
| clinic_stretcher_b | généré art-gen/gen_sheet2.jpg #3 | 0.4 (direct) | 0.06 | 0.48 / 0.6 | accepté |
| home_mattress_b | généré art-gen/gen_sheet3.jpg #0 | 0.5 (direct) | 0.02 | 1.0 / 0.35 | REJETÉ |
| bar_table_b | généré art-gen/gen_sheet3.jpg #1 | 0.35 (direct) | 0.05 | 0.79 / 0.9 | accepté |
| shop_filter_b | généré art-gen/gen_sheet3.jpg #2 | 0.45 (direct) | 0.1 | 1.21 / 1.4 | REJETÉ |
| shop_sacks_b | généré art-gen/gen_sheet3.jpg #3 | 0.45 (direct) | 0.16 | 0.77 / 1.0 | REJETÉ |
| clinic_cot_c | généré art-gen/gen_sheet4.jpg #0 | 0.45 (direct) | 0.07 | 0.96 / 0.95 | REJETÉ |
| home_mattress_c | généré art-gen/gen_sheet4.jpg #1 | 0.5 (direct) | 0.09 | 0.4 / 0.35 | REJETÉ |
| shop_filter_c | généré art-gen/gen_sheet4.jpg #2 | 0.5 (direct) | 0.07 | 0.79 / 1.2 | REJETÉ |
| shop_sacks_c | généré art-gen/gen_sheet4.jpg #3 | 0.45 (direct) | 0 | 0.64 / 1.0 | REJETÉ |
| home_mattress_d | généré art-gen/gen_mattress_d.jpg #-1 | 0.4 (direct) | 0 | 0.35 / 0.45 | accepté |
| m_archive_shelf | maquette art-source/interiors-v2.png #2 | 0.4 (direct) | 0.05 | 1.81 / 1.9 | accepté |
| m_desk | maquette art-source/service-v10-B.png #3 | 0.25 (direct) | 0 | 1.03 / 1.0 | accepté |
| m_locker | maquette art-source/service-v10-B.png #5 | 0.35 (direct) | 0.21 | 1.48 / 1.9 | REJETÉ |
| m_stove | maquette art-source/props-v9-domestic.png #3 | 0.3 (miroir) | 0.15 | 1.1 / 1.3 | REJETÉ |
| m_cooktable | maquette art-source/Props-v6.png #3 | 0.45 (direct) | 0.16 | 1.07 / 1.0 | REJETÉ |
| m_bed | maquette art-source/interiors-v2.png #0 | 0.5 (direct) | 0 | 1.03 / 0.9 | REJETÉ |
| m_bar_counter | maquette art-source/service-v10-A.png #0 | 0.45 (direct) | 0 | 1.73 / 1.2 | REJETÉ |
| m_shop_shelf | maquette art-source/service-v10-A.png #1 | 0.45 (direct) | 0 | 1.62 / 1.9 | REJETÉ |
| m_medchair | maquette art-source/service-v10-A.png #5 | 0.55 (direct) | 0 | 1.21 / 1.6 | REJETÉ |
| m_desk2 | maquette art-source/interiors-v2.png #3 | 0.45 (direct) | 0.05 | 0.88 / 1.0 | REJETÉ |

## v7 (2026-10-21) : toute la ville (Le Transit, Le Scellé, Les Sables)

Plan et fiches : `quartiers/DUSK_TOWN_PLAN.md`. Même ordre des sources : maquette d'abord, génération sinon, contrôle d'angle `judge()` de `tools_interiors.py`.

**Bâtiments.** `tools_buildings.py` est passé en multi-quartiers : `CELLS` (un sprite par case de planche, recadrage et emprise mesurés une seule fois) et `DISTRICTS`
(placement par quartier). Sortie : `src/data/buildings_q1.js` (identique octet pour octet à la v6, vérifié par diff) et `src/data/buildings_town.js`.
Les planches dusk de la maquette n'ont que 12 bâtiments : les 10 de La Pompe sont réutilisés dans les autres quartiers, **jamais deux fois dans le même quartier**,
jamais en miroir. Les rangées et les voisinages changent d'un quartier à l'autre.
| Sprite | Provenance | Emprise (m) | Quartiers |
|---|---|---|---|
| b_cinema | **maquette** buildings-v6.png, case (2,1), seule case dusk encore inutilisée | 8 × 4,5 | Transit (cinéma muré), Sables (cinéma ensablé) |
| b_lab | **généré** (`art-gen/gen_lab_bunker.jpg` : blockhaus de béton, porte d'acier soudée, pochoir « HUMAN CORPORATION »). Aucune case de la maquette ne convient : les bâtiments de `settlement-v9-city` sont rejetés par `judge` (projection 2:1 ou miroir) ou trop « Steel » (néons). 1er essai rejeté à l'œil (face est à 0,3 au lieu de 0,7) ; 2e accepté (pente dominante 0,30, 2:1 opposée 0,00). Mis à l'échelle K = 50 px/m d'après l'emprise voulue (× 0,347) | 6 × 3,5 | Scellé |
| b_house_a, b_garages, b_mara_house, … (10) | maquette, déjà au catalogue v4 | inchangées | voir DUSK_TOWN_PLAN.md § 4 |
Portes peintes nouvelles (pixel source → ouverture monde) : maison à escalier, porte du bas (713, 919, face sud) ; maison aux garages, petite porte latérale (1453, 487, face est).

**Personnages générés** (`tools_npcs_v7.py`, même détourage que `tools_assets.py`, portrait recadré) : `gen_teo` (1,70 m), `gen_ezequiel` (1,78 m), `gen_sol` (1,80 m ; 1er essai écarté : trop proche de Mara).

**Intérieurs** (guet, atelier, citerne) : uniquement des meubles et textures déjà contrôlés en v6 (aucun nouvel asset d'intérieur).

**Écartés v7** : scenery-waste-v4 (bus, mur, pylône, arbre, tuyau, sacs : 0/6 accepté), landmarks-v4 (navire et wagonnet acceptés en pente mais en miroir, les autres rejetés), utility-v9 (1/6, écran, sans usage), settlement-v9-city (néons de Steel, hors ton Dusk), settlement-v9-dusk case (0,1) atelier ouvert (projection différente, déjà écarté en v4).

## v9 : audio
| Fichier | Origine | Usage |
|---|---|---|
| `game/assets/audio/dusk_town_ambiance.mp3` | fourni par Valentin (`incoming/dusk_town_ambiance.mp3`), copié tel quel, SHA-256 `ae1d8ee965840781fa5c5ed46f8489d34bdf70a10ec461ffb1ec0788ca166b12` | musique d'ambiance, 4 quartiers + intérieurs |

## v15 (2026-10-22) : finitions visuelles (branche `creation/finitions-visuelles`)

Script : `tools_finitions.py` (n'écrit rien dans `src/`). Toutes les images nouvelles sont **générées** (GenerateImage), sources gardées dans `art-gen/`.
| Asset | Provenance | Contrôle |
|---|---|---|
| `buildings/b_st_porte2.webp` | **généré** `art-gen/gen_steel_gate3_raw.jpg` (référence : `gen_steel_gate2.jpg`, même angle v4), fond vert uni. Dôme entier ; marge haute brute 4,7 % portée à 18 % par ajout de 140 px de fond uni en haut (`gen_steel_gate3.jpg`). Détourage `key_green` de `tools_steel.py`, échelle K (× 1,10 pour que l'arche ait la taille de l'ancien sprite). Ancre recalée par corrélation sur l'arche de l'ancien sprite (score 0,73) : l'image ne grandit que vers le haut. Manifeste : px 1640 × 1084, crop [10, 10, 1650, 1094], ancre [1491, 1067] (coin bas détecté [1527, 1083]), emprise 30 × 8 inchangée | capture `nml-shots/v2/apres_porte_dome*.png` |
| `generated/st_projecteur.webp` | même source (`gen_fort_sheet.jpg` #3) ; matte refait : alpha durci, érosion 1 px, bord (1 px) recoloré depuis les voisins opaques, despill magenta sur la bande de bord | pixels de bord magenta 4,53 % → 0,03 % |
| `buildings/b_st_ct_dome.webp` | sprite v14 d'origine (`art-gen/matte-src/b_st_ct_dome_v14.webp`) ; même matte (érosion 2 px, bande 3 px), trous intérieurs bouchés ; néons violets intérieurs intacts | pixels de bord magenta 5,06 % → 0,02 % |
| `interiors/sv_cardtable_b.webp` (rév. 2) | **généré** `art-gen/gen_sv_cardtable5.jpg` : tapis vert, cartes, jetons, pieds en caisses, lampe conique suspendue (halo repeint en jaune chaud : le vert du fond restait dans le dégradé). Pieds trop longs à la génération (1,68 m implicite) : bande horizontale de 280 px retirée dans les pieds seulement. Angle mesuré sur l'enveloppe convexe des pieds (0,66/0,66 → 0,33/0,70), lampe hors calcul. Accepté, hauteur implicite 0,94 / 0,9 m. Écartés : `gen_sv_cardtable4.jpg` (0,37 m, trop basse), `gen_sv_cardtable3.jpg` (rév. 1, bloc de caisses peu lisible) | `nml-shots/v2/apres_tripot_table.png` |
| ~~rév. 1~~ | `art-gen/gen_sv_cardtable3.jpg` : table de jeu rectangulaire sur caisses, cartes et jetons, sans tabouret. 1er essai `gen_sv_cardtable2.jpg` écarté (trop bas : hauteur implicite 0,46 m pour 0,9). Angle corrigé `v4fix` (pentes 0,76/0,78 → 0,33/0,70) | `rapport_angles.json` : accepté (arête basse v4), hauteur implicite 0,84 / 0,9 m, emprise 1,2 × 1,2 |
| `portraits/portraits-v3-mutant-0..2.webp`, `portraits-v3-cyborg-0..2.webp` | **générés** (`art-gen/portraits-v3/*.jpg`, 1024 → 480 px), cadrage buste, lumière chaude ; références : `Population-Mutants.png` / `Population-Cyborgs.png` (roman-docs) et `portraits-v2-0`. Mutants : homme ~55 ans (excroissances osseuses), femme ~20 ans (peau marbrée, nodules), aînée ~70 ans (cicatrices, talisman). Cyborgs : femme ~35 ans cadre d'IO (céramique blanche et or), officier ~45 ans (plaques graphite, capteurs rouges), déserteur ~60 ans (chrome usé, foulard rouge). 1er essai mutant-0 écarté (copie de portraits-v2-0). Rév. 2 : mutant-1 (capuche, clé à molette), mutant-2 (aînée, excroissances calcifiées, yeux laiteux), cyborg-1 (bras croisés, fond brun chaud), cyborg-2 (capuche, câbles, fer à souder) régénérés : plus aucun fusil à l'épaule | planche `nml-shots/v2/portraits_v3_planche.png` |

## Asia-Ground — lot 1 (branche `creation/asia-ground-sprites`, 2026-10-22)

Source : `PLAN_IMPLEMENTATION.md` §2, fiche `ASIA_GROUND.md`, planche validée `art-gen/concepts/quartier_asia_ground_*` (nml-quartiers). Pipeline `tools_asiaground.py` (dérivé de `tools_lowertown.py`) : fond vert, `key_green_obj` + despill de bord, `v4fix`, `keystone` auto, `judge`, 50 px/m, pivot = coin avant bas géométrique. Rapport : `assets/buildings/rapport_angles_asiaground.json`. Planche : `nml-shots/asiaground_sprites.png` (planche d'assets, pas une capture). Canon : enseignes bilingues lisibles, pas de pagode, pas de rose, un seul cyan (`ag_neon_io`).

| id | origine | source | emprise m | h m | px | pivot | judge | arête basse v4 | h implicite |
|---|---|---|---|---|---|---|---|---|---|
| `ag_restaurant` (« Chez Lin 林记 ») | **généré** | `art-gen/gen_ag_restaurant.jpg` | 8 × 6 | 10 | 500×569 | [330, 568] | oui | True | 7.77 |
| `ag_restaurant_b` | **généré** | `art-gen/gen_ag_restaurant_b.jpg` | 8 × 6 | 10 | 500×667 | [330, 666] | oui | True | 10.02 |
| `ag_halle_module` | **généré** | `art-gen/gen_ag_halle_module.jpg` | 8 × 16 | 3 | 783×551 | [330, 550] | oui | True | 2.84 |
| `ag_boutique` | **généré** | `art-gen/gen_ag_boutique.jpg` | 6 × 5 | 4 | 389×330 | [247, 329] | oui | True | 3.41 |
| `ag_boutique_b` (rév. 2) | **généré** | `art-gen/gen_ag_boutique_b2.jpg` | 6 × 5 | 4 | 389×325 | [247, 324] | oui | True | 3.29 |
| `ag_bureau` | **généré** | `art-gen/gen_ag_bureau.jpg` | 6 × 5 | 7 | 389×440 | [247, 439] | oui | True | 5.92 |
| `ag_escalier` | **généré** | `art-gen/gen_ag_escalier.jpg` | 8 × 14 | 10 | 726×866 | [330, 865] | oui | True | 10.93 |
| `ag_monte_charge` | **généré** | `art-gen/gen_ag_monte_charge.jpg` | 4 × 4 | 9 | 278×545 | [165, 544] | oui | True | 9.39 |
| `ag_stand_nouilles` | **généré** | `art-gen/gen_ag_stand_nouilles.jpg` | 2.5 × 1.5 | 2.5 | 145×164 | [103, 163] | oui | True | 2.28 |
| `ag_stand_poisson` (rév. 2) | **généré** | `art-gen/gen_ag_stand_poisson.jpg` | 3.5 × 3 | 1.1 | 229×154 | [144, 153] | oui | True | 1.08 |
| `ag_stand_pieces` | **maquette** | `reference/maquette/No-Mans-Land_Reconstruction/07_MAQUETTE_ARCHIVE_v0.13/art-source/street-detail-v9.png 1038,520,1499,988` | 4 × 2 | 2.2 | 221×182 | [165, 181] | oui | True | 1.99 |
| `ag_lanterne_cable` | **généré** | `art-gen/gen_ag_lanterne_cable.jpg` | 5 × 1 | 3 | 234×212 | [206, 211] | oui | True | 2.84 |
| `ag_auvent` | **généré** | `art-gen/gen_ag_auvent.jpg` | 5 × 2.5 | 2.4 | 277×218 | [206, 217] | oui | True | 2.29 |
| `ag_caisses_legumes` (rév. 2) | **généré** | `art-gen/gen_ag_caisses_legumes.jpg` | 1.2 × 0.8 | 0.7 | 72×48 | [49, 47] | oui | True | 0.36 |
| `ag_glaciere` | **généré** | `art-gen/gen_ag_glaciere.jpg` | 1 × 0.6 | 0.9 | 58×57 | [41, 56] | oui | True | 0.72 |
| `ag_wok` (rév. 2) | **généré** | `art-gen/gen_ag_wok2.jpg` | 1 × 1 | 0.9 | 70×71 | [41, 70] | oui | True | 0.86 |
| `ag_chariot` | **maquette** | `reference/maquette/No-Mans-Land_Reconstruction/07_MAQUETTE_ARCHIVE_v0.13/art-source/props-v9-domestic.png 554,127,1009,432` | 1.8 × 0.9 | 1 | 100×49 | [74, 48] | oui | True | 0.15 |
| `ag_hautparleur_io` | **généré** | `art-gen/gen_ag_hautparleur_io.jpg` | 0.6 × 0.6 | 4.5 | 42×166 | [25, 165] | oui | None | 3.33 |
| `ag_neon_io` | **généré** | `art-gen/gen_ag_neon_io.jpg` | 1.2 × 0.3 | 1 | 58×57 | [49, 56] | oui | False | 0.79 |

Maquette réutilisée (origine `reference/maquette/No-Mans-Land_Reconstruction/07_MAQUETTE_ARCHIVE_v0.13/art-source/`, étalonnage nuit) : `ag_stand_pieces` (street-detail-v9), `ag_chariot` (props-v9-domestic). Rév. 2 : `ag_boutique_b` enseigne corrigée ÉLECTRONIQUE 电器 (retouche par régénération de la même image, `gen_ag_boutique_b2.jpg`, mêmes px/pivot en largeur, hauteur 331 → 325 px) ; `ag_stand_poisson` régénéré sur socle (la version maquette Props-v6, écrasée par le cisaillement, est abandonnée) ; `ag_wok` posé sur une plaque carrée rivetée (arêtes v4 mesurables) ; `ag_caisses_legumes` despill limité à la bande de bord, verts des légumes conservés. Réserve restante : `ag_chariot` hauteur implicite non significative (objet bas et long).
