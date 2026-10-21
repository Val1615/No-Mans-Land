# No Man's Land (prototype)

RPG tactique narratif en vue isométrique, 2175. Ce dépôt contient la reconstruction en 3D orthographique (Three.js, site statique) : premier quartier de Dusk-Town, « La Pompe ».

**Jouer :** https://val1615.github.io/No-Mans-Land/

## Contrôles
- Souris : clic au sol pour marcher, clic sur une porte pour entrer ou sortir, clic sur un personnage pour lui parler.
- Tactile : un appui fait la même chose ; le bouton d'action en bas sert à entrer ou sortir.
- Le compagnon (Nilo) suit et passe les portes avec vous.

## Statut
Prototype. Bâtiments : sprites entiers de la maquette (v4). Intérieurs (v6) : sols et murs en textures réelles, mobilier en sprites contrôlés à l'angle de la caméra (maquette d'abord, sinon générés ; provenance dans `docs/ASSETS_CATALOGUE.md`). Les dialogues sont des propositions à relire.

## Local
`python3 -m http.server 8765` à la racine, puis ouvrir http://localhost:8765/. Recette navigateur : `tests/dusk_q1_check.py`, `tests/flip_pixels.py`, `tests/interiors_pixels.py` (Playwright, contrôles sur pixels rendus).

## Documentation
Voir [docs/](docs/) : `JOURNAL.md`, `CANON_ARBITRAGES.md`, `DECISION_TECHNIQUE.md`, `quartiers/DUSK_TOWN_Q1.md`, `ASSETS_CATALOGUE.md`.
