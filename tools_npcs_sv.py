# v14 : PNJ de la Sous-Ville (GenerateImage), même chaîne que tools_npcs_steel.py ; planche 2x2 découpée par quadrant.
import numpy as np, json
from PIL import Image
OUT = '/workspace/nml/game/assets/'
gen = {'gen_elio': ('art-gen/gen_elio.jpg', None, 1.78), 'gen_sv_guetteuse': ('art-gen/gen_sv_people.jpg', 0, 1.64), 'gen_sv_receleur': ('art-gen/gen_sv_people.jpg', 1, 1.74),
       'gen_sv_gang': ('art-gen/gen_sv_people.jpg', 2, 1.84), 'gen_sv_dealer': ('art-gen/gen_sv_people.jpg', 3, 1.80)}
man = json.load(open(OUT + 'reused/manifest.json'))
for k, (f, q, h) in gen.items():
  a = np.asarray(Image.open('/workspace/nml/game/' + f).convert('RGB')).astype(float)
  if q is not None: H, W = a.shape[:2]; c, r = q % 2, q // 2; a = a[r * H // 2:(r + 1) * H // 2, c * W // 2:(c + 1) * W // 2].copy()
  key = np.median(np.concatenate([a[:8].reshape(-1, 3), a[:, :8].reshape(-1, 3), a[:, -8:].reshape(-1, 3)]), axis=0)
  d = np.linalg.norm(a - key, axis=2); al = np.clip((d - 40) / 50, 0, 1)
  k_ = np.clip(al, 0.05, 1)[..., None]; a = np.clip((a - (1 - k_) * key) / k_, 0, 255)
  im = Image.fromarray(np.dstack([a, al * 255]).astype('uint8'), 'RGBA'); im = im.crop(im.getbbox())
  im.thumbnail((512, 512), Image.LANCZOS); im.save(OUT + 'generated/' + k + '.webp', quality=90)
  man[k] = {'file': 'generated/' + k + '.webp', 'source': 'GenerateImage (cursor), ' + f + ('' if q is None else f' #{q}'), 'height_m': h, 'px': list(im.size), 'footprint_m': [0.6, 0.6], 'status': 'généré v14'}
  w, hh = im.size; s = int(w * 0.62); cx = w // 2; box = (max(0, cx - s // 2), 0, max(0, cx - s // 2) + s, s)
  bg = Image.new('RGBA', (s, s), (58, 44, 32, 255)); bg.alpha_composite(im.crop(box)); bg.convert('RGB').resize((192, 192)).save(OUT + 'generated/portrait-' + k + '.webp', quality=88)
  print(k, im.size)
json.dump(man, open(OUT + 'reused/manifest.json', 'w'), indent=1, ensure_ascii=False)
