# Test rapide de l'éditeur généralisé, par région : chaque zone de la région s'ouvre dans l'éditeur sans erreur JS,
# un fichier editor-maps.json (zone de la région modifiée, produit par l'éditeur) est chargé par le jeu, chaque zone se visite sans erreur JS,
# et un fichier invalide laisse le jeu démarrer sur ses données intégrées. L'aller-retour enregistrer -> recharger est vérifié par
# tests/editor-regions.mjs (node). Usage : python3 tests/editor_regions.py [steel|dusk]   (serveur local sur 8862)
import time,os,sys,json
from playwright.sync_api import sync_playwright
URL=os.environ.get('URL','http://127.0.0.1:8862/'); REGION=(sys.argv[1] if len(sys.argv)>1 else 'steel'); fails=[]; n=0
def ok(c,m,d=''):
    global n; print(('OK   ' if c else 'ECHEC ')+m+('' if c else f'  {d}'),flush=True); n+=c; c or fails.append(m)
with sync_playwright() as p:
    br=p.chromium.launch(channel='chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    ctx=br.new_context(viewport={'width':1280,'height':800}); pg=ctx.new_page(); E=pg.evaluate; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
    pg.goto(URL+'editor/'); pg.wait_for_function("document.querySelectorAll('#district option').length>10",timeout=60000)
    zones=E("r=>{const g=[...document.querySelectorAll('#district optgroup')].find(g=>g.label.toLowerCase().startsWith(r));return g?[...g.children].map(o=>o.value):[]}",REGION)
    ok(len(zones)>0,f'éditeur : région {REGION} listée ({len(zones)} zones)')
    bad=[]
    for z in zones:
        pg.select_option('#district',z); pg.wait_for_timeout(120)
        if E("window.editorDiagnostics?.().location")!=z: bad.append(z)
    pg.wait_for_timeout(400); ok(not bad and not errs,f'éditeur : les {len(zones)} zones s ouvrent sans erreur JS',(bad,errs[:3]))
    # Fichier publié produit par le modèle de l'éditeur : un bâtiment de la première zone à bâtiments décalé de 0,5 m.
    pub=E("""async zones=>{const {loadEditorSource}=await import('/editor/source.js');const {initial,compact,transform,validate}=await import('/editor/model.js');
      const {base}=await loadEditorSource(),doc=initial(base),z=zones.find(id=>doc.locations[id].buildings.length),b=doc.locations[z].buildings[0],x0=b.x;transform(doc,z,b.id,{x:x0+0.5});
      const out=compact(validate(doc,base),base);return {json:JSON.stringify(out),zone:z,id:b.id,x:x0,zones:Object.keys(out.locations)}}""",zones)
    ok(pub['zones']==[pub['zone']],f"export compact : seule la zone modifiée ({pub['zone']}) est publiée",pub['zones'])
    ctx.close()
    for label,body in [('carte éditée',pub['json']),('carte invalide',json.dumps({'format':'nml-map-editor','version':5,'locations':{pub['zone']:{'id':pub['zone']}},'doors':[]}))]:
        ctx=br.new_context(viewport={'width':1280,'height':800}); pg=ctx.new_page(); E=pg.evaluate; errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
        ctx.route('**/src/data/editor-maps.json*',(lambda b:lambda r:r.fulfill(status=200,content_type='application/json',body=b))(body))
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell',timeout=60000); time.sleep(.8)
        E("localStorage.removeItem('nml_save_auto')"); E("document.getElementById('m-new').click()"); time.sleep(.4)
        E("document.querySelector('[data-race=\"humain\"]').click()"); time.sleep(.2); E("document.getElementById('cr-next').click()"); time.sleep(.2); E("document.getElementById('cr-enter').click()"); time.sleep(1.2)
        x=E(f"window.__nml.world.LOCATIONS['{pub['zone']}'].buildings.find(b=>b.id==='{pub['id']}').x")
        if label=='carte éditée':
            ok(abs(x-(pub['x']+0.5))<1e-6,f"jeu : la modification de {pub['zone']} est appliquée",x)
            visited=[]
            for z in zones:
                E(f"(()=>{{const g=window.__nml.game,l=window.__nml.world.LOCATIONS['{z}'],s=g.snapshot();s.location='{z}';const sp=l.spawn?.player||{{x:l.size.w/2,z:l.size.d-1}};s.player.x=sp.x;s.player.z=sp.z;g.restore(s,true)}})()"); pg.wait_for_timeout(150)
                if E("window.__nml.state.location")==z: visited.append(z)
            pg.wait_for_timeout(300); ok(len(visited)==len(zones) and not errs,f'jeu : les {len(zones)} zones se chargent sans erreur JS',([z for z in zones if z not in visited],errs[:3]))
        else:
            ok(abs(x-pub['x'])<1e-6 and E("!!document.getElementById('editor-map-invalid')"),'jeu : carte invalide ignorée, données intégrées utilisées, avertissement affiché',x)
            ok(all('invalide' in e.lower() for e in errs),'jeu : seule l erreur de carte invalide est journalisée',errs[:2])
        ctx.close()
    br.close()
print(f'\n{n}/{n+len(fails)} OK' + ('' if not fails else ' — ECHECS : '+'; '.join(fails)))
sys.exit(1 if fails else 0)
