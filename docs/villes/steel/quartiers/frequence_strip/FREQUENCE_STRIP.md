

## Suite : devantures basses du sud [proposition]
Huit pièces nouvelles, toutes différentes, pour remplacer les répétitions `fs_bas1` à `fs_bas7` sur x 24-28, 34-38, 46-54 et 60-80. 2 m au plus, murets et auvents bas, rouges et roses dominants, rien d'explicite. Chacune a sa couche `<clé>_neon.webp` au format de `docs/villes/steel/ENSEIGNES_CODE.md` (même taille, même ancre, `neon_coins`). Les portes sont décrites par `porte_coins`, les comptoirs par `comptoir_coins`, le distributeur par `distributeur_coins`. Face x à la pente 0,33, front au bord de la zone (z 24), pose `BAS(id, label, clé, x, largeur)`.

| clé | thème | enseigne | px | ancre | pose |
|---|---|---|---|---|---|
| `fs_bas_preservatifs` | préservatifs et « tonifiants », comptoir | « BIEN COUVERT » | 200 x 166 | [198, 165] | x 24 à 28, front z 24 (BAS(..., 24, 4)) |
| `fs_bas_shots` | bar à shots, comptoir | « SHOT DE GRÂCE » | 200 x 166 | [198, 165] | x 34 à 38, front z 24 (BAS(..., 34, 4)) |
| `fs_bas_distributeur` | distributeur de billets bricolé | « BILLETS DOUX » | 200 x 166 | [198, 165] | x 46 à 50, front z 24 (BAS(..., 46, 4)) |
| `fs_bas_massages` | guichet de « massages », porte à rideau de perles | « MAINS DE FÉE » | 200 x 166 | [198, 165] | x 50 à 54, front z 24 (BAS(..., 50, 4)) |
| `fs_bas_laverie` | laverie de nuit, 8 m | « BLANCHIMENT » | 400 x 232 | [398, 231] | x 60 à 68, front z 24 (BAS(..., 60, 8)) |
| `fs_bas_gage` | prêteur sur gage | « MONT-DE-PITIÉ » | 200 x 166 | [198, 165] | x 68 à 72, front z 24 (BAS(..., 68, 4)) |
| `fs_bas_perruques` | perruques et costumes | « FAUX-SEMBLANTS » | 200 x 166 | [198, 165] | x 72 à 76, front z 24 (BAS(..., 72, 4)) |
| `fs_bas_implants` | réparateur d’implants | « RECHROMAGE » | 200 x 166 | [198, 165] | x 76 à 80, front z 24 (BAS(..., 76, 4)) |

Jeux de mots : « Bien couvert » (préservatifs), « Shot de grâce », « Billets doux » (le distributeur trafiqué), « Mains de fée », « Blanchiment » (la laverie), « Mont-de-pitié » (le vieux mont-de-piété, sans pitié), « Faux-semblants » (perruques et costumes), « Rechromage », d'après « Danse, sois plus chrome ».

Planche de contrôle : `/workspace/nml-shots/strip_sud_suite.png` (maquette de pose en bas, pas une capture du jeu).

## Pose retenue de la suite (main, revue Régie)
- Les huit devantures basses sont posées comme proposé (BAS, front z 24) : `fs_couvert` (Bien couvert) x 24-28, `fs_shots` 34-38, `fs_billets` 46-50, `fs_massages` 50-54, `fs_laverie` 60-68, `fs_gage` (Mont-de-pitié) 68-72, `fs_perruques` 72-76, `fs_implants` 76-80. Les répétitions au néon éteint sont retirées. Néons fixes, sauf Billets doux (grésille) et Rechromage (clignote).
- Cadre de départ (`cadre`) borné sur la rue, en 390 comme en 1280 : arrivée ouest et arrivée est sans vide au centre.
- Étiquettes à l'approche (3 m, `labelsProches`, comme Pulse Plaza) pour Rouge, Rubis, Zibeline, le rabatteur, la rabatteuse, Monsieur Velours, Brehm et Kessler. La grappe et la patrouille sont étalées le long de l'horizontale de l'écran pour que les étiquettes restent côte à côte.

## Densification de la vie (Régie, sans nouvelles pièces)

- Enseignes `_neon` : effets poussés avec parcimonie sur sexshop, salon, nouilles, couvert, shots, massages (en plus de peep, Effeuillée, lovehotel, Club 404, cabines, billets, implants). Fleurs, tabac, laverie, gage, perruques restent en néon fixe. Hors `animStats.on`.
- Figurants densifiés devant les seuils du quartier chaud, aux cabines et aux stands (miroir `face` ±1, sprites existants). PNJ nommés et dialogues inchangés. Accès ouest/est et ruelle Fusible libres. `view.masques()` vide.
## Volumes en morceaux (côtés, toits, fenêtres) [ABANDONNÉ]
Statut : **abandonné** (`"obsolete": true` dans `manifest.json`, clés conservées sans suppression). L'assemblage par morceaux (`fs_vol_*`, `<clé>_cote`, `<clé>_toit`, `<clé>_fenetres`) donnait des blocs artificiels ; Valentin a demandé des **bâtiments complets en 3/4** (voir section suivante « Bâtiments complets (3/4) »). Répond au retour de Valentin : certaines devantures n'étaient que des façades plates (carton).

### Constat
- **Déjà en volume 3/4** (non refaits) : `fs_neon7`, `fs_corestack`, `fs_retour`, `fs_capsules`, `fs_facade_nord`, `fs_facade_sud` (ancres centrales, toit et retours déjà dans le sprite).
- **Plates, complétées ici** : devantures nord `fs_sexshop`, `fs_peep`, `fs_salon`, `fs_lovehotel`, `fs_clubprive`, `fs_club`, `fs_bouche_nord` ; sud `fs_cabines` et toutes les `fs_bas_*`. Les façades existantes restent telles quelles (pas de `_v2`).

### Pièces
Pour chaque bâtiment plat, trois nouvelles clés (fichiers webp dédiés, images mutualisées par gabarit) :
1. `<clé>_cote` : retour de coin, face z pente 0,70, même hauteur que la façade, profondeur 4 ou 8 m ;
2. `<clé>_toit` : toit plat iso avec caissons, tuyaux, balises rouges peintes ; `fond:true` ;
3. `<clé>_fenetres` : calque des fenêtres ambre/rouges allumées, même taille et même ancre que la façade (comme `_neon`), pour battement ou vacillement. Pas sur les `fs_bas_*` (2 m).

Les gabarits `fs_vol_cote_*` et `fs_vol_toit_*` portent `utilise_par` ; chaque `<clé>_cote` / `_toit` a `gabarit_de`.

### Pose et ordre de dessin
- **Nord** (FN, front z 6) : toit `B(x, 6-D, W, D)` ancre `(x+W ; 6)` ; côté ancré `(x+W ; 6)` ; façade inchangée. Profondeur vers le nord.
- **Sud** (BAS / cabines, front z 24) : mêmes gabarits (retour visible à droite). Toit `B(x, 20, W, 4)` ancre `(x+W ; 24)` ; côté ancré `(x+W ; 24)`. Profondeur 4 m vers le nord (z 20–24), entre la façade et le trottoir, pour garder le raccord iso sans masquer la porte.
- **Ordre** : toits (`fond`) → côtés → façades → `_fenetres` → `_neon` → figurants.

| bâtiment | côté rue | côté | toit | fenêtres |
|---|---|---|---|---|
| `fs_sexshop` | nord | `fs_sexshop_cote` (h10_d8_a) | `fs_sexshop_toit` (8x8_a) | `fs_sexshop_fenetres` |
| `fs_peep` | nord | `fs_peep_cote` (h8_d4_a) | `fs_peep_toit` (4x4_a) | `fs_peep_fenetres` |
| `fs_salon` | nord | `fs_salon_cote` (h8_d4_b) | `fs_salon_toit` (4x4_b) | `fs_salon_fenetres` |
| `fs_lovehotel` | nord | `fs_lovehotel_cote` (h10_d8_b) | `fs_lovehotel_toit` (8x8_b) | `fs_lovehotel_fenetres` |
| `fs_clubprive` | nord | `fs_clubprive_cote` (h9_d8_a) | `fs_clubprive_toit` (8x8_a) | `fs_clubprive_fenetres` |
| `fs_club` | nord | `fs_club_cote` (h8_d8_a) | `fs_club_toit` (10x8_a) | `fs_club_fenetres` |
| `fs_bouche_nord` | nord | `fs_bouche_nord_cote` (h8_d4_a) | `fs_bouche_nord_toit` (4x4_b) | `fs_bouche_nord_fenetres` |
| `fs_cabines` | sud | `fs_cabines_cote` (h6_d4_a) | `fs_cabines_toit` (8x4_a) | `fs_cabines_fenetres` |
| `fs_bas_*` 4 m | sud | `…_cote` (h2_d4_a/b) | `…_toit` (4x4_low) | - |
| `fs_bas_nouilles` / `laverie` | sud | `…_cote` (h2_d4_a/b) | `…_toit` (8x4_low) | - |

### Gabarits

| clé | px | ancre | utilise_par |
|---|---|---|---|
| `fs_vol_cote_h10_d8_a` | 275 x 692 | [0, 691] | `fs_sexshop` |
| `fs_vol_cote_h10_d8_b` | 275 x 692 | [0, 691] | `fs_lovehotel` |
| `fs_vol_cote_h2_d4_a` | 138 x 196 | [0, 195] | `fs_bas_massages`, `fs_bas_nouilles`, `fs_bas_perruques`, `fs_bas_shots`, `fs_bas_tabac` |
| `fs_vol_cote_h2_d4_b` | 138 x 196 | [0, 195] | `fs_bas_distributeur`, `fs_bas_fleurs`, `fs_bas_gage`, `fs_bas_implants`, `fs_bas_laverie`, `fs_bas_preservatifs` |
| `fs_vol_cote_h6_d4_a` | 138 x 396 | [0, 395] | `fs_cabines` |
| `fs_vol_cote_h6_d4_b` | 138 x 396 | [0, 395] |  |
| `fs_vol_cote_h8_d4_a` | 138 x 496 | [0, 495] | `fs_bouche_nord`, `fs_peep` |
| `fs_vol_cote_h8_d4_b` | 138 x 496 | [0, 495] | `fs_salon` |
| `fs_vol_cote_h8_d8_a` | 275 x 592 | [0, 591] | `fs_club` |
| `fs_vol_cote_h9_d8_a` | 275 x 642 | [0, 641] | `fs_clubprive` |
| `fs_vol_toit_10x8_a` | 780 x 761 | [502, 760] | `fs_club` |
| `fs_vol_toit_4x4_a` | 343 x 565 | [202, 564] | `fs_peep` |
| `fs_vol_toit_4x4_b` | 343 x 565 | [202, 564] | `fs_bouche_nord`, `fs_salon` |
| `fs_vol_toit_4x4_low` | 343 x 265 | [202, 264] | `fs_bas_distributeur`, `fs_bas_fleurs`, `fs_bas_gage`, `fs_bas_implants`, `fs_bas_massages`, `fs_bas_perruques`, `fs_bas_preservatifs`, `fs_bas_shots`, `fs_bas_tabac` |
| `fs_vol_toit_8x4_a` | 543 x 531 | [402, 530] | `fs_cabines` |
| `fs_vol_toit_8x4_low` | 543 x 331 | [402, 330] | `fs_bas_laverie`, `fs_bas_nouilles` |
| `fs_vol_toit_8x8_a` | 680 x 828 | [402, 827] | `fs_clubprive`, `fs_sexshop` |
| `fs_vol_toit_8x8_b` | 680 x 828 | [402, 827] | `fs_lovehotel` |

Planche de contrôle : `/workspace/nml-shots/strip_volumes.png` (maquette hors jeu, pas une capture).

Limites : les bâtiments sud partagent les gabarits nord (retour à droite) avec une emprise z 20–24 plutôt qu'un volume hors zone au sud ; texture de côté mutualisée (2 variantes) ; calques `_fenetres` = extraction des pixels chauds, à juger en jeu.

## Bâtiments complets (3/4)
Statut : livré (`status: "v1"`), à poser par Rivet à la place des façades plates d'origine (les pièces séparées `fs_vol_*` / `*_cote` / `*_toit` / `*_fenetres` de `adb39df` sont marquées `"obsolete": true` et ne doivent pas être posées).

### Principe et conventions
- Un seul sprite complet en 3/4 isométrique `<clé>_3q` par bâtiment (façade de rue `face x` pente 0,33 à gauche de l'ancre, retour de côté `face z` pente 0,70 à droite de l'ancre, toit plat industriel avec caissons, ventilateurs, tuyaux, cheminées et balises rouges peint d'un seul tenant).
- Échelle moteur exacte (`K = 50` px/m-écran, lacet 34,5°, tangage 28,8°) : largeur gauche = `W × 41,21` px, largeur droite = `D × 28,32` px, ancre au pied du coin avant sud-est `(x + W ; z + D)`, comme `fs_neon7`, `fs_corestack`, `fs_retour` et `fs_capsules`. Aucun chevauchement ni trou entre voisins sur toute la rue de 80 m.
- Deux calques séparés à la même taille `px` et sur la même ancre `anchor` :
  - `<clé>_3q_neon` : enseigne lumineuse seule (tubes peints éteints sur `<clé>_3q`), prise en charge automatiquement en additif par `view.js` dès que `b.sprite` vaut `<clé>_3q` (`fs_bouche_nord_3q` n'a pas d'enseigne, donc pas de `_3q_neon` pour préserver la ruelle noire de Fusible).
  - `<clé>_3q_fenetres` : fenêtres, vitrines, comptoirs et ouvertures chaudes seules, pour vacillement ou pulsation par le code.

### Tableau des 19 bâtiments `_3q`

| clé `_3q` | remplace | enseigne | px | ancre | emprise (W × D) | h (m) | pose (`x, z, w, d`) | calques |
|---|---|---|---|---|---|---|---|---|
| `fs_bouche_nord_3q` | `fs_bouche_nord` | *(sans enseigne)* | 282 × 482 | [167, 480] | 4 × 4 m | 8,0 | `B(..., 7, -1, 4, 4)` (ruelle z 3) et `B(..., 50, 2, 4, 4)` (front z 6) | `_fenetres` |
| `fs_sexshop_3q` | `fs_sexshop` | « Jouets calibrés » | 561 × 649 | [332, 647] | 8 × 8 m | 10,0 | `B(..., 22, -2, 8, 8)` (nord, front z 6) | `_neon`, `_fenetres` |
| `fs_peep_3q` | `fs_peep` | « 3 secondes » | 282 × 491 | [167, 489] | 4 × 4 m | 8,0 | `B(..., 30, 2, 4, 4)` (nord, front z 6) | `_neon`, `_fenetres` |
| `fs_salon_3q` | `fs_salon` | « Tombé de rideau » | 282 × 532 | [167, 529] | 4 × 4 m | 8,5 | `B(..., 34, 2, 4, 4)` (nord, front z 6) | `_neon`, `_fenetres` |
| `fs_club_3q` | `fs_club` | « L’Effeuillée » | 643 × 654 | [414, 652] | 10 × 8 m | 8,5 | `B(..., 54, -2, 10, 8)` (nord, front z 6) | `_neon`, `_fenetres` |
| `fs_lovehotel_3q` | `fs_lovehotel` | « L’Heure exquise » | 561 × 675 | [332, 673] | 8 × 8 m | 10,0 | `B(..., 64, -2, 8, 8)` (nord, front z 6) | `_neon`, `_fenetres` |
| `fs_clubprive_3q` | `fs_clubprive` | « Club 404 » | 561 × 594 | [332, 592] | 8 × 8 m | 9,0 | `B(..., 72, -2, 8, 8)` (nord, front z 6) | `_neon`, `_fenetres` |
| `fs_cabines_3q` | `fs_cabines` | « Cabines sans C.A.G.E. » | 447 × 417 | [332, 415] | 8 × 4 m | 6,0 | `B(..., 38, 20, 8, 4)` (sud, front z 24) | `_neon`, `_fenetres` |
| `fs_bas_nouilles_3q` | `fs_bas_nouilles` | « Nouilles de minuit » | 447 × 296 | [332, 294] | 8 × 4 m | 2,6 | `B(..., 0, 20, 8, 4)` (sud, front z 24) | `_neon`, `_fenetres` |
| `fs_bas_fleurs_3q` | `fs_bas_fleurs` | « Excuses » | 282 × 230 | [167, 228] | 4 × 4 m | 2,5 | `B(..., 8, 20, 4, 4)` (sud, front z 24) | `_neon`, `_fenetres` |
| `fs_bas_tabac_3q` | `fs_bas_tabac` | « À crédit » | 282 × 232 | [167, 230] | 4 × 4 m | 2,4 | `B(..., 12, 20, 4, 4)` (sud, front z 24) | `_neon`, `_fenetres` |
| `fs_bas_preservatifs_3q` | `fs_bas_preservatifs` | « Bien couvert » | 282 × 229 | [167, 227] | 4 × 4 m | 2,5 | `B(..., 24, 20, 4, 4)` (sud, front z 24) | `_neon`, `_fenetres` |
| `fs_bas_shots_3q` | `fs_bas_shots` | « Shot de grâce » | 282 × 237 | [167, 235] | 4 × 4 m | 2,7 | `B(..., 34, 20, 4, 4)` (sud, front z 24) | `_neon`, `_fenetres` |
| `fs_bas_distributeur_3q` | `fs_bas_distributeur` | « Billets doux » | 282 × 253 | [167, 251] | 4 × 4 m | 2,4 | `B(..., 46, 20, 4, 4)` (sud, front z 24) | `_neon`, `_fenetres` |
| `fs_bas_massages_3q` | `fs_bas_massages` | « Mains de fée » | 282 × 237 | [167, 235] | 4 × 4 m | 2,8 | `B(..., 50, 20, 4, 4)` (sud, front z 24) | `_neon`, `_fenetres` |
| `fs_bas_laverie_3q` | `fs_bas_laverie` | « Blanchiment » | 447 × 298 | [332, 296] | 8 × 4 m | 2,7 | `B(..., 60, 20, 8, 4)` (sud, front z 24) | `_neon`, `_fenetres` |
| `fs_bas_gage_3q` | `fs_bas_gage` | « Mont-de-piété » | 282 × 217 | [167, 215] | 4 × 4 m | 2,6 | `B(..., 68, 20, 4, 4)` (sud, front z 24) | `_neon`, `_fenetres` |
| `fs_bas_perruques_3q` | `fs_bas_perruques` | « Faux-semblants » | 282 × 233 | [167, 231] | 4 × 4 m | 2,7 | `B(..., 72, 20, 4, 4)` (sud, front z 24) | `_neon`, `_fenetres` |
| `fs_bas_implants_3q` | `fs_bas_implants` | « Rechromage » | 282 × 218 | [167, 216] | 4 × 4 m | 2,6 | `B(..., 76, 20, 4, 4)` (sud, front z 24) | `_neon`, `_fenetres` |

### Notes d'intégration pour le code (Rivet)
1. **Remplacement dans `BUILDINGS_STRIP`** :
   - Nord (`front z = 6`) : remplacer `FN(id, label, '<clé>', x, w)` par `B(id, label, '<clé>_3q', x, 6 - d, w, d)` avec `d = 8` pour `fs_sexshop_3q`, `fs_club_3q`, `fs_lovehotel_3q`, `fs_clubprive_3q` (donc `z = -2`) et `d = 4` pour `fs_peep_3q`, `fs_salon_3q`, `fs_bouche1` (donc `z = 2`). Pour `fs_bouche0` (fond de la ruelle Fusible `x 8–10`), poser `B('fs_bouche0', '', 'fs_bouche_nord_3q', 7, -1, 4, 4, { named: false, solid: [{ x: 8, z: 0, w: 2, d: 3 }] })` pour laisser `z 3–6` libre autour de Fusible `(9 ; 5,4)`.
   - Sud (`front z = 24`, aligné sur `fs_retour` et `fs_capsules`) : remplacer `BAS(id, label, '<clé>', x, w)` par `B(id, label, '<clé>_3q', x, 20, w, 4)` et `fs_cabines` par `B('fs_cabines', 'Cabines sans C.A.G.E.', 'fs_cabines_3q', 38, 20, 8, 4)`.
2. **Enseignes `_3q_neon`** : chargées automatiquement par `view.js` (`b.sprite + '_neon'`). Pour `fs_n_club` (`effet: 'saute'`), recaler la tranche `saute` de `[0.52, 0.58]` (ancien sprite sans retour de côté) vers `[0.334, 0.36]` sur `fs_club_3q_neon` (le retour droit occupe la moitié droite de l'image).
3. **Fenêtres `_3q_fenetres`** : brancher un calque additif léger (vacillement lent / réaction hors plafond mobile, sur le modèle de `_neon`).
4. **Dégagement `view.masques()` côté sud** : l'emprise sud passant de `z 23–24` (1 m) à `z 20–24` (4 m, comme `fs_retour` et `fs_capsules`), avancer légèrement vers le nord sur le trottoir (`z ≈ 17,2–18,2`, comme Mme Okoro et Vieux Marius) les 4 personnages qui se tenaient à `z 19,4–20,2` (`fs_ocre`, `fs_racoleuse`, `fs_mac`, et le figurant `gen_fs_client_imper` en `(45 ; 19,4)`), ainsi que le figurant `(38,4 ; 13,6)` d'environ 0,8 m vers le nord si le haut de `fs_cabines_3q` l'effleure.

Planches de contrôle (maquettes hors jeu, pas des captures) :
- `/workspace/nml-shots/strip_3q.png` (assemblage iso complet de la rue de 80 m avec sols, lueurs et figurants `gen_fs_*`)
- `/workspace/nml-shots/strip_3q_zoom.png` (gros plan 1:1 de 4 bâtiments avec échelle PNJ et calques `_neon` / `_fenetres`)
