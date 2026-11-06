# Pulse Plaza (Center-Town, dalle de Steel-Mégalopolis)

Pack créatif d'Ocre pour le développeur. Légende : **[canon]** = site Groovy Crew ou roman ; **[décision]** = consigne de Valentin ; **[proposition]** = idée d'Ocre, à valider.
Sources : `GROOVY_CREW.md`, `quartiers/CENTER_TOWN_LIEUX.md`, `docs/villes/STEEL_MEGALOPOLIS_PLAN.md`, `docs/CANON_ARBITRAGES.md`, `docs/assets/`.

## Ce qui est fixé
- **[canon]** Center-Town : des tours, dont l'Arcadius Center, siège de la gestion d'IO (roman, Ch. III §854). La ville utilise le crédit.
- **[canon]** Pulse Plaza (site) : écrans géants, clones chrome, foule en mode applaudir, Feed 24/7, Audience sync. Écran du feed : « L'idole démasquée. Qui est vraiment Groovy Vibes ? » et « 100% connection stable. Jusqu'à la prochaine alerte. »
- **[canon]** Éléments de rue : billboard HCM-88X de Vibes (« Le sourire est une mise à jour »), projection Holo-Tron, pubs GT, caméras C.A.G.E. (« Inactives. Officiellement. »).
- **[décision]** Center-Town est sur la dalle surélevée au-dessus de Lower-Town. Pulse Plaza en est un quartier.
- **[décision]** Groovy Vibes et Groovy-Tron ne paraissent que sur les écrans et dans les médias. Aucune rencontre en personne, aucun sosie qui parle à leur place.
- **[décision]** Le nom civil de Vibes n'apparaît jamais. Les PNJ en parlent comme d'un mystère, sans avancer de nom ni d'origine.
- **[décision]** Le Dôme Fréquence reste dans la rue d'arrivée, fermé au joueur. Il n'est donc pas sur la place.

## Ambiance [proposition]
**Lumière.** Nuit permanente sous le sarcophage, mais la place n'est jamais sombre : ce sont les écrans qui éclairent. La lumière vient d'en haut et de côté, elle change toutes les 8 à 12 secondes quand le feed passe d'un clip à l'autre. Sol mouillé qui renvoie les reflets. Les angles de la place, loin des écrans, retombent dans le bleu acier du reste de Steel.

**Palette.**
| Rôle | Couleur | Hex |
|---|---|---|
| fond, nuit | bleu nuit | `#060a10` |
| structures, dalle | bleu acier | `#2b3e52` |
| métal clair | gris-bleu | `#6f8496` |
| néon dominant (Groovy Crew) | violet | `#8a3cff` |
| néon secondaire | magenta | `#e03ca8` |
| écrans, reflets froids | cyan pâle | `#a9d2e6` |
| Human Corp, IO | blanc cassé | `#e8eef2` |
| alerte C.A.G.E. | rouge discret | `#c8323c` |
Le violet est réservé aux médias du groupe : pubs, écrans, merch. IO et Human Corp restent en blanc et bleu froid, ce qui laisse lire qui parle sur chaque écran.

**Sons.** Rumeur de foule constante, applaudissements qui partent tous en même temps quand l'écran affiche « Audience sync », puis s'arrêtent net. Bourdonnement électrique des panneaux, gouttes sur la tôle, drones de surveillance qui passent, annonces courtes d'IO en voix neutre. Près des caméras, un petit déclic quand l'objectif suit le joueur.

**Musique.** Boucle principale autour de 170 BPM, nu-disco et synthwave, filtrée comme si elle sortait des écrans. Près de l'écran principal, le morceau est net ; ailleurs on n'entend que la basse et la voix vocodée de Tron. Titres repris en extraits (canon) : « HeartSync », « Toujours en ligne », « Erreur 404, Argument introuvable ». Quand une alerte passe sur le feed, la musique se coupe deux secondes puis reprend sur le même temps, sans transition.

## Plan de la zone [proposition]
**[décision du développeur, 29/10]** Zone `steel_pulse`, zone à part, reliée à Center-Town par une porte, comme Lower-Town. Sortie sud vers `c_sud`.

**[proposition]** 48 x 36 m, cases de 2 m (24 colonnes x 18 rangées). x vers l'est, z vers le sud, comme `CHINA_LAKE_POSITIONS.md`. Nord = haut du cadre (tours, Arcadius Center au fond).

```
   col 0         6           12          18        23
r0  T T T T T T [ A R C A D I U S   C E N T E R ] T T
r1  T T T T T T [ A A A A A A A A A A A A ] T T T T T
r2  T T . . . . . . . . P P . . . . . . . . . . T T
r3  H H . . c . . . . . . . . . . . . c . . . . K K
r4  H H . . . . E E E E E E E E E E . . . . . . K K
r5  H H . . . . E E E E E E E E E E . . . . . . K K
r6  . . . . . . . . . . . . . . . . . . . . . . . >  sortie est : Fréquence Strip
r7  < . . . . . . . . . . o o . . . . . . . . . . .
r8  < . . . . . . . . . o O O o . . . . . . . . . .   sortie ouest : porte vers Center-Town (rue d'arrivée, Dôme Fréquence)
r9  . . . . . . . . . . o O O o . . . . . . . . . .
r10 . . B B . . . . . . . o o . . . . . . . M M . .
r11 . . B B . . . . . . . . . . . . . . . . M M . .
r12 G G . . . . . . c . . . . . . . . c . . . . S S
r13 G G . . . . . . . . . . . . . . . . . . . . S S
r14 G G . . . . . . . . . . . . . . . . . . . . S S
r15 . . . . . . . . . . . v v . . . . . . . . . . .
r16 . . . . . . . . . . . v v . . . . . . . . . . .
r17 . . . . . . . . . . . V V . . . . . . . . . . .   sortie sud : grille c_sud
```
Légende : T tours de fond ; A Arcadius Center (non visitable) ; P portique de contrôle de l'Arcadius ; E écran géant du Feed 24/7 ; O socle de la projection Holo-Tron, o rambarde du socle ; H billboard HCM-88X ; K kiosque merch officiel ; B bancs ; M distributeur « sourire calibré » ; G guérite SMPD ; S stand de nouilles ; c caméra C.A.G.E. ; v, V escalier vers la grille `c_sud` ; < > sorties.

Repères en mètres (centre des cases) :
| id | élément | cases | x, z (m) | visitable |
|---|---|---|---|---|
| pp_arcadius | façade de l'Arcadius Center | c6-17, r0-1 | 12-36, 0-4 | non |
| pp_portique | portique IO | c10-11, r2 | 20-24, 4-6 | non, monte le Repérage |
| pp_ecran_feed | écran géant Feed 24/7 | c6-15, r4-5 | 12-32, 8-12 | non |
| pp_holo | socle Holo-Tron | c10-13, r7-10 | 20-28, 14-22 | non, pleine au centre |
| pp_billboard | billboard HCM-88X | c0-1, r3-5 | 0-4, 6-12 | non |
| pp_kiosque | kiosque merch | c22-23, r3-5 | 44-48, 6-12 | oui (marchand) |
| pp_guerite | guérite SMPD | c0-1, r12-14 | 0-4, 24-30 | non |
| pp_nouilles | stand de nouilles | c22-23, r12-14 | 44-48, 24-30 | oui (marchand) |
| pp_distrib | distributeur | c20-21, r10-11 | 40-44, 20-24 | oui (objet) |
| pp_bancs | bancs | c2-3, r10-11 | 4-8, 20-24 | non |
| caméras | C.A.G.E. | (4,3) (17,3) (8,12) (17,12) | (9,7) (35,7) (17,25) (35,25) | non |
Jonctions : ouest (r7-8), **porte vers Center-Town** [décision], à traiter comme la porte de Lower-Town ; sud (c11-12), **sortie vers `c_sud`** [décision], la grille où arrive le monte-charge de la Sous-Ville ; est (r6) vers Fréquence Strip [proposition].

Assets : `assets/steel/pulse_plaza/`, index `assets/steel/pulse_plaza/manifest.json` (placeholders, voir `ASSETS.md`).

## Bâtiments et mobilier [proposition sauf mention]
- **Arcadius Center** [canon pour l'existence] : la façade ferme le nord. Verre noir, structure blanche, aucun violet. Logo IO. Entrée gardée, fermée.
- **Écran du Feed 24/7** [canon pour l'écran] : mur d'écrans incurvé sur pieds. Boucle d'images : clip de Vibes, démarrage « GROOVY-TRON.EXE », titre « L'idole démasquée. Qui est vraiment Groovy Vibes ? », bandeau « 100% connection stable. Jusqu'à la prochaine alerte. », puis « Audience sync » (la foule applaudit).
- **Socle Holo-Tron** [canon pour la projection] : disque chromé, Groovy-Tron en hologramme à taille double, qui tourne lentement. C'est une image, il ne réagit pas au joueur.
- **Billboard HCM-88X** [canon] : Vibes en visuel, « Status : Optimum. Le sourire est une mise à jour. »
- **Kiosque merch officiel** : vitrine Human Corp, produits du site (casquette pixel, stickers holo, pack EXE, poster Error 404).
- **Distributeur « sourire calibré »** : borne qui vend des passes pour la soirée Next Drop du Club Neon-7.
- **Guérite SMPD** et **caméras C.A.G.E.** : relient la place au système de Repérage du plan (0 à 3).
- **Stand de nouilles** : seul coin sans écran, lumière chaude, zone aveugle des caméras (le Repérage y baisse).
- **Foule** : 10 à 14 figurants non interactifs autour de l'écran, animation commune d'applaudissement.

## PNJ [proposition]
Clé de sprite `gen_pp_<id>`. Aucun d'eux n'est Vibes ni Tron, aucun ne cite d'identité civile.

1. **Maëlle, fan au premier rang** (`gen_pp_maelle`, 1,64 m, augmentée). Casquette pixel, sticker cœur sur la joue. Près de l'écran (16 ; 13).
   - « Tu l'as vue hier, sur le feed ? Elle a regardé la caméra une demi-seconde de trop. Moi j'appelle ça un message. »
   - « Personne ne sait qui elle est vraiment. Et franchement, je préfère. Si on savait, elle serait comme nous. »
   - Si Repérage à 2 : « Souris un peu. Ici, ceux qui ne sourient pas, on les remarque. »
2. **Dorian, vendeur du kiosque** (`gen_pp_dorian`, 1,78 m). Gilet Human Corp blanc. Kiosque (45 ; 9). Marchand.
   - « Pack EXE, la clé chrome est vide, mais c'est la vraie. C'est écrit sur la boîte. »
   - « Le poster Error 404 part mieux que tout le reste. Les gens aiment bien qu'on leur dise qu'ils sont introuvables. »
3. **Agente Brisset, SMPD** (`gen_pp_brisset`, 1,80 m, cyborg). Guérite (4 ; 26).
   - « Implant, s'il vous plaît. Simple routine. Ici, tout est simple routine. »
   - Clandestin : « Je ne vous lis pas. Ça arrive, un implant fatigué. Ne restez pas sur la place, d'accord ? »
4. **Oncle Pham, stand de nouilles** (`gen_pp_pham`, 1,62 m, humain avec implant). Stand (45 ; 27). Marchand, zone aveugle.
   - « Assieds-toi de ce côté. La caméra du coin voit tout sauf mes casseroles. »
   - « Moi, la musique, je ne l'entends plus. Je ne remarque que quand elle s'arrête. Là, je regarde l'écran. »
5. **Isaure, technicienne de l'écran** (`gen_pp_isaure`, 1,70 m). Harnais, tablette. Sous l'écran (24 ; 12).
   - « L'audience sync, c'est un signal. Il part de l'écran et les implants font le reste. Les mains suivent. »
   - « Tu crois qu'ils applaudissent parce qu'ils veulent ? Moi, ça fait trois ans que je ne pose plus la question. »
6. **Le Clone 7, androïde de série GT** (`gen_pp_clone_gt`, 1,85 m). Chrome, sans visage, posté près du socle (22 ; 22). Proposition déjà notée dans `GROOVY_CREW.md` : modèle vendu par Human Corp, pas Groovy-Tron.
   - « Bonsoir. Je suis un modèle de démonstration. On me pose ici pour que vous voyiez à quoi ressemble un modèle réussi. »
   - Si le joueur insiste : « Question non prévue. Je vous renvoie au refrain. »
7. **Gaspard, chroniqueur de rumeurs** (`gen_pp_gaspard`, 1,72 m). Long manteau, micro de poche. Sur les bancs (6 ; 22).
   - « Chaque semaine quelqu'un jure avoir trouvé qui elle est. Chaque semaine le feed passe à autre chose. Drôle de hasard. »
   - « Si un jour tu entends son vrai nom, garde-le pour toi. Les gens qui le disent trop fort ne reviennent plus sur la place. »
8. **Noor, ado qui sèche** (`gen_pp_noor`, 1,58 m, humaine sans implant, clandestine). Capuche, hoodie « Live Rain » trop grand. Près de l'escalier sud (26 ; 31).
   - « Pas d'implant, pas d'applaudissement. Du coup on me regarde. C'est bête, non ? »
   - « Disconnected, c'est ma chanson. Hors réseau, encore trop réelle. Elle l'a écrite pour des gens comme moi, je le sais. »
   - Indice : « Si tu veux descendre sans passer devant la guérite, l'escalier de service ne ferme jamais vraiment. »
9. **Monsieur Vasseur, employé de l'Arcadius** (`gen_pp_vasseur`, 1,76 m, augmenté). Costume gris, badge IO. Près du portique (22 ; 7).
   - « Je travaille juste là. Non, je ne sais pas ce qu'on y fait. Je sais seulement ce que je fais, moi. »
   - « L'écran ? C'est nous qui louons la place. Le groupe chante, nous on comptera les mains. »

## Concept arts
Dans `concepts/` : `maquette_pulse_plaza_a.jpg` et `maquette_pulse_plaza_iso.jpg`. Ce sont des **maquettes générées**, des références d'ambiance, **pas des captures du jeu**. Elles ne fixent ni le plan ni les positions.


## Bâtiments complets (3/4)

Statut : **proposition d'Ocre**, à poser par Rivet. Même méthode que les `fs_*_3q` du Strip et les `ar_*_3q` de l'Arena (`7e5478b`, posée en `da2c189`). Valentin a rejeté les façades plates : chaque bâtiment est un seul sprite en 3/4 (façade + retour + toit peints ensemble), plus des calques additifs de même taille et même ancre.

Pour Pulse Plaza, le décor doit **réagir au rythme** de la playlist commune (Center-Town / Strip / Pulse / Arena). En plus de `_3q_neon` et `_3q_fenetres` (déjà lus par `view.js`), ce lot ajoute `_3q_ecran` (panneaux / zone écran) et `_3q_pulse` (bandes, balises, projecteurs) à brancher côté code sur le beat.

Les murets sud/est (`pp_muret*`), lampadaires, bancs, caméras, statues, jardinieres, Holo-Tron et écrans hauts `pp_ecran_haut_*` **restent**. Les façades plates `pp_facade_*` et les stands plats sont remplacés à la pose par les `*_3q` (clés anciennes conservées, non modifiées).

### Géométrie
- 50 px/m ; façade rue (face x) = W × 41,21 px ; retour (face z) = D × 28,32 px ; pentes 0,33 / 0,70.
- Ancre au pied du coin avant sud-est `(x+W ; z+D)`.
- Emprises en multiples de 4 m, profondeur min 4 m (les façades nord/ouest passent de 1,5–2 m à 4 m).
- Palette : anthracite + ambre / blanc chaud + accents violet/magenta/cyan (réfs de direction seulement : `nml-refs/pulse_plaza/pulse_a.png`, `pulse_b.png`). Éviter une place uniformément violette.

### Tableau

| clé `_3q` | remplace | enseigne | px | ancre | emprise | h (m) | pose | calques |
|---|---|---|---|---|---|---|---|---|
| `pp_kiosque_3q` | pp_kiosque (4×6) | « Merch officiel » | 282 × 312 | [167, 310] | 4 × 4 m | 4,0 | `B('pp_kiosque', 'Kiosque merch officiel', 'pp_kiosque_3q', 44, 8, 4, 4)` | `_neon`, `_fenetres` |
| `pp_guerite_3q` | pp_guerite (4×6) | « SMPD » | 282 × 273 | [167, 271] | 4 × 4 m | 3,5 | `B('pp_guerite', 'Guérite SMPD', 'pp_guerite_3q', 0, 28, 4, 4)` | `_neon`, `_fenetres`, `_pulse` |
| `pp_nouilles_3q` | pp_nouilles (4×6) | « Nouilles » | 282 × 256 | [167, 254] | 4 × 4 m | 3,2 | `B('pp_nouilles', 'Stand de nouilles', 'pp_nouilles_3q', 44, 28, 4, 4)` | `_neon`, `_fenetres` |
| `pp_billboard_3q` | pp_billboard (4×6) | « HCM-88X » | 282 × 518 | [167, 516] | 4 × 4 m | 7,0 | `B('pp_billboard', 'Billboard HCM-88X', 'pp_billboard_3q', 0, 8, 4, 4)` | `_neon`, `_ecran`, `_pulse` |
| `pp_portique_3q` | pp_portique (4×2) | « Contrôle IO » | 282 × 313 | [167, 311] | 4 × 4 m | 4,0 | `B('pp_portique', 'Portique IO', 'pp_portique_3q', 20, 0, 4, 4)` | `_neon`, `_fenetres`, `_pulse` |
| `pp_distrib_3q` | pp_distrib (2×2) | « sourire calibré » | 282 × 305 | [167, 303] | 4 × 4 m | 2,8 | `B('pp_distrib', 'Distributeur « sourire calibré »', 'pp_distrib_3q', 40, 20, 4, 4)` | `_neon`, `_ecran`, `_pulse` |
| `pp_kiosque_presse_3q` | pp_kiosque_presse (2×2) | « Holo-presse » | 282 × 242 | [167, 240] | 4 × 4 m | 3,0 | `B('pp_kiosque_presse', 'Kiosque presse', 'pp_kiosque_presse_3q', 8, 28, 4, 4)` | `_neon`, `_fenetres`, `_ecran` |
| `pp_kiosque_boissons_3q` | pp_kiosque_boissons (2×2) | « Hydratation » | 282 × 252 | [167, 250] | 4 × 4 m | 3,0 | `B('pp_kiosque_boissons', 'Kiosque boissons', 'pp_kiosque_boissons_3q', 36, 28, 4, 4)` | `_neon`, `_fenetres` |
| `pp_nord_a_3q` | pp_facade_a (16×2) | « Pulse » | 776 × 708 | [661, 706] | 16 × 4 m | 10,0 | `B('pp_fac_n2', '', 'pp_nord_a_3q', 12, -4, 16, 4, { named: false })` | `_neon`, `_fenetres`, `_ecran`, `_pulse` |
| `pp_nord_b_3q` | pp_facade_b (8×1,5) | « Lounge » | 447 × 571 | [332, 569] | 8 × 4 m | 8,0 | `B('pp_fac_n4', '', 'pp_nord_b_3q', 28, -4, 8, 4, { named: false })` | `_neon`, `_fenetres`, `_pulse` |
| `pp_nord_c_3q` | — | — | — | — *(obsolete)* |
| `pp_nord_c2_3q` | fixe (Résidences du Pulse, ambre) | vacillement ambre | égaliseur : sync kick | bandes violettes : pulse kick |
| `pp_nord_c3_3q` | fixe (Arcades Nord) | vacillement ambre | égaliseur : sync kick déphasé | bandes violettes : pulse 1/2 kick |
| `pp_nord_c2_3q` | pp_nord_c_3q (x 0) | « Résidences du Pulse » | 611 × 748 | [496, 746] | 12 × 4 m | 10 | `B('pp_fac_n1', '', 'pp_nord_c2_3q', 0, -4, 12, 4, { named: false })` | `_neon`, `_fenetres`, `_ecran`, `_pulse` |
| `pp_nord_c3_3q` | pp_nord_c_3q (x 36) | « Arcades Nord » | 611 × 692 | [496, 690] | 12 × 4 m | 10 | `B('pp_fac_n3', '', 'pp_nord_c3_3q', 36, -4, 12, 4, { named: false })` | `_neon`, `_fenetres`, `_ecran`, `_pulse` |
| `pp_ouest_a_3q` | pp_facade_a_o (2×12) | « *(sans enseigne)* » | 509 × 674 | [167, 672] | 4 × 12 m | 10,0 | `B('pp_fac_o1', '', 'pp_ouest_a_3q', -4, 0, 4, 12, { named: false })` | `_fenetres`, `_ecran`, `_pulse` |
| `pp_ouest_b_3q` | pp_facade_b_o2 (1,5×8) | « *(sans enseigne)* » | 396 × 576 | [167, 573] | 4 × 8 m | 8,0 | `B('pp_fac_o2', '', 'pp_ouest_b_3q', -4, 16, 4, 8, { named: false }) (+ `pp_fac_o3` en z 24)` | `_fenetres`, `_pulse` |
| `pp_ecran_feed_3q` | pp_ecran_feed | « Feed 24/7 » | 941 × 672 | [826, 670] | 20 × 4 m | 8,0 | `B('pp_ecran_feed', 'Écran du Feed 24/7', 'pp_ecran_feed_3q', 12, 8, 20, 4, { sign: true, ecran: ECRAN_FEED })` | `_neon`, `_ecran`, `_pulse` |

### Calques rythmiques (effets conseillés)

| bâtiment | `_neon` | `_fenetres` | `_ecran` | `_pulse` |
|---|---|---|---|---|
| `pp_kiosque_3q` | fixe (enseigne MERCH OFFICIEL) | vacillement lent ambre (hors plafond mobile) | — | — |
| `pp_guerite_3q` | fixe (SMPD, blanc IO) | vacillement lent froid | — | balise toit : clignote lent hors beat ; voyants rouges discrets |
| `pp_nouilles_3q` | fixe ou grésillement très léger (ambre) | flicker ambre chaud (seul coin sans écran) | — | — |
| `pp_billboard_3q` | fixe (logo HCM-88X) | — | pages du feed / portrait Vibes — période ~9 s, sync possible avec ECRAN_FEED | projecteurs de base : pulse sur le kick (période = 60/BPM, ~170 BPM → 0,35 s) |
| `pp_portique_3q` | fixe (CONTRÔLE IO) | glow scanner cyan, vacillement lent | — | voyants verts : pulse court sur le beat (audience sync) |
| `pp_distrib_3q` | pulse lent magenta | — | sourire calibré : pulse sur le kick | bandes d’angle : balayage vertical 1 tour / 2 mesures |
| `pp_kiosque_presse_3q` | fixe (HOLO-PRESSE, cyan) | vacillement ambre comptoir | affiche Groovy Vibes : change avec le feed (période 11 s) | — |
| `pp_kiosque_boissons_3q` | fixe (HYDRATATION) | vacillement cyan des frigos | — | — |
| `pp_nord_a_3q` | pulse lent (PULSE) | vacillement ambre étages | égaliseur façade : réagit au mid (pas au kick) — budget 1 calque | bandes verticales violettes : pulse sur le kick, déphasage par travée |
| `pp_nord_b_3q` | fixe (LOUNGE) | vacillement ambre | — | bandes magenta : pulse doux 1/2 kick |
| `pp_nord_c_3q` | — | vacillement ambre / blanc chaud | bande visualizer : sync kick | filets verticaux : balayage sur la mesure |
| `pp_ouest_a_3q` | — | vacillement ambre | écran égaliseur : sync kick | bandes violettes : pulse kick, décalé vs nord |
| `pp_ouest_b_3q` | — | vacillement ambre léger | — | liserés cyan des baies : pulse 1/2 kick |
| `pp_ecran_feed_3q` | fixe (FEED 24/7) | — | zone vide : contenu dessiné par le code (ECRAN_FEED) — opacity pulse léger sur Audience sync | filets magentas du cadre + tirets cyan : pulse fort sur le kick ; budget prioritaire |

### Budget d'animation mobile (proposition)
- `view.js` charge déjà `*_neon` et `*_fenetres` hors plafond `animStats.on` (8).
- **Nouveaux** `*_ecran` et `*_pulse` : à brancher comme les enseignes (additif, une couleur/opacité par image). Compter dans `animStats.enseignes` ou une catégorie `pulse`.
- Sur mobile : garder actifs en priorité `pp_ecran_feed_3q_pulse`, `pp_nord_a_3q_pulse`, `pp_billboard_3q_ecran` ; les autres `_pulse` / `_ecran` peuvent tomber en fixe si `animStats` dépasse.
- BPM cible playlist commune ~170 : période kick ≈ 0,35 s ; ne pas animer plus d'un calque « fort » par bâtiment.

### À faire côté code (Rivet)
1. Remplacer les sprites plats des stands et les façades `pp_facade_*` / `pp_facade_*_o` par les appels `B(...)` du tableau (emprises en multiples de 4 m, profondeur min 4 m).
2. Nord : fronts à z 0 (emprise z −4→0). Ouest : fronts à x 0 (emprise x −4→0) ; **laisser libre** l'accès ouest z 12–16.
3. `*_neon` / `*_fenetres` : chargement auto actuel dès que `b.sprite` vaut `<clé>_3q`.
4. Brancher `*_ecran` et `*_pulse` (additif, effets du tableau) ; pour `pp_ecran_feed_3q`, conserver `ECRAN_FEED` — mettre à jour `ecran_coins` d'après le manifeste si besoin.
5. Recaler PNJ / figurants / lueurs autour des nouvelles emprises 4×4 (stands) et des bords 4 m de profondeur.
6. Vérifier les trois accès (ouest, Strip, escalier sud) : aucun écran ni emprise ne doit les gêner.


### Correctif nord_c / billboard (suite)
- `pp_nord_c_3q` et ses calques sont `"obsolete": true` (texte parasite « 2175 cyberpunk Pulse Plaza », trop violet).
- Poser `pp_nord_c2_3q` en x 0 (« Résidences du Pulse », façade ambre dominante) et `pp_nord_c3_3q` en x 36 (« Arcades Nord », variante non clonée).
- Billboard : préférer le calque `pp_billboard_3q_neon2` (cadre violet + textes renforcés) à la place de `pp_billboard_3q_neon` trop faible ; même taille et même ancre. En `loc.enseignes` : `{ building: 'pp_billboard', neon: 'pp_billboard_3q_neon2', effet: 'fixe' }`.

### Planches
- `/workspace/nml-shots/pulse_3q.png` (maquette iso de la place avec les 14 bâtiments espacés comme en jeu, pas une capture)
- `/workspace/nml-shots/pulse_3q_zoom.png` (gros plan 1:1 de 4 bâtiments avec calques)

## Playlist OST commune (`fecc483`, `src/core/ost_centre.js`)
- Playlist commune Groovy Crew posée sur `main` (4 titres MP3 `assets/audio/ost_centre/`, pack `fecc483`) et partagée en singleton entre Center-Town, Fréquence Strip, Pulse Plaza et Steel Arena (aucune coupure ni remise à zéro aux changements de zone). L'API Web Audio `window.__nml.ostCentre` (`beat`, `energy`, `bass`, `mid`, `high`, `kick`, `onKick`) est exposée sur cette même lecture pour piloter les calques `_3q_ecran` et `_3q_pulse`.
