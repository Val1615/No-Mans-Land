# Pulse Plaza : assets à produire

Conventions reprises de `docs/assets/PNJ_ASIA_CHINA.md`, `CHINA_LAKE_POSITIONS.md` et des manifestes `assets/*/manifest.json`. Tout ce qui suit est une **[proposition]** d'Ocre ; les tailles des décors sont estimées à 50 px/m et seront recalées après génération.

## Conventions
- Format : webp RGBA, fond transparent, recadrage serré, pivot bas-centre pour les PNJ, `anchor` au coin avant pour les bâtiments (comme `assets/buildings/manifest.json`).
- Préfixes : `g_pp_` pour les sols, `pp_` pour bâtiments et mobilier, `gen_pp_` pour les PNJ, `portrait-gen_pp_<id>.webp` pour les portraits.
- Sols : 512 x 512 px, tuilables sans raccord, comme `g_sv` et `g_wet`.
- PNJ : 512 px de haut, largeur libre (placeholder à 180), `height_m` et `footprint_m` [0.6, 0.6] dans le manifeste, statut « généré, pulse-plaza ».
- Portraits : 192 x 192, recadrage du haut du sprite sur fond (58,44,32).
- Chaîne PNJ : GenerateImage sur fond vert uni `#00E600`, détourage, comme le lot Asia-China.
- Angle des décors : contrôle d'angle v4 (`tools_steel.py`) avant intégration.

## Placeholders et manifest
Zone `steel_pulse` [décision du développeur]. Les 36 placeholders (cadre magenta et croix) sont dans `assets/steel/pulse_plaza/`, aux noms et tailles ci-dessous. Ils sont générés par `docs/villes/steel/quartiers/pulse_plaza/gen_placeholders.py`, qui écrit à cet emplacement.
v1 (branche creation/pulse-plaza-sprites) : les 36 fichiers sont des sprites v1 (ancres recalées). `pp_billboard` et `pp_holo_tron` viennent des sources fournies (`nml-shots/refs/`), détourées ; l'hologramme a une alpha de 0,8.
Index : `assets/steel/pulse_plaza/manifest.json`, un manifest par dossier comme `assets/buildings/` ou `assets/interiors/`. Les chemins `file` sont relatifs à `assets/` (ex. `steel/pulse_plaza/pp_kiosque.webp`). Champs : `px`, `footprint_m` et `anchor` (bas-centre, provisoire) pour les décors, `height_m` et `footprint_m` pour les PNJ, `tile_m` pour les sols, `npc` pour les portraits, `status` « placeholder ». Les vrais assets remplaceront les fichiers sous le même nom.

## Sols
| fichier | px | usage |
|---|---|---|
| `g_pp_dalle.webp` | 512 x 512 | dalle de béton bleu acier, joints fins |
| `g_pp_dalle_mouillee.webp` | 512 x 512 | même dalle avec flaques et reflets violets et cyan |
| `g_pp_grille.webp` | 512 x 512 | grille de service, accès sud |

## Bâtiments et mobilier
| fichier | px | footprint_m | dossier | note |
|---|---|---|---|---|
| `pp_arcadius.webp` | 1200 x 900 | 24 x 4 | steel/pulse_plaza/ | façade seule, verre noir, logo IO |
| `pp_ecran_feed.webp` | 1000 x 700 | 20 x 4 | steel/pulse_plaza/ | écran vierge ; contenu animé par le code |
| `pp_holo_socle.webp` | 400 x 300 | 8 x 8 | steel/pulse_plaza/ | disque chromé et rambarde |
| `pp_holo_tron.webp` | 220 x 512 | 0.6 x 0.6 | steel/pulse_plaza/ | hologramme semi-transparent de Groovy-Tron, image d'écran, pas un PNJ |
| `pp_billboard.webp` | 220 x 520 | 4 x 6 | steel/pulse_plaza/ | HCM-88X, visuel de Vibes |
| `pp_kiosque.webp` | 220 x 260 | 4 x 6 | steel/pulse_plaza/ | merch officiel |
| `pp_guerite.webp` | 220 x 260 | 4 x 6 | steel/pulse_plaza/ | SMPD |
| `pp_nouilles.webp` | 220 x 240 | 4 x 6 | steel/pulse_plaza/ | lumière chaude |
| `pp_distrib.webp` | 110 x 160 | 2 x 2 | steel/pulse_plaza/ | borne Next Drop |
| `pp_banc.webp` | 110 x 60 | 2 x 1 | steel/pulse_plaza/ | x 2 |
| `pp_portique.webp` | 220 x 180 | 4 x 2 | steel/pulse_plaza/ | portique IO |
| `pp_camera.webp` | 40 x 140 | 0.4 x 0.4 | steel/pulse_plaza/ | C.A.G.E. sur mât, x 4 |
| `pp_escalier.webp` | 200 x 200 | 4 x 4 | steel/pulse_plaza/ | descente vers la grille |

Contenus d'écran à prévoir (images ou séquences, hors placeholders) : clip de Vibes, démarrage GROOVY-TRON.EXE, titre « L'idole démasquée », bandeau feed, écran « Audience sync », alerte IO.

## PNJ
| clé | height_m | placeholder px | portrait |
|---|---|---|---|
| `gen_pp_maelle` | 1.64 | 180 x 512 | oui |
| `gen_pp_dorian` | 1.78 | 180 x 512 | oui |
| `gen_pp_brisset` | 1.80 | 180 x 512 | oui |
| `gen_pp_pham` | 1.62 | 180 x 512 | oui |
| `gen_pp_isaure` | 1.70 | 180 x 512 | oui |
| `gen_pp_clone_gt` | 1.85 | 180 x 512 | oui |
| `gen_pp_gaspard` | 1.72 | 180 x 512 | oui |
| `gen_pp_noor` | 1.58 | 180 x 512 | oui |
| `gen_pp_vasseur` | 1.76 | 180 x 512 | oui |
| `gen_pp_foule_a` | 1.70 | 180 x 512 | non (figurant) |
| `gen_pp_foule_b` | 1.74 | 180 x 512 | non (figurant) |

Entrée type de `assets/steel/pulse_plaza/manifest.json` :
```json
"gen_pp_maelle": {"file": "steel/pulse_plaza/gen_pp_maelle.webp", "source": "docs/villes/steel/quartiers/pulse_plaza/gen_placeholders.py", "height_m": 1.64, "px": [180, 512], "footprint_m": [0.6, 0.6], "status": "placeholder, pulse-plaza"}
```


## Lot `pulse_v4` (régénération sans warp)

Nouvelles clés (statut `pulse_v4`, champ `remplace`), voir `PULSE_PLAZA.md` § « Régénération v4 sans déformation » pour les mesures et les poses.

| ancienne | nouvelle | px | ancre | calques |
|---|---|---|---|---|
| `pp_nord_a_v2_3q` | `pp_nord_a_v3_3q` | 796×823 | [660, 820] | _ecran, _fenetres, _neon, _pulse, _pulse_b |
| `pp_nord_b_v2_3q` | `pp_nord_b_v3_3q` | 444×563 | [334, 560] | _fenetres, _neon, _pulse, _pulse_b |
| `pp_nord_c2_v2_3q` | `pp_nord_c2_v3_3q` | 630×674 | [494, 671] | _ecran, _fenetres, _neon, _pulse, _pulse_b |
| `pp_nord_c3_v2_3q` | `pp_nord_c3_v3_3q` | 622×670 | [495, 667] | _ecran, _fenetres, _neon, _pulse, _pulse_b |
| `pp_ouest_a_v3_3q` | `pp_ouest_a_v4_3q` | 513×757 | [170, 754] | _ecran, _fenetres, _pulse |
| `pp_ouest_b_v3_3q` | `pp_ouest_b_v4_3q` | 400×564 | [182, 561] | _fenetres, _pulse |
| `pp_ecran_feed_v3_3q` | `pp_ecran_feed_v4_3q` | 951×864 | [828, 861] | _ecran, _neon, _pulse |
| `pp_billboard_v2_3q` | `pp_billboard_v3_3q` | 281×409 | [168, 406] | _ecran, _neon, _pulse, _pulse_b |
| `pp_kiosque_v2_3q` | `pp_kiosque_v3_3q` | 276×294 | [174, 291] | _fenetres, _neon, _pulse, _pulse_b |
| `pp_nouilles_v2_3q` | `pp_nouilles_v3_3q` | 290×270 | [176, 267] | _fenetres, _neon |
| `pp_kiosque_presse_v2_3q` | `pp_kiosque_presse_v3_3q` | 280×272 | [169, 269] | _ecran, _fenetres, _neon, _pulse, _pulse_b |
| `pp_kiosque_boissons_v2_3q` | `pp_kiosque_boissons_v3_3q` | 289×270 | [172, 267] | _fenetres, _neon, _pulse, _pulse_b |
| `pp_portique_v2_3q` | `pp_portique_v3_3q` | 281×283 | [167, 280] | _fenetres, _neon, _pulse, _pulse_b |
| `pp_distrib_v2_3q` | `pp_distrib_v3_3q` | 281×241 | [166, 238] | _ecran, _neon, _pulse, _pulse_b |
| `pp_guerite_3q` | `pp_guerite_v2_3q` | 293×285 | [177, 282] | _fenetres, _neon, _pulse |
| `pp_dalle_pulse_a_3q` | `pp_dalle_pulse_a_v2_3q` | 280×146 | [166, 143] | _pulse, _pulse_b |
| `pp_dalle_pulse_b_3q` | `pp_dalle_pulse_b_v2_3q` | 280×146 | [167, 143] | _pulse, _pulse_b |
| `pp_totem_pulse_3q` | `pp_totem_pulse_v2_3q` | 141×284 | [84, 281] | _pulse, _pulse_b |
| `pp_enceinte_pulse_3q` | `pp_enceinte_pulse_v2_3q` | 141×228 | [83, 225] | _pulse, _pulse_b |
| `pp_arche_holo_3q` | `pp_arche_holo_v2_3q` | 305×334 | [249, 331] | _pulse, _pulse_b |
| `pp_pont_projecteurs_v3_3q` | `pp_pont_projecteurs_v4_3q` | 367×375 | [328, 372] | _faisceau, _pulse |
| `pp_banc_beton_o` | `pp_banc_beton_o_v2` | 81×87 | [23, 84] |  |
| `pp_ecran_haut_e2` | `pp_ecran_haut_e2_v2` | 141×248 | [26, 245] |  |
