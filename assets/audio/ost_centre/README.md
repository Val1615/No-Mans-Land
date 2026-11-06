# Playlist commune : Center-Town, Fréquence Strip, Pulse Plaza, Steel Arena

Fichiers fournis par Valentin le 2026-11-06, interprétés par Groovy Crew (canon). Ils sont copiés tels quels, sans conversion (`fecc483`).

| Ordre | Fichier | Titre | Durée |
|---|---|---|---|
| 1 | `01_bad_buzz_protocol_remix.mp3` | Bad Buzz Protocol (Remix) | 3 min 25 |
| 2 | `02_dance_soit_plus_chrome_16bit.mp3` | Dance soit plus chrome (16bit) | 3 min 42 |
| 3 | `03_steel_megalopolis_remix.mp3` | Steel-Megalopolis (Remix) | 3 min 37 |
| 4 | `04_we_already_knew_remix.mp3` | We Already Knew (Remix) | 3 min 35 |

Règle : une seule rotation partagée par les quatre zones (`steel_center` + intérieur `change_in`, `steel_strip`, `steel_pulse`, `steel_arena`). Changer de zone ne coupe pas et ne relance pas le morceau en cours. Les morceaux s'enchaînent dans l'ordre du tableau puis recommencent en boucle. Hors de ces quatre quartiers, l'unique lecteur `<audio id="music">` délègue à l'ambiance habituelle et reprend la piste en cours au retour.

## Intégration et API de rythme (`src/core/ost_centre.js`, posée en `27b3f1f`)

- **Singleton** : `createMusic` pilote l'unique élément `<audio id="music">` (exposé dans `window.__nml.music` et `window.__nml.ostCentre`). Tant que le joueur circule entre Center-Town, Pulse Plaza, Fréquence Strip et Steel Arena (ou entre dans `change_in`, atténué à `0,25`), `el.src` et `el.currentTime` restent intacts.
- **Analyse de rythme (`window.__nml.ostCentre` / `view.ostCentre`)** : un `AnalyserNode` Web Audio (`fftSize = 1024`, compensé du volume courant) échantillonne en continu cette même lecture pour exposer :
  - `ostCentre.beat` (`0..1`, impulsion à `1` sur chaque kick puis décroissance rapide),
  - `ostCentre.energy`, `ostCentre.bass`, `ostCentre.mid`, `ostCentre.high` (`0..1`),
  - `ostCentre.kick` (booléen sur la frame de rendu), `ostCentre.kickCount`, `ostCentre.bpm`,
  - `ostCentre.onKick(fn)` (retourne la fonction de désabonnement) et `ostCentre.bands()`.
- **Suite de vérification** : `tests/ost_centre.py` + `tests/music_check.py`.
