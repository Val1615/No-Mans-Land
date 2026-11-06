

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
## Volumes (côtés, toits, fenêtres)
Statut : proposition d'Ocre, à poser par le code. Répond au retour de Valentin : certaines devantures n'étaient que des façades plates (carton).

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
