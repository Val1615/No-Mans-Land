

## Suite
`ar_toit_x`, `ar_toit_z`, `ar_toit_angle_se`, `ar_toit_angle_so`, `ar_facade_retour_ouest`, `gen_ar_fan_echarpe`, `gen_ar_fan_pancarte`, `gen_ar_fan_batons`, `gen_ar_fans_duo`, `g_ar_dalles_neutre`, `g_ar_parvis_marquages`, `g_ar_parvis_use`. Détail dans STEEL_ARENA.md, section Suite.

- Enceinte basse `ar2_` (façades 15 m, toit dôme 23 m en six morceaux, écrans géants réduits) : voir STEEL_ARENA.md, section « Enceinte basse (ar2) ». Les clés `ar_` de 28 et 42 m restent mais ne sont plus recommandées.

- **Bâtiments complets en 3/4** `ar_*_3q` + calques `ar_*_3q_neon` / `ar_*_3q_fenetres` (12 bâtiments : guichets, booking, contrôle IO, 2 merch, 2 food trucks, régie, tribunes, 3 techniques ouest) : voir `STEEL_ARENA.md`, section « Bâtiments complets (3/4) ». Enceinte `ar2_` inchangée.


## Lot `arena_v2` (régénération sans warp)

Nouvelles clés (statut `arena_v2`, champ `remplace`), voir `STEEL_ARENA.md` § « Régénération v2 sans déformation » pour les mesures et les poses.

| ancienne | nouvelle | px | ancre | calques |
|---|---|---|---|---|
| `ar_barriere_file` | `ar_barriere_file_v2` | 180×111 | [165, 108] | — |
| `ar_barriere_file_o` | `ar_barriere_file_o_v2` | 135×134 | [22, 131] | — |
| `ar_guichets_3q` | `ar_guichets_v2_3q` | 279×300 | [171, 297] | fenetres, neon, pulse |
| `ar_booking_3q` | `ar_booking_v2_3q` | 277×284 | [171, 281] | fenetres, neon, pulse |
| `ar_securite_3q` | `ar_securite_v2_3q` | 277×291 | [172, 288] | fenetres, neon, pulse |
| `ar_stand_merch_b_3q` | `ar_stand_merch_b_v2_3q` | 277×261 | [171, 258] | fenetres, neon, pulse |
| `ar_stand_merch_c_3q` | `ar_stand_merch_c_v2_3q` | 279×267 | [170, 264] | fenetres, neon |
| `ar_regie_3q` | `ar_regie_v2_3q` | 440×347 | [335, 344] | fenetres, neon, pulse, pulse2 |
| `ar_tribunes_3q` | `ar_tribunes_v2_3q` | 718×510 | [504, 507] | fenetres, neon, pulse, pulse2 |
| `ar_tech_ouest_a_3q` | `ar_tech_ouest_a_v2_3q` | 554×604 | [345, 601] | fenetres, neon, pulse |
| `ar_tech_ouest_b_3q` | `ar_tech_ouest_b_v2_3q` | 398×507 | [179, 504] | fenetres |
| `ar_tech_ouest_c_3q` | `ar_tech_ouest_c_v2_3q` | 399×508 | [186, 505] | fenetres |
| `ar_mat_projecteur_pulse_3q` | `ar_mat_projecteur_pulse_v2_3q` | 141×337 | [84, 334] | faisceau, pulse, pulse_b |
| `ar_enceinte_pulse_3q` | `ar_enceinte_pulse_v2_3q` | 181×242 | [125, 239] | pulse, pulse_b |
| `ar_gantry_led_pulse_3q` | `ar_gantry_led_pulse_v2_3q` | 331×408 | [123, 405] | pulse, pulse_b |
| `ar_strobe_pulse_3q` | `ar_strobe_pulse_v2_3q` | 105×154 | [63, 151] | pulse, pulse_b |
