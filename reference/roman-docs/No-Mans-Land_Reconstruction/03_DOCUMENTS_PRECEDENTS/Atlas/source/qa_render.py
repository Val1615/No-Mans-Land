from pathlib import Path
import fitz,json
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1];pdf=fitz.open(root/'output/No-Mans-Land_Atlas-Conception_v01.pdf');pages=json.loads((root/'qa/pages.json').read_text())
for i,page in enumerate(pdf):
 pix=page.get_pixmap(matrix=fitz.Matrix(.6,.6),alpha=False);pix.save(root/'qa'/f'final-{i+1:03}.png')
for group in range((len(pdf)+15)//16):
 sheet=Image.new('RGB',(1400,1060),'#dadbd1');d=ImageDraw.Draw(sheet)
 for k in range(16):
  n=group*16+k+1
  if n>len(pdf):break
  im=Image.open(root/'qa'/f'final-{n:03}.png').convert('RGB');im.thumbnail((340,240));x=(k%4)*350;y=(k//4)*265;sheet.paste(im,(x,y));d.text((x+6,y+244),f'page {n}',fill='#173a35')
 sheet.save(root/'qa'/f'final-contact-{group+1}.jpg')
for id in ['SM10','DT01','BA04','AN03']:
 rec=next(p for p in pages if p['title'].startswith(id+'  |') and 'Fonctions' not in p['title']);idx=rec['page']-1
 pdf[idx].get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).save(root/'qa'/f'detail-{id}.png')
 pdf[idx+1].get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).save(root/'qa'/f'fiche-{id}.png')
for city in ['SM','DT','JB','BA','NC','PU','SU']:
 # city sections use the exact city title in the page log.
 from atlas_data import CITIES
 rec=next(p for p in pages if p['title']==CITIES[city]['name']);idx=rec['page']-1
 (root/'plans'/f'ENSEMBLE_{city}.svg').write_text(pdf[idx].get_svg_image())
print(len(pdf),'pages rendered, 7 city overview SVGs exported')
