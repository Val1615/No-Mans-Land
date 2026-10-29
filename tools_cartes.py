# Cartes du chantier interface (docs/design/INTERFACE.md §4, branche docs/regie-interface 8e70070) : fonds dessinés, sans texte ni icône.
# NML : relief recalé sur la grille 22 x 20 de la maquette v0.13 (dist/world.js : CONTINENT, cellBiome, WORLD_GRID size 50), à 100 px par case.
# Steel : 4 planches de couche 1600 x 1200, même cadrage (contour du sarcophage identique), Upper-Town désaturée.
# Dessin déterministe (graine 2175) : la géographie reste exacte, aucune génération d image. Écrit assets/ui/maps/ et assets/ui/maps/manifest.json.
import json, math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = HERE + '/assets/ui/maps/'
CONTINENT = [[72,38],[1035,38],[1032,75],[981,112],[916,119],[868,158],[873,198],[929,219],[994,247],[970,293],[914,321],[857,351],[832,385],[861,414],[839,444],[798,465],[786,505],[811,535],[803,570],[754,592],[773,625],[812,645],[803,678],[842,700],[827,739],[817,778],[825,808],[849,831],[839,869],[883,886],[934,913],[962,942],[923,969],[864,953],[809,930],[764,897],[723,862],[674,822],[630,781],[597,735],[550,698],[511,652],[479,610],[450,562],[406,520],[365,472],[315,472],[265,450],[260,410],[275,390],[275,343],[250,301],[219,275],[190,239],[165,206],[137,171],[112,132],[90,91]]
LIEUX = {'farm': ('Granja Altruista', 234, 143), 'dusk': ('Dusk-Town', 367, 180), 'crater': ('Zone de Big Larry', 464, 108), 'buenos': ('Buenos Aires', 715, 184),
         'customs': ('Douane ouest', 499, 268), 'steel': ('Steel-Megalopolis', 622, 290), 'titan': ('Le Titan échoué', 580, 238), 'junk': ('Junk-Burgh', 879, 271),
         'relay': ('Station de répartition', 478, 426), 'temple': ('Le temple du couchant', 302, 432), 'port': ('Nœud maritime IO', 740, 442),
         'nova': ('Novo Córdoba', 568, 621), 'coast': ('Waste Coast', 762, 749)}  # maquette dist/data.js (x, y en unités maquette, 50 par case) ; 'under' (602, 333) est un niveau de Steel
def inside(x, y):
    hit = False; n = len(CONTINENT)
    for i in range(n):
        a, b = CONTINENT[i], CONTINENT[i - 1]
        if (a[1] > y) != (b[1] > y) and x < (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]) + a[0]: hit = not hit
    return hit
def cell_of(x, y): return int(x // 50), int(y // 50)
def is_land(c, r): return inside(c * 50 + 25, r * 50 + 25) or any(cell_of(x, y) == (c, r) for _, x, y in LIEUX.values())
def biome(x, y):  # cellBiome de la maquette, sur des coordonnées continues
    if math.hypot(x - 464, y - 108) < 95: return 'glass'
    if x < 355 and 325 < y < 495: return 'forest'
    if abs(x - (y * .83 + 15)) < 40 and y > 270: return 'rock'
    if (x > 735 and y > 650) or (not inside(x + 42, y) and x > 760): return 'coast'
    return 'desert'
def noise(h, w, scales, seed):
    rng = np.random.default_rng(seed); out = np.zeros((h, w))
    for s, a in scales:
        g = rng.random((h // s + 2, w // s + 2)); out += a * np.asarray(Image.fromarray((g * 255).astype('uint8')).resize((w + 2 * s, h + 2 * s), Image.BICUBIC))[s:s + h, s:s + w] / 255
    return out / sum(a for _, a in scales)
# ---------------- NML ----------------
BCOL = {'desert': (104, 78, 46), 'rock': (86, 74, 58), 'forest': (56, 58, 38), 'glass': (60, 56, 50), 'coast': (78, 68, 52)}
def carte_nml(S=2):
    W, H = 1100 * S, 1000 * S; ss = 2; Wb, Hb = W * ss, H * ss
    # champ de biomes (résolution 1/4 puis lissé), terre / mer
    q = 4; bw, bh = W // q, H // q; field = np.zeros((bh, bw, 3)); land = np.zeros((bh, bw))
    for j in range(bh):
        for i in range(bw):
            x, y = (i + .5) * q / S, (j + .5) * q / S; field[j, i] = BCOL[biome(x, y)]
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([(x * S, y * S) for x, y in CONTINENT], fill=255)
    fieldI = Image.fromarray(field.astype('uint8')).resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(18 * S / 2))
    f = np.asarray(fieldI).astype(float); n1 = noise(H, W, [(64, 1), (16, .6), (4, .35)], 1)[..., None]; f = f * (0.78 + 0.42 * n1)
    sea = np.array([22, 19, 15.]) * (0.85 + 0.3 * noise(H, W, [(128, 1), (32, .5)], 2))[..., None]
    lm = np.asarray(m.filter(ImageFilter.GaussianBlur(1.5))).astype(float)[..., None] / 255
    # bande côtière : terre assombrie au bord, haut-fond plus clair côté mer
    from scipy import ndimage
    dl = ndimage.distance_transform_edt(np.asarray(m) > 0); ds = ndimage.distance_transform_edt(np.asarray(m) == 0)
    f = f * (0.72 + 0.28 * np.clip(dl / (14 * S), 0, 1))[..., None]
    sea = sea + (np.exp(-ds / (9 * S)) * 22)[..., None] * np.array([1, .85, .6])
    img = f * lm + sea * (1 - lm)
    im = Image.fromarray(np.clip(img, 0, 255).astype('uint8'))
    d = ImageDraw.Draw(im, 'RGBA'); rnd = random.Random(2175); P = lambda x, y: (x * S, y * S)
    # zone sèche du nord (map.py) et taches de végétation basse
    # canaux et lits asséchés (map.py), pistes (map.py, pointillés : terrain « piste »)
    def curve(pts, col, w, dash=None):
        for a, b in zip(pts, pts[1:]):
            if dash:
                L = math.dist(a, b); k = int(L / (dash[0] + dash[1]))
                for t in range(k + 1):
                    t0 = t * (dash[0] + dash[1]) / max(L, 1); t1 = min(1, t0 + dash[0] / max(L, 1))
                    if t0 < 1: d.line([P(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), P(a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], fill=col, width=w)
            else: d.line([P(*a), P(*b)], fill=col, width=w)
    def qbez(p0, p1, p2, n=24): return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in np.linspace(0, 1, n)]
    for seg in [qbez((180, 160), (400, 80), (510, 210)), qbez((510, 210), (620, 340), (720, 390)), qbez((720, 390), (620, 520), (740, 610)), qbez((740, 610), (860, 700), (780, 790)), qbez((780, 790), (700, 870), (880, 915)),
                qbez((280, 260), (390, 320), (600, 290)), qbez((600, 290), (810, 260), (880, 200)), qbez((350, 390), (570, 340), (740, 442)), qbez((500, 575), (680, 510), (785, 520))]:
        curve(seg, (52, 40, 26, 150), 3 * S)  # lits asséchés, sombres
    for path in [[(234, 143), (367, 180), (499, 268), (622, 290), (879, 271)], [(367, 180), (464, 108), (715, 184), (622, 290), (740, 442), (762, 749)],
                 [(499, 268), (478, 426), (302, 432)], [(478, 426), (568, 621), (762, 749), (907, 924)], [(580, 238), (622, 290), (602, 333), (478, 426)]]:
        curve(path, (200, 160, 100, 120), 2 * S, dash=(6, 5))
    # cordillère : chaîne de crêtes (map.py, 65 sommets), ombrée au sud-est
    for i in range(150):  # crêtes plus petites et serrées, éclairées au nord-ouest
        t = i / 149; x = 240 + t * 615 + rnd.uniform(-22, 18); y = 280 + t * 650 + rnd.uniform(-10, 10); w = rnd.uniform(7, 14); h = rnd.uniform(9, 18)
        if not inside(x, y) or not inside(x, y - h): continue
        d.polygon([P(x - w, y + 5), P(x, y - h), P(x + w, y + 5)], fill=(92, 78, 58, 210)); d.polygon([P(x, y - h), P(x + w, y + 5), P(x + 1, y + 5)], fill=(44, 36, 27, 220))
        d.line([P(x - w, y + 5), P(x, y - h)], fill=(168, 138, 92, 150), width=S)
    # forêt occidentale : bosquets
    for i in range(700):
        x, y = rnd.gauss(305, 26), rnd.gauss(410, 40)
        if inside(x, y) and biome(x, y) == 'forest' and abs(x - (y * .83 + 15)) > 30: r = rnd.uniform(2.5, 5); d.ellipse([P(x - r, y - r), P(x + r, y + r)], fill=(38, 42, 24, 190), outline=(84, 84, 50, 120))
    # Big Larry : cratère, retombées vitrifiées hachurées
    for r, a in [(85, 40), (56, 90)]: d.ellipse([P(464 - r, 108 - r), P(464 + r, 108 + r)], outline=(150, 120, 80, a), width=2 * S)
    for k in range(-56, 57, 6):
        h2 = math.sqrt(max(0, 56 ** 2 - (k / math.sqrt(2)) ** 2)) / math.sqrt(2); c0 = (464 + k / 2, 108 + k / 2)
        d.line([P(c0[0] - h2, c0[1] + h2), P(c0[0] + h2, c0[1] - h2)], fill=(30, 28, 24, 80), width=S)
    d.ellipse([P(439, 83), P(489, 133)], fill=(34, 32, 27, 255), outline=(160, 130, 85, 200), width=2 * S)
    # dunes du désert : petites virgules (map.py, 1500 traits)
    for i in range(1500):
        x, y = rnd.randint(80, 1000), rnd.randint(45, 965)
        if inside(x, y) and biome(x, y) == 'desert': d.line([P(x, y), P(x + 2, y - 1), P(x + 5, y)], fill=rnd.choice([(170, 130, 78, 70), (60, 44, 26, 70)]), width=S)
    # sarcophage de Steel-Megalopolis : masse noire (relief, pas une icône)
    d.ellipse([P(622 - 30, 290 - 26), P(622 + 30, 290 + 26)], fill=(18, 16, 13, 255), outline=(140, 110, 70, 200), width=2 * S)
    d.ellipse([P(622 - 38, 290 - 33), P(622 + 38, 290 + 33)], outline=(120, 95, 60, 70), width=S)
    # contour côtier
    d.line([P(x, y) for x, y in CONTINENT + [CONTINENT[0]]], fill=(170, 135, 85, 120), width=2 * S)
    # grain papier, vignette
    a = np.asarray(im.convert('RGB')).astype(float); g = noise(H, W, [(2, 1)], 3)[..., None]; a = a * (0.93 + 0.12 * g)
    yy, xx = np.mgrid[:H, :W]; v = 1 - 0.25 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) ** 1.5; a = a * np.clip(v, 0.6, 1)[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype('uint8'))
    im.save(OUT + 'nml_fond.webp', quality=90); im.resize((W // 2, H // 2), Image.LANCZOS).save(OUT + 'nml_fond_mobile.webp', quality=72)
    cells = [{'col': c, 'row': r, 'label': chr(65 + c) + '%02d' % (r + 1), 'biome': biome(c * 50 + 25, r * 50 + 25)} for r in range(20) for c in range(22) if is_land(c, r)]
    lieux = {k: {'nom': n, 'case': list(cell_of(x, y)), 'px': [x * S, y * S]} for k, (n, x, y) in LIEUX.items()}
    return {'px': [W, H], 'mobile': {'fichier': 'ui/maps/nml_fond_mobile.webp', 'px': [W // 2, H // 2]}, 'grille': {'cols': 22, 'rows': 20, 'case_px': 50 * S,
            'px_vers_case': 'col = floor(x / %d), row = floor(y / %d)' % (50 * S, 50 * S), 'case_vers_px': 'coin = (col * %d, row * %d), centre = coin + %d' % (50 * S, 50 * S, 25 * S),
            'unites_maquette': 'px = unités maquette v0.13 x %d (dist/world.js, 50 unités par case)' % S}, 'cases_terrestres': len(cells), 'cases': cells, 'lieux': lieux}
# ---------------- Steel : 4 couches, même cadrage ----------------
# Cadrage commun : sarcophage = ellipse centre (800, 610), demi-axes 700 x 500 (vue de dessus). Positions des quartiers [proposition, voir CARTES.md],
# déduites des jonctions du code (src/data, lecture seule) : douane à l ouest (c_ouest), Center-Town au centre (c_est -> Lower-Town),
# Lower-Town à l est, Asia-Ground au sud de Lower-Town (INTERFACE.md), China Lake au sud d Asia-Ground (k_nord -> a_sud) relié à Lower-Town
# par une ruelle (k_est -> l_sud_est) ; Sous-Ville : Les Poutres sous la douane (trappe r_trappe), La Cuve à l est, monte-charge vers Center-Town (c_sud).
SW, SH, CX, CY, RX, RY = 1600, 1200, 800, 610, 700, 500
ZONES = {
 'sous_ville': {'sv_poutres': [400, 760], 'sv_cuve': [700, 800], 'sv_trappe': [250, 690], 'sv_monte_charge': [760, 700], 'sv_sortie_sud': [620, 1080], 'sv_sortie_ouest': [130, 820]},
 'lower_town': {'steel_lower': [1130, 470], 'steel_asia': [1130, 760], 'steel_china': [880, 960], 'lac_lower_street': [1220, 260], 'lt_descente': [960, 520], 'lt_acces_sous_ville': [1000, 880]},
 'center_town': {'steel_center': [720, 560], 'steel_route': [130, 600], 'arcadius_center': [720, 470], 'cz_rotonde': [610, 640], 'ct_monte_charge': [760, 700], 'ct_descente': [960, 520], 'ct_ascenseur_upper': [800, 560]},
 'upper_town': {'ut_ascenseur': [800, 560]}}
def _base(seed, tone=(30, 24, 16)):
    a = np.ones((SH, SW, 3)) * np.array(tone, float); n = noise(SH, SW, [(96, 1), (24, .5), (3, .3)], seed)[..., None]; a = a * (0.8 + 0.4 * n)
    yy, xx = np.mgrid[:SH, :SW]; e = ((xx - CX) / RX) ** 2 + ((yy - CY) / RY) ** 2
    a = a * np.where(e <= 1, 1.25, 0.55)[..., None]  # intérieur du dôme plus clair, extérieur sombre (désert de nuit)
    return Image.fromarray(np.clip(a, 0, 255).astype('uint8'))
def _dome(d, col=(170, 130, 78)):
    d.ellipse([CX - RX, CY - RY, CX + RX, CY + RY], outline=col + (200,), width=4); d.ellipse([CX - RX + 14, CY - RY + 12, CX + RX - 14, CY + RY - 12], outline=col + (70,), width=2)
    for k in range(48):  # nervures du sarcophage
        t = 2 * math.pi * k / 48; d.line([(CX + (RX - 14) * math.cos(t), CY + (RY - 12) * math.sin(t)), (CX + RX * math.cos(t), CY + RY * math.sin(t))], fill=col + (90,), width=2)
def _fill(d, rnd, col, skip=None, n=260):  # tissu urbain discret sur tout le dôme (lisible derrière icônes)
    for k in range(-8, 9): d.line([(CX + k * 80, 120), (CX + k * 80, 1100)], fill=col + (22,), width=2); d.line([(100, CY + k * 62), (1500, CY + k * 62)], fill=col + (22,), width=2)
    for i in range(n):
        x, y = rnd.uniform(CX - RX, CX + RX), rnd.uniform(CY - RY, CY + RY)
        if ((x - CX) / (RX - 30)) ** 2 + ((y - CY) / (RY - 30)) ** 2 > 1 or (skip and skip(x, y)): continue
        w, h = rnd.uniform(12, 30), rnd.uniform(8, 20); d.rectangle([x, y, x + w, y + h], fill=col + (38,))
def _blocks(d, cx, cy, r, rnd, col, n=60, sz=(14, 34), street=None):
    for i in range(n):
        a = rnd.uniform(0, 2 * math.pi); rr = r * math.sqrt(rnd.random()); x, y = cx + rr * math.cos(a), cy + rr * .8 * math.sin(a); w, h = rnd.uniform(*sz), rnd.uniform(*sz) * .7
        d.rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], fill=col + (150,), outline=(col[0] + 40, col[1] + 32, col[2] + 20, 120))
def _blob(d, cx, cy, rx, ry, rnd, fill, outline=None, n=24):
    pts = [(cx + rx * (0.85 + 0.15 * rnd.random()) * math.cos(2 * math.pi * k / n), cy + ry * (0.85 + 0.15 * rnd.random()) * math.sin(2 * math.pi * k / n)) for k in range(n)]
    d.polygon(pts, fill=fill, outline=outline)
PALETTE = 'bleu'  # 'bleu' (retour Valentin 29/10 : Steel en bleu acier, contraste avec le désert ambre) ou 'ambre' (3556d7d)
RAMPE = np.array([[8, 12, 18], [22, 34, 48], [52, 76, 98], [110, 146, 170], [196, 222, 236.]])  # nuit, bleu acier, gris-bleu, cyan froid pâle
def _bleu(a, desat=False):  # luminance -> rampe bleu acier ; les accents chauds (lanternes, feux) gardent une pointe de couleur, atténuée
    L = a.mean(2) / 255; L = np.clip(L * 1.35, 0, 1) ** 0.85; t = L * (len(RAMPE) - 1); i = np.clip(t.astype(int), 0, len(RAMPE) - 2); f = (t - i)[..., None]
    b = RAMPE[i] * (1 - f) + RAMPE[i + 1] * f
    warm = np.clip((a[..., 0] - a[..., 2] - 70) / 80, 0, 1)[..., None] * (a[..., 0:1] > 150)
    b = b * (1 - 0.6 * warm) + a * 0.6 * warm
    if desat: G = b.mean(2, keepdims=True); b = G * 0.75 + b * 0.25 + np.array([0, 3, 8]); b = b * 0.85 + 8
    return b
def _finish(im, seed, desat=False):
    im = im.convert('RGB'); a = np.asarray(im).astype(float) * (0.93 + 0.12 * noise(SH, SW, [(2, 1)], seed)[..., None])
    if PALETTE == 'bleu': return Image.fromarray(np.clip(_bleu(a, desat), 0, 255).astype('uint8'))
    if desat: L = a.mean(2, keepdims=True); a = (L * 0.85 + a * 0.15) * 0.8 + 10
    return Image.fromarray(np.clip(a, 0, 255).astype('uint8'))
def carte_steel():
    out = {}
    # 1 Sous-Ville : machineries (cuves rondes), galeries, feux, routes de sortie vers l extérieur
    rnd = random.Random(1); im = _base(11, (24, 18, 12)); d = ImageDraw.Draw(im, 'RGBA'); _dome(d, (120, 92, 56)); _fill(d, rnd, (120, 92, 56), n=120)
    for i in range(26):
        x, y, r = rnd.uniform(300, 1300), rnd.uniform(300, 950), rnd.uniform(18, 46)
        if ((x - CX) / RX) ** 2 + ((y - CY) / RY) ** 2 < .8: d.ellipse([x - r, y - r, x + r, y + r], fill=(46, 36, 24, 200), outline=(130, 100, 60, 140), width=2); d.ellipse([x - r * .45, y - r * .45, x + r * .45, y + r * .45], outline=(130, 100, 60, 90), width=2)
    gal = [[(250, 690), (400, 760), (700, 800), (760, 700)], [(400, 760), (130, 820)], [(700, 800), (620, 1080)], [(700, 800), (1000, 880), (1200, 760)], [(400, 760), (520, 560), (760, 700)]]
    for g in gal: d.line(g, fill=(18, 13, 8, 255), width=22, joint='curve'); d.line(g, fill=(150, 112, 64, 150), width=3, joint='curve')
    _blocks(d, 400, 760, 90, rnd, (60, 46, 30), 40, (10, 22)); _blocks(d, 700, 800, 80, rnd, (60, 46, 30), 30, (12, 26))
    for i in range(40):  # feux dans les ruelles
        x, y = rnd.uniform(300, 1000), rnd.uniform(650, 950); g = rnd.uniform(6, 14)
        for k in range(6, 0, -1): d.ellipse([x - g * k / 3, y - g * k / 3, x + g * k / 3, y + g * k / 3], fill=(220, 140, 60, 18))
    im = _finish(im, 21); im.save(OUT + 'steel_1_sous_ville.webp', quality=88); out['steel_1_sous_ville'] = im
    # 2 Lower-Town : nuit permanente ; pied de la dalle de Center-Town (piliers), Lower-Town à l est, Asia-Ground au sud, China Lake plus au sud, lac de Lower Street
    rnd = random.Random(2); im = _base(12, (26, 20, 13)); d = ImageDraw.Draw(im, 'RGBA'); _dome(d); _fill(d, rnd, (150, 115, 70), skip=lambda x, y: ((x - 720) / 260) ** 2 + ((y - 560) / 210) ** 2 < 1)
    d.ellipse([720 - 250, 560 - 200, 720 + 250, 560 + 200], fill=(14, 11, 8, 220), outline=(120, 95, 60, 160), width=3)  # ombre de la dalle
    for k in range(12): t = 2 * math.pi * k / 12; x, y = 720 + 190 * math.cos(t), 560 + 150 * math.sin(t); d.rectangle([x - 8, y - 8, x + 8, y + 8], fill=(90, 72, 48, 220))
    streets = [[(960, 520), (1130, 470), (1350, 420)], [(1130, 470), (1130, 760), (1100, 1000)], [(1130, 760), (1350, 760)], [(1130, 470), (1220, 260)], [(1350, 700), (1150, 880), (1020, 960), (880, 960)], [(880, 960), (640, 1000)], [(960, 520), (1000, 880)]]
    for g in streets: d.line(g, fill=(70, 54, 34, 255), width=16, joint='curve'); d.line(g, fill=(160, 120, 70, 110), width=2, joint='curve')
    _blocks(d, 1130, 470, 150, rnd, (64, 50, 32), 70, (16, 36)); _blocks(d, 1130, 760, 110, rnd, (70, 52, 30), 90, (8, 16))  # Asia-Ground : marché, petites halles
    _blob(d, 1220, 260, 70, 42, rnd, (22, 26, 24, 255), (150, 120, 70, 180))  # lac de Lower Street
    _blocks(d, 880, 960, 120, rnd, (60, 46, 30), 40, (12, 26)); _blob(d, 880, 960, 70, 46, rnd, (20, 24, 22, 255), (200, 160, 100, 200))  # China Lake, lac au centre
    for i in range(14): a = 2 * math.pi * i / 14; x, y = 880 + 80 * math.cos(a), 960 + 54 * math.sin(a); d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(200, 60, 45, 200))  # lanternes
    im = _finish(im, 22); im.save(OUT + 'steel_2_lower_town.webp', quality=88); out['steel_2_lower_town'] = im
    # 3 Center-Town : dalle surélevée au centre, quatre tours Arcadius, Rotonde, douane à l ouest au bout de la route, rampes
    rnd = random.Random(3); im = _base(13, (28, 22, 15)); d = ImageDraw.Draw(im, 'RGBA'); _dome(d); _fill(d, rnd, (110, 85, 52), n=140)
    d.line([(0, 600), (130, 600), (480, 570)], fill=(80, 62, 40, 255), width=26); d.line([(0, 600), (130, 600), (480, 570)], fill=(170, 130, 78, 120), width=2)
    d.rectangle([100, 560, 170, 640], fill=(60, 48, 32, 230), outline=(180, 140, 85, 200), width=2)  # place forte de la douane
    d.ellipse([720 - 250, 560 - 200, 720 + 250, 560 + 200], fill=(62, 50, 34, 240), outline=(200, 155, 95, 220), width=4)  # dalle
    d.line([(960, 520), (1100, 500)], fill=(80, 62, 40, 255), width=18)  # la Descente vers Lower-Town
    _blocks(d, 720, 560, 200, rnd, (84, 66, 44), 80, (14, 30))
    for dx, dy in [(-40, -40), (40, -40), (-40, 30), (40, 30)]: x, y = 720 + dx, 470 + dy; d.rectangle([x - 16, y - 16, x + 16, y + 16], fill=(40, 32, 22, 255), outline=(220, 170, 100, 230), width=3)
    d.ellipse([610 - 28, 640 - 28, 610 + 28, 640 + 28], fill=(48, 38, 26, 255), outline=(200, 155, 95, 200), width=3)  # Rotonde
    im = _finish(im, 23); im.save(OUT + 'steel_3_center_town.webp', quality=88); out['steel_3_center_town'] = im
    # 4 Upper-Town : silhouette, parcs, avenues ; version désaturée (verrouillée)
    rnd = random.Random(4); im = _base(14, (30, 26, 20)); d = ImageDraw.Draw(im, 'RGBA'); _dome(d, (150, 140, 120))
    for k in range(8): t = 2 * math.pi * k / 8; d.line([(800, 560), (800 + 560 * math.cos(t), 610 + 400 * math.sin(t))], fill=(90, 84, 70, 200), width=14)
    for i in range(10): _blob(d, rnd.uniform(400, 1200), rnd.uniform(350, 900), rnd.uniform(40, 80), rnd.uniform(25, 50), rnd, (60, 70, 50, 200))
    _blocks(d, 800, 600, 480, rnd, (90, 84, 70), 160, (16, 40)); d.ellipse([800 - 60, 560 - 45, 800 + 60, 560 + 45], fill=(110, 104, 90, 230), outline=(180, 170, 150, 200), width=3)
    im = _finish(im, 24, desat=True); im.save(OUT + 'steel_4_upper_town.webp', quality=88); out['steel_4_upper_town'] = im
    return out
LAYERS = [('steel_1_sous_ville', 'sous_ville', 1, 'accessible'), ('steel_2_lower_town', 'lower_town', 2, 'accessible'), ('steel_3_center_town', 'center_town', 3, 'accessible'), ('steel_4_upper_town', 'upper_town', 4, 'affichee_verrouillee')]
def manifest(nml):
    m = {'source': 'docs/design/INTERFACE.md §4 (origin/docs/regie-interface 8e70070)', 'outil': 'tools_cartes.py (dessin déterministe)',
         'nml_fond': {'fichier': 'ui/maps/nml_fond.webp', **nml},
         'steel': {'px': [SW, SH], 'sarcophage_ellipse': {'centre': [CX, CY], 'demi_axes': [RX, RY]}, 'couches': [
             {'cle': k, 'fichier': 'ui/maps/%s.webp' % k, 'couche': n, 'id': z, 'statut': st, 'reperes_px_proposition': ZONES[z]} for k, z, n, st in LAYERS],
             'note': 'même cadrage sur les 4 planches ; repères = positions proposées des lieux, sorties et liens entre couches (même x, y d une couche à l autre pour un ascenseur)'},
         'icones_lieux': {k: {'svg': 'ui/maps/icones/%s.svg' % k, 'png24': 'ui/maps/icones/%s_24.png' % k, 'png48': 'ui/maps/icones/%s_48.png' % k}
                          for k in ('lieu_decouvert', 'lieu_non_decouvert', 'joueur', 'sortie', 'lien_couches', 'verrouille')}}
    m['icones_lieux_steel'] = {k + '_steel': {'svg': 'ui/maps/icones/%s_steel.svg' % k, 'png24': 'ui/maps/icones/%s_steel_24.png' % k, 'png48': 'ui/maps/icones/%s_steel_48.png' % k}
                               for k in ('lieu_decouvert', 'lieu_non_decouvert', 'joueur', 'sortie', 'lien_couches', 'verrouille')}  # variante bleue (#a9d2e6) pour la carte Steel
    m['steel']['palette'] = PALETTE
    json.dump(m, open(OUT + 'manifest.json', 'w'), ensure_ascii=False, indent=1)
def chemin(a, b):  # A* 8 directions sans couper les angles marins (comme worldPath), coût uniforme : pour la maquette seulement
    import heapq
    land = {(c, r) for r in range(20) for c in range(22) if is_land(c, r)}; pq = [(0, a)]; prev = {a: None}; cost = {a: 0}
    while pq:
        _, p = heapq.heappop(pq)
        if p == b: break
        for dc in (-1, 0, 1):
            for dr in (-1, 0, 1):
                n = (p[0] + dc, p[1] + dr)
                if n == p or n not in land or (dc and dr and ((p[0] + dc, p[1]) not in land or (p[0], p[1] + dr) not in land)): continue
                c = cost[p] + (1.414 if dc and dr else 1)
                if c < cost.get(n, 1e9): cost[n] = c; prev[n] = p; heapq.heappush(pq, (c + math.dist(n, b), n))
    out = [b]
    while prev[out[-1]]: out.append(prev[out[-1]])
    return out[::-1]
