# Lot 2 interface : carte de Steel-Megalopolis (1280x800 et 390x844). Ouverture (M / icône carte), 4 couches empilées, couche du joueur par défaut,
# marqueur du joueur sur la bonne couche, Upper-Town désaturée et verrouillée (non cliquable), découverts / silhouettes « ? », passages entre couches,
# molette et flèches, Asia-Ground au sud de Lower-Town, Sous-Ville distincte de Lower-Town, carte de Dusk-Town inchangée hors de Steel, aucune erreur JS.
import time,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from _chev import chevauchements
from playwright.sync_api import sync_playwright
OUT='/tmp/nml-test-out/cartes/'; os.makedirs(OUT,exist_ok=True); fails=[]; errs=[]; n_ok=0
def ok(c,m,d=''):
    global n_ok
    print(('OK   ' if c else 'ECHEC ')+m+(f'  {d}' if d!='' and not c else ''))
    if c: n_ok+=1
    else: fails.append(m)
with sync_playwright() as p:
    br=p.chromium.launch(channel='chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    for name,vp,mob in [('desktop',(1280,800),False),('mobile',(390,844),True)]:
        ctx=br.new_context(viewport={'width':vp[0],'height':vp[1]},has_touch=mob,is_mobile=mob,device_scale_factor=1); pg=ctx.new_page(); E=pg.evaluate
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
        pg.goto(os.environ.get('URL','http://127.0.0.1:8862/')); pg.wait_for_function('window.__nml && window.__nml.shell',timeout=60000); time.sleep(1.5)
        E("document.getElementById('m-new').click()"); time.sleep(.5); E("document.querySelector('[data-race=\"augmente\"]').click()"); time.sleep(.3); E("document.getElementById('cr-next').click()"); time.sleep(.3); E("document.getElementById('cr-enter').click()"); time.sleep(1.5)
        def go(loc,x,z,seen=()):
            E(f"(()=>{{const g=window.__nml.game,s=g.snapshot();s.location='{loc}';s.player.x={x};s.player.z={z};s.seen={{}};for(const k of {list(seen)!r})s.seen[k]=true;g.restore(s,true)}})()"); time.sleep(1.2)
        smap="(()=>{const m=document.querySelector('#panel .smap');if(!m||document.getElementById('panel').hidden)return null;const P=m.querySelector('.smap-plan').getBoundingClientRect();return {couche:+m.dataset.n,sel:[...m.querySelectorAll('.smap-pile button')].map(b=>[+b.dataset.couche,b.classList.contains('sel'),b.classList.contains('lock')]),here:[...m.querySelectorAll('.mk.here')].map(b=>b.dataset.key),me:m.querySelectorAll('.mk .me').length,known:[...m.querySelectorAll('.mk.known')].map(b=>b.dataset.key),unk:[...m.querySelectorAll('.mk.unk')].map(b=>[b.dataset.key,b.textContent]),locked:m.querySelector('.smap-plan').classList.contains('locked'),filt:getComputedStyle(m.querySelector('.fond')).filter,mkPE:[...m.querySelectorAll('.mk')].map(b=>getComputedStyle(b).pointerEvents),pos:Object.fromEntries([...m.querySelectorAll('.mk')].map(b=>{const r=b.getBoundingClientRect();return [b.dataset.key,[r.left,r.top]]})),plan:[P.left,P.top,P.right,P.bottom],vw:innerWidth,vh:innerHeight,bg:getComputedStyle(document.getElementById('panel')).backgroundColor}})()"
        # Asia-Ground : ouverture par l'icône carte (mobile) ou M (ordinateur), couche 2 par défaut
        go('steel_asia',24,20,['steel_asia','steel_lower'])
        if mob: E("document.getElementById('k-carte').click()")
        else: pg.keyboard.press('m')
        time.sleep(.5); m=E(smap)
        ok(m is not None,f'{name} carte de Steel ouverte ({"icône" if mob else "touche M"})')
        if not m: continue
        ok(m['couche']==2 and [c for c,s,l in m['sel'] if s]==[2],f'{name} couche du joueur (2, Lower-Town) ouverte par défaut',m['couche'])
        ok([c for c,_,_ in m['sel']]==[4,3,2,1],f'{name} 4 couches empilées (4 en haut, 1 en bas)',m['sel'])
        ok(m['here']==['steel_asia'] and m['me']==1,f'{name} marqueur du joueur sur Asia-Ground',m['here'])
        ok(m['pos']['steel_asia'][1]>m['pos']['steel_lower'][1],f'{name} Asia-Ground au sud de Lower-Town')
        time.sleep(.4)
        fog=E("""(()=>{const f=document.querySelector('.smap-plan .fog');if(!f||!f.dataset.pret)return null;const M=window.__nml.mapsMan,c=M.steel.couches[1].reperes_px_proposition,k=f.width/M.steel.px[0],x=f.getContext('2d');
          const a=p=>x.getImageData(Math.round(p[0]*k),Math.round(p[1]*k),1,1).data[3];return {trous:JSON.parse(f.dataset.holes).length,liste:document.querySelector('.smap-liste').textContent,china:a(c.steel_china),asia:a(c.steel_asia)}})()""")
        ok('steel_china' not in m['pos'] and not m['unk'] and fog and fog['trous']==len(m['known']) and 'China' not in fog['liste'] and fog['china']>200 and fog['asia']<40,f'{name} China Lake non découvert : sous le brouillard bleu (ni repère ni nom), Asia-Ground dégagé',(m['unk'],fog))
        ok(all(0<=v[0] and v[0]<=m['vw'] for v in m['pos'].values()) and m['plan'][2]<=m['vw']+.5 and m['plan'][3]<=m['vh']+.5,f'{name} plan et repères dans l écran',m['plan'])
        a=float(m['bg'].split(',')[3].strip(' )')) if m['bg'].count(',')==3 else 1
        ok(a<0.8,f'{name} panneau semi-transparent ({m["bg"]})')
        pg.screenshot(path=OUT+f'steel_{name}_lower.png')
        # passage vers la Sous-Ville (clic sur le repère), puis molette / flèches vers le haut
        E("document.querySelector('.mk[data-key=\"lt_acces_sous_ville\"]').click()"); time.sleep(.3); m=E(smap)
        ok(m['couche']==1 and m['me']==0 and 'steel_asia' not in m['pos'] and 'sv_poutres' not in m['pos'] and 'sv_fosse' in m['pos'],f'{name} passage vers la couche 1 (Sous-Ville distincte, inexplorée : brouillard sauf l arrivée de la Fosse)',(m['couche'],list(m['pos'])))
        if mob: E("document.querySelector('.smap-pile [data-couche=\"3\"]').click()")
        else:
            b=E("(()=>{const r=document.querySelector('.smap-plan').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()"); pg.mouse.move(b[0],b[1]); pg.mouse.wheel(0,-120); time.sleep(.4); pg.mouse.wheel(0,-120); time.sleep(.4)
        m=E(smap); ok(m['couche']==3,f'{name} couche 3 ({"onglet" if mob else "molette"})',m['couche'])
        ov=E("(()=>{const R=[...document.querySelectorAll('#panel .smap .mk')].flatMap(b=>[...b.children].map(e=>[b.dataset.key+':'+e.tagName,e.getBoundingClientRect()])).filter(([,r])=>r.width>0);const o=[];for(let i=0;i<R.length;i++)for(let j=i+1;j<R.length;j++){const[a,r]=R[i],[b,s]=R[j];if(a.split(':')[0]===b.split(':')[0])continue;const w=Math.min(r.right,s.right)-Math.max(r.left,s.left),h=Math.min(r.bottom,s.bottom)-Math.max(r.top,s.top);if(w>1&&h>1)o.push(a+'/'+b)}return o})()"); ok(not ov,f'{name} couche 3 : aucun libellé ni icône ne se chevauchent',ov)
        # Upper-Town : verrouillée, désaturée, repères non cliquables
        if mob: E("document.querySelector('.smap-pile [data-couche=\"4\"]').click()")
        else: pg.keyboard.press('ArrowUp')
        time.sleep(.3); m=E(smap)
        ok(m['couche']==4 and m['locked'] and 'grayscale' in m['filt'] and all(v=='none' for v in m['mkPE']) and [l for c,_,l in m['sel'] if c==4]==[True],f'{name} Upper-Town affichée désaturée et verrouillée, non cliquable',(m['couche'],m['filt'],m['mkPE']))
        ok(E("!!document.querySelector('.smap-plan .lockmsg img[src*=verrouille]')"),f'{name} icône verrou sur Upper-Town')
        pg.screenshot(path=OUT+f'steel_{name}_upper.png')
        if not mob: pg.keyboard.press('ArrowDown'); time.sleep(.3); ok(E(smap)['couche']==3,f'{name} flèche bas -> couche 3')
        E("document.getElementById('panel-close').click()"); time.sleep(.3)
        # Center-Town : marqueur couche 3 ; Sous-Ville : couche 1 ; intérieur de la douane : couche 3 (douane)
        for loc,x,z,c,key in [('steel_center',24,20,3,'steel_center'),('sv_poutres',18,14,1,'sv_poutres'),('douane_in',5,4,3,'steel_route')]:
            go(loc,x,z,[loc]); E("document.getElementById('k-carte').click()"); time.sleep(.4); m=E(smap)
            ok(m and m['couche']==c and m['here']==[key] and m['me']==1,f'{name} {loc} : couche {c}, marqueur sur {key}',m and (m['couche'],m['here']))
            if loc=='steel_center': pg.screenshot(path=OUT+f'steel_{name}_center.png')
            E("document.getElementById('panel-close').click()"); time.sleep(.2)
        # Dusk-Town : ancienne carte des quartiers
        go('dusk_q1',20,20,['dusk_q1']); E("document.getElementById('k-carte').click()"); time.sleep(.4)
        ok(E("!document.querySelector('#panel .smap') && document.querySelector('#panel h3').textContent.includes('DUSK')"),f'{name} Dusk-Town : carte des quartiers')
        # tout découvert (tous les lieux vus) : sur chaque couche, aucun libellé ni icône ne se chevauchent
        E("document.getElementById('panel-close').click()"); time.sleep(.3)
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_center';for(const k of Object.keys(window.__nml.world.LOCATIONS))s.seen[k]=true;g.restore(s,true)})()"); time.sleep(1.2)
        if mob: E("document.getElementById('k-carte').click()")
        else: pg.keyboard.press('m')
        time.sleep(.6)
        for c in (1,2,3):
            E(f"document.querySelector('.smap-pile [data-couche=\"{c}\"]').click()"); time.sleep(.6)
            n=E("document.querySelectorAll('#panel .smap .mk.known').length"); ov=chevauchements(E,'#panel .smap .mk')
            ok(E(smap)['couche']==c and n>0 and not ov,f'{name} tout découvert, couche {c} ({n} repères) : aucun chevauchement libellé/icône',ov)
            pg.screenshot(path=OUT+f'steel_{name}_tout_couche{c}.png')
        E("document.getElementById('panel-close').click()"); ctx.close()
    ok(not errs,'aucune erreur JS',errs[:3])
    print(f'{n_ok}/{n_ok+len(fails)} OK'); print('ECHECS',len(fails)); sys.exit(1 if fails else 0)
