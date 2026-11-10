# Menu principal « Terminal Human Corp » : implémentation

Notes de Rivet, 10 novembre 2026 (heure de Paris). La direction artistique reste dans `docs/ui/MENU_TERMINAL.md` (fiche d'Ocre), que ce fichier ne remplace pas.

## Fichiers

- `index.html` : structure de `#menu` (classe `term`). Calques dans l'ordre de la fiche : fond de ville (`.t-fond`) < tampon (`#t-tampon`) < texte (`.m-main` : titre, liste, commande EXEC, note, statut, bandeau) < sous-panneaux (`#menu-sub`) < glitch < effets CRT (scanlines, scintillement, vignette, ligne d'allumage) < cadre métal (`#t-cadre`). Le texte, et donc les choix, reste au-dessus du tampon.
- `src/ui/menu_terminal.js` : mise en page, allumage, bandeau, glitch, navigation clavier, lignes de la fiche §6.
- `src/ui/menu_terminal.css` : tout le style du terminal (préfixe `#menu.term`). `src/style.css` n'est pas modifié.
- `src/ui/shell.js` : inchangé sur le fond (sauvegardes, options, mode DEV), branché sur le terminal (`open` / `close` / `confirmer`).
- `tests/menu_rapide.py` : contrôle multi-formats.

IDs et comportements conservés : `#m-resume`, `#m-continue`, `#m-new`, `#m-load`, `#m-options`, `#m-codex`, `#m-credits`, `#m-quit`, `#menu-sub`, `#menu-note`, `#m-version`, la création `[data-race]` / `#cr-next` / `#cr-enter`, la classe `body.menu-open`. La musique de menu reste celle d'avant (ambiance de Dusk-Town, `src/core/ost_centre.js`).

## Choix et actions

| Choix (fiche) | Bouton | Action |
|---|---|---|
| CONTINUER | `#m-continue` | Dernière sauvegarde. Désactivé sans sauvegarde (sous-texte `AUCUNE SESSION ANTERIEURE`, ligne §6.4 au toucher) |
| NOUVELLE PARTIE | `#m-new` | Création de personnage |
| CHARGER | `#m-load` | Sous-panneau des emplacements (CHARGER / SAUVEGARDER en pause) |
| OPTIONS | `#m-options` | Sous-panneau des options |
| CRÉDITS | `#m-credits` | Sous-panneau des crédits |
| QUITTER | `#m-quit` | **Désactivé sur l'écran titre** : le jeu n'a pas d'action « quitter » (un onglet ne se ferme pas par script). Actif en pause : retour à l'écran titre, ligne `SESSION CONSIGNEE...` |

REPRENDRE et CODEX ne sont affichés qu'en pause (fiche §4.2 : hors de la liste de l'écran titre).

## Géométrie : une configuration par variante

`menu_terminal.js` lit `assets/ui/menu_terminal/manifest.json` : clés paysage d'origine, plus l'objet `portrait`. Chaque variante donne canevas, rectangle écran, rayon, cadre, fond, masque et tampon. Un repli intégré reprend les valeurs paysage si le manifeste manque. Une variante n'est utilisée que si son cadre et son fond se chargent.

- **Paysage** (largeur ≥ hauteur) : cadre 1920 × 1080 en `contain` uniforme, centré. Écran 168, 117, 1584 × 821, rayon 54. Tampon 1286, 708, 436 × 232, opacité 0,85.
- **Portrait** (hauteur > largeur, largeur ≥ 390 px) : cadre 1080 × 1920 en `contain` uniforme. Écran 122, 132, 832 × 1625, rayon 60. Tampon 309, 1416, 458 × 243, centré en bas au-dessus du bandeau.
- **Repli plein cadre** (largeur < 390 px, ou échelle du cadre < 0,3) : pas de cadre métal. L'écran occupe toute la fenêtre. Le fond de ville (portrait si la fenêtre est en portrait) est en `cover`, c'est la seule image recadrée. Le tampon est réduit (46 % de la largeur, 220 px au plus) et centré en bas, au-dessus du bandeau. Scanlines, vignette et scintillement restent, en code.

Le cadre n'est jamais étiré de façon non uniforme. Le fond est posé à l'échelle exacte du cadre, aligné sur son canevas, et vu par le rectangle arrondi de l'écran (`overflow:hidden` + `border-radius`, équivalent du masque PNG).

Tailles : valeurs du canevas × échelle (`--k`), avec les planchers en px CSS de la fiche §8.2 (entrées 19 px, titre 44 px, journal 13,5 px, statut et bandeau 11 à 12 px). Cibles des choix : au moins 44 px de haut. Une garde, après chaque mise en page, réduit le tampon (× 0,7), puis le retire s'il touche encore un choix, la note ou un sous-panneau.

## Animation

Allumage (§5.1) piloté par un seul `requestAnimationFrame` le temps de la séquence. Journal tapé à 36 car/s, pause de 60 ms entre les lignes. En portrait : journal de 6 lignes, silences d'allumage raccourcis (× 0,6). Ensuite, plus aucune boucle JS : curseur (530 / 530 ms), scanlines (dérive 3 px en 12 s), scintillement (paliers 96 à 100 %), dérive du fond et bandeau (~45 px/s à l'échelle) sont des animations CSS. Le glitch (120 ms, toutes les 8 à 20 s) est un minuteur unique ; sa bande évite la liste des choix et ne part pas pendant une confirmation.

Saut : toute touche ou tout geste termine l'allumage. Une touche ne fait que sauter. Un geste sur un choix (déjà à sa place, invisible pendant l'allumage) le saute et active ce choix, pour qu'un joueur qui connaît le menu ne perde pas un clic.

Confirmation : flash de 100 ms sur la ligne et commande `> EXEC ...` tapée à 36 car/s sous la liste. **Écart à la fiche :** l'action part tout de suite, sans attendre la fin de la frappe, pour garder un menu réactif.

Pas de boucle hors du menu : en jeu, `#menu` est masqué (`display:none`, plus d'animation CSS) et le minuteur de glitch est coupé. Onglet caché : animations en pause (`animation-play-state`), glitch coupé, allumage terminé.

Mouvement réduit (`prefers-reduced-motion` ou option « Réduire les animations ») : pas d'allumage, pas de scintillement, de glitch, de dérive ni de défilement. Le bandeau affiche un message toutes les 4 s. Le curseur est fixe et la lueur réduite à une couche.

## Lignes de la fiche §6.4 branchées

CONTINUER sans sauvegarde, QUITTER à l'écran titre (« fonction non incluse »), choix grisé, QUITTER en pause, spam de flèches (14 en 2 s), F1 ou frappe libre `AIDE` / `HELP`, commande inconnue (frappe libre de 3 lettres ou plus), cinq appuis sur la version (`MODE MAINTENANCE DEVERROUILLE.`, comportement du mode DEV inchangé).

## Non fait

Sons du terminal (optionnels, non livrés). Menu pause rendu dans le même terminal, sans rallumage, mais sans réécriture animée des lignes. Courbure du tube : non, vignette seulement.
