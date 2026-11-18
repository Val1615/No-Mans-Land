# Rencontres de route : architecture (Rivet, 17/11/2026)

Une page. Point d’entrée, suivi des lots et journal : [`README.md`](README.md). Règle : chaque rencontre est un **petit lieu isométrique jouable**, jamais une fenêtre sur la carte.

## 1. Ce qui existe et sert tel quel
- **Crochet de route** : `src/core/voyage.js:10` `onCaseEntree()` tire `TERRAINS[t].p` puis pondère `EVENEMENTS_ROUTE` (`terrains`, `si`, `poids`) ; branché en `voyage.js:53` (`crochets`), appelé à chaque case par `pas()` (`:78-86`). Un événement tiré met déjà `statut = 'halte'`, garde `case` et `trajet` restant, et émet `evenement` (`:83`).
- **Probabilités** : `src/data/nml.js:6-13` (côte 5 %, désert 10 %, forêt 10 %, rocher 15 %, verre 20 %, piste 5 %). On ne les touche pas. `EVENEMENTS_ROUTE = []` (`:16`).
- **Sauvegarde** : `state.region` (case, statut, trajet, dest, vues…) et `state.heures` sont dans `snapshot()` / `restore()` (`game.js:272-297`) ; `restaure()` repasse une partie chargée « en route » en halte (`voyage.js:89`) ; autosave à chaque case (`main.js:171`).
- **Moteur local** : déplacement, dialogues à conditions et actions (`give:`, `take:`, `flag:`, `combat:`…), fouille par `SPOTS` (`kind: 'pickup'`), `TRIGGERS` d'arrivée : tout est piloté par des données.
- **Combat** : `combat.start(id)` (`combat.js:52`) lit `ENCOUNTERS[id]` (`data/combat.js`) : ancre par lieu, ennemis en `dx/dz` relatifs au joueur, zone 19 × 19 m dont le bord = fuite (`combat.js:13`), issues victoire / fuite / reddition / défaite en actions (`finish`, `:173`). Autosave avant combat.
- **Rendu et images** : `view.js:346 build(locId)` reconstruit la scène à chaque changement de lieu et relit `game.world.LOCATIONS` (`:911`) ; `chargement.js` charge les images **par lieu** à la demande. Rien à changer côté rendu.

## 2. Vrais blocages
1. `game.js:15` construit **toutes** les grilles de collision à l'init ; `LOCATIONS/DOORS/NPCS/SPOTS` sont figés à `game.js:11`, `state.npcs` (orientation) aussi (`:24`). Un lieu ajouté après coup n'a ni grille, ni PNJ dialoguables (`openDialogue` plante sur `state.npcs[id]`).
2. `restore()` refuse un lieu inconnu (`game.js:278`), `shell.load` aussi (`shell.js:107`) : une sauvegarde **dans** une rencontre ne se rechargerait pas.
3. Boucle principale (`main.js:204-205`) : hors `statut 'lieu'`, le jeu local ne tourne pas et la carte se rouvre ; personne n'écoute `evenement` (`carte_nml.js:60`).
4. Pas de verbe d'action « quitter la rencontre », pas de sortie de bord qui rende la main au voyage (`cross()` `game.js:220` ne connaît que `regional`).
5. Combat : ennemis seulement en relatif au joueur, ancre par `state.location` ; il faut des positions absolues dans la scène.
6. `onCaseEntree` ne reçoit pas la case dans `si(etat)` (biome, région) et tire aussi sur les cases de ville.

## 3. Architecture proposée (extensions, aucun moteur réécrit)
- **Catalogue** `src/data/rencontres.js` : une entrée par rencontre (format §4). `EVENEMENTS_ROUTE` devient `Object.values(RENCONTRES)` ; `si(etat, case)` reçoit la case. Jalon 3 : `mod(etat, case)` multiplie `p` (région, factions, scénario, récence via `region.rencontres[]`), défaut 1.
- **`game.ajouterLieu(loc, { npcs, doors, spots, dialogues })`** (≈ 30 lignes dans `game.js`) : enregistre dans les mêmes tableaux, construit `grids[id]` avec `buildGrid`, crée `state.npcs[id]`. `retirerLieu(id)` à la sortie. Même chemin que les lieux écrits à la main.
- **Gestionnaire** `src/core/rencontres.js` : sur `evenement`, `statut = 'rencontre'`, `region.rencontre = { id, case, graine, etat:{} }`, construit le lieu `rc_<id>` depuis le gabarit (sol du biome, décor d'Ocre, PNJ, caisses, sorties), `ajouterLieu`, puis `game.arriveVia('rc_<id>_entree')` (transition existante). `main.js` fait tourner `game.step` quand `statut` vaut `'lieu'` **ou** `'rencontre'`.
- **Sortie** : portes de bord `rencontre: true` → `cross()` appelle `onRencontreSortie` ; verbe d'action `rencontre:quitter` pour les issues de dialogue / combat. Effet : `retirerLieu`, `statut = 'halte'`, `heures += rencontre.duree`, carte rouverte sur la case, bouton Reprendre (trajet intact). Un PNJ hostile en vue peut bloquer une sortie (`conditions` de porte existantes).
- **Sauvegarde** : `region.rencontre` est déjà dans `region` (sérialisé). Crochet `game.onLieuManquant(snap)` appelé par `restore()` et `shell.load` : le gestionnaire reconstruit la scène depuis `id + graine`, puis l'état local (drapeaux de la rencontre pour caisses fouillées, morts, péage payé). `SAVE_VERSION` inchangé (champ optionnel).
- **Combat** : nouvelles entrées `ENCOUNTERS['<id>']` ; ajout dans `start()` d'un `e.x/e.z` absolu (repli sur `dx/dz`) et de ``E.centre` (centre de zone sans téléporter le joueur)`. Issues → actions (`rencontre:quitter`, `give:`, `flag:`).
- **DEV** (`src/ui/dev.js`) : section « Rencontre » : liste du catalogue + `Forcer sur cette case` = appel direct du gestionnaire avec l'id choisi (pas de tirage, probabilités intactes) ; `?rencontre=<id>` pour les tests Playwright.

## 4. Format à remplir par Ocre (une rencontre)
```js
embuscade_piste: {
  nom: 'Embuscade sur la piste', famille: 'pillards',
  terrains: ['piste'], biomes: ['desert', 'rock'], poids: 1, duree: 1,      // h ajoutées au voyage à la sortie
  scene: { size: { w: 30, d: 24 },           // m ; mini 24 × 24, maxi 48 × 36 ; zone de combat 19 × 19 entièrement dedans
    ground: { skin: 'g_sand', tint: 'rgba(…)', paint: [ /* bandes de piste, comme ground.paint */ ] },
    light: { /* même forme que les lieux */ },
    buildings: [ G('rc_pickup', 'rc_emb_pickup_appat_3q', x, z, w, d, ph, { solid: [...] }) ], // pose identique à mega_line.js
    props: [ { sprite: 'rc_emb_caisses_eventrees_3q', x, z, solid: 0.8 } ],
    entree: { x: 20, z: 28, side: 'south' },  // arrivée du joueur, loin du cœur de la scène
    sorties: [ { id: 'nord', x: 20, z: 0.5, side: 'north', w: 4 }, { id: 'sud', … } ] },
  pnj: [ { id: 'rc_pibe', name: 'Pibe', sprite: 'gen_rc_pibe', x, z, y: 2.5, faceTo: [x, z], dialogue: 'rc_pibe', si: 'emb_vu_talus' } ],  // si = condition de visibilité
  dialogues: { rc_quilla: { start: { text: '…', options: [ { label: 'Payer 20 $', if: 'money>=20', next: 'paye' }, { label: 'Bluffer', test: 'charisme:6', pass: 'passe', fail: 'combat' } ] }, /* nœuds avec enter: 'take:…;flag:…;rencontre:quitter' */ } },
  fouilles: [ { id: 'rc_caisse1', x, z, item: 'ration', text: '…', empty: '…' } ],      // SPOTS pickup
  examens: [ { id: 'rc_traces', x, z, text: 'Des traces de bottes fraîches remontent le talus.' } ],
  combat: { ennemis: [ { id: 'pillard1', nom: 'Pillard', sprite: 'gen_…', x, z, pv: 12, pa: 6, initiative: 5, arme: 'pistolet', competences: { melee: 30, armes: 40 } } ],
            ancre: { x: 20, z: 15 }, issues: { victoire: '…', fuite: 'rencontre:quitter', reddition: '…', defaite: '…' }, textes: { … } },
}
```
Contraintes : 1 unité = 1 m, cases de 0,5 m ; sprites `_3q` à la caméra du jeu (lacet 34,5°, tangage 28,8°, 50 px/m), manifeste dans `assets/rencontres/manifest.json` (même champs que Mega-Line : `file, px, anchor, footprint_m, height_m, pose, ordre`), préfixe `rc_` (`rc_ds_` modules désert, `rc_emb_` propres à l'embuscade, `g_rc_` sols) ; webp ; chaque PNJ, caisse et sortie atteignable à pied depuis l'entrée ; ennemis à ≥ 8 m de l'entrée (positions **absolues** en m, plus de dx/dz) et pas tous au même endroit ; décor lisible en 1280 × 800 et 390 × 844. Sol réutilisé (`g_sand`) sauf besoin argumenté. Les gardes visibles au loin, les guetteurs `si: '<drapeau>'` apparaissent quand le drapeau est posé (examen, déclencheur de zone, début du combat).

## 5. Jalon 1 : l'embuscade de pillards, de bout en bout
Piste en désert ou rocher. Arrêt du marqueur, pause, autosave, scène `rc_embuscade_piste` construite à la demande ; contourner (sortie nord par le talus), parler (payer / bluffer / intimider), combattre (combat existant, fuite par le bord = sortie), fouiller le pick-up et les caisses, partir ; retour carte en halte et reprise du trajet ; sauvegarde / chargement dans la scène ; DEV « forcer une rencontre » ; suite `tests/rencontres_rapide.py` (forcée, 1280 et 390, local puis Pages).
**Estimation Rivet** : ≈ 2 jours de dev (ajouterLieu + gestionnaire + boucle + sortie : 0,5 j ; sauvegarde / reconstruction : 0,5 j ; combat positions absolues + issues : 0,25 j ; DEV + carte : 0,25 j ; tests et captures : 0,5 j), dès réception du décor d'Ocre ; câblage possible avant sur gabarits gris.

## 6. Pilote « L'appât de la piste » (PILOTE.md, ff499ea) : verdict
**Rentre tel quel** : emprise 30 × 24 m, un niveau de sol à 0 ; zone de combat 19 × 19 centrée (18 ; 13) entièrement dedans ; lumière (`bg/hemi/sun/tint`) ; dialogues au format existant (`action`, `pay:`, `take:`, `give:`, `gain:`, `flag:`, `combat:`, `test` + `pass/fail/partial/partialAt/opposed`, `if` composés `a&b`, `inv:water>=2`) ; compétences `parole`, `discretion`, `melee`, `troc` ; `warp:` pour « Tuerto te raccompagne » ; objets `water`, `ration`, `plaque`, armes `fusil`/`poignard` ; couvertures 1 (pick-up, caisses, rochers, pneus) et 2 (épave) ; sorties S_O (halte) et S_E_route / S_E_lit (reprise) ; `gen_rodeur` réutilisé ; miroir `_neon` (éclat sur l'objet).

**Sente et crête : on garde la sente.** Même schéma que la Mega-Line (quai + escalier + garde-corps) : `loc.niveaux` = plateau `{ x 5, z 0, w 25, d 5, y 2.5 }` + rampe `{ x 2, z 3, w 3, d 7, y0 2.5, y1 0, axe 'z' }`, pente du talus en solides. Le combat ignore les hauteurs (pas de bonus de tir en hauteur) mais marche : cases praticables = grille, vue = couvertures. **Ajustement** : la pente du talus doit être une couverture 1, pas 2 (un solide 2 coupe la vue entre la crête et la piste) → champ `couv` par solide (petite extension de `coverSolids`). Repli si le test 390 échoue : crête pleine, Pibe dans une niche praticable fermée (2 × 2 m autour de (16,5 ; 4,2)), sente retirée. `combat.js` accepte un adversaire hors d'atteinte : l'IA sans chemin passe son tour (`aiStep`), le joueur reçoit « hors portée » en mêlée et peut tirer ; **mais** un ennemi posé sur une case pleine est déplacé (`nearestFree`, ≤ 4 m) : toute position d'ennemi doit être une case libre.

**Rentre avec une petite extension (Rivet, compté dans le jalon 1)** :
- PNJ cachés → `si: '<drapeau>'` sur le PNJ (rendu, clic, dialogue) ; la levée à < 6 m passe par un déclencheur de zone.
- Déclencheurs T1-T3 et la garde x = 23 → `TRIGGERS` avec `zone: {x,z,w,d}` vérifiés à chaque changement de case (aujourd'hui seulement à l'entrée d'un lieu, `game.js:241`).
- Quilla qui « se lève et marche jusqu'à (19 ; 12) » : pas de PNJ scripté en marche → **deux poses** (`rc_quilla_assise` si `!emb_t1`, `rc_quilla` debout en (19 ; 12) si `emb_t1`), dialogue ouvert par T1.
- Morsa sur le plateau à +1,3 (plancher de l'épave mesuré par Ocre, PILOTE §15 ; corrige 2,0) : rendu par `y: 1.3` sur le PNJ (`userData.y0` au rendu, trié au-dessus de l'épave), **pas** par `niveaux` (sinon l'approche depuis le lit est refusée, écart > 1,2 m, `game.js:73`) ; sa case doit rester libre (niche dans le solide de l'épave) ; approche filtrée sur les cases atteignables.
- Examens (traces ★, panneau, pneus…) → `SPOTS` `kind: 'examen'` (texte + `flag:`) ; texte selon Observation → condition `observation>=4` lue sur la compétence (aujourd'hui `cond` ne lit que les attributs).
- Fouilles à condition ou à test (C2, cache, plateau) → `SPOTS` `kind: 'scene'` + petit nœud de dialogue (existe) ; fouille simple → `pickup` (un objet) ; plusieurs objets + argent → nœud `enter: 'gain:22;give:water:3;…'`.
- Combat `embuscade_piste` : ennemis en positions absolues (table §8 recalculée), `centre` sans téléporter le joueur, `si` par ennemi (absent si `_ko`, `_parti`, `_achete`), `entreTour: 2` (Tuerto), `rendSous: 0.25` (Quilla → issue victoire), issue fuite → `rencontre:quitter`.
- Issues : `pay:` refuse si l'argent manque → `payMax:20` (prend au plus 20 $) pour reddition et défaite ; défaite = `warp` à l'apparition + 1 PV (existe).

**Ne rentre pas, à changer dans la fiche (Ocre)** :
1. **Lit à −0,8 m** : `niveaux` ne descend pas sous 0 → lit au niveau 0, creux rendu par le sol `g_rc_lit` et les berges `rc_ds_berge_3q`.
2. **« Ne tire pas si acheté »** : pas d'ennemi neutre en combat → un guetteur acheté est **absent** du combat.
3. **Persistance par case `emb_regle_<case>`** : un drapeau ne porte pas la case → journal `region.rencontres['col,row'] = { id, regle }` tenu par le gestionnaire ; les drapeaux `emb_*` sont remis à zéro à la sortie (sinon la prochaine embuscade, sur une autre case, hérite des traces vues).
4. **Trait « Œil de pillard »** : n'existe pas → C2 sur `observation>=4` seul, ou trait à créer plus tard.
5. **Survol à 4 m sur mobile** : pas d'examen au survol → clic / appui sur le point d'examen (anneau comme les portes).
6. **Pibe `fuitTour: 2` + `rendSous`** : gardés, mais la « reddition de la bande » = victoire (le moteur n'a pas d'issue « l'ennemi se rend »).
7. Combat sur la crête : aucun avantage de hauteur ni « crête vue d'en bas = 2 » ; couverture de Pibe = 1 (rocher R1 voisin).

Format : clés `rc_*` et `g_rc_*` validées, ancre et 50 px/m comme les autres lots ; PNJ debout + pose assise pour Quilla et couchée pour Morsa (déjà prévue). Ocre peut lancer les sprites.

Maquette v0.13 (idées seulement, code non repris ; `dist/` absent de l'archive) : convoi à fouiller, caravane à stock limité, récupératrice blessée, péage de pillards, mutants déments, drone IO, front de poussière (`README.md:70`, `tests/world.test.js:16-28`). Règles utiles : une case visitée ne relance pas sa rencontre, butin et morts persistants, sortie bloquée tant qu'un hostile tient la position, chargement en trajet = halte sur la dernière case.
