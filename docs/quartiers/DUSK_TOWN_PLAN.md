# Dusk-Town : plan de la ville (v7)

Rédigé le 21 octobre 2026 (heure de Paris). Base : quartier 1 « La Pompe » (DUSK_TOWN_Q1.md), mêmes règles d'échelle (1 u = 1 m), de caméra (v4) et d'assets.
Légende : **[canon]** = appuyé sur le roman (Ch. I, `src/b`) ou une décision de Valentin ; **[proposition]** = invention de conception, non canon, à valider.

## 1. Plan

```
                 ┌──────────────────────────┐
                 │  Q3  LE SCELLÉ  (nord)   │  bords ouest / est : désert (annoncés)
                 │  accès scellé du labo    │
                 └────────────┬─────────────┘
                     ruelle x=28 (bout sud ↔ bout nord de la ruelle de la pompe)
 désert (piste) ┌─────────────┴────────────┐  avenue z=20  ┌───────────────────────────┐
  ◄── bord ouest│  Q1  LA POMPE  (centre)  │◄────────────►│  Q2  LE TRANSIT  (est)    │── bord est : route des
                └─────────────┬────────────┘               └───────────────────────────┘   patrouilles (annoncée)
                     ruelle x=28 (bout sud de La Pompe ↔ bout nord des Sables)
                 ┌────────────┴─────────────┐
                 │  Q4  LES SABLES  (sud)   │
                 └────────────┬─────────────┘
                     bout sud : terres dévastées (annoncé, sans contenu)
```

Quatre quartiers de 48 × 36 m. Capture du plan rendu : `captures/dusk-v7/plan-global.png`.

| Jonction | Sortie | Arrivée | Cohérence |
|---|---|---|---|
| La Pompe ↔ Le Transit | Q1 (47, 20), passage piéton dans les éboulis, côté sud de l'avenue | Q2 (1, 20) | même avenue, même z |
| La Pompe ↔ Le Scellé | Q1 (28, 1), bout nord de la ruelle de la pompe | Q3 (28, 35), bout sud de la rue du Scellé | même x |
| La Pompe ↔ Les Sables | Q1 (28, 35), bout sud, entre la ruine et les garages | Q4 (28, 1) | même x |

Bouts de rue sans voisin (bords) : Q1 ouest (la piste, existante), Q2 est (route des patrouilles), Q3 ouest et est, Q4 sud (terres dévastées). Ils affichent un texte et ne mènent nulle part.

**Mécanique** : une jonction est une entrée de `DOORS` (`junction: true`, ouverture sur le bord, seuil 1 m à l'intérieur, cible = jonction du quartier voisin). Elle se franchit quand le joueur s'arrête sur le seuil après une marche (tap sur le sol près du bout de rue, sur l'anneau, ou bouton). Transition de groupe atomique (Nilo suit jusqu'à 8 m). Verrou anti-rebond : la jonction d'arrivée ne se redéclenche qu'après s'en être éloigné de 1,5 m. Les étiquettes « Vers … » sont posées hors carte pour ne jamais cacher le joueur.
**État** : un seul état de partie (argent, PV, inventaire, lieux découverts, drapeaux), conservé entre quartiers.

## 2. Ce qui vient du roman

| Élément | Appui | Statut |
|---|---|---|
| Une avenue principale traversante | « l'avenue principale » (Ch. I §107) | [canon] |
| Une patrouille passe par la route | Ch. I §69 ; décision de Valentin : point de passage du Service Militarisé, rafles anti-mutants | [canon] |
| Laboratoire Human Corporation sous la ville, accès verrouillé, portes scellées que beaucoup tentent de forcer | Ch. I §75 | [canon] |
| Sable, herbes mortes, murs délabrés | Ch. I §71 | [canon] |
| Bains de sang entre troupes de récupérateurs | Ch. I §77 | [canon] (évoqué par Ezequiel) |
| Rues vides, habitants et mutants cachés, aucune milice, quelques Los Invictos isolés, dollar | décisions de Valentin (CANON_ARBITRAGES.md) | [canon] |

## 3. Propositions (non canon)
- [proposition] Le découpage en 4 quartiers et leurs noms (Le Transit, Le Scellé, Les Sables).
- [proposition] L'accès au labo est un blockhaus de béton à porte d'acier soudée, au nord de la ville. Le roman dit seulement « sous cette ville » et « l'accès est verrouillé ». Rien n'est dit de ce qu'il y a derrière, et le jeu n'en dit rien non plus.
- [proposition] La route des patrouilles part vers l'est. Le roman ne donne pas la direction.
- [proposition] Les terres dévastées commencent au sud.
- [proposition] Le guetteur et son miroir (signal vers La Pompe), la citerne sous un garage des Sables, la grille d'aération sur le toit du blockhaus.
- [proposition] Les noms Teo, Ezequiel, Sol, « les fils Ortega ».
- [proposition] Aucun nouveau Los Invicto : Ileana (Q1) reste la seule. La consigne « quelques Los Invictos isolés » est donc tenue a minima.

## 4. Quartiers

### Q2 · Le Transit (est)
Fonction : l'avenue où passent les camions. C'est le quartier le plus mort : ici, on ne vit pas, on guette.
Bâtiments (sprites entiers de la maquette, aucun en double dans le quartier) : Le guet (maison à escalier, **visitable**, entrée camouflée par la porte du bas, indice : miroir), Cinéma muré, Dépôt pillé, Relais routier, Ancien marché, Maison basse, Ruine, Station effondrée.
Sol : avenue en asphalte (tuile maquette), bas-côtés ensablés, piste au bout est.
Intérieur `guet_in` (5 × 6 m) : sol en terre, murs enduits, matelas, bureau sous la fente du volet, bac à eau.

**Teo**, 17 ans, guetteur. Phrases courtes, impératifs, il parle en surveillant la fente du volet.
- Désir : être payé en dollars « comme un adulte » et se payer une place sur une caravane.
- Peur : rater un camion.
- Secret : il s'est endormi une fois, et les deux fils Ortega ont été pris. Personne ne sait qu'il était de guet.
- Service : pour 5 $, il dit où trouver quelqu'un au Scellé. Le dialogue révèle L'atelier (son nom s'affiche au Scellé avant même d'y être allé).

### Q3 · Le Scellé (nord)
Fonction : une place de terre battue devant l'accès scellé du labo. Une rue part vers le sud et La Pompe, un chemin traverse d'ouest en est.
Bâtiments : Accès Human Corporation (blockhaus, **généré**, cliquable : message, aucune entrée), Halle, L'atelier (maison basse, **visitable**, indice : clé), Palais muré, Entrepôt, Bâtisse jaune, Ruine, Maison aux garages.
Intérieur `atelier_in` (7 × 6 m) : béton, briques, étagères, brancard, table.

**Ezequiel**, récupérateur, la cinquantaine, boiteux. Voix lente et sèche, il appelle tout le monde « petit ».
- Désir : être le premier à passer la porte. Il ne sait pas ce qu'il y a derrière, et c'est justement pour ça qu'il y tient.
- Peur : entendre une autre bande arriver et ne pas pouvoir courir.
- Secret : sa jambe. Il raconte un combat à six contre un ; il est en fait tombé du toit du blockhaus en voulant desceller une grille, seul, de nuit.

### Q4 · Les Sables (sud)
Fonction : des ruines à moitié ensevelies le long d'une rue de terre qui s'efface. Au bout, la ville s'arrête.
Bâtiments : La citerne (maison aux garages, **visitable** par la petite porte latérale est, indice : goutte), Ruine ensablée, Maison ensablée, Cinéma ensablé, Entrepôt ensablé, Marché ensablé.
Intérieur `citerne_in` (8 × 6 m) : béton, planches, trois bacs d'eau, table, rideau, matelas.

**Sol**, gardienne de la citerne. Calme, ironique, ne dit rien d'elle-même.
- Désir : que la pompe à main tienne, pour que personne n'ait à remonter chercher de l'eau à La Pompe à découvert.
- Peur : les camions, qui « regardent les mains, le cou, les yeux ».
- Secret : elle est mutante (plaque de peau grise et écailleuse sous le foulard, visible sur son sprite). Elle ne le dit jamais ; le joueur peut le comprendre.
- Service : de l'eau à 3 $, moins chère que chez Anselme (non filtrée).

## 5. Règles d'écriture tenues
Chaque PNJ a un désir, une peur et un secret, une voix propre, et aucune tirade d'exposition. Pas de tiret long, pas de tournure « ce n'est pas X, c'est Y » (vérifié par recherche dans `dialogues_town.js`).
