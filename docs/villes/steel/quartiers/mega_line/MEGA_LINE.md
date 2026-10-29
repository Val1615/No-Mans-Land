# Mega-Line (Center-Town, dalle de Steel-Mégalopolis)

Fiche du quartier de la Mega-Line, la ligne aérienne qui traverse Center-Town, et de son terminus de fret.
Sources : la maquette `concepts/maquette_mega_line_iso.jpg`, `src/data/steel.js` (lu, non modifié), les fiches Pulse Plaza, Fréquence Strip, Steel Arena et Dôme Fréquence.

## Ce qui est fixé
- **[canon]** Steel-Mégalopolis vit sous le sarcophage. Le périmètre est désertique et gardé par des douanes.
- **[décision]** Vibes et Tron ne paraissent que sur des écrans et dans les médias, jamais en personne. Aucun autre visage sur les écrans.
- **[décision Valentin]** Le terminus est une gare de fret au bout nord de la ligne, du côté opposé à la douane. La voie bute sur des portes massives fermées, sans ouverture, hublot ni lumière venue de dehors. On ne voit jamais le désert : ni sable ni ciel dans les sprites. Un panneau y affiche « Dernier arrêt avant No Man's Land ».

## Raccordement [proposition]
- Zone `steel_megaline`, 48 x 24 m. On y entre depuis le bord nord de `steel_center`, par une porte `c_mega` vers (8 ; 0), à l'ouest de la sortie de Pulse Plaza (`c_nord`, x 33). On arrive au sud de la zone, au pied des deux escaliers de la station.
- Le viaduc traverse la zone en diagonale, du sud-ouest au nord-est. La rame passe toutes les quarante secondes environ, déplacée par le code, sans s'arrêter tant que le joueur n'a pas de billet.
- Zone `steel_terminus`, 30 x 20 m, au bout nord-est du viaduc **[décision Valentin pour le lieu, proposition pour le raccord]**. On y accède à pied par une passerelle de service au fond de `steel_megaline`, ou plus tard en prenant la rame. Le sas reste fermé : aucune porte de sortie n'est prévue.

## Ambiance [proposition]
La Mega-Line est le seul endroit de Center-Town où la ville a l'air de bouger toute seule. Le viaduc de fer noir passe au-dessus des têtes, les piles ruissellent, et la rame violette glisse sans bruit, fenêtres ambrées. Sous le quai, des échoppes vivent de l'attente : nouilles, réparations, câbles. Sur le quai, deux écrans passent Vibes et Tron en boucle, que personne ne regarde vraiment parce que tout le monde les connaît par cœur.

Le terminus est l'inverse. Plus d'écran, plus de pub. Une gare de fret sous une voûte de béton, des conteneurs, un portique jaune, et au bout de la voie des portes si grandes qu'on les prend d'abord pour un mur. Deux lampes d'alerte clignotent dessus. Le panneau est la seule chose qui parle du dehors.

## Bâtiments et décor [proposition]
**La ligne (`steel_megaline`)**
- Viaduc (`ml_viaduc`), segment de 24 m répétable, sur piles de fer riveté.
- Station aérienne (`ml_station`), quai de 20 x 6 m, rambardes laiton, ligne jaune, deux escaliers, échoppes dessous. Deux cadres d'écran éteints où le code pose les écrans de Vibes et de Tron.
- Rame (`ml_rame`), trois voitures violettes, 24 m.
- Mobilier : lampadaires, bancs, borne de billets, tableau des départs, poubelles.
- Façade Human Corp sous le viaduc, avec son logo qui respire.

**Le terminus (`steel_terminus`)**
- Sas (`ml_sas`), mur de béton et d'acier de 18 m, portes pleines, heurtoir de fin de voie.
- Bureau de la gare de fret (`ml_bureau_fret`), quai de chargement, une fenêtre ambrée.
- Conteneurs empilés (`ml_conteneurs`) et portique de levage (`ml_portique`).
- Panneau du terminus (`ml_panneau_terminus`), vierge à l'image, la phrase est affichée par le code.

## PNJ [proposition]
Clé de sprite `gen_ml_<id>`. Aucun d'eux n'est Vibes ni Tron, aucun ne cite d'identité civile.

**Sur la ligne**
1. **Anselme Roque, navetteur** (`gen_ml_navetteur`, 1,76 m). Imperméable gris, mallette. Bout du quai.
   - « Trente-huit minutes de trajet, tous les jours. J'ai fini par connaître les écrans mieux que mes enfants. »
   - « La rame n'est jamais en retard. C'est nous qui sommes en avance, d'après eux. »
2. **Sabine, contrôleuse** (`gen_ml_controleuse`, 1,66 m). Uniforme violet, casquette, lecteur de billets. Haut de l'escalier ouest.
   - « Billet, s'il vous plaît. Ou votre bracelet. Ou votre visage, la borne sait faire. »
   - « Le terminus ? Il n'y a rien là-bas, que du fret. Personne n'achète de billet pour le terminus. »
3. **Lou, étudiante** (`gen_ml_etudiante`, 1,60 m). Sac à dos, casque autour du cou. Sur un banc.
   - « Je révise dans la rame. C'est le seul endroit où le réseau me laisse tranquille. »
   - « Le prof dit que la ligne allait jusqu'au désert, avant. Maintenant elle s'arrête contre une porte. »
4. **Marcel, agent d'entretien** (`gen_ml_entretien`, 1,72 m). Combinaison orange, balai à brosse lumineuse. Sous le viaduc.
   - « Ça goutte du viaduc toute l'année. Il ne pleut jamais, ici, mais le fer transpire. »
   - « Au terminus, on nettoie les portes une fois par mois. Elles n'ont pas bougé depuis que je travaille. »
5. **Mme Tran, vendeuse de nouilles** (`gen_ml_nouilles`, 1,58 m). Tablier rouge, bol fumant. Échoppe sous le quai. Marchande.
   - « Un bol avant la rame, un bol après. Entre les deux, on attend. »
   - « Mon mari conduisait le fret. Il disait que derrière la porte, ça sent le sable. Je ne sais pas comment il savait. »
6. **Kessler, vigile Human Corp** (`gen_ml_vigile`, 1,92 m, augmenté). Armure grise, matraque. Au pied de la borne.
   - « Circulez. Le quai est fait pour attendre, pas pour rester. »
   - Si Repérage à 2 : « Vous avez pris les escaliers trois fois. La borne aime bien qu'on prenne la rame. »
7. **Noé, l'homme à la pancarte** (`gen_ml_pancarte`, 1,74 m). Masque, veste sombre, pancarte en carton vierge. Bas de l'escalier est.
   - « Je n'écris rien dessus. Quand j'écrivais, on me l'enlevait. »
   - « Tout le monde sait ce qu'il y a derrière la dernière porte. Personne n'a le droit de le dire. »
8. **Yuna, fan** (`gen_ml_fan`, 1,64 m). Veste violette, téléphone levé vers l'écran. Devant l'écran de Vibes.
   - « Je filme l'écran pour mon fil. Oui, je sais, c'est déjà une vidéo. »
   - « Tron bégaie toujours au même endroit. Je crois que c'est fait exprès. »

**Au terminus**
9. **Odile Ferraz, cheffe de la gare de fret** (`gen_ml_cheffe_fret`, 1,68 m). Long manteau à boutons laiton, planchette. Devant le bureau.
   - « Ici on charge, on décharge, on signe. Les portes, ce n'est pas mon service. »
   - « Le panneau, c'est la seule blague qu'ils aient laissée. Dernier arrêt. Comme si on pouvait aller plus loin. »
10. **Bruno, docker** (`gen_ml_docker`, 1,86 m, bras mécanique). Gilet orange, casque. Près du portique.
    - « Les conteneurs arrivent pleins de l'intérieur et repartent vers l'intérieur. Rien ne vient de dehors. Officiellement. »
    - « Pose ta main sur la porte, un jour de grand vent. Tu sentiras qu'elle tremble. »

Figurants sans dialogue : `gen_ml_foule_a` et `gen_ml_foule_b`, voyageurs sur le quai et au terminus.

## Animations et budget mobile [proposition]
Plafond de 8 animations visibles à la fois, groupes comptés pour une.
- Ligne : écrans de quai Vibes et Tron (un groupe, une horloge), tableau des départs, logo Human Corp, passage de la rame (code), lueurs des lampadaires (code, un groupe). Soit 5.
- Terminus : lampes d'alerte du sas, gyrophares (x 2, un groupe), lueurs de quai (code). Soit 3.
Aucun faisceau, halo ou lumière animée n'est peint dans les sprites de base.

## Questions ouvertes
- La rame doit-elle s'arrêter et devenir un vrai trajet vers le terminus, ou le terminus reste-t-il accessible à pied seulement ?
- Le billet de la Mega-Line est-il un objet, un drapeau, ou une ligne du bracelet ?
- Faut-il une quête liée aux portes du terminus, sachant qu'elles ne s'ouvriront jamais à l'écran ?
