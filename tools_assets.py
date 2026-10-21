# Pipeline d'assets v3 (reproductible). Sources jamais modifiées : on lit, on écrit dans game/assets/.
import numpy as np, json
from PIL import Image
S='/workspace/nml/src/a/No-Mans-Land_Reconstruction/07_MAQUETTE_ARCHIVE_v0.13/art-source/'
G='/cursor/stores/store-316802a2-159c-4040-b26c-d4482758b85e/grok-bot/agents/5b481b92-c3dc-4cae-a775-eb657c8f04f3/attachments/'
OUT='/workspace/nml/game/assets/'
# 1) façades redressées (quadrilatère de la vue iso -> rectangle)
F={'cottage_s':('settlement-v9-dusk.png',(65,255),(68,390),(325,478),(325,350),(512,256)),
'cottage_e':('settlement-v9-dusk.png',(330,350),(330,478),(452,400),(450,232),(256,256)),
'palazzo_s':('buildings-v6.png',(50,160),(50,405),(265,488),(265,210),(512,512)),
'palazzo_e':('buildings-v6.png',(265,210),(265,488),(470,390),(470,130),(512,512)),
'ruin_s':('settlement-v9-dusk.png',(1100,635),(1100,850),(1420,940),(1420,695),(512,256)),
'ruin_e':('settlement-v9-dusk.png',(1420,660),(1420,945),(1505,920),(1505,650),(128,256)),
'yellow_s':('buildings-v6.png',(25,635),(25,870),(240,960),(240,680),(512,512)),
'yellow_e':('buildings-v6.png',(240,680),(240,960),(455,870),(455,640),(512,512)),
'shop_s':('settlement-v9-dusk.png',(590,140),(590,450),(782,480),(782,215),(384,512)),
'shop_e':('settlement-v9-dusk.png',(782,215),(782,480),(932,410),(932,130),(320,512)),
'garage_s':('settlement-v9-dusk.png',(1058,140),(1058,395),(1410,510),(1410,325),(640,384))}
cat={}
for k,(f,tl,bl,br,tr,sz) in F.items():
  im=Image.open(S+f).convert('RGBA').transform(sz,Image.QUAD,(*tl,*bl,*br,*tr),Image.BICUBIC)
  bg=Image.new('RGBA',sz,(120,100,80,255)); bg.alpha_composite(im); bg.convert('RGB').save(OUT+'mockup/'+k+'.webp',quality=88)
  cat[k]={'source':f,'quad':[tl,bl,br,tr],'px':sz}
# 2) toits (recadrages) et sols (tuiles terrain-v4 6x4 de 256 px)
R={'roof_tiles':('settlement-v9-dusk.png',(150,170,330,250)),'roof_palazzo':('buildings-v6.png',(170,115,360,175)),
   'roof_ruin':('settlement-v9-dusk.png',(1220,610,1420,690)),'roof_flat':('buildings-v6.png',(250,600,410,650))}
for k,(f,b) in R.items(): Image.open(S+f).convert('RGB').crop(b).resize((256,128)).save(OUT+'mockup/'+k+'.webp',quality=85); cat[k]={'source':f,'crop':b}
# planches 3x2 de tuiles 512 px
T={'g_sand':('terrain-v4.png',0,0),'g_asphalt':('terrain-v4.png',1,0),'g_dirt':('terrain-nature-v4.png',0,0),'g_gravel':('terrain-nature-v4.png',1,0),
   'g_grass':('terrain-nature-v4.png',2,0),'g_concrete':('terrain-nature-v4.png',1,1),'g_stone':('terrain-nature-v4.png',2,1)}
for k,(f,c,r) in T.items(): Image.open(S+f).convert('RGB').crop((c*512,r*512,c*512+512,r*512+512)).resize((384,384)).save(OUT+'mockup/'+k+'.webp',quality=88); cat[k]={'source':f,'tile512':[c,r]}
Image.open(S+'interior-wood-v10.png').convert('RGB').resize((256,256)).save(OUT+'mockup/g_wood.webp',quality=88); cat['g_wood']={'source':'interior-wood-v10.png'}
json.dump(cat,open(OUT+'mockup/catalogue.json','w'),indent=1)
# 3) sprites générés : détourage du fond uni
gen={'gen_mara':('8356fda47aac4d6a9d7a99c706d056886cf34092d4faa7028b52830d4f83ee76.jpg',1.66),
 'gen_vera':('b394c8cbf61fcc492e9850aca3284eecbc48f49b5b94eeae0e25f8f462c74845.jpg',1.68),
 'gen_hector':('81808778394e70b7f6066d70ac5eb432b1570ec4a0336acd3e25a4904fda968d.jpg',1.82),
 'gen_pump':('da92d40565f53b4fd9b4d2cdf2e4c9ae27533c9b9b5242ce8967da2594122244.jpg',1.5)}
man=json.load(open(OUT+'reused/manifest.json'))
for k,(f,h) in gen.items():
  a=np.asarray(Image.open(G+f).convert('RGB')).astype(float)
  key=np.median(np.concatenate([a[:8].reshape(-1,3),a[:, :8].reshape(-1,3),a[:,-8:].reshape(-1,3)]),axis=0)
  d=np.linalg.norm(a-key,axis=2); al=np.clip((d-40)/50,0,1)
  # despill : retire la teinte du fond sur les bords
  sp=(1-al)[...,None]; a=np.clip(a-sp*0.6*(key-a.mean(2,keepdims=True))*0.5,0,255)
  im=Image.fromarray(np.dstack([a,al*255]).astype('uint8'),'RGBA'); im=im.crop(im.getbbox())
  im.thumbnail((512,512),Image.LANCZOS); im.save(OUT+'generated/'+k+'.webp',quality=90)
  fp=[0.6,0.6] if k!='gen_pump' else [0.9,0.9]
  man[k]={'file':'generated/'+k+'.webp','source':'GenerateImage (cursor), '+f,'height_m':h,'px':list(im.size),'footprint_m':fp,'status':'généré, provisoire'}
json.dump(man,open(OUT+'reused/manifest.json','w'),indent=1,ensure_ascii=False)
print('ok',len(cat),len(gen))
# 4) portraits des sprites générés : tête recadrée depuis l'image source (fond remplacé par un brun neutre)
G2={'gen_mara':'8356fda47aac4d6a9d7a99c706d056886cf34092d4faa7028b52830d4f83ee76.jpg','gen_vera':'b394c8cbf61fcc492e9850aca3284eecbc48f49b5b94eeae0e25f8f462c74845.jpg','gen_hector':'81808778394e70b7f6066d70ac5eb432b1570ec4a0336acd3e25a4904fda968d.jpg'}
for k in G2:
  im=Image.open(OUT+'generated/'+k+'.webp').convert('RGBA'); w,h=im.size; s=int(w*0.62)
  cx=w//2; box=(max(0,cx-s//2),0,max(0,cx-s//2)+s,s)
  bg=Image.new('RGBA',(s,s),(58,44,32,255)); bg.alpha_composite(im.crop(box)); bg.convert('RGB').resize((192,192)).save(OUT+'generated/portrait-'+k+'.webp',quality=88)
