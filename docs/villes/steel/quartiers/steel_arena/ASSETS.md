# Steel Arena : assets à produire

Mêmes conventions que `frequence_strip/ASSETS.md`. Tout est **[proposition]** d'Ocre ; tailles des décors estimées à 50 px/m.

## Conventions
- webp RGBA, fond transparent ; PNJ 512 px de haut, pivot bas-centre ; bâtiments avec `anchor` au point avant bas ; sols 512 x 512 (`tile_m` 4).
- Préfixes : `g_ar_` sols, `ar_` bâtiments et mobilier, `ar_ens_` enseignes animées, `gen_ar_` PNJ, `portrait-gen_ar_<id>` portraits (192 x 192, fond (58,44,32)).
- Zone `steel_arena` [décision], entrée ouest par la grille `fs_grille_est` du Strip [décision].

## Placeholders et manifest
48 fichiers dans `assets/steel/steel_arena/`, générés par `docs/villes/steel/quartiers/steel_arena/gen_placeholders.py` (cadre magenta). Le script ne réécrit pas une entrée déjà en status « v1 ».
Index : `assets/steel/steel_arena/manifest.json`, chemins `file` relatifs à `assets/`.

## Sols
| fichier | px | usage |
|---|---|---|
| `g_ar_parvis.webp` | 512 x 512 | grandes dalles du parvis |
| `g_ar_parvis_mouille.webp` | 512 x 512 | parvis mouillé, reflets violets et cyan |
| `g_ar_ligne_file.webp` | 512 x 512 | dalle avec ligne de file lumineuse cyan |

## Bâtiments et mobilier
| fichier | px | footprint_m | note |
|---|---|---|---|
| `ar_arena.webp` | 1400 x 900 | 48 x 12 | dôme, sans écrans ni fronton (animés à part) |
| `ar_entree.webp` | 420 x 360 | 8 x 2 | entrée vitrée, portes |
| `ar_portique.webp` | 200 x 220 | 2 x 1 | portique Human Corp, x 4 |
| `ar_barriere.webp` | 220 x 120 | 4 x 0.5 | barrière chromée, répétable |
| `ar_projecteur.webp` | 160 x 300 | 2 x 2 | tour de projecteur, sans faisceau |
| `ar_lampadaire.webp` | 80 x 300 | 0.6 x 0.6 | lampadaire, x 4 |
| `ar_guichets.webp` | 220 x 260 | 4 x 4 | cabine vitrée |
| `ar_merch.webp` | 220 x 260 | 4 x 4 | merch officiel |
| `ar_securite.webp` | 220 x 240 | 4 x 4 | poste Human Corp |
| `ar_regie.webp` | 340 x 240 | 6 x 4 | camion régie |
| `ar_panneau_nml.webp` | 120 x 220 | 2 x 0.5 | panneau en pictogramme, phrase affichée par le code |
Réemploi : caméra `steel/pulse_plaza/pp_camera.webp`.

## Enseignes animées
Planches horizontales, images côte à côte de gauche à droite, lues en boucle (`frames`, `frame_px`, `fps` dans le manifest). Chaque planche a une version `_mobile` à mi-résolution.

| fichier | images | taille d'une image | planche | cadence | contenu |
|---|---|---|---|---|---|
| `ar_ens_ecran_vibes` | 4 | 256 x 144 | 1024 x 144 | 2 i/s | écran du dôme, Vibes en concert |
| `ar_ens_ecran_tron` | 4 | 256 x 144 | 1024 x 144 | 3 i/s | écran du dôme, Tron, glitch |
| `ar_ens_fronton` | 4 | 384 x 96 | 1536 x 96 | 3 i/s | fronton sans texte, onde violette |
| `ar_ens_faisceau` | 6 | 128 x 256 | 768 x 256 | 6 i/s | faisceau qui balaie (x 4 projecteurs) |
| `ar_ens_coeurs` | 4 | 64 x 64 | 256 x 64 | 4 i/s | bâton-cœur des fans |
| `ar_ens_guichet` | 2 | 96 x 64 | 192 x 64 | 1 i/s | écran du guichet |
| `ar_ens_human_corp` | 3 | 128 x 128 | 384 x 128 | 1,5 i/s | logo abstrait Human Corp |

**Plafond mobile [décision] : 8 animations visibles à la fois.** Inventaire si tout est posé : 2 écrans + 1 fronton + 4 faisceaux + 1 guichet + 1 logo + cœurs dans la file = plus de 8. Règle proposée : les 4 faisceaux comptent pour 1 (même planche, même horloge, décalés d'une image) ; les cœurs de la file comptent pour 1 (une seule instance animée, les autres figées sur l'image 1). On arrive à 7, ce qui laisse 1 place.
**Budget mobile [proposition]** : au plus 6 images par enseigne, images mobiles de 192 px au plus de côté, webp qualité 80, moins de 250 Ko pour toutes les planches mobiles.

## PNJ
| clé | height_m | px | portrait |
|---|---|---|---|
| `gen_ar_ferrand` | 1.90 | 180 x 512 | oui |
| `gen_ar_anouk` | 1.64 | 180 x 512 | oui |
| `gen_ar_zelie` | 1.60 | 180 x 512 | oui |
| `gen_ar_malik` | 1.80 | 180 x 512 | oui |
| `gen_ar_ines` | 1.62 | 180 x 512 | oui |
| `gen_ar_clem` | 1.72 | 180 x 512 | oui |
| `gen_ar_garnier` | 1.82 | 180 x 512 | oui |
| `gen_ar_bastien` | 1.76 | 180 x 512 | oui |
| `gen_ar_laure` | 1.58 | 180 x 512 | oui |
| `gen_ar_foule_a` | 1.70 | 180 x 512 | non |
| `gen_ar_foule_b` | 1.66 | 180 x 512 | non |
