

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
