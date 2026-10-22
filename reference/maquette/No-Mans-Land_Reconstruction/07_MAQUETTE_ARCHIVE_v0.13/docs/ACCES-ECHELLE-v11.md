# Accès aux bâtiments et échelle — version 0.11

## Repères de visite

| Repère | Signification | Interaction |
|---|---|---|
| Porte et flèche turquoise « ENTRER » | Un intérieur réel est accessible par cette porte | Cliquer le badge approche le joueur de la porte et propose d’entrer |
| Cadenas ambre « VERROUILLÉ » | Une vraie porte verrouillée protège un intérieur | Crochetage ou force selon les règles de cette porte ; le badge devient turquoise après ouverture |
| Petite porte barrée grise | Ce bâtiment ne possède pas d’intérieur visitable | Aucun faux accès |

Les badges se dessinent au-dessus des toits, après le décor, à taille constante à l’écran. Leurs zones de clic restent assez larges au dézoom. Les pictogrammes et le texte complètent les couleurs. Une légende est présente au-dessus de la barre de commandes. La liste « Interagir » précise également si une entrée est visitable ou verrouillée. Les états proviennent des vrais objets porte de la scène et de leurs verrous sauvegardés.

## Échelle des bâtiments

L’ancien mode `footprintFit` agrandissait le sprite pour remplir la totalité de l’emprise, sans respecter la hauteur `h` prévue dans le plan. Une maison prévue à 165 pixels pouvait atteindre 427 pixels ; le pilier du siège IO prévu à 570 pixels atteignait 1574 pixels.

La hauteur prévue est désormais une limite effective pour tous les bâtiments. L’audit couvre les 35 scènes extérieures : 495 constructions de 31 zones nécessitaient une correction. Les quatre autres zones conservent leurs dimensions. Les 21 intérieurs gardent leurs plans.

Les emprises de collision sont réduites dans les parcelles existantes, avec conservation de leur angle avant. Les cours libérées deviennent praticables ; les modèles ne sont pas seulement rétrécis à l’intérieur de collisions trop grandes. Les corrections sont fixes, consignées dans `building-scale-v11.json` et appliquées par `building-scale-v11.js`. Aucun remplissage de décor n’est généré. Les 21 seuils ont été recalés sur les façades : leur distance au point visible de la porte reste inférieure à une case. Les extrémités des passerelles suivent les façades corrigées.

## Transparence restaurée

Le bâtiment entier devient semi-transparent lorsque le joueur se trouve à deux cases de son emprise. Son opacité passe à 48 %, et à 40 % si le modèle masque directement le personnage. À distance, le modèle reste opaque. La découpe circulaire introduite en version 0.10 est retirée. Les repères d’accès restent opaques et lisibles.

## Vérification

149 tests Node passent, dont le classement des accès, le changement d’état après déverrouillage, les badges à quatre niveaux de zoom, le ciblage de la vraie porte, la transparence du modèle entier, la limite de hauteur, les collisions et les seuils des 21 portes. Les parcours de quête, les retours des intérieurs et les sauvegardes restent testés. Les 56 scènes ont été rendues avec le Canvas de production ; les vues d’ensemble des 35 extérieurs et les vues rapprochées ont été inspectées hors navigateur. L’interface et les gestes sur téléphone restent à vérifier dans un navigateur réel.

## Constructions corrigées par zone

| Zone | Constructions |
|---|---:|
| dusk | 25 |
| buenos | 19 |
| customs | 15 |
| steel | 19 |
| under | 25 |
| junk | 18 |
| relay | 6 |
| port | 7 |
| nova | 16 |
| coast | 5 |
| dusk-courts | 26 |
| dusk-workshops | 19 |
| china | 18 |
| asia | 20 |
| blocks | 19 |
| center | 17 |
| cliniccity | 12 |
| civic | 13 |
| smpd | 13 |
| upper | 12 |
| spire | 9 |
| industry | 15 |
| northcustoms | 15 |
| eastcustoms | 15 |
| northbase | 15 |
| eastbase | 15 |
| southbase | 15 |
| ba-avenues | 18 |
| ba-habitat | 19 |
| ba-ateliers | 16 |
| ba-front | 19 |
