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
FP = {'sv_cab0': (5.0, 4.0), 'sv_cab1': (5.0, 4.0), 'sv_cab2': (5.0, 4.0), 'sv_cab3': (5.0, 4.5), 'sv_tripot': (8.0, 7.0), 'sv_atelier': (6.5, 5.5), 'sv_lift': (3.5, 3.5), 'st_porte2': (30.0, 8.0), 'st_poste': (9.0, 8.0), 'st_ct_dome': (15.0, 12.0), 'st_ct_shop': (8.0, 8.0), 'st_ct_tower': (9.0, 9.0)}  # v13 : emprises imposées (images générées non boîtes)
CELLS = {
 'st_tour': ('settlement-v9-city.png', 0, 0), 'st_boutiques': ('settlement-v9-city.png', 1, 0), 'st_neon': ('settlement-v9-city.png', 2, 0),
 'st_usine': ('settlement-v9-city.png', 0, 1), 'st_verre': ('settlement-v9-city.png', 1, 1), 'st_immeuble': ('settlement-v9-city.png', 2, 1),
 'st_jumelles': ('city-v3.png', 0, 0), 'st_galerie': ('city-v3.png', 1, 0), 'st_blanc': ('city-v3.png', 2, 0), 'st_douane': ('city-v3.png', 2, 1),
 'st_porte': ('GEN:art-gen/gen_steel_gate.jpg', 30.0, 7.0), 'st_service': ('GEN:art-gen/gen_service_exit.jpg', 5.0, 3.0),
 # v13 : place forte IO et Center-Town de nuit (générés d'après le concept art ; FIX = cisaillement v4 de tools_interiors.v4fix)
 'st_porte2': ('GEN:art-gen/gen_steel_gate2.jpg', 30.0, 9.0),
 # v14 : Sous-Ville (concept_sous_ville.jpg) : cabanes de tôle (planche 2x2), tripot, atelier d'Elio, monte-charge
 **{f'sv_cab{q}': (f'GENFIXQ:art-gen/gen_sv_shacks.jpg:{q}', 5.0, 4.0) for q in range(4)},
 'sv_tripot': ('GENFIX:art-gen/gen_sv_tripot.jpg', 8.0, 7.0), 'sv_atelier': ('GENFIX:art-gen/gen_sv_atelier.jpg', 6.5, 5.5), 'sv_lift': ('GENFIX:art-gen/gen_sv_lift.jpg', 3.5, 3.5), 'st_poste': ('GENFIX:art-gen/gen_douane_post.jpg', 9.0, 9.0),
 'st_ct_dome': ('GENFIX:art-gen/gen_ct_dome.jpg', 15.0, 13.0), 'st_ct_shop': ('GENFIX:art-gen/gen_ct_shop.jpg', 9.0, 9.0), 'st_ct_tower': ('GENFIX:art-gen/gen_ct_tower.jpg', 10.0, 10.0),
}
FRONT_Z = 13.0
# quartier -> id: (case, x, z (None = FRONT_Z - d), label, visitable, portes peintes [(px, py, face)] en px source, indice)
DISTRICTS = {
 'route': {  # v13 : place forte. Porte du sarcophage en haut à droite (la route y monte), poste de douane à gauche.
  'r_porte':   ('st_porte2', 17.0, 0.0, 'Porte du sarcophage', False, [], None),
  'r_douane':  ('st_poste', 2.0, 20.0, 'Douane', True, [], 'card'),
  'r_service': ('st_service', 40.0, 29.5, 'Sortie de service', False, [], None)},
 'sv1': {  # v14 : Sous-Ville, quartier des Poutres (arrivée par la trappe) : cabanes, tripot
  'v_cab_a': ('sv_cab0', 2.0, 3.0, 'Cabane', False, [], None), 'v_cab_b': ('sv_cab1', 9.0, 2.5, 'Cabane', False, [], None),
  'v_tripot': ('sv_tripot', 16.0, 2.0, 'Le Tripot', True, [], 'dice'), 'v_cab_c': ('sv_cab2', 27.0, 3.0, 'Cabane', False, [], None),
  'v_cab_d': ('sv_cab3', 3.0, 20.0, 'Cabane', False, [], None), 'v_cab_e': ('sv_cab1', 22.0, 21.0, 'Cabane', False, [], None), 'v_cab_f': ('sv_cab0', 30.0, 20.5, 'Cabane', False, [], None)},
 'sv2': {  # v14 : Sous-Ville, la Cuve : atelier d'Elio, monte-charge vers Center-Town
  'v_cab_g': ('sv_cab2', 2.0, 3.0, 'Cabane', False, [], None), 'v_atelier': ('sv_atelier', 10.0, 2.5, 'Atelier d\'Elio', True, [], 'key'),
  'v_cab_h': ('sv_cab3', 19.0, 2.0, 'Cabane', False, [], None), 'v_lift': ('sv_lift', 30.0, 4.0, 'Monte-charge', False, [], None),
  'v_cab_i': ('sv_cab0', 4.0, 20.0, 'Cabane', False, [], None), 'v_cab_j': ('sv_cab1', 18.0, 20.5, 'Cabane', False, [], None)},
 'center': {  # v13 : Center-Town de nuit (concept art) : rotonde, change, tour Arcadius au nord ; rangée sud de la maquette
  'c_tour':      ('st_ct_dome', 16.0, 1.0, 'La Rotonde', False, [], None),
  'c_change':    ('st_ct_shop', 4.0, 5.0, 'Change de Teng', True, [], 'coin'),
  'c_arcadius':  ('st_ct_tower', 35.0, 3.0, 'Arcadius Center', False, [], None),
  'c_immeuble':  ('st_immeuble', 2.0, 24.0, 'Immeuble aux escaliers', False, [], None),
  'c_galerie':   ('st_galerie', 10.0, 24.0, 'Passage couvert', False, [], None),
  'c_neon':      ('st_neon', 21.0, 24.0, 'Galerie Néon', False, [], None),
  'c_jumelles':  ('st_jumelles', 28.0, 24.0, 'Tours jumelles', False, [], None),
  'c_blanc':     ('st_blanc', 37.0, 24.0, 'Bureau des permis', False, [], None)},
}
DOORS_PX = json.load(open(OUT + 'art-gen/steel_doors_px.json')) if len(sys.argv) < 2 else {}
for q in DISTRICTS:
  for bid in DISTRICTS[q]:
    if bid in DOORS_PX:
      c, x, z, l, v, _, cue = DISTRICTS[q][bid]; DISTRICTS[q][bid] = (c, x, z, l, v, [tuple(p) for p in DOORS_PX[bid]], cue)
def key_green(path):  # v13 : porte générée sur fond vert sombre uni (0, 24, 0) ; l'objet, très sombre, est gris neutre
  a = np.asarray(Image.open(path).convert('RGB')).astype(float); r, g, b = a[..., 0], a[..., 1], a[..., 2]
  ex = g - np.maximum(r, b); al = np.clip((15 - ex) / 8, 0, 1); al = ndimage.binary_opening(al > 0.5, iterations=2) * al
  a[..., 1] = np.minimum(g, np.maximum(r, b) + 4)  # retire le voile vert des bords
  import tools_interiors as TI
  return TI.clean(np.dstack([a, al * 255]).astype('uint8'), 4000)
def key_bg(path, q=None):  # v13 : fond uni (magenta) retiré par distance à la couleur du fond seulement : garde les néons violets de l'objet
  a = np.asarray(Image.open(path).convert('RGB')).astype(float)
  if q is not None: H, W = a.shape[:2]; c, r = q % 2, q // 2; a = a[r * H // 2:(r + 1) * H // 2, c * W // 2:(c + 1) * W // 2]  # v14 : planche 2x2
  bg = np.median(np.concatenate([a[:10, :10].reshape(-1, 3), a[:10, -10:].reshape(-1, 3), a[-10:, :10].reshape(-1, 3), a[-10:, -10:].reshape(-1, 3)]), 0)
  d = np.sqrt(((a - bg) ** 2).sum(2)); al = np.clip((d - 45) / 45, 0, 1)
  al = ndimage.binary_erosion(ndimage.binary_opening(al > 0.5, iterations=2), iterations=2) * al  # v13 : on rogne 2 px de bord (liseré violet du fond)
  k = np.clip(al, 0.05, 1)[..., None]; a = np.clip((a - (1 - k) * bg) / k, 0, 255)  # retire la part de fond des bords
  if 'gen_sv_' in path:  # v14 : Sous-Ville (tons chauds, aucun violet voulu) : liseré magenta du fond retiré sur 8 px de bord
    edge = (al > 0) & ~ndimage.binary_erosion(al > 0, iterations=8); mag = (a[..., 0] > a[..., 1] + 40) & (a[..., 2] > a[..., 1] + 25)
    al = np.where(edge & mag, 0, al); al = ndimage.binary_opening(al > 0.5, iterations=1) * al
    mag = (a[..., 0] > a[..., 1] + 20) & (a[..., 2] > a[..., 1] + 12); gg = a[..., 1][mag]; a[mag] = np.stack([gg * 1.25, gg, gg * 0.85], 1)  # ombres teintées de rose -> brun
  import tools_interiors as TI
  return TI.clean(np.dstack([a, al * 255]).astype('uint8'), 4000)
def load_cell(cell):
  f, c, r = CELLS[cell]
  if f.startswith('GEN'):
    sys.path.insert(0, OUT); import tools_interiors as TI
    fix = f.startswith('GENFIX'); q = int(f.split(':')[2]) if f.startswith('GENFIXQ:') else None; f = 'GEN:' + f.split(':')[1]
    rgba = key_green(OUT + f[4:]) if cell == 'st_porte2' else key_bg(OUT + f[4:], q) if fix else TI.quad(OUT + f[4:], -1).copy()
    if fix: rgba, info = TI.v4fix(rgba, **({'force': (0.5, 0.5), 'mirror': False} if cell == 'st_ct_tower' else {})); print(f'  {cell}: correction v4', info)
    if cell == 'st_porte':  # v12 : dé-contamination du magenta (la v13 st_porte2 est générée sur fond vert sombre : rien à corriger)
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
  if cell in FP: w = d = 0  # pas d'ajustement au masque
  while w > 2 and not opaque(w - 0.4, 0.4): w -= 0.5
  while d > 2 and not opaque(0.4, d - 0.4): d -= 0.5
  while (w > 2 or d > 2) and not opaque(w - 0.4, d - 0.4): w, d = (w - 0.5, d) if w >= d else (w, d - 0.5)
  if cell in FP: w, d = FP[cell]
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
js = '// Généré par tools_steel.py : ne pas éditer à la main. v12-v14 Steel-Megalopolis (route + douane, Center-Town, Sous-Ville).\n'
for q in out:
  js += f'export const BUILDINGS_{q.upper()} = ' + json.dumps(out[q][0], ensure_ascii=False) + ';\n'
  js += f'export const PAINTED_DOORS_{q.upper()} = ' + json.dumps(out[q][1], ensure_ascii=False) + ';\n'
open(OUT + 'src/data/buildings_steel.js', 'w').write(js)
for q in out:
  for b in out[q][0]: print(q, b['id'], b['x'], b['z'], b['w'], b['d'])
  for d in out[q][1]: print(q, d['id'], d['opening'], d['threshold'])
