"""Placeholders Pulse Plaza : RGBA webp aux tailles attendues, cadre magenta + croix.
A remplacer par les vrais assets. Ecrit dans assets/steel/pulse_plaza/."""
from PIL import Image, ImageDraw
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..', 'assets', 'steel', 'pulse_plaza')
ITEMS = {
 # sols (512x512, tuilables)
 'g_pp_dalle.webp': (512, 512, True), 'g_pp_dalle_mouillee.webp': (512, 512, True), 'g_pp_grille.webp': (512, 512, True),
 # batiments et mobilier (px estimes a 50 px/m)
 'pp_arcadius.webp': (1200, 900, False), 'pp_ecran_feed.webp': (1000, 700, False), 'pp_holo_socle.webp': (400, 300, False),
 'pp_holo_tron.webp': (220, 512, False), 'pp_billboard.webp': (220, 520, False), 'pp_kiosque.webp': (220, 260, False),
 'pp_guerite.webp': (220, 260, False), 'pp_nouilles.webp': (220, 240, False), 'pp_distrib.webp': (110, 160, False),
 'pp_banc.webp': (110, 60, False), 'pp_portique.webp': (220, 180, False), 'pp_camera.webp': (40, 140, False),
 'pp_escalier.webp': (200, 200, False),
}
NPCS = {'maelle': 1.64, 'dorian': 1.78, 'brisset': 1.80, 'pham': 1.62, 'isaure': 1.70,
        'clone_gt': 1.85, 'gaspard': 1.72, 'noor': 1.58, 'vasseur': 1.76, 'foule_a': 1.70, 'foule_b': 1.74}
for k in NPCS:
    ITEMS[f'gen_pp_{k}.webp'] = (180, 512, False)
    if not k.startswith('foule'):
        ITEMS[f'portrait-gen_pp_{k}.webp'] = (192, 192, True)
os.makedirs(OUT, exist_ok=True)
for name, (w, h, opaque) in ITEMS.items():
    im = Image.new('RGBA', (w, h), (58, 44, 32, 255) if name.startswith('portrait') else ((43, 62, 82, 255) if opaque else (0, 0, 0, 0)))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=(224, 60, 168, 255), width=3)
    d.line([0, 0, w - 1, h - 1], fill=(224, 60, 168, 160), width=2)
    d.line([0, h - 1, w - 1, 0], fill=(224, 60, 168, 160), width=2)
    d.text((6, 6), 'PLACEHOLDER', fill=(255, 255, 255, 255))
    im.save(os.path.join(OUT, name), 'WEBP', lossless=True)
print(len(ITEMS))
