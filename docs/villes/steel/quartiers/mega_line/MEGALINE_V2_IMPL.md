# Mega-Line v2 et terminus v2 : implémentation (Rivet, 17 nov. 2026)

Refonte demandée par Valentin le 17/11 (« aussi travaillée que les autres zones »), sur les planches d'Ocre du 12/11
(`nml-shots/concepts_megaline/NOTES.md`, planches 01 et 02). Ce document fixe **les emprises, les zones cotées et les clés d'assets attendues**,
pour qu'Ocre nomme ses modules pareil. Tant qu'une clé n'est pas livrée, le jeu pose un gabarit (volume à la bonne emprise et hauteur,
couleurs de la palette) ; dès que la clé apparaît dans `assets/steel/mega_line/manifest.json`, elle remplace le gabarit sans autre changement
de code (champ `attente { cle, h }`, comme Center-Town : `src/main.js`).

## Conventions de livraison (identiques à Center-Town)
- 50 px par mètre, vue du jeu (yaw 34,5°, pitch 28,8°), projection parallèle, **aucun étirement ni recompression** par le code.
- Un sprite = une emprise rectangulaire au sol `x × z` (m). x = est, z = sud. L'ancre (`anchor` du manifeste) est le **coin avant sud-est
  de l'emprise, au sol** (y = 0), sauf mention « base y = … » (pièce portée en hauteur : l'ancre est alors le coin avant sud-est à cette hauteur).
- Clés en `ml_<module>_v2_3q` (ligne) et `ml_tm_<module>_v2_3q` (terminus) : le préfixe `ml_` est celui que le catalogue range dans les décors.
- Palette : fer noir, laiton, béton, ambre ; **violet réservé à la rame et aux écrans** ; terminus en palette froide, sans violet, sans écran, sans pub.
- Canon : sous le sarcophage, ni ciel ni pluie ; Vibes (écran ouest) et Tron (écran est) seulement en image, aucun nom civil ; portes du sas
  pleines et fermées pour toujours, aucune lumière de dehors, jamais de désert ; panneau du terminus vierge (phrase affichée par le code) ;
  enseignes sans faux texte.

## Emprises
- `steel_megaline` : **64 × 40 m** (était 48 × 24). z0 = nord (vers le terminus), z40 = sud (Center-Town).
- `steel_terminus` : **40 × 28 m** (était 30 × 20). z0 = nord (sas), z28 = sud (vers la ligne).

## Clés d'assets attendues d'Ocre, par lot de production

### Lot 1 · structure de la ligne (viaduc, quai à +6 m, escaliers perpendiculaires, rame)
| clé | emprise x × z (m) | hauteur (m) | poses (m) | note |
|---|---|---|---|---|
| `ml_viaduc_seg24_v2_3q` | 24 × 4 | sous-poutre 6,0, dessus des rails 6,8 | x0–24 et x24–48, z10–14 | tablier de fer noir riveté, sans les piles |
| `ml_viaduc_seg16_v2_3q` | 16 × 4 | idem | x48–64, z10–14 | dernier segment (bord est) |
| `ml_viaduc_pile_v2_3q` | 1,6 × 1,6 | 6,0 | centres x2, 14, 26, 38, 50, 62 ; z11,2–12,8 | fer qui ruisselle ; passage libre 10,4 m entre piles |
| `ml_rame_3v_v2_3q` | 28 × 3 | 3,6, **base y = 6,8** | sur le viaduc, z10,5–13,5 | 3 voitures violettes, fenêtres ambre ; vue native vers l'est (+x), défile par le code sans s'arrêter |
| `ml_quai_tablier_v2_3q` | 28 × 8 | plancher **+6,0**, épaisseur 0,6, garde-corps laiton 1,1 (ouvrage 7,1) | x18–46, z14–22 | ancre au sol : le sprite comprend les poteaux de la galerie (bord sud z22, tous les 4 m). Garde-corps O, E et S sauf trémies d'escalier x18–21 et x43–46 ; pas de garde-corps côté voie (bord nord). Ligne jaune z15,2 |
| `ml_quai_barriere_v2_3q` | 12,6 × 0,3 | 1,1, **base y = 6,0** | x18,4–31 et x32,6–45,2 ; z17,35–17,65 | sépare la bande d'embarquement (z14–17,5) de la zone publique ; le portique à implant est entre les deux |
| `ml_escalier_v2_3q` | 3 × 10 | montée de 6,0 (z32 au sol -> z22 à +6) | x18–21 et x43–46, z22–32 | perpendiculaire au quai, vers la rue ; garde-corps des deux côtés ; même clé pour les deux poses |
| `ml_ecran_cadre_v2_3q` | 5,2 × 0,4 | 3,0, **base y = 7,2** | x19,9–25,1 et x36,9–42,1 ; z13,6–14 | cadre d'écran suspendu au flanc sud du viaduc ; le contenu reste `ml_ens_ecran_vibes` (ouest) et `ml_ens_ecran_tron` (est), déjà livrés (256 px = 5,12 m) |

Réutilisés tels quels (aucun nouveau module à faire) : `ml_portique_implant` + `ml_ens_portique_accepte` / `_refuse`, `ml_ens_ecran_vibes`,
`ml_ens_ecran_tron`, `ml_tableau`, `ml_ens_horaires`, `ml_banc`, `ml_poubelle`, `ml_borne`, `ml_lampadaire`, `ml_cafe_froid` (posés sur le quai
avec base y = 6 quand ils y sont). Repli de la rame : l'ancienne `ml_rame` (24 m) défile tant que `ml_rame_3v_v2_3q` n'est pas livrée.

### Lot 2 · rez-de-chaussée : échoppes sous le quai et bâti
| clé | emprise x × z (m) | hauteur (m) | poses (m) | note |
|---|---|---|---|---|
| `ml_echoppe_tran_v2_3q` | 6 × 6 | 5,4 (sous le tablier) | x18–24, z14–20 | nouilles de Mme Tran : vapeur, lanternes rouges, enseigne vierge |
| `ml_echoppe_cables_v2_3q` | 6 × 6 | 5,4 | x24–30, z14–20 | câbles et réparations |
| `ml_facade_humancorp_v2_3q` | 8 × 6 | 5,4 | x30–38, z14–20 | logo triangle, **sans lettrage** ; le logo animé `ml_ens_human_corp` existant est posé par le code |
| `ml_atelier_rivet_v2_3q` | 8 × 6 | 5,4 | x38–46, z14–20 | atelier de Rivet, établi (café froid `ml_cafe_froid` posé par le code) |
| `ml_bati_n1_v2_3q` | 24 × 8 | 12 | x0–24, z0–8 | 3 à 5 niveaux, fenêtres ambre, gabarit Center-Town sans tour |
| `ml_bati_n2_v2_3q` | 20 × 8 | 16 | x24–44, z0–8 | |
| `ml_passerelle_nord_v2_3q` | 4 × 8 | 4 | x44–48, z0–8 | passerelle de service ouverte à tous, vers le terminus (sortie au bord nord) |
| `ml_bati_n3_v2_3q` | 16 × 8 | 10 | x48–64, z0–8 | |
| `ml_bati_w_v2_3q` | 10 × 18 | 12 | x0–10, z14–32 | rez actif sur la rue latérale (face est) |
| `ml_bati_e_v2_3q` | 10 × 18 | 10 | x54–64, z14–32 | rez actif sur la rue latérale (face ouest, peu visible dans la vue : à soigner sur la face sud) |
| `ml_terrasse_v2_3q` | 2 × 2 | 1,0 | 6 poses, rue piétonne x21–43, z23–31 | table et deux tabourets |
| `ml_ruelle_benne_v2_3q` | 2 × 1,2 | 1,4 | ruelle de service z8–10 | |
| `ml_ruelle_caisses_v2_3q` | 1,6 × 1,2 | 1,2 | ruelle de service | |

Réutilisés : `ml_lampadaire` (parvis sud), `ml_banc`, `ml_poubelle`.

### Lot 3 · terminus (voûte, sas, portique, conteneurs, quai à l'est de la voie)
| clé | emprise x × z (m) | hauteur (m) | poses (m) | note |
|---|---|---|---|---|
| `ml_tm_voute_v2_3q` | 40 × 2 | clé 18 | x0–40, z0–2 | fond de voûte en coupe (nervures, suspensions sodium), peint **derrière tout** (pièce de fond) |
| `ml_tm_sas_mur_o_v2_3q` | 10 × 2 | 13 | x0–10, z0–2 | mur du sas, béton et acier |
| `ml_tm_sas_portes_v2_3q` | 20 × 2 | 13 | x10–30, z0–2 | portes pleines, jointives, sans hublot ni fente ; bandes jaune et noir ; lampes peintes éteintes (clignotement : `ml_ens_sas` existant + lueurs du code) |
| `ml_tm_sas_mur_e_v2_3q` | 10 × 2 | 13 | x30–40, z0–2 | |
| `ml_tm_heurtoir_v2_3q` | 3 × 1,4 | 1,2 | x14–17, z2–3,4 | heurtoir rouge au pied des portes |
| `ml_tm_voie_v2_3q` | 3 × 24,6 | 0,2 | x14–17, z3,4–28 | voie unique au ras du sol (traversable à pied) |
| `ml_tm_quai_v2_3q` | 6 × 21 | plancher +1,1 | x17–23, z3–24 | quai à l'**est** de la voie, rampe d'accès au sud (z22–24) comprise |
| `ml_tm_voiture_v2_3q` | 3 × 8 | 3,6 | x14–17, z20–28 | voiture sombre (pas de violet), porte est ouverte éclairée orange, marchepied (accès rame) |
| `ml_tm_bureau_fret_v2_3q` | 7 × 5 | 4 | x2–9, z9–14 | une fenêtre ambrée ; Odile devant |
| `ml_tm_dock_v2_3q` | 2 × 5 | 1,2 | x9–11, z9–14 | quai de chargement du bureau |
| `ml_tm_portique_levage_v2_3q` | 13 × 13 | 13 | x24–37, z8–21 | portique jaune ; seuls les 4 pieds (1 × 1 aux coins) sont pleins ; gyrophares : `ml_ens_gyrophare` existant |
| `ml_tm_conteneurs_x3_v2_3q` | 6 × 2,5 | 7,8 | sous le portique (voir plan) | pile de 3 conteneurs ; la pile de 2 est l'existant `ml_conteneurs` (6 × 2,5 × 5,2) |
| `ml_tm_hangar_v2_3q` | 9 × 5 | 6 | x0–9, z2–7 | hangar en tôle près du sas |
| `ml_tm_locaux_so_v2_3q` | 8 × 11 | 5 | x0–8, z17–28 | locaux techniques sud-ouest |
| `ml_tm_locaux_e_v2_3q` | 3 × 26 | 6 | x37–40, z2–28 | locaux techniques est, contre la paroi |
| `ml_tm_passerelle_v2_3q` | 4 × 4 | 2 | x8–12, z24–28 | arrivée de la passerelle de service (sud-ouest) |

Réutilisés : `ml_panneau_terminus` (vierge, x18,5–21,5 sur le quai, base y = 1,1), `ml_ens_sas`, `ml_ens_gyrophare`, `ml_conteneurs`.
