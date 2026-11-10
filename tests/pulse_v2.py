# Test de régression Pulse Plaza (ex-pulse_rapide v2, clés v4 sans warp depuis le swap pulse_v4) : la zone se charge depuis Center-Town, se traverse (ouest -> sud), aucune erreur JS (1280 et 390).
# Chantier pilote + festif v2 (b3bd9a6 + 769c16d) : 9 PNJ nommés, 8 figurants distincts sans clone, aucune étiquette sur les accès, écran du Feed v2 allumé,
# aucun chevauchement d'emprises ni inversion dynamique d'ordre (painter stable), aucun PNJ masqué, budget d'animations (view.animStats, 8 au plus sur mobile)
# avec priorité Feed / Nord_A / Billboard, accès ouest et jonction de Fréquence Strip libres ; captures sous l'angle du concept.
import time,os,sys,io
from PIL import Image
from playwright.sync_api import sync_playwright
URL=os.environ.get('URL','http://127.0.0.1:8862/'); OUT=os.environ.get('OUT','/tmp/nml-test-out/pulse_v2/'); CAP=OUT+'apres_'; os.makedirs(OUT,exist_ok=True); fails=[]; n=0
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
        ok(len(L['ex'])>=30 and len(L['wk'])>=4 and len(set(L['ex']+L['wk']))>=22 and {f'gen_pp_foule_{c}' for c in 'cdefghij'}<=set(L['ex']),f'{name} foule densifiée ({len(L["ex"])} figurants + {len(L["wk"])} passants, {len(set(L["ex"]+L["wk"]))} sprites distincts)',L)
        ok(L['skin']=='g_pp_dalle_sombre' and 'g_pp_allee' in L['paint'],f'{name} dalle sombre et allées (ground.paint)',L['skin'])
        ok(E("document.querySelectorAll('.wlabel.junction,.wlabel.edge').length")==0 and E("[...document.querySelectorAll('.wlabel')].every(l=>!/Escalier|Center-Town|Strip|Arena/.test(l.textContent))"),f'{name} aucune étiquette sur les accès')
        W=E("window.__nml.world.LOCATIONS.steel_pulse.buildings.filter(b=>/^pp_(facade|mur|nord|ouest)/.test(b.sprite)).map(b=>[b.id,b.x,b.z,b.x+b.w,b.z+b.d])")
        chev=[(a[0],b[0]) for i,a in enumerate(W) for b in W[i+1:] if a[1]<b[3]-1e-6 and b[1]<a[3]-1e-6 and a[2]<b[4]-1e-6 and b[2]<a[4]-1e-6]
        ok(not chev,f'{name} aucun mur ou façade 3/4 ne chevauche un autre ({len(W)} pièces)',chev)
        SOL=E("window.__nml.world.LOCATIONS.steel_pulse.buildings.flatMap(b=>(b.solid??[{x:b.x,z:b.z,w:b.w,d:b.d}]).map(s=>[b.id,s.x,s.z,s.x+s.w,s.z+s.d]))")
        chev_sol=[(a[0],b[0]) for i,a in enumerate(SOL) for b in SOL[i+1:] if a[0]!=b[0] and a[1]<b[3]-1e-6 and b[1]<a[3]-1e-6 and a[2]<b[4]-1e-6 and b[2]<a[4]-1e-6]
        ok(not chev_sol,f'{name} aucun chevauchement d emprises solides sur la place',chev_sol)
        STAB=E("""(()=>{const loc=window.__nml.world.LOCATIONS.steel_pulse,v=window.__nml.view,g=window.__nml.game,s=g.state;v.render();
          const B=loc.buildings.map(b=>({id:b.id,x0:b.x,x1:b.x+b.w,z0:b.z,z1:b.z+b.d,fond:!!b.fond,cover:!!b.cover,sol:(b.solid??[1]).length,o0:v.orderOf(b.id)}));
          const boxOv=[];for(let i=0;i<B.length;i++)for(let j=i+1;j<B.length;j++){const a=B[i],b=B[j];if(a.fond||b.fond||a.cover||b.cover||!a.sol||!b.sol)continue;
            if(a.x0<b.x1-1e-6&&b.x0<a.x1-1e-6&&a.z0<b.z1-1e-6&&b.z0<a.z1-1e-6)boxOv.push(a.id+'/'+b.id);}
          const rel={};for(let i=0;i<B.length;i++)for(let j=i+1;j<B.length;j++)rel[B[i].id+'/'+B[j].id]=B[i].o0<B[j].o0;
          const flips=[],snap=g.snapshot();
          for(const [px,pz] of [[6,14],[16,14],[24,18],[40,16],[24,30],[8,26]]){s.player.x=px;s.player.z=pz;g.step(0.4);v.render();
            for(let i=0;i<B.length;i++)for(let j=i+1;j<B.length;j++){const k=B[i].id+'/'+B[j].id;if((v.orderOf(B[i].id)<v.orderOf(B[j].id))!==rel[k])flips.push(k);}}
          g.restore(snap,true);v.render();return {boxOv,flips:[...new Set(flips)]};})()""")
        ok(not STAB['boxOv'] and not STAB['flips'],f'{name} aucune superposition d emprises ni inversion aléatoire d ordre de profondeur',STAB)
        B=E("window.__nml.world.LOCATIONS.steel_pulse.buildings.map(b=>[b.id,b.sprite,b.x,b.z,b.x+b.w,b.z+b.d])")
        def trous(axe,ligne,lo,hi,acces):
            segs=sorted([(b[2],b[4]) if axe=='x' else (b[3],b[5]) for b in B if (abs((b[3] if axe=='x' else b[2])-ligne)<1e-6 or abs((b[5] if axe=='x' else b[4])-ligne)<1e-6) and not b[1].startswith(('pp_ecran','pp_dalle'))]+[acces])
            t=[];cur=lo
            for a0,a1 in segs:
                if a0>cur+1e-6: t.append((cur,a0))
                cur=max(cur,a1)
            if cur<hi-1e-6: t.append((cur,hi))
            return t
        T={'nord':trous('x',0,0,48,(0,0)),'sud':trous('x',36,0,48,(20,28)),'ouest':trous('z',0,0,36,(12,16)),'est':trous('z',48,0,36,(12,16))}
        ok(not any(T.values()),f'{name} aucun trou vers le vide hors des accès (nord, sud, ouest, est)',T)
        sprites_3q={b[1] for b in B if b[1].endswith('_3q')}
        expected_3q={
            'pp_kiosque_v3_3q','pp_guerite_v2_3q','pp_nouilles_v3_3q','pp_billboard_v3_3q','pp_portique_v3_3q','pp_distrib_v3_3q',
            'pp_kiosque_presse_v3_3q','pp_kiosque_boissons_v3_3q','pp_nord_a_v3_3q','pp_nord_b_v3_3q','pp_nord_c2_v3_3q','pp_nord_c3_v3_3q',
            'pp_ouest_a_v4_3q','pp_ouest_b_v4_3q','pp_ecran_feed_v4_3q',
            'pp_dalle_pulse_a_v2_3q','pp_dalle_pulse_b_v2_3q','pp_arche_holo_v2_3q','pp_pont_projecteurs_v4_3q','pp_totem_pulse_v2_3q','pp_enceinte_pulse_v2_3q'
        }
        ok(sprites_3q==expected_3q and not E("!!document.getElementById('editor-map-invalid')") and all(b[1] not in ('pp_nord_c_3q','pp_pont_projecteurs_3q','pp_pont_projecteurs_v2_3q','pp_pont_projecteurs_v3_3q','pp_ouest_a_v2_3q','pp_ouest_b_v2_3q','pp_ouest_a_v3_3q','pp_ouest_b_v3_3q','pp_ecran_feed_v2_3q','pp_ecran_feed_v3_3q','pp_guerite_3q') for b in B),
           f'{name} bâtiments Pulse v4 sans warp (23 clés) + 6 props rythmiques posés (aucun obsolète)',sorted(expected_3q^sprites_3q))
        neon_bb=E("window.__nml.world.LOCATIONS.steel_pulse.enseignes.find(e=>e.building==='pp_billboard')?.neon")
        ok(neon_bb=='pp_billboard_v3_3q_neon',f'{name} billboard branché sur pp_billboard_v3_3q_neon',neon_bb)
        e2=[b for b in B if b[0]=='pp_ecran_e2']; ok(e2 and e2[0][1]=='pp_ecran_haut_e2_v2' and abs(e2[0][4]-48.4)<1e-6 and abs(e2[0][5]-24)<1e-6 and [b for b in B if b[1]=='pp_support_ecran_o' and abs(b[4]-48.4)<1e-6 and abs(b[5]-24)<1e-6] and not [b for b in B if b[1]=='pp_mur_bas_o'] and not [b for b in B if b[1]=='pp_ecran_haut_e1'],f'{name} écran est e2 v2 (panneau sur poteaux 0,6 x 4) sur son support léger, même ancre (48,4 ; 24), plus de mur bas de 4 m, e1 retiré',e2)
        ok(set(b[1] for b in B if b[0].startswith('pp_mur_s'))=={'pp_muret','pp_muret_4'} and E("window.__nml.world.LOCATIONS.steel_pulse.gardeCorps.length")==0,f'{name} sud fermé par les murets de 1,2 m (8 et 4 m), plus de garde-corps')
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=24;s.player.z=30;g.restore(s,true)})()"); time.sleep(1)
        mq=[]
        for _ in range(4): mq+=[m for m in E("window.__nml.view.masques()") if not m[1].startswith('passant') or m[0].startswith(('pp_fac','pp_mur','pp_ecran'))]; time.sleep(1.5)
        ok(not mq,f'{name} aucun personnage masqué : PNJ et figurants par aucun élément, passants par aucun mur ni écran',sorted(set(map(tuple,mq))))
        vis=lambda: E("['pp_vasseur','pp_isaure','pp_maelle'].filter(id=>{const l=document.querySelector(`.wlabel[data-npc=${id}]`);return l&&!l.hidden}).concat([...document.querySelectorAll('.wlabel[data-building=pp_ecran_feed]')].filter(l=>!l.hidden).map(()=>'feed'))")
        ok(vis()==[],f'{name} scène centrale : étiquettes cachées loin du joueur',vis())
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=17;s.player.z=12.6;g.restore(s,true)})()"); time.sleep(1.2)
        v=vis(); ok('pp_maelle' in v and 'pp_vasseur' not in v,f'{name} étiquette de Maëlle à l approche (3 m)',v)
        if not mob:
            E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=16;s.player.z=22;g.restore(s,true)})()"); time.sleep(1.2)
            q=E("window.__nml.project(22,5,12)"); pg.mouse.move(q['x'],q['y']); pg.mouse.move(q['x']+3,q['y']+2); time.sleep(.8)
            ok('feed' in vis(),f'{name} étiquette de l écran du Feed au survol',vis()); pg.mouse.move(5,5); time.sleep(.3)
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=24;s.player.z=27;g.restore(s,true)})()"); time.sleep(1.2)
        ppm=13 if mob else 22; E(f"window.__nml.view.setCamera({{x:24,z:17,ppm:{ppm}}})"); time.sleep(2.5)
        a=E("window.__nml.project(32,0,12)"); cx,cy=a['x']-7.30*ppm,a['y']-9.90*ppm
        im=Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); px=[im.getpixel((int(cx)+i,int(cy)+j)) for i in range(-10,11,2) for j in range(-10,11,2)]
        lum=sum(sum(c) for c in px)/len(px)/3; ok(lum>40,f'{name} écran du Feed v4 allumé (luminance {lum:.0f})',(cx,cy))
        pg.screenshot(path=CAP+f'concept_{vp[0]}.png'); E("window.__nml.view.setCamera(null)"); time.sleep(1)
        st=E("window.__nml.view.animStats"); pls=E("window.__nml.view.pulses()")
        prio_keys=('pp_ecran_feed_v4_3q_pulse','pp_ecran_feed_v4_3q_ecran','pp_nord_a_v3_3q_pulse','pp_nord_a_v3_3q_ecran','pp_billboard_v3_3q_pulse','pp_billboard_v3_3q_ecran')
        prio_on={p['key']:p['on'] for p in pls if p['key'] in prio_keys}
        modes_b={p['mode'] for p in pls if p['calque']=='pulse_b'}
        ok(st.get('on',0)<=(8 if mob else 16) and st.get('pulses')==45 and st.get('pulsesOn',0)<=(8 if mob else 48)
           and len(prio_on)==6 and all(prio_on.values()) and modes_b<={'mid','high'},
           f'{name} budget animations + 45 calques rythmiques (_pulse/faisceau->kick, _pulse_b->mid/high, prio={prio_on})',(st,prio_on,modes_b))
        def acces(x0,z0,x1,z1,dest):
            E(f"(()=>{{const g=window.__nml.game,s=g.snapshot();s.location='steel_pulse';s.player.x={x0};s.player.z={z0};g.restore(s,true)}})()"); time.sleep(1); E(f"window.__nml.game.moveTo({x1},{z1})"); t0=time.time()
            while time.time()-t0<20 and E("window.__nml.state.location")=='steel_pulse': time.sleep(.3)
            return E("window.__nml.state.location")
        loc=acces(40,16,47,13,'steel_arena'); ok(loc=='steel_arena',f'{name} jonction Steel Arena libre (à pied, boucle Center -> Pulse -> Arena)',loc)
        loc=acces(8,14,1,14,'steel_center'); ok(loc=='steel_center',f'{name} accès ouest libre (à pied vers Center-Town)',loc)
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_pulse';s.player.x=3;s.player.z=14;g.restore(s,true)})()"); time.sleep(1.5)
        pg.screenshot(path=CAP+f'acces_ouest_{vp[0]}.png')
        E("window.__nml.game.moveTo(24,33)"); t0=time.time()
        while time.time()-t0<40 and E("(()=>{const p=window.__nml.state.player;return Math.hypot(p.x-24,p.z-33)>1.2})()"): time.sleep(.3)
        pz=E("[window.__nml.state.player.x,window.__nml.state.player.z]"); ok(abs(pz[0]-24)<1.3 and abs(pz[1]-33)<1.3,f'{name} traversée ouest -> escalier sud à pied',pz)
        pg.screenshot(path=OUT+f'{name}_traversee.png'); time.sleep(1.5)
        E("window.__nml.game.useDoor('pp_sud')"); t0=time.time()
        while time.time()-t0<8 and E("[window.__nml.state.location,Math.round(window.__nml.state.player.x)]")!=['steel_center',26]: time.sleep(.3)
        pz=E("[window.__nml.state.location,Math.round(window.__nml.state.player.x)]"); ok(pz==['steel_center',26],f'{name} sortie sud -> Escalier de Pulse Plaza (Center-Town)',pz)
        E("window.__nml.game.useDoor('c_pp_sud')"); time.sleep(2); ok(E("window.__nml.state.location")=='steel_pulse',f'{name} retour Escalier de Pulse Plaza -> Pulse Plaza',E("window.__nml.state.location"))
        ok(not errs,f'{name} aucune erreur JS',errs[:3]); ctx.close()
    print(f'{n}/{n+len(fails)} OK'); print('ECHECS',len(fails)); sys.exit(1 if fails else 0)
