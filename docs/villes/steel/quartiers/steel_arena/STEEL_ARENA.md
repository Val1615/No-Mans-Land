

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
