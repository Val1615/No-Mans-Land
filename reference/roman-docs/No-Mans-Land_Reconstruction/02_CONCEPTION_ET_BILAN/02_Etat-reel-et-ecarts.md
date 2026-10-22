# État réel et écarts de la maquette

Relevé du commit 1fe00eb76e5b85c57e68a8a7530237cb8c352ab6 après chargement des installations de scènes et de services. « Présent » signifie retrouvé dans le code ; cela ne signifie ni équilibré, ni beau, ni validé sur téléphone.

## Chiffres vérifiés

| Élément | Nombre | Limite de lecture |
| --- | ---: | --- |
| Lieux fixes | 56 | 35 extérieurs et 21 intérieurs |
| Bâtiments extérieurs placés | 527 | Pas 527 modèles uniques |
| Cases terrestres régionales | 167 | Sept compositions de halte réutilisées |
| Définitions de PNJ | 113 | Pas 113 biographies et routines profondes |
| Placements fixes de PNJ | 112 | Pas une simulation permanente de population |
| Routes locales de PNJ | 12 | Surtout Dusk-Town et services |
| Fils de quête | 21 | Longueurs et profondeur inégales |
| Objets d’inventaire | 34 | Types déclarés |
| Objets du monde | 216 | Définitions interactives, pas des intérieurs |
| Scénarios développeur | 18 | Pas toutes les branches de toutes les quêtes |
| Tests historiques réexécutés | 164 | Logique et coordonnées, pas recette mobile |

## Fonctionnalités et limites

| Domaine | Présent | Écart à traiter |
| --- | --- | --- |
| Exploration | Hexagones, chemins, caméra, zoom, sélection | Proportions, masquage et circulation à reconstruire |
| Carte régionale | Cases, trajet, interruption, reprise | Peu de compositions locales distinctes |
| Rencontres | Sept événements, coûts et persistance | Pas les 32 propositions du dossier historique |
| Création | Quatre origines, attributs, compétences, passés, apparences | Personnalisation visuelle et équilibre limités |
| Progression | XP, niveaux et aptitudes | Richesse des spécialisations non validée |
| Combat | PA, portée, couvert, visée, fumée, garde et réaction | IA et objectifs limités |
| Survie | Santé, fatigue, radiations et eau | Entretien corporel et matériel incomplet |
| Dialogues | Voix, choix, conditions et variantes | Écriture inégale, conséquences souvent locales |
| Quêtes | 21 fils, quatre conclusions principales | Pas un monde réactif complet |
| Services | Commerce, soins, repas, chambre et établis | Beaucoup de bâtiments non visitables |
| Intérieurs | 21 scènes reliées à des portes | Tests d’accès partiellement neutralisés |
| Compagnie | Nilo, suivi, attente, ordres, ressources, incapacité | Un seul compagnon ; confiance détaillée absente |
| Routines | Douze routes sauvegardées | Pas de mémoire sociale ou simulation régionale complète |
| Caravanes | Rencontre avec marchand et stock limité | Six circuits persistants seulement proposés |
| Conflits | Front local IO/Nativos à Buenos Aires | Pas de guerre régionale dynamique |
| Factions/populations | Codex de sept factions et cinq populations | Codex ne signifie pas campagne ou région jouable |
| Steel-Megalopolis | 18 secteurs, dont 11 protégés | Identité, échelle perçue et raccord spatial insuffisants |
| Buenos Aires | Cinq extérieurs, trois intérieurs | Revue de densité et d’identité nécessaire |
| Dusk-Town | Trois extérieurs, cinq intérieurs | Retours persistants sur taille et accès |
| Junk-Burgh | Un extérieur, trois intérieurs | Les quatre plans JB ne sont pas quatre quartiers jouables |
| Novo Córdoba | Un extérieur, deux intérieurs | Les trois plans NC restent partiellement transposés |
| Port/siège UFSA | Plans de conception | Implantations non jouables |
| Ranch/Rakkens | Références de factions | Régions non réalisées |
| Interface | HUD, inventaire, fiche, cartes, options | Fidélité visuelle et vrai tactile insuffisamment vérifiés |
| Atelier | Copie de test, commandes, scénarios et annulation | Pas d’éditeur complet ni couverture exhaustive |
| Sauvegarde | Locale, reprise, import/export et migrations | Aucun compte ni synchronisation distante |
| Audio | Ambiance synthétisée | Bande originale non livrée |

## Intérieurs visitables

| Identifiant | Fonction | Parent |
| --- | --- | --- |
| clinic | Clinique de Dusk-Town | dusk |
| dusk-hotel | Hôtel des Volets | dusk |
| dusk-bar | Bar du Passage | dusk |
| dusk-grocery | Épicerie de la pompe | dusk |
| dusk-repair | Atelier de Nilo | dusk-workshops |
| backroom | Arrière-salle des comptes | junk |
| junk-bazaar | Bazar de Roque | junk |
| junk-surgery | Clinique du comptant | junk |
| bunker | Coursives du Striker Oméga | titan |
| forum-service | Agence de services du Forum | steel |
| lin-workshop | Électronique Lin | china |
| sen-clinic | Consultations K-12 | cliniccity |
| civic-hall | Hall du registre | civic |
| smpd-reception | Bureau de garde SMPD | smpd |
| ba-cinema | Cinéma des Patios | ba-habitat |
| ba-reading | Archives | buenos |
| ba-dispensary | Dispensaire des Patios | ba-habitat |
| nova-surplus | Intendance UFSA | nova |
| nova-infirmary | Infirmerie UFSA | nova |
| port-office | Capitainerie | port |
| relay-control | Salle de conduite 07 | relay |

Une scène intérieure n’est pas forcément accessible sans condition : serrure, combat, autorisation et état du compagnon peuvent s’y opposer. Un refus intentionnel doit être distingué d’un clic défaillant ou d’un trajet impossible.

## Architecture historique

Le jeu est une application statique HTML/CSS, JavaScript ES modules et Canvas. Le dossier dist contient sources principales et distribution. Aucun moteur 3D, modèle Blender ou serveur de monde n’est fourni.

| Ensemble | Responsabilité |
| --- | --- |
| data.js et extensions | Lieux, objets, PNJ, règles, quêtes |
| engine.js | État, actions, combat, dialogue, progression, sauvegarde |
| scenes.js et modules de plans | Implantations et installation des transformations |
| settlement-v9.js, infrastructure-v10.js, service-interiors.js | Corrections urbaines et services |
| geometry.js, building-scale-v11.js, door-approaches-v11.js | Projection, tailles, emprises et seuils |
| render.js, scenery.js, terrain.js | Rendu, ressources et matériaux |
| world.js, overland.js, wild-plans.js | Cases, trajet, haltes et événements |
| companions.js, residents.js | Nilo et routines locales |
| app.js, interface.css et modules UI | Écrans, commandes, options et audio |
| developer.js | Atelier et scénarios |
| runtime-v13 | Copie active de 39 modules chargée par index.html |
| runtime-v12 | Copie antérieure conservée dans l’archive |
| art-source, tests, tools | Originaux raster, vérifications et outils historiques |

Des installations modifient des registres et des plans en place. Le catalogue est donc extrait après initialisation. Le JSON ne sérialise pas les fonctions ; les règles exécutables restent dans les sources.

## Vérification et limites

Les 164 tests ont été réexécutés sur les sources récupérées. Les tests UI utilisent un adaptateur DOM et un Canvas natif, sans moteur de mise en page de navigateur. Les tests d’accès ouvrent parfois les serrures et retirent les adversaires pour isoler le cheminement.

Les captures Canvas jointes sont historiques et hors navigateur. Cet export n’a pas effectué une nouvelle campagne complète, une recette Android/iOS, une mesure de performance sur appareil modeste ni un contrôle de toutes les anciennes sauvegardes.

Les PDF antérieurs, le roman, les planches, les dix maquettes, les prompts et manifestes d’images disponibles sont conservés. Aucun fichier musical Suno historique ou sauvegarde personnelle n’a été retrouvé.
