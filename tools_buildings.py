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
# id: (planche, case col,row, placement x,z (coin min), label, visitable, portes peintes [(px, py, face)], indice)
B = {
 'mara_house': ('settlement-v9-dusk.png', 0, 0, 1.0, None, 'Maison de Mara', True, [(210, 418, 's')], 'drop'),
 'clinic':     ('buildings-v6.png', 0, 1, 10.0, None, 'Clinique', True, [(170, 890, 's')], 'cross'),
 'grocery':    ('settlement-v9-dusk.png', 1, 0, 20.0, None, 'Épicerie', True, [(718, 450, 's'), (893, 440, 'e')], 'jar'),
 'bar':        ('buildings-v6.png', 0, 0, 31.0, None, 'Le Passage', True, [(225, 460, 's')], 'bottle'),
 'halle':     ('buildings-v6.png', 1, 0, 40.0, None, 'Halle effondrée', False, [], None),
 'house_a':    ('settlement-v9-dusk.png', 1, 1, 3.0, 24.0, 'Maison à escalier', False, [], None),
 'marche':     ('buildings-v6.png', 1, 1, 9.0, 24.0, 'Marché couvert', False, [], None),
 'ruin':       ('settlement-v9-dusk.png', 2, 1, 19.0, 25.0, 'Ruine', False, [], None),
 'garages':    ('settlement-v9-dusk.png', 2, 0, 29.0, 25.0, 'Maison aux garages', False, [], None),
 'entrepot':   ('buildings-v6.png', 2, 0, 39.5, 25.0, 'Entrepôt éventré', False, [], None),
}
FRONT_Z = 13.0  # rangée nord : façade sud alignée sur le trottoir
man, blds, doors, dbg = {}, [], [], []
for bid, (f, c, r, bx, bz, label, vis, dpx, cue) in B.items():
  full = Image.open(S + f).convert('RGBA'); A = ndimage.binary_opening(np.asarray(full)[..., 3] > 100)
  lab, n = ndimage.label(A); sizes = ndimage.sum(A, lab, range(1, n + 1))
  for i in np.argsort(-sizes):
    ys, xs = np.nonzero(lab == i + 1)
    if c*512 <= xs.mean() < (c+1)*512 and r*512 <= ys.mean() < (r+1)*512: li = i + 1; break
  x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max(); ax = int(np.median(xs[ys >= y1 - 3])); ay = int(y1)
  w, d = r05((ax - x0) / (K * cy)), r05((x1 - ax) / (K * sy))
  # Emprise = plus grand rectangle dont les coins (rentrés de 0,4 m, à 0,3 m de haut) tombent sur des pixels opaques du sprite :
  # la collision ne dépasse jamais la base visible (planches dessinées avec un lacet un peu différent de la caméra).
  sp, cp = math.sin(math.radians(PITCH)), math.cos(math.radians(PITCH)); M = lab == li
  def opaque(a, b):
    px = ax + K * (-a * cy + b * sy); py = ay - K * (a * sy * sp + b * cy * sp) - K * 0.3 * cp
    px, py = int(round(px)), int(round(py)); return 0 <= py < M.shape[0] and 0 <= px < M.shape[1] and M[py, px]
  w0, d0 = w, d
  while w > 2 and not opaque(w - 0.4, 0.4): w -= 0.5
  while d > 2 and not opaque(0.4, d - 0.4): d -= 0.5
  while (w > 2 or d > 2) and not opaque(w - 0.4, d - 0.4): w, d = (w - 0.5, d) if w >= d else (w, d - 0.5)
  if (w, d) != (w0, d0): print(f'  {bid}: emprise réduite {w0}x{d0} -> {w}x{d} (base visible)')
  if bz is None: bz = FRONT_Z - d
  P = (bx + w, bz + d)
  m = ndimage.binary_dilation(lab == li, iterations=2)[y0:y1 + 1, x0:x1 + 1]
  sub = full.crop((x0, y0, x1 + 1, y1 + 1)); sub.putalpha(Image.fromarray(np.minimum(np.asarray(sub)[..., 3], m * 255).astype('uint8')))
  name = 'b_' + bid; sub.save(OUT + 'assets/buildings/' + name + '.webp', quality=90, lossless=False)
  man[name] = {'file': 'buildings/' + name + '.webp', 'source': f, 'crop': [int(x0), int(y0), int(x1) + 1, int(y1) + 1],
               'px': list(sub.size), 'anchor': [ax - int(x0), ay - int(y0)], 'footprint_m': [w, d]}
  blds.append({'id': bid, 'label': label, 'sprite': name, 'x': bx, 'z': bz, 'w': w, 'd': d, 'visitable': vis, 'cue': cue})
  t = Image.new('RGB', sub.size, '#444'); t.paste(sub, mask=sub); dr = ImageDraw.Draw(t)
  dr.ellipse([ax-x0-6, ay-y0-6, ax-x0+6, ay-y0+6], outline='red', width=3)
  for k, (px, py, face) in enumerate(dpx):
    dx = px - ax
    if face == 's': s = -dx / (K * cy); o = (round(P[0] - s, 2), P[1]); th = (o[0], P[1] + 1)
    else: s = dx / (K * sy); o = (P[0], round(P[1] - s, 2)); th = (P[0] + 1, o[1])
    doors.append({'id': f'{bid}_door' + ('' if k == 0 else str(k + 1)), 'buildingId': bid, 'painted_px': [px, py], 'face': face, 'opening': o, 'threshold': th})
    dr.ellipse([px-x0-7, py-y0-7, px-x0+7, py-y0+7], outline='#0f0', width=3)
  dbg.append(t)
json.dump(man, open(OUT + 'assets/buildings/manifest.json', 'w'), indent=1, ensure_ascii=False)
js = '// Généré par tools_buildings.py : ne pas éditer à la main.\n'
js += f'export const ART = {{ pxPerMeter: {K}, yawDeg: {YAW}, pitchDeg: {PITCH} }};\n'
js += 'export const BUILDINGS_Q1 = ' + json.dumps(blds, ensure_ascii=False) + ';\n'
js += 'export const PAINTED_DOORS_Q1 = ' + json.dumps(doors, ensure_ascii=False) + ';\n'
open(OUT + 'src/data/buildings_q1.js', 'w').write(js)
W = Image.new('RGB', (5 * 500, 2 * 520), '#222')
for i, t in enumerate(dbg): t.thumbnail((490, 510)); W.paste(t, ((i % 5) * 500, (i // 5) * 520))
W.save('/tmp/bdbg.jpg')
for b in blds: print(b['id'], b['x'], b['z'], b['w'], b['d'])
for d in doors: print(d['id'], d['opening'], d['threshold'])
