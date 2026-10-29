# Lot 3 interface : carte des No Man's Land et voyage case par case (1280x800 et 390x844).
# Ouverture (consultative depuis la carte de Dusk-Town, puis par la sortie régionale), brouillard de guerre (sauvegardé), destination proposée,
# trajet Dusk-Town -> Steel case par case avec temps cumulé = somme de la table des terrains, onCaseEntree appelé une fois par case,
# halte + reprise (trajet intact), sauvegarde / rechargement en cours de trajet (reprise en halte), arrivée = chargement du lieu
# (texte d'arrivée, autosave), mer bloquée, retour vers Dusk annulable, aucune erreur JS.
import time,os,sys,json
from playwright.sync_api import sync_playwright
OUT='/tmp/nml-test-out/cartes/'; os.makedirs(OUT,exist_ok=True); fails=[]; errs=[]; n_ok=0
TABLE={'cote':2,'desert':2,'foret':3,'rocher':3,'verre':3,'piste':1}  # table validée par Valentin (heures)
def ok(c,m,d=''):
    global n_ok
    print(('OK   ' if c else 'ECHEC ')+m+(f'  {d}' if d!='' and not c else ''))
    if c: n_ok+=1
    else: fails.append(m)
URL=os.environ.get('URL','http://127.0.0.1:8862/')
with sync_playwright() as p:
    br=p.chromium.launch(channel='chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    for name,vp,mob in [('desktop',(1280,800),False),('mobile',(390,844),True)]:
        ctx=br.new_context(viewport={'width':vp[0],'height':vp[1]},has_touch=mob,is_mobile=mob,device_scale_factor=1); pg=ctx.new_page(); E=pg.evaluate
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
        def wait(js,t=15):
            t0=time.time()
            while time.time()-t0<t:
                if E(js): return True
                time.sleep(.15)
            return False
        R=lambda: E("JSON.parse(JSON.stringify(window.__nml.voyage.region()))")
        vis=lambda: E("!document.getElementById('nml').hidden")
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell',timeout=60000); time.sleep(1.5)
        E("localStorage.removeItem('nml_save_auto')")
        E("document.getElementById('m-new').click()"); time.sleep(.5); E("document.querySelector('[data-race=\"humain\"]').click()"); time.sleep(.3); E("document.getElementById('cr-next').click()"); time.sleep(.3); E("document.getElementById('cr-enter').click()"); time.sleep(1.5)
        E("(()=>{window.__msgs=[];const m=document.getElementById('msg');new MutationObserver(()=>window.__msgs.push(m.textContent)).observe(m,{childList:true,characterData:true,subtree:true})})()")
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='dusk_q2';s.player.x=42;s.player.z=18;Object.assign(s.flags,{q_start:true,q_cric:true,q_signal:true,q_fin:true});g.restore(s,true)})()"); time.sleep(1.2)
        # 1. consultation depuis la carte de Dusk-Town : pas de départ possible, brouillard, lieux connus
        E("document.getElementById('k-carte').click()"); time.sleep(.3); E("document.getElementById('p-nml').click()"); time.sleep(.8)
        r=R(); ok(vis() and r['statut']=='lieu' and r['lieu']=='dusk' and E("document.getElementById('nml-partir').hidden"),f'{name} carte NML consultative ouverte depuis la carte de Dusk-Town',r['statut'])
        ok(E("window.__nml.voyage.cells.size")==167,f'{name} 167 cases terrestres')
        lieux=E("[...document.querySelectorAll('#nml-lieux .nl')].map(b=>b.dataset.lieu)")
        ok(sorted(lieux)==['dusk','steel'],f'{name} brouillard : seuls les grands lieux connus (Dusk-Town, Steel) sont affichés',lieux)
        fogA=lambda c,r_: E(f"(()=>{{const f=document.getElementById('nml-fog'),s=f.width/22;return f.getContext('2d').getImageData(Math.floor(({c}+.5)*s),Math.floor(({r_}+.5)*s),1,1).data[3]}})()")
        time.sleep(.5); a_dusk,a_far=fogA(7,3),fogA(15,14)
        ok(a_dusk<40 and a_far>200,f'{name} brouillard dissipé sur Dusk-Town (alpha {a_dusk}), opaque au loin (alpha {a_far})')
        pg.keyboard.press('Escape'); time.sleep(.3); ok(not vis(),f'{name} carte consultative fermée (Échap)')
        # 2. sortie régionale : la route des patrouilles ouvre la carte, Steel proposé
        E("window.__nml.game.useDoor('j_q2_est')"); ok(wait("!document.getElementById('nml').hidden",15),f'{name} sortie régionale (route des patrouilles) : carte NML ouverte')
        r=R(); ok(r['statut']=='depart' and r['dest']=={'lieu':'steel'} and len(r['trajet'])>0 and E("window.__nml.state.location")=='dusk_q2',f'{name} départ : Steel-Megalopolis proposé, trajet calculé ({len(r["trajet"])} cases)',r)
        trajet=r['trajet']; terr=E(f"{json.dumps(trajet)}.map(([c,r])=>window.__nml.voyage.cellAt(c,r).terrain)")
        attendu=sum(TABLE[t] for t in terr); print('   trajet',trajet,terr,'=',attendu,'h')
        ok(all(abs(a[0]-b[0])<=1 and abs(a[1]-b[1])<=1 for a,b in zip([r['case']]+trajet,trajet)),f'{name} trajet case par case (voisines)')
        ok(E("window.__nml.voyage.viser({case:[0,0]}).reason")=='mer' and R()['trajet']==trajet,f'{name} mer bloquée (case en mer refusée, trajet inchangé)')
        E("window.__nml.voyage.viser({lieu:'steel'})")
        # 3. départ, crochet espionné, halte après 2 cases
        E("(()=>{const v=window.__nml.voyage;window.__calls=[];const f=v.crochets.onCaseEntree;v.crochets.onCaseEntree=(c,e)=>{window.__calls.push([c.col,c.row,c.terrain]);return f(c,e)}})()")
        h0=E("window.__nml.state.heures"); E("document.getElementById('nml-partir').click()")
        ok(wait("window.__calls.length>=2",10),f'{name} le marqueur avance case par case')
        E("document.getElementById('nml-halte').click()"); time.sleep(.6); r=R(); n=E("window.__calls.length")
        ok(r['statut']=='halte' and r['trajet']==trajet[n:] and r['case']==trajet[n-1],f'{name} halte après {n} cases : trajet restant intact',r)
        ok(E("window.__nml.state.heures")-h0==sum(TABLE[t] for t in terr[:n]),f'{name} temps avancé selon la table ({E("window.__nml.state.heures")-h0} h)')
        ok(E("window.__nml.state.location")=='dusk_q2' and E("document.getElementById('nml-close').disabled"),f'{name} en halte : carte non fermable, lieu de jeu inchangé')
        lieux2=E("[...document.querySelectorAll('#nml-lieux .nl')].map(b=>b.dataset.lieu)"); vues=len(r['vues'])
        pg.screenshot(path=OUT+f'nml_{name}_trajet.png')
        # 4. sauvegarde : autosave en halte, rechargement de la page, Continuer -> halte sur la même case, trajet et brouillard conservés
        sv=E("JSON.parse(localStorage.getItem('nml_save_auto')).state")
        ok(sv['region']['case']==r['case'] and sv['region']['trajet']==r['trajet'] and len(sv['region']['vues'])==vues and sv['heures']==E("window.__nml.state.heures"),f'{name} autosave en cours de trajet (case, trajet, brouillard, heure)')
        # reprise avant rechargement, puis rechargement en pleine marche (sauvegarde écrite à chaque case, statut route)
        E("document.getElementById('nml-partir').click()"); ok(wait(f"window.__calls.length>={n+1}",8),f'{name} reprise du trajet')
        pg.reload(); pg.wait_for_function('window.__nml && window.__nml.shell',timeout=60000); time.sleep(1.2)
        sv=E("JSON.parse(localStorage.getItem('nml_save_auto')).state"); ok(sv['region']['statut']=='route',f'{name} sauvegarde écrite en pleine marche',sv['region']['statut'])
        E("document.getElementById('m-continue').click()"); ok(wait("!document.getElementById('nml').hidden",10),f'{name} partie rechargée en cours de trajet : carte NML rouverte')
        r=R(); ok(r['statut']=='halte' and r['case']==sv['region']['case'] and r['trajet']==sv['region']['trajet'] and r['vues']==sv['region']['vues'],f'{name} reprise en halte sur la dernière case, trajet et brouillard restaurés',(r['statut'],r['case'],sv['region']['case']))
        ok(set(lieux2)<=set(E("[...document.querySelectorAll('#nml-lieux .nl')].map(b=>b.dataset.lieu)")),f'{name} lieux connus restaurés')
        E("(()=>{const v=window.__nml.voyage;window.__calls=[];const f=v.crochets.onCaseEntree;v.crochets.onCaseEntree=(c,e)=>{window.__calls.push([c.col,c.row,c.terrain]);return f(c,e)}})()")
        E("(()=>{window.__msgs=[];const m=document.getElementById('msg');new MutationObserver(()=>window.__msgs.push(m.textContent)).observe(m,{childList:true,characterData:true,subtree:true})})()")
        reste=r['trajet']; h1=E("window.__nml.state.heures"); E("document.getElementById('nml-partir').click()")
        # 5. arrivée : chargement de la route de Steel
        ok(wait("window.__nml.state.location==='steel_route'",20),f'{name} arrivée : route de Steel chargée',E("window.__nml.state.location"))
        time.sleep(.8); c2=E("window.__calls")
        ok([x[:2] for x in c2]==reste and len(c2)==len(reste),f'{name} onCaseEntree appelé une fois par case ({len(c2)} pour {len(reste)})',c2)
        ok(E("window.__nml.state.heures")-h1==sum(TABLE[t] for t in E(f"{json.dumps(reste)}.map(([c,r])=>window.__nml.voyage.cellAt(c,r).terrain)")),f'{name} temps cumulé de la fin du trajet = somme de la table')
        ok(E("window.__nml.state.heures")-h0==attendu,f'{name} temps total Dusk-Town -> Steel = {attendu} h (somme de la table)',E("window.__nml.state.heures")-h0)
        ok(not vis() and R()['statut']=='lieu' and R()['lieu']=='steel',f'{name} carte fermée, statut lieu (Steel)',(vis(),R()['statut'],R()['lieu']))
        ok(wait("window.__msgs.some(t=>t.includes('journée de marche'))",6),f'{name} texte d arrivée (une journée de marche)')
        ok(E("JSON.parse(localStorage.getItem('nml_save_auto')).state.location")=='steel_route',f'{name} autosave à l arrivée')
        ok(E("window.__nml.state.flags.q_fin")==True,f'{name} progression de quête conservée (q_fin)')
        # 6. retour : la sortie de Steel propose Dusk-Town ; « Rester » annule
        E("window.__nml.game.useDoor('j_route_sud')"); ok(wait("!document.getElementById('nml').hidden",15),f'{name} sortie de Steel : carte NML ouverte')
        r=R(); ok(r['dest']=={'lieu':'dusk'} and len(r['trajet'])==len(trajet),f'{name} retour : Dusk-Town proposé ({len(r["trajet"])} cases)')
        if mob:
            E("document.getElementById('nml-zoom').click()"); time.sleep(.4); w=E("document.getElementById('nml-plan').getBoundingClientRect().width")
            ok(w>vp[0],f'{name} zoom de la carte ({w:.0f} px)'); E("document.getElementById('nml-zoom').click()"); E("document.getElementById('nml-zoom').click()"); time.sleep(.3)
        pg.screenshot(path=OUT+f'nml_{name}_retour.png')
        E("document.getElementById('nml-close').click()"); time.sleep(.4)
        ok(not vis() and R()['statut']=='lieu' and E("window.__nml.state.location")=='steel_route',f'{name} « Rester » : on reste à la douane')
        time.sleep(1.5); ok(E("window.__nml.state.location")=='steel_route' and not vis(),f'{name} pas de rebond sur la sortie')
        ctx.close()
    ok(not errs,'aucune erreur JS',errs[:3])
    print(f'{n_ok}/{n_ok+len(fails)} OK'); print('ECHECS',len(fails)); sys.exit(1 if fails else 0)
