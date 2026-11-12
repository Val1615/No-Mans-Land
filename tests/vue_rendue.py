# Contrôle au pixel de la vue réellement affichée d'un véhicule (rendu isolé, fond magenta) : on compare la silhouette et la luminance
# du rendu aux quatre vues possibles (avant / dos, native / miroir) tirées des assets d'Ocre. Renvoie la vue la plus ressemblante.
import base64, io, os
import numpy as np
from PIL import Image

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'steel', 'center_town')
W, H = 96, 56

def _norm(gray, mask):
    g = gray[mask]
    return (gray - g.mean()) / (g.std() + 1e-6) if g.size else gray * 0

def _prep_rendu(url):
    im = Image.open(io.BytesIO(base64.b64decode(url.split(',', 1)[1]))).convert('RGB'); a = np.asarray(im).astype(int)
    fond = (a[..., 0] > 200) & (a[..., 1] < 70) & (a[..., 2] > 200)
    ys, xs = np.where(~fond)
    if not len(xs): return None
    box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    m = Image.fromarray((~fond * 255).astype(np.uint8)).crop(box).resize((W, H), Image.NEAREST)
    g = im.convert('L').crop(box).resize((W, H), Image.BILINEAR)
    return np.asarray(m) > 127, np.asarray(g).astype(float)

def _prep_asset(key, miroir):
    im = Image.open(os.path.join(ASSETS, key + '.webp')).convert('RGBA')
    if miroir: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    box = im.split()[3].point(lambda v: 255 if v > 127 else 0).getbbox(); im = im.crop(box)
    m = np.asarray(im.split()[3].resize((W, H), Image.NEAREST)) > 127
    fond = Image.new('RGBA', im.size, (0, 0, 0, 255)); fond.alpha_composite(im)
    return m, np.asarray(fond.convert('L').resize((W, H), Image.BILINEAR)).astype(float)

def vue_rendue(url, cle):
    """cle : clé de la vue avant (ct_veh_<type>_avant_v4_3q). Renvoie (meilleure, scores) ; meilleure = (clé, sx)."""
    r = _prep_rendu(url)
    if r is None: return None, {}
    mr, gr = r; scores = {}
    for key in (cle, cle.replace('_avant_', '_dos_')):
        if not os.path.exists(os.path.join(ASSETS, key + '.webp')): continue
        for sx in (1, -1):
            ma, ga = _prep_asset(key, sx < 0); u = mr | ma; inter = (mr & ma).sum() / max(1, u.sum())
            c = float((_norm(gr, u) * _norm(ga, u))[u].mean()) if u.any() else 0
            scores[(key, sx)] = round(inter + c, 4)
    best = max(scores, key=scores.get)
    return best, scores
