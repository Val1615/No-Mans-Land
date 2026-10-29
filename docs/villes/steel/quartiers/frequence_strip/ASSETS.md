# Fréquence Strip : assets à produire

Mêmes conventions que `pulse_plaza/ASSETS.md`. Tout est **[proposition]** d'Ocre ; les tailles des décors sont estimées à 50 px/m.

## Conventions
- webp RGBA, fond transparent ; PNJ 512 px de haut, pivot bas-centre ; bâtiments avec `anchor` au point avant bas ; sols 512 x 512 tuilables (`tile_m` 4).
- Préfixes : `g_fs_` sols, `fs_` bâtiments et mobilier, `fs_ens_` enseignes animées, `gen_fs_` PNJ, `portrait-gen_fs_<id>` portraits (192 x 192, fond (58,44,32)).
- Zone `steel_strip` [décision], entrée ouest depuis la sortie est de Pulse Plaza [décision].

## Placeholders et manifest
49 fichiers dans `assets/steel/frequence_strip/`, générés par `docs/villes/steel/quartiers/frequence_strip/gen_placeholders.py` (cadre magenta). Le script ne réécrit pas une entrée déjà passée en status « v1 ».
Index : `assets/steel/frequence_strip/manifest.json`, chemins `file` relatifs à `assets/`.

## Sols
| fichier | px | usage |
|---|---|---|
| `g_fs_asphalte_mouille.webp` | 512 x 512 | chaussée mouillée, reflets magenta et violets |
| `g_fs_trottoir.webp` | 512 x 512 | trottoir en dalles sombres |
| `g_fs_grille_vapeur.webp` | 512 x 512 | grille d'aération au sol |

## Bâtiments et mobilier
| fichier | px | footprint_m | note |
|---|---|---|---|
| `fs_neon7.webp` | 600 x 500 | 12 x 6 | Club Neon-7, sans enseigne (elle est animée à part) |
| `fs_corestack.webp` | 600 x 560 | 12 x 6 | Core Stack, baies empilées |
| `fs_retour.webp` | 400 x 360 | 8 x 6 | bar Le Retour |
| `fs_capsules.webp` | 300 x 420 | 6 x 6 | hôtel capsule |
| `fs_facade_nord.webp` | 400 x 420 | 8 x 6 | façade générique, côté nord, répétable |
| `fs_facade_sud.webp` | 400 x 360 | 8 x 6 | façade générique, côté sud, répétable |
| `fs_stand_brochettes.webp` | 200 x 220 | 4 x 4 | stand de rue, ambre |
| `fs_stand_merch.webp` | 200 x 220 | 4 x 4 | merch pirate |
| `fs_tapis.webp` | 200 x 110 | 4 x 2 | tapis rouge et cordon |
| `fs_grille_est.webp` | 200 x 220 | 4 x 1 | grille qui ferme le bout de rue |
Réemploi : la caméra C.A.G.E. reprend `steel/pulse_plaza/pp_camera.webp`, le GT de promotion peut reprendre `gen_pp_clone_gt` si on veut économiser un sprite.

## Enseignes animées
Planches horizontales : les images sont côte à côte, de gauche à droite, toutes de la même taille, lues en boucle. Le code découpe la planche avec `frames` et `frame_px` du manifest et affiche une image toutes les `1 / fps` secondes.
Chaque planche a une version `_mobile` à mi-résolution (mêmes images, même cadence).

| fichier | images | taille d'une image | planche | cadence | contenu |
|---|---|---|---|---|---|
| `fs_ens_neon7` | 4 | 256 x 128 | 1024 x 128 | 4 i/s | logo Neon-7, allumage par segments |
| `fs_ens_corestack` | 6 | 192 x 192 | 1152 x 192 | 6 i/s | baies qui défilent, lumière cyan |
| `fs_ens_vibes` | 4 | 128 x 256 | 512 x 256 | 2 i/s | écran vertical, Vibes à l'écran |
| `fs_ens_tron` | 4 | 128 x 256 | 512 x 256 | 3 i/s | écran vertical, Tron à l'écran, glitch |
| `fs_ens_coeur` | 6 | 96 x 96 | 576 x 96 | 8 i/s | cœur néon qui bat |
| `fs_ens_retour` | 3 | 192 x 64 | 576 x 64 | 1,5 i/s | néon ambre du bar, grésillement |
| `fs_ens_capsules` | 2 | 96 x 192 | 192 x 192 | 1 i/s | hublots qui s'allument |
| `fs_vapeur` | 4 | 80 x 200 | 320 x 200 | 6 i/s | panache de vapeur (sol), semi-transparent |
Mobile : mêmes noms suffixés `_mobile`, images à mi-taille (ex. `fs_ens_neon7_mobile` : 4 x 128 x 64, planche 512 x 64).

**Budget mobile [proposition].** Au plus 6 images par enseigne, aucune image au-dessus de 128 px de côté en mobile, webp avec perte (qualité 80). Cible : moins de 250 Ko pour les 8 planches mobiles réunies, moins de 800 Ko en version ordinateur. Pas plus de 8 animations visibles en même temps ; hors champ, le code les met en pause. Si l'appareil est lent, l'enseigne reste sur sa première image.
Placement des enseignes : 4 en façade nord (Neon-7, Core Stack, Vibes, cœur), 2 en façade sud (Retour, capsules), Tron entre le Neon-7 et le Core Stack ; positions exactes à fixer avec le développeur.

## PNJ
| clé | height_m | px | portrait |
|---|---|---|---|
| `gen_fs_rocco` | 1.95 | 180 x 512 | oui |
| `gen_fs_lila` | 1.68 | 180 x 512 | oui |
| `gen_fs_hugo` | 1.74 | 180 x 512 | oui |
| `gen_fs_okoro` | 1.70 | 180 x 512 | oui |
| `gen_fs_tibo` | 1.66 | 180 x 512 | oui |
| `gen_fs_yun` | 1.72 | 180 x 512 | oui |
| `gen_fs_gt_promo` | 1.85 | 180 x 512 | oui |
| `gen_fs_sacha` | 1.78 | 180 x 512 | oui |
| `gen_fs_marius` | 1.70 | 180 x 512 | oui |
| `gen_fs_foule_a` | 1.72 | 180 x 512 | non |
| `gen_fs_foule_b` | 1.66 | 180 x 512 | non |
