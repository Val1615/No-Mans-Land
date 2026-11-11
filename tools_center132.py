# Center-Town v2 (132 x 116 m) : tire la foule (environ 140 figurants) le long des trottoirs et du parvis de l'Arcadius,
# dans le jeu lui-même (grille, seuils, masques view.masqueEn), puis écrit src/data/center_foule.js.
# Usage : serveur local sur le dépôt (python3 -m http.server 8930) puis  python3 tools_center132.py [URL]
import json, sys, time, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')); from nml_boot import passer_boot
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8930/'
# Foule le long des trottoirs et du parvis (concept) : petits groupes de 1 à 3, espacés, tournés le long de l'avenue ;
# groupes plus denses seulement aux têtes de passages piétons (angles du carrefour) et devant les portes.
# Rien sur les passages piétons ni sur la chaussée (les taxis y roulent), rien sur une case solide, rien de masqué.
# bandes : [x0, z0, x1, z1, axe, nombre de figurants, rôle]
BANDES = [
  [12.5, 36.8, 55.5, 47.9, 'x', 20, 'citoyen'],    # parvis sud de l'Arcadius (des deux côtés de la grille IO z46)
  [44.5, 5, 55.5, 35, 'z', 10, 'citoyen'],          # parvis est
  [2, 48.6, 55.5, 55.4, 'x', 14, 'voyageur'],      # trottoir nord av. E-O, ouest (arrêt du tram)
  [92.5, 48.6, 130, 55.4, 'x', 10, 'passant'],      # trottoir nord av. E-O, est
  [2, 76.6, 55.5, 83.4, 'x', 10, 'client'],        # trottoir sud av. E-O, ouest (échoppe)
  [92.5, 76.6, 130, 83.4, 'x', 6, 'passant'],      # trottoir sud av. E-O, est
  [56.6, 2, 63.4, 47.5, 'z', 11, 'passant'],        # trottoir ouest av. N-S, nord
  [56.6, 84.5, 63.4, 114, 'z', 6, 'passant'],      # trottoir ouest av. N-S, sud
  [84.6, 2, 91.4, 47.5, 'z', 9, 'passant'],        # trottoir est av. N-S, nord
  [84.6, 84.5, 91.4, 114, 'z', 8, 'passant'],      # trottoir est av. N-S, sud
]
# groupes denses : [x, z, rayon, nombre, rôle, axe d'orientation] (têtes de passages piétons et portes)
GROUPES = [
  [60.5, 52.5, 2.2, 6, 'attente', 'x'], [87.5, 52.5, 2.2, 6, 'attente', 'x'],   # angles NO / NE (attendent de traverser)
  [60.5, 79.5, 2.2, 6, 'attente', 'x'], [87.5, 79.5, 2.2, 6, 'attente', 'x'],   # angles SO / SE
  # devant le Dôme (x44-56, z96-100) : rien, la bande est masquée par le remplissage bas ct_rempl6 au sud
  [98, 50.3, 2.6, 4, 'porte', 'x'],     # file du Bureau des permis
  [12.5, 44.5, 1.6, 3, 'porte', 'z'],   # devant le change de Teng
  [28, 39.5, 2.2, 5, 'porte', 'x'],     # au pied des marches de l'Arcadius, derrière le portail IO
  [20.5, 47.3, 1.6, 3, 'porte', 'x'],   # devant la grille, à gauche du portail
]
SOLDATS = [[23.4, 47.7, 1], [32.6, 47.7, -1], [26.6, 43.6, 1], [29.4, 43.6, -1]]  # deux devant les piliers du portail IO, deux dans le passage
POOL = ['st_civil0', 'st_civil1', 'st_civil2', 'st_civil3', 'st_civil4', 'st_civil5', 'gen_ml_navetteur', 'gen_fs_client_costume',
        'gen_fs_client_imper', 'gen_fs_passante', 'gen_fs_passant_canne', 'gen_ml_foule_a', 'gen_df_foule_a', 'gen_pp_foule_c']
JS = """async ([B, G, S, POOL]) => {
  const g = window.__nml.game, gr = g.grids.steel_center, v = window.__nml.view, L = window.__nml.world.LOCATIONS.steel_center;
  let seed = 2611; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const D = window.__nml.doors.filter(d => d.location === 'steel_center').map(d => [d.threshold.x, d.threshold.z]);
  const W = L.walkers.flatMap(w => w.path.map((a, i) => [a, w.path[(i + 1) % w.path.length]]));
  const dSeg = (p, [a, b]) => { const dx = b[0] - a[0], dz = b[1] - a[1], l2 = dx * dx + dz * dz || 1, t = Math.max(0, Math.min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dz) / l2));
    return Math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dz); };
  const libre = (x, z) => { for (const [dx, dz] of [[0, 0], [0.5, 0], [-0.5, 0], [0, 0.5], [0, -0.5]]) { const [i, j] = gr.toCell(x + dx, z + dz); if (!gr.free(i, j)) return false; } return true; };
  const pp = [[64, 52, 84, 56], [64, 76, 84, 80], [60, 56, 64, 76], [84, 56, 88, 76]];
  const route = (x, z) => pp.some(r => x >= r[0] - 0.4 && x <= r[2] + 0.4 && z >= r[1] - 0.4 && z <= r[3] + 0.4) || (x > 63.6 && x < 84.4) || (z > 55.6 && z < 76.4);
  // orientation le long d'un axe : signe de l'avancée à l'écran d'un pas de +1 m sur cet axe
  const P = (x, z) => window.__nml.project(x, 0, z).x, sens = (x, z, axe, s) => Math.sign((axe === 'x' ? P(x + s, z) : P(x, z + s)) - P(x, z)) || 1;
  const out = [], rejets = { solide: 0, route: 0, masque: 0, seuil: 0, passant: 0, voisin: 0 }; let k = 0;
  const ok = (x, z, ecart) => { if (route(x, z)) return rejets.route++, false; if (!libre(x, z)) return rejets.solide++, false; if (D.some(d => Math.hypot(d[0] - x, d[1] - z) < 2)) return rejets.seuil++, false;
    if (W.some(s => dSeg([x, z], s) < 0.7)) return rejets.passant++, false; if (out.some(e => Math.hypot(e.x - x, e.z - z) < ecart)) return rejets.voisin++, false;
    if (v.masqueEn(x, z).length) return rejets.masque++, false; return true; };
  const pose = (x, z, face, role, extra = {}) => { const e = { sprite: POOL[(k * 5 + 3) % POOL.length], x: +x.toFixed(1), z: +z.toFixed(1), face, role, ...extra }; out.push(e); k++; return e; };
  for (const [x, z, f] of S) if (ok(x, z, 0.75)) pose(x, z, f, 'soldat', { sprite: 'gen_halloran' });
  const bilan = {}; let ng = 0;
  // 1) groupes denses (têtes de passages, portes) : espacement 0,75 m
  for (const [cx, cz, r, n, role, axe] of G) { let pris = 0, s0 = rnd() < 0.5 ? 1 : -1;
    for (let t = 0; t < 900 && pris < n; t++) { const a = rnd() * 6.283, d = Math.sqrt(rnd()) * r, x = cx + Math.cos(a) * d, z = cz + Math.sin(a) * d;
      if (!ok(+x.toFixed(1), +z.toFixed(1), 0.75)) continue; pose(x, z, sens(x, z, axe, rnd() < 0.75 ? s0 : -s0), role, { groupe: 'g' + ng, dense: pris % 2 === 1 }); pris++; }
    bilan[role + '@' + cx + ',' + cz] = pris; ng++; }
  // 2) petits groupes de 1 à 3 le long des bandes : 0,8 m dans le groupe, 2,4 m au moins d'un autre groupe
  for (const [x0, z0, x1, z1, axe, n, role] of B) { let pris = 0, gi = 0;
    for (let t = 0; t < 4000 && pris < n; t++) {
      const taille = Math.min(n - pris, rnd() < 0.45 ? 1 : rnd() < 0.65 ? 2 : 3), cx = x0 + 0.6 + rnd() * (x1 - x0 - 1.2), cz = z0 + 0.6 + rnd() * (z1 - z0 - 1.2);
      const membres = [[0, 0], [0.85, 0.45], [-0.8, 0.5]].slice(0, taille).map(([u, w]) => axe === 'x' ? [cx + u, cz + w] : [cx + w, cz + u]);
      if (membres.some(([x, z]) => x < x0 || x > x1 || z < z0 || z > z1)) continue;
      if (out.some(e => membres.some(([x, z]) => Math.hypot(e.x - x, e.z - z) < 2.4))) { rejets.voisin++; continue; }
      if (!membres.every(([x, z]) => ok(+x.toFixed(1), +z.toFixed(1), 0.75))) continue;
      const s0 = rnd() < 0.5 ? 1 : -1, face2 = taille === 2 && rnd() < 0.4; // à deux : parfois face à face (conversation)
      membres.forEach(([x, z], m) => pose(x, z, sens(x, z, axe, face2 && m === 1 ? -s0 : s0), role, { groupe: 'g' + ng, dense: gi % 2 === 1 }));
      pris += taille; gi++; ng++; }
    bilan[role + '@' + x0 + ',' + z0] = pris + '/' + n; }
  return { out, rejets, bilan };
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
    r = E(JS, [BANDES, GROUPES, SOLDATS, POOL])
    print(r['bilan'])
    print(len(r['out']), 'figurants,', sum(1 for e in r['out'] if e.get('dense')), 'dense ; rejets', r['rejets'])
    lines = ',\n'.join('  ' + json.dumps(e, ensure_ascii=False) for e in r['out'])
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src/data/center_foule.js'), 'w').write(
      "// Généré par tools_center132.py (Center-Town v2, 132 x 116 m) : foule en petits groupes le long des trottoirs (groupes denses aux passages et aux portes), hors solides, chaussée, passages piétons, seuils, trajets des passants et masques.\n"
      "// dense: true = figurant masqué en plan large d'arrivée (version allégée).\nexport const CT_FOULE = [\n" + lines + "\n];\n")
