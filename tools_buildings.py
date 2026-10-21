# Bâtiments v4 : sprites entiers de la maquette, posés tels quels. Une seule échelle (K px d'image par mètre-écran),
# une caméra accordée à la projection des planches (lacet 34,5°, tangage 28,8°, mesurés sur les pentes des arêtes de base).
# Planche exterior-buildings-v4 écartée : projection différente (lacet inversé), emprise incohérente avec la caméra.
# Pour chaque sprite : recadrage, ancre = coin de base avant (point opaque le plus bas), emprise w x d déduite des
# extrêmes gauche/droite de la base, porte peinte (pixel source) -> point monde. Sources jamais modifiées.
import numpy as np, math, json
from PIL import Image, ImageDraw
from scipy import ndimage
S='/workspace/nml/src/a/No-Mans-Land_Reconstruction/07_MAQUETTE_ARCHIVE_v0.13/art-source/'
OUT='/workspace/nml/game/'
YAW, PITCH, K = 34.5, 28.8, 50
cy, sy = math.cos(math.radians(YAW)), math.sin(math.radians(YAW))
r05 = lambda v: round(v * 2) / 2
# Cases de la maquette (ou image générée contrôlée) : un sprite par case, réutilisable dans plusieurs quartiers (jamais deux fois dans le même).
CELLS = {
 'mara_house': ('settlement-v9-dusk.png', 0, 0), 'clinic': ('buildings-v6.png', 0, 1), 'grocery': ('settlement-v9-dusk.png', 1, 0),
 'bar': ('buildings-v6.png', 0, 0), 'halle': ('buildings-v6.png', 1, 0), 'house_a': ('settlement-v9-dusk.png', 1, 1),
 'marche': ('buildings-v6.png', 1, 1), 'ruin': ('settlement-v9-dusk.png', 2, 1), 'garages': ('settlement-v9-dusk.png', 2, 0),
 'entrepot': ('buildings-v6.png', 2, 0),
 'cinema': ('buildings-v6.png', 2, 1),  # v7 : dernière case dusk inutilisée
 'lab': ('GEN:art-gen/gen_lab_bunker.jpg', 6.0, 4.0),  # v7 : GenerateImage (aucune case maquette), angle contrôlé par judge(), mis à l'échelle K
}
FRONT_Z = 13.0  # rangée nord de La Pompe : façade sud alignée sur le trottoir
# quartier -> id: (case, x, z (None = FRONT_Z - d), label, visitable, portes peintes [(px, py, face)] en px source, indice)
DISTRICTS = {
 'q1': {
  'mara_house': ('mara_house', 1.0, None, 'Maison de Mara', True, [(210, 418, 's')], 'drop'),
  'clinic':     ('clinic', 10.0, None, 'Clinique', True, [(170, 890, 's')], 'cross'),
  'grocery':    ('grocery', 20.0, None, 'Épicerie', True, [(718, 450, 's'), (893, 440, 'e')], 'jar'),
  'bar':        ('bar', 31.0, None, 'Le Passage', True, [(225, 460, 's')], 'bottle'),
  'halle':      ('halle', 40.0, None, 'Halle effondrée', False, [], None),
  'house_a':    ('house_a', 3.0, 24.0, 'Maison à escalier', False, [], None),
  'marche':     ('marche', 9.0, 24.0, 'Marché couvert', False, [], None),
  'ruin':       ('ruin', 19.0, 25.0, 'Ruine', False, [], None),
  'garages':    ('garages', 29.0, 25.0, 'Maison aux garages', False, [], None),
  'entrepot':   ('entrepot', 39.5, 25.0, 'Entrepôt éventré', False, [], None)},
 'q2': {  # Le Transit (est) : l'avenue des patrouilles
  't_guet':     ('house_a', 3.0, None, 'Le guet', True, [(713, 919, 's')], 'mirror'),
  't_cinema':   ('cinema', 10.0, None, 'Cinéma muré', False, [], None),
  't_entrepot': ('entrepot', 24.0, None, 'Dépôt pillé', False, [], None),
  't_garages':  ('garages', 35.0, None, 'Relais routier', False, [], None),
  't_marche':   ('marche', 3.0, 24.0, 'Ancien marché', False, [], None),
  't_maison':   ('mara_house', 15.0, 24.0, 'Maison murée', False, [], None),
  't_ruin':     ('ruin', 26.0, 25.0, 'Ruine', False, [], None),
  't_halle':    ('halle', 38.5, 24.0, 'Station effondrée', False, [], None)},
 'q3': {  # Le Scellé (nord) : l'accès au laboratoire
  's_lab':      ('lab', 25.0, 1.5, 'Accès Human Corporation', False, [], None),
  's_halle':    ('halle', 2.0, None, 'Halle', False, [], None),
  's_atelier':  ('mara_house', 12.0, None, 'L\'atelier', True, [(210, 418, 's')], 'key'),
  's_palais':   ('bar', 33.0, None, 'Palais muré', False, [], None),
  's_entrepot': ('entrepot', 40.0, None, 'Entrepôt', False, [], None),
  's_clinic':   ('clinic', 3.0, 27.0, 'Bâtisse jaune', False, [], None),
  's_ruin':     ('ruin', 14.0, 28.0, 'Ruine', False, [], None),
  's_garages':  ('garages', 33.0, 28.0, 'Maison aux garages', False, [], None)},
 'q4': {  # Les Sables (sud) : ruines ensablées, sortie vers les terres dévastées
  'd_citerne':  ('garages', 16.0, 6.0, 'La citerne', True, [(1453, 487, 'e')], 'drop'),
  'd_ruin':     ('ruin', 13.0, 16.0, 'Ruine ensablée', False, [], None),
  'd_maison':   ('house_a', 18.0, 25.0, 'Maison ensablée', False, [], None),
  'd_cinema':   ('cinema', 33.0, 3.0, 'Cinéma ensablé', False, [], None),
  'd_entrepot': ('entrepot', 34.0, 15.0, 'Entrepôt ensablé', False, [], None),
  'd_marche':   ('marche', 33.0, 25.0, 'Marché ensablé', False, [], None)},
}
def load_cell(cell):
  f, c, r = CELLS[cell]
  if f.startswith('GEN:'):
    import tools_interiors as TI
    rgba = TI.quad('/workspace/nml/game/' + f[4:], -1); a = rgba[..., 3] > 100
    ys, xs = np.nonzero(a); lo = xs.min(); ax = int(np.median(xs[ys >= ys.max() - 3]))
    # mise à l'échelle : la largeur écran de l'emprise voulue (c x r m) = K (w cy + d sy)
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
man, out, dbg, geo = {}, {}, [], {}
sp, cp = math.sin(math.radians(PITCH)), math.cos(math.radians(PITCH))
for cell in CELLS:
  full, lab, li, f = load_cell(cell)
  ys, xs = np.nonzero(lab == li)
  x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max(); ax = int(np.median(xs[ys >= y1 - 3])); ay = int(y1)
  w, d = r05((ax - x0) / (K * cy)), r05((x1 - ax) / (K * sy))
  # Emprise = plus grand rectangle dont les coins (rentrés de 0,4 m, à 0,3 m de haut) tombent sur des pixels opaques du sprite :
  # la collision ne dépasse jamais la base visible (planches dessinées avec un lacet un peu différent de la caméra).
  M = lab == li
  def opaque(a, b):
    px = ax + K * (-a * cy + b * sy); py = ay - K * (a * sy * sp + b * cy * sp) - K * 0.3 * cp
    px, py = int(round(px)), int(round(py)); return 0 <= py < M.shape[0] and 0 <= px < M.shape[1] and M[py, px]
  w0, d0 = w, d
  while w > 2 and not opaque(w - 0.4, 0.4): w -= 0.5
  while d > 2 and not opaque(0.4, d - 0.4): d -= 0.5
  while (w > 2 or d > 2) and not opaque(w - 0.4, d - 0.4): w, d = (w - 0.5, d) if w >= d else (w, d - 0.5)
  if (w, d) != (w0, d0): print(f'  {cell}: emprise réduite {w0}x{d0} -> {w}x{d} (base visible)')
  m = ndimage.binary_dilation(lab == li, iterations=2)[y0:y1 + 1, x0:x1 + 1]
  sub = full.crop((x0, y0, x1 + 1, y1 + 1)); sub.putalpha(Image.fromarray(np.minimum(np.asarray(sub)[..., 3], m * 255).astype('uint8')))
  name = 'b_' + cell; sub.save(OUT + 'assets/buildings/' + name + '.webp', quality=90, lossless=False)
  man[name] = {'file': 'buildings/' + name + '.webp', 'source': f, 'crop': [int(x0), int(y0), int(x1) + 1, int(y1) + 1],
               'px': list(sub.size), 'anchor': [ax - int(x0), ay - int(y0)], 'footprint_m': [w, d]}
  geo[cell] = (w, d, ax, ay, x0, y0, sub)
for q, B in DISTRICTS.items():
  blds, doors = [], []
  for bid, (cell, bx, bz, label, vis, dpx, cue) in B.items():
    w, d, ax, ay, x0, y0, sub = geo[cell]
    if bz is None: bz = FRONT_Z - d
    P = (bx + w, bz + d)
    blds.append({'id': bid, 'label': label, 'sprite': 'b_' + cell, 'x': bx, 'z': bz, 'w': w, 'd': d, 'visitable': vis, 'cue': cue})
    if q == 'q1' or dpx:
      t = Image.new('RGB', sub.size, '#444'); t.paste(sub, mask=sub); dr = ImageDraw.Draw(t)
      dr.ellipse([ax-x0-6, ay-y0-6, ax-x0+6, ay-y0+6], outline='red', width=3)
    for k, (px, py, face) in enumerate(dpx):
      dx = px - ax
      if face == 's': s_ = -dx / (K * cy); o = (round(P[0] - s_, 2), P[1]); th = (o[0], P[1] + 1)
      else: s_ = dx / (K * sy); o = (P[0], round(P[1] - s_, 2)); th = (P[0] + 1, o[1])
      doors.append({'id': f'{bid}_door' + ('' if k == 0 else str(k + 1)), 'buildingId': bid, 'painted_px': [px, py], 'face': face, 'opening': o, 'threshold': th})
      dr.ellipse([px-x0-7, py-y0-7, px-x0+7, py-y0+7], outline='#0f0', width=3)
    if q == 'q1' or dpx: dbg.append(t)
  out[q] = (blds, doors)
json.dump(man, open(OUT + 'assets/buildings/manifest.json', 'w'), indent=1, ensure_ascii=False)
js = '// Généré par tools_buildings.py : ne pas éditer à la main.\n'
js += f'export const ART = {{ pxPerMeter: {K}, yawDeg: {YAW}, pitchDeg: {PITCH} }};\n'
js += 'export const BUILDINGS_Q1 = ' + json.dumps(out['q1'][0], ensure_ascii=False) + ';\n'
js += 'export const PAINTED_DOORS_Q1 = ' + json.dumps(out['q1'][1], ensure_ascii=False) + ';\n'
open(OUT + 'src/data/buildings_q1.js', 'w').write(js)
js = '// Généré par tools_buildings.py : ne pas éditer à la main. v7 : quartiers 2 à 4 (mêmes sprites, autres emplacements).\n'
for q in ['q2', 'q3', 'q4']:
  js += f'export const BUILDINGS_{q.upper()} = ' + json.dumps(out[q][0], ensure_ascii=False) + ';\n'
  js += f'export const PAINTED_DOORS_{q.upper()} = ' + json.dumps(out[q][1], ensure_ascii=False) + ';\n'
open(OUT + 'src/data/buildings_town.js', 'w').write(js)
blds = [b for q in out for b in out[q][0]]; doors = [d for q in out for d in out[q][1]]
for b in blds: print(b['id'], b['x'], b['z'], b['w'], b['d'])
for d in doors: print(d['id'], d['opening'], d['threshold'])
