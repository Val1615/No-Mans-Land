# Dusk-Town : positions (combat)

Coordonnées en mètres (x, z) dans le lieu ; cartes de 48 × 36 m.

## Rencontre du rôdeur (`ENCOUNTERS.rodeur.ancres`, `src/data/combat.js`)
Au lancement du combat, le joueur est placé à l'ancre du lieu, qui est le centre de la zone de 19 × 19 cases de 1 m (rayon 9). Toute la zone tient sur la carte : aucune case dans le vide. Les bâtiments restent des obstacles, et donc des couvertures en C2. Le rôdeur se place à (+4, +2) cases de l'ancre, dans le terrain dégagé au sud de l'avenue, côté caméra.

| Lieu | Ancre (x, z) | Zone (cases i × j) | Cases bloquées par des solides |
|---|---|---|---|
| `dusk_q1` La Pompe | 22,5 ; 26,5 | 13–31 × 17–35 | 101 / 361 (le minimum, 93 en 27 ; 23, est caché derrière deux bâtiments) |
| `dusk_q2` Le Transit | 32,5 ; 26,5 | 23–41 × 17–35 | 82 / 361 |

Avant, la zone était centrée sur le joueur à l'entrée (par exemple 28 ; 35 depuis Les Sables), et une partie tombait hors de la carte.
Vérification : `tests/combat_c1.py`, assertion « zone 19 × 19 entièrement sur la carte » (`game.combat.horsCarte()` vide).

Sprite `gen_rodeur` (Ocre 3c0fc1d) : `pivot: 0.08` dans le manifeste. Pose en marche : le pied avant est au bas de l'image, le pied arrière environ 80 px plus haut. Le pivot est placé entre les deux pieds, et les deux pieds tombent dans l'anneau de la case (capture `combat_c1/desktop-01_debut_combat.png`).
