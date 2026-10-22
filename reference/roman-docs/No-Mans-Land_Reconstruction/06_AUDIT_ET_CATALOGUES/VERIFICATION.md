# Vérification et limites

Source : commit 1fe00eb76e5b85c57e68a8a7530237cb8c352ab6. Export du 21 octobre 2026.

La commande npm test a été réexécutée sur le dépôt récupéré : 164 tests réussis, aucun échec. Le journal Tests-reexecutes-2026-10-21.txt est fourni. Les journaux de Verification-historique sont plus anciens et ne constituent pas de nouveaux essais.

Les tests UI utilisent un DOM minimal et le Canvas natif. Ils ne valident pas le CSS d’un vrai navigateur, les gestes tactiles ou la qualité artistique. Certains contrôles d’accès retirent les ennemis et ouvrent les serrures pour isoler la navigation. Les captures Canvas sont historiques, hors navigateur.

Le catalogue extrait après initialisation recense 56 lieux, 21 intérieurs, 35 extérieurs, 527 placements de bâtiments, 113 définitions de PNJ, 112 placements fixes, 21 quêtes, 34 objets d’inventaire, 216 objets du monde, 167 cases, 12 routines et 18 scénarios.

Source-fichiers.csv contient les empreintes des fichiers du dépôt et les exclusions. La configuration d’hébergement existante est retirée de l’export ; le jeu statique reste identique. Aucun secret ni métadonnée Git n’est volontairement inclus.

Pour rejouer les tests, utiliser npm test dans 07_MAQUETTE_ARCHIVE_v0.13. Certains tests et outils ont besoin de @napi-rs/canvas, recherché par CODEX_PRIMARY_RUNTIME_NODE_MODULES. Ce module natif n’est pas distribué ; il n’est pas nécessaire au jeu navigateur. Des outils de rendu historiques possèdent des chemins absolus de l’ancienne session, à adapter dans une copie d’analyse.

Le tome 1 original est conservé intégralement. Son empreinte attendue est 7c3e79a54e54b6a9d2db59b2a93af4e75529dbfa4b6dc10ee2144670076031c2.

Les contrôles finaux de composition, correspondance des sources, PDF, références locales et intégrité du ZIP figurent dans CONTROLE-LIVRAISON.json et le bilan de validation fourni avec l’export.
