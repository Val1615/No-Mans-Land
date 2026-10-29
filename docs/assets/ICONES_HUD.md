# Icônes de la barre HUD

Dossier `assets/ui/icons/` : 11 icônes en SVG (viewBox 24, trait 1,75, ambre `#f2b44a` = `--c` de src/style.css, fond transparent) et exports PNG 64 et 128 px (`<clé>_64.png`, `<clé>_128.png`). Index : `assets/ui/icons/manifest.json` (clé, fichiers, touche suggérée).

| Clé | Touche | Dessin |
|---|---|---|
| menu | Échap | trois traits |
| sac | I | sac à dos |
| journal | J | carnet à reliure, lignes |
| carte | M | carte pliée en trois |
| son_on / son_off | S | haut-parleur avec ondes / barré d une croix |
| discret_on / discret_off | H | œil fermé (furtif) / œil ouvert |
| entrer | E (suggestion) | porte et flèche entrante, pour le bouton contextuel |
| replier / deplier | Tab (suggestion) | barre et chevron bas / haut |

Monochromes, sans néon ni lueur : la couleur peut être reprise en CSS (SVG inline avec `stroke="currentColor"` si besoin, en remplaçant la valeur). Lisibles à partir de 20 px.

Planche (maquette, pas une capture) : /workspace/nml-shots/icones_hud.png
