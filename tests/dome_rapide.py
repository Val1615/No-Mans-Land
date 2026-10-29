# Test rapide Dôme Fréquence : porte fermée sans le drapeau, accès de debug, intérieur (chargement, traversée, sortie), Center-Town, aucune erreur JS (1280 et 390).
import time,os,sys
from playwright.sync_api import sync_playwright
URL=os.environ.get('URL','http://127.0.0.1:8862/'); OUT='/tmp/nml-test-out/dome/'; os.makedirs(OUT,exist_ok=True); fails=[]; n=0
def ok(c,m,d=''):
    global n; print(('OK   ' if c else 'ECHEC ')+m+('' if c else f'  {d}'),flush=True); n+=c; c or fails.append(m)
with sync_playwright() as p:
    br=p.chromium.launch(channel='chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    for name,vp,mob in [('desktop',(1280,800),False),('mobile',(390,844),True)]:
        errs=[]; ctx=br.new_context(viewport={'width':vp[0],'height':vp[1]},has_touch=mob,is_mobile=mob); pg=ctx.new_page(); E=pg.evaluate
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell',timeout=60000); time.sleep(1)
        E("localStorage.removeItem('nml_save_auto')"); E("document.getElementById('m-new').click()"); time.sleep(.5)
        E("document.querySelector('[data-race=\"humain\"]').click()"); time.sleep(.3); E("document.getElementById('cr-next').click()"); time.sleep(.3); E("document.getElementById('cr-enter').click()"); time.sleep(1.5)
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_center';s.player.x=23.5;s.player.z=15;g.restore(s,true)})()"); time.sleep(2)
        st=E("({...window.__nml.view.animStats})"); print('   center',st); ok(st['total']==2,f'{name} Center-Town : 2 écrans de façade animés sur c_tour',st)
        pg.screenshot(path=OUT+f'{name}_facade.png')
        E("window.__nml.game.useDoor('c_dome')"); time.sleep(1.5); ok(E("window.__nml.state.location")=='steel_center',f'{name} porte du Dôme fermée sans le drapeau')
        ok(E("window.__nml.ouvrirDome()"),f'{name} accès de debug'); E("window.__nml.game.useDoor('c_dome')"); time.sleep(2)
        ok(E("window.__nml.state.location")=='steel_dome',f'{name} entrée dans le Dôme',E("window.__nml.state.location"))
        ok(E("window.__nml.game.world.NPCS.filter(n=>n.location==='steel_dome').length")==10,f'{name} 10 PNJ')
        pg.screenshot(path=OUT+f'{name}_foyer.png')
        E("window.__nml.game.moveTo(18,7.5)"); t0=time.time()
        while time.time()-t0<40 and E("(()=>{const p=window.__nml.state.player;return Math.hypot(p.x-18,p.z-7.5)>1.2})()"): time.sleep(.3)
        pz=E("[window.__nml.state.player.x,window.__nml.state.player.z]"); ok(abs(pz[0]-18)<1.3 and abs(pz[1]-7.5)<1.3,f'{name} traversée foyer -> bord de scène',pz)
        fps=E("new Promise(r=>{let k=0;const t0=performance.now();const f=()=>{k++;if(performance.now()-t0<3000)requestAnimationFrame(f);else r(k*1000/(performance.now()-t0))};requestAnimationFrame(f)})")
        st=E("({...window.__nml.view.animStats})"); print(f'   {name} fps={fps:.1f} dome {st}'); pg.screenshot(path=OUT+f'{name}_scene.png')
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=15;s.player.z=28.6;g.restore(s,true)})()"); time.sleep(1); E("window.__nml.game.useDoor('df_sortie')"); time.sleep(2)
        pz=E("[window.__nml.state.location,Math.round(window.__nml.state.player.x*2)/2]"); ok(pz[0]=='steel_center',f'{name} sortie du Dôme -> porte de c_tour',pz)
        ok(not errs,f'{name} aucune erreur JS',errs[:3]); ctx.close()
    print(f'{n}/{n+len(fails)} OK'); print('ECHECS',len(fails)); sys.exit(1 if fails else 0)
