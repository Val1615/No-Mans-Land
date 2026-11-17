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
| Bâti nord N1 / N2 / N3 | x0–24 / x24–44 / x48–64, z0–8 (h 12 / 16 / 10) | gabarits pleins, fenêtres ambrées |
| Passerelle de service | x44–48, z0–8 | couloir ouvert entre deux garde-corps ; porte `ml_passerelle` au bord nord (46 ; 0) -> `tm_sud` |
| Ruelle de service | z8–14 | praticable, passe sous le viaduc entre les piles ; bennes, caisses ; Marcel (entretien) sous le viaduc |
| Viaduc | z10–14, sous-poutre 6, rails 6,8 | 3 segments (24, 24, 16 m) non bloquants ; 6 piles 1,6 × 1,6 pleines (x2…62) |
| Rame | z10,5–13,5, base 6,8 | défile vers l'est toutes les 40 s (10 s de passage), ne s'arrête jamais ; repli `ml_rame` |
| Quai | x18–46, z14–22, plancher +6 | tablier, poteaux de galerie, garde-corps laiton ; bande d'embarquement z14–17,5 fermée par 2 barrières et le portique |
| Portique à implant | x31–32,6, z17–18 (+6) | planches accepté/refusé inchangées ; porte `ml_rame_quai` (seuil 31,8 ; 18,6) |
| Écrans | x19,9–25,1 et x36,9–42,1, flanc du viaduc, base 7,2 | Vibes à l'ouest, Tron à l'est (planches existantes, comptées comme une animation) |
| Rez sous le quai | z14–20 (galerie z20–22) | Mme Tran x18–24, câbles x24–30, Human Corp x30–38 (logo animé), atelier de Rivet x38–46 ; non bloquants (sous le tablier) |
| Escaliers O / E | x18–21 / x43–46, z22–32 | montée de 6 m vers le nord, seuls accès au quai |
| Rue piétonne, terrasses | x21–43, z22–32 | 6 terrasses, établi de Rivet, Mme Tran et Rivet devant leurs échoppes |
| Rues latérales | x10–18, x46–54 | praticables du parvis à la ruelle |
| Bâti W / E | x0–10 / x54–64, z14–32 | gabarits pleins (h 12 / 10) |
| Parvis sud | z32–40 | lampadaires, bancs ; porte `ml_sud` au centre du bord sud (32 ; 40) -> `c_mega` |

PNJ (dialogues inchangés) : Sabine (contrôleuse, haut de l'escalier ouest), Anselme Roque (navetteur, bout est du quai), Kessler (vigile, au portique),
Lou (étudiante, banc du quai), Yuna (fan, sous l'écran de Vibes), Noé (pancarte, pied de l'escalier est), Marcel (entretien, ruelle sous le viaduc),
Mme Tran (devant son échoppe), Rivet (devant son atelier). Figurants : 5 voyageurs sur la bande d'embarquement, 8 passants (3 masqués en plan large) ;
passants qui marchent : un qui monte l'escalier ouest, traverse le quai et redescend à l'est, un sur le parvis, un qui fait le tour par la ruelle.

### Le terminus (`steel_terminus`, 40 × 28, plan 2)
| zone | cotes (m) | dans le jeu |
|---|---|---|
| Voûte | x0–40, z0–2, clé 18 | pièce de fond (toujours derrière) ; suspensions sodium (lueurs du code) |
| Mur et portes du sas | x0–40, z0–2 ; portes x10–30, h 13 | pleins ; **aucune porte de jeu vers le sas**, clic = « Elles ne s'ouvriront pas » ; 2 planches `ml_ens_sas` + lueurs rouges clignotantes |
| Voie, heurtoir | x14–17, z3,4–28 ; heurtoir z2–3,4 | voie au ras du sol, traversable ; heurtoir plein |
| Quai | x17–23, z3–24, +1,1 | bords en pente douce de 0,6 m (pas de marche ratée), rampe au sud ; panneau vierge x18,5–21,5 (phrase par le code) ; Régie côté sas face à la voie |
| Voiture d'accès | x14–17, z20–28 | porte est éclairée orange : `tm_rame_quai` (seuil 18,2 ; 25,2) |
| Bureau de fret + dock | x2–9 + x9–11, z9–14 | Odile Ferraz devant |
| Portique de levage | x24–37, z8–21, h 13 | 4 pieds pleins ; 2 gyrophares orange (planche existante + lueurs) ; Bruno au pied, au sud |
| Conteneurs | 3 rangées × 2 piles, x24,5–36,5, z9,5–19 | piles de 2 = `ml_conteneurs` existant ; piles de 3 = gabarit `ml_tm_conteneurs_x3_v2_3q` |
| Hangar, locaux techniques | x0–9 z2–7 ; x0–8 z17–28 ; x37–40 z2–28 | gabarits pleins |
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
- Tout est en gabarits tant que les lots d'Ocre ne sont pas livrés (sauf mobilier, écrans, portique à implant, rame de repli, conteneurs de 2, panneau, lampes).
- Le rez sous le quai n'est pas praticable (voir plus haut) ; la galerie couverte se voit, on n'y marche pas.
- Bâti E : sa façade sur rue (ouest) est peu visible dans l'angle du jeu ; à soigner côté sud.
- Le quai du terminus est à +1,1 m avec des bords en pente douce (pas d'escalier) : simplification de jeu.

## Lots 1 et 2 d'Ocre reçus pendant la pose (ef04794, a203f03) : pas encore posés

Le lot 1 (structure : 22 clés `*_v2_3q`, plus `ml_rame_3v_dos_v2_3q` et les couches `_avant`, `_neon`, `_fenetres`, `_texte`) est arrivé sur main pendant ce lot, suivi du lot 2 (rez et bâti, a203f03, poses dans ASSETS.md lot 2). Comme demandé, ni l'un ni l'autre n'est **posé** ici : `gabaritsSeuls: true` sur `steel_megaline` empêche la substitution automatique des clés `attente` (src/main.js), et les gabarits restent affichés. Pour le prochain lot, il faut :
- retirer `gabaritsSeuls` ;
- câbler `base_y` (rame 6,8, barrière et cadre 6,0) ;
- poser les couches `_avant` du viaduc après la rame, avec les vues dos et miroir de la rame et leur `_texte_miroir` jamais retourné, puis l'image des écrans dans `ecran.quad_px` ;
- reprendre les écarts de la fiche de poses (ASSETS.md, lot 1) : cadre d'écran en z14–14,4, largeur 5,4, avec des mâts depuis le quai ; poteaux de galerie du quai ; profil de l'escalier (palier z22–23 à +6, puis une pente jusqu'à z32).
