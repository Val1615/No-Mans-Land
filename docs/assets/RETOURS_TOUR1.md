# Retours tour 1 (2026-10-28)

Pipeline : génération sur fond vert, détourage key_green_obj, despill limité à la bande de bord de 4 px, v4fix (+ balayage keystone si judge refuse), contrôle judge (Hough). Échelle 50 px/m.

## Chez Moss : `lt_comptoir_moss` (tools_lowertown.py)
- Source : art-gen/gen_lt_comptoir_moss_t1.jpg. Un seul niveau, bois et tôle sombres, comptoir éclairé ambre, enseigne peinte (sans néon).
- Clé inchangée. Emprise imposée 6 × 5 m (FP), pivot `anchor` [247, 486] (coin avant bas), taille 389 × 487 px (avant 389 × 669).
- `height_m` 4,5 (avant 7). Dans src/data/lower_town.js, `h: 7` peut passer à 4,5 (à voir côté Rivet).

## Maison de thé 茶馆 : `cl_maison_the` (tools_chinalake.py)
- Source : art-gen/gen_cl_maison_the_t1.jpg. Un seul niveau, toit recourbé noir, lanternes rouges, enseigne MAISON DE THÉ 茶馆.
- Clé inchangée. Emprise imposée 10 × 5,5 m, pivot [412, 450], taille 568 × 451 px (avant 568 × 588). `height_m` 5,5.

## Lac : `g_cl_lac` (tools_chinalake.build_lac)
- assets/generated/g_cl_lac.webp, RGBA 1000 × 700 px, couvre LAKE (x 14, z 12, 20 × 14 m), origine px = monde (14, 12).
- Eau = carreau g_cl_eau v3 (a301df7, inchangé) + couche tournée 37°, contour arrondi irrégulier, quai en planches de 0,6 m, pilotis, reflets des lanternes.
- Contour (monde, m) et version px : assets/generated/g_cl_lac.json (`polygone_monde_m`). Le polygone est le bord extérieur du quai ; zone non marchable = polygone rétréci de 0,6 m.
- Intégration proposée : dessiner g_cl_lac à la place de paintWater sur LAKE, et remplacer le rectangle non marchable par le polygone.
- Lanternes hors de l eau avec ce contour, positions proposées : (16,5 ; 13,4) vers (19,5 ; 15,6), (31,5 ; 17,2) vers (30,2 ; 17,5), (30,6 ; 24,4) vers (28,7 ; 22,9), (15,6 ; 24,8) vers (18,7 ; 22,6).

Planche avant / après : /workspace/nml-shots/retours_tour1.png
