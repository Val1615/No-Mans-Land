# Éditeur de cartes intégré à No Man’s Land

Ouvrir `editor/` sur le site du jeu, ou utiliser le lien du panneau DEV (`?dev=1`). Le catalogue est construit depuis les modules et manifestes actuels du dépôt. Aucun asset n’est recopié et le rendu Three.js, les coordonnées, les textures, collisions et chemins sont partagés avec le jeu.

## Publier une modification

1. Choisir une zone (Dusk-Town ou Steel) et modifier sols, bâtiments, décors, personnages ou intérieurs. `Brouillon` conserve le travail dans ce navigateur.
2. Cliquer **Publier sur GitHub**. Dépôt `Val1615/No-Mans-Land`, branche `main` et fichier `src/data/editor-maps.json` sont préremplis ; le message « Éditeur : <zone> modifiée » est proposé et reste modifiable.
3. À la première utilisation, l’aide donne le lien direct [créer le jeton](https://github.com/settings/personal-access-tokens/new) : dépôt `Val1615/No-Mans-Land`, **Contents : Read and write** (et **Pull requests : Read and write** si « Proposer en PR plutôt » est cochée). Coller le jeton dans le champ masqué.
4. Par défaut : commit direct sur `main`. Statut : « Publication en cours… », puis « Publié » avec le lien du commit (GitHub Pages met environ 1 minute). Option « Proposer en PR plutôt » (décochée par défaut) : branche `editeur/<zone>-<date>`, PR vers `main`, « PR ouverte » avec le lien.
5. Avant tout envoi, le fichier est relu et validé (JSON lisible, schéma, zones / identifiants / assets existants, coordonnées dans les bornes). En cas d’erreur, rien n’est envoyé et la liste des erreurs s’affiche en français.
6. Conflit (quelqu’un a publié entre-temps) : rien n’est écrasé ; la version fraîche est relue et « Réessayer avec la version actuelle » renvoie nos zones par-dessus en gardant les autres zones publiées entre-temps.
7. Secours : **Télécharger le JSON** (fichier `editor-maps.json` à déposer dans `src/data/`) ; sous « Autres options », écriture directe dans un dépôt local (Chrome/Edge).

Erreurs traduites : jeton invalide ou expiré (401), droits insuffisants (403 / 404), conflit (409), limite GitHub, réseau. Le jeton est envoyé uniquement à `api.github.com` dans l’en-tête Authorization ; il est mémorisé dans le `localStorage` de ce navigateur seulement (clé `nml-editeur-jeton-github`, bouton « Oublier le jeton »), jamais dans le dépôt, le JSON ou l’URL. Le site public ne contient aucun secret : sans son propre jeton, un visiteur ne peut rien écrire. Limite : 900 ko.

Côté jeu, le chargement est tolérant : un `editor-maps.json` illisible ou invalide est ignoré, le jeu démarre sur ses données intégrées et affiche un avertissement.

## Données effectivement utilisées par le jeu

`src/data/editor-maps.json` vaut initialement `null` : aucun réagencement de démonstration n’est imposé aux joueurs. Après publication, il contient un document `nml-map-editor` version 5 **compact** : seules les zones réellement modifiées (et leurs portes) y figurent. Règle clé : le code de chaque zone reste la valeur par défaut ; une zone ouverte puis enregistrée sans changement n’est pas écrite et le jeu reste strictement identique. Au chargement, chaque zone du fichier est comparée à la source du jeu ; seules celles qui diffèrent sont remplacées. Les fichiers version 1 à 4 restent lisibles.

Au démarrage, `src/main.js` charge ce fichier **avant** `createGame`. `src/core/editor-maps.js` applique les tailles, sols et peintures, bâtiments, emprises, décors, points de départ, portes et personnages aux données réellement transmises au moteur. Les grilles de collision sont alors calculées sur les positions modifiées. Recharger une partie réajuste le joueur si son ancienne position est devenue bloquée.

Les conditions exécutables des portes et les dialogues natifs sont conservés. Les points de collecte correspondant exactement à un décor d’origine suivent son déplacement ; supprimer le décor supprime le point associé. Le point d’approche de la porte du laboratoire suit le bâtiment. Les scènes, combats et clés narratives restent natifs. Les identifiants de PNJ des exports du prototype sont rapprochés des identifiants natifs pour préserver les dialogues existants.

Le sol utilise `ground.paint` : rectangles de textures sur une grille de 0,5 m. Il ne devient pas un objet de collision. L’éditeur conserve les anciennes zones nommées pour les objectifs et permet encore de les éditer par l’option avancée.

Les dialogues et quêtes créés dans l’éditeur sont reliés au vrai moteur par `src/core/editor-story.js` : conversations, conditions, objectifs parler/interagir/visiter et journal. Leur progression est conservée dans `flags.editor_story` par les sauvegardes natives. Les récompenses de l’éditeur restent narratives et n’attribuent pas automatiquement d’argent ou d’objets.

## Zones couvertes (régions dérivées des données)

L’éditeur ouvre **toutes les zones chargées par le jeu** (`src/data/dusk_town.js` : 39 lieux) ; la liste n’est plus une liste blanche. La région d’un extérieur vient de ses données (`city: 'steel'`, préfixes `steel_`, `sv_`, `dusk_`), celle d’un intérieur de l’extérieur auquel ses portes mènent. Le sélecteur de zone regroupe les lieux par région.

- Steel (28) : steel_route, steel_center, sv_poutres, sv_cuve, steel_asia, steel_megaline, steel_terminus, steel_dome, steel_arena, steel_strip, steel_pulse, steel_china, steel_lower et leurs 15 intérieurs.
- Dusk-Town (11) : dusk_q1 à dusk_q4 et 7 intérieurs.
- Hors éditeur : la carte du monde (`carte_nml`, voyage) est une interface, pas une zone ; les combats (`combat`, arène) et scènes (`startScene`) sont du code ; les PNJ sans sprite (déclencheurs `porte`, `rodeur`, `raid`, `poste`) ne sont pas affichés et restent toujours à leur place.

Catalogue : `src/core/catalogue.js` charge tous les manifestes exactement comme le jeu (reused, interiors, buildings, `assets/steel/<quartier>/manifest.json`, sols `g_*`). Le jeu et l’éditeur partagent ce module.

## Format (version 5)

Couvert : taille, sol (couleur, texture, motif, teinte, propreté, eau, zones dont `wet`, peinture `ground.paint`), bâtiments (emprise, collision, calque, écrans, enseignes, défilements, groupes, réglages repris du jeu), décors (y compris lueur et miroir), PNJ, figurants (`extras`), passants (`walkers`), drones, lueurs (`glows`) et lumière (`light`), garde-corps, enseignes animées par le code (`enseignes`, voir docs/villes/steel/ENSEIGNES_CODE.md) et projecteurs (`projecteurs`), habillage de porte, portes (ouverture, seuil, destination), départs.
Non couvert, reste dans le code : conditions exécutables des portes et métadonnées scriptées (jonctions, interruptions), dialogues natifs, scènes, combats, quêtes natives, clés narratives de lieu (`city`, `arrive`, `labelsProches`, `accessLabels`).
Validation : JSON lisible, schéma attendu, zones / identifiants / assets existants, coordonnées dans les bornes ; en cas d’échec, la liste complète des erreurs est donnée en français. Un réglage du jeu que l’éditeur ne sait pas éditer est accepté tant qu’il est identique à la source.

## Portée et limites

- Projets v4 de l’ancien éditeur (Dusk-Town) : relus tels quels ; les PNJ des quartiers, absents de ces fichiers, sont repris de la source au lieu d’être retirés.
- Les nouveaux intérieurs possèdent des entrées/sorties réciproques et fonctionnent dans le jeu natif.
- Les nouveaux quartiers peuvent être essayés dans le jeu avec `?dev=1&map=IDENTIFIANT`. Leur raccordement aux routes du monde doit encore être défini ; l’éditeur n’invente pas de jonction. Le lien « Jeu publié » ouvre le lieu courant quand celui-ci a été publié.
- Les zones d’interaction ajoutées via une quête utilisent leurs identifiants éditables. Les textes narratifs natifs décrivant un ancien agencement ne sont pas réécrits automatiquement.
- Supprimer un PNJ natif peut rendre sa quête inaccessible : ses données narratives sont conservées mais son sprite est retiré du lieu.
- Les sauvegardes locales du prototype Work restent sur son ancienne adresse. Pour les transférer : Export JSON dans le prototype, puis Import JSON dans l’éditeur intégré.
- Le jeu public dépend de WebGL. Le rendu Canvas de l’éditeur reste un secours pour l’édition ; il ne remplace pas l’intégralité du moteur RPG.

## Vérifications ciblées

Depuis la racine, Node 24 :

```sh
node --experimental-vm-modules tests/editor-integration.mjs
node --experimental-vm-modules tests/editor-github.mjs
node --experimental-vm-modules tests/editor-render.mjs
node --experimental-vm-modules tests/editor-regions.mjs steel   # ou dusk, all
python3 tests/editor_publier.py                                # fenêtre de publication, API GitHub simulée
python3 tests/editor_regions.py steel                          # serveur local sur 8862
```

`editor-regions.mjs` : chaque zone de la région s’ouvre, enregistrer sans changement publie 0 zone et laisse le jeu identique, chaque zone réappliquée est identique au code, une modification ne publie que sa zone. `editor_regions.py` : chaque zone s’ouvre dans l’éditeur sans erreur JS, le jeu charge une carte éditée et visite chaque zone sans erreur JS, une carte invalide est ignorée (données intégrées + avertissement).

L’intégration exécute le vrai `createGame` avec les données actuelles : géométrie et collision modifiées, conservation des conditions et dialogues natifs, entrée/sortie d’un nouvel intérieur, collecte liée à un décor déplacé, quête personnalisée terminée et progression restaurée par les sauvegardes natives. Les tests de publication (`editor-github.mjs`, `editor_publier.py`) simulent l’API GitHub : commit sur main, PR, erreurs, conflit et nouvel essai, export cassé bloqué avant envoi ; aucun push réel ni jeton réel. Le test de scène Three.js utilise un renderer GPU simulé ; il ne vérifie pas visuellement WebGL.
