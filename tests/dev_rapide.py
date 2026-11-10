# Test rapide du mode DEV : absent sans ?dev=1 (ni panneau ni module chargé) ; avec ?dev=1 : Déplacement (zone, porte, PNJ), Réinitialisation (instantané, restauration),
# sauvegardes du joueur intactes (emplacements DEV séparés), aucune erreur JS, en 1280 et 390.
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from nml_boot import passer_boot  # menu Terminal : sauter l'allumage
import time,os,sys,json
from playwright.sync_api import sync_playwright
URL=os.environ.get('URL','http://127.0.0.1:8862/'); OUT='/tmp/nml-test-out/dev/'; os.makedirs(OUT,exist_ok=True); fails=[]; n=0
def ok(c,m,d=''):
    global n; print(('OK   ' if c else 'ECHEC ')+m+('' if c else f'  {d}'),flush=True); n+=c; c or fails.append(m)
with sync_playwright() as p:
    br=p.chromium.launch(channel='chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    for name,vp,mob in [('desktop',(1280,800),False),('mobile',(390,844),True)]:
        errs=[]; reqs=[]; ctx=br.new_context(viewport={'width':vp[0],'height':vp[1]},has_touch=mob,is_mobile=mob); pg=ctx.new_page(); E=pg.evaluate
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:m.type=='error' and errs.append(m.text)); pg.on('request',lambda r:reqs.append(r.url))
        def demarrer(q):
            pg.goto(URL+q); pg.wait_for_function('window.__nml && window.__nml.shell',timeout=60000); time.sleep(1.5)
        demarrer('')
        ok(E("!document.getElementById('dev') && !window.__nml.dev") and not any('ui/dev.js' in u for u in reqs),f'{name} sans ?dev=1 : panneau absent, module non chargé')
        # sauvegarde du joueur témoin
        E("localStorage.setItem('nml_save_1', JSON.stringify({v:1,t:1,label:'témoin',state:{}})); localStorage.setItem('nml_save_auto','TEMOIN_AUTO')")
        avant=E("Object.fromEntries(Object.keys(localStorage).filter(k=>k.startsWith('nml_save_')).map(k=>[k,localStorage.getItem(k)]))")
        demarrer('?dev=1'); pg.wait_for_function('window.__nml.dev',timeout=20000)
        passer_boot(E); E("document.getElementById('m-new').click()"); time.sleep(.5); E("document.querySelector('[data-race=\"humain\"]').click()"); time.sleep(.3); E("document.getElementById('cr-next').click()"); time.sleep(.3); E("document.getElementById('cr-enter').click()"); time.sleep(1.5)
        ok(E("!!document.getElementById('dev-tog')"),f'{name} ?dev=1 : bouton DEV présent')
        pg.click('#dev-tog'); time.sleep(.3)
        bb=E("(()=>{const r=document.getElementById('dev-box').getBoundingClientRect();return [r.left,r.right,r.top,r.bottom]})()")
        ok(bb[0]>=0 and bb[1]<=vp[0] and bb[3]<=vp[1],f'{name} panneau entièrement à l écran',bb)
        pg.screenshot(path=OUT+f'{name}_panneau.png')
        # Déplacement : zone, porte, PNJ via l'interface
        pg.select_option('#dev-type','zone'); pg.select_option('#dev-cible','steel_megaline'); pg.click('#dev-go'); time.sleep(1.5)
        ok(E("window.__nml.state.location")=='steel_megaline',f'{name} déplacement zone : Mega-Line')
        pg.select_option('#dev-type','porte'); pg.select_option('#dev-cible','c_dome'); pg.click('#dev-go'); time.sleep(1.5)
        d=E("(()=>{const s=window.__nml.state,d=window.__nml.doors.find(d=>d.id==='c_dome');return [s.location,Math.hypot(s.player.x-d.threshold.x,s.player.z-d.threshold.z)]})()")
        ok(d[0]=='steel_center' and d[1]<2.5,f'{name} déplacement porte : c_dome',d)
        pg.select_option('#dev-type','pnj'); pg.select_option('#dev-cible','fs_fusible'); pg.click('#dev-go'); time.sleep(1.5)
        d=E("(()=>{const s=window.__nml.state,n=window.__nml.npcs.find(n=>n.id==='fs_fusible');return [s.location,Math.hypot(s.player.x-n.x,s.player.z-n.z)]})()")
        ok(d[0]=='steel_strip' and d[1]<3,f'{name} déplacement PNJ : Fusible',d)
        pg.screenshot(path=OUT+f'{name}_fusible.png')
        # Réinitialisation
        pg.click('#dev-snap'); time.sleep(.2); E("window.__nml.state.player.credits=4242; window.__nml.state.flags.dev_test=true")
        pg.select_option('#dev-type','zone'); pg.select_option('#dev-cible','steel_terminus'); pg.click('#dev-go'); time.sleep(1.5)
        pg.click('#dev-rest'); time.sleep(1.5)
        r=E("[window.__nml.state.location, window.__nml.state.player.credits, !!window.__nml.state.flags.dev_test]")
        ok(r[0]=='steel_strip' and r[1]!=4242 and not r[2],f'{name} restauration de l instantané',r)
        E("window.__nml.shell.autosave()"); time.sleep(.3)
        apres=E("Object.fromEntries(Object.keys(localStorage).filter(k=>k.startsWith('nml_save_')).map(k=>[k,localStorage.getItem(k)]))")
        ok(apres==avant,f'{name} sauvegardes du joueur intactes',(avant,apres))
        ok(E("Object.keys(localStorage).some(k=>k.startsWith('nml_dev_save_'))"),f'{name} autosave DEV dans nml_dev_save_*')
        # bouton « Mode DEV » d'Options (débloqué par la visite ?dev=1)
        def options_dev():
            passer_boot(E); E("document.getElementById('m-options').click()"); time.sleep(.4); return E("!!document.getElementById('m-dev')")
        E("localStorage.removeItem('nml_dev_unlocked')"); demarrer('')
        ok(not options_dev(),f'{name} sans drapeau : pas de bouton Mode DEV dans Options')
        demarrer('?dev=1'); ok(E("localStorage.getItem('nml_dev_unlocked')")=='1',f'{name} visite ?dev=1 : drapeau nml_dev_unlocked=1')
        demarrer(''); ok(options_dev(),f'{name} avec drapeau : bouton Mode DEV dans Options')
        pg.screenshot(path=OUT+f'{name}_options_mode_dev.png')
        with pg.expect_navigation(): E("document.getElementById('m-dev').click()")
        pg.wait_for_function('window.__nml && window.__nml.dev',timeout=30000); time.sleep(.5)
        ok(E("!document.getElementById('dev-box').hidden"),f'{name} bouton Mode DEV : panneau ouvert')
        E("document.getElementById('dev-oublier').click()"); time.sleep(.2)
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell',timeout=60000); time.sleep(1)
        ok(not options_dev(),f'{name} après Oublier : bouton Mode DEV disparu')
        E("document.querySelector('#menu-sub .m-back')?.click()"); time.sleep(.3)
        for _ in range(5): pg.click('#m-version'); time.sleep(.15)
        ok(E("localStorage.getItem('nml_dev_unlocked')")=='1' and 'DEV' in E("document.getElementById('menu-note').textContent"),f'{name} 5 appuis sur la version : drapeau et message')
        pg.screenshot(path=OUT+f'{name}_version_5_appuis.png')
        ok(options_dev(),f'{name} 5 appuis : bouton Mode DEV dans Options')
        E("localStorage.removeItem('nml_dev_unlocked')")
        apres2=E("Object.fromEntries(Object.keys(localStorage).filter(k=>k.startsWith('nml_save_')).map(k=>[k,localStorage.getItem(k)]))")
        ok(apres2==avant,f'{name} sauvegardes du joueur toujours intactes')
        ok(not errs,f'{name} aucune erreur JS',errs[:3]); ctx.close()
    print(f'{n}/{n+len(fails)} OK'); print('ECHECS',len(fails)); sys.exit(1 if fails else 0)
