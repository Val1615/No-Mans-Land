# China Lake (branche creation/china-lake-sprites, dérivé de tools_asiaground.py) : sprites de bâtiments générés sur fond vert uni.
# Détourage + despill vert (tools_finitions.key_green_obj), correction d'angle caméra v4 (tools_interiors.v4fix),
# contrôle d'angle et d'échelle (tools_interiors.judge + hauteur implicite), mise à l'échelle K=50 px/m comme tools_steel (GENFIX).
# Écrit assets/buildings/<id>.webp, entrées assets/buildings/manifest.json, assets/buildings/rapport_angles_chinalake.json. N'écrit jamais dans src/.
import json, os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import tools_interiors as TI, tools_finitions as TF
K, cy, sy = TF.K, TF.cy, TF.sy
G, A = HERE + '/art-gen/', HERE + '/assets/buildings/'
# id: (source, emprise indicative [x, z] m (seule la plus grande dimension compte, cf. build), hauteur m, rôle)
MAQ = 'reference/maquette/No-Mans-Land_Reconstruction/07_MAQUETTE_ARCHIVE_v0.13/art-source/'
# China Lake (PLAN_IMPLEMENTATION.md §3, CHINA_LAKE.md §7, planches quartier_china_lake_* 19c137c/6610e92) : 5 bâtiments (+1 façade), stand illégal
# en 5 variantes lisibles par marchandise (une rive par type), 13 props (ballon ×4, déchets ×3), préfixe cl_. Sol g_cl_eau : voir build_eau().
LT = {
 'cl_maison_the': ('gen_cl_maison_the.jpg', [10.0, 8.0], 8.5, 'maison de thé de la mafia, seul toit recourbé (un seul pan, sans étages de pagode), porte gardée, MAISON DE THÉ 茶馆'),
 'cl_immeuble_fond': ('gen_cl_immeuble_fond.jpg', [8.0, 6.0], 9.0, 'immeuble de fond 3 niveaux sur pilotis, toit plat, Pavillon du Dragon PAVILLON DU DRAGON 龙阁'),
 'cl_immeuble_fond_b': ('gen_cl_immeuble_fond_b2.jpg', [6.0, 8.0], 8.0, 'variante façade muette LOGEMENTS 住房, toit plat, linge'),
 'cl_pilotis': ('gen_cl_pilotis.jpg', [6.0, 6.0], 4.5, 'module de structure sur pilotis 6 m (plateforme, garde-corps, caisses, filets pliés, lanterne)'),
 'cl_cabane': ('gen_cl_cabane2.jpg', [8.0, 6.0], 3.5, 'Les Filets, cabane sur pilotis, toit simple, FILETS 渔网'),
 'cl_ponton': ('gen_cl_ponton.jpg', [5.0, 3.0], 3.5, 'Ponton de Shen, stand du technicien au bord de l eau, ordinateurs, pièces, RÉPARATIONS 修理'),
 'cl_stand_implants': ('gen_cl_stand_implants2.jpg', [2.5, 1.5], 2.6, 'stand illégal, quai nord : implants piratés, IMPLANTS 植入物'),
 'cl_stand_puces': ('gen_cl_stand_puces2.jpg', [2.5, 1.5], 2.6, 'stand illégal, quai nord : puces, PUCES 芯片'),
 'cl_stand_armes': ('gen_cl_stand_armes3.jpg', [2.5, 1.5], 2.6, 'stand illégal, quai est : armes, ARMES 武器'),
 'cl_stand_papiers': ('gen_cl_stand_papiers2.jpg', [2.5, 1.5], 2.4, 'stand illégal (guichet), quai sud : faux papiers, PAPIERS 证件'),
 'cl_stand_medocs': ('gen_cl_stand_medocs2.jpg', [2.5, 1.5], 2.6, 'stand illégal, quai ouest : médicaments, MÉDICAMENTS 药品'),
 'cl_cable_lanternes': ('gen_cl_cable_lanternes.jpg', [14.0, 0.5], 5.0, 'câble à 9 lanternes rouges au-dessus du lac (portée 14 m)'),
 'cl_ballon_dragon': ('gen_cl_sheet_ballons_0.jpg', [3.0, 1.5], 3.0, 'ballon de papier dragon, éclairé de l intérieur (flottant)'),
 'cl_ballon_carpe': ('gen_cl_sheet_ballons_1.jpg', [3.0, 1.0], 3.0, 'ballon de papier carpe (flottant)'),
 'cl_ballon_tigre': ('gen_cl_sheet_ballons_2.jpg', [3.0, 1.2], 3.0, 'ballon de papier tigre (flottant)'),
 'cl_ballon_phenix': ('gen_cl_sheet_ballons_3.jpg', [3.0, 1.5], 3.0, 'ballon de papier phénix (flottant)'),
 'cl_bache': ('gen_cl_sheet_props_a_0.jpg', [3.0, 3.0], 2.4, 'bâche sur quatre perches'),
 'cl_treteaux': ('gen_cl_sheet_props_a_1.jpg', [2.0, 0.6], 0.8, 'tréteaux et plateau'),
 'cl_caisse_armes': ('gen_cl_sheet_props_a_2.jpg', [1.2, 0.6], 0.6, 'caisse d armes ouverte'),
 'cl_bac_puces': ('gen_cl_sheet_props_a_3.jpg', [0.6, 0.4], 0.4, 'bac de puces et câbles'),
 'cl_presse_papiers': ('gen_cl_sheet_props_b_0.jpg', [1.0, 0.6], 1.2, 'presse à faux papiers sur banc'),
 'cl_bocaux': ('gen_cl_sheet_props_b_1.jpg', [0.8, 0.4], 0.8, 'étagère de bocaux de médicaments'),
 'cl_friture': ('gen_cl_sheet_props_b_2.jpg', [1.0, 0.7], 1.1, 'bassine à friture sur chariot'),
 'cl_mahjong': ('gen_cl_sheet_props_b_3.jpg', [1.6, 1.6], 1.0, 'table de mah-jong et quatre chaises'),
 'cl_barriere_caisses': ('gen_cl_sheet_props_c_0.jpg', [4.0, 0.8], 2.0, 'barrière de caisses du barrage, lanterne'),
 'cl_pieux': ('gen_cl_sheet_props_c_1.jpg', [0.8, 0.8], 2.0, 'faisceau de pieux d amarrage, corde, chaîne'),
 'cl_pieux_b': ('MAQ:utility-v9.png:588,512,977,961', [0.8, 0.8], 0.9, 'bitte d amarrage à corde (maquette utility-v9), variante de cl_pieux'),
 'cl_dechets_a': ('gen_cl_sheet_dechets_0.jpg', [2.0, 2.0], 0.2, 'déchets flottants : bouteilles, bidon, mousse (décalque sur l eau)'),
 'cl_dechets_b': ('gen_cl_sheet_dechets_1.jpg', [2.0, 2.0], 0.2, 'déchets flottants : filet, planche, poisson mort'),
 'cl_dechets_c': ('gen_cl_sheet_dechets_2.jpg', [2.0, 2.0], 0.2, 'déchets flottants : papier de lanterne, pneu, nappe'),
}
HULL = {'cl_cable_lanternes', 'cl_bache', 'cl_treteaux', 'cl_friture', 'cl_pilotis', 'cl_cabane', 'cl_ponton', 'cl_stand_implants', 'cl_stand_puces', 'cl_stand_armes', 'cl_stand_medocs', 'cl_barriere_caisses', 'cl_presse_papiers'}
GRADE = {}
# correctifs 2026-10-22 : pentes source mesurées (Hough) sur les axes de l objet quand l arête basse n est pas mesurable
# (coude : bras en V renversé, apex à l arrière ; passerelle : escalier et poteaux). (pente axe x, pente axe z), sans miroir.
FORCE = {}
FITFP = {'cl_maison_the', 'cl_immeuble_fond', 'cl_cabane'}  # proportions x/z mesurées sur le dessin (plus grande dimension = plan) pour que le pivot tombe sur le coin dessiné
FP = {k: v[1] for k, v in LT.items() if not k.startswith('cl_stand_') and k not in FITFP}  # stands : proportions mesurées, plus grande dimension 2,5 m (les générations sont plus longues que profondes)  # emprises du plan imposées (pivot géométrique au coin avant)
STRICT = set()
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
ZCUT = {}
def zcut(rgba, f0, f1, tz=0.70):
    H, W = rgba.shape[:2]; x1, x2 = int(W * f0), int(W * f1); L = x2 - x1; dy = int(round(tz * L))
    out = np.zeros((H, W - L, 4), np.uint8); out[:, :x1] = rgba[:, :x1]
    right = np.zeros((H, W - x2, 4), np.uint8); right[dy:] = rgba[:H - dy, x2:]
    m = right[..., 3] > 0; seg = out[:, x1:]; seg[m] = right[m]
    return TI.clean(out, 200)
# correction de tangage : le générateur voit les stands plus en plongée que la caméra v4 (pentes de base 0,46/1,37) ; v4fix ramène les pentes
# par une échelle verticale uniforme d (~0,56), qui écrase aussi les hauteurs. stretch_heights() rallonge d un facteur f, colonne par colonne,
# seulement ce qui dépasse au-dessus du bord arrière du losange d emprise (arêtes 0,33/0,70 depuis le coin avant) : le losange au sol et
# l arête basse ne bougent pas, les verticales restent verticales.
def stretch_heights(rgba, f):
    a = rgba[..., 3] > 100; ys, xs = np.nonzero(a); by = ys.max(); bx = int(np.median(xs[ys >= by - 3])); x0, x1 = xs.min(), xs.max()
    L, Rr = bx - x0, x1 - bx; X = np.arange(rgba.shape[1]).astype(float)
    # bord arrière : du coin gauche (x0, by-0,331L) au coin arrière (x0+Rr, ...) pente 0,70 montante, puis descente 0,331 jusqu au coin droit
    ytop = np.where(X <= x0 + Rr, by - 0.331 * L - 0.70 * (X - x0), by - 0.70 * Rr - 0.331 * (x1 - X))
    pad = int((f - 1) * (ytop.max())) + 4; H = rgba.shape[0] + pad
    Yo = np.arange(H)[:, None].astype(float) - pad; T = ytop[None, :]
    src_y = np.where(Yo >= T, Yo, T - (T - Yo) / f)
    out = cv2.remap(rgba, np.broadcast_to(X[None, :], src_y.shape).astype(np.float32), src_y.astype(np.float32), cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    return TI.clean(out, 200)
PITCH = {'cl_stand_implants': 2.0, 'cl_stand_puces': 2.0, 'cl_stand_armes': 2.0, 'cl_stand_papiers': 1.8, 'cl_stand_medocs': 2.0, 'cl_caisse_armes': 2.2, 'cl_bac_puces': 2.5, 'cl_friture': 2.2}
TEXT = {'cl_maison_the', 'cl_immeuble_fond', 'cl_immeuble_fond_b', 'cl_cabane', 'cl_ponton', 'cl_stand_implants', 'cl_stand_puces', 'cl_stand_armes', 'cl_stand_papiers', 'cl_stand_medocs'}  # enseignes : jamais de miroir (texte inversé)
THIN = {'cl_cable_lanternes'}  # câble fin : pas d ouverture morphologique, petits éléments (lanternes) conservés
def key_green_thin(path):
    a = np.asarray(Image.open(path).convert('RGB')).astype(float); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    ex = g - np.maximum(r, b); al = np.clip((150 - ex) / 60, 0, 1)
    a[..., 1] = np.minimum(g, np.maximum(r, b) * 1.15 + 6) * (al < 0.999) + g * (al >= 0.999)
    return TI.clean(np.dstack([np.clip(a, 0, 255), al * 255]).astype('uint8'), 150)
PREFLIP = {'cl_cable_lanternes'}  # câble dessiné le long de l axe x en miroir : retournement horizontal avant contrôle
NOFIX = {'cl_cable_lanternes', 'cl_mahjong', 'cl_ballon_dragon', 'cl_ballon_carpe', 'cl_ballon_tigre', 'cl_ballon_phenix', 'cl_pieux', 'cl_pieux_b', 'cl_dechets_a', 'cl_dechets_b', 'cl_dechets_c'}  # ballons flottants, pieux ronds, décalques d eau
KEEPGREEN = {'cl_mahjong'}  # tapis de jeu vert sombre conservé
FULLDESPILL = {'cl_stand_medocs', 'cl_bocaux'}  # bocaux de verre : le fond vert transparaît
def load_maq(spec):
    _, f, bb = spec.split(':'); x0, y0, x1, y1 = map(int, bb.split(','))
    rgba = np.asarray(Image.open(HERE + '/' + MAQ + f).convert('RGBA'))[y0:y1, x0:x1].copy()
    # étalonnage nuit (même que Lower-Town) : désaturation partielle, assombrissement, dominante chaude (sprites de maquette éclairés plein jour)
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
KS = {}
def build(aid):
    src, (w, d), h, role = LT[aid]
    maq = src.startswith('MAQ:')
    rgba = load_maq(src) if maq else key_green_strict(G + src) if aid in STRICT else key_green_thin(G + src) if aid in THIN else TF.key_green_obj(G + src)
    if aid in GRADE: rgba = rgba.copy(); rgba[..., :3] = np.clip(rgba[..., :3].astype(float) * GRADE[aid] * np.array([1.0, 0.98, 0.95]), 0, 255).astype('uint8')
    # despill vert ciblé (passe 2) : seulement la bande de bord (4 px) et les pixels nettement verts. Le despill global de la passe 1
    # modifiait ~90 % des pixels (gris neutres légèrement verts assombris), créait de faux contours (tôle ondulée) et faisait basculer judge.
    from scipy import ndimage
    p = rgba[..., :3].astype(float); op = rgba[..., 3] > 0; ex = p[..., 1] - np.maximum(p[..., 0], p[..., 2])
    m = (op & ~ndimage.binary_erosion(op, iterations=4)) | ((ex > 8) & (aid not in KEEPGREEN))
    p[..., 1] = np.where(m, np.minimum(p[..., 1], np.maximum(p[..., 0], p[..., 2]) * 1.05 + 2), p[..., 1]); rgba = rgba.copy(); rgba[..., :3] = p.astype('uint8')
    if aid in PREFLIP: rgba = np.ascontiguousarray(rgba[:, ::-1])
    if aid in FULLDESPILL: p = rgba[..., :3].astype(float); p[..., 1] = np.minimum(p[..., 1], np.maximum(p[..., 0], p[..., 2])); rgba[..., :3] = p.astype('uint8')
    if aid in NOFIX: fix = {'v4fix': 'non applicable (' + ('flottant / révolution / décalque') + ')', 'pentes_apres': [None, None]}
    elif aid in FORCE:
        rgba, fix = TI.v4fix(rgba, force=FORCE[aid], mirror=False); fix['mesure'] = 'pentes forcées (axes mesurés par Hough sur la source)'
        fix['pentes_apres'] = [round(v, 2) for v in TI.base_slopes(rgba)[:2]]
    elif aid in HULL:
        ys, xs = np.nonzero(rgba[..., 3] > 100); hull = cv2.convexHull(np.stack([xs, ys], 1).astype(np.int32))
        hm = np.zeros(rgba.shape[:2], np.uint8); cv2.fillPoly(hm, [hull.reshape(-1, 2)], 1); hrgba = np.dstack([rgba[..., :3], hm * 255]).astype('uint8')
        sl, sr, _, _ = TI.base_slopes(hrgba); mir = (sr < sl) and aid not in TEXT
        rgba, fix = TI.v4fix(rgba, force=(sl, sr), mirror=mir); h2, _ = TI.v4fix(hrgba, force=(sl, sr), mirror=mir)
        fix['pentes_apres'] = [round(v, 2) for v in TI.base_slopes(h2)[:2]]; fix['mesure'] = 'enveloppe convexe'
    else: rgba, fix = TI.v4fix(rgba, mirror=False if aid in TEXT else None)
    if aid in ZCUT: rgba = zcut(rgba, *ZCUT[aid]); fix['coupe_z'] = list(ZCUT[aid])
    if KS.get(aid): rgba = keystone(rgba, KS[aid]); fix['keystone_k'] = KS[aid]; fix['pentes_apres'] = [round(v, 2) for v in TI.base_slopes(rgba)[:2]]
    elif aid not in KS and aid not in NOFIX and not TI.judge(rgba)['accepte']:
        # lot props : balayage automatique du redressement (k > 0 si arêtes hautes trop plates, k < 0 si trop raides), plus petit |k| accepté
        for k in (0.05, -0.05, 0.1, -0.1, 0.15, -0.15, 0.2, -0.2, 0.25, 0.3):
            o = keystone(rgba, k)
            if TI.judge(o)['accepte']: rgba = o; fix['keystone_k'] = k; break
    if PITCH.get(aid): rgba = stretch_heights(rgba, PITCH[aid]); fix['rallonge_hauteurs'] = PITCH[aid]
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
    man[aid] = {'file': 'buildings/' + aid + '.webp', 'source': (MAQ + src.split(':')[1] + ' ' + src.split(':')[2]) if maq else 'art-gen/' + src, 'origine': 'maquette' if maq else 'généré', 'px': list(im.size), 'anchor': [int(round(K * w * TI.R[0])), int(ay)],
                'footprint_m': [w, d], 'height_m': h, 'lot': 'china-lake v1 (creation/china-lake-sprites)',
                'anchor_note': 'pivot = coin avant bas géométrique (K w cos34,5 depuis le bord gauche, ligne opaque la plus basse)'}
    json.dump(man, open(A + 'manifest.json', 'w'), ensure_ascii=False, indent=1)
    rp = A + 'rapport_angles_chinalake.json'; rep = json.load(open(rp)) if os.path.exists(rp) else {}
    rep[aid] = j; json.dump(rep, open(rp, 'w'), ensure_ascii=False, indent=1)
    print(aid, json.dumps(j, ensure_ascii=False), man[aid]['px'], man[aid]['anchor'])
if __name__ == '__main__':
    for aid in (sys.argv[1:] or LT): build(aid)


# ---- sol g_cl_eau (convention des sols : assets/generated/g_*.webp, 512 × 512 RGB, chargé par loadSkins / ground.skin, tileM au choix de Rivet) ----
# La génération (1024²) est déjà périodique de 512 px (écart moyen 2/255 entre les deux moitiés) : on garde le carreau 64..576, dont les bords
# se raccordent (écart moyen 3,4/255, de l ordre du bruit entre pixels voisins), éclairci de 20 % (noir pétrole lisible sous la teinte de zone).
def build_eau(src='gen_cl_eau_src.jpg', off=64, gain=1.2):
    a = np.asarray(Image.open(G + src).convert('RGB')).astype(float)[off:off + 512, off:off + 512] * gain
    out = Image.fromarray(np.clip(a, 0, 255).astype('uint8'))
    out.save(HERE + '/assets/generated/g_cl_eau.webp', quality=88)
    t = np.asarray(out).astype(float); seam = float(np.abs(t[:, 0] - t[:, -1]).mean() + np.abs(t[0] - t[-1]).mean()) / 2
    inner = float(np.abs(np.diff(t, axis=1)).mean()); print('g_cl_eau', out.size, 'raccord', round(seam, 2), 'voisins', round(inner, 2))
    return seam, inner
