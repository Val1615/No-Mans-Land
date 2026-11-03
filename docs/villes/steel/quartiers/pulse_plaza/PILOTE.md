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

## Lot murs (main) : pose retenue et vérifications
- Tout est reculé hors de la place, bord à bord, sans chevauchement d'emprise entre murs (vérifié par tests/pulse_rapide.py) ni PNJ masqué par un mur (`view.masques()`).
- Nord : deux `pp_facade_c` (x 0 à 12 et 36 à 48, z -1,5 à 0), écrans `pp_ecran_haut_n2` (x 3 à 7) et `pp_ecran_haut_n1` (x 39 à 47) devant. L'Arcadius (immeuble blanc d'IO, nommé, avec portique et texte) est gardé ; `pp_facade_c` remplace la façade sombre à sa droite.
- Ouest : `pp_facade_a_o` (z 3 à 15), `pp_facade_b_o2` (z 17 à 25 et 25 à 33), x < 0. Accès ouest z 15 à 17 libre.
- Sud : `pp_mur_bas` x 0 à 16 et 40 à 48 (z 36 à 36,5) ; x 32 à 40 la pièce masquait Noor, remplacée par un garde-corps bas dessiné par le code ; x 20 à 28 (escalier, grille) libre.
- Est : `pp_mur_bas_o` z 20,5 à 36,5 (x 48 à 48,5) ; écran `pp_ecran_haut_e1` à x 45,4 à 46, z 16 à 24 ; jonction Strip z 12 à 14 libre ; garde-corps bas z 0 à 6 et 14 à 20,5.
- Pentes des faces x, mesurées sur l'alpha de la base : théorie de la caméra 0,331 ; `pp_facade_c` et `pp_mur_bas` 0,330 (collent au sol) ; `pp_facade_a` 0,539 et `pp_facade_b` 0,510 décollent (environ 2,7 m d'écran sur les 16 m de `pp_facade_a`, 1,2 m sur les 8 m de `pp_facade_b`) : elles ne sont plus posées. Faces z : 0,69 à 0,70 pour 0,70 attendu.
- À reprendre par Ocre : les murs « bas » de 4 m restent hauts sur les bords sud et est, côté caméra (ils cachent une bande d'environ 7 m derrière eux) ; une version à 1,2 m serait plus juste. L'écran `pp_ecran_haut_e1` (8,9 m) paraît grand au premier plan ; n1 et n2, au fond, passent bien. Si les façades hautes du fond paraissent encore intrusives, une version à 4 m est possible.

## Retouches après pose (lot creation/pulse-retouches)
Verdict de Rivet sur capture : la pente 0,33 des faces x est la bonne.
- `pp_facade_a` recisaillée de 0,54 à 0,33 : 687 x 488, ancre [607, 486].
- `pp_facade_b` recisaillée de 0,51 à 0,33 : 359 x 282, ancre [297, 280].
- `pp_ecran_haut_e2` : même design que e1, face z pente 0,70, 4 m de z, 138 x 394, ancre [0, 393]. Il se pose **en hauteur sur la façade est**, jamais au sol au milieu de la place (bas des supports à 4 m, `elevation_m`). L'ancre est le pied de la façade porteuse sous le bord sud de l'écran, par exemple (46 ; 24). Zone d'écran vide, `ecran_rect` [13, 17, 125, 143], `ecran_coins` [[13, 95], [125, 17], [125, 64], [13, 143]]. e1 est conservé.
- `pp_muret` (face x, 8 m, 1,2 m) : 400 x 200, ancre [398, 199]. `pp_muret_o` (face z, 8 m) : 275 x 260, ancre [0, 259]. Même logique que pp_mur_bas : ancre au coin, raccord bord à bord, pièce suivante ancrée 8 m plus loin.
Planche de contrôle : `/workspace/nml-shots/pulse_retouches.png`.

## Revue 2 (main) : pose retenue
- Nord : l'immeuble blanc (`pp_arcadius`) est retiré. Bord nord bord à bord : `pp_facade_c` x 0 à 12, `pp_facade_a` (recisaillée 0,33) x 12 à 28, `pp_facade_b` (recisaillée 0,33) x 28 à 36, `pp_facade_c` x 36 à 48. Portique IO au pied de `pp_facade_a` (20 ; 0). A et B sont des faces x : leur place est le bord nord, pas les bords latéraux (faces z, qui gardent `pp_facade_a_o` et `pp_facade_b_o2`).
- Sud : `pp_muret` x 0 à 24 et 32 à 48 (z 36 à 36,4) ; escalier de service et sa grille décalés de 4 m (escalier x 26 à 30, seuil 28 ; 35) pour que l'accès tombe sur la trame de 8 m (x 24 à 32) ; Noor suit (25 ; 31).
- Est : `pp_muret_o` z 0 à 8 et 28 à 36 ; kiosque merch (z 6 à 12) et stand de nouilles (z 24 à 30) adossés au bord ; jonction Strip z 12 à 16 ; `pp_mur_bas_o` (4 m) z 16 à 24 porte `pp_ecran_haut_e2` (z 20 à 24, supports à 4 m). e1 n'est plus posé.
- Ouest : `pp_facade_a_o` z 0 à 12, accès z 12 à 20, `pp_facade_b_o2` z 20 à 28 et 28 à 36. Plus aucun garde-corps dessiné par le code.
- Isaure (22,5 ; 23,4) devant le Holo, Vasseur (34,5 ; 8,5) à droite de l'écran du Feed : plus aucun PNJ ni figurant masqué.
- Attend une pièce d'Ocre : un tronçon de 4 m (`pp_muret` et `pp_muret_o`, et un 4 m porteur de 4 m de haut) permettrait de garder l'escalier à x 22 à 26 et de resserrer les accès ouest (8 m) et est ; le seul mur porteur de 4 m de haut à l'est reste `pp_mur_bas_o` (une version porteuse plus fine, au style des murets, serait plus juste sous e2).

## Murets de 4 m et support d'écran (lot creation/pulse-murets4)
- `pp_muret_4` (face x, 4 m, 1,2 m, pente 0,33) : 200 x 134, ancre [198, 133]. `pp_muret_4_o` (face z, 4 m, pente 0,70) : 138 x 165, ancre [0, 163]. Faits des deux embouts des murets de 8 m (2 m chacun, joints sur un panneau), pas d'une coupe au milieu. Ancre au coin, raccord bord à bord avec pp_muret et pp_muret_o : la pièce suivante s'ancre 4 m plus loin. Usage prévu : remettre l'escalier sud à sa place et resserrer l'accès ouest à 2 m.
- `pp_support_ecran_o` (face z, 4 m) : 138 x 307, ancre [0, 305]. Muret de 4 m et deux mâts fins en métal sombre et laiton jusqu'à 4 m, avec platines de fixation et traverse haute. Remplace le pp_mur_bas_o de 4 m sous l'écran est. Pose : façade est, bord x 46, z 20 à 24, ancre au coin bas (46 ; 24). `pp_ecran_haut_e2` se pose avec la même ancre au sol (46 ; 24) : le bas de ses supports tombe à 4 m (`fixation_ecran.elevation_m`), sur les platines.
Planche de contrôle : `/workspace/nml-shots/pulse_murets4.png`.

## Revue 3 (main) : murets de 4 m et support d'écran
- Sud, trame de 4 m : `pp_muret` x 0 à 16, `pp_muret_4` x 16 à 20, accès x 20 à 28 (escalier x 22 à 26, seuil 24 ; 35 et Noor 27 ; 31 remis à leur place d'origine), `pp_muret_4` x 28 à 32, `pp_muret` x 32 à 48.
- Ouest : `pp_facade_a_o` z 0 à 12, accès z 12 à 16 (4 m ; seuil déplacé de 16 à 14 pour le centrer : 2 m ne tombe pas sur la trame de 4 m), `pp_facade_b_o2` z 16 à 24 et 24 à 32, `pp_muret_4_o` z 32 à 36.
- Est : `pp_muret_o` z 0 à 8, `pp_muret_4_o` z 8 à 12, jonction Strip z 12 à 16, `pp_muret_4_o` z 16 à 20, `pp_support_ecran_o` z 20 à 24 (à la place du `pp_mur_bas_o`), `pp_muret_4_o` z 24 à 28, `pp_muret_o` z 28 à 36. `pp_ecran_haut_e2` sur la même ancre que son support : (48,4 ; 24), sur la ligne x 48 du bord est (x 46 du manifeste laisserait la ligne du bord ouverte sur z 20 à 24).
