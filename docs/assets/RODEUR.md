# Rôdeur du désert : sprite gen_rodeur

Branche creation/rodeur. Remplace l emprunt gen_sv_dealer de l ennemi `rodeur` (src/data/combat.js). Description suivie : dialogues_argent.js (homme maigre, lèvres fendues, barre de fer, regarde les bidons et pas le visage) et docs/design/COMBAT.md (un seul adversaire, mêlée, panique vite).

Convention (comme les PNJ gen_*) : webp RGBA, fond transparent, recadré serré, 512 px de haut, pivot bas-centre (pieds), échelle par height_m (environ 50 px/m en jeu). Portrait portrait-gen_rodeur.webp, 192x192. Chaîne : GenerateImage sur fond vert uni, détourage, despill limité à une bande de 4 px au bord.

A brancher (hors de ce lot) : dans src/data/combat.js, `sprite: 'gen_sv_dealer'` devient `sprite: 'gen_rodeur'` ; ajouter l entrée ci-dessous à assets/reused/manifest.json.

```json
 "gen_rodeur": {
  "file": "generated/gen_rodeur.webp",
  "source": "GenerateImage (cursor), b971fb3d",
  "height_m": 1.72,
  "px": [
   195,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, rodeur Dusk-Town"
 }
```
