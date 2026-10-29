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

## Placeholders
Dans `placeholders/`, générés par `gen_placeholders.py` : cadre magenta et croix, aux noms et tailles ci-dessous. Ils restent dans ce dossier de docs et ne sont pas dans `assets/`, pour ne rien brancher par erreur. Le développeur peut les copier dans `assets/generated/` ou `assets/buildings/` s'il veut tester le placement.

## Sols
| fichier | px | usage |
|---|---|---|
| `g_pp_dalle.webp` | 512 x 512 | dalle de béton bleu acier, joints fins |
| `g_pp_dalle_mouillee.webp` | 512 x 512 | même dalle avec flaques et reflets violets et cyan |
| `g_pp_grille.webp` | 512 x 512 | grille de service, accès sud |

## Bâtiments et mobilier
| fichier | px | footprint_m | dossier cible | note |
|---|---|---|---|---|
| `pp_arcadius.webp` | 1200 x 900 | 24 x 4 | buildings/ | façade seule, verre noir, logo IO |
| `pp_ecran_feed.webp` | 1000 x 700 | 20 x 4 | buildings/ | écran vierge ; contenu animé par le code |
| `pp_holo_socle.webp` | 400 x 300 | 8 x 8 | buildings/ | disque chromé et rambarde |
| `pp_holo_tron.webp` | 220 x 512 | 0.6 x 0.6 | generated/ | hologramme semi-transparent de Groovy-Tron, image d'écran, pas un PNJ |
| `pp_billboard.webp` | 220 x 520 | 4 x 6 | buildings/ | HCM-88X, visuel de Vibes |
| `pp_kiosque.webp` | 220 x 260 | 4 x 6 | buildings/ | merch officiel |
| `pp_guerite.webp` | 220 x 260 | 4 x 6 | buildings/ | SMPD |
| `pp_nouilles.webp` | 220 x 240 | 4 x 6 | buildings/ | lumière chaude |
| `pp_distrib.webp` | 110 x 160 | 2 x 2 | buildings/ | borne Next Drop |
| `pp_banc.webp` | 110 x 60 | 2 x 1 | buildings/ | x 2 |
| `pp_portique.webp` | 220 x 180 | 4 x 2 | buildings/ | portique IO |
| `pp_camera.webp` | 40 x 140 | 0.4 x 0.4 | buildings/ | C.A.G.E. sur mât, x 4 |
| `pp_escalier.webp` | 200 x 200 | 4 x 4 | buildings/ | descente vers la grille |

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

Entrée de manifeste type (à ajouter à `assets/reused/manifest.json` si le chargeur l'exige) :
```json
"gen_pp_maelle": {"file": "generated/gen_pp_maelle.webp", "source": "GenerateImage (cursor)", "height_m": 1.64, "px": [180, 512], "footprint_m": [0.6, 0.6], "status": "placeholder, pulse-plaza"}
```
