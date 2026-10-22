# Reconstruction neuve et recette

Proposition de méthode. Les critères ci-dessous sont à réaliser dans le nouveau projet ; ils ne constituent pas une validation de la maquette.

## 1. Décider et étalonner

Créer un dépôt neuf, conserver l’archive séparée. Choisir plateformes, perspective, caméra, déplacement et chaîne de fabrication après lecture des échecs. Éprouver le moteur sur échelle, porte, occlusion, intérieur, compagnon et performance mobile.

Comparer si utile une scène 3D orthographique et une chaîne 2,5D avec les mêmes volumes et le même parcours. Le choix dépend de lisibilité, temps d’édition, cohérence et coût de production, pas de l’héritage du premier jet.

| Bloc | Contrat |
| --- | --- |
| Canon | Références, invariants, contradictions et décisions visibles |
| Contenu | Identifiants stables, définitions validées |
| Partie | État sérialisable, schéma versionné, migrations |
| Commandes | Préconditions, coût, résultat et refus explicites |
| Simulation | Horloge de jeu, persistance et limites hors champ |
| Présentation | Rendu et animation sans règles cachées |
| Outils | Mêmes données et commandes que le jeu |
| Livraison | Build reproductible, ressources identifiées et version connue |

La porte relie bâtiment, orientation, sélection, seuil, condition, cible, retour et groupe dans un seul contrat. La fiche PNJ relie identité, métier, lieux, horaires, connaissances, dialogue et réactions. L’événement relie région, prérequis, participants, plan écrit, issues et répétition.

## 2. Tranche initiale

Construire un quartier de Dusk-Town avec pompe, logements, clinique, bar, hôtel et atelier. Les voies piétonnes, accès de service, cours et limites sont prévues. Au moins trois services possèdent un intérieur fonctionnel ; l’hôtel permet de tester repos et passage du temps.

Ajouter une courte route, une halte, une rencontre à plusieurs issues, une quête avec deux résolutions différentes et un compagnon. La quête traverse un intérieur et permet un retour après changement d’état.

Le personnel interrompt et reprend son activité. Les soins consomment un paiement réel. Le compagnon suit, attend, combat et passe les portes. La sauvegarde conserve tous ces états.

Valider cette tranche sur ordinateur et téléphone avant l’expansion. Ajouter ensuite douane désertique et quartier protégé de Steel pour tester le contraste avec la même échelle.

## 3. Étapes

| Phase | Livrable | Condition de sortie |
| --- | --- | --- |
| A | Canon, moteur et référentiel | Porte et masquage lisibles dans la scène d’étalonnage |
| B | Contrat d’asset et éditeur de quartier | Collisions, orientations et accès édités ensemble |
| C | Dusk-Town et services | Parcours sans blocage, proportions et usages vérifiés |
| D | Boucle RPG | Quête, route, combat, compagnon, conséquences et sauvegarde |
| E | Contraste IO | Extérieur aride et intérieur entretenu, droits différenciés |
| F | Monde vivant limité | Première caravane, routines et conflit inspectables |
| G | Extension | Revue individuelle de chaque région et quartier |
| H | Campagne et finition | Parcours complets, écriture, équilibre, audio et accessibilité |

La phase D valide une fondation, pas la densité finale de Fallout 1 ou 2. Cette ampleur exige ensuite un travail de contenu conséquent.

## 4. Critères spatiaux

| ID | Vérification | Réussite |
| --- | --- | --- |
| GEO-01 | Acteur, porte, étage | Proportions du référentiel respectées au zoom de jeu |
| GEO-02 | Emprise et passage | Aucun chemin ne semble traverser une façade ; passage visible utilisable |
| GEO-03 | Orientation | Porte, lumière, pivot et collision contrôlés pour chaque variante |
| GEO-04 | Seuil et intérieur | Arrivées, sorties et fonction cohérentes |
| GEO-05 | Masquage | Personnage lisible, fondu stable, collision conservée |
| GEO-06 | Réseaux | Continuité des voies et flux de fret/eau crédibles |
| ART-01 | Ressources | Aucun asset requis absent ou provisoire silencieusement publié |
| ART-02 | Sol | Échelle stable, transitions et raccords soignés |
| ART-03 | Quartier | Identité reconnaissable sans lire son nom |
| ART-04 | Décor | Fonction ou indice narratif, dégagements préservés |
| LORE-01 | Big Larry | Aucun habitant permanent ni ville sur l’impact |
| LORE-02 | Sarcophage | Frontière visuelle et sociale entre dehors et dedans |
| LORE-03 | Populations | Cyborg, androïde, mutant et Aura conformes au lore |

Les tolérances physiques sont fixées avec la projection choisie. Un écart arbitraire en pixels ne doit pas remplacer une mesure monde et une revue de lecture.

## 5. Accès, compagnie et états

Pour chaque porte réelle, tester l’arrivée générale et plusieurs directions locales ; ouverture, serrure, restriction, combat, obstruction et chargement à proximité. Vérifier façade, badge, liste et bouton, souris et toucher, avec plusieurs zooms.

Répéter entrer-sortir-entrer avec compagnon proche, éloigné, en attente et à terre. Tout refus intentionnel est expliqué. Après sortie, l’allié ne reste pas au point d’arrivée général.

Contrôler santé, munitions, matériel, état d’attente et objets de quête. Une interruption de transition reprend dans un état valide. Une ancienne sauvegarde est migrée ou refusée sans écraser la partie saine.

| Domaine | Scénarios indispensables |
| --- | --- |
| Quête | Solutions différentes, refus, abandon, décès pertinent, retour après résolution |
| Combat | Ligne bloquée, couvert, manque de PA/munitions, fumée, alliés et factions |
| Commerce | Stock, argent, capacité, transfert et paiement unique |
| Routine | Conversation, heure, combat, absence puis retour |
| Caravane | Départ, retard, intervention, arrivée et stock sans duplication |
| Réputation | Connaissance justifiée, effet local compréhensible |
| Dialogue | Voix identifiable, information située et choix clair |
| Progression | Styles viables et récompenses hors combat |
| Sauvegarde | Conservation complète, migration et isolation de l’atelier |

## 6. UI, technique et atelier

Tester téléphone étroit portrait, format intermédiaire et bureau ; paysage si supporté. Tâches : créer, lire une compétence, trouver une boutique, entrer, acheter, équiper, préparer une route, comprendre un refus, combattre et sauvegarder.

Vérifier texte agrandi, contraste, mouvement réduit, clavier, focus, panneaux fermables et lecture sans couleur seule. Sur mobile, mesurer les zones tactiles, vérifier le clavier virtuel et empêcher qu’un glissement de carte déclenche un déplacement involontaire.

Définir des budgets de chargement, mémoire et fluidité sur un appareil cible, puis mesurer. Charger les grandes images selon leur usage. Tester un rechargement après publication pour détecter les mélanges de versions.

L’atelier prépare des états cohérents avec les mêmes règles que le jeu. Le retour à la campagne restaure exactement son état. Afficher collisions, seuils, masques, trajectoires, points de routine, quêtes et événements.

Un rapport de bug comprend version, appareil/format, lieu, état de quête, ordre des actions, graine, porte et état du compagnon. Ces éléments doivent permettre une reproduction sans deviner.

## 7. Définition d’une livraison

Fournir contenu réalisé, scénarios exécutés, captures du vrai jeu, limites et écarts. Les propositions restent étiquetées. Une quantité de fichiers, sprites ou tests ne suffit pas à déclarer un quartier terminé.

Les retours de Valentin sur identité, densité et proportions doivent provoquer une révision de conception lorsqu’ils révèlent un problème structurel. Le nouveau projet possède son identité et son hébergement ; l’ancien reste une référence.
