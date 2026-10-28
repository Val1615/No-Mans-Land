# Dusk-Town : positions (combat)

Coordonnées en mètres (x, z) dans le lieu ; cartes de 48 × 36 m.

## Rencontre du rôdeur (`ENCOUNTERS.rodeur.ancres`, `src/data/combat.js`)
Au lancement du combat, le joueur est placé à l'ancre du lieu, qui est le centre de la zone de 19 × 19 cases de 1 m (rayon 9). Toute la zone tient sur la carte : aucune case dans le vide. Les bâtiments restent des obstacles, et donc des couvertures en C2. Le rôdeur se place à (+4, −2) cases de l'ancre.

| Lieu | Ancre (x, z) | Zone (cases i × j) | Cases bloquées par des solides |
|---|---|---|---|
| `dusk_q1` La Pompe | 27,5 ; 23,5 | 18–36 × 14–32 | 93 / 361 (minimum trouvé sur la carte) |
| `dusk_q2` Le Transit | 32,5 ; 23,5 | 23–41 × 14–32 | 80 / 361 (minimum trouvé sur la carte) |

Avant, la zone était centrée sur le joueur à l'entrée (par exemple 28 ; 35 depuis Les Sables), et une partie tombait hors de la carte.
Vérification : `tests/combat_c1.py`, assertion « zone 19 × 19 entièrement sur la carte » (`game.combat.horsCarte()` vide).
