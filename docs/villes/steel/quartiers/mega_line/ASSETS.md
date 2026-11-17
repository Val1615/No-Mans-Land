# Mega-Line : assets

Mêmes conventions que `dome_frequence/ASSETS.md`. 50 px par mètre pour les décors, PNJ en 180 x 512 avec pivot bas-centre, portraits 192 x 192 sur fond (58,44,32). Préfixes `g_ml_`, `ml_`, `ml_ens_`, `gen_ml_`, `portrait-gen_ml_`. Index : `assets/steel/mega_line/manifest.json`, chemins relatifs à `assets/`. Le champ `partie` dit si l'asset sert à la ligne ou au terminus.

Tous les fichiers sont en status v1, générés (GenerateImage, fond vert retiré) ou procéduraux (PIL). Les écrans de quai reprennent les écrans de scène du Dôme, faits d'après `nml-shots/refs`. Chaque planche animée a sa version `_mobile` à mi-résolution.

## La ligne
| fichier | px | note |
|---|---|---|
| `g_ml_pave.webp` | 512 x 512 | tuile 4.0 m |
| `g_ml_quai.webp` | 512 x 512 | tuile 4.0 m |
| `gen_ml_controleuse.webp` | 180 x 512 | footprint [0.6, 0.6] m, 1.66 m |
| `gen_ml_entretien.webp` | 180 x 512 | footprint [0.6, 0.6] m, 1.72 m |
| `gen_ml_etudiante.webp` | 180 x 512 | footprint [0.6, 0.6] m, 1.6 m |
| `gen_ml_fan.webp` | 180 x 512 | footprint [0.6, 0.6] m, 1.64 m |
| `gen_ml_navetteur.webp` | 180 x 512 | footprint [0.6, 0.6] m, 1.76 m |
| `gen_ml_nouilles.webp` | 180 x 512 | footprint [0.6, 0.6] m, 1.58 m |
| `gen_ml_pancarte.webp` | 180 x 512 | footprint [0.6, 0.6] m, 1.74 m |
| `gen_ml_vigile.webp` | 180 x 512 | footprint [0.6, 0.6] m, 1.92 m |
| `ml_banc.webp` | 140 x 90 | footprint [2, 0.6] m, 0.9 m |
| `ml_borne.webp` | 80 x 150 | footprint [0.8, 0.6] m, 1.8 m |
| `ml_ens_ecran_tron.webp` | 1024 x 144 | 4 images de 256 x 144, 3 i/s, écran de quai, Tron (réf. pp_holo_tron_src), glitch |
| `ml_ens_ecran_tron_mobile.webp` | 512 x 72 | 4 images de 128 x 72, 3 i/s, écran de quai, Tron (réf. pp_holo_tron_src), glitch |
| `ml_ens_ecran_vibes.webp` | 1024 x 144 | 4 images de 256 x 144, 2 i/s, écran de quai, Vibes en concert (réf. pp_billboard_src) |
| `ml_ens_ecran_vibes_mobile.webp` | 512 x 72 | 4 images de 128 x 72, 2 i/s, écran de quai, Vibes en concert (réf. pp_billboard_src) |
| `ml_ens_horaires.webp` | 384 x 80 | 3 images de 128 x 80, 1 i/s, tableau des départs en pictogrammes (aucun texte), une ligne change à chaque image |
| `ml_ens_horaires_mobile.webp` | 192 x 40 | 3 images de 64 x 40, 1 i/s, tableau des départs en pictogrammes (aucun texte), une ligne change à chaque image |
| `ml_ens_human_corp.webp` | 384 x 128 | 3 images de 128 x 128, 1.5 i/s, logo abstrait Human Corp qui respire, en façade sous le viaduc |
| `ml_ens_human_corp_mobile.webp` | 192 x 64 | 3 images de 64 x 64, 1.5 i/s, logo abstrait Human Corp qui respire, en façade sous le viaduc |
| `ml_lampadaire.webp` | 80 x 300 | footprint [0.6, 0.6] m, 6 m |
| `ml_poubelle.webp` | 50 x 70 | footprint [0.6, 0.6] m, 1 m |
| `ml_rame.webp` | 1200 x 680 | footprint [24, 3] m, 3.6 m, déplacée par le code le long du viaduc |
| `ml_station.webp` | 1100 x 820 | footprint [20, 6] m, 7 m, deux cadres d’écran éteints sur le quai, écrans posés par le code |
| `ml_tableau.webp` | 160 x 180 | footprint [2.4, 0.4] m, 3 m |
| `ml_viaduc.webp` | 1200 x 900 | footprint [24, 3] m, 6 m |
| `portrait-gen_ml_controleuse.webp` | 192 x 192 | footprint None m,  m |
| `portrait-gen_ml_entretien.webp` | 192 x 192 | footprint None m,  m |
| `portrait-gen_ml_etudiante.webp` | 192 x 192 | footprint None m,  m |
| `portrait-gen_ml_fan.webp` | 192 x 192 | footprint None m,  m |
| `portrait-gen_ml_navetteur.webp` | 192 x 192 | footprint None m,  m |
| `portrait-gen_ml_nouilles.webp` | 192 x 192 | footprint None m,  m |
| `portrait-gen_ml_pancarte.webp` | 192 x 192 | footprint None m,  m |
| `portrait-gen_ml_vigile.webp` | 192 x 192 | footprint None m,  m |

## Le terminus [décision Valentin]
Aucun sable ni ciel dans ces sprites. Les portes du sas sont pleines, sans hublot ni lumière venue de dehors ; leurs petites lampes peintes ont été éteintes, le clignotement vient de `ml_ens_sas`. Le panneau est vierge, la phrase « Dernier arrêt avant No Man's Land » est affichée par le code.

| fichier | px | note |
|---|---|---|
| `g_ml_fret.webp` | 512 x 512 | tuile 4.0 m |
| `gen_ml_cheffe_fret.webp` | 180 x 512 | footprint [0.6, 0.6] m, 1.68 m |
| `gen_ml_docker.webp` | 180 x 512 | footprint [0.6, 0.6] m, 1.86 m |
| `gen_ml_foule_a.webp` | 180 x 512 | footprint [0.6, 0.6] m, 1.76 m |
| `gen_ml_foule_b.webp` | 180 x 512 | footprint [0.6, 0.6] m, 1.66 m |
| `ml_bureau_fret.webp` | 300 x 260 | footprint [5, 4] m, 4 m |
| `ml_conteneurs.webp` | 280 x 220 | footprint [6, 2.5] m, 5.2 m |
| `ml_ens_gyrophare.webp` | 256 x 64 | 4 images de 64 x 64, 4 i/s, gyrophare orange de la gare de fret, x 2 regroupés |
| `ml_ens_gyrophare_mobile.webp` | 128 x 32 | 4 images de 32 x 32, 4 i/s, gyrophare orange de la gare de fret, x 2 regroupés |
| `ml_ens_sas.webp` | 1024 x 64 | 4 images de 256 x 64, 2 i/s, deux lampes d’alerte du sas qui clignotent en alternance, posées sur l’encadrement |
| `ml_ens_sas_mobile.webp` | 512 x 32 | 4 images de 128 x 32, 2 i/s, deux lampes d’alerte du sas qui clignotent en alternance, posées sur l’encadrement |
| `ml_panneau_terminus.webp` | 200 x 150 | footprint [3, 0.5] m, 3 m, panneau vierge, phrase affichée par le code |
| `ml_portique.webp` | 320 x 300 | footprint [7, 4] m, 7 m |
| `ml_sas.webp` | 1000 x 750 | footprint [18, 2] m, 12 m, portes pleines, sans ouverture ni hublot ; ni ciel ni sable ; lampes éteintes, clignotement par ml_ens_sas |
| `portrait-gen_ml_cheffe_fret.webp` | 192 x 192 | footprint None m,  m |
| `portrait-gen_ml_docker.webp` | 192 x 192 | footprint None m,  m |

## Poids et planche
50 fichiers au total. Planches animées : environ 52 Ko en version ordinateur, 24 Ko en version mobile. Planche d'aperçu : `/workspace/nml-shots/mega_line_sprites.png`.

## Portique à implant, Pique-Puce et vendeur
| fichier | px | ancre | note |
|---|---|---|---|
| `ml_portique_implant.webp` | 110 x 110 | [71, 109] | footprint 1,6 x 1 m, 1,3 m, éteint |
| `ml_ens_portique_accepte.webp` | 660 x 110 | [71, 109] | 6 images de 110 x 110, 10 i/s, non bouclée, jouée au passage |
| `ml_ens_portique_accepte_mobile.webp` | 330 x 55 | [35, 54] | mi-résolution |
| `ml_ens_portique_refuse.webp` | 440 x 110 | [71, 109] | 4 images de 110 x 110, 12 i/s, non bouclée, jouée au passage |
| `ml_ens_portique_refuse_mobile.webp` | 220 x 55 | [35, 54] | mi-résolution |
| `icone_pique_puce_128.webp` | 128 x 128 | sans objet | icône d'inventaire |
| `icone_pique_puce_64.webp` | 64 x 64 | sans objet | icône d'inventaire |
| `gen_ml_fusible.webp` | 180 x 512 | [90, 511] | vendeur, 1,72 m, Fréquence Strip |
| `portrait-gen_ml_fusible.webp` | 192 x 192 | sans objet | portrait |

Les planches du portique ont la même taille et la même ancre que le sprite de base : le code les met à sa place le temps du passage. Les lumières n'existent que dans les planches, le sprite de base est éteint. Planche d'aperçu : `/workspace/nml-shots/megaline_implant.png`.

## Mega-Line v2 — lot 1 : structure de la ligne (Ocre, 2026-11-17)

Clés de `MEGALINE_V2_IMPL.md` (lot 1), plus `ml_rame_3v_dos_v2_3q` (vue dos) et les couches `_avant` du viaduc. Toutes les autres clés de `assets/steel/mega_line/manifest.json` sont intactes.

**Méthode (identique au bus v5 de Center-Town).** Chaque pièce est d'abord un modèle 3D aux cotes ci-dessous, rendu à la caméra exacte du jeu (lacet 34,5°, tangage 28,8°, projection parallèle, 50 px/m). Ce rendu verrouille la silhouette, les arêtes et l'alpha. La matière est ensuite repeinte par génération image-à-image, recalée par une échelle uniforme et une translation (IoU 0,87 à 0,99). Il y a une seule réduction et jamais d'agrandissement. Les grandes pièces (viaduc de 24 m, tablier du quai) sont repeintes par tuiles, raccordées par un fondu. Pentes au pied mesurées : 0,329 à 0,333 et 0,688 à 0,714, pour une cible de 0,33 / 0,70. Aucun texte généré : le seul lettrage, « MEGA-LINE », est en PIL sur un calque.

**Ancre.** Coin avant sud-est de l'emprise (x+w, z+d), au sol. Pour la rame, la barrière et le cadre d'écran, l'ancre est à « base y » (champ `base_y_m`).

| clé | px | ancre | emprise × h (m) | base y | calques | rôle |
|---|---|---|---|---|---|---|
| `ml_viaduc_pile_v2_3q` | 152 × 339 | [86, 326] | 1,6 × 1,6 × 6 | 0 | — | Pile de fer rivetée avec socle béton de 2 × 2 m (débord de 0,2 m) et chapiteau de 1,8 m. |
| `ml_viaduc_seg24_v2_3q` | 1125 × 745 | [1003, 741] | 24 × 4 × 7,45 | 0 (sans piles) | `_neon`, `_avant` | Auge rivetée, traverses, deux rails, chemin de câbles, feux de balisage ambre. Sous-poutre à 6,0, rails à 6,8. |
| `ml_viaduc_seg16_v2_3q` | 796 × 636 | [674, 632] | 16 × 4 × 7,45 | 0 | `_neon`, `_avant` | Même tablier, segment est. |
| `ml_rame_3v_v2_3q` | 1251 × 621 | [1160, 614] (miroir [91, 614]) | 28 × 3 × 3,6 | 6,8 | `_fenetres`, `_neon`, `_texte`, `_texte_miroir` | Rame violette à 3 voitures, fenêtres ambre avec voyageurs. Vue avant : phares blancs côté +x. |
| `ml_rame_3v_dos_v2_3q` | 1251 × 621 | [1160, 614] (miroir [91, 614]) | 28 × 3 × 3,6 | 6,8 | idem | Même rame en vue dos : feux rouges côté +x, la rame roule vers −x. |
| `ml_quai_tablier_v2_3q` | 1394 × 863 | [1161, 856] | 28 × 8 × 7,1 | 0 (plancher +6,0) | — | Dalle de 0,6 m, poteaux de galerie, tôle striée, ligne jaune à z15,2, garde-corps O / E / S avec trémies. |
| `ml_quai_barriere_v2_3q` | 535 × 235 | [521, 231] | 12,6 × 0,3 × 1,1 | 6,0 | `_neon` (filet ambre) | Barrière de verre dépoli à 42 % d'opacité. |
| `ml_escalier_v2_3q` | 419 × 563 | [130, 553] | 3 × 10 × 7 | 0 | — | Escalier droit perpendiculaire au quai : palier haut z22–23, 36 marches jusqu'à z32. |
| `ml_ecran_cadre_v2_3q` | 248 × 437 | [229, 433] | 5,4 × 0,4 × 7,6 | 6,0 | — | Cadre d'écran VIERGE suspendu au flanc sud du viaduc. Dalle de 5,12 × 2,88 m entre +10,5 et +13,38. |

**Poses.** Appel `B(...)` de `src/data/mega_line.js` ; `base_y` est à câbler côté rendu. Ordre de dessin, de l'arrière vers l'avant : piles → segments de viaduc → rame (+ `_texte`) → couches `_avant` du viaduc → tablier du quai → cadres d'écran → barrières → escaliers.
```js
// piles : AVANT le tablier du viaduc (le tablier couvre leur chapiteau)
...[2, 14, 26, 38, 50, 62].map((cx, i) => B('ml_v_pile' + i, '', 'ml_viaduc_pile_v2_3q', cx - 0.8, 11.2, 1.6, 1.6, { solid: [{ x: cx - 0.8, z: 11.2, w: 1.6, d: 1.6 }] })),
B('ml_v_seg0', '', 'ml_viaduc_seg24_v2_3q',  0, 10, 24, 4),     // aucun solide : on passe sous le viaduc
B('ml_v_seg1', '', 'ml_viaduc_seg24_v2_3q', 24, 10, 24, 4),
B('ml_v_seg2', '', 'ml_viaduc_seg16_v2_3q', 48, 10, 16, 4),
// rame : base_y 6,8, z10,5–13,5, coulisse le long de x ; puis la couche ml_viaduc_seg*_v2_3q_avant de chaque segment
// (poutre sud, à la même place que le segment) pour masquer les bogies : 0,65 m sous le haut de la poutre
B('ml_quai', '', 'ml_quai_tablier_v2_3q', 18, 14, 28, 8, { floor_y: 6, solid: [/* poteaux 0,36 × 0,36 à z21,52 aux x18,2 22 26 30 34 38 42 45,8 */] }),
B('ml_ecran_vibes', '', 'ml_ecran_cadre_v2_3q', 19.8, 14, 5.4, 0.4, { base_y: 6, solid: [{ x: 19.8, z: 14, w: 0.3, d: 0.2 }, { x: 24.9, z: 14, w: 0.3, d: 0.2 }] }),
B('ml_ecran_tron',  '', 'ml_ecran_cadre_v2_3q', 36.8, 14, 5.4, 0.4, { base_y: 6, solid: [{ x: 36.8, z: 14, w: 0.3, d: 0.2 }, { x: 41.9, z: 14, w: 0.3, d: 0.2 }] }),
B('ml_barr_o', '', 'ml_quai_barriere_v2_3q', 18.4, 17.35, 12.6, 0.3, { base_y: 6, solid: [{ x: 18.4, z: 17.4, w: 12.6, d: 0.2 }] }),
B('ml_barr_e', '', 'ml_quai_barriere_v2_3q', 32.6, 17.35, 12.6, 0.3, { base_y: 6, solid: [{ x: 32.6, z: 17.4, w: 12.6, d: 0.2 }] }),
B('ml_esc_o', '', 'ml_escalier_v2_3q', 18, 22, 3, 10, { solid: [{ x: 18, z: 22, w: 0.15, d: 10 }, { x: 20.85, z: 22, w: 0.15, d: 10 }] }),
B('ml_esc_e', '', 'ml_escalier_v2_3q', 43, 22, 3, 10, { solid: [{ x: 43, z: 22, w: 0.15, d: 10 }, { x: 45.85, z: 22, w: 0.15, d: 10 }] }),
// hauteur dans l'escalier : y = 6 sur z22–23, puis y = 6 × (32 − z) / 9 ; plancher du quai à 6,0 sur x18–46, z14–22 (trémies x18–21 et x43–46 côté sud)
```

**Rame : orientations (règle des véhicules de Center-Town).** Les caisses ne portent aucun lettrage ; seule la girouette du nez porte « MEGA-LINE ».

| sens de marche | sprite | calque texte |
|---|---|---|
| +x | `ml_rame_3v_v2_3q`, vue native | `_texte` |
| −x | `ml_rame_3v_dos_v2_3q`, vue native | `_texte` |
| +z | miroir horizontal de l'avant, ancre miroir [91, 614] | `_texte_miroir`, jamais retourné |
| −z | miroir horizontal du dos, même ancre miroir | `_texte_miroir`, jamais retourné |

Au terminus, la rame arrive par le sud, tête au nord : c'est le cas −z. Les calques `_fenetres` et `_neon` sont retournés avec la caisse.

**Écran : poser l'image.** La dalle de l'écran est vue de biais (face sud, pente 0,33). Sa position dans le sprite est donnée par `ecran.quad_px` du manifeste : haut-gauche [12,3, 37,9], haut-droit [223,2, 107,7], bas-droit [223,2, 233,9], bas-gauche [12,3, 164,1]. `ecran.affine_256x144` = [0,82383, 0,27266, 0, 0,87639, 12,3, 37,9], relative au coin haut-gauche du sprite. Pour poser l'image (`ml_ens_ecran_vibes` / `_tron`, 256 × 144) : `ctx.setTransform(a, b, c, d, X0 + e, Y0 + f)`, où X0, Y0 est le coin haut-gauche du sprite à l'écran. Pour les planches `_mobile` (128 × 72), multiplier a à d par 2.

**Écarts avec MEGALINE_V2_IMPL.md (la fiche de poses gagne).**
- Cadre d'écran : z14–14,4 (et non 13,6–14, qui est dans la poutre du viaduc), largeur 5,4, base y 6,0, mâts montant depuis le quai. La dalle, entre +10,5 et +13,38, passe au-dessus du toit de la rame (+10,4) et ne la masque jamais. Poses : x19,8–25,2 et x36,8–42,2.
- Rame : 3 voitures de 9,6 + 8,8 + 9,6 m, caisse de 2,8 m dans l'emprise de 3 m. La vue dos est livrée sous une clé de plus, `ml_rame_3v_dos_v2_3q`.
- Pile : emprise solide de 1,6 × 1,6 conservée ; le socle visuel déborde de 0,2 m, le chapiteau de 0,1 m.
- Viaduc : nouvelles couches `_avant` (poutre sud) pour que la rame paraisse DANS l'auge, et non posée dessus.

**Défauts connus.**
- Les nez de marche de l'escalier sont repeints en ambre très lumineux : de jour, ils paraissent éclairés.
- Le pied ouest de l'escalier manquait au brut ; il vient du rendu procédural, un peu plus lisse (IoU 0,87).
- La barrière est entièrement procédurale (pièce trop fine pour le générateur).
- Sous le viaduc, rien n'est encore posé : sol et rez arrivent au lot 2.

Planche contact : `/workspace/nml-shots/megaline_sprites/lot1_planche_contact.png`. Maquettes de pose : `/workspace/nml-shots/megaline_sprites/lot1_maquette_pose.png` et `lot1_maquette_nuit.png`. Ces trois images sont hors jeu.

## Mega-Line v2 — lot 2 : rez et bâti (Ocre, 2026-11-17)

Ce lot reprend les clés de `MEGALINE_V2_IMPL.md` (lot 2) avec la même méthode que le lot 1 : modèle 3D aux cotes, rendu à la caméra du jeu qui verrouille l'alpha, repeint image-à-image et recalé (IoU de 0,94 à 0,999), une seule réduction. Les cinq immeubles sont repeints en 4 tuiles chacun. Pentes au pied mesurées entre 0,32 et 0,34 et entre 0,69 et 0,70 (la terrasse n'a pas de pied rectiligne). Calques `_fenetres` / `_neon` : masque géométrique des vitres allumées et des lampes du modèle, à la couleur du sprite. Il n'y a aucun halo sans source. Toutes les enseignes sont vierges et le caisson Human Corp est noir. Aucune clé existante n'a été modifiée.

| clé | px | ancre | emprise × h (m) | calques | rôle |
|---|---|---|---|---|---|
| `ml_echoppe_tran_v2_3q` | 465 × 454 | [289, 444] | 6 × 6 × 5,4 | `_fenetres`, `_neon` | Nouilles de Mme Tran : comptoir, tabourets, marmites, auvent rouge, 4 lanternes rouges |
| `ml_echoppe_cables_v2_3q` | 430 × 463 | [253, 444] | 6 × 6 × 5,4 | idem | Câbles et réparations : rideau à mi-hauteur, bobines, écran de test |
| `ml_facade_humancorp_v2_3q` | 512 × 481 | [336, 471] | 8 × 6 × 5,4 | idem | Bardage bleu nuit, filets LED froids, vitrine blanche, caisson de logo noir |
| `ml_atelier_rivet_v2_3q` | 512 × 484 | [336, 471] | 8 × 6 × 5,4 | idem | Établi, étau, outils, bouteilles de soudure, caisses ; flanc est avec une fenêtre |
| `ml_bati_n1_v2_3q` | 1253 × 1047 | [1011, 1040] | 24 × 8 × 12 | idem | Brique, 3 niveaux, escalier de secours, rez de boutiques |
| `ml_bati_n2_v2_3q` | 1078 × 1146 | [836, 1139] | 20 × 8 × 16 | idem | Enduit ocre-gris, 4 niveaux plus un édicule, escalier de secours |
| `ml_bati_n3_v2_3q` | 923 × 848 | [681, 841] | 16 × 8 × 10 | idem | Béton brut à pilastres, 3 niveaux |
| `ml_passerelle_nord_v2_3q` | 404 × 392 | [171, 386] | 4 × 8 × 4 | `_neon` | Passage de service couvert vers le terminus, passage libre de 3,4 m |
| `ml_bati_w_v2_3q` | 990 × 1033 | [434, 1026] | 10 × 18 × 12 | `_fenetres`, `_neon` | Brique d'angle ; rez actif au sud ET à l'est, sur la rue latérale |
| `ml_bati_e_v2_3q` | 959 × 971 | [434, 963] | 10 × 18 × 10 | idem | Enduit, face sud soignée ; escalier de secours sur la face est |
| `ml_terrasse_v2_3q` | 106 × 89 | [66, 85] | 2 × 2 × 1 | `_neon` (photophore) | Guéridon et deux tabourets |
| `ml_ruelle_benne_v2_3q` | 129 × 118 | [88, 114] | 2 × 1,2 × 1,4 | — | Benne verte, sacs noirs |
| `ml_ruelle_caisses_v2_3q` | 107 × 106 | [72, 100] | 1,6 × 1,2 × 1,2 | — | Trois caisses cerclées |

**Poses** (`B(...)`, ancre au sol au coin sud-est). Ordre de dessin, à intégrer à celui du lot 1 :
1. bâti nord N1 / N2 / passerelle / N3 ;
2. benne et caisses de la ruelle ;
3. piles, viaduc, rame, couches `_avant` ;
4. échoppes, toujours **avant** le tablier du quai, qui couvre leur dessus à +5,4 ;
5. tablier, écrans, barrières ;
6. bâti W et E ;
7. escaliers ;
8. terrasses.
```js
B('ml_n1', '', 'ml_bati_n1_v2_3q',  0, 0, 24, 8, { solid: [{ x: 0,  z: 0, w: 24, d: 8 }] }),
B('ml_n2', '', 'ml_bati_n2_v2_3q', 24, 0, 20, 8, { solid: [{ x: 24, z: 0, w: 20, d: 8 }] }),
B('ml_pass_n', '', 'ml_passerelle_nord_v2_3q', 44, 0, 4, 8, { solid: [{ x: 44, z: 0, w: 0.3, d: 8 }, { x: 47.7, z: 0, w: 0.3, d: 8 }, { x: 44.2, z: 6.4, w: 0.4, d: 0.6 }] }),  // libre x44,3–47,7, sortie au bord nord
B('ml_n3', '', 'ml_bati_n3_v2_3q', 48, 0, 16, 8, { solid: [{ x: 48, z: 0, w: 16, d: 8 }] }),
B('ml_benne0', '', 'ml_ruelle_benne_v2_3q', 3, 8.4, 2, 1.2, { solid: [{ x: 3, z: 8.4, w: 2, d: 1.2 }] }),              // 2e pose (37, 8.4)
B('ml_caisses0', '', 'ml_ruelle_caisses_v2_3q', 5.6, 8.6, 1.6, 1.2, { solid: [{ x: 5.6, z: 8.6, w: 1.6, d: 1.2 }] }), // aussi (52, 8.6), (16.5, 30.5)
B('ml_ech_tran',   '', 'ml_echoppe_tran_v2_3q',   18, 14, 6, 6, { solid: [{ x: 18, z: 14, w: 6, d: 6.5 }] }),
B('ml_ech_cables', '', 'ml_echoppe_cables_v2_3q', 24, 14, 6, 6, { solid: [{ x: 24, z: 14, w: 6, d: 6.5 }] }),
B('ml_hc',         '', 'ml_facade_humancorp_v2_3q', 30, 14, 8, 6, { solid: [{ x: 30, z: 14, w: 8, d: 6.6 }] }),
B('ml_atelier',    '', 'ml_atelier_rivet_v2_3q',  38, 14, 8, 6, { solid: [{ x: 38, z: 14, w: 8, d: 6.6 }] }),   // ml_cafe_froid sur l'établi : x≈39,8, z≈20,1, base y 0,98
B('ml_bw', '', 'ml_bati_w_v2_3q',  0, 14, 10, 18, { solid: [{ x: 0,  z: 14, w: 10, d: 18 }] }),
B('ml_be', '', 'ml_bati_e_v2_3q', 54, 14, 10, 18, { solid: [{ x: 54, z: 14, w: 10, d: 18 }] }),
...[[22, 24], [26, 27.5], [30, 24], [34, 28], [37.5, 24], [40.5, 28]].map(([x, z], i) =>
  B('ml_ter' + i, '', 'ml_terrasse_v2_3q', x, z, 2, 2, { solid: [{ x: x + 0.6, z: z + 0.6, w: 0.8, d: 0.8 }] })),
```
**Logo Human Corp.** Le caisson noir de la façade est vierge. Le champ `logo` du manifeste donne `quad_px` : haut-gauche [226,3, 237,8], haut-droit [333,4, 273,3], bas-droit [333,4, 388,1], bas-gauche [226,3, 352,6]. Il donne aussi `affine_128x128` = [0,83672, 0,27734, 0, 0,89688, 226,3, 237,8]. Pour poser une image de `ml_ens_human_corp` (128 × 128) : `ctx.setTransform(a, b, c, d, X0 + e, Y0 + f)`, où X0, Y0 est le coin haut-gauche du sprite. Pour la planche `_mobile`, multiplier a à d par 2.

**Défauts connus.**
- Les toits des échoppes sont sombres et sans détail : ils restent cachés sous le tablier.
- La façade Human Corp est volontairement lisse et froide. Elle tranche avec la rouille environnante, mais paraît un peu plus « rendu 3D » que ses voisines.
- La passerelle nord : le caillebotis du toit laisse voir des trous repeints d'après le rendu (IoU 0,76). La pièce reste lisible, mais elle est plus pauvre que les immeubles.
- N3 : léger dédoublement d'un climatiseur sur la face est, au raccord des tuiles.
- Les fenêtres allumées par le générateur ne correspondent pas toujours au masque `_fenetres` : quelques fenêtres peintes allumées ne s'allument pas en plus la nuit.
- Le portique à implant, les bancs, les lampadaires et les PNJ ne sont pas des pièces de ce lot : ce sont les clés existantes à poser.

Planche contact : `/workspace/nml-shots/megaline_sprites/lot2_planche_contact.png`. Maquettes de la zone avec les lots 1 et 2 : `lot2_maquette_ligne.png` et `lot2_maquette_ligne_nuit.png`. Ces images sont hors jeu.

## Mega-Line v2 — lot 3 : terminus (Ocre, 2026-11-17)

Dix-huit nouvelles clés `ml_tm_*_v2_3q` dans `assets/steel/mega_line/` (+ calques `_fenetres` / `_neon` par masque géométrique, + `ml_tm_portique_levage_v2_3q_avant`), groupe `ml_v2_terminus`, partie `terminus`. Noms de la liste de Rivet (`src/data/mega_line.js`), plus deux clés en plus (`ml_tm_rame_nord_v2_3q`, `ml_tm_conteneurs_x2_v2_3q`). Même méthode que les lots 1 et 2 : modèle 3D à la caméra du jeu (silhouette et alpha verrouillés), matière repeinte image-à-image, une seule mise à l'échelle uniforme. Pentes mesurées 0,33 / 0,70. Ancre = coin (x+w, z+d) au sol. Aucun ciel, aucun désert, aucune lumière du dehors ; le seul violet du terminus est la rame.

| Clé | Emprise (m) | h | px | Ancre | Calques |
|---|---|---|---|---|---|
| `ml_tm_voute_v2_3q` | 40 × 2 | 18 | 1717 × 1192 | 1654, 1188 | neon |
| `ml_tm_sas_mur_o_v2_3q` | 10 × 2 | 13 | 481 × 758 | 418, 752 | neon |
| `ml_tm_sas_portes_v2_3q` | 20 × 2 | 13 | 905 × 903 | 841, 888 | — |
| `ml_tm_sas_mur_e_v2_3q` | 10 × 2 | 13 | 481 × 758 | 418, 752 | neon |
| `ml_tm_heurtoir_v2_3q` | 3 × 1,4 | 1,2 | 151 × 129 | 113, 125 | neon |
| `ml_tm_voie_v2_3q` | 3 × 24,6 | 0,2 | 833 × 545 | 130, 539 | — |
| `ml_tm_quai_v2_3q` | 6 × 21 | 1,1 | 854 × 560 | 253, 553 | — |
| `ml_tm_rame_nord_v2_3q` (en plus) | 3 × 16,6 | 3,6 | 598 × 502 | 125, 498 | fenetres, neon |
| `ml_tm_voiture_v2_3q` | 3 × 8 | 3,6 | 354 × 361 | 125, 357 | fenetres, neon |
| `ml_tm_bureau_fret_v2_3q` | 7 × 5 | 4 | 456 × 387 | 301, 379 | fenetres |
| `ml_tm_dock_v2_3q` | 2 × 5 | 1,2 | 237 × 226 | 88, 219 | — |
| `ml_tm_portique_levage_v2_3q` (+ `_avant`) | 13 × 13 | 13,6 | 944 × 1024 | 556, 1011 | — |
| `ml_tm_conteneurs_x3_v2_3q` | 6 × 2,5 | 7,8 | 331 × 486 | 253, 479 | — |
| `ml_tm_conteneurs_x2_v2_3q` (en plus) | 6 × 2,5 | 5,2 | 331 × 372 | 253, 365 | — |
| `ml_tm_hangar_v2_3q` | 9 × 5 | 6 | 525 × 463 | 377, 441 | neon |
| `ml_tm_locaux_so_v2_3q` | 8 × 11 | 5 | 662 × 588 | 339, 580 | fenetres, neon |
| `ml_tm_locaux_e_v2_3q` | 3 × 26 | 6 | 875 × 840 | 132, 833 | neon |
| `ml_tm_passerelle_v2_3q` | 4 × 4 | 2,6 | 249 × 231 | 158, 227 | — |

**Poses.** Celles du plan de Rivet, base y 0 partout (le quai et la rame portent leur hauteur dans l'image) :
```js
G('tm2_voute', 'ml_tm_voute_v2_3q', 0, 0, 40, 2, …, { solid: [], fond: true }),
G('tm2_mur_o', 'ml_tm_sas_mur_o_v2_3q', 0, 0, 10, 2, …),
B('ml_sas', 'Les portes du sas', 'ml_tm_sas_portes_v2_3q', 10, 0, 20, 2, …),   // boîtiers éteints en x 13,5 / 26,5 : ml_ens_sas (z 2,15, h 12,4) tombe dessus
G('tm2_mur_e', 'ml_tm_sas_mur_e_v2_3q', 30, 0, 10, 2, …),
G('tm2_hangar', 'ml_tm_hangar_v2_3q', 0, 2, 9, 5, …),
G('tm2_heurtoir', 'ml_tm_heurtoir_v2_3q', 14, 2, 3, 1.4, …),
G('tm2_voie', 'ml_tm_voie_v2_3q', 14, 3.4, 3, 24.6, …, { solid: [], fond: true }),
G('tm2_quai', 'ml_tm_quai_v2_3q', 17, 3, 6, 21, …, { solid: [], etage: 1 }),   // plancher +1,1 sur z 3–22, rampe z 22–24
G('tm2_rame_nord', 'ml_tm_rame_nord_v2_3q', 14, 3.4, 3, 16.6, { h: 3.6 }, { solid: [{ x: 14, z: 3.4, w: 3, d: 16.6 }] }),  // NOUVELLE
G('tm2_voiture', 'ml_tm_voiture_v2_3q', 14, 20, 3, 8, …),   // porte est ouverte en z 25–26, face à la jonction tm_rame_quai (17 ; 25,2)
G('ml_bureau', 'ml_tm_bureau_fret_v2_3q', 2, 9, 7, 5, …),
G('tm2_dock', 'ml_tm_dock_v2_3q', 9, 9, 2, 5, …),
B('ml_portique', 'Portique de levage', 'ml_tm_portique_levage_v2_3q', 24, 8, 13, 13, { solid: [4 pieds 1 × 1] }),
// CONT : piles de 3 -> ml_tm_conteneurs_x3_v2_3q ; piles de 2 -> ml_tm_conteneurs_x2_v2_3q (au lieu de ml_conteneurs)
G('tm2_portique_avant', 'ml_tm_portique_levage_v2_3q_avant', 24, 8, 13, 13, { solid: [] }),   // APRÈS les conteneurs
G('tm2_loc_e', 'ml_tm_locaux_e_v2_3q', 37, 2, 3, 26, …),
G('tm2_loc_so', 'ml_tm_locaux_so_v2_3q', 0, 17, 8, 11, …),
G('tm2_pass', 'ml_tm_passerelle_v2_3q', 8, 24, 4, 4, { solid: [{ x: 8, z: 24, w: 0.3, d: 4 }, { x: 11.7, z: 24, w: 0.3, d: 4 }] }),  // UNE pose
```
**Ordre de dessin.**
1. voûte (fond), murs et portes du sas ;
2. hangar, heurtoir, voie, quai ;
3. rame nord, puis voiture ; panneau `ml_panneau_terminus` ;
4. bureau et dock ;
5. portique, conteneurs (z croissant), puis `ml_tm_portique_levage_v2_3q_avant` ;
6. locaux E, locaux SO, passerelle.
Les gyrophares (`ml_ens_gyrophare`) se posent sur les embases vides aux coins du portique (h 13,1).

**Écarts avec le plan de Rivet.**
- `ml_tm_voiture_v2_3q` est la dernière voiture de la vraie rame, violette (Rivet attendait une voiture sombre `#34383d`) ; feux de queue rouges au sud.
- `ml_tm_rame_nord_v2_3q` en plus (deux voitures, z 3,4–20, tête au nord hors champ) : sans elle, la voiture d'accès est seule à quai. À poser avant la voiture.
- `ml_tm_conteneurs_x2_v2_3q` en plus : `ml_conteneurs` existant n'est pas à 50 px/m (280 px pour 6 × 2,5 m) et paraît trop petit à côté des piles de 3.
- Passerelle : une seule pose 4 × 4 en (8, 24), pas deux garde-corps 0,3 × 4 ; les solides des garde-corps restent ceux de Rivet.
- Quai : la rampe occupe z 22–24 (le plancher +1,1 s'arrête à z 22).

**Défauts connus.**
- Portique : peint d'un seul tenant, léger agrandissement ×1,10 (pièce fine, continuité des poutres) ; un reste d'échelle et de cabine du brut subsiste en haut du pied SE.
- Voie : recalage plus lâche (IoU 0,86) ; moins de traverses que le modèle, rives jaunes irrégulières côté ouest. Pièce de sol, peu visible sous la rame.
- Passerelle SO : pièce petite et pauvre (tôle des garde-corps pleine, IoU 0,96 mais matière peu lisible).
- Portes du sas : pas de calque lumineux (boîtiers éteints, c'est voulu) ; l'alerte vient de `ml_ens_sas`.
- Conteneurs : petites marques illisibles sur les portes (pas de lettrage lisible).
- Maquette de nuit : la voûte reste sombre, ses suspensions sodium ne sont qu'en `_neon`.

Planche contact : `/workspace/nml-shots/megaline_sprites/lot3_planche_contact.png`. Maquettes posées : `lot3_maquette_terminus.png` et `lot3_maquette_terminus_nuit.png`. Ces images sont hors jeu.

## Mega-Line v2 — sol du parvis et de la rue (Ocre, 2026-11-17)

Le sol actuel de `steel_megaline` (`g_ml_pave`) peint des halos violets et cyan dans la tuile. Répétés tous les 4 m, ils font des taches sans source sur toute la rue et le parvis (défaut de la consigne NML). Remplacement par une dalle mate, sans aucune lumière peinte : la couleur vient seulement des lumières du code (lampadaires, échoppes, reflets des écrans sur le quai).

| Clé | px | Tuile | Contenu |
|---|---|---|---|
| `g_ml_parvis_v2` | 512 × 512 | 4 m | base : dalles de béton 1 × 0,5 m à joints décalés, gris-brun chaud, arêtes usées, crasse, deux petites taches d'huile, une fissure |
| `g_ml_parvis_v2_b` | 512 × 512 | 4 m | variante : une flaque et deux taches d'huile |
| `g_ml_parvis_v2_c` | 512 × 512 | 4 m | variante : fissures, une dalle ragréée, huile et crasse |
| `g_ml_parvis_v2_d` | 512 × 512 | 4 m | variante : deux flaques, une tache d'huile |

Même format que `g_ml_pave` (512 px = 4 m, raccordable). Les variantes ont des bords identiques à la base sur 48 px : elles se posent n'importe où sur la grille de 4 m sans couture. Pas de calque `_nuit` : aucune dalle de sol existante n'en a, la nuit passe par l'éclairage et `ground.tint`.

**Pose** (dans `steel_megaline`, `src/data/mega_line.js`) : `g_ml_parvis_v2` **remplace `g_ml_pave`** comme skin du sol ; les variantes cassent la répétition par `ground.paint`, en carreaux de 4 × 4 m dont x et z sont multiples de 4 (le motif part du coin de la pose, donc il reste en phase).
```js
ground: { base: '#12121a', skin: 'g_ml_parvis_v2', tileM: 4, clean: true,
  paint: [[12, 24, '_c'], [24, 24, '_b'], [36, 28, '_d'], [48, 24, '_c'], [28, 32, '_c'], [8, 36, '_b'], [20, 36, '_d'], [40, 36, '_b'], [56, 36, '_c'], [12, 8, '_b'], [32, 8, '_c']]
    .map(([x, z, v]) => ({ x, z, w: 4, d: 4, skin: 'g_ml_parvis_v2' + v, tileM: 4 })) },
```
Les carreaux proposés tombent sur la rue (z 22–32), le parvis (z 32–40) et la ruelle (z 8–10). Ceux qui passent sous un bâtiment ou sous le quai sont simplement invisibles. `g_ml_pave` reste dans le manifeste, intact. Les deux reflets d'écran au sol (`glows` violet et cyan en z 15,6, sur le quai) ont une source : ils restent.

Planche : `/workspace/nml-shots/megaline_sprites/parvis_dalle_contact.png` (les quatre tuiles + un aperçu 6 × 6 raccordé à la caméra du jeu). Hors jeu.
