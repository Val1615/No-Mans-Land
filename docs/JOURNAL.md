# Journal de reconstruction NML

## 2026-10-21 (heure de Paris)

### Décisions
- Le tome 1 est la seule source canonique. Arbitrages dans `CANON_ARBITRAGES.md`.
- Technique : 3D orthographique avec Three.js 0.170, en modules ES servis statiquement, avec une interface HTML. Voir `DECISION_TECHNIQUE.md`.
- Référentiel : 1 unité = 1 m, cases de 0,5 m, personnage de 1,8 m, porte de 1,0 × 2,2 m, seuil à 1 m.
- Aucun code repris de la v0.13.

### Fait
- `ETAT_DES_LIEUX.md`, `CANON_ARBITRAGES.md`, `DECISION_TECHNIQUE.md`.
- `/workspace/nml/game/` : scène d'étalonnage avec :
  - une rue de 24 × 20 m ;
  - une boutique placeholder de 8 × 6 m, avec une porte réelle et un seuil marqué ;
  - un intérieur de 8 × 6 m avec murs, porte de sortie et comptoir ;
  - une tour placeholder de 12 m qui sert de volume occultant ;
  - une caisse ;
  - un joueur (bleu) et un compagnon (vert).
- Contrôles : clic ou tap sur le sol (déplacement), sur la façade ou sur la porte (trajet jusqu'au seuil puis entrée), et bouton contextuel « Entrer » ou « Sortir ».
- Bandeau « GÉOMÉTRIE PROVISOIRE (PLACEHOLDER) » et étiquettes sur chaque volume provisoire.

### Vérifié
`tests/browser_check.py` dans Chrome headless (WebGL logiciel SwiftShader), avec de vrais événements souris (1280×800) et tactiles (390×844, `has_touch`). Résultat : **22 sur 22**, détail dans `captures/resultats-verification.json`.
- Clic sur la façade (bureau) et tap sur la porte (mobile) : trajet jusqu'au seuil puis entrée dans l'intérieur. Aucun échantillon du trajet n'est passé dans l'emprise du bâtiment (38 échantillons).
- Le compagnon entre avec le joueur, à 1,0 m.
- Sortie : par clic sur la porte intérieure (bureau) et par tap sur le bouton « Sortir » (mobile). Arrivée exacte au seuil extérieur (8 ; 11), compagnon ressorti à 1,0 m.
- Réentrée immédiate après sortie. C'est la régression du bug historique de Nilo, réécrite pour ce nouveau code.
- Le compagnon suit après un clic réel sur le sol, et s'arrête à 1,48 m.
- Une destination dans l'emprise du bâtiment est refusée avec le motif `chemin_bloque`. Testé par appel de commande, pas par clic.
- Occultation : la tour passe à une opacité de 0,25 quand le joueur est derrière, puis revient à 1,0 quand il est devant. Le déplacement derrière la tour se fait par commande, pas par clic.
- Aucune erreur console après ajout d'une favicon vide (l'erreur 404 initiale venait de la favicon).

### Non vérifié
- Vrai téléphone, vrai geste tactile, performance sur GPU mobile, Safari iOS, rotation, texte agrandi.
- Le cas « compagnon trop loin » (resté derrière avec un message) est codé mais n'est pas testé.
- Aucune condition de porte (serrure, combat) n'est implémentée.
- Pas de sauvegarde ni de rechargement.

### Corrigés en cours de route
- Le compagnon visait une case à 2 m du joueur : il choisit maintenant l'anneau libre le plus proche.
- La sélection et la projection pouvaient utiliser la scène de l'image précédente juste après une transition. Le rendu est maintenant forcé avant `pick` et `project`.

### Problèmes ouverts
- La grille d'aide déborde du sol (elle est carrée).
- Les étiquettes sont peu lisibles sur mobile.
- Pas de rotation ou de zoom de caméra.
- Une seule porte, piétonne. Pas de porte de fret.
- Pas de dépendances verrouillées hors `package-lock.json`. Pas encore de build.

### Prochaine étape
Faire valider le référentiel par Valentin sur les captures. Ajouter ensuite :
- une porte verrouillée avec refus typé ;
- une porte de fret ;
- le cas « compagnon resté derrière » ;
- sauvegarde et rechargement.

Puis rédiger le programme du quartier de Dusk-Town.

## 2026-10-21, 13 h 15 (heure de Paris)

### Décisions de Valentin
- Steel-Megalopolis est la capitale d'IO. L'ancienne capitale de l'UFSA est Buenos Aires. La question des deux capitales est close.

### Vérifié dans le roman
- Ch. I §250 dit bien « Qui ne connait pas SteelMegalopolis ? Oui… la capitale de l'Ex UFSA. » : pas d'erreur de lecture. Le roman est à corriger, la décision prévaut.
- Ch. I §288 : cryogénisation en août 2065, réveil prévu en juillet 2165, « Nous voilà le 5 Octobre 2202 », « cent trente longues années ».
- Inventaire verbatim des citations temporelles ajouté à `CANON_ARBITRAGES.md` §2.

## 2026-10-21, 13 h 20 (heure de Paris)

### Décisions de Valentin
- Règle de lecture : seuls les faits posés par la narration sont des dates canoniques. Les durées dites par les personnages sont approximatives. « 130 ans » et « plus de deux cents ans » ne sont donc **pas** des contradictions : point retiré.
- La cryogénisation de 2065 précède la guerre et est indépendante des autres dates.
- 2075 (Grand Exode) et 2081 (début de la guerre) sont des dates de travail compatibles avec le roman.

## 2026-10-21, après-midi (heure de Paris) : Dusk-Town, quartier 1 « La Pompe »

### Décisions
- Programme du quartier : `docs/quartiers/DUSK_TOWN_Q1.md`. Chaque détail canon est cité depuis le roman (Ch. I §61 à §107) ; PNJ et accroches sont marqués « proposition ».
- Assets :
  - bâtiments, sols et mobilier faits par code (volumes en mètres, textures peintes) ;
  - personnages et accessoires repris de la maquette, dimensionnés par hauteur en mètres ;
  - catalogue : `docs/ASSETS_CATALOGUE.md`.
- Monnaie affichée en dollars : **proposition** (le roman cite des dollars en 2202, Ch. VII §1691).
- La scène d'étalonnage est archivée (`src/data/archive_calibration.js`, `tests/archive/`). `main.js` charge désormais Dusk-Town.

### Fait
- Zone de 48 × 36 m :
  - avenue de 8 m, ruelles de 6 m, place de la pompe ;
  - 9 bâtiments tous différents, dont 3 visitables (clinique, bar, épicerie) avec intérieurs ;
  - 5 PNJ avec dialogues (Mara, Ruth, Vera, Hector, Anselme) ;
  - services : soin, repas, verre, eau, ration ;
  - piste de quête notée (pompe) ;
  - sortie est barrée ; retour « fermé » sur les bâtiments non visitables, sans marqueur.
- Défauts d'étalonnage corrigés :
  - la grille d'aide qui débordait est supprimée (sol texturé limité à la zone) ;
  - les étiquettes sont en HTML, 12 à 13 px, sur fond opaque ;
  - les intérieurs sont zoomés.
- Ajout : un clic sur une case occupée vise la case libre la plus proche (1,5 m maximum). Ce cas bloquait la marche sur mobile, à cause d'un banc.

### Vérifié
`tests/dusk_q1_check.py` dans Chrome headless (WebGL logiciel), avec de vrais clics (1280×800) et de vrais taps (390×844). Résultat : **62 sur 62**, détail dans `docs/captures/dusk-q1/resultats.json`.
- Les 3 portes : entrée par clic sur la façade (bureau) ou tap sur la porte (mobile), sortie par clic sur la porte intérieure (bureau) ou bouton « Sortir » (mobile), arrivée exacte au seuil.
- Le compagnon entre et ressort à chaque passage, et suit jusqu'à la pompe.
- Les 5 dialogues s'ouvrent par geste sur le PNJ. Les branches sont parcourues et le dialogue se ferme (y compris par le bouton ×).
- Services : eau (−4 $, inventaire +1), repas (−6 $, +5 PV), soin (−15 $, PV au maximum).
- Le poste de milice ne déclenche pas de transition.
- La sortie est est barrée (déplacement par commande, arrêt avant les sacs).
- Le bar devient transparent quand le joueur est derrière (déplacement par commande).
- Aucune erreur console.

### Non vérifié
- Vrai téléphone et vrai geste, performance sur GPU mobile, Safari iOS.
- Les branches « pas assez d'argent » des dialogues.
- Lisibilité réelle pour un humain ; seul Valentin peut juger la qualité visuelle.

### Problèmes ouverts
- Personnages sans animation, avec armes longues pour des civils.
- Ruine trop schématique ; pompe non conforme (machinerie, pas pompe à bras).
- Message de transition laissé affiché 3,5 s.
- PNJ fixes, sans routine.
- Pas de sauvegarde.

### Prochaine étape
Revue visuelle par Valentin des captures `docs/captures/dusk-q1/`, puis :
- sprites civils animés ;
- sauvegarde et rechargement ;
- routines simples (Mara à la pompe le soir) ;
- atelier de Nilo visitable.

## 2026-10-21, 14 h 05 (heure de Paris)
- Décision de Valentin : la monnaie est le dollar (ancienne monnaie de l'UFSA) dans les No Man's Land, et le crédit uniquement à Steel-Megalopolis. Les dollars restent à Dusk-Town. Consigné dans `CANON_ARBITRAGES.md` §9 bis.
- Recherche dans tout le roman sur Dusk-Town : le nom n'apparaît que dans le chapitre I (8 occurrences, §61 à §351). Aucune milice ni aucun défenseur local n'est mentionné. Jeu inchangé.

## 2026-10-21, après-midi (heure de Paris) : Dusk-Town Q1 v2 (« ville morte habitée »)

### Décisions de Valentin
- Rues vides : habitants cachés dans les ruines.
- Aucune milice.
- Mutants cachés parmi les villageois.
- Quelques Invictos isolés.
- Les rafles anti-mutants du Service Militarisé, qui fait de Dusk-Town un point de passage, s'apprennent par les personnages.
- Consigné dans `CANON_ARBITRAGES.md` §9 ter et dans `DUSK_TOWN_Q1.md`.

### Fait
- Plus aucun PNJ dehors. Ruth (milice) est supprimée ; le poste de milice devient une tour effondrée ; les sacs de sable sont remplacés par des éboulis et une épave.
- Maison de Mara visitable, avec Mara et Bruno (mutant caché). Ileana (Invicta) est au bar.
- Entrées camouflées : planches, filet de lumière, symbole gravé, seuil dégagé, anneau discret. Enseignes supprimées, aucune fenêtre éclairée dehors.
- Décrépitude renforcée ; traces de vie déplacées à l'intérieur.
- Dialogues réécrits : l'histoire des rafles est répartie entre Mara, Bruno, Hector, Vera, Anselme et Ileana.
- Sprites sans arme longue pour Bruno, Anselme et Vera.

### Vérifié
`tests/dusk_q1_check.py` en Chrome headless, avec de vrais clics (1280×800) et de vrais taps (390×844). Résultat : **74 sur 74**, détail dans `docs/captures/dusk-q1-v2/resultats.json`.
- Aucun PNJ dehors.
- Les 4 portes camouflées entrent et ressortent, compagnon compris.
- Les 6 dialogues s'ouvrent, se parcourent et se ferment.
- Services : eau, repas, soin.
- Piste de la pompe notée.
- Tour effondrée sans transition.
- Sortie est bloquée (déplacement par commande).
- Occultation du bar (déplacement par commande).
- Aucune erreur console.

### Non vérifié
- Vrai téléphone.
- Lisibilité réelle des entrées camouflées pour un joueur humain, à juger par Valentin.
- Branches « pas assez d'argent ».

### Problèmes ouverts
- Mara (actor-1) porte encore une arme ; Vera a un sprite trop propre (style IO).
- L'épave paraît petite.
- Pas de cycle jour-nuit : la pompe nocturne n'est qu'évoquée.
- Les étiquettes HTML des services restent affichées au-dessus de façades qui se veulent mortes. Choix d'ergonomie à confirmer avec Valentin : afficher seulement à proximité ?

## 2026-10-21 14:40 · Étiquettes de services après découverte (décision de Valentin)
- Règle retenue : le nom d'un service n'apparaît au-dessus de sa façade qu'une fois le lieu découvert. Découvert = le joueur y est entré, OU un personnage l'a nommé explicitement (action de dialogue `reveal:<bâtiment>`). Rien à l'approche, rien avant. Une découverte est définitive (persiste après la sortie).
- Implémenté : `state.discovered` (game.js), entrée par une porte de bâtiment et action `reveal`, étiquettes masquées tant que non découvertes (view.js). Seul cas « raconté » pour l'instant : Mara, réplique « Il n'y avait personne. », mentionne Vera et la porte à la croix, ce qui révèle la Clinique.
- Vérifié (navigateur, desktop 1280x800 et mobile 390x844) : 88/88 contrôles, dont 14 nouveaux sur les étiquettes (aucune au départ ; chacune apparaît après entrée ; Clinique apparaît après le dialogue de Mara avant toute entrée, Épicerie et Bar encore masqués ; les 4 persistent après sortie).
- Captures : captures/dusk-q1-v2/desktop-06-avant-decouverte.png, desktop-07-apres-decouverte.png.
- Ouvert : pas de sauvegarde, donc persistance limitée à la session.

## 2026-10-21 15:30 · v3 : assets de la maquette, sprites générés, orientation
- Fait : sols en tuiles de la maquette ; façades redressées depuis settlement-v9-dusk et buildings-v6, appliquées aux volumes mesurés (la géométrie ne vient jamais de l'image) ; portes réelles alignées sur les portes peintes ; vitrine de l'épicerie condamnée ; 4 assets générés (Mara, Vera, Hector sans arme, pompe à bras) et 3 portraits. Inventaire et raisons dans ASSETS_CATALOGUE.md.
- Orientation : miroir horizontal des sprites selon le sens de marche à l'écran (joueur, compagnon) ; PNJ statiques orientés vers un point qui a du sens (`faceTo` : Mara vers la porte, Bruno vers la table, Vera vers l'armoire, Hector vers la salle, Ileana vers la porte, Anselme vers sa porte) ; PNJ tourné vers le joueur pendant le dialogue, puis retour à sa pose.
- Vérifié (navigateur, desktop 1280x800 et mobile 390x844) : 106/106 contrôles, dont orientation (joueur et compagnon à droite puis miroir à gauche) et PNJ tourné vers le joueur à chaque dialogue (Mara, Bruno, Anselme, Hector, Vera).
- Captures : captures/dusk-q1-v3/ (vue d'ensemble, détail rue, intérieurs, dialogues, mobile, comparaison-vue-ensemble-v2-v3.png).
- À vérifier : les toits sont plats (les sprites ont des toits à deux pans) ; murs intérieurs encore unis ; sprites générés à valider par Valentin ; le miroir inverse aussi les détails asymétriques (sacoche, fusil).

## 2026-10-21 16:20 · v4 : bâtiments en sprites entiers de la maquette (correction de Valentin)
- Retiré : volumes de code texturés (façades redressées v3). Les fichiers assets/mockup/*_s|_e et toits ne sont plus utilisés.
- Fait : 10 bâtiments distincts, chacun l'image complète d'une planche (settlement-v9-dusk, buildings-v6), posés en billboard ; caméra recalée sur la projection des planches (lacet 34,5°, tangage 28,8°) ; échelle unique K = 50 px/m ; emprise, ancre et portes mesurées sur l'image par tools_buildings.py ; ordre du peintre par emprise ; occultation au pixel ; pictogramme sur la porte peinte. Détail par bâtiment dans ASSETS_CATALOGUE.md (section v4).
- Vérifié (navigateur, desktop 1280x800 et mobile 390x844) : 138/138 contrôles, dont : base opaque aux 3 coins de chaque emprise (10 bâtiments), écart porte peinte / ouverture < 0,8 m (5 portes), centre de chaque emprise bloqué, toutes les portes entrent et sortent au seuil devant la porte peinte, bar transparent quand le joueur est derrière, aucune erreur console.
- Captures : captures/dusk-q1-v4/.
- À vérifier : planches dessinées avec un lacet un peu variable (bases pas parfaitement sur la grille, emprises de la maison à escalier, du marché et de l'entrepôt réduites) ; pas de partie arrière visible quand on contourne (sprite unique) ; décor du marché et de l'entrepôt plus monumental que le reste ; exterior-buildings-v4 écarté.

## 2026-10-21 16:20 · v5 : miroir réellement visible, animation procédurale
- Cause du miroir invisible : THREE.Sprite ignore le signe de scale.x (le shader de sprite calcule l'échelle par la longueur de la colonne de la matrice, toujours positive). Le code mettait scale.x à -1 et l'état interne `facing` changeait, mais l'image rendue ne se retournait jamais. Les tests v3/v4 lisaient `facing` (état) : ils ne pouvaient pas voir le défaut.
- Correctif : chaque personnage a sa propre texture ; le miroir se fait par les UV (map.repeat.x = -1, offset.x = 1). Le clic et l'occultation au pixel tiennent compte du miroir.
- Animation (sans toucher aux assets) : demi-tour rapide (la largeur passe à 0 puis revient en 0,14 s, l'image bascule au milieu) ; marche : rebond de 4,5 cm, léger tassement et balancement (1,9 pas/s) ; repos : respiration de 1,2 % en hauteur, phase propre à chaque personnage. Amplitudes en mètres, donc identiques sur mobile.
- Règle de test retenue : un effet visuel se vérifie sur les pixels rendus, jamais sur l'état. tests/flip_pixels.py rend le personnage isolé (même pipeline, fond magenta) face à droite puis à gauche et exige écart(A, miroir(B)) < 0,6 × écart(A, B).
- Vérifié : flip_pixels 8/8 (joueur, Nilo, Vera qui se tourne vers le joueur ; desktop et mobile ; rebond présent) ; suite complète 138/138.
- Captures : captures/dusk-q1-v5/.

## 2026-10-21 17:45 · v6 : intérieurs en assets réels, district La Pompe clôturé (exigence de Valentin)
- Fait : les 4 intérieurs (clinique de Vera, Le Passage d'Hector, épicerie d'Anselme avec ses 2 entrées camouflées, maison de Mara) n'ont plus aucune boîte ni couleur unie :
  sols et murs en textures réelles (2 de la maquette, 6 générées), porte de sortie en texture générée, 16 meubles en sprites (2 de la maquette, 14 générés). Détail et provenance : ASSETS_CATALOGUE.md § v6.
- Contrôle d'angle automatique (`tools_interiors.py`) : 39 candidats mesurés, 22 rejetés (dont 8 meubles de la maquette, en 2:1) ; rejet aussi des sprites `reused/` qui servaient dans les intérieurs.
- Rendu : intérieur trié par l'ordre du peintre comme la rue (meubles, joueur, Nilo, PNJ) ; murs du fond, puis sprites, puis murs avant bas et porte ; meuble qui cache un personnage à 35 % ; porte et mur avant estompés quand le joueur est derrière (rayons aussi sur les bords du sprite).
- Corrigés : l'étiquette « Sortie » posée sur le seuil cachait le joueur à l'arrivée (déplacée au-dessus de la porte) ; un clic sur le mur avant bas ne faisait rien (il passe maintenant au sol) ; une porte estompée laisse passer le clic ; **la porte est de l'épicerie était inaccessible** depuis la v4 (seuil bloqué par un tonneau, jamais testé) : tonneau déplacé.
- Vérifié (Chrome headless, clics 1280x800 et taps 390x844, contrôles sur PIXELS) : suite locale 138/138 + flip_pixels 8/8 + nouvelle `tests/interiors_pixels.py` 107/107. Nouveaux contrôles : chaque meuble visible à ≥ 50 % de son image rendue (capture comparée au rendu isolé du même meuble) ; murs et sol texturés (écart-type local des pixels) ; chaque PNJ de service dans son lieu et visible au pixel (Bruno derrière le rideau et Hector derrière son comptoir : seuils abaissés par conception) ; joueur visible au seuil ; entrée par geste sur la porte peinte et sortie par la porte / bouton Sortir avec arrivée au seuil ; nom du service affiché dehors après découverte ; miroir et animation de marche du joueur en intérieur mesurés sur le rendu ; comptoir du bar estompé quand le joueur passe derrière.
- Captures live : captures/dusk-q1-v6/ (une par intérieur, mobile clinique et bar, occultation du comptoir, gif entrée/sortie de la clinique).
- À vérifier : vrai téléphone ; lisibilité humaine (Valentin) ; deux sprites retournés depuis la source (armoire, étagère de l'épicerie) ont leur éclairage à droite ; le linge, les bacs de culture, le filtre à eau et les sacs de rations n'ont pas de version à l'angle v4 ; le placement du joueur devant chaque façade dans interiors_pixels.py se fait par commande (le trajet de rue est couvert par dusk_q1_check.py) ; le passage derrière le comptoir est commandé, pas cliqué.

## 2026-10-21 · v7 : toute la ville (4 quartiers reliés à pied)
- Fait : Dusk-Town = La Pompe (centre) + Le Transit (est) + Le Scellé (nord, accès scellé du labo Human Corporation) + Les Sables (sud, sortie vers les terres dévastées). Plan, canon et propositions : quartiers/DUSK_TOWN_PLAN.md.
- Jonctions : bouts de rue (`junction: true` dans `DOORS`), franchis en s'arrêtant sur le seuil après une marche ; arrivée au bout correspondant du voisin, Nilo suit ; verrou anti-rebond ; bords sans voisin annoncés par un texte (désert, route des patrouilles, terres dévastées).
- La Pompe : l'épave de la sortie est barre toujours l'avenue mais laisse un passage piéton côté sud (z 20) vers Le Transit. Le contrôle v4 « sortie est barrée » est remplacé par « épave infranchissable, passage piéton seulement ».
- 3 entrées camouflées avec intérieur (le guet, l'atelier, la citerne), 3 PNJ écrits (Teo, Ezequiel, Sol : désir, peur, secret). Teo vend un tuyau qui révèle L'atelier dans un autre quartier ; Sol vend l'eau 3 $.
- Assets : 1 bâtiment de la maquette encore libre (cinéma), 1 bâtiment généré (blockhaus du labo), 3 personnages générés ; détail ASSETS_CATALOGUE.md § v7.
- Tests : nouvelle `tests/town_pixels.py` (bureau 1280x800 clics, mobile 390x844 taps) : les 3 jonctions dans les 2 sens par marche réelle, arrivée au bon bout, Nilo, bâtiment du quartier et personnages vérifiés au pixel, pas de rebond, bords annoncés, porte scellée, 2 entrées camouflées par geste, dialogues par geste, argent / PV / inventaire / lieux découverts conservés.
- Vérifié en local (Chrome headless, clics 1280x800 et taps 390x844, contrôles au pixel) : town_pixels 129/129, dusk_q1_check 138/138, flip_pixels 8/8, interiors_pixels 106/106 (sans GIF).
- Captures : captures/dusk-v7/ (plan-global.png, quartier-q1..q4, arrivées de chaque jonction bureau et mobile, porte scellée, bord sud, jonction-q1-q2.gif).
- À vérifier : vrai téléphone ; lisibilité et écriture (Valentin) ; sprites de bâtiments réutilisés d'un quartier à l'autre (12 cases dusk seulement) ; blockhaus et 3 PNJ générés à valider ; plan-global = prises de vue avec placement par commande (les trajets sont testés à part) ; un seul Los Invicto dans toute la ville (Ileana).
