# Accès et décors — version 0.12

## Taille et repères

La version 0.11 sert de référence. Le rectangle de chaque sprite de bâtiment est multiplié par 1,25 sur les deux axes ; son centre horizontal et sa ligne de sol restent fixes. Les parcelles, les rues et les plans écrits ne sont pas redistribués. Le Titan, qui est un décor monumental distinct, conserve ses proportions. Les murs intérieurs ne sont pas agrandis.

Les points visibles des portes, les zones de clic et les badges partagent ce rectangle agrandi, y compris pour les façades retournées. Les 21 seuils sont recalculés dans les cases libres devant les portes ; leur distance à l’ancrage visible se situe entre 4 et 20 pixels monde. Le registre `dist/interiors-directory.json` est actualisé. La transparence du bâtiment entier reste à 48 % à proximité, et à 40 % lorsqu’il masque directement le joueur.

| État réel | Repère affiché |
|---|---|
| Intérieur avec porte ouverte | Porte et flèche turquoise « ENTRER » |
| Intérieur avec porte verrouillée | Cadenas ambre « VERROUILLÉ » |
| Bâtiment sans intérieur | Aucun |

## Blocage des entrées : cause reproduite

Avec Nilo, quitter un intérieur chargeait d’abord le quartier et son point d’arrivée. Le joueur était ensuite replacé devant la porte, tandis que Nilo restait au point d’arrivée, à 8–59 cases selon le lieu. Le contrôle de distance du compagnon refusait donc l’entrée suivante, sans message exploitable.

Le retour place maintenant le compagnon après le positionnement final du joueur. Les entrées signalent le combat en cours, la mauvaise zone, la distance à la porte, son verrou ou l’état du compagnon. Les serrures et les règles du combat restent effectives.

Une migration unique reconnaît l’ancien état sans ambiguïté : compagnon en suivi au point d’arrivée, joueur devant une porte dont le retour a été enregistré, distance excessive entre les deux. Elle le rapproche du joueur. Les états d’attente, de blessure et les compagnons volontairement éloignés dans d’autres situations sont préservés.

## Longues barres identifiées

Les liaisons de canalisations, grillages et balustrades étaient encore des traits épais ou des poteaux tracés. Elles utilisent désormais six images transparentes, avec une orientation pour chaque axe isométrique. Les matières présentent isolation, brides, supports, mailles et pierre sculptée.

Chaque liaison est dessinée en sections raccordées de deux ou trois cases, avec un tri de profondeur par section. Les longues distances ne grossissent plus artificiellement une seule image. Les positions d’extrémité des plans sont conservées ; les conduites non alignées suivent les deux axes du plan. Cette opération découpe le dessin des infrastructures existantes, sans générer de remplissage des lieux.

Les câbles fins et les murs intérieurs texturés restent des géométries natives. Cette passe vise les trois familles de barres identifiées ; elle ne revendique pas une révision de chaque détail artistique du jeu.

## Livraison et vérification

Le point d’entrée HTML utilise `runtime-v12/app.js`. Les 39 modules y sont copiés depuis les sources canoniques par `node tools/package-runtime.mjs`, avec un manifeste SHA-256. Le répertoire versionné renouvelle les URL de tout le graphe d’importation pour éviter de mélanger d’anciens modules mis en cache avec cette livraison. Cela constitue une prévention supplémentaire, distincte du défaut de compagnon reproduit.

158 tests Node passent. Les nouveaux contrôles vérifient le facteur exact de 1,25, la conservation de la base des modèles, l’absence de badges non visitables, les allers-retours répétés des 21 intérieurs avec Nilo, la migration ciblée et les refus expliqués. Un test de branchement de l’interface clique les badges de la clinique, de l’hôtel et du bar de Dusk-Town, entre, sort et rentre à nouveau. Les six images et le découpage de toutes les infrastructures sont contrôlés. Le manifeste confirme que les modules livrés correspondent aux sources testées.

Les 56 scènes ont été rendues avec le Canvas de production hors navigateur. Les vues d’ensemble des 35 extérieurs, les nouveaux décors et une vue de proximité ont été inspectés. L’adaptateur DOM ne valide ni le rendu CSS ni les gestes réels d’un téléphone ; ces contrôles restent à effectuer dans un navigateur réel.
