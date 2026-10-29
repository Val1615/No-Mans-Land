# Dôme Fréquence (Center-Town, dalle de Steel-Mégalopolis)

Pack créatif d'Ocre, même méthode que la Steel Arena. Légende : **[canon]** = site Groovy Crew ou roman ; **[décision]** = consigne de Valentin ou du développeur ; **[proposition]** = idée d'Ocre, à valider.
Sources : `GROOVY_CREW.md` et `CENTER_TOWN_LIEUX.md` (branche creation/groovy-crew), `src/data/buildings_steel.js` (lu, non modifié), `docs/villes/STEEL_MEGALOPOLIS_PLAN.md`, `docs/CANON_ARBITRAGES.md`.

## Ce qui est fixé
- **[canon]** Le Dôme Fréquence est une salle de concert de la tournée : le groupe y a joué le 11/10.
- **[décision]** (Valentin, 29/10) Le bâtiment à dôme couvert d'écrans de Center-Town, ex-« Rotonde », est le Dôme Fréquence. Il est dans la rue d'arrivée, fermé au joueur pour l'instant.
- **[décision]** En jeu, c'est déjà le bâtiment `c_tour` de la zone Center-Town (`steel_center`), sprite `b_st_ct_dome`, emprise x 16-31, z 1-13, non visitable.
- **[décision]** Zone `steel_dome`.
- **[décision]** Vibes et Tron ne paraissent que sur des écrans. Aucun visage inventé sur les écrans : seulement Vibes, Tron, ou des silhouettes de foule.
- **[décision]** Le nom civil de Vibes n'apparaît jamais.
- **[décision]** Plafond de 8 animations visibles à la fois sur mobile. Aucun faisceau ni effet peint dans une image si le code l'anime aussi.

## Raccordement [proposition]
Le Dôme ne s'ouvre pas sur une nouvelle rue : c'est un bâtiment de la rue d'arrivée. Le plus cohérent avec `CENTER_TOWN_LIEUX.md` et le code est donc d'en faire **l'intérieur de `c_tour`** :
- `steel_dome` est une zone intérieure, reliée à `steel_center` par la porte de façade du Dôme, au milieu du côté sud de son emprise, vers (23,5 ; 13).
- La porte reste fermée tant que le Dôme est fermé au joueur [décision] ; quand elle s'ouvrira, `c_tour` passera `visitable: true`.
- Aucun lien direct avec Pulse Plaza, le Strip ou l'Arena : on y entre et on en sort par la rue d'arrivée.
- Les écrans de façade (Vibes et Tron) sont fournis ici comme enseignes animées à poser sur `b_st_ct_dome`, dans la zone `steel_center`.

## Ambiance [proposition]
**Lumière.** Dehors, la rotonde est couverte d'écrans violets. Dedans, tout vient d'en haut : la verrière du dôme laisse tomber une lumière ambrée et froide à la fois, comme un ciel qui n'existe pas. Le foyer est sombre, marbre noir et laiton, avec le bar en ambre. La salle est ronde, en gradins, la scène au nord sous deux écrans géants.

**Palette.**
| Rôle | Couleur | Hex |
|---|---|---|
| fond | bleu nuit | `#060a10` |
| marbre du foyer | noir veiné | `#15121a` |
| laiton | laiton | `#b8893c` |
| verrière | ambre pâle | `#f0c27a` |
| écrans, moquette | violet | `#8a3cff` |
| lumières de scène | magenta et cyan | `#e03ca8` / `#5fd3f0` |

**Sons.** Le foyer étouffe tout : verres, pas sur la moquette, une sono d'ambiance très basse. Dans la salle, l'écho de la coupole, des balances qui reprennent la même mesure, la voix d'un technicien dans un micro. Quand les lumières de scène s'allument, un souffle électrique.

**Musique.** Le Dôme est la salle « propre » de Human Corp : on y joue les versions les plus lisses du répertoire. Extraits (canon) : « First Signal, First Light », « AUTHENTIC™ », « CGU ».

## Plan de la zone [proposition]
Zone `steel_dome`, 30 x 30 m, cases de 2 m (15 x 15). x vers l'est, z vers le sud. Entrée au sud, scène au nord.

```
    col 0       7        14
r0  . . . . E E E E E E . . . . .
r1  . . . S S S S S S S S S . . .
r2  . . . S S S S S S S S S . . .
r3  . . k . . . . . . . . . k . .
r4  . . . g g g g g g g g g . . .
r5  . . . g g g g g g g g g . . .
r6  . . . g g g g g g g g g . . .
r7  . . . g g g g R R g g g . . .
r8  . . . g g g g R R g g g . . .
r9  . c . . . . . . . . . . . c .
r10 # # # # # # D D D # # # # # #
r11 . . B B B . . . . . V V V . .
r12 . . . . . . . . . . . . . . .
r13 . . . n . . . p . . . n . . .
r14 . . . . . . P P P . . . . . .   sortie sud : porte du Dôme vers steel_center
```
Légende : E écrans de scène (Vibes à gauche, Tron à droite) ; S scène ; k enceintes ; g gradins ; R régie et console ; c colonnes ; # cloison entre salle et foyer ; D portes de la salle ; B bar du foyer ; V vestiaire ; n banquettes ; p borne de contrôle des billets ; P porte de façade.
Au-dessus de la salle (r1-r9), la verrière : un calque au plafond, vu en transparence.

Repères (m) :
| id | élément | cases | x, z (m) | visitable |
|---|---|---|---|---|
| df_scene | scène | c3-11, r1-2 | 6-24, 2-6 | non |
| df_ecrans | écrans de scène | c4-9, r0 | 8-20, 0-2 | non |
| df_gradins | gradins | c3-11, r4-8 | 6-24, 8-18 | non |
| df_regie | régie | c7-8, r7-8 | 14-18, 14-18 | non |
| df_bar | bar du foyer | c2-4, r11 | 4-10, 22-24 | oui (marchand) |
| df_vestiaire | vestiaire | c10-12, r11 | 20-26, 22-24 | oui |
| df_borne | borne de billets | c7, r13 | 14-16, 26-28 | non |
| df_porte | porte vers steel_center | c6-8, r14 | 12-18, 28-30 | jonction |

## Mobilier et décor [proposition]
- **Scène** : plateau noir à bord laiton, deux écrans géants au-dessus. Les lumières de scène sont une enseigne animée à part, rien n'est peint sur la scène.
- **Verrière** : coupole de verre en losanges, lumière ambre animée à part (calque de plafond).
- **Gradins** en arc, moquette violette, rambardes laiton.
- **Régie** : console, écrans de contrôle, VU-mètres animés à part.
- **Foyer** : bar en laiton et ambre, vestiaire, banquettes en velours, colonnes, borne Human Corp.

## PNJ [proposition]
Clé de sprite `gen_df_<id>`. Aucun d'eux n'est Vibes ni Tron, aucun ne cite d'identité civile.

1. **Mme Varenne, directrice du Dôme** (`gen_df_varenne`, 1,72 m, augmentée). Tailleur blanc Human Corp. Foyer (15 ; 24).
   - « Ici, nous ne faisons pas de bruit. Nous faisons de la musique validée. »
   - « Le 11, la salle était pleine à cent deux pour cent. Les deux pour cent restants, c'était la sécurité qui chantait. »
2. **Octave, régisseur de salle** (`gen_df_octave`, 1,78 m). Casque, lampe frontale. À la régie (16 ; 16).
   - « On refait les balances tous les soirs, même quand il n'y a personne. La salle doit sonner comme sur l'enregistrement. »
   - « Les voix sur l'écran sont parfaites. Ce sont les applaudissements qui me demandent le plus de travail. »
3. **Jade, barmaid** (`gen_df_jade`, 1,66 m). Gilet laiton, cheveux courts. Bar (7 ; 23). Marchande.
   - « Le cocktail du moment s'appelle HeartSync. Il a le même goût que le précédent, mais en violet. »
   - « Les gens viennent ici pour dire qu'ils sont venus. Ils regardent l'écran plus que la scène. »
4. **Nils, vestiairiste** (`gen_df_nils`, 1,70 m). Vieux costume de service, gants blancs. Vestiaire (23 ; 23).
   - « J'ai un ticket pour chaque manteau. Pour les gens, on n'a pas de ticket. »
   - « Une fois, quelqu'un a oublié une veste ici, avec un badge du groupe dedans. Le lendemain, la veste avait disparu, et le badge aussi. »
5. **Pia, technicienne lumière** (`gen_df_pia`, 1,64 m). Harnais, gants, tablette lumineuse. Bord de scène (22 ; 7).
   - « Je règle les lumières pour une scène qui joue surtout sur écran. Mes projecteurs éclairent des gens qui ne sont pas là. »
6. **Ruben, agent de sécurité** (`gen_df_ruben`, 1,88 m, cyborg). Uniforme gris Human Corp. Borne de billets (15 ; 27).
   - « Le Dôme est fermé ce soir. Il est fermé presque tous les soirs. C'est ce qui le rend désirable. »
   - Si Repérage à 2 : « Vous étiez déjà venu hier. La borne s'en souvient, moi aussi. »
7. **Hélène, critique musicale** (`gen_df_helene`, 1,68 m). Manteau long, carnet papier. Banquette ouest (7 ; 27).
   - « J'écris sur leurs disques depuis le début. Je n'ai jamais réussi à savoir qui écrit vraiment les paroles. »
   - « Le meilleur morceau de l'album, c'est celui qu'on ne passe jamais ici. Devine lequel. »
8. **Le Gardien des balcons** (`gen_df_gardien`, 1,60 m, âgé). Ancien ouvreur de la Rotonde. Près des colonnes (3 ; 19).
   - « Avant, ça s'appelait la Rotonde. On y jouait de l'orgue. L'orgue est toujours sous la scène, personne n'a pensé à l'enlever. »
   - « Le dôme ne laisse pas passer le ciel. Il le montre. Ce n'est pas pareil. »

## Concepts
Dans `concepts/` : deux **maquettes générées**, références d'ambiance, **pas des captures du jeu**.
