# Échelle et accès — version 0.13

## Augmentation supplémentaire des modèles

La référence est la version 0.12. Le centre horizontal, la ligne de sol et l’orientation restent communs au dessin, aux repères et aux ancrages des portes. Les modèles déjà dessinés à 300 pixels de haut ou plus restent à leur taille. Les autres reçoivent les facteurs suivants :

| Groupe | Hausse par rapport à 0.12 | Nombre |
|---|---:|---:|
| Petites maisons, murs habités, abris et bureaux modulaires v0/v4/x1/x5 | 50 % | 142 |
| Services, ateliers, serres et pavillons b0/b1/v1/v3/v7/v16/v17/x0/x3 | 35 % | 146 |
| Autres modèles modestes | 25 % | 165 |
| Grands modèles déjà à l’échelle | Aucune | 74 |

Les dimensions avant et après des 527 modèles sont consignées dans `building-scale-v13.json`. Le Titan reste un décor monumental distinct. Les plans de parcelles, les réseaux et le mobilier n’ont pas été remplis ou déplacés aléatoirement.

Les 21 seuils sont recalculés devant les façades agrandies, dans les cases libres reliées au point d’arrivée. Leur distance au point visible de la porte est de 2–27 pixels monde. Les coordonnées du registre des intérieurs sont actualisées.

## Interaction des bâtiments

Le moteur reconnaissait uniquement le petit point de porte et le badge sur le toit. Un clic ailleurs sur le bâtiment pouvait donc faire marcher le joueur sous le décor au lieu de proposer l’entrée.

Le clic examine désormais les pixels visibles de la construction, dans l’ordre de profondeur du décor, et renvoie sa vraie porte si elle en possède une. Les façades retournées utilisent le même masque alpha retourné. Les marges transparentes restent disponibles pour le terrain. Un modèle sans intérieur ne reçoit pas de fausse entrée ; les badges des bâtiments non visitables restent absents.

Le trajet d’approche peut choisir le seuil lui-même, parmi les destinations libres. Le contrôle de distance reste identique pour entrer. Une tentative impossible à cause du passage ou d’un combat présente un message dans le dialogue, au lieu d’un retour silencieux. Les serrures et l’état du compagnon gardent leurs règles.

Les 21 intérieurs existants restent le périmètre de visite de cette version. La correction du clic ne crée pas d’intérieur supplémentaire dans les autres constructions.

## Vérification

164 tests Node passent. Ils incluent les dimensions et points d’appui, les pixels cliquables des 20 façades avec intérieur, les façades retournées, les badges, les approches depuis les points d’arrivée avec et sans compagnon, les allers-retours des 21 intérieurs, les refus expliqués et les anciennes sauvegardes réparées en version 0.12. Le Titan conserve son accès ancré au bras.

Le test de branchement de l’interface entre dans la clinique en cliquant la façade avec une surface de 393 × 716, puis ressort avec Nilo. Il utilise un adaptateur DOM et le Canvas natif, sans moteur de navigateur : il valide les coordonnées et les actions, pas le CSS ni les gestes réels sur téléphone.

Les 56 scènes ont été rendues hors navigateur et les 35 vues d’ensemble extérieures inspectées. La distribution charge `runtime-v13/app.js` ; un manifeste contrôle l’égalité des 39 modules livrés et des sources testées. Les sauvegardes restent au même format.
