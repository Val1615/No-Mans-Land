# Center-Town v2 (132 x 116 m) : tire la foule (environ 140 figurants) concentrée sur le carrefour et le parvis de l'Arcadius,
# dans le jeu lui-même (grille, seuils, masques view.masqueEn), puis écrit src/data/center_foule.js.
# Usage : serveur local sur le dépôt (python3 -m http.server 8930) puis  python3 tools_center132.py [URL]
import json, sys, time, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')); from nml_boot import passer_boot
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8930/'
# zones : [x0, z0, x1, z1, nombre, rôle, part dense (masquée en plan large)]
ZONES = [
  # rien sur les passages piétons : les taxis y passent (seuls les passants qui traversent y circulent, les taxis les attendent)
  [12, 42.5, 55, 47.5, 32, 'citoyen', 0.5],    # parvis sud de l'Arcadius (devant l'escalier et la grille IO)
  [45, 6, 55, 41, 10, 'citoyen', 0.5],         # parvis est
  [56.5, 48.5, 63.5, 55.5, 16, 'foule', 0.5],  # angle NO du carrefour
  [84.5, 48.5, 91.5, 55.5, 16, 'foule', 0.5],  # angle NE
  [56.5, 76.5, 63.5, 83.5, 16, 'foule', 0.5],  # angle SO
  [84.5, 76.5, 91.5, 83.5, 16, 'foule', 0.5],  # angle SE
  [14, 48.5, 55, 55.5, 11, 'voyageur', 0.5],    # trottoir nord av. E-O (arrêt tram, bannière)
  [16, 76.5, 55, 83.5, 8, 'client', 0.5],      # trottoir sud av. E-O (échoppe, cerisier)
  [44, 96.4, 55.5, 99.6, 3, 'client', 0.3],    # passage vers l'entrée du Dôme
  [92.5, 48.5, 104, 52, 4, 'attente', 0.25],   # file du Bureau des permis
  [92.5, 48.5, 130, 55.5, 4, 'foule', 0.5],    # trottoir nord est
]
SOLDATS = [[24.5, 43.2, 1], [31.5, 43.2, -1], [26.5, 45.4, 1], [29.5, 45.4, -1]]
POOL = ['st_civil0', 'st_civil1', 'st_civil2', 'st_civil3', 'st_civil4', 'st_civil5', 'gen_ml_navetteur', 'gen_fs_client_costume',
        'gen_fs_client_imper', 'gen_fs_passante', 'gen_fs_passant_canne', 'gen_ml_foule_a', 'gen_df_foule_a', 'gen_pp_foule_c']
JS = """async ([Z, S, POOL]) => {
  const g = window.__nml.game, gr = g.grids.steel_center, v = window.__nml.view, L = window.__nml.world.LOCATIONS.steel_center;
  let seed = 1312; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const D = window.__nml.doors.filter(d => d.location === 'steel_center').map(d => [d.threshold.x, d.threshold.z]);
  const W = L.walkers.flatMap(w => w.path.map((a, i) => [a, w.path[(i + 1) % w.path.length]]));
  const dSeg = (p, [a, b]) => { const dx = b[0] - a[0], dz = b[1] - a[1], l2 = dx * dx + dz * dz || 1, t = Math.max(0, Math.min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dz) / l2));
    return Math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dz); };
  const libre = (x, z) => { for (const [dx, dz] of [[0, 0], [0.5, 0], [-0.5, 0], [0, 0.5], [0, -0.5]]) { const [i, j] = gr.toCell(x + dx, z + dz); if (!gr.free(i, j)) return false; } return true; };
  const out = [], rejets = { solide: 0, masque: 0, seuil: 0, passant: 0, voisin: 0 }; let k = 0;
  const ok = (x, z, why) => { if (!libre(x, z)) return why.solide++, false; if (D.some(d => Math.hypot(d[0] - x, d[1] - z) < 2)) return why.seuil++, false;
    if (W.some(s => dSeg([x, z], s) < 0.6)) return why.passant++, false; if (out.some(e => Math.hypot(e.x - x, e.z - z) < 0.95)) return why.voisin++, false;
    if (v.masqueEn(x, z).length) return why.masque++, false; return true; };
  for (const [x, z, f] of S) if (ok(x, z, rejets)) out.push({ sprite: 'gen_halloran', x, z, face: f, role: 'soldat' });
  for (const [x0, z0, x1, z1, n, role, dense] of Z) { let pris = 0;
    for (let t = 0; t < 600 && pris < n; t++) { const x = +(x0 + rnd() * (x1 - x0)).toFixed(1), z = +(z0 + rnd() * (z1 - z0)).toFixed(1);
      if (!ok(x, z, rejets)) continue; const e = { sprite: POOL[(k * 5 + 3) % POOL.length], x, z, face: rnd() < 0.5 ? -1 : 1, role };
      if (pris % Math.round(1 / dense) !== 0 || dense >= 0.6 && pris % 5 < 3) e.dense = true; out.push(e); pris++; k++; } }
  return { out, rejets };
}"""
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    pg = br.new_page(viewport={'width': 1280, 'height': 800}); E = pg.evaluate
    pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=90000); passer_boot(pg)
    E("document.getElementById('m-new').click()"); time.sleep(.5)
    for s in ['[data-race="augmente"]', '#cr-next', '#cr-enter']: E(f"document.querySelector('{s}').click()"); time.sleep(.4)
    pg.wait_for_function('!document.body.classList.contains("menu-open")'); time.sleep(.5)
    E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_center';s.player.x=74;s.player.z=66;Object.assign(s.flags,{q_start:true,q_fin:true,steel_passe:true});g.restore(s,true)})()")
    time.sleep(1.5); E("window.__nml.view.render()")
    r = E(JS, [ZONES, SOLDATS, POOL])
    print(len(r['out']), 'figurants,', sum(1 for e in r['out'] if e.get('dense')), 'dense ; rejets', r['rejets'])
    lines = ',\n'.join('  ' + json.dumps(e, ensure_ascii=False) for e in r['out'])
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src/data/center_foule.js'), 'w').write(
      "// Généré par tools_center132.py (Center-Town v2, 132 x 116 m) : foule hors solides, hors seuils, hors trajets des passants et hors masques.\n"
      "// dense: true = figurant masqué en plan large d'arrivée (version allégée).\nexport const CT_FOULE = [\n" + lines + "\n];\n")
