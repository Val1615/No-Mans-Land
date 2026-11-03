# Test rapide des enseignes animées par le code (loc.enseignes) et des projecteurs de la Steel Arena (loc.projecteurs), serveur local 8862.
# Vérifie : démo DEV des enseignes visible seulement avec ?dev=1, luminosité qui varie, faisceaux qui balaient, budget mobile animStats.on <= 8
# (enseignes et projecteurs comptés à part), schéma de l'éditeur (enseigne ou projecteur invalide refusé), aucune erreur JS.
import time,os,sys,json
from playwright.sync_api import sync_playwright
URL=os.environ.get('URL','http://127.0.0.1:8862/'); OUT='/tmp/nml-test-out/strip_arena_prep/'; os.makedirs(OUT,exist_ok=True); fails=[]; n=0
def ok(c,m,d=''):
    global n; print(('OK   ' if c else 'ECHEC ')+m+('' if c else f'  {d}'),flush=True); n+=c; c or fails.append(m)
def start(pg,q):
    E=pg.evaluate; pg.goto(URL+q); pg.wait_for_function('window.__nml && window.__nml.shell',timeout=60000); time.sleep(1)
    E("localStorage.removeItem('nml_save_auto')"); E("document.getElementById('m-new').click()"); time.sleep(.5)
    E("document.querySelector('[data-race=\"humain\"]').click()"); time.sleep(.3); E("document.getElementById('cr-next').click()"); time.sleep(.3); E("document.getElementById('cr-enter').click()"); time.sleep(1.5)
def go(pg,zone,x,z): pg.evaluate(f"(()=>{{const g=window.__nml.game,s=g.snapshot();s.location='{zone}';s.player.x={x};s.player.z={z};g.restore(s,true)}})()"); time.sleep(2)
with sync_playwright() as p:
    br=p.chromium.launch(channel='chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    for name,vp,mob in [('390',(390,844),True),('1280',(1280,800),False)]:
        errs=[]; ctx=br.new_context(viewport={'width':vp[0],'height':vp[1]},has_touch=mob,is_mobile=mob); pg=ctx.new_page(); E=pg.evaluate
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
        start(pg,''); go(pg,'steel_strip',16,10)
        ok(E("window.__nml.view.animStats.enseignes")==12,f'{name} : sans ?dev=1 : 10 calques _neon d Ocre (L Effeuillée en 3 morceaux), démo absente, répétitions éteintes',E("window.__nml.view.animStats.enseignes"))
        start(pg,'?dev=1'); go(pg,'steel_strip',16,10)
        st=E("window.__nml.view.animStats"); ok(st['enseignes']==16,f'{name} : Strip ?dev=1 : + démo Neon-7 (3 morceaux) et Retour',st)
        a=[E("window.__nml.view.codeAnims().neons") for _ in range(12) if not time.sleep(.15)]
        ok(len({tuple(x) for x in a})>2 and all(0<=v<=1 for x in a for v in x),f'{name} : luminosité des contours animée par le code',a[:3])
        if mob: ok(st['on']<=8,f'{name} : budget mobile animStats.on <= 8 (Strip, enseignes code hors budget)',st)
        pg.screenshot(path=OUT+f'test_strip_enseignes_dev_{name}.png')
        go(pg,'steel_arena',26,40); st=E("window.__nml.view.animStats")
        ok(st['projecteurs']==4,f'{name} : Arena : 4 projecteurs code',st)
        b0=E("window.__nml.view.codeAnims().beams"); time.sleep(1.5); b1=E("window.__nml.view.codeAnims().beams")
        ok(len(b0)==4 and all(abs(x-y)>1e-3 for x,y in zip(b0,b1)) and len(set(b1))==4,f'{name} : faisceaux qui balaient, mouvements décalés',(b0,b1))
        if mob: ok(st['on']<=8,f'{name} : budget mobile animStats.on <= 8 (Arena, projecteurs hors budget)',st)
        pg.screenshot(path=OUT+f'test_arena_projecteurs_{name}.png')
        E("document.body.classList.add('reduce-motion')"); time.sleep(.3); b0=E("window.__nml.view.codeAnims().beams"); time.sleep(1); b1=E("window.__nml.view.codeAnims().beams")
        ok(b0==b1,f'{name} : mouvement réduit : faisceaux figés'); E("document.body.classList.remove('reduce-motion')")
        if not mob:
            r=E("""async()=>{const {loadEditorSource}=await import('/editor/source.js');const {initial,validate}=await import('/editor/model.js');const {base}=await loadEditorSource();
              const t=(f)=>{const d=initial(base);f(d.locations);try{validate(d,base);return 'accepté';}catch(e){return e.message;}};
              return {bon:t(()=>{}),effet:t(L=>L.steel_strip.enseignes[0].effet='danse'),bat:t(L=>L.steel_strip.enseignes[1].building='inconnu'),neon:t(L=>L.steel_strip.enseignes[0].neon='fs_absent_neon'),
                proj:t(L=>L.steel_arena.projecteurs[0].building='inconnu'),coul:t(L=>L.steel_arena.projecteurs[1].couleur='rouge')};}""")
            ok(r['bon']=='accepté','éditeur : enseignes et projecteurs du jeu acceptés par le schéma',r['bon'])
            ok(all('enseignes' in r[k] for k in ['effet','bat','neon']) and all('projecteurs' in r[k] for k in ['proj','coul']),'éditeur : effet, bâtiment, calque, position ou couleur invalides refusés',r)
        if not mob:  # format d'Ocre branché sans déclaration : une façade avec calque <clé>_neon et un pylône à source_faisceau_px posés à la volée
            E("""(()=>{const L=window.__nml.world.LOCATIONS,B=(id,sprite,x,z,w,d)=>({id,label:'',sprite,x,z,w,d,visitable:false,cue:null,named:false,solid:[]});
              L.steel_arena.buildings.push(B('t_pyl','ar_pylone_projecteur',30,32,1.5,1.5));})()"""); go(pg,'steel_strip',2,10)
            go(pg,'steel_arena',26,40); src=E("window.__nml.view.codeAnims().sources"); st=E("window.__nml.view.animStats")
            py=[q for q in src if abs(q[2]-33.5)<0.5 and abs(q[0]-31.5)<0.5]; ok(st['projecteurs']==5 and len(py)==1 and 9<py[0][1]<12.5,'pylône : faisceau tiré depuis source_faisceau_px (lentilles à ~10 m)',(st,src))
            pg.screenshot(path=OUT+'test_format_ocre_pylone_1280.png')
        ok(not errs,f'{name} : aucune erreur JS',errs[:3]); ctx.close()
    br.close()
print(f'\n{n}/{n+len(fails)} OK' + ('' if not fails else ' — ECHECS : '+'; '.join(fails)))
sys.exit(1 if fails else 0)
