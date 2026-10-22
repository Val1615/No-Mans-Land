"""Crop generated RGBA sheets only; retain original art, alpha and visible RGB."""
from pathlib import Path
from PIL import Image, ImageDraw
import json, shutil, numpy as np
from scipy.ndimage import label, find_objects, distance_transform_edt
ROOT=Path(__file__).resolve().parent.parent
SOURCE=Path('/workspace/scratch/00d29d1aab63/generated_images')
sets=[('A','exec-fd48145e-6223-4758-a5f2-64c0534eeb34.png',['barCounter','groceryShelf','reception','diagnostic','archiveShelf','examChair']),('B','exec-9ac42996-80fa-4050-bd9c-9cfc1bd079d0.png',['stoneArch','valveManifold','pipeSegment','harbourDesk','messTable','lockers'])]
rows=[]
for group,filename,names in sets:
 original=ROOT/'art-source'/f'service-v10-{group}.png';shutil.copy2(SOURCE/filename,original)
 im=Image.open(original).convert('RGBA');arr=np.array(im);alpha=arr[:,:,3];labels,count=label(alpha>32);components=[]
 for number,slices in enumerate(find_objects(labels),1):
  if slices is not None and np.count_nonzero(labels[slices]==number)>3000:components.append((number,slices))
 assert len(components)==6,(group,len(components))
 components.sort(key=lambda v:(0 if (v[1][0].start+v[1][0].stop)/2<512 else 1,(v[1][1].start+v[1][1].stop)/2))
 seeds=np.zeros(labels.shape,dtype=np.uint8)
 for order,(number,slices) in enumerate(components,1):seeds[labels==number]=order
 _,nearest=distance_transform_edt(seeds==0,return_indices=True);belongs=seeds[nearest[0],nearest[1]]
 for order,(number,slices) in enumerate(components,1):
  index=len(rows);selection=belongs==order;ys,xs=np.where(selection&(alpha>16));x0,y0=max(0,int(xs.min())-4),max(0,int(ys.min())-4);x1,y1=min(im.width,int(xs.max())+5),min(im.height,int(ys.max())+5)
  crop=arr[y0:y1,x0:x1].copy();crop[:,:,3][~selection[y0:y1,x0:x1]]=0
  part=Image.fromarray(crop,'RGBA');padded=Image.new('RGBA',(part.width+8,part.height+8));padded.paste(part,(4,4));output=ROOT/'dist/assets'/f'service-v10-{index}.webp';padded.save(output,'WEBP',lossless=True,exact=True,method=6)
  restored=np.array(Image.open(output).convert('RGBA'));expected=np.array(padded);assert np.array_equal(restored[:,:,3],expected[:,:,3]);visible=expected[:,:,3]>0;assert np.array_equal(restored[:,:,:3][visible],expected[:,:,:3][visible])
  rows.append({'index':index,'kind':names[order-1],'file':str(output.relative_to(ROOT)),'width':padded.width,'height':padded.height,'source':str(original.relative_to(ROOT)),'source_bbox':[x0,y0,x1,y1],'alpha_extrema':padded.getchannel('A').getextrema()})
manifest={'mode':'built-in image_gen; transparent_background=true','prompts':json.loads((ROOT/'art-source/service-v10-prompts.json').read_text()),'sprites':rows}
(ROOT/'art-source/service-v10-manifest.json').write_text(json.dumps(manifest,indent=2))
contact=Image.new('RGB',(1200,500),(37,45,43));draw=ImageDraw.Draw(contact)
for row in rows:
 i=row['index'];sp=Image.open(ROOT/row['file']);sp.thumbnail((185,210));x,y=i%6*200+(200-sp.width)//2,i//6*250+8;contact.paste(sp,(x,y),sp);draw.text((i%6*200+8,i//6*250+232),f"{i} {row['kind']}",fill='white')
contact.save('/workspace/scratch/00d29d1aab63/service-v10-contact.jpg')
print(json.dumps(rows,indent=2))
