# Rencontre 05 : les mutants errants

Fiche courte (gel de la finition). Consigne : [`CONSIGNE.md`](CONSIGNE.md) §6 rencontre 05, environnement D (zone vitrifiée). Groupe hostile, distinct des Verriers. Pas de sprites dans ce lot.

Maquette concept (MAQUETTE, croquis de pose, pas une capture) : `/workspace/nml-shots/rencontres/errants_concept.png`. Les touffes pâles de la maquette ne sont pas canoniques : en jeu, on réutilise les dalles et les éclats brun-noir / vert bouteille déjà publiés.

## 1. Identité

| | |
|---|---|
| id | `errants_verre`, préfixe de drapeaux `err_` |
| Titre | Les Brûlés |
| Famille | hostiles (mutants déments, type d'adversaire de la maquette v0.13) |
| Terrains / biomes | `['verre']` / `['glass']` (dans le verre, pas sur la piste de l'écluse) |
| Poids / durée | 1 / 1 h |
| Rejouable | oui, sur une autre case (journal par case). Disposition tirée à l'arrivée. |
| Emprise | 32 × 26 m, un seul niveau au sol, zone de combat 19 × 19 entièrement dedans |
| Maquette | `/workspace/nml-shots/rencontres/errants_concept.png` (MAQUETTE) |

## 2. Pitch

Une poche de croûte chaude, au milieu du verre. Trois figures tournent autour, s'arrêtent, écoutent. Ce ne sont pas une horde, et ce ne sont pas les Verriers. Les Verriers les appellent les Brûlés : des gens restés trop longtemps sur la plaque, qui ont gardé le corps et perdu le fil. On peut les contourner, glisser en silence, jeter un bruit ailleurs, se battre, ou partir.

## 3. Décor

Plaine vitrifiée, sans le canal ni l'écluse. Entrée à l'est. Au centre, une poche plus sombre (croûte, sel, pas de lueur). Une carcasse civile à demi prise dans le verre, un peu au sud. Dalles soulevées pour le couvert. Éclats sur quelques passages : ils sont bruyants (§7, §12).

**Clés réutilisées** (groupe `rc_ecluse_verriers`, modules `rc_vr_*` et sols) : `g_rc_verre` `_b` `_c`, `g_rc_cendre` `_b`, `rc_vr_dalles_3q` `_b`, `rc_vr_eclats_3q` `_b` `_c` et leurs `_reflet` (jour seulement, le verre ne luit pas), `rc_vr_plaques_3q`, `rc_vr_aretes_3q`, `rc_vr_aiguilles_3q` `_b`, `rc_vr_coulures_3q`.

**Ne pas réutiliser** : le four, la cabane, la péniche, les portes d'écluse, les parapets, le quai, le limon, le blindé du Service et son calque à la craie, les Verriers, les chanchos. Trop liés à l'écluse.

**Clés nouvelles** (à produire après cette fiche) :

| Clé | Rôle |
|---|---|
| `rc_err_carcasse_3q` | Carcasse civile prise dans le verre (nid, fouillable, couvert) |
| `rc_err_croute_3q` | Décalque de la poche chaude (`fond: true`) : verre plus sombre, sel, pas d'émission |
| `rc_err_ferraille_3q` | Ferraille lançable (boîte, fragment), 2 ou 3 poses |
| `gen_rc_brule_a` / `_dos` | Variante « l'écouteur » (yeux laiteux, tête tournée) |
| `gen_rc_brule_b` / `_dos` | Variante « l'osseux » (crêtes, plaques) |
| `gen_rc_brule_c` / `_dos` | Variante « le marcheur » |

Pas de portraits parlants : ils n'ont pas de dialogue d'arbre. Un examen de près suffit.

## 4. Dispositions variables

Même décor, mêmes trois figures, trois placements tirés à l'arrivée (le DEV peut forcer).

| Disposition | Mise en place | Ce qui change |
|---|---|---|
| `ronde` | Ils tournent autour de la poche, un peu écartés | Contourner par le bord, ou jeter au centre et glisser |
| `nid` | Deux à la carcasse, un sentinelle vers l'entrée | Distraire la sentinelle, passer derrière l'épave |
| `file` | Une ligne en travers de la bande, entre l'entrée et la sortie ouest | Plus dur à contourner ; un bruit à une extrémité ouvre un trou |

## 5. PNJ / adversaires

Trois mutants humains, type de combat « mutants déments » (maquette v0.13). Ce sont des gens malades, pas des morts-vivants : vêtements usés, peaux marbrées, yeux laiteux, plaques ou crêtes (même famille visuelle que Lena ou Rufina, plus avancée). Ils ne parlent presque plus. L'écouteur, si on s'approche sans être vu, peut laisser échapper « chaud… » ou un nom qu'on n'éclaircit pas.

Ils tiennent un territoire (la poche). Ils chassent au bruit plus qu'à la vue. Ils n'attaquent pas d'office à l'arrivée : tant qu'on reste hors de la ronde et qu'on ne fait pas de bruit, la scène reste exploratoire.

Les Verriers (pacifiques) les redoutent et ne sont pas dans cette scène.

## 6. Dialogues

Pas d'arbre. Examens courts : la poche (« trop chaude pour s'y tenir longtemps »), la carcasse, un éclat, une figure de loin. Si `monde_verriers_vus` : le texte peut rappeler que Balta en a parlé comme d'une chose à éviter, sans nouvelle quête.

## 7. Issues

Le joueur n'est forcé ni de parler ni de se battre à l'arrivée.

- **Se déplacer discrètement.** Marcher hors des éclats, ou les traverser avec discrétion 4. Un échec, ou une course sur un éclat, fait un bruit à la position du joueur (§12).
- **Contourner.** Possible surtout en `ronde` et en `nid` : la sortie ouest reste accessible sans croiser la ronde, si l'on reste au bord.
- **Attirer leur attention ailleurs.** Lancer une ferraille sur une case visée. Ils quittent leur ronde, vont au bruit, restent un moment, reprennent la ronde s'ils n'ont vu personne. Décrit pour Rivet au §12, **à ne pas implémenter dans ce lot**. En attendant, un examen « lancer » peut poser un flag et un texte, ou rester indiqué comme action prévue.
- **Combattre.** Si on les attaque, ou s'ils voient le joueur dans le territoire, ou s'ils arrivent au bruit et le trouvent. Combat tactique existant, §8.
- **Fuir.** Avant le combat : sortir par l'est (reprise) ou l'ouest (halte). Pendant le combat : la règle habituelle (sortie tenue tant qu'un hostile la contrôle ; fuite si l'on atteint une sortie libre).

## 8. Combat

Trois adversaires « mutants déments », au corps à corps (un peut jeter un éclat, portée courte). Positions selon la disposition, à ≥ 8 m de l'entrée, répartis, sur cases libres. Couvert : dalles, carcasse. Ils ne négocient pas, ils ne se rendent pas. On peut fuir (§7). Zone 19 × 19.

## 9. Objets

Existants seulement. Dans la carcasse, une fois : 1 × `ration`, ou 4 $. Rien d'autre. Pas d'objet de quête.

## 10. Lumière

Courbe `glass` déjà en place. Le jour, le soleil, et les `_reflet` des éclats (1 − lune, jamais une émission). La nuit, pas de lampe : la poche ne luit pas. Une nuit sur le verre est simplement sombre.

## 11. DA

Même palette que l'écluse : brun-noir, vert bouteille sale, sel, rouille, ocre. Pas de cyan, pas de violet, pas de lueur. Les trois silhouettes restent lisibles comme des gens, pas comme une horde identique. La maquette est un croquis de territoire (poche, ronde, carcasse) ; les cristaux pâles du croquis ne se produisent pas.

## 12. Câblage pour Rivet

- Catalogue : `errants_verre`, `famille: 'hostiles'`, `prefixe: 'err_'`, `terrains: ['verre']`, `biomes: ['glass']`, `poids: 1`, `duree: 1`.
- Disposition tirée à l'arrivée : `ronde` | `nid` | `file`. Le DEV doit pouvoir la forcer.
- Drapeaux de scène `err_*` remis à zéro à la sortie. Optionnel, répliques seulement : `monde_errants_vus` à la sortie (pour une réplique des Verriers plus tard, garde-fou de Régie).
- Journal par case : `{ id, disposition }`. Pas de `si` d'unicité.
- Sortie est : reprise. Sortie ouest : halte.

**« Attirer leur attention ailleurs »** (contrat, à ne pas coder dans ce lot) :

1. Une action `bruit:x:z` (lancer une `rc_err_ferraille_3q`, ou l'équivalent), qui pose une source sonore aux coordonnées visées, rayon ~6 m, durée courte (quelques secondes ou 1–2 tours).
2. Une machine d'états simple pour ces trois hostiles, **sans nouveau moteur** : `ronde` (points de passage de la disposition) → `enquete` (ils marchent vers le bruit, s'arrêtent, regardent) → `ronde` s'ils n'ont vu personne, ou `combat` s'ils voient le joueur. Le combat existant reprend ensuite.
3. Détection : la vue (ligne de vue, dans le territoire) **ou** le bruit. Un déplacement sur un décor `bruyant: true` (les éclats) fait un bruit à la position du joueur, sauf si un test de discrétion 4 réussit. La course ignore le test.
4. En attendant cet état, la scène peut se jouer en combat à l'attaque, et en sortie libre tant qu'on n'est pas vu (les textes portent le reste).

- Combat : id `errants_verre`. Sprites en gabarits gris acceptables. Pas de poses définitives avant les sprites (§15).

## 13. Décisions de DA et de lore à signaler à Valentin

1. **Les Brûlés**, nom que leur donnent les Verriers. Adversaires de combat : « mutants déments » (maquette v0.13). Ce sont des mutants humains malades, pas des bêtes, pas les Féraux-horde écartés dans [MUTANTS.md §13](MUTANTS.md#13-décisions-de-da-et-de-lore-à-signaler-à-valentin). C'est le traitement rare annoncé alors : des gens, jamais une masse sans motif.
2. **Cause de la démence**, cohérente avec le canon : le verre de Big Larry est supportable pour un mutant (`radResist`, territoire déjà proposé au §13 de MUTANTS), mais les poches de croûte chaude (contamination, consigne §5.D) brûlent l'esprit si l'on s'y tient. Les Verriers le savent et campent au bord. Ceux qui restent, ou que une rafle a poussés trop loin, deviennent les Brûlés. À valider.
3. Les Verriers restent une communauté pacifique, absente de cette scène, et les redoutent.
4. Terrains `['verre']` seulement, pour ne pas les tirer sur la piste de l'écluse.
5. `monde_errants_vus` : répliques seulement.
6. Le Service (IO) n'entre pas dans cette scène (cohérent avec « le Service n'entre pas dans le verre », déjà soumis).

## 14. Entrée au format d'ARCHI.md §4

Poses définitives au §15, après les sprites. Positions indicatives, disposition `ronde`.

```js
errants_verre: {
  nom: 'Les Brûlés', famille: 'hostiles', prefixe: 'err_',
  terrains: ['verre'], biomes: ['glass'], poids: 1, duree: 1,
  // disposition tirée à l'arrivée : ronde | nid | file
  arrivee: 'Le verre craque sous la semelle. Plus loin, trois figures tournent autour d\'une croûte plus sombre. Elles s\'arrêtent. Elles écoutent.',
  scene: { size: { w: 32, d: 26 },
    ground: { skin: 'g_rc_verre', tint: null, paint: [ /* variantes _b/_c ; poche plus sombre au centre */ ] },
    ambiance: 'glass',
    buildings: [ /* dalles, carcasse : poses au §15 */ ],
    props: [ /* éclats bruyants, arêtes, ferraille lançable, croûte : poses au §15 */ ],
    entrees: [{ id: 'entree', x: 30.5, z: 16, side: 'east' }],
    sorties: [
      { id: 'S_E', x: 31.5, z: 14, w: 0.5, d: 5, rencontre: true, reprise: true },
      { id: 'S_O', x: 0, z: 14, w: 0.5, d: 5, rencontre: true }
    ]
  },
  pnj: [
    // trois Brûlés, positions de la disposition ; dialogue: null ; hostiles une fois err_alerte
  ],
  // examens : §6–§7 ; combat : §8 ; bruit : §12 (plus tard)
}
```

## 15. Poses définitives et sprites publiés

Après les sprites. Ce lot n'en produit pas.
