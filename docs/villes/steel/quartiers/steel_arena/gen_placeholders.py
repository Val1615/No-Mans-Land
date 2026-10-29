"""Placeholders Steel Arena (zone steel_arena) : RGBA webp aux tailles attendues, cadre magenta + croix,
et manifest assets/steel/steel_arena/manifest.json. Les planches d'enseignes ont des cases numérotées.
Ne réécrit pas une entrée déjà passée en status v1."""
from PIL import Image, ImageDraw
import os, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..')
OUT = os.path.join(ROOT, 'assets', 'steel', 'steel_arena')
SRC = 'docs/villes/steel/quartiers/steel_arena/gen_placeholders.py'
STATUS = 'placeholder, steel-arena (zone steel_arena)'
TILES = ['g_ar_parvis', 'g_ar_parvis_mouille', 'g_ar_ligne_file']
BUILD = {  # px, footprint_m
 'ar_arena': ((1400, 900), [48, 12]), 'ar_entree': ((420, 360), [8, 2]), 'ar_portique': ((200, 220), [2, 1]),
 'ar_barriere': ((220, 120), [4, 0.5]), 'ar_projecteur': ((160, 300), [2, 2]), 'ar_lampadaire': ((80, 300), [0.6, 0.6]),
 'ar_guichets': ((220, 260), [4, 4]), 'ar_merch': ((220, 260), [4, 4]), 'ar_securite': ((220, 240), [4, 4]),
 'ar_regie': ((340, 240), [6, 4]), 'ar_panneau_nml': ((120, 220), [2, 0.5]),
}
SIGNS = {  # frame px, frames, fps, contenu
 'ar_ens_ecran_vibes': ((256, 144), 4, 2, 'écran du dôme, Vibes en concert (réf. pp_billboard_src)'),
 'ar_ens_ecran_tron': ((256, 144), 4, 3, 'écran du dôme, Tron (réf. pp_holo_tron_src), glitch'),
 'ar_ens_fronton': ((384, 96), 4, 3, 'fronton lumineux sans texte, onde violette'),
 'ar_ens_faisceau': ((128, 256), 6, 6, 'faisceau de projecteur qui balaie, semi-transparent'),
 'ar_ens_coeurs': ((64, 64), 4, 4, 'bâton-cœur des fans qui pulse'),
 'ar_ens_guichet': ((96, 64), 2, 1, 'écran du guichet, complet / ouvert en pictogramme'),
 'ar_ens_human_corp': ((128, 128), 3, 1.5, 'logo abstrait Human Corp qui respire'),
}
NPCS = {'ferrand': 1.90, 'anouk': 1.64, 'zelie': 1.60, 'malik': 1.80, 'ines': 1.62, 'clem': 1.72,
        'garnier': 1.82, 'bastien': 1.76, 'laure': 1.58, 'foule_a': 1.70, 'foule_b': 1.66}
def ph(name, w, h, bg=(0, 0, 0, 0), cells=1):
    im = Image.new('RGBA', (w, h), bg); d = ImageDraw.Draw(im); cw = w // cells
    for i in range(cells):
        x0 = i * cw; d.rectangle([x0, 0, x0 + cw - 1, h - 1], outline=(224, 60, 168, 255), width=2)
        d.line([x0, 0, x0 + cw - 1, h - 1], fill=(224, 60, 168, 160)); d.line([x0, h - 1, x0 + cw - 1, 0], fill=(224, 60, 168, 160))
        d.text((x0 + 4, 4), f'PH {i + 1}' if cells > 1 else 'PLACEHOLDER', fill=(255, 255, 255, 255))
    im.save(os.path.join(OUT, name + '.webp'), 'WEBP', lossless=True)
os.makedirs(OUT, exist_ok=True)
mp = os.path.join(OUT, 'manifest.json')
old = json.load(open(mp)) if os.path.exists(mp) else {}
man = {}
def add(k, e, draw):
    if old.get(k, {}).get('status') == 'v1': man[k] = old[k]; return
    draw(); e.update(source=SRC, status=STATUS); man[k] = e
for k in TILES:
    add(k, {'file': f'steel/steel_arena/{k}.webp', 'px': [512, 512], 'tile_m': 4.0, 'tuilable': True}, lambda k=k: ph(k, 512, 512, (43, 62, 82, 255)))
for k, ((w, h), fp) in BUILD.items():
    add(k, {'file': f'steel/steel_arena/{k}.webp', 'px': [w, h], 'anchor': [w // 2, h - 1], 'footprint_m': fp}, lambda k=k, w=w, h=h: ph(k, w, h))
for k, ((fw, fh), n, fps, note) in SIGNS.items():
    for suf, s in (('', 1), ('_mobile', 2)):
        W, H = fw // s, fh // s
        add(k + suf, {'file': f'steel/steel_arena/{k}{suf}.webp', 'px': [W * n, H], 'anime': True, 'frames': n,
                      'frame_px': [W, H], 'fps': fps, 'boucle': True, 'contenu': note},
            lambda k=k + suf, W=W, H=H, n=n: ph(k, W * n, H, cells=n))
for k, hm in NPCS.items():
    add(f'gen_ar_{k}', {'file': f'steel/steel_arena/gen_ar_{k}.webp', 'px': [180, 512], 'height_m': hm, 'footprint_m': [0.6, 0.6], 'anchor': [90, 511]},
        lambda k=k: ph(f'gen_ar_{k}', 180, 512))
    if not k.startswith('foule'):
        p = f'portrait-gen_ar_{k}'
        add(p, {'file': f'steel/steel_arena/{p}.webp', 'px': [192, 192], 'npc': f'gen_ar_{k}'}, lambda p=p: ph(p, 192, 192, (58, 44, 32, 255)))
json.dump(man, open(mp, 'w'), ensure_ascii=False, indent=2)
print(len(man))
