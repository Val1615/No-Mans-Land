

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
