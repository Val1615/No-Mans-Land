# Rencontre 07 : la tempête de poussière

Fiche courte (gel de la finition). Consigne : [`CONSIGNE.md`](CONSIGNE.md) §6 rencontre 07, événement d'environnement. Même bibliothèque que le convoi : la route désertique, modules du pilote et de la caravane. Pas de sprites dans ce lot, pas d'implémentation de l'effet de poussière (description pour Rivet au §10).

Maquette concept (MAQUETTE, croquis de pose, pas une capture) : `/workspace/nml-shots/rencontres/tempete_concept.png`.

## 1. Identité

| | |
|---|---|
| id | `tempete_poussiere`, préfixe de drapeaux `tp_` |
| Titre | La tempête de poussière |
| Famille | environnement |
| Terrains / biomes | `['piste', 'desert']` / `['desert']` |
| Poids / durée | 1 / 1 h (+2 h si l'on attend l'accalmie, §7) |
| Rejouable | oui, sur une autre case (journal par case). Pas unique. |
| Emprise | 30 × 24 m, un seul niveau au sol. Pas de combat dans ce lot. |
| Maquette | `/workspace/nml-shots/rencontres/tempete_concept.png` (MAQUETTE) |

## 2. Pitch

Le vent se lève sur la piste. Le fond du désert disparaît, le premier plan reste lisible. Une carcasse à demi ensevelie, porte ouverte, et une tôle contre les rochers : un abri. On peut s'y blottir et attendre, fouiller l'épave, ou traverser malgré tout.

## 3. Décor

Même route désertique que le convoi (piste est–ouest, z 14–19, entrée à l'est), sans le camion ni l'équipage. L'abri est un peu au sud de la piste, assez loin de l'entrée pour que l'on choisisse d'y aller ou de rester sur la bande tassée.

**Clés réutilisées** : `g_rc_sable` `_b` `_c`, `g_rc_piste` `_b` `_c`, `rc_ds_talus_a/b/fin_3q`, `rc_ds_rochers_3q` `_b`, `rc_ds_panneau_ufsa_3q`, `rc_car_ferraille_3q`, `rc_car_traces_3q`. Pas le relais de la caravane, pas l'épave du Service (IO), pas le pick-up de l'appât : trop reconnaissables.

**Clés nouvelles** :

| Clé | Rôle |
|---|---|
| `rc_tp_carcasse_3q` | Carcasse civile à demi ensevelie, portière ouverte, on peut s'y abriter (solide = caisse, passage par la portière) |
| `rc_tp_tole_3q` | Tôle ondulée appuyée contre les rochers |
| `rc_tp_caisse_3q` | Caisse éventrée, fouillable |
| `rc_tp_gourde_3q` | Bidon / gourde dans le sable, examinable |

Pas de PNJ. Le vent tient la scène.

## 4. Variantes

Aucune dans ce lot. Une seule situation. Une variante de nuit se règle par la courbe d'ambiance, pas par un second décor.

## 5. PNJ

Aucun.

## 6. Dialogues

Aucun. Tout passe par l'examen et les actions d'objets (abri, carcasse, tôle, caisse, gourde, piste).

Textes courts, à l'arrivée : « Le vent racle la piste. Plus loin, une carcasse offre un peu d'ombre. »

## 7. Issues

Le joueur n'est forcé à rien à l'arrivée.

- **S'abriter** dans la carcasse ou sous la tôle : `tp_abri`. Débloque « attendre l'accalmie ».
- **Attendre l'accalmie** (depuis l'abri seulement) : +2 h sur l'horloge régionale, `tp_accalmie`. Le voile de poussière tombe (§10). Les sorties redeviennent sûres.
- **Fouiller l'épave** (carcasse, caisse, gourde) : voir §9. Possible pendant la tempête, un peu plus lisible après l'accalmie (rien de bloqué).
- **Risquer la traversée** (prendre une sortie sans `tp_accalmie`) : Observation 4 pour rester sur la piste. Réussite : `pv:-2`, +1 h. Échec : `pv:-4`, +1 h. Dans les deux cas on sort (reprise ou halte selon la sortie). Si l'action `pv:` n'existe que pour soigner le joueur (écart déjà noté sur le témoin), Rivet pose l'équivalent le plus proche et le signale.
- **Partir après l'accalmie** : sortie libre, sans dégât.

Pas de combat.

## 8. Combat

Aucun dans ce lot.

## 9. Objets

Existants seulement : 1 × `water` dans la gourde (une fois), 1 × `ration` au fond de la caisse (une fois, Observation 2 ou fouille simple). La carcasse, examinée : une banquette déchirée, rien à prendre. La tôle : un abri, pas un butin.

## 10. Lumière et effet de poussière (pour Rivet, à ne pas implémenter dans ce lot)

Courbe `desert` inchangée : `ambiance('desert', heures)`. La tempête n'est pas un nouveau moteur de lumière. C'est un voile par-dessus.

Description de l'effet, pour quand il sera branché :

- Un voile de sable semi-transparent, animé (lentes rafales), posé au-dessus de la scène, **pas** à la place de la courbe.
- Opacité modeste : environ 0,25 à 0,40 le jour, un peu plus la nuit, jamais opaque. Le premier plan, le tracé de déplacement, les objets examinables et l'interface restent lisibles, surtout en 390.
- Des traînées ponctuelles possibles en mi-distance, pas sur l'UI, pas sur les invites d'examen.
- Quand `tp_accalmie` est posé : le voile tombe à ~0,05 ou s'éteint.
- La carcasse est vide : pas de lampe, pas de halo. Une nuit de tempête est simplement sombre (nuit du désert + voile). On peut attendre l'accalmie, et l'aube si les heures y tombent.
- Le polissage du voile (grain, direction du vent, variants) va en phase D.

## 11. DA

Même palette que le pilote. La tempête remplit le cadre (le fond se perd, le premier plan reste net) : ce n'est pas un terrain vide avec un objet au milieu. La carcasse est une berline ou un petit utilitaire civil, distincte des véhicules déjà en jeu. Maquette simple, pas une cible de pixels.

## 12. Câblage pour Rivet

- Catalogue : `tempete_poussiere`, `famille: 'environnement'`, `prefixe: 'tp_'`, `terrains: ['piste', 'desert']`, `biomes: ['desert']`, `poids: 1`, `duree: 1` (+2 h si `tp_accalmie`).
- Pas de `si` d'unicité. Journal par case : `{ id }`.
- Drapeaux de scène `tp_*` remis à zéro à la sortie.
- Pas de drapeau de monde dans ce lot (événement de météo).
- Sortie est : reprise. Sortie ouest : halte. Sans `tp_accalmie`, toute sortie déclenche la traversée risquée (§7).
- DEV : `?rencontre=tempete_poussiere`. Pouvoir poser `tp_accalmie` pour comparer le voile, une fois l'effet branché.
- Effet de poussière : §10, plus tard. En attendant, la scène se joue sans voile (les textes suffisent). Gabarits gris acceptables pour la carcasse et la tôle.
- `pv:` à la traversée : voir l'écart possible au §7.

## 13. Décisions de DA et de lore à signaler à Valentin

1. C'est un **événement de météo**, pas une scène de faction. Pas de nouveau nom, pas de nouvelle organisation.
2. Le coût en heures (+2 h à l'abri, +1 h si l'on traverse) est un vrai coût de voyage, sur l'horloge régionale déjà en place.
3. On ne réutilise pas l'épave du Service (IO) ni le relais UFSA de la caravane, pour ne pas faire de chaque case du désert le même lieu.
4. Pas de drapeaux `monde_*` dans ce lot.
5. L'effet de poussière est décrit pour plus tard ; il s'ajoute à la courbe `desert`, il ne la remplace pas.

## 14. Entrée au format d'ARCHI.md §4

Poses définitives au §15, après les sprites. Positions indicatives.

```js
tempete_poussiere: {
  nom: 'La tempête de poussière', famille: 'environnement', prefixe: 'tp_',
  terrains: ['piste', 'desert'], biomes: ['desert'], poids: 1, duree: 1, // +2 h si tp_accalmie
  arrivee: 'Le vent racle la piste. Plus loin, une carcasse offre un peu d\'ombre.',
  scene: { size: { w: 30, d: 24 },
    ground: { skin: 'g_rc_sable', tint: null, paint: [ /* bande g_rc_piste z 14-19 ; variantes _b/_c */ ] },
    ambiance: 'desert',
    // voile de poussière : §10, pas dans ce lot
    buildings: [
      // carcasse, tôle, rochers, talus, panneau : poses au §15
    ],
    props: [
      // caisse, gourde, traces, ferraille : poses au §15
    ],
    entrees: [{ id: 'entree', x: 28.5, z: 16, side: 'east' }],
    sorties: [
      { id: 'S_E', x: 29.5, z: 14, w: 0.5, d: 5, rencontre: true, reprise: true },
      { id: 'S_O', x: 0, z: 14, w: 0.5, d: 5, rencontre: true }
    ]
  },
  pnj: [],
  // examens et fouilles : §7 et §9 ; pas de combat
}
```

## 15. Poses définitives et sprites publiés

Après les sprites. Ce lot n'en produit pas.
