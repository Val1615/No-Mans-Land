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
| `ml_etabli_v2_3q` | 1,6 × 0,6 | 0,9 | x39,2–40,8, z22,5–23,1 | établi de Rivet devant l'atelier (le café froid est posé dessus par le code) |
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

## Ce qui est posé (code, 17/11) — `src/data/mega_line.js`

### La ligne (`steel_megaline`, 64 × 40, plan 2)
| zone | cotes (m) | dans le jeu |
|---|---|---|
| Bâti nord N1 / N2 / N3 | x0–24 / x24–44 / x48–64, z0–8 (h 12 / 16 / 10) | sprites d'Ocre (lot 2) |
| Passerelle de service | x44–48, z0–8 | couloir ouvert entre deux garde-corps ; porte `ml_passerelle` au bord nord (46 ; 0) -> `tm_sud` |
| Ruelle de service | z8–14 | praticable, passe sous le viaduc entre les piles ; bennes, caisses ; Marcel (entretien) sous le viaduc |
| Viaduc | z10–14, sous-poutre 6, rails 6,8 | 3 segments (24, 24, 16 m) non bloquants ; 6 piles 1,6 × 1,6 pleines (x2…62) |
| Rame | z10,5–13,5, base 6,8 | passe sans s'arrêter toutes les 30 s (12 s), sens alternés : vue avant vers l'est, vue dos vers l'ouest |
| Quai | x18–46, z14–22, plancher +6 | tablier, poteaux de galerie, garde-corps laiton ; bande d'embarquement z14–17,5 fermée par 2 barrières et le portique |
| Portique à implant | x31–32,6, z17–18 (+6) | planches accepté/refusé inchangées ; porte `ml_rame_quai` (seuil 31,8 ; 18,6) |
| Écrans | cadres x19,8–25,2 et x36,8–42,2, z14–14,4, mâts depuis le quai ; dalle +10,5–13,38 | Vibes à l'ouest, Tron à l'est, posés dans la dalle (une seule animation) |
| Rez sous le quai | z14–20 (galerie z20–22) | Mme Tran x18–24, câbles x24–30, Human Corp x30–38 (logo animé), atelier de Rivet x38–46 ; non bloquants (sous le tablier) |
| Escaliers O / E | x18–21 / x43–46, z22–32 | palier +6 (z22–23), puis 36 marches jusqu'à z32 ; seuls accès au quai |
| Rue piétonne, terrasses | x21–43, z22–32 | 6 terrasses, Mme Tran et Rivet devant leurs échoppes |
| Rues latérales | x10–18, x46–54 | praticables du parvis à la ruelle |
| Bâti W / E | x0–10 / x54–64, z14–32 | sprites d'Ocre (lot 2) |
| Parvis sud | z32–40 | lampadaires, bancs ; porte `ml_sud` au centre du bord sud (32 ; 40) -> `c_mega` |

PNJ (dialogues inchangés) : Sabine (contrôleuse, haut de l'escalier ouest), Anselme Roque (navetteur, bout est du quai), Kessler (vigile, au portique),
Lou (étudiante, banc du quai), Yuna (fan, sous l'écran de Vibes), Noé (pancarte, pied de l'escalier est), Marcel (entretien, ruelle sous le viaduc),
Mme Tran (devant son échoppe), Rivet (devant son atelier). Figurants : 5 voyageurs sur la bande d'embarquement, 8 passants (3 masqués en plan large) ;
passants qui marchent : un qui monte l'escalier ouest, traverse le quai et redescend à l'est, un sur le parvis, un qui fait le tour par la ruelle.

### Le terminus (`steel_terminus`, 40 × 28, plan 2)
| zone | cotes (m) | dans le jeu |
|---|---|---|
| Voûte | x0–40, z0–2, clé 18 | pièce de fond (toujours derrière) ; suspensions sodium (lueurs du code) |
| Mur et portes du sas | x0–40, z0–2 ; portes x10–30, h 13 | sprites d'Ocre, joint plein ; **aucune porte de jeu vers le sas**, clic = « Elles ne s'ouvriront pas » ; 2 planches `ml_ens_sas` + lueurs rouges clignotantes |
| Voie, heurtoir | x14–17, z3,4–28 ; heurtoir z2–3,4 | voie au ras du sol, traversable ; heurtoir plein |
| Quai | x17–23, z3–24, +1,1 | bords en pente douce de 0,6 m (pas de marche ratée), rampe au sud ; panneau vierge x18,5–21,5 (phrase par le code) ; Régie côté sas face à la voie |
| Rame à quai | x14–17, z3,4–20 (2 voitures) + voiture d'accès z20–28 | la vraie rame, violette (exception au terminus) ; porte est de la voiture : `tm_rame_quai` (seuil 18,2 ; 25,2) |
| Bureau de fret + dock | x2–9 + x9–11, z9–14 | Odile Ferraz devant |
| Portique de levage | x24–37, z8–21, h 13 | 4 pieds pleins ; 2 gyrophares orange (planche existante + lueurs) ; Bruno au pied, au sud |
| Conteneurs | 3 rangées × 2 piles, x24,5–36,5, z9,5–19 | piles de 2 = `ml_tm_conteneurs_x2_v2_3q`, piles de 3 = `ml_tm_conteneurs_x3_v2_3q` ; poutres `_avant` du portique dessinées après |
| Hangar, locaux techniques | x0–9 z2–7 ; x0–8 z17–28 ; x37–40 z2–28 | sprites d'Ocre, pleins |
| Passerelle sud-ouest | x8–12, z24–28 | arrivée ; porte `tm_sud` au bord sud (10 ; 28) -> `ml_passerelle` |

## Le quai à +6 m : choix de modélisation
Le moteur n'a qu'un niveau de marche par point (grille 0,5 m, A*). Plutôt qu'un vrai second niveau, chaque lieu peut déclarer `niveaux`
(`src/core/niveaux.js`) : planchers plats `{ x, z, w, d, y }` et pentes `{ …, y0, y1, axe }` (escaliers, rampes). La hauteur sert au rendu
(personnages, PNJ, figurants et passants posés à la hauteur du sol, étiquettes et anneaux de porte relevés, caméra qui monte avec le joueur,
clic sur le quai résolu par lancer de rayon contre la hauteur du sol) et au jeu (on aborde un PNJ à son niveau, pas à travers le garde-corps).
L'accès est fait par les solides : bords du quai (nord côté voie, ouest, est, sud entre les trémies), côtés des escaliers, barrières de la bande.
Conséquences assumées : sous le tablier, le rez (z14–22) n'est pas praticable au sol, il se voit depuis la rue (échoppes ouvertes sur la galerie) ;
Mme Tran et Rivet se tiennent devant, dans la rue piétonne. L'ordre de dessin utilise un champ `etage` (rez 0 < tablier, escaliers, viaduc 1 <
ce qui est posé dessus et personnages en hauteur 2) quand deux emprises se recouvrent.

## Portes et sauvegardes
- `c_mega` (Center-Town, inchangée) <-> `ml_sud` (32 ; 40) ; `ml_passerelle` (46 ; 0) <-> `tm_sud` (10 ; 28) ; `ml_rame_quai` (portique) <-> `tm_rame_quai` (voiture).
- Chaque lieu refait porte `plan: 2` ; l'instantané enregistre `plans`. Une sauvegarde sans version (ancien plan 48 × 24 / 30 × 20) reprend à
  l'arrivée du lieu ; une position du bon plan mais coupée de l'arrivée (bande d'embarquement) aussi. Les autres sauvegardes ne bougent pas.

## Tests
`tests/megaline_rapide.py` (URL, OUT) ; `tests/mega_rapide.py` (rame jouable, 4 espèces) mis aux nouvelles coordonnées.

## Écarts connus
- Ligne : lots 1 et 2 posés. Terminus : lot 3 posé. Plus aucun gabarit dans les deux lieux.
- Quand on passe dans la ruelle derrière le quai, le tablier passe à 30 % (règle d'occultation commune) et laisse voir les échoppes. Le cadre caméra ordinateur (z16–24) montre peu la ruelle.
- Le rez sous le quai n'est pas praticable (voir plus haut) ; la galerie couverte se voit, on n'y marche pas.
- Bâti E : sa façade sur rue (ouest) est peu visible dans l'angle du jeu ; à soigner côté sud.
- Le quai du terminus est à +1,1 m avec des bords en pente douce (pas d'escalier) : simplification de jeu.

## Lots 1 et 2 d'Ocre posés (structure ef04794, rez et bâti a203f03)

Toutes les poses suivent les fiches d'ASSETS.md (lots 1 et 2) : sprites à l'échelle 1 (50 px/m), ancre au coin avant sud-est, `base_y` -> `y`,
octets inchangés. Plus aucun gabarit sur la ligne (`gabaritsSeuls` reste disponible dans main.js, inutilisé). Le terminus garde ses gabarits jusqu'au lot 3.

| pièce | clé | pose |
|---|---|---|
| bâti nord | `ml_bati_n1/n2/n3_v2_3q` | x0 / x24 / x48, z0, pleins |
| passerelle de service | `ml_passerelle_nord_v2_3q` | x44–48 z0–8, limons x44 et x47,7 (0,3 m) + borne x44,2 z6,4 ; libre x44,3–47,7 |
| ruelle | `ml_ruelle_benne_v2_3q` ×2, `ml_ruelle_caisses_v2_3q` ×3 | (3 ; 8,4) (37 ; 8,4) ; (5,6 ; 8,6) (52 ; 8,6) (16,5 ; 30,5) |
| viaduc | `ml_viaduc_seg24_v2_3q` ×2, `ml_viaduc_seg16_v2_3q`, `ml_viaduc_pile_v2_3q` ×6 | x0 / 24 / 48, z10 ; piles x2…62 tous les 12 m ; `_neon` automatique |
| poutres sud | `ml_viaduc_seg24_v2_3q_avant` ×2, `ml_viaduc_seg16_v2_3q_avant` | mêmes places, étage 3 : après la rame |
| rame | `ml_rame_3v_v2_3q` / `ml_rame_3v_dos_v2_3q` | base y 6,8, z10,5–13,5 ; un passage de 12 s toutes les 30 s, sens alternés (avant vers +x, dos vers −x), calques `_fenetres` `_neon` `_texte` de la vue courante, coupée aux bords du lieu |
| échoppes sous le quai | `ml_echoppe_tran/cables_v2_3q`, `ml_facade_humancorp_v2_3q`, `ml_atelier_rivet_v2_3q` | x18 / 24 / 30 / 38, z14 ; logo `ml_ens_human_corp` dans `logo.quad_px` ; café froid sur l'établi (39,8 ; 20,1 ; y 0,98) |
| quai | `ml_quai_tablier_v2_3q` | x18–46 z14–22, plancher +6 |
| escaliers | `ml_escalier_v2_3q` ×2 | x18 / x43, z22–32 ; limons de 0,15 m ; niveau : palier +6 z22–23 puis pente jusqu'à z32 |
| barrières | `ml_quai_barriere_v2_3q` ×2 | x18,4 / x32,6, z17,35, y 6 |
| écrans | `ml_ecran_cadre_v2_3q` ×2 | x19,8 / x36,8, z14–14,4, y 6, mâts pleins ; Vibes (ouest) et Tron (est) posés dans `ecran.quad_px` |
| terrasses | `ml_terrasse_v2_3q` ×6 | (22 ; 24) (26 ; 27,5) (30 ; 24) (34 ; 28) (37,5 ; 24) (40,5 ; 28), solide 0,8 × 0,8 |
| bâti W / E | `ml_bati_w_v2_3q`, `ml_bati_e_v2_3q` | x0 / x54, z14–32, pleins |

**Dalles posées par le code** (`b.dalles` : `{ champ, image }`) : plan vertical du monde, face sud, à la place exacte du quad du manifeste ; la caméra
iso le projette en parallélogramme (pente 0,33). L'image garde sa taille (256 px = 5,12 m), aucune retaille.

**Tri du peintre** : `b.zone` (quai et son rez, viaduc et ses piles). Dans une même zone, l'étage décide même sans emprise commune
(piles 0 < viaduc 1 < rame 2 < poutres `_avant` 3 ; rez 0 < tablier 1 < posé sur le quai 2). Sans cette règle, un bâti voisin en x passait devant
(tableau du quai derrière la façade Human Corp, poutre ouest derrière une pile). Personnage sur le quai ou l'escalier : zone `zoneNiveau` du lieu.

**Écarts avec la fiche, assumés** : solides des échoppes (z14–20,6) et poteaux de galerie non posés, parce que le sol à cet endroit est le quai
(un seul niveau de marche). Deux bouts de barrière invisibles (x18–18,4 et x45,2–46) ferment la bande d'embarquement aux extrémités.

**Échelle** : aucune pièce hors échelle. Largeur et hauteur des images mesurées par rapport à la boîte projetée (w × d × h à 50 px/m) : 1,01 à 1,07.
Les écarts viennent des débords (auvents, socle de pile 2 × 2, escaliers de secours). La terrasse fait 0,76 parce que le mobilier ne remplit pas ses 2 × 2 m.

## Lot 3 d'Ocre posé (terminus, f86e5ec)

Poses de la fiche d'ASSETS.md (lot 3), base y 0, échelle 1. Les six écarts avec notre fiche, sa fiche gagne :
1. `ml_tm_voiture_v2_3q` est la dernière voiture de la vraie rame, violette (exception au « pas de violet » du terminus) ;
2. `ml_tm_rame_nord_v2_3q` (x14–17, z3,4–20, pleine) est posée avant la voiture ;
3. les piles de deux conteneurs passent sur `ml_tm_conteneurs_x2_v2_3q`. L'ancien `ml_conteneurs` n'est pas à 50 px/m et n'est plus posé ;
4. la passerelle est posée une seule fois, en 4 × 4 en (8 ; 24), avec les solides des deux garde-corps ;
5. la rampe du quai va de z22 à z24 (déjà le cas dans `niveaux`) ;
6. `ml_tm_portique_levage_v2_3q_avant` se dessine après les conteneurs.

Tri : zone `cour` (portique 0 < conteneurs 1 < poutres `_avant` 2 < gyrophares 3) et zone `quai` (quai 1 < panneau 2, personnages sur le quai).
Les portes du sas restent pleines et ne s'ouvrent jamais : aucune porte de jeu, le clic dit « Elles ne s'ouvriront pas ». Lampes d'alerte rouges
`ml_ens_sas` sur les boîtiers éteints. La phrase « Dernier arrêt avant No Man's Land » est affichée par le code sur le panneau vierge.

Échelle : rien n'est hors échelle (rapport image / boîte projetée entre 0,95 et 1,06). Trois exceptions, sans gravité :
- la voûte (0,87 en hauteur) parce qu'elle est cintrée ;
- le dock (1,26 en hauteur), à cause des caisses et des bidons posés dessus ;
- la passerelle SO, plus étroite que son emprise : 249 px pour 278 attendus, et 91 px à droite de l'ancre pour 113, soit environ 3,2 m de profondeur sur 4. À reprendre si Ocre la refait.

Le portique, peint à ×1,10 d'après sa fiche, mesure 944 × 1024 px pour 904 × 1031 attendus : il reste dans la tolérance.

**Passage par le vestibule (choix de jeu, à valider par Régie et Ocre).** Avec la rame nord pleine (z3,4–20), la voiture (z20–28) et le heurtoir
(z2–3,4), la voie est occupée sur toute sa longueur. Le quai, Régie, la cour et Bruno seraient alors coupés de l'arrivée (passerelle SO).
On traverse donc par le vestibule de la voiture d'accès, portes ouvertes en z25–26 : le solide de la voiture laisse 1 m libre à cet endroit.
La face ouest de la voiture ne se voit pas dans l'angle du jeu. La jonction `tm_rame_quai` reste au seuil (18,2 ; 25,2).
