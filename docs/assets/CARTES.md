# Cartes de l interface (lots 2 et 3)

Suit docs/design/INTERFACE.md §4 (branche docs/regie-interface, 8e70070). Dessin déterministe par `tools_cartes.py` (pas de génération d image : la géographie reste exacte). Fonds sans texte ; les noms sont affichés par le code. Index : `assets/ui/maps/manifest.json`.

## No Man's Land
- `assets/ui/maps/nml_fond.webp` 2200 × 2000 px (ordinateur), `nml_fond_mobile.webp` 1100 × 1000 px (allégée).
- Recalé sur la grille de la maquette v0.13 (`dist/world.js` : CONTINENT, WORLD_GRID 22 × 20, 50 unités par case) : 1 case = 100 px (50 px en mobile). px = unités maquette × 2.
- Case → px : coin (col × 100, row × 100), centre + 50. px → case : col = floor(x / 100), row = floor(y / 100).
- Le manifest liste les 167 cases terrestres (col, row, libellé A01, biome de la maquette : desert, rock, forest, glass, coast) et les 13 grands lieux (case et px).
- Peint : contour côtier, mer sombre, biomes, cordillère, forêt occidentale, cratère et retombées de Big Larry, lits asséchés, pistes en pointillés (terrain « piste »), masse du sarcophage.

## Steel-Megalopolis
- 4 planches 1600 × 1200, même cadrage (sarcophage : ellipse centre 800, 610, demi-axes 700 × 500) : `steel_1_sous_ville`, `steel_2_lower_town`, `steel_3_center_town`, `steel_4_upper_town` (désaturée, verrouillée).
- Palette bleu acier (retour Valentin 29/10, contraste avec le désert ambre) : rampe nuit, bleu acier, gris-bleu, cyan froid pâle, sans néon ; Upper-Town en gris-bleu désaturé. Option `PALETTE = 'bleu'` ou `'ambre'` dans tools_cartes.py (l ambre de 3556d7d reste reproductible).
- Repères proposés par couche (px) dans le manifest (`reperes_px_proposition`) : lieux, sorties, liens entre couches ; un lien garde les mêmes x, y d une couche à l autre.

## Icônes de lieux
`assets/ui/maps/icones/` : SVG + PNG 24 et 48 px, ambre `#f2b44a` sur fond sombre : `lieu_decouvert`, `lieu_non_decouvert`, `joueur`, `sortie`, `lien_couches`, `verrouille` (Upper-Town).
Variante bleue pour la carte Steel (`#a9d2e6`, fond `#060a10`), mêmes noms suffixés `_steel` (ex. `lieu_decouvert_steel_24.png`), entrée `icones_lieux_steel` du manifest. Les ambres restent pour la carte NML.

## Brouillard de guerre (carte NML)
Décision de Valentin (29/10) : les cases et les lieux pas encore vus restent sous un brouillard, que le joueur dissipe autour de son trajet. Fichiers produits par `tools_brouillard.py` (seed fixe), entrée `brouillard_nml` du manifest.
- `assets/ui/maps/fog/nml_brouillard.webp` (et `.png`) 512 × 512 px : brume de poussière ambre sombre, tuilable sans raccord. Version mobile `nml_brouillard_mobile` 256 × 256 px.
- `assets/ui/maps/fog/nml_brouillard_masque.png` 300 × 300 px : blanc dont l alpha donne la force d effacement, plein sur la case, fondu doux sur la case voisine. Version mobile `nml_brouillard_masque_mobile.png` 150 × 150 px.
- Usage conseillé : remplir un calque au-dessus du fond avec la texture en motif répété, opacité 0,94 environ. Pour chaque case vue (la case du trajet et ses 8 voisines), dessiner le masque centré sur le centre de la case en `destination-out`. Les icônes et les noms des lieux restent cachés tant que leur case est dans le brouillard.
- Aperçu (maquette) : /workspace/nml-shots/brouillard.png

## Décisions prises (à valider)
- Disposition de Steel déduite des jonctions du code : douane à l ouest, Center-Town au centre (dalle surélevée), Lower-Town à l est (la Descente), Asia-Ground au sud de Lower-Town, China Lake au sud d Asia-Ground (sortie nord de China Lake vers Asia-Ground) et reliée à Lower-Town par une ruelle ; lac de Lower Street au nord-est. Sous-Ville : Les Poutres sous la douane (trappe), La Cuve à l est, monte-charge sous Center-Town, deux routes de sortie (ouest, sud).
- Sur la couche Lower-Town, l emprise de Center-Town est une ombre sur piliers (la dalle est au-dessus).
- Les lieux NML et leurs noms viennent de la maquette v0.13 (`dist/data.js`), lue dans l archive `src/a.zip` sans modification ; la Sous-Ville n y est pas une case séparée.
- Fonds sans grille peinte : la grille est tracée par le code.

## Questions ouvertes
- Positions des quartiers dans Steel : proposition, à confirmer par Valentin (aucun plan topographique canon).
- Le canon du repo place-t-il d autres grands lieux NML (Junk-Burgh est repris de la maquette) ?
- Biomes et coûts : la fiche propose des terrains (piste, plaine, relief, forêt, irradié) ; le manifest donne les 5 biomes de la maquette, la correspondance reste à fixer par Rivet et Régie.

Planches (maquettes) : /workspace/nml-shots/carte_steel.png, /workspace/nml-shots/carte_nml.png
