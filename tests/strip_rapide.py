# Test rapide Fréquence Strip (80 x 24 m, en marge derrière le dôme) : Center-Town (c_strip) <-> Strip <-> Steel Arena (fs_est/ar_est), aucune erreur JS ;
# fps et enseignes animées (1280 et 390), façades bord à bord sans chevauchement ni trou ni inversion d'ordre dynamique, view.masques() vide, calques néon d'Ocre posés.
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from nml_boot import passer_boot  # menu Terminal : sauter l'allumage
import time,os,sys
from playwright.sync_api import sync_playwright
URL=os.environ.get('URL','http://127.0.0.1:8862/'); OUT=os.environ.get('OUT','/tmp/nml-test-out/strip/'); os.makedirs(OUT,exist_ok=True); fails=[]; n=0
def ok(c,m,d=''):
    global n; print(('OK   ' if c else 'ECHEC ')+m+('' if c else f'  {d}'),flush=True); n+=c; c or fails.append(m)
with sync_playwright() as p:
    br=p.chromium.launch(channel='chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    for name,vp,mob in [('desktop',(1280,800),False),('mobile',(390,844),True)]:
        errs=[]; ctx=br.new_context(viewport={'width':vp[0],'height':vp[1]},has_touch=mob,is_mobile=mob); pg=ctx.new_page(); E=pg.evaluate
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell',timeout=60000); time.sleep(1)
        E("localStorage.removeItem('nml_save_auto')"); passer_boot(E); E("document.getElementById('m-new').click()"); time.sleep(.5)
        E("document.querySelector('[data-race=\"humain\"]').click()"); time.sleep(.3); E("document.getElementById('cr-next').click()"); time.sleep(.3); E("document.getElementById('cr-enter').click()"); time.sleep(1.5)
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_center';s.player.x=58;s.player.z=1;g.restore(s,true)})()"); time.sleep(1.2)
        E("window.__nml.game.useDoor('c_strip')"); time.sleep(2)
        ok(E("window.__nml.state.location")=='steel_strip',f'{name} Center-Town (c_strip) -> Fréquence Strip',E("window.__nml.state.location"))
        ok(E("window.__nml.game.world.NPCS.filter(n=>n.location==='steel_strip').length")==19,f'{name} 19 PNJ (11 d origine dont Fusible et Ocre, 8 des compléments d Ocre)')
        STAB=E("""(()=>{const L=window.__nml.game.world.LOCATIONS.steel_strip,v=window.__nml.view,g=window.__nml.game,s=g.state;v.render();
          const B=L.buildings.map(b=>({id:b.id,x0:b.x,x1:b.x+b.w,z0:b.z,z1:b.z+b.d,fond:!!b.fond,cover:!!b.cover,sol:(b.solid??[1]).length,o0:v.orderOf(b.id)}));
          const boxOv=[];for(let i=0;i<B.length;i++)for(let j=i+1;j<B.length;j++){const a=B[i],b=B[j];if(a.fond||b.fond||a.cover||b.cover||!a.sol||!b.sol)continue;if(a.x0<b.x1-1e-6&&b.x0<a.x1-1e-6&&a.z0<b.z1-1e-6&&b.z0<a.z1-1e-6)boxOv.push(a.id+'/'+b.id);}
          const rel={};for(let i=0;i<B.length;i++)for(let j=i+1;j<B.length;j++)rel[B[i].id+'/'+B[j].id]=B[i].o0<B[j].o0;
          const flips=[],snap=g.snapshot();
          for(const [px,pz] of [[6,10],[16,10],[32,12],[54,10],[74,12]]){s.player.x=px;s.player.z=pz;g.step(0.4);v.render();
            for(let i=0;i<B.length;i++)for(let j=i+1;j<B.length;j++){const k=B[i].id+'/'+B[j].id;if((v.orderOf(B[i].id)<v.orderOf(B[j].id))!==rel[k])flips.push(k);}}
          g.restore(snap,true);v.render();return {boxOv,flips:[...new Set(flips)]};})()""")
        ok(not STAB['boxOv'] and not STAB['flips'],f'{name} emprises bord à bord sans superposition ni inversion dynamique d ordre',STAB)
        if not mob:
            B=E("window.__nml.game.world.LOCATIONS.steel_strip.buildings.map(b=>[b.id,b.sprite,b.x,b.z,b.w,b.d,(b.solid||[{x:b.x,z:b.z,w:b.w,d:b.d}])])")
            S=[(b[0],r) for b in B if not b[0].startswith(('fs_e_','fs_vap')) and b[0] not in ('fs_tapis','fs_cam','fs_grille_est') for r in b[6]]
            ov=[(a[0],c[0]) for i,a in enumerate(S) for c in S[i+1:] if a[0]!=c[0] and min(a[1]['x']+a[1]['w'],c[1]['x']+c[1]['w'])-max(a[1]['x'],c[1]['x'])>0.01 and min(a[1]['z']+a[1]['d'],c[1]['z']+c[1]['d'])-max(a[1]['z'],c[1]['z'])>0.01]
            ok(not ov,'aucun chevauchement d emprises solides entre façades, devantures et stands',ov)
            def couvre(f):
                iv=sorted((b[2],b[2]+b[4]) for b in B if f(b)); x=0
                for a,c in iv:
                    if a>x+0.01: return x
                    x=max(x,c)
                return x if x<80-0.01 else None
            tn=couvre(lambda b:abs(b[3]+b[5]-6)<0.01 or b[0]=='fs_bouche0'); ts=couvre(lambda b:abs(b[3]+b[5]-24)<0.01)
            ok(tn is None and ts is None,'bords nord (front z 6) et sud (front z 24) fermés de x 0 à 80',(tn,ts))
            ok(E("window.__nml.view.animStats.enseignes")>=10,'calques _neon d Ocre posés en additif (enseignes code)',E("window.__nml.view.animStats.enseignes"))
            M=set()
            for _ in range(10):
                for m in E("window.__nml.view.masques()"): M.add(tuple(m))
                time.sleep(1)
            ok(not M,'view.masques() vide : aucun PNJ ni figurant caché par une façade (10 s de passants)',sorted(M))
        pg.screenshot(path=OUT+f'{name}_arrivee.png')
        LAB='''(()=>{const r=[...document.querySelectorAll('.wlabel.npc')].filter(e=>!e.hidden&&e.offsetWidth).map(e=>[e.textContent,e.getBoundingClientRect()]);const o=[];
          for(let i=0;i<r.length;i++)for(let j=i+1;j<r.length;j++){const a=r[i][1],b=r[j][1];if(a.left<b.right&&b.left<a.right&&a.top<b.bottom+2&&b.top<a.bottom+2)o.push(r[i][0]+'/'+r[j][0])}return o})()'''
        c=E("window.__nml.view.camCible()"); ok(c and 8.9<=c[0]<=71.1 and 9<=c[1]<=14.1,f'{name} arrivée ouest : cadre centré sur la rue',c)
        for (px,pz,qui) in [(56,11,'Rouge/Rubis/Zibeline'),(66.6,11.4,'Brehm/Kessler'),(56.2,9.2,'Rouge/Rubis/Zibeline (au milieu)')]:
            E(f"(()=>{{const g=window.__nml.game,s=g.snapshot();s.player.x={px};s.player.z={pz};g.restore(s,true)}})()"); time.sleep(1.2)
            o=E(LAB); ok(not o,f'{name} étiquettes {qui} : aucune superposée',o)
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=2;s.player.z=10;g.restore(s,true)})()"); time.sleep(1)
        E("window.__nml.game.moveTo(30,12)"); time.sleep(6); pg.screenshot(path=OUT+f'{name}_milieu.png')
        fps=E("new Promise(r=>{let k=0;const t0=performance.now();const f=()=>{k++;if(performance.now()-t0<3000)requestAnimationFrame(f);else r(k*1000/(performance.now()-t0))};requestAnimationFrame(f)})")
        st=E("({...window.__nml.view.animStats})"); print(f'   {name} fps={fps:.1f} enseignes animées {st}')
        ok(st['total']==9 and st['on']<=(8 if mob else 16) and st['on']>0,f'{name} enseignes : {st["on"]} animées sur {st["total"]} (plafond {"8" if mob else "16"})',st)
        E("window.__nml.game.moveTo(78,12.5)"); t0=time.time()
        while time.time()-t0<60 and E("(()=>{const p=window.__nml.state.player;return Math.hypot(p.x-78,p.z-12.5)>1.2})()"): time.sleep(.3)
        pz=E("[window.__nml.state.player.x,window.__nml.state.player.z]"); ok(abs(pz[0]-78)<1.3 and abs(pz[1]-12.5)<1.3,f'{name} traversée ouest -> est à pied',pz)
        pg.screenshot(path=OUT+f'{name}_est.png')
        E("window.__nml.game.useDoor('fs_est')"); time.sleep(2); ok(E("window.__nml.state.location")=='steel_arena',f'{name} grille est -> Steel Arena (ar_est)',E("window.__nml.state.location"))
        E("window.__nml.game.useDoor('ar_est')"); time.sleep(2); c=E("window.__nml.view.camCible()"); ok(c and c[0]<=71.1,f'{name} arrivée est : cadre centré sur la rue',c); pz=E("[window.__nml.state.location,window.__nml.state.player.x]"); ok(pz[0]=='steel_strip' and pz[1]>75,f'{name} retour de l Arena (ar_est) au bout est du Strip',pz)
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=2;s.player.z=10;g.restore(s,true)})()"); time.sleep(1); E("window.__nml.game.useDoor('fs_ouest')"); time.sleep(2); ok(E("window.__nml.state.location")=='steel_center',f'{name} sortie ouest du Strip -> retour Center-Town (boucle complète)',E("window.__nml.state.location"))
        ok(not errs,f'{name} aucune erreur JS',errs[:3]); ctx.close()
    print(f'{n}/{n+len(fails)} OK'); print('ECHECS',len(fails)); sys.exit(1 if fails else 0)
