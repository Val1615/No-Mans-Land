# Steel Arena (Center-Town, dalle de Steel-Mégalopolis)

Pack créatif d'Ocre, même méthode que Pulse Plaza et Fréquence Strip. Légende : **[canon]** = site Groovy Crew ou roman ; **[décision]** = consigne de Valentin ou du développeur ; **[proposition]** = idée d'Ocre, à valider.
Sources : `GROOVY_CREW.md`, `CENTER_TOWN_LIEUX.md` (branche creation/groovy-crew), `frequence_strip/FREQUENCE_STRIP.md` (branche creation/frequence-strip), `docs/villes/STEEL_MEGALOPOLIS_PLAN.md`, `docs/CANON_ARBITRAGES.md`.

## Ce qui est fixé
- **[canon]** Steel-Mégalopolis Arena (site) : « Le dôme. Les spots. Human Corp sponsorise le sourire. » « Live tonight. » Images de réf. du site : concert, Vibes en scène à l'Arena.
- **[canon]** Sur la même page du site : « Building a better tomorrow. Tous les rythmes appartiennent à Human Corp. », billboard HCM-88X, projection GT (« Beat. Circuit. Command. Le showman ne cligne pas. ») et le panneau « Au-delà de ce point : pas de droits, pas de loi, pas de retour ».
- **[canon]** Festival Pulse of Steel, le 14/11 (tournée).
- **[décision]** Zone `steel_arena`, reliée à la grille du bout est du Fréquence Strip (`fs_grille_est`), qui sera ouverte plus tard.
- **[décision]** Vibes et Tron ne paraissent que sur des écrans. Personne ne les rencontre, aucun sosie ne parle à leur place.
- **[décision]** Le nom civil de Vibes n'apparaît jamais.
- **[décision]** Plafond de 8 enseignes animées visibles à la fois sur mobile.

## Ambiance [proposition]
**Lumière.** Le dôme noir occupe tout le nord, ceinturé de bandes violettes. Quatre colonnes de projecteurs balaient le plafond du sarcophage en lents arcs cyan, c'est la seule lumière qui monte dans toute la ville. Le parvis est sombre, piqué de flaques de lumière violette sous les lampadaires, avec les lignes de file qui brillent au sol jusqu'aux portiques.

**Palette.**
| Rôle | Couleur | Hex |
|---|---|---|
| fond, nuit | bleu nuit | `#060a10` |
| dôme | noir bleuté | `#11131c` |
| bandes du dôme | violet | `#8a3cff` |
| faisceaux, écrans | cyan | `#5fd3f0` |
| cœurs des fans | magenta | `#e03ca8` |
| Human Corp | blanc cassé | `#e8eef2` |
| sécurité | rouge discret | `#c8323c` |

**Sons.** De l'extérieur, le concert n'est qu'une basse sourde qui fait vibrer les barrières. Rumeur de la file, bips des portiques, annonces Human Corp en voix douce, crissement des faisceaux qui tournent. Toutes les quelques minutes, une clameur venue du dôme couvre tout pendant deux secondes.

**Musique.** Le morceau du soir sort étouffé des murs, filtré dans les graves ; plus on approche des portiques, plus il devient net. Extraits (canon) : « Toujours en ligne », « Drop the Galaxy », « HeartSync ».

## Plan de la zone [proposition]
Zone `steel_arena`, 56 x 40 m, cases de 2 m (28 colonnes x 20 rangées). x vers l'est, z vers le sud.

```
    col 0         8          16         24   27
r0  . P A A A A A A A A A A A A A A A A A A A A A A A A P .
r1  . . A A A A A A A A A A A A A A A A A A A A A A A A . .
r2  . . A A A A A A A A A A A A A A A A A A A A A A A A . .
r3  . . A A A A A A A A A A A A A A A A A A A A A A A A . .
r4  . . A A A A A A A A A A A A A A A A A A A A A A A A . .
r5  . P A A A A A A A A A E E E E A A A A A A A A A A A P .
r6  . . . . . . . . . . . g g g g . . . . . . . . . . . . .
r7  . . . . l . . . . . . f f f f . . . . . . . . l . . . .
r8  . . . . . . . . . . . f f f f . . . . . . . . . . . . .
r9  . . . . . . . . . . . f f f f . . . . . . . . . . . . .
r10 < . . K K . . . . . . f f f f . . . . . . . . M M . . .   entrée ouest : grille est du Strip
r11 < . . K K . . . . . . f f f f . . . . . . . . M M . . .
r12 . . . . . . . . . . . . . . . . . . . . . . . . . . . .
r13 . . . . l . . S S . . . . . . . . . . . . . T T T l . .
r14 . . . . . . . S S . . . . c . . . . . . . . T T T . . .
r15 . . . . . . . . . . . . . . . . . . . . . . . . . . . .
r16 . . . . . . . . . . . . . . . . . . . . . . . . . . . .
r17 . . . . . . . . . . . . . . . . . . . . . . . . . . . .
r18 . . . . . . . . . . . . . . . . . . . . . . . . . N . .
r19 . . . . . . . . . . . . . . . . . . . . . . . . . N . .
```
Légende : A dôme de l'Arena (non visitable) ; E entrée principale et fronton ; g portiques de sécurité ; f file d'attente entre barrières ; P projecteurs de ciel ; K guichets ; M stand de merch officiel ; S poste de sécurité Human Corp ; T camion régie ; N panneau « No Man's Land » ; l lampadaires ; c caméra C.A.G.E. ; < entrée.

Repères (m) :
| id | élément | cases | x, z (m) | visitable |
|---|---|---|---|---|
| ar_arena | dôme de l'Arena | c2-25, r0-5 | 4-52, 0-12 | non |
| ar_entree | entrée et fronton | c11-14, r5 | 22-30, 10-12 | non pour l'instant |
| ar_portiques | portiques | c11-14, r6 | 22-30, 12-14 | non |
| ar_file | barrières de file | c11-14, r7-11 | 22-30, 14-24 | non |
| ar_guichets | guichets | c3-4, r10-11 | 6-10, 20-24 | oui (billets) |
| ar_merch | stand de merch officiel | c23-24, r10-11 | 46-50, 20-24 | oui (marchand) |
| ar_securite | poste Human Corp | c7-8, r13-14 | 14-18, 26-30 | non, monte le Repérage |
| ar_regie | camion régie | c22-24, r13-14 | 44-50, 26-30 | non |
| ar_panneau | panneau « No Man's Land » | c25, r18-19 | 50-52, 36-40 | non |
| projecteurs | 4 | (1,0) (26,0) (1,5) (26,5) | (3,1) (53,1) (3,11) (53,11) | non |
| lampadaires | 4 | (4,7) (23,7) (4,13) (24,13) | | non |
Jonctions : ouest (c0, r10-11) vers `fs_grille_est` du Strip [décision], fermée tant que la grille n'est pas ouverte. Pas d'autre sortie pour l'instant [proposition].

## Bâtiments [proposition sauf mention]
- **Le dôme** [canon pour l'existence] : coque noire à nervures, bandes violettes, deux grands écrans en façade (Vibes à l'ouest, Tron à l'est), fronton lumineux sans texte au-dessus de l'entrée. Le nom est affiché par le code.
- **Projecteurs de ciel** [canon : « les spots »] : tours trapues, faisceaux cyan animés.
- **Portiques et file** : portiques blancs Human Corp, barrières chromées, lignes de file lumineuses au sol.
- **Guichets** : cabine vitrée, écran animé du prochain concert.
- **Stand de merch officiel** : vitrine Human Corp, produits du site.
- **Poste de sécurité Human Corp**, **camion régie** (antennes, câbles vers le dôme).
- **Panneau « No Man's Land »** [canon pour la phrase] : panneau métallique en pictogramme, la phrase est affichée par le code quand on l'examine.

## PNJ [proposition]
Clé de sprite `gen_ar_<id>`. Aucun d'eux n'est Vibes ni Tron, aucun ne cite d'identité civile.

1. **Ferrand, vigile Human Corp** (`gen_ar_ferrand`, 1,90 m, cyborg). Uniforme blanc, visière. Aux portiques (26 ; 13).
   - « Billet, implant, sourire. Dans cet ordre, s'il vous plaît. »
   - Clandestin : « Vous n'êtes pas dans la liste. Personne n'est pas dans la liste. Reculez. »
2. **Anouk, guichetière** (`gen_ar_anouk`, 1,64 m). Gilet Human Corp, casque micro. Guichets (8 ; 22). Vend les billets.
   - « Ce soir c'est complet. Demain aussi. Pour le Festival du 14, il reste des places debout derrière les places debout. »
   - « Le prix change selon votre score d'engagement. Ne me demandez pas comment, c'est l'écran qui calcule. »
3. **Zélie, revendeuse de billets** (`gen_ar_zelie`, 1,60 m). Manteau à doublure pleine de poches. Près du lampadaire ouest (9 ; 27).
   - « Vrai billet, vraie puce, faux nom. Ça passe neuf fois sur dix. La dixième, tu cours. »
   - Si Repérage à 2 : « Tu es grillé, toi. Je ne te connais pas. »
4. **Malik, régisseur** (`gen_ar_malik`, 1,80 m). Gilet à poches, tablette, oreillette. Devant le camion régie (45 ; 31).
   - « Trois mille personnes à l'intérieur, et le show tient sur une seule console. Si elle plante, je deviens célèbre. »
   - « Les cris du public sont mixés, comme le reste. Ce soir, on en a ajouté vingt pour cent. »
5. **Inès, fan au cœur lumineux** (`gen_ar_ines`, 1,62 m). Bâton-cœur magenta, joues peintes, hoodie « Live Rain ». Dans la file (24 ; 18).
   - « Je n'ai pas de billet. Je viens pour la file. Ici, au moins, on est ensemble. »
   - « Personne ne sait qui elle est sous le chapeau. Moi je dis qu'elle est comme nous, et qu'elle a juste eu de la chance. Ou pas. »
6. **Clém, journaliste du feed** (`gen_ar_clem`, 1,72 m). Drone-caméra sur l'épaule. Près de l'entrée (31 ; 15).
   - « Je fais le direct de la file. Les gens adorent regarder d'autres gens attendre. »
   - « On m'a demandé de ne pas filmer le panneau du fond. Alors évidemment, tout le monde le filme. »
7. **Agent Garnier, SMPD** (`gen_ar_garnier`, 1,82 m, augmenté). Uniforme bleu. Près du poste de sécurité (18 ; 28).
   - « Ici c'est Human Corp qui garde la porte. Nous, on garde ceux qui restent dehors. »
   - « Le panneau là-bas ? Une blague de mauvais goût. Ou un avertissement. Je ne suis pas payé pour choisir. »
8. **Bastien, technicien des projecteurs** (`gen_ar_bastien`, 1,76 m). Harnais, gants. Au pied du projecteur sud-est (52 ; 12).
   - « Quatre faisceaux, et ils doivent rester synchrones avec la musique. Le jour où ils se décalent, ça fait une prière ratée. »
9. **Madame Laure, ouvreuse retraitée** (`gen_ar_laure`, 1,58 m). Vieux gilet de l'Arena, assise près du panneau (49 ; 37).
   - « J'ai placé des gens ici pendant trente ans. Avant, on voyait les visages des chanteurs. Maintenant on voit les écrans. »
   - « Ce panneau était là avant l'Arena. On a construit autour, et on n'a jamais osé l'enlever. »

## Concept art
`concepts/maquette_steel_arena_iso.jpg` : **maquette générée**, référence d'ambiance, **pas une capture du jeu**.
