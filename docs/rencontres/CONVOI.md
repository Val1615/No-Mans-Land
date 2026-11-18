# Rencontre 01 : le convoi ensablé

Fiche courte (gel de la finition). Consigne : [`CONSIGNE.md`](CONSIGNE.md) §6 rencontre 01, environnement A (route désertique). Une seule scène réutilisable, quatre cargaisons. Pas de sprites dans ce lot.

Maquette concept (MAQUETTE, croquis de pose, pas une capture) : `/workspace/nml-shots/rencontres/convoi_concept.png`. Le panneau anglais de la maquette n'est pas canonique : en jeu, on réutilise `rc_ds_panneau_ufsa_3q` couché, ou une clé tombée si le sprite debout ne se couche pas.

## 1. Identité

| | |
|---|---|
| id | `convoi_ensable`, préfixe de drapeaux `cv_` |
| Titre | Le convoi ensablé |
| Famille | convoi |
| Terrains / biomes | `['piste', 'desert']` / `['desert']` (tirage terrain + biome, comme le reste du catalogue) |
| Poids / durée | 1 / 1 h (+1 h si l'on aide à dégager, §7) |
| Rejouable | oui, sur une autre case (journal par case). Pas unique. La variante est tirée à l'arrivée. |
| Emprise | 30 × 24 m, un seul niveau au sol, zone de combat 19 × 19 entièrement dedans |
| Maquette | `/workspace/nml-shots/rencontres/convoi_concept.png` (MAQUETTE) |

## 2. Pitch

Un camion civil a quitté la piste tassée là où un panneau UFSA est tombé. La langue de sable a pris les essieux. Nando s'acharne sur un cric déjà à demi enterré. Sola ne quitte pas les caisses. Quatre cargaisons possibles, un seul décor : médical, eau, pièces, ou de la contrebande qui n'a rien à voir avec la filière de Remedios.

## 3. Décor

Piste est–ouest (z 14–19), entrée à l'est sur la piste, à ≥ 8 m du camion. Le camion est au sud de la piste, dans une langue de sable : ornières qui quittent la bande tassée, panneau UFSA couché, cric enfoncé, planches sous une roue arrière. Le décor doit dire pourquoi le camion est coincé, pas seulement qu'il l'est.

**Clés réutilisées** (groupes `rc_pilote_appat` et `rc_caravane`) : `g_rc_sable` `_b` `_c`, `g_rc_piste` `_b` `_c`, `rc_ds_talus_a/b/fin_3q`, `rc_ds_rochers_3q` `_b`, `rc_ds_panneau_ufsa_3q` (couché, ou nouvelle clé si besoin), `rc_car_ferraille_3q`, `rc_car_traces_3q`.

**Ne pas réutiliser** comme camion : `rc_car_tracteur_3q`, `rc_car_citerne_3q`, `rc_emb_pickup_*`, `rc_emb_epave_service_3q` (identité trop marquée).

**Clés nouvelles** (à produire après cette fiche) :

| Clé | Rôle |
|---|---|
| `rc_cv_camion_3q` | Camion bâché civil, essieux dans le sable, portes arrière refermables visuellement |
| `rc_cv_cric_3q` | Cric à demi enterré (examinable) |
| `rc_cv_planches_3q` | Planches sous une roue |
| `rc_cv_langue_3q` | Décalque : langue de sable et ornières qui quittent la piste (`fond: true`) |
| `rc_cv_caisse_med_3q` | Caisse de la variante médicale |
| `rc_cv_caisse_eau_3q` | Bidons / caisse de la variante eau |
| `rc_cv_caisse_pieces_3q` | Caisse de la variante pièces |
| `rc_cv_caisse_contre_3q` | Caisse anonyme de la variante contrebande |
| `rc_cv_panneau_tombe_3q` | Seulement si `rc_ds_panneau_ufsa_3q` ne peut pas être posé couché |
| `gen_rc_nando` / `_dos` / portrait | Chauffeur-mécano |
| `gen_rc_sola` / `_dos` / portrait | Garde de la cargaison |

Une seule caisse visible à la fois, selon la variante.

## 4. Variantes

Même scène, mêmes PNJ, mêmes issues. Changent : la caisse, deux ou trois répliques, le stock et la récompense.

| Variante | Cargaison | Stock (objets existants, prix de piste) | Récompense si l'on aide |
|---|---|---|---|
| `medical` | Caisses de soins | `bandage` (nouveau, 8 $), `water` (6 $) | 1 × `bandage` |
| `eau` | Bidons d'eau filtrée | `water` (5 $) | 1 × `water` |
| `pieces` | Pièces de rechange | rien à vendre (ils en ont besoin) | 8 $ |
| `contrebande` | Lampes de radio sans tampon, pour un atelier de la Sous-Ville | `tubes_radio` (nouveau, 12 $, seulement si Troc ou Parole) | 10 $, et Sola veut qu'on parte |

La contrebande n'est pas la filière de Remedios, ni un convoi du Service (IO). Ce sont des civils qui roulent pour un atelier, pas pour un réseau.

## 5. PNJ

**Nando**, chauffeur et mécano. Il veut juste sortir le camion avant la nuit. Il refuse la charité, accepte un coup de main ou le prêt du `cric` du joueur (s'il l'a, celui d'Anselme convient : clin d'œil, pas une quête). Debout ou accroupi au cric.

**Sola**, responsable de la cargaison. Elle négocie, elle surveille, elle ne s'éloigne pas des caisses. Pas hostile d'office. Une seule mention du Service (IO), si le joueur l'invoque : elle n'a aucune envie de voir une patrouille.

Deux personnes, pas une escorte militaire.

## 6. Dialogues (courts)

Nando, départ : « Le cric s'enfonce plus vite que le camion ne monte. Tu regardes, ou tu pousses ? »

- « Je pousse. » → aide (§7).
- « Qu'est-ce que vous transportez ? » → il renvoie à Sola.
- « Je peux vendre ou acheter. » → Sola.
- « Je n'ai rien à faire ici. » → fin, on peut partir.

Sola, départ : « Tu t'approches des caisses, tu parles d'abord. »

- Négocier une récompense avant d'aider (`parole` 4 : elle promet la récompense de la variante ; échec : « Tu aides, ou tu parcours. »).
- Troquer, stock de la variante.
- Variante contrebande, si on insiste : « Des lampes. Pour un atelier, en bas de Steel. Ce n'est écrit nulle part, et ça m'arrange. »
- Si le joueur parle d'un convoi du Service (IO) : « Si c'est le Service (IO) que tu ramènes, tu rentres dans le sable, pas moi. »

Pas d'arbre long. Pas d'exposition sur les factions.

## 7. Issues

Le joueur n'est forcé ni de parler ni de se battre à l'arrivée.

- **Aider.** Pas de compétence nouvelle. Coût : +1 h, ou le `cric` du joueur s'il l'a (le temps ne s'ajoute pas : le cric de Nando est déjà perdu dans le sable). Succès : récompense de la variante, `cv_aide`, le camion reste coincé visuellement (pas de sprite « dégagé » dans ce lot).
- **Négocier** la récompense, puis aider.
- **Troquer** le stock de la variante (Sola).
- **Examiner** la cargaison (portes arrière, ou caisse) : Observation 3, ou libre si `cv_aide`. Texte selon la variante.
- **Voler** avec discrétion 5. Succès : 1 objet de la variante (`bandage` / `water` / 8 $ en pièces détachées sous forme d'argent / `tubes_radio`), `cv_vole`. Échec : Sola dégaine → combat, ou on peut payer 15 $ pour clore (`cv_vu`).
- **Attaquer** : combat optionnel, §8.
- **Ignorer / partir** par une sortie, sans flag d'aide.

## 8. Combat

Seulement si l'on attaque, ou si le vol échoue et qu'on refuse de payer. Nando (barre de fer) et Sola (pistolet), positions derrière le camion et les caisses (couvert). Ils se rendent sous 50 %. Pas d'ennemis d'office. Zone 19 × 19, le camion est une couverture.

## 9. Objets

Existants : `water` « Eau filtrée », `ration`, `cric` « Cric de camion », dollars, armes du combat (`barre`, `pistolet`) si prises.

Nouveaux, à ajouter au catalogue d'objets :

- `bandage` : « Bande de toile », soin léger (même famille que `ration` / `water`, pas un objet de quête).
- `tubes_radio` : « Lampes de radio », sans effet, sans quête.

## 10. Lumière

Courbe `desert` existante (`ambiance('desert', heures)`). Le jour, le soleil suffit. La nuit, une seule source : une lampe de travail accrochée au battant arrière (`_neon` + enseigne, flaque générique r 1,5, nuit seulement). Pas de halo sans source.

## 11. DA

Palette du pilote et de la caravane : ocre, rouille, beige poussiéreux, olive-gris. Pas de cyan, pas de violet. Le camion est un civil rouille-rouge délavé, lisible depuis l'entrée, distinct du pick-up de l'appât, du tracteur de Remedios et de l'épave du Service (IO). Composition fermée par les rochers et le talus, piste ouverte aux deux bouts. La maquette est un croquis simple, pas une cible de pixels.

## 12. Câblage pour Rivet

- Catalogue : `convoi_ensable`, `famille: 'convoi'`, `prefixe: 'cv_'`, `terrains: ['piste', 'desert']`, `biomes: ['desert']`, `poids: 1`, `duree: 1` ( +1 h si `cv_aide` et sans `cric` prêté).
- Variante tirée à l'arrivée parmi `medical`, `eau`, `pieces`, `contrebande` ; le DEV doit pouvoir la forcer (`?rencontre=convoi_ensable&variante=eau`, ou l'équivalent déjà en place).
- Drapeaux de scène `cv_*` remis à zéro à la sortie (comme `emb_*`, `car_*`).
- Drapeaux de monde, répliques seulement (garde-fou de Régie) : `monde_cv_aide`, `monde_cv_vole`. Posés à la sortie si les flags de scène correspondants sont là.
- Journal par case : `{ id, variante }`. Pas de `si` d'unicité.
- Sortie est : reprise du trajet. Sortie ouest : halte. Textes courts.
- Objets nouveaux : `bandage`, `tubes_radio` (§9). Le prêt du `cric` ne le consomme pas (le joueur le récupère).
- Combat : id `convoi_ensable`, deux adversaires, reddition sous 50 %.
- Sprites : gabarits gris acceptables tant que les clés du §3 sont réservées. Pas de poses définitives avant les sprites (§15).

## 13. Décisions de DA et de lore à signaler à Valentin

1. **Alignement (question de Régie).** « Le Service » des fiches est le Service Militarisé d'IO, bras armé d'IO. Première mention, ici et dans les dialogues : « le Service (IO) ».
2. **Nando et Sola** sont des transporteurs civils indépendants, sans faction. Noms nouveaux.
3. **Quatre variantes de cargaison** sur une seule scène-bibliothèque (consigne §5). La contrebande (lampes de radio pour un atelier de la Sous-Ville) n'étend pas la filière de Remedios, ni Mateo, ni les Verriers.
4. **Objets nouveaux** `bandage` et `tubes_radio` : pas des objets de quête.
5. **Drapeaux `monde_cv_*`** : répliques et indices seulement, tant que Valentin n'a pas validé de suite.
6. Le panneau tombé est un débris UFSA, pas un commentaire politique.

## 14. Entrée au format d'ARCHI.md §4

Poses définitives au §15, après les sprites. Positions indicatives, en mètres, ancre des décors au coin sud-est.

```js
convoi_ensable: {
  nom: 'Le convoi ensablé', famille: 'convoi', prefixe: 'cv_',
  terrains: ['piste', 'desert'], biomes: ['desert'], poids: 1, duree: 1, // +1 h si cv_aide sans cric
  // variante tirée à l'arrivée : medical | eau | pieces | contrebande
  arrivee: 'Un camion a quitté la piste. Les essieux sont dans le sable. Quelqu\'un s\'acharne sur un cric. Quelqu\'un d\'autre ne quitte pas les caisses.',
  scene: { size: { w: 30, d: 24 },
    ground: { skin: 'g_rc_sable', tint: null, paint: [ /* bande g_rc_piste z 14-19 ; variantes _b/_c */ ] },
    ambiance: 'desert',
    buildings: [
      // camion, talus, rochers, panneau couché : poses au §15
    ],
    props: [
      // cric, planches, traces, caisse de la variante, ferraille : poses au §15
    ],
    entrees: [{ id: 'entree', x: 28.5, z: 16, side: 'east' }],
    sorties: [
      { id: 'S_E', x: 29.5, z: 14, w: 0.5, d: 5, rencontre: true, reprise: true },
      { id: 'S_O', x: 0, z: 14, w: 0.5, d: 5, rencontre: true }
    ],
    enseignes: [{ id: 'cv_lampe', building: 'rc_cv_camion_3q', effet: 'pulse', periode: 6, intensite: 0.5,
      flaque: { r: 1.5, couleur: '#ffb060', i: 0.45 } }] // nuit seulement ; ancre au battant arrière, §15
  },
  pnj: [
    { id: 'cv_nando', name: 'Nando', sprite: 'gen_rc_nando', x: 14.5, z: 18.2, faceTo: [14.2, 17.8], dialogue: 'cv_nando' },
    { id: 'cv_sola', name: 'Sola', sprite: 'gen_rc_sola', x: 17.8, z: 17.6, faceTo: [28.5, 16], dialogue: 'cv_sola' }
  ],
  // dialogues : §6 ; fouilles : §7 ; combat : §8
}
```

## 15. Poses définitives et sprites publiés

Après les sprites. Ce lot n'en produit pas.
