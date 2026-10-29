# Interface : fiche de conception (lots 1 à 3)

Légende : **[canon]** roman tome 1 ou maquette v0.13 (`reference/`, lecture seule) · **[décision]** Valentin, 2026-10-29 · **[proposition]** Régie, à valider.
Sources : `docs/villes/STEEL_MEGALOPOLIS_PLAN.md`, `reference/maquette/.../07_MAQUETTE_ARCHIVE_v0.13/ART.md` et `tests/world.test.js`.

## 0. Objectifs
- **[décision]** Interface discrète, semi-transparente, qui ne cache pas l'art.
- **[décision]** Deux formats de référence : mobile 390×844, ordinateur 1280×800.
- **[décision]** Aucun élément d'interface ne recouvre un bouton contextuel (entrée de bâtiment, dialogue).
- **[décision]** Deux cartes : Steel-Megalopolis par couches d'étages, et carte des No Man's Land à cases avec voyage à la Fallout 1 et 2.

## 1. Lot 1 : barre du bas (en cours chez Rivet, résumé)
- **[décision]** Barre Menu, Sac, Journal, Carte, Son, Discret : réduite, icônes adaptées, touche clavier affichée sur ordinateur.
- **[décision]** Elle ne doit plus se superposer au bouton contextuel d'entrée de bâtiment.
- **[proposition]** Barre en icônes seules, fond semi-transparent (opacité 60 % environ), étiquette au survol ou à l'appui long ; le bouton contextuel se place au-dessus de la barre avec une marge fixe.

Défauts relevés à corriger dans ce lot :
1. 6 étiquettes de lieux ou PNJ masquées sous le HUD.
2. Bloc OBJECTIF sur 3 lignes en mobile, qui cache la scène. **[proposition]** 1 ligne tronquée, dépliable au toucher.
3. Étiquette ramenée dans l'écran qui couvre la tête d'un PNJ. **[proposition]** Décaler l'étiquette au-dessus du sprite, jamais sur sa boîte.
4. « Établi du technicien » et « Le technicien » superposés. **[proposition]** Évitement de collision entre étiquettes (décalage vertical), priorité au PNJ.
5. Masquage hors écran seulement horizontal. **[proposition]** Appliquer aussi le masquage ou le rabattement en vertical, en tenant compte des zones HUD haut et bas.

## 2. Lot 2 : carte de Steel-Megalopolis
### Couches
| N° | Couche | Statut | Source |
|---|---|---|---|
| 1 | Sous-Ville, souterraine, séparée de Lower-Town | accessible | [canon] Ch. VII §1701, §1716 ; [décision] |
| 2 | Lower-Town, nuit permanente, quartiers China Lake et Asia-Ground (Asia-Ground au sud) | accessible | [canon] Ch. II §696, Ch. IV §1038, Ch. IX §2069 ; [décision] position |
| 3 | Center-Town, surélevée, au centre (tours, Arcadius Center) | accessible, premier quartier après la douane | [canon] Ch. III §854 ; [décision] 21/10 |
| 4 | Upper-Town, ciel synthétique | affichée, inaccessible | [canon] Ch. II §696 ; [décision] |

- **[canon maquette]** La v0.13 a déjà des planches `steel-under`, `steel-lower`, `steel-center`, `steel-upper` et `steel-perimeter` : schémas de desserte, pas des plans topographiques. Leçon reprise, dessin à refaire.

### Contenu par couche [proposition]
- Sous-Ville : machineries, ruelles à feux, entrées secrètes, routes de sortie vers l'extérieur.
- Lower-Town : rues principales, lac de Lower Street, China Lake, Asia-Ground (marché), accès à la Sous-Ville et à Center-Town.
- Center-Town : douane d'entrée, tours, Arcadius Center, ascenseurs vers les autres couches.
- Upper-Town : silhouette grisée, mention « Accès refusé », aucun lieu cliquable.

### Navigation et état [proposition]
- Onglets ou pile verticale 1 à 4 (Sous-Ville en bas, Upper-Town en haut) ; la couche du joueur s'ouvre par défaut.
- Lieux découverts : icône pleine et nom. Non découverts : silhouette sombre sans nom, ou absents si jamais entendus.
- Position du joueur : marqueur unique sur sa couche ; rappel discret sur l'onglet de cette couche.
- Sorties : douane (Center-Town), routes de la Sous-Ville, liens entre couches (ascenseurs, escaliers) marqués d'un symbole distinct. Un clic sur une sortie vers l'extérieur ouvre la carte NML.

## 3. Lot 3 : carte des No Man's Land
### Canon maquette v0.13
- Grille de 22 colonnes × 20 lignes, cases de 50 unités, **167 cases terrestres** accessibles, mer non franchissable.
- Trajet case par case (8 directions, sans couper les angles marins), l'heure avance à chaque case, eau consommée en route.
- Halte : le joueur s'arrête sur la case courante, qui s'ouvre comme terrain explorable ; l'itinéraire restant est conservé et **reprise** possible. Annulation possible.
- Rencontre de route annoncée une seule fois, interrompt le trajet (péage, combat, fuite par la sortie).
- Cases vides : terrain calme sans habitants, 7 compositions de halte réutilisées (167 cases ≠ 167 niveaux).
- Mobile : carte défilable et sélecteur colonne/ligne pour viser une case.

### Règles [décision] et [proposition]
- **[décision]** Voyage à la Fallout 1 et 2 : le joueur choisit une destination, le marqueur avance case par case (ex. Dusk-Town vers Steel-Megalopolis), chaque case peut déclencher un événement.
- **[proposition] Coût en temps par case** : piste ou route 1 h, désert ou plaine 2 h, relief ou forêt 3 h, verre vitrifié ou zone irradiée 3 h.
- **[proposition] Terrain** : un type par case, porté par les données de la grille (même source que le contour).
- **[proposition] Repères** : villes et grands lieux (Dusk-Town, Steel-Megalopolis, Junk-Burgh, etc.) en icônes ; cases visitées éclaircies, brouillard sur le reste.
- **[proposition] Halte** : bouton « Halte » pendant le trajet ; « Reprendre » sur la carte après la halte.
- **[décision] Crochet événement** : à chaque case, appel `onCaseEntree(case, terrain)` qui tire dans une table `EVENEMENTS_ROUTE` **vide pour l'instant** ; aucun événement codé maintenant.
- **[proposition] Probabilité par terrain** : route 5 %, plaine 10 %, désert 12 %, forêt ou relief 15 %, zone irradiée 20 %. Valeurs en données, réglables.
- **[proposition] Entrée dans un lieu** : à l'arrivée sur une case de lieu, écran court « Entrer dans [lieu] ? » ; pour Steel-Megalopolis, arrivée devant la guérite (règle d'entrée selon la race, décision du 21/10).

## 4. Besoins pour Ocre
- Fond carte NML : relief peint sans texte ni icône, recalé sur la grille 22×20 ; 2200×2000 px (ordinateur) et version allégée WebP pour mobile.
- Fonds carte Steel : 4 planches de couche, même cadrage, 1600×1200 px, Upper-Town en version désaturée.
- Icônes de lieux : 24 et 48 px, SVG ou WebP alpha, lisibles à 24 px ; états découvert / non découvert / joueur / sortie / lien entre couches.
- Icônes de la barre du bas : 6 icônes monochromes 24 px, SVG.

## 5. Besoins pour Rivet
- Lot 1 : collisions d'étiquettes, masquage vertical, zone réservée au bouton contextuel, OBJECTIF sur 1 ligne en mobile.
- Lot 2 : données des lieux par couche (id, couche, coordonnées, découvert, sortie), état « joueur ici ».
- Lot 3 : grille et terrain en données, coût par terrain, trajet pas à pas, halte et reprise, crochet événement et table vide, sauvegarde de l'itinéraire.

## 6. Critères de test (Régie)
- En 390×844 et 1280×800 : aucune étiquette sous le HUD, aucun recouvrement entre barre du bas et bouton contextuel, aucune étiquette sur une tête de PNJ, aucune paire d'étiquettes superposées.
- OBJECTIF tient sur 1 ligne en mobile.
- Carte Steel : 4 couches présentes, Upper-Town non cliquable, Asia-Ground au sud de Lower-Town, Sous-Ville distincte de Lower-Town, marqueur joueur sur la bonne couche.
- Carte NML : 167 cases accessibles, trajet Dusk-Town vers Steel-Megalopolis case par case, temps avancé selon le terrain, halte puis reprise avec itinéraire intact, crochet appelé à chaque case sans erreur avec table vide.

## 7. Questions ouvertes pour Valentin
1. Coûts en temps et probabilités par terrain proposés ci-dessus : à valider ou à remplacer ?
2. Lieux non découverts : silhouettes visibles ou entièrement cachés ?
3. Upper-Town sur la carte : silhouette grisée suffisante, ou quelques noms de lieux visibles ?
