# Test rapide Pulse Plaza : la zone se charge depuis Center-Town, se traverse (ouest -> sud), aucune erreur JS (1280 et 390).
import time,os,sys
from playwright.sync_api import sync_playwright
URL=os.environ.get('URL','http://127.0.0.1:8862/'); OUT='/tmp/nml-test-out/pulse/'; os.makedirs(OUT,exist_ok=True); fails=[]; n=0
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
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_center';s.player.x=33;s.player.z=2;g.restore(s,true)})()"); time.sleep(1.2)
        E("window.__nml.game.useDoor('c_nord')"); time.sleep(2)
        ok(E("window.__nml.state.location")=='steel_pulse',f'{name} porte Center-Town -> Pulse Plaza',E("window.__nml.state.location"))
        pg.screenshot(path=OUT+f'{name}_arrivee.png')
        ok(E("window.__nml.game.world.NPCS.filter(n=>n.location==='steel_pulse').length")==9,f'{name} 9 PNJ')
        E("window.__nml.game.moveTo(24,33)"); t0=time.time()
        while time.time()-t0<40 and E("(()=>{const p=window.__nml.state.player;return Math.hypot(p.x-24,p.z-33)>1.2})()"): time.sleep(.3)
        pz=E("[window.__nml.state.player.x,window.__nml.state.player.z]"); ok(abs(pz[0]-24)<1.3 and abs(pz[1]-33)<1.3,f'{name} traversée ouest -> escalier sud à pied',pz)
        pg.screenshot(path=OUT+f'{name}_traversee.png')
        E("window.__nml.game.useDoor('pp_sud')"); time.sleep(2); pz=E("[window.__nml.state.location,Math.round(window.__nml.state.player.x)]"); ok(pz==['steel_center',26],f'{name} sortie sud -> Escalier de Pulse Plaza (Center-Town)',pz)
        E("window.__nml.game.useDoor('c_pp_sud')"); time.sleep(2); ok(E("window.__nml.state.location")=='steel_pulse',f'{name} retour Escalier de Pulse Plaza -> Pulse Plaza',E("window.__nml.state.location"))
        ok(not errs,f'{name} aucune erreur JS',errs[:3]); ctx.close()
    print(f'{n}/{n+len(fails)} OK'); print('ECHECS',len(fails)); sys.exit(1 if fails else 0)
