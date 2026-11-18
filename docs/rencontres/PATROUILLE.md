# Rencontre 06 : la patrouille du Service (IO)

Fiche courte (gel de la finition). Consigne : [`CONSIGNE.md`](CONSIGNE.md) §6 rencontre 06, environnement E (poste routier abandonné, scène de bibliothèque). Pas de sprites dans ce lot.

Maquette concept (MAQUETTE, croquis de pose, pas une capture) : `/workspace/nml-shots/rencontres/patrouille_concept.png`. Les containers un peu bleutés de la maquette ne sont pas canoniques : en jeu, rouille et graphite seulement.

## 1. Identité

| | |
|---|---|
| id | `patrouille_io`, préfixe de drapeaux `pat_` |
| Titre | La patrouille du Service (IO) |
| Famille | faction |
| Terrains / biomes | `['piste', 'desert']` / `['desert']` |
| Poids / durée | 1 / 1 h (+1 h si l'inspection s'éternise, §7) |
| Rejouable | oui, sur une autre case (journal par case). Pas unique. |
| Emprise | 32 × 26 m, un seul niveau au sol, zone de combat 19 × 19 entièrement dedans |
| Environnement | `poste_routier` : bibliothèque réutilisable (péages de pillards, camps, négociants, plus tard) |
| Maquette | `/workspace/nml-shots/rencontres/patrouille_concept.png` (MAQUETTE) |

Première mention : **le Service (IO)**, Service Militarisé d'IO, bras armé d'IO.

## 2. Pitch

Un ancien poste, à des kilomètres du dôme. La barrière est baissée. L'adjudant Prato tient un registre que la poussière a déjà gagné. Il applique, avec un sérieux sans fissure, un règlement qui n'a plus de bureau pour le recevoir. Kenn tient la barrière. Orel fume du côté du local technique, et c'est par là qu'on peut éviter tout le monde. Selon qui l'on est, on passe, on paie une catégorie qui n'existe pas, ou on se fait tirer dessus.

## 3. Décor (bibliothèque E)

Piste est–ouest, entrée à l'est. Le poste enjambe la piste : guérite au nord, barrière baissée, sacs de sable, véhicule de contrôle stationné à l'est de la guérite. Au sud : containers et un local technique éventré (stockage, passage pour contourner). Rien n'est neuf. Ce n'est pas le dôme : c'est une guérite perdue, cohérente avec le canon (une guérite « à plusieurs kilomètres du dôme »).

Les éléments (barrages, guérites, véhicules de contrôle, containers, bâtiments techniques, zones de stockage) restent en place pour d'autres occupations plus tard : on change les PNJ et quelques caisses, pas le gros œuvre.

**Clés réutilisées** (désert du pilote / de la caravane) : `g_rc_sable` `_b` `_c`, `g_rc_piste` `_b` `_c`, `rc_ds_talus_a/b/fin_3q`, `rc_ds_rochers_3q` `_b`, `rc_ds_panneau_ufsa_3q`, `rc_car_ferraille_3q`, `rc_car_traces_3q`.

**Ne pas réutiliser** comme véhicule de la patrouille : `rc_emb_epave_service_3q`, `rc_emb_pickup_appat_3q`, `rc_vr_blinde_vitrifie_3q`, le tracteur de Remedios.

**Clés nouvelles**, préfixe `rc_pr_` (poste routier, bibliothèque) :

| Clé | Rôle |
|---|---|
| `rc_pr_guerite_3q` | Guérite rouillée, guichet, registre |
| `rc_pr_barriere_3q` | Barrière / lisse baissée en travers de la piste |
| `rc_pr_sacs_3q` | Barrage de sacs de sable (`_b` si besoin) |
| `rc_pr_vehicule_3q` | Véhicule de contrôle du Service (IO), roues au sol, bande pochoir rouille-oxyde, graphite et laiton sale |
| `rc_pr_container_3q` `_b` | Containers de stockage, rouille et graphite, pas de bleu |
| `rc_pr_local_3q` | Bâtiment technique éventré, passage sur le flanc |
| `rc_pr_caisse_3q` | Caisses de la zone de stockage |
| `gen_rc_prato` / `_dos` / portrait | Adjudant Prato |
| `gen_rc_kenn` / `_dos` / portrait | Soldat Kenn |
| `gen_rc_orel` / `_dos` / portrait | Soldat Orel |

Lampe de la guérite : `_neon` + enseigne, seule source la nuit.

## 4. Variantes

Pas de variante de décor dans ce lot. L'attitude de la patrouille change selon la race, l'implant, et quelques drapeaux de monde (§7, répliques seulement).

## 5. PNJ

**Adjudant Prato**, le registre. Il veut une ligne propre. Il ne plaisante pas, et le règlement qu'il cite n'a plus d'administration derrière lui. C'est lui qui inspecte, qui parle, qui invente une « catégorie provisoire » s'il le faut.

**Soldat Kenn**, à la barrière. Il s'ennuie. Il lève la lisse quand Prato signe, et il tire si Prato le dit.

**Soldat Orel**, du côté du local et des containers. Moins attentif. C'est lui qu'on évite, ou qu'on croise si le détour rate.

Trois motivations distinctes, pas un bloc unique « soldats méchants ».

## 6. Dialogues (courts, sérieux bureaucratique)

Prato, départ, si le joueur n'est pas encore signalé comme mutant vu : « Itinéraire. Destination. Et l'immatriculation, si tu en as une. On ne retient personne sans motif. On ne laisse passer personne sans motif non plus. »

- Inspection, selon le cas (§7).
- Discuter : « C'est un poste abandonné. » — « Le poste, peut-être. Le règlement, non. »
- Mentir (`parole`) : un itinéraire inventé, un motif de transit. Succès variable selon qu'on a un implant ou non.
- Montrer une autorisation : l'autorisation que le système connaît, c'est **l'implant** (`if: 'implant'`). Prato approche un boîtier râpé, une diode ambre, pas un écran bleu. « Référencé. Tu peux passer. Reste sur la piste. » La `plaque` de camion du Service n'est pas une autorisation : « C'est une plaque de véhicule. Où est le véhicule ? » (`parole` 5 pour s'en tirer, sinon soupçon, pas de quête).
- Si `monde_mateo_pris` : en feuilletant, « On a sorti un gamin de la forêt, récemment. Fiche d'accompagnement. Ce n'est pas toi. » Indice seulement.
- Si `monde_lena_connue` ou `monde_remedios_vue` : « Des listes circulent. Des passagers qu'on n'a pas comptés. On ne te les lit pas. » Indice seulement, aucune conséquence de quête.
- Si `monde_message_ines` : rien de plus qu'une formule du même genre. On n'ouvre pas de quête.

Pas d'arbre long. Pas d'exposé sur IO.

## 7. Issues

Le joueur n'est forcé ni de parler ni de se battre à l'arrivée. Un mutant peut (et doit pouvoir) tenter le détour sans s'annoncer.

- **Se soumettre à l'inspection.**
  - `implant` (augmenté, cyborg) : scan, questions, parfois +1 h (« mise à jour d'itinéraire » qui ne part nulle part). Puis la barrière se lève, `pat_laisse`.
  - Humain, sans implant : « biomasse non référencée, catégorie provisoire ». 10 $, ou `parole` 4. Succès : `pat_laisse`. Échec : Kenn se rapproche, on peut payer 15 $, partir en demi-tour, ou résister.
  - Mutant, s'il se présente ou s'il est vu de face : le Service (IO) tire à vue (canon, `CANON_ARBITRAGES`, fiche de race). Combat, §8. Pas de négociations une fois l'arme levée.
- **Discuter / mentir.** Voir §6.
- **Montrer une autorisation.** L'implant, s'il y en a un. Pas de laissez-passer papier dans le jeu pour l'instant ; on n'en invente pas.
- **Éviter les soldats.** Détour sud, derrière les containers et le local, discrétion 4 (5 si on passe près d'Orel). Succès : sortie ouest ou est sans inspection, `pat_evite`. Échec : Orel donne l'alerte — inspection forcée, ou combat si `race_mutant`.
- **Résister.** Combat optionnel, §8.
- **Demi-tour** par la sortie est, sans traverser, toujours possible tant que le combat n'a pas commencé.

## 8. Combat

Seulement si l'on résiste, si un mutant est vu, ou si l'alerte part et qu'on refuse l'inspection. Prato (pistolet), Kenn (fusil), Orel (fusil), positions à la guérite, à la barrière et au véhicule (couvert). Ils ne se rendent pas facilement ; sous 50 %, Prato peut crier une pause et exiger que l'on parte (`pat_chasse`). Zone 19 × 19. Issue habituelle : victoire, fuite par une sortie libre, défaite (perte d'argent / objet, reprise du trajet, pas de quête nouvelle).

## 9. Objets

Aucun objet nouveau. L'implant est un flag de personnage, pas un objet d'inventaire. La `plaque` déjà existante n'est pas un sauf-conduit. Pas de butin obligatoire ; sur le soldat ou dans une caisse du local, au plus 1 × `ration` ou quelques dollars, une fois, si l'on fouille après une victoire ou un détour réussi (discrétion).

## 10. Lumière

Courbe `desert`. Le jour, le soleil. La nuit, une seule source : la lampe de la guérite (`_neon` + enseigne, flaque générique r 1,5, ambre sale, nuit seulement). Le boîtier de scan, le jour, a une petite diode ambre sur un boîtier visible, pas un halo, pas un écran cyan. Le véhicule n'allume ses phares que si l'on en fait plus tard une source (phase D : ce n'est pas nécessaire tant que la guérite éclaire).

## 11. DA

Palette du désert (ocre, rouille, beige poussiéreux) **plus un accent IO** : graphite, laiton / ambre sale, bande au pochoir d'un rouge-oxyde foncé. **Pas de violet, pas de cyan**, même pour une faction d'IO. Pas d'écrans holographiques, pas de gyrophares bleus. Les containers sont rouille et graphite. Décision DA à signaler au §13.

La scène est conçue comme bibliothèque : le poste reste, l'occupation change. Composition lisible depuis l'entrée (barrière, guérite, véhicule), détour lisible au sud sans être un couloir vide. Maquette simple, pas une cible de pixels.

## 12. Câblage pour Rivet

- Catalogue : `patrouille_io`, `famille: 'faction'`, `prefixe: 'pat_'`, `terrains: ['piste', 'desert']`, `biomes: ['desert']`, `poids: 1`, `duree: 1` (+1 h si inspection longue avec implant).
- Drapeaux de scène `pat_*` remis à zéro à la sortie. Pas de nouveau `monde_*` dans ce lot : on **lit** `implant`, `race_mutant`, `race_humain`, `inv:plaque`, `monde_mateo_pris`, `monde_lena_connue`, `monde_remedios_vue`, `monde_message_ines`. Répliques et indices seulement, aucune conséquence de quête (garde-fou de Régie).
- Journal par case : `{ id }`. Pas de `si` d'unicité.
- Sortie est : reprise. Sortie ouest : halte. La barrière, tant qu'elle est baissée et que l'on n'a pas `pat_laisse` ni `pat_evite`, bloque le milieu de la piste (on passe par le détour, ou on fait demi-tour).
- DEV : `?rencontre=patrouille_io`, et pouvoir forcer une race / un implant pour tester les trois inspections.
- Combat : id `patrouille_io`. Sprites et gros œuvre du poste en gabarits gris acceptables. Pas de poses définitives avant les sprites (§15).
- Le boîtier de scan n'a pas besoin d'un nouveau système : c'est un texte et, au plus, une petite diode sur le décor de la guérite.

## 13. Décisions de DA et de lore à signaler à Valentin

1. Première mention : **le Service (IO)**, Service Militarisé d'IO, bras armé d'IO. Cette patrouille est bien la 06 de la consigne.
2. Cohérence politique et technique (`CANON_ARBITRAGES`) : implants d'immatriculation (l'autorisation que le jeu connaît déjà) ; humain = biomasse non référencée ; mutant abattu à vue hors Sous-Ville ; poste = guérite à plusieurs kilomètres du dôme, pas la douane de Steel.
3. **Accent visuel IO**, décision DA : graphite, laiton / ambre sale, rouge-oxyde au pochoir. Pas de cyan, pas de violet, même pour IO.
4. Noms nouveaux : Adjudant Prato, Soldat Kenn, Soldat Orel.
5. Pas de laissez-passer papier nouveau. La plaque de camion n'en est pas un.
6. Antécédents (`monde_lena_connue`, `monde_mateo_pris`, etc.) : répliques et indices seulement.
7. Le poste est une **scène de bibliothèque** (consigne §5.E), réutilisable plus tard pour un péage de pillards ou un camp. Seuls les PNJ et quelques caisses changeront.

## 14. Entrée au format d'ARCHI.md §4

Poses définitives au §15, après les sprites. Positions indicatives.

```js
patrouille_io: {
  nom: 'La patrouille du Service (IO)', famille: 'faction', prefixe: 'pat_',
  terrains: ['piste', 'desert'], biomes: ['desert'], poids: 1, duree: 1, // +1 h si inspection longue
  arrivee: 'Un ancien poste, la barrière baissée. Quelqu\'un écrit dans un registre. Quelqu\'un d\'autre tient la lisse.',
  scene: { size: { w: 32, d: 26 },
    ground: { skin: 'g_rc_sable', tint: null, paint: [ /* bande g_rc_piste z 14-19 ; variantes _b/_c */ ] },
    ambiance: 'desert',
    buildings: [
      // guérite, local, containers, véhicule, barrière : poses au §15
    ],
    props: [
      // sacs, caisses, traces, panneau : poses au §15
    ],
    entrees: [{ id: 'entree', x: 30.5, z: 16, side: 'east' }],
    sorties: [
      { id: 'S_E', x: 31.5, z: 14, w: 0.5, d: 5, rencontre: true, reprise: true },
      { id: 'S_O', x: 0, z: 14, w: 0.5, d: 5, rencontre: true }
    ],
    enseignes: [{ id: 'pat_lampe', building: 'rc_pr_guerite_3q', effet: 'pulse', periode: 6, intensite: 0.5,
      flaque: { r: 1.5, couleur: '#d4a05a', i: 0.4 } }] // nuit seulement ; ambre sale
  },
  pnj: [
    { id: 'pat_prato', name: 'Adjudant Prato', sprite: 'gen_rc_prato', x: 12.2, z: 12.8, faceTo: [30.5, 16], dialogue: 'pat_prato' },
    { id: 'pat_kenn', name: 'Kenn', sprite: 'gen_rc_kenn', x: 16.5, z: 15.2, faceTo: [30.5, 16], dialogue: 'pat_kenn' },
    { id: 'pat_orel', name: 'Orel', sprite: 'gen_rc_orel', x: 22.0, z: 21.5, faceTo: [20, 20], dialogue: 'pat_orel' }
  ],
  // dialogues : §6 ; détour : §7 ; combat : §8
}
```

## 15. Poses définitives et sprites publiés

Après les sprites. Ce lot n'en produit pas.
