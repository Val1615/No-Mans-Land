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
