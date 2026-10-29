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

## Concept art
`concepts/maquette_frequence_strip_iso.jpg` : **maquette générée**, référence d'ambiance, **pas une capture du jeu**.
