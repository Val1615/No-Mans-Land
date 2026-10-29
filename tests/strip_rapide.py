# Test rapide Fréquence Strip : Pulse Plaza -> Strip (porte est), traversée jusqu'à la grille est, retour, aucune erreur JS ; fps et enseignes animées (1280 et 390).
import time,os,sys
from playwright.sync_api import sync_playwright
URL=os.environ.get('URL','http://127.0.0.1:8862/'); OUT='/tmp/nml-test-out/strip/'; os.makedirs(OUT,exist_ok=True); fails=[]; n=0
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
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_pulse';s.player.x=46;s.player.z=13;g.restore(s,true)})()"); time.sleep(1.2)
        E("window.__nml.game.useDoor('pp_est')"); time.sleep(2)
        ok(E("window.__nml.state.location")=='steel_strip',f'{name} Pulse Plaza (sortie est) -> Fréquence Strip',E("window.__nml.state.location"))
        ok(E("window.__nml.game.world.NPCS.filter(n=>n.location==='steel_strip').length")==10,f'{name} 10 PNJ (dont Fusible)')
        pg.screenshot(path=OUT+f'{name}_arrivee.png')
        E("window.__nml.game.moveTo(30,12)"); time.sleep(6); pg.screenshot(path=OUT+f'{name}_milieu.png')
        fps=E("new Promise(r=>{let k=0;const t0=performance.now();const f=()=>{k++;if(performance.now()-t0<3000)requestAnimationFrame(f);else r(k*1000/(performance.now()-t0))};requestAnimationFrame(f)})")
        st=E("({...window.__nml.view.animStats})"); print(f'   {name} fps={fps:.1f} enseignes animées {st}')
        ok(st['total']==9 and st['on']<=(8 if mob else 16) and st['on']>0,f'{name} enseignes : {st["on"]} animées sur {st["total"]} (plafond {"8" if mob else "16"})',st)
        E("window.__nml.game.moveTo(58,12)"); t0=time.time()
        while time.time()-t0<40 and E("(()=>{const p=window.__nml.state.player;return Math.hypot(p.x-58,p.z-12)>1.2})()"): time.sleep(.3)
        pz=E("[window.__nml.state.player.x,window.__nml.state.player.z]"); ok(abs(pz[0]-58)<1.3 and abs(pz[1]-12)<1.3,f'{name} traversée ouest -> est à pied',pz)
        pg.screenshot(path=OUT+f'{name}_est.png')
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=2;s.player.z=10;g.restore(s,true)})()"); time.sleep(1); E("window.__nml.game.useDoor('fs_ouest')"); time.sleep(2); ok(E("window.__nml.state.location")=='steel_pulse',f'{name} retour vers Pulse Plaza',E("window.__nml.state.location"))
        ok(not errs,f'{name} aucune erreur JS',errs[:3]); ctx.close()
    print(f'{n}/{n+len(fails)} OK'); print('ECHECS',len(fails)); sys.exit(1 if fails else 0)
