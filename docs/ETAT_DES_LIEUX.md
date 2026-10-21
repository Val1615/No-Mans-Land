# No Man's Land : état des lieux et leçons de la maquette v0.13

Rédigé le 21 octobre 2026 (heure de Paris). Sources extraites dans `/workspace/nml/src/a/` et `/workspace/nml/src/b/`, sans aucune modification.

**Cadre.** Tout ce qui est archivé est une **maquette** accompagnée de rapports. On ne prolonge pas ce projet : on repart de zéro. Ce document sert à retenir les intentions et le canon, et à **ne pas reproduire** les erreurs.

**Conventions de lecture**
- **[OBS]** : constaté directement dans un fichier (le chemin est donné).
- **[SUP]** : supposition ou interprétation de ma part.
- Statuts : **CANON** (canon établi), **DÉCISION** (décision validée par Valentin), **PROPOSITION** (proposition en attente), **PROTO** (contenu prototype à réévaluer).
- Abréviations de chemins : `B/` = `src/b/No-Mans-Land_Reconstruction/`, `A/` = `src/a/No-Mans-Land_Reconstruction/07_MAQUETTE_ARCHIVE_v0.13/`.

**Ce que je n'ai pas fait.** Je n'ai pas lancé la maquette, pas exécuté les tests, et je n'ai pas lu les PDF historiques en entier. J'ai regardé 2 images sur environ 200. Les chiffres de tests cités viennent des rapports de l'archive, pas de moi.

---

## 1. Inventaire

[OBS] Les deux ZIP se réunissent dans un même dossier racine, `No-Mans-Land_Reconstruction` (voir `EXTRACTION-DEUX-PARTIES.txt`). Attention, l'étiquetage est inversé : ce fichier dit « Partie 1 : documentation » et « Partie 2 : jeu », alors que `a.zip` contient le jeu et `b.zip` la documentation. Ce n'est qu'un détail de nommage.

| Archive | Fichiers | Taille | Contenu |
|---|---:|---:|---|
| a.zip | 460 | 139 Mo | `07_MAQUETTE_ARCHIVE_v0.13` : 220 webp, 134 js, 39 png, 22 json, 12 svg, 10 md, 7 mjs, 6 css, 5 py |
| b.zip | 230 | 188 Mo | Dossiers 00 à 06 : 91 png, 51 svg, 19 jpg, 14 py, 12 txt, 11 csv, 9 md, 8 html, 7 json, 4 pdf, 2 docx |

**Arborescence et fichiers clés** [OBS]
- `B/00_LIRE_EN_PREMIER.md` : guide de l'archive, statut des documents, provenance (commit `1fe00eb7...`), procédure pour lancer la maquette.
- `B/01_CONSIGNE_NOUVEAU_WORK.md` : **consigne de Valentin pour la reconstruction**. C'est le document d'exigences le plus direct.
- `B/02_CONCEPTION_ET_BILAN/` :
  - `01_Conception-complete.md` : conception consolidée (canon, factions, lieux, systèmes).
  - `02_Etat-reel-et-ecarts.md` : relevé chiffré de la v0.13.
  - `03_Rapport-echecs-et-causes.md` : **bilan critique**.
  - `04_Reconstruction-et-recette.md` : méthode et critères proposés.
  - `05_Catalogues.md`.
  - `Dossier-de-reconstruction.pdf` regroupe ces documents.
- `B/03_DOCUMENTS_PRECEDENTS/` : 3 PDF historiques (Atlas 104 p. de 21 Mo, Gameplay-PNJ 90 p., Interface et atelier 72 p. de 40 Mo), avec :
  - leurs sources (`world.json`, `audit.json`, `batiments.csv`, `personnages.csv`, `decors.csv`, `voirie.csv`) ;
  - 51 SVG de plans (44 plans et 7 vues d'ensemble) ;
  - 3 concepts de villes ;
  - 10 maquettes d'interface `M01.png` à `M10.png`.
- `B/04_ROMAN_ET_ECRITURE/` :
  - `No-Mans-Land_Tome-1_Un-reveil-tardif_Final.docx` (11 Mo, environ 75 700 mots, chapitres I à XIII) ;
  - `Bible-Sylvinia_V1.1.docx`, à utiliser **uniquement comme principes d'écriture**, sans reprendre l'univers de Sylvinia.
- `B/05_REFERENCES_VISUELLES/` :
  - `Planches-et-cartes` (9) : carte régionale en croquis, 2 croquis du périmètre de Steel, planche des factions, 5 planches de populations ;
  - `Captures-retours-utilisateur` (14 jpg) ;
  - `Generations-originales` (5).
- `B/06_AUDIT_ET_CATALOGUES/` :
  - `Catalogue-complet-v0.13.json` (1,2 Mo) ;
  - CSV des lieux, PNJ, quêtes et objets ;
  - `Tests-reexecutes-2026-10-21.txt` ;
  - 70 rendus Canvas historiques.
- `B/INVENTAIRE.csv`, `SHA256SUMS.txt`, `CONTROLE-LIVRAISON.json` : contrôle d'intégrité.
- `A/` :
  - `README.md` (historique empilé de la v0.2 à la v0.13), `ART.md`, `WRITING.md` ;
  - `dist/` : le jeu, avec 39 modules JS à la racine, `runtime-v12/` et `runtime-v13/` (40 fichiers chacun) et `assets/` (235 fichiers) ;
  - `art-source/` (58 fichiers, 98 Mo, atlas raster et prompts) ;
  - `docs/` (notes de correctifs v09 à v13) ;
  - `tests/` (17 fichiers) ;
  - `tools/` (9 scripts).

## 2. Sources attendues : présentes ou absentes

| Source attendue | Statut | Où |
|---|---|---|
| Tome 1 | Présent | `B/04_ROMAN_ET_ECRITURE/...Tome-1...docx` |
| Documents de lore | Partiel | Pas de bible NML dédiée. Le lore est dispersé entre le roman, les planches et `01_Conception-complete.md` §2-4 |
| Planches de référence art | Présentes | `B/05_REFERENCES_VISUELLES/Planches-et-cartes`, `B/03_.../Atlas/concepts` |
| Décisions art validées | **Absentes en tant que document** | Aucun fichier « décisions art validées ». `A/ART.md` décrit la maquette, et `LIRE_LES_IMAGES.md` précise qu'aucune image n'est approuvée d'office |
| Dossier, plans et spécifications de design | Présents | `B/02_...`, `B/03_DOCUMENTS_PRECEDENTS` (décrivent la v0.6 et des propositions) |
| Bilan critique de la v0.13 | Présent | `B/02_.../03_Rapport-echecs-et-causes.md` (et `02_Etat-reel-et-ecarts.md`) |
| Code du prototype v0.13 | Présent | `A/dist`, `A/tests`, `A/tools` |
| Captures | Présentes | 14 captures de retours, 70 rendus Canvas |

Signalés absents par l'archive elle-même (`00_LIRE_EN_PREMIER.md`) : musique et prompts Suno, sauvegardes personnelles, modèles 3D ou Blender.

**Retours de Valentin.** Ses retours ne sont pas sous forme de verbatim. Ils apparaissent :
- reformulés dans `01_CONSIGNE` et `03_Rapport` ;
- à travers les captures, qui sont des images sans annotation. Le classement thématique des captures se trouve dans `LIRE_LES_IMAGES.md`.

## 3. Faits de canon (CANON, sauf mention contraire)

- [OBS roman] **Steel-Megalopolis**, une ville sous **sarcophage**, avec le siège d'IO, une tour-pilier qui rejoint le sommet du sarcophage. Le nom compte 108 occurrences de « Steel » dans le roman et **0 de « SteelCity »**.
- [OBS roman] **UFSA** signifie « United Federation of South America ». La planche `Factions.png` porte une autre expansion (voir §7).
- [OBS roman] **Big Larry Area** : point d'impact nucléaire, un « cratère géant » entouré de désert, près des vestiges de l'ancienne capitale.
- [OBS roman] Termes présents : IO (88), Titans (21), Human Corporation (18), Rakkens (18), Aura (4), Dusk (30). L'intrigue du roman se déroule le 5 octobre 2202.
- [OBS `01_Conception` §2] Le jeu se situe en **2175**. Grand Exode en 2075, début de la Dernière Grande Guerre en 2081. Le sarcophage couvre plus de 100 km² (c'est une surface, pas un rayon).
  - [SUP] Je n'ai pas trouvé ces dates écrites en chiffres dans le texte du roman (aucune occurrence de « 2075 », « 2081 » ou « 2175 »). Elles viennent peut-être d'une écriture en lettres ou d'une autre source : à vérifier.
- [OBS `01_Conception` §2-3] Autres éléments posés par la conception :
  - Les Titans sont des machines de dissuasion exceptionnelles.
  - Le laboratoire Human Corporation sous Dusk-Town reste scellé en 2175.
  - L'Aura est ancienne, mystique et stigmatisée. Les implants l'entravent et **un cyborg ne peut pas la pratiquer** (DÉCISION de Valentin).
  - On n'invente pas d'explication sur les Érudits.
- [OBS `01_Conception` §3, `Factions.png`] **7 factions** : IO, UFSA, Sine Vincula, Protectores del Nuevo Mundo, Los Nativos, Los Invictos, Les Rakkens.
- [OBS] **5 populations** : Humains, Augmentés (ISIO), Cyborgs, Androïdes, Mutants. Une planche par population.
- [OBS `01_Conception` §3] Forces : SMPD, Interception Troupers, Dusk Forces, Presidential Soldiers (androïdes).
- [OBS `01_Conception` §4] Quartiers de Steel-Megalopolis : Lower-Town, China Lake, Asia-Ground, Center-Town, Upper-Town, Sous-Ville. Le périmètre est désertique et comporte des douanes. Statut [SUP] : mélange de CANON et de conception, la source exacte de chaque quartier n'est pas précisée.

## 4. Décisions de design trouvées

**DÉCISION (Valentin, `B/01_CONSIGNE_NOUVEAU_WORK.md`)**
- Projet neuf : la v0.13 ne sert pas de base de code. Le moteur Canvas n'est pas repris d'office.
- RPG ouvert et dense, inspiré de Fallout 1 et 2, avec une interface moderne. On ne survend pas une petite démo.
- Un référentiel commun (personnages, portes, bâtiments, parcelles, rues, collisions, caméra) **avant** le terrain.
- Quartiers faits main. **Aucun remplissage procédural.**
- Contrastes de lieux :
  - Steel-Megalopolis cyberpunk sous le sarcophage, périmètre désertique ;
  - Dusk-Town à échelle humaine et habitée ;
  - Buenos Aires en plusieurs quartiers ;
  - Big Larry sans population.
- Portes et intérieurs :
  - Les services ont de vrais intérieurs, avec du personnel.
  - La porte est **une seule définition** (visuel, clic, seuil, chemin, sortie).
  - Pas de marqueur sur les bâtiments non visitables. Transparence des volumes qui masquent le personnage.
- Assets orientés, texturés et fonctionnels. Pas de barres ni de cubes provisoires publiés.
- Dialogues naturels, humour noir dosé. Pas d'exposition systématique, pas de métaphores en série, pas de « Ce n'est pas X, c'est Y ».
- Monde et outils :
  - PNJ avec routines, événements, caravanes et conflits.
  - Un compagnon fiable.
  - Un atelier développeur dès le départ.
- Première tranche : un quartier de Dusk-Town, plusieurs services avec intérieurs, une route, une rencontre, un compagnon, une quête à 2 solutions. Ensuite seulement : douane et secteur intérieur de Steel.
- À chaque livraison : ce qui est réalisé et vérifié, ce qui reste à vérifier, ce qui est prévu. Captures du vrai jeu, recette tactile réelle.
- Nouvel hébergement. On ne réutilise pas l'identité de déploiement.

**PROPOSITION (rédigée dans les rapports, non validée explicitement)**
- Phases A à H et critères GEO, ART et LORE (`04_Reconstruction-et-recette.md`).
- Comparer une scène 3D orthographique et une chaîne 2,5D.
- Catalogue d'assets avec des états (concept, temporaire, intégré, vérifié).
- 32 événements, 6 circuits de caravanes, compagnons Esteban, Lucero et Noa, 44 plans d'atlas (`03_DOCUMENTS_PRECEDENTS`).

**PROTO (à réévaluer)**
- Campagne « Les Héritiers du silence » ; quête principale « La dette des vivants » (eau, 4 fins).
- PNJ Mara, Vera, Nilo, Roque, Alma, Eva, Ada Voss.
- Règles chiffrées : 40 points d'attributs, PV = 35 + 3 × Endurance, PA = 5 + Agilité/2.
- 7 attributs, 10 compétences, 4 origines.
- `01_Conception` §1 précise que ces éléments sont dérivés et révisables.

## 5. Analyse de la maquette v0.13

**Technique** [OBS `02_Etat-reel`, `A/package.json`]
- Application statique HTML/CSS, modules ES JavaScript et Canvas 2D, sans dépendance de jeu.
- `index.html` charge `runtime-v13/` (39 modules). `runtime-v12/` est une copie quasi identique (6 différences).
- Les plus gros modules font de 35 à 78 Ko. `building-scale-v11.js` compte 3 531 lignes de données d'échelle.
- Tests : `node --test` (17 fichiers).

**Comment la lancer** [OBS `00_LIRE_EN_PREMIER.md`]
```
python3 -m http.server 8000 --bind 127.0.0.1 --directory A/dist
```
Pas de `file://`. **Je ne l'ai pas lancée.**

**Fonctions présentes dans le code, d'après le relevé `02_Etat-reel`** (je n'ai pas vérifié leur fonctionnement moi-même)
- Monde : 56 lieux (35 extérieurs, 21 intérieurs), 527 bâtiments placés, 167 cases régionales (7 compositions de halte réutilisées).
- Population et contenu : 113 PNJ, 12 routines, 21 quêtes, 34 objets d'inventaire, 216 objets du monde, 18 scénarios développeur.
- Systèmes :
  - combat (PA, couvert, visée, fumée, réaction) ;
  - survie (santé, fatigue, radiations, eau) ;
  - compagnon Nilo (5 ordres) ;
  - sauvegarde locale avec migrations ;
  - audio synthétisé.

**Preuves que ça fonctionne**
- [OBS `Tests-reexecutes-2026-10-21.txt`] 164 tests passés sur 164.
- Le rapport précise lui-même leurs limites :
  - adaptateur DOM sans moteur de mise en page ;
  - serrures ouvertes et ennemis retirés pour tester les accès ;
  - aucune recette Android ou iOS.
- **Conclusion : la logique tourne, mais l'usage réel n'est pas prouvé.**

**Points principaux du bilan critique** (`03_Rapport-echecs-et-causes.md`)

| Priorité | Défaut |
|---|---|
| P0 | Échelle corrigée par pourcentages empilés (+25 %, puis +25, 35 ou 50 % selon la famille), l'image étant séparée de l'emprise physique |
| P0 | Entrées fragiles. Bug Nilo reproduit en v0.12 : le compagnon replacé loin bloquait l'entrée suivante. Clic sur la façade ajouté tardivement |
| P0 | Plans d'atlas séparés du terrain, modifiés par transformations successives |
| P0 | Absence de recette tactile réelle |
| P1 | Quartiers vides ou répétitifs : grille passée de 25×25 à 50×50 sans plus d'usages |
| P1 | Assets sans contrat (échelle, angle, pivot, porte), substituts publiés |
| P1 | Lore appliqué tardivement (Big Larry habité, corrigé ensuite) |
| P1 | Simulation peu profonde, dialogues inégaux |
| P2 | Documentation en avance sur le jeu, README périmé, copies runtime, outils à chemins absolus |

[OBS capture `05-1000036700.jpg`] Upper-Town, « Jardins suspendus » : le même modèle de bâtiment à colonnes est répété environ 9 fois sur un dallage vide. Le bandeau « MODE TEST · COPIE ISOLÉE » est visible. C'est une illustration directe des défauts de répétition et de vide.

**Intentions et contenus qui méritent d'être retenus** [OBS `03_Rapport` §12]
- Crise de l'eau, contraste entre IO et les terres, origines, Aura.
- Services avec intérieurs, preuves consultables, solutions non violentes.
- Ressources finies du compagnon, copie de test isolée dans l'atelier.
- Cas de régression à réécrire :
  - retour de Nilo ;
  - façades retournées ;
  - coûts appliqués une seule fois ;
  - sauvegardes ;
  - retours de dialogue après une conclusion.

## 6. Inventaire des assets

- [OBS] `A/dist/assets` : 220 webp, dont les acteurs (`actor-*`, `actors-v2-*`). Les dimensions sont très hétérogènes : 12 en 384², 6 en 480², 5 en 1087×1536, 2 en 1774×887, 2 en 1254², puis une longue traîne de tailles uniques (165×239, 474×426, etc.).
- [OBS] `A/art-source` : 58 fichiers (98 Mo). Ce sont des atlas raster avec des manifestes et prompts versionnés v9, v10 et v12 (props, settlement, service, linear, interiors, freighter).
- [OBS] Références : 9 planches et cartes, 3 concepts de villes, 10 maquettes UI, 51 SVG de plans, 5 générations originales. `Correspondance-images-generees.json` recense 57 images générées et 52 doublons évités.
- [OBS `03_Rapport` §6] Pas d'échelle, d'angle, de pivot ni de porte uniformes. Les miroirs horizontaux inversent l'éclairage et la position des portes. Il n'existe aucun modèle 3D.
- [SUP] Les tailles disparates et les trois générations de prompts confirment l'absence de gabarit commun. **Aucun asset n'est réutilisable sans un nouveau contrôle** dans le nouveau référentiel (c'est aussi l'avis de `LIRE_LES_IMAGES.md`). Les planches de factions et de populations sont de bonne qualité comme direction artistique, pas comme sprites.

## 7. Contradictions et questions ouvertes

**Contradictions repérées** (signalées, non tranchées)
1. **UFSA**
   - `Tome-1` : « United Federation of South America ».
   - `Factions.png` : « United Federal Survivors Alliance ».
2. **Cyborg et Aura**
   - Planche (selon `01_Conception` §2) : compatibilité réduite.
   - Consigne de Valentin : incapacité totale.
3. **Dates**
   - `01_Conception` attribue 2075 et 2081 au « texte fourni ».
   - Je ne les trouve pas en chiffres dans le roman, et les formules approximatives (« cent ans plus tard ») coexistent avec ces dates.
4. **Big Larry**
   - Habité dans les versions antérieures de la maquette, contre le roman et la consigne.
   - Corrigé en v0.13 (`03_Rapport` §7).
5. **README contre état réel**
   - `A/README.md` empile des sections v0.2 à v0.13 avec des chiffres périmés.
   - `02_Etat-reel` fait foi selon `00_LIRE`.
6. **Nommage des parties d'extraction**
   - `EXTRACTION-DEUX-PARTIES.txt` contre le contenu réel de a.zip et b.zip (mineur).
7. **SteelCity (legacy)**
   - Seules occurrences : `01_Conception-complete.md` et `.html`, dans la consigne même de remplacer ce nom.
   - Aucune ailleurs, ni dans le code ni dans le roman.

**Questions pour Valentin**
1. Quelle expansion d'UFSA est canon ?
2. D'où viennent les dates 2075 et 2081, et lesquelles sont fixées ?
3. Y a-t-il des décisions art **validées** (palette, perspective, références retenues parmi les 10 maquettes UI et les planches) ? Aucun document ne les liste.
4. Quels éléments PROTO veux-tu garder comme canon de jeu : la quête de l'eau, Nilo, Mara et les autres PNJ, les 4 origines, les règles chiffrées ?
5. Quelles plateformes cibler (mobile, bureau, les deux), et quel choix entre 3D orthographique et 2,5D pré-rendue ?
6. Les quartiers de Steel (Lower-Town, China Lake, etc.) et la carte régionale en croquis sont-ils canon ou proposition ?
7. Les 44 plans de l'atlas : base de travail ou à refaire ?
8. Peux-tu donner des retours verbatim, notamment sur les derniers bâtiments inaccessibles, dont aucun n'est reproduit individuellement ?

## 8. Erreurs à ne pas reproduire

| Erreur | Cause racine | Règle préventive |
|---|---|---|
| Échelle qui oscille (trop gros, puis trop petit) | Pas d'unité monde ; la taille d'image sert de géométrie ; facteurs en % empilés | Unité monde fixée (personnage, porte, étage, rue) dans une scène d'étalonnage validée **avant** toute production. Aucun facteur correctif ad hoc |
| Portes inaccessibles ou décalées | Porte ajoutée après l'image, et plusieurs définitions (point, badge, façade, seuil) | Un seul objet Porte (bâtiment, ouverture, zone de clic, seuil, condition, cible, retour, positions du groupe). Refus toujours explicite et typé |
| Compagnon bloquant les transitions | Transition joueur puis compagnon non atomique | La transition de groupe est une transaction unique, avec tests de régression (allié proche, loin, en attente, blessé) |
| Villes vides et répétitives | Taille augmentée au lieu d'usages, gabarits réutilisés | Programme de quartier écrit d'abord (qui vit, travaille, stocke, circule). Identité reconnaissable sans étiquette. Critère d'arrêt : densité d'usages, pas surface |
| Assets provisoires publiés comme finis | Pas de catalogue ni d'état de production | Catalogue d'assets (source, dimensions, pivot, orientations, portes, collision, état). Le build refuse un asset requis absent ou temporaire |
| Lore appliqué après coup | Pas de revue préalable | Fiche d'invariants par lieu relue avant production. Contrôle LORE dans la recette |
| Tests verts, usage cassé | Tests de coordonnées et rendus hors navigateur | Recette en vrai navigateur et sur vrai téléphone dès la première tranche. Tests par tâche (entrer, acheter, ressortir avec l'allié) |
| Recette faite par les retours de Valentin après publication | Pas de validation interne | Revue par captures réelles comparées aux maquettes retenues, avant toute livraison |
| Documentation plus avancée que le jeu, README mêlant les versions | Spécification et état non séparés | Exigences identifiées avec statut et preuve. Un document d'état distinct de la spécification |
| Couches de correctifs, ordre de chargement, copies runtime | Installations successives qui modifient des registres globaux | Données immuables validées au chargement. Séparation état, règles, rendu, interface et outils. Build unique versionné, chemins portables |
| Survente de l'ambition | Annonces fondées sur les noms et les plans | Chaque livraison distingue réalisé et vérifié, existant non vérifié, prévu |
| Dialogues fonctionnels ou maniérés | Écriture hors scène | Relecture en contexte. Liste de tics proscrits (« Ce n'est pas X, c'est Y », métaphores en série, exposition) |

## 9. Trois premières étapes recommandées

1. **Arbitrer le canon et la cible.** Une bible NML courte avec les statuts CANON, DÉCISION et PROPOSITION. Elle tranche les questions du §7 avec Valentin (UFSA, dates, plateformes, éléments PROTO conservés, références art validées).
2. **Fixer le référentiel et le moteur sur une scène d'étalonnage** : humain, portes piétonne et de fret, maison, boutique, immeuble, ruelle, voie camion, couverture. On y vérifie l'objet Porte unique, la transition de groupe, le masquage et le tactile réel. Le choix moteur et la chaîne d'assets (3D orthographique ou 2,5D) se font sur cette preuve.
3. **Écrire le programme du quartier de Dusk-Town et le catalogue d'assets** avant la production : usages, flux, PNJ, services avec intérieurs, et contrat d'asset avec états. Ensuite seulement, construire la tranche jouable décrite dans `01_CONSIGNE`.
