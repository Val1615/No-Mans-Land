# Test rapide Steel Arena : grille est du Strip -> Arena, traversée du parvis, retour, aucune erreur JS ; fps et enseignes animées (1280 et 390).
import time,os,sys
from playwright.sync_api import sync_playwright
URL=os.environ.get('URL','http://127.0.0.1:8862/'); OUT='/tmp/nml-test-out/arena/'; os.makedirs(OUT,exist_ok=True); fails=[]; n=0
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
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_strip';s.player.x=78;s.player.z=13;g.restore(s,true)})()"); time.sleep(1.2)
        E("window.__nml.game.useDoor('fs_est')"); time.sleep(2)
        ok(E("window.__nml.state.location")=='steel_arena',f'{name} grille du Strip -> Steel Arena',E("window.__nml.state.location"))
        ok(E("window.__nml.game.world.NPCS.filter(n=>n.location==='steel_arena').length")==11,f'{name} 11 PNJ (9 + revendeur et revendeuse)')
        pg.screenshot(path=OUT+f'{name}_arrivee.png')
        # revue Régie : plan d'arrivée large (toit visible), foule fixe variée, duo d'Ocre en double largeur, retour au cadre de jeu après les premiers pas
        z0=E("window.__nml.view.camCible()"); D=E("window.__nml.view.decor()"); fx=[d for d in D if d['role'] not in ('passant','file','drone')]
        ok(len(fx)>=60 and len({d['sprite'] for d in fx})>=20,f'{name} foule fixe : {len(fx)} figurants, {len({d["sprite"] for d in fx})} sprites différents',(len(fx),len({d['sprite'] for d in fx})))
        duo=[d for d in D if d.get('sprite')=='gen_ar_fans_duo']; ok(len(duo)==1 and abs(duo[0]['ratio']-360/512)<0.01,f'{name} gen_ar_fans_duo accepté en 360 x 512 (rapport largeur/hauteur gardé)',duo)
        ok(E("window.__nml.view.masques()")==[],f'{name} départ : aucun personnage masqué',E("window.__nml.view.masques()"))
        E("window.__nml.game.moveTo(30,46)"); time.sleep(6); ok(E("window.__nml.view.camCible()")!=z0 and E("Math.hypot(window.__nml.view.camCible()[0]-window.__nml.state.player.x,window.__nml.view.camCible()[1]-window.__nml.state.player.z)")<0.5,f'{name} après les premiers pas : cadre de jeu centré sur le joueur'); pg.screenshot(path=OUT+f'{name}_milieu.png')
        fps=E("new Promise(r=>{let k=0;const t0=performance.now();const f=()=>{k++;if(performance.now()-t0<3000)requestAnimationFrame(f);else r(k*1000/(performance.now()-t0))};requestAnimationFrame(f)})")
        st=E("({...window.__nml.view.animStats})"); print(f'   {name} fps={fps:.1f} enseignes animées {st}')
        ok(st['total']>=1 and st['on']<=(8 if mob else 16) and st['ecrans']==3 and st['projecteurs']==4,f'{name} animations : {st["on"]} planches animées sur {st["total"]} (plafond {"8" if mob else "16"}), 3 écrans code (2 géants + fronton), 4 faisceaux de pylône',st)
        ok(E("window.__nml.view.masques()")==[],f'{name} aucun personnage masqué par un bâtiment',E("window.__nml.view.masques()"))
        ov=E("""(()=>{const L=window.__nml.world.LOCATIONS.steel_arena,r=[];const S=L.buildings.flatMap(b=>(b.solid??[{x:b.x,z:b.z,w:b.w,d:b.d}]).map(s=>({...s,id:b.id})));
          for(let i=0;i<S.length;i++)for(let j=i+1;j<S.length;j++){const a=S[i],b=S[j];if(a.id==='ar_toit_s0'||b.id==='ar_toit_s0')continue;if(a.x<b.x+b.w-1e-6&&b.x<a.x+a.w-1e-6&&a.z<b.z+b.d-1e-6&&b.z<a.z+a.d-1e-6)r.push(a.id+'/'+b.id)}return r})()""")
        ok(not ov,f'{name} aucun chevauchement de solides',ov)
        E("window.__nml.game.moveTo(88,46)"); t0=time.time()
        while time.time()-t0<60 and E("(()=>{const p=window.__nml.state.player;return Math.hypot(p.x-88,p.z-46)>1.2})()"): time.sleep(.3)
        pz=E("[window.__nml.state.player.x,window.__nml.state.player.z]"); ok(abs(pz[0]-88)<1.3 and abs(pz[1]-46)<1.3,f'{name} traversée ouest -> est à pied',pz)
        pg.screenshot(path=OUT+f'{name}_est.png')
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=2;s.player.z=44;g.restore(s,true)})()"); time.sleep(1); E("window.__nml.game.useDoor('ar_ouest')"); time.sleep(2); ok(E("window.__nml.state.location")=='steel_strip',f'{name} retour vers le Strip',E("window.__nml.state.location"))
        ok(not errs,f'{name} aucune erreur JS',errs[:3]); ctx.close()
    print(f'{n}/{n+len(fails)} OK'); print('ECHECS',len(fails)); sys.exit(1 if fails else 0)
