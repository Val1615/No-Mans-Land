# No Man’s Land - dossier de reconstruction

Univers de Valentin. Export du 21 octobre 2026. Maquette archivée : v0.13.

**Repartir de zéro dans un nouveau projet. Le jeu fourni est un premier jet à étudier, pas une base technique à prolonger.**

Le nouveau Work doit comprendre les intentions, examiner les défauts puis concevoir une architecture et une production neuves. Les assets sont des références à réévaluer ; leur présence ne signifie pas que leur échelle, leur perspective ou leurs portes sont validées.

## Commencer

Ouvrir INDEX.html pour naviguer dans les documents et images. Lire ensuite :

1. 01_CONSIGNE_NOUVEAU_WORK.md : instruction prête à transmettre.
2. 02_CONCEPTION_ET_BILAN : conception consolidée, état réel, rapport critique, reconstruction et catalogues. Le PDF Dossier-de-reconstruction.pdf regroupe ces documents.
3. 03_DOCUMENTS_PRECEDENTS : les trois PDF historiques, leurs sources, les plans SVG et registres, les dix maquettes UI.
4. 04_ROMAN_ET_ECRITURE : tome 1 original et bible de Sylvinia, référence d’écriture uniquement.
5. 05_REFERENCES_VISUELLES : planches, cartes, captures des retours et autres originaux générés.
6. 06_AUDIT_ET_CATALOGUES : relevés du contenu, données et preuves de contrôle.
7. 07_MAQUETTE_ARCHIVE_v0.13 : sources, jeu exécutable, assets, tests et outils historiques.

## Statut des documents

Les trois anciens PDF totalisent 266 pages : Atlas 104, Gameplay et PNJ 90, Interface et atelier 72. Ils décrivent la v0.6 et des propositions ; ils ne sont pas une description intégralement réalisée de la v0.13.

L’atlas contient 44 plans détaillés et 7 vues d’ensemble. Les tableaux donnent bâtiments, fonctions, accès prévus, routes, PNJ et décors. Les dix PNG M01 à M10 sont des maquettes d’interface. Les plans et images ne valent pas validation de l’implémentation.

Le README du prototype contient aussi des paragraphes de versions anciennes et des nombres périmés. Pour l’état actuel, utiliser le relevé consolidé et les catalogues extraits.

## Ouvrir la maquette

Depuis le dossier décompressé, avec Python 3 installé :

    python3 -m http.server 8000 --bind 127.0.0.1 --directory 07_MAQUETTE_ARCHIVE_v0.13/dist

Puis ouvrir http://127.0.0.1:8000. Arrêter le serveur avec Ctrl+C. Ne pas lancer directement index.html avec file:// : les modules JavaScript nécessitent un serveur HTTP.

Le jeu navigateur est autonome et ne nécessite pas de serveur de monde. Les sauvegardes appartiennent au navigateur et à son adresse. Aucune sauvegarde personnelle n’a été récupérée : les fichiers du jeu sont fournis, mais une partie doit être exportée depuis le jeu pour être transférée.

Les tests historiques nécessitent Node et, pour certains rendus, @napi-rs/canvas via CODEX_PRIMARY_RUNTIME_NODE_MODULES. Ces dépendances de vérification ne sont pas nécessaires pour jouer. Certains outils historiques ont un chemin de sortie propre à l’ancienne session ; ne pas les considérer comme des outils portables du nouveau projet.

## Provenance et intégrité

Source archivée : commit 1fe00eb76e5b85c57e68a8a7530237cb8c352ab6. Site de référence : https://no-mans-land-2175.val1615.chatgpt.site. Aucun changement ni redéploiement du site pendant l’export.

Tous les fichiers de jeu suivis dans le dépôt sont conservés sans modification. Seuls les liens de configuration à l’ancien hébergement et les métadonnées Git sont exclus pour éviter de réutiliser son identité. Les caches, fichiers temporaires, anciens paquets de déploiement et rendus de pages PDF redondants ne sont pas inclus.

Le tome 1 est le DOCX intégral « Un réveil tardif », conservé sans correction. Sa copie fournie correspond à celle retrouvée. Aucun morceau audio Suno ni fichier de prompts Suno historique n’a été retrouvé dans les fichiers disponibles ; l’audio du prototype est synthétisé.

Les images générées identiques sont dédoublonnées par empreinte, avec une table indiquant où retrouver chacun des originaux. INVENTAIRE.csv décrit les fichiers ; SHA256SUMS.txt permet leur contrôle. CONTROLE-LIVRAISON.json résume les vérifications.

Les captures des retours utilisateur montrent différentes étapes du projet. Les rendus Canvas sont historiques et hors navigateur ; ils ne prouvent pas l’ergonomie réelle du téléphone.
