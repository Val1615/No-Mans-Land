# Asia-Ground — positions (lot 2, zone `steel_asia`, 48 x 36 m)

Généré depuis `src/data/asia_ground.js`. Fiches : ASIA_GROUND.md, PLAN_IMPLEMENTATION.md §2. Sprites Ocre 99f6759 (inchangés), emprises = `footprint_m` du manifeste, pivot au coin avant (x+w, z+d).

## Bâtiments et stands

| id | nom | sprite | x | z | w | d | visitable | parties pleines |
|---|---|---|---|---|---|---|---|---|
| ag_lin | Chez Lin 林记 | ag_restaurant | 13 | 0.5 | 8 | 6 |  | emprise |
| ag_resto2 | — | ag_restaurant_b | 23 | 0.5 | 8 | 6 |  | emprise |
| ag_escalier | — | ag_escalier | 39 | 0 | 8 | 14 |  | 2 blocs |
| ag_halle0 | — | ag_halle_module | 12 | 10 | 8 | 16 |  | 4 blocs |
| ag_halle1 | Marché couvert | ag_halle_module | 20 | 10 | 8 | 16 |  | 4 blocs |
| ag_halle2 | — | ag_halle_module | 28 | 10 | 8 | 16 |  | 4 blocs |
| ag_lau | Pharmacie Lau | ag_boutique | 2 | 13 | 6 | 5 | oui | emprise |
| ag_okafor | Électronique Okafor | ag_boutique_b | 2 | 23 | 6 | 5 | oui | emprise |
| ag_bureau | Bureau des Emplacements | ag_bureau | 39 | 18 | 6 | 5 | oui | emprise |
| ag_monte_charge | — | ag_monte_charge | 42 | 28 | 4 | 4 |  | emprise |
| ag_mei | Les Nouilles de Mei | ag_stand_nouilles | 14 | 12 | 2.5 | 1.5 |  | emprise |
| ag_p0 | — | ag_stand_poisson | 20.5 | 14 | 3.5 | 3 |  | emprise |
| ag_p1 | — | ag_stand_pieces | 29 | 14.5 | 4 | 2 |  | emprise |
| ag_p2 | — | ag_stand_poisson | 22 | 20.5 | 3.5 | 3 |  | emprise |
| ag_p3 | — | ag_stand_nouilles | 30 | 20.5 | 2.5 | 1.5 |  | emprise |
| ag_barrage0 | — | ag_caisses_legumes | 21.5 | 33.6 | 1.2 | 0.8 |  | emprise |
| ag_barrage1 | — | ag_caisses_legumes | 23 | 34 | 1.2 | 0.8 |  | emprise |
| ag_barrage2 | — | ag_caisses_legumes | 25.4 | 33.8 | 1.2 | 0.8 |  | emprise |

## Props

| id | sprite | x | z | w | d |
|---|---|---|---|---|---|
| ag_prop0 | ag_wok | 17 | 12.2 | 1 | 1 |
| ag_prop1 | ag_caisses_legumes | 18.6 | 18.4 | 1.2 | 0.8 |
| ag_prop2 | ag_caisses_legumes | 26.5 | 18.6 | 1.2 | 0.8 |
| ag_prop3 | ag_glaciere | 24.4 | 14.6 | 1 | 0.6 |
| ag_prop4 | ag_glaciere | 33.6 | 22 | 1 | 0.6 |
| ag_prop5 | ag_chariot | 38 | 30.6 | 1.8 | 0.9 |
| ag_prop6 | ag_chariot | 9.5 | 31 | 1.8 | 0.9 |
| ag_prop7 | ag_caisses_legumes | 40.4 | 32.4 | 1.2 | 0.8 |
| ag_prop8 | ag_auvent | 2.5 | 18.2 | 5 | 2.5 |
| ag_prop9 | ag_hautparleur_io | 35.4 | 8.6 | 0.6 | 0.6 |
| ag_prop10 | ag_neon_io | 22.4 | 9.4 | 1.2 | 0.3 |
| ag_prop11 | ag_lanterne_cable | 13 | 7.2 | 5 | 1 |
| ag_prop12 | ag_lanterne_cable | 24 | 7.2 | 5 | 1 |
| ag_prop13 | ag_lanterne_cable | 31.5 | 7.2 | 5 | 1 |

## Accès et portes

| id | lieu | ouverture | seuil | vers | état |
|---|---|---|---|---|---|
| a_nord | steel_asia | 8, 0 | 8, 1 | l_sud | ouverte |
| a_escalier | steel_asia | 43, 0 | 43, 1 | c_sud_est | ouverte |
| c_sud_est | steel_center | 38, 36 | 38, 35 | a_escalier | ouverte |
| a_sud | steel_asia | 24, 36 | 24, 35 | — | fermée (lot 3/4) |
| ag_lau_door | steel_asia | 5, 18 | 5, 19 | lau_in_door | ouverte |
| lau_in_door | lau_in | 5, 8 | 5, 7 | ag_lau_door | ouverte |
| ag_okafor_door | steel_asia | 5, 28 | 5, 29 | okafor_in_door | ouverte |
| okafor_in_door | okafor_in | 5, 8 | 5, 7 | ag_okafor_door | ouverte |
| ag_bureau_door | steel_asia | 42, 23 | 42, 24 | emplacements_in_door | ouverte |
| emplacements_in_door | emplacements_in | 5, 8 | 5, 7 | ag_bureau_door | ouverte |
| ag_mei_door | steel_asia | 15.25, 13.5 | 15.25, 14.5 | mei_in_door | ouverte |
| mei_in_door | mei_in | 5, 8 | 5, 7 | ag_mei_door | ouverte |

Lower-Town : `l_sud` (8, 36) ↔ `a_nord` ouverte au lot 2, sans condition. `l_sud_est` (China Lake) reste fermée (lot 3).

## PNJ

| id | nom | lieu | x | z | sprite (PROVISOIRE) |
|---|---|---|---|---|---|
| ag_mei | Mei Tran | steel_asia | 15.2 | 11.2 | gen_vera |
| ag_lau | Hana Lau | lau_in | 4 | 2 | gen_odile |
| ag_okafor | Okafor | okafor_in | 6 | 2 | gen_ezequiel |
| ag_seng | Victor Seng | emplacements_in | 5 | 2 | gen_teng |
| ag_kim | Kim Tran | mei_in | 8 | 5 | gen_sv_guetteuse |

## Intérieurs

- `lau_in` Asia-Ground · Pharmacie Lau : 10 x 8 m, sortie sud au milieu, seuil à 1 m.
- `okafor_in` Asia-Ground · Électronique Okafor : 10 x 8 m, sortie sud au milieu, seuil à 1 m.
- `emplacements_in` Asia-Ground · Bureau des Emplacements : 10 x 8 m, sortie sud au milieu, seuil à 1 m.
- `mei_in` Asia-Ground · Arrière du stand de Mei : 10 x 8 m, sortie sud au milieu, seuil à 1 m.

## Points ouverts

- a_nord posé en (8, 0) comme le plan ; la fiche indique (0, 18).
- Repérage +1 sur a_escalier : système absent, non branché.
- a_quai (Cour des Porteurs) : lot 4, non posé. Quête « Le loyer de Mei » non branchée.
- Sprites des PNJ : réemplois provisoires.
