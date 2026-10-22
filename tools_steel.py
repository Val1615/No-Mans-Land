# v12 Steel-Megalopolis L1 : bâtiments entiers, même chaîne que tools_buildings.py (même caméra v4, même échelle K),
# sans toucher aux sprites de Dusk-Town : écrit seulement les sprites b_st_* et fusionne le manifeste.
# Sources : planches maquette settlement-v9-city.png et city-v3.png (même série et même angle que settlement-v9-dusk),
# plus 2 images générées (porte du sarcophage, sortie de service), mises à l'échelle K comme gen_lab_bunker.
import numpy as np, math, json, sys
from PIL import Image, ImageDraw
from scipy import ndimage
S = '/workspace/nml/src/a/No-Mans-Land_Reconstruction/07_MAQUETTE_ARCHIVE_v0.13/art-source/'
OUT = '/workspace/nml/game/'
YAW, PITCH, K = 34.5, 28.8, 50
cy, sy = math.cos(math.radians(YAW)), math.sin(math.radians(YAW))
r05 = lambda v: round(v * 2) / 2
CELLS = {
 'st_tour': ('settlement-v9-city.png', 0, 0), 'st_boutiques': ('settlement-v9-city.png', 1, 0), 'st_neon': ('settlement-v9-city.png', 2, 0),
 'st_usine': ('settlement-v9-city.png', 0, 1), 'st_verre': ('settlement-v9-city.png', 1, 1), 'st_immeuble': ('settlement-v9-city.png', 2, 1),
 'st_jumelles': ('city-v3.png', 0, 0), 'st_galerie': ('city-v3.png', 1, 0), 'st_blanc': ('city-v3.png', 2, 0), 'st_douane': ('city-v3.png', 2, 1),
 'st_porte': ('GEN:art-gen/gen_steel_gate.jpg', 30.0, 7.0), 'st_service': ('GEN:art-gen/gen_service_exit.jpg', 5.0, 3.0),
}
FRONT_Z = 13.0
# quartier -> id: (case, x, z (None = FRONT_Z - d), label, visitable, portes peintes [(px, py, face)] en px source, indice)
DISTRICTS = {
 'route': {
  'r_porte':   ('st_porte', 1.5, 3.0, 'Porte du sarcophage', False, [], None),
  'r_douane':  ('st_douane', 22.0, 11.0, 'Douane', True, [], 'card'),
  'r_service': ('st_service', 40.0, 29.5, 'Sortie de service', False, [], None)},
 'center': {
  'c_tour':      ('st_tour', 1.0, None, 'Tour d\'habitation', False, [], None),
  'c_change':    ('st_boutiques', 11.0, None, 'Change de Teng', True, [], 'coin'),
  'c_neon':      ('st_neon', 24.0, None, 'Galerie Néon', False, [], None),
  'c_arcadius':  ('st_verre', 36.0, None, 'Arcadius Center', False, [], None),
  'c_immeuble':  ('st_immeuble', 2.0, 24.0, 'Immeuble aux escaliers', False, [], None),
  'c_galerie':   ('st_galerie', 13.0, 24.0, 'Passage couvert', False, [], None),
  'c_jumelles':  ('st_jumelles', 26.0, 24.0, 'Tours jumelles', False, [], None),
  'c_blanc':     ('st_blanc', 37.0, 24.0, 'Bureau des permis', False, [], None)},
}
DOORS_PX = json.load(open(OUT + 'art-gen/steel_doors_px.json')) if len(sys.argv) < 2 else {}
for q in DISTRICTS:
  for bid in DISTRICTS[q]:
    if bid in DOORS_PX:
      c, x, z, l, v, _, cue = DISTRICTS[q][bid]; DISTRICTS[q][bid] = (c, x, z, l, v, [tuple(p) for p in DOORS_PX[bid]], cue)
def load_cell(cell):
  f, c, r = CELLS[cell]
  if f.startswith('GEN:'):
    sys.path.insert(0, OUT); import tools_interiors as TI
    rgba = TI.quad(OUT + f[4:], -1).copy()
    # dé-contamination du magenta résiduel (liserés roses au pied du mur) : on ramène rouge et bleu vers le vert
    px = rgba[..., :3].astype(float); spill = np.clip((px[..., 0] + px[..., 2]) / 2 - px[..., 1] - 18, 0, None)
    px[..., 0] -= spill * 0.9; px[..., 2] -= spill; rgba[..., :3] = np.clip(px, 0, 255).astype('uint8')
    a = rgba[..., 3] > 100
    ys, xs = np.nonzero(a)
    sc = K * (c * cy + r * sy) / (xs.max() - xs.min() + 1)
    im = Image.fromarray(rgba).resize((int(rgba.shape[1] * sc), int(rgba.shape[0] * sc)), Image.LANCZOS)
    pad = Image.new('RGBA', (im.size[0] + 20, im.size[1] + 20), (0, 0, 0, 0)); pad.alpha_composite(im, (10, 10)); full = pad
    print(f'  {cell}: image générée mise à l échelle x{sc:.3f}')
    A = ndimage.binary_opening(np.asarray(full)[..., 3] > 100); lab, n = ndimage.label(A); sizes = ndimage.sum(A, lab, range(1, n + 1))
    return full, lab, int(np.argmax(sizes)) + 1, f[4:]
  full = Image.open(S + f).convert('RGBA'); A = ndimage.binary_opening(np.asarray(full)[..., 3] > 100)
  lab, n = ndimage.label(A); sizes = ndimage.sum(A, lab, range(1, n + 1))
  for i in np.argsort(-sizes):
    ys, xs = np.nonzero(lab == i + 1)
    if c*512 <= xs.mean() < (c+1)*512 and r*512 <= ys.mean() < (r+1)*512: return full, lab, i + 1, f
man = json.load(open(OUT + 'assets/buildings/manifest.json')); out, geo = {}, {}
sp, cp = math.sin(math.radians(PITCH)), math.cos(math.radians(PITCH))
for cell in CELLS:
  full, lab, li, f = load_cell(cell)
  ys, xs = np.nonzero(lab == li)
  x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max(); ax = int(np.median(xs[ys >= y1 - 3])); ay = int(y1)
  w, d = r05((ax - x0) / (K * cy)), r05((x1 - ax) / (K * sy))
  M = lab == li
  def opaque(a, b):
    px = ax + K * (-a * cy + b * sy); py = ay - K * (a * sy * sp + b * cy * sp) - K * 0.3 * cp
    px, py = int(round(px)), int(round(py)); return 0 <= py < M.shape[0] and 0 <= px < M.shape[1] and M[py, px]
  w0, d0 = w, d
  while w > 2 and not opaque(w - 0.4, 0.4): w -= 0.5
  while d > 2 and not opaque(0.4, d - 0.4): d -= 0.5
  while (w > 2 or d > 2) and not opaque(w - 0.4, d - 0.4): w, d = (w - 0.5, d) if w >= d else (w, d - 0.5)
  print(f'  {cell}: emprise {w0}x{d0} -> {w}x{d}, source {f}')
  m = ndimage.binary_dilation(lab == li, iterations=2)[y0:y1 + 1, x0:x1 + 1]
  sub = full.crop((x0, y0, x1 + 1, y1 + 1)); sub.putalpha(Image.fromarray(np.minimum(np.asarray(sub)[..., 3], m * 255).astype('uint8')))
  name = 'b_' + cell; sub.save(OUT + 'assets/buildings/' + name + '.webp', quality=90, lossless=False)
  man[name] = {'file': 'buildings/' + name + '.webp', 'source': f, 'crop': [int(x0), int(y0), int(x1) + 1, int(y1) + 1],
               'px': list(sub.size), 'anchor': [ax - int(x0), ay - int(y0)], 'footprint_m': [w, d], 'lot': 'steel-l1 v12'}
  geo[cell] = (w, d, ax, ay, x0, y0, sub)
  # aide au choix des portes : quadrillage en px source
  t = Image.new('RGB', sub.size, '#444'); t.paste(sub, mask=sub); dr = ImageDraw.Draw(t)
  for gx in range(0, sub.size[0], 50): dr.line([(gx, 0), (gx, sub.size[1])], fill='#0ff' if (gx + x0) % 100 < 50 else '#088')
  for gy in range(0, sub.size[1], 50): dr.line([(0, gy), (sub.size[0], gy)], fill='#0ff')
  dr.text((4, 4), f'x0={x0} y0={y0}', fill='yellow'); t.save(f'/tmp/steel_dbg_{cell}.png')
for q, B in DISTRICTS.items():
  blds, doors = [], []
  for bid, (cell, bx, bz, label, vis, dpx, cue) in B.items():
    w, d, ax, ay, x0, y0, sub = geo[cell]
    if bz is None: bz = FRONT_Z - d
    P = (bx + w, bz + d)
    blds.append({'id': bid, 'label': label, 'sprite': 'b_' + cell, 'x': bx, 'z': bz, 'w': w, 'd': d, 'visitable': vis, 'cue': cue})
    for k, (px, py, face) in enumerate(dpx):
      dx = px - ax
      if face == 's': s_ = -dx / (K * cy); o = (round(P[0] - s_, 2), P[1]); th = (o[0], P[1] + 1)
      else: s_ = dx / (K * sy); o = (P[0], round(P[1] - s_, 2)); th = (P[0] + 1, o[1])
      doors.append({'id': f'{bid}_door' + ('' if k == 0 else str(k + 1)), 'buildingId': bid, 'painted_px': [px, py], 'face': face, 'opening': o, 'threshold': th})
  out[q] = (blds, doors)
json.dump(man, open(OUT + 'assets/buildings/manifest.json', 'w'), indent=1, ensure_ascii=False)
js = '// Généré par tools_steel.py : ne pas éditer à la main. v12 Steel-Megalopolis L1 (route + douane, Center-Town).\n'
for q in out:
  js += f'export const BUILDINGS_{q.upper()} = ' + json.dumps(out[q][0], ensure_ascii=False) + ';\n'
  js += f'export const PAINTED_DOORS_{q.upper()} = ' + json.dumps(out[q][1], ensure_ascii=False) + ';\n'
open(OUT + 'src/data/buildings_steel.js', 'w').write(js)
for q in out:
  for b in out[q][0]: print(q, b['id'], b['x'], b['z'], b['w'], b['d'])
  for d in out[q][1]: print(q, d['id'], d['opening'], d['threshold'])
