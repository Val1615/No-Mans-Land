

## Suite : toit, retour ouest, fans et sols [proposition]
- **Toit et masse de l'enceinte.** Gradins supérieurs et anneau de toit en treillis, 42 m au total, posés 4 m en retrait derrière les façades de 28 m (ligne z 26 au sud, x 88 à l'est). La partie du haut, environ 14 m, dépasse nettement au-dessus des façades. Le bas reste caché derrière elles. Modulaire comme les façades : `ar_toit_x` (16 m), `ar_toit_z` (16 m), `ar_toit_angle_se` (rayon 4 m, centre (84 ; 22)) et `ar_toit_angle_so` (rayon 4 m, centre (4 ; 22)). Filets violets et cyan fixes, projecteurs et feux de balisage peints allumés, aucun faisceau.
- **Retour ouest.** `ar_facade_retour_ouest` arrondit le bout ouest de la façade sud sur x 0 à 4 (quart de cercle de 4 m, centre (4 ; 26)). La partie de l'arc tournée vers l'ouest est de dos et n'est pas dessinée.
- **Fans** (ajout de Régie). Quatre silhouettes nouvelles, à la lumière d'appoint chaude et ambrée : écharpe levée, pancarte vierge, deux bâtons lumineux ambre, et un groupe de deux. Ce groupe tient dans un seul sprite de 360 x 512 (double largeur), avec l'ancre [180, 511], pour garder l'échelle des PNJ. Aucune feuille de marche, le moteur ne fait pas encore marcher les PNJ.
- **Sols.** `g_ar_dalles_neutre` est l'anthracite neutre qui remplace `g_ar_dalles_usees`, trop bleu (l'ancienne clé est gardée). Deux variantes : `g_ar_parvis_marquages` (lignes de file continues le long de x, flèches, cases des portes 3 et 4, peinture usée) et `g_ar_parvis_use` (zones usées, taches, mégots). Toutes sont sombres, tuilables en 512 x 512 et sans reflet.

Ordre d'affichage conseillé : toit z, toit x d'ouest en est, angles du toit, puis façade est, façades sud, retour ouest, angle de façade, écrans.

| clé | px | ancre | pose suggérée |
|---|---|---|---|
| `ar_toit_x` | 801 x 2366 | [800, 2364] | en retrait de 4 m derrière la façade sud, ligne z 26 : segments x 4 à 20, 20 à 36, 36 à 52, 52 à 68, 68 à 84 ; ancre au pied de l’extrémité est (x fin ; 26) |
| `ar_toit_z` | 552 x 2488 | [0, 2485] | en retrait de 4 m derrière la façade est, ligne x 88 : z 6 à 22 ; ancre au pied de l’extrémité sud (88 ; 22) |
| `ar_toit_angle_se` | 339 x 2153 | [0, 2130] | angle sud-est du toit : centre (84 ; 22), raccords (84 ; 26) et (88 ; 22) ; ancre au raccord sud (84 ; 26), option ancre [-4, 0] si posé par son coin avant (88 ; 26) |
| `ar_toit_angle_so` | 107 x 2197 | [105, 2195] | angle sud-ouest du toit : centre (4 ; 22), raccords (0 ; 22) et (4 ; 26) ; ancre au raccord sud (4 ; 26), c’est-à-dire son coin avant |
| `ar_facade_retour_ouest` | 107 x 1497 | [105, 1495] | extrémité ouest de la façade sud : emprise x 0 à 4, z 26 à 30 ; ancre au pied du raccord avec ar_f_s0 (4 ; 30), soit B(x 0, z 26, 4, 4) avec ancre [0, 0] par rapport au coin avant (4 ; 30) |
| `gen_ar_fan_echarpe` | 180 x 512 | [90, 511] | brandit son écharpe, au bord de la file : (34 ; 38,5) |
| `gen_ar_fan_pancarte` | 180 x 512 | [90, 511] | pancarte vierge levée, devant les portiques hors couloir : (54 ; 33) |
| `gen_ar_fan_batons` | 180 x 512 | [90, 511] | deux bâtons ambre levés, parvis central : (48 ; 46) |
| `gen_ar_fans_duo` | 360 x 512 | [180, 511] | groupe de deux qui chante, près du food truck nouilles : (26 ; 47) |
| `g_ar_dalles_neutre` | 512 x 512 | tuile | parvis, remplace g_ar_dalles_usees qui tire vers le bleu ; à alterner avec les deux variantes |
| `g_ar_parvis_marquages` | 512 x 512 | tuile | parvis devant l’entrée (x 36 à 52, z 32 à 42) : lignes de file le long de x, flèches vers les portiques, cases de portes 3 et 4 ; pas sur le reste du parvis |
| `g_ar_parvis_use` | 512 x 512 | tuile | parvis : autour des food trucks, des stands et au pied des pylônes, là où l’on piétine |

Planche de contrôle : `/workspace/nml-shots/arena_toit_suite.png` (maquette de pose en bas, pas une capture du jeu).

## Pose retenue de la suite (main, revue Régie)
- Toit : `ar_toit_z` (x 84-88, z 6-22), `ar_toit_x` ×5 (ligne z 26, x 4 à 84), `ar_toit_angle_se` (ancre [-4, 0]) et `ar_toit_angle_so`, posés comme proposé, dessinés avant tout le reste (option `fond`). Le premier segment porte le solide de l'enceinte ; l'ancien dôme `ar_arena` est retiré. `ar_facade_retour_ouest` est posé sur x 0-4, z 26-30.
- Toit visible au départ : à 30 px/m (24 en mobile), l'image de 33 m des façades remplit l'écran. Un plan d'arrivée (`cadre.arrivee`) cadre donc large, à 15 px/m, 40 m devant le joueur : le toit dépasse au-dessus des façades, la foule est en bas. Dès les premiers pas, le cadre revient en douceur au cadre de jeu habituel.
- Fans : écharpe (34 ; 38,5), pancarte (54 ; 33), bâtons (53 ; 47,6, décalés de la nouvelle file), duo (26 ; 47). `gen_ar_fans_duo` en 360 x 512 passe : la largeur du sprite suit le rapport de l'image.
- Sols : `g_ar_dalles_neutre` partout ; une rangée de `g_ar_parvis_marquages` (x 36-52, z 31,6-41,8) ; `g_ar_parvis_use` autour des stands, des trucks et des pylônes ; rue en asphalte au sud (z 60-64). Hors zone, une marge de rue (`ground.marge`, 90 m) remplace le vide.
- Bords : à l'ouest, façades de Steel (`pp_facade_a_o`, `pp_facade_b_o`, `pp_facade_b_o2`) sur x 0-2, l'arrivée `ar_ouest` (z 42-46) reste libre. Au sud, barrières de police (`ar_barriere_file`) sur z 59,6, avec des passages en x 32-40 et 56-64.
- Foule : 66 figurants fixes, plus de 20 sprites de foule différents (Arena, Strip, Pulse, Méga-Line, Dôme), miroir alterné. Ils se répartissent en grappes autour des stands et des trucks, dans le serpentin, devant les portiques et devant l'écran ouest. Le serpentin est prolongé de deux lignes (z 43 et 46) et 7 passants avancent dans la file.
- Lumière : appoint chaud ; chaque stand et chaque truck a une lueur ambre ou orangée au sol et une petite lumière (option `y` des lueurs, triée avec sa source) ; ambres aux pieds des portiques ; cyan réservé aux pylônes et à l'écran est.
- Reste pour Ocre : des immeubles bas ou des devantures pour le bord sud (aujourd'hui une rue et des barrières, la marge est une rue nue) ; éventuellement des façades de fond pour la marge ouest.


## Enceinte basse (ar2)
Statut : proposition d'Ocre, à poser par le code. Elle répond à la revue de départ : façades de 28 m et toit de 42 m formaient un mur violet qui remplissait l'écran, le toit n'était jamais vu et la foule paraissait minuscule.

- **Façades** (décision de taille de la Régie : environ 15 m). Les clés `ar2_facade_*` reprennent exactement les lignes de pose des `ar_facade_*` : façade sud sur z 30 (x 4-20, 20-36, entrée 36-52, 52-68, 68-84), angle sud-est de rayon 8 centré en (84 ; 22), façade est sur x 92 (z 6-22), retour ouest x 0-4, z 26-30. Même emprise, mêmes ancres au pied, hauteur 15 m. Matière : acier anthracite et métal sombre, bandeaux lumineux blancs sobres en haut de façade, violet et cyan en filets courts seulement. Au pied : portes de service, grilles de ventilation, appliques, socle.
- **Entrée** `ar2_facade_entree` : portiques sous lumière ambre chaude. Coins recalculés dans le manifest : `porte_coins` [[120, 535], [650, 710], [650, 954], [120, 779]], `portiques_coins` [[200, 749], [551, 865], [551, 926], [200, 809]], `fronton_coins` [[93, 414], [685, 609], [685, 705], [93, 510]]. Les coins du fronton posés dans le code (`ecran.coins` de l'entrée, calés sur l'ancienne image de 28 m) doivent être remplacés par ces valeurs.
- **Toit** : un dôme bas et bombé, couronne à 23 m, rive à 15,6 m juste au-dessus des façades, entièrement visible depuis le parvis. Silhouette ovale : rectangle arrondi x 0-92, z 0-30, rayon 8 à l'est, 4 à l'ouest, qui suit le ventre des façades. Anneau lumineux peint sur la rive, tirets violets et cyan, projecteurs de rive et balises rouges de couronne peints allumés. Aucun faisceau : ils restent au code. Le toit se pose en six morceaux, tous avec `fond: true` et ancrés au coin avant au sol de leur emprise :
  - `ar2_toit_angle_so` : B(0, 0, 20, 30) ;
  - `ar2_toit_x` trois fois : B(20, 0, 16, 30), B(36, 0, 16, 30), B(52, 0, 16, 30) (la même image, le dôme est identique tous les 16 m) ;
  - `ar2_toit_angle_se` : B(68, 14, 24, 16) ;
  - `ar2_toit_z` : B(68, 0, 24, 14).
  Ces emprises remplacent celles de `ar_toit_*` (lignes z 26 et x 88) : le toit couvre maintenant toute l'enceinte.
- **Écrans géants** : l'ancien écran sud (12 x 6,75 m à 12 m d'élévation) dépasserait une façade de 15 m. `ar2_ecran_geant_x` fait 9,6 x 5,4 m à 7,5 m (x 8,4 à 18), `ar2_ecran_geant_z` fait 8 x 4,5 m à 7,5 m (z 11 à 19). Mêmes ancres que les anciens : (18 ; 30,8) et (92,8 ; 19). Zone d'écran vide (8, 8, 12), `ecran_coins` dans le manifest, contenu animé par le code.
- **Ordre d'affichage** : les six morceaux de toit d'abord (`fond`), d'ouest en est puis `ar2_toit_z` avant `ar2_toit_angle_se` ; ensuite façade est, façades sud, retour ouest, angle ; écrans en dernier.
- **Ce qui ne change pas** : le parvis (fans, stands, trucks, barrières, sols, pylônes) reste tel quel.
- **Anciennes clés** : les `ar_facade_*`, `ar_toit_*` et `ar_ecran_geant_*` (28 et 42 m) restent dans le manifest et disponibles, mais ne sont plus recommandées.
- **Proposition** : avec une enceinte de 15 à 23 m, le plan d'arrivée large (`cadre.arrivee`) n'est peut-être plus nécessaire. À juger en jeu.

| clé | px | ancre | remplace | pose |
|---|---|---|---|---|
| `ar2_facade_courbe_x` | 801 x 1016 | [800, 1014] | ar_facade_courbe_x (28 m) | façade sud, ligne z 30, segments de 16 m bord à bord : x 4 à 20, 20 à 36, 52 à 68, 68 à 84 ; ancre au pied de l’extrémité est (x fin ; 30), comme ar_facade_courbe_x |
| `ar2_facade_entree` | 801 x 1016 | [800, 1014] | ar_facade_entree (28 m) | milieu de la façade sud : x 36 à 52, z 30 ; ancre (52 ; 30) ; la file arrive du sud vers (44 ; 31) |
| `ar2_facade_courbe_z` | 552 x 1138 | [0, 1135] | ar_facade_courbe_z (28 m) | façade est, ligne x 92 : z 6 à 22 ; ancre au pied de l’extrémité sud (92 ; 22) |
| `ar2_facade_angle` | 677 x 854 | [0, 811] | ar_facade_angle (28 m) | angle sud-est : centre (84 ; 22), raccords (84 ; 30) et (92 ; 22) ; ancre au pied du raccord sud (84 ; 30), soit B(84, 22, 8, 8, { ancre: [-8, 0] }) comme ar_facade_angle |
| `ar2_facade_retour_ouest` | 107 x 847 | [105, 845] | ar_facade_retour_ouest (28 m) | bout ouest de la façade sud : emprise x 0 à 4, z 26 à 30 ; ancre au pied du raccord (4 ; 30), soit B(0, 26, 4, 4) comme ar_facade_retour_ouest |
| `ar2_toit_angle_so` | 1952 x 1808 | [915, 1807] |  | bout ouest du dôme : B(0, 0, 20, 30) ; ancre au coin avant au sol (20 ; 30) ; couvre x 0 à 20 (débord à x -0,15) |
| `ar2_toit_x` | 1841 x 1853 | [804, 1852] |  | partie courante du dôme, identique tous les 16 m : B(20, 0, 16, 30), B(36, 0, 16, 30), B(52, 0, 16, 30) ; ancre au coin avant au sol (x fin ; 30) |
| `ar2_toit_angle_se` | 1803 x 1930 | [1204, 1929] |  | angle sud-est du dôme : B(68, 14, 24, 16) ; ancre au coin avant au sol (92 ; 30) |
| `ar2_toit_z` | 1501 x 1600 | [1198, 1599] |  | bout est du dôme, au nord de l’angle : B(68, 0, 24, 14) ; ancre au coin avant au sol (92 ; 14) |
| `ar2_ecran_geant_x` | 480 x 803 | [479, 802] | ar_ecran_geant_x (12 x 6,75 m à 12 m : dépasserait la façade de 15 m) | façade sud, sur ar2_facade_courbe_x (x 4 à 20) : x 8,4 à 18, de 7,5 à 12,9 m ; même ancre que ar_ecran_geant_x (18 ; 30,8) ; largeur 9,6 au lieu de 12 |
| `ar2_ecran_geant_z` | 275 x 792 | [0, 792] | ar_ecran_geant_z (10 m à 12 m : dépasserait la façade de 15 m) | façade est, sur ar2_facade_courbe_z : z 11 à 19, de 7,5 à 12 m ; même ancre que ar_ecran_geant_z (92,8 ; 19) ; longueur 8 au lieu de 10 |

Planche de contrôle : `/workspace/nml-shots/arena_enceinte_basse.png` (maquette de pose hors jeu avec figurants gen_ar_* pour l'échelle, pas une capture). Raccords du toit vérifiés en recomposant les morceaux à leurs ancres contre le rendu entier : 2 px de trou, 6 px en trop, 18 px de chevauchement sur 5,26 millions.

Limites : la façade est s'arrête à z 6 comme avant, le bout nord-est du toit (z 0 à 6) n'a pas de façade dessous, il n'est visible qu'en bord de silhouette ; la texture de façade est agrandie et reste un peu douce de près.

## Pose retenue (ar2)

- Les pièces `ar2_` remplacent les `ar_` dans `steel_arena` (les `ar_` restent dans les assets, plus posées) : dôme en six morceaux (`ar2_toit_angle_so`, trois `ar2_toit_x`, `ar2_toit_z`, `ar2_toit_angle_se`) en `fond: true`, z 0→30 ; façades 15 m sur les mêmes emprises et lignes ; écrans géants `ar2_ecran_geant_x/z` (coins lus au manifeste, contenu au code) ; fronton aux coins `[[93,414],[685,609],[685,705],[93,510]]`.
- Moteur : `src/core/catalogue.js` ne faisait passer en bâtiments que `pp|fs|ar|df|ml_` ; `ar2_` ajouté (même chargement pour le jeu et l'éditeur).
- Plan d'arrivée gardé, recalé : sans lui, au départ (1, 44) le cadre de jeu (30 px/m, 24 en mobile) ne montre que l'angle ouest (ovale de 92 m). Desktop 12 px/m, avance 10 ; mobile 4 px/m, avance 12 ; u [26, 30]. Les noms (PNJ, services) sont masqués tant que le plan large domine, les sorties restent.
- Coin nord-est : la façade est s'arrête à z 6 ; en jeu, au bord est (95, 31), la coupe tombe en haut d'écran, sombre sur fond noir, sans trou clair. Une pièce z 0→6 fermerait la silhouette, non bloquante.

## Densification de la vie (Régie, sans nouvelles pièces)

- Écrans code : pages BATTLE et FRONTON enrichies, périodes un peu plus courtes et décalées. Projecteurs : balayages et périodes différenciés (hors `animStats.on`).
- Figurants FIXES densifiés autour des stands/trucks et un second rang devant les portiques (sprites du pool existant). Plan large d'arrivée et enceinte ar2 inchangés.
- Ambres des stands/trucks/guichets : `flicker` lent (sol + lampes y), sans teinte violette.
