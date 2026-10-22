# Rapport critique : échecs, causes et traitement à la racine

## 1. Conclusion

La maquette a éprouvé une boucle de RPG, des choix, des factions, des services, une interface et des familles d’assets. Elle n’a pas atteint la densité, la cohérence spatiale, la fiabilité d’accès ni le niveau artistique demandé. La multiplication des contenus et correctifs n’a pas remplacé un référentiel commun entre conception, images et navigation.

Les retours répétés sur les villes et les accès constituent un échec de validation du résultat, même lorsque les tests passent. Repartir de zéro doit changer la méthode et les fondations ; prolonger les mêmes correctifs multiplierait les symptômes.

Ce rapport distingue les faits du code, les retours utilisateur, les bugs reproduits puis corrigés et les hypothèses. Les derniers bâtiments inaccessibles signalés ne sont pas individuellement identifiés avec une sauvegarde permettant leur reproduction exacte.

## 2. Priorités

| Priorité | Défaut | Preuve ou limite | Traitement |
| --- | --- | --- | --- |
| P0 | Échelle incohérente | Retours et facteurs dans geometry.js | Unité monde et scène d’étalonnage |
| P0 | Entrées fragiles | Retours ; bug Nilo reproduit ; clic façade élargi | Contrat unique d’accès et transition de groupe |
| P0 | Plans distincts du terrain | Atlas séparé et transformations successives | Donnée de quartier de référence et éditeur |
| P0 | Absence de recette tactile | Tests DOM sans navigateur | Vrai navigateur et téléphone dès la tranche initiale |
| P1 | Quartiers vides ou similaires | Retours et familles réutilisées | Programme fonctionnel et identité locale |
| P1 | Assets absents ou provisoires | Captures et correctifs v0.9-v0.12 | Catalogue, état de production, contrôle de livraison |
| P1 | Lore appliqué tardivement | Big Larry et périmètre corrigés après retours | Invariants et revue de lieu avant production |
| P1 | Simulation peu profonde | Douze routines, un compagnon, pas d’économie régionale | États explicites et périmètre progressif |
| P1 | Dialogue inégal | Passes successives, répliques fonctionnelles | Voix, scène et relecture en contexte |
| P2 | Documentation périmée | README mêlant les versions | Séparer état courant et historique |
| P2 | Copies runtime | Répertoires v12/v13 | Chaîne de build et cache versionnés |

## 3. Échelle corrigée par pourcentages

Le problème a oscillé entre bâtiments trop gros et trop petits. La v0.12 ajoute 25 % au rectangle dessiné ; la v0.13 ajoute 25, 35 ou 50 % selon famille et hauteur, en préservant certains grands modèles. Ces facteurs répondent au retour immédiat sans définir la taille physique d’une porte, d’un étage ou d’un personnage.

Dans geometry.js, le rectangle dépend de l’emprise projetée, du rapport de l’image, d’une hauteur plafonnée et de facteurs. L’image peut grandir alors que l’emprise bloquée n’évolue pas de façon équivalente. Les rues et parcelles ne sont pas toutes recomposées avec la silhouette agrandie.

Cela peut produire un passage logiquement praticable sous une façade, un masque trop envahissant ou une entrée visuellement incohérente. Le recalage vers une case libre rapproche le seuil du dessin, mais ne démontre pas que le bâtiment est correctement implanté.

Le nouveau référentiel doit définir unité monde, étages, portes, largeur de rue, corps et caméra. Un agrandissement vérifie simultanément parcelle, dégagements, collision, intérieur et accès. Toute variante passe dans une scène d’étalonnage avant d’être placée dans plusieurs quartiers.

## 4. Accès et compagnon insuffisamment robustes

Un bug concret a été reproduit en v0.12 : la sortie d’intérieur chargeait d’abord le quartier et plaçait Nilo au point d’arrivée général, puis remettait le joueur devant la porte. La distance excessive empêchait l’entrée suivante. Le correctif replace le compagnon après le joueur et migre certains anciens états reconnaissables.

Avant v0.13, le petit point de porte et le badge étaient cliquables, mais cliquer la façade pouvait faire marcher le joueur. La v0.13 ajoute la sélection des pixels opaques du bâtiment visitable, recale les 21 seuils, autorise le seuil comme destination et explique plusieurs refus.

Ces corrections sont présentes. Elles ne prouvent pas que chaque blocage ressenti sur téléphone est reproduit et résolu : les 21 portes passaient déjà des essais dans un contexte neutralisé, sans reproduire la sauvegarde et le geste exacts de l’utilisateur.

Il faut une définition unique comprenant bâtiment, ouverture, sélection, seuil extérieur, condition, intérieur cible, retour et positions de groupe. La commande retourne un état précis : autorisé, chemin bloqué, serrure, restriction, combat ou allié empêché. La transition est cohérente pour tout le groupe.

Tester clic façade, badge, liste contextuelle, bouton, différents zooms, vrai toucher, ancien état sauvegardé, allié proche, loin, en attente et blessé. Ouvrir toutes les serrures pour un test de trajet ne vérifie pas les autorisations d’une partie normale.

## 5. Grande surface sans densité suffisante

Passer de 25 × 25 à 50 × 50 cases quadruple une surface. Cela ne multiplie pas les usages et relations. De grandes distances, des bâtiments indépendants et des accessoires dispersés donnent l’impression d’une exposition de sprites.

Les implantations actuelles sont écrites à la main ; ce fait évite le remplissage aléatoire mais ne garantit pas leur pertinence. Les silhouettes, familles et sols se répètent. Des services existent sans que la ville explique clairement habitat, travail, stockage, eau, déplacement et pouvoir.

Le redémarrage doit concevoir un programme de quartier : qui y vit, ce qui entre, ce qui est fabriqué, les lieux publics, les voies de fret et les conflits d’usage. Le plan exprime ces relations. La densité crée des choix et des indices ; elle n’est pas une quantité de décor.

Vérifier que Dusk-Town, Junk-Burgh, Buenos Aires et Steel-Megalopolis se distinguent sans étiquette. Faire varier aussi les quartiers d’une ville : patios, artères, fronts industriels, niveaux, place civique ou maisons mitoyennes.

## 6. Assets sans contrat de production assez fort

Les atlas générés ont apporté de la variété, mais pas toujours une échelle, un angle, un pivot et des entrées uniformes. Le miroir horizontal ne garantit ni éclairage cohérent ni porte au bon endroit. Les originaux raster ne constituent pas des modèles 3D.

Les captures montrent des infrastructures sous forme de barres, des arches provisoires et des éléments simplifiés. Les passes suivantes ont ajouté plusieurs familles raster. Les conduites, grillages et balustrades sont désormais segmentés avec six images orientées. Les câbles fins et certains murs restent volontairement des géométries natives.

Il faut distinguer un élément final intentionnel d’un substitut publié par défaut. Ne pas affirmer que toute géométrie native est une ressource absente, ni que les dernières images ont réglé tous les défauts.

Créer un catalogue avec source, usage, dimensions, pivot, orientations, portes, collision, occlusion, matériau, export et état : concept, temporaire, intégré, vérifié. Une ressource requise manquante déclenche un diagnostic et bloque sa publication comme élément fini. Les anciens sprites ne sont réutilisables qu’après contrôle dans le nouveau référentiel.

## 7. Lore, topographie et fonctions dissociés

Big Larry a été signalé comme ville habitée alors que c’est un impact vitrifié. La v0.13 ne contient plus de bâtiment ou de PNJ permanent sur ce lieu. Cette correction tardive montre la nécessité d’un contrôle préalable de lore.

Le futurisme protégé doit rester sous le sarcophage ; le périmètre est désertique. Le port doit avoir chenal, bassin, quais, grues et routes. La station doit montrer le chemin de l’eau et les accès de maintenance.

Le port et le relais ont été recomposés en v0.10. Leur correction dans l’historique ne signifie pas que leur qualité est approuvée. Les captures signalent une logique fonctionnelle et visuelle insuffisante à plusieurs étapes.

Avant production, chaque lieu reçoit invariants, topographie, flux, activités, risques, population, silhouette et accès. Le plan est relu sur ces points ; toute modification doit se répercuter sur les routes, textes, rencontres et métiers.

## 8. Documentation plus avancée que le jeu

Les anciens documents contiennent 44 plans, des fiches, 32 événements proposés, six circuits et quatre candidats compagnons, dix maquettes. Leur couverture dépasse l’implémentation. Certains concepts sont consultables dans l’atelier sans exister comme terrains jouables.

Le README cumule des sections anciennes mentionnant d’autres nombres de scènes et d’intérieurs. Il mélange historique et état courant. Le nouveau dossier actualise cette lecture sans transformer les propositions en acquis.

La reconstruction doit séparer spécification cible et état de livraison. Chaque exigence reçoit un identifiant, un statut et une preuve. Un quartier n’est pas terminé parce que son nom et trois services existent. Une fiche de compagnon ne signifie pas qu’il est jouable.

## 9. Tests insuffisants pour la qualité d’usage

Les rendus Canvas inspectent les scènes sans navigateur complet. Le DOM minimal relie fonctions et boutons sans calcul de CSS, police, défilement ou recouvrement. Une suite de tests peut réussir alors que le toucher est imprécis ou l’écran surchargé.

Les retours après publication ont servi de principale recette visuelle. Cette méthode a entraîné plusieurs séries de retouches sans certitude sur leur effet réel.

La première tranche doit être vérifiée sur téléphone étroit, format intermédiaire et bureau, puis sur vrai tactile. Tester portrait/paysage, clavier virtuel, zones système, texte agrandi, mouvements réduits et glissement de carte. Comparer des captures réellement rendues aux maquettes retenues.

Les tests de règles restent utiles : ressources, migrations, transitions et sauvegarde. Ils se complètent par des tâches : identifier une boutique, entrer, parler, acheter, ressortir avec l’allié et reprendre une route.

## 10. Systèmes de monde encore isolés

Douze routines et un compagnon ne produisent pas un monde social persistant. Une rencontre de caravane n’est pas un réseau économique. Deux détachements ne simulent pas la guerre entre régions.

Beaucoup de conséquences reposent sur des drapeaux, textes et changements locaux. L’extension sans modèle commun multiplierait les cas particuliers. La simulation doit rester bornée mais explicite : stocks, horaires, transit, témoins et états de conflit, avec inspection dans l’atelier.

Ajouter une règle seulement lorsqu’elle crée une décision perceptible. Une complexité invisible qui ne sert ni l’histoire ni le jeu alourdit la production et la vérification.

## 11. Accumulation technique

Des responsabilités sont séparées en modules, mais des registres globaux et plans sont modifiés par installations successives. L’ordre de chargement intervient dans l’état final. Le moteur et l’application concentrent encore de nombreuses branches.

Échelle, accès, services et décors sont répartis dans des correctifs de versions différentes. Les copies runtime renouvellent les URL pour prévenir un mélange de cache, mais dupliquent la distribution. Certains outils écrivent vers un chemin absolu de l’ancienne session.

Cela ne prouve pas que tous les bugs viennent du cache ou des imports. Cela montre une maintenance fragile et peu adaptée à un éditeur de contenu durable.

La nouvelle architecture sépare définitions immuables, état, règles, simulation, rendu, interface et outils. Les données sont validées avant chargement. Un build unique produit les ressources versionnées et un manifeste. Les outils acceptent des chemins portables.

## 12. Connaissances à conserver et limites ouvertes

Conserver comme intentions : crise de l’eau, contrastes IO/terres, origines, Aura, services intérieurs, preuves consultables, solutions non violentes, ressources du compagnon et copie de test.

Conserver comme cas de régression : retour de Nilo, façades retournées, coûts appliqués une fois, atelier isolé, sauvegardes et retours de dialogue après une conclusion. Ces cas seront réécrits dans les tests du nouveau système.

Ne pas conserver comme fondation : taille visuelle servant de géométrie physique, facteurs d’échelle empilés, gabarits répétés pour remplir les cartes, installations successives et recette de mise en page simulée.

Les derniers cas exacts d’inaccessibilité et de taille restent sans reproduction individualisée. Les captures représentent plusieurs versions. Aucune suite de tests ne prouve à elle seule la qualité des dialogues, le bon niveau de densité ou l’équilibrage. Ces retours restent ouverts jusqu’à une revue effective du nouveau résultat.
