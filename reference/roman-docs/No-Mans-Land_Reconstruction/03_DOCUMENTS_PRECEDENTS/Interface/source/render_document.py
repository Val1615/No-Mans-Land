from pathlib import Path
import json,math,re
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4,A3,landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,Table,TableStyle,PageBreak,NextPageTemplate,Image,KeepTogether
from reportlab.platypus.tableofcontents import TableOfContents
from content import PAGES
from visuals import MOCKUPS,SOURCES

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
W,H=A4;WW,WH=landscape(A3);M=48;CW=W-2*M;BH=H-118
INK=colors.HexColor('#162127');MUTED=colors.HexColor('#536169');LINE=colors.HexColor('#D3DADD');ACCENT=colors.HexColor('#376F70')
for n,f in [('D','DejaVuSans.ttf'),('DB','DejaVuSans-Bold.ttf'),('DM','DejaVuSansMono.ttf')]:pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
pdfmetrics.registerFontFamily('D',normal='D',bold='DB',italic='D',boldItalic='DB')
ST={
 'body':ParagraphStyle('body',fontName='D',fontSize=10.1,leading=14.3,textColor=INK,spaceAfter=8),
 'intro':ParagraphStyle('intro',fontName='D',fontSize=10.5,leading=15,textColor=INK,spaceAfter=14),
 'small':ParagraphStyle('small',fontName='D',fontSize=8.3,leading=11.5,textColor=MUTED,spaceAfter=7),
 'note':ParagraphStyle('note',fontName='D',fontSize=8.8,leading=12.4,textColor=MUTED,spaceBefore=9),
 'h1':ParagraphStyle('h1',fontName='DB',fontSize=22,leading=27,textColor=colors.black,spaceAfter=17),
 'h2':ParagraphStyle('h2',fontName='DB',fontSize=11.2,leading=15,textColor=colors.black,spaceBefore=4,spaceAfter=4),
 'table':ParagraphStyle('table',fontName='D',fontSize=9.15,leading=12.7,textColor=INK),
 'th':ParagraphStyle('th',fontName='DB',fontSize=9.25,leading=13,textColor=colors.black),
 'caption':ParagraphStyle('caption',fontName='D',fontSize=11.5,leading=16,textColor=INK,spaceAfter=7),
 'prompt':ParagraphStyle('prompt',fontName='D',fontSize=8.6,leading=12,textColor=INK,spaceAfter=8),
}
def clean(t):return str(t).replace('\u2011','-').replace('\u2013','-').replace('\u2014','-')
def p(t,style='body'):return Paragraph(escape(clean(t)).replace('\n','<br/>'),ST[style])
def b(label,text,style='caption'):return Paragraph('<b>'+escape(clean(label))+'</b> '+escape(clean(text)),ST[style])
class Heading(Paragraph):
    def __init__(self,title,key,toc=True):
        super().__init__(escape(clean(title)),ST['h1']);self.key=key;self.title=title;self.toc=toc
class Doc(BaseDocTemplate):
    def __init__(self,path):
        super().__init__(str(path),pagesize=A4,leftMargin=M,rightMargin=M,topMargin=65,bottomMargin=53,title='No Man’s Land - Interface et atelier développeur - Conception v0.1',author='Conception pour Valentin',pageCompression=1)
        normal=PageTemplate(id='normal',frames=[Frame(M,53,CW,BH,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],pagesize=A4,onPage=self.paint)
        wide=PageTemplate(id='wide',frames=[Frame(M,55,WW-2*M,WH-120,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],pagesize=(WW,WH),onPage=self.paint)
        self.addPageTemplates([normal,wide]);self.index={}
    def paint(self,c,doc):
        pw,ph=c._pagesize;c.saveState()
        if doc.page>1:
            c.setFont('DB',7.5);c.setFillColor(MUTED);c.drawString(M,ph-33,'NO MAN’S LAND  /  INTERFACE ET ATELIER DÉVELOPPEUR')
            c.setFont('D',7.5);c.drawRightString(pw-M,ph-33,'CONCEPTION 0.1  ·  PROPOSÉ')
            c.setStrokeColor(LINE);c.setLineWidth(.5);c.line(M,39,pw-M,39)
            c.setFont('D',7.2);c.drawString(M,26,'Références et spécifications  ·  Jeu inchangé  ·  20 octobre 2026')
            c.drawRightString(pw-M,26,f'{doc.page:03d}')
        c.restoreState()
    def afterFlowable(self,f):
        if isinstance(f,Heading):
            self.canv.bookmarkPage(f.key);self.canv.addOutlineEntry(f.title,f.key,level=0,closed=False);self.index[f.key]=self.page
            if f.toc:self.notify('TOCEntry',(0,f.title,self.page,f.key))

def table(spec):
    heads,rows=spec
    widths=[CW*.235,CW*.345,CW*.42] if len(heads)==3 else [CW*.29,CW*.71]
    data=[[p(x,'th') for x in heads]]+[[p(x,'table') for x in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EDF1F1')),('BOX',(0,0),(-1,-1),.45,LINE),('INNERGRID',(0,0),(-1,-1),.4,LINE)]));return t
def measure(flow):
    total=0
    for f in flow:
        _,h=f.wrap(CW,BH);total+=h+f.getSpaceBefore()+f.getSpaceAfter()
    return total
def content(pg,key,suffix=''):
    out=[p(pg['section'].upper(),'small'),Heading(pg['title']+suffix,key)]
    if pg.get('intro'):out.append(p(pg['intro'],'intro'))
    if pg.get('table'):out.extend([table(pg['table']),Spacer(1,8)])
    for title,text in pg.get('blocks',[]):out.extend([p(title,'h2'),p(text)])
    if pg.get('note'):out.append(p(pg['note'],'note'))
    return out
def fit_content(pg,key):
    flows=content(pg,key)
    if measure(flows)<=BH:return [(pg['title'],flows)]
    if pg.get('table'):
        heads,rows=pg['table']
        for count in range(2,len(rows)+1):
            out=[];start=0;small,extra=divmod(len(rows),count)
            for part in range(count):
                stop=start+small+(part<extra)
                candidate={**pg,'table':(heads,rows[start:stop]),'intro':pg['intro'] if part==0 else '', 'blocks':pg['blocks'] if part==count-1 else [],'note':pg['note'] if part==count-1 else None}
                suffix='' if part==0 else ' suite'
                fs=content(candidate,key+('-'+str(part+1) if part else ''),suffix)
                out.append((pg['title']+suffix,fs));start=stop
            if all(measure(f)<=BH for _,f in out):return out
        raise RuntimeError('Trop haut '+pg['title'])
    raise RuntimeError('Page non tabulaire trop haute '+pg['title'])

def visual(m):
    out=[p('RÉFÉRENCE VISUELLE  /  PROPOSITION À RECONSTRUIRE EN COMPOSANTS','small'),Heading('M'+m['id']+'  '+m['title'],'M'+m['id'])]
    width=WW-2*M;im=Image(str(ROOT/'reference-images'/('M'+m['id']+'.png')))
    ratio=im.imageHeight/im.imageWidth;im.drawWidth=width;im.drawHeight=width*ratio
    # Garder le texte explicatif lisible sous l’image à sa taille native de composition.
    im.drawHeight=min(im.drawHeight,540);im.drawWidth=im.drawHeight/ratio;im.hAlign='CENTER'
    out+=[im,Spacer(1,10)]
    # Deux colonnes de notes, pas de calque placé sur le visuel généré.
    widthc=(width-24)/2
    a=b('À retenir.',m['keep']);z=b('Application et corrections.',m['apply'])
    q=Table([[a,z]],colWidths=[widthc,widthc+24]);q.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),16),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    out+=[q,b('Mouvement.',m['motion'],'small')]
    return out

def cover():
    st=ParagraphStyle('cover',parent=ST['h1'],fontSize=31,leading=38)
    im=Image(str(ROOT/'reference-images/M01.png'),width=CW,height=CW*941/1672)
    return [Spacer(1,30),p('NO MAN’S LAND','small'),Spacer(1,8),Paragraph('Interface et<br/>atelier développeur',st),p('Dix maquettes pour une refonte complète','intro'),Spacer(1,16),im,Spacer(1,20),p('Conception 0.1 · 2175\nPour Valentin · 20 octobre 2026','body'),p('Écrans, animations, ergonomie, personnalisation et accès aux séquences de test. Les images sont des références de conception ; toutes les fonctions nouvelles restent proposées.','intro'),p('Jeu de référence : v0.6. Aucun code du jeu ni déploiement modifié.','note'),PageBreak()]

def bibliography():
    out=[Heading('Sources de la conception','sources')]
    out.append(p('Références primaires consultées le 20 octobre 2026. Les propositions d’ergonomie et d’équilibrage du présent dossier appartiennent à la conception de No Man’s Land.','intro'))
    for id,title,desc,url in SOURCES:
        out.extend([p(id+'  '+title,'h2'),p(desc,'body'),Paragraph('<link href="'+escape(url)+'" color="#376F70">Ouvrir la source officielle</link>',ST['small'])])
    return out

def main_story():
    story=cover();story.extend([Heading('Sommaire','sommaire',False),p('Les dix images M01 à M10 précèdent les spécifications. Chaque écran et chaque sujet possèdent aussi un signet PDF.','small')])
    toc=TableOfContents();toc.levelStyles=[ParagraphStyle('toc0',fontName='D',fontSize=9.2,leading=14.2,textColor=INK,spaceBefore=0)]
    toc.tableStyle=TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),3)]);toc.dotsMinLevel=0
    story.extend([toc,PageBreak()])
    # Cadre et référence avant les maquettes, puis toutes les spécifications d’application.
    measures=[]
    for idx in range(3):
        for title,flows in fit_content(PAGES[idx],'spec-'+str(idx)):
            measures.append({'title':title,'height':measure(flows)});story.extend(flows);story.append(PageBreak())
    for n,m in enumerate(MOCKUPS):
        story.pop();story.extend([NextPageTemplate('wide'),PageBreak()]);story.extend(visual(m));story.append(PageBreak())
    story.pop();story.extend([NextPageTemplate('normal'),PageBreak()])
    for idx in range(3,len(PAGES)):
        for title,flows in fit_content(PAGES[idx],'spec-'+str(idx)):
            measures.append({'title':title,'height':measure(flows)});story.extend(flows);story.append(PageBreak())
    story.extend(bibliography());story.append(PageBreak())
    provenance=dict(section='Sources',title='Audit et fabrication des références',intro='La rédaction s’appuie sur les sources locales et sur les dix images créées avant la réalisation de l’interface.',blocks=[
        ('Code audité','/workspace/sites/no-mans-land-2175 : dist/app.js, index.html, style.css, hud-v2.css, city-v3.css, world-v5.css, engine.js, data.js, overland.js, city-play.js et expanse-play.js. Instantané 07724023af4978a5c99d9c281c6f76d1cb746e2f. Audit de structure et de logique ; aucune nouvelle validation navigateur n’est revendiquée.'),
        ('Documents du projet','Atlas de conception v0.1 et Gameplay et personnages v0.1. Les lieux, origines, fonctions de PNJ et restrictions du monde y sont distingués des propositions nouvelles. Le fond cartographique de M07 ne remplace pas ces plans.'),
        ('Fabrication des images','Dix références finales produites avec la génération d’images intégrée, sans script d’appel API externe. Deux références ont reçu une correction ciblée de texte : M06 et M10. Les variantes antérieures sont écartées du dossier. Aucun asset des jeux cités n’a été repris.'),
        ('Fichiers de référence','Les références employées sont M01.png à M10.png dans /workspace/scratch/00d29d1aab63/interface-refonte-v01/reference-images. Elles sont intégrées au PDF à leur ratio d’origine. Les prompts exacts et corrections sont reproduits dans l’annexe suivante.'),
        ('Limites d’une image','Ces visuels fixent une direction, des proportions et un vocabulaire graphique. Les chiffres, noms, règles d’accès et objets viennent ensuite des définitions validées du jeu. Les paysages peints ne constituent pas une annonce de moteur 3D ni de reconstruction des villes.'),
        ('Prochaine étape','Transformer les écrans retenus en composants testables et réutilisables, puis appliquer les lots de réalisation. La conception des villes et le code du jeu n’ont pas été touchés pendant cette préparation.')],table=None,note=None)
    story.extend(content(provenance,'provenance'));story.append(PageBreak())
    manifest=json.loads((ROOT/'source/image_manifest.json').read_text())
    for r in manifest:
        flows=[p('ANNEXE  /  PROMPTS EXACTS DE GÉNÉRATION','small'),Heading('M'+r['id']+'  Brief de référence','prompt-'+r['id'],toc=(r['id']=='01')),
            p('Prompt initial','h2'),p(r['prompt'],'prompt')]
        if r.get('correction'):flows.extend([p('Correction finale appliquée','h2'),p(r['correction'],'prompt')])
        # Les annexes longues peuvent continuer ; le contenu de la spécification reste prioritaire.
        story.extend(flows);story.append(PageBreak())
    story.pop()
    (ROOT/'qa/measurements.json').write_text(json.dumps(measures,ensure_ascii=False,indent=2))
    return story

if __name__=='__main__':
    dest=OUT/'No-Mans-Land_Interface-et-Mode-Developpeur_v01.pdf'
    doc=Doc(dest);doc.multiBuild(main_story())
    (ROOT/'qa/page_index.json').write_text(json.dumps(doc.index,ensure_ascii=False,indent=2))
    print(dest);print('Poids MiB',round(dest.stat().st_size/1048576,2));print('Signets',len(doc.index))
