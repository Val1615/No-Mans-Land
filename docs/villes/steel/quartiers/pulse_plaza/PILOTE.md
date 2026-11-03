# Pulse Plaza, chantier pilote [proposition]

But : rapprocher la capture en jeu du concept `1_pulse_plaza.jpg`. Captures de départ sur origin/main : `/workspace/nml-shots/pulse_actuel_1280.png` et `pulse_actuel_390.png`.

## Écarts relevés
- Sol : une seule tuile violette et cyan, saturée et répétée partout, sans allées. Le concept a une dalle sombre neutre et des circulations lisibles.
- Façades : seuls l'Arcadius et la tour Human Corp ferment la place, les bords nord, ouest et est restent ouverts sur le vide.
- Volumes plats : rien entre le sol et les grands bâtiments, pas de statues, de bornes ni de lampadaires hauts.
- Halos sans source : des taches de lumière violette au sol sans lampe visible.
- PNJ : deux sprites de foule clonés, dispersés en ligne au lieu d'un public groupé devant le Holo et l'écran.
- Écran du Feed noir dans la capture (animations à 0), et étiquettes posées sur les accès (escalier de service, sorties).
- Palette : trop violette et cyan, il manque les ambres chaudes des vitrines.

## Modules ajoutés (assets/steel/pulse_plaza/, status v1, champ `pilote`)
| fichier | px | ancre | où le poser (x ; z en m) |
|---|---|---|---|
| `pp_facade_a.webp` | 800 x 600 | [664, 599] | nord, x 36 à 48 (raboutée à l’Arcadius), z 0 à 2 |
| `pp_facade_a_o.webp` | 800 x 600 | [133, 599] | est, x 46 à 48, z 12 à 24 (entre kiosque et nouilles) |
| `pp_facade_b.webp` | 420 x 330 | [343, 329] | nord, x 0 à 8 puis x 4 à 12 en doublon, z 0 à 1,5 |
| `pp_facade_b_o.webp` | 420 x 330 | [74, 329] | ouest, x 0 à 1,5, z 14 à 22 (entre billboard et guérite, accès ouest laissé libre) |
| `pp_lampadaire.webp` | 120 x 300 | [59, 299] | (8 ; 14), (8 ; 26), (40 ; 14), (36 ; 31) ; halo cyan du code centré au pied |
| `pp_statue.webp` | 150 x 170 | [74, 169] | socles autour du Holo : (13 ; 19), (15 ; 25), (33 ; 25) |
| `pp_borne_neon.webp` | 50 x 110 | [24, 109] | de part et d’autre de l’écran du Feed : (11 ; 11) et (33 ; 11) ; halo magenta du code |
| `pp_jardiniere.webp` | 90 x 90 | [45, 89] | à côté des bancs : (4 ; 21,5), et (40 ; 24) |
| `g_pp_dalle_sombre.webp` | 512 x 512 | tuile | sol de base de steel_pulse à la place de g_pp_dalle_mouillee, qui reste en zones |
| `g_pp_allee.webp` | 512 x 512 | tuile | allées : x 22 à 26 de z 4 à 28 (portique vers escalier) et z 15 à 17 de x 0 à 48 |
| `gen_pp_foule_c.webp` | 180 x 512 | [90, 511] | figurant, remplace un clone : (15 ; 14,5) |
| `gen_pp_foule_d.webp` | 180 x 512 | [90, 511] | figurant, remplace un clone : (19 ; 13,6) |
| `gen_pp_foule_e.webp` | 180 x 512 | [90, 511] | figurant, remplace un clone : (29 ; 15) |
| `gen_pp_foule_f.webp` | 180 x 512 | [90, 511] | figurant, remplace un clone : (14 ; 16,6) |
| `gen_pp_foule_g.webp` | 180 x 512 | [90, 511] | figurant, remplace un clone : (26 ; 23,4) |
| `gen_pp_foule_h.webp` | 180 x 512 | [90, 511] | figurant, remplace un clone : (18 ; 23,2) |
| `gen_pp_foule_i.webp` | 180 x 512 | [90, 511] | figurant, remplace un clone : (30,5 ; 16,8) |
| `gen_pp_foule_j.webp` | 180 x 512 | [90, 511] | figurant, remplace un clone : (27 ; 13,8) |

Les lampadaires et bornes portent leur source de lumière, sans halo au sol : le halo reste celui du code, à centrer sur l'ancre. Rien de ce qui existait n'a été régénéré.

## Pose réalisée (main, src/data/pulse_plaza.js) et notes pour Ocre
- Sol : `g_pp_dalle_sombre` en base ; `g_pp_dalle_mouillee` reste en zones (devant l'écran, au sud du Holo) ; allées `g_pp_allee` posées en `ground.paint` (format de l'éditeur de cartes) : x 22 à 26 de z 4 à 28, z 15 à 17 de x 0 à 48.
- Transition sol / bâtiments : bande `g_pp_grille` assombrie au pied des façades, de l'Arcadius, du portique et des stands.
- Halos : chaque halo a une source (écran, Holo, billboard, kiosque, distributeur, portique, stand, guérite, caméras, lampadaires, bornes, vitrines) ; ceux des lampadaires et des bornes sont centrés sur l'ancre ; ambres chaudes au pied des façades.
- Figurants : `gen_pp_foule_c` à `j` aux points du tableau ; `foule_a` et `foule_b` ne servent plus qu'aux deux passants. Les 9 PNJ nommés sont inchangés.
- Accès : plus d'étiquette sur les jonctions de la place (`accessLabels: false`) ni sur l'escalier de service ; les anneaux de seuil restent.
- Écran du Feed : `pp_ecran_feed.webp` est un écran vierge (« contenu animé par le code ») et aucun code ne le remplissait ; la teinte de la lumière l'assombrissait encore. Le contenu est maintenant dessiné par le code dans la dalle de l'image (4 pages, une toutes les 9 s).
- **Échelle, à reprendre par Ocre** : les variantes `_o` ne suivent pas l'axe z de la caméra (lacet 34,5°, un mètre en z vaut 0,566 m d'écran contre 0,824 en x). `pp_facade_b_o` est dessinée sur environ 12 m de z pour une emprise de 8 m, `pp_facade_a_o` sur environ 23,6 m pour 16 m ; la pente de leur base (environ 0,43) ne suit pas un bord en z (0,70 attendu). Posées aux coordonnées du tableau, elles couvraient l'accès ouest (seuil 1 ; 16) et la jonction vers Fréquence Strip (seuil 47 ; 13). Pose retenue : ouest en quatre `pp_facade_b_o` (ancres z 8, 15, 29, 36), est en `pp_facade_b_o` (ancres z 6, 26, et z 36 à l'échelle 0,5 pour ne pas masquer le stand de nouilles). `pp_facade_a_o` n'est pas posée : aucune place sur l'est sans masquer le kiosque et la jonction. Il faudrait une version `_o` d'environ 420 px de large pour 12 m de z.
- `g_pp_allee` n'a pas de variante tournée : sur l'allée est-ouest, la bande de laiton traverse l'allée tous les 4 m au lieu de la border.

## Mobilier, écrans, façade et murs bas (lot creation/pulse-mobilier) [proposition]
Faces construites à partir d'élévations de face générées, puis cisaillées : face x à 50 px/m et pente 0,33, face z à 34,4 px/m et pente 0,70 (lacet 34,5°), hauteur à 50 px/m. Les écrans sont vides (8, 8, 12) : le code y dessine le contenu comme pour le Feed, d'après `ecran_coins` (haut gauche, haut droit, bas droit, bas gauche) ou `ecran_rect` (x0, y0, x1, y1) en px de l'image. Leur ancre est au sol, sous les supports (`elevation_m`).

| fichier | px | ancre | rect d'écran | pose suggérée |
|---|---|---|---|---|
| `pp_mur_bas.webp` | 400 x 342 | [398, 340] |  | sud : bord z 35,5 à 36, de x 40 à 48 (répéter vers l’ouest tous les 8 m) ; raccord bord à bord avec pp_mur_bas_o au coin (48 ; 36) |
| `pp_mur_bas_o.webp` | 275 x 402 | [0, 401] |  | est : bord x 47,5 à 48, de z 28 à 36 (répéter vers le nord tous les 8 m) ; même ancre (48 ; 36) que pp_mur_bas au coin |
| `pp_facade_c.webp` | 600 x 698 | [598, 697] |  | nord-est, face x : x 36 à 48, z 0 à 1,5 ; remplace l’immeuble blanc et cyan ; ancre au coin avant droit (48 ; 1,5) |
| `pp_ecran_haut_n1.webp` | 400 x 665 | [399, 664] | [37, 35, 363, 280] | façade nord, sur pp_facade_c : x 39 à 47, z 1,5 ; bas des supports à 5 m, ancre au pied sous le bord droit (47 ; 1,5) |
| `pp_ecran_haut_n2.webp` | 200 x 544 | [199, 543] | [16, 17, 181, 188] | façade nord, sur pp_facade_b : x 3 à 7, z 1,5 ; ancre (7 ; 1,5) |
| `pp_ecran_haut_e1.webp` | 275 x 636 | [0, 635] | [25, 33, 249, 285] | façade est, sur pp_facade_a_o : x 46, z 16 à 24 ; ancre au pied sous le bord sud (46 ; 24) ; laisse libre la jonction Strip (47 ; 13) |
| `pp_banc_bois.webp` | 118 x 90 | [77, 89] |  | banc métal et bois, assise le long de x ; ex. (6 ; 21) et (38 ; 21), dos à la façade |
| `pp_banc_bois_o.webp` | 63 x 96 | [18, 95] |  | banc métal et bois, assise le long de z ; ex. bord ouest (3 ; 10) ou est (44,5 ; 20) |
| `pp_banc_beton.webp` | 118 x 90 | [82, 89] |  | banc béton, dossier laiton, assise le long de x ; ex. (6 ; 21) et (38 ; 21), dos à la façade |
| `pp_banc_beton_o.webp` | 67 x 98 | [16, 96] |  | banc béton, dossier laiton, assise le long de z ; ex. bord ouest (3 ; 10) ou est (44,5 ; 20) |
| `pp_kiosque_presse.webp` | 170 x 232 | [96, 231] |  | kiosque holo-presse : (10 ; 30), entre la guérite et l’escalier, sans gêner l’accès sud |
| `pp_kiosque_boissons.webp` | 170 x 232 | [99, 231] |  | kiosque à boissons : (38 ; 30), près du stand de nouilles |

Planche de contrôle (pas une capture du jeu) : `/workspace/nml-shots/pulse_mobilier.png`.
