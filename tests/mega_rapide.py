# Test rapide Mega-Line (et rame jouable : billet lié à l'implant, 4 espèces) et terminus : Center-Town -> ligne (c_mega), traversée, passerelle -> terminus, traversée, retours, budget d'animations, aucune erreur JS (1280 et 390).
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
        msg=lambda: E("document.getElementById('msg').textContent")
        def choisir(txt):
            i=E(f"(()=>{{const n=window.__nml.game.currentNode?.()||null;return n?(n.options.find(o=>o.label.includes({txt!r}))||{{}}).index:null}})()")
            return E(f"window.__nml.game.choose({i})") if i is not None else None
        def portiqueEssai(): E("window.__nml.game.useDoor('ml_rame_quai')"); time.sleep(.25); return E("({...window.__nml.portique, cle: window.__nml.view.joueEtat.cle})")
        for race in ['humain','mutant','augmente','cyborg']:
            tp('steel_megaline',32,16.4); time.sleep(4 if race=='humain' else 1); E(f"window.__nml.debugMega({{race:'{race}',passe:false,cr:0}})")
            ok(E("window.__nml.state.character.race")==race,f'{name} {race} : espèce posée (state.character.race)')
            if race in ('humain','mutant'):
                r=portiqueEssai(); time.sleep(1); m=msg()
                ok(loc()=='steel_megaline' and r['cle']=='ml_ens_portique_refuse' and 'passerelle' in m,f'{name} {race} sans Pique-Puce : planche « refusé », refus + passerelle',(loc(),r,m))
                if race=='humain':
                    pg.screenshot(path=OUT+f'{name}_portique_refuse.png'); portiqueEssai(); time.sleep(.4); portiqueEssai(); time.sleep(1); m=msg()
                    hd=E("(()=>{const s=window.__nml.state,k=window.__nml.npcs.find(n=>n.id==='ml_vigile');return Math.abs(s.npcs.ml_vigile.heading-Math.atan2(s.player.x-k.x,s.player.z-k.z))<0.01})()")
                    ok(E("window.__nml.portique.kessler") and hd and 'Kessler' in m,f'{name} 3 insistances : Kessler se retourne',m)
                    # achat chez Fusible (Fréquence Strip)
                    tp('steel_strip',39.6,14.6); time.sleep(1); E("window.__nml.debugMega({cr:100})"); E("window.__nml.game.talkTo('fs_fusible')"); time.sleep(2.5)
                    choisir('Combien'); choisir('Je la prends'); time.sleep(.4)
                    ok(not E("window.__nml.state.player.inv.pirate_implant"),f'{name} Fusible : 100 cr, achat refusé',E("window.__nml.game.currentNode?.()?.text"))
                    E("window.__nml.game.choose(window.__nml.game.currentNode().options[0].index)"); time.sleep(.3)
                    E("window.__nml.debugMega({cr:700})"); E("window.__nml.game.talkTo('fs_fusible')"); time.sleep(2.5); choisir('Combien'); time.sleep(.3)
                    if name=='desktop': pg.screenshot(path=OUT+f'{name}_fusible.png')
                    choisir('Je la prends'); time.sleep(.4)
                    ok(E("window.__nml.state.player.inv.pirate_implant")==1 and E("window.__nml.state.player.credits")==100,f'{name} Fusible : Pique-Puce acheté 600 cr',E("window.__nml.state.player"))
                    E("window.__nml.game.choose(window.__nml.game.currentNode().options[0].index)"); time.sleep(.3)
                    ok(E("window.__nml.game.useDoor('ml_rame_quai').reason")=='porte_absente',f'{name} Pique-Puce limité à la Mega-Line (aucune porte ailleurs)')
                    tp('steel_megaline',32,16.4); time.sleep(1)
                else: E("window.__nml.debugMega({passe:true})")
            r=portiqueEssai(); time.sleep(.5); r=E("({...window.__nml.portique, cle: window.__nml.view.joueEtat.cle})")
            ok(r['cle']=='ml_ens_portique_accepte',f'{name} {race} : planche « accepté »',r)
            if race=='cyborg': pg.screenshot(path=OUT+f'{name}_portique_accepte.png')
            time.sleep(1.4); ok(E("document.getElementById('trajet').classList.contains('on')"),f'{name} {race} : trajet animé (fondu)')
            if race=='cyborg': time.sleep(.4); pg.screenshot(path=OUT+f'{name}_trajet_rame.png')
            time.sleep(3.4); m=msg()
            ok(loc()=='steel_terminus' and not E("window.__nml.trajetActif()") and 'validé' in m,f'{name} {race} : rame -> terminus, validation',(loc(),m))
            tp('steel_terminus',6,6.5); time.sleep(1); E("window.__nml.game.useDoor('tm_rame_quai')"); time.sleep(5)
            ok(loc()=='steel_megaline',f'{name} {race} : rame retour -> ligne',loc())
        ok(not errs,f'{name} aucune erreur JS',errs[:3]); ctx.close()
    print(f'{n}/{n+len(fails)} OK'); print('ECHECS',len(fails)); sys.exit(1 if fails else 0)
