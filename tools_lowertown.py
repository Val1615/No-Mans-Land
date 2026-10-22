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
