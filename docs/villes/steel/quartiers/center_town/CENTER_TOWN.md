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
