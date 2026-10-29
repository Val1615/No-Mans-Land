# Test rapide Mega-Line et terminus : Center-Town -> ligne (c_mega), traversée, passerelle -> terminus, traversée, retours, budget d'animations, aucune erreur JS (1280 et 390).
import time,os,sys
from playwright.sync_api import sync_playwright
URL=os.environ.get('URL','http://127.0.0.1:8862/'); OUT='/tmp/nml-test-out/mega/'; os.makedirs(OUT,exist_ok=True); fails=[]; n=0
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
        tp=lambda loc,x,z: E(f"(()=>{{const g=window.__nml.game,s=g.snapshot();s.location='{loc}';s.player.x={x};s.player.z={z};g.restore(s,true)}})()")
        def walk(x,z,t=40):
            E(f"window.__nml.game.moveTo({x},{z})"); t0=time.time()
            while time.time()-t0<t and E(f"(()=>{{const p=window.__nml.state.player;return Math.hypot(p.x-{x},p.z-{z})>1.2}})()"): time.sleep(.3)
            p_=E("[window.__nml.state.player.x,window.__nml.state.player.z]"); return abs(p_[0]-x)<1.3 and abs(p_[1]-z)<1.3, p_
        loc=lambda: E("window.__nml.state.location"); st=lambda: E("({...window.__nml.view.animStats})")
        tp('steel_center',8,2); time.sleep(1.5); E("window.__nml.game.useDoor('c_mega')"); time.sleep(2)
        ok(loc()=='steel_megaline',f'{name} Center-Town (c_mega) -> Mega-Line',loc())
        r,pz=walk(24,18); ok(r,f'{name} ligne : marche jusqu au quai',pz); time.sleep(3); a=st(); print(f'   {name} ligne {a}')
        ok(a['on']<=5,f'{name} ligne : {a["on"]} animations (<= 5)',a); pg.screenshot(path=OUT+f'{name}_ligne.png')
        r,pz=walk(46,2.5,60); ok(r,f'{name} ligne traversée jusqu a la passerelle',pz)
        E("window.__nml.game.useDoor('ml_passerelle')"); time.sleep(2); ok(loc()=='steel_terminus',f'{name} passerelle -> terminus',loc())
        r,pz=walk(15,5.2); ok(r,f'{name} terminus : traversée jusqu au panneau',pz); time.sleep(2); a=st(); print(f'   {name} terminus {a}')
        ok(a['on']<=3,f'{name} terminus : {a["on"]} animations (<= 3)',a)
        lab=E("[...document.querySelectorAll('#labels *')].map(e=>e.textContent).filter(t=>t.includes('Dernier arrêt'))"); ok(bool(lab),f'{name} panneau « Dernier arrêt avant No Man\u2019s Land » affiché par le code',lab)
        pg.screenshot(path=OUT+f'{name}_terminus_panneau.png')
        tp('steel_terminus',15,18.6); time.sleep(1); E("window.__nml.game.useDoor('tm_sud')"); time.sleep(2); ok(loc()=='steel_megaline',f'{name} retour terminus -> ligne',loc())
        tp('steel_megaline',24,22.6); time.sleep(1); E("window.__nml.game.useDoor('ml_sud')"); time.sleep(2); ok(loc()=='steel_center',f'{name} retour ligne -> Center-Town',loc())
        ok(not errs,f'{name} aucune erreur JS',errs[:3]); ctx.close()
    print(f'{n}/{n+len(fails)} OK'); print('ECHECS',len(fails)); sys.exit(1 if fails else 0)
