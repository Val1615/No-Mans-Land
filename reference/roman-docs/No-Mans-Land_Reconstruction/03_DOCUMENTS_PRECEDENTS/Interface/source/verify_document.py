from pathlib import Path
import json,fitz
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/'output/No-Mans-Land_Interface-et-Mode-Developpeur_v01.pdf'
doc=fitz.open(PDF);qa=ROOT/'qa';(qa/'pages').mkdir(exist_ok=True)
for old in list((qa/'pages').glob('page-*.png'))+list(qa.glob('contact-*.jpg')):old.unlink()
issues=[];rows=[];wide=[]
for i,page in enumerate(doc):
    text=page.get_text();w,h=page.rect.width,page.rect.height
    if w>h:wide.append(i+1)
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for sp in line['spans']:
                x0,y0,x1,y1=sp['bbox']
                if x0<20 or x1>w-20 or y0<15 or y1>h-17:issues.append({'page':i+1,'text':sp['text'],'bbox':sp['bbox']})
    if not text.strip():issues.append({'page':i+1,'error':'blank'})
    page.get_pixmap(matrix=fitz.Matrix(.95,.95),alpha=False).save(qa/'pages'/f'page-{i+1:03d}.png')
    rows.append({'page':i+1,'words':len(text.split()),'size':[round(w),round(h)],'text':text})
for start in range(0,len(doc),9):
    cw,ch=286,400;canvas=Image.new('RGB',(cw*3,ch*3),'#DDE3E3');draw=ImageDraw.Draw(canvas)
    for j,i in enumerate(range(start,min(start+9,len(doc)))):
        im=Image.open(qa/'pages'/f'page-{i+1:03d}.png');im.thumbnail((264,365),Image.Resampling.LANCZOS)
        x=(j%3)*cw+11;y=(j//3)*ch+9;canvas.paste(im,(x,y));draw.text((x,y+371),f'{i+1:03d}',fill='#152127')
    canvas.save(qa/f'contact-{start//9+1:02d}.jpg',quality=91)
index=json.loads((qa/'page_index.json').read_text())
missing=[f'M{i:02d}' for i in range(1,11) if f'M{i:02d}' not in index]
report={'pages':len(doc),'MiB':round(PDF.stat().st_size/1048576,2),'bookmarks':len(doc.get_toc()),'visual_pages':wide,'missing_visuals':missing,'bounds_issues':issues,'last_pages':[(r['page'],r['words']) for r in rows[-12:]]}
(qa/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
(qa/'pages.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
assert not issues and not missing and len(wide)==10
