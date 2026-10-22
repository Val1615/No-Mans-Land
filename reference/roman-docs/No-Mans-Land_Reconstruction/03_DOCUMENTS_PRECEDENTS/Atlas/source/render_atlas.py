from atlas_data import *
import json,csv,math,html,textwrap,zipfile,os,hashlib
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from audit import intersections

OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont('Atlas','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('AtlasB','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Mono','/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
W,H=1190.55,841.89
BG='#f4f0e6';INK='#203d40';MUTED='#62716b';ACCENT='#a06339';STATUS={'O':('#d9e7dd','#287260','OUVERT'),'C':('#f1e4c5','#aa772c','CONDITIONNEL'),'N':('#d7d8d1','#68716c','FERMÉ'),'R':('#e6d1cc','#984b44','RÉSERVÉ')}
P=ParagraphStyle('normal',fontName='Atlas',fontSize=10.3,leading=15,textColor=HexColor(INK),spaceAfter=7)
SMALL=ParagraphStyle('small',parent=P,fontSize=8.6,leading=12)
BOLD=ParagraphStyle('bold',parent=P,fontName='AtlasB')
PAGELOG=[]

def tx(c,x,y,s,size=10,font='Atlas',color=INK):
 c.setFont(font,size);c.setFillColor(HexColor(color));c.drawString(x,y,str(s))
def para(c,s,x,y,w,style=P):
 p=Paragraph(s,style);_,hh=p.wrap(w,1000);p.drawOn(c,x,y-hh);return y-hh-6

def footer(c,title):
 c.setStrokeColor(HexColor('#c9c9bb'));c.line(35,30,W-35,30);tx(c,36,16,'NO MAN’S LAND  /  ATLAS DE CONCEPTION  /  v0.1',8,'Mono',MUTED);c.setFont('Mono',8);c.drawRightString(W-36,16,f'{title}  |  {c.getPageNumber():03d}')
def page(c,title,kicker,subtitle=''):
 c.setFillColor(HexColor(BG));c.rect(0,0,W,H,fill=1,stroke=0);tx(c,36,H-38,kicker.upper(),9,'Mono',ACCENT);tx(c,36,H-72,title,26,'AtlasB');
 if subtitle:tx(c,37,H-94,subtitle,10,'Atlas',MUTED)
 PAGELOG.append({'page':c.getPageNumber(),'title':title,'kind':kicker})
def end(c,title):footer(c,title);c.showPage()

def door(b,offset=0):
 x,y,w,h=b['x'],b['y'],b['w'],b['h'];f=b['face']
 return {'N':(x+w/2,y-offset),'S':(x+w/2,y+h+offset),'W':(x-offset,y+h/2),'E':(x+w+offset,y+h/2)}[f]
def paths_legend():return 'O : ouvert  /  C : conditionnel  /  N : fermé  /  R : réservé     P : PNJ ou groupe     D : groupe de décors'
def label_lines(s,n):
 return textwrap.wrap(s,n,break_long_words=False,break_on_hyphens=False)

def draw_map(c,q,x,y,scale=8):
 # y is top, local north is up; positions increase towards east and south.
 def pt(p):return (x+p[0]*scale,y-p[1]*scale)
 def line(pts,color,width,dash=None):
  c.saveState();c.setStrokeColor(HexColor(color));c.setLineWidth(width);c.setLineCap(0);c.setLineJoin(1)
  if dash:c.setDash(*dash)
  p=c.beginPath();p.moveTo(*pt(pts[0]))
  for a in pts[1:]:p.lineTo(*pt(a))
  c.drawPath(p);c.restoreState()
 c.setFillColor(HexColor('#e5dfd0' if q['level']=='Extérieur' or 'aride' in q['level'] else '#e4e9e3'));c.rect(x,y-80*scale,100*scale,80*scale,fill=1,stroke=0)
 c.saveState();c.setStrokeColor(HexColor('#bdbba9'));c.setLineWidth(.3)
 for a in range(0,101,10):c.line(x+a*scale,y,x+a*scale,y-80*scale);tx(c,x+a*scale-5,y+7,str(a),7,'Mono',MUTED)
 for a in range(0,81,10):c.line(x,y-a*scale,x+100*scale,y-a*scale);tx(c,x-23,y-a*scale-2,str(a),7,'Mono',MUTED)
 c.restoreState()
 for f in q['features']:
  cols={'eau':'#a8c0bf','canal':'#789b99','impact':'#777e70','foret':'#6c8466','jardin':'#a0b48c','metal':'#969c92'}
  c.setFillColor(HexColor(cols.get(f['kind'],'#bdbba9')));c.setStrokeColor(HexColor('#7d8d7a'));c.setLineWidth(.8);p=c.beginPath();p.moveTo(*pt(f['points'][0]));
  for a in f['points'][1:]:p.lineTo(*pt(a))
  p.close();c.drawPath(p,fill=1,stroke=1)
 for r in q['roads']:
  typ=r['kind'];points=r['points']
  if typ.startswith('rail'):
   # Conventional rail symbol, not new scene furniture.
   line(points,'#544f45',r['w']*scale+1)
   line(points,'#d9d4c1',max(.6,r['w']*scale-2))
   line(points,'#5e5f55',.8,[3,5] if typ=='rail_mort' else [7,3])
   for a,b in zip(points,points[1:]):
    dx,dy=b[0]-a[0],b[1]-a[1];ln=math.hypot(dx,dy)
    for step in range(1,int(ln),3):
     xx,yy=a[0]+dx*step/ln,a[1]+dy*step/ln;ox,oy=-dy/ln*(r['w']*.75),dx/ln*(r['w']*.75);line([(xx-ox,yy-oy),(xx+ox,yy+oy)],'#6d6759',.8)
  elif typ=='pont':line(points,'#507c76',r['w']*scale+2);line(points,'#e3dbc5',r['w']*scale);line(points,'#9b967c',.7,[3,4])
  elif typ=='sureleve':line(points,'#9aaeb6',r['w']*scale);line(points,'#2b5968',1.3,[8,4])
  else:
   line(points,'#9a9e90',r['w']*scale+1.8)
   line(points,'#d7c59c' if typ=='pieton' else '#c1c4b7' if typ=='service' else '#b4afa0',r['w']*scale)
   if typ!='pieton':line(points,'#e6e2ce',.6,[7,6])
  a,b=points[0],points[-1]
  for z in [a,b]:
   if z[0] in (0,100) or z[1] in (0,80):
    xx,yy=pt(z);c.setFillColor(HexColor(INK));c.circle(xx,yy,3,fill=1,stroke=0)
 for b in q['buildings']:
  xx,yy=pt((b['x'],b['y']));bw,bh=b['w']*scale,b['h']*scale;fill,stroke,_=STATUS[b['status']]
  c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke));c.setLineWidth(1.5);
  if b.get('shape')=='cercle':c.ellipse(xx,yy-bh,xx+bw,yy,fill=1,stroke=1)
  elif b.get('shape')=='decroche':
   pp=c.beginPath();pp.moveTo(xx,yy);pp.lineTo(xx+bw*.65,yy);pp.lineTo(xx+bw*.65,yy-bh*.25);pp.lineTo(xx+bw,yy-bh*.25);pp.lineTo(xx+bw,yy-bh);pp.lineTo(xx,yy-bh);pp.close();c.drawPath(pp,fill=1,stroke=1)
  else:c.rect(xx,yy-bh,bw,bh,fill=1,stroke=1)
  # closed blocks and reserved volumes have a roof convention.
  if b['status'] in ('N','R'):
   c.saveState();pp=c.beginPath();pp.rect(xx,yy-bh,bw,bh);c.clipPath(pp,stroke=0);c.setStrokeColor(HexColor('#a7aaa0'));c.setLineWidth(.4)
   for k in range(-int(bh),int(bw),16):c.line(xx+k,yy-bh,xx+k+bh,yy)
   c.restoreState()
  tx(c,xx+5,yy-14,b['id']+' '+b['status'],8,'AtlasB',stroke)
  if bw>95 and bh>58:
   names=label_lines(b['name'],max(11,int(bw/5.6)))[:2]
   for i,t in enumerate(names):tx(c,xx+5,yy-29-i*12,t,8.5,'Atlas',INK)
  if b['status'] in ('O','C'):
   px,py=pt(door(b));c.setStrokeColor(HexColor(BG));c.setLineWidth(3)
   if b['face'] in 'NS':c.line(px-5,py,px+5,py)
   else:c.line(px,py-5,px,py+5)
   dx,dy={'N':(0,1),'S':(0,-1),'W':(-1,0),'E':(1,0)}[b['face']];c.setFillColor(HexColor(stroke));p=c.beginPath();p.moveTo(px,py);p.lineTo(px+dx*9-dy*4,py+dy*9+dx*4);p.lineTo(px+dx*9+dy*4,py+dy*9-dx*4);p.close();c.drawPath(p,fill=1,stroke=0)
 for d in q['decor']:
  xx,yy=pt((d['x'],d['y']));c.saveState();c.setStrokeColor(HexColor('#6e8977'));c.setLineWidth(.7);c.setDash(2,2);c.rect(xx,yy-d['h']*scale,d['w']*scale,d['h']*scale,fill=0,stroke=1);c.restoreState()
  px,py=pt((d['x']+d['w']/2,d['y']+d['h']/2));c.setFillColor(HexColor('#eef0df'));c.roundRect(px-12,py-5.5,24,11,3,fill=1,stroke=0);tx(c,px-10,py-2.7,d['id'],6.5,'Mono','#466650')
 for n in q['npcs']:
  for xx,yy in n.get('members',[(n['x'],n['y'])]):
   px,py=pt((xx,yy));c.setFillColor(HexColor('#a75932'));c.setStrokeColor(HexColor('#fffaf0'));c.setLineWidth(1);c.circle(px,py,3.3,fill=1,stroke=1)
  px,py=pt((n['x'],n['y']));c.setFillColor(HexColor('#fff6e8'));c.roundRect(px+5,py-5.5,25,12,3,fill=1,stroke=0);tx(c,px+7,py-2.5,n['id'],7,'Mono','#994a27')
 # Scale and direction are graphic conventions; exact world scale is not committed.
 tx(c,x+100*scale-18,y+24,'N',11,'AtlasB');c.setStrokeColor(HexColor(INK));c.setLineWidth(1);c.line(x+100*scale-15,y+8,x+100*scale-15,y+19)
 c.setStrokeColor(HexColor('#8d988e'));c.setLineWidth(1);c.rect(x,y-80*scale,100*scale,80*scale,fill=0,stroke=1)

def map_page(c,q):
 page(c,f"{q['id']}  |  {q['name']}",CITIES[q['city']]['name'],q['level']+'  /  PLAN D’IMPLANTATION')
 c.bookmarkPage(q['id']);c.addOutlineEntry(q['id']+' '+q['name'],q['id'],1,False)
 draw_map(c,q,59,H-142,7.5)
 y=H-139;x=850;ww=300
 y=para(c,q['parti'],x,y,ww,BOLD);y=para(c,'<b>Connexions</b><br/>'+q['flux'],x,y-3,ww,SMALL)
 tx(c,x,y-12,'BÂTIMENTS ET ACCÈS',9,'AtlasB',ACCENT);y-=30
 for b in q['buildings']:
  fill,col,st=STATUS[b['status']];tx(c,x,y,b['id'],9,'Mono',col)
  y=para(c,f"<b>{html.escape(b['name'])}</b> <font color='{col}'>[{b['status']}]</font>",x+35,y+8,ww-35,SMALL)-2
 tx(c,x,y-12,'RÉSEAUX DESSINÉS',9,'AtlasB',ACCENT);y-=27
 for r in q['roads']:
  types={'route':'route','piste':'piste','pieton':'piétons','service':'service','sureleve':'voie élevée','pont':'pont','rail_mort':'rail HS','rail_propose':'rail proposé'}
  y=para(c,html.escape(r['name'])+' · '+types.get(r['kind'],r['kind'])+f" · largeur {r['w']:g}",x,y,ww,SMALL)
 y=para(c,'<b>Lecture</b><br/>Triangles : vrais seuils des bâtiments ouverts ou conditionnels. Rectangles pointillés : emprises des groupes D. Points : positions des personnages P ; plusieurs points peuvent relever d’un même groupe.',x,y-3,ww,SMALL)
 if q['extra']:y=para(c,q['extra'],x,y-4,ww,SMALL)
 tx(c,59,74,paths_legend(),8.6,'AtlasB',INK)
 tx(c,59,56,'Coordonnées : origine au nord-ouest ; x vers l’est, y vers le sud. Repère de composition 100 × 80, sans conversion automatique en cases du jeu.',8,'Atlas',MUTED)
 end(c,q['id']+' / implantation')

def build_table(c,rows,x,y,widths,fontsize=9.2):
 st=ParagraphStyle('t',parent=P,fontSize=fontsize,leading=fontsize*1.35,spaceAfter=0)
 data=[[Paragraph(str(cell),st) for cell in row] for row in rows]
 table=Table(data,colWidths=widths,hAlign='LEFT')
 table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('BACKGROUND',(0,0),(-1,0),HexColor('#d8e0d7')),('LINEBELOW',(0,0),(-1,0),.7,HexColor('#809284')),('LINEBELOW',(0,1),(-1,-1),.3,HexColor('#d0d2c6'))]))
 _,hh=table.wrap(sum(widths),1000)
 if y-hh<50:raise RuntimeError(f'Table trop haute page {c.getPageNumber()}, bas {y-hh:.1f}')
 table.drawOn(c,x,y-hh);return y-hh

def details_page(c,q):
 page(c,f"{q['id']}  |  Fonctions et présences",CITIES[q['city']]['name'],q['name']+'  /  FICHE DE CONCEPTION')
 rows=[['ID / accès','Bâtiment et emprise','Fonction et intérieur proposé']]
 for b in q['buildings']:
  p=door(b);status=STATUS[b['status']][2];coord=f"x {b['x']:g}, y {b['y']:g} ; {b['w']:g} × {b['h']:g}"
  seuil=f"<br/><font color='#537c67'>Seuil {b['face']} : ({p[0]:g} ; {p[1]:g})</font>" if b['status'] in ('O','C') else '<br/>Aucune entrée interactive.'
  text=html.escape(b['fonction'])+(('<br/><b>Visite :</b> '+html.escape(b['interieur'])) if b['interieur'] else '')
  rows.append([b['id']+'<br/><b>'+status+'</b>',html.escape(b['name'])+'<br/>'+coord+seuil,text])
 bottom=build_table(c,rows,36,H-126,[85,210,365],8.6)
 if q['extra']:para(c,'<b>À préserver :</b> '+html.escape(q['extra']),39,bottom-15,650,SMALL)
 x=725;y=H-126
 tx(c,x,y,'PERSONNAGES / SITUATION',10,'AtlasB',ACCENT);y-=15
 if not q['npcs']:y=para(c,'Aucune présence permanente. Les événements éventuels ne créent pas de résidents.',x,y,425,P)
 for n in q['npcs']:
  pos=f"({n['x']:g} ; {n['y']:g})"
  if n.get('members'):pos=' / '.join(f'({a:g};{b:g})' for a,b in n['members'])
  y=para(c,f"<b>{n['id']} · {html.escape(n['name'])}</b> <font color='#9b5a33'>{pos}</font><br/>{html.escape(n['role'])} <font color='#62716b'>{html.escape(n['rythme'])}</font>",x,y,425,SMALL)
 y-=8;tx(c,x,y,'DÉCORS / EMPRISES FONCTIONNELLES',10,'AtlasB',ACCENT);y-=15
 for d in q['decor']:
  y=para(c,f"<b>{d['id']} · {html.escape(d['name'])}</b> ({d['x']:g};{d['y']:g}) · {d['w']:g}×{d['h']:g}<br/>{html.escape(d['contenu'])}",x,y,425,SMALL)
 if y<50:raise RuntimeError(f'Colonne trop haute {q["id"]}, {y}')
 end(c,q['id']+' / fonctions')

def overview(c,city):
 info=CITIES[city];page(c,info['name'],'Organisation d’ensemble',info['basis'])
 c.bookmarkPage(city);c.addOutlineEntry(info['name'],city,0,False)
 x,y,s=57,H-145,7.4;ps=OVERVIEWS[city]
 # a schematic, explicitly without metric scale. Steel is sectioned vertically at right.
 c.setFillColor(HexColor('#e4e5d9'));c.roundRect(x,y-80*s,100*s,80*s,8,fill=1,stroke=0)
 if city=='SM':
  c.setFillColor(HexColor('#c6d7d5'));c.setStrokeColor(HexColor('#658a89'));c.setLineWidth(2);c.circle(x+51*s,y-41*s,20*s,fill=1,stroke=1)
  tx(c,x+40*s,y-39*s,'SARCOPHAGE',12,'AtlasB');tx(c,x+38*s,y-44*s,'sur plusieurs niveaux',9,'Atlas')
  active={p[0] for p in ps[:7]};nodes={id:(xx,yy) for id,xx,yy in ps if id in active}
 else:nodes={id:(xx,yy) for id,xx,yy in ps}
 for a,b,kind in LINKS[city]:
  if a not in nodes or b not in nodes:continue
  aa,bb=nodes[a],nodes[b];c.setStrokeColor(HexColor('#879b8a'));c.setLineWidth(4);c.line(x+aa[0]*s,y-aa[1]*s,x+bb[0]*s,y-bb[1]*s)
 for id,(xx,yy) in nodes.items():
  px,py=x+xx*s,y-yy*s;c.setFillColor(HexColor(INK));c.circle(px,py,18,fill=1,stroke=0);tx(c,px-13,py-3,id,9,'Mono','#f7f3df');c.linkRect('',id,(px-22,py-22,px+22,py+22),relative=0,thickness=0)
  name=BY_ID[id]['name'];tx(c,max(x+4,min(px-50,x+100*s-170)),py-35,name,9,'AtlasB')
 xx=850;yy=H-140
 yy=para(c,info['identity'],xx,yy,300,BOLD);yy=para(c,info['notes'],xx,yy-4,300,SMALL)
 if city=='SM':
  bands=[('UPPER-TOWN',['SM17','SM18']),('CENTER-TOWN',['SM13','SM14','SM15','SM16']),('LOWER-TOWN',['SM09','SM10','SM11','SM12']),('FONDATIONS',['SM08'])]
  for title,ids in bands:
   yy-=5;c.setFillColor(HexColor('#dae3d9'));c.roundRect(xx,yy-68,300,66,4,fill=1,stroke=0);tx(c,xx+9,yy-16,title,10,'AtlasB')
   for i,id in enumerate(ids):
    px=xx+10+(i%2)*145;py=yy-33-(i//2)*17;tx(c,px,py,id+' '+BY_ID[id]['name'][:19],8,'Atlas');c.linkRect('',id,(px,py-3,px+140,py+10),thickness=0)
   yy-=72
 else:
  tx(c,xx,yy-13,'QUARTIERS',10,'AtlasB',ACCENT);yy-=30
  for id,_,_ in ps:
   yy=para(c,f"<b>{id}</b>  {BY_ID[id]['name']}",xx,yy,300,P);c.linkRect('',id,(xx,yy+5,xx+295,yy+25),thickness=0)
  yy-=10;yy=para(c,'<b>Relations de desserte</b><br/>'+'<br/>'.join(a+' ↔ '+b+' : '+k for a,b,k in LINKS[city]),xx,yy,300,SMALL)
 tx(c,58,71,'Schéma de desserte et de voisinage, sans échelle géographique. Cliquez sur un identifiant pour ouvrir son plan.',9,'AtlasB')
 tx(c,58,53,'Les contours des quartiers et les tracés détaillés sont des propositions de conception ; ils n’ajoutent pas des faits au roman.',8.3,'Atlas',MUTED)
 end(c,info['name']+' / ensemble')

def art_page(c,file,title,desc):
 page(c,title,'Concept d’architecture et d’ambiance','Illustration exploratoire ; les plans cotés du dossier font autorité pour les implantations.')
 im=ImageReader(str(ROOT/'concepts'/file));iw,ih=im.getSize();scale=min((W-72)/iw,(H-190)/ih);ww,hh=iw*scale,ih*scale;c.drawImage(im,36+(W-72-ww)/2,110+(H-190-hh)/2,ww,hh)
 para(c,desc,38,88,W-76,SMALL);end(c,'Concept / '+file)

def front(c):
 page(c,'NO MAN’S LAND','Atlas de conception urbaine','V0.1  /  20 octobre 2026  /  proposition avant intégration')
 im=ImageReader(str(ROOT/'concepts'/'steel.png'));iw,ih=im.getSize();hh=(W-72)*ih/iw;c.saveState();pp=c.beginPath();pp.rect(36,260,W-72,460);c.clipPath(pp,stroke=0);c.drawImage(im,36,260-(hh-460)/2,width=W-72,height=hh,mask='auto');c.restoreState()
 tx(c,42,222,'7 VILLES · 37 SECTEURS URBAINS · 7 SITES ISOLÉS',21,'AtlasB')
 para(c,'Plans d’implantation, fonctions, accès aux intérieurs, voirie, rail, personnages et groupes de décors. Le dossier remplace une logique de remplissage par des usages et des parcours identifiables.',43,190,1030,P)
 para(c,'<b>Statut :</b> document de travail à discuter avec Valentin. Les propositions de 2175 restent distinctes du roman et de ses événements de 2202. Aucun changement du jeu ou du site publié n’est inclus dans ce dossier.',43,137,1030,BOLD)
 end(c,'Couverture')
 page(c,'Comment lire cet atlas','Principes de composition','Les fonctions et les parcours précèdent la modélisation.')
 text=[('Deux échelles complémentaires','Les schémas d’ensemble montrent les relations entre quartiers. Les plans 100 × 80 décrivent leurs noyaux jouables : ils ne réduisent pas toute la mégalopole à quelques pâtés de maisons. Le quartier continue hors cadre. Le repère de composition n’est pas la grille du jeu ; la conversion métrique devra suivre une validation de la volumétrie.'),('Chaque seuil appartient à sa façade','Un triangle vert ou ocre matérialise le seul point d’entrée proposé. Sa position figure sur la fiche. Une entrée n’existe que si un intérieur est annoncé. Les façades fermées restent occupées ou condamnées, avec une fonction renseignée.'),('Accès et réserves','O : accès public. C : accès sur accord, document, paiement, quête ou contrôle ; la raison est décrite. N : volume non visitable. R : zone réservée, sans promesse d’ouverture dans cette version. C ne signifie pas que le joueur peut entrer en forçant n’importe quelle porte.'),('Réseaux lisibles','Une route conduit à un quai, à un contrôle ou à un quartier. Une desserte de service reste distincte des rues habitées. Les passerelles sont au-dessus du sol. Un rail gris pointillé est hors service ; une voie proposée reste une hypothèse. Aucune ligne ferroviaire régionale active n’est inventée.'),('Présences et décors utiles','Chaque repère P donne une position, un rôle et une logique de présence. Les petits groupes disposent de positions par membre. Chaque D a une emprise et un contenu : atelier, file, cuisine, fret, eau, entretien, limite ou trace. Ce ne sont pas des endroits à remplir de caisses.'),('Validation de cette version','Les emprises de bâtiments, les corridors de voirie au sol et les approches de portes ont été contrôlés. Le dessin reste une proposition de level design : visibilité isométrique, métrique finale, dénivelés détaillés et navigation d’un avatar seront vérifiés après accord sur les plans.')]
 yy=H-135
 for title,body in text:
  yy=para(c,title,42,yy,1090,BOLD);yy=para(c,body,42,yy,1090,P)-12
 end(c,'Méthode')
 page(c,'Sommaire et portée','Navigation du dossier','Chaque plan est suivi de sa fiche détaillée.')
 yy=H-137
 for city in list(CITIES)[:-1]:
  n=sum(q['city']==city for q in PLANS);yy=para(c,f"<b>{CITIES[city]['name']}</b>  /  {n} secteurs",43,yy,700,BOLD);c.linkRect('',city,(42,yy+5,740,yy+30),thickness=0);yy=para(c,' · '.join(q['id']+' '+q['name'] for q in PLANS if q['city']==city),43,yy,1090,SMALL)-10
 yy=para(c,'<b>Annexes :</b> '+' · '.join(q['id']+' '+q['name'] for q in PLANS if q['city']=='AN'),43,yy-5,1090,SMALL)
 end(c,'Sommaire')
 page(c,'Fidélité au monde et arbitrages','Sources et statut','Les repères de lecture du manuscrit ne sont pas des numéros de page d’édition.')
 sources=[['Base','Ce qui est conservé','Ce qui reste proposé'],['Lore fourni par Valentin','Année 2175 ; IO, ISIO, cyborgs, exclusion des mutants ; villes et factions ; Aura difficile ; prudence hors des murs.','Noms des rues, fonctions des bâtiments secondaires, postes locaux et détails de vie quotidienne.'],['Croquis régional et détail de Steel','Relations générales : Steel, Buenos Aires, Junk-Burgh, zones UFSA ; douanes, industries et trois avant-postes autour du sarcophage.','Tracés exacts, distances intermédiaires, fonctionnement détaillé des ports et structure des secteurs UFSA.'],['Manuscrit Un réveil tardif','Dusk : façades, sable, herbes mortes et laboratoire scellé (paragraphes 70-74). Upper-Town : ciel synthétique, blanc et or, pilier IO (695-699). Arcadius : quatre tours (853). Titan : bras droit, intérieur couché (1049-1062). China Lake : influence mafieuse (2066-2070).','Usage de ces lieux en 2175 ; les événements et protagonistes de l’intrigue de 2202 ne sont pas importés.'],['Jeu existant','Les habitants et affaires de 2175 peuvent être conservés : Mara, Nilo, Tomás, Alma, Candela, etc.','Leurs nouveaux placements et intérieurs sont des propositions. Leur présence dans l’atlas ne valide pas le plan actuel du jeu.']]
 build_table(c,sources,38,H-132,[205,535,375],10)
 yy=310
 yy=para(c,'<b>Arbitrages à confirmer</b>',42,yy,1080,BOLD)
 for s in ['Étendue et statut précis des trois implantations UFSA ; quartiers ajoutés et ordre de visite.','Liste finale des intérieurs ouverts ; conditions d’accès des logements et locaux privés.','Rail de manutention interne du port UFSA, proposé mais non indispensable.','Périmètre de l’Aura et des sites spéciaux ; aucune ouverture du laboratoire ou remise en marche du Titan.','Conversion des unités de plan en mètres, tailles de scènes et limites de continuité urbaine.']:
  yy=para(c,'• '+s,48,yy,1070,P)
 end(c,'Sources et arbitrages')

def export_svg(q):
 # SVG vector deliverable derives from the same authoritative geometry as the PDF.
 from xml.sax.saxutils import escape
 head='<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1280" viewBox="-4 -7 110 93"><style>text{font-family:DejaVu Sans,sans-serif}.id{font-size:1.5px;font-weight:bold}.small{font-size:1.1px}</style>'
 a=[head,f'<title>{escape(q["id"]+" "+q["name"])}</title>','<rect x="-4" y="-7" width="110" height="93" fill="#f4f0e6"/>',f'<text x="0" y="-4" font-size="2.5" font-weight="bold" fill="{INK}">{escape(q["id"]+" | "+q["name"])}</text>','<rect width="100" height="80" fill="#e5e5d8" stroke="#89988b" stroke-width=".2"/>']
 for v in range(0,101,10):a.append(f'<path d="M{v} 0V80" stroke="#c4c5b6" stroke-width=".06"/><text x="{v}" y="-1" class="small" fill="#62716b">{v}</text>')
 for v in range(0,81,10):a.append(f'<path d="M0 {v}H100" stroke="#c4c5b6" stroke-width=".06"/><text x="-3" y="{v}" class="small" fill="#62716b">{v}</text>')
 for f in q['features']:
  col={'eau':'#a8c0bf','canal':'#789b99','impact':'#777e70','foret':'#6c8466','jardin':'#a0b48c','metal':'#969c92'}.get(f['kind'],'#bdbba9');a.append(f'<polygon points="'+ ' '.join(f'{x},{y}' for x,y in f['points'])+f'" fill="{col}" stroke="#80927d" stroke-width=".2"/>')
 for r in q['roads']:
  rail=r['kind'].startswith('rail');col='#887e66' if rail else '#b4afa0' if r['kind']!='pieton' else '#d7c59c';dash=' stroke-dasharray="1 .6"' if rail or r['kind']=='sureleve' else ''
  a.append(f'<polyline points="'+ ' '.join(f'{x},{y}' for x,y in r['points'])+f'" fill="none" stroke="{col}" stroke-width="{r["w"]}"{dash}><title>{escape(r["name"]+" / "+r["kind"])}</title></polyline>')
 for b in q['buildings']:
  fill,col,st=STATUS[b['status']];title=escape(b['id']+' | '+b['name']+' | '+st+' | '+b['fonction']);attrs=f'fill="{fill}" stroke="{col}" stroke-width=".22"'
  if b.get('shape')=='cercle':a.append(f'<ellipse cx="{b["x"]+b["w"]/2}" cy="{b["y"]+b["h"]/2}" rx="{b["w"]/2}" ry="{b["h"]/2}" {attrs}><title>{title}</title></ellipse>')
  elif b.get('shape')=='decroche':
   bx,by,bw,bh=b['x'],b['y'],b['w'],b['h'];points=[(bx,by),(bx+bw*.65,by),(bx+bw*.65,by+bh*.25),(bx+bw,by+bh*.25),(bx+bw,by+bh),(bx,by+bh)];a.append('<polygon points="'+' '.join(f'{xx},{yy}' for xx,yy in points)+f'" {attrs}><title>{title}</title></polygon>')
  else:a.append(f'<rect x="{b["x"]}" y="{b["y"]}" width="{b["w"]}" height="{b["h"]}" {attrs}><title>{title}</title></rect>')
  a.append(f'<text x="{b["x"]+.7}" y="{b["y"]+2.1}" class="id" fill="{col}">{b["id"]} {b["status"]}</text>')
  if b['status'] in ['O','C']:
   xx,yy=door(b);dx,dy={'N':(0,-1),'S':(0,1),'W':(-1,0),'E':(1,0)}[b['face']];pts=[(xx,yy),(xx+dx*1.3-dy*.6,yy+dy*1.3+dx*.6),(xx+dx*1.3+dy*.6,yy+dy*1.3-dx*.6)];a.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="{col}"/>')
 for d in q['decor']:
  a.append(f'<rect x="{d["x"]}" y="{d["y"]}" width="{d["w"]}" height="{d["h"]}" fill="none" stroke="#6e8977" stroke-width=".13" stroke-dasharray=".5 .4"><title>{escape(d["name"]+" | "+d["contenu"])}</title></rect>');a.append(f'<text x="{d["x"]+d["w"]/2-1.2}" y="{d["y"]+d["h"]/2+.4}" class="small" fill="#44664c">{d["id"]}</text>')
 for n in q['npcs']:
  for xx,yy in n.get('members',[(n['x'],n['y'])]):a.append(f'<circle cx="{xx}" cy="{yy}" r=".5" fill="#a75932"><title>{escape(n["name"]+" | "+n["role"])}</title></circle>')
  a.append(f'<text x="{n["x"]+1}" y="{n["y"]+.4}" class="small" fill="#9b4f2c">{n["id"]}</text>')
 a.append('<text x="0" y="84" class="small" fill="#62716b">O ouvert · C conditionnel · N fermé · R réservé | P personnages · D décors | Nord en haut</text></svg>')
 (ROOT/'plans'/f'{q["id"]}.svg').write_text('\n'.join(a))

def main():
 issues=[(q['id'],i) for q in PLANS for i in intersections(q)]
 assert not issues,issues
 pdf=OUT/'No-Mans-Land_Atlas-Conception_v01.pdf';c=canvas.Canvas(str(pdf),pagesize=(W,H),pageCompression=1);c.setTitle('No Man’s Land - Atlas de conception urbaine v0.1');c.setAuthor('Valentin - dossier de travail accompagné par Codex')
 front(c)
 art_page(c,'steel.png','Steel-Megalopolis : trois régimes urbains','De gauche à droite : Lower-Town, Upper-Town et périmètre. La taille et la densité diffèrent radicalement ; le plan précise ensuite les accès.')
 art_page(c,'exterieur.png','Les villes des terres','Dusk-Town, Junk-Burgh et Buenos Aires. Les volumes et les usages sont distincts. À Buenos Aires, concentrer la végétation dans les patios entretenus, plutôt que généraliser la verdure de cette illustration.')
 art_page(c,'ufsa.png','Trois implantations UFSA proposées','Novo Córdoba, port UFSA et siège UFSA. Ces identités visuelles restent des hypothèses fondées sur le croquis ; elles ne fixent pas la politique ou les moyens militaires du canon.')
 for city in list(CITIES)[:-1]:
  overview(c,city)
  for q in PLANS:
   if q['city']==city:map_page(c,q);details_page(c,q)
 page(c,'Sites hors des villes','Annexes de circulation','Ces sept plans ne doivent pas être interprétés comme sept villes supplémentaires.');c.bookmarkPage('AN');c.addOutlineEntry('Sites isolés','AN',0,False)
 yy=H-145
 for q in PLANS:
  if q['city']=='AN':
   yy=para(c,f"<b>{q['id']} · {q['name']}</b><br/>{q['parti']}",43,yy,1000,P)-18
 end(c,'Annexes')
 for q in PLANS:
  if q['city']=='AN':map_page(c,q);details_page(c,q)
 page(c,'Avant de revenir au jeu','Revue de conception','La prochaine implémentation doit se conformer aux plans validés, pas les réinterpréter au hasard.')
 yy=H-145
 for title,body in [('1. Valider les ensembles','Quartiers, connexions, fonctions des lieux et séparation des zones habitées, industrielles et dangereuses.'),('2. Valider les accès','Bâtiments ouverts et fermés, seuils sur façade, conditions d’entrée et taille raisonnable de leurs intérieurs.'),('3. Valider les présences','Situation de chaque interlocuteur, déplacements utiles, horaires et absences liées aux quêtes.'),('4. Valider l’architecture','Volumes, hauteurs et silhouettes propres aux quartiers, puis vues isométriques de contrôle. La topologie exacte vient des plans, pas des illustrations d’ambiance.'),('5. Vérifier les parcours après volumétrie','Lignes de vue, largeur réellement praticable, sorties, couverts et approches des portes ; test du déplacement sur les décors modélisés.'),('6. Intégrer par zone complète','Modélisation, matériaux, éclairage, décor, PNJ et intérieurs d’un même ensemble. Pas de multiplication des scènes avant validation du premier secteur de référence.')]:
  yy=para(c,title,43,yy,1070,BOLD);yy=para(c,body,43,yy,1070,P)-17
 end(c,'Revue de conception');c.save()
 (OUT/'atlas_positions.json').write_text(json.dumps(dict(cities=CITIES,plans=PLANS,links=LINKS,overviews=OVERVIEWS),ensure_ascii=False,indent=2))
 for kind,file in [('buildings','batiments.csv'),('npcs','personnages.csv'),('decor','decors.csv'),('roads','voirie.csv')]:
  rows=[]
  for q in PLANS:
   for item in q[kind]:
    row={'ville':CITIES[q['city']]['name'],'quartier_id':q['id'],'quartier':q['name'],**item}
    if kind=='buildings' and item['status'] in ('O','C'):row['seuil_x'],row['seuil_y']=door(item)
    for k,v in list(row.items()):
     if isinstance(v,(list,dict)):row[k]=json.dumps(v,ensure_ascii=False)
    rows.append(row)
  fields=list(dict.fromkeys(k for row in rows for k in row))
  with (OUT/file).open('w',newline='',encoding='utf-8-sig') as f:
   wr=csv.DictWriter(f,fieldnames=fields,delimiter=';');wr.writeheader();wr.writerows(rows)
 for q in PLANS:export_svg(q)
 (ROOT/'qa'/'pages.json').write_text(json.dumps(PAGELOG,ensure_ascii=False,indent=2))
 print(json.dumps({'pdf':str(pdf),'pages':len(PAGELOG),'plans':len(PLANS),'buildings':sum(len(q['buildings']) for q in PLANS),'npcs':sum(len(q['npcs']) for q in PLANS),'decor':sum(len(q['decor']) for q in PLANS)},ensure_ascii=False))
if __name__=='__main__':main()
