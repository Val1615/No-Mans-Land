

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

## Bâtiments complets (3/4)

Statut : **posé sur `main`** (pack d'Ocre `7e5478b`), en remplacement des sprites plats, trucks, stands et bords ouest `pp_facade_*_o` (les anciennes clés plates restent conservées dans le manifeste et les assets). Même méthode que les 19 `fs_*_3q` du Strip (`FREQUENCE_STRIP.md`). Valentin a rejeté les façades plates et les volumes assemblés par pièces : chaque bâtiment est un seul sprite en 3/4 avec façade, retour et toit peints ensemble, plus des calques `_3q_neon` et `_3q_fenetres` de même taille et même ancre (additif par le code).

L'enceinte `ar2_` (commit 58703a8, posée en 3e5a8c6) **reste telle quelle**.

### Géométrie
- 50 px/m ; façade rue (face x) = W × 41,21 px ; retour (face z) = D × 28,32 px ; pentes 0,33 / 0,70.
- Ancre au pied du coin avant sud-est `(x+W ; z+D)`.
- Emprises en multiples de 4 m, profondeur min 4 m.
- Palette anthracite et ambre (réfs de direction seulement : `nml-refs/steel_arena/arena_a.png`, `arena_b.png`).

### Tableau

| clé `_3q` | remplace / nouveau | enseigne | px | ancre | emprise (W × D) | h (m) | pose | calques |
|---|---|---|---|---|---|---|---|---|
| `ar_guichets_3q` | ar_guichets | « Guichets » | 282 × 267 | [167, 265] | 4 × 4 m | 3,5 | `B('ar_guichets', 'Guichets', 'ar_guichets_3q', 6, 44, 4, 4)` | `_neon`, `_fenetres` |
| `ar_booking_3q` | *(nouveau)* | « Booking » | 282 × 299 | [167, 297] | 4 × 4 m | 3,2 | `B('ar_booking', 'Booking', 'ar_booking_3q', 10, 48, 4, 4)` | `_neon`, `_fenetres` |
| `ar_securite_3q` | ar_securite | « Contrôle IO » | 282 × 255 | [167, 253] | 4 × 4 m | 3,5 | `B('ar_securite', 'Poste Human Corp', 'ar_securite_3q', 14, 52, 4, 4)` | `_neon`, `_fenetres` |
| `ar_stand_merch_b_3q` | ar_stand_merch_b (3×2) | « Merch officiel » | 282 × 216 | [167, 213] | 4 × 4 m | 2,8 | `B('ar_merch_b', 'Merch officiel', 'ar_stand_merch_b_3q', 26, 40, 4, 4)` | `_neon`, `_fenetres` |
| `ar_stand_merch_c_3q` | ar_stand_merch_c (3×2) | « Merch » | 282 × 240 | [167, 237] | 4 × 4 m | 2,8 | `B('ar_merch_c', 'Chariot de merch', 'ar_stand_merch_c_3q', 54, 40, 4, 4)` | `_neon`, `_fenetres` |
| `ar_foodtruck_nouilles_3q` | ar_foodtruck_nouilles (6×2,5) | « Nouilles du parvis » | 447 × 317 | [332, 315] | 8 × 4 m | 3,2 | `B('ar_truck_n', 'Nouilles du parvis', 'ar_foodtruck_nouilles_3q', 16, 46, 8, 4)` | `_neon`, `_fenetres` |
| `ar_foodtruck_boissons_3q` | ar_foodtruck_boissons (6×2,5) | « Hydratation » | 447 × 317 | [332, 315] | 8 × 4 m | 3,2 | `B('ar_truck_b', 'Boissons', 'ar_foodtruck_boissons_3q', 68, 46, 8, 4)` | `_neon`, `_fenetres` |
| `ar_regie_3q` | ar_regie (6×4) | « Régie » | 447 × 314 | [332, 312] | 8 × 4 m | 3,5 | `B('ar_regie', 'Camion régie', 'ar_regie_3q', 76, 50, 8, 4)` | `_neon`, `_fenetres` |
| `ar_tribunes_3q` | *(nouveau)* | « Tribunes » | 725 × 469 | [496, 467] | 12 × 8 m | 4,0 | `B('ar_tribunes', 'Tribunes', 'ar_tribunes_3q', 20, 32, 12, 8)` | `_neon`, `_fenetres` |
| `ar_tech_ouest_a_3q` | ar_bord_o0 / pp_facade_a_o | « Technique » | 561 × 694 | [332, 691] | 8 × 8 m | 8,0 | `B('ar_tech_a', 'Technique ouest', 'ar_tech_ouest_a_3q', 0, 30, 8, 8)` | `_neon`, `_fenetres` |
| `ar_tech_ouest_b_3q` | ar_bord_o1 / pp_facade_b_o | « *(sans enseigne)* » | 396 × 506 | [167, 504] | 4 × 8 m | 7,0 | `B('ar_tech_b', '', 'ar_tech_ouest_b_3q', 0, 46, 4, 8, { named: false })` | `_fenetres` |
| `ar_tech_ouest_c_3q` | ar_bord_o2 / pp_facade_b_o2 | « *(sans enseigne)* » | 396 × 499 | [167, 496] | 4 × 8 m | 7,0 | `B('ar_tech_c', '', 'ar_tech_ouest_c_3q', 0, 54, 4, 8, { named: false })` | `_fenetres` |

### À faire côté code (Rivet)

1. Remplacer les sprites plats / trucks / stands et les bords ouest `pp_facade_*_o` par les appels `B(...)` du tableau (emprises recalées en multiples de 4 m, profondeur min 4 m).
2. Ajouter `ar_booking` (près des guichets) et `ar_tribunes` (gradins du parvis, ouest de la file).
3. Enseignes `_3q_neon` : chargées automatiquement par `view.js` dès que `b.sprite` vaut `<clé>_3q` (sauf `ar_tech_ouest_b_3q` et `ar_tech_ouest_c_3q`, sans enseigne).
4. Fenêtres `_3q_fenetres` : calque additif léger (vacillement lent / flicker ambre, hors plafond mobile).
5. Lueurs existantes (ambre stands/trucks/guichets) : recalculer légèrement les centres si l'emprise change (trucks 8×4, merch 4×4, régie 8×4).
6. Figurants près des bords ouest : vérifier qu'ils ne rentrent pas dans les nouvelles emprises 4×8 / 8×8.

### Effets conseillés
- `ar_guichets_3q_neon` : fixe (écran guichet déjà en `ar_ens_guichet`).
- `ar_booking_3q_neon` : pulse lent.
- `ar_securite_3q_neon` : fixe ; voyants verts des portiques éventuellement en code.
- `ar_stand_merch_*_3q_neon` : flicker ambre lent (comme aujourd'hui).
- `ar_foodtruck_*_3q_neon` : fixe ou grésillement très léger.
- `ar_regie_3q_neon` : pulse lent.
- `ar_tribunes_3q_neon` : fixe.
- `ar_tech_ouest_a_3q_neon` : fixe (stencil TECHNIQUE).

### Planches
- `/workspace/nml-shots/arena_3q.png` (maquette iso du parvis avec enceinte `ar2_` et les 12 bâtiments, pas une capture du jeu)
- `/workspace/nml-shots/arena_3q_zoom.png` (gros plan 1:1 de 4 bâtiments avec calques `_neon` / `_fenetres`)

### Pose retenue (3/4, main)
- Les 12 sprites `*_3q` d'Ocre (`7e5478b`) sont posés dans `BUILDINGS_ARENA`, enceinte `ar2_` inchangée (`3e5a8c6`) : `ar_guichets`, `ar_booking`, `ar_securite`, `ar_merch_b`, `ar_merch_c`, `ar_truck_n`, `ar_truck_b`, `ar_regie`, `ar_tribunes`, `ar_tech_a`, `ar_tech_b` et `ar_tech_c` ; répliques `CLOSED_ARENA` ajoutées pour `ar_booking`, `ar_tribunes` et `ar_tech_a`.
- Ajustements géométriques : `ar_booking` posé en `(10, 44, 4, 4)` bord à bord à l'est d'`ar_guichets` sur `z 44–48` (`ar_e_guichet` recentré en `(8,2 ; 48,2)`) plutôt qu'en `(10, 48)`, où la perspective 3/4 recouvrait 51 % de l'enseigne « GUICHETS », 45 % des vitrines et masquait Anouk ; `ar_tribunes` conservé tel quel en `(20, 32, 12, 8)` (couloir de 4 m vers la file et les portiques libre). Lampadaire ouest `ar_lamp0` avancé en `(4 ; 40)` au sud de `ar_tech_a` (`8×8`), grille d'évacuation décalée en `(34 ; 36)`.
- Calques additifs hors plafond mobile (`animStats.on <= 8`) : 12 `*_3q_fenetres` à vacillement lent (`animStats.fenetres = 12`) et 10 `*_3q_neon` (`animStats.enseignes = 10` : 5 fixes auto sur `ar_guichets`, `ar_securite`, `ar_truck_b`, `ar_tribunes`, `ar_tech_a` ; 5 réglés dans `loc.enseignes` — `ar_booking` et `ar_regie` en `pulse` lent, `ar_merch_b` et `ar_merch_c` en `pulse` ambre décalé, `ar_truck_n` en léger `gresille` ; `ar_tech_b` et `ar_tech_c` sans néon).
- Lueurs ambre/orangé, zones d'usure, PNJ et foule recalés autour des emprises élargies (`4×4` et `8×4`) et des bords ouest (`8×8` et `4×8`) : Clém avancée en `(53,6 ; 45)` devant `ar_merch_c`, spectateurs de l'écran ouest et grappes des stands/trucks/régie dégagés + clients devant Booking et Tribunes (85 figurants fixes, `view.masques()` vide, accès file/portiques/parvis vérifiés).

## Playlist OST commune (`fecc483` / `27b3f1f`, `src/core/ost_centre.js`)
- Playlist commune Groovy Crew posée sur `main` (4 titres MP3 `assets/audio/ost_centre/`, pack `fecc483`) et partagée en singleton avec Center-Town, Fréquence Strip et Pulse Plaza : franchir la grille `fs_est` / `ar_ouest` garde l'instance `<audio>` et sa position de lecture sans coupure ; API rythme `ostCentre` branchée sur la même lecture.

## Calques rythmiques pulse [proposition Ocre 2026-11-06]
Overlays additifs **même taille et même ancre** que les sprites existants (`ar2_*_pulse`, `ar_*_3q_pulse`) : rubans LED dôme/enceinte, projecteurs, cadres d’écrans. Props neufs : mâts, enceintes, gantry, strobe.

| clé overlay | parent | px | ancre | bande | effet | prio mobile |
|---|---|---|---|---|---|---|
| `ar2_facade_entree_pulse` | `ar2_facade_entree` | [801, 1016] | [800, 1014] | kick | bandeaux LED entrée + appliques | 1 |
| `ar2_facade_courbe_x_pulse` | `ar2_facade_courbe_x` | [801, 1016] | [800, 1014] | mid | filets façade sud | 2 |
| `ar2_facade_courbe_z_pulse` | `ar2_facade_courbe_z` | [552, 1138] | [0, 1135] | mid | filets façade est | 3 |
| `ar2_facade_angle_pulse` | `ar2_facade_angle` | [677, 854] | [0, 811] | kick | rubans angle SE | 2 |
| `ar2_facade_retour_ouest_pulse` | `ar2_facade_retour_ouest` | [107, 847] | [105, 845] | aigus | liseré retour ouest | 4 |
| `ar2_toit_x_pulse` | `ar2_toit_x` | [1841, 1853] | [804, 1852] | kick | anneau rive dôme + projecteurs | 1 |
| `ar2_toit_z_pulse` | `ar2_toit_z` | [1501, 1600] | [1198, 1599] | kick | rive est dôme | 2 |
| `ar2_toit_angle_se_pulse` | `ar2_toit_angle_se` | [1803, 1930] | [1204, 1929] | kick | projecteurs angle SE | 1 |
| `ar2_toit_angle_so_pulse` | `ar2_toit_angle_so` | [1952, 1808] | [915, 1807] | kick | projecteurs angle SO | 2 |
| `ar2_ecran_geant_x_pulse` | `ar2_ecran_geant_x` | [480, 803] | [479, 802] | mid | cadre écran géant | 2 |
| `ar2_ecran_geant_z_pulse` | `ar2_ecran_geant_z` | [275, 792] | [0, 792] | mid | cadre écran géant z | 3 |
| `ar_tribunes_3q_pulse` | `ar_tribunes_3q` | [725, 469] | [496, 467] | kick | écrans tribunes + rubans | 1 |
| `ar_regie_3q_pulse` | `ar_regie_3q` | [447, 314] | [332, 312] | mid | voyants régie | 3 |
| `ar_guichets_3q_pulse` | `ar_guichets_3q` | [282, 267] | [167, 265] | aigus | liserés guichets | 4 |
| `ar_booking_3q_pulse` | `ar_booking_3q` | [282, 299] | [167, 297] | mid | enseigne booking | 4 |
| `ar_securite_3q_pulse` | `ar_securite_3q` | [282, 255] | [167, 253] | kick | voyants portiques | 3 |
| `ar_tech_ouest_a_3q_pulse` | `ar_tech_ouest_a_3q` | [561, 694] | [332, 691] | mid | bandes technique | 3 |
| `ar_stand_merch_b_3q_pulse` | `ar_stand_merch_b_3q` | [282, 216] | [167, 213] | aigus | vitrine merch | 4 |
| `ar_foodtruck_nouilles_3q_pulse` | `ar_foodtruck_nouilles_3q` | [447, 317] | [332, 315] | mid | auvent truck | 4 |
| `ar_mat_projecteur_pulse_3q_pulse` | prop | [143, 338] | [84, 335] | kick | faisceau mât | 2 |
| `ar_enceinte_pulse_3q_pulse` | prop | [184, 242] | [125, 239] | kick | enceinte parvis | 3 |
| `ar_gantry_led_pulse_3q_pulse` | prop | [390, 376] | [331, 373] | mid | gantry LED | 2 |
| `ar_strobe_pulse_3q_pulse` | prop | [108, 154] | [64, 152] | aigus | strobe ambre | 3 |

### Props rythmiques Arena (clés neuves)
| clé | emprise proposée (x,z,w,d) | B(...) |
|---|---|---|
| `ar_mat_projecteur_pulse_3q` | voir pose | `B('ar_mat_p0', '', 'ar_mat_projecteur_pulse_3q', 40, 36, 2, 2, { named: false })` |
| `ar_enceinte_pulse_3q` | voir pose | `B('ar_ence_p0', '', 'ar_enceinte_pulse_3q', 48, 38, 3, 2, { named: false })` |
| `ar_gantry_led_pulse_3q` | voir pose | `B('ar_gantry0', '', 'ar_gantry_led_pulse_3q', 30, 34, 8, 2, { solid: [], named: false })` |
| `ar_strobe_pulse_3q` | voir pose | `B('ar_strobe0', '', 'ar_strobe_pulse_3q', 56, 36, 1.5, 1.5, { named: false })` |

### Chevauchements Arena détectés dans src/
- `ar_toit_so` ∩ `ar_f_retour` = 16.0 m² — [0.0, 0.0, 20.0, 30.0] vs [0.0, 26.0, 4.0, 4.0] (**toit fond** au-dessus façade : attendu, pas un bug de pose au sol).
- `ar_toit_se` ∩ `ar_f_angle` = 64.0 m² — [68.0, 14.0, 24.0, 16.0] vs [84.0, 22.0, 8.0, 8.0] (**toit fond** au-dessus façade : attendu, pas un bug de pose au sol).

## Calques rythmiques pulse2 (kick fort) [proposition Ocre 2026-11-06]
Les `_pulse` v1 étaient trop discrets (surtout toit, entrée, retour ouest, écrans). **Nouvelles clés `*_pulse2`** : même `px` / `ancre` que le parent ; rubans LED **larges et denses** ambre + blanc chaud (accents cyan), cohérents anthracite/ambre Arena. Anciennes `_pulse` correspondantes : `"obsolete": true` uniquement.
**Priorité Rivet (kick)** : 1) `ar2_ecran_geant_x_pulse2` + `ar2_ecran_geant_z_pulse2` ; 2) faisceaux `*_faisceau` (toit + entrée + projecteurs) ; 3) `ar2_facade_entree_pulse2` + toits `ar2_toit_*_pulse2`.

| clé | parent | px | ancre | bande | effet | prio mobile |
|---|---|---|---|---|---|---|
| `ar2_ecran_geant_x_pulse2` | `ar2_ecran_geant_x` | [480, 803] | [479, 802] | kick | cadre ambre/blanc + waveform/EQ lumineux (contenu additif) | 1 |
| `ar2_ecran_geant_z_pulse2` | `ar2_ecran_geant_z` | [275, 792] | [0, 792] | kick | cadre ambre/blanc + waveform/EQ lumineux (contenu additif) | 1 |
| `ar2_facade_entree_faisceau` | `ar2_facade_entree` | [801, 1016] | [800, 1014] | kick | cônes projecteurs ambre/blanc chaud visibles | 1 |
| `ar2_toit_angle_se_faisceau` | `ar2_toit_angle_se` | [1803, 1930] | [1204, 1929] | kick | cônes projecteurs ambre/blanc chaud visibles | 1 |
| `ar2_toit_x_faisceau` | `ar2_toit_x` | [1841, 1853] | [804, 1852] | kick | cônes projecteurs ambre/blanc chaud visibles | 1 |
| `ar2_facade_entree_pulse2` | `ar2_facade_entree` | [801, 1016] | [800, 1014] | kick | bandeaux LED entrée + appliques | 2 |
| `ar2_toit_angle_se_pulse2` | `ar2_toit_angle_se` | [1803, 1930] | [1204, 1929] | kick | rubans LED rive + anneaux dômes denses | 2 |
| `ar2_toit_angle_so_faisceau` | `ar2_toit_angle_so` | [1952, 1808] | [915, 1807] | kick | cônes projecteurs ambre/blanc chaud visibles | 2 |
| `ar2_toit_angle_so_pulse2` | `ar2_toit_angle_so` | [1952, 1808] | [915, 1807] | kick | rubans LED rive + anneaux dômes denses | 2 |
| `ar2_toit_x_pulse2` | `ar2_toit_x` | [1841, 1853] | [804, 1852] | kick | rubans LED rive + anneaux dômes denses | 2 |
| `ar2_toit_z_faisceau` | `ar2_toit_z` | [1501, 1600] | [1198, 1599] | kick | cônes projecteurs ambre/blanc chaud visibles | 2 |
| `ar2_toit_z_pulse2` | `ar2_toit_z` | [1501, 1600] | [1198, 1599] | kick | rubans LED rive + anneaux dômes denses | 2 |
| `ar_ens_faisceau` | `?` | [768, 256] | [64, 255] | kick | rubans horizontaux façade | 2 |
| `ar_mat_projecteur_pulse_3q_faisceau` | `ar_mat_projecteur_pulse_3q` | [143, 338] | [84, 335] | kick | cônes projecteurs ambre/blanc chaud visibles | 2 |
| `ar_projecteur_faisceau` | `ar_projecteur` | [160, 300] | [80, 299] | kick | cônes projecteurs ambre/blanc chaud visibles | 2 |
| `ar_pylone_projecteur_faisceau` | `ar_pylone_projecteur` | [218, 600] | [105, 599] | kick | cônes projecteurs ambre/blanc chaud visibles | 2 |
| `ar2_facade_angle_pulse2` | `ar2_facade_angle` | [677, 854] | [0, 811] | kick | rubans horizontaux façade | 3 |
| `ar2_facade_courbe_x_pulse2` | `ar2_facade_courbe_x` | [801, 1016] | [800, 1014] | kick | rubans horizontaux façade | 3 |
| `ar2_facade_courbe_z_pulse2` | `ar2_facade_courbe_z` | [552, 1138] | [0, 1135] | kick | rubans horizontaux façade | 3 |
| `ar2_facade_retour_ouest_pulse2` | `ar2_facade_retour_ouest` | [107, 847] | [105, 845] | kick | bandeaux serrés retour ouest (ex-faible) | 3 |
| `ar_tribunes_3q_pulse2` | `ar_tribunes_3q` | [725, 469] | [496, 467] | kick | rubans horizontaux façade | 3 |
| `ar_regie_3q_pulse2` | `ar_regie_3q` | [447, 314] | [332, 312] | kick | rubans horizontaux façade | 4 |

### Faisceaux projecteurs (calque séparé `_faisceau`)
- Toits / entrée : `ar2_toit_x_faisceau`, `ar2_toit_z_faisceau`, `ar2_toit_angle_se_faisceau`, `ar2_toit_angle_so_faisceau`, `ar2_facade_entree_faisceau` — même taille/ancre que le parent ; brancher sur le **kick** (opacity pulse fort).
- Props : `ar_projecteur_faisceau`, `ar_pylone_projecteur_faisceau`, `ar_mat_projecteur_pulse_3q_faisceau`.

Maquettes : `/workspace/nml-shots/arena_pulse2.png` (avant `_pulse` / après `_pulse2`+`_faisceau`).

### Branchement Rivet (résumé)
```
// kick fort — plafond mobile : garder en priorité
ecrans: ar2_ecran_geant_x_pulse2, ar2_ecran_geant_z_pulse2
faisceaux: ar2_toit_*_faisceau, ar2_facade_entree_faisceau, ar_*_faisceau
rubans: ar2_facade_entree_pulse2, ar2_toit_*_pulse2, ar2_facade_*_pulse2, ar_tribunes_3q_pulse2
// ne plus brancher les *_pulse obsolete (toit/entrée/écrans/facades listés)
```
