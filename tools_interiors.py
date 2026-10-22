# Intérieurs Dusk-Town Q1 (v6) : extraction et CONTRÔLE D'ANGLE des assets d'intérieur.
# Lit (sans les modifier) les planches de la maquette src/a/.../art-source/ et les générations game/art-gen/,
# écrit game/assets/interiors/*.webp + manifest.json + rapport_angles.json. Reproductible.
# Règle d'angle (caméra v4 : lacet 34,5°, tangage 28,8°) : l'axe x monde apparaît à l'écran avec une pente de 0,33
# (vers le bas-droite), l'axe z avec une pente de 0,70 (vers le bas-gauche). Un sprite est accepté si la pente dominante
# de ses arêtes (Hough sur les contours) est dans [0,25 ; 0,42] (bande mesurée sur les 10 planches de bâtiments v4 :
# 0,30 à 0,40) et si la pente opposée, quand elle est détectée, n'est pas proche de 0,5 (projection 2:1). Sinon : rejet.
import json, math, os, sys
import numpy as np, cv2
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '../src/a/No-Mans-Land_Reconstruction/07_MAQUETTE_ARCHIVE_v0.13/art-source/')
GEN = os.path.join(HERE, 'art-gen/'); OUT = os.path.join(HERE, 'assets/interiors/'); os.makedirs(OUT, exist_ok=True)
YAW, PIT = math.radians(34.5), math.radians(28.8)
cd = np.array([-math.sin(YAW)*math.cos(PIT), -math.sin(PIT), -math.cos(YAW)*math.cos(PIT)])
R = np.cross(cd, [0, 1, 0]); R /= np.linalg.norm(R); U = np.cross(R, cd); U /= np.linalg.norm(U)

def slope_hist(rgba):
    a = rgba[:, :, 3]; g = cv2.cvtColor(np.ascontiguousarray(rgba[:, :, :3]), cv2.COLOR_RGB2GRAY); g[a < 128] = 0
    e = cv2.Canny(g, 60, 160); L = cv2.HoughLinesP(e, 1, np.pi/360, 30, minLineLength=max(25, rgba.shape[1]//10), maxLineGap=3)
    h = {}
    for x1, y1, x2, y2 in ([] if L is None else L.reshape(-1, 4)):
        dx, dy = x2-x1, y2-y1
        if dx == 0: continue
        s = dy/dx
        if 0.12 < abs(s) < 1.3: b = round(round(s/0.05)*0.05, 2); h[b] = h.get(b, 0) + math.hypot(dx, dy)
    t = sum(h.values()) or 1
    return {k: v/t for k, v in h.items()}
def judge(rgba):
    h = slope_hist(rgba)
    pos = sum(v for k, v in h.items() if k > 0); neg = sum(v for k, v in h.items() if k < 0)
    sign = 1 if pos >= neg else -1
    side = {abs(k): v for k, v in h.items() if k*sign > 0}; other = {abs(k): v for k, v in h.items() if k*sign < 0}
    band = lambda d, lo, hi: sum(v for k, v in d.items() if lo <= k <= hi)
    prim = max(side, key=side.get) if side else None
    near21_other = band(other, 0.45, 0.55)
    ok = prim is not None and 0.25 <= prim <= 0.42 and near21_other < 0.12
    # v13 : objet plus profond que large (face z dominante) : pente dominante dans la bande z de la caméra v4 (0,70)
    ok = ok or (prim is not None and 0.62 <= prim <= 0.8 and near21_other < 0.12)
    return {'pente_dominante': prim, 'sens': 'direct' if sign > 0 else 'miroir', 'part_bande_v4': round(band(side, 0.25, 0.42), 2),
            'part_2_1_opposee': round(near21_other, 2), 'accepte': bool(ok)}

def key_magenta(im):
    a = np.asarray(im.convert('RGB')).astype(float); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    bg = np.median(np.concatenate([a[:8, :8].reshape(-1, 3), a[:8, -8:].reshape(-1, 3), a[-8:, :8].reshape(-1, 3), a[-8:, -8:].reshape(-1, 3)]), 0)  # fond uni estimé aux coins
    d = np.sqrt((r-bg[0])**2 + (g-bg[1])**2*1.6 + (b-bg[2])**2)
    al = np.clip((d - 70) / 60, 0, 1)
    mag = (np.minimum(r, b) - g) / (np.maximum(r, b) + 1)  # ombres magenta peintes par le générateur : teinte magenta quelle que soit la luminosité
    al = al * np.clip((0.42 - mag) / 0.2, 0, 1)
    # despill : retire la teinte magenta des bords
    m = np.minimum(r, b); spill = np.clip(m - g, 0, None) * (1 - al) ; a[..., 0] -= spill*0.8; a[..., 2] -= spill*0.8
    al = ndimage.binary_opening(al > 0.5, iterations=1) * al
    return np.dstack([np.clip(a, 0, 255), al*255]).astype('uint8')
def clean(rgba, min_area=400):
    a = rgba[:, :, 3] > 40; lab, n = ndimage.label(a); sizes = ndimage.sum(a, lab, range(1, n+1))
    keep = np.isin(lab, [i+1 for i, s in enumerate(sizes) if s >= min_area]); rgba = rgba.copy(); rgba[~keep, 3] = 0
    ys, xs = np.nonzero(rgba[:, :, 3] > 40); return rgba[ys.min():ys.max()+1, xs.min():xs.max()+1]
def quad(path, q):
    rgba = key_magenta(Image.open(path)); H, W = rgba.shape[:2]
    if q < 0: return clean(rgba)  # image d'un seul objet
    c, r = q % 2, q // 2
    return clean(rgba[r*H//2:(r+1)*H//2, c*W//2:(c+1)*W//2])
# v13 : correction d'angle des images générées en isométrie 2:1 (pentes ~0,5 / 0,5) vers la caméra v4 (0,33 à gauche, 0,70 à droite).
# Cisaillement vertical seulement (les verticales restent verticales) : y' = d*y + c*(x - ax), calculé sur les pentes mesurées
# de l'arête basse (enveloppe inférieure du masque). Si l'arête la plus douce est à droite, l'image est d'abord mise en miroir.
def base_slopes(rgba):
    a = rgba[:, :, 3] > 100; cols = np.nonzero(a.any(0))[0]; low = np.array([np.nonzero(a[:, x])[0].max() for x in cols])
    i = int(np.argmax(low)); ax = cols[i]; W = cols[-1] - cols[0]
    L = (cols < ax - 0.08 * W) & (cols > cols[0] + 0.08 * W); Rr = (cols > ax + 0.08 * W) & (cols < cols[-1] - 0.08 * W)
    sl = np.polyfit(cols[L], low[L], 1)[0] if L.sum() > 5 else 0.5; sr = -np.polyfit(cols[Rr], low[Rr], 1)[0] if Rr.sum() > 5 else 0.5
    return float(sl), float(sr), int(ax), int(low[i])
def v4fix(rgba, tl=0.33, tr=0.70, force=None, mirror=None):
    sl, sr, ax, ay = base_slopes(rgba); mirrored = False
    if force: sl, sr = force  # objet à pieds (arche, tourniquet) : l'arête basse ne se mesure pas, pentes 2:1 de la génération
    if (sr < sl if mirror is None else mirror):
        rgba = rgba[:, ::-1].copy(); mirrored = True
        if force: sl, sr = sr, sl; ax = rgba.shape[1] - 1 - ax
        else: sl, sr, ax, ay = base_slopes(rgba)
    d = (tl + tr) / max(0.2, sl + sr); c = tl - d * sl
    H, W = rgba.shape[:2]; top = min(0, c * (0 - ax), c * (W - ax)); bot = max(d * H + c * (0 - ax), d * H + c * (W - ax))
    nh = int(bot - top) + 2
    # PIL : pixel source = A^-1 (x', y') ; y = (y' + top - c*(x - ax)) / d, x = x'
    im = Image.fromarray(rgba, 'RGBA').transform((W, nh), Image.AFFINE, (1, 0, 0, -c / d, 1 / d, (top + c * ax) / d), resample=Image.BICUBIC)
    out = clean(np.asarray(im).copy(), 200)
    return out, {'pentes_source': [round(sl, 2), round(sr, 2)], 'cisaillement': [round(d, 3), round(c, 3)], 'miroir': mirrored, 'pentes_apres': [round(v, 2) for v in base_slopes(out)[:2]]}
def mock(sheet, idx):
    im = np.array(Image.open(SRC + sheet).convert('RGBA')); a = im[:, :, 3] > 40
    lab, n = ndimage.label(ndimage.binary_dilation(a, iterations=6)); objs = []
    for k, sl in enumerate(ndimage.find_objects(lab)):
        m = (lab[sl] == k+1) & a[sl]
        if m.sum() >= 4000: objs.append((sl, m))
    objs.sort(key=lambda t: (t[0][0].start // 300, t[0][1].start)); sl, m = objs[idx]; sub = im[sl].copy(); sub[~m, 3] = 0
    return clean(sub)

# (id, source, extraction, emprise w x d en m (w le long de l'axe x monde), hauteur réelle attendue (m), rôle)
ASSETS = [
  ('clinic_cot',     ('gen', 'gen_clinic_sheet.jpg', 0), 2.0, 0.9, 0.95, 'lit de camp en fer, clinique'),
  ('clinic_stretcher',('gen', 'gen_clinic_sheet.jpg', 1), 2.0, 0.6, 0.6, 'civière derrière la porte (accroche quête rafles)'),
  ('clinic_cabinet', ('gen', 'gen_clinic_sheet.jpg', 2), 0.9, 0.5, 1.8, 'armoire à pharmacie'),
  ('clinic_table',   ('gen', 'gen_clinic_sheet.jpg', 3), 1.3, 0.7, 1.15, 'table de soins, cuvette, lampe'),
  ('bar_counter',    ('gen', 'gen_bar_sheet.jpg', 0), 3.8, 0.8, 1.35, 'comptoir de récupération'),
  ('bar_backshelf',  ('gen', 'gen_bar_sheet.jpg', 1), 1.8, 0.6, 2.1, 'étagère à bouteilles contre le mur'),
  ('bar_table',      ('gen', 'gen_bar_sheet.jpg', 2), 1.7, 1.3, 0.9, 'table carrée et deux tabourets'),
  ('bar_reel',       ('gen', 'gen_bar_sheet.jpg', 3), 1.9, 1.3, 0.85, 'touret de câble en table, caisses'),
  ('shop_shelf',     ('gen', 'gen_grocery_sheet.jpg', 0), 1.9, 0.5, 1.9, 'étagère de conserves'),
  ('shop_counter',   ('gen', 'gen_grocery_sheet.jpg', 1), 2.2, 0.7, 1.6, 'comptoir et balance d Anselme'),
  ('shop_filter',    ('gen', 'gen_grocery_sheet.jpg', 2), 1.3, 0.9, 1.4, 'filtre à eau en fûts, bouteilles'),
  ('shop_sacks',     ('gen', 'gen_grocery_sheet.jpg', 3), 1.6, 1.0, 1.1, 'sacs et caisses de rations (stock caché)'),
  ('home_mattress',  ('gen', 'gen_home_sheet.jpg', 0), 1.9, 0.9, 0.35, 'paillasse sur palettes'),
  ('home_curtain',   ('gen', 'gen_home_sheet.jpg', 1), 2.4, 0.15, 2.1, 'rideau derrière lequel se tient Bruno'),
  ('home_table',     ('gen', 'gen_home_sheet.jpg', 2), 1.7, 1.0, 1.0, 'table et deux chaises'),
  ('home_water',     ('gen', 'gen_home_sheet.jpg', 3), 1.3, 0.8, 0.75, 'seaux, jerrican, jarres'),
  ('bar_counter_b',  ('gen', 'gen_sheet2.jpg', 0), 3.8, 0.8, 1.4, 'comptoir de récupération, bouteilles comprises (2e génération)'),
  ('bar_backshelf_b',('gen', 'gen_sheet2.jpg', 1), 2.0, 0.6, 1.05, 'étagère basse à bouteilles et radio (2e génération)'),
  ('clinic_cot_b',   ('gen', 'gen_sheet2.jpg', 2), 2.0, 0.9, 0.95, 'lit de camp en fer (2e génération)'),
  ('clinic_stretcher_b',('gen', 'gen_sheet2.jpg', 3), 2.0, 0.6, 0.6, 'civière (2e génération)'),
  ('home_mattress_b',('gen', 'gen_sheet3.jpg', 0), 1.9, 0.9, 0.35, 'paillasse sur palettes (2e génération)'),
  ('bar_table_b',    ('gen', 'gen_sheet3.jpg', 1), 1.6, 1.2, 0.9, 'table et tabourets (2e génération)'),
  ('shop_filter_b',  ('gen', 'gen_sheet3.jpg', 2), 1.5, 0.8, 1.4, 'filtre à eau, caisse de bouteilles (2e génération)'),
  ('shop_sacks_b',   ('gen', 'gen_sheet3.jpg', 3), 1.6, 0.9, 1.0, 'sacs et caisses de rations (2e génération)'),
  ('clinic_cot_c',   ('gen', 'gen_sheet4.jpg', 0), 2.0, 0.9, 0.95, 'lit de camp en fer (3e génération)'),
  ('home_mattress_c',('gen', 'gen_sheet4.jpg', 1), 1.9, 0.9, 0.35, 'paillasse sur palette (3e génération)'),
  ('shop_filter_c',  ('gen', 'gen_sheet4.jpg', 2), 1.5, 0.8, 1.2, 'filtre à eau en fûts (3e génération)'),
  ('shop_sacks_c',   ('gen', 'gen_sheet4.jpg', 3), 1.6, 0.9, 1.0, 'sacs et caisses de rations (3e génération)'),
  ('home_mattress_d',('gen', 'gen_mattress_d.jpg', -1), 1.9, 0.9, 0.45, 'paillasse sur cadre bas (4e génération, objet seul)'),
  # maquette (prioritaire quand l'angle passe)
  ('m_archive_shelf',('mock', 'interiors-v2.png', 2), 1.6, 0.5, 1.9, 'étagère métallique (maquette)'),
  ('m_desk',         ('mock', 'service-v10-B.png', 3), 1.5, 0.7, 1.0, 'bureau métallique (maquette)'),
  ('m_locker',       ('mock', 'service-v10-B.png', 5), 0.9, 0.5, 1.9, 'casier (maquette)'),
  ('m_stove',        ('mock', 'props-v9-domestic.png', 3), 0.9, 0.7, 1.3, 'cuisinière à bois (maquette)'),
  ('m_cooktable',    ('mock', 'Props-v6.png', 3), 1.6, 0.7, 1.0, 'table de cuisine et marmites (maquette)'),
  ('m_bed',          ('mock', 'interiors-v2.png', 0), 2.0, 0.9, 0.9, 'lit d hôpital (maquette)'),
  ('m_bar_counter',  ('mock', 'service-v10-A.png', 0), 3.0, 0.8, 1.2, 'comptoir de bar (maquette)'),
  ('m_shop_shelf',   ('mock', 'service-v10-A.png', 1), 1.9, 0.5, 1.9, 'étagère d épicerie (maquette)'),
  ('m_medchair',     ('mock', 'service-v10-A.png', 5), 1.0, 1.4, 1.6, 'fauteuil médical (maquette)'),
  ('m_desk2',        ('mock', 'interiors-v2.png', 3), 1.6, 0.8, 1.0, 'bureau (maquette)'),
  # v13 Steel : poste de douane IO (cyberpunk). Maquette io-interiors-v10 et générations, angle corrigé (v4fix) puis jugé.
  ('io_reception',   ('mockfix', 'io-interiors-v10.png', 0, {}), 0.8, 2.7, 1.2, 'guichet IO en arc (maquette, angle corrigé)'),
  ('io_server',      ('mockfix', 'io-interiors-v10.png', 3, {}), 1.3, 1.5, 2.0, 'baie serveur IO (maquette, angle corrigé)'),
  ('io_sofa',        ('mockfix', 'io-interiors-v10.png', 4, {}), 0.9, 3.0, 0.7, 'banquette d attente IO (maquette, angle corrigé)'),
  ('io_display',     ('mockfix', 'io-interiors-v10.png', 5, {}), 1.8, 0.5, 2.0, 'écran sur pied IO (maquette, angle corrigé)'),
  ('io_scanner',     ('genfix', 'gen_douane_furn.jpg', 0, {'force': (0.5, 0.5), 'mirror': False}), 1.7, 0.75, 2.3, 'portique scanner corporel (généré, angle corrigé)'),
  ('io_turnstile',   ('genfix', 'gen_douane_furn.jpg', 1, {'force': (0.5, 0.5), 'mirror': False}), 1.45, 2.1, 1.0, 'tourniquet de contrôle (généré, angle corrigé)'),
  ('io_console',     ('genfix', 'gen_douane_furn.jpg', 2, {}), 1.1, 0.55, 1.5, 'console de surveillance à trois écrans (généré, angle corrigé)'),
  ('io_locker',      ('genfix', 'gen_douane_furn.jpg', 3, {}), 1.4, 0.85, 2.0, 'armoire forte à armes (généré, angle corrigé)'),
]
# acceptés par l'angle mais non retenus pour le canon ou le rendu
NOT_EXPORTED = {'bar_backshelf': 'pan de mur en ruine peint avec l étagère : double le vrai mur, remplacé par bar_backshelf_b'}
def run():
    man, rep = {}, {}
    for aid, (kind, f, *rest), w, d, h, role in ASSETS:
        i = rest[0]; f = (f, rest[0], rest[1]) if kind.endswith('fix') else f
        fix = None
        if kind in ('genfix', 'mockfix'):
            f, i, o = f[0], f[1], f[2]; rgba, fix = v4fix(quad(GEN + f, i) if kind == 'genfix' else mock(f, i), **o)
        else: rgba = quad(GEN + f, i) if kind == 'gen' else mock(f, i)
        j = judge(rgba); hh = rgba.shape[0] / rgba.shape[1]
        if fix: j['correction_v4'] = fix; j['sens'] = 'direct'  # orientation déjà fixée par v4fix
        # v13 : après correction mesurée (pas forcée), l'arête basse doit tomber sur les deux pentes v4 (0,33 et 0,70, à 0,06 près)
        if fix and not rest[1].get('force') and abs(fix['pentes_apres'][0] - 0.33) <= 0.06 and abs(fix['pentes_apres'][1] - 0.70) <= 0.06: j['accepte'] = True; j['regle'] = 'arête basse v4'
        # échelle : largeur écran de l'emprise (m) -> hauteur implicite de l'objet
        sw = w*abs(R[0]) + d*abs(R[2]); sh = sw*hh; implied = (sh - w*abs(U[0]) - d*abs(U[2])) / U[1]
        j.update({'source': ('maquette art-source/' if kind.startswith('mock') else 'généré art-gen/') + f + f' #{i}', 'role': role,
                  'emprise_m': [w, d], 'hauteur_attendue_m': h, 'hauteur_implicite_m': round(implied, 2)})
        j['echelle_ok'] = bool(abs(implied - h) <= 0.3*h + 0.15)
        rep[aid] = j
        if aid in NOT_EXPORTED: j['non_exporte'] = NOT_EXPORTED[aid]
        if j['accepte'] and j['echelle_ok'] and aid not in NOT_EXPORTED:
            if j['sens'] == 'miroir': rgba = rgba[:, ::-1]
            im = Image.fromarray(rgba, 'RGBA'); im.thumbnail((640, 640)); im.save(OUT + aid + '.webp', quality=90)
            man[aid] = {'file': f'interiors/{aid}.webp', 'px': list(im.size), 'footprint_m': [w, d], 'height_m': h, 'origin': 'maquette' if kind.startswith('mock') else 'généré',
                        'source': j['source'], 'mirrored_from_source': j['sens'] == 'miroir'}
        print(f"{aid:18s} {'ACCEPTE' if aid in man else 'REJETE '} pente={j['pente_dominante']} ({j['sens']}, bande {j['part_bande_v4']}, 2:1 opp {j['part_2_1_opposee']}) h impl={j['hauteur_implicite_m']} / {h}")
    # textures (plans en mètres : l'angle est donné par la géométrie 3D, pas par l'image)
    def tile(f, q, name, size=512):
        im = Image.open(GEN + f).convert('RGB'); W, H = im.size; c, r = q % 2, q // 2; m = 6
        im.crop((c*W//2+m, r*H//2+m, (c+1)*W//2-m, (r+1)*H//2-m)).resize((size, size)).save(OUT + name + '.webp', quality=88)
        man[name] = {'file': f'interiors/{name}.webp', 'texture': True, 'origin': 'généré', 'source': 'généré art-gen/' + f + f' #{q}'}
    tile('gen_walls_sheet.jpg', 0, 'w_plaster'); tile('gen_walls_sheet.jpg', 1, 'w_brick'); tile('gen_walls_sheet.jpg', 2, 'w_clay'); tile('gen_walls_sheet.jpg', 3, 'w_planks')
    tile('gen_io_surfaces.jpg', 0, 'w_io_dark'); tile('gen_io_surfaces.jpg', 1, 'w_io_white'); tile('gen_io_surfaces.jpg', 2, 'f_io_grate'); tile('gen_io_surfaces.jpg', 3, 'f_io_dark')  # v13 Steel
    tile('gen_floors_sheet.jpg', 0, 'f_tiles'); tile('gen_floors_sheet.jpg', 2, 'f_earth')
    Image.open(SRC + 'interior-wood-v10.png').convert('RGB').resize((512, 512)).save(OUT + 'f_wood.webp', quality=88)
    man['f_wood'] = {'file': 'interiors/f_wood.webp', 'texture': True, 'origin': 'maquette', 'source': 'maquette art-source/interior-wood-v10.png'}
    t = Image.open(SRC + 'terrain-nature-v4.png').convert('RGB'); tw = t.size[0] // 3
    t.crop((tw, tw, 2*tw, 2*tw)).resize((512, 512)).save(OUT + 'f_concrete.webp', quality=88)
    man['f_concrete'] = {'file': 'interiors/f_concrete.webp', 'texture': True, 'origin': 'maquette', 'source': 'maquette art-source/terrain-nature-v4.png (tuile béton)'}
    d = Image.open(GEN + 'gen_door_in.jpg').convert('RGB'); W, H = d.size; d.crop((6, 6, W-6, H-6)).resize((256, 563)).save(OUT + 'door_in.webp', quality=90)
    man['door_in'] = {'file': 'interiors/door_in.webp', 'texture': True, 'origin': 'généré', 'source': 'généré art-gen/gen_door_in.jpg'}
    d = Image.open(GEN + 'gen_io_door.jpg').convert('RGB'); W, H = d.size; d.crop((6, 6, W-6, H-6)).resize((256, 563)).save(OUT + 'door_io.webp', quality=90)  # v13 Steel
    man['door_io'] = {'file': 'interiors/door_io.webp', 'texture': True, 'origin': 'généré', 'source': 'généré art-gen/gen_io_door.jpg'}
    json.dump(man, open(OUT + 'manifest.json', 'w'), ensure_ascii=False, indent=1)
    json.dump(rep, open(OUT + 'rapport_angles.json', 'w'), ensure_ascii=False, indent=1)
if __name__ == '__main__': run()
