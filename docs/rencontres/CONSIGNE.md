# CONSIGNE WORK : NO MAN'S LAND
## Développement des rencontres aléatoires et de l'exploration régionale
### Mission collective : Rivet, Ocre et Régie

**Projet :** No Man's Land, RPG isométrique post-apocalyptique  
**Dépôt GitHub :** https://github.com/Val1615/No-Mans-Land  
**Jeu :** https://val1615.github.io/No-Mans-Land/  
**Priorité :** Haute  
**Objectif :** Transformer les voyages entre les villes en véritables expériences de gameplay, grâce à des rencontres aléatoires intégralement jouables en vue isométrique.

---

# 1. DIRECTIVE PRINCIPALE DE L'AUTEUR

L'objectif est de donner vie aux terres désolées de No Man's Land.

Actuellement, le jeu dispose d'une carte régionale permettant de voyager entre plusieurs destinations, notamment Dusk-Town et Steel-Megalopolis.

Le déplacement s'effectue case par case, avec des durées variables selon les terrains, un brouillard de guerre et un système d'interruption du trajet.

La structure est présente, mais les événements de voyage sont encore largement absents.

**Votre mission consiste à développer et intégrer les rencontres aléatoires directement dans le jeu.**

Ces rencontres doivent être variées :

- Groupes de pillards et embuscades.
- Caravanes marchandes.
- Négociants itinérants.
- Créatures sauvages mutantes.
- Convois en difficulté.
- Patrouilles de factions.
- Voyageurs isolés.
- Survivants blessés.
- Événements environnementaux.
- Découvertes et lieux insolites.

## DÉCISION NON NÉGOCIABLE

**Toutes les rencontres doivent se dérouler dans de véritables environnements isométriques jouables.**

Aucune rencontre ne doit être résolue uniquement par une fenêtre textuelle sur la carte du monde.

Les dialogues et les choix narratifs sont autorisés, mais ils interviennent à l'intérieur de la scène isométrique.

Le joueur doit pouvoir se déplacer, examiner son environnement, interagir avec les personnages, combattre, négocier, récupérer des ressources et quitter les lieux.

Une rencontre est une petite zone de jeu, pas une notification.

---

# 2. ORGANISATION DE L'ÉQUIPE

## RIVET : DÉVELOPPEMENT

Responsable de l'architecture technique et de l'intégration.

Missions :

- Étudier le système régional existant.
- Développer le gestionnaire de rencontres.
- Raccorder les événements à la carte du monde.
- Charger les environnements isométriques.
- Réutiliser les mécaniques existantes de déplacement, collision, dialogue, inventaire et combat.
- Assurer les transitions entre les scènes et la carte régionale.
- Préserver les sauvegardes et la progression.
- Intégrer les assets produits par Ocre.
- Publier régulièrement des versions fonctionnelles.

**Consigne particulière :** Ne pas reconstruire les moteurs déjà existants sans nécessité démontrée. Privilégier les extensions modulaires.

## OCRE : CRÉATION

Responsable de la conception artistique et narrative.

Missions :

- Créer les différents types de rencontres.
- Concevoir les environnements isométriques.
- Réaliser ou sélectionner les sprites nécessaires.
- Définir les PNJ, créatures, dialogues et comportements.
- Proposer des variantes de situations.
- Donner une identité visuelle aux différents biomes.
- Assurer la cohérence avec le lore du jeu.

**Consigne particulière :** Les décors doivent raconter quelque chose. Éviter les terrains vides avec trois ennemis placés au milieu.

## RÉGIE : PRODUCTION

Responsable de la coordination et des priorités.

Missions :

- Découper le développement en étapes livrables.
- Distribuer les tâches.
- Veiller à la cohérence entre les systèmes.
- Éviter la multiplication inutile des fonctionnalités secondaires.
- Optimiser l'utilisation du temps et des ressources.
- Organiser les publications.
- Surveiller les blocages techniques.
- Assurer le suivi du contenu réellement intégré.

**Consigne particulière :** Favoriser les fonctionnalités concrètes et jouables plutôt que les longues phases d'audit.

L'équipe doit travailler de manière collaborative, sans attendre une validation de l'auteur pour chaque choix technique mineur.

Les décisions artistiques structurantes et les modifications importantes du lore doivent en revanche être signalées.

---

# 3. ANALYSE DE L'EXISTANT

Avant de développer, consulter les éléments suivants.

### Système de voyage actuel

`src/core/voyage.js`

Ce module gère notamment :

- Le déplacement case par case.
- Le calcul des itinéraires.
- Les haltes.
- Le temps de voyage.
- La découverte des lieux.
- Le brouillard de guerre.
- Les interruptions potentielles du trajet.

Il comporte déjà un point d'extension pour les rencontres :

`onCaseEntree()`

**Ce système doit être conservé et enrichi.**

### Données régionales

`src/data/nml.js`

Le fichier contient les paramètres des terrains et les probabilités de rencontres.

La table `EVENEMENTS_ROUTE` est actuellement vide.

Elle doit devenir une véritable source de rencontres, ou être reliée à un catalogue spécialisé.

### Interface de la carte

`src/ui/carte_nml.js`

Conserver les fonctionnalités existantes et ajouter la transition vers les scènes jouables.

### Moteur principal

`src/core/game.js`

Il contient les mécanismes de déplacement local, transitions, dialogues, combats et sauvegardes.

Attention : les grilles des lieux sont actuellement constituées lors de l'initialisation du jeu. Ne pas supposer qu'une scène arbitraire peut être injectée à chaud sans adapter cette architecture.

### Système de combat

`src/core/combat.js`  
`src/data/combat.js`

Réutiliser les combats tactiques existants plutôt que développer un second système spécifique aux rencontres.

Adapter si nécessaire le choix des adversaires, les positions de combat et les conditions de déclenchement.

### Références historiques

Consulter également :

`reference/maquette/No-Mans-Land_Reconstruction/07_MAQUETTE_ARCHIVE_v0.13/`

La maquette historique contenait déjà plusieurs rencontres.

Ses descriptions, événements et idées constituent une base de travail, mais son ancien code ne doit pas être réintégré aveuglément dans l'architecture actuelle.

---

# 4. FONCTIONNEMENT GLOBAL DES RENCONTRES

## Étape 1 : déplacement régional

Le joueur quitte une ville et sélectionne sa destination sur la carte.

Son marqueur avance normalement.

À chaque nouvelle case, le système évalue la possibilité d'une rencontre.

Les probabilités doivent dépendre :

- Du type de terrain.
- De la région traversée.
- Des factions présentes.
- De certains événements du scénario.
- Des rencontres récentes.

Les probabilités existantes constituent la base initiale.

Ne pas les augmenter artificiellement simplement pour rendre le système visible.

## Étape 2 : déclenchement

Si une rencontre survient :

1. Le marqueur régional s'immobilise.
2. Le temps de voyage est mis en pause.
3. La position régionale est enregistrée.
4. L'itinéraire restant est conservé.
5. Le type de rencontre est déterminé.
6. Le jeu charge l'environnement isométrique correspondant.

Une courte transition visuelle peut être utilisée.

L'objectif est de rester cohérent avec l'interface existante, sans introduire un écran supplémentaire inutile.

## Étape 3 : arrivée dans la rencontre

Le joueur apparaît à un emplacement adapté.

L'environnement doit être entièrement navigable.

Selon la situation, des personnages, véhicules, objets, ennemis ou créatures peuvent déjà être présents.

Les entités ne doivent pas toutes apparaître au même endroit.

La mise en scène doit favoriser une découverte progressive.

Par exemple, une caravane peut être visible au loin, tandis que ses gardes surveillent les abords d'un camion.

## Étape 4 : exploration libre

Le joueur décide lui-même comment agir.

Il peut notamment :

- Approcher un groupe.
- L'éviter.
- Engager la conversation.
- Examiner un véhicule.
- Fouiller des caisses.
- Récupérer des objets.
- Déclencher un combat.
- Battre en retraite.
- Quitter la zone.

Les possibilités exactes dépendent de la rencontre.

**Ne pas imposer systématiquement une conversation ou un combat dès l'arrivée.**

## Étape 5 : retour au voyage

Lorsque le joueur quitte la scène :

- Le jeu revient sur la carte régionale.
- La progression du voyage est restaurée.
- La position du marqueur est conservée.
- Les ressources utilisées restent consommées.
- Les objets récupérés restent dans l'inventaire.
- Les conséquences de la rencontre sont enregistrées.

Le joueur peut reprendre son trajet vers la destination initiale ou choisir un autre itinéraire lorsque le système le permet.

Ne jamais replacer automatiquement le joueur dans sa ville de départ.

---

# 5. BIBLIOTHÈQUE D'ENVIRONNEMENTS ISOMÉTRIQUES

Créer des environnements réutilisables, compatibles avec le moteur actuel.

L'idée n'est pas de générer une carte entièrement différente pour chaque événement.

Il faut plutôt développer une bibliothèque de scènes dont les objets, personnages et situations peuvent varier.

## Environnements prioritaires

### A. Route désertique

Grande piste poussiéreuse traversant des terres arides.

Éléments :

- Route endommagée.
- Épaves.
- Rochers.
- Panneaux rouillés.
- Végétation morte.
- Débris de véhicules.
- Traces de pneus.

Utilisation : caravanes, négociants, convois et pillards.

### B. Terrain rocheux

Relief irrégulier avec obstacles naturels.

Éléments :

- Affleurements rocheux.
- Passages étroits.
- Petites falaises.
- Éboulis.
- Abris naturels.

Utilisation : embuscades, créatures territoriales et cachettes.

### C. Forêt dégradée

Forêt sauvage marquée par les mutations et les catastrophes.

Éléments :

- Arbres morts ou altérés.
- Racines.
- Carcasses.
- Ruines envahies.
- Petites clairières.
- Végétation mutante.

Utilisation : rencontres animales, survivants isolés et découvertes.

### D. Zone vitrifiée

Étendue dévastée rappelant les conséquences des catastrophes nucléaires.

Éléments :

- Sol fondu et vitrifié.
- Roches noircies.
- Carcasses métalliques.
- Débris anciens.
- Cratères secondaires.
- Poches de contamination.

Utilisation : récupérateurs, créatures dangereuses, drones et événements environnementaux.

### E. Poste routier abandonné

Ancienne infrastructure partiellement détruite.

Éléments :

- Barrages.
- Guérites.
- Véhicules de contrôle.
- Containers.
- Bâtiments techniques.
- Zones de stockage.

Utilisation : péages de pillards, patrouilles, groupes de négociants et camps temporaires.

## Directives artistiques

Conserver la vue isométrique du jeu.

Les assets doivent respecter :

- L'échelle des personnages et véhicules.
- Les proportions existantes.
- La perspective.
- Le point d'ancrage au sol.
- Les collisions.
- La lisibilité des chemins.
- La direction artistique post-apocalyptique.

Aucun asset ne doit être étiré indépendamment sur ses axes pour le faire correspondre à une emprise.

Éviter également les scènes artificiellement surchargées.

La densité doit servir la crédibilité de l'endroit.

Les environnements peuvent partager des éléments, mais leur implantation doit varier suffisamment pour empêcher l'impression de toujours visiter le même terrain.

---

# 6. PREMIER CATALOGUE DE RENCONTRES

Développer les rencontres suivantes, en réutilisant les concepts historiques de la maquette.

## RENCONTRE 01 : LE CONVOI ENSABLÉ

**Type :** Exploration et interaction sociale.

Un camion de transport est immobilisé dans le désert.

Son équipage tente de réparer le véhicule.

Possibilités :

- Proposer de l'aide.
- Négocier une récompense.
- Commercer.
- Examiner la cargaison.
- Voler discrètement.
- Attaquer les transporteurs.
- Ignorer le convoi.

Prévoir plusieurs variantes : transport médical, eau, pièces mécaniques ou marchandises de contrebande.

## RENCONTRE 02 : LA CARAVANE MARCHANDE

**Type :** Commerce et rencontre pacifique.

Une petite caravane effectue une halte.

Plusieurs commerçants et gardes entourent les véhicules.

Possibilités :

- Acheter.
- Vendre.
- Négocier.
- Demander des informations.
- Obtenir des renseignements sur les routes.
- Éventuellement tenter un vol.

Les marchandises doivent correspondre à l'inventaire du jeu.

Utiliser un stock limité et cohérent avec l'identité des négociants.

## RENCONTRE 03 : LE VOYAGEUR BLESSÉ

**Type :** Rencontre sociale et choix moral.

Un voyageur est retrouvé près d'une épave.

Possibilités :

- Lui apporter des soins.
- Lui donner des ressources.
- L'interroger.
- Le dépouiller.
- L'abandonner.
- Découvrir les circonstances de son accident.

Certaines variantes peuvent révéler un piège, mais ce ne doit pas devenir systématique.

## RENCONTRE 04 : LE PÉAGE DES PILLARDS

**Type :** Hostile ou négociable.

Un groupe armé contrôle une portion de route.

Possibilités :

- Payer un droit de passage.
- Négocier.
- Intimider.
- Chercher un contournement.
- Attaquer.
- Tenter de fuir.

Le groupe doit réagir à l'attitude du joueur.

Un paiement ne doit pas automatiquement déclencher un combat.

## RENCONTRE 05 : LES MUTANTS ERRANTS

**Type :** Rencontre hostile.

Un groupe de mutants déments ou de créatures dangereuses occupe une zone.

Possibilités :

- Se déplacer discrètement.
- Contourner les ennemis.
- Attirer leur attention ailleurs.
- Combattre.
- Fuir.

Prévoir des dispositions variables.

Le combat doit utiliser le système tactique existant.

## RENCONTRE 06 : LA PATROUILLE IO

**Type :** Rencontre de faction.

Une patrouille inspecte une route ou un ancien point de contrôle.

Son attitude dépend de la situation du joueur et de ses éventuels antécédents.

Possibilités :

- Se soumettre à une inspection.
- Discuter.
- Mentir.
- Montrer une autorisation si le système le permet.
- Éviter les soldats.
- Résister.

Attention à la cohérence politique et technologique de l'IO.

## RENCONTRE 07 : LA TEMPÊTE DE POUSSIÈRE

**Type :** Environnementale.

Une tempête surprend le joueur dans une région exposée.

La rencontre se déroule dans une véritable zone isométrique.

Le joueur doit pouvoir :

- Chercher un abri.
- Explorer une épave.
- Attendre une accalmie.
- Risquer une traversée.
- Récupérer des ressources.

Les effets de poussière doivent être visibles, sans masquer totalement le gameplay.

## RENCONTRE 08 : LA FAUNE MUTANTE

**Type :** Rencontre animale.

Une ou plusieurs créatures sauvages occupent un territoire.

Elles ne sont pas obligatoirement agressives.

Certaines peuvent s'enfuir, observer le joueur ou défendre une carcasse.

Éviter les comportements purement humains chez les animaux.

Les créatures doivent avoir une identité biologique et visuelle cohérente avec l'environnement.

## EXTENSIONS ULTÉRIEURES

Après ce premier catalogue, prévoir notamment :

- Camps temporaires de survivants.
- Groupes de négociants indépendants.
- Contrebandiers.
- Scientifiques en expédition.
- Mercenaires.
- Récupérateurs.
- Caravanes attaquées.
- Conflits entre factions.
- Signaux de détresse.
- Épaves inhabitées.
- Rencontres rares et insolites.

Ne pas bloquer la première livraison pour réaliser l'intégralité de cette liste.

---

# 7. COMPORTEMENTS ET INTELLIGENCE ARTIFICIELLE

Les rencontres doivent paraître vivantes.

Cependant, ne développez pas un nouveau moteur comportemental complet.

Réutilisez et étendez les systèmes disponibles.

## Comportements prioritaires

**Neutre :** Le personnage reste occupé à son activité et ne devient pas hostile sans raison.

**Prudent :** Le personnage observe le joueur, peut lui demander de s'arrêter ou réagir à une intrusion.

**Hostile :** L'ennemi peut attaquer lorsque les conditions sont réunies.

**Animal :** La créature privilégie la fuite, la défense de territoire ou la chasse selon son espèce.

**Marchand :** Le PNJ peut discuter et commercer.

**Blessé :** Le PNJ peut demander de l'aide ou rester immobilisé.

Privilégier des comportements simples et fiables.

Une caravane dont les membres discutent, surveillent la route et réagissent aux provocations est préférable à une simulation complexe mais instable.

---

# 8. RÈGLES DE GÉNÉRATION ALÉATOIRE

Le système doit produire de la variété sans devenir incohérent.

## Conditions de sélection

Chaque rencontre doit disposer de données précisant :

- Son identifiant.
- Sa catégorie.
- Les biomes autorisés.
- Ses conditions de déclenchement.
- Sa rareté.
- Sa scène isométrique.
- Ses personnages.
- Ses variantes possibles.
- Ses issues.
- Ses conséquences.
- Ses règles de répétition.

## Cohérence régionale

Une patrouille IO doit être plus probable sur les routes qu'elle contrôle.

Une créature sauvage peut apparaître loin des centres urbains.

Les caravanes empruntent principalement les voies praticables.

Les mutants dangereux peuvent être plus présents près des régions contaminées.

Ne pas placer aléatoirement une rencontre sans tenir compte de la géographie.

## Répétitions

Éviter qu'un même événement soit sélectionné plusieurs fois d'affilée.

Mettre en place une mémoire légère des rencontres récentes.

Certaines rencontres peuvent revenir avec des variantes.

D'autres, notamment les événements uniques, ne doivent plus apparaître une fois résolus.

## Fréquence

Conserver les probabilités existantes comme base d'équilibrage.

Prévoir un réglage centralisé permettant de modifier la fréquence globale sans réécrire les événements.

Un voyage court peut parfaitement se dérouler sans rencontre.

Une longue traversée doit offrir davantage d'occasions de découvrir le monde.

---

# 9. CONSÉQUENCES ET PERSISTANCE

Les rencontres doivent exploiter les systèmes de progression existants.

Un événement peut affecter :

- Les points de vie.
- Les munitions.
- L'inventaire.
- L'argent.
- Les ressources.
- Le temps.
- La réputation.
- Les relations avec une faction.
- Certains états de quête.

Les conséquences doivent rester cohérentes après le retour sur la carte.

Un objet récupéré ne doit pas disparaître.

Une récompense ne doit pas pouvoir être encaissée indéfiniment en rechargeant la même rencontre.

Un personnage éliminé ne doit pas réapparaître immédiatement dans la même instance sans raison.

## Sauvegarde

Prévoir un état persistant de rencontre contenant au minimum :

- L'identifiant de l'événement.
- Le modèle de scène.
- Sa variante.
- La case régionale.
- Les objets déjà récupérés.
- Les interactions réalisées.
- Les personnages neutralisés.
- Les états narratifs.
- L'itinéraire à reprendre.

L'objectif est de permettre une sauvegarde et un rechargement pendant l'exploration d'une rencontre.

**Attention :** Le moteur de combat actuel ne sauvegarde pas l'intégralité des combats en cours.

Ne pas prétendre que cette fonctionnalité fonctionne sans adaptation.

Pour la première version, privilégier une sauvegarde fiable hors combat et un point de reprise sécurisé avant l'engagement. La sauvegarde au milieu d'un combat pourra être étendue ultérieurement.

L'essentiel est de ne pas corrompre la partie.

---

# 10. TRANSITION ENTRE CARTE ET SCÈNE

Cette partie est particulièrement importante pour Rivet.

Le système actuel possède déjà les statuts régionaux de départ, route et halte.

Créer une gestion explicite des rencontres sans casser ces états.

### Principes

1. Une rencontre suspend le trajet sans l'effacer.
2. La rencontre active est enregistrée dans les données de la partie.
3. Le lieu isométrique correspondant est chargé.
4. Le joueur utilise les commandes habituelles du jeu.
5. Les interactions modifient les données normales de progression.
6. Quitter la scène restaure la carte régionale.
7. Le trajet restant peut être repris.
8. Aucune nouvelle rencontre n'est tirée pendant la résolution de la rencontre active.

## Recommandation architecturale

Pour limiter les risques techniques, commencer avec des modèles de scènes isométriques déclarés avant l'initialisation du moteur.

Le contenu d'une rencontre peut ensuite varier grâce à son état et à son identifiant.

Cette méthode est préférable, pour le premier lot, à la création entièrement dynamique de nouveaux mondes et grilles en cours de partie.

L'enregistrement des lieux, des grilles, des PNJ et des combats doit rester compatible avec `createGame()`.

Si une adaptation du moteur est nécessaire, la garder modulaire et documentée.

Ne pas dupliquer le rendu isométrique.

Ne pas développer un second système de déplacement.

Ne pas créer un inventaire réservé aux rencontres.

Ne pas remplacer la sauvegarde existante.

**Le joueur doit avoir l'impression d'explorer une nouvelle partie du même jeu, pas de lancer un mini-jeu indépendant.**

---

# 11. DIRECTION ARTISTIQUE ET NARRATIVE

No Man's Land est un univers post-apocalyptique mature, brutal, parfois absurde, traversé par un humour noir satirique.

Les rencontres doivent respecter cette identité.

Il ne faut pas transformer chaque événement en tragédie ni chaque conversation en plaisanterie.

La variété des tons est essentielle.

Certaines rencontres peuvent être :

- Inquiétantes.
- Violentes.
- Mélancoliques.
- Étranges.
- Drôles.
- Cyniques.
- Touchantes.
- Moralement ambiguës.

Un marchand peut vendre des pièces détachées au milieu de nulle part.

Une patrouille peut appliquer avec un sérieux bureaucratique une réglementation totalement absurde.

Un survivant peut refuser de quitter une épave parce qu'il attend quelqu'un qui ne reviendra jamais.

Une créature mutante peut simplement défendre sa progéniture.

L'objectif est de créer des situations crédibles et mémorables, pas une succession de combats sans contexte.

## Dialogues

Respecter le style narratif du jeu.

Les personnages doivent posséder des motivations distinctes.

Éviter les dialogues génériques et les longues expositions artificielles.

Favoriser les échanges permettant au joueur de comprendre progressivement la situation.

Les compétences du personnage peuvent offrir des possibilités supplémentaires lorsque les mécaniques correspondantes existent.

## Visuels

Les effets d'ambiance peuvent inclure :

- Poussière animée.
- Fumée.
- Lumières vacillantes.
- Étincelles.
- Éclairage de véhicules.
- Brouillard.
- Particules environnementales.

Ils doivent rester légers et ne pas nuire à la lisibilité du jeu, notamment sur mobile.

---

# 12. COMPATIBILITÉ MOBILE ET INTERFACE

Le jeu doit rester utilisable sur téléphone, notamment sur les écrans pliables.

Les rencontres utilisent la caméra et les commandes normales du jeu.

Prévoir :

- Déplacement tactile.
- Zoom.
- Sélection des PNJ.
- Interactions avec les objets.
- Accès au combat.
- Accès à l'inventaire.
- Sortie de rencontre clairement identifiable.

Ne pas développer une nouvelle interface complète pour ces scènes.

Privilégier les composants déjà présents.

Les messages contextuels doivent rester courts et ne pas recouvrir inutilement le terrain.

---

# 13. OUTILS DE DÉVELOPPEMENT

Ajouter un accès aux rencontres depuis le mode développeur existant.

Objectif : permettre à l'équipe de vérifier directement une scène sans effectuer un long voyage depuis Dusk-Town.

Fonctionnalités minimales :

- Sélectionner une rencontre.
- Choisir éventuellement une variante.
- Charger immédiatement la scène.
- Revenir au point de départ du test.

Ce raccourci doit être réservé au mode DEV.

Il ne doit pas apparaître dans le jeu normal.

Les parties de test doivent rester séparées des sauvegardes de campagne lorsque cela est possible.

Cette fonctionnalité doit rester simple. Ne pas créer un laboratoire de simulation complet.

---

# 14. PLAN DE PRODUCTION

Le travail doit être réalisé par étapes successives.

**Chaque étape fonctionnelle doit être intégrée et publiée avant de passer à une longue phase de vérification.**

## PHASE A : PREMIÈRE RENCONTRE JOUABLE

Priorité absolue.

Développer le fonctionnement complet avec une première rencontre : **la caravane marchande**.

Elle doit permettre :

- Le déclenchement pendant un trajet.
- Le chargement d'une véritable zone isométrique.
- Le déplacement du joueur.
- La présence de PNJ.
- Une conversation.
- Un échange commercial.
- Une sortie de zone.
- La reprise du voyage.

Cette première rencontre servira de modèle technique.

Ne pas développer les huit rencontres simultanément avant de disposer de cette boucle complète.

## PHASE B : RENCONTRES HOSTILES

Ajouter :

- Le péage des pillards.
- La faune mutante.

Objectif : faire fonctionner les comportements hostiles, le combat, l'évitement et la fuite.

Réutiliser le moteur tactique existant.

## PHASE C : VARIÉTÉ DES SITUATIONS

Intégrer :

- Le convoi ensablé.
- Le voyageur blessé.
- Les mutants errants.
- La patrouille IO.
- La tempête de poussière.

Les huit rencontres prioritaires doivent alors être accessibles et jouables.

Leur finition artistique pourra varier, mais aucune ne doit se résumer à un événement textuel.

## PHASE D : ENRICHISSEMENT

Une fois les huit rencontres fonctionnelles :

- Ajouter des variantes.
- Améliorer les compositions des décors.
- Affiner les comportements.
- Ajouter les réactions aux factions.
- Réduire les répétitions.
- Enrichir le catalogue.
- Corriger les principaux défauts visuels.

Ne pas inverser cet ordre en perfectionnant indéfiniment une seule scène.

---

# 15. POLITIQUE DE TEST : LÉGÈRE ET PRAGMATIQUE

## DIRECTIVE PRIORITAIRE

L'équipe a précédemment consacré trop de ressources à des cycles répétitifs de tests, diagnostics et corrections.

Cette méthode ne doit pas se reproduire.

**La priorité est de produire du contenu réellement jouable.**

Les tests servent à identifier les défauts bloquants, pas à retarder indéfiniment la livraison.

## Méthode imposée

Pour chaque grande étape :

1. Développer.
2. Intégrer.
3. Publier une version fonctionnelle.
4. Effectuer quelques vérifications ciblées.
5. Corriger les défauts bloquants.
6. Continuer la production.

Ne pas attendre une couverture complète des tests pour publier un contenu utilisable.

## Vérifications prioritaires

Se concentrer sur cinq situations :

**Test 1 :** Un voyage déclenche une rencontre et charge correctement sa scène isométrique.

**Test 2 :** Le joueur peut se déplacer, interagir et quitter une rencontre pacifique.

**Test 3 :** Une rencontre hostile déclenche correctement le combat et permet une issue.

**Test 4 :** Le retour à la carte conserve les ressources et l'itinéraire.

**Test 5 :** Une sauvegarde réalisée hors combat dans une rencontre peut être rechargée sans perdre l'état de l'événement.

Ces vérifications peuvent être automatisées si cela reste simple.

Ne pas construire une infrastructure complexe de tests autour de ce premier lot.

## Gestion des anomalies

**Bloquant :** Le jeu ne démarre pas, le joueur reste enfermé, une transition échoue, un combat est impossible à terminer ou une sauvegarde est corrompue.

À corriger prioritairement.

**Important mais non bloquant :** Problème d'affichage, PNJ mal positionné, déséquilibre ou défaut visuel.

À noter et corriger dans une passe dédiée.

**Mineur :** Animation imparfaite, décoration secondaire, détail de texte, petite imperfection artistique.

Ne doit pas interrompre toute la production.

## Règle anti-blocage

Si un test automatisé devient trop complexe à maintenir ou donne des résultats douteux :

- Consigner le problème.
- Effectuer une vérification manuelle ciblée si possible.
- Corriger uniquement si le problème est confirmé.
- Reprendre la production.

Ne pas relancer en boucle les mêmes tests sans modification pertinente.

Ne pas réécrire plusieurs systèmes existants pour satisfaire un test secondaire.

Ne pas annoncer comme testé ce qui ne l'a pas été.

**Régie doit activement empêcher les boucles improductives de diagnostic.**

---

# 16. PUBLICATION ET LIVRABLES

Le développement doit aboutir à une intégration réelle dans le dépôt GitHub.

Il ne s'agit pas de produire une démonstration indépendante.

Les fonctionnalités doivent être accessibles depuis le jeu normal.

## Livrables attendus

1. Un gestionnaire de rencontres intégré au moteur régional.
2. Des scènes isométriques réutilisables.
3. Huit rencontres prioritaires réellement jouables.
4. Des événements adaptés aux terrains.
5. Des transitions fiables entre carte et rencontres.
6. Des interactions sociales et hostiles.
7. Des conséquences persistantes.
8. Une reprise correcte du voyage.
9. Un accès rapide aux rencontres depuis le mode DEV.
10. Une documentation synthétique indiquant les fonctionnalités réellement terminées.

## Publication

Publier la progression fonctionnelle au fil des phases.

Ne pas laisser l'ensemble des modifications uniquement dans un environnement temporaire.

Avant une publication, vérifier que la version ne présente pas de défaut bloquant connu.

Une fois une phase publiée, fournir :

- Le lien du commit ou de la branche.
- Les fonctionnalités intégrées.
- Les rencontres accessibles.
- Les éventuelles limitations restantes.
- Le résultat des quelques vérifications effectuées.

Ne pas présenter une fonctionnalité comme terminée si elle n'est encore qu'une structure de code non reliée au jeu.

---

# 17. INTERDICTIONS ET ERREURS À ÉVITER

L'équipe ne doit pas :

- Recommencer le jeu depuis zéro.
- Remplacer le moteur isométrique.
- Refaire entièrement la carte régionale.
- Créer des rencontres uniquement textuelles.
- Produire des zones impossibles à explorer.
- Multiplier les scènes vides avec des ennemis immobiles.
- Réutiliser des assets en déformant leurs proportions.
- Casser les sauvegardes existantes.
- Modifier les villes sans nécessité.
- Introduire des mécanismes incompatibles avec le lore.
- Bloquer la production sur des tests interminables.
- Développer un framework générique disproportionné.
- Construire un système complexe de simulation économique avant que les rencontres soient jouables.
- Ajouter une fonctionnalité visuellement annoncée mais non fonctionnelle.

L'équipe doit privilégier les solutions simples, réutilisables et directement intégrées.

---

# 18. CRITÈRES DE RÉUSSITE

La mission sera considérée comme fonctionnellement réussie lorsque le joueur pourra :

1. Quitter Dusk-Town en direction de Steel-Megalopolis.
2. Voir son marqueur progresser sur la carte.
3. Être interrompu par une rencontre aléatoire.
4. Découvrir une véritable zone isométrique.
5. Se déplacer dans cette zone.
6. Interagir avec les personnages ou les objets.
7. Résoudre la situation de plusieurs manières lorsque le scénario le permet.
8. Récupérer ou perdre des ressources.
9. Quitter la rencontre.
10. Retrouver sa position régionale et reprendre son voyage.

Ces fonctionnalités devront exister dans le jeu publié et pas uniquement dans une maquette.

---

# 19. PHILOSOPHIE FINALE

No Man's Land ne doit pas donner l'impression que ses villes sont les seuls lieux habités du monde.

Entre deux destinations, il existe des survivants, des factions, des créatures, des négociants, des opportunistes et des gens qui tentent simplement de continuer à vivre.

Le voyage doit rendre cette réalité perceptible.

Certaines rencontres seront insignifiantes à l'échelle du monde, mais mémorables pour le joueur.

D'autres pourront avoir des conséquences à long terme.

Il ne faut pas chercher à rendre chaque trajet spectaculaire. Le silence et les territoires vides font également partie de l'atmosphère.

L'essentiel est que le joueur ne puisse jamais être totalement certain de ce qu'il trouvera sur la route.

**Le monde ne doit pas attendre le joueur pour exister.**

---

# 20. ORDRE FINAL À L'ÉQUIPE

**Rivet :** Construis et intègre le système de rencontres en t'appuyant sur les moteurs existants. Commence par une caravane marchande complètement jouable, puis généralise.

**Ocre :** Prépare les environnements, les personnages et les situations des huit rencontres prioritaires. Recherche la variété visuelle et narrative, sans perdre la cohérence de No Man's Land.

**Régie :** Coordonne les étapes, arbitre les priorités et assure des publications régulières. Empêche les dérives de périmètre et les boucles de tests improductives.

**Priorité collective :**

**PRODUIRE → INTÉGRER → PUBLIER → VÉRIFIER L'ESSENTIEL → ENRICHIR**

Ne pas inverser cette logique.

L'auteur autorise les décisions techniques et créatives nécessaires à la réalisation de cet objectif, sous réserve de conserver l'identité du jeu et les règles fondamentales de son univers.

**LIVRABLE ATTENDU : UN NO MAN'S LAND OÙ LE VOYAGE DEVIENT UNE VÉRITABLE AVENTURE ISOMÉTRIQUE.**

**Fin de consigne.**
