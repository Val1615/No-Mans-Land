# Rencontre du jalon 2 : « Le témoin sous les pins » (survivant blessé)

Jalon 2 du chantier (voir [README.md](README.md)), famille **survivant blessé (choix)**, variante du biome de forêt. Création : Ocre, 18/11/2026 (heure de Paris). Même format que [PILOTE.md](PILOTE.md), [CARAVANE.md](CARAVANE.md) et [MUTANTS.md](MUTANTS.md).

> **Écrite sur [`ARCHI.md`](ARCHI.md) et sur le format réel des lots 1 et 2** : format §4, `points`, `entrees`, `dureeSi`, `drapeauArrivee`, `enseignes`. Préfixes `rc_` / `rc_fo_` (modules de la forêt, nouveaux, réutilisables) / `rc_sur_` (propres à cette rencontre) / `g_rc_` / `gen_rc_`, 50 px/m. Scène 32 × 26 m (dans la plage 24 × 24 à 48 × 36), zone de combat 19 × 19 entièrement dedans. Ennemis en positions absolues sur des cases libres, à ≥ 8 m de l'entrée. **Aucun ennemi par défaut** : Roque n'est jamais dans la liste ; Paca n'y entre que si le joueur engage le combat. **Aucune hauteur** : pas de `niveaux`, pas de `y` pour les unités, tout le monde au sol. Journal par case. Drapeaux de scène `sur_*` remis à zéro à la sortie ; drapeaux de monde `monde_roque_*`, `monde_mateo_pris`, `monde_sur_vu` justifiés au §7 et au §13. Examen au toucher sur mobile. Ambiance qui suit l'heure du voyage : courbe `forest` proposée au §11 (repli : `desert`). Liseré de lune existant (50 %, tête et épaules seulement). Une seule lumière artificielle : la lanterne accrochée au pin mort, source visible.
>
> **Sans sprites** : rien n'est produit dans ce lot. Les clés nouvelles sont listées au §10 ; le §15 donnera les poses définitives après production.

Maquette concept (MAQUETTE, pas une capture) : `/workspace/nml-shots/rencontres/survivant_concept.png` sur la machine d'Ocre. Elle montre une vue iso d'ambiance et le plan coté. Le plan coté de ce document fait foi.

**Décisions de lore nouvelles, à signaler à Valentin** (détail au §13). Rien n'est imposé.
1. La forêt occidentale (quatre cases autour du Temple du couchant) est un vrai bois de pins secs, première rencontre du biome `forest`.
2. Le Temple du couchant n'est ici qu'un **repère géographique** : pas de culte nouveau, pas de sanctuaire, pas d'étape de la filière.
3. Trois noms nouveaux : **Roque** (muletier blessé), **Mateo** (son neveu, jeune mutant, **absent** : le Service l'a emmené), **Paca** (charognarde).
4. Le Service patrouille la branche ouest Douane ouest → Station de répartition → Temple, et **entre dans la forêt** (contrairement au verre).
5. Roque menait Mateo vers un contact, à la Station, qui devait le faire passer par la filière de Remedios. Si la filière est refusée, le contact reste « quelqu'un qui les emmène plus au nord ».

## 1. Fiche
| Champ | Valeur |
|---|---|
| id | `survivant_pins` [proposition], préfixe de drapeaux `sur_` |
| Famille | Survivant blessé (choix) |
| Terrains | `foret` (p = 0,10) de `src/data/nml.js` ; taux inchangés. La piste de la maquette ne traverse que **G09** (le Temple, un grand lieu) : les cases de forêt F08, G08 et F09 n'ont pas le terrain `piste`. Pas besoin d'ajouter `piste`. |
| Biome | forêt (`forest` du manifeste) : bois de pins secs à l'ouest, autour du Temple du couchant |
| Cases de référence | **F08 (5,7), G08 (6,7), F09 (5,8)**. On exclut **G09 (6,8)**, case du Temple du couchant. Pour le test : forcée par le mode DEV |
| Moment | l'heure du voyage (lanterne le jour, seule lumière la nuit) |
| Emprise | 32 × 26 m (x vers l'est, z vers le sud, origine au coin nord-ouest), **un seul niveau de marche, au sol** |
| Faction | aucune : un blessé et une charognarde, indépendants |
| Rejouable | non : journal par case, et la rencontre est **unique** : `si` refuse si `monde_sur_vu` (drapeau de monde, jamais purgé) |
| Durée ajoutée | 1 h ; +1 h si Roque a été escorté (`sur_escorte`) |

## 2. Pitch et situation
**Pitch.** Au bord de la piste qui mène au Temple du couchant, un muletier est assis contre un pin foudroyé. Son mulet est mort sur la piste. Une traînée de sang part vers l'est. Quelqu'un regarde, depuis un fourré.

**Situation.** **Roque**, muletier de la Station de répartition, menait son neveu **Mateo**, un jeune mutant, vers un contact qui devait le faire passer plus loin — par la filière de Remedios, si elle est retenue. À l'aube, une patrouille du Service les a rattrapés sous les pins. Ils ont chargé Mateo sur un véhicule, tiré le mulet, et laissé Roque pour mort. Il s'est traîné jusqu'au pin, a allumé sa lanterne, et il n'arrive plus à se lever.

**Paca** est arrivée après. Elle n'a pas fait ça. Elle attend, à une distance polie, que l'homme finisse de mourir, ou que quelqu'un d'autre tranchera.

Le joueur arrive par l'est, depuis la Station. Il peut soigner Roque, lui laisser de l'eau, l'escorter, suivre la traînée, parler à Paca, dépouiller le blessé, ou passer sans s'arrêter. La piste traverse la scène ; la sortie est est **ouverte** dès l'arrivée.

## 3. Ce que le décor raconte
Tout est examinable (clic sur ordinateur ; sur mobile, appui sur le point d'examen, avec un anneau comme les portes ; pas d'examen au survol). Les indices marqués ★ racontent ce qui est arrivé à Mateo.

| Où (x ; z) | Ce qu'on voit | Texte d'examen | Effet |
|---|---|---|---|
| Pin mort (13,5-17,5 ; 9-12,5) | pin foudroyé, écorce éclatée, lanterne accrochée à une branche sud | « Un pin foudroyé, mort depuis des années. Quelqu'un a accroché une lanterne à la branche la plus basse : elle brûle encore. Au pied, côté piste, la terre est piétinée et tachée. » | — |
| Lanterne (15,8 ; 12,2) | lanterne à huile accrochée, verre fuligineux | « Une lanterne de piste, le réservoir à moitié. C'est une vraie flamme. » | source de la seule lumière artificielle (§11) |
| Roque, de loin (15,8 ; 12,8) | un homme assis contre le tronc, la jambe gauche entourée d'un chiffon | de loin : « Un homme assis contre le pin. Il ne se lève pas. » ; à 3 m : le dialogue de Roque s'ouvre | — |
| Mulet (20,2-22,6 ; 16-17,3) | mulet mort, harnais encore bouclé, flanc ouvert | « Un mulet de bât, tué d'un coup net au flanc. Le harnais est encore bouclé : on n'a pas eu le temps de le décharger, ou on ne voulait pas. Le sang est déjà sombre. » | — |
| Besace (18,4 ; 15,6) | besace éventrée, gourde, un soulier d'enfant à quelques pas | « Une besace ouverte. Une gourde presque vide, un morceau de pain dur, et à deux pas, dans les aiguilles : un soulier d'enfant, trop petit pour l'homme du pin, trop propre pour avoir longtemps traîné ici. » ★ | `flag:sur_vu_soulier` ; ouvre la fouille `sur_besace` (§9) |
| ★ Traînée de sang (21,5 ; 16,6) → (29,5 ; 16,4) | sang séché dans les aiguilles, vers l'est | « Une traînée part du mulet et suit la piste vers l'est. Elle n'est pas d'un corps qu'on a traîné : trop étroite, trop interrompue. Quelqu'un a marché, en saignant, jusqu'à là-bas. » | `flag:sur_vu_trainee` |
| ★ Ornières (26,2-30,2 ; 15,4-18,4) | terre retournée, deux paires d'ornières larges, étuis vides | « La terre a été labourée par un véhicule lourd, pas un mulet. Deux paires d'ornières, récentes, qui repartent vers l'est. Dans la poussière : trois étuis de fusil du Service, encore brillants. » ★ Observation 3 : « Des pas d'enfant, à côté des bottes, s'arrêtent pile au bord des ornières. Ils ne repartent pas. » | `flag:sur_vu_ornieres` ; pose aussi `monde_mateo_pris` à la sortie si Roque a parlé de Mateo, sinon le drapeau attend le dialogue |
| Borne (2,5 ; 12) | petite borne de pierre, flèche gravée vers l'ouest | « Une borne de pierre, plus ancienne que la piste. Une flèche vers l'ouest, et ce qui reste d'un mot : …CHANT. Le Temple du couchant n'est plus très loin. Personne n'a déposé grand-chose au pied : une pierre posée sur une pierre, c'est tout. » | — (repère seulement, pas de culte) |
| Fourré de Paca (24,5-27 ; 6,5-8,7) | fourré de pins rabougris, une forme trop droite | de loin : « Quelqu'un est là, dans le fourré, et ne vient pas. » ; à 3 m : le dialogue de Paca s'ouvre | `flag:sur_vu_paca` |

Lecture à 1280 et en 390 : dès l'arrivée par l'est, l'œil trouve d'abord **le mulet sur la piste** (on ne peut pas ne pas le voir), puis **le pin et l'homme**, puis la lanterne. Paca ne se lit pas tout de suite. **Une seule lumière artificielle : la lanterne**, calque `_neon` serré sur la flamme, source visible, sans halo ; une flaque chaude au sol la nuit seulement, comme le feu du bivouac et le four. La lumière de la scène suit l'heure du voyage.

## 4. Plan coté (provisoire)
Les poses définitives, après sprites, sont au §15. Deux figures ont été décalées un peu vers le sud (Roque 13,3 au lieu de 12,8 ; Paca 25,8 ; 8,9 au lieu de 25,5 ; 8) pour rester lisibles devant le pin et le fourré.
Vue de dessus, 1 caractère = 1 m. Légende : `=` piste d'aiguilles (5 m, z 15-20), `p` pins, `P` pin mort, `R` Roque, `m` mulet, `b` besace, `s` soulier, `.` traînée, `O` ornières, `B` borne, `f` fourré de Paca, `2` Paca, `@` apparition, `t` sous-bois. `O>` sortie ouest (vers le Temple, halte), `<E` sortie est (reprise).

```text
      0         1         2         3
      01234567890123456789012345678901
  0   tttttpppttttttttttttpppttttttppp
  1   tttttpppttttttttttttpppttttttppp
  2   ttttttpppttttttttttttppptttttppp
  3   tttttttttttttttttttttttttttttttt
  4   tttttttttttttttttttttttttttttttt
  5   tttttttttttttttttttttttttttttttt
  6   ttttttttttttttttttttttttfffttttt
  7   ttttttttttttttttttttttttff2ttttt
  8   ttttttttttttttttttttttttfffttttt
  9   tttttttttttttPPPPttttttttttttttt
 10   tttttttttttttPPPPttttttttttttttt
 11   tttttttttttttPPPPttttttttttttttt
 12   ttBBtttttttttRPPPPtttttttttttttt
 13   tttttttttttttttttttttttttttttttt
 14   tttttttttttttttttttttttttttttttt
 15   =====b================OOO=======
 16   ========R=======m.s...OOOO=====@
 17   =================================
 18   =================================
 19   =================================
 20   tttttttttttttttttttttttttttttttt
 21   tttttttttttttttttttttttttttttttt
 22   ttttpppttttttpppttttttppptttpppt
 23   ttttpppttttttpppttttttppptttpppt
 24   tttttttttttttttttttttttttttttttt
 25   tttttttttttttttttttttttttttttttt
```

(Le `R` du plan est en (15,8 ; 12,8) ; le caractère à la ligne 16 n'est là que pour le reminder de la lecture depuis la piste.)

### Éléments et solides
| id | Élément | x0-x1 | z0-z1 | Haut. (m) | Solide | Couverture combat |
|---|---|---|---|---|---|---|
| piste | bande d'aiguilles tassées | 0-32 | 15-20 | 0 | non | — |
| pin mort | tronc foudroyé, silhouette | 13,5-17,5 | 9-12,5 | 5,5 | oui | 2 |
| pins (modules) | pins debout, réutilisables | voir poses | | 4-6 | oui (tronc 0,6×0,6) | 1 |
| mulet | mulet mort | 20,2-22,6 | 16,0-17,3 | 0,9 | oui | 1 |
| borne | borne de pierre | 2,5-3,7 | 12-13,2 | 0,8 | oui | 1 |
| fourré | fourré de Paca | 24,5-27 | 6,5-8,7 | 1,6 | oui (bord) | 1 |
| lanterne | accrochée au pin, sud | 15,6-16,0 | 12,0-12,3 | (sur le pin) | non | — |

### Apparition, sorties, déclencheurs
| id | Type | Position (m) | Rôle |
|---|---|---|---|
| entree | apparition | (30,5 ; 17) | arrivée depuis la Station, face à l'ouest |
| S_E | sortie | x 31,5 ; z 15-20 | reprise du voyage (vers la Station, d'où l'on vient, ou la suite du trajet) |
| S_O | sortie | x 0,5 ; z 15-20 | halte (vers le Temple) ; ouverte dès l'arrivée |
| pres_roque | déclencheur | autour de (15,8 ; 13,3), rayon 3 m | ouvre le dialogue de Roque |
| pres_paca | déclencheur | autour de (25,8 ; 8,9), rayon 3 m | ouvre le dialogue de Paca ; `flag:sur_vu_paca` |

### Zone de combat
Centre (18 ; 15), zone 19 × 19 (x 8,5-27,5 ; z 5,5-24,5), entièrement dans l'emprise.
- **Dedans** : le pin, Roque, le mulet, le fourré de Paca, une partie des ornières.
- **Couverture** : le pin mort vaut 2 ; le mulet, les pins, le fourré et la borne valent 1.
- L'entrée (30,5 ; 17) est hors de la zone. Distance à Paca (25,8 ; 8,9) : 9,9 m (≥ 8).

## 5. Mise en scène échelonnée (découverte progressive)
1. **Arrivée** (x 30,5) : la piste d'aiguilles, un mulet mort en travers, plus loin un pin mort et une lanterne. Rien n'impose de s'arrêter ; la sortie ouest est ouverte.
2. **Le mulet et la besace** : le soulier, trop petit. La traînée part vers l'est, d'où l'on vient.
3. **Roque** : il ne menace pas. Il a soif, il a mal, et il demande des nouvelles de « l'enfant ».
4. **Les ornières** : le Service, les étuis, les pas qui s'arrêtent.
5. **Paca** : elle n'a « rien pris encore ». Elle proposera de partager, ou de laisser faire.
6. **Après** : soigner, escorter, laisser de l'eau, dépouiller, ou partir. Mateo n'est plus ici.

## 6. PNJ : fiches et dialogues

### 6.1 Roque, le muletier
Homme d'une cinquantaine d'années, peau sombre, veste poussiéreuse déchirée au flanc, chiffon sanglant autour de la cuisse gauche, gourde presque vide à côté de lui. Il ne peut pas se lever tout seul. Il n'est pas un combattant.

- Sprite : `gen_rc_roque` (+ `_dos`), pose assise contre le pin, faceTo (30,5 ; 17). Portrait 192 px.
- Position : (15,8 ; 13,3). Hauteur 1,4 m assis. (Un peu plus au sud que le plan provisoire, pour rester devant les racines ; voir §15.2.)
- Dialogue `sur_roque`, ouvert par `pres_roque` ou examen à 3 m.

**start** (première approche)
- « …De l'eau. S'il t'en reste. Je… je me relèverai. L'enfant. Tu l'as vu, sur la piste ? »
  - « Tiens, bois. » (`inv:water>=1`) → `take:water;pv:4;flag:sur_soigne;flag:sur_parle` → **soigne**
  - « Je n'ai plus d'eau, mais j'ai une ration. » (`inv:ration>=1`, pas d'eau) → `take:ration;pv:2;flag:sur_soigne;flag:sur_parle` → **soigne**
  - « Quel enfant ? » → `flag:sur_parle` → **enfant**
  - « Qu'est-ce qui s'est passé ? » → `flag:sur_parle` → **recit**
  - « Je ne peux rien pour toi. » → `flag:sur_parle` → **refus**
  - [s'éloigner] → (ferme ; Roque n'insiste pas la première fois)

**soigne**
- « Merci. Ça… ça tient. Je m'appelle Roque. C'est mon neveu, Mateo. On allait à la Station. Il y avait quelqu'un, pour lui. Pour le faire passer. » S'il a `monde_remedios_vue` : « La caravane. Celle de la citerne. Tu la connais, toi aussi. » Sinon : « Un contact, à la Station. Il fait passer les gens comme lui. Plus au nord. Plus à l'abri. »
  - « Le Service est venu ? » → **recit**
  - « Je peux te relever. On marche jusqu'à la Station. » → **escorte_offre**
  - « J'ai vu un soulier, près du mulet. » (`sur_vu_soulier`) → **soulier**
  - « Il y a des ornières, plus à l'est. » (`sur_vu_ornieres`) → **ornieres**
  - « Repose-toi. Je reviens. » → (ferme)

**enfant** / **recit** (même nœud si déjà dit, variantes)
- « Mateo. Le fils de ma sœur. Il a… la peau, tu vois, les plaques, comme certains, au bord du fleuve. À Dusk-Town ils baissent les cols, pour ça. On se levait avant le jour, pour ne pas les croiser. Ils nous ont eus quand même. Deux hommes, un véhicule. Ils ont pris l'enfant. Ils m'ont tiré dessus comme à un chien. Le mulet aussi. »
  - si `race_mutant` : « Toi aussi, tu… Oui. Je vois. Alors tu comprends pourquoi je le menais là-bas. »
  - « Je vais suivre la piste. » → `flag:sur_promet` → **promet**
  - « Je peux t'emmener à la Station. » → **escorte_offre**
  - « Je n'ai rien à te donner. » → **refus**

**soulier**
- « C'est le sien. L'autre est… je ne sais pas. Il l'a perdu quand ils l'ont fait monter. Il a treize ans. Il ne pèse pas lourd. » (`flag:sur_vu_soulier` déjà, `flag:monde_mateo_pris` à la sortie)

**ornieres**
- « Je les ai entendus. Le moteur. Ils sont repartis vers la Station, ou vers la douane. Si tu vas de ce côté-là… si tu vois un enfant, les plaques sur les bras, un soulier à un pied… » Il s'arrête. « Dis-lui que son oncle n'a pas couru. »

**escorte_offre**
- « Tu ferais ça ? C'est une heure, peut-être deux, et je pèse. Mais j'arriverai. À la Station, je sais qui voir. Je te paierai ce que j'ai : huit dollars, et mon couteau, s'il te sert. »
  - « Viens. » → `flag:sur_escorte;flag:sur_soigne;flag:sur_regle` → **escorte_ok** (la sortie est déclenche `dureeSi` +1 h, `monde_roque_sauve`, `monde_roque_escorté`, et on lui laisse le couteau ou on le prend s'il l'offre : `give:poignard` optionnel + 8 $)
  - « Je ne peux pas m'attarder. » → **refus**

**escorte_ok**
- « Bien. Aide-moi à me mettre debout. On avance doucement. S'il est encore à la Station… on verra. »

**promet**
- « Merci. Même si tu ne le trouves pas. Merci d'avoir dit ça. »

**refus**
- S'il a déjà été soigné : « Va. Tu as déjà fait plus que les autres. » Sinon : « Alors laisse-moi au moins la gourde, si tu en as une. Ou pars, et que Paca attende encore un peu. »
  - « Je te laisse de l'eau. » (`inv:water>=1`) → `take:water;flag:sur_laisse_eau` → « Elle est là. Merci. »
  - [partir]

**Reprise** (déjà parlé, `sur_parle`)
- S'il est soigné : « Tu reviens. J'ai moins froid. »
- S'il a de l'eau laissée : « Ta gourde est encore là. J'en ai pris une gorgée. »
- Sinon, plus faible : « Tu… tu as de l'eau, cette fois ? »

**Dépouiller** (verbe d'action sur Roque, ou option si on insiste)
- Option cachée, ou après « Je prends ce que tu as. » :
  - S'il peut encore parler : « Prends. L'eau d'abord, je t'en prie, laisse-moi l'eau. » → on peut prendre 8 $, le `poignard`, et la gourde (`water`) ; `flag:sur_depouille`. S'il prend **aussi** la dernière eau : `flag:sur_laisse_mourir`. « Va. Que tu ne le retrouves pas, l'enfant. »
  - Après `sur_soigne` : il ne résiste pas, mais : « Je ne t'aurais pas demandé ça. » Même butin, `flag:sur_depouille` sans `sur_laisse_mourir`.

Roque n'attaque pas. Si le joueur l'attaque, voir §8.

### 6.2 Paca, la charognarde
Femme mince, la quarantaine, châle poussiéreux, bâton, sac vide. Elle n'a rien d'une assassin : elle vit de ce que la piste abandonne. Elle n'est pas venue avec le Service.

- Sprite : `gen_rc_paca` (+ `_dos`), debout dans le fourré, faceTo (20 ; 16). Portrait 192 px.
- Position : (25,8 ; 8,9). Hauteur 1,68 m. (Un peu plus au sud que le plan provisoire, pour dépasser du fourré ; voir §15.2.)
- Visible dès l'arrivée, mais peu lisible en 390. Dialogue `sur_paca`.

**start**
- « Je n'ai encore rien pris. Tu peux vérifier. J'attendais de voir s'il se relevait, ou si quelqu'un passait. Ça tombe bien : quelqu'un passe. »
  - « Tu l'as vu, ce qui s'est passé ? » → **temoin**
  - « Tu compte le dépouiller. » → **aveu**
  - « Laisse-le. Tu t'en vas. » (Intimidation 5, ou juste l'ordre si on a déjà soigné Roque) → **degage**
  - « On peut partager, s'il meurt. » → `flag:sur_paca_pacte` → **pacte**
  - [s'éloigner]

**temoin**
- « J'étais plus bas, vers la borne. J'ai entendu le moteur, les voix, un coup. Quand je suis remontée, l'enfant n'y était plus, et l'homme était déjà contre le pin. Les hommes du Service ne s'attardent pas sous les arbres. Ils n'aiment pas ce bois. Mais ils y entrent, quand il le faut. »
  - « Que vas-tu faire ? » → **aveu**

**aveu**
- « Ce qu'on fait tous, sur la piste. J'attends. S'il se relève, je n'ai rien vu. S'il ne se relève pas, le mulet a encore un harnais, et l'homme a un couteau. Je ne suis pas celle qui a tiré. »
  - « Touche-le, et on a un problème. » → **degage** (sans test, si franc)
  - « Fais ce que tu veux. » → `flag:sur_paca_libre` → (elle restera ; si on part sans soigner ni laisser d'eau, à la sortie le jeu peut considérer que Paca a pris le butin : pas de `monde_roque_sauve`)

**degage**
- « Bien. Tu l'as dit clairement. Je rentre vers la Station. Il y a d'autres pistes. » Elle s'en va (`si` la cache : Paca disparaît, `flag:sur_paca_partie`).

**pacte**
- « D'accord. Toi l'eau et le couteau, moi le harnais et les semelles, si tu veux. On n'est pas des bêtes. » (ne se déclenche vraiment que si Roque meurt ou est dépouillé ; sinon elle attend)

**Après `sur_soigne`**
- « Alors il se relèvera. Tant mieux. J'irai voir plus loin. » (`flag:sur_paca_partie`)

### 6.3 Mateo (absent)
Aucun sprite, aucun dialogue. Treize ans, mutant, plaques sur les avant-bras (même forme que Lena et Rufina, « dans certaines familles au bord du fleuve », MUTANTS §13.6). On le lit dans le soulier, les pas, et la bouche de Roque. Drapeau de monde `monde_mateo_pris` : une accroche pour la Station, Dusk-Town ou la douane, plus tard, pas une quête.

### 6.4 Textes de déclencheurs et des points d'action
| id | Texte |
|---|---|
| arrivee | « Un bois de pins secs. Un mulet mort sur la piste, un homme contre un arbre foudroyé. Une lanterne brûle encore. » |
| pres_roque (première) | (ouvre le dialogue, pas de texte à part) |
| S_O (vers le Temple) | « La piste descend vers l'ouest, vers le Temple du couchant. » |
| S_E | si `sur_escorte` : « Tu prends Roque sous le bras. Une heure de plus, à son pas. » ; sinon : « Tu reprends la piste. » |

## 7. Manières d'agir et conséquences
| Approche | Comment | Conséquence |
|---|---|---|
| Passer | longer la piste jusqu'à S_O ou S_E, sans s'arrêter (Roque appelle une fois, rien de plus) | reprise ou halte ; `monde_sur_vu` ; Roque n'est pas sauvé |
| Soigner | donner 1 `water` (4 PV) ou 1 `ration` (2 PV) | `sur_soigne` ; ouvre l'escorte et le récit ; à la sortie : `monde_roque_sauve` |
| Laisser de l'eau | 1 `water`, sans s'attarder | `sur_laisse_eau` ; `monde_roque_sauve` (il tient jusqu'à un secours, ou jusqu'à la Station) |
| Escorter | après le soin, accepter de le ramener | +1 h, 8 $, éventuellement un `poignard` ; `monde_roque_sauve`, `monde_roque_escorté` |
| Suivre la traînée | examiner ornières et soulier | `monde_mateo_pris` ; Roque a des répliques |
| Promettre de chercher Mateo | dialogue | `sur_promet` ; accroche, pas une quête |
| Parler à Paca | la chasser, pactiser, ou l'ignorer | `sur_paca_partie` / `sur_paca_pacte` / `sur_paca_libre` |
| Dépouiller Roque | prendre l'argent, le couteau, l'eau | `sur_depouille`, `monde_roque_depouille` ; s'il perd aussi sa dernière eau : `sur_laisse_mourir` (pas de `monde_roque_sauve`) |
| Combattre | attaquer Paca, ou Roque | voir §8 |
| Partir | S_E ou S_O à tout moment ; fuite pendant le combat | halte ou reprise |

Drapeaux de scène (préfixe `sur_`, purgés à la sortie) : `sur_parle`, `sur_soigne`, `sur_laisse_eau`, `sur_escorte`, `sur_promet`, `sur_vu_soulier`, `sur_vu_trainee`, `sur_vu_ornieres`, `sur_vu_paca`, `sur_paca_partie`, `sur_paca_pacte`, `sur_paca_libre`, `sur_depouille`, `sur_laisse_mourir`, `sur_regle`, `sur_vaincue`.

Drapeaux de monde (**pas** de préfixe `sur_`, jamais purgés) : `monde_sur_vu` (arrivée, rencontre unique), `monde_roque_sauve`, `monde_roque_escorté`, `monde_roque_depouille`, `monde_mateo_pris`.

À la sortie, le gestionnaire pose `monde_sur_vu`. Il pose `monde_roque_sauve` si `sur_soigne` ou `sur_laisse_eau` ou `sur_escorte`, et pas `sur_laisse_mourir`. Il pose `monde_mateo_pris` si `sur_vu_ornieres` ou si Roque a raconté l'enfant.

## 8. Combat optionnel
Aucun combat n'est requis. Le Service n'est plus là.

| id | Sprite | Position absolue (x ; z) | Case | PV | PA | Init. | Arme | Mêlée / armes | Particularité |
|---|---|---|---|---|---|---|---|---|---|
| paca | gen_rc_paca | (25,8 ; 8,9), au fourré | libre | 10 | 6 | 6 | bâton | 35 / 15 | couverture 1 (fourré) ; `rendSous: 0.5` ; `fuitTour: 2` ; seulement si le joueur l'attaque ou brise un pacte par la force |
| roque | gen_rc_roque | (15,8 ; 13,3), au pin | libre | 4 | 3 | 2 | (mains) | 10 / 0 | **jamais dans la liste par défaut** ; seulement si le joueur l'attaque ; `rendSous: 1.0` dès le premier coup |

Distances à l'entrée (30,5 ; 17) : Paca 10,3 m, Roque 15,3 m (toutes ≥ 8 m).

Issues (aucune mort obligatoire à l'écran) :
- **victoire** (Paca se rend ou fuit) : `flag:sur_paca_partie`. Texte : « Paca lève les mains. "D'accord. La piste est grande." Elle rentre dans les pins, vers le sud. »
- **fuite** : `rencontre:quitter` ; halte. Texte : « Tu cours. Personne ne te poursuit. »
- **reddition** (du joueur, si Paca est en cause) : `payMax:8`. Texte : « Paca ramasse ce qui tombe. "Je t'avais dit que j'attendais. Voilà, j'attends plus." »
- **defaite** : `warp:rc_survivant_pins:30.5:17` + 1 PV. Texte : « Tu te réveilles plus bas sur la piste, la tête lourde. La lanterne, au loin, brûle encore — ou plus. »
- Si le joueur attaque Roque : il se rend au premier coup. Texte : « Il ne se défend pas. Il tourne la tête vers le pin. "Vas-y. Mais l'enfant, toi, tu ne le retrouveras pas." » `flag:sur_depouille;flag:sur_laisse_mourir`.

## 9. Objets à fouiller (butin et récompenses)
Objets existants (`water`, `ration`, `poignard`). Pas de nouvel objet obligatoire ; le soulier est un indice, pas un item.

| Où | Condition | Contenu |
|---|---|---|
| Besace (18,4 ; 15,6) | toujours | 1 `ration` (le pain dur) ; la gourde est vide (l'eau de Roque est sur lui, en dialogue). Texte vide ensuite : « La besace est vide. Le soulier est toujours là. » |
| Roque, soigné / escorté | récompense | 8 $ ; il offre aussi son `poignard` (« s'il te sert ») |
| Roque, dépouillé | `sur_depouille` | 8 $, 1 `poignard`, 1 `water` s'il en restait |
| Paca, après victoire | fouille de son sac | 1 `ration`, 4 $ |
| Mulet | après `sur_laisse_mourir` ou victoire cruelle, ou pacte avec Paca | rien de vendre : un harnais, pas un item ; texte : « Le harnais viendrait, à qui voudrait le couper. Tu le laisses. » |

## 10. Clés d'assets : réutilisations et clés nouvelles à produire
Sprites produits et publiés (groupe `rc_survivant_pins`) : lot 1 sols et décors `014db7e`, lot 2 PNJ `98a6fd2`. Même pipeline que le pilote, la caravane et l'écluse : caméra du jeu, 50 px/m, manifeste `assets/rencontres/manifest.json`, aucune clé existante modifiée, aucun étirement. Poses définitives au §15.

Préfixes :
- `rc_fo_` pour les modules de la **forêt**, réutilisables par d'autres rencontres de ce biome ;
- `rc_sur_` pour les éléments propres à cette rencontre ;
- `g_rc_` pour les sols ;
- `gen_rc_` pour les PNJ.

**Le soleil** : même direction que le pilote. Seule la couleur change, et c'est l'ambiance de la scène qui la règle (§11).

**Réutilisé tel quel** : aucun module de désert ou de verre n'est posé ici (l'identité du biome doit se tenir seule). On peut, plus tard, réutiliser un rocher `rc_ds_rochers_*` dans un fourré si le besoin est argumenté ; ce n'est pas le cas aujourd'hui.

**Clés nouvelles à produire** :

| Clé | Rôle | Emprise L × P × H (m) | Notes |
|---|---|---|---|
| `g_rc_aiguilles` (+ `_b`, `_c`) | tapis d'aiguilles de pin, rouille et ocre, terre sèche | tuile 4 m | jamais uni ; pas de vert « jardin » |
| `g_rc_piste_foret` (+ `_b`) | piste tassée, aiguilles écrasées, ornières légères | tuile 4 m | raccord avec `g_rc_aiguilles` |
| `rc_fo_pin_mort_3q` | pin foudroyé, écorce éclatée, branche basse pour la lanterne | 4 × 3,5 × 5,5 | **la silhouette de la scène** |
| `rc_fo_pin_3q` (+ `_b`) | pin sec debout, tronc pâle, frondaison olive-gris | 2,2 × 2,2 × 5,5 (`_b` un peu plus petit) | module forêt, plusieurs poses |
| `rc_fo_fourre_3q` | fourré de pins rabougris | 2,5 × 2,2 × 1,6 | cache de Paca |
| `rc_fo_borne_3q` | borne de pierre, flèche ouest | 1,2 × 1,2 × 0,8 | texte d'examen, pas un décalque de lettres obligatoires |
| `rc_sur_mulet_3q` | mulet de bât mort, harnais bouclé | 2,4 × 1,3 × 0,9 | sur la piste, lisible dès l'arrivée |
| `rc_sur_besace_3q` | besace ouverte, gourde, pain | 0,8 × 0,6 × 0,3 | |
| `rc_sur_soulier_3q` | soulier d'enfant dans les aiguilles | 0,3 × 0,3 × 0,1 | doit se lire à 1280 ; en 390, l'anneau d'examen suffit |
| `rc_sur_lanterne_3q` (+ `_neon`) | lanterne à huile accrochée | 0,25 × 0,25 × 0,4 | `_neon` serré sur la flamme, orange, **source visible** ; flaque nocturne générique au sol (comme le bivouac) |
| `rc_sur_trainee_3q` | décalque : traînée de sang séché vers l'est | 8 × 1,5 × 0 | fond |
| `rc_sur_ornieres_3q` | décalque : ornières larges, terre retournée, étuis | 4 × 3 × 0 | fond |
| `gen_rc_roque` (+ `_dos`, portrait) | Roque assis, jambe bandée | — | vue de face et vraie vue de dos ; ancre au milieu des hanches au sol (posé) |
| `gen_rc_paca` (+ `_dos`, portrait) | Paca debout, châle, bâton | 1,68 m | face + dos, portraits 192 px |

## 11. Identité du biome (forêt occidentale, pins secs)
- **Biome** : le petit bois à l'ouest, autour du Temple du couchant, première forêt du chantier. Ce n'est pas une jungle, ce n'est pas un sous-bois humide. Pins secs, aiguilles rouille, terre ocre, troncs pâles. Le dernier ombrage avant la Station.
- **Palette** :
  - **Aiguilles** : rouille `#8a5a32`. **Terre** : ocre `#b08a58`.
  - **Troncs** : gris pâle `#c8b89a`, écorce sombre `#5a5848`.
  - **Frondaison** : olive-gris `#6a6a40`, jamais un vert de jardin, jamais un vert « radioactif ».
  - **Sang séché** : `#6a3020`.
  - **Accents** : flamme de la lanterne `#ff9a48` (seule source), pierre de la borne `#8a8276`.
  - **Ciel du jour** : blanc-jaune un peu plus doux que le verre, moins ambre que le désert.
  - **Interdits** : aucun cyan, aucun violet, pas de mousse bleutée, pas de brume enchantée.
- **Lumière** : même direction de soleil que le pilote. **Courbe `forest` proposée** pour `src/data/ambiances.js`, même structure et mêmes heures que `desert` :
  - **Jour** : un peu plus doux et un peu plus olive que l'ambre du désert, sans devenir vert.
  - **Nuit** : la même nuit bleu-gris que le désert et le verre (pas de teinte propre).
  Scène `ambiance: 'forest'`. Repli si la courbe n'est pas ajoutée : `ambiance: 'desert'`.
- **Liseré de lune** : déjà tranché (MUTANTS §11, 50 %, tête et épaules seulement, coupé à 25 % de la silhouette).
- **Sol** : jamais uni. Aiguilles, terre à nu, ornières, sang.
- **À éviter** :
  - une forêt luxuriante, des fougères, de l'eau vive ;
  - un temple « magique » ou un autel chargé (la borne est une pierre, c'est tout) ;
  - une lanterne qui éclaire toute la clairière (halo) ;
  - Mateo visible en cadavre (il a été emmené : le décor le dit, pas un corps).

## 12. Points d'accroche pour Rivet
1. Catalogue `src/data/rencontres.js` : entrée `survivant_pins` du §14 (fichier `rencontres_survivant.js`, comme la caravane).
   - `prefixe: 'sur_'`, `terrains: ['foret']`, `biomes: ['forest']`.
   - `si: (etat, kase) => !etat.flags.monde_sur_vu && !(kase.col===6 && kase.row===8)` : unique, et l'on ne tire pas sur G09 (Temple).
   - `drapeauArrivee: 'monde_sur_vu'`.
   - Taux de `TERRAINS` inchangés.
2. Sorties : S_E reprend le trajet ; S_O met en halte (vers le Temple, qui n'a pas encore de terrain jouable).
3. `dureeSi` : +1 h si `sur_escorte`.
4. Enseigne de la lanterne : `effet: 'pulse'` lent, `flaque` générique au sol, la nuit seulement, comme le bivouac. La lanterne peut être un `building` léger (pour porter le `_neon`) ou un prop avec enseigne, selon ce qui est le plus simple.
5. Roque n'est pas un ennemi. Paca n'entre dans le combat que si le joueur l'attaque.
6. Action `pv:N` déjà posée au lot Verriers : le soin à l'eau l'utilise.
7. À la sortie, poser les drapeaux de monde selon le §7 (Roque sauvé / dépouillé, Mateo pris).
8. Tests : `?dev=1` → forcer `survivant_pins` sur F08, F09 ou G08, 1280 et 390. Rien à tester tant que les sprites et le câblage ne sont pas là.
9. **Sprites** : produits (`014db7e` sols et décors, `98a6fd2` PNJ). Poses, mesures et défauts au §15. La lanterne porte le `_neon` ; la flaque nocturne est l'enseigne générique du §14 (comme le bivouac), pas un décalque.

## 13. Décisions de DA et de lore à signaler à Valentin
**Garde-fou (Régie, 18 novembre 2026)** : les drapeaux `monde_*` déjà posés par la caravane, les Verriers et maintenant Mateo servent seulement à des répliques et à des indices, sans aucune conséquence de quête, tant que Valentin n'a pas validé une quête de la filière.

Rien n'est imposé ; tout est [proposition]. Les points 1 à 5 sont des **modifications ou des extensions de lore**, à valider ou à refuser une par une.

**Modifications importantes**
1. **La forêt occidentale est un vrai lieu**, pas seulement une couleur sur la carte : un bois de pins secs, quatre cases (F08, G08, F09, et G09 pour le Temple). C'est la première rencontre du biome `forest`, distincte du désert (pilote, caravane) et du verre (écluse).
2. **Le Temple du couchant** reste ce qu'il est sur la carte : un grand lieu, pas encore jouable. Dans cette scène, il n'est qu'un **repère** (une borne, une flèche, un mot effacé). Je n'en fais ni un culte, ni un sanctuaire, ni une étape de la filière. Si tu veux lui donner un rôle plus tard, cette rencontre ne le grève pas.
3. **Roque, Mateo, Paca** : trois noms nouveaux, même saveur hispanophone que la caravane et les Verriers. Mateo n'apparaît pas : il a treize ans, il est mutant (plaques des avant-bras, même forme déjà proposée pour Lena et Rufina), le Service l'a emmené. C'est une accroche (`monde_mateo_pris`), pas une quête.
4. **Le Service entre dans la forêt.** Ce n'est pas le verre : ici, une patrouille peut passer, prendre quelqu'un, et repartir. Ça distingue les deux biomes, et ça rend le refuge des Verriers plus précieux, s'il est retenu.
5. **Un contact à la Station**, pour faire passer Mateo, s'appuie sur la filière de Remedios (CARAVANE §13.1) sans l'étendre d'un nouveau nœud : pas de cache, pas de nouveau personnage nommé à la Station. Si tu refuses la filière, Roque dit seulement « quelqu'un qui les emmène plus au nord ».

**Points de cohérence**
6. Pas de cadavre d'enfant dans la scène. Le soulier, les pas qui s'arrêtent, et le récit de Roque suffisent.
7. Paca n'est pas une « méchante » : elle attend, elle peut s'en aller, elle n'a pas tiré.
8. Le soin coûte quelque chose (une eau, une ration, ou une heure). Partir sans rien donner est possible. Dépouiller aussi.
9. **Noms et objets** : Roque, Mateo, Paca ; « Le témoin sous les pins » ; une lanterne de piste ; une borne vers le Temple.

**DA**
10. **Biome de forêt** : pins secs, aiguilles rouille, ocre, olive-gris ; une seule lumière, la lanterne ; courbe `forest` proposée, nuit commune.
11. Première forêt du chantier : aucun module de désert ou de verre réutilisé, pour que l'identité tienne seule.

## 14. Entrée au format d'ARCHI.md §4
Poses définitives au §15 (même principe que l'écluse) ; positions en mètres, ancre des décors au coin sud-est de l'emprise. Roque et Paca sont un peu plus au sud que le plan provisoire du §4, pour rester lisibles devant le pin et le fourré.

```js
survivant_pins: {
  nom: 'Le témoin sous les pins', famille: 'survivant', prefixe: 'sur_',
  terrains: ['foret'], biomes: ['forest'], poids: 1, duree: 1,            // +1 h si sur_escorte (§12)
  si: (etat, kase) => !etat.flags.monde_sur_vu && !(kase.col === 6 && kase.row === 8),
  drapeauArrivee: 'monde_sur_vu',
  arrivee: 'Un bois de pins secs. Un mulet mort sur la piste, un homme contre un arbre foudroyé. Une lanterne brûle encore.',
  scene: { size: { w: 32, d: 26 },
    ground: { skin: 'g_rc_aiguilles', tint: null, paint: [ /* bande g_rc_piste_foret z 15-20 ; variantes _b/_c semées */ ] },
    ambiance: 'forest',
    buildings: [
      // poses définitives : §15.1 (pin mort, pins, fourré, borne, lanterne)
    ],
    props: [
      // poses définitives : §15.1 (mulet, besace, soulier, décalques)
    ],
    entrees: [{ id: 'entree', x: 30.5, z: 17, side: 'east' }],
    sorties: [
      { id: 'S_E', x: 31.5, z: 15, w: 0.5, d: 5, rencontre: true, reprise: true },
      { id: 'S_O', x: 0, z: 15, w: 0.5, d: 5, rencontre: true }
    ],
    enseignes: [{ id: 'sur_lampe', building: 'sur_lanterne', effet: 'pulse', periode: 6, intensite: 0.6,
      flaque: { r: 1.5, x: 15.8, z: 12.6, couleur: '#ff9a48', i: 0.55 } }]
  },
  pnj: [
    { id: 'sur_roque', name: 'Roque', sprite: 'gen_rc_roque', x: 15.8, z: 13.3, faceTo: [30.5, 17], dialogue: 'sur_roque' },
    { id: 'sur_paca', name: 'Paca', sprite: 'gen_rc_paca', x: 25.8, z: 8.9, faceTo: [20, 16], dialogue: 'sur_paca', si: '!sur_paca_partie' }
  ],
  // dialogues : §6 ; fouilles et examens : §3 et §9 ; combat : §8 (vide par défaut)
}
```

## 15. Poses définitives et sprites publiés
Sprites produits et publiés dans `assets/rencontres/` (groupe `rc_survivant_pins`, manifeste sans clé existante modifiée, vérifié par script) : lot 1 sols et décors `014db7e`, lot 2 PNJ `98a6fd2`. Même pipeline que le pilote, la caravane et l'écluse : caméra du jeu (lacet 34,5°, tangage 28,8°, 50 px/m), échelle uniforme, aucun étirement. Ombres de contact au pied des décors (pas sur la lanterne, qui est accrochée). Planche : `/workspace/nml-shots/rencontres/survivant_planche_sprites.png` ; MAQUETTE : `/workspace/nml-shots/rencontres/survivant_maquette.png`.

**Tirage** : cases de forêt F08, G08, F09 (G09 Temple exclu), §1 ; la scène ne dépend pas de la case.

### 15.1 Table des poses (décors)
x, z = coin nord-ouest de l'emprise ; l'ancre du sprite tombe au coin sud-est au sol (x + w ; z + d). `depth` = (x + w) + (z + d) ; `ordre` = ordre de dessin conseillé (décalques `fond` d'abord). Deux ajustements par rapport au plan provisoire du §4, pour que les figures se lisent : Roque un peu plus au sud, Paca juste au sud du fourré.

| Clé | x | z | w | d | Solides (x, z, w, d, couv) | Ordre | Depth |
|---|---|---|---|---|---|---|---|
| `rc_sur_trainee_3q` | 21.5 | 16.2 | 8 | 1.5 | fond | 1 | 47.2 |
| `rc_sur_ornieres_3q` | 26.2 | 15.4 | 4 | 3 | fond | 2 | 48.6 |
| `rc_fo_pin_3q` | 2 | 1 | 2.2 | 2.2 | 2, 1, 2.2, 2.2, 2 | 3 | 7.4 |
| `rc_fo_pin_b_3q` | 7 | 2 | 2 | 2 | 7, 2, 2, 2, 2 | 4 | 13 |
| `rc_fo_borne_3q` | 2.5 | 12 | 1.2 | 1.2 | 2.5, 12, 1.2, 1.2, 1 | 5 | 16.9 |
| `rc_fo_pin_3q` | 22 | 1.5 | 2.2 | 2.2 | 22, 1.5, 2.2, 2.2, 2 | 6 | 27.9 |
| `rc_fo_pin_mort_3q` | 13.5 | 9 | 4 | 3.5 | 13.5, 9, 4, 3.5, 2 | 7 | 30 |
| `rc_sur_lanterne_3q` | 15.6 | 12.0 | 0.25 | 0.25 | — | 8 | 30.5 (forcer après le pin : elle est accrochée à la branche sud) |
| `rc_fo_pin_3q` | 4 | 22.5 | 2.2 | 2.2 | 4, 22.5, 2.2, 2.2, 2 | 9 | 30.9 |
| `rc_fo_pin_b_3q` | 28 | 2 | 2 | 2 | 28, 2, 2, 2, 2 | 10 | 34 |
| `rc_fo_fourre_3q` | 24.5 | 6.5 | 2.5 | 2.2 | 24.5, 6.5, 2.5, 2.2, 1 | 11 | 35.7 |
| `rc_sur_besace_3q` | 18.4 | 15.6 | 0.8 | 0.6 | — | 12 | 35.4 |
| `rc_fo_pin_b_3q` | 12 | 23 | 2 | 2 | 12, 23, 2, 2, 2 | 13 | 39 |
| `rc_sur_soulier_3q` | 22.2 | 16.8 | 0.3 | 0.3 | — | 14 | 39.6 |
| `rc_sur_mulet_3q` | 20.2 | 16.0 | 2.4 | 1.3 | 20.2, 16.0, 2.4, 1.3, 1 | 15 | 39.9 |
| `rc_fo_pin_3q` | 24 | 22.8 | 2.2 | 2.2 | 24, 22.8, 2.2, 2.2, 2 | 16 | 51.2 |
| `rc_fo_pin_b_3q` | 29 | 22.5 | 2 | 2 | 29, 22.5, 2, 2, 2 | 17 | 55.5 |

Calques : `rc_sur_lanterne_3q_neon` (additif, même canevas, même ancre, flamme seulement, orange `#ff9a48`, pas de halo). Flaque nocturne : enseigne générique du §14 (`sur_lampe`, `flaque` r 1,5 au sol en (15,8 ; 12,6)), comme le bivouac ; ce n'est pas un décalque.

### 15.2 PNJ
| Clé | Position (x ; z) | Hauteur | Remarques |
|---|---|---|---|
| `gen_rc_roque` (+ `_dos`) | (15,8 ; 13,3) | 1,4 m assis | faceTo (30,5 ; 17) ; ancre au sol sous les hanches (`pivot: 0`) ; un peu plus au sud que le §4 (12,8), pour rester devant les racines du pin |
| `gen_rc_paca` (+ `_dos`) | (25,8 ; 8,9) | 1,68 m | faceTo (20 ; 16) ; absente si `sur_paca_partie` ; un peu plus au sud que le §4 (25,5 ; 8), pour dépasser du fourré dès l'arrivée |

Portraits `portrait-gen_rc_roque`, `portrait-gen_rc_paca` (192 px). Ancre au pied, au centre, comme les autres rencontres.

### 15.3 Clés publiées
| Clé | px | Ancre | Emprise L × P × H (m) |
|---|---|---|---|
| `g_rc_aiguilles` | 512 × 512 | — | tuile 4 m |
| `g_rc_aiguilles_b` | 512 × 512 | — | tuile 4 m |
| `g_rc_aiguilles_c` | 512 × 512 | — | tuile 4 m |
| `g_rc_piste_foret` | 512 × 512 | — | tuile 4 m |
| `g_rc_piste_foret_b` | 512 × 512 | — | tuile 4 m |
| `rc_fo_pin_mort_3q` | 144 × 254 | [105, 253] | 4 × 3,5 × 5,5 |
| `rc_fo_pin_3q` | 177 × 245 | [102, 244] | 2,2 × 2,2 × 5,5 |
| `rc_fo_pin_b_3q` | 116 × 215 | [70, 214] | 2 × 2 × 4,8 |
| `rc_fo_fourre_3q` | 164 × 127 | [102, 126] | 2,5 × 2,2 × 1,6 |
| `rc_fo_borne_3q` | 56 × 85 | [35, 84] | 1,2 × 1,2 × 0,8 |
| `rc_sur_mulet_3q` | 136 × 97 | [99, 96] | 2,4 × 1,3 × 0,9 |
| `rc_sur_besace_3q` | 41 × 44 | [29, 43] | 0,8 × 0,6 × 0,3 |
| `rc_sur_soulier_3q` | 20 × 24 | [12, 21] | 0,3 × 0,3 × 0,12 |
| `rc_sur_lanterne_3q` | 12 × 23 | [7, 22] | 0,25 × 0,25 × 0,4 |
| `rc_sur_lanterne_3q_neon` | 12 × 23 | [7, 22] | calque additif |
| `rc_sur_trainee_3q` | 351 × 117 | [318, 116] | 8 × 1,5 × 0 |
| `rc_sur_ornieres_3q` | 213 × 88 | [148, 87] | 4 × 3 × 0 |
| `gen_rc_roque` | 614 × 512 | [307, 511] | height_m 1,4 ; pivot 0 |
| `gen_rc_roque_dos` | 636 × 512 | [318, 511] | height_m 1,4 ; pivot 0 |
| `portrait-gen_rc_roque` | 192 × 192 | — | portrait |
| `gen_rc_paca` | 244 × 512 | [122, 511] | height_m 1,68 ; pivot 0 |
| `gen_rc_paca_dos` | 252 × 512 | [126, 511] | height_m 1,68 ; pivot 0 |
| `portrait-gen_rc_paca` | 192 × 192 | — | portrait |

Pentes mesurées (cible 0,33 / 0,70), pied gauche / droit :

| Clé | Pente mesurée |
|---|---|
| `rc_fo_pin_mort_3q` | 0,10 / 0,39 |
| `rc_fo_pin_3q` | 0,67 / 0,22 |
| `rc_fo_pin_b_3q` | 0,09 / 0,03 |
| `rc_fo_fourre_3q` | 0,81 / 0,29 |
| `rc_fo_borne_3q` | 0,50 / 1,00 |
| `rc_sur_mulet_3q` | 0,67 / 0,12 |
| `rc_sur_besace_3q` | 1,00 / 1,00 |
| `rc_sur_soulier_3q` | — / 0,80 |
| `rc_sur_lanterne_3q` | — / — (trop petite) |

### 15.4 Défauts connus (v1)
- Les pins (et le pin foudroyé) sont des silhouettes peintes, calées sur le volume à la caméra ; leurs flancs restent plus verticaux que la boîte iso (pentes mesurées loin de 0,33 / 0,70). Ce n'est pas un étirement : l'échelle est uniforme.
- Le fourré se lit un peu plus « vu de dessus » que les pins debout.
- Les racines du pin foudroyé sont amples : Roque, à la position provisoire (15,8 ; 12,8), disparaissait derrière. La pose du §15.2 le met juste au sud.
- De même, Paca à (25,5 ; 8) tombait dans l'emprise du fourré. La pose du §15.2 la fait dépasser au sud. Si le moteur trie seulement sur le pied, garder un `ordre` / `depth` supérieur à celui du fourré.
- La lanterne fait 12 × 23 px (c'est sa taille réelle, 0,4 m) : la flamme tient en quelques pixels. La poser **après** le pin (depth > 30), sinon la branche sud la cache. Pas de halo.
- Le soulier fait 20 × 24 px : il se lit à 1280 ; en 390, l'anneau d'examen suffit, comme prévu.
- Les étuis des ornières sont à peine visibles à 50 px/m (volontairement un peu plus gros que nature, mais encore discrets).
- Les joints de la piste `g_rc_piste_foret` restent un peu lisibles tous les 4 m, en bande.
- La vue de dos de Paca est un 3/4 un peu plus profilé que celle de Roque ; le dos, le nœud du châle et le sac se lisent quand même (ce n'est pas un profil).
- Les cheveux de Roque sont un peu moins gris de dos que de face (illisible à la taille du jeu).
