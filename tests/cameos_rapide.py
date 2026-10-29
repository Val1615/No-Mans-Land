# Test rapide des caméos (Ocre au Strip, Rivet sur la ligne, Régie au terminus) : zones chargées, PNJ abordables, répliques, budget d'animations, aucune erreur JS (1280 et 390).
import time,os,sys
from playwright.sync_api import sync_playwright
URL='http://127.0.0.1:8862/'; OUT='/tmp/nml-test-out/cameos/'; os.makedirs(OUT,exist_ok=True); fails=[]; n=0
def ok(c,m,d=''):
    global n; print(('OK   ' if c else 'ECHEC ')+m+('' if c else f'  {d}'),flush=True); n+=c; c or fails.append(m)
CAS=[('steel_strip','fs_ocre',31,14.8,'Recule un peu'),('steel_megaline','ml_rivet',37.4,11,'Ça fonctionne'),('steel_terminus','ml_regie',10,6.5,'Dernier arrêt')]
with sync_playwright() as p:
    br=p.chromium.launch(channel='chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    for name,vp,mob in [('desktop',(1280,800),False),('mobile',(390,844),True)]:
        errs=[]; ctx=br.new_context(viewport={'width':vp[0],'height':vp[1]},has_touch=mob,is_mobile=mob); pg=ctx.new_page(); E=pg.evaluate
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell',timeout=60000); time.sleep(1)
        E("localStorage.removeItem('nml_save_auto')"); E("document.getElementById('m-new').click()"); time.sleep(.5)
        E("document.querySelector('[data-race=\"humain\"]').click()"); time.sleep(.3); E("document.getElementById('cr-next').click()"); time.sleep(.3); E("document.getElementById('cr-enter').click()"); time.sleep(1.5)
        for loc,npc,x,z,txt in CAS:
            E(f"(()=>{{const g=window.__nml.game,s=g.snapshot();s.location='{loc}';s.player.x={x};s.player.z={z};g.restore(s,true)}})()"); time.sleep(2.5)
            ok(E("window.__nml.state.location")==loc,f'{name} {loc} chargée')
            a=E("({...window.__nml.view.animStats})"); ok(a['on']<=(8 if mob else 16) and (not mob or a['on']<=8),f'{name} {loc} : {a["on"]} animations (<= 8 sur mobile)',a)
            pg.screenshot(path=OUT+f'{name}_{npc}.png')
            E(f"window.__nml.game.talkTo('{npc}')"); t0=time.time()
            while time.time()-t0<15 and not E("window.__nml.state.dialogue"): time.sleep(.3)
            t=E("window.__nml.game.currentNode()?.text||''"); ok(txt in t,f'{name} {npc} : première réplique',t)
            pg.screenshot(path=OUT+f'{name}_{npc}_dialogue.png'); E("window.__nml.game.choose(window.__nml.game.currentNode().options.at(-1).index)"); time.sleep(.3)
        ok(not errs,f'{name} aucune erreur JS',errs[:3]); ctx.close()
    print(f'{n}/{n+len(fails)} OK'); print('ECHECS',len(fails)); sys.exit(1 if fails else 0)
