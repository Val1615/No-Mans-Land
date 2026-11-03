# Enseignes et faisceaux animés par le code — format d'Ocre, lu tel quel par view.js

1. Une enseigne = la façade `<clé>.webp` (panneau peint éteint) + son calque `<clé>_neon.webp` : même taille en pixels, même ancre, fond transparent (déjà livré : fs_club, fs_cabines, fs_sexshop, fs_peep, fs_salon, fs_lovehotel, fs_clubprive, fs_bas_*).
2. Manifeste : deux entrées ordinaires `<clé>` et `<clé>_neon` (px, anchor, file), sans `anime`, `frames` ni `fps` ; `neon_coins` situe le texte.
3. Le code pose le calque en additif sur la façade dès qu'elle est posée dans une zone : rien d'autre à déclarer, allumé fixe par défaut.
4. Le noir du calque ne s'ajoute pas : pas de halo peint ; la tache au sol reste une `glow` de la zone, de la couleur de l'enseigne.
5. Réglage facultatif dans la zone (validé par l'éditeur) : `enseignes: [{ id, building, effet, periode, decale, intensite, couleur, saute, dev }]`.
6. `effet` : `fixe`, `clignote`, `gresille`, `saute` (la colonne `saute: [u0, u1]` de l'image, une lettre lue dans `neon_coins`, grésille seule), `pulse`.
7. Coût : une couleur par image, aucune planche ni échange de texture ; hors plafond `view.animStats.on` (8 sur mobile), compté dans `animStats.enseignes`.
8. Démo en place derrière `?dev=1` : Neon-7 (`saute`) et Le Retour (`pulse`), qui n'ont pas encore de calque `_neon` (le support sert de contour).
9. Faisceaux : tout bâtiment dont le manifeste donne `source_faisceau_px` (ar_pylone_projecteur, `anime_par_code`) tire un cône additif depuis ce pixel, sans déclaration.
10. Réglage facultatif : `projecteurs: [{ building | x, z | fx, fz, y, couleur, longueur, ouverture, inclinaison, cap, balayage, periode, decale, intensite }]`, hors budget (`animStats.projecteurs`).
