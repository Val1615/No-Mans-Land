# v7 : captures de documentation (pas un test) : vue d'ensemble de chaque quartier et plan global assemblé en croix.
# Le placement du joueur se fait par commande ici : c'est une prise de vue, les trajets sont couverts par town_pixels.py.
import sys, os, time, io
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765/'; OUT = sys.argv[2] if len(sys.argv) > 2 else '/workspace/nml/docs/captures/dusk-v7/'
os.makedirs(OUT, exist_ok=True)
Q = {'dusk_q1': 'La Pompe', 'dusk_q2': 'Le Transit', 'dusk_q3': 'Le Scellé', 'dusk_q4': 'Les Sables'}
ims = {}
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = br.new_page(viewport={'width': 1280, 'height': 800}); pg.goto(URL); pg.wait_for_function('window.__nml', timeout=60000); (pg.locator('#m-new').tap if pg.evaluate('navigator.maxTouchPoints>0') else pg.locator('#m-new').click)(); pg.wait_for_function('!document.body.classList.contains("menu-open")'); time.sleep(2)
    pg.evaluate("document.getElementById('hud').style.visibility='hidden'; document.getElementById('act').style.visibility='hidden'")
    for i, (loc, name) in enumerate(Q.items()):
        pg.evaluate(f"()=>{{const s=__nml.state; s.location='{loc}'; s.junctionLock='x'; Object.assign(s.player,{{x:24,z:19,path:[]}}); Object.assign(s.companion,{{x:25,z:19.5,path:[],location:'{loc}'}})}}"); time.sleep(1.2)
        pg.evaluate('window.__nml.setCamera({x:24,z:18,ppm:15})'); time.sleep(1.2)
        im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); im.save(OUT + f'quartier-q{i+1}-{name.lower().replace(" ", "-").replace("é", "e")}.png'); ims[loc] = im
        pg.evaluate('window.__nml.setCamera(null)')
    br.close()
# plan en croix : Q3 au nord, Q1 au centre, Q2 à l'est, Q4 au sud (orientation monde : nord = haut-gauche de l'écran isométrique)
w, h = 640, 400; W = Image.new('RGB', (3 * w, 3 * h + 60), '#1d1915'); d = ImageDraw.Draw(W)
try: F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
except Exception: F = ImageFont.load_default()
pos = {'dusk_q3': (1, 0), 'dusk_q1': (1, 1), 'dusk_q2': (2, 1), 'dusk_q4': (1, 2)}
for loc, (c, r) in pos.items():
    W.paste(ims[loc].resize((w, h)), (c * w, 60 + r * h)); d.text((c * w + 14, 60 + r * h + 10), Q[loc], fill='#f2c14e', font=F)
d.text((14, 16), 'Dusk-Town v7 : 4 quartiers reliés à pied (Q3 nord, Q1 centre, Q2 est, Q4 sud). Bords sans voisin = désert.', fill='#f3e6c8', font=F)
for (x0, y0, x1, y1) in [(w * 1.5, 60 + h - 10, w * 1.5, 60 + h + 10), (w * 2 - 10, 60 + h * 1.5, w * 2 + 10, 60 + h * 1.5), (w * 1.5, 60 + 2 * h - 10, w * 1.5, 60 + 2 * h + 10)]:
    d.line([(x0, y0), (x1, y1)], fill='#f2c14e', width=6)
W.save(OUT + 'plan-global.png'); print('ok')
