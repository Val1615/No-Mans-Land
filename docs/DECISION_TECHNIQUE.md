# Décision technique : 3D orthographique (Three.js) plutôt que 2,5D pré-rendue

Rédigé le 21 octobre 2026 (heure de Paris). Valentin m'a délégué ce choix.

## 1. Contraintes
- Diffusion web statique, avec tactile mobile obligatoire.
- Développeur solo, assets générés par IA.
- Défauts racines à rendre impossibles par construction :
  - image utilisée comme géométrie ;
  - facteurs d'échelle empilés ;
  - décalage entre porte et collision ;
  - transparence d'occultation bricolée.

## 2. Comparaison

| Critère | 2,5D (sprites peints sur grille iso) | 3D orthographique (Three.js) |
|---|---|---|
| Source de vérité spatiale | Deux vérités : l'image et une emprise saisie à la main. C'est exactement l'erreur de la v0.13 | Une seule : le volume en mètres sert au rendu, à la collision et à la sélection |
| Porte, seuil et collision | Coordonnées à recaler sur chaque image et chaque miroir | La porte est un objet placé sur la façade du volume ; seuil et collision s'en déduisent |
| Échelle | Dépend de la résolution et du cadrage de chaque génération IA (tailles de 165 à 1774 px observées dans la v0.13) | Imposée par le maillage. Une texture IA ne peut pas changer la taille |
| Occultation | Découpe par sprite, ordre de tri, masques à fabriquer | Lancer de rayon caméra vers personnage, puis opacité du maillage (démontré dans la scène d'étalonnage) |
| Orientations | Une image par angle, et le miroir inverse lumière et porte | Rotation libre, éclairage cohérent |
| Assets IA | Très adapté pour le « joli » immédiat, mais angle, pivot et échelle ne sont pas maîtrisés | Les textures IA (façades, matériaux) s'appliquent sur des volumes simples ; modèles low-poly en option ; des sprites restent possibles pour les petits objets, posés sur une emprise en mètres |
| Look « Fallout 1 et 2 » | Natif | Atteignable : caméra iso fixe, textures peintes, éclairage cuit |
| Web et mobile | Léger | WebGL est disponible partout ; une scène simple tourne même en rendu logiciel (vérifié en headless). Performance sur vrai téléphone **non mesurée** |
| Outillage solo | Peu de dépendances | Three.js : une seule bibliothèque, sans éditeur imposé. Godot est plus lourd en export web (taille, démarrage) et moins direct pour le DOM et l'interface |

**Choix : 3D orthographique avec Three.js** (version 0.170, modules ES, sans étape de build pour l'instant).

**Critères décisifs**
1. Une seule géométrie fait foi pour le rendu, la collision, la sélection et les portes. Cela supprime les causes P0 de la v0.13.
2. L'échelle est imposée en mètres.
3. L'occultation est triviale.
4. L'interface reste en HTML/CSS par-dessus le canvas, ce qui facilite l'accessibilité, la personnalisation et le tactile.

**Pourquoi pas Godot.** C'est un bon moteur, mais l'export web est plus lourd et l'intégration d'une interface DOM accessible plus indirecte. Il devient à reconsidérer si l'on vise une version native.

**Risques**
- Le rendu « peint » demande un travail de matériaux et d'éclairage.
- Les modèles 3D ne sortent pas directement des générateurs d'images.
- Mitigation : un kit modulaire de volumes en mètres (murs, portes, toits) habillé de textures générées, et des sprites autorisés seulement pour les petits props avec une emprise déclarée.

## 3. Référentiel spatial commun (`game/src/data/units.js`)

| Élément | Valeur |
|---|---|
| Unité monde | **1 unité = 1 mètre** |
| Grille de navigation et collision | Cases de 0,5 m ; centre de case = multiple de 0,5 m |
| Personnage | Hauteur 1,8 m, rayon de collision 0,3 m (les volumes sont dilatés de ce rayon) |
| Porte piétonne | Largeur 1,0 m, hauteur 2,2 m. Seuil praticable à 1,0 m devant l'ouverture, sur la normale de façade |
| Porte de fret (à ajouter) | Largeur 3,0 m, hauteur 3,5 m |
| Étage | 3,0 m ; mur 0,2 m |
| Bâtiment | Emprise et hauteur en mètres, multiples de 0,5 m |
| Parcelle | Module de 4 m (une parcelle fait n × 4 m) |
| Rue | Largeur minimale 6 m, trottoir 1,5 m |
| Caméra | Orthographique, lacet 45°, tangage 35,264° (iso vraie). 34 px/m sur bureau, 26 px/m sur mobile. Suit le joueur |
| Compagnon | Distance de suivi 1,5 m ; distance maximale pour passer une porte avec le groupe : 6 m |
| Vitesse de marche | 3 m/s |

**Règles**
- Aucun facteur d'échelle par famille.
- Une variante d'asset est validée dans la scène d'étalonnage avant toute utilisation.
- La porte est définie une seule fois (`DOORS`) : ouverture, seuil, cible, retour, conditions.
- Les commandes renvoient un refus typé (`chemin_bloque`, `porte_absente`, condition...).

## 4. Architecture retenue (scène d'étalonnage)
- `src/data/` : définitions immuables (unités, lieux, portes).
- `src/core/` : grille dérivée des volumes, A*, état sérialisable, commandes. Aucune dépendance au rendu.
- `src/render/` : Three.js. Lit l'état, ne contient aucune règle.
- `src/input/` : Pointer Events (souris, toucher et stylet par le même chemin).
- `tests/browser_check.py` : vérification en vrai navigateur (Chrome headless, Playwright).
