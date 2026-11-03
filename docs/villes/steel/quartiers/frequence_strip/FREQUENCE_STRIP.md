# Fréquence Strip (Center-Town, dalle de Steel-Mégalopolis)

Pack créatif d'Ocre pour le développeur, sur le modèle de Pulse Plaza. Légende : **[canon]** = site Groovy Crew ou roman ; **[décision]** = consigne de Valentin ou du développeur ; **[proposition]** = idée d'Ocre, à valider.
Sources : `GROOVY_CREW.md`, `quartiers/CENTER_TOWN_LIEUX.md` (branche creation/groovy-crew), `pulse_plaza/PULSE_PLAZA.md`, `docs/villes/STEEL_MEGALOPOLIS_PLAN.md`, `docs/CANON_ARBITRAGES.md`.

## Ce qui est fixé
- **[canon]** Fréquence Strip (site) : « After hours ». « Néons mouillés, publicités qui chantent plus fort que les gens. » « Le slogan de la ville. Répété jusqu'à devenir une prière. »
- **[canon]** Club Neon-7 : « Next Drop. Entrée : sourire calibré. » Le groupe y a joué le 26/09, soirée Next Drop.
- **[canon]** Core Stack : salle de concert de la tournée, date du 31/10. Le site n'en dit rien de plus.
- **[canon]** Devise de la ville : « Heart. Rhythm. Groove. » Pubs GT : « Be iconic. Be perfect. Be groovy. »
- **[décision]** Zone `steel_strip`, reliée à la sortie est de Pulse Plaza (`steel_pulse`).
- **[décision]** Groovy Vibes et Groovy-Tron ne paraissent que sur des écrans, des affiches et dans les médias. Personne ne les rencontre.
- **[décision]** Le nom civil de Vibes n'apparaît jamais.
- **[décision, CENTER_TOWN_LIEUX]** Fréquence Strip est sur la dalle de Center-Town, pas dans Lower-Town.

## Ambiance [proposition]
**Lumière.** C'est la rue la plus lumineuse de la dalle, mais d'une lumière sale : néons violets et magenta qui grésillent, reflets sur un sol toujours mouillé, vapeur qui sort des grilles et accroche les couleurs. Chaque enseigne clignote à son propre rythme, si bien que la rue ne paraît jamais tout à fait stable. Les ruelles de côté restent noires.

**Palette.**
| Rôle | Couleur | Hex |
|---|---|---|
| fond, nuit | bleu nuit | `#060a10` |
| façades | brun-noir | `#1c1418` |
| néon dominant | magenta | `#e03ca8` |
| néon secondaire | violet | `#8a3cff` |
| écrans, reflets | cyan pâle | `#a9d2e6` |
| bars, cuisine | ambre chaud | `#f2b44a` |
| tapis du Neon-7 | rouge velours | `#7a1428` |
Le Strip est plus chaud que Pulse Plaza : moins de blanc d'IO, plus d'ambre dans les bars et les stands.

**Sons.** Basses qui traversent les murs du Neon-7 et du Core Stack, chacune sur son propre morceau, ce qui fait se chevaucher deux tempos au milieu de la rue. Pubs qui chantent leur jingle quand on passe devant, vapeur qui siffle, verres, rires, une dispute au loin, pluie fine sur les auvents.

**Musique.** Pas de boucle unique : la musique dépend de la porte la plus proche. Près du Neon-7, funk house autour de 124 BPM ; près du Core Stack, synthwave plus lourde ; entre les deux, un mélange volontairement brouillé. Extraits du groupe (canon) qui passent sur les écrans : « Danse, sois plus chrome », « Bad Buzz Protocol », « Trois secondes pour m'aimer ».

## Plan de la zone [proposition]
Zone `steel_strip`, 64 x 24 m, cases de 2 m (32 colonnes x 12 rangées). x vers l'est, z vers le sud. La rue court d'ouest en est.

```
    col 0        8          16         24        31
r0  F F F F F N N N N N N F F F F F F F F C C C C C C F F F F F F F
r1  F F F F F N N N N N N F F F F F F F F C C C C C C F F F F F F F
r2  F F F F F N N N N N N F F F F F F F F C C C C C C F F F F F F F
r3  . . e . . . . t t . . . e . . . . . . . . q q . . . e . . . . .
r4  < . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   entrée ouest : Pulse Plaza (sortie est)
r5  < . s . . . . . . . . . . . v . . . . . . . . . . . . . s . . .
r6  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
r7  . . . . b b . . . . . . c . . . . . . . . . . r r . . . . . . .
r8  . . . . b b . . . . . . . . . . . . . . . . . r r . . . . . . .
r9  G G G G G G G G R R R R G G G G G G G G G G G G G G G H H H G G
r10 G G G G G G G G R R R R G G G G G G G G G G G G G G G H H H G G
r11 G G G G G G G G R R R R G G G G G G G G G G G G G G G H H H G G
```
Légende : F façades nord ; N Club Neon-7 ; C Core Stack ; G façades sud ; R bar Le Retour ; H hôtel capsule ; t tapis rouge et cordon du Neon-7 ; q file d'attente du Core Stack ; b, r stands de rue ; e enseignes animées en façade (voir ASSETS.md) ; s bouches de vapeur ; v videur ; c caméra C.A.G.E. ; < entrée.

Repères (m) :
| id | élément | cases | x, z (m) | visitable |
|---|---|---|---|---|
| fs_neon7 | Club Neon-7 | c5-10, r0-2 | 10-22, 0-6 | non pour l'instant (porte gardée) |
| fs_corestack | Core Stack | c19-24, r0-2 | 38-50, 0-6 | non pour l'instant |
| fs_retour | bar Le Retour | c8-11, r9-11 | 16-24, 18-24 | oui (intérieur à prévoir) |
| fs_capsules | hôtel capsule | c27-29, r9-11 | 54-60, 18-24 | non |
| fs_stand_brochettes | stand de brochettes | c4-5, r7-8 | 8-12, 14-18 | oui (marchand) |
| fs_stand_merch | stand de merch pirate | c23-24, r7-8 | 46-50, 14-18 | oui (marchand) |
| fs_tapis | tapis du Neon-7 | c7-8, r3 | 14-18, 6-8 | non |
| fs_file | file du Core Stack | c21-22, r3 | 42-46, 6-8 | non |
| fs_vapeur | bouches de vapeur | (2,5) (28,5) | (5,11) (57,11) | non |
| fs_camera | C.A.G.E. | (12,7) | (25,15) | non |
| enseignes | 4 en façade nord, 2 en façade sud | voir ASSETS.md | | non |
Jonctions : ouest (c0, r4-5) vers la sortie est de Pulse Plaza [décision]. Est (c31) : bout de rue fermé par une grille pour l'instant [proposition].

## Bâtiments [proposition sauf mention]
- **Club Neon-7** [canon pour le nom et la phrase d'entrée] : façade noire, cadre de néons magenta, tapis rouge, cordon, porte capitonnée. Au-dessus de la porte, un portique scanne le sourire des clients (« sourire calibré »). Fermé au joueur.
- **Core Stack** [canon pour le nom] : ancien bloc de serveurs reconverti en salle, empilement de baies métalliques, ventilations qui crachent de la vapeur, écrans cyan. Affiche de la date du 31/10 [proposition, minuteur possible].
- **Le Retour** : bar d'habitués, ambre chaud, seul endroit de la rue où la musique est plus basse.
- **Hôtel capsule** : façade de cases empilées, quelques hublots allumés.
- **Stands** : brochettes (ambre, fumée), merch pirate du groupe (contrefaçons de la casquette pixel et du tee 8-bit).
- **Écrans de la rue** : clips de Vibes et de Tron, uniquement à l'écran.

## PNJ [proposition]
Clé de sprite `gen_fs_<id>`. Aucun d'eux n'est Vibes ni Tron, aucun ne cite d'identité civile.

1. **Rocco, videur du Neon-7** (`gen_fs_rocco`, 1,95 m, cyborg). Costume sombre, mâchoire chromée. Près du tapis (16 ; 9).
   - « Le scanner dit que ton sourire est à soixante pour cent. Il faut quatre-vingts. Reviens quand tu seras content. »
   - « Moi je ne choisis personne. C'est la machine. Je me contente d'être grand. »
2. **Lila, danseuse en pause** (`gen_fs_lila`, 1,68 m, augmentée). Paillettes, veste sur les épaules. Devant le Neon-7 (22 ; 8).
   - « Douze sets cette semaine. Dans le contrat, il y a une clause sur le sourire. Je l'ai lue deux fois pour être sûre. »
   - « Ils passent "Danse, sois plus chrome" toutes les heures. Je crois qu'au bout d'un moment, plus personne n'entend les paroles. »
3. **Hugo, file du Core Stack** (`gen_fs_hugo`, 1,74 m). Tee 8-bit contrefait, billet froissé. Dans la file (44 ; 7).
   - « J'attends depuis six heures. Le concert du 31, c'est ce soir ou dans un an, personne n'est sûr. »
   - « Si elle passe en vrai, tu crois qu'on la reconnaîtra ? Personne ne sait à quoi elle ressemble sans le chapeau. »
4. **Mme Okoro, patronne du Retour** (`gen_fs_okoro`, 1,70 m, humaine avec implant). Tablier, bras croisés. Comptoir du Retour (20 ; 18).
   - « Ici on baisse le son. Les gens viennent pour s'entendre penser, et ça, la rue ne le fait plus. »
   - « Les caméras du Strip ne marchent pas, c'est écrit dessus. Moi, je fais comme si elles marchaient. »
5. **Tibo, vendeur de merch pirate** (`gen_fs_tibo`, 1,66 m). Sac à dos ouvert, casquettes empilées. Stand (48 ; 15). Marchand.
   - « La casquette officielle coûte trois fois plus et elle déteint pareil. »
   - Si Repérage à 2 : « Tu peux t'éloigner un peu ? Tu attires les drones, et moi je n'ai pas de licence. »
6. **Yun, cuisinier des brochettes** (`gen_fs_yun`, 1,72 m). Toque en papier, gants. Stand (10 ; 15). Marchand.
   - « Brochettes de quoi ? De protéines. C'est marqué sur le carton, et le carton, je ne l'ai pas écrit. »
   - « À l'heure où le Neon-7 ferme, je vends trois fois plus. Les gens sortent avec faim et sans sourire. »
7. **Un GT de promotion** (`gen_fs_gt_promo`, 1,85 m). Androïde chrome de série, même modèle que le Clone 7 de Pulse Plaza, tient un panneau lumineux sans texte. Milieu de rue (32 ; 12).
   - « Bonsoir. Je suis ici pour vous rappeler qu'il y a un concert. Il y a toujours un concert. »
   - Si le joueur insiste : « Je n'ai pas d'avis. Mon modèle n'en avait pas en option. »
8. **Sacha, ingé son du Core Stack** (`gen_fs_sacha`, 1,78 m). Casque autour du cou, câbles. Côté Core Stack (50 ; 8).
   - « Tron chante en direct, enfin c'est ce qu'on dit. Moi je règle le son, je ne vérifie rien. »
   - « La salle tient mille personnes. Le soir où le système de sync a planté, il en restait trois cents qui applaudissaient. »
9. **Vieux Marius, assis sur les marches de l'hôtel** (`gen_fs_marius`, 1,70 m). Manteau usé. Devant l'hôtel capsule (58 ; 17).
   - « Avant les écrans, le Strip s'appelait autrement. Je ne me souviens plus comment. C'est peut-être ça, le but. »
   - « Un conseil : la nuit, ne regarde pas les pubs dans les yeux. Elles te reconnaissent. »

## Caméo : Ocre, peintre de rue
**[décision]** Caméo d'un membre du studio, PNJ ordinaire, sans mécanique. Les vigiles regardent ailleurs : aucune réaction de leur part. La fresque est une image de Groovy Vibes, donc un média, pas une apparition en personne.
- Sprite `gen_fs_ocre` (1,68 m), portrait `portrait-gen_fs_ocre`, décor `fs_fresque_vibes` (mur de fresque inachevée, 6 m).
- Femme de 29 ans, cheveux cuivrés bouclés, yeux ambrés, taches de rousseur, tenue bohème et industrielle, soignée, doigts tachés de peinture.
- **Emplacement proposé** : façade sud, entre Le Retour et l'hôtel capsule, mur de fresque vers x 28 à 34, z 18 ; Ocre devant, vers (31 ; 16,8), tournée vers le mur.
- Répliques [proposition] :
  - « Recule un peu, tu me fais de l'ombre. Et ton ombre n'a aucun talent. »
  - « Non, elle n'a pas posé pour moi. Personne ne l'a jamais vue poser. J'ai mieux que ça, j'ai de la mémoire. »
  - « Les vigiles ? Ils adorent la fresque. Ils font semblant de ne pas me voir depuis trois nuits. »
  - Clin d'œil au joueur : « Toi, je te mettrais bien dans un coin du mur. Tout petit. Personne ne regarde jamais les coins, et c'est là que je cache les meilleurs. »

## Concept art
`concepts/maquette_frequence_strip_iso.jpg` : **maquette générée**, référence d'ambiance, **pas une capture du jeu**.

## Compléments : quartier rouge, rue allongée [proposition]
Code couleur d'un quartier rouge **[décision Valentin]** : les enseignes dominent en rouge et rose, l'ambre vient en touche, le violet existant reste un accent. La palette rouge fait foi : la lumière du code passe au rouge et au rose (voir `docs/villes/steel/ENSEIGNES_CODE.md`), le violet ne reste que sur Core Stack et Vibes, et les vitrines violettes peintes sortent en rose.
- **Devantures.** Un club de strip (`fs_club`, 10 m) et des cabines à rideaux (`fs_cabines`, 8 m), faces x à la pente 0,33. Chaque devanture a une porte lisible, documentée en `porte_coins` dans le manifest pour un futur intérieur. Les enseignes sont peintes éteintes : le code dessine les néons qui clignotent dans `neon_coins`. Aucune enseigne ni auvent ne déborde sur un accès.
- **PNJ.** Prostitué·es et racoleurs en grappes devant les portes (club et cabines), un mac un peu en retrait, et une patrouille de police de deux agents qui marche le long de la rue en regardant ailleurs. Tous habillés, rien d'explicite.
- **Sols.** À 50 px/m, mats, sans reflet (le moteur gère les zones mouillées) : trottoirs étroits, asphalte de chaussée, et en pièces séparées le caniveau, les plaques d'égout, les détritus et les cartons. Raccords fondus pour ne pas lire de damier.
- **Rue allongée et plus dense.** Les poses ci-dessous supposent la rue actuelle (64 m) prolongée vers l'est ; les coordonnées sont à recaler si la longueur change.

| fichier | px | ancre | pose suggérée (x ; z en m) |
|---|---|---|---|
| `fs_club.webp` (+ `fs_club_neon.webp`) | 500 x 565 | [498, 564] | façade nord, x 54 à 64, z 0 à 1,5 (à la place de fs_fn3 et fs_fn4) ; porte au centre, vers (59 ; 1,5) ; l’auvent ne dépasse pas sur l’accès |
| `fs_cabines.webp` (+ `fs_cabines_neon.webp`) | 400 x 432 | [398, 431] | façade sud, entre Le Retour et l’hôtel capsule, à l’est de la fresque d’Ocre : x 38 à 46, z 22,5 à 24 ; porte à droite, vers (44,5 ; 22,5) |
| `gen_fs_rouge.webp` | 180 x 512 | [90, 511] | grappe devant le club : (55 ; 3,2) |
| `gen_fs_rubis.webp` | 180 x 512 | [90, 511] | grappe devant le club : (56,6 ; 3,6) |
| `gen_fs_fourrure.webp` | 180 x 512 | [90, 511] | grappe devant le club : (55,8 ; 4,4) |
| `gen_fs_racoleur.webp` | 180 x 512 | [90, 511] | à côté de la porte du club : (58 ; 3) |
| `gen_fs_racoleuse.webp` | 180 x 512 | [90, 511] | devant la porte des cabines : (44 ; 20,6) |
| `gen_fs_mac.webp` | 180 x 512 | [90, 511] | adossé près des cabines, un peu en retrait : (47 ; 20,2) |
| `gen_fs_flic_a.webp` | 180 x 512 | [90, 511] | patrouille qui ferme les yeux, marche le long de z 12 de x 30 à 62, regard tourné vers la rue |
| `gen_fs_flic_b.webp` | 180 x 512 | [90, 511] | patrouille, suit flic_a à 1,5 m |
| `g_fs_trottoir_etroit.webp` | 128 x 320 | sans ancre | trottoirs étroits des deux côtés de la rue (z 6 à 8 et z 16 à 18), dalles de longueurs inégales |
| `g_fs_asphalte.webp` | 512 x 512 | sans ancre | chaussée (z 8 à 16) |
| `fs_caniveau.webp` | 200 x 40 | [100, 20] | bordure de trottoir côté chaussée, répété tous les 4 m le long de x (z 8 et z 16) |
| `fs_plaque_egout.webp` | 40 x 40 | [20, 20] | sur la chaussée, 3 ou 4 dans la rue, ex. (20 ; 12), (44 ; 10) |
| `fs_detritus.webp` | 60 x 50 | [30, 25] | pieds de façade et coins de porte, ex. (50 ; 6,5), (36 ; 17,5) |
| `fs_carton.webp` | 60 x 60 | [30, 30] | ruelles de côté, près de l’hôtel capsule |

Portraits 192 x 192 : `portrait-gen_fs_<id>` pour les huit PNJ. Planche de contrôle : `/workspace/nml-shots/strip_arena_complements.png`.

## Compléments 2 : devantures étroites, premier plan bas, figurants [proposition]
Rue étroite et sombre, éclairée seulement par les enseignes. Couleurs **[décision Valentin]** : rouges et roses dominants, ambre en touche, violet en accent. Budget d'animations à 8 sur 8 : aucune nouvelle animation. Chaque enseigne est une image fixe, avec sa couche `_neon.webp` séparée (même taille, même ancre que la façade) que le code pose en mode additif. Elle reste allumée en fixe tant que le budget est plein.

**Enseignes et jeux de mots** [proposition] : le texte est dans la couche néon seulement, en lettres nettes, la façade porte un panneau éteint.
- `fs_club` : « L'Effeuillée ».
- `fs_cabines` : « Cabines sans C.A.G.E. » (les caméras du Strip ne marchent pas, c'est écrit dessus).
- `fs_sexshop` : « Jouets calibrés », clin d'œil au « sourire calibré » du Neon-7. Vitrines de jouets stylisés, rien de graphique.
- `fs_peep` : « 3 secondes », en vertical, d'après « Trois secondes pour m'aimer ». Cabines à crédits, fente à crédits près de la porte.
- `fs_salon` : « Tombé de rideau », salon à rideaux rouges et bar à hôtesses.
- `fs_lovehotel` : « L'Heure exquise », hôtel facturé à l'heure. Le rideau de lanières couvre une alcôve de stationnement, ce n'est pas un accès.
- `fs_clubprive` : « Club 404 », club privé où l'on ne trouve jamais les membres.
- Premier plan sud : « Nouilles de minuit », « Excuses » (des fleurs pour se faire pardonner en sortant), « À crédit » (tabac et recharges).

**Portes.** Chaque porte est décrite par `porte_coins` (haut gauche, haut droit, bas droit, bas gauche, en px du sprite). Les deux comptoirs du premier plan ont `comptoir_coins` et `guichet_coins` : on y sert depuis la rue, sans entrer. Aucune enseigne ne couvre une porte.

**Côté nord**, de l'ouest à l'est, rue prolongée à 80 m : `fs_facade_nord` 0 à 8, `fs_bouche_nord` 7 à 11 (bouche le trou de x 8 à 10), Neon-7 10 à 22, `fs_sexshop` 22 à 30, `fs_peep` 30 à 34, `fs_salon` 34 à 38, Core Stack 38 à 50, `fs_bouche_nord` 50 à 54, `fs_club` 54 à 64, `fs_lovehotel` 64 à 72, `fs_clubprive` 72 à 80.

**Côté sud, premier plan.** Trois devantures basses de 2 m au plus, à la manière de murets et d'auvents bas, pour ne masquer aucun personnage.

| fichier | px | ancre | enseigne | pose suggérée (x ; z en m) |
|---|---|---|---|---|
| `fs_sexshop.webp` | 400 x 632 | [398, 631] | Jouets calibrés | façade nord, x 22 à 30, z 0 à 1,5 (à la place de fs_fn1) ; porte au centre, vers (26 ; 1,5) |
| `fs_peep.webp` | 200 x 466 | [198, 465] | Trois secondes | façade nord, x 30 à 34, z 0 à 1,5 (moitié ouest de fs_fn2) ; porte à gauche, vers (31 ; 1,5) |
| `fs_salon.webp` | 200 x 466 | [198, 465] | Tombé de rideau | façade nord, x 34 à 38, z 0 à 1,5 (moitié est de fs_fn2) ; porte à gauche, vers (35 ; 1,5) ; l’auvent reste au-dessus de 2,6 m |
| `fs_lovehotel.webp` | 400 x 632 | [398, 631] | L’Heure exquise | façade nord, rue allongée : x 64 à 72, z 0 à 1,5 ; porte à gauche, vers (65,5 ; 1,5) ; le rideau de lanières n’est pas un accès |
| `fs_clubprive.webp` | 400 x 582 | [398, 581] | Club 404 | façade nord, rue allongée : x 72 à 80, z 0 à 1,5 ; double porte au centre, vers (76 ; 1,5) |
| `fs_bouche_nord.webp` | 200 x 466 | [198, 465] |  | bouche le trou de la façade nord de x 8 à 10 : poser de x 7 à 11, z 0 à 1,5, derrière fs_fn0 et fs_neon7 (1 m de recouvrement de chaque côté, le rideau métallique tombe dans le trou) ; second exemplaire possible de x 50 à 54, entre le Core Stack et fs_club |
| `fs_bas_nouilles.webp` | 400 x 232 | [398, 231] | Nouilles de minuit | côté sud, premier plan : x 0 à 8, z 17 à 18, devant fs_fs0 ; comptoir tourné vers la rue |
| `fs_bas_fleurs.webp` | 200 x 166 | [198, 165] | Excuses (fleurs pour se faire pardonner) | côté sud, premier plan : x 8 à 12, z 17 à 18 ; passage au centre, vers (10 ; 17) |
| `fs_bas_tabac.webp` | 200 x 166 | [198, 165] | À crédit | côté sud, premier plan : x 12 à 16, z 17 à 18, juste à l’ouest du bar Le Retour ; guichet tourné vers la rue |

Chaque façade avec enseigne a sa couche `<clé>_neon.webp`, de la même taille et avec la même ancre.

**Figurants** [proposition] : cinq silhouettes en plus des rôles déjà faits, tous habillés, sans réplique.

| fichier | px | ancre | pose suggérée |
|---|---|---|---|
| `gen_fs_client_imper.webp` | 180 x 512 | [90, 511] | hésite à 3 m de la porte des cabines, tourné vers la rue : (41 ; 19,5) |
| `gen_fs_client_costume.webp` | 180 x 512 | [90, 511] | devant le peep-show, regarde par-dessus l’épaule : (32,5 ; 3,4) |
| `gen_fs_passante.webp` | 180 x 512 | [90, 511] | passante, traverse de (20 ; 8) à (28 ; 16) |
| `gen_fs_passant_canne.webp` | 180 x 512 | [90, 511] | passant lent le long du trottoir nord, de x 40 à x 60 sur z 7 |
| `gen_fs_videur_prive.webp` | 180 x 512 | [90, 511] | videur du club privé, à droite de la double porte : (78 ; 2,6) |

**Sols assombris.** `g_fs_asphalte` (presque noir), `g_fs_trottoir_etroit` (pavés sombres) et `g_ar_dalles_usees` (anthracite) sont étalonnés sombres, et les grandes taches qui se répétaient d'une tuile à l'autre sont retirées par un passe-haut. Ils restent mats : le mouillé et les reflets sont au moteur.

Planche de contrôle : `/workspace/nml-shots/strip_complements2.png` (maquette de pose en bas, pas une capture du jeu).

## Pose retenue (main, lot construction du Strip)
La palette rouge de la préparation (1782ca8) fait foi.
- **Rue de 80 m**, zone 80 x 24 m. Portes : ouest vers Pulse Plaza inchangée (0 ; 10), est vers l'Arena recalée en (80 ; 13), grille `fs_grille_est` en x 76 à 80.
- **Nord, front sur le trottoir (z 6).** Les devantures minces (profondeur 1,5 m) sont posées z 4,5 à 6 et non z 0 à 1,5, pour garder une rue droite entre les blocs d'origine (fs_facade_nord, Neon-7, Core Stack, z 0 à 6). Ordre et x conformes. `fs_bouche_nord` ferme la ruelle x 8-10 en retrait (z 3 à 4,5) : c'est la cachette de Fusible.
- **Sud, premier plan (front z 24).** Rien de haut devant les personnages : `fs_bas_*` au bord de la zone (z 23 à 24) ; Le Retour, l'hôtel capsule, la fresque (x 28-34, z 23,4 à 24) et les cabines (z 22,5 à 24) restent. Les autres trous du bord sud sont fermés par des répétitions des trois devantures basses, calque néon éteint.
- **Personnages.** Aucun dans l'ombre d'écran d'une façade : `view.masques()` est vide (vérifié par `view.masqueEn(x, z)`). Écarts : Ocre recule à (27,5 ; 19,8) face à sa fresque, le client en imperméable hésite à 3 m à l'est des cabines (45 ; 19,4), la rabatteuse et M. Velours sont à l'est de la porte des cabines, Tibo et Yun à côté de leur stand, Okoro devant « À crédit », Marius à l'est de l'hôtel. La patrouille (deux PNJ, le moteur ne fait pas marcher un PNJ) se tient au milieu de la rue, le regard tourné vers l'est. Le passant à canne marche de x 40 à 52,6 (au-delà, la règle de tri passe la devanture du club devant lui).
- **Sols.** `g_fs_asphalte` en tuiles de 10,24 m, `g_fs_trottoir_etroit` aux proportions 2,56 x 6,4 m ; caniveaux, plaques, détritus et cartons peints dans le sol (`ground.decals`), sans sprite.
- **Enseignes.** Les calques `_neon` sont posés automatiquement ; effets : peep-show et cabines grésillent, L'Effeuillée a une lettre qui saute, L'Heure exquise pulse, le Club 404 clignote. Vibes et Tron se font face sur le mur aveugle x 50-54.
- **Reste à fournir.** Trois ou quatre devantures basses de plus pour le sud (x 24-28, 34-38, 46-54, 60-80 portent aujourd'hui des répétitions éteintes) ; idéalement un passant de patrouille marchant (planche de marche) si la patrouille doit bouger.
