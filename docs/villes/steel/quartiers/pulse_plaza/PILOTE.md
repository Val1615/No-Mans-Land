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
