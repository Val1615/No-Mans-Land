# Vidéo

| Fichier | Contenu | Format | sha256 |
|---|---|---|---|
| `cinematique_ouverture.mp4` | Cinématique d'ouverture de Valentin (2026-11-13) : splash du studio, avec son | 12,87 s, H.264 High 1280×720 30 i/s + AAC stéréo, 15,2 Mo | `d3ba44185f2e213a03f6bd312c7fc34f306a93669ccae755e167e42bda33de66` |

Copiée telle quelle (version allégée envoyée par Valentin), jamais réencodée ni retaillée. Lecture : `src/ui/cinematique.js`, une fois par chargement de page, avant l'allumage du Terminal. Le fondu au noir de fin est un voile CSS, pas une retouche du fichier.
Note : l'atome `moov` est en fin de fichier (pas de « faststart ») ; le navigateur va le chercher par requête Range (GitHub Pages les sert), d'où un court délai avant la première image sur réseau lent.
