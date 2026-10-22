"""Extract already generated sprites; preserve RGBA, separate adjacent alpha silhouettes."""
from pathlib import Path
from PIL import Image, ImageDraw
import json, shutil, numpy as np
from scipy.ndimage import label, find_objects, distance_transform_edt

ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path('/workspace/scratch/00d29d1aab63/generated_images')
SETS = [
    ('props-v9', 'domestic', 'exec-be37ef18-dcc2-4a16-95f5-bc05f7fcae0d.png', ['clothesline','linenCart','firewood','cookstove','fountainRuined','gardenboxes']),
    ('props-v9', 'salvage', 'exec-7637948a-8a40-42f7-9850-5010c65cbd91.png', ['hullplate','netrack','capstan','rubble','sandbag','rail']),
    ('props-v9', 'urban', 'exec-02bfbec1-3f03-48d1-a53d-e9e8a8846ccf.png', ['fountain','balustrade','advert','sortingbins','electrical','sculpture']),
    ('props-v9', 'natural', 'exec-e0cd0c05-6c64-40e9-b6a9-33384b11ecf8.png', ['rock','scrub','tyre','pallet','cablecoil','buoy']),
    ('settlement-v9', 'dusk', 'exec-6763930d-f5b7-47bb-ade4-2c939b7e8e55.png', ['house','shop','inn','workshop','stairhouse','abandoned']),
    ('settlement-v9', 'city', 'exec-abb60b96-d6bf-40dc-9a61-8e91e4999f5d.png', ['apartment','shoprow','neoncorner','substation','offices','serviceblock']),
    ('settlement-v9', 'upper', 'exec-6b751d37-1bee-4920-aac4-c08f68a1047a.png', ['conservatory','residence','gallery','tower','atrium','villa']),
]
rows = {'props-v9': [], 'settlement-v9': []}
for prefix, group, filename, names in SETS:
    original = ROOT / 'art-source' / f'{prefix}-{group}.png'
    shutil.copy2(SOURCE / filename, original)
    im = Image.open(original).convert('RGBA')
    arr = np.array(im)
    alpha = arr[:, :, 3]
    labels, count = label(alpha > 32)
    components = []
    for number, slices in enumerate(find_objects(labels), 1):
        if slices is not None and np.count_nonzero(labels[slices] == number) > 3000:
            components.append((number, slices))
    assert len(components) == 6, (group, len(components))
    # Reading order is based on silhouette centre, not crop-cell edges.
    components.sort(key=lambda v: (0 if (v[1][0].start+v[1][0].stop)/2 < 512 else 1, (v[1][1].start+v[1][1].stop)/2))
    seeds = np.zeros(labels.shape, dtype=np.uint8)
    for order, (number, slices) in enumerate(components, 1):
        seeds[labels == number] = order
    _, nearest = distance_transform_edt(seeds == 0, return_indices=True)
    belongs_to = seeds[nearest[0], nearest[1]]
    for order, (number, slices) in enumerate(components, 1):
        index = len(rows[prefix])
        selection = belongs_to == order
        ys, xs = np.where(selection & (alpha > 16))
        x0, y0 = max(0, int(xs.min())-4), max(0, int(ys.min())-4)
        x1, y1 = min(im.width, int(xs.max())+5), min(im.height, int(ys.max())+5)
        crop = arr[y0:y1, x0:x1].copy()
        crop[:, :, 3][~selection[y0:y1, x0:x1]] = 0
        part = Image.fromarray(crop, 'RGBA')
        padded = Image.new('RGBA', (part.width+8, part.height+8))
        padded.paste(part, (4, 4))
        output = ROOT / 'dist/assets' / f'{prefix}-{index}.webp'
        padded.save(output, 'WEBP', lossless=True, exact=True, method=6)
        restored = np.array(Image.open(output).convert('RGBA'))
        expected = np.array(padded)
        assert np.array_equal(restored[:, :, 3], expected[:, :, 3]), output
        visible = expected[:, :, 3] > 0
        assert np.array_equal(restored[:, :, :3][visible], expected[:, :, :3][visible]), output
        rows[prefix].append({'index': index, 'kind': names[order-1], 'file': str(output.relative_to(ROOT)), 'width': padded.width, 'height': padded.height, 'source_bbox': [x0,y0,x1,y1], 'alpha_extrema': padded.getchannel('A').getextrema()})
        print(prefix, index, names[order-1], padded.size, flush=True)

for prefix, manifest in rows.items():
    (ROOT / 'art-source' / f'{prefix}-manifest.json').write_text(json.dumps(manifest, indent=2))
    contact = Image.new('RGB', (1200, ((len(manifest)+5)//6)*237), (44,50,48))
    draw = ImageDraw.Draw(contact)
    for row in manifest:
        index = row['index']
        sprite = Image.open(ROOT / row['file'])
        sprite.thumbnail((185,195))
        x, y = (index%6)*200+(200-sprite.width)//2, (index//6)*237+15
        contact.paste(sprite, (x,y), sprite)
        draw.text(((index%6)*200+8,(index//6)*237+218), f"{index} {row['kind']}", fill='white')
    contact.save(f'/workspace/scratch/00d29d1aab63/{prefix}-contact.jpg')
