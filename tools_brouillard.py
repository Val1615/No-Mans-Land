"""Brouillard de guerre de la carte des No Man's Land (dessin déterministe, seed fixe).
Sorties dans assets/ui/maps/fog/ : texture tuilable (512 et 256 px) et masque de dissipation (300 et 150 px).
Usage : python3 tools_brouillard.py"""
import os
import numpy as np
from PIL import Image

OUT = 'assets/ui/maps/fog'
SEED = 2175
# rampe ambre sombre tirée du fond nml_fond.webp (centiles 5 à 95), plus sombre pour rester un voile
RAMPE = np.array([[10, 8, 7], [20, 16, 12], [36, 28, 19], [58, 45, 29], [78, 60, 38.]])


def bruit_periodique(n, beta, seed, fmin=2):
    """Bruit fractal 1/f^beta filtré en fréquence : périodique, donc tuilable sans couture."""
    r = np.random.default_rng(seed)
    f = np.fft.fft2(r.standard_normal((n, n)))
    k = np.fft.fftfreq(n) * n
    kk = np.sqrt(k[:, None] ** 2 + k[None, :] ** 2)
    filt = np.where(kk < fmin, 0, 1 / np.maximum(kk, 1) ** beta)
    b = np.real(np.fft.ifft2(f * filt))
    return (b - b.min()) / (b.max() - b.min())


def rampe(L):
    t = np.clip(L, 0, 1) * (len(RAMPE) - 1)
    i = np.clip(t.astype(int), 0, len(RAMPE) - 2)
    f = (t - i)[..., None]
    return RAMPE[i] * (1 - f) + RAMPE[i + 1] * f


def texture(n):
    nuages = bruit_periodique(n, 1.6, SEED)            # grandes masses de brume
    voiles = bruit_periodique(n, 1.1, SEED + 1, 6)     # traînées plus fines
    grain = bruit_periodique(n, 0.3, SEED + 2, 1)      # poussière
    L = 0.62 * nuages + 0.28 * voiles + 0.10 * grain
    L = (L - L.min()) / (L.max() - L.min())
    L = 0.12 + 0.62 * L ** 1.3
    return Image.fromarray(np.clip(rampe(L), 0, 255).astype('uint8'), 'RGB')


def masque(n):
    """Alpha du brouillard pour une case dissipée : 0 au centre (transparent), 255 aux bords.
    À utiliser en destination-out : on efface le brouillard là où le masque est opaque, donc on fournit l'inverse."""
    y, x = np.mgrid[0:n, 0:n] + 0.5
    c = n / 2
    a = np.arctan2(y - c, x - c)
    rng = np.random.default_rng(SEED + 3)
    bord = 1 + sum(rng.uniform(0.012, 0.025) * np.sin(k * a + rng.uniform(0, 6.3)) for k in (2, 3, 5))
    d = np.hypot(x - c, y - c) / (c * bord)
    # plein jusqu'au tiers (la case elle-même, 100 px sur 300), puis fondu doux jusqu'au bord
    v = np.clip((d - 0.30) / 0.68, 0, 1)
    v = v * v * (3 - 2 * v)
    efface = (1 - v) * 255                              # opacité de l'effacement
    rgba = np.zeros((n, n, 4), 'uint8'); rgba[..., :3] = 255; rgba[..., 3] = np.clip(efface, 0, 255).astype('uint8')
    return Image.fromarray(rgba, 'RGBA')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for n, suf in ((512, ''), (256, '_mobile')):
        t = texture(n)
        t.save(f'{OUT}/nml_brouillard{suf}.png', optimize=True)
        t.save(f'{OUT}/nml_brouillard{suf}.webp', quality=88, method=6)
    masque(300).save(f'{OUT}/nml_brouillard_masque.png', optimize=True)
    masque(150).save(f'{OUT}/nml_brouillard_masque_mobile.png', optimize=True)
    print('ok')
