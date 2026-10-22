"""Extract six generated linear props without altering source visible RGB or alpha."""
from pathlib import Path
from PIL import Image, ImageDraw
import json
import numpy as np
from scipy.ndimage import label, find_objects, distance_transform_edt

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'art-source/linear-v12.png'
NAMES = ['chainFenceQ', 'chainFenceR', 'stoneBalustradeQ', 'stoneBalustradeR', 'insulatedPipeQ', 'insulatedPipeR']
# Estimated ground contact centres in the original image. Q goes down-right;
# R goes up-right. Pipe ground contacts are the two support-foot centres.
GROUND = [
    [(100, 254), (448, 446)],
    [(604, 450), (938, 263)],
    [(1111, 278), (1433, 435)],
    [(110, 916), (417, 748)],
    [(634, 772), (861, 904)],
    [(1183, 915), (1410, 782)],
]
PIPE_CENTRES = {4: [(589, 622), (933, 807)], 5: [(1124, 815), (1459, 625)]}

im = Image.open(SOURCE).convert('RGBA')
arr = np.array(im)
alpha = arr[:, :, 3]
labels, count = label(alpha > 32)
components = []
for number, slices in enumerate(find_objects(labels), 1):
    if slices is not None and np.count_nonzero(labels[slices] == number) > 3000:
        components.append((number, slices))
assert len(components) == 6, len(components)
components.sort(key=lambda v: (0 if (v[1][0].start + v[1][0].stop) / 2 < im.height / 2 else 1, (v[1][1].start + v[1][1].stop) / 2))
seeds = np.zeros(labels.shape, dtype=np.uint8)
for order, (number, slices) in enumerate(components, 1):
    seeds[labels == number] = order
_, nearest = distance_transform_edt(seeds == 0, return_indices=True)
belongs = seeds[nearest[0], nearest[1]]
rows = []
for index, (number, slices) in enumerate(components):
    selection = belongs == index + 1
    ys, xs = np.where(selection & (alpha > 16))
    x0, y0 = max(0, int(xs.min()) - 4), max(0, int(ys.min()) - 4)
    x1, y1 = min(im.width, int(xs.max()) + 5), min(im.height, int(ys.max()) + 5)
    crop = arr[y0:y1, x0:x1].copy()
    crop[:, :, 3][~selection[y0:y1, x0:x1]] = 0
    part = Image.fromarray(crop, 'RGBA')
    padded = Image.new('RGBA', (part.width + 8, part.height + 8))
    padded.paste(part, (4, 4))
    output = ROOT / 'dist/assets' / f'linear-v12-{index}.webp'
    padded.save(output, 'WEBP', lossless=True, exact=True, method=6)
    expected = np.array(padded)
    restored = np.array(Image.open(output).convert('RGBA'))
    assert np.array_equal(restored[:, :, 3], expected[:, :, 3])
    visible = expected[:, :, 3] > 0
    assert np.array_equal(restored[:, :, :3][visible], expected[:, :, :3][visible])
    def uv(points):
        return [[round((x - x0 + 4) / padded.width, 6), round((y - y0 + 4) / padded.height, 6)] for x, y in points]
    row = {'index': index, 'kind': NAMES[index], 'file': str(output.relative_to(ROOT)),
           'orientation': 'q+' if index % 2 == 0 else 'r+',
           'width': padded.width, 'height': padded.height,
           'source': str(SOURCE.relative_to(ROOT)), 'source_bbox': [x0, y0, x1, y1],
           'crop_padding_px': 4, 'ground_endpoints_uv': uv(GROUND[index]),
           'ground_endpoints_source_px': GROUND[index],
           'alpha_extrema': padded.getchannel('A').getextrema(),
           'validation': 'lossless decoded alpha and all RGB under nonzero alpha identical to source crop'}
    if index in PIPE_CENTRES:
        row['pipe_center_endpoints_uv'] = uv(PIPE_CENTRES[index])
        row['pipe_center_endpoints_source_px'] = PIPE_CENTRES[index]
        row['tiling_note'] = 'Ground endpoints are inset support feet; use flange centre endpoints for end-to-end pipe joins.'
    rows.append(row)
manifest = {'mode': 'built-in image_gen; transparent_background=true',
            'source_dimensions': [im.width, im.height],
            'prompts': json.loads((ROOT / 'art-source/linear-v12-prompts.json').read_text()),
            'endpoint_note': 'Manually estimated contact centres; normalized crop UV with origin at top-left. Intended for proportional rendering, without nonuniform stretching.',
            'sprites': rows}
(ROOT / 'art-source/linear-v12-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
contact = Image.new('RGB', (1350, 800), (35, 43, 43))
draw = ImageDraw.Draw(contact)
for row in rows:
    i = row['index']
    sp = Image.open(ROOT / row['file'])
    sp.thumbnail((425, 350))
    x, y = i % 3 * 450 + (450 - sp.width) // 2, i // 3 * 400 + 8
    contact.paste(sp, (x, y), sp)
    draw.text((i % 3 * 450 + 12, i // 3 * 400 + 378), f"{i} {row['kind']} {row['width']}x{row['height']}", fill='white')
contact.save('/workspace/scratch/00d29d1aab63/linear-v12-contact.jpg')
print(json.dumps(rows, indent=2))
