# PNJ Asia-Ground et China Lake : sprites finis

Branche creation/pnj-asia-china. Remplacent les reemplois provisoires (gen_vera, gen_odile, etc.). Cle = gen_ + id du PNJ dans src/data (asia_ground.js, china_lake.js).

Convention (identique a gen_teng, gen_elio, gen_vera) : webp RGBA, fond transparent, recadre serre sur la silhouette, 512 px de haut, pivot = bas-centre (pieds). Echelle donnee par height_m dans assets/reused/manifest.json (environ 50 px/m en jeu). Portrait : portrait-<cle>.webp, 192x192, recadre du haut du sprite sur fond (58,44,32), comme tools_npcs_steel.py.

Chaine : GenerateImage sur fond vert uni (#00E600), detourage par excès de vert, trous interieurs verts retires, despill limite a une bande de 4 px au bord.

A brancher (hors de ce lot, fichiers d autres agents) : 1) remplacer sprite: 'gen_xxx' par la cle ci-dessous dans NPCS_ASIA et NPCS_CHINA ; 2) ajouter ces entrees a assets/reused/manifest.json si le chargeur l exige.

| cle | height_m | px |
|---|---|---|
| gen_ag_mei | 1.62 | 175x512 |
| gen_ag_lau | 1.66 | 136x512 |
| gen_ag_okafor | 1.8 | 203x512 |
| gen_ag_seng | 1.72 | 185x512 |
| gen_ag_kim | 1.74 | 174x512 |
| gen_ag_ahlam | 1.86 | 199x512 |
| gen_cl_shen | 1.72 | 167x512 |
| gen_cl_m_nord | 1.68 | 177x512 |
| gen_cl_m_est | 1.78 | 194x512 |
| gen_cl_m_sud | 1.84 | 142x512 |
| gen_cl_m_ouest | 1.55 | 231x512 |
| gen_cl_tech | 1.72 | 189x512 |
| gen_cl_zhou | 1.72 | 138x512 |
| gen_cl_main1 | 1.88 | 156x512 |
| gen_cl_main2 | 1.78 | 149x512 |
| gen_cl_serveur | 1.74 | 221x512 |
| gen_cl_lo | 1.6 | 218x512 |
| gen_cl_yu | 1.64 | 221x512 |

Entrees de manifeste proposees :

```json
{
 "gen_ag_mei": {
  "file": "generated/gen_ag_mei.webp",
  "source": "GenerateImage (cursor), 67f7be5b",
  "height_m": 1.62,
  "px": [
   175,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 },
 "gen_ag_lau": {
  "file": "generated/gen_ag_lau.webp",
  "source": "GenerateImage (cursor), 291da5f1",
  "height_m": 1.66,
  "px": [
   136,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 },
 "gen_ag_okafor": {
  "file": "generated/gen_ag_okafor.webp",
  "source": "GenerateImage (cursor), 6d94b5ef",
  "height_m": 1.8,
  "px": [
   203,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 },
 "gen_ag_seng": {
  "file": "generated/gen_ag_seng.webp",
  "source": "GenerateImage (cursor), 59b0fd97",
  "height_m": 1.72,
  "px": [
   185,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 },
 "gen_ag_kim": {
  "file": "generated/gen_ag_kim.webp",
  "source": "GenerateImage (cursor), 9d05f75e",
  "height_m": 1.74,
  "px": [
   174,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 },
 "gen_ag_ahlam": {
  "file": "generated/gen_ag_ahlam.webp",
  "source": "GenerateImage (cursor), 62d95423",
  "height_m": 1.86,
  "px": [
   199,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 },
 "gen_cl_shen": {
  "file": "generated/gen_cl_shen.webp",
  "source": "GenerateImage (cursor), 31262777",
  "height_m": 1.72,
  "px": [
   167,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 },
 "gen_cl_m_nord": {
  "file": "generated/gen_cl_m_nord.webp",
  "source": "GenerateImage (cursor), 6604ab08",
  "height_m": 1.68,
  "px": [
   177,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 },
 "gen_cl_m_est": {
  "file": "generated/gen_cl_m_est.webp",
  "source": "GenerateImage (cursor), 26fa7452",
  "height_m": 1.78,
  "px": [
   194,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 },
 "gen_cl_m_sud": {
  "file": "generated/gen_cl_m_sud.webp",
  "source": "GenerateImage (cursor), ed8241a8",
  "height_m": 1.84,
  "px": [
   142,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 },
 "gen_cl_m_ouest": {
  "file": "generated/gen_cl_m_ouest.webp",
  "source": "GenerateImage (cursor), d4922e78",
  "height_m": 1.55,
  "px": [
   231,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 },
 "gen_cl_tech": {
  "file": "generated/gen_cl_tech.webp",
  "source": "GenerateImage (cursor), 450aa3f8",
  "height_m": 1.72,
  "px": [
   189,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 },
 "gen_cl_zhou": {
  "file": "generated/gen_cl_zhou.webp",
  "source": "GenerateImage (cursor), 3d926f9c",
  "height_m": 1.72,
  "px": [
   138,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 },
 "gen_cl_main1": {
  "file": "generated/gen_cl_main1.webp",
  "source": "GenerateImage (cursor), eaf1b082",
  "height_m": 1.88,
  "px": [
   156,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 },
 "gen_cl_main2": {
  "file": "generated/gen_cl_main2.webp",
  "source": "GenerateImage (cursor), 6a8689e6",
  "height_m": 1.78,
  "px": [
   149,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 },
 "gen_cl_serveur": {
  "file": "generated/gen_cl_serveur.webp",
  "source": "GenerateImage (cursor), effc8bfe",
  "height_m": 1.74,
  "px": [
   221,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 },
 "gen_cl_lo": {
  "file": "generated/gen_cl_lo.webp",
  "source": "GenerateImage (cursor), 595a1b22",
  "height_m": 1.6,
  "px": [
   218,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 },
 "gen_cl_yu": {
  "file": "generated/gen_cl_yu.webp",
  "source": "GenerateImage (cursor), 1be8cae4",
  "height_m": 1.64,
  "px": [
   221,
   512
  ],
  "footprint_m": [
   0.6,
   0.6
  ],
  "status": "généré, pnj-asia-china"
 }
}
```
