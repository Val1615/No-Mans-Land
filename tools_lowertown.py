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
    rgba = TF.key_green_obj(G + src)
    # despill vert ciblé (passe 2) : seulement la bande de bord (4 px) et les pixels nettement verts. Le despill global de la passe 1
    # modifiait ~90 % des pixels (gris neutres légèrement verts assombris), créait de faux contours (tôle ondulée) et faisait basculer judge.
    from scipy import ndimage
    p = rgba[..., :3].astype(float); op = rgba[..., 3] > 0; ex = p[..., 1] - np.maximum(p[..., 0], p[..., 2])
    m = (op & ~ndimage.binary_erosion(op, iterations=4)) | (ex > 8)
    p[..., 1] = np.where(m, np.minimum(p[..., 1], np.maximum(p[..., 0], p[..., 2]) * 1.05 + 2), p[..., 1]); rgba = rgba.copy(); rgba[..., :3] = p.astype('uint8')
    rgba, fix = TI.v4fix(rgba)
    if KS.get(aid): rgba = keystone(rgba, KS[aid]); fix['keystone_k'] = KS[aid]; fix['pentes_apres'] = [round(v, 2) for v in TI.base_slopes(rgba)[:2]]
    # emprise : proportions x/z mesurées sur l'arête basse corrigée (coin avant = point le plus bas), échelle fixée par la plus grande dimension
    m = rgba[..., 3] > 100; ys, xs = np.nonzero(m); by = ys.max(); bx = int(np.median(xs[ys >= by - 3]))
    lw, ld = (bx - xs.min()) / cy, (xs.max() - bx) / sy; s = max(w, d) / max(lw, ld)
    w, d = round(lw * s * 2) / 2, round(ld * s * 2) / 2
    j = TI.judge(rgba); j['correction_v4'] = fix
    pa = fix['pentes_apres']
    if abs(pa[0] - 0.33) <= 0.06 and abs(pa[1] - 0.70) <= 0.08: j['accepte_arete_basse'] = True
    else: j['accepte_arete_basse'] = False
    R, U = TI.R, TI.U; hh = rgba.shape[0] / rgba.shape[1]; sw = w * abs(R[0]) + d * abs(R[2])
    implied = (sw * hh - w * abs(U[0]) - d * abs(U[2])) / U[1]
    j.update({'source': 'art-gen/' + src, 'role': role, 'emprise_m': [w, d], 'hauteur_attendue_m': h, 'hauteur_implicite_m': round(implied, 2),
              'echelle_ok': bool(abs(implied - h) <= 0.3 * h + 0.15)})
    sc = K * (w * cy + d * sy) / rgba.shape[1]
    im = Image.fromarray(rgba, 'RGBA').resize((round(rgba.shape[1] * sc), round(rgba.shape[0] * sc)), Image.LANCZOS)
    a = np.asarray(im)[..., 3] > 100; ys, xs = np.nonzero(a); ay = ys.max(); ax = int(np.median(xs[ys >= ay - 3]))
    j['magenta_bord_pct'] = TF.mag_edge_pct(np.asarray(im))[0]
    im.save(A + aid + '.webp', quality=90)
    man = json.load(open(A + 'manifest.json'))
    man[aid] = {'file': 'buildings/' + aid + '.webp', 'source': 'art-gen/' + src, 'px': list(im.size), 'anchor': [ax, int(ay)],
                'footprint_m': [w, d], 'height_m': h, 'lot': 'lower-town v1 (creation/lower-town-sprites)',
                'anchor_note': 'coin avant bas (pivot), emprises provisoires à réconcilier avec Rivet'}
    json.dump(man, open(A + 'manifest.json', 'w'), ensure_ascii=False, indent=1)
    rp = A + 'rapport_angles_lowertown.json'; rep = json.load(open(rp)) if os.path.exists(rp) else {}
    rep[aid] = j; json.dump(rep, open(rp, 'w'), ensure_ascii=False, indent=1)
    print(aid, json.dumps(j, ensure_ascii=False), man[aid]['px'], man[aid]['anchor'])
if __name__ == '__main__':
    for aid in (sys.argv[1:] or LT): build(aid)
