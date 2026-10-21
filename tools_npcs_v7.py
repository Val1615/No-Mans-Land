# v7 : PNJ des nouveaux quartiers (GenerateImage, même chaîne que tools_assets.py : détourage du fond uni, portrait recadré).
import numpy as np, json
from PIL import Image
OUT = '/workspace/nml/game/assets/'
gen = {'gen_teo': ('art-gen/gen_teo.jpg', 1.70), 'gen_ezequiel': ('art-gen/gen_ezequiel.jpg', 1.78), 'gen_sol': ('art-gen/gen_sol.jpg', 1.80)}
man = json.load(open(OUT + 'reused/manifest.json'))
for k, (f, h) in gen.items():
  a = np.asarray(Image.open('/workspace/nml/game/' + f).convert('RGB')).astype(float)
  key = np.median(np.concatenate([a[:8].reshape(-1, 3), a[:, :8].reshape(-1, 3), a[:, -8:].reshape(-1, 3)]), axis=0)
  d = np.linalg.norm(a - key, axis=2); al = np.clip((d - 40) / 50, 0, 1)
  m = np.minimum(a[..., 0], a[..., 2]); sp = np.clip(m - a[..., 1], 0, None) * (1 - al); a[..., 0] -= sp * 0.8; a[..., 2] -= sp * 0.8
  im = Image.fromarray(np.dstack([np.clip(a, 0, 255), al * 255]).astype('uint8'), 'RGBA'); im = im.crop(im.getbbox())
  im.thumbnail((512, 512), Image.LANCZOS); im.save(OUT + 'generated/' + k + '.webp', quality=90)
  man[k] = {'file': 'generated/' + k + '.webp', 'source': 'GenerateImage (cursor), ' + f, 'height_m': h, 'px': list(im.size), 'footprint_m': [0.6, 0.6], 'status': 'généré v7'}
  w, hh = im.size; s = int(w * 0.62); cx = w // 2; box = (max(0, cx - s // 2), 0, max(0, cx - s // 2) + s, s)
  bg = Image.new('RGBA', (s, s), (58, 44, 32, 255)); bg.alpha_composite(im.crop(box)); bg.convert('RGB').resize((192, 192)).save(OUT + 'generated/portrait-' + k + '.webp', quality=88)
json.dump(man, open(OUT + 'reused/manifest.json', 'w'), indent=1, ensure_ascii=False)
print('ok')
