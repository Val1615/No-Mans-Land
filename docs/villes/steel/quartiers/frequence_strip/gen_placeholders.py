"""Placeholders Fréquence Strip (zone steel_strip) : RGBA webp aux tailles attendues, cadre magenta + croix,
et manifest assets/steel/frequence_strip/manifest.json. Les planches d'enseignes ont des cases numérotées.
Ne réécrit pas une entrée déjà passée en status v1."""
from PIL import Image, ImageDraw
import os, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..')
OUT = os.path.join(ROOT, 'assets', 'steel', 'frequence_strip')
SRC = 'docs/villes/steel/quartiers/frequence_strip/gen_placeholders.py'
STATUS = 'placeholder, frequence-strip (zone steel_strip)'
TILES = ['g_fs_asphalte_mouille', 'g_fs_trottoir', 'g_fs_grille_vapeur']
BUILD = {  # px, footprint_m
 'fs_neon7': ((600, 500), [12, 6]), 'fs_corestack': ((600, 560), [12, 6]), 'fs_retour': ((400, 360), [8, 6]),
 'fs_capsules': ((300, 420), [6, 6]), 'fs_facade_nord': ((400, 420), [8, 6]), 'fs_facade_sud': ((400, 360), [8, 6]),
 'fs_stand_brochettes': ((200, 220), [4, 4]), 'fs_stand_merch': ((200, 220), [4, 4]), 'fs_tapis': ((200, 110), [4, 2]),
 'fs_grille_est': ((200, 220), [4, 1]),
}
SIGNS = {  # frame px, frames, fps, contenu
 'fs_ens_neon7': ((256, 128), 4, 4, 'logo Neon-7, allumage par segments'),
 'fs_ens_corestack': ((192, 192), 6, 6, 'baies qui défilent, lumière cyan'),
 'fs_ens_vibes': ((128, 256), 4, 2, 'écran vertical, Vibes (réf. pp_billboard_src)'),
 'fs_ens_tron': ((128, 256), 4, 3, 'écran vertical, Tron (réf. pp_holo_tron_src), glitch'),
 'fs_ens_coeur': ((96, 96), 6, 8, 'cœur néon qui bat'),
 'fs_ens_retour': ((192, 64), 3, 1.5, 'néon ambre du bar, grésillement'),
 'fs_ens_capsules': ((96, 192), 2, 1, 'colonne de hublots allumés'),
 'fs_vapeur': ((80, 200), 4, 6, 'panache de vapeur, semi-transparent'),
}
NPCS = {'rocco': 1.95, 'lila': 1.68, 'hugo': 1.74, 'okoro': 1.70, 'tibo': 1.66, 'yun': 1.72,
        'gt_promo': 1.85, 'sacha': 1.78, 'marius': 1.70, 'foule_a': 1.72, 'foule_b': 1.66}
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
    add(k, {'file': f'steel/frequence_strip/{k}.webp', 'px': [512, 512], 'tile_m': 4.0, 'tuilable': True}, lambda k=k: ph(k, 512, 512, (43, 62, 82, 255)))
for k, ((w, h), fp) in BUILD.items():
    add(k, {'file': f'steel/frequence_strip/{k}.webp', 'px': [w, h], 'anchor': [w // 2, h - 1], 'footprint_m': fp}, lambda k=k, w=w, h=h: ph(k, w, h))
for k, ((fw, fh), n, fps, note) in SIGNS.items():
    for suf, s in (('', 1), ('_mobile', 2)):
        W, H = fw // s, fh // s
        add(k + suf, {'file': f'steel/frequence_strip/{k}{suf}.webp', 'px': [W * n, H], 'anime': True, 'frames': n,
                      'frame_px': [W, H], 'fps': fps, 'boucle': True, 'contenu': note},
            lambda k=k + suf, W=W, H=H, n=n: ph(k, W * n, H, cells=n))
for k, hm in NPCS.items():
    add(f'gen_fs_{k}', {'file': f'steel/frequence_strip/gen_fs_{k}.webp', 'px': [180, 512], 'height_m': hm, 'footprint_m': [0.6, 0.6], 'anchor': [90, 511]},
        lambda k=k: ph(f'gen_fs_{k}', 180, 512))
    if not k.startswith('foule'):
        p = f'portrait-gen_fs_{k}'
        add(p, {'file': f'steel/frequence_strip/{p}.webp', 'px': [192, 192], 'npc': f'gen_fs_{k}'}, lambda p=p: ph(p, 192, 192, (58, 44, 32, 255)))
json.dump(man, open(mp, 'w'), ensure_ascii=False, indent=2)
print(len(man))
