# Reconstruction urbaine — 0.9

## Périmètre réellement livré

| Ensemble | Terrains recomposés | Intention conservée |
| --- | --- | --- |
| Dusk-Town | Avenue des services, Cours habitées, Ateliers et veille | Habitat ancien de petite échelle, façades discrètes, travail et vie dans les cours ; ancien site condamné au nord. |
| Steel-Megalopolis | Les onze terrains sous le sarcophage | Sous-Ville technique et précaire ; Lower-Town dense et sombre ; Center-Town entretenu et commercial ; Upper-Town en marbre, or et végétation. |
| Buenos Aires | Avenues, Patios, Centre administratif, Ateliers du rail, Lisière | Ruines réoccupées par des habitants conscients ; usages civils séparés du face-à-face militaire. |
| Waste Coast | Côte des naufrages | Station abandonnée, épaves sur la ligne d’eau, abri de récupération et mobilier maritime. |

Les douanes, les bases, Granja, la station de répartition, Novo Córdoba, le port et Junk-Burgh conservent leur circulation existante. Leurs variantes de bâtiments sont choisies explicitement dans `BUILDING_VARIANTS`. L’échelle des structures est également recalée sur leur emprise dans les trois bourgs et les sept sites du périmètre, sans agrandir leurs collisions. Cette passe ne prétend pas reconstruire l’ensemble des 44 plans du dossier de conception ni ouvrir leurs intérieurs.

## Règles de construction

- Une emprise désigne la structure physique. Les cours, jardins et aires de déchargement restent des surfaces distinctes. À Dusk-Town, aucune structure nouvelle ne dépasse 64 cases d’emprise, contre des parcelles de plus de 150 cases occupées précédemment par un seul sprite.
- Les maisons forment des ensembles avec annexes et passages. Les quatre tours Arcadius restent des repères de Center-Town ; elles ne sont pas réparties dans tous les quartiers.
- Les boutiques font face aux flux piétons. Les pièces mécaniques restent près des ateliers ; le linge, le bois et les cuisines dans les cours habitées ; les palettes au chargement ; les filets et les cordages près des épaves.
- Les nouveaux plans utilisent uniquement des coordonnées écrites dans `settlement-v9.js`. Aucun tirage, grille de remplissage ou densification aléatoire n’est ajouté au runtime.
- Les variantes retournées sont déclarées par bâtiment ou accessoire. Les textes restent lisibles et les ancrages des entrées suivent la façade. Certaines variantes possèdent une véritable vue arrière dessinée, au lieu d’un simple miroir.

## Catalogue artistique

55 fichiers WebP supplémentaires : 18 bâtiments, 24 éléments domestiques / maritimes / urbains / naturels, 6 utilitaires, 6 éléments de rue, 1 passerelle. Les sources PNG et manifests de découpe sont conservés sous `art-source`.

| Famille | Fichiers consommés | Exemples |
| --- | --- | --- |
| Bâtiments | `settlement-v9-0.webp` à `settlement-v9-17.webp` | Maison basse, épicerie, hôtel, atelier, escalier arrière, boutique condamnée ; habitat augmenté, rangée de commerces, angle de nuit, sous-station, bureaux, façade technique ; serre, résidence, galerie, tour, atrium, villa. |
| Décors | `props-v9-0.webp` à `props-v9-23.webp` | Linge, chariot, bois, fourneau, fontaine ruinée, potagers ; membrure de coque, filets, cabestan, décombres, sacs de tir, rails ; fontaine, balustrade, afficheur, tri, armoire électrique, sculpture ; rochers, broussailles, pneus, palette, câbles, bouée. |
| Utilitaires | `utility-v9-0.webp` à `utility-v9-5.webp` | Réfrigérateur, écran de cinéma, raccord mécanique, drapeau, bitte d’amarrage, colonne brisée. |
| Rue | `street-detail-v9-0.webp` à `street-detail-v9-5.webp` | Banc ancien, support de fondation, abri de toile, râtelier de métal, lampe ancienne, échoppe de récupération. |
| Liaison | `skybridge-v9.webp` | Passerelle vitrée en acier graphite avec conduites et éclairage intérieur. |

Le support de fondation est cadré comme une structure se prolongeant vers le plafond ; son sommet sort du cadre source. Les effets de terrain, câbles, clôtures et murs intérieurs restent des géométries du moteur. Les accessoires et bâtiments ordinaires ne reçoivent plus de boîte de remplacement pendant le chargement. Certains petits contenants partagent toujours un modèle ; 55 assets ne signifient pas un modèle unique pour chaque objet du jeu.

Prompts et méthode : `art-source/settlement-v9-prompts.md`, `props-v9-prompts.md` et les manifests. Outil intégré image_gen ; alpha d’origine conservé lors de la découpe et de la conversion sans perte.

## Accès, habitants et sauvegardes

La porte de la clinique est ancrée sur les marches de son sprite ; sa case d’approche reste à moins d’une case du repère visible. Le mécanisme conserve aussi les accès au cinéma, à l’arrière-boutique et au Titan. Les arrivées de China Lake, Asia-Ground et du siège IO sont déplacées sur un passage libre.

Les identifiants, quêtes et récompenses restent identiques. Une ancienne position occupée par un nouveau bâtiment est replacée à l’arrivée du terrain par le mécanisme existant, sans réinitialiser l’inventaire ni les quêtes. Les douze routines persistantes de Dusk-Town sont conservées. Les passants d’ambiance ajoutés ne sont pas présentés comme de nouveaux personnages à dialogues ou à horaires simulés.

## Vérification

130 tests : navigation vers tous les contacts, objets et sorties ; portes ; sauvegardes ; combat ; compagnie ; UI ; présence des modèles ; absence de chevauchement entre les nouvelles emprises ; mobilier placé hors des structures ; ancrages retournés. Les cas existants qui imposaient cinquante accessoires par lieu ont été remplacés par un minimum de présence, puis complétés par les contrôles de placement : un quota d’objets ne garantit pas une ville cohérente.

`node tools/render-scene.mjs --all --overview` rend les 39 terrains avec le code Canvas de production. Le cadrage d’ensemble tient compte des véritables hauteurs et permet de voir les toitures sans les couper. Les vérifications sont effectuées hors navigateur ; les performances réseau et les gestes tactiles sur téléphone restent à contrôler sur l’appareil.
