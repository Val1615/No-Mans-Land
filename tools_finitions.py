# Finitions visuelles (branche creation/finitions-visuelles). N'écrit jamais dans src/.
# 1) porte du sarcophage v3 (dôme entier)  2) matte du projecteur et de la rotonde  3) table de jeu rectangulaire
import json, math, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tools_interiors as TI
YAW, PITCH, K = 34.5, 28.8, 50
cy, sy = math.cos(math.radians(YAW)), math.sin(math.radians(YAW))
G = HERE + '/art-gen/'; A = HERE + '/assets/'

def mag_edge_pct(rgba):
    """% des pixels de bord (alpha 1..254, ou opaques à 2 px du transparent) à teinte magenta."""
    a = rgba[..., 3].astype(int); op = a > 0
    edge = ((a > 0) & (a < 255)) | (op & ~ndimage.binary_erosion(op, iterations=2))
    p = rgba[..., :3].astype(int); r, g, b = p[..., 0], p[..., 1], p[..., 2]
    mag = (np.minimum(r, b) - g > 25) & (r > 60) & (b > 60)
    n = edge.sum(); return round(100 * (mag & edge).sum() / max(1, n), 2), int(n)

def rematte(rgba, erode=2, band_px=3):
    """despill magenta, alpha durci, érosion, bords recolorés depuis les voisins opaques."""
    rgba = rgba.copy(); p = rgba[..., :3].astype(float); al = rgba[..., 3].astype(float) / 255
    hard = ndimage.binary_opening(al > 0.6, iterations=1)
    hard = ndimage.binary_erosion(hard, iterations=erode)
    hard = ndimage.binary_fill_holes(hard)  # trous intérieurs (lampes blanches mal détourées) bouchés
    lab, n = ndimage.label(hard); s = ndimage.sum(hard, lab, range(1, n + 1)); hard = np.isin(lab, [i + 1 for i, v in enumerate(s) if v >= 30])
    core = ndimage.binary_erosion(hard, iterations=band_px)
    # recoloration : chaque pixel de la bande de bord prend la couleur du pixel du coeur le plus proche
    _, (iy, ix) = ndimage.distance_transform_edt(~core, return_indices=True)
    p0 = p.copy(); holes = hard & (al < 0.6)  # pixels de trou bouchés : couleur d origine conservée (premultipliée par le fond, déjà sombre ou blanche)
    band = hard & ~core; p[band] = p[iy[band], ix[band]]
    r, g, b = p[..., 0], p[..., 1], p[..., 2]; spill = np.clip(np.minimum(r, b) - g, 0, None)
    m = band  # seulement la bande de bord : les néons violets voulus de l objet restent intacts
    p[..., 0] = np.where(m, r - spill * 0.85, r); p[..., 2] = np.where(m, b - spill * 0.85, b)
    # alpha : 255 à l'intérieur, 1 px d'anticrénelage
    soft = ndimage.gaussian_filter(hard.astype(float), 0.6); soft[hard] = np.maximum(soft[hard], 0.85)
    out = np.dstack([np.clip(p, 0, 255), np.clip(soft, 0, 1) * 255]).astype('uint8'); out[soft < 0.08] = 0
    return out

GATE_SCALE = 1.10  # mesuré : l'arche de gen_steel_gate3 est 0,91x celle de gen_steel_gate2 à largeur totale égale
def align_to_old(new, old_path=G + 'matte-src/b_st_porte2_v13.webp', old_anchor=(1486, 828)):
    # ancre recalée pour que l'arche et les murs restent au même point monde que dans l'ancien sprite (l'image ne grandit que vers le haut)
    import cv2
    g = lambda a: cv2.cvtColor(np.ascontiguousarray(a[..., :3]), cv2.COLOR_RGB2GRAY).astype(np.float32)
    o = np.asarray(Image.open(old_path).convert('RGBA')); T = g(o)[120:620, 420:1050]
    r = cv2.matchTemplate(g(np.asarray(new)), T, cv2.TM_CCOEFF_NORMED); _, mx, _, loc = cv2.minMaxLoc(r)
    dx, dy = loc[0] - 420, loc[1] - 120; print('  recalage arche: score', round(mx, 3), 'décalage', dx, dy)
    return [old_anchor[0] + dx, old_anchor[1] + dy]
def gate():
    raw = Image.open(G + 'gen_steel_gate3_raw.jpg').convert('RGB'); a = np.asarray(raw)
    bg = tuple(int(v) for v in np.median(a[:10, :10].reshape(-1, 3), 0)); P = 140
    pad = Image.new('RGB', (raw.size[0], raw.size[1] + P), bg); pad.paste(raw, (0, P)); pad.save(G + 'gen_steel_gate3.jpg', quality=95)
    import importlib.util
    src = open(HERE + '/tools_steel.py').read(); ns = {}
    exec(src[src.index('def key_green'):src.index('def key_bg')], {'np': np, 'Image': Image, 'ndimage': ndimage, '__builtins__': __builtins__}, ns)
    rgba = ns['key_green'](G + 'gen_steel_gate3.jpg')
    al = rgba[..., 3] > 100; ys, xs = np.nonzero(al)
    sc = K * (30.0 * cy + 9.0 * sy) / (xs.max() - xs.min() + 1) * GATE_SCALE  # GATE_SCALE : arche à la même taille que l'ancien sprite
    im = Image.fromarray(rgba).resize((int(rgba.shape[1] * sc), int(rgba.shape[0] * sc)), Image.LANCZOS)
    full = Image.new('RGBA', (im.size[0] + 20, im.size[1] + 20), (0, 0, 0, 0)); full.alpha_composite(im, (10, 10))
    M = ndimage.binary_opening(np.asarray(full)[..., 3] > 100); lab, n = ndimage.label(M); sz = ndimage.sum(M, lab, range(1, n + 1)); M = lab == int(np.argmax(sz)) + 1
    ys, xs = np.nonzero(M); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max(); ax = int(np.median(xs[ys >= y1 - 3])); ay = int(y1)
    m = ndimage.binary_dilation(M, iterations=2)[y0:y1 + 1, x0:x1 + 1]
    sub = full.crop((x0, y0, x1 + 1, y1 + 1)); sub.putalpha(Image.fromarray(np.minimum(np.asarray(sub)[..., 3], m * 255).astype('uint8')))
    sub.save(A + 'buildings/b_st_porte2.webp', quality=90)
    man = json.load(open(A + 'buildings/manifest.json')); old = dict(man['b_st_porte2'])
    man['b_st_porte2'].update({'source': 'art-gen/gen_steel_gate3.jpg', 'crop': [int(x0), int(y0), int(x1) + 1, int(y1) + 1], 'px': list(sub.size),
                               'anchor': align_to_old(sub), 'anchor_note': 'ancre recalée sur l ancien sprite (arche au même point monde) ; coin bas détecté ' + str([ax - int(x0), ay - int(y0)]), 'lot': 'steel-l1 v12 ; finitions v15 : dôme entier'})
    json.dump(man, open(A + 'buildings/manifest.json', 'w'), indent=1, ensure_ascii=False)
    print('porte2', old, '->', man['b_st_porte2'], 'echelle', round(sc, 3))
    q = np.asarray(pad).astype(int); obj = np.abs(q - np.array(bg)).sum(2) > 40; rows = np.nonzero(obj.sum(1) > 5)[0]
    print('  marge haute source : brute %.1f%%, après pad %.1f%%' % (100 * (rows.min() - P) / a.shape[0], 100 * rows.min() / q.shape[0]))

def mattes():
    res = {}
    sheet = TI.quad(G + 'gen_fort_sheet.jpg', 3)  # même extraction que tools_steel_decor
    im = Image.fromarray(sheet, 'RGBA'); im.thumbnail((512, 512)); before = np.asarray(im).copy()
    old_disk = before  # même extraction que le sprite v13 d'origine
    fixed = rematte(before, 1, 1)  # petit sprite : bande de recoloration de 1 px (garde les arêtes nettes); Image.fromarray(fixed).save(A + 'generated/st_projecteur.webp', quality=92)
    res['st_projecteur'] = (mag_edge_pct(old_disk), mag_edge_pct(np.asarray(Image.open(A + 'generated/st_projecteur.webp').convert('RGBA'))), fixed.shape[1::-1])
    d = np.asarray(Image.open(G + 'matte-src/b_st_ct_dome_v14.webp').convert('RGBA'))  # sprite v14 d'origine (idempotent)
    fd = rematte(d, 2); Image.fromarray(fd).save(A + 'buildings/b_st_ct_dome.webp', quality=92)
    res['b_st_ct_dome'] = (mag_edge_pct(d), mag_edge_pct(np.asarray(Image.open(A + 'buildings/b_st_ct_dome.webp').convert('RGBA'))), fd.shape[1::-1])
    for k, v in res.items(): print(k, 'magenta bord avant %s%% (n=%d) -> après %s%% (n=%d), px %s' % (v[0][0], v[0][1], v[1][0], v[1][1], v[2]))
    return res

def key_green_obj(path):
    a = np.asarray(Image.open(path).convert('RGB')).astype(float); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    ex = g - np.maximum(r, b)                      # fond vert vif (0, 230, 0)
    al = np.clip((150 - ex) / 60, 0, 1)
    al = ndimage.binary_opening(al > 0.5, iterations=2) * al
    a[..., 1] = np.minimum(g, np.maximum(r, b) * 1.15 + 6) * (al < 0.999) + g * (al >= 0.999)  # despill vert des bords
    hard = ndimage.binary_fill_holes(al > 0.5); al = np.where(hard, np.maximum(al, (ex < 60)), al)
    return TI.clean(np.dstack([np.clip(a, 0, 255), al * 255]).astype('uint8'), 4000)

def cardtable():
    aid, w, d, h = 'sv_cardtable_b', 1.2, 1.2, 0.9
    rgba, fix = TI.v4fix(key_green_obj(G + 'gen_sv_cardtable3.jpg'))
    j = TI.judge(rgba); hh = rgba.shape[0] / rgba.shape[1]; j['correction_v4'] = fix; j['sens'] = 'direct'
    if abs(fix['pentes_apres'][0] - 0.33) <= 0.06 and abs(fix['pentes_apres'][1] - 0.70) <= 0.06: j['accepte'] = True; j['regle'] = 'arête basse v4'
    R, U = TI.R, TI.U; sw = w * abs(R[0]) + d * abs(R[2]); implied = (sw * hh - w * abs(U[0]) - d * abs(U[2])) / U[1]
    j.update({'source': 'généré art-gen/gen_sv_cardtable3.jpg #-1', 'role': 'table de jeu rectangulaire sur caisses, cartes et jetons (généré, angle corrigé ; remplace sv_cardtable rejetée)',
              'emprise_m': [w, d], 'hauteur_attendue_m': h, 'hauteur_implicite_m': round(implied, 2)})
    j['echelle_ok'] = bool(abs(implied - h) <= 0.3 * h + 0.15)
    rep = json.load(open(A + 'interiors/rapport_angles.json')); rep[aid] = j; json.dump(rep, open(A + 'interiors/rapport_angles.json', 'w'), ensure_ascii=False, indent=1)
    print(aid, j)
    if j['accepte'] and j['echelle_ok']:
        im = Image.fromarray(rgba, 'RGBA'); im.thumbnail((640, 640)); im.save(A + 'interiors/' + aid + '.webp', quality=90)
        man = json.load(open(A + 'interiors/manifest.json'))
        man[aid] = {'file': f'interiors/{aid}.webp', 'px': list(im.size), 'footprint_m': [w, d], 'height_m': h, 'origin': 'généré', 'source': j['source'], 'mirrored_from_source': False}
        json.dump(man, open(A + 'interiors/manifest.json', 'w'), ensure_ascii=False, indent=1); print('exporté', man[aid])

if __name__ == '__main__':
    for step in (sys.argv[1:] or ['gate', 'mattes', 'cardtable']): globals()[step]()
