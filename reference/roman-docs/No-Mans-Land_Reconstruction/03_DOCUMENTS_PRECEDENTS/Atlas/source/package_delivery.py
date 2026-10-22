from pathlib import Path
import json,csv,zipfile,sys
import fitz
import xml.etree.ElementTree as ET
from atlas_data import *
from audit import intersections
out=ROOT/'output';pdf=out/'No-Mans-Land_Atlas-Conception_v01.pdf';pages=json.loads((ROOT/'qa/pages.json').read_text())
assert len(PLANS)==44 and len(list((ROOT/'plans').glob('*.svg')))==51
assert not [(q['id'],i) for q in PLANS for i in intersections(q)]
for f in (ROOT/'plans').glob('*.svg'):ET.parse(f)
doc=fitz.open(pdf);assert len(doc)==104
bad=[]
for i,p in enumerate(doc):
 for word in p.get_text('words'):
  x0,y0,x1,y1,*_=word
  if x0<0 or y0<0 or x1>p.rect.width+1 or y1>p.rect.height+1:bad.append((i+1,word))
assert not bad,bad[:5]
with (out/'INDEX-PLANS.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['id','ville','quartier','page_plan','page_fiche','fichier_svg'])
 for q in PLANS:
  rec=next(p for p in pages if p['title']==q['id']+'  |  '+q['name']);w.writerow([q['id'],CITIES[q['city']]['name'],q['name'],rec['page'],rec['page']+1,q['id']+'.svg'])
p=out/'LIRE-MOI.txt';s=p.read_text().replace('- 44 plans vectoriels SVG : 37 secteurs urbains et 7 sites isolés.', '- 44 plans locaux SVG : 37 secteurs urbains et 7 sites isolés.\n- 7 schémas d’ensemble SVG : soit 51 planches vectorielles au total.').replace('- 4 fichiers CSV à séparateur point-virgule', '- Un index CSV des plans et pages du PDF, plus 4 fichiers CSV à séparateur point-virgule');p.write_text(s)
(out/'CONTROLES.txt').write_text('Validation du dossier v0.1\n104 pages PDF rendues et contrôlées visuellement.\n51 SVG valides.\n351 emprises bâties vérifiées.\nAucun chevauchement des volumes bâtis ; aucune traversée de bâtiment par un corridor de voie au sol ; seuils hors des autres volumes et de l’eau.\nLes voies élevées occupent un autre niveau, signalé.\nCe contrôle de composition ne remplace pas un test d’avatar après volumétrie.\nAucun fichier du jeu modifié.\n')
archive=out/'No-Mans-Land_Plans-et-Concepts_v01.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 prefix='No-Mans-Land_Conception-v01/'
 for p in out.iterdir():
  if p.suffix!='.zip':z.write(p,prefix+p.name)
 for folder in ['plans','concepts']:
  for p in (ROOT/folder).iterdir():z.write(p,prefix+folder+'/'+p.name)
 for id,name in [('SM10','China-Lake'),('DT01','Dusk-Town'),('BA04','Ateliers-Buenos-Aires'),('AN03','Titan')]:z.write(ROOT/'qa'/f'detail-{id}.png',prefix+f'apercus/{name}.png')
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(json.dumps({'pdf':str(pdf),'pdf_bytes':pdf.stat().st_size,'zip':str(archive),'zip_bytes':archive.stat().st_size,'pages':len(doc),'svg':51,'entries':len(z.namelist())}))
