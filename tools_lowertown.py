# Lower-Town (branche creation/lower-town-sprites) : sprites de bâtiments générés sur fond vert uni.
# Détourage + despill vert (tools_finitions.key_green_obj), correction d'angle caméra v4 (tools_interiors.v4fix),
# contrôle d'angle et d'échelle (tools_interiors.judge + hauteur implicite), mise à l'échelle K=50 px/m comme tools_steel (GENFIX).
# Écrit assets/buildings/<id>.webp, entrées assets/buildings/manifest.json, assets/buildings/rapport_angles_lowertown.json. N'écrit jamais dans src/.
import json, os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tools_interiors as TI, tools_finitions as TF
K, cy, sy = TF.K, TF.cy, TF.sy
G, A = HERE + '/art-gen/', HERE + '/assets/buildings/'
# id: (source, emprise indicative [x, z] m (seule la plus grande dimension compte, cf. build), hauteur m, rôle)
LT = {
 'lt_portique_io': ('gen_lt_portique_io_p2.jpg', [7.0, 2.0], 7.0, 'portique de contrôle IO sur la rampe de La Descente, scanner, voyants ambre, guérite vide'),
 'lt_atelier_usine': ('gen_lt_atelier_usine.jpg', [14.0, 10.0], 9.0, 'atelier-usine à toit en sheds (Usine 7 / Atelier Bastide), porte coulissante entrouverte, lueur de four, cheminée'),
 'lt_immeuble_ouvrier': ('gen_lt_immeuble_ouvrier_p2.jpg', [8.0, 6.0], 13.0, 'immeuble ouvrier, 4 niveaux, coursives extérieures, linge, rez-de-chaussée à rideau'),
 'lt_foyer_ruiz': ('gen_lt_foyer_ruiz.jpg', [10.0, 7.0], 5.5, 'Foyer Ruiz, ancienne cantine d usine, porte basse, vitre embuée, soupirail à barreaux au ras de la rue'),
}
# lot props (2026-10-22) : bâtiments/props de PLAN_IMPLEMENTATION.md §1. 'MAQ:fichier:x0,y0,x1,y1' = sprite repris de la maquette
# (reference/maquette/.../art-source/, fond transparent), recadré, étalonné nuit Lower-Town, puis même correction/contrôle.
MAQ = 'reference/maquette/No-Mans-Land_Reconstruction/07_MAQUETTE_ARCHIVE_v0.13/art-source/'
LT.update({
 'lt_atelier_petit': ('gen_lt_atelier_petit.jpg', [8.0, 6.0], 5.0, 'Atelier Bastide, petit atelier de ferrailleur, rideau ouvert, établi éclairé'),
 'lt_comptoir_moss': ('gen_lt_comptoir_moss.jpg', [6.0, 5.0], 7.0, 'Chez Moss, comptoir sans enseigne au rez d un immeuble, guichet éclairé ambre'),
 'lt_tuyau': ('MAQ:linear-v12.png:512,512,1024,1024', [3.0, 0.8], 1.3, 'tuyau suspendu droit, brides boulonnées, sur pieds'),
 'lt_tuyau_coude': ('gen_lt_tuyau_coude.jpg', [2.5, 2.5], 1.3, 'tuyau, coude à 90° (variante de lt_tuyau)'),
 'lt_sodium': ('MAQ:street-detail-v9.png:692,486,917,980', [0.8, 0.8], 4.5, 'poteau d éclairage à lanterne chaude (lampe sodium)'),
 'lt_horloge_pointage': ('gen_lt_horloge_pointage.jpg', [1.2, 0.8], 2.0, 'horloge de pointage de l Usine 7, casier à cartes'),
 'lt_voiture_panne': ('MAQ:props-v2.png:930,540,1525,940', [4.2, 1.8], 1.5, 'voiture en panne, roue manquante, vitres cassées'),
 'lt_bidons': ('MAQ:props-v2.png:1198,87,1413,453', [0.6, 0.6], 0.9, 'bidon (fût de 200 L) rouillé'),
 'lt_ferraille': ('gen_lt_ferraille.jpg', [1.5, 1.2], 1.0, 'caisse de ferraille'),
 'lt_palettes': ('gen_lt_palettes.jpg', [1.2, 1.0], 0.6, 'pile de palettes'),
 'lt_grille_fosse': ('gen_lt_grille_fosse.jpg', [2.0, 2.0], 1.2, 'grille cadenassée de l Escalier de la Fosse (vers la Sous-Ville)'),
 'lt_flaque': ('gen_lt_flaque.jpg', [2.5, 1.5], 0.0, 'flaque huileuse (décalque au sol)'),
 'lt_passerelle': ('gen_lt_passerelle2.jpg', [1.5, 6.0], 3.8, 'passerelle haute sur poteaux (tablier en tôle striée, garde-corps en tubes), escalier'),
})
HULL = {'lt_tuyau', 'lt_tuyau_coude', 'lt_voiture_panne', 'lt_passerelle'}  # objets à pieds/roues : arête basse mesurée sur l enveloppe convexe (comme sv_cardtable_b)
GRADE = {'lt_tuyau': 0.55, 'lt_tuyau_coude': 0.40}  # coude : 0,40 pour égaler la luminance moyenne du tuyau droit (~37)  # métal trop clair pour la nuit de Lower-Town : assombri vers le gris acier
# correctifs 2026-10-22 : pentes source mesurées (Hough) sur les axes de l objet quand l arête basse n est pas mesurable
# (coude : bras en V renversé, apex à l arrière ; passerelle : escalier et poteaux). (pente axe x, pente axe z), sans miroir.
FORCE = {'lt_tuyau_coude': (0.60, 0.62), 'lt_passerelle': (0.95, 0.58)}
FP = {'lt_passerelle': [1.5, 6.0], 'lt_tuyau_coude': [2.5, 2.5]}  # emprise imposée (le masque, escalier compris, ne donne pas la largeur du tablier)
STRICT = {'lt_passerelle'}  # grillage : le vert du fond traverse les mailles -> détourage plus strict + despill complet
def key_green_strict(path):
    a = np.asarray(Image.open(path).convert('RGB')).astype(float); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    ex = g - np.maximum(r, b); al = np.clip((45 - ex) / 25, 0, 1)
    a[..., 1] = np.minimum(g, np.maximum(r, b))  # despill complet : aucun vert voulu
    from scipy import ndimage
    al = ndimage.binary_opening(al > 0.5, iterations=1) * al
    return TI.clean(np.dstack([np.clip(a, 0, 255), al * 255]).astype('uint8'), 4000)
# passerelle : la génération est trop longue pour sa hauteur (tablier ~0,9 m implicite pour 6 m). Le tablier est une extrusion
# le long de l axe z (pente écran 0,70) : on retire un tronçon entre deux fractions de la largeur (poteau central compris) et on recolle
# la partie arrière décalée le long de z (comme la bande retirée des pieds de sv_cardtable_b).
ZCUT = {'lt_passerelle': (0.30, 0.86)}
def zcut(rgba, f0, f1, tz=0.70):
    H, W = rgba.shape[:2]; x1, x2 = int(W * f0), int(W * f1); L = x2 - x1; dy = int(round(tz * L))
    out = np.zeros((H, W - L, 4), np.uint8); out[:, :x1] = rgba[:, :x1]
    right = np.zeros((H, W - x2, 4), np.uint8); right[dy:] = rgba[:H - dy, x2:]
    m = right[..., 3] > 0; seg = out[:, x1:]; seg[m] = right[m]
    return TI.clean(out, 200)
NOFIX = {'lt_sodium', 'lt_bidons', 'lt_flaque'}  # objets de révolution / décalque : pas de cisaillement (l arête basse n est pas une arête)
def load_maq(spec):
    _, f, bb = spec.split(':'); x0, y0, x1, y1 = map(int, bb.split(','))
    rgba = np.asarray(Image.open(HERE + '/' + MAQ + f).convert('RGBA'))[y0:y1, x0:x1].copy()
    # étalonnage nuit Lower-Town : désaturation partielle, assombrissement, dominante chaude (sprites de maquette éclairés plein jour)
    p = rgba[..., :3].astype(float); g = p.mean(2, keepdims=True); p = (0.55 * p + 0.45 * g) * 0.62 * np.array([1.06, 0.97, 0.86])
    rgba[..., :3] = np.clip(p, 0, 255).astype('uint8')
    return TI.clean(rgba, 400)
# passe 2 : redressement de perspective. Le générateur dessine les arêtes hautes plus plates que l'arête basse (fuyantes) ;
# v4fix (cisaillement affine) ne corrige que la base. keystone() écarte verticalement les points selon |x - coin avant|,
# d'un coefficient nul à la base et égal à k au sommet (k choisi par balayage 0..0,3 : plus petit k où judge accepte avec pente ~0,30).
import cv2
def keystone(rgba, k):
    a = rgba[...,3]>100; ys,xs=np.nonzero(a); ay=ys.max(); ax=int(np.median(xs[ys>=ay-3])); yt=ys.min()
    H,W=a.shape; pad=int(k*W)+2
    X,Yo=np.meshgrid(np.arange(W),np.arange(-pad,H)); Y=Yo.astype(float); dist=np.abs(X-ax)
    for _ in range(6):
        t=np.clip((ay-Y)/(ay-yt),0,1); Y=Yo + k*t*dist
    out=cv2.remap(rgba,X.astype(np.float32),Y.astype(np.float32),cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT,borderValue=0)
    return TI.clean(out,200)
KS = {'lt_portique_io': 0.10, 'lt_immeuble_ouvrier': 0.10}
def build(aid):
    src, (w, d), h, role = LT[aid]
    maq = src.startswith('MAQ:')
    rgba = load_maq(src) if maq else key_green_strict(G + src) if aid in STRICT else TF.key_green_obj(G + src)
    if aid in GRADE: rgba = rgba.copy(); rgba[..., :3] = np.clip(rgba[..., :3].astype(float) * GRADE[aid] * np.array([1.0, 0.98, 0.95]), 0, 255).astype('uint8')
    # despill vert ciblé (passe 2) : seulement la bande de bord (4 px) et les pixels nettement verts. Le despill global de la passe 1
    # modifiait ~90 % des pixels (gris neutres légèrement verts assombris), créait de faux contours (tôle ondulée) et faisait basculer judge.
    from scipy import ndimage
    p = rgba[..., :3].astype(float); op = rgba[..., 3] > 0; ex = p[..., 1] - np.maximum(p[..., 0], p[..., 2])
    m = (op & ~ndimage.binary_erosion(op, iterations=4)) | (ex > 8)
    p[..., 1] = np.where(m, np.minimum(p[..., 1], np.maximum(p[..., 0], p[..., 2]) * 1.05 + 2), p[..., 1]); rgba = rgba.copy(); rgba[..., :3] = p.astype('uint8')
    if aid in NOFIX: fix = {'v4fix': 'non applicable (' + ('révolution' if aid != 'lt_flaque' else 'décalque') + ')', 'pentes_apres': [None, None]}
    elif aid in FORCE:
        rgba, fix = TI.v4fix(rgba, force=FORCE[aid], mirror=False); fix['mesure'] = 'pentes forcées (axes mesurés par Hough sur la source)'
        fix['pentes_apres'] = [round(v, 2) for v in TI.base_slopes(rgba)[:2]]
    elif aid in HULL:
        ys, xs = np.nonzero(rgba[..., 3] > 100); hull = cv2.convexHull(np.stack([xs, ys], 1).astype(np.int32))
        hm = np.zeros(rgba.shape[:2], np.uint8); cv2.fillPoly(hm, [hull.reshape(-1, 2)], 1); hrgba = np.dstack([rgba[..., :3], hm * 255]).astype('uint8')
        sl, sr, _, _ = TI.base_slopes(hrgba); mir = sr < sl
        rgba, fix = TI.v4fix(rgba, force=(sl, sr), mirror=mir); h2, _ = TI.v4fix(hrgba, force=(sl, sr), mirror=mir)
        fix['pentes_apres'] = [round(v, 2) for v in TI.base_slopes(h2)[:2]]; fix['mesure'] = 'enveloppe convexe'
    else: rgba, fix = TI.v4fix(rgba)
    if aid in ZCUT: rgba = zcut(rgba, *ZCUT[aid]); fix['coupe_z'] = list(ZCUT[aid])
    if KS.get(aid): rgba = keystone(rgba, KS[aid]); fix['keystone_k'] = KS[aid]; fix['pentes_apres'] = [round(v, 2) for v in TI.base_slopes(rgba)[:2]]
    elif aid not in KS and aid not in NOFIX and not TI.judge(rgba)['accepte']:
        # lot props : balayage automatique du redressement (k > 0 si arêtes hautes trop plates, k < 0 si trop raides), plus petit |k| accepté
        for k in (0.05, -0.05, 0.1, -0.1, 0.15, -0.15, 0.2, -0.2, 0.25, 0.3):
            o = keystone(rgba, k)
            if TI.judge(o)['accepte']: rgba = o; fix['keystone_k'] = k; break
    # emprise : proportions x/z mesurées sur l'arête basse corrigée (coin avant = point le plus bas), échelle fixée par la plus grande dimension
    m = rgba[..., 3] > 100; ys, xs = np.nonzero(m); by = ys.max(); bx = int(np.median(xs[ys >= by - 3]))
    if aid in FP: w, d = FP[aid]
    elif aid not in NOFIX:
        lw, ld = (bx - xs.min()) / cy, (xs.max() - bx) / sy; s = max(w, d) / max(lw, ld)
        w, d = max(0.5, round(lw * s * 2) / 2), max(0.5, round(ld * s * 2) / 2)
    j = TI.judge(rgba); j['correction_v4'] = fix
    pa = fix['pentes_apres']
    if pa[0] is None: j['accepte_arete_basse'] = None
    elif abs(pa[0] - 0.33) <= 0.06 and abs(pa[1] - 0.70) <= 0.08: j['accepte_arete_basse'] = True
    else: j['accepte_arete_basse'] = False
    R, U = TI.R, TI.U; hh = rgba.shape[0] / rgba.shape[1]; sw = w * abs(R[0]) + d * abs(R[2])
    implied = (sw * hh - w * abs(U[0]) - d * abs(U[2])) / U[1]
    j.update({'source': (MAQ + src.split(':')[1] + ' ' + src.split(':')[2]) if maq else 'art-gen/' + src, 'origine': 'maquette' if maq else 'généré', 'role': role, 'emprise_m': [w, d], 'hauteur_attendue_m': h, 'hauteur_implicite_m': round(implied, 2),
              'echelle_ok': bool(abs(implied - h) <= 0.3 * h + 0.15)})
    sc = K * (w * cy + d * sy) / rgba.shape[1]
    im = Image.fromarray(rgba, 'RGBA').resize((round(rgba.shape[1] * sc), round(rgba.shape[0] * sc)), Image.LANCZOS)
    a = np.asarray(im)[..., 3] > 100; ys, xs = np.nonzero(a); ay = ys.max(); ax = int(np.median(xs[ys >= ay - 3]))
    j['magenta_bord_pct'] = TF.mag_edge_pct(np.asarray(im))[0]
    im.save(A + aid + '.webp', quality=90)
    man = json.load(open(A + 'manifest.json'))
    man[aid] = {'file': 'buildings/' + aid + '.webp', 'source': (MAQ + src.split(':')[1] + ' ' + src.split(':')[2]) if maq else 'art-gen/' + src, 'origine': 'maquette' if maq else 'généré', 'px': list(im.size), 'anchor': [ax, int(ay)],
                'footprint_m': [w, d], 'height_m': h, 'lot': 'lower-town v1 (creation/lower-town-sprites)',
                'anchor_note': 'coin avant bas (pivot), emprises provisoires à réconcilier avec Rivet'}
    json.dump(man, open(A + 'manifest.json', 'w'), ensure_ascii=False, indent=1)
    rp = A + 'rapport_angles_lowertown.json'; rep = json.load(open(rp)) if os.path.exists(rp) else {}
    rep[aid] = j; json.dump(rep, open(rp, 'w'), ensure_ascii=False, indent=1)
    print(aid, json.dumps(j, ensure_ascii=False), man[aid]['px'], man[aid]['anchor'])
if __name__ == '__main__':
    for aid in (sys.argv[1:] or LT): build(aid)

# ---- lt_dalle_center (2026-10-22) : sous-face de la dalle de Center-Town au-dessus des toits, bord nord de steel_lower ----
# Entrée LOWER_TOWN_POSITIONS.md : x 0, z 0, emprise 48 × 2,5 m, pivot (48, 2,5), pylônes x = 2 + 10,5 i (i = 0..4), z 0,6, 1,4 × 1,4 m,
# dalle à 15 m (src/data/lower_town.js : kind 'dalle', h 15). Un module généré (une travée, un pylône) est détouré, cisaillé pour que
# les arêtes de la dalle suivent l'axe x de la caméra v4 (pente 0,331), mis à l'échelle (pylône = 15 m), puis répété 5 fois le long de x
# (translation monde de 10,5 m = vecteur écran exact), avec fondu de 24 px aux raccords ; extrémités coupées à x = 0 et x = 48.
DALLE = dict(src='gen_lt_dalle_module.jpg', L=48.0, D=2.5, H=15.0, pitch=10.5, x0=2.7, zp=1.3, n=5)
def scr(x, y, z):
    p = np.array([x, y, z]); return K * float(TI.R @ p), -K * float(TI.U @ p)
def build_dalle():
    c = DALLE; rgba = TF.key_green_obj(G + c['src']).copy()
    p = rgba[..., :3].astype(float); ex = p[..., 1] - np.maximum(p[..., 0], p[..., 2]); p[..., 1] = np.where(ex > 2, np.maximum(p[..., 0], p[..., 2]), p[..., 1]); rgba[..., :3] = p.astype('uint8')  # despill (tuyaux de descente)
    a = rgba[..., 3] > 100; W0 = rgba.shape[1]
    cols = np.arange(W0); top = np.array([np.nonzero(a[:, x])[0].min() if a[:, x].any() else -1 for x in cols])
    s0 = float(np.polyfit(cols[50:-50], top[50:-50], 1)[0]); tx = -float(TI.U[0] / TI.R[0])  # pente écran de l'axe x
    # pylône : colonne de masse maximale sous la dalle ; base = dernière ligne opaque
    ys, xs = np.nonzero(a); yb = ys.max(); low = a[int(yb * 0.75):]; pc = int(np.median(np.nonzero(low)[1]))
    # cisaillement vertical autour de la colonne du pylône (les verticales restent verticales)
    k = tx - s0; Hn = rgba.shape[0] + int(abs(k) * W0) + 4; off = int(max(0, -k * (W0 - pc), k * pc)) + 2
    X, Y = np.meshgrid(np.arange(W0), np.arange(Hn)); src_y = (Y - off - k * (X - pc)).astype(np.float32)
    sh = cv2.remap(rgba, X.astype(np.float32), src_y, cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    a2 = sh[..., 3] > 100; colp = a2[:, pc]; ybase = np.nonzero(colp)[0].max()
    # bas de la dalle au droit du pylône : premier trou vertical de transparence en remontant ? -> on prend la sous-face = ligne où la largeur opaque chute
    widths = a2.sum(1); rows = np.arange(len(widths)); band_rows = rows[widths > 0.6 * W0]; yslab = band_rows.max()
    sc = (c['H'] * K * TI.U[1]) / (ybase - yslab)   # sous-face à 15 m
    per = c['pitch'] * K * TI.R[0] / sc               # période en px source
    x1, x2 = int(pc - per / 2) - 12, int(pc + per / 2) + 12
    mod = sh[:, max(0, x1):min(W0, x2)]
    if x1 < 0 or x2 > W0: print('  module trop étroit, période', per, 'largeur', W0)
    mod = np.asarray(Image.fromarray(mod).resize((round(mod.shape[1] * sc), round(mod.shape[0] * sc)), Image.LANCZOS)).astype(float)
    mw, mh = mod.shape[1], mod.shape[0]; pcs = (pc - max(0, x1)) * sc; ybs = ybase * sc
    ramp = np.ones(mw); f = int(24 * sc / sc); ramp[:f] = np.linspace(0, 1, f); ramp[-f:] = np.linspace(1, 0, f)
    # canevas : coordonnées écran du monde, origine au coin (0, 0, 0)
    corners = [scr(x, y, z) for x in (0, c['L']) for z in (0, c['D']) for y in (0, c['H'] + 3)]
    minx = min(p[0] for p in corners) - mw; miny = min(p[1] for p in corners) - mh
    Wc = int(max(p[0] for p in corners) - minx + mw); Hc = int(max(p[1] for p in corners) - miny + mh)
    acc = np.zeros((Hc, Wc, 3)); wsum = np.zeros((Hc, Wc)); alpha = np.zeros((Hc, Wc))
    for i in range(c['n']):
        bx, by = scr(c['x0'] + i * c['pitch'], 0, c['zp']); ox, oy = int(round(bx - minx - pcs)), int(round(by - miny - ybs))
        w = (mod[..., 3] / 255) * ramp[None, :]
        acc[oy:oy + mh, ox:ox + mw] += mod[..., :3] * w[..., None]; wsum[oy:oy + mh, ox:ox + mw] += w
        alpha[oy:oy + mh, ox:ox + mw] = np.maximum(alpha[oy:oy + mh, ox:ox + mw], mod[..., 3] / 255 * np.minimum(1, ramp[None, :] * 2.5))
    rgb = acc / np.maximum(wsum, 1e-6)[..., None]
    # extrémités : coupe verticale écran aux bornes x = 0 et x = 48 (bord de zone)
    xl = scr(0, 0, c['D'])[0] - minx  # coupe ouest prise au bord sud : le premier pylône (z 0,6-2) reste entier
    xr = scr(c['L'], 0, 0)[0] - minx; colsC = np.arange(Wc); alpha[:, (colsC < xl) | (colsC > xr)] = 0
    out = np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype('uint8')
    ys, xs = np.nonzero(out[..., 3] > 20); y0, y1, x0, x1c = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    axw, ayw = scr(c['L'], 0, c['D']); y1 = max(y1, int(round(ayw - miny)) + 2); x1c = max(x1c, int(round(axw - minx)) + 2)  # pivot au sol inclus dans le sprite
    out = out[y0:y1, x0:x1c]; anchor = [int(round(axw - minx - x0)), int(round(ayw - miny - y0))]
    j = TI.judge(out); j.update({'source': 'art-gen/' + c['src'] + ' (module ×5)', 'origine': 'généré', 'role': 'sous-face de la dalle de Center-Town, 5 pylônes',
        'emprise_m': [c['L'], c['D']], 'hauteur_attendue_m': c['H'], 'correction_v4': {'pente_source': round(s0, 3), 'cisaillement': round(k, 3), 'pente_cible': round(tx, 3),
        'echelle': round(sc, 3), 'periode_px': round(c['pitch'] * K * TI.R[0], 1), 'pentes_apres': [round(float(np.polyfit(*[(lambda m: (np.nonzero(m.any(0))[0], np.array([np.nonzero(m[:, x])[0].min() for x in np.nonzero(m.any(0))[0]])))(out[..., 3] > 100)][0], 1)[0]), 3), None]}})
    j['magenta_bord_pct'] = TF.mag_edge_pct(out)[0]
    Image.fromarray(out, 'RGBA').save(A + 'lt_dalle_center.webp', quality=88)
    man = json.load(open(A + 'manifest.json'))
    man['lt_dalle_center'] = {'file': 'buildings/lt_dalle_center.webp', 'source': j['source'], 'origine': 'généré', 'px': [int(out.shape[1]), int(out.shape[0])],
        'anchor': anchor, 'footprint_m': [c['L'], c['D']], 'height_m': c['H'], 'lot': 'lower-town v1 (creation/lower-town-sprites)',
        'anchor_note': 'pivot (48, 2,5) au sol ; pylônes au sol en x = 2 + 10,5 i, z 0,6 (LOWER_TOWN_POSITIONS.md)'}
    json.dump(man, open(A + 'manifest.json', 'w'), ensure_ascii=False, indent=1)
    rp = A + 'rapport_angles_lowertown.json'; rep = json.load(open(rp)); rep['lt_dalle_center'] = j; json.dump(rep, open(rp, 'w'), ensure_ascii=False, indent=1)
    print('lt_dalle_center', json.dumps(j, ensure_ascii=False), man['lt_dalle_center']['px'], anchor)

# ---- réconciliation avec LOWER_TOWN_POSITIONS.md (main e92b1c8, Rivet) ----
# view.js pose le sprite par anchor/px et px/K : la largeur doit valoir K (w cos34,5 + d sin34,5) (vérifié : écart ≤ 1 %) et le pivot x
# tomber sur le coin avant de l'emprise, à K w cos34,5 du bord gauche. Le pivot x mesuré (point opaque le plus bas) s'en écartait
# pour les objets dont le point bas n'est pas le coin avant (coude, passerelle, poteau, fût). Hauteurs alignées sur lower_town.js.
POS = {'lt_atelier_usine': (7, 14, 9), 'lt_atelier_petit': (8, 6, 4.5), 'lt_immeuble_ouvrier': (8, 6.5, 13), 'lt_comptoir_moss': (6, 5, 7),
       'lt_foyer_ruiz': (10, 7, 5.5), 'lt_portique_io': (7, 2.5, 7), 'lt_tuyau': (3, 2, None), 'lt_tuyau_coude': (2.5, 2.5, None),
       'lt_sodium': (0.8, 0.8, None), 'lt_horloge_pointage': (1, 1, None), 'lt_voiture_panne': (4, 2, None), 'lt_bidons': (0.6, 0.6, None),
       'lt_ferraille': (1.5, 1, None), 'lt_palettes': (1, 1, None), 'lt_grille_fosse': (2, 2, None), 'lt_flaque': (2.5, 1.5, None),
       'lt_passerelle': (1.5, 6, None), 'lt_dalle_center': (48, 2.5, 15)}
def reconcile():
    man = json.load(open(A + 'manifest.json')); rows = []
    for k, (w, d, h) in POS.items():
        e = man[k]; old = dict(fp=list(e['footprint_m']), anchor=list(e['anchor']), h=e.get('height_m'))
        exp_w = K * (w * TI.R[0] - d * TI.R[2]); e['footprint_m'] = [float(w), float(d)]
        if k != 'lt_dalle_center': e['anchor'] = [int(round(K * w * TI.R[0])), e['anchor'][1]]
        if h is not None: e['height_m'] = float(h)
        e['anchor_note'] = 'pivot = coin avant bas de l emprise (x+w, z+d), réconcilié avec LOWER_TOWN_POSITIONS.md (main e92b1c8)'
        rows.append((k, old, dict(fp=e['footprint_m'], anchor=e['anchor'], h=e.get('height_m')), e['px'], round(e['px'][0] / exp_w, 3)))
    json.dump(man, open(A + 'manifest.json', 'w'), ensure_ascii=False, indent=1)
    for r in rows: print(*r)
    return rows
