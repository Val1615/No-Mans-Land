# Dôme Fréquence : assets à produire

Mêmes conventions que `steel_arena/ASSETS.md`. Tout est **[proposition]** d'Ocre ; tailles estimées à 50 px/m.

## Conventions
- webp RGBA, fond transparent ; PNJ 512 px de haut, pivot bas-centre ; mobilier avec `anchor` au point avant bas ; sols 512 x 512 (`tile_m` 4).
- Préfixes : `g_df_` sols, `df_` mobilier et décor, `df_ens_` enseignes animées, `gen_df_` PNJ, `portrait-gen_df_<id>` portraits (192 x 192, fond (58,44,32)).
- Zone `steel_dome` [décision], intérieur de `c_tour`, porte de façade vers `steel_center` [proposition].
- Aucun faisceau, halo ou lumière animée n'est peint dans les images fixes [décision] : la scène, la verrière et la console sont livrées éteintes, leurs lumières sont des enseignes à part.

## Placeholders et manifest
50 fichiers dans `assets/steel/dome_frequence/`, générés par `docs/villes/steel/quartiers/dome_frequence/gen_placeholders.py` (cadre magenta). Le script ne réécrit pas une entrée déjà en status « v1 ».
Index : `assets/steel/dome_frequence/manifest.json`, chemins `file` relatifs à `assets/`.

## Sols
| fichier | px | usage |
|---|---|---|
| `g_df_marbre.webp` | 512 x 512 | marbre noir veiné du foyer |
| `g_df_moquette.webp` | 512 x 512 | moquette violette des gradins |
| `g_df_scene.webp` | 512 x 512 | plancher noir de la scène |

## Mobilier et décor
| fichier | px | footprint_m | note |
|---|---|---|---|
| `df_scene.webp` | 900 x 360 | 18 x 4 | plateau, éteint |
| `df_ecran_cadre.webp` | 300 x 200 | 6 x 0.5 | cadre vide des écrans de scène (contenu = enseigne) |
| `df_gradin.webp` | 300 x 160 | 6 x 2 | section de gradins, répétable |
| `df_regie.webp` | 220 x 180 | 4 x 4 | console de régie, éteinte |
| `df_enceinte.webp` | 90 x 220 | 1 x 1 | pile d enceintes, x 2 |
| `df_bar.webp` | 320 x 200 | 6 x 2 | bar laiton du foyer |
| `df_vestiaire.webp` | 320 x 220 | 6 x 2 | comptoir du vestiaire |
| `df_banquette.webp` | 140 x 90 | 2 x 1 | banquette velours, x 2 |
| `df_colonne.webp` | 80 x 320 | 1 x 1 | colonne laiton, x 2 |
| `df_borne.webp` | 80 x 150 | 1 x 1 | borne Human Corp de billets |
| `df_cloison.webp` | 300 x 220 | 6 x 0.5 | cloison salle et foyer, répétable |
| `df_porte.webp` | 200 x 240 | 6 x 0.5 | porte de façade, vue de l intérieur |
| `df_verriere.webp` | 900 x 900 | 30 x 30 | verrière vue d en dessous, calque de plafond, sans lueur |

## Enseignes animées
Planches horizontales, images de gauche à droite, lues en boucle (`frames`, `frame_px`, `fps` du manifest). Chaque planche a une version `_mobile` à mi-résolution.

| fichier | images | taille d'une image | planche | cadence | contenu |
|---|---|---|---|---|---|
| `df_ens_ecran_vibes` | 4 | 256 x 144 | 1024 x 144 | 2 i/s | écran de scène 16:9, Vibes (réf. pp_billboard_src) |
| `df_ens_ecran_tron` | 4 | 256 x 144 | 1024 x 144 | 3 i/s | écran de scène 16:9, Tron (réf. pp_holo_tron_src), glitch |
| `df_ens_lumieres` | 6 | 384 x 128 | 2304 x 128 | 6 i/s | rampe de lumières de scène, magenta et cyan, un seul sprite pour toute la rampe |
| `df_ens_verriere` | 4 | 256 x 256 | 1024 x 256 | 1 i/s | lueur ambre de la verrière, calque de plafond semi-transparent |
| `df_ens_bar` | 3 | 192 x 64 | 576 x 64 | 1,5 i/s | néon ambre du bar, pictogramme |
| `df_ens_vu` | 4 | 96 x 64 | 384 x 64 | 8 i/s | VU-mètres de la console |
| `df_ens_facade_vibes` | 4 | 128 x 256 | 512 x 256 | 2 i/s | écran de façade, Vibes, pour b_st_ct_dome (zone steel_center) |
| `df_ens_facade_tron` | 4 | 128 x 256 | 512 x 256 | 3 i/s | écran de façade, Tron, pour b_st_ct_dome (zone steel_center) |

**Plafond mobile [décision] : 8 animations visibles à la fois.**
- Dans `steel_dome` : écran Vibes, écran Tron, rampe de lumières, verrière, bar, VU-mètres = 6. Le bar est dans le foyer, la rampe et les écrans dans la salle : en pratique 4 ou 5 à l'écran.
- Regroupements : toute la rampe de lumières tient dans un seul sprite ; la verrière est un seul calque ; les VU-mètres de la console sont une seule enseigne.
- Les deux écrans de façade sont dans `steel_center` et s'ajoutent aux enseignes déjà présentes dans cette zone : à compter par le développeur.

**Budget mobile [proposition]** : 6 images au plus par enseigne, 192 px au plus de côté en mobile, webp qualité 80, moins de 250 Ko pour les planches mobiles.

## PNJ
| clé | height_m | px | portrait |
|---|---|---|---|
| `gen_df_varenne` | 1.72 | 180 x 512 | oui |
| `gen_df_octave` | 1.78 | 180 x 512 | oui |
| `gen_df_jade` | 1.66 | 180 x 512 | oui |
| `gen_df_nils` | 1.7 | 180 x 512 | oui |
| `gen_df_pia` | 1.64 | 180 x 512 | oui |
| `gen_df_ruben` | 1.88 | 180 x 512 | oui |
| `gen_df_helene` | 1.68 | 180 x 512 | oui |
| `gen_df_gardien` | 1.6 | 180 x 512 | oui |
| `gen_df_foule_a` | 1.7 | 180 x 512 | non |
| `gen_df_foule_b` | 1.66 | 180 x 512 | non |

## Sprites v1 (29/10/2026)

Les 50 entrées du manifest passent en v1. Les enseignes animées pèsent environ 152 Ko en version ordinateur et 69 Ko en version mobile. Les écrans de scène et de façade réutilisent les références de Vibes et de Tron, et aucun visage n'y apparaît hormis le leur. Les lumières de la herse, la lueur de la verrière et les vumètres sont dessinés par le code, ou ajoutés en PIL sur une base éteinte. Aucun faisceau n'est peint dans les images. Planche d'aperçu : /workspace/nml-shots/dome_frequence_sprites.png.
