"""Placeholders Dôme Fréquence (zone steel_dome) : RGBA webp aux tailles attendues, cadre magenta + croix,
et manifest assets/steel/dome_frequence/manifest.json. Les planches d'enseignes ont des cases numérotées.
Ne réécrit pas une entrée déjà passée en status v1."""
from PIL import Image, ImageDraw
import os, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..')
OUT = os.path.join(ROOT, 'assets', 'steel', 'dome_frequence')
SRC = 'docs/villes/steel/quartiers/dome_frequence/gen_placeholders.py'
STATUS = 'placeholder, dome-frequence (zone steel_dome)'
TILES = ['g_df_marbre', 'g_df_moquette', 'g_df_scene']
BUILD = {  # px, footprint_m (intérieur)
 'df_scene': ((900, 360), [18, 4]), 'df_ecran_cadre': ((300, 200), [6, 0.5]), 'df_gradin': ((300, 160), [6, 2]),
 'df_regie': ((220, 180), [4, 4]), 'df_enceinte': ((90, 220), [1, 1]), 'df_bar': ((320, 200), [6, 2]),
 'df_vestiaire': ((320, 220), [6, 2]), 'df_banquette': ((140, 90), [2, 1]), 'df_colonne': ((80, 320), [1, 1]),
 'df_borne': ((80, 150), [1, 1]), 'df_cloison': ((300, 220), [6, 0.5]), 'df_porte': ((200, 240), [6, 0.5]),
 'df_verriere': ((900, 900), [30, 30]),
}
SIGNS = {  # frame px, frames, fps, contenu
 'df_ens_ecran_vibes': ((256, 144), 4, 2, 'écran de scène 16:9, Vibes (réf. pp_billboard_src)'),
 'df_ens_ecran_tron': ((256, 144), 4, 3, 'écran de scène 16:9, Tron (réf. pp_holo_tron_src), glitch'),
 'df_ens_lumieres': ((384, 128), 6, 6, 'rampe de lumières de scène, magenta et cyan, un seul sprite pour toute la rampe'),
 'df_ens_verriere': ((256, 256), 4, 1, 'lueur ambre de la verrière, calque de plafond semi-transparent'),
 'df_ens_bar': ((192, 64), 3, 1.5, 'néon ambre du bar, pictogramme'),
 'df_ens_vu': ((96, 64), 4, 8, 'VU-mètres de la console'),
 'df_ens_facade_vibes': ((128, 256), 4, 2, 'écran de façade, Vibes, pour b_st_ct_dome (zone steel_center)'),
 'df_ens_facade_tron': ((128, 256), 4, 3, 'écran de façade, Tron, pour b_st_ct_dome (zone steel_center)'),
}
NPCS = {'varenne': 1.72, 'octave': 1.78, 'jade': 1.66, 'nils': 1.70, 'pia': 1.64, 'ruben': 1.88,
        'helene': 1.68, 'gardien': 1.60, 'foule_a': 1.70, 'foule_b': 1.66}
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
    add(k, {'file': f'steel/dome_frequence/{k}.webp', 'px': [512, 512], 'tile_m': 4.0, 'tuilable': True}, lambda k=k: ph(k, 512, 512, (43, 62, 82, 255)))
for k, ((w, h), fp) in BUILD.items():
    add(k, {'file': f'steel/dome_frequence/{k}.webp', 'px': [w, h], 'anchor': [w // 2, h - 1], 'footprint_m': fp}, lambda k=k, w=w, h=h: ph(k, w, h))
for k, ((fw, fh), n, fps, note) in SIGNS.items():
    for suf, s in (('', 1), ('_mobile', 2)):
        W, H = fw // s, fh // s
        add(k + suf, {'file': f'steel/dome_frequence/{k}{suf}.webp', 'px': [W * n, H], 'anime': True, 'frames': n,
                      'frame_px': [W, H], 'fps': fps, 'boucle': True, 'contenu': note},
            lambda k=k + suf, W=W, H=H, n=n: ph(k, W * n, H, cells=n))
for k, hm in NPCS.items():
    add(f'gen_df_{k}', {'file': f'steel/dome_frequence/gen_df_{k}.webp', 'px': [180, 512], 'height_m': hm, 'footprint_m': [0.6, 0.6], 'anchor': [90, 511]},
        lambda k=k: ph(f'gen_df_{k}', 180, 512))
    if not k.startswith('foule'):
        p = f'portrait-gen_df_{k}'
        add(p, {'file': f'steel/dome_frequence/{p}.webp', 'px': [192, 192], 'npc': f'gen_df_{k}'}, lambda p=p: ph(p, 192, 192, (58, 44, 32, 255)))
json.dump(man, open(mp, 'w'), ensure_ascii=False, indent=2)
print(len(man))
