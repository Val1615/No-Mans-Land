# Center-Town : Carrefour Arcadius (`steel_center`, dalle de Steel-Mégalopolis)

Pack créatif et modulaire d'Ocre pour le développeur (Rivet). Légende : **[canon]** = site Groovy Crew ou roman ; **[décision]** = consigne de Valentin ; **[proposition]** = mise en œuvre d'Ocre, prête à brancher.

## Périmètre et règles fixées
- **[canon]** Center-Town : des tours, dont l'Arcadius Center, siège de la gestion et de la sécurité d'IO (roman, Ch. III §854). La ville utilise le crédit. Le jeu se déroule en 2175.
- **[décision]** Premier quartier après la douane : `steel_center` (48 x 36 m), sur la dalle surélevée de Steel-Mégalopolis.
- **[décision]** Périmètre strict de cette refonte : uniquement le **carrefour Arcadius**, c'est-à-dire le QG Arcadius IO, le grand carrefour, les rues, les trottoirs, le Dôme Fréquence, le Bureau des Permis Administratifs, les tours à publicités qui bordent ce carrefour et le mobilier/transport de ce carrefour. Rien d'autre dans Center-Town, et rien qui touche Lower-Town.
- **[décision]** Direction visuelle (synthèse des concepts validés par Valentin) :
  - **Vraie nuit noire** (`#05070d`), chaussée d'asphalte noir mouillé à reflets localisés sous les sources visibles, trottoirs en grandes dalles d'anthracite humides.
  - **Fenêtres ambre** sur tous les bâtiments, véhicules et abris.
  - **Rouge réservé exclusivement aux bannières et aux balises IO** (QG Arcadius, mâts de bannières IO, lampadaires IO, balises de toit). Aucune autre façade ni devanture rouge.
  - **Publicités multicolores** (ambre, blanc chaud, cyan, vert émeraude, bleu électrique, magenta ; jamais uniformément violet) sur au moins quatre tours différentes sans clone : *ARCHEON Industries*, *Orc Énergie*, *Teng Banque Nationale*, *Human Corp*, *NEXUS*, *« Groovy Crew en concert »*.
  - **Caissons techniques sur tous les toits** : groupes CVC, ventilateurs, gaines, conduites, cheminées et balise rouge IO de gabarit.
  - **Enseignes lisibles** en français ou en anglais uniquement, sans faux idéogramme ni texte parasite.
  - **Secret absolu** : le nom civil de Groovy Vibes ne figure nulle part.

## Géométrie et conventions techniques
- Échelle moteur : `50 px/m` (`K = 50`), lacet `34,5°`, tangage `28,8°`.
- Pente des faces `x` (rue, à gauche de l'ancre) : `0,33` (`W x 41,21 px`).
- Pente des faces `z` (retour, à droite de l'ancre) : `0,70` (`D x 28,32 px`).
- **Emprises** : toutes les pièces `ct_*_3q` sont en **multiples de 4 m**, avec une **profondeur minimale de 4 m** (`D >= 4 m`).
- **Ancre** : au pied exact du coin avant sud-est `(x + W ; z + D)`, posé au sol (`dy = 0 px`), avec **ombre de contact** intégrée et silhouette de toit nette sans dents de scie.
- **Calques additifs** (même taille `px` et même `anchor` que le sprite parent) :
  - `<clé>_fenetres` : lueur chaude ambre des fenêtres, vitrines et lanternes (chargement automatique par `view.js`, hors plafond mobile).
  - `<clé>_neon` : enseignes lumineuses, lettrages et balisage IO (chargement automatique par `view.js`, réglable via `loc.enseignes`, hors plafond mobile).
  - `<clé>_ecran` : grands panneaux publicitaires numériques, hologramme suspendu et balises de toit (piloté par `view.js` via `loc.pulses` en modes `mesure` ou `balise`).
- **Dossier et index** : `assets/steel/center_town/`, index `assets/steel/center_town/manifest.json` (86 entrées : 7 sols `g_ct_*`, 22 éléments `ct_*_3q` et 57 calques additifs).

---

## 1. Sols, carrefour et trottoirs (`g_ct_*`, 512 x 512 px, `tile_m: 4.0`) [proposition]

Toutes les tuiles font `512 x 512 px` (`4 x 4 m`), tuilables sans raccord. Comme `paintTerrain` dans `src/render/textures.js` répète les motifs sur un pas de `4 m` depuis `(0 ; 0)`, caler la chaussée est-ouest sur `z = 16..20` et l'avenue nord-sud sur `x = 28..36` aligne les passages piétons, les rails et la case jaune hachurée au pixel près.

| clé | px | `tile_m` | rôle et pose sur `steel_center` (48 x 36 m) |
|---|---|---|---|
| `g_ct_trottoir_dalles` | 512 x 512 | 4,0 | Sol de base (`ground.skin`) : grandes dalles de granit anthracite humides (trottoirs nord `z 12..16`, sud `z 20..24`, parvis et passages) |
| `g_ct_asphalte_mouille` | 512 x 512 | 4,0 | Voie nord-sud est (`x 32..36`, `z 0..12` et `24..36`) et `ground.marge` (`m: 48`, voile nocturne `rgba(4,6,12,.64)`) |
| `g_ct_rails_tram_ew` | 512 x 512 | 4,0 | Chaussée est-ouest à rails encastrés : `(0, 16, 24, 4)` et `(40, 16, 8, 4)` |
| `g_ct_rails_tram_ns` | 512 x 512 | 4,0 | Voie de tram nord-sud : `(28, 0, 4, 12)` et `(28, 24, 4, 12)` |
| `g_ct_passage_pieton_ns` | 512 x 512 | 4,0 | Passages piétons ouest et est du carrefour : `(24, 16, 4, 4)` et `(36, 16, 4, 4)` |
| `g_ct_passage_pieton_ew` | 512 x 512 | 4,0 | Passages piétons nord et sud du carrefour : `(28, 12, 8, 4)` et `(28, 20, 8, 4)` |
| `g_ct_carrefour_jaune` | 512 x 512 | 4,0 | Case centrale jaune hachurée du carrefour Arcadius : `(28, 16, 8, 4)` |

---

## 2. Bâtiments, tours à pubs, transports et mobilier (`ct_*_3q`) [proposition]

### A. Monuments et tours à publicités (8 bâtiments majeurs, 0 clone)

| clé `_3q` | rôle / enseigne | px | ancre | emprise WxD | h (m) | calques | pose proposée `(x, z, w, d)` |
|---|---|---|---|---|---|---|---|
| `ct_arcadius_qg_3q` | **QG Arcadius IO** (« ARCADIUS QG IO · SÉCURITÉ IO », bannières rouges IO, statues dorées, portail gardé) | 838 x 1115 | [496, 1113] | 12 x 12 m | 17,5 | `_neon`, `_fenetres`, `_ecran` | `B('c_arcadius', 'Arcadius Center', 'ct_arcadius_qg_3q', 36, 0, 12, 12)` |
| `ct_dome_frequence_3q` | **Le Dôme Fréquence** (verrière dorée, écran chanteuse Vibes, « LE DÔME FRÉQUENCE · MÉDIAS INFORMATION CULTURE ») | 838 x 1044 | [496, 1042] | 12 x 12 m | 14,5 | `_neon`, `_fenetres`, `_ecran` | `B('c_tour', 'Le Dôme Fréquence', 'ct_dome_frequence_3q', 16, 0, 12, 12, { visitable: true })` |
| `ct_bureau_permis_3q` | **Bureau des Permis Administratifs** (logo IO blanc, « BUREAU DES PERMIS · IDENTITÉ · ACTIVITÉS ») | 561 x 640 | [332, 638] | 8 x 8 m | 8,0 | `_neon`, `_fenetres`, `_ecran` | `B('c_blanc', 'Bureau des permis', 'ct_bureau_permis_3q', 40, 28, 8, 8)` |
| `ct_tour_teng_3q` | **Tour 1 : Teng Banque Nationale & Change de Teng** (visitable, « TENG BANQUE NATIONALE · CHANGE · CRÉDITS ») | 561 x 934 | [332, 931] | 8 x 8 m | 15,5 | `_neon`, `_fenetres`, `_ecran` | `B('c_change', 'Change de Teng', 'ct_tour_teng_3q', 4, 4, 8, 8, { visitable: true, cue: 'coin' })` |
| `ct_tour_archeon_3q` | **Tour 2 : ARCHEON Industries** (billboard ambre géant « ARCHEON INDUSTRIES » + écran bleu) | 561 x 1048 | [332, 1046] | 8 x 8 m | 17,0 | `_neon`, `_fenetres`, `_ecran` | `B('ct_archeon', 'Tour Archeon Industries', 'ct_tour_archeon_3q', -8, 4, 8, 8)` |
| `ct_tour_orc_3q` | **Tour 3 : Orc Énergie** (billboard vert émeraude et cyan « ORC ÉNERGIE » + néon vertical « ORC ») | 561 x 1109 | [332, 1107] | 8 x 8 m | 16,5 | `_neon`, `_fenetres`, `_ecran` | `B('ct_orc', 'Tour Orc Énergie', 'ct_tour_orc_3q', 48, 2, 8, 8)` |
| `ct_tour_humancorp_3q` | **Tour 4 : Human Corp** (panneau blanc/cyan « HUMAN CORP » + affiche magenta « GROOVY CREW EN CONCERT ») | 561 x 1011 | [332, 1009] | 8 x 8 m | 16,0 | `_neon`, `_fenetres`, `_ecran` | `B('ct_humancorp', 'Tour Human Corp', 'ct_tour_humancorp_3q', 4, -8, 8, 8)` |
| `ct_tour_nexus_3q` | **Tour 5 : NEXUS** (enseigne verticale cyan électrique « NEXUS » + écran « RÉSEAU OPTIMUM ») | 561 x 984 | [332, 982] | 8 x 8 m | 17,0 | `_neon`, `_fenetres`, `_ecran` | `B('ct_nexus', 'Tour Nexus', 'ct_tour_nexus_3q', 20, -8, 8, 8)` |

### B. Bâtiments bas de bordure sud (hauteur 6,5 m pour dégager la vue sur le carrefour, 0 clone)

| clé `_3q` | rôle / enseigne | px | ancre | emprise WxD | h (m) | calques | pose proposée `(x, z, w, d)` |
|---|---|---|---|---|---|---|---|
| `ct_bord_sud_a_3q` | Immeuble commercial sud-ouest (« NEXUS TRANSIT », caissons CVC) | 447 x 517 | [332, 515] | 8 x 4 m | 6,5 | `_neon`, `_fenetres`, `_ecran` | `B('c_immeuble', 'Immeuble Nexus Transit', 'ct_bord_sud_a_3q', 0, 32, 8, 4)` |
| `ct_bord_sud_b_3q` | Galerie couverte sud (« GROOVY CREW EN CONCERT », vitrines ambre, caissons CVC) | 447 x 565 | [332, 563] | 8 x 4 m | 6,5 | `_neon`, `_fenetres`, `_ecran` | `B('c_galerie', 'Galerie du Carrefour', 'ct_bord_sud_b_3q', 8, 32, 8, 4)` |
| `ct_bord_sud_c_3q` | Pavillon d'angle sud-ouest du carrefour (« HUMAN CORP · GUICHETS », caissons CVC) | 396 x 517 | [167, 515] | 4 x 8 m | 6,5 | `_neon`, `_fenetres`, `_ecran` | `B('c_neon', 'Guichets Human Corp', 'ct_bord_sud_c_3q', 20, 28, 4, 8)` |

### C. Transports, hologramme suspendu et mobilier urbain (toutes emprises >= 4 m de profondeur)

Pour les ouvrages franchissants (`cover: true`) et le mobilier sur dalle de trottoir `4 x 4 m`, le champ `solid` ne bloque que les piles ou le fût central afin de laisser les trottoirs et accès entièrement praticables.

| clé `_3q` | rôle / enseigne | px | ancre | emprise WxD | h (m) | calques | pose proposée et `solid` |
|---|---|---|---|---|---|---|---|
| `ct_monorail_viaduc_3q` | Viaduc surélevé du monorail sur piles (segment nord, feux ambre en sous-face) | 509 x 460 | [167, 458] | 4 x 12 m | 8,5 | `_neon`, `_fenetres` | `(0, 0, 4, 12)`, `cover: true`, `solid` sur piles `(0.4, 0.4, 2, 2)` et `(0.4, 9.8, 2, 2)` |
| `ct_monorail_rame_3q` | Viaduc surélevé avec rame profilée « MEGA-LINE » en passage au-dessus de l'entrée ouest | 509 x 428 | [167, 426] | 4 x 12 m | 9,2 | `_neon`, `_fenetres` | `(0, 12, 4, 12)`, `cover: true`, `solid` sur piles `(0.4, 12.4, 2, 2)` et `(0.4, 21.8, 2, 2)` (`c_ouest` en `z=18` passe sous l'arche) |
| `ct_holo_suspendu_3q` | Portique d'avenue projetant l'hologramme suspendu cyan/ambre « NEXUS » sur le carrefour | 509 x 581 | [167, 579] | 4 x 12 m | 9,0 | `_neon`, `_fenetres`, `_ecran` | `(24, 12, 4, 12)`, `cover: true`, `solid` sur mâts `(24.6, 12.6, 1.4, 1.4)` et `(24.6, 22.0, 1.4, 1.4)` |
| `ct_arret_tram_3q` | Arrêt de tramway vitré sur quai dallé (« TRAM CENTRAL », éclairage ambre) | 447 x 346 | [332, 344] | 8 x 4 m | 3,8 | `_neon`, `_fenetres`, `_ecran` | `(4, 12, 8, 4)`, `solid: [{ x: 4.5, z: 12.3, w: 7.0, d: 1.4 }]` |
| `ct_tram_3q` | Tramway articulé argent et anthracite (« CENTER-TOWN », fenêtres ambre, pantographe) | 509 x 314 | [167, 312] | 4 x 12 m | 3,8 | `_neon`, `_fenetres` | `(28, 22, 4, 12)` sur les rails N-S, `solid: [{ x: 28.8, z: 22.8, w: 2.4, d: 10.4 }]` |
| `ct_taxi_3q` | Taxi jaune de Steel sur dalle d'asphalte mouillé (lumineux « TAXI » ambre) | 282 x 231 | [167, 229] | 4 x 4 m | 2,2 | `_neon`, `_fenetres` | `(14, 16, 4, 4)` et `(42, 16, 4, 4)` (dégage `c_est` en `48, 18`), `solid` `3,0 x 2,1 m` |
| `ct_echoppe_vapeur_3q` | Échoppe de rue à vapeur (« NOUILLES & VAPEUR », acier sombre et laiton, marmites fumantes) | 282 x 317 | [167, 315] | 4 x 4 m | 3,6 | `_neon`, `_fenetres` | `(4, 20, 4, 4)`, `solid: [{ x: 4.5, z: 21.5, w: 3.0, d: 2.1 }]` |
| `ct_kiosque_info_3q` | Kiosque multimédia (« PRESSE · MÉDIAS », comptoir ambre, écran latéral magenta/cyan) | 282 x 322 | [167, 320] | 4 x 4 m | 3,6 | `_neon`, `_fenetres`, `_ecran` | `(12, 20, 4, 4)`, `solid: [{ x: 12.6, z: 21.5, w: 2.8, d: 2.1 }]` |
| `ct_lampadaire_io_3q` | Lampadaire fonte/laiton à double lanterne ambre et bannière rouge « IO » sur dalle 4x4 | 282 x 295 | [167, 292] | 4 x 4 m | 5,4 | `_neon`, `_fenetres` | `(20, 12, 4, 4)` et `(36, 20, 4, 4)`, `solid` fût `1,0 x 1,0 m` |
| `ct_banniere_io_3q` | Mât cérémoniel à bannière verticale rouge « IO » et balise rouge sur socle 4x4 | 282 x 326 | [167, 323] | 4 x 4 m | 6,2 | `_neon`, `_fenetres` | `(36, 12, 4, 4)` et `(44, 12, 4, 4)` devant le QG Arcadius, `solid` `1,2 x 1,2 m` |
| `ct_cerisier_bac_3q` | Cerisier en fleurs roses dans un bac carré en granit anthracite éclairé en ambre | 282 x 349 | [167, 347] | 4 x 4 m | 4,2 | `_fenetres` | `(12, 12, 4, 4)` et `(36, 24, 4, 4)`, `solid` bac `2,0 x 2,0 m` |

---

## 3. Anciennes clés marquées `"obsolete": true` (champs existants intacts)

Aucune clé existante n'a été supprimée ni altérée dans ses dimensions ou son ancre ; seul `"obsolete": true` a été ajouté :
- Dans `assets/buildings/manifest.json` (8 clés remplacées) :
  - `b_st_ct_tower` -> `ct_arcadius_qg_3q` (`c_arcadius`)
  - `b_st_ct_dome` -> `ct_dome_frequence_3q` (`c_tour`)
  - `b_st_ct_shop` -> `ct_tour_teng_3q` (`c_change`)
  - `b_st_blanc` -> `ct_bureau_permis_3q` (`c_blanc`)
  - `b_st_immeuble` -> `ct_bord_sud_a_3q` (`c_immeuble`)
  - `b_st_galerie` -> `ct_bord_sud_b_3q` (`c_galerie`)
  - `b_st_neon` -> `ct_bord_sud_c_3q` (`c_neon`)
  - `b_st_jumelles` -> retiré au profit du dégagement de l'avenue nord-sud `x 28..36` (remplacé visuellement par les tours à pubs `ct_tour_*_3q`)
- Dans `assets/reused/manifest.json` (8 props remplacés par les modules `ct_*_3q` ; `st_civil0..5` et `st_drone` restent actifs) :
  - `st_echoppe` -> `ct_echoppe_vapeur_3q`
  - `st_kiosque` -> `ct_kiosque_info_3q`
  - `st_lampadaire` -> `ct_lampadaire_io_3q`
  - `st_holo` -> `ct_holo_suspendu_3q`
  - `st_voiture` -> `ct_taxi_3q` et `ct_tram_3q`
  - `st_borne`, `st_banc`, `st_pylone` -> `ct_arret_tram_3q`, `ct_banniere_io_3q`, `ct_cerisier_bac_3q`

---

## 4. Swaps et intégration à faire côté code (Rivet)

1. **Catalogue (`src/core/catalogue.js` et `tests/editor-integration.mjs`)** :
   - Ajouter `'center_town'` à `QUARTIERS_STEEL`.
   - Étendre l'expression régulière des bâtiments de quartiers à `/^(pp|fs|ar2?|df|ml|ct)_/` pour charger `ct_*_3q` et leurs calques dans `bman` (les `g_ct_*` passent déjà automatiquement dans `sols`).
2. **Portes intérieures de `steel_center` (`buildings_steel.js` et `dome_frequence.js`)** :
   - `c_change_door` (sur `c_change`, `ct_tour_teng_3q` en `(4, 4, 8, 8)`) : face est, `painted_px: [430, 825]`, `opening: [12.0, 8.5]`, `threshold: [13.0, 8.5]` (donne dans l'allée libre `x 12..16`).
   - `c_dome` (sur `c_tour`, `ct_dome_frequence_3q` en `(16, 0, 12, 12)`) : face sud, `opening: { x: 22.0, z: 12, side: 'south' }`, `threshold: { x: 22.0, z: 13 }`.
   - Retirer `...FACADE_DOME` de `LOCATIONS.steel_center.buildings` dans `src/data/steel.js` : l'écran chanteuse est désormais peint et éclairé directement dans `ct_dome_frequence_3q` + `ct_dome_frequence_3q_ecran` (et `c_e_tron` en `x = 28,5` flotterait au milieu de l'avenue nord-sud).
3. **Vérification des 8 jonctions de bord (toutes dégagées sans modifier leurs coordonnées)** :
   - Ouest `c_ouest` `(0 ; 18)` (passe sous l'arche de `ct_monorail_rame_3q`), Est `c_est` `(48 ; 18)`.
   - Nord `c_mega` `(8 ; 0)`, `c_strip` `(14 ; 0)`, `c_nord` `(33 ; 0)`.
   - Sud `c_sud` `(19,5 ; 36)`, `c_pp_sud` `(26 ; 36)`, `c_sud_est` `(38 ; 36)`.
4. **Éclairage de vraie nuit, calques et halos (`src/data/steel.js`)** :
   - Lumière de vraie nuit noire sans dominante violette : `{ bg: '#05070d', hemi: ['#9ab0d4', '#141824', 1.08], sun: ['#dce4f5', 0.55], tint: '#d8dce8', actor: '#e2dee8' }`, et `tint: '#ffffff'` sur les bâtiments `ct_*_3q`.
   - Vider `loc.props` (remplacé par les modules `ct_*_3q` dans `loc.buildings`).
   - Brancher `loc.pulses` en modes autonomes hors kick (`mode: 'balise'` sur `c_arcadius` pour les balises rouges IO ; `mode: 'mesure'` sur `c_tour`, `ct_holo0`, `ct_orc`, `ct_archeon`, `ct_nexus`, `ct_humancorp` avec `priorite` sur 4 calques afin de rester sous le plafond mobile `pulsesOn <= 8`).
   - Ne poser des `glows` au sol **que sous les sources visibles** : arrêt de tram `(8 ; 14,5)` cyan doux, échoppe vapeur `(6 ; 23,8)` ambre vacillant, kiosque `(14 ; 23,8)` magenta doux, lampadaires `(22 ; 14,2)` et `(38 ; 21,8)` ambre chaud, hologramme suspendu `(26 ; 18)` cyan, entrée du Dôme `(22 ; 12,8)` ambre, parvis QG Arcadius `(42 ; 13)` rouge IO discret, phares des deux taxis `(16 ; 18)` et `(44 ; 18)` ambre.
5. **Figurants, passants et suite `tests/steel_l1.py`** :
   - Boucles `walkers` et `extras` testées dans un rendu moteur hors repo avec **`window.__nml.view.masques() === []`** :
     - `extras` : soldats devant le QG en `(41,2 ; 13,8)` et `(43,8 ; 13,8)` ; clients en `(21,8 ; 14,2)` et `(28,8 ; 13,8)`.
     - `walkers` : `[[17.5, 16.3], [35.0, 16.3], [35.0, 19.7], [17.5, 19.7]]`, `[[35.0, 19.5], [18.5, 19.5], [18.5, 16.5], [35.0, 16.5]]`, `[[2.5, 16.4], [22.5, 16.4], [22.5, 19.4], [2.5, 19.4]]`, `[[30.2, 2.5], [30.2, 19.5], [32.2, 19.5], [32.2, 2.5]]`, `[[27.0, 16.2], [32.4, 16.2], [32.4, 19.2], [27.0, 19.2]]`.
   - Dans `tests/steel_l1.py` (lignes 227 et 239) : adapter l'assertion `ground.skin === 'g_wet'` / `bg === '#0b0a16'` et le comptage des anciens `props` `st_echoppe` / `st_holo` / `st_lampadaire` vers les nouveaux modules `ct_*_3q` dans `W['buildings']`.

---

## 5. Planches de contrôle
- `/workspace/nml-shots/center_town_v1.png` : **maquette composée d'assets** (présentation DA avec scène isométrique recomposée, décomposition des calques `_fenetres` / `_neon` / `_ecran` et catalogue des 22 modules + 7 sols ; **pas une capture du jeu**).
- `/workspace/nml-shots/center_town_audit.png` : **vraie capture moteur Three.js hors repo** (`/tmp/nml-ct-preview`, desktop `1280 x 800` dézoomé `x0,6`, vue carrefour `x1,0`, entrée ouest et mobile `390 x 844` DPR 2 ; `masques = []`, `0` erreur console/réseau, `10/10` portes et PNJ joignables, `pulsesOn = 8/8` sur mobile).

---

## 6. Correctif v2 : échelle cerisier/taxi et vraies hautes tours à pubs (`*_v2_3q`)

Toutes les clés v1 remplacées ci-dessous (ainsi que leurs calques v1) reçoivent uniquement `"obsolete": true` dans `assets/steel/center_town/manifest.json` ; aucun fichier ni champ existant n'est écrasé.

### A. Tableau des swaps v1 -> v2

| Ancienne clé (`obsolete: true`) | Problème v1 | Nouvelle clé v2 | `px` | `anchor` | Emprise `W x D` | `h` (m) | Calques | Pose `B(...)` mise à jour |
|---|---|---|---|---|---|---|---|---|
| `ct_cerisier_bac_3q` | Trop massif (`349 px`), dépassait les immeubles bas | `ct_cerisier_bac_v2_3q` | `282 x 260` | `[167, 257]` | `4 x 4 m` (bac `2 x 2 m` centré sur la dalle `4 x 4 m`) | `4,4` | `_fenetres` | `B('ct_ceris0', '', 'ct_cerisier_bac_v2_3q', 12, 12, 4, 4, { named: false, solid: [{ x: 13, z: 13, w: 2, d: 2 }] })` et `ct_ceris1` en `(36, 24, 4, 4)` |
| `ct_taxi_3q` | Aussi gros qu'une échoppe (`282 x 231` sur socle) | `ct_taxi_v2_3q` | `240 x 143` | `[187, 141]` | `4,5 x 1,8 m` (vraie berline à `50 px/m`, sans dalle socle) | `1,45` | `_neon`, `_fenetres` | `B('ct_taxi0', '', 'ct_taxi_v2_3q', 41.5, 17.1, 4.5, 1.8, { named: false })` et `ct_taxi1` en `(13.5, 17.1, 4.5, 1.8)` |
| `ct_tour_teng_3q` | Trop basse (`15,5 m`), pubs trop sages | `ct_tour_teng_v2_3q` | `561 x 1902` | `[332, 1900]` | `8 x 8 m` *(inchangée)* | `40,3` | `_neon`, `_fenetres`, `_ecran`, `_pulse` | `B('c_change', 'Change de Teng', 'ct_tour_teng_v2_3q', 4, 4, 8, 8, { visitable: true, cue: 'coin' })` |
| `ct_tour_archeon_3q` | Trop basse (`17,0 m`), pubs trop sages | `ct_tour_archeon_v2_3q` | `561 x 2079` | `[332, 2077]` | `8 x 8 m` *(inchangée)* | `44,3` | `_neon`, `_fenetres`, `_ecran`, `_pulse` | `B('ct_archeon', 'Tour Archeon Industries', 'ct_tour_archeon_v2_3q', -8, 4, 8, 8)` |
| `ct_tour_orc_3q` | Trop basse (`16,5 m`), pubs trop sages | `ct_tour_orc_v2_3q` | `561 x 1888` | `[332, 1886]` | `8 x 8 m` *(inchangée)* | `40,0` | `_neon`, `_fenetres`, `_ecran`, `_pulse` | `B('ct_orc', 'Tour Orc Énergie', 'ct_tour_orc_v2_3q', 48, 2, 8, 8)` |
| `ct_tour_humancorp_3q` | Trop basse (`16,0 m`), pubs trop sages | `ct_tour_humancorp_v2_3q` | `561 x 2038` | `[332, 2035]` | `8 x 8 m` *(inchangée)* | `43,4` | `_neon`, `_fenetres`, `_ecran`, `_pulse` | `B('ct_humancorp', 'Tour Human Corp', 'ct_tour_humancorp_v2_3q', 4, -8, 8, 8)` |
| `ct_tour_nexus_3q` | Trop basse (`17,0 m`), pubs trop sages | `ct_tour_nexus_v2_3q` | `561 x 2113` | `[332, 2111]` | `8 x 8 m` *(inchangée)* | `45,1` | `_neon`, `_fenetres`, `_ecran`, `_pulse` | `B('ct_nexus', 'Tour Nexus', 'ct_tour_nexus_v2_3q', 20, -8, 8, 8)` |

### B. Points côté code spécifiques à la v2 (Rivet)

1. **Porte peinte de `c_change` (`ct_tour_teng_v2_3q`, `561 x 1902 px`)** :
   - Mettre `painted_px: [430, 1792]`, `face: 'e'`, `opening: [12.0, 8.5]`, `threshold: [13.0, 8.5]`.
2. **Non-masquage des portes, du joueur et des passants par les tours de 40–45 m (vérifié en rendu Three.js réel)** :
   - `ct_archeon` `(-8, 4, 8, 8)`, `ct_humancorp` `(4, -8, 8, 8)` et `ct_nexus` `(20, -8, 8, 8)` ont leur emprise hors du rectangle jouable nord/ouest (`x1 <= 0` ou `z1 <= 0`) : `inFront(tour, acteur)` dans `view.js` vaut **toujours `false`**, elles restent en permanence derrière le joueur, les PNJ et tous les anneaux de portes.
   - `ct_orc` `(48, 2, 8, 8)` est hors bord est (`visitable: false`) : le clic sol passe au travers (`view.js` l. 832) et `spriteOcclusion()` la fond à `0,30` si le joueur longe le coin nord-est.
   - `c_change` (`ct_tour_teng_v2_3q`, `(4, 4, 8, 8)`, `40,3 m`, `visitable: true`) : dès que le joueur passe au nord (`z < 4`, accès `c_mega` en `(8 ; 0)`), **`spriteOcclusion()` (`view.js` l. 630) passe automatiquement la tour et ses 4 calques en fondu à `30 %` (`fondu`)**, laissant le joueur et le seuil `c_mega` `(8 ; 1)` parfaitement visibles et cliquables (`pick(8, 0.03, 1)` renvoie bien `ground` / `c_mega`).
   - *Astuce optionnelle `pick()` (`view.js` l. 836)* : tant que le joueur est encore au sud (`z > 4`, `c_change` à opacité `1`), cliquer directement l'anneau doré `c_mega` fonctionne déjà (priorité `ring` l. 825), mais un clic sur le sol `(8 ; 2,5)` à travers le haut de la tour `c_change` renvoie `c_change_door` parce que `u.visitable === true` ne passe pas par le filtre d'emprise de la l. 832. Appliquer le même test `g.point` hors `[b.x - 1 .. b.x + b.w + 1, b.z - 1 .. b.z + b.d + 1]` avant de renvoyer la porte d'un bâtiment visitable rend aussi le sol nord directement cliquable à distance.
   - Pour le passant ouest `civ(3)`, borner sa boucle sur la chaussée `[[2.5, 16.4], [22.5, 16.4], [22.5, 18.4], [2.5, 18.4]]` pour qu'il ne frôle jamais l'arrière de `ct_kiosque0` (`view.masques() === []` à tout instant).
3. **Calques `_pulse` sur le kick (`ct_tour_*_v2_3q_pulse`)** :
   - Les 5 tours v2 fournissent chacune leur calque `<clé>_pulse` (bandeaux LED égaliseur, tubes d'angle et balise de toit, `bande: "kick"`).
   - Dans `src/core/ost_centre.js` l. 181 et 183, `sampleRhythm()` n'échantillonne actuellement l'analyseur Web Audio que si `mode === 'ost_centre'`. Étendre ce test à `(mode === 'ost_centre' || mode === 'ost_center_town')` permet aux `_pulse` des 5 tours de battre en direct sur le kick de `01_center_town.mp3` (sinon ils restent sagement en `veille` fixe, plafonnés à `pulsesOn <= 8` sur mobile).

### C. Planches de contrôle v2
- `/workspace/nml-shots/center_town_v2.png` : **maquette composée d'assets** (scène isométrique v2 recomposée, comparatif d'échelle 1:1 `v1 obsolete` vs `v2` avec humain `1,8 m`, décomposition des 4 calques dont `_pulse` et galerie des 7 clés `*_v2_3q` ; **pas une capture du jeu**).
- `/workspace/nml-shots/center_town_v2_audit.png` : **vraie capture moteur Three.js hors repo** (vue dézoomée `x0,6` des tours de `40–45 m`, échelle rue `1:1` joueur / taxi v2 / cerisier v2, test de fondu automatique `30 %` de la Tour Teng `40,3 m` devant `c_mega`, et mobile `390 x 844` avec `pulsesOn = 8/8`).

---

## 7. Correctif v3 : régénération sans déformation de tous les modules `ct_*` (`*_v3_3q`)

Les sprites v1/v2 avaient été mis en perspective par `build_center_town.py` / `build_center_town_v2.py` (warp par morceaux et cisaillement). La v3 repart de bruts neufs générés au gabarit caméra du jeu (`/workspace/ct_raw/gen_v3*.jpg`, hors dépôt) et **n'utilise aucun de ces deux scripts**.

### A. Méthode (`/workspace/ct_raw/build_center_town_v3.py` + `run_center_town_v3.py`)

1. **Détourage** du fond chroma (vert, ou magenta pour la Tour Orc).
2. **Crop polygonal du pied** : coupe alpha uniquement, aucun pixel déplacé. On suit les deux droites théoriques à 18,3° et 35° qui passent par les coins latéraux mesurés. Les bruts ont un pied plus raide que la caméra (perspective), le toit est juste. L'écart ≤ 8 px sous la coupe est comblé par une bande d'ombre de contact gris-noir.
3. **Une seule échelle uniforme `sx = sy`** (Lanczos prémultiplié), par moindres carrés sur les faces gauche/droite (`W x 41,21` / `D x 28,32` px). Pour les piles du viaduc, de la rame et du portique, l'échelle est réglée sur l'écart entre les piles. Pour le taxi, elle est réglée sur la caisse.
4. **Ancrage** sur le pied du coin avant (`anchor` à `H-3`) et ombre de contact. Aucun warp, aucun cisaillement, aucune mise à l'échelle anisotrope.
5. **Calques** `_neon` / `_fenetres` / `_ecran` / `_pulse` extraits du sprite final, sur le **même canevas et avec la même ancre** que le parent (`px` et `anchor` identiques, `additive: true`, `parent`).
6. **Contrôle** : arêtes de toit mesurées sur le sprite final à ±2° de 35° / 18,3°, toit en parallélogramme. Les mesures sont dans `geometrie_v3` de chaque entrée du manifest (`echelle_uniforme`, `emprise_mesuree_m`, `arete_*_deg`, `dy`, données de piles).

**`"obsolete": true` est différé jusqu'à la bascule du code.** Depuis `d297ad6`, `src/core/catalogue.js` (l. 13) retire du catalogue toute clé `obsolete`. Or les 22 clés remplacées sont encore posées par `src/data/buildings_steel.js` (intégration `801a7f3`). Les marquer maintenant ferait disparaître les 22 modules de Center-Town sur `main` : c'est vérifié en rendu réel (`enseignes = fenetres = pulses = 0`), et `npm run test:editor` échoue avec 26 « asset de bâtiment inconnu ». Ce lot ne fait donc **qu'ajouter** des entrées : aucun champ ni fichier existant n'est modifié, et chaque entrée v3 porte `remplace: <ancienne clé>`. Les 84 anciennes entrées à marquer `"obsolete": true` **dans le même commit que le swap des poses** sont les 22 clés du tableau B (colonne de gauche) et tous leurs calques `_neon` / `_fenetres` / `_ecran` / `_pulse` présents dans le manifest.

### B. Tableau des swaps ancien -> v3

| Ancienne clé (à marquer `obsolete` avec le swap) | Ancien `px` / `anchor` | Nouvelle clé v3 | `px` | `anchor` | Emprise code `W x D` | Emprise mesurée (m) | Échelle uniforme | Arêtes toit G/D (°) | Calques | Pose `B_CT(...)` |
|---|---|---|---|---|---|---|---|---|---|---|
| `ct_arcadius_qg_3q` | `838 x 1115` / `[496, 1113]` | `ct_arcadius_qg_v3_3q` | `833 x 938` | `[516, 935]` | `12 x 12 m` | [12.42, 10.99] | `1.13059` | 35.28 / 18.06 | _ecran, _fenetres, _neon | `B_CT('c_arcadius', 'Arcadius Center', 'ct_arcadius_qg_v3_3q', 36, 0, 12, 12)` |
| `ct_dome_frequence_3q` | `838 x 1044` / `[496, 1042]` | `ct_dome_frequence_v3_3q` | `840 x 822` | `[504, 819]` | `12 x 12 m` | [12.15, 11.67] | `1.06425` | 35.23 / 18.26 | _ecran, _fenetres, _neon | `B_CT('c_tour', 'Le Dôme Fréquence', 'ct_dome_frequence_v3_3q', 16, 0, 12, 12, { visitable: true })` |
| `ct_bureau_permis_3q` | `561 x 640` / `[332, 638]` | `ct_bureau_permis_v3_3q` | `556 x 590` | `[342, 587]` | `8 x 8 m` | [8.25, 7.41] | `0.72161` | 35.03 / 18.4 | _ecran, _fenetres, _neon | `B_CT('c_blanc', 'Bureau des permis', 'ct_bureau_permis_v3_3q', 40, 28, 8, 8)` |
| `ct_tour_teng_v2_3q` | `561 x 1902` / `[332, 1900]` | `ct_tour_teng_v3_3q` | `554 x 1555` | `[352, 1552]` | `8 x 8 m` | [8.41, 6.95] | `1.36521` | 35.15 / 17.75 | _ecran, _fenetres, _neon, _pulse | `B_CT('c_change', 'Change de Teng', 'ct_tour_teng_v3_3q', 4, 4, 8, 8, { visitable: true, cue: 'coin' })` |
| `ct_tour_archeon_v2_3q` | `561 x 2079` / `[332, 2077]` | `ct_tour_archeon_v3_3q` | `548 x 1563` | `[357, 1560]` | `8 x 8 m` | [8.53, 6.54] | `1.35188` | 34.49 / 18.32 | _ecran, _fenetres, _neon, _pulse | `B_CT('ct_archeon', 'Tour Archeon Industries', 'ct_tour_archeon_v3_3q', -8, 4, 8, 8)` |
| `ct_tour_orc_v2_3q` | `561 x 1888` / `[332, 1886]` | `ct_tour_orc_v3_3q` | `555 x 1490` | `[350, 1487]` | `8 x 8 m` | [8.37, 7.06] | `1.29774` | 33.74 / 17.0 | _ecran, _fenetres, _neon, _pulse | `B_CT('ct_orc', 'Tour Orc Énergie', 'ct_tour_orc_v3_3q', 48, 2, 8, 8)` |
| `ct_tour_humancorp_v2_3q` | `561 x 2038` / `[332, 2035]` | `ct_tour_humancorp_v3_3q` | `558 x 1569` | `[346, 1566]` | `8 x 8 m` | [8.29, 7.3] | `1.38489` | 35.04 / 17.86 | _ecran, _fenetres, _neon, _pulse | `B_CT('ct_humancorp', 'Tour Human Corp', 'ct_tour_humancorp_v3_3q', 4, -8, 8, 8)` |
| `ct_tour_nexus_v2_3q` | `561 x 2113` / `[332, 2111]` | `ct_tour_nexus_v3_3q` | `560 x 1607` | `[347, 1604]` | `8 x 8 m` | [8.28, 7.33] | `1.41062` | 35.19 / 17.81 | _ecran, _fenetres, _neon, _pulse | `B_CT('ct_nexus', 'Tour Nexus', 'ct_tour_nexus_v3_3q', 20, -8, 8, 8)` |
| `ct_bord_sud_a_3q` | `447 x 517` / `[332, 515]` | `ct_bord_sud_a_v3_3q` | `444 x 355` | `[332, 352]` | `8 x 4 m` | [8.02, 3.9] | `0.50223` | 35.3 / 18.28 | _ecran, _fenetres, _neon | `B_CT('c_immeuble', 'Immeuble Nexus Transit', 'ct_bord_sud_a_v3_3q', 0, 32, 8, 4)` |
| `ct_bord_sud_b_3q` | `447 x 565` / `[332, 563]` | `ct_bord_sud_b_v3_3q` | `444 x 341` | `[332, 338]` | `8 x 4 m` | [8.03, 3.86] | `0.48437` | 35.17 / 17.92 | _ecran, _fenetres, _neon | `B_CT('c_galerie', 'Galerie du Carrefour', 'ct_bord_sud_b_v3_3q', 8, 32, 8, 4)` |
| `ct_bord_sud_c_3q` | `396 x 517` / `[167, 515]` | `ct_bord_sud_c_v3_3q` | `397 x 452` | `[190, 449]` | `4 x 8 m` | [4.57, 7.24] | `0.50487` | 34.71 / 18.51 | _ecran, _fenetres, _neon | `B_CT('c_neon', 'Guichets Human Corp', 'ct_bord_sud_c_v3_3q', 20, 28, 4, 8)` |
| `ct_monorail_viaduc_3q` | `509 x 460` / `[167, 458]` | `ct_monorail_viaduc_v3_3q` | `512 x 643` | `[231, 640]` | `4 x 12 m` | piles 36.43°, pile arr. [-0.23, -0.11] | `0.86713` | — | _fenetres, _neon | `B_CT('ct_mono_v0', '', 'ct_monorail_viaduc_v3_3q', 0, 0, 4, 12, { cover: true, named: false, solid: [{ x: 0.4, z: 0.4, w: 2.0, d: 2.0 }, { x: 0.4, z: 9.8, w: 2.0, d: 2.0 }] })` |
| `ct_monorail_rame_3q` | `509 x 428` / `[167, 426]` | `ct_monorail_rame_v3_3q` | `511 x 603` | `[227, 600]` | `4 x 12 m` | piles 33.91°, pile arr. [0.19, -0.03] | `0.8206` | — | _fenetres, _neon | `B_CT('ct_mono_r0', 'Viaduc Mega-Line', 'ct_monorail_rame_v3_3q', 0, 12, 4, 12, { cover: true, named: false, solid: [{ x: 0.4, z: 12.4, w: 2.0, d: 2.0 }, { x: 0.4, z: 21.8, w: 2.0, d: 2.0 }] })` |
| `ct_holo_suspendu_3q` | `509 x 581` / `[167, 579]` | `ct_holo_suspendu_v3_3q` | `417 x 609` | `[167, 606]` | `4 x 12 m` | piles 31.89°, pile arr. [0.51, 0.4] | `0.83472` | — | _ecran, _fenetres, _neon | `B_CT('ct_holo0', '', 'ct_holo_suspendu_v3_3q', 24, 12, 4, 12, { cover: true, named: false, solid: [{ x: 24.6, z: 12.6, w: 1.4, d: 1.4 }, { x: 24.6, z: 22.0, w: 1.4, d: 1.4 }] })` |
| `ct_arret_tram_3q` | `447 x 346` / `[332, 344]` | `ct_arret_tram_v3_3q` | `442 x 368` | `[334, 365]` | `8 x 4 m` | [8.06, 3.72] | `0.5082` | 35.03 / 18.0 | _ecran, _fenetres, _neon | `B_CT('ct_arret0', 'Arrêt Tram Central', 'ct_arret_tram_v3_3q', 4, 12, 8, 4, { named: false, solid: [{ x: 4.5, z: 12.3, w: 7.0, d: 1.4 }] })` |
| `ct_tram_3q` | `509 x 314` / `[167, 312]` | `ct_tram_v3_3q` | `490 x 475` | `[135, 472]` | `4 x 12 m` | [3.23, 12.42] | `0.65979` | 33.11 / 21.73 | _fenetres, _neon | `B_CT('ct_tram0', 'Tramway Center-Town', 'ct_tram_v3_3q', 28, 22, 4, 12, { named: false, solid: [{ x: 28.8, z: 22.8, w: 2.4, d: 10.4 }] })` |
| `ct_kiosque_info_3q` | `282 x 322` / `[167, 320]` | `ct_kiosque_info_v3_3q` | `279 x 295` | `[169, 292]` | `4 x 4 m` | [4.07, 3.83] | `0.35303` | 35.39 / 17.83 | _ecran, _fenetres, _neon | `B_CT('ct_kiosque0', 'Kiosque Presse & Médias', 'ct_kiosque_info_v3_3q', 12, 20, 4, 4, { named: false, solid: [{ x: 12.6, z: 21.5, w: 2.8, d: 2.1 }] })` |
| `ct_echoppe_vapeur_3q` | `282 x 317` / `[167, 315]` | `ct_echoppe_vapeur_v3_3q` | `272 x 297` | `[176, 294]` | `4 x 4 m` | [4.24, 3.35] | `0.34397` | 30.84 / 16.42 | _fenetres, _neon | `B_CT('ct_echoppe0', 'Nouilles & Vapeur', 'ct_echoppe_vapeur_v3_3q', 4, 20, 4, 4, { named: false, solid: [{ x: 4.5, z: 21.5, w: 3.0, d: 2.1 }] })` |
| `ct_lampadaire_io_3q` | `282 x 295` / `[167, 292]` | `ct_lampadaire_io_v3_3q` | `279 x 472` | `[171, 469]` | `4 x 4 m` | [4.11, 3.75] | `0.52364` | — | _fenetres, _neon | `B_CT('ct_lamp0', '', 'ct_lampadaire_io_v3_3q', 16, 12, 4, 4, { named: false, solid: [{ x: 17.5, z: 13.5, w: 1.0, d: 1.0 }] }) ; B_CT('ct_lamp1', '', 'ct_lampadaire_io_v3_3q', 36, 20, 4, 4, { named: false, solid: [{ x: 37.5, z: 21.5, w: 1.0, d: 1.0 }] })` |
| `ct_banniere_io_3q` | `282 x 326` / `[167, 323]` | `ct_banniere_io_v3_3q` | `280 x 457` | `[170, 454]` | `4 x 4 m` | [4.08, 3.81] | `0.46339` | — | _fenetres, _neon | `B_CT('ct_bann0', '', 'ct_banniere_io_v3_3q', 36, 12, 4, 4, { named: false, solid: [{ x: 37.4, z: 13.4, w: 1.2, d: 1.2 }] }) ; B_CT('ct_bann1', '', 'ct_banniere_io_v3_3q', 44, 12, 4, 4, { named: false, solid: [{ x: 45.4, z: 13.4, w: 1.2, d: 1.2 }] })` |
| `ct_cerisier_bac_v2_3q` | `282 x 260` / `[167, 257]` | `ct_cerisier_bac_v3_3q` | `282 x 357` | `[174, 354]` | `4 x 4 m` | [4.14, 3.68] | `0.38505` | — | _fenetres | `B_CT('ct_ceris0', '', 'ct_cerisier_bac_v3_3q', 12, 12, 4, 4, { named: false, solid: [{ x: 13.0, z: 13.0, w: 2.0, d: 2.0 }] }) ; B_CT('ct_ceris1', '', 'ct_cerisier_bac_v3_3q', 36, 24, 4, 4, { named: false, solid: [{ x: 37.0, z: 25.0, w: 2.0, d: 2.0 }] })` |
| `ct_taxi_v2_3q` | `240 x 143` / `[187, 141]` | `ct_taxi_v3_3q` | `205 x 109` | `[136, 106]` | `4.5 x 1.8 m` | caisse 1.45 m | `0.24584` | — | _fenetres, _neon | `B_CT('ct_taxi1', '', 'ct_taxi_v3_3q', 13.5, 17.1, 4.5, 1.8, { named: false }) ; B_CT('ct_taxi0', '', 'ct_taxi_v3_3q', 41.5, 17.1, 4.5, 1.8, { named: false })` |

**Écarts documentés** (le ratio du brut ne colle pas exactement à l'emprise, on adapte et on documente au lieu de déformer) :
- **Tours 8 x 8** : les profondeurs mesurées vont de 6,5 à 7,3 m pour une emprise code de 8 x 8 m. L'emprise de collision reste 8 x 8 et la façade rue fait bien 8 m. Les hauteurs v3 sont `teng` 29.2 m, `archeon` 29.3 m, `orc` 27.7 m, `humancorp` 29.5 m, `nexus` 30.4 m, contre 40–45 m en v2 : la hauteur suit le ratio du brut à échelle uniforme, sans étirement vertical.
- **`ct_tram_v3_3q`** : la caisse fait 3,2 m de large sur 12,4 m. L'arête de toit droite mesure 21,7° parce que le pantographe dépasse le toit. La caisse elle-même suit 18,3°.
- **`ct_echoppe_vapeur_v3_3q`** : les arêtes de toit mesurées (30,8° / 16,4°) sont celles des capots et de la cheminée. Le bloc suit les pentes du pied (18,4° / 35,1°).
- **Piles** (écart de la pile arrière par rapport à la position théorique) : viaduc (-0,23 ; -0,11) m, rame (0,19 ; -0,03) m, portique holo (0,51 ; 0,40) m. Les `solid` actuels restent valables, avec un recalage optionnel du solide arrière du portique de +0,5 m en x et en z.

### C. Points côté code (Rivet)

1. **Poses + obsolete, en un seul commit** : remplacer la clé de sprite de chaque ligne `B_CT(...)` de `src/data/buildings_steel.js` par la clé v3 (colonne « Pose » ci-dessus). Positions, emprises et `solid` sont inchangés. Dans le même commit, ajouter `"obsolete": true` aux anciennes clés et à leurs calques (voir A), et uniquement là.
2. **`c_change_door` (Tour Teng v3, `554 x 1555 px`)** : la porte peinte est au milieu de la face est. Dans `PAINTED_DOORS_CENTER`, mettre `painted_px: [451, 1444]` au lieu de `[430, 1792]` (v2). `face: 'e'`, `opening: [12.0, 8.5]` et `threshold: [13.0, 8.5]` ne changent pas. La même valeur est écrite dans le manifest (`porte_px`).
3. **`c_dome`** : rien à changer. La porte est en coordonnées monde (`src/data/dome_frequence.js` : opening `(22, 12)`, threshold `(22, 13)`), sans `painted_px`. L'entrée du dôme v3 est peinte au milieu de la face sud.
4. **`view.masques()`** : le tram v3 a enfin sa vraie hauteur. La v1 était tassée à `509 x 314`, la v3 fait `490 x 475` à l'échelle. En rendu réel, il masque désormais `patrouilleur`, `foule18`, `foule19`, `foule20`, `foule24`, `foule25`, `foule39` et `passant53`. De plus, `c_blanc` (Bureau des permis v3) masque `foule23`, et `ct_ceris1` (cerisier v3, 5 m) masque `foule26`. Il faut déplacer ces figurants hors de l'ombre portée de ces sprites (ou décaler le tram) pour retrouver `masques() === []`.
5. **Taxi** : aucune modification de code. L'emprise `4,5 x 1,8 m` est conservée.

### D. Taxi à l'échelle piéton (vérifié en rendu moteur réel)

- `ct_taxi_v3_3q` (`205 x 109 px`, ancre `[136, 106]`) a une échelle uniforme de 0,24584, soit l'échelle de largeur d'emprise multipliée par 0,86. La caisse fait 63,6 px à `K = 50`, mesurée du bord de toit au pilier B jusqu'à la ligne de sol passant par le bas des pneus. Cela donne **1,45 m, soit 38,2 px à ppm 30** (cible Rivet : 38 px ; la v2 faisait 68–73 px).
- En rendu réel à ppm 30 : une boîte théorique de `4,5 x 1,8 x 1,45 m` projetée par `window.__nml.project` encadre le taxi (hauteur 38,1 px). Le joueur de 1,8 m mesure 47,3 px en projection et 45 px en silhouette dans la capture. Le rapport caisse / joueur vaut 0,81 (réel : 1,45 / 1,8 = 0,81).

### E. Planches de contrôle v3

- `/workspace/nml-shots/center_town_v3_fix.png` : **planche de sprites avant / après** (assets du manifest sur fond neutre, emprise théorique et parallélogramme de toit en surimpression, angles mesurés). **Ce n'est pas une capture du jeu.**
- `/workspace/nml-shots/center_town_v3_audit.png` : **vraie capture moteur hors dépôt** (`/tmp/nml-ct-v3`, clés v3 branchées dans la copie de `buildings_steel.js`). Elle contient la vue large, le carrefour avec passants, l'ouest, l'est, le taxi à ppm 30 avec la boîte théorique et le mobile `390 x 844`. Résultats : 0 erreur, 10/10 portes joignables, `pulsesOn` 13 en desktop et 8 en mobile, `masques()` listés au point C.4.

## 8. v4 : sprites à l'échelle du plan cible 132 x 116 m (`*_v4_3q`)

Plan validé par Valentin le 11/11/2026 (`center_town_plan_cible` v2 : 132 x 116 m, chaussées de 20 m). Consigne : « Les bâtiments trop petits sont à refaire. On n'étire pas les sprites et on ne les déforme pas non plus. Notamment l'Arcadius Tower. » Ce lot **ajoute** des clés : aucune clé existante n'est modifiée, chaque entrée porte `remplace`, et `obsolete` reste à poser par Rivet au moment du swap. Coordonnées des poses : repère absolu du plan v2.

### A. Méthode (`/workspace/ct_v4/`, hors dépôt)

Le générateur sort au plus 1280 px de côté. Un Arcadius de 60 m à 50 px/m mesure environ 2200 x 3400 px : il ne tient pas dans une seule génération sans agrandissement. D'où :
1. **Maître** : socle 32 x 32 x 16 m et tour 16 x 16 x 44 m générés chacun en entier au gabarit caméra du jeu (yaw 34,5°, pitch 28,8°), puis posés par **échelle uniforme + translation** (ajustement de silhouette sur le gabarit, IoU 0,89 et 0,95). Le maître ne sert que de référence.
2. **Tuiles** : 12 fenêtres de 1152 x 864 px, régénérées par le modèle à **52 px/m** d'après le maître. Chaque tuile est recalée sur le maître par translation + échelle uniforme seulement (0,994 à 0,998, corrélation 0,92 à 0,97), puis raccordée par couture (chaque pixel vient de la tuile la plus intérieure, transition sur une dizaine de pixels, pas de fondu large donc pas de fantômes).
3. **Réduction uniforme 50/52** vers le pipeline à 50 px/m : le rendu final n'est jamais agrandi. Coupe alpha sous les arêtes de pied (escalier conservé), découpe en colonnes d'emprise (tri par emprise du moteur), ancre sur le coin avant de chaque emprise, calques `_ecran` / `_fenetres` / `_neon` extraits sur le même canevas.

### B. Arcadius (3 sprites, remplacent `ct_arcadius_qg_v3_3q`)

| Clé | Emprise (x, z, w, d) | `px` | `anchor` | Contenu | Pose proposée |
|---|---|---|---|---|---|
| `ct_arcadius_arriere_v4_3q` | 12, 4, 24, 22 | `1676 x 3172` | `[1041, 3168]` | tour 16 x 16 x 60 m (x20-36, z10-26) + toit nord-ouest du socle | `B_CT('c_arcadius_n', '', 'ct_arcadius_arriere_v4_3q', 12, 4, 24, 22, { named: false })` |
| `ct_arcadius_aile_est_v4_3q` | 36, 4, 8, 22 | `889 x 1287` | `[332, 1283]` | façade est du socle | `B_CT('c_arcadius_e', '', 'ct_arcadius_aile_est_v4_3q', 36, 4, 8, 22, { named: false })` |
| `ct_arcadius_facade_v4_3q` | 12, 26, 32, 10 | `1662 x 1407` | `[1374, 1402]` | façade sud (portail x25-31, enseigne, gardiens, bannières) + escalier peint à plat x22-34, z36-42,6 | `B_CT('c_arcadius', 'Arcadius Center', 'ct_arcadius_facade_v4_3q', 12, 26, 32, 10)` |

Les trois emprises ne se chevauchent pas : le tri par emprise de `canvas-view.js` / `view.js` les ordonne correctement (arrière, puis aile est, puis façade). L'escalier est peint dans le sprite de façade, hors de son emprise : il est praticable, sans `solid`, et un personnage qui s'y tient est trié devant la façade. Pas de clôture IO dans ce lot (la grille z46 / x54 du plan reste à faire).

Planche de contrôle (image composée hors jeu, **pas une capture**) : `/workspace/nml-shots/ct_v4_arcadius_controle_echelle.jpg`.

### C. Remplissage (façades continues du plan v2)

Dix sprites neufs pour les emplacements `ct_rempl0` à `ct_rempl10` (silhouettes `RES` en attente). Les clés reprennent exactement les noms du plan (`ct_remplissage_*`), sans suffixe, pour que le branchement soit direct. Toutes à 50 px/m, ancre au coin avant (x+w, z+d), calques `_ecran`, `_fenetres`, `_neon` extraits sur le même canevas. Ce sont de nouveaux emplacements : aucune clé v3 n'est remplacée.

| Clé | Emprise x hauteur cible | Hauteur mesurée | px | Emplacements | Méthode |
|---|---|---|---|---|---|
| ct_remplissage_8x8_a | 8 x 8 x 12 m | 12,1 m | 614 x 806 | rempl1, rempl5 | génération unique, réduction x0,82 |
| ct_remplissage_8x8_b | 8 x 8 x 16 m | 16,2 m | 611 x 987 | rempl2 | génération unique, x0,91 |
| ct_remplissage_8x8_c | 8 x 8 x 20 m | 20,7 m | 637 x 1182 | rempl0 | génération unique, x1,00 (bornée à 1) |
| ct_remplissage_16x8_a | 16 x 8 x 14 m | 14,2 m | 942 x 1007 | rempl4 | maître + 2 tuiles à 52 px/m, x0,96 |
| ct_remplissage_16x8_b | 16 x 8 x 18 m | 19,1 m | 939 x 1225 | rempl3 | maître + 2 tuiles à 52 px/m, x0,96 |
| ct_remplissage_8x8_bas_a | 8 x 8 x 5 m | 4,9 m | 579 x 490 | rempl8 | génération unique, x0,62 |
| ct_remplissage_8x8_bas_b | 8 x 8 x 6 m | 6,4 m | 556 x 554 | rempl10 | génération unique, x0,66 |
| ct_remplissage_16x8_bas_a | 16 x 8 x 6 m | 6,0 m | 921 x 646 | rempl7 | génération unique, x0,83 |
| ct_remplissage_8x16_bas_a | 8 x 16 x 6 m | 6,1 m | 857 x 699 | rempl9 | génération unique, x0,89 |
| ct_remplissage_8x16_bas_b | 8 x 16 x 6 m | 6,1 m | 794 x 702 | rempl6 | génération unique, x0,87 |

La hauteur mesurée inclut les édicules de toiture (antennes, groupes de clim). Vitrines et enseignes uniquement sur les faces sud et est, les seules que montre la caméra. Les enseignes sont des pictogrammes sans lettres. Le 8x8_c garde plus d'étages que la norme (env. 9 pour 20 m) : lecture « logements serrés » assumée. Planche de contrôle hors jeu : `nml-shots/ct_v4_remplissage_controle_echelle.jpg` (non versionnée).

### D. Sol du carrefour (tuiles dérivées du plan v2)

Treize tuiles neuves à 128 px/m, dessinées en procédural sur les bases existantes `g_ct_asphalte_mouille` et `g_ct_trottoir_dalles` (marquage usé, bruit périodique, donc tuilables). Aucun agrandissement.

| Clé | px | Motif | Pose conseillée |
|---|---|---|---|
| g_ct_voie_tirets_ns | 512 x 1536 | 4 x 12 m | bandes x66-70 et x78-82 (tiret 3 m / 3 m, axe à 2 m) |
| g_ct_voie_tirets_ew | 1536 x 512 | 12 x 4 m | bandes z58-62 et z70-74 |
| g_ct_ligne_arret_ns / _ew | 512 x 512 | 4 m | tuile avant chaque passage piéton, ligne 0,5 m centrée |
| g_ct_bordure_n / _s / _e / _o | 512 x 512 | 4 m | dernière rangée de trottoir côté chaussée (granit 0,3 m + caniveau 0,4 m) |
| g_ct_bordure_angle_se / _so / _ne / _no | 512 x 512 | 4 m | les 4 angles du carrefour, R 2 m, raccord exact avec les bordures droites |
| g_ct_case_jaune_12m | 1536 x 1536 | 12 m | une seule pose en x68 z60, `remplace` g_ct_carrefour_jaune |

Les deux tuiles de tirets ne sont pas carrées : le manifest porte `motif_m` en plus de `tile_m`. Planche de contrôle hors jeu : `nml-shots/ct_v4_sol_controle_echelle.jpg` (non versionnée).

### E. Audit des bâtiments v3 et tours régénérées

Audit contre le plan v2 (132 x 116 m) : les cinq tours font 8 x 8 m pour 27,7 à 30,4 m, trop basses face au concept et à un Arcadius de 60 m. L'emprise 8 x 8 m reste imposée par les façades continues du plan (NE façade O sans écart, SO façade N, passage Teng), donc la masse vient de la hauteur. Elles sont refaites en `*_v4_3q` avec `remplace` vers la clé v3 (sans `obsolete`).

| Clé | Remplace | Hauteur v3 -> v4 | px | Ancre | Pose |
|---|---|---|---|---|---|
| ct_tour_teng_v4_3q | ct_tour_teng_v3_3q | 29,2 -> 39 m | 569 x 1986 | [342, 1981] | c_change, x0 z40 ; porte peinte face est, `painted_px` [441, 1873] (au lieu de [451, 1444]) |
| ct_tour_archeon_v4_3q | ct_tour_archeon_v3_3q | 29,3 -> 43 m | 569 x 2196 | [343, 2191] | ct_archeon, x16 z84 |
| ct_tour_orc_v4_3q | ct_tour_orc_v3_3q | 27,7 -> 45 m | 574 x 2281 | [350, 2277] | ct_orc, x92 z8 |
| ct_tour_nexus_v4_3q | ct_tour_nexus_v3_3q | 30,4 -> 46 m | 565 x 2286 | [337, 2281] | ct_nexus, x92 z24 |
| ct_tour_humancorp_v4_3q | ct_tour_humancorp_v3_3q | 29,5 -> 48 m | 562 x 2399 | [342, 2394] | ct_humancorp, x104 z40 |

Méthode : la génération reproduit d'elle-même les proportions v3 (environ 30 m). Le maître est donc calé en largeur sur l'emprise (échelle uniforme), puis élevé en répétant des étages entiers par translation verticale (pas d'étirement), redessiné en tuiles à 52 px/m et réduit à 50 px/m. Gardés tels quels, car à l'échelle : Dôme 12 x 12 x 9,4 m (inchangé au plan), Bureau des permis 8 x 8 x 7,2 m, bords sud a/b/c (rez commerçants 3,4 à 5,3 m), viaduc du monorail, mobilier et véhicules. Planche hors jeu : `nml-shots/ct_v4_tours_controle_echelle.jpg` (non versionnée).

### F. Taxi : vraie deuxième vue `vue_axe2` (axe N-S)

En miroir, l'enseigne de toit « TAXI » de `ct_taxi_v3_3q` se lit à l'envers sur l'axe N-S. Nouvelle clé `ct_taxi_v3_axe2_3q` (+ `_fenetres`, `_neon`), qui ne remplace rien : `ct_taxi_v3_3q` reste la vue de l'axe E-O.

| Clé | px | `anchor` | Emprise | Champs |
|---|---|---|---|---|
| `ct_taxi_v3_axe2_3q` | 205 x 109 (identique) | `[69, 106]` (= 205 - 136, ancre miroir) | 4,5 x 1,8 m, h 1,45 m | `axe: 'z'`, `vue_axe2_de: 'ct_taxi_v3_3q'`, calques `_fenetres` / `_neon` au même canevas |

Méthode : miroir horizontal pixel pour pixel de la caisse et des deux calques (échelle 1, aucun étirement), puis lettrage miroir effacé dans le caisson de toit et « TAXI » repeint à l'endroit, cisaillé sur la face du caisson à la pente du toit miroir (0,33), rendu x24 puis réduit en boîte vers 1x. Dans `_neon`, le caisson est comblé et les lettres sont creusées dans la lueur.

Branchement (Rivet, `src/data/vehicules.js`) : `ct_taxi_v3_3q: { axe: 'x', vue_axe2: 'ct_taxi_v3_axe2_3q' }`. `view.js` prend alors `ct_taxi_v3_axe2_3q`, `_fenetres` et `_neon` sur l'axe z, sans miroir. Le champ `vue_axe2` n'est pas posé dans l'entrée manifeste de `ct_taxi_v3_3q`, pour ne pas modifier une clé existante. Planche hors jeu : `nml-shots/ct_taxi_vue_axe2_controle.png` (non versionnée).

### G. Clôture et portail IO du parvis de l'Arcadius (`ct_arcadius_grille_*_v4_3q`, `ct_arcadius_portail_io_v4_3q`)

Il s'agit de la grille z46 / x54 du plan v2 (`facades_continues.NO` : clôture/grille IO continue x12-54 / z4-46, portail face sud), restée à faire au §8B. Ce sont sept sprites neufs, sans `remplace`, découpés en segments d'emprise pour le tri du moteur. Tous sont à 50 px/m, avec l'ancre au coin avant (x+w, z+d) et les calques `_neon` (filets rouges, balises, plaque IO) et `_fenetres` (appliques ambre) au même canevas.

| Clé | Emprise (x, z, w, d) | px | `anchor` | h |
|---|---|---|---|---|
| `ct_arcadius_grille_s1_v4_3q` | 12, 45,7, 12, 0,6 | 527 x 319 | [506, 315] | 3,12 m |
| `ct_arcadius_portail_io_v4_3q` | 24, 45,4, 8, 1,2 | 392 x 359 | [344, 353] | 5,1 m |
| `ct_arcadius_grille_s2_v4_3q` | 32, 45,7, 11, 0,6 | 480 x 277 | [459, 273] | 3,12 m |
| `ct_arcadius_grille_s3_v4_3q` | 43, 45,7, 10,55, 0,6 | 467 x 299 | [445, 295] | 3,12 m |
| `ct_arcadius_grille_e1_v4_3q` | 53,7, 4, 0,6, 14 | 437 x 430 | [29, 425] | 3,12 m |
| `ct_arcadius_grille_e2_v4_3q` | 53,7, 18, 0,6, 14 | 437 x 430 | [29, 425] | 3,12 m |
| `ct_arcadius_grille_e3_v4_3q` | 53,55, 32, 0,9, 14,45 | 461 x 440 | [46, 436] | 3,56 m (pilier d'angle) |

Clôture : socle de pierre noire de 0,5 m avec un filet néon rouge, barreaux de métal sombre de 2,4 m à pointes laiton, piliers de 0,7 m sur 3,1 m tous les 3,5 m environ, chacun avec son applique ambre au pied. Le pilier d'angle (x54, z46) porte une balise rouge IO. Portail : deux piliers de 1,2 m à filets rouges verticaux (repris du pilier de façade), linteau de 3,7 à 4,9 m, plaque lumineuse « IO » de 3,2 x 0,8 m et deux balises rouges à 5,1 m. La grille coulissante est rentrée, ce qui laisse un passage libre de 5,6 m (x25,2-30,8) dans l'axe du portail x25-31 et de l'escalier. Le champ `passage` du manifeste le décrit. Pose proposée avec des `solid` sur les seuls piliers (champ `pose`).

Méthode : rendu iso procédural au gabarit caméra du jeu (yaw 34,5°, pitch 28,8°), géométrie en mètres du plan, rendu x4 puis réduction en boîte vers 50 px/m. Il n'y a ni agrandissement ni déformation. Les matériaux reprennent ceux de `ct_arcadius_*_v4_3q`. Planche hors jeu avec silhouettes de 1,8 m : `nml-shots/ct_arcadius_grille_io_controle.jpg` (non versionnée).
