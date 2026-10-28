# China Lake — positions (lot 3, zone `steel_china`, 48 x 36 m)

Généré depuis `src/data/china_lake.js`. Sources : PLAN_IMPLEMENTATION.md §3 et lot 3 (fiche CHINA_LAKE.md perdue), DA d'Ocre (`creation/quartiers`, DA_QUARTIERS.md). Sprites Ocre a301df7 (inchangés), emprises = `footprint_m` du manifeste, pivot au coin avant (x+w, z+d).

Composition [décision Valentin] : marché illégal de contrefaçons ; lac au centre (x 14-34, z 12-26, `ground.water`, non praticable) ; stands sur les quatre quais (nord implants et puces, est armes, sud faux papiers + établi du technicien au bord de l'eau, ouest médicaments) ; bâtiments au fond = bord nord (haut du cadre), trouée du Barrage x 21,5-29,5 ; ruelle de l'angle est (k_est).

Eau : `g_cl_eau` (512 px) non modifié ; répétition cassée dans `paintWater` (textures.js) : décalage UV, seconde couche tournée de 37° et x1,7 en fondu, taches lentes, 9 lanternes flottantes peintes + lueurs rouges.

## Bâtiments et stands

| id | nom | sprite | x | z | w | d | visitable | parties pleines |
|---|---|---|---|---|---|---|---|---|
| cl_pilotis_no | — | cl_pilotis | 0.5 | 0.5 | 6 | 6 |  | emprise |
| cl_dragon | Pavillon du Dragon | cl_immeuble_fond | 8 | 0.5 | 7 | 8 | oui | emprise |
| cl_fond1 | — | cl_immeuble_fond_b | 15.5 | 0.5 | 6 | 8 |  | emprise |
| cl_the | Maison de thé | cl_maison_the | 30 | 0.5 | 10 | 5.5 | oui | emprise |
| cl_fond2 | — | cl_immeuble_fond_b | 41 | 0.5 | 6 | 8 |  | emprise |
| cl_filets | Les Filets | cl_cabane | 40 | 24 | 8 | 2 | oui | emprise |
| cl_pilotis_so | — | cl_pilotis | 0.5 | 29.5 | 6 | 6 |  | emprise |
| cl_ponton | Ponton de Shen | cl_ponton | 9 | 17 | 5 | 3 |  | aucune |
| cl_s_implants | Implants « garantis » | cl_stand_implants | 16 | 10.6 | 2.5 | 1 |  | emprise |
| cl_s_puces | Puces et lecteurs | cl_stand_puces | 19.5 | 10.6 | 2.5 | 1 |  | emprise |
| cl_s_puces2 | — | cl_stand_puces | 27.5 | 10.6 | 2.5 | 1 |  | emprise |
| cl_s_implants2 | — | cl_stand_implants | 31 | 10.6 | 2.5 | 1 |  | emprise |
| cl_s_armes | Armes sans numéro | cl_stand_armes | 37 | 13 | 2.5 | 2 |  | emprise |
| cl_s_armes2 | — | cl_stand_armes | 37 | 17 | 2.5 | 2 |  | emprise |
| cl_s_armes3 | — | cl_stand_armes | 37 | 21 | 2.5 | 2 |  | emprise |
| cl_s_papiers | Faux papiers | cl_stand_papiers | 16 | 28.5 | 2.5 | 1 |  | emprise |
| cl_s_tech | Établi du technicien | cl_stand_implants | 22.75 | 26.6 | 2.5 | 1 |  | emprise |
| cl_s_papiers2 | — | cl_stand_papiers | 28 | 28.5 | 2.5 | 1 |  | emprise |
| cl_s_medocs | Médicaments et stimulants | cl_stand_medocs | 10.5 | 13.6 | 2.5 | 1.5 |  | emprise |
| cl_s_medocs2 | — | cl_stand_medocs | 10.5 | 22.6 | 2.5 | 1.5 |  | emprise |

## Props

| id | sprite | x | z | w | d | plein |
|---|---|---|---|---|---|---|
| cl_cable1 | cl_cable_lanternes | 17 | 14 | 14 | 0.5 | non |
| cl_cable2 | cl_cable_lanternes | 17 | 22 | 14 | 0.5 | non |
| cl_b_dragon | cl_ballon_dragon | 17 | 15.5 | 3 | 1.5 | non |
| cl_b_carpe | cl_ballon_carpe | 28 | 15 | 3 | 1 | non |
| cl_b_tigre | cl_ballon_tigre | 20.5 | 22.8 | 3 | 1.2 | non |
| cl_b_phenix | cl_ballon_phenix | 27.5 | 19 | 3 | 1.5 | non |
| cl_dech_a | cl_dechets_a | 19 | 17.5 | 2 | 2 | non |
| cl_dech_b | cl_dechets_b | 29.5 | 22.5 | 2 | 2 | non |
| cl_dech_c | cl_dechets_c | 15.5 | 23 | 2 | 2 | non |
| cl_pieux0 | cl_pieux | 13.6 | 11.6 | 0.8 | 0.8 | oui |
| cl_pieux1 | cl_pieux_b | 33.6 | 11.6 | 0.8 | 0.8 | oui |
| cl_pieux2 | cl_pieux | 13.6 | 25.6 | 0.8 | 0.8 | oui |
| cl_pieux3 | cl_pieux_b | 33.6 | 25.6 | 0.8 | 0.8 | oui |
| cl_pieux4 | cl_pieux | 24 | 25.6 | 0.8 | 0.8 | oui |
| cl_bache1 | cl_bache | 21.4 | 30.4 | 3 | 3 | non |
| cl_bache2 | cl_bache | 42 | 12.4 | 3 | 3 | non |
| cl_treteaux1 | cl_treteaux | 31.5 | 29.4 | 2 | 0.6 | oui |
| cl_treteaux2 | cl_treteaux | 4 | 14.2 | 2 | 0.6 | oui |
| cl_friture | cl_friture | 22.2 | 9.6 | 1 | 0.7 | oui |
| cl_mahjong | cl_mahjong | 43.6 | 18.4 | 1.6 | 1.6 | oui |
| cl_caisse_armes | cl_caisse_armes | 40.4 | 15.6 | 1.2 | 0.6 | oui |
| cl_bac_puces | cl_bac_puces | 22.6 | 11.4 | 0.6 | 0.4 | oui |
| cl_presse | cl_presse_papiers | 14.2 | 30.8 | 1 | 0.6 | oui |
| cl_bocaux | cl_bocaux | 8.6 | 14.2 | 0.8 | 0.4 | oui |
| cl_barriere | cl_barriere_caisses | 25.8 | 2.4 | 4 | 0.8 | oui |

## Accès et portes

| id | lieu | ouverture | seuil | vers | condition |
|---|---|---|---|---|---|
| k_nord | steel_china | 24, 0 | 24, 1 | a_sud | aucune |
| k_est | steel_china | 48, 32 | 47, 32 | l_sud_est | aucune |
| cl_dragon_door | steel_china | 11.5, 8.5 | 11.5, 9.5 | dragon_in_door | aucune |
| dragon_in_door | dragon_in | 6, 9 | 6, 8 | cl_dragon_door | aucune |
| cl_the_door | steel_china | 35, 6 | 35, 7 | the_in_door | aucune |
| the_in_door | the_in | 6, 9 | 6, 8 | cl_the_door | aucune |
| cl_filets_door | steel_china | 44, 26 | 44, 27 | filets_in_door | aucune |
| filets_in_door | filets_in | 5, 8 | 5, 7 | cl_filets_door | aucune |
| a_sud (Asia-Ground) | steel_asia | 24, 36 | 24, 35 | k_nord | 20 cr payés à Ah-Lam (drapeau `cl_barrage`) |
| l_sud_est (Lower-Town) | steel_lower | 30, 36 | 30, 35 | k_est | aucune : China Lake reste joignable sans argent |

## PNJ

| id | nom | lieu | x | z | sprite (PROVISOIRE) |
|---|---|---|---|---|---|
| cl_shen | Shen | steel_china | 7.6 | 18.6 | gen_sv_receleur |
| cl_m_nord | Marchande d’implants | steel_china | 17.25 | 9.9 | gen_mara |
| cl_m_est | Armurier | steel_china | 38.25 | 12.3 | gen_sv_gang |
| cl_m_sud | Faussaire | steel_china | 19.1 | 28.6 | gen_teng |
| cl_m_ouest | Apothicaire | steel_china | 11.75 | 12.9 | gen_odile |
| cl_tech | Le technicien | steel_china | 24 | 25.900000000000002 | gen_sv_dealer |
| cl_zhou | Madame Zhou | the_in | 6 | 2 | gen_vera |
| cl_main1 | Homme de main | the_in | 2 | 4 | gen_halloran |
| cl_main2 | Homme de main | the_in | 10 | 4 | gen_halloran |
| cl_serveur | Serveur | dragon_in | 2.4 | 3.2 | gen_teo |
| cl_lo | Vieux Lo | dragon_in | 9 | 6 | gen_hector |
| cl_yu | Yu | filets_in | 4 | 3 | gen_sv_guetteuse |
| ag_ahlam | Ah-Lam | steel_asia | 26.4 | 32.2 | gen_sv_gang |

## Intérieurs

- `the_in` China Lake · Maison de thé : 12 x 9 m, sortie sud au milieu, seuil à 1 m.
- `dragon_in` China Lake · Pavillon du Dragon : 12 x 9 m, sortie sud au milieu, seuil à 1 m.
- `filets_in` China Lake · Les Filets : 10 x 8 m, sortie sud au milieu, seuil à 1 m.

## Écarts et points ouverts

- Bâtiments du fond au bord nord (haut du cadre) : les portes s'ouvrent au sud, un bâtiment au bord sud n'aurait pas de porte praticable. La maison de thé est donc au nord-est (x 30-40) et non sur l'axe x 24 (qui est la trouée du Barrage) ; elle reste visible depuis le Barrage.
- Ah-Lam est côté Asia-Ground (il encaisse avant le passage), pas à x 27, z 2 de China Lake comme le plan.
- l_sud_est ↔ k_est libre dans les deux sens (le plan prévoyait « après une première visite ») : c'est la route sans argent.
- Stands : marchands figurants derrière l'étal (côté nord) ; le faussaire est au bout de son étal (le sprite masquait le tap).
- Sans objet : achats des stands, lecture de puce chez Shen, cache des Filets, salle de jeu du Pavillon, bureau de Zhou (lot 4, quêtes).
- Sprites des PNJ : réemplois provisoires.
