# Éditeur de cartes intégré à No Man’s Land

Ouvrir `editor/` sur le site du jeu, ou utiliser le lien du panneau DEV (`?dev=1`). Le catalogue est construit depuis les modules et manifestes actuels du dépôt. Aucun asset n’est recopié et le rendu Three.js, les coordonnées, les textures, collisions et chemins sont partagés avec le jeu.

## Enregistrer une vraie modification

1. Modifier Dusk-Town, ses sols, bâtiments, décors, personnages ou intérieurs. `Brouillon` conserve seulement le travail dans ce navigateur.
2. Cliquer **Enregistrer dans le jeu**.
3. Choisir une branche existante, puis **Lire la version GitHub**. Il est possible de charger ce projet ou de conserver son projet actuel, notamment après import d’un export du prototype V1–V4.
4. Pour écrire, fournir dans la fenêtre un jeton GitHub à expiration courte, limité au dépôt `Val1615/No-Mans-Land`, avec **Contents: Read and write**. Le jeton n’est jamais enregistré. Ne pas l’envoyer dans une conversation.
5. **Publier mon projet sur cette branche** crée un vrai commit modifiant `src/data/editor-maps.json`. Un lien permet d’inspecter ce commit. Toute modification concurrente du fichier bloque l’écriture et demande de relire GitHub ; aucun écrasement forcé.
6. Sur `main`, attendre le déploiement GitHub Pages puis recharger le jeu. Une branche de travail doit être fusionnée avant d’être visible sur le jeu public.

Le mode GitHub accepte un projet de moins de 900 ko. Le jeton est envoyé exclusivement à `api.github.com`, dans l’en-tête Authorization, jamais dans le JSON, l’URL ou le stockage navigateur. Fermer la fenêtre efface le champ. Ce site public ne contient aucun secret ni droit d’écriture : les visiteurs ne peuvent pas modifier le dépôt sans leur propre autorisation GitHub.

Sur un ordinateur disposant de l’accès aux dossiers (notamment Chrome/Edge), **Choisir le dépôt local et enregistrer** écrit réellement le même fichier dans le dossier sélectionné. Le jeu lancé depuis ce dossier charge immédiatement ces données après actualisation. Le commit/push local reste séparé. Sur les autres navigateurs, utiliser GitHub ou l’export JSON.

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

Couvert : taille, sol (couleur, texture, motif, teinte, propreté, eau, zones dont `wet`, peinture `ground.paint`), bâtiments (emprise, collision, calque, écrans, enseignes, défilements, groupes, réglages repris du jeu), décors (y compris lueur et miroir), PNJ, figurants (`extras`), passants (`walkers`), drones, lueurs (`glows`) et lumière (`light`), garde-corps, habillage de porte, portes (ouverture, seuil, destination), départs.
Non couvert, reste dans le code : conditions exécutables des portes et métadonnées scriptées (jonctions, interruptions), dialogues natifs, scènes, combats, quêtes natives, clés narratives de lieu (`city`, `arrive`, `labelsProches`, `accessLabels`).
Validation : JSON lisible, schéma attendu, zones / identifiants / assets existants, coordonnées dans les bornes ; en cas d’échec, la liste complète des erreurs est donnée en français. Un réglage du jeu que l’éditeur ne sait pas éditer est accepté tant qu’il est identique à la source.

## Portée et limites

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
python3 tests/editor_regions.py steel                          # serveur local sur 8862
```

`editor-regions.mjs` : chaque zone de la région s’ouvre, enregistrer sans changement publie 0 zone et laisse le jeu identique, chaque zone réappliquée est identique au code, une modification ne publie que sa zone. `editor_regions.py` : chaque zone s’ouvre dans l’éditeur sans erreur JS, le jeu charge une carte éditée et visite chaque zone sans erreur JS, une carte invalide est ignorée (données intégrées + avertissement).

L’intégration exécute le vrai `createGame` avec les données actuelles : géométrie et collision modifiées, conservation des conditions et dialogues natifs, entrée/sortie d’un nouvel intérieur, collecte liée à un décor déplacé, quête personnalisée terminée et progression restaurée par les sauvegardes natives. Les tests HTTP de publication simulent succès, refus et conflit, sans utiliser de jeton. Le test de scène Three.js utilise un renderer GPU simulé ; il ne vérifie pas visuellement WebGL.
