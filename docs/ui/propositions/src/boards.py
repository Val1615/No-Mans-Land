from PIL import Image, ImageDraw, ImageFont
F = lambda s, b=True: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if b else ''), s)
NAMES = {'A': 'A · Radio de récupération (ambre)', 'B': 'B · Carnet de route (papier, encre)', 'C': 'C · Diégétique minimal (transparent)'}
NOTE = {'A': 'Terminal de récupérateur : mono ambre, trames, cadres fins semi-transparents.',
        'B': "Carnet tenu par le joueur : papier usé translucide, encre, annotations à la main.",
        'C': "Presque rien : texte sur ombre portée, dégradés bas et droite, aucun cadre."}
OUT = '/workspace/nml/docs/ui/propositions/'
def board(D):
    W = Image.new('RGB', (2*1280 + 3*40 + 2*390 + 40, 70 + 2*800 + 3*30), '#16120f'); d = ImageDraw.Draw(W)
    d.text((40, 18), NAMES[D], fill='#f2c14e', font=F(30)); d.text((900, 26), NOTE[D], fill='#d8ccb4', font=F(20, False))
    cap = lambda t, x, y: d.text((x, y - 24), t, fill='#bba98a', font=F(16, False))
    for i, (f, t) in enumerate([('dlg', 'Bureau 1280x800 · HUD + dialogue (Le Passage)'), ('inv', 'Bureau · sac et troc (rue de La Pompe)')]):
        x, y = 40, 90 + i*(800+30); W.paste(Image.open(f'{D}_desk_{f}.png'), (x, y)); cap(t, x, y)
    x0 = 40 + 1280 + 40
    W.paste(Image.open(f'{D}_desk_mini.png').resize((640, 400)), (x0, 90)); cap('Option « interface minimale » (touche H)', x0, 90)
    for i, f in enumerate(['dlg', 'inv']):
        x = x0 + 680 + i*0  # placeholders
    for i, f in enumerate(['dlg', 'inv']):
        im = Image.open(f'{D}_mob_{f}.png').resize((390, 844)); x = x0 + i*(390 + 40); y = 90 + 400 + 70
        W.paste(im, (x, y)); cap('Mobile 390x844 · ' + ('dialogue' if f == 'dlg' else 'sac / troc'), x, y)
    W = W.crop((0, 0, max(x0 + 2*430, x0 + 680), W.size[1]))
    W.save(OUT + f'direction-{D}.png'); return W
bs = [board(D) for D in 'ABC']
# comparatif : même écran (dialogue bureau) + mobile dialogue, côte à côte
C = Image.new('RGB', (3*(640+390+30) + 40, 90 + 844 + 90), '#16120f'); d = ImageDraw.Draw(C)
d.text((40, 20), 'Comparatif : mêmes scènes (bureau à 50 % : dialogue puis sac et troc ; mobile 390x844 : dialogue)', fill='#f2c14e', font=F(26))
for i, D in enumerate('ABC'):
    x = 40 + i*(640+390+30); d.text((x, 62), NAMES[D], fill='#e6d8bc', font=F(19))
    C.paste(Image.open(f'{D}_desk_dlg.png').resize((640, 400)), (x, 100)); C.paste(Image.open(f'{D}_desk_inv.png').resize((640, 400)), (x, 100 + 420))
    C.paste(Image.open(f'{D}_mob_dlg.png').resize((390, 844)), (x + 640 + 10, 100 - 0))
C.save(OUT + 'comparatif.png'); print('ok')
