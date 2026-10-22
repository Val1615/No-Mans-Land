from pathlib import Path
import json,sys,math,unicodedata,re
from xml.sax.saxutils import escape
from reportlab.platypus import (BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether,Flowable)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from content import PAGES
from profiles import PROFILES,ROAD_PROFILES,NEW_PROFILES
from appendices import EXTRA_PAGES

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
AUD=json.loads((ROOT/'source/audit.json').read_text())
ATLAS=json.loads(Path('/workspace/scratch/00d29d1aab63/atlas-conception-v01/output/atlas_positions.json').read_text())
WORLD=json.loads((ROOT/'source/world.json').read_text())
for name,file in [('D','DejaVuSans.ttf'),('DB','DejaVuSans-Bold.ttf'),('DM','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFontFamily('D',normal='D',bold='DB',italic='D',boldItalic='DB')
W,H=A4;M=48;CW=W-2*M;BH=H-118
INK=colors.HexColor('#151a1c');MUTED=colors.HexColor('#525b5f');LINE=colors.HexColor('#d4d7d7')
ACCENT=colors.HexColor('#8c5b36')
S={
 'body':ParagraphStyle('body',fontName='D',fontSize=10.1,leading=14.2,textColor=INK,spaceAfter=8),
 'intro':ParagraphStyle('intro',fontName='D',fontSize=10.5,leading=15,textColor=INK,spaceAfter=15),
 'small':ParagraphStyle('small',fontName='D',fontSize=8.5,leading=11.7,textColor=MUTED,spaceAfter=7),
 'note':ParagraphStyle('note',fontName='D',fontSize=8.8,leading=12.5,textColor=MUTED,spaceBefore=10),
 'title':ParagraphStyle('title',fontName='DB',fontSize=23,leading=28,textColor=colors.black,spaceAfter=18),
 'head':ParagraphStyle('head',fontName='DB',fontSize=11.2,leading=15,textColor=colors.black,spaceBefore=5,spaceAfter=4),
 'person':ParagraphStyle('person',fontName='DB',fontSize=13.2,leading=17,textColor=colors.black,spaceAfter=4),
 'profile':ParagraphStyle('profile',fontName='D',fontSize=9.4,leading=13.1,textColor=INK,spaceAfter=4),
 'table':ParagraphStyle('table',fontName='D',fontSize=9.2,leading=12.8,textColor=INK),
 'th':ParagraphStyle('th',fontName='DB',fontSize=9.3,leading=13,textColor=colors.black),
}
def clean(t):
    return str(t).replace('\u2011','-').replace('\u2013','-').replace('\u2014','-')
def p(t,style='body'):
    return Paragraph(escape(clean(t)).replace('\n','<br/>'),S[style])
def bold(label,t,style='profile'):
    return Paragraph('<b>'+escape(clean(label))+'</b> '+escape(clean(t)),S[style])
def norm(t):
    return ''.join(c for c in unicodedata.normalize('NFKD',t.lower()) if not unicodedata.combining(c))

PAGE_RECORD=[];PROFILE_RECORD={};MEASURES=[]
class Heading(Paragraph):
    def __init__(self,title,key,section='',level=0,toc=True):
        super().__init__(escape(clean(title)),S['title'] if level==0 else S['person'])
        self.doc_key=key;self.doc_title=title;self.doc_section=section;self.doc_level=level;self.doc_toc=toc

class Line(Flowable):
    def __init__(self,w=CW):super().__init__();self.width=w;self.height=8
    def draw(self):
        self.canv.setStrokeColor(LINE);self.canv.setLineWidth(.5);self.canv.line(0,4,self.width,4)

class RegionMap(Flowable):
    def __init__(self):super().__init__();self.width=CW;self.height=535
    def draw(self):
        c=self.canv;s=19;x0=34;y0=122;top=y0+20*s
        c.setFillColor(colors.HexColor('#f0f4f4'));c.rect(x0,y0,22*s,20*s,fill=1,stroke=0)
        for cell in WORLD['cells']:
            col,row=cell['col'],cell['row'];c.setFillColor(colors.HexColor('#e7e2d2'))
            c.setStrokeColor(colors.white);c.setLineWidth(.5);c.rect(x0+col*s,top-(row+1)*s,s,s,fill=1,stroke=1)
        locs={x['id']:x for x in WORLD['locations']}
        locs['buenos']={'name':'Buenos Aires','cell':{'col':14,'row':3}}
        def pt(cell):return x0+(cell['col']+.5)*s,top-(cell['row']+.5)*s
        routes=[('CR 01','farm','dusk','#64815b',0),('CR 02','dusk','junk','#a4763b',1.5),('CR 03','port','customs','#3e7782',-1.5),('CR 04','buenos','junk','#8b5372',0)]
        for label,a,b,color,dy in routes:
            r=next(r for r in WORLD['routes'] if r['from']==a and r['to']==b)
            points=[r['fromCell']]+r['path'];c.setStrokeColor(colors.HexColor(color));c.setLineWidth(2.1)
            path=c.beginPath();xx,yy=pt(points[0]);path.moveTo(xx,yy+dy)
            for cell in points[1:]:xx,yy=pt(cell);path.lineTo(xx,yy+dy)
            c.drawPath(path)
        # Numérotation sans étiquettes qui se chevauchent.
        order=['farm','dusk','crater','buenos','titan','customs','steel','junk','relay','temple','port','nova','coast']
        for i,id in enumerate(order,1):
            x,y=pt(locs[id]['cell']);c.setFillColor(colors.HexColor('#a45c3b') if id=='crater' else INK)
            c.circle(x,y,7,fill=1,stroke=0);c.setFillColor(colors.white);c.setFont('DB',6.6);c.drawCentredString(x,y-2.3,str(i))
        c.setFont('D',6.9);c.setFillColor(MUTED)
        for k in range(22):c.drawCentredString(x0+(k+.5)*s,top+8,str(k))
        for k in range(20):c.drawRightString(x0-7,top-(k+.65)*s,str(k))
        c.setFont('DB',8);c.drawString(x0,top+23,'Grille actuelle : colonnes et lignes indexées à partir de 0')
        c.setFont('D',8)
        for i,id in enumerate(order,1):
            col=(i-1)//7;row=(i-1)%7;c.drawString(x0+col*220,y0-17-row*10.8,str(i)+'  '+locs[id]['name'])
        for i,(label,a,b,color,dy) in enumerate(routes):
            xx=x0+(i%2)*220;yy=20-(i//2)*13
            c.setStrokeColor(colors.HexColor(color));c.setLineWidth(2);c.line(xx,yy+3,xx+20,yy+3)
            c.setFillColor(INK);c.setFont('D',8);c.drawString(xx+27,yy,label+'  '+({'CR 01':'vivres Granja / Dusk','CR 02':'Dusk / bazars','CR 03':'logistique IO','CR 04':'Buenos Aires / bazars'}[label]))

class Doc(BaseDocTemplate):
    def __init__(self,path):
        super().__init__(str(path),pagesize=A4,leftMargin=M,rightMargin=M,topMargin=65,bottomMargin=53,title='No Man’s Land - Gameplay et personnages - Conception v0.1',author='Conception pour Valentin',pageCompression=1)
        self.addPageTemplates(PageTemplate(id='main',frames=[Frame(M,53,CW,BH,id='body',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=self.paint))
        self.section='';self.profile_index={}
    def paint(self,c,doc):
        c.saveState()
        if doc.page>1:
            c.setFont('DB',7.5);c.setFillColor(MUTED);c.drawString(M,H-34,'NO MAN’S LAND  /  GAMEPLAY ET PERSONNAGES')
            c.setFont('D',7.5);c.drawRightString(W-M,H-34,'CONCEPTION 0.1')
            c.setStrokeColor(LINE);c.setLineWidth(.5);c.line(M,40,W-M,40)
            c.setFont('D',7.2);c.drawString(M,27,'Audit v0.6  ·  Propositions non intégrées  ·  20 octobre 2026')
            c.drawRightString(W-M,27,f'{doc.page:03d}')
        c.restoreState()
    def afterFlowable(self,f):
        if isinstance(f,Heading):
            self.canv.bookmarkPage(f.doc_key)
            self.canv.addOutlineEntry(f.doc_title,f.doc_key,level=f.doc_level,closed=True)
            if f.doc_toc:self.notify('TOCEntry',(0,f.doc_title,self.page,f.doc_key))
            if f.doc_key.startswith('npc-'):self.profile_index[f.doc_key[4:]]=self.page

def table_flow(spec):
    headers,rows=spec;cols=len(headers)
    widths=([CW*.23,CW*.34,CW*.43] if cols==3 else [CW*.30,CW*.70])
    data=[[p(x,'th') for x in headers]]+[[p(x,'table') for x in row] for row in rows]
    tb=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    tb.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eceeed')),
        ('BOX',(0,0),(-1,-1),.45,LINE),('INNERGRID',(0,0),(-1,-1),.4,LINE),
    ]));return tb

def content_flow(pg,index):
    out=[p(pg['section'].upper(),'small'),Heading(pg['title'],'section-'+str(index),pg['section'])]
    if pg.get('intro'):out.append(p(pg['intro'],'intro'))
    if pg.get('table'):out.append(table_flow(pg['table']));out.append(Spacer(1,8))
    if pg.get('kind')=='map':out.append(RegionMap())
    for title,text in pg.get('blocks',[]):out.extend([p(title,'head'),p(text)])
    if pg.get('note'):out.append(p(pg['note'],'note'))
    return out

def height(items):
    h=0
    for x in items:
        _,v=x.wrap(CW,BH);h+=v+x.getSpaceBefore()+x.getSpaceAfter()
    return h

SCENE_ATLAS={
 'farm':'AN01','dusk':'DT01','clinic':'DT01','crater':'AN02','buenos':'BA03','customs':'SM01','steel':'SM09','under':'SM08','junk':'JB01','titan':'AN03','relay':'AN04','temple':'AN05','port':'AN06','nova':'NC02','coast':'AN07','backroom':'JB02','bunker':'AN03',
 'china':'SM10','asia':'SM11','blocks':'SM12','center':'SM13','cliniccity':'SM14','civic':'SM15','smpd':'SM16','upper':'SM17','spire':'SM18','industry':'SM04','northcustoms':'SM02','eastcustoms':'SM03','northbase':'SM05','eastbase':'SM06','southbase':'SM07','ba-avenues':'BA01','ba-habitat':'BA02','ba-ateliers':'BA04','ba-front':'BA05','ba-cinema':'BA02'}
OVERRIDE={'nilo':'DT03','nadia':'DT02','abel':'DT02','alma':'JB02','debtor':'JB03','scrapper':'JB04','silas':'JB02','noemi':'JB02','bruna':'NC01','ramos':'NC03','patient':'DT01','paz':'DT01'}
NAMES={n['id']:n for n in AUD['roster']}
LOCNAMES={s['id']:s['name'] for s in AUD['scenes']}
def match_atlas(n):
    name=norm(n['name'])
    aliases={'inesguard':['milicienne'],'deserter':['esteban rios']}
    names=[name]+aliases.get(n['id'],[])
    return [(plan,a) for plan in ATLAS['plans'] for a in plan['npcs'] if norm(a['name']) in names]
def atlas_label(n):
    matches=match_atlas(n)
    if matches:return ' ; '.join(f"{pl['id']} x{a['x']}/y{a['y']}" for pl,a in matches)
    if n['id']=='prospector':return 'Aucun emplacement retenu.'
    plan=OVERRIDE.get(n['id']) or SCENE_ATLAS.get(n['locations'][0])
    return plan+' ; point individuel à préciser dans le bâtiment de fonction.'
def profile_flow(n):
    pp=PROFILES[n['id']]
    status='PRÉSENT' if n['locations'] else 'DÉFINITION RETIRÉE DES SCÈNES'
    pos=' ; '.join(LOCNAMES[a['loc']]+f" q{a['q']}/r{a['r']}" for a in n['anchors']) or 'Aucune scène.'
    out=[Line(),Heading(n['name'],'npc-'+n['id'],level=1,toc=False),
         p(status+'  ·  '+n['id']+'  ·  '+n['faction'],'small'),
         bold('Fonction actuelle.',n['role']+'. '+n['look']),
         bold('Position actuelle.',pos),bold('Repère atlas.',atlas_label(n)),
         bold('Voix et but.',pp['voix']+' '+pp['motif']),bold('Routine proposée.',pp['routine']),
         bold('Réaction et savoir proposés.',pp['reaction']),Spacer(1,5)]
    return out

GROUPS=[
 ('Dusk Town','mara vera paz patient nilo inesguard nadia abel ezequiel'),
 ('Granja Altruista','ines irisfarm'),
 ('Douanes de Steel','vidal luz mirek north-agent reina east-agent dario'),
 ('Industries et avant postes','avel delta north-officer pavel east-officer cielo south-officer grisel'),
 ('Sous Ville et Forum','salma inspector enid ada security astor'),
 ('China Lake et Asia Ground','rita lin yu leda hassan sami nour'),
 ('Blocs et Avenue Centrale','cora elias tala berenice central-host odette'),
 ('Cliniques registre et SMPD','broker sen yuna eva ivo leal aural'),
 ('Upper Town','maelle eilin valen sem'),
 ('Junk Burgh','roque alma debtor scrapper silas noemi beltra'),
 ('Buenos Aires centre et avenues','tomas celia vesta candela mauro isma'),
 ('Buenos Aires Patios et cinéma','esme mila gaspar teo renzo'),
 ('Buenos Aires ateliers et lisière','vico rocio sergio lian alder'),
 ('Titan relais et temple','otero pilar veiled senda'),
 ('Nœud maritime IO','marin deserter celso'),
 ('Novo Córdoba','ortiz quartermaster ramos bruna'),
 ('Waste Coast','courier leoncoast'),
 ('Définition hors scène','prospector')]

def cover():
    out=[Spacer(1,50),p('NO MAN’S LAND','small'),Spacer(1,12)]
    st=ParagraphStyle('cover',parent=S['title'],fontSize=36,leading=42,spaceAfter=20)
    out.append(Paragraph('Gameplay et<br/>personnages',st));out.append(p('Dossier de conception 0.1','intro'))
    out+=[Spacer(1,15),Line(),Spacer(1,14),p('2175. Des habitants qui vivent dans leurs quartiers, des ressources qui circulent et un allié qui partage la route.','intro'),Spacer(1,25)]
    metrics=[['92','32','6','4'],['PNJ placés audités','événements proposés','circuits proposés','candidats compagnons']]
    data=[[p(t,'title') for t in metrics[0]],[p(t,'small') for t in metrics[1]]]
    t=Table(data,colWidths=[CW/4]*4);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),12)]));out.append(t)
    out+=[Spacer(1,35),p('État de référence : version jouable 0.6.\nDocument complémentaire à l’Atlas de conception v0.1.\nUnivers de Valentin. Revue du 20 octobre 2026.','body'),Spacer(1,20),p('PRÉSENT  /  PARTIEL  /  PROPOSÉ\nLes nouvelles règles, personnes et routines restent des propositions de conception. Aucun code ni déploiement n’a été modifié.','note'),PageBreak()]
    return out

def make_story():
    story=cover()
    story.append(Heading('Sommaire','toc',toc=False))
    toc=TableOfContents();toc.levelStyles=[ParagraphStyle('toc0',fontName='D',fontSize=9.4,leading=14.4,leftIndent=0,firstLineIndent=0,spaceBefore=0,textColor=INK)]
    toc.tableStyle=TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),3)])
    toc.dotsMinLevel=0
    story.extend([p('Le PDF contient aussi un signet pour chaque personne nommée. La recherche par nom ou identifiant permet d’accéder directement à une fiche.','small'),toc,PageBreak()])
    counter=0
    before_npc=[]
    for pg in PAGES:
        if pg['title']=='États à conserver':
            before_npc.append(EXTRA_PAGES[0])
        before_npc.append(pg)
    for pg in before_npc:
        flows=content_flow(pg,counter);counter+=1
        MEASURES.append({'title':pg['title'],'height':round(height(flows),1),'available':round(BH,1)})
        story.extend(flows);story.append(PageBreak())
    for group,ids in GROUPS:
        items=[profile_flow(NAMES[id]) for id in ids.split()]
        count=math.ceil(len(items)/3);small,extra=divmod(len(items),count)
        chunks=[];offset=0
        for k in range(count):
            size=small+(1 if k<extra else 0);chunk=items[offset:offset+size];offset+=size
            assert sum(height(f) for f in chunk)<=BH-74,group
            chunks.append(chunk)
        for i,chunk in enumerate(chunks,1):
            name=group+(f' {i}' if len(chunks)>1 else '')
            story.extend([p('REGISTRE PNJ  /  EXISTANT ET ROUTINES PROPOSÉES','small'),Heading(name,'group-'+str(counter),toc=(i==1))]);counter+=1
            for flows in chunk:story.append(KeepTogether(flows))
            story.append(PageBreak())
    story.extend([p('REGISTRE PNJ  /  RENCONTRES ACTUELLES','small'),Heading('Personnes des rencontres de route','road-npcs')])
    for road in ROAD_PROFILES:
        story.extend([Line(),Heading(road['name'],'npc-'+road['id'],level=1,toc=False),bold('Présence actuelle.',road['present']),bold('Voix.',road['voice']),bold('Suite proposée.',road['routine']),bold('Réaction et limites.',road['react']),Spacer(1,14)])
    story.append(PageBreak())
    # Nouveaux noms : trois fiches par page, regroupées par territoire.
    territory=lambda pl:'Steel Megalopolis' if pl.startswith('SM') else 'Dusk et Junk Burgh' if pl.startswith(('DT','JB')) else 'Novo Córdoba' if pl.startswith('NC') else 'Port UFSA' if pl.startswith('PU') else 'Siège UFSA'
    grouped={}
    for rec in NEW_PROFILES:grouped.setdefault(territory(rec[1]),[]).append(rec)
    new_ids=['aro','noa','dena','rafi','mina','elisa','ana','cira','iago','sol','alba','damian','salo','elva','lina','tessa','daro','neri','elsa','ulmo','salvat','orel','joana','farel','numa','oso']
    id_by_name={rec[0]:id for rec,id in zip(NEW_PROFILES,new_ids)}
    nidx=0
    for region,recs in grouped.items():
        count=math.ceil(len(recs)/3);small,extra=divmod(len(recs),count);offset=0
        for chunknum in range(count):
            start=chunknum*3;size=small+(1 if chunknum<extra else 0);batch=recs[offset:offset+size];offset+=size
            title='Nouveaux PNJ '+region+(f' {start//3+1}' if len(recs)>3 else '')
            story.extend([p('REGISTRE PNJ  /  NOUVELLES PROPOSITIONS','small'),Heading(title,'new-'+str(nidx),toc=(chunknum==0))])
            for name,plan,identity,motive,route,react in batch:
                pl=next(x for x in ATLAS['plans'] if x['id']==plan)
                anchor=next((n for n in pl['npcs'] if n['name']==name),None)
                key='proposition-'+id_by_name[name];nidx+=1
                pos=f"{plan} x{anchor['x']}/y{anchor['y']}" if anchor else plan+' ; position à préciser.'
                flows=[Line(),Heading(name,'npc-'+key,level=1,toc=False),p('PROPOSÉ  ·  identifiant '+id_by_name[name]+'  ·  '+pos,'small'),bold('Identité.',identity),bold('But.',motive),bold('Routine proposée.',route),bold('Voix réaction et savoir.',react),Spacer(1,8)]
                story.append(KeepTogether(flows))
            story.append(PageBreak())
    extra=list(EXTRA_PAGES[1:]);collective=extra.pop(0);headers,rows=collective['table']
    extra.insert(0,{**collective,'title':'Gardes et menaces','intro':'Fonctions collectives proposées pour la sécurité et les adversaires. Les équipes du front possèdent déjà une première logique tactique dans la version actuelle.','table':(headers,rows[4:])})
    extra.insert(0,{**collective,'table':(headers,rows[:4])})
    for pg in extra:
        flows=content_flow(pg,counter);counter+=1;MEASURES.append({'title':pg['title'],'height':round(height(flows),1),'available':round(BH,1)});story.extend(flows);story.append(PageBreak())
    story.pop() # pas de dernière page blanche
    return story

if __name__=='__main__':
    assert len(PROFILES)==len(AUD['roster'])==93
    assert {id for _,ids in GROUPS for id in ids.split()}==set(PROFILES)
    assert len(NEW_PROFILES)==26
    dest=OUT/'No-Mans-Land_Gameplay-et-PNJ_Conception_v01.pdf'
    doc=Doc(dest);doc.multiBuild(make_story())
    (ROOT/'qa/measurements.json').write_text(json.dumps(MEASURES,ensure_ascii=False,indent=2))
    (ROOT/'qa/profile_pages.json').write_text(json.dumps(doc.profile_index,ensure_ascii=False,indent=2))
    print(dest);print('Fiches indexées',len(doc.profile_index))
    print('Pages prévues trop hautes',[(x['title'],x['height']) for x in MEASURES if x['height']>BH])
