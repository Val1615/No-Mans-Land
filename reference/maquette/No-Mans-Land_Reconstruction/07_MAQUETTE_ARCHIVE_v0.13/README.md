# No Man’s Land — Les Héritiers du silence

RPG web isométrique original dans l’univers de No Man’s Land de Valentin. Version jouable 0.13, sans dépendance de production. L’aventure se déroule en 2175, avant le récit du roman *Un réveil tardif*, daté de 2202. Les personnages jouables, PNJ locaux et la crise du réseau hydraulique sont des créations dérivées pour le jeu ; ils ne remplacent pas les protagonistes du livre.


## Échelle et interaction des façades — 0.13

Hausse supplémentaire par rapport à la 0.12 : +50 % pour les petites maisons et abris, +35 % pour plusieurs services, +25 % pour les autres modèles modestes. Les bâtiments déjà dessinés à au moins 300 pixels gardent leur taille. L’audit couvre 527 modèles extérieurs : 453 agrandis, 74 conservés. Les 21 seuils sont recalés.

Les pixels visibles d’un bâtiment visitable sont maintenant cliquables, en plus du badge et de la porte. Les zones transparentes de l’image ne capturent pas le clic. Le trajet peut utiliser le seuil lui-même ; les refus dus au passage ou au combat donnent une explication dans le dialogue. Les 21 entrées existantes sont contrôlées depuis le point d’arrivée, avec et sans Nilo. 164 tests passent et les 35 vues d’ensemble extérieures sont inspectées avec le Canvas de production. [Détails et limites](docs/ECHELLE-ACCES-v13.md).

## Accès, taille et décors — 0.12

Tous les modèles de bâtiments gagnent exactement 25 % en largeur et en hauteur par rapport à la version 0.11, avec le même point d’appui au sol. Les 21 seuils sont recalés sur les façades agrandies. La transparence de proximité reste active. Seules les vraies entrées portent un badge ; les bâtiments sans intérieur n’ont plus de marqueur.

Le retour d’un intérieur replaçait Nilo au point d’arrivée du quartier, loin du joueur : l’entrée suivante était refusée sans explication. Le compagnon revient maintenant près de la porte avec le joueur. Les sauvegardes présentant cet ancien défaut sont réparées de façon ciblée, sans déplacer un compagnon laissé en attente. Les conditions qui empêchent d’entrer sont affichées dans le dialogue.

Six sprites remplacent les traits épais des conduites, grillages et balustrades : deux orientations par modèle, raccordées par sections courtes et triées en profondeur. Aucun ajout de remplissage des villes. 158 tests Node passent ; les 56 scènes ont été rendues hors navigateur. [Détails, vérification et limites](docs/ACCES-ASSETS-v12.md).

## Lisibilité et échelle — 0.11

État de la version 0.11, remplacé par la 0.12 ci-dessus : porte turquoise « Entrer », cadenas ambre pour une vraie porte verrouillée, porte barrée grise pour un bâtiment non visitable. Les repères d’entrée sont cliquables à taille constante ; une légende complète les symboles. La transparence du bâtiment entier revient à proximité du joueur.

Audit des 35 extérieurs : 495 modèles corrigés dans 31 zones. La hauteur dessinée respecte la hauteur prévue, les collisions suivent les emprises réduites et les 21 accès restent alignés aux portes. Corrections fixes, sans remplissage de décor. [Détails et limites de vérification](docs/ACCES-ECHELLE-v11.md).

## Services et infrastructures — 0.10

21 intérieurs visitables au total, dont 17 nouveaux : hôtel, bar, épicerie et atelier de Dusk-Town ; bazar et clinique de Junk-Burgh ; services du Forum, atelier Lin, K-12, registre et accueil SMPD ; archives et dispensaire de Buenos Aires ; intendance et infirmerie UFSA ; capitainerie IO et salle de conduite 07. [Détail des accès et services](docs/SERVICES-INTERIEURS-v10.md).

Les commerces, soins, décontamination, repas, chambre et établis ont des effets réels sur le personnage. Elvira, Beto, Vera, Sen, le chirurgien K-12, Lin, Eva et Leal travaillent dans leurs intérieurs. Les anciens identifiants et les routines migrées préservent les sauvegardes.

AN06 et AN04 ont été recomposés : un seul bassin maritime à l’est, cargo actif, grues sur le quai, route et cour de fret séparées ; station hydraulique organisée par fonctions, collecteurs et conduites regroupés. Arches en pierre réelles au temple. 20 nouveaux assets raster dont un ensemble intérieur IO et un parquet texturé. Les façades restent opaques hors d’une découpe locale autour du personnage masqué.

Validation : tests Node et rendu Canvas de production, sans navigateur. Voir le dossier de version pour les limites : plusieurs hangars et logements restent non visitables.

## Interface reconstruite — 0.8

Les captures de la version 0.7 ont révélé que les anciennes règles mobiles contredisaient les nouvelles. La version 0.8 remplace les cinq feuilles de style actives par `interface.css`, avec des cadres vectoriels cuivrés, une fonte locale condensée et une seule hiérarchie de tailles.

- Terrain sur toute la surface, localisation flottante et barre de commande mobile de 146 px. Portrait, santé et radiations restent groupés ; les actions tiennent sur une ligne défilante en combat. En exploration, la barre affiche les actions contextuelles et les panneaux principaux. Le repos reste disponible par Actions. La minicarte s’agrandit au toucher.
- Fiche personnage avec silhouette, sept tuiles d’attributs, équipement réellement porté et onglets distincts pour les compétences / aptitudes et les réputations. Les informations ne forment plus une longue colonne avant d’atteindre les compétences.
- Dialogue en bandeau bas, portrait dans le cadre et zone de lecture / choix défilante. Le terrain reste visible.
- Atlas centré sur une carte de relief, panneau de trajet compact, zoom réel du plateau et déplacement par glissement. Le fond d’illustration n’altère ni le contour géographique, ni les 167 cases, ni les coordonnées des lieux, ni le calcul des trajets. Les coordonnées manuelles et les descriptions détaillées sont repliables.
- Inventaire avec catégories directes, liste et grande présentation de l’objet. Sur les écrans larges, la colonne de Nilo montre son équipement, sa santé et le transfert réel d’un exemplaire sélectionné.

La vérification comporte 126 tests Node, dont les nouveaux parcours de l’interface et le contrôle d’une seule feuille de style active. Les tests de branchement utilisent un adaptateur DOM, sans moteur de mise en page. Le fond de carte a été rendu avec Inkscape et inspecté. Aucun navigateur de contrôle n’est disponible dans cet environnement : le rendu CSS sur téléphone reste à confirmer dans un navigateur réel.

## Reprise à partir des dossiers de conception — 0.7

- Interface graphite / ivoire, accents cuivre et turquoise, animations courtes et option de mouvements réduits. Quatre profils d’affichage, taille du HUD 85–150 %, texte 100–200 %, contraste, panneaux masquables, ordre des huit actions et raccourcis personnalisables. Inventaire filtrable, recherche conservant le focus, liste ou grille, favoris et comparaison avec l’équipement porté. Le journal conserve les dernières conversations et leurs lieux connus.
- Atelier accessible dès le titre ou par F2 : campagne préservée en mémoire, copie de test, emplacements `nml-test-*`, annulation et retour à la campagne. Dix-huit scénarios cohérents : début, Nilo, contrôles d’origine, garde de Sami, confrontation, réseau prêt et quatre conclusions, sept rencontres routières. Catalogue des 21 quêtes avec accès au donneur ; aperçu des dialogues sans effet ; téléportation au point d’arrivée ; soin, ressources, objets, compétences effectives et options de test indépendantes. Les commandes sont enregistrées, sans `eval`.
- Copie complète des états de scène, ennemis, définitions dynamiques, routes régionales, compagnon, contacts, horloge, état et compteur du générateur aléatoire. Une opération invalide revient à l’état précédent. L’espace de test ne remplace aucune sauvegarde de campagne. La copie et le point de retour de l’atelier restent en mémoire : recharger la page revient à l’écran titre et à vos sauvegardes normales.
- Dusk-Town : services, cours habitées, ateliers / veille. Implantations fixes tirées de DT01–03, circulation, matériel regroupé par usage, clinique existante conservée. L’échelle des modèles correspond aux emprises de collision. Les logements privés et les intérieurs supplémentaires prévus dans le dossier restent à construire ; les marqueurs actuels décrivent précisément les services accessibles. Human Corporation demeure scellée.
- Douze parcours locaux fixes : habitants des services, cuisines, laverie, atelier, dépôt et milice. Le temps de jeu, pas le temps réel, fait avancer ces parcours par cases praticables ; ils s’arrêtent en combat. Les positions sont sauvegardées. Les routines interrégionales, perception, souvenirs de témoins et économie simulée restent à développer.
- Nilo devient un compagnon unique : 46 PV, 7 PA, pistolet, manteau, 12 cartouches et une trousse personnelles, charge de 22 kg. Recrutement par le dialogue existant, cheminement autour des obstacles, attente persistante, reprise à proximité, transferts conservant les quantités, cinq ordres. Il joue avant les adversaires avec portée, couvert, ligne de tir, fumée, précision et munitions. Les adversaires peuvent le prendre pour cible. À terre, stabilisation à deux cases avec une trousse et 3 PA ; en difficulté Difficile, trois phases sans soin sont mortelles. Les autres difficultés protègent le compagnon au sol. Les autres candidats et la confiance détaillée ne sont pas encore actifs.
- Codex des cinq populations et des sept factions avec les six planches fournies. Les cyborgs conservent un cerveau humain ; les androïdes sont entièrement synthétiques. La règle du lore prévaut sur la mention « compatibilité réduite » de la planche : un cyborg ne pratique pas l’Aura. Population et faction sont des champs distincts ; l’accueil de Center-Town est une unité androïde, Valen un cyborg, les autres citoyens IO sont principalement augmentés.
- Les 44 plans de l’atlas sont consultables dans l’atelier sous forme de géométrie et de registres précis. Ils décrivent les objectifs de conception, et ne constituent pas 44 nouveaux terrains jouables. Les quartiers restants de Junk-Burgh, les nouvelles villes UFSA, le Ranch Liberté et la région des Rakkens attendent leur transposition.

### Vérification de cette reprise

Les tests Node couvrent les parcours, les conversations, les 18 scénarios, les ressources du compagnon, les transferts, les états au sol, la migration, l’isolation des sauvegardes et les commandes. Le test d’interface utilise un adaptateur DOM minimal ; il ne valide pas une mise en page de navigateur. Les trois quartiers de Dusk-Town sont rendus et inspectés avec le moteur Canvas de production hors navigateur. Aucun contrôle de navigateur n’est disponible dans cet environnement : la disposition CSS, le tactile et les animations restent à revoir dans un navigateur réel.

### Prochaines intégrations des dossiers

Intérieurs dessinés séparément ; autres implantations de l’atlas ; caravanes CR01–06 persistantes et conflits régionaux ; mémoire et réactions des témoins ; compagnons Esteban, Lucero et Noa ; préparation complète de toutes les branches de quête et couverture exhaustive des variantes de dialogue ; remappage avancé manette et écran tactile. Les options développeur présentes n’annoncent pas ces fonctions comme actives.

## Contenu de cette version

- 167 cases terrestres sur une grille régionale de 22 × 20. Itinéraires progressifs, marqueur de position, haltes explorables, mer bloquée et reprise du trajet après une rencontre. Désert, piémonts, forêt occidentale, retombées de Big Larry et côte.
- Sept rencontres : convoi à fouiller, caravane à stock limité, récupératrice blessée, péage de pillards, mutants déments, drone IO et front de poussière. Combats réels, solutions par compétences, coûts et conséquences persistants. Une case visitée ne relance pas sa rencontre ; son butin et les morts restent enregistrés.
- 39 terrains fixes de 50 × 50 cases au lieu de 25 × 25 (surface quadruplée). 18 secteurs de Steel-Megalopolis, 5 quartiers de Buenos Aires, 4 intérieurs visitables. Les autres lieux conservent leurs identifiants. Dusk-Town possède maintenant trois quartiers et son plan de circulation. Les atlas régional, de Steel et de Buenos Aires restent téléchargeables.
- Six nouvelles affaires relient les lieux : citerne partagée, treuil du dispensaire, lot incomplet, réserve UFSA, confrontation IO / Nativos, séance du cinéma. Preuves à consulter sur place, ressources consommées, solutions pacifiques et décisions persistantes. 45 habitants supplémentaires ont une conversation propre ; certains proposent commerce ou soins.
- La lisière de Buenos Aires oppose deux détachements de trois combattants. Ils restent en poste pendant les discussions. Une prise de parti déclenche une IA capable de combattre l’autre équipe ; ses victimes ne donnent ni butin ni crédit de meurtre au joueur. Le registre des ateliers permet une suspension de l’opération sans combat.
- Les entrées utilisent le même rectangle de sprite que le rendu et le clic. L’accès du Striker Oméga est fixé sur le bras droit, à une case du point d’approche ; le cœur reste inaccessible.
- Création de personnage : 4 origines (Humain, Augmenté, Mutant, Cyborg déclassé), 7 attributs, 10 compétences, 3 spécialités, 4 profils et 3 difficultés. Six nouvelles apparences avec portrait et silhouette correspondante, cinq passés et quatre particularités à contrepartie (ou aucune).
- Exploration sur hexagones, recherche de chemin, caméra mobile, zoom et sélection des éléments par une liste accessible.
- Combats au tour par tour : PA, portée, obstacles, couvert, tirs au torse/tête/bras/jambes, munitions, consommables et changement d’arme. Grenades, fumée affectant les deux camps, garde défensive et tir de réaction. Adversaires récupérateurs, mutants déments et drones IO.
- 21 fils de quête, dont une histoire principale à 4 issues et une crise énergétique à deux destinations concurrentes. Une route principale sans victime est entièrement fonctionnelle. Exploration possible après l’épilogue.
- Négociation, réparation, piratage, achat, vol discret, menaces, violence contre les PNJ et conséquences persistantes. Certains décès ferment des pistes secondaires ; la pompe demeure une alternative à Mara pour la quête principale.
- Réputations par faction, compagnon recrutable, niveaux et aptitudes, ajustement des armes, modifications cybernétiques, éveil difficile de l’Aura.
- Santé, fatigue, contamination, résistance propre aux origines et seuil fatal pour les mutants.
- Trois intérieurs explorables depuis des portes : clinique de Dusk-Town, comptabilité de Junk-Burgh, bunker du Titan.
- Établis : six recettes et démontage d’équipement de rechange. Caches à crocheter ou forcer, avec dépenses et conséquences. Piratage manuel par circuit à reconnecter, état et verrouillage conservés dans la sauvegarde.
- Dialogues réécrits selon les principes de la Bible de Sylvinia : voix distinctes, échanges situés, relances, connaissances limitées et humour propre à chacun. Voir `WRITING.md`.
- Steel-Megalopolis : 11 quartiers sous le sarcophage : trois niveaux urbains et une Sous-Ville sous les fondations, 3 douanes, IO Industries et 3 avant-postes. China Lake, Asia-Ground, blocs, Sous-Ville, Forum, Avenue Centrale, pôle des augmentations, registre, préfecture SMPD, jardins et atrium IO. Accès contrôlés, trajets urbains en minutes, navettes ou marche, quatre affaires locales et interventions de liaison.
- Plans propres aux 39 terrains, avec rues, places, cours, quais et accès placés à la main. Le périmètre extérieur reste désertique. Big Larry est un impact vitrifié inhabité ; China Lake possède son lac pollué et ses lanternes ; la Sous-Ville rassemble des habitations précaires sous les conduites. Les obstacles et l’eau contraignent les déplacements.
- Douze textures de sol, six bâtiments extérieurs supplémentaires, trente nouveaux accessoires, arbre forestier et Titan couché face contre terre. Les textures sont mises en cache et projetées en isométrie.
- HUD en plein écran : tableau de commande, huit actions rapides, minicarte réelle, ciblage ancré au terrain et trajet de déplacement affiché.
- Inventaire, commerces, soins, repos, sauvegarde locale, point de reprise automatique et import/export JSON.
- Visuels originaux générés : panorama, six bâtiments, six types d’acteurs et un Titan échoué. Trente sprites/portraits pour la passe 0.2, puis vingt-six pour la ville futuriste (bâtiments entretenus, mobilier, citoyens et portraits). Sons d’ambiance synthétisés en Web Audio et désactivés par défaut.

## Jouer

Le répertoire `dist/` est le site statique complet. Aucun build ni service distant n’est nécessaire au jeu après chargement. Pour développer hors Sites, utilisez n’importe quel serveur HTTP statique ; les modules ES ne se lancent pas directement avec `file://`.

Raccourcis : M atlas, I inventaire, C personnage, J journal, G grille, V discrétion, Q trousse de soin, touches 1–8 actions rapides, Espace fin du tour, F5 sauvegarde, Échap retour/menu. Le clic et le tactile sont pris en charge. Les longues traversées s’effectuent depuis l’atlas.

Les sauvegardes appartiennent au navigateur et à l’origine du site. L’export JSON permet de transférer une partie entre appareils. Version de format : 1.

## Architecture

- `dist/data.js` : univers jouable, lieux, objets, PNJ, quêtes, encyclopédie.
- `dist/engine.js` : état, exploration, économie, combats, progression, dialogues et conséquences. Fonctionne sous Node sans navigateur.
- `dist/world.js` : géographie et cases régionales, recherche d’itinéraire et compositions des haltes.
- `dist/overland.js` : état du voyage, consommation d’eau, événements et interactions des rencontres.
- `dist/world-atlas.js` et `world-v5.css` : grille interactive, trajet et commandes de halte/reprise.
- `dist/scenes.js` : plans et implantations explicites de chaque lieu, obstacles, routes et plans d’eau.
- `dist/terrain.js` et `dist/scenery.js` : matériaux et dessin des accessoires.
- `dist/render.js` : rendu Canvas, sprites, décor caché, projection, caméra et effets.
- `dist/app.js` : interface, création, écrans de jeu, audio et contrôles.
- `dist/interface.css` : base unique des interfaces de bureau et mobiles.
- `dist/expansion-data.js` : passés, particularités, recettes, objets, intérieurs et circuit.
- `dist/voices.js` : voix et relances supplémentaires des PNJ.
- `dist/city-data.js`, `city-play.js` : quartiers, cartes, activités, dialogues et présentation urbaine.
- `tools/city-map.py` : génération des cinq cartes de niveau et de leur export étiqueté.
- `tools/map.py` : génération déterministe de l’atlas.
- `tools/render-world.mjs` : contrôle des coordonnées et de l’itinéraire régional, sans rendu navigateur.
- `dist/extended-plans.js`, `buenos-plans.js`, `wild-plans.js` : implantations fixes, fonctions des ensembles, passages et obstacles.
- `dist/expanse-data.js`, `expanse-play.js` : habitants et affaires de la passe 0.6.
- `dist/geometry.js` : géométrie commune des sprites et entrées.
- `tools/render-scene.mjs` : contrôle visuel indépendant du Canvas avec @napi-rs/canvas du runtime.
- `tests/` : tests de logique et des branchements d’interface avec un adaptateur DOM minimal. Ces derniers ne remplacent pas un navigateur réel.

## Validation

`node --test tests/*.test.js` (130 tests) vérifie le moteur, les quatre affaires urbaines, les accès, les coûts et durées des trajets, les sauvegardes et les branchements d’interface. `tests/ui-smoke.test.js` utilise @napi-rs/canvas fourni par le runtime (`CODEX_PRIMARY_RUNTIME_NODE_MODULES`) pour vérifier le démarrage de l’application, la création, les dialogues, le troc et la carte. Aucun navigateur automatisé n’est disponible dans l’environnement de création : pas de validation réelle de mise en page ou de gestes tactiles. Le rendu des terrains est contrôlé séparément en images.

## Périmètre et développement restant

Cette version est une aventure jouable, pas le volume de Fallout 1 ou Fallout 2. Les lieux fixes sont des terrains séparés reliés par une carte quadrillée, à la manière d’un RPG de cette génération. Les cases entre les lieux réutilisent sept compositions fixes de 50 × 50 cases : canal, bretelle, station de pompage, forêt, piémont, retombées vitrifiées et côte. Le choix dépend de leur position géographique. Les plans ne sont ni tournés, ni dispersés, ni garnis aléatoirement ; la graine sert uniquement aux rencontres. Les 167 cases ne sont pas 167 niveaux écrits et dessinés individuellement. Les 18 secteurs du complexe comprennent 11 quartiers intérieurs et 7 secteurs de périmètre. Les étages de la présidence et les casernements militaires restent réservés et ne sont pas des intérieurs explorables. La ville possède des passants et des décors propres ; tous les immeubles ne sont pas visitables.

Les animations restent simples. Six silhouettes humaines personnalisables sont proposées à la création ; les mutants et cyborgs conservent les silhouettes propres à leur origine. La prochaine passe devrait approfondir les rencontres et la variété des situations plutôt qu’augmenter le nombre de lieux.

La sauvegarde reste au format 1. Les sauvegardes antérieures reçoivent une position régionale correspondant au lieu courant. Une partie chargée pendant un trajet reprend en halte sur la dernière case parcourue, avec son itinéraire conservé. L’eau est déduite par tranches cumulées de quatre heures de traversée, même après une halte. Les sauvegardes antérieures sans données d’expansion sont migrées avec une apparence par défaut, sans réappliquer de bonus de passé. L’apparence peut être changée depuis la fiche de personnage. Les anciens identifiants de lieux sont conservés : `steel` devient le Forum et `under` reste la Sous-Ville. Une position devenue bloquée par le nouveau plan est replacée à l’entrée du terrain sans réinitialiser la progression. La révision 6 replace les ennemis des sauvegardes anciennes sur leurs nouveaux emplacements en conservant blessures et morts ; les anciens habitants et rencontres permanentes de Big Larry sont retirés. Les nouveaux passés et particularités se choisissent en début de partie.

## Références et droits

Univers, roman et croquis : Valentin. La dénomination utilisée est toujours **Steel-Megalopolis**. Aucun fichier complet du roman n’est distribué par le jeu. Aucune ressource de Fallout n’est utilisée. Assets originaux réalisés avec l’outil intégré imagegen ; voir `ART.md`.

## Références visuelles de la passe 0.2

Captures officielles de Trudograd (https://atomrpg.com/en/trudograd/) et Wasteland 3 (https://wasteland3.inxile-entertainment.com/games/wasteland-3) : recherche sur la lisibilité du HUD, les commandes de combat et la présentation du personnage. Aucune de leurs images, icônes ni ressources n’a été intégrée.


## Reconstruction urbaine — 0.9

Vingt plans sont recomposés dans `dist/settlement-v9.js` : Dusk-Town (3), les quartiers sous le sarcophage (11), Buenos Aires (5) et Waste Coast. Les bâtiments ont des emprises physiques plus petites à Dusk-Town ; les parcelles ne sont plus occupées par un seul modèle étiré. Les autres complexes reçoivent des substitutions et orientations explicitement choisies. Chaque implantation reste écrite à la main, avec ses rues, cours et groupes de mobilier.

55 nouveaux assets raster : 18 bâtiments, 36 décors/utilitaires et une passerelle. Les orientations sont gérées par le rendu et les ancrages de porte suivent la façade retournée. Les modèles comprennent de vraies vues arrière pour certaines maisons et blocs techniques. Les accessoires indisponibles pendant le chargement restent absents jusqu’à leur réception ; aucun cube ou polygone de remplacement n’est dessiné. Le terrain, les câbles, les effets de combat et les murs intérieurs demeurent des géométries du moteur.

La clinique de Dusk-Town conserve un accès ancré sur ses marches ; les arrivées de China Lake, Asia-Ground et du siège IO sont replacées hors des nouvelles emprises. Les identifiants de quêtes, dialogues, objets et sauvegardes restent compatibles. Les passants ajoutés sont de l’ambiance : les douze routines persistantes existantes sont conservées, sans prétendre que tous les figurants ont une simulation. Aucun nouvel intérieur ou nouvelle quête n’est annoncé par cette passe.

Contrôles : 130 tests passent, dont les accès à tous les contacts, objets et sorties, les obstacles, les quatre conclusions et les sauvegardes. `node tools/render-scene.mjs --all --overview` produit une vue de chaque terrain avec le véritable moteur Canvas. Ces images sont une vérification graphique hors navigateur ; elles ne valident pas le tactile ni le chargement réseau sur téléphone.

Les assets sources, prompts et manifests sont conservés sous `art-source`. `docs/RECONSTRUCTION-URBAINE-v09.md` décrit les règles de placement et le périmètre exact.
