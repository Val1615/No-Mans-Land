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
