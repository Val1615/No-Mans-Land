# Test rapide Pulse Plaza : la zone se charge depuis Center-Town, se traverse (ouest -> sud), aucune erreur JS (1280 et 390).
# Chantier pilote (PILOTE.md) : 9 PNJ nommés, 8 figurants distincts sans clone, aucune étiquette sur les accès, écran du Feed allumé (pixels),
# budget d'animations (view.animStats, 8 au plus sur mobile), accès ouest et jonction de Fréquence Strip libres ; captures sous l'angle du concept.
import time,os,sys,io
from PIL import Image
from playwright.sync_api import sync_playwright
URL=os.environ.get('URL','http://127.0.0.1:8862/'); OUT='/tmp/nml-test-out/pulse/'; CAP='/tmp/nml-test-out/pulse_pilote/'; os.makedirs(OUT,exist_ok=True); os.makedirs(CAP,exist_ok=True); fails=[]; n=0
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
        L=E("(()=>{const l=window.__nml.world.LOCATIONS.steel_pulse;return {ex:l.extras.map(e=>e.sprite),wk:l.walkers.map(w=>w.sprite),skin:l.ground.skin,paint:(l.ground.paint||[]).map(r=>r.skin)}})()")
        ok(len(L['ex'])==8 and len(set(L['ex']+L['wk']))==len(L['ex']+L['wk']) and all(x.startswith('gen_pp_foule_') and x[-1] in 'cdefghij' for x in L['ex']),f'{name} 8 figurants distincts, aucun clone',L)
        ok(L['skin']=='g_pp_dalle_sombre' and 'g_pp_allee' in L['paint'],f'{name} dalle sombre et allées (ground.paint)',L['skin'])
        ok(E("document.querySelectorAll('.wlabel.junction,.wlabel.edge').length")==0 and E("[...document.querySelectorAll('.wlabel')].every(l=>!/Escalier|Center-Town|Strip/.test(l.textContent))"),f'{name} aucune étiquette sur les accès')
        ppm=13 if mob else 22; E(f"window.__nml.view.setCamera({{x:24,z:17,ppm:{ppm}}})"); time.sleep(2.5)
        a=E("window.__nml.project(32,0,12)"); cx,cy=a['x']-4.98*ppm,a['y']-7.84*ppm
        im=Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); px=[im.getpixel((int(cx)+i,int(cy)+j)) for i in range(-10,11,2) for j in range(-10,11,2)]
        lum=sum(sum(c) for c in px)/len(px)/3; ok(lum>40,f'{name} écran du Feed allumé (luminance {lum:.0f})',(cx,cy))
        pg.screenshot(path=CAP+f'concept_{vp[0]}.png'); E("window.__nml.view.setCamera(null)"); time.sleep(1)
        st=E("window.__nml.view.animStats"); ok(st.get('on',0)<=(8 if mob else 16),f'{name} budget d animations {st}')
        def acces(x0,z0,x1,z1,dest):
            E(f"(()=>{{const g=window.__nml.game,s=g.snapshot();s.location='steel_pulse';s.player.x={x0};s.player.z={z0};g.restore(s,true)}})()"); time.sleep(1); E(f"window.__nml.game.moveTo({x1},{z1})"); t0=time.time()
            while time.time()-t0<20 and E("window.__nml.state.location")=='steel_pulse': time.sleep(.3)
            return E("window.__nml.state.location")
        loc=acces(40,16,47,13,'steel_strip'); ok(loc=='steel_strip',f'{name} jonction Fréquence Strip libre (à pied)',loc)
        loc=acces(8,16,1,16,'steel_center'); ok(loc=='steel_center',f'{name} accès ouest libre (à pied vers Center-Town)',loc)
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_pulse';s.player.x=3;s.player.z=16;g.restore(s,true)})()"); time.sleep(1.5)
        pg.screenshot(path=CAP+f'acces_ouest_{vp[0]}.png')
        E("window.__nml.game.moveTo(24,33)"); t0=time.time()
        while time.time()-t0<40 and E("(()=>{const p=window.__nml.state.player;return Math.hypot(p.x-24,p.z-33)>1.2})()"): time.sleep(.3)
        pz=E("[window.__nml.state.player.x,window.__nml.state.player.z]"); ok(abs(pz[0]-24)<1.3 and abs(pz[1]-33)<1.3,f'{name} traversée ouest -> escalier sud à pied',pz)
        pg.screenshot(path=OUT+f'{name}_traversee.png'); time.sleep(1.5) # fin du trajet en cours avant de prendre la porte (sinon il continue dans Center-Town)
        E("window.__nml.game.useDoor('pp_sud')"); t0=time.time()
        while time.time()-t0<8 and E("[window.__nml.state.location,Math.round(window.__nml.state.player.x)]")!=['steel_center',26]: time.sleep(.3)
        pz=E("[window.__nml.state.location,Math.round(window.__nml.state.player.x)]"); ok(pz==['steel_center',26],f'{name} sortie sud -> Escalier de Pulse Plaza (Center-Town)',pz)
        E("window.__nml.game.useDoor('c_pp_sud')"); time.sleep(2); ok(E("window.__nml.state.location")=='steel_pulse',f'{name} retour Escalier de Pulse Plaza -> Pulse Plaza',E("window.__nml.state.location"))
        ok(not errs,f'{name} aucune erreur JS',errs[:3]); ctx.close()
    print(f'{n}/{n+len(fails)} OK'); print('ECHECS',len(fails)); sys.exit(1 if fails else 0)
