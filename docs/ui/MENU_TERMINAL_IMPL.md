# Menu principal « Terminal Human Corp » : implémentation

Notes de Rivet, 10 novembre 2026 (heure de Paris). La direction artistique reste dans `docs/ui/MENU_TERMINAL.md` (fiche d'Ocre), que ce fichier ne remplace pas.

## Fichiers

- `index.html` : structure de `#menu` (classe `term`). Calques dans l'ordre de la fiche : fond de ville (`.t-fond`) < tampon (`#t-tampon`) < texte (`.m-main` : titre, liste, commande EXEC, note, statut, bandeau) < sous-panneaux (`#menu-sub`) < glitch < effets CRT (scanlines, scintillement, vignette, ligne d'allumage) < cadre métal (`#t-cadre`). Le texte, et donc les choix, reste au-dessus du tampon. Le `body` porte `menu-open` dès le HTML, et `#menu` est déjà en `term booting b-off` : dès la première image, le HUD, la barre d'icônes et le monde sont cachés, l'écran est celui du Terminal éteint.
- `src/lancement.js` : point d'entrée. Ouvre le Terminal dès que son code et ses calques sont prêts, puis charge `main.js` en arrière-plan. Le catalogue et le rendu de Center-Town ne bloquent plus l'écran titre. L'allumage, sautable, est inchangé.
- Optimisation du lancement (12/11) : dès le HTML, ligne d'attente ambre du Terminal (`#t-attente`, classe `t-attend`) tant que le cadre et le fond de l'orientation affichée ne sont pas chargés (l'autre orientation : au besoin, à la rotation). Le repli plein cadre reste réservé à < 390 px, au cadre trop mince et aux images introuvables, jamais comme état d'attente. `main.js` n'est importé qu'une fois le cadre posé. La ligne sous CONTINUER est lue dans localStorage par `lancement.js` (même format que `shell.js`, préfixe DEV respecté) ; la musique du menu part au premier geste sur `<audio id="music">` (`preload="none"`), reprise sans coupure par `ost_centre.js`. Ouvrir une partie garde le Terminal à l'écran (classe `t-charge`, choix gelés) avec le monogramme NML dans `#menu-note`, jusqu'à ce que le lieu ait ses images.
- Monogramme NML (12/11, proposition B d'Ocre choisie par Valentin) : `src/ui/monogramme.js` dessine en canvas (devicePixelRatio) la géométrie de `mark_mono()` (hexagone 108 / 96, anneau 118, « NML » en VT, légende Plex `SECTEUR   n %`, `n %` seul si la place manque). Entrée ~1 s (hexagone tracé, lettres allumées), puis l'anneau suit le vrai progrès du lieu (`chargeur.lieu` : fait / total). Terminal : sous les choix gelés et la ligne EXEC, dans la bande libre au-dessus du statut (paysage) ou du bandeau (portrait), sans croiser de texte. En jeu (`#chargement`) : badge en bas, centre de l'anneau à 75,7 % de la hauteur, opacité 0,96, sans plaque. Mouvement réduit : hexagone et lettres déjà là, seul l'anneau avance. Texte lu (secteur + %, par paliers de 10 %) dans l'élément `role=status`.
- `src/core/chargement.js` : images du jeu chargées par lieu (clés trouvées dans le lieu, ses portes et PNJ, puis calques, vues de dos et sols de base), d'abord le lieu d'entrée (préchargé pendant le menu : lieu de la dernière sauvegarde, sinon départ), le reste en arrière-plan après l'entrée en jeu. En jeu, un lieu pas encore chargé affiche la même ligne (`#chargement`) et n'est construit qu'une fois prêt. Fichiers et URL inchangés.
- `src/ui/menu_terminal.js` : mise en page, allumage, bandeau, glitch, navigation clavier, lignes de la fiche §6.
- `src/ui/menu_terminal.css` : tout le style du terminal (préfixe `#menu.term`).
- `src/ui/shell.js` : sauvegardes, options, mode DEV, branché sur le terminal (`open` / `close` / `confirmer`). Réutilise le terminal déjà ouvert par `lancement.js`, sans relancer l'allumage.
- `tests/menu_rapide.py`, `tests/nml_boot.py` : contrôle multi-formats, premier cadre sans vestige, Terminal indépendant du rendu de la carte.
- Cinématique d'ouverture et OST du menu (13/11, fichiers de Valentin, servis identiques à l'octet) : voir « Cinématique d'ouverture » plus bas. `src/ui/cinematique.js`, `assets/video/cinematique_ouverture.mp4`, `assets/audio/ost_menu/01_ost_menu.mp3`, `tests/cinematique.py`.

IDs et comportements conservés : `#m-resume`, `#m-continue`, `#m-new`, `#m-load`, `#m-options`, `#m-codex`, `#m-credits`, `#m-quit`, `#menu-sub`, `#menu-note`, `#m-version`, la création `[data-race]` / `#cr-next` / `#cr-enter`, la classe `body.menu-open`. Musique du menu (13/11) : OST du menu de Valentin (`assets/audio/ost_menu/01_ost_menu.mp3`) en boucle sur l'écran titre et la création, mode `menu` de `src/core/ost_centre.js` ; l'ambiance de Dusk-Town reste pour le jeu.

## Cinématique d'ouverture (13/11)

Demande de Valentin : sa cinématique (splash du studio, 12,87 s, 1280×720 avec son) « dans le terminal au tout début », puis l'OST du menu.

- **Décision avant la première image** (`index.html`, script en ligne juste après `<body>`) : la page pose `html.intro` et le `src` de `#intro-video`. Sautée avec `?intro=0`, avec `?dev=1&map=…`, et pour un navigateur piloté (`navigator.webdriver`, toutes les suites de tests) sauf `?intro=1`. Le joueur la voit à chaque chargement de page ; jamais au retour à l'écran titre depuis le jeu (QUITTER), puisqu'elle ne vit que dans `lancement.js`.
- **Affichage** : `#intro` en `position:fixed`, `z-index:90` au-dessus de tout, fond noir ; vidéo `object-fit: contain` (bandes noires en portrait 390 / fold 412 et 884, en haut et en bas en 1280×800 ; jamais d'étirement), `playsinline`, `preload="auto"`. Le Terminal n'est pas visible derrière.
- **Son et autoplay** : `play()` avec son tout de suite. Si le navigateur refuse (`NotAllowedError`, cas courant), invite ambre semi-transparente au centre sur noir, « ▸ TOUCHER POUR COMMENCER » (VT, 0,62, pulsation lente, fixe en mouvement réduit) ; le premier geste (tap / clic / touche) lance la vidéo **avec son**. Si l'autoplay est permis, pas d'invite. Geste très tôt (avant que le refus de l'autoplay soit tombé, le navigateur rejette alors toutes les lectures en attente) : réponses d'un essai dépassé ignorées, relance unique si le geste est encore actif (`navigator.userActivation.isActive`), sinon retour à l'invite.
- **Passer** : « PASSER ▸ » discret en bas à droite pendant le chargement et la lecture ; clic, tap, Échap, Entrée, Espace passent (fondu noir 0,4 s, le son de la vidéo baisse avec le voile). Tous les gestes sont captés au premier niveau (`window`, capture, `stopImmediatePropagation`) tant que la cinématique est là : ni le menu, ni la musique, ni l'allumage ne les voient (le clic qui passe ne choisit rien).
- **Fondus** (le fichier finit sur une image claire, sans fondu) : voile CSS noir `#intro-voile`. Entrée 0,15 s depuis le noir à `playing` ; fin naturelle : voile noir sur les 0,6 dernières secondes (suivi de `currentTime` par rAF, minuteur de secours si l'onglet est caché) ; puis le calque est retiré et le Terminal s'allume depuis le noir comme d'habitude. Le son du fichier n'est jamais touché en fin naturelle.
- **Préchargement non bloqué** : pendant la cinématique, `lancement.js` continue comme avant (cadre du Terminal, puis `main.js`, catalogue, lieu de CONTINUER). Seul `term.open()` est retenu (enveloppé : l'appel de `lancement.js` comme celui du shell est rejoué à la fin), et `__nmlMenuPret` n'est posé qu'à l'allumage réel. Au passage, le Terminal est donc déjà prêt (pas de ligne d'attente) et Continuer reste rapide.
- **Échecs** : erreur vidéo (404, format, y compris avant le chargement du module) → Terminal tout de suite. Rien à l'écran 8 s après le lancement de la lecture → Terminal. Jamais d'écran noir sans retour (l'invite, elle, attend un geste).
- **Mouvement réduit** : cinématique gardée (c'est le contenu de Valentin), passable ; l'allumage du Terminal est sauté comme d'habitude.
- **OST du menu** : à la fin (naturelle, passage ou échec), `lancement.js` démarre `<audio id="music">` (OST du menu, `loop`, `preload="none"`) : par `window.__nml.demarrerMusique()` si `main.js` est prêt (volume réglé d'emblée, sans brancher l'analyseur Web Audio), sinon directement. Volume `0,55 × réglage Musique`, muet `nml_muted` respecté. Si le navigateur refuse quand même (échec vidéo sans geste), l'OST part au premier geste comme avant. `ost_centre.js` : mode `menu` tant que le shell est en `title` ou `create` (pas en `pause`), retour au lieu en jeu, reprise de l'OST du menu (à sa position) au retour à l'écran titre.
- **État exposé** (tests) : `window.__nmlIntro = { etat: chargement | invite | lecture | fondu | fini, fin: naturelle | passee | erreur | absente, mode: autoplay | geste }`, `window.__nmlIntroActive`.
- **Tests** : `tests/cinematique.py` (hash servis, invite / geste / lecture avec son / passage par chaque touche et tap / Terminal depuis le noir / OST en boucle, réglages son, échec 404, mouvement réduit, autoplay permis avec fin naturelle et voile, pas de rejeu en session, rejeu au rechargement, bandes noires et captures 1280 / 390 / fold 412 / 884 ; un processus et un navigateur par scénario) ; `tests/nml_boot.py` §3, `tests/menu_chargement.py` §11, `tests/menu_rapide.py` (élément audio).

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

- **Paysage** (largeur ≥ hauteur) : cadre 1920 × 1080 en `contain` uniforme, centré. Écran 168, 117, 1584 × 821, rayon 54. Tampon recalé dans le code (le manifeste n'est pas modifié) : x = 1350, y = 590, w = 370, proportions du PNG conservées (h ≈ 197), opacité 0,85.
- **Portrait** (hauteur > largeur, largeur ≥ 390 px) : cadre 1080 × 1920 en `contain` uniforme. Écran 122, 132, 832 × 1625, rayon 60. Tampon 309, 1416, 458 × 243, centré en bas au-dessus du bandeau.
- **Repli plein cadre** (largeur < 390 px, ou échelle du cadre < 0,3) : pas de cadre métal. L'écran occupe toute la fenêtre. Le fond de ville (portrait si la fenêtre est en portrait) est en `cover`, c'est la seule image recadrée. Le tampon est réduit (46 % de la largeur, 220 px au plus) et centré en bas, au-dessus du bandeau. Scanlines, vignette et scintillement restent, en code.

Le cadre n'est jamais étiré de façon non uniforme. Le fond est posé à l'échelle exacte du cadre, aligné sur son canevas, et vu par le rectangle arrondi de l'écran (`overflow:hidden` + `border-radius`, équivalent du masque PNG).

Tailles : valeurs du canevas × échelle (`--k`), avec les planchers en px CSS de la fiche §8.2 (entrées 19 px, titre 44 px, journal 13,5 px, statut et bandeau 11 à 12 px). Cibles des choix : au moins 44 px de haut. Le tampon est décoratif et cède toujours. Il garde au moins 24 px (canevas de base, × échelle) de marge avec les choix, le bandeau, « proto v15 », le statut, la note, la commande EXEC et un sous-panneau ouvert. S'il manque de la place, une garde le réduit par paliers de 5 % (ancré au centre, puis en bas, puis en haut), jusqu'à 40 %, et ne le retire qu'en dernier recours. Le texte ne bouge jamais. La garde repasse à chaque mise en page, rendu ou nouvelle note. Au moment du lot correctif : taille nominale en 1920, 1280, 360 et Fold déplié ; × 0,6 en 390 × 844 et × 0,8 en Fold plié (412 × 915).

## Animation

Allumage (§5.1) piloté par un seul `requestAnimationFrame` le temps de la séquence. Journal tapé à 36 car/s, pause de 60 ms entre les lignes. En portrait : journal de 6 lignes, silences d'allumage raccourcis (× 0,6). Ensuite, plus aucune boucle JS : curseur (530 / 530 ms), scanlines (dérive 3 px en 12 s), scintillement (paliers 96 à 100 %), dérive du fond et bandeau (~45 px/s à l'échelle) sont des animations CSS. Le glitch (120 ms, toutes les 8 à 20 s) est un minuteur unique ; sa bande évite la liste des choix et ne part pas pendant une confirmation.

Saut : toute touche, tout clic ou tout tap termine l'allumage, **et ne fait que ça** : c'est le geste suivant qui choisit. Pendant l'allumage, la liste ne reçoit aucun geste (`pointer-events:none`), le clic qui suit le geste de saut est avalé, et un clic programmatique est ignoré. Les tests passent l'allumage par l'aide commune `tests/nml_boot.py` (`passer_boot`) avant leur premier clic sur `#m-new`.

Confirmation : flash de 100 ms sur la ligne et commande `> EXEC ...` tapée à 36 car/s sous la liste.

## Écart à la fiche

Un seul : l'action part tout de suite, sans attendre la fin de la frappe de `> EXEC ...`, pour garder un menu réactif. Validé par Ocre.

Pas de boucle hors du menu : en jeu, `#menu` est masqué (`display:none`, plus d'animation CSS) et le minuteur de glitch est coupé. Onglet caché : animations en pause (`animation-play-state`), glitch coupé, allumage terminé.

Mouvement réduit (`prefers-reduced-motion` ou option « Réduire les animations ») : pas d'allumage, pas de scintillement, de glitch, de dérive ni de défilement. Le bandeau affiche un message toutes les 4 s. Le curseur est fixe et la lueur réduite à une couche.

## Lignes de la fiche §6.4 branchées

CONTINUER sans sauvegarde, QUITTER à l'écran titre (« fonction non incluse »), choix grisé, QUITTER en pause, spam de flèches (14 en 2 s), F1 ou frappe libre `AIDE` / `HELP`, commande inconnue (frappe libre de 3 lettres ou plus), cinq appuis sur la version (`MODE MAINTENANCE DEVERROUILLE.`, comportement du mode DEV inchangé).

## Non fait

Sons du terminal (optionnels, non livrés). Menu pause rendu dans le même terminal, sans rallumage, mais sans réécriture animée des lignes. Courbure du tube : non, vignette seulement.
