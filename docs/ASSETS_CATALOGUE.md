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
