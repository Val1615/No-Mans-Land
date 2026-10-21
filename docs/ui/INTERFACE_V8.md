# Interface v8 — direction A « radio de récupération ambre »

Référence : `docs/ui/propositions/direction-A.png`. Code : `game/index.html`, `game/src/style.css`, bloc v8 de `game/src/main.js`.

## Éléments
- HUD haut-gauche : PV (barre), $, Nilo (suit / resté en arrière). Haut-droite : lieu + quartier.
- Bas-droite : touches Sac (I), Journal (J), Carte (M), Minimal (H / bouton mobile).
- Dialogue bas-gauche (≤560 px), choix numérotés (touches 1–9), Échap ferme.
- Sac : inventaire + « ACHAT · <PNJ> » = achats existants du dialogue courant. **Le troc objet-contre-objet n'existe pas** dans la logique : non inventé, signalé dans le panneau.
- Journal : lieux découverts + notes. Carte : grille 3×3 des quartiers, « > ici », non vus = « ? ».
- Mode minimal : HUD, lieu et touches masqués (seul le bouton minimal reste).
- Mobile (≤600 px, testé 390×844) : le panneau remplace le dialogue (jamais d'empilement).

## Règles tenues
Cadres fins, voile `rgba(10,7,4,.72)` + flou 2 px, jamais empilés ; ambre (#f2b44a) réservé au texte/accents (teinte du fond de panneau < 0,25 mesurée) ; aucun choix au centre ; couverture d'écran en exploration ≤12 % bureau, ≤22 % mobile.

## Contraste mesuré (pixels, sur le sable le plus clair trouvé parmi 36 vues caméra)
Méthode : texte = 75e centile de luminance des pixels que l'UI éclaircit par rapport à la scène nue (le voile ne fait qu'assombrir) ; fond = médiane du rectangle. Seuil WCAG 4,5:1.

| élément | bureau | mobile |
|---|---|---|
| HUD | 7,23 | 6,66 |
| lieu | 7,74 | 7,36 |
| touche Sac | 11,68 | 15,12 |
| texte dialogue | 14,16 | 15,99 |

Note : la première métrique (95e centile des pixels « modifiés ») comptait le fond voilé comme texte sur les petits boutons (3,3:1 alors que le rendu est net) ; corrigée, seuil inchangé.

## Polices (SIL Open Font License 1.1)
IBM Plex Mono (Regular, Medium) — IBM ; VT323 — Peter Hull. Fichiers dans `game/assets/fonts/`.

## Test
`game/tests/ui_pixels.py` (53 vérifications, gestes réels bureau + mobile), captures `docs/captures/ui-v8/`.

## Ajouts v9
- `#obj` : objectif de quête courant, sous le lieu, même voile que les touches.
- `#k-son` (touche S) : coupe / rétablit la musique ; état mémorisé ; reste visible en mode minimal.
- Journal : section « Quête · … » avec étapes `[x]`, étape courante `>` en ambre, étape hors de portée annoncée.
