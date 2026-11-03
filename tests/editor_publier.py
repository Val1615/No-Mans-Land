# Test rapide de la fenêtre « Publier sur GitHub » de l'éditeur, API GitHub simulée (page.route, aucun push réel) :
# aide + lien du jeton à la première utilisation, champ masqué, message automatique, commit direct sur main, conflit -> nouvel essai,
# option « Proposer en PR plutôt » -> PR ouverte, jeton en localStorage seulement et bouton « Oublier ». Serveur local sur 8862.
import time,os,sys,json,base64
from playwright.sync_api import sync_playwright
URL=os.environ.get('URL','http://127.0.0.1:8862/'); fails=[]; n=0; TOKEN='github_pat_TEST_ui'
def ok(c,m,d=''):
    global n; print(('OK   ' if c else 'ECHEC ')+m+('' if c else f'  {d}'),flush=True); n+=c; c or fails.append(m)
gh={'sha':'v1','puts':[],'refs':[],'pulls':[],'conflict':0,'content':None}
def api(route):
    r=route.request; u=r.url; m=r.method; js=lambda code,b:route.fulfill(status=code,content_type='application/json',body=json.dumps(b))
    if '/contents/src/data/editor-maps.json' in u and m=='GET':
        return js(200,{'type':'file','sha':gh['sha'],'encoding':'base64','content':base64.b64encode(json.dumps(gh['content']).encode()).decode()})
    if '/contents/src/data/editor-maps.json' in u and m=='PUT':
        b=json.loads(r.post_data); gh['puts'].append({**b,'auth':r.headers.get('authorization')})
        if gh['conflict']: gh['conflict']-=1; gh['sha']='v-autre'; return js(409,{'message':'conflict'})
        if b.get('sha')!=gh['sha']: return js(409,{'message':'conflict'})
        if b['branch']=='main': gh['sha']='v'+str(len(gh['puts'])+1); gh['content']=json.loads(base64.b64decode(b['content']))
        return js(200,{'commit':{'sha':'abcdef1234567','html_url':'https://github.com/Val1615/No-Mans-Land/commit/abcdef1234567'},'content':{'sha':gh['sha'] if b['branch']=='main' else 'branche'}})
    if u.endswith('/git/ref/heads/main'): return js(200,{'object':{'sha':'c0'}})
    if u.endswith('/git/refs') and m=='POST': gh['refs'].append(json.loads(r.post_data)); return js(201,{})
    if u.endswith('/pulls') and m=='POST': gh['pulls'].append(json.loads(r.post_data)); return js(201,{'number':12,'html_url':'https://github.com/Val1615/No-Mans-Land/pull/12'})
    return js(500,{})
with sync_playwright() as p:
    br=p.chromium.launch(channel='chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    ctx=br.new_context(viewport={'width':1280,'height':800}); ctx.route('https://api.github.com/**',api); pg=ctx.new_page(); E=pg.evaluate; errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:m.type=='error' and '409' not in m.text and errs.append(m.text))  # le 409 simulé est journalisé par le navigateur
    pg.goto(URL+'editor/'); pg.wait_for_function("document.querySelectorAll('#district option').length>10",timeout=60000)
    E("""async()=>{localStorage.clear();const {loadEditorSource}=await import('/editor/source.js');const {initial,compact,transform}=await import('/editor/model.js');const {base}=await loadEditorSource(),d=initial(base),b=d.locations.steel_pulse.buildings[0];transform(d,'steel_pulse',b.id,{x:b.x+0.5});localStorage.setItem('nml-map-editor-github-v1-auto',JSON.stringify(compact(d,base)));}""")
    pg.goto(URL+'editor/?zone=steel_pulse'); pg.wait_for_function("document.querySelectorAll('#district option').length>10",timeout=60000); time.sleep(.5)
    ok(E("document.getElementById('publishProject').textContent.trim()")=='Publier sur GitHub','un seul bouton « Publier sur GitHub »')
    pg.click('#publishProject'); time.sleep(.3)
    ok(E("!document.getElementById('pubHelp').hidden && document.getElementById('pubTokenLink').href")=='https://github.com/settings/personal-access-tokens/new','première utilisation : aide avec le lien direct du jeton')
    ok(E("document.getElementById('pubHelpPr').hidden"),'aide : Pull requests non mentionné tant que la PR n est pas cochée')
    ok(E("document.getElementById('gitToken').type")=='password','champ du jeton masqué')
    ok(E("document.getElementById('gitMessage').value")=='Éditeur : steel_pulse modifiée','message automatique « Éditeur : steel_pulse modifiée »',E("document.getElementById('gitMessage').value"))
    ok(not E("document.getElementById('pubPr').checked"),'« Proposer en PR plutôt » décoché par défaut')
    ok('Val1615/No-Mans-Land' in E("document.querySelector('.pub-target').textContent") and 'main' in E("document.querySelector('.pub-target').textContent"),'dépôt, main et fichier préremplis')
    pg.screenshot(path='/tmp/nml-test-out/editeur_publier_aide.png')
    pg.check('#pubPr'); ok(not E("document.getElementById('pubHelpPr').hidden") and 'Pull requests' in E("document.getElementById('pubHelp').textContent"),'PR cochée : l aide mentionne Pull requests : Read and write'); pg.uncheck('#pubPr')
    pg.fill('#gitToken',TOKEN); pg.click('#gitWrite'); pg.wait_for_function("/Publié|Erreur|refus|Conflit/i.test(document.getElementById('gitResult').textContent)",timeout=10000)
    t=E("document.getElementById('gitResult').textContent"); put=gh['puts'][-1]
    ok('Publié' in t and '1 minute' in t and E("document.querySelector('#gitResult a').href").endswith('/commit/abcdef1234567'),'publié : lien du commit et délai Pages ~1 min',t)
    ok(put['branch']=='main' and put['sha']=='v1' and put['auth']=='Bearer '+TOKEN and TOKEN not in json.dumps(put['content']),'commit direct sur main avec le SHA lu, jeton dans l en-tête seulement')
    ok(list(gh['content']['locations'])==['steel_pulse'],'fichier envoyé : seule la zone modifiée',list(gh['content']['locations']))
    ok(E("localStorage.getItem('nml-editeur-jeton-github')")==TOKEN,'jeton mémorisé dans le localStorage du navigateur')
    pg.keyboard.press('Escape'); time.sleep(.2); pg.click('#publishProject'); time.sleep(.3)
    ok(E("document.getElementById('pubHelp').hidden") and E("document.getElementById('gitToken').value")==TOKEN,'utilisation suivante : aide masquée, jeton prérempli')
    gh['conflict']=1; pg.click('#gitWrite'); pg.wait_for_function("/Conflit|Publié/.test(document.getElementById('gitResult').textContent)",timeout=10000)
    ok('Conflit' in E("document.getElementById('gitResult').textContent") and not E("document.getElementById('pubRetry').hidden"),'conflit : message clair et bouton « Réessayer »')
    pg.click('#pubRetry'); pg.wait_for_function("/Publié/.test(document.getElementById('gitResult').textContent)",timeout=10000)
    ok(gh['puts'][-1]['sha']=='v-autre','nouvel essai avec le SHA frais (aucun écrasement silencieux)',gh['puts'][-1]['sha'])
    pg.check('#pubPr'); pg.click('#gitWrite'); pg.wait_for_function("/PR ouverte|Erreur|Droits|Conflit|refusé/.test(document.getElementById('gitResult').textContent)",timeout=10000)
    t=E("document.getElementById('gitResult').textContent")
    ok('PR ouverte' in t and E("document.querySelector('#gitResult a').href").endswith('/pull/12') and gh['refs'][-1]['ref'].startswith('refs/heads/editeur/steel_pulse-') and gh['pulls'][-1]['base']=='main','PR : branche editeur/<zone>-<date>, PR vers main, « PR ouverte » avec le lien',t)
    pg.screenshot(path='/tmp/nml-test-out/editeur_publier_pr.png')
    pg.click('#pubForget'); ok(E("localStorage.getItem('nml-editeur-jeton-github')") is None and E("document.getElementById('gitToken').value")=='','« Oublier le jeton » efface le localStorage')
    ok(not errs,'aucune erreur JS',errs[:3])
    br.close()
print(f'\n{n}/{n+len(fails)} OK' + ('' if not fails else ' — ECHECS : '+'; '.join(fails)))
sys.exit(1 if fails else 0)
