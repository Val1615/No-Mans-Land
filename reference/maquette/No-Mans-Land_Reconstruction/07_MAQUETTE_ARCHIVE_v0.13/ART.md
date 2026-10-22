# Direction et fabrication des assets

Tous les assets illustrés ont été créés avec l’outil intégré imagegen, puis uniquement recadrés en sprites et convertis en WebP pour le chargement. Aucune API externe ni ressource Fallout.

## Panorama · assets/title.webp

Brief : vue panoramique sur les terres sud-américaines détruites en 2175, ciel d’hiver nucléaire, sarcophage métallique gigantesque de Steel-Megalopolis aux lueurs cyan, carcasse d’un Mecha-Colossus au premier plan et silhouette de vagabond. Rendu peint/pré-rendu 3D de RPG des années 1990, rouille ocre, gris pétrole, noir, cyan retenu. Aucun texte ni logo.

## Bâtiments · assets/building-0.webp à building-5.webp

Brief : atlas transparent 3 colonnes × 2 lignes, objets isolés en vue isométrique sud-est 2:1, détails réalistes de RPG pré-rendu des années 1990. Ordre : clinique délabrée en béton, marché de ferraille et tôles de Junk-Burgh, immeuble corporatiste cyberpunk IO, station industrielle avec turbines et tuyaux, ruines municipales de Buenos Aires, temple ancien. Sans sol, socle, textes, chiffres ni éléments hors de leur cellule. Les débordements effectifs ont été pris en compte dans les rectangles de recadrage.

## Acteurs · assets/actor-0.webp à actor-5.webp

Brief : atlas transparent 3 × 2, silhouettes plein pied isométriques vues légèrement du dessus, 3/4 sud-est, proportions humaines et rendu cohérent avec les bâtiments. Ordre : vagabond au manteau et fusil ; récupératrice et sac ; mutant humanoïde vêtu ; agent IO en armure à accents cyan ; marchand en veste marron ; drone flottant compact. Les portraits 0 à 4 sont des recadrages des acteurs correspondants.

## Titan · assets/titan.webp

Prompt final : One isolated transparent isometric game sprite of a gigantic fallen military robot for the original post-apocalyptic CRPG No Man’s Land. Massive Mecha-Colossus collapsed on its side, lying diagonally across the image. Recognizable armored head with dead optical visor, huge ripped-open ribcage-like mechanical torso, two articulated arms and two colossal mechanical legs. One arm stretches forward, a shattered leg bends back. Severed cables, broken armor, dislocated joints. Tiny hatches, crew access doors, ladders and narrow attached maintenance catwalks imply an internal crew of ten and enormous scale. Unmistakably a collapsed humanoid robot, not a building or factory. Elevated southeast 2:1 isometric camera showing top and side. Complete wide landscape sprite. Highly detailed late-1990s pre-rendered 3D CRPG style, gritty tangible surfaces, muted rust ochre, bronze, petrol gray, coal black, corroded industrial armor. Major shapes readable at small scale. True transparent alpha background. No ground, terrain, pedestal, floor, sky, frame, explosion, fire, smoke, figurines, text, logo or watermark.

## Atlas · assets/world-map.svg et world-map-labeled.svg

Cartographie vectorielle déterministe et non générée : disposition basée sur les croquis de Valentin. La précision des positions interactives est conservée en HTML ; le SVG sans étiquettes interactives sert de fond. Le second SVG est l’atlas autonome téléchargeable.

## Passe 0.2 — nouveaux assets

Outil intégré imagegen, cinq nouveaux atlases 1536 × 1024. Originaux dans `art-source/`. Recadrages individuels WebP dans `dist/assets/`, sans remplacement des originaux v1.

- `portraits-v2-0.webp` à `portraits-v2-5.webp` : six portraits adultes épaules, fond olive sombre, identités et vêtements distincts : homme brun barbu en manteau brun, femme cheveux courts noirs et écharpe rouge, homme noir rasé en veste kaki, femme mate cheveux argentés et manteau bordeaux, homme asiatique cheveux attachés et veste gris pétrole, femme noire tressée et cicatrice en manteau sable. Rendu détaillé de RPG pré-rendu des années 1990, aucun texte ni cadre.
- `actors-v2-0.webp` à `actors-v2-5.webp` : les six mêmes identités et costumes, références visuelles des portraits fournies à imagegen. Personnages plein pied vus légèrement du dessus, trois-quarts sud-est, armes baissées, arrière-plan transparent. Pose prête au départ, proportions naturelles.
- `props-v2-0.webp` à `props-v2-5.webp` : établi de réparation, coffre industriel, baril rouillé, terminal IO, caisse d’armement et voiture abandonnée. Objets isolés, alpha, isométrie sud-est 2:1, matériaux usés, palette rouille/olive/gris pétrole. Aucun texte ni socle.
- `interiors-v2-0.webp` à `interiors-v2-5.webp` : lit de clinique métallique et drap usé, chariot médical, rayonnage de dossiers/livres, bureau et contrats, petit générateur cuivre/tuyaux, fauteuil d’attente. Même cadrage et rendu. Les fragments d’objets voisins dus aux cellules chevauchantes ont été exclus par extraction des composantes alpha des sprites.

- `items-v2-0.webp` à `items-v2-5.webp` : pistolet de récupération, carabine artisanale, émetteur laser IO cyan, couteau de ferrailleur, trousse de secours verte à croix crème, grenade rouillée. Objets isolés en trois-quarts, rendu détaillé assorti au terrain, alpha, aucune marque ni inscription. Ils servent à l’inventaire, aux commerces et à la barre d’actions.

Le HUD, les autres icônes de commande, la minicarte et le circuit de piratage restent vectoriels et pilotés par le moteur. Les captures de RPG consultées ont servi de référence de lisibilité ; elles ne sont pas distribuées.

## Passe 0.3 — Steel-Megalopolis

Quatre nouveaux atlases originaux, générés avec imagegen et conservés dans `art-source/` :

- `city-v3.png` : tours résidentielles reliées par une passerelle, galerie commerciale magenta/cyan, clinique blanche, tour corporatiste verre/noir/or, industrie entretenue, poste SMPD bleu. Isométrie sud-est 2:1, rendu détaillé de RPG pré-rendu, objets isolés alpha, aucun texte, aucune ruine.
- `city-props-v3.png` : kiosque holographique, lampadaire, arbre en bac, berline électrique, banc métal/verre, borne de transport. Acier propre, céramique, lumière cyan.
- `city-upper-v3.png` : pavillon grec modernisé et tour cylindrique IO, marbre blanc, verre, or et jardins intégrés. Cette direction vient des descriptions du roman ; le ciel synthétique et l’éclairage du terrain sont pilotés par le moteur.
- `city-people-v3.png` : agent de transport, technicienne, médecin, employée des archives, cadre en tenue crème, cyborg blanc et or. Citoyens adultes sans armes ni sacs de voyage. Portraits recadrés sur les mêmes visages pour conserver la correspondance avec les silhouettes.

26 recadrages WebP supplémentaires : 8 bâtiments, 6 accessoires, 6 acteurs et 6 portraits. Les composantes alpha isolent les sprites lorsque les cellules de l’atlas se chevauchent.

Les cartes `steel-perimeter.svg`, `steel-lower.svg`, `steel-center.svg`, `steel-upper.svg` et l’atlas complet étiqueté `steel-atlas.svg` sont dessinés de manière déterministe par `tools/city-map.py`. Le périmètre reprend les douanes, avant-postes, industries, routes et sarcophage de la maquette fournie. Les cartes des niveaux sont des projections de desserte, non des plans topographiques exacts. Les étiquettes et positions interactives utilisent les mêmes coordonnées que l’export.


## Passe 0.4 — implantation et matériaux

Les 32 lieux utilisent désormais des plans distincts dans `dist/scenes.js`, sans implantation générique de bâtiments ni tirage aléatoire des accessoires. Les empreintes, routes, regroupements de mobilier et contacts sont spécifiés par lieu. Le hasard déterministe ne sert qu’aux nuances de sol, aux fissures et aux rides de l’eau.

Originaux imagegen dans `art-source/`, recadrés en WebP avec extraction des composantes alpha :

- `terrain-v4.png` : sable, chaussée poussiéreuse, verre vitrifié noir verdâtre, pavement municipal, marbre et caillebotis.
- `terrain-nature-v4.png` : terre sèche, gravier, herbes sèches, boue saline, béton sale et pierre moussue. Les surfaces forestières et jardins sont modulés en couleur par le moteur.
- `scenery-waste-v4.png` : autobus effondré, pan de mur, pylône tombé, arbre mort, conduite ouverte et barricade.
- `scenery-city-v4.png` : échoppe, distributeurs, benne, climatiseurs, jardinière et abri de transport.
- `exterior-buildings-v4.png` : serre, habitations de tôle, maison de Dusk-Town, entrepôt, sanctuaire ruiné et baraquement préfabriqué.
- `landmarks-v4.png` : épave côtière, grue, citerne sur pieds, wagonnet, conteneur et antenne.
- `props-detail-v4.png` : affleurement de verre vitrifié, entrée de mine, pompe, autel, tableau d’affichage et barrière. Le verre demeure sombre et minéral, sans lave ni cristal fantastique.
- `forest-tree-v4.png` : arbre naturel sans bac.
- `titan-prone-v4.png` : Mecha-Colossus face contre terre, bras étendus, jambes en arrière, brèche de maintenance visible sur le flanc. Remplace le précédent sprite latéral.

Soit 44 fichiers WebP supplémentaires. Les grands bâtiments possèdent tous un sprite dédié ; les petits accessoires de signalisation, clôtures, câbles et raccords peuvent encore être dessinés en Canvas. Aucun intérieur n’est promis pour les bâtiments sans porte interactive.

La passe de fidélité s’appuie sur le lore fourni et le manuscrit *Un réveil tardif* : périmètre aride ; lac pollué et lanternes de China Lake ; habitat précaire sous les fondations ; quatre tours Arcadius ; Titan au nord ; ancienne mine au rebord de Big Larry, sans implantation permanente sur l’impact. Les PNJ locaux restent des créations pour 2175. Le laboratoire sous Dusk-Town décrit dans l’intrigue de 2202 n’est pas ouvert dans ce jeu.

`steel-under.svg` ajoute la projection des fondations. L’export `steel-atlas.svg` regroupe désormais cinq planches. Les cartes restent des schémas de desserte ; les plans de terrain sont ceux de `scenes.js`.

Validation : tests de navigation sur tous les contacts et sorties, obstacles des plans d’eau, conservation des anciens états de combat, modèles présents et rendus offline du code Canvas. Ces images ne constituent pas une vérification de navigateur ni du tactile.


## Passe 0.5 — cases régionales

La grille logique et les cellules cliquables suivent les cases de 50 unités du SVG : 22 colonnes, 20 lignes, 167 cases terrestres accessibles. Le contour continental, le calcul des routes et les atlas SVG partagent désormais la même source `CONTINENT` de `world.js`. Les déplacements diagonaux ne coupent pas les angles marins. La position du temple sur la rive occidentale dispose d’un passage terrestre dans le contour corrigé.

Les terrains de halte réutilisent les assets originaux déjà présents. Quatre compositions de piste, érosion et débris sont tournées suivant une graine conservée par partie ; les accessoires d’un même groupe restent ensemble. Le milieu ajoute les lisières forestières, les plaques de verre des retombées, le piémont ou le rivage. Les rencontres ajoutent leurs véhicules, abris, personnages, coffrets ou positions hostiles. Les villes conservent leurs plans écrits à la main.

L’atlas HTML superpose des boutons de case, l’itinéraire et la position au SVG. Sur les petits écrans, la carte est parcourable par défilement et un sélecteur colonne/ligne permet de viser une case sans dépendre de la précision du toucher. `render-world.mjs` vérifie les coordonnées et `render-scene.mjs wild-8-4 --event=caravan` produit un rendu offline du terrain de rencontre. Ces contrôles ne valident pas la mise en page réelle d’un navigateur.


## Passe 0.6 — extension écrite des terrains

Deux nouveaux atlas originaux, conservés dans `art-source`, fournissent douze WebP : six bâtiments (immeuble ancien, gare, atelier du tram, dispensaire, halle, cinéma Art déco) et six accessoires (tram déraillé, poissonnerie, atelier, cuisine commune, moteur/pompe, mémorial). Les découpes conservent les contours transparents et ne réemploient aucune ressource d’un autre jeu.

Les 37 lieux fixes passent à 50 × 50 cases. Les maisons, cours de service, distributions de repas, dépôts de marchandises et zones de contrôle ont des coordonnées explicites. Big Larry reste un impact inhabité. Les douanes, les industries et les postes extérieurs restent désertiques ; la ville protégée conserve ses matériaux et son éclairage propres. Buenos Aires reçoit cinq plans et un cinéma intérieur, avec une carte schématique originale téléchargeable.

Les sept compositions géographiques de halte sont réutilisées entre cases, sans rotation ni placement aléatoire. Seuls les événements peuvent être sélectionnés aléatoirement ; ils ajoutent un groupe fixé de véhicules, habitants ou combattants. Les 167 cases ne sont pas 167 niveaux uniques. Les variations fines de matériau restent des textures de sol, sans ajout de décor.

Les références discrètes se limitent à un essai de protection dans un réfrigérateur et à un bulletin de cinéma daté du 17 mars. Aucun personnage ni titre d’œuvre n’est cité.

Les portes n’ajoutent plus un cadre indépendant dans la rue : leur repère visuel et leur zone de clic suivent le sprite du bâtiment ou celui du Titan. Une vérification numérique contrôle les quatre accès ; leurs points d’approche restent à moins de 40 pixels monde de l’ancrage. Le Titan conserve un cœur isolé, sans promesse de le relancer.

## Références et interface — 0.7

Les six planches de Valentin sont conservées en WebP sous `reference-*-v7.webp` pour le codex. Elles sont converties sans retouche ni découpage. Elles guident les populations, les matières et les factions ; elles ne servent pas de boutons raster. L’interface est du HTML/CSS interactif construit à partir des dix maquettes du dossier, avec des tailles de texte et une palette centralisées. `atlas-blueprints.json` conserve les 44 plans sources du dossier de conception ; le lecteur de l’atelier utilise leurs coordonnées exactes.

`dusk-v7.js` contient trois plans fixes distincts pour les usages des services, des cours et des ateliers. Chaque bâtiment dispose d’une emprise explicite ; `footprintFit` ajuste le modèle entier à cette emprise. Aucun générateur de remplissage n’est introduit. Les trois rendus Canvas ont été inspectés. La visite de la clinique est conservée ; les nouveaux intérieurs attendent des plans et modèles propres.

## Interface et atlas — 0.8

Références de composition : M01/M02 pour le terrain et le dock ; M03 pour le combat ; M04 pour les dialogues ; M05 pour l’inventaire ; M06 pour la mise en scène du personnage ; M07 pour la carte. La composition mobile est adaptée sans reproduire des fenêtres de bureau à largeur réduite. Le cadre est `dist/assets/ui-frame.svg`. Les fontes locales Nimbus Sans Narrow sont livrées avec leur licence dans `dist/assets/FONT-LICENSE.txt`.

Le fond de relief a été créé avec l’outil de génération d’images intégré, puis enregistré dans `dist/assets/atlas-terrain-v8.webp`. Il sert de matière visuelle. Le contour, les cours d’eau décoratifs, les routes et les repères restent dans `dist/assets/world-map-v8.svg`, avec les coordonnées de la carte existante. Le fichier consommé par le jeu est `dist/assets/world-map-v8.webp`, rasterisé depuis le SVG par Inkscape pour éviter les différences de prise en charge des images incorporées entre moteurs SVG. Ce fond ne contient ni villes ni marqueurs interactifs : ces éléments sont superposés par `world-atlas.js`.

Prompt de l’asset généré : « Decorative top-down terrain texture beneath a precise RPG map overlay. Richly painted satellite-view land surface, no labels, text, icons, symbols, roads, cities, borders, grid, coast or ocean. Entire image is land. Rugged mountain cordillera follows a diagonal arc from 18%/24% through 38%/48% and 56%/71% to 81%/94%, with branching gullies, pale rock and occasional snow. Dry tan and ochre plateaus above and to the right, eroded ravines and muted olive scrub toward the lower right. Mature post-apocalyptic atlas art, restrained realistic painterly terrain, warm weathered earth, deep gray-green shadows, orthographic bird’s-eye view, no large circular crater. »

Le fond final et le cadre ont été inspectés comme éléments graphiques. La vérification de la mise en page CSS reste distincte ; les tests DOM ne la prouvent pas.


## Construction des villes — 0.9

55 nouveaux sprites transparents sont intégrés : 18 bâtiments `settlement-v9-*`, 24 décors `props-v9-*`, 6 utilitaires `utility-v9-*`, 6 éléments de rue `street-detail-v9-*` et `skybridge-v9.webp`. Les sources et leurs manifests sont conservés dans `art-source`. Les prompts exacts et le mode intégré image_gen sont consignés dans `art-source/settlement-v9-prompts.md` et `art-source/props-v9-prompts.md`. Les découpes WebP conservent alpha et RGB visibles de l’original, sans repeindre les images.

La précédente mention de `footprintFit` en 0.7 décrivait l’étirement du bâtiment sur sa parcelle. La reconstruction 0.9 distingue les emprises physiques, les cours et les aires de service. Les nouvelles emprises sont plus petites à Dusk-Town ; le rendu se cale sur la structure. Les ancrages d’entrée et les variantes retournées utilisent la même géométrie. Les cubes de remplacement de bâtiments et les formes de substitution des accessoires sont supprimés ; des effets de sol et des géométries structurelles restent rendus par le moteur.

Les vingt compositions reconstruites et les limites de cette passe sont documentées dans `docs/RECONSTRUCTION-URBAINE-v09.md`. Les images de contrôle sont des rendus du Canvas de production, pas des concepts générés ni des captures navigateur.

## Version 0.10 — services et port

20 assets produits avec l’outil image_gen intégré : service-v10-0..11.webp (12 mobiliers / arche / collecteur / segment de conduite), io-interior-v10-0..5.webp (6 mobiliers IO), io-freighter-v10.webp (cargo opérationnel) et interior-wood-v10.webp (texture de parquet). Les sources, prompts, manifests et extracteurs se trouvent dans art-source/service-v10-*, art-source/io-interiors-v10-*, art-source/io-freighter-v10-* et art-source/interior-wood-v10-*. Extraction sans repeinture ; alpha et RGB visibles validés pour les sprites transparents. Le parquet est opaque. Les géométries de murs sont texturées avec les matériaux du catalogue existant.


## Version 0.12 — infrastructures dans les deux orientations

Six nouveaux sprites transparents `linear-v12-0..5.webp` : grillage métallique q/r, balustrade en pierre q/r, conduite isolée sur supports q/r. Créés avec l’outil image_gen intégré, puis extraits sans repeinture. Sources, prompts de génération et de correction de l’orientation, mesures des points d’appui et centres de brides, ainsi que validation lossless RGB/alpha : `art-source/linear-v12.png`, `linear-v12-prompts.json`, `linear-v12-manifest.json` et `linear-v12-extract.py`.

Les anciennes liaisons de type pipe/fence/balustrade n’utilisent plus de traits de substitution. Les sprites se raccordent sur les axes du plan, en sections de deux ou trois cases, avec les poteaux verticaux et un tri en profondeur par section. La légère différence de perspective peinte est compensée par un cisaillement vertical calculé à partir des deux points mesurés. Les liens obliques suivent deux axes orthogonaux ; leurs extrémités écrites dans les plans sont conservées. Les câbles fins, effets et murs intérieurs texturés gardent leur géométrie native. Les passerelles utilisent déjà un asset raster propre.
