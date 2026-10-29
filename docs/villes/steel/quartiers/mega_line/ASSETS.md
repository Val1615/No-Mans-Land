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
