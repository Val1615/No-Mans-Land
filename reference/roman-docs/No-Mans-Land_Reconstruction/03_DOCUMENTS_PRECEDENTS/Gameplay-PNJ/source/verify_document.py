from pathlib import Path
import json,fitz,math
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
pdf=ROOT/'output/No-Mans-Land_Gameplay-et-PNJ_Conception_v01.pdf'
doc=fitz.open(pdf);qa=ROOT/'qa';(qa/'pages').mkdir(exist_ok=True)
issues=[];records=[]
for i,pg in enumerate(doc):
    for block in pg.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for sp in line['spans']:
                x0,y0,x1,y1=sp['bbox']
                if x0<22 or x1>pg.rect.width-22 or y0<17 or y1>pg.rect.height-18:
                    issues.append({'page':i+1,'text':sp['text'],'bbox':sp['bbox']})
    text=pg.get_text()
    if not text.strip():issues.append({'page':i+1,'error':'blank'})
    pg.get_pixmap(matrix=fitz.Matrix(1.12,1.12),alpha=False).save(qa/'pages'/f'page-{i+1:03d}.png')
    records.append({'page':i+1,'words':len(text.split()),'text':text})
for start in range(0,len(doc),9):
    thumbw=250;thumbh=354;cellw=274;cellh=384
    canvas=Image.new('RGB',(cellw*3,cellh*3),'#dfe2e2');draw=ImageDraw.Draw(canvas)
    for j,i in enumerate(range(start,min(start+9,len(doc)))):
        im=Image.open(qa/'pages'/f'page-{i+1:03d}.png');im.thumbnail((thumbw,thumbh),Image.Resampling.LANCZOS)
        x=(j%3)*cellw+12;y=(j//3)*cellh+9;canvas.paste(im,(x,y));draw.text((x,y+thumbh+4),str(i+1),fill='#111111')
    canvas.save(qa/f'contact-{start//9+1:02d}.jpg',quality=91)
names=json.loads((ROOT/'source/audit.json').read_text())['roster']
idx=json.loads((qa/'profile_pages.json').read_text())
missing=[n['id'] for n in names if n['id'] not in idx]
alltext='\n'.join(r['text'] for r in records)
events=['EV SM 0'+str(i) for i in range(1,7)]+['EV DT 01','EV DT 02','EV GR 01','EV GR 02','EV JB 01','EV JB 02','EV JB 03']+['EV BA 0'+str(i) for i in range(1,6)]+['EV RT 01','EV NC 01','EV NC 02','EV PU 01','EV PU 02','EV SU 01','EV SU 02','EV BL 01','EV BL 02','EV TI 01','EV RE 01','EV TE 01','EV IO 01','EV WC 01']
missing_events=[x for x in events if x not in alltext]
report={'pages':len(doc),'bytes':pdf.stat().st_size,'bookmarks':len(doc.get_toc()),'profile_bookmarks':len(idx),'placed_npc_profiles':sum(bool(n['locations']) for n in names),'event_count':len(events),'missing_npcs':missing,'missing_events':missing_events,'bounds_issues':issues}
(qa/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
(qa/'pages.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2));assert not issues and not missing and not missing_events
