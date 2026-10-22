PAGES=[]
def page(section,title,intro='',blocks=None,table=None,note=None,mock=None):
    PAGES.append(dict(section=section,title=title,intro=intro,blocks=blocks or [],table=table,note=note,mock=mock))

page('Cadre','Une refonte pour jouer',
 'L’interface de No Man’s Land doit rendre les décisions faciles à comprendre tout en laissant voir le monde. Ce dossier propose une refonte complète de l’expérience joueur et un atelier développeur pour atteindre, inspecter et modifier les différentes situations du jeu.',[
 ('Statut','Tout ce qui est présenté comme refonte, maquette, commande développeur ou animation est PROPOSÉ. Le jeu de référence reste la version 0.6. Aucun écran du site publié n’a été modifié pour cette livraison.'),
 ('Objectifs','Savoir où l’on est, ce qui peut être fait et ce que cela coûte ; retrouver les fonctions sans mémoriser une suite de menus ; adapter l’interface à son écran, ses commandes et sa lecture. Les choix importants restent compréhensibles sans afficher toutes les statistiques en permanence.'),
 ('Périmètre','Exploration, combat, dialogue, personnage, inventaire, commerce, fabrication, piratage, trois échelles de cartes, journal, compagnon, caravanes, conflits, sauvegardes, options et aide. Les systèmes futurs s’appuient sur le dossier Gameplay et personnages v0.1, sans être annoncés comme déjà jouables.'),
 ('Mode développeur','Accès aux scènes et séquences, issues de quête, dialogues, états du personnage et situations de test. Deux usages distincts : préparer une situation cohérente, ou inspecter volontairement un cas défectueux. Les modifications sont visibles, isolées dans une partie de test et réversibles.'),
 ('Livraison','Spécifications fonctionnelles, règles visuelles, comportements des commandes, animations chiffrées, maquettes vectorielles et critères de validation. Les fonds de terrain des maquettes sont schématiques ; ils ne proposent pas un remplacement des plans de villes.')])

page('Audit','Ce qui existe et ce qui manque',
 'Audit des sources app.js, index.html et feuilles de style de la v0.6, sur l’instantané 07724023af4978a5c99d9c281c6f76d1cb746e2f. Il s’agit d’un examen du code et de la structure, pas d’un test utilisateur dans un navigateur.',table=(['Existant vérifié','Constat','Orientation proposée'],[
 ['HUD et actions','8 actions fixes, santé, radiations, fatigue, PA, arme, journal et minicarte.','Hiérarchie par contexte, barre configurable et panneau d’information repliable.'],
 ['Ciblage','Torse, tête, bras, jambes ; chance, coût, PV, protection et couvert.','Prévisualiser ensemble déplacement, portée et PA restants ; expliquer une action refusée.'],
 ['Menus','Une infrastructure de fenêtre modale sert aux dialogues et à la plupart des écrans.','Cadres adaptés : dialogue, panneau latéral, espace de gestion et boîte de décision.'],
 ['Navigation','Clavier, clic et gestes ; focus initial, retour au bouton d’origine et boucle Tab dans la modale.','Parcours cohérent à tous les niveaux ; graphe de focus manette ; zones tactiles dédiées.'],
 ['Réglages','Audio activable, zoom, grille ; adaptation CSS aux tailles ; règle de mouvement réduit dans le style principal.','Menu complet de réglages, texte indépendant, profils de HUD, animations et remappage.'],
 ['Informations','Journal, manuel, liste des éléments du terrain ; quelques raisons d’échec en message bref.','Aides à deux niveaux, recherche, état verrouillé explicable et informations limitées à ce qui est connu.'],
 ['Mode développeur','Aucun menu ni module dev/debug/cheat trouvé dans les sources chargées.','Atelier de scénarios, inspecteurs, catalogue de contenu et console de commandes typées.']
 ]),note='Ne pas présenter les réglages avancés, la manette complète ou le mode développeur comme disponibles aujourd’hui. Les migrations devront conserver les raccourcis et habitudes déjà acquis lorsque c’est possible.')

page('Références','Des classiques aux usages récents',
 'Les références servent à choisir des principes, pas à copier une interface. Les observations ci-dessous viennent de manuels ou publications de leurs créateurs. Les décisions pour No Man’s Land restent des propositions de ce dossier.',table=(['Référence primaire','Observation retenue','Application à No Man’s Land'],[
 ['Fallout 1 · manuel [R1]','La barre regroupe objet actif, munitions, santé, PA et retours d’action. La carte mondiale possède son échelle de déplacement.','Un socle tactique stable en bas ; cartes régionale et locale distinctes ; coût et réponse d’action à portée du regard.'],
 ['Fallout 2 · manuel [R2]','Les compagnons disposent d’inventaire et de réglages de combat ; carte, dialogue et commerce sont des espaces identifiables.','Fiche de compagnon avec ordres lisibles ; responsabilités claires entre parler, donner du matériel et combattre.'],
 ['Baldur’s Gate 3 · Larian [R3]','Barre organisée en groupes déplaçables et masquables, filtrage des actions.','Groupes d’actions configurables ; un accès “Toutes les actions” conservé même si la barre est réduite.'],
 ['BG3 · notes de mise à jour [R4]','Les états de concentration sont explicités ; corrections de focus, disposition des options et navigation à la manette.','Avertissements liés à l’action exacte ; options prévisualisées ; test de chaque panneau avec plusieurs commandes.'],
 ['Avowed · Obsidian [R5]','Taille du texte UI et sous-titres, fond des sous-titres, commandes remappables et réduction des effets de caméra.','Échelle de lecture indépendante du HUD ; réglages de mouvement et de commandes séparés.'],
 ['Xbox Accessibility Guidelines [R6–R7]','Texte lisible et contrôles des contenus animés ou actualisés dans les interfaces de lecture.','Contraste vérifié, fond opaque réglable, pause des mises à jour et mouvement réduit.']
 ]),note='Le dossier n’imite pas le vieillissement des commandes des années 1990. Les petites cibles, le texte minuscule et les changements de curseur peu explicites n’apportent pas de profondeur tactique.')

page('Direction visuelle','Un instrument de terrain',
 'La proposition repose sur une interface sombre, précise et chaleureuse par sa typographie et ses matières. Elle peut évoquer un équipement de terrain sans supposer que chaque personnage possède une puce ISIO.',[
 ('Socle commun','Surfaces graphite opaques ou légèrement translucides, texte ivoire, séparateurs fins et icônes dessinées dans une même famille. Le monde reste le premier élément de l’écran. Une seule couleur d’accent indique l’action sélectionnée ; le danger garde son code sémantique distinct.'),
 ('Identité régionale','Terres extérieures : bordures mates, traces discrètes et sons plus secs. Intérieur de Steel-Megalopolis : contours nets, lumière contrôlée et micro-signaux techniques. Upper-Town peut employer une finition claire et dorée dans ses supports locaux. Le HUD ne devient pas une armure de faction.'),
 ('Cohérence du lore','Les supports IO peuvent être noirs avec rappels rouges ; les lentilles actives bleues et les équipements présidentiels blancs et dorés restent des caractéristiques du monde. Ces couleurs ne signifient pas que tous les panneaux du joueur appartiennent à IO.'),
 ('Typographie','Police de lecture sans empattement pour texte, chiffres tabulaires pour quantités, police de titre sobre. Pas de paragraphes en capitales. Les acronymes sont expliqués à la première rencontre ; les étiquettes importantes restent accompagnées de mots.'),
 ('Décor UI','Grain très léger et statique, uniquement sur les surfaces. Aucun filtre CRT, balayage, texte brouillé ou scintillement obligatoire. Les contrastes de la scène ne doivent jamais rendre un panneau illisible.')],mock='explore')

page('Hiérarchie','Ce qui reste et ce qui apparaît',table=(['Niveau','Information','Règle d’affichage'],[
 ['Permanent','PV, situation actuelle, arme ou action active, accès au menu et aux actions essentielles.','Visible dans tout contexte concerné ; taille stable et placement prévisible.'],
 ['Contextuel','PA en combat ; coût de déplacement ; porte sélectionnée ; départ de voyage ; ordre du compagnon.','Apparaît lorsque la décision en dépend ; ne déplace pas les commandes déjà sous le pointeur.'],
 ['À la demande','Détail des calculs, états complets, historique, biographies connues, réputation et stocks.','Survol/focus puis épinglage, panneau ou écran de gestion. Ne masque pas une cible au moment du tir.'],
 ['Alerte','Danger létal, contrôle d’accès incompatible, perte de progression possible, ressource critique.','Message court avec raison et réponse disponible. L’urgence ne repose jamais sur une couleur seule.']
 ]),blocks=[('Budget visuel proposé','Exploration : une carte d’objectif compacte, une seule invite d’interaction et deux informations récentes au maximum. Combat : action, coût, cible et fin de tour prioritaires. Les alertes mineures sont regroupées dans l’historique.'),('Aucun masquage arbitraire','Un mode discret peut réduire une jauge normale mais doit la rétablir à la demande ou au seuil d’alerte. Santé critique, PA insuffisants et interdiction de passage restent explicables. Les options “toujours visible” donnent la main au joueur.'),('Diffusion progressive','Premier niveau : phrase courte, par exemple “Il manque 1 PA”. Second niveau : calcul détaillé épinglable. Les deux doivent lire le même résultat du moteur, sans calcul parallèle qui pourrait diverger.')])

page('Navigation','Des espaces adaptés aux tâches',table=(['Espace','Usage','Sortie et continuité'],[
 ['Terrain','Exploration et combat ; action sélectionnée, chemin et cible.','Annuler quitte d’abord la visée, puis la sélection ; ouvre ensuite le menu de pause.'],
 ['Panneau latéral','Inspection courte d’objet, détails d’état, commandes du compagnon.','Retour conserve cible, zoom et position de caméra.'],
 ['Espace de gestion','Inventaire, personnage, commerce, fabrication, journal et cartes.','Onglets stables ; recherche et défilement conservés par écran pendant la session.'],
 ['Dialogue','Texte, interlocuteur, réponses et conditions ; historique de cet échange.','Retour ne choisit pas une réplique. Sortie disponible selon la scène, sans saut de branche caché.'],
 ['Boîte de décision','Achat engageant, action hostile, reprise qui écrase l’état de travail.','Résumé exact de l’effet ; bouton de retour au focus initial. Pas de confirmation pour ouvrir un menu.'],
 ['Atelier développeur','Scénarios, inspecteurs et outils réservés aux parties de test.','Peut se refermer sans perdre la situation testée ; partie de jeu d’origine conservée.']
 ]),blocks=[('Ordre de priorité','Une seule couche de décision engageante à la fois. Une fiche peut rester épinglée, mais n’ouvre pas une cascade de fenêtres modales. Les infobulles ne capturent pas les commandes de déplacement sans raison.'),('Retour prévisible','La commande Annuler ferme le niveau courant. Revenir au terrain ne réapplique pas une action ou une dépense. Après fermeture, focus et sélection retrouvent une cible encore valide ; sinon, un voisin logique est choisi.')])

page('Exploration','Un HUD qui laisse respirer le terrain',
 'Le HUD de base ne doit pas ressembler à un tableau de bord rempli à toutes les places. Les éléments s’organisent autour de la décision actuelle et laissent libre le centre de la scène.',table=(['Zone proposée','Contenu','Comportement'],[
 ['Haut gauche','Lieu, sous-lieu, heure ; météo seulement utile à la décision.','Deux lignes au maximum en mode compact ; détail en focus.'],
 ['Haut droit','Minicarte et objectif suivi court, modules masquables séparément.','La minicarte ne révèle ni PNJ caché ni couloir non découvert. Objectif développé à la demande.'],
 ['Bas gauche','Portrait du joueur, PV, état dominant ; compagnon s’il est présent.','Rad/fatigue affichées si demandées ou pertinentes ; pas de portrait compagnon fantôme avant recrutement.'],
 ['Bas centre','Arme, actions favorites et accès “Toutes les actions”.','6 à 8 emplacements visibles selon format. Barre verrouillable, ordre personnel et noms courts.'],
 ['Près de l’élément','Invite “Parler”, “Examiner”, “Entrer” avec distance et coût utile.','Placée hors de la silhouette ; une seule invite active. Le bouton confirme une action décrite.'],
 ['Bord discret','Derniers événements regroupés et accès au journal.','Ne recouvre pas un accès ni un choix. L’historique complet reste consultable.']
 ]),note='La liste actuelle des entités couvre des éléments de toute la scène. La refonte doit séparer “visible à proximité” et “repères déjà connus”, pour ne pas transformer la recherche d’une personne en révélation automatique.')

page('Combat','Lire le prochain choix',
 'Conserver le vocabulaire de PA et d’hexagones des combats actuels. Les aides décrivent les règles réelles de cette version ; elles ne lui attribuent pas une initiative individuelle qui n’existe pas encore.',[
 ('Phases','Aujourd’hui : joueur, puis phase des opposants ; le soutien de Nilo est automatique. Refonte visuelle initiale : bandeau “Votre tour” ou “Opposants”. La future phase compagnon n’apparaît que lorsque son IA complète est intégrée.'),
 ('Centre tactique','Prévisualisation du chemin, PA de déplacement, PA d’action et reste. Cases hors budget différenciées par motif et texte. Une prévisualisation ne dépense rien. Le clic final ou la validation manette engage seulement une action encore légale.'),
 ('Fin de tour','Bouton stable, nettement distingué d’Attaquer. Si une action encore utile reste possible, proposer un rappel discret paramétrable. Aucune boîte obligatoire à chaque tour. Le comportement de garde ou de réaction est expliqué dans son propre bouton.'),
 ('Cible et responsabilités','Nom connu, statut hostile ou en poste, portée, chance et principaux états. Tirer sur un groupe neutre affiche un avertissement d’hostilité avant l’engagement, comme l’intention déjà prévue à la lisière de Buenos Aires.'),
 ('Opposants','Pendant leur phase, afficher qui agit et un accès à la vitesse des animations. Ne pas faire sauter la caméra entre chaque action si le joueur a désactivé ce suivi. Le journal conserve les résultats et une commande permet de revoir le dernier déplacement observé.')],mock='combat')

page('Combat','Prévisualisation et explications',table=(['Exemple','Affichage proposé','Condition de validation'],[
 ['8 PA disponibles ; marche 3 ; tir 4','“Déplacement 3 PA + tir 4 PA = 7 ; reste 1”. Tracé distinguant marche et poste de tir.','Pas de chemin, cible disparue ou PA changés : rafraîchir et expliquer avant engagement.'],
 ['Même marche ; tir visé à la tête 5','“Total 8 PA ; reste 0”. Chance liée à cette localisation.','La visée n’a pas la même chance qu’un tir au torse ; la différence reste visible.'],
 ['Cible derrière un obstacle','“Ligne de tir bloquée”. Montrer le premier obstacle connu dans la vue tactique.','Aucune dépense de cartouche ou PA si le moteur refuse le tir.'],
 ['Couvert ou fumée','État nommé, chance finale et détail épinglable des modificateurs.','L’aide reprend le calcul du moteur, pas une soustraction approximative créée par l’interface.'],
 ['Grenade près d’un allié','Zone d’effet visible ; cibles connues exposées ; message d’alerte.','Confirmation spécifique si un allié est dans l’effet connu. Aucune révélation d’ennemi caché.'],
 ['Action inaccessible','Libellé et raison : “3 PA requis, 2 disponibles”, “Aucune trousse”, “Arme à distance requise”.','La raison est consultable même si le contrôle est indisponible.']
 ]),blocks=[('Résultat incertain','Afficher une plage de dégâts comme estimation, les PV et états comme observations accessibles, et les critiques comme une possibilité. Ne pas promettre une élimination quand le tir peut manquer.'),('Précision du vocabulaire','Le stock actuel de cartouches est consommé directement. Ne pas afficher un faux chargeur avec bouton Recharger tant qu’un système de chargeurs n’a pas été conçu et intégré.')])

page('Interaction','Choisir une action sans deviner',table=(['Situation','Commande par défaut','Action secondaire et information'],[
 ['Personne visible','Parler ; approche automatique prévisualisée hors danger.','Examiner, compagnie si disponible ; menace dans une rubrique distincte et explicite.'],
 ['Porte','Entrer si le seuil et le droit sont valides.','Si fermée : raison connue et alternatives réelles, par exemple attendre, présenter un document ou crocheter.'],
 ['Objet manipulable','Examiner avant l’action engageante si le contexte l’exige.','Fouiller, utiliser, réparer ; coût matériel et temps annoncés avant validation.'],
 ['Plusieurs objets superposés','Liste courte sous le pointeur ou touche de cycle.','Même liste au clavier et à la manette ; nom, verbe et repère spatial, pas une suite d’icônes identiques.'],
 ['Personne connue hors champ','Repère de dernière localisation connue dans le carnet.','Cadrer un repère connu ne déplace pas le héros et ne garantit pas que la personne soit encore là.'],
 ['Chemin impossible','Aucun déplacement puis message lié au seuil ou à l’obstacle.','Ne pas téléporter le joueur pour ouvrir malgré tout un dialogue.']
 ]),blocks=[('Distance et temps','Afficher “À 6 hexagones” ou le coût avant une approche en combat. Une interaction qui demanderait un déplacement dangereux reste un choix explicite. La porte utilise le même point d’approche que le décor et la navigation.'),('Entrées et décor','Les bâtiments visitables possèdent une signalétique cohérente et un point d’accès sur leur façade réelle. Les volumes non visitables peuvent être inspectés ; ils ne montrent pas une poignée interactive trompeuse.')])

page('Dialogue','Lire une personne et choisir',
 'La fenêtre de dialogue donne la priorité au texte et à la voix du personnage. Les conditions mécaniques restent dans des étiquettes de l’interface ; elles n’apparaissent pas dans sa réplique comme un commentaire de développement.',[
 ('Disposition','Portrait sur un côté, nom et fonction connus, texte sur largeur maîtrisée. Réponses en dessous, avec au moins trois choix lisibles dans une vue normale. Sur petit format, portrait réduit et hauteur du texte prioritaire.'),
 ('Lecture','Texte affiché immédiatement par défaut. Défilement progressif facultatif, vitesse réglable et validation affichant d’abord la phrase complète, sans choisir la réponse suivante. Historique de l’échange consultable sans avancer la scène.'),
 ('Conditions','Exemple : “Éloquence 42 / 50” et “Il manque 8 points”. Dans le jeu actuel, ces exigences sont des seuils, pas des jets cachés. La refonte ne doit pas leur inventer un pourcentage de réussite. Une condition inconnue ne dévoile pas une quête secrète.'),
 ('Choix longs','Retours à la ligne naturels, hauteur variable ; ordre stable. Aucune réponse nouvelle n’apparaît sous le pointeur en remplaçant celle qui vient d’être choisie. La sélection doit être relâchée puis réarmée après un changement de page.'),
 ('Ton','Les personnages gardent leur vocabulaire et leurs limites de connaissance. La satire vient de ce qui arrive et de la manière de répondre. Les infobulles expliquent “Pourquoi cette option est verrouillée ?”, sans décrire la personnalité de l’interlocuteur à sa place.')],mock='dialogue')

page('Inventaire','Trouver comparer et agir',table=(['Fonction','Proposition','Limite de compréhension'],[
 ['Organisation','Onglets catégories, recherche, tri par nom/type/valeur/poids, favoris. Vue liste par défaut ; grille compacte facultative.','Les objets de quête restent identifiés et protégés des actions de vente/démontage non prévues.'],
 ['Détail','Image, fonction, portée, coût, dégâts ou effet, quantité et poids. Comparaison avec l’équipement actuel épinglable.','Indiquer “estimation” pour un résultat dépendant d’un ennemi ; ne pas comparer une lame à une armure.'],
 ['Actions','Équiper, utiliser, fractionner si le système le permet, affecter à un favori, transférer au compagnon.','Coût en PA affiché en combat. Les transferts futurs ne sont pas des actions gratuites cachées.'],
 ['Charge','Poids actuel visible ; capacité et pénalité seulement lorsqu’elles sont réellement intégrées.','Aujourd’hui le poids est calculé à l’écran, mais ne justifie pas l’affichage d’un plafond d’encombrement inventé.'],
 ['Quantités','Sélecteur, valeur restante et récapitulatif ; touches rapides 1, moitié, maximum autorisé.','“Maximum” respecte les réserves, crédits et restrictions du destinataire.'],
 ['Saisie','Sélection puis bouton ; double-clic configurable pour équiper/utiliser seulement si l’action est sûre.','Le glisser-déposer est un raccourci, jamais l’unique méthode.']
 ]),note='Le panneau compagnon et la répartition des charges dépendent du système de compagnie proposé. Ils restent absents ou clairement marqués non disponibles dans un prototype qui conserve le soutien rudimentaire actuel.',mock='inventory')

page('Commerce et ateliers','Voir la transaction entière',table=(['Écran','Informations utiles','Validation'],[
 ['Commerce','Acheter/vendre clairement séparés ; votre argent, prix final, quantité et possession. Panier optionnel avec solde avant/après.','Le prix affiché vient du même calcul que la transaction. Une variation de stock met à jour le panier avant paiement.'],
 ['Marchandage','Valeur de compétence et facteurs applicables ; dialogue de négociation si une scène le prévoit.','Aucune animation de jet factice pour un simple seuil. Le prix ne change pas secrètement entre survol et clic.'],
 ['Fabrication','Recette, résultat, composants possédés/requis, compétence, établi et temps. Filtre “Fabricable”.','Toutes les ressources et le temps sont consommés une fois. Le résultat demeure affiché après fabrication.'],
 ['Démontage','Objet de rechange, matériaux récupérés, équipement actuel protégé.','Demander confirmation pour un objet rare ou favori ; ne pas exiger trois boîtes pour une ferraille ordinaire.'],
 ['Circuit','Puzzle centré, connecteurs lisibles sans couleur seule, progression et chaleur.','Rotation au clic ou au focus. Blocage : durée restante et option de retour ; résolution persistante.'],
 ['Services','Soin, repos ou chirurgie avec coût, durée et résultat attendu.','Implant : rappeler conséquence sur origine et Aura avant engagement ; pas d’aperçu présenté comme appliqué.']
 ]),note='Les stocks mobiles, les délais de livraison et les marchandises réservées des caravanes appartiennent à la prochaine conception gameplay. L’interface ne doit pas annoncer une économie simulée avant sa réalisation.')

page('Personnage','Construire un choix compréhensible',
 'La création et la progression doivent expliquer l’effet d’un choix avant de demander de l’assumer. L’identité visuelle, l’histoire et les chiffres restent organisés en étapes courtes.',table=(['Étape','Contenu','Aide proposée'],[
 ['Origine','Humain, augmenté, mutant, cyborg déclassé ; portrait et silhouette.','Résumé des forces, contraintes sociales et compatibilité avec l’Aura. Ce sont des informations de départ, pas des révélations du récit.'],
 ['Apparence','Portrait, silhouette, couleurs et options réellement disponibles.','Aperçu avec rotation ou poses seulement si ces ressources existent. Un changement visuel ne modifie pas l’origine.'],
 ['Passé et particularité','5 passés actuels, 4 particularités ou aucune.','Chaque avantage affiche sa contrepartie ; comparaison avant/après sans perdre les choix déjà saisis.'],
 ['Attributs','7 attributs, total 40 ; profils préétablis modifiables.','“Ce que cela améliore” avec deux exemples de gameplay. Compteur restant visible, bouton réinitialiser local.'],
 ['Spécialités','3 compétences parmi les 10 actuelles.','Filtrage par usage : combat, technique, social, survie. Les catégories n’ajoutent pas de compétences nouvelles.'],
 ['Résumé','Origine, contraintes, équipement initial et difficulté.','Retour à une étape sans effacer les suivantes ; confirmation finale seulement si les contraintes sont valides.']
 ]),blocks=[('Progression','Signaler les points disponibles dans la fiche, sans ouvrir un écran forcé après chaque gain. Aptitudes : prérequis, effet et aperçu ; la dépense de points de compétence se confirme en lot pour permettre de comparer.')])

page('Cartes','Trois échelles un même langage',table=(['Échelle','Informations visibles','Action principale'],[
 ['Région','Cases terrestres, lieux connus, position, route, durée, eau et exposition estimée.','Tracer puis confirmer. Montrer une plage ou une incertitude si un incident peut changer le trajet.'],
 ['Ville','Quartiers, niveaux, accès publics et connus, services, navettes et passages découverts.','Choisir un quartier ; indiquer coût, durée et accès pour le joueur et le compagnon.'],
 ['Local','Volumes, chemins, portes découvertes, objectifs connus et dernière position observée.','Placer un repère ou cadrer le terrain. Ne pas marcher ou entrer sans validation distincte.'],
 ['Caravane future','Position observée, dernière nouvelle, destination connue et heure d’information.','Consulter le contrat, rejoindre une étape accessible ; aucune position exacte d’un convoi jamais rencontré.'],
 ['Conflit futur','Blocage connu, danger et voie de retrait rapportée.','Lire la source et sa date. Un cessez-le-feu local ne recolore pas toute une faction en alliée.']
 ]),blocks=[('Couches','Cases et route prioritaires ; services, quêtes, personnes et ressources en couches indépendantes. Légende accessible en un geste. Un symbole change de forme et de libellé autant que de couleur.'),('Information cachée','L’éditeur développeur peut révéler toute la carte dans une partie de test. Cette fonction reste distincte des options de confort du joueur. Agrandir une police ne révèle jamais un passage clandestin.')],mock='map')

page('Journal','Savoir ce que l’on sait',table=(['Rubrique','Contenu','Principe'],[
 ['Quêtes','Objectif actuel, dernier fait reçu, interlocuteurs et pistes déjà connues.','Ne pas convertir une rumeur en objectif certain ni dévoiler une solution alternative non découverte.'],
 ['Personnes','Nom connu, fonction, dernier lieu et heure, services, engagement de compagnie éventuel.','La dernière localisation n’est pas un suivi GPS. Un visage inconnu n’a pas automatiquement son vrai nom.'],
 ['Monde','Documents lus, cartes découvertes, factions rencontrées et termes expliqués.','Distinguer observation, propos rapporté et document. Les secrets ne figurent pas d’emblée dans une encyclopédie totale.'],
 ['Événements','Conversations et résultats d’action, filtres combat/voyage/social/système.','Défilement stable pendant la lecture ; notification “3 nouvelles entrées” sans ramener de force en bas.'],
 ['Recherche','Nom, lieu, objet ou mot du document connu ; résultats regroupés.','La recherche ne révèle pas les entrées verrouillées. Aucun résultat : formulation utile et proposition de changer le filtre.']
 ]),blocks=[('Suivi','Un objectif principal affiché ; possibilité d’épingler deux pistes secondaires dans le journal sans tripler le HUD. Bouton “Retrouver la source” vers la dernière conversation ou pièce effectivement consultée.'),('Échec','Un protagoniste mort peut interrompre une piste ; l’état et la cause sont annoncés sans solution inventée. Les informations déjà acquises restent lisibles. Le mode développeur peut inspecter la dépendance, mais ce détail n’apparaît pas dans le texte du monde.')])

page('Compagnons et régions','Des systèmes futurs lisibles',table=(['Système proposé','Vue compacte','Vue détaillée'],[
 ['Compagnon','Portrait, santé, état et ordre en cours. Signal de retard ou refus d’accès près du portrait.','Suivre, attendre, se regrouper, posture, matériel, blessures et rendez-vous. Une raison accompagne un refus d’ordre.'],
 ['Confiance','Indices dans la réaction et évolution nommée après un acte important.','Résumé des désaccords connus ; pas de jauge d’affection simulée en permanence sur la tête d’un PNJ.'],
 ['Caravane','Prochain départ ou contrat actif si suivi. Alerte de retard seulement si reçue.','Manifeste connu, réserves vendables distinctes des réserves de route, étapes et conséquences du contrat.'],
 ['Conflit','Passage bloqué et niveau d’alerte connu sur la carte.','Acteurs rencontrés, objectif local, preuves transmises, propositions et horaire annoncé.'],
 ['Horaire PNJ','“En service”, “Revient vers 18 h” ou dernière information reçue.','Lieu de travail et rendez-vous publics connus ; pas de routine secrète complète au premier clic.']
 ]),blocks=[('Nilo dans la version actuelle','Afficher son statut de compagnon et l’aide réelle dont il dispose. Tant que l’IA complète n’existe pas, ne pas dessiner une fausse réserve de cartouches, une barre de santé indépendante ou des ordres sans effet.'),('Préparation au futur','Chaque module connaît son statut de disponibilité. Dans une maquette de développement, une étiquette “simulation UI” est visible. Dans la version joueur, un module incomplet n’apparaît pas comme une fonction prête.')])

page('Alertes et sauvegardes','Informer sans interrompre tout',table=(['Catégorie','Réponse proposée','Durée ou persistance'],[
 ['Événement mineur','Bref message au bord ; événements identiques regroupés.','3,5 secondes proposées ; historique conservé. Pause de disparition pendant focus ou lecture.'],
 ['Ressource critique','État près de la jauge et message d’action possible.','Persiste jusqu’à changement ou acquittement ; ne masque pas le combat avec une boîte répétée.'],
 ['Erreur de commande','Raison au même endroit que l’action ; aucune animation de réussite.','Lisible sans délai court ; regroupement des répétitions.'],
 ['Sauvegarde','Indicateur discret “Sauvegarde…” puis “Enregistré”. Échec clairement distinct.','Ne pas afficher la réussite avant fin réelle ; proposer export si le stockage local échoue.'],
 ['Reprise','Emplacement, jour, niveau et statut de la sauvegarde ; tests séparés des parties normales.','Écrasement du travail courant : résumé et point de retour proposé.'],
 ['Import','Valider format et compatibilité ; aperçu avant application.','Fichier incorrect : la partie en cours reste intacte. Les préférences UI ne se remplacent pas sans choix explicite.']
 ]),blocks=[('Menu de pause','Reprendre, sauvegarder, charger, options, commandes, aide et retour titre. Les réglages sont accessibles avant de commencer une partie. Une dernière partie valide est mise en avant, sans recouvrir l’écran d’accueil de statistiques.'),('Classement','Saves de jeu, copies de test et points de restauration possèdent des catégories distinctes. Un point dev peut être exporté avec son manifeste de test ; le joueur ne le confond pas avec sa dernière progression normale.')])

page('Personnalisation','Des profils qui changent vraiment la lecture',table=(['Profil','Disposition proposée','Destinataire et limites'],[
 ['Équilibré','Santé, arme, barre de favoris, objectif compact, minicarte ; états secondaires contextuels.','Point de départ proposé. Maintient les verbes d’action et le coût lorsqu’ils sont utiles.'],
 ['Discret','Barre réduite au repos ; objectif et minicarte à la demande ; états critiques toujours accessibles.','Exploration et immersion. Un simple retour au profil équilibré est disponible sans repasser tous les réglages.'],
 ['Tactique','PA et modificateurs plus détaillés, grille contextuelle, journal combat compact et compagnon étendu.','Préparation des combats ; aucune information cachée révélée par le profil.'],
 ['Lecture','Texte plus grand, surfaces opaques, moins d’animations et priorité aux libellés.','Petit écran ou besoin de lecture confortable ; ne remplace pas tous les choix d’accessibilité par un seul bouton.']
 ]),blocks=[('Réglages indépendants','Le profil sert de point de départ. Taille du texte, contraste, vitesse d’animation, position des modules et raccourcis peuvent ensuite être modifiés séparément. Appliquer un profil annonce les groupes qu’il va changer et conserve les réglages d’accès déjà choisis.'),('Prévisualisation','L’éditeur M08 montre le terrain, un dialogue et un cas de combat de démonstration. Aucun déplacement, soin, tir ou effet de quête n’est exécuté depuis cet aperçu. Les repères de manipulation disparaissent en quittant l’éditeur.'),('Profils par format','Mémoriser séparément bureau, portable/manette et tactile. Changer de périphérique n’écrase pas le profil du précédent. Exporter un profil UI ne transporte pas la sauvegarde ni les triches.')],mock='settings')

page('Personnalisation','Catalogue des options',table=(['Groupe','Réglages proposés','Valeurs de départ à essayer'],[
 ['Texte','Taille HUD, dialogue et journal indépendantes ; interligne ; vitesse d’apparition ; fond.','Corps UI 18 px logiques ; dialogue 22 ; journal 20. Échelle texte de 100 à 200 % ; débordement traité par repli, pas par réduction forcée.'],
 ['HUD','Échelle, emplacement, minicarte, objectif, états secondaires, libellés, historique compact.','Échelle de 85 à 150 % ; modules ancrés ; états critiques non perdus par un masquage contextuel.'],
 ['Couleurs','Accent, palettes de distinction, contraste renforcé, fonds opaques, contours d’éléments.','Accent teal pâle ; états toujours doublés par un symbole et du texte. Avertir d’un contraste insuffisant dans l’éditeur.'],
 ['Animations','Mouvement réduit, durée des transitions, suivi caméra, secousse, fond animé, gain de jauge.','Transitions normales 120–220 ms ; aucune secousse obligatoire. Réduction initiale selon préférence système, avec choix explicite conservé.'],
 ['Son','Ambiance, musique, effets, UI séparés ; bip de focus facultatif.','Son UI discret et désactivable ; aucune information importante transmise uniquement par le son.'],
 ['Commandes','Remappage, sensibilité, maintien/bascule, validation tactile, double-clic, navigation au focus.','Commande secondaire disponible pour toute manipulation de glisser-déposer. Conflits de raccourcis signalés.'],
 ['Aide','Infobulles, délais, détails mécaniques, rappels, historique des tutoriels.','Délai d’aide 300 ms au survol, ouverture directe au bouton d’inspection ; rappels désactivables après apprentissage.'],
 ['Performance','Qualité des ombres UI, arrière-plan animé, résolution du rendu terrain distincte du texte.','Le texte conserve la résolution de l’interface. La fluidité n’exige pas une police floue ou des effets permanents.']
 ]),note='Ces nombres sont des objectifs de conception, pas des réglages déjà mesurés sur la version actuelle. Tester également le zoom navigateur et les densités de pixels différentes.')

page('Personnalisation','Déplacer sans casser le HUD',
 'L’éditeur doit permettre de composer son interface tout en préservant les accès essentiels. Un HUD complètement libre, sans contraintes de taille ou d’empilement, deviendrait vite difficile à réparer.',[
 ('Ancrages','Quatre bords et quelques emplacements définis : portraits, barre d’actions, carte, objectif et historique. Aimantation sur un pas de 8 px logiques ; marges de sécurité propres à chaque écran. Le centre conserve une surface libre minimale.'),
 ('Manipulation','Sélection du module, poignées claires, aperçu de destination. Au clavier ou à la manette : choisir le module puis l’emplacement, sans exiger de pointeur précis. Une commande remet le module sélectionné à sa position par défaut.'),
 ('Collisions','Avant application, détecter chevauchement, sortie de zone sûre et contrôle masqué. Proposer le prochain ancrage disponible. Sur petit écran, replier les modules secondaires selon l’ordre choisi, avec indication des éléments déplacés.'),
 ('Vérification','Prévisualisations Exploration, Combat et Dialogue. Tester le nom d’arme le plus long, une valeur à quatre chiffres et un message critique. Un réglage valide dans un état ne suffit pas s’il recouvre Fin du tour dans un autre.'),
 ('Retour','Annuler revient au profil d’entrée de l’éditeur ; Appliquer enregistre une copie de la configuration validée. Réinitialiser ce profil ne supprime ni les raccourcis personnels ni les sauvegardes. Un profil importé incompatible est adapté avec compte rendu.'),
 ('Animations de manipulation','Le module déplacé suit immédiatement le pointeur ; les voisins prennent leur place en 140 ms, sans rebond. En mouvement réduit, le cadre de destination change simplement d’état. Une animation ne déplace jamais un bouton au moment de sa validation.')])

page('Accessibilité','Lire et naviguer sans surcharge',
 'Les recommandations de texte et de mouvement [R6–R7] sont utilisées comme références. Les valeurs suivantes sont des cibles propres au projet, à mesurer ; elles ne constituent pas une certification.',table=(['Besoin','Règle proposée','Vérification'],[
 ['Contraste','Cible de 4,5:1 pour le texte courant et 3:1 pour les grands éléments ou repères graphiques essentiels.','Mesurer sur fond effectif, avec transparence et scène claire/sombre. Le mode opaque doit rester disponible.'],
 ['Lecture','Police agrandissable à 200 %, interligne confortable, texte sélectionnable dans les longs documents si possible.','Aucun bouton couvert par un paragraphe ; noms complets consultables sans dépendre du survol.'],
 ['Couleurs','Danger, allié, état neutre et chemin différenciés par forme, contour et libellé.','Tester en niveaux de gris et avec plusieurs simulations de perception des couleurs.'],
 ['Focus','Contour visible, ordre logique, retour au contrôle d’origine et absence de piège de clavier.','Toute fonction essentielle utilisable sans souris ; les options verrouillées restent inspectables.'],
 ['Terrain Canvas','Liste sémantique des actions et éléments actuellement perceptibles ; description des prévisions tactiques.','Une alternative DOM donne les mêmes informations connues que la scène. La refonte ne peut pas promettre un lecteur d’écran complet sans essais réels.'],
 ['Effort moteur','Cibles de 44 × 44 px logiques au minimum proposées pour les commandes tactiles ; commandes persistantes sans maintien prolongé obligatoire.','Tester les commandes proches du bord, le double contact et les tremblements de pointeur.'],
 ['Mouvement','Retirer translations, zoom UI, fonds animés et secousses sur demande ; aucune information n’en dépend.','Tous les états restent lisibles avec des transitions instantanées ou un fondu bref.']
 ]),note='Un contrôle indisponible peut recevoir le focus avec une raison visible, tout en refusant l’exécution. Il ne faut pas le rendre introuvable en le retirant de tous les parcours.')

page('Commandes','Souris clavier manette et tactile',table=(['Action','Souris et clavier','Manette ou tactile'],[
 ['Sélection','Clic ou navigation de liste ; Entrée valide ; Échap remonte un niveau.','A valide, B revient ; tactile : premier contact sélectionne si le risque exige une prévisualisation.'],
 ['Caméra','Glisser hors contrôle, commandes de déplacement caméra et zoom.','Stick caméra ; gestes pincement/glissement seulement sur terrain libre. Bouton de recentrage accessible.'],
 ['Actions','Raccourcis 1–8 remappables et entrée Toutes les actions.','Roue ou liste de catégories jusqu’à 8 actions par page ; alternative de liste pour une précision moindre.'],
 ['Inspecter','Survol puis épingler ; F1 ou touche configurée pour l’aide au focus.','Commande Inspecter explicite ; tactile : bouton d’information, sans dépendre d’un appui long.'],
 ['Gestion','Onglets, recherche, listes et raccourcis visibles au focus.','LB/RB entre catégories ; stick ou croix dans le groupe courant ; retour de focus mémorisé.'],
 ['Texte','Raccourcis de gameplay neutralisés pendant la saisie.','Clavier virtuel à la demande ; fermer le clavier ne ferme pas tout l’écran.'],
 ['Fin du tour','Touche existante Espace conservable et remappable ; bouton séparé.','Commande dédiée clairement affichée ; validation tactile distincte du choix d’une cible.']
 ]),blocks=[('Web et raccourcis','F5 est aujourd’hui intercepté pour la sauvegarde. Prévoir un réglage de compatibilité navigateur et un accès par bouton ; ne pas monopoliser les raccourcis du navigateur ou du système. Toute combinaison dev possède aussi une entrée de menu.'),('Périphériques mixtes','Changer les icônes après une entrée intentionnelle ; dérive d’un stick ignorée. Temporisation indicative de 300 ms pour éviter le clignotement des invites. Un mouvement de souris ne vole pas le focus d’une saisie manette en cours.')])

page('Formats','Réorganiser plutôt que tout rétrécir',table=(['Format logique de test','Disposition proposée','Point de contrôle'],[
 ['1920 × 1080 et au-delà','Barre complète, panneaux en deux ou trois colonnes, carte avec résumé latéral.','Espaces centraux libres ; les listes ne deviennent pas des lignes interminables.'],
 ['1280 × 800 portable','6 actions directes et catégories ; portraits compacts ; gestion en deux colonnes ou onglets.','Texte et cibles gardent leur taille. Ce format est un scénario de test, pas une déclaration de résolution native d’un appareil.'],
 ['1024 × 768','Carte et détail alternent ; inventaire : liste et panneau à largeur contrôlée.','Pas de trois colonnes compressées jusqu’à rendre le texte minuscule.'],
 ['844 × 390 tactile paysage','Barre basse compacte, panneaux pleine hauteur, dialogue prioritaire et portrait réduit.','Respecter zones système et encoche ; grand clavier virtuel et messages longs testés.'],
 ['390 × 844 tactile portrait','Menus en une colonne ; terrain conservé avec commandes essentielles et accès à un écran tactique dédié.','Fonctions accessibles par listes ; expliquer si le paysage est recommandé pour le confort, sans bloquer l’usage.'],
 ['Ultralarge','Ancrages dans une zone centrale configurable, non aux coins très éloignés par défaut.','Ne pas demander de parcourir tout l’écran entre santé, cible et Fin du tour.']
 ]),blocks=[('État conservé','Un changement d’orientation ou de taille garde cible, onglet, texte en cours et position de lecture. La fenêtre se réorganise ; elle ne relance pas le dialogue ni le voyage.'),('Limite d’espace','Priorité au repli : masquer une illustration décorative, transformer une colonne en onglet, déplacer un groupe dans un tiroir. Ne jamais supprimer une action essentielle ou réduire une police sous le seuil choisi pour faire tenir le décor.')])

page('Animations','Un langage de mouvement utile',
 'Les images fixent les états de repos et de sélection. Les animations décrites ici relient ces états : elles donnent une réponse au geste, montrent une continuité et rendent les changements compréhensibles.',[
 ('Réponse immédiate','Survol et focus se voient en moins de 100 ms ; l’activation change l’état dès sa réception. La durée du mouvement ne retarde pas la prise en compte d’une commande. Les calculs et écritures attendent leur résultat avant d’annoncer une réussite.'),
 ('Mouvement mesuré','Transitions courtes à ralentissement final, sans rebond sur la lecture. Un panneau peut avancer de 8 à 16 px et apparaître ; aucun grand trajet à travers le terrain. Limiter les animations simultanées à la tâche en cours.'),
 ('Continuité','Une carte ouverte conserve le repère sélectionné ; une fiche se déploie depuis son ancrage. Les jauges montrent brièvement l’ancienne valeur puis rejoignent la nouvelle. Le nombre exact est à jour dès le changement du moteur.'),
 ('Interruptibilité','Échap ou Retour interrompt l’ouverture et ferme proprement. Un nouvel onglet remplace la transition précédente. Une entrée de scène invalide l’animation attachée à l’ancienne scène ; pas de notification qui réapparaît dans un autre dialogue.'),
 ('Lecture et ambiance','Fond animé, poussière ou oscillation de lumière facultatifs et limités hors des zones de lecture. En dialogue ou journal, l’ambiance visuelle peut se figer. Les réglages de mouvement ne modifient pas le coût des actions ni le temps simulé.'),
 ('Mode réduit','Remplacer les déplacements par un changement d’état ou un fondu de 60–80 ms. Aucune secousse, translation de texte, pulsation infinie ou scintillement. Les informations et réponses aux gestes restent les mêmes.')])

page('Animations','Catalogue des transitions',table=(['Élément','Durée normale proposée','Comportement et mode réduit'],[
 ['Survol et focus','60–90 ms','Accent et contour ; pas de saut de taille. Mode réduit : état immédiat.'],
 ['Bouton pressé','60 ms','Contraste et enfoncement de 1 px maximum ; validation au relâchement. Réduit : contraste seul.'],
 ['Panneau bref','160–180 ms ouvrir ; 100–120 fermer','Fondu et translation 12 px. Fermeture interruptible ; réduit : fondu bref ou instantané.'],
 ['Tiroir de gestion','200–220 ms','Déplacement maximal 16 px ; le contenu est prêt avant apparition. Réduit : fondu 80 ms.'],
 ['Changement d’onglet','120–140 ms','Surlignage puis contenu ; pas de balayage d’écran. Réduit : changement direct.'],
 ['Infobulle','Délai 300 ms puis 100 ms','Épinglable ; annuler le délai quand la cible disparaît. Réduit : même délai, sans mouvement.'],
 ['Compteur et jauge','160–220 ms','Chiffre réel immédiat ; traîne discrète facultative. Réduit : valeur finale seule.'],
 ['Objectif mis à jour','180 ms','Deux lignes maximum puis historique. Aucun bandeau central masquant le terrain.'],
 ['Début ou fin de phase','180–220 ms','Libellé stable, indication de l’acteur. Réduit : changement direct avec symbole.'],
 ['Retour de fabrication','140 ms','Résultat et quantités ; pas d’attente de spectacle. Une recette ne peut pas être payée deux fois par le même geste.'],
 ['Réorganisation du HUD','140 ms voisins ; déplacement direct du module','Grille de destination sans oscillation. Réduit : déplacement direct et cadres statiques.'],
 ['Trajet sur carte','Marqueur par étape, vitesse réglable','Interpolation visuelle distincte du temps de jeu ; pause explicite. Réduit : passage de repère en repère.']
 ]),note='Courbes proposées : ouverture cubic-bezier(0.16,1,0.3,1), fermeture ease-in courte, changement de valeur ease-out. Mesurer les budgets avant d’introduire flous ou ombres animées coûteuses.')

page('Animations','Chronologie de trois gestes',table=(['Geste','Séquence proposée','Contrôles utiles'],[
 ['Sélectionner un tir','0 ms : sélection ; 60 ms : contour ; calcul du moteur ; résultat + coût ; validation ; application ; animation du résultat.','Sélectionner ne tire pas. Une réponse de calcul devenue périmée est ignorée si la cible a changé. Retour annule la visée.'],
 ['Ouvrir un inventaire','0 ms : commande acceptée ; pause des minuteurs concernés ; contenu préparé ; fondu 180 ms ; focus sur dernier objet valide.','Les entrées répétées pendant l’ouverture ne créent pas trois fenêtres. Fermer rend le focus au terrain sans consommer un objet.'],
 ['Changer un réglage','Valeur modifiée ; aperçu immédiat ; annonce du résultat ; appliquer ou annuler ; configuration validée sauvegardée.','Changer l’échelle ne déplace pas le curseur sur une commande dangereuse. Annuler restaure uniquement le groupe de réglages en cours.'],
 ['Charger un scénario dev','Créer le point de retour ; préparer la copie ; valider les dépendances ; afficher le bilan ; lancer le terrain ou la séquence.','Une erreur laisse la copie précédente intacte. La barre d’attente annonce un travail réel, sans durée de chargement artificielle.']
 ]),blocks=[('Temps de jeu','L’interface ne fait pas avancer les horaires, la fatigue, les caravanes ou les délais pendant la lecture. Un achat, une réparation ou une transition applique uniquement son coût temporel prévu. Fermer la carte suspend le voyage comme aujourd’hui.'),('Son et mouvement','Clic, ouverture et confirmation possèdent trois sons discrets et distincts. Les sons peuvent être réduits ou coupés. La confirmation d’une action ne repose pas sur une animation ou un son isolé.')])

page('Fluidité','Budgets et architecture de l’interface',
 'Les objectifs ci-dessous sont à instrumenter sur les formats de test. Aucune mesure de fluidité de la future refonte n’est revendiquée ici.',[
 ('Rendu sélectif','Mettre à jour les composants dont les données changent, conserver les lignes et le focus au lieu de reconstruire tout l’écran. La fonction actuelle update recrée plusieurs listes et compteurs ; elle constitue un point d’audit avant extension.'),
 ('Texte net','Terrain et interface peuvent avoir des échelles de rendu différentes. Réduire le coût d’un fond de scène ne doit pas flouter le texte ou agrandir un sprite UI pixellisé. Charger les portraits utiles et prévoir un état de remplacement de même taille.'),
 ('Objectifs de réponse','Cible : retour visuel d’une commande simple en moins de 100 ms ; ouverture prête en moins de 250 ms sur appareil de référence. Animation UI à 60 images/s quand le matériel le permet, soit environ 16,7 ms par image ; ces chiffres restent des budgets, pas une garantie.'),
 ('Calculs lourds','Prévisualisation de chemin et filtres volumineux peuvent être différés ou calculés séparément. Chaque demande porte l’identifiant de scène, la cible et une révision d’état ; un résultat obsolète ne remplace pas l’affichage courant.'),
 ('Réduction de coût','Prioriser composition et opacité sur de petits panneaux. Éviter les flous plein écran, ombres géantes recalculées et effets de verre empilés. Réutiliser les fonds et les icônes ; virtualiser une longue liste sans perdre son ordre de navigation.'),
 ('Trace de diagnostic','Mesurer durée de préparation, temps de rendu, variations de mémoire et nombre de mises à jour. Le panneau de diagnostic appartient au mode test ; il ne remplit pas le HUD de chiffres techniques en partie normale.')])

page('Mode développeur','Accéder aux contenus dès le départ',
 'Le mode développeur doit permettre de rejoindre toutes les séquences cataloguées, leurs conditions et leurs variantes sans terminer le jeu. Cela comprend les fins, retours de quête, dialogues, rencontres, refus, échecs et situations de combat.',[
 ('Entrée','Depuis l’écran titre et Options → Outils → Atelier développeur. Une commande clavier remappable peut le rouvrir ; aucune combinaison secrète indispensable. Sur manette ou tactile, le même accès de menu existe. Il peut créer une session de test sans sauvegarde de départ.'),
 ('Session','Ouvrir une copie du dernier état ou un scénario de référence. Un badge MODE TEST persiste sur tous les écrans, exports et sauvegardes de cette session. La partie d’origine reste dans son propre espace d’enregistrement.'),
 ('Deux niveaux de test','Préparer un état cohérent est l’usage principal : les prérequis, ressources et acteurs nécessaires sont réunis. Tester un état invalide est une opération distincte : un écart volontaire est visible, consigné et réversible, pour vérifier une erreur ou une récupération.'),
 ('Accès complet','Aucune quête à finir, argent à gagner ou réputation à monter avant d’ouvrir un inspecteur. Le catalogue affiche les contenus verrouillés et explique leurs conditions. Pour une fonction seulement prévue, il montre “Non implémentée” et un lien de spécification, sans lancer un faux contenu.'),
 ('Portée technique','Dans le jeu statique actuel, ce mode serait un outil local de développement et de triche. Un mot de passe JavaScript ou un paramètre d’URL ne constituerait pas une protection de serveur. L’atelier ne donne aucun droit de publication ni accès à un service distant.'),
 ('Sortie','Fermer l’atelier revient à la scène testée. Quitter le mode test propose de conserver cette copie ou de reprendre la partie d’origine. Ni une autosauvegarde ni le retour au titre ne doivent écraser silencieusement la campagne normale.')],mock='dev-library')

page('Mode développeur','Le catalogue de scénarios',table=(['Zone de M09','Contenu','Action'],[
 ['Recherche et filtres','Lieu, quête, personnage, stade, origine, difficulté, système et disponibilité.','Rechercher par nom lisible ou identifiant ; favoris de test personnels.'],
 ['Fiche de scénario','Objectif du test, aperçu, scène d’arrivée, état de préparation et résultat attendu.','Lire les changements puis lancer une copie prête à jouer.'],
 ['Dépendances','Acteurs vivants, documents consultés, inventaire, accès, ennemis et phase de combat.','Chaque contrôle donne sa source et son éventuelle correction. Pas de simple coche décorative.'],
 ['Variantes','Avant/après décision ; plusieurs origines ; seuil juste atteint ou manquant ; version pacifique ou armée.','Changer une variante affiche la différence, sans appliquer avant validation du lancement.'],
 ['Point de retour','État avant préparation et historique des opérations.','Restaurer au dernier point connu ; ne dépend pas d’une quête de sauvegarde dans le récit.'],
 ['Scénario personnalisé','Créer à partir de la copie actuelle avec nom, description et paramètres.','Exporter une recette de préparation versionnée plutôt qu’un fichier sans contexte.']
 ]),blocks=[('Un lancement cohérent','La recette définit un état de base et les écarts nécessaires. Elle vérifie les identifiants disponibles dans cette version, prépare les données, reconstruit la scène et contrôle les accès avant de remplacer la session de travail.'),('Sens de la maquette','Dans M09, “registre récent obtenu” représente le fait d’avoir consulté/copié la preuve. Dans le moteur actuel, frontProof est un drapeau ; la préparation ne doit pas créer un objet de quête imaginaire nommé registre récent.')])

page('Mode développeur','Inspecter et préparer les quêtes',
 'M10 distingue le choix d’une issue, l’aperçu de sa séquence et son application au monde. Cela évite que lire une fin la valide accidentellement.',table=(['Outil','Comportement proposé','Limite'],[
 ['Catalogue','Les 21 quêtes actuelles, leurs noms, stades et références d’acteurs.','Liste chargée depuis les définitions de la version ; pas de faux titres ajoutés par une illustration.'],
 ['Étape','Présenter l’étape et les conditions associées ; proposer une recette Avant ou Après.','Changer uniquement un entier de progression ne suffit pas à préparer l’histoire.'],
 ['Issues exclusives','Choix radio parmi les issues d’une même affaire ; exemple main : io, free, native, break.','Une issue active à la fois. Préparer une autre variante repart d’un point de base, sans accumuler leurs récompenses.'],
 ['Aperçu','Affiche texte, interlocuteur et conditions d’une branche dans une instance de lecture isolée.','Aucun gain d’XP, objet, réputation, déplacement ou effet secondaire ; le simple rendu ne doit pas muter l’état.'],
 ['Jouer la séquence','Prépare l’état nécessaire puis ouvre l’échange en mode test.','Les choix exécutés peuvent modifier la copie ; le badge le rend explicite.'],
 ['Effets','Comparaison avant/après : inventaire, quête, drapeaux, réputation, présence et ennemis.','Écritures regroupées en une opération ; une erreur restitue tout l’état précédent.'],
 ['État invalide','Permet une incohérence ciblée pour reproduire un défaut.','Marquage et commentaire obligatoires dans le rapport de test, pas un verrou de progression dans le jeu.']
 ]),note='L’application d’une fin à partir du mode test doit passer par une recette et les mêmes transitions de domaine que le jeu lorsque c’est pertinent. Elle ne doit pas regratifier des récompenses à chaque ouverture de l’inspecteur.',mock='dev-quest')

page('Mode développeur','Toutes les séquences et variantes de dialogue',table=(['Fonction','Spécification proposée','Exemple'],[
 ['Index des nœuds','Personnage, clé de nœud, lieu, conditions, actions et références de textes.','Mara avant réparation, après allocation et après chacune des quatre issues.'],
 ['Vue des conditions','Valeur requise, valeur courante, origine de la donnée et résultat.','Éloquence 42 / 50 ; contrôle d’accès ; personnage mort ou déplacé.'],
 ['Préparer une condition','Bouton “Préparer ce cas” avec état cohérent ou dérogation de test nommée.','Passer de 49 à 50 en Éloquence pour tester la frontière exacte d’une réponse.'],
 ['Comparer','Deux panneaux Avant/Après, origine A/B ou branche A/B.','Même nœud devant un humain sans passe et un augmenté identifié.'],
 ['Historique de parcours','Nœuds et choix visités avec heure simulée et effets.','Retrouver la réponse qui a livré un module à Salma ou l’a dénoncé.'],
 ['Rejouer','Repartir d’un point précis avec inventaire et drapeaux de ce point.','Voir à nouveau l’annonce de sortie de Sami sans donner deux fois la récompense.'],
 ['Contenu absent','Afficher une référence cassée, une branche introuvable ou une scène prévue.','Entrée “Non disponible dans cette version”, sans substituer un texte générique trompeur.']
 ]),blocks=[('Couverture du contenu','Les dialogues actuels sont produits par des fonctions conditionnelles, pas tous stockés dans un graphe de nœuds autonome. Un simple scan des noms de fonctions ne garantit donc pas un catalogue complet. Prévoir un registre déclaratif des nœuds et scénarios qui référence aussi leurs effets.'),('Lecture isolée','Certaines entrées de dialogue peuvent avoir un effet de préparation. Le mode Aperçu utilise une copie jetable et interdit les écritures de persistance ; si un nœud tente de modifier le monde, le diagnostic signale l’effet au lieu de l’appliquer à la session.')])

page('Mode développeur','Monde accès et géométrie',table=(['Outil','Usage','Règle de test'],[
 ['Téléportation','Rejoindre un lieu ou une porte depuis le catalogue ; point d’arrivée choisi et validé.','Vérifier limites, occupation et case praticable. Conserver un point de retour avant transport.'],
 ['Dérogation d’accès','Passer un contrôle pour atteindre un contenu à tester.','Badge “accès forcé” ; la dérogation ne crée pas de laissez-passer canonique ni de réputation. Retrait restaure les vraies règles.'],
 ['Révéler la carte','Afficher zones, passages et éléments cachés pour contrôle.','Donnée de debug dans la copie ; distincte des lieux réellement découverts du personnage.'],
 ['Portes et passages','Afficher volume, point d’approche, seuil, destination et trajet vers la porte.','Trouver une entrée trop loin du bâtiment, notamment au bras droit du Titan, sans déplacer le décor à la volée.'],
 ['Superpositions','Hexagones, obstacles, eau, collision, volumes, ancrages de PNJ et zones d’événement.','Calques indépendants, légende, export du repère sélectionné ; le joueur peut encore voir la scène.'],
 ['Route et ville','Inspecter le chemin régional, étapes, niveaux urbains et refus d’accès.','37 terrains actuels séparés des 44 plans proposés. Un plan non intégré ne devient pas une scène de jeu par téléportation.'],
 ['Placement libre de test','Déplacer une entité dans la copie pour reproduire un cas.','Diff enregistré ; aucun changement du fichier source du plan sans un outil d’édition distinct et explicite.']
 ]),note='Le catalogue du monde utilise les identifiants existants. port est le nœud maritime IO, jamais le Port UFSA futur. Big Larry garde une couche de contrôle sans PNJ permanent ; le cœur du Titan reste hors de la visite canonique.')

page('Mode développeur','Personnage et outils de triche',table=(['Outil proposé','Effet dans la copie','Point à contrôler'],[
 ['Santé et ressources','Soigner ; restaurer les ressources présentes ; fixer radiation et fatigue à une valeur autorisée.','Une jauge de ressource non implémentée n’est pas inventée par l’outil. La valeur reste dans les limites de sauvegarde.'],
 ['Invulnérabilité','Neutraliser les dégâts ou la mort selon deux options distinctes pour tester une scène.','Indicateur persistant ; ne pas retirer silencieusement la condition normale de folie radioactive d’un mutant. Un test létal peut désactiver la protection.'],
 ['PA et munitions','Ignorer coût des PA, ajouter des munitions ou ignorer leur dépense.','Options indépendantes ; toujours visibles dans le diagnostic pour ne pas attribuer un faux problème d’équilibrage au combat normal.'],
 ['Attributs et compétences','Valeur directe, seuil requis, juste en dessous ou juste au-dessus ; niveau et aptitudes.','Recalculer les dérivés concernés ; dépassement délibéré dans un cas invalide marqué.'],
 ['Inventaire','Donner/retirer un objet connu ; quantité, équipé, favori, destination.','Les objets uniques et récompenses possèdent un historique ; pas de duplication automatique en restaurant un écran.'],
 ['Origine et Aura','Préparer un humain, augmenté, mutant ou cyborg ; scénario d’éveil compatible.','En mode cohérent, un cyborg ne reçoit pas l’Aura. Dérogation expérimentale distincte avec signalement si l’on teste précisément un refus.'],
 ['Réputation et accès','Valeurs par faction, documents connus et convictions de test.','Une réputation IO élevée ne donne pas un droit légal aux mutants à Upper-Town.'],
 ['Déblocage total','Découvrir les contenus dans le catalogue développeur et fournir les recettes d’accès.','“Tout débloquer” ouvre les outils ; il n’achève pas toutes les quêtes mutuellement exclusives à la fois.']
 ]),note='L’objectif est l’accès rapide et contrôlable aux situations, pas la reproduction cachée d’un run impossible dans la campagne normale. Aucun de ces boutons de triche n’est présent dans la v0.6.')

page('Mode développeur','PNJ compagnons et intelligence locale',table=(['Inspection','Commandes proposées','Contrôles'],[
 ['Identité et présence','Rechercher, cadrer, rejoindre, convoquer dans un emplacement de test ou restaurer au point de référence.','Une identité unique ; un résident recruté ne reste pas en double à son poste.'],
 ['État physique','Santé, blessure, contamination, mort, matériel et capacité si implémentés.','Ressusciter en test restaure aussi les dépendances sélectionnées ; ne promet pas une résurrection canonique.'],
 ['Conversation','Nœud actif, connaissances, preuves reçues et branches accessibles.','Ne pas prendre l’affiliation pour une preuve d’origine biologique ou de savoir global.'],
 ['Routine future','Activité, prochain point, porte, blocage, destination, service et motif de priorité.','Pas-à-pas de décision sans faire avancer toute la journée ; acteur et monde restent synchronisés.'],
 ['Compagnon futur','Recruter, suivre, attendre, ordre de combat, confiance, accès et rendez-vous.','Stock propre, PA, chemin et ligne de vue vérifiés. Nilo actuel est identifié comme soutien simplifié.'],
 ['Combat','Groupes, cibles, couverture, portée, intention et règles de détection.','Rejouer une décision avec la même graine ; aucun coup automatique hors des règles du mode cohérent.'],
 ['Équipe de test','Créer un ennemi temporaire ou une équipe connue sur un emplacement valide.','Identifiant d’instance distinct ; retour au point supprime les entités temporaires et leur butin.']
 ]),blocks=[('Systèmes non réalisés','La v0.6 ne possède pas la routine générale, la mémoire sociale et le suivi autonome proposés. Leurs panneaux futurs montrent l’état de développement et le scénario attendu ; ils n’affichent pas de décisions d’IA fictives comme si elles étaient calculées.'),('Panneau d’intention','Texte lisible d’abord, détail technique ensuite : “Attend la porte”, “Cherche un couvert”, “Refuse Upper-Town”. Le développeur peut ouvrir la condition et la source exacte qui ont produit ce choix.')])

page('Mode développeur','Événements temps et conflits',table=(['Système','Commande de test proposée','Effet attendu'],[
 ['7 rencontres actuelles','Choisir salvage, caravan, injured, raiders, mutants, drone ou storm dans une case de test compatible.','Instance et persistance contrôlables ; réinitialisation limitée à cette copie de rencontre, sans effacer toutes les cases visitées.'],
 ['Temps','Pause, heure fixée, avance d’une étape ou d’une heure, saut vers la relève d’un acteur.','Lire le bilan des coûts de fatigue, eau et exposition avant le saut. Avancer le temps a des effets différents de changer seulement une étiquette d’horloge.'],
 ['Graine de hasard','Afficher graine et compteur ou état du générateur ; rejouer un segment depuis un point.','Même état et mêmes actions donnent le même test. La graine seule ne suffit pas si la position dans la suite a changé.'],
 ['Caravanes futures','Préparer chargement, départ, panne, contrôle, livraison, perte ou retour.','Conservation du fret et des réserves ; aucun départ d’une cargaison déjà détruite sans nouvelle recette.'],
 ['Conflit actuel','Avant prise de parti, preuves prêtes, cessez-le-feu ou affrontement d’un côté choisi.','Les deux équipes et la responsabilité du joueur restent cohérentes ; pas de prime pour des morts entre équipes sans crédit joueur.'],
 ['Conflits futurs','Forcer un état local d’escalade, transmettre un rapport, tester un retrait ou un accord.','Acteurs vivants, objectifs, victimes et circulation de l’information vérifiés. Aucune conquête du continent implicite.'],
 ['Événement proposé','Lister les 32 définitions de conception avec leurs sites et prérequis.','Avant intégration : uniquement fiche et référence ; après intégration : recette réellement exécutable.']
 ]),note='La simulation peut être figée pour inspecter, puis avancée pas à pas. Ne pas mélanger vitesse d’animation, nombre de tours et temps de jeu : trois contrôles distincts.')

page('Mode développeur','Console et palette de commandes',
 'La palette est utilisable sans connaître une syntaxe : rechercher “soigner”, “fin réseau” ou un nom de PNJ ouvre un formulaire. La console propose une saisie plus rapide sur les mêmes commandes enregistrées. Les noms ci-dessous sont proposés, non exécutables dans le jeu actuel.',table=(['Commande proposée','Exemple','Résultat'],[
 ['scenario.load','scenario.load main.ready origin=humain','Prépare la station avant décision finale, depuis un état de référence.'],
 ['quest.prepare','quest.prepare main outcome=free phase=after','Applique la recette cohérente de l’issue communes puis ouvre le retour prévu.'],
 ['dialog.preview','dialog.preview mara variant=network.free','Lit le retour de Mara dans une instance sans effets.'],
 ['world.goto','world.goto titan entry=right-arm','Place la copie au point praticable relié à la brèche du bras droit.'],
 ['player.heal','player.heal','Restaure les PV sans changer automatiquement fatigue et contamination.'],
 ['player.resource','player.resource rad=70 fatigue=80','Fixe des valeurs de test et signale les seuils touchés.'],
 ['inventory.give','inventory.give ammo qty=24','Ajoute 24 cartouches dans la copie et journalise le diff.'],
 ['skill.set','skill.set parole value=50','Prépare une valeur effective d’Éloquence ; affiche contributions et modification.'],
 ['cheat.set','cheat.set invulnerable=true infiniteAP=false','Bascule séparément les dérogations actives.'],
 ['snapshot.restore','snapshot.restore before-last-operation','Restaure le point précédent complet, y compris scène et générateur aléatoire.']
 ]),blocks=[('Contrat commun','Nom enregistré, description, schéma d’arguments, périmètre de disponibilité, préconditions, préparation, validation, application et diff. La palette et la console utilisent le même registre.'),('Pas de code arbitraire','Aucune évaluation JavaScript libre nécessaire pour ces outils. Les identifiants sont choisis dans le catalogue ; l’outil refuse une quantité ou une destination invalide avec une raison précise. L’objectif est un test reproductible.')])

page('Mode développeur','Commandes spécialisées à prévoir',table=(['Famille proposée','Exemples de commande','Observation attendue'],[
 ['Personnage','player.prepare origin=mutant ; perk.grant id=diplomate','Origine et dérivés recalculés ; prérequis d’aptitude visibles.'],
 ['Accès et cartes','access.override enabled=true ; map.reveal scope=city','Dérogation et couche de découverte de test séparées de l’histoire.'],
 ['État et argent','inventory.give medkit qty=3 ; money.set value=500','Quantités exactes ; état avant/après consultable.'],
 ['Objet et verrou','object.prepare id=backdoor state=open ; circuit.prepare id=bunker-power state=solved','Porte, verrou, alimentation et scène liée synchronisés.'],
 ['PNJ','npc.inspect id=luz ; npc.restore id=debtor recipe=before-debt','Présence unique et conditions de quête affichées ; aucun reset général des autres PNJ.'],
 ['Compagnon','companion.prepare id=nilo mode=current ; companion.order follow','Mode simplifié ou IA future explicitement choisi ; commande refusée si l’IA n’est pas intégrée.'],
 ['Rencontre','encounter.prepare event=storm region=desert','Instance de tempête neuve dans une case valide de copie.'],
 ['Conflit','conflict.prepare id=front state=before-talk','Deux équipes au poste, aucun tir, preuves selon variante sélectionnée.'],
 ['Simulation future','caravan.prepare id=CR01 state=loading ; clock.step hours=1','Commande marquée indisponible avant intégration du système de caravanes.'],
 ['Inspection','ui.inspect focus=current ; nav.trace target=selected ; state.diff','Afficher la source du contrôle, le chemin bloqué et les modifications de session.'],
 ['Reproduction','snapshot.capture name=before-door ; test.record start ; report.export','Point de retour, trace d’entrées et rapport choisis par le développeur.']
 ]),note='Les points de référence de scénario sont des recettes métier, pas une collection de cases à cocher sans dépendances. Les identifiants de commande définitifs seront stabilisés lors de l’intégration ; les libellés français restent la voie principale.')

page('Mode développeur','Points de retour et cohérence',
 'L’atelier doit rendre l’expérimentation rapide et récupérable. La copie de test est une session complète ; une copie superficielle du seul état s ne suffit pas.',[
 ('Périmètre sauvegardé','État du personnage, inventaires, quêtes, drapeaux, présences, morts, ennemis, position locale et régionale, rencontre, route, horloge, générateur aléatoire et données futures de compagnons/caravanes. Ajouter les paramètres d’UI nécessaires à la reproduction, séparés des préférences globales.'),
 ('Isolation','Toutes les écritures de la session passent par un stockage de test distinct, y compris autosauvegarde de combat, départ de voyage, retour au titre, sauvegarde rapide et import. Les entités dynamiques de rencontre ne doivent pas contaminer un catalogue partagé avec la campagne normale.'),
 ('Application atomique','Préparer un candidat en mémoire → contrôler les identifiants et dépendances → reconstruire scène et présences → vérifier navigation et accès → appliquer la copie entière → afficher le bilan. Un échec conserve la session précédente.'),
 ('Restauration','Chaque opération engageante crée un point précédent. Le retour rétablit les ressources et effets de monde, pas seulement le panneau visible. Le système annonce quand un effet externe ne serait pas restaurable ; dans le jeu local actuel, aucune publication ne fait partie de ces commandes.'),
 ('Anciennes versions','Conserver identifiant de build, schéma, révision de monde et version de la recette. Un scénario incompatible explique quels identifiants manquent. Une migration ne redonne ni prime de recrutement ni kit d’équipement à chaque chargement.'),
 ('Diff lisible','Résumé : “+24 cartouches ; Mara replacée à Dusk ; issue communes préparée ; 2 ennemis conservés”. Détail technique repliable. Une opération sans effet est annoncée comme telle ; elle n’ajoute pas de récompense pour paraître avoir fonctionné.')])

page('Mode développeur','Quatre préparations de référence',table=(['Cas','Préparation cohérente','Vérification'],[
 ['MAIN READY','À la station de répartition ; régulateur déjà installé ; progression principale au bon stade ; archive ou accès administratif choisi ; aucune issue appliquée.','Les quatre choix se comportent selon leurs conditions ; aucune récompense de fin déjà reçue.'],
 ['MAIN FREE AFTER','Recette communes depuis le point précédent ; résultat hydraulique free ; états et récompenses de la résolution appliqués une seule fois ; retour auprès de Mara.','Réplique de retour exacte, niveau et inventaire stables si l’aperçu est rouvert. Les variantes io/native/break repartent du même point.'],
 ['FRONT TALK','À ba-front ; Lian et Alder vivants ; deux équipes de trois au poste ; pas de combat engagé ; quête ouverte et frontProof disponible dans la variante avec preuve.','Le cessez-le-feu passe par la preuve ; sans preuve, le choix requis n’est pas miraculeusement présent. Les acteurs ne tirent pas pendant l’entretien.'],
 ['SAMI RELEASE','Quête custody au stade du contrôle ; reçu disponible ou custodyRecord préparé ; Sami encore retenu ; Leal vivant ; état de sortie initial non validé.','Jouer la libération consomme les bons éléments, déclenche samiReleased et fait apparaître Sami une seule fois à son retour. Le retour Leda ne récompense qu’une fois.']
 ]),blocks=[('Variantes négatives','Pour chaque recette : acteur absent, preuve manquante, origine refusée, inventaire insuffisant et rechargement. Le test d’un état invalide doit nommer l’incohérence, par exemple “main résolue mais pompe non réparée”, pour vérifier sa détection ou la récupération prévue.'),('Couverture des fins','Le catalogue comprend les quatre issues et leurs retours auprès des personnes concernées. Un raccourci vers une fin ouvre au choix l’aperçu, le jeu de la décision ou l’état après décision ; ces trois gestes ne sont pas fusionnés.')])

page('Mode développeur','Catalogue initial des scénarios',table=(['Groupe','Cas à fournir dès le premier palier','But du test'],[
 ['Accueil et identité','Nouvelle partie humaine ; augmentée ; mutante ; cyborg ; reprise d’une ancienne sauvegarde.','Création, droits et migration ; toutes les commandes de départ utilisables.'],
 ['Dusk et ferme','Pompe en panne ; régulateur livré ; pharmacie vide ; irrigation réparée ; Nilo disponible puis recruté.','Actions locales, textes et cohérence de présence.'],
 ['Accès Steel','Humain sans ISIO/passe ; humain avec passe ; mutant au poste ; passage clandestin ; accès visiteur.','Affichage des raisons, itinéraires et restrictions individuelles.'],
 ['Affaires urbaines','Avant/après recours du bloc ; lot froid livré à Sen ou aux ouvriers ; Sami retenu/libéré/rentré ; métro en panne/rétabli.','Déblocages, choix concurrents, horaires futurs et retours de dialogue.'],
 ['Junk et justice locale','Dette avant règlement/après sortie ; vol remarqué futur ; lot manquant avec et sans preuve.','Liste d’actions, commerce, responsabilité et piste interrompue.'],
 ['Buenos Aires','Citerne sans preuve/avec deux relevés ; treuil avant/après ; lisière neutre/cessez-le-feu/combat ; cinéma avant/après.','Choix de région, prévisualisation et maintien de l’état après rechargement.'],
 ['Route','Une variante pour chacune des 7 rencontres ; case déjà résolue ; trajet interrompu ; manque d’eau.','Compréhension du voyage, stock limité et absence de relance du même butin.'],
 ['Personnage et Aura','Humain avant/après éveil ; augmenté ou cyborg refusé ; mutant proche de sa tolérance.','Contraintes, jauges et avertissements.'],
 ['Conclusions','Station prête ; io/free/native/break avant et après décision ; retour de Mara correspondant.','Accès direct à toutes les conclusions de la version actuelle.'],
 ['Modules à venir','Suivi autonome, cargaison et routines : entrées descriptives puis recettes activées à intégration.','Pas de fonction fantôme ; disponibilité contrôlée par build.']
 ]),note='Chaque ligne regroupe plusieurs variantes à numéroter lors de la réalisation. La couverture est mesurée par branches et situations réellement exécutables, pas par le nombre de miniatures dans le catalogue.')

page('Mode développeur','Diagnostic et rapport reproductible',table=(['Outil','Informations','Usage'],[
 ['Inspecteur UI','Contrôle au focus, couche active, source de données, état activé/verrouillé et raison.','Identifier un bouton sans effet, une erreur de coût ou une capture de focus.'],
 ['Navigation','Case de départ, destination, porte, obstacles et chemin calculé.','Comparer clic, sprite et point d’approche ; repérer un blocage au Titan ou dans un sas.'],
 ['Performances','Temps de préparation/rendu, mises à jour, mémoire approximative, animations actives.','Vérifier les budgets de fluidité et l’impact d’un panneau. Pas de fausse promesse issue d’un seul appareil.'],
 ['État','Build, recette, graine et compteur, lieu, jour/heure, drapeaux touchés, ordre de compagnon.','Savoir quelle dérogation explique une reproduction différente.'],
 ['Enregistrement','Commandes de test et entrées pertinentes horodatées en temps simulé.','Exporter un segment choisi ; arrêter sans téléversement automatique.'],
 ['Rapport','Attendu, observé, étapes, état initial, trace et capture facultative.','Fichier local sélectionné par le développeur ; identifiants de sauvegarde et noms personnels retirables avant partage.']
 ]),blocks=[('Rejouabilité','Une trace reproductible dépend d’un build compatible et d’un état initial complet. Une simple liste de clics n’est pas suffisante si la navigation, les dialogues ou le hasard ont changé.'),('Limites','Le mode développeur n’est pas un outil de modification du dépôt ni un bouton de déploiement. Les recettes exportées préparent une session du jeu ; toute intégration au code ou à la carte suit le travail de développement normal.')])

page('Système visuel','Valeurs communes à stabiliser',table=(['Jeton de conception','Proposition','Usage'],[
 ['Surfaces','Fond #10171C ; panneau #141C23 ; panneau dense #1C272D.','Surfaces suffisamment opaques derrière le texte ; texture légère facultative.'],
 ['Texte','Principal #EAE7DC ; secondaire #AEB7B7 ; aucun texte indispensable très assombri.','Hiérarchie par taille et poids avant multiplication des couleurs.'],
 ['Action et focus','Accent #A8DACC ; contour visible de 2 px logiques au focus.','Sélection, lien actif et accès courant. Le focus clavier se distingue du simple survol.'],
 ['Alertes','Attention #E0BF81 ; danger #F08B7E ; mode test #9EC2FF.','Toujours accompagnés d’un mot et d’un symbole. Ne pas coder toute l’interface par faction.'],
 ['Espacement','Grille 4 / 8 / 12 / 16 / 24 / 32 px ; marges sûres initiales 24 px.','Contenu lisible et zones de clic séparées ; adaptation aux encoches et petits écrans.'],
 ['Typographie','UI 18 px ; texte long 20 ; dialogue 22 ; petit libellé 16 au minimum proposé.','Les paramètres d’agrandissement restent indépendants ; chiffres tabulaires pour coûts et quantités.'],
 ['Cadres','Angles légèrement coupés ou rayon 4 px ; ligne fine, ombre courte.','Référence industrielle des images ; éviter les gravures répétées sur chaque séparateur.'],
 ['Icônes','Famille cohérente ; trait stable et pictogrammes action/état distincts.','Un symbole de pistolet pour tir ; un réticule pour visée ; mots conservés aux premières utilisations.'],
 ['Focus et validation','Survol, focus, pressé, sélectionné, occupé, verrouillé, erreur et succès.','Chaque composant possède des exemples de tous ses états avant d’être dupliqué dans les écrans.']
 ]),note='Les fichiers d’images sont des références d’aspect ; les jetons, métriques, libellés et règles de ce dossier gouvernent la réalisation. Les chiffres ne doivent jamais être lus dans une image pour calculer une action.')

page('Vérification','Parcours utilisateur à tester',table=(['Parcours','Critère proposé','Conditions'],[
 ['Première exploration','Trouver comment parler, examiner, ouvrir l’inventaire et revenir au terrain.','Avec et sans raccourcis ; aucune aide orale du testeur après l’instruction initiale.'],
 ['Comprendre un tir','Expliquer coût de marche, coût du tir, PA restants et raison d’une ligne bloquée.','Tester le cas 8 − 3 − 4 = 1, puis une cible non visible et une ressource manquante.'],
 ['Dialogue verrouillé','Comprendre le seuil manquant et consulter son explication sans choisir une autre réponse par erreur.','Souris, manette, clavier, tactile ; texte long à 200 %.'],
 ['Équiper et comparer','Retrouver une carabine, comparer au pistolet et comprendre le coût en combat.','Inventaire vide, 34 types actuels, noms longs et compagnon absent/présent.'],
 ['Voyager','Distinguer tracer, confirmer, faire halte et reprendre ; lire les coûts annoncés.','Case d’eau refusée, route interrompue, compagnon interdit et réouverture de carte.'],
 ['Personnaliser','Agrandir le texte sans gonfler tout le HUD ; déplacer la carte puis annuler.','Petit format, zoom navigateur, redimensionnement et profil importé.'],
 ['Reprendre','Différencier sauvegarde normale et point de test ; importer sans perdre l’état en cas d’échec.','Stockage indisponible, ancienne version, données invalides.'],
 ['Développer','Atteindre une fin, une branche avant décision et un refus d’accès sans jouer l’histoire.','Depuis l’écran titre ; comparaison avant/après et restauration vérifiée.']
 ]),blocks=[('Mesure','Objectif de première étude : la majorité des participants trouve les actions de base sans consulter le manuel, puis explique correctement coût et incertitude. Mesurer erreurs, temps et demandes d’aide ; fixer les seuils finaux après une petite session réelle.'),('Variété','Inclure nouveaux joueurs de CRPG et habitués de Fallout. Tester au moins un format portable et un parcours uniquement au clavier. Les maquettes statiques ne prouvent pas à elles seules la fluidité ou l’accessibilité.')])

page('Vérification','Cas limites de l’interface et du mode test',table=(['Cas','Résultat attendu'],[
 ['Double validation','Une seule dépense et un seul effet ; le choix suivant n’est pas activé par le même relâchement.'],
 ['Cible changée pendant un calcul','L’ancienne prévision ne remplace pas la nouvelle ; aucun tir automatique sur une autre cible.'],
 ['Mouvement réduit','Aucune information supprimée ; panneaux, jauges et messages compréhensibles sans translation ni secousse.'],
 ['Redimensionnement en dialogue','Même nœud, même texte lu, même choix sélectionné ; pas de retour forcé au début.'],
 ['Fermer une animation','État final propre, focus récupéré et commande suivante acceptée.'],
 ['Réglage invalide','Modules hors écran ou recouvrant Fin du tour détectés avant application ; retour accessible.'],
 ['Ouvrir Aperçu dev','XP, objets, réputation, morts, horloge et sauvegardes inchangés ; effets tentés visibles au diagnostic.'],
 ['Lancer un scénario incompatible','Bilan précis ; copie actuelle conservée ; aucune scène générique substituée.'],
 ['Sauvegarder depuis chaque voie','Bouton, raccourci, auto-combat, voyage et retour titre écrivent tous dans l’espace test si le mode est actif.'],
 ['Restaurer après une fin','État initial complet retrouvé ; récompenses et réponses de Mara correspondent à une seule issue.'],
 ['Recruter puis restaurer','Un Nilo seulement, pas de kit ou prime dupliqué ; statut et position cohérents.'],
 ['Révéler une carte de test','La campagne d’origine conserve ses vraies découvertes ; réimportation marquée comme partie test.'],
 ['Changer de périphérique','Les invites se stabilisent ; aucune sélection perdue, commande répétée ou saisie interrompue.'],
 ['Nouvel outil futur','Commande indisponible tant que son système manque ; sa présence dans une maquette ne la rend pas exécutable.']
 ]),note='Avant intégration, ces lignes sont des critères. La livraison du présent dossier n’affirme pas que ces comportements sont déjà vérifiés sur le jeu publié.')

page('Réalisation','Ordre de mise en œuvre proposé',table=(['Lot','Contenu','Passage au suivant'],[
 ['A · direction et composants','Arrêter la lecture des dix maquettes ; jetons, typographie, contrôles et états ; navigation et mouvements de base.','Prototype de composants lisible aux trois tailles principales ; aucune dépendance au contenu d’une image.'],
 ['B · terrain et combat','HUD d’exploration, prévisualisation, ciblage, Fin du tour et infos à deux niveaux.','Parcours de tir et de retour sans dépense accidentelle ; faits alignés sur les règles de la v0.6.'],
 ['C · narration et gestion','Dialogues, inventaire, commerce, personnage, journal, cartes et sauvegardes.','Lecture et focus conservés ; noms/chiffres exacts ; densité maîtrisée sur portable et tactile.'],
 ['D · personnalisation','Profils, échelles indépendantes, dock des modules, couleurs, commandes et mouvement réduit.','Aucun réglage ne masque une fonction essentielle ; annulation et migration de profil éprouvées.'],
 ['E · atelier développeur','Stockage isolé, points de retour, recettes principales, fins, dialogue et commandes de base.','Réussite des cas d’isolation et d’aperçu sans effet ; un scénario rejouable pour chaque fonction actuelle.'],
 ['F · systèmes futurs','Compagnon complet, routines, caravanes et conflits selon le dossier gameplay.','Les panneaux sont activés avec leur système réel, puis enrichis par des scénarios dev dédiés.']
 ]),blocks=[('Travail avant le code du jeu','Le présent livrable s’arrête aux références et spécifications. La future intégration commencera par les éléments approuvés des plans et de l’interface. Aucun déploiement du jeu n’a été effectué pour produire ces maquettes.'),('Réutilisation','M01–M10 servent de cibles d’aspect. Les contrôles doivent être reconstruits comme composants vivants, avec texte, focus et données réelles. Un bouton ne sera pas une zone de clic invisible posée sur une capture.')])
