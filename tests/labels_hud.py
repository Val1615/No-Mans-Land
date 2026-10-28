# Mobile 390x844 : aucun libellé du monde visible ne chevauche un panneau d'interface, en plusieurs lieux, dialogue ouvert ou non.
import time,json,sys
from playwright.sync_api import sync_playwright
OUT='/tmp/nml-test-out/labels_hud/'; import os; os.makedirs(OUT,exist_ok=True); bad=0
with sync_playwright() as p:
    br=p.chromium.launch(channel='chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    ctx=br.new_context(viewport={'width':390,'height':844},has_touch=True,is_mobile=True,device_scale_factor=2); pg=ctx.new_page(); E=pg.evaluate
    pg.goto(os.environ.get('URL', 'http://127.0.0.1:8799/')); pg.wait_for_function('window.__nml && window.__nml.shell',timeout=60000); time.sleep(1.5)
    E("document.getElementById('m-new').click()"); time.sleep(.5); E("document.querySelector('[data-race=\"augmente\"]').click()"); time.sleep(.3); E("document.getElementById('cr-next').click()"); time.sleep(.3); E("document.getElementById('cr-enter').click()"); time.sleep(1.5)
    CHK="""(()=>{const ids=['hud','locbox','obj','msg','dialogue','panel','keys','act'];const R=ids.map(i=>document.getElementById(i)).filter(e=>e&&!e.hidden&&e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden').map(e=>e.getBoundingClientRect());
      const out=[];for(const l of document.querySelectorAll('.wlabel')){if(l.hidden||l.style.visibility==='hidden')continue;const a=l.getBoundingClientRect();if(!a.width)continue;
      if(R.some(q=>a.left<q.right&&a.right>q.left&&a.top<q.bottom&&a.bottom>q.top))out.push(l.textContent)}return out})()"""
    for loc,x,z,npc,n in [('steel_asia',15.2,13.4,'ag_mei','asia_mei'),('steel_asia',8,2,None,'asia_arrivee'),('steel_china',24,10,'cl_m_nord','china_nord'),('steel_lower',30,33,None,'lower_sud'),('steel_center',30,17,'patrouilleur','center'),('dusk_q1',20,20,None,'dusk')]:
        try: E(f"(()=>{{const g=window.__nml.game,s=g.snapshot();s.location='{loc}';s.player.x={x};s.player.z={z};g.restore(s,true)}})()")
        except Exception as e: print('skip',loc,e); continue
        time.sleep(2.5)
        if npc: E(f"window.__nml.state.dialogue={{npc:'{npc}',node:'start',tree:null}}"); time.sleep(1.2)
        o=E(CHK); hid=E("[...document.querySelectorAll('.wlabel')].filter(l=>l.dataset.underHud==='1').map(l=>l.textContent)")
        pg.screenshot(path=OUT+n+'.png'); print(n,'chevauchent:',o,'masqués:',hid); bad+=len(o)
        E("window.__nml.state.dialogue=null"); time.sleep(.3)
    print('ECHECS',bad); sys.exit(1 if bad else 0)
