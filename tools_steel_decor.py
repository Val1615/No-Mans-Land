# v13 Steel : décor (PNJ de foule, soldats, fortifications, échoppes, drones, hologrammes) et sol mouillé de Center-Town.
# Écrit seulement des entrées st_* nouvelles dans assets/reused/manifest.json (existant inchangé) et assets/generated/st_*.webp.
# Les décors sont des sprites debout (billboards) dimensionnés par leur hauteur réelle, comme les props de Dusk-Town.
import json, os, numpy as np
from PIL import Image
from scipy import ndimage
import tools_interiors as TI
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = HERE + '/assets/generated/'; GEN = HERE + '/art-gen/'
SRC = TI.SRC
def comps(sheet):  # composantes d'une planche maquette (fond transparent), triées en lignes puis colonnes
    im = np.array(Image.open(SRC + sheet).convert('RGBA')); a = im[:, :, 3] > 40
    lab, n = ndimage.label(ndimage.binary_dilation(a, iterations=6)); objs = []
    for k, sl in enumerate(ndimage.find_objects(lab)):
        m = (lab[sl] == k + 1) & a[sl]
        if m.sum() >= 4000: objs.append((sl, m))
    objs.sort(key=lambda t: (t[0][0].start // 300, t[0][1].start)); out = []
    for sl, m in objs: sub = im[sl].copy(); sub[~m, 3] = 0; out.append(TI.clean(sub))
    return out
# (id, source, hauteur m, emprise [w, d], rôle)
people = comps('city-people-v3.png'); cprops = comps('city-props-v3.png')
D = [
 *[(f'st_civil{i}', ('arr', people[i]), h, [0.6, 0.6], 'passant / file d attente (maquette city-people-v3)') for i, h in enumerate([1.84, 1.68, 1.72, 1.66, 1.70, 1.82])],
 ('st_mirador', ('gen', 'gen_fort_sheet.jpg', 0), 7.5, [2.4, 2.4], 'mirador (généré)'),
 ('st_tourelle', ('gen', 'gen_fort_sheet.jpg', 1), 2.8, [2.0, 2.0], 'tourelle automatique (généré)'),
 ('st_barricade', ('gen', 'gen_fort_sheet.jpg', 2), 1.9, [3.4, 0.8], 'barricade béton et barbelés (généré)'),
 ('st_projecteur', ('gen', 'gen_fort_sheet.jpg', 3), 6.5, [0.6, 0.6], 'mât de projecteur (généré)'),
 ('st_echoppe', ('gen', 'gen_ct_props.jpg', 0), 2.7, [2.6, 1.4], 'échoppe de rue éclairée (généré)'),
 ('st_drone', ('gen', 'gen_ct_props.jpg', 1), 0.55, [0.6, 0.6], 'drone de surveillance (généré)'),
 ('st_kiosque', ('gen', 'gen_ct_props.jpg', 2), 2.6, [1.4, 1.2], 'kiosque néon (généré)'),
 ('st_holo', ('gen', 'gen_ct_props.jpg', 3), 3.4, [0.4, 0.4], 'panneau holographique (généré)'),
 ('st_borne', ('arr', cprops[0]), 1.9, [0.8, 0.6], 'borne holographique (maquette city-props-v3)'),
 ('st_lampadaire', ('arr', cprops[1]), 4.6, [0.4, 0.4], 'lampadaire néon (maquette city-props-v3)'),
 ('st_voiture', ('arr', cprops[3]), 1.4, [4.4, 2.0], 'voiture (maquette city-props-v3)'),
 ('st_banc', ('arr', cprops[4]), 0.95, [1.8, 0.6], 'banc lumineux (maquette city-props-v3)'),
 ('st_pylone', ('arr', cprops[5]), 2.7, [0.7, 0.7], 'pylône lumineux (maquette city-props-v3)'),
 # v14 Sous-Ville
 ('sv_brasero', ('gen', 'gen_sv_props.jpg', 0), 1.3, [0.8, 0.8], 'fût brasero (généré)'),
 ('sv_linge', ('gen', 'gen_sv_props.jpg', 1), 2.4, [3.0, 0.3], 'corde à linge (généré)'),
 ('sv_tuyau', ('gen', 'gen_sv_props.jpg', 2), 1.8, [4.2, 1.2], 'gros tuyau sur supports (généré)'),
 ('sv_ecrans', ('gen', 'gen_sv_props.jpg', 3), 2.4, [2.6, 1.2], 'mur de télés en neige (généré)'),
 ('sv_panneau', ('gen', 'gen_sv_props2.jpg', 0), 2.0, [0.4, 0.4], 'panneau bricolé (généré)'),
 ('sv_armes', ('gen', 'gen_sv_props2.jpg', 1), 1.1, [1.4, 1.0], 'caisse d armes (généré)'),
 ('sv_pneus', ('gen', 'gen_sv_props2.jpg', 2), 1.0, [2.0, 1.6], 'tas de pneus (généré)'),
 ('sv_implants', ('gen', 'gen_sv_props2.jpg', 3), 1.6, [1.8, 0.9], 'étal d implants volés (généré)'),
]
man = json.load(open(HERE + '/assets/reused/manifest.json')); before = json.dumps({k: v for k, v in man.items() if not k.startswith(('st_', 'sv_'))}, sort_keys=True)
for aid, (kind, *src), h, fp, role in D:
    rgba = src[0] if kind == 'arr' else TI.quad(GEN + src[0], src[1])
    im = Image.fromarray(rgba, 'RGBA'); im.thumbnail((512, 512)); im.save(OUT + aid + '.webp', quality=88)
    man[aid] = {'file': 'generated/' + aid + '.webp', 'height_m': h, 'px': list(im.size), 'footprint_m': fp, 'status': 'v13 Steel : ' + role,
                'src': ('art-gen/' + src[0] + f' #{src[1]}') if kind == 'gen' else 'maquette art-source (planche city-*-v3)'}
    print(aid, im.size)
assert json.dumps({k: v for k, v in man.items() if not k.startswith(('st_', 'sv_'))}, sort_keys=True) == before
json.dump(man, open(HERE + '/assets/reused/manifest.json', 'w'), indent=1, ensure_ascii=False)
# sol mouillé (vue de dessus, tuile) : 1 image = 6 m
Image.open(GEN + 'gen_wet_ground.jpg').convert('RGB').resize((512, 512)).save(OUT + 'g_wet.webp', quality=88)
Image.open(GEN + 'gen_sv_ground.jpg').convert('RGB').resize((512, 512)).save(OUT + 'g_sv.webp', quality=88)  # v14 : sol de la Sous-Ville
