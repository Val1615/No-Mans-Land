# Steel-Megalopolis · Lower-Town : positions dans la scène (lot 1)

Généré depuis `src/data/lower_town.js` (zone `steel_lower`, 48 × 36 m). Repère : x vers l'est, z vers le sud, origine au coin nord-ouest. x, z = coin min de l'emprise ; le pivot du sprite (coin avant bas) tombe sur (x + w, z + d). Orientation : une seule (caméra v4, façades sud et est visibles), aucun miroir. « collision » = emprise bloquante.

## Bâtiments et props
| id | clé sprite | x | z | emprise w × d (m) | pivot (x+w, z+d) | collision | état |
|---|---|---|---|---|---|---|---|
| lt_dalle | lt_dalle_center | 0 | 0 | 48 × 2.5 | 48, 2.5 | partielle (pylônes) | PROVISOIRE (volume) |
| lt_usine7 | lt_atelier_usine | 25 | 1 | 7 × 14 | 32, 15 | emprise | sprite Ocre |
| lt_bastide | lt_atelier_petit | 36 | 7 | 8 × 6 | 44, 13 | emprise | sprite Ocre |
| lt_immeuble | lt_immeuble_ouvrier | 5 | 5 | 8 × 6.5 | 13, 11.5 | emprise | sprite Ocre |
| lt_immeuble3 | lt_immeuble_ouvrier | 14.5 | 5 | 8 × 6.5 | 22.5, 11.5 | emprise | sprite Ocre |
| lt_moss | lt_comptoir_moss | 37 | 24.5 | 6 × 5 | 43, 29.5 | emprise | sprite Ocre |
| lt_prop0 | lt_tuyau | 18.5 | 13 | 3 × 2 | 21.5, 15 | emprise | sprite Ocre |
| lt_prop1 | lt_tuyau | 33 | 13 | 3 × 2 | 36, 15 | emprise | sprite Ocre |
| lt_prop2 | lt_sodium | 9.6 | 14.8 | 0.8 × 0.8 | 10.4, 15.6 | emprise | sprite Ocre |
| lt_prop3 | lt_sodium | 25.6 | 15.6 | 0.8 × 0.8 | 26.4, 16.4 | emprise | sprite Ocre |
| lt_prop4 | lt_sodium | 39.6 | 20.6 | 0.8 × 0.8 | 40.4, 21.4 | emprise | sprite Ocre |
| lt_prop5 | lt_sodium | 20.6 | 28.2 | 0.8 × 0.8 | 21.4, 29 | emprise | sprite Ocre |
| lt_prop6 | lt_horloge_pointage | 24 | 20.9 | 1 × 1 | 25, 21.9 | emprise | sprite Ocre |
| lt_prop7 | lt_voiture_panne | 30 | 19.4 | 4 × 2 | 34, 21.4 | emprise | sprite Ocre |
| lt_prop8 | lt_voiture_panne | 1.5 | 32.5 | 4 × 2 | 5.5, 34.5 | emprise | sprite Ocre |
| lt_prop9 | lt_bidons | 33.3 | 15.4 | 0.6 × 0.6 | 33.9, 16 | emprise | sprite Ocre |
| lt_prop10 | lt_bidons | 34.1 | 15.6 | 0.6 × 0.6 | 34.7, 16.2 | emprise | sprite Ocre |
| lt_prop11 | lt_ferraille | 44.6 | 13.4 | 1.5 × 1 | 46.1, 14.4 | emprise | sprite Ocre |
| lt_prop12 | lt_palettes | 46.5 | 11 | 1 × 1 | 47.5, 12 | emprise | sprite Ocre |
| lt_prop13 | lt_palettes | 17.6 | 30 | 1 × 1 | 18.6, 31 | emprise | sprite Ocre |
| lt_prop14 | lt_grille_fosse | 44.5 | 33.6 | 2 × 2 | 46.5, 35.6 | aucune | sprite Ocre |
| lt_prop15 | lt_flaque | 11 | 20.6 | 2.5 × 1.5 | 13.5, 22.1 | aucune | sprite Ocre |
| lt_prop16 | lt_flaque | 34 | 21.6 | 2.5 × 1.5 | 36.5, 23.1 | aucune | sprite Ocre |
| lt_prop17 | lt_tuyau_coude | 32.5 | 3 | 2.5 × 2.5 | 35, 5.5 | emprise | sprite Ocre |
| lt_prop18 | lt_passerelle | 23.4 | 2.5 | 1.5 × 6 | 24.9, 8.5 | emprise | sprite Ocre |
| lt_foyer | lt_foyer_ruiz | 3 | 24 | 10 × 7 | 13, 31 | emprise | sprite Ocre |
| lt_portique | lt_portique_io | 1.5 | 13.5 | 7 × 2.5 | 8.5, 16 | emprise | sprite Ocre |

## Portes et jonctions
| id | ouverture (x, z) | seuil | vers |
|---|---|---|---|
| l_ouest (steel_lower) | 0, 18 | 1, 18 | c_est |
| l_fosse (steel_lower) | 42, 36 | 42, 35 | v_fosse |
| v_fosse (sv_poutres) | 18, 28 | 18, 27 | l_fosse |
| l_sud (steel_lower) | 8, 36 | 8, 35 | fermé (bord) |
| l_sud_est (steel_lower) | 30, 36 | 30, 35 | fermé (bord) |
| lt_foyer_door (steel_lower) | 9.5, 31 | 9.5, 32 | foyer_in_door |
| foyer_in_door (foyer_in) | 6, 9 | 6, 8 | lt_foyer_door |
| lt_bastide_door (steel_lower) | 40.5, 13 | 40.5, 14 | bastide_in_door |
| bastide_in_door (bastide_in) | 5, 8 | 5, 7 | lt_bastide_door |
| lt_moss_door (steel_lower) | 41, 29.5 | 41, 30.5 | moss_in_door |
| moss_in_door (moss_in) | 5, 8 | 5, 7 | lt_moss_door |
| lt_usine7_door (steel_lower) | 28.5, 15 | 28.5, 16 | pointage_in_door |
| pointage_in_door (pointage_in) | 5, 8 | 5, 7 | lt_usine7_door |

## PNJ
| id | lieu | x | z | sprite (provisoire) |
|---|---|---|---|---|
| Mère Ruiz | foyer_in | 3 | 2 | gen_vera |
| Pia | steel_lower | 14.4 | 25.5 | gen_sv_guetteuse |
| Joaquim Bastide | bastide_in | 7 | 2 | gen_ezequiel |
| Moss | moss_in | 5 | 2 | gen_sv_receleur |
| Ilse Raack | pointage_in | 5 | 2 | gen_odile |
| Agent Dorn | steel_lower | 20 | 18 | gen_halloran |
