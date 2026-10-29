# Lot 1 interface : barre d'icônes compacte et repliable (Tab), bouton « entrer » jamais sur la barre (1280x800, 880x1000, 1000x880, 390x844),
# étiquettes relevées par Régie hors du HUD, OBJECTIF sur une ligne en mobile, Mei visible depuis (24;34), étiquette de PNJ jamais sur sa tête.
import time,os,sys
from playwright.sync_api import sync_playwright
OUT='/tmp/nml-test-out/hud_barre/'; os.makedirs(OUT,exist_ok=True); fails=[]; errs=[]
def ok(c,m):
    print(('OK   ' if c else 'ECHEC ')+m)
    if not c: fails.append(m)
HUD="['hud','locbox','obj','msg','dialogue','panel','keys','act'].map(i=>document.getElementById(i)).filter(e=>e&&!e.hidden&&e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden').map(e=>e.getBoundingClientRect())"
LAB="""(t=>{const l=[...document.querySelectorAll('.wlabel')].find(l=>l.textContent===t);if(!l)return null;const a=l.getBoundingClientRect();const R=%s;
  return {shown:!l.hidden&&l.style.visibility!=='hidden'&&a.width>0,under:R.some(q=>a.left<q.right&&a.right>q.left&&a.top<q.bottom&&a.bottom>q.top),r:[a.left,a.top,a.right,a.bottom]}})""" % HUD
X=lambda a,b: a[0]<b[2] and a[2]>b[0] and a[1]<b[3] and a[3]>b[1]
with sync_playwright() as p:
    br=p.chromium.launch(channel='chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    for name,vp,mob in [('desktop',(1280,800),False),('tab_portrait',(880,1000),True),('tab_paysage',(1000,880),True),('mobile',(390,844),True)]:
        ctx=br.new_context(viewport={'width':vp[0],'height':vp[1]},has_touch=mob,is_mobile=mob,device_scale_factor=1); pg=ctx.new_page(); E=pg.evaluate
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
        pg.goto(os.environ.get('URL','http://127.0.0.1:8862/')); pg.wait_for_function('window.__nml && window.__nml.shell',timeout=60000); time.sleep(1.5)
        E("document.getElementById('m-new').click()"); time.sleep(.5); E("document.querySelector('[data-race=\"augmente\"]').click()"); time.sleep(.3); E("document.getElementById('cr-next').click()"); time.sleep(.3); E("document.getElementById('cr-enter').click()"); time.sleep(1.5)
        go=lambda loc,x,z:(E(f"(()=>{{const g=window.__nml.game,s=g.snapshot();s.location='{loc}';s.player.x={x};s.player.z={z};g.restore(s,true)}})()"),time.sleep(2.2))
        # barre : 7 icônes compactes, semi-transparentes
        k=E("[...document.querySelectorAll('#keys button')].filter(b=>b.getClientRects().length).map(b=>{const r=b.getBoundingClientRect(),c=getComputedStyle(b).backgroundColor;return [r.width,r.height,c]})")
        ok(len(k)==7 and all(w<=44 and h<=44 for w,h,_ in k),f'{name} barre : {len(k)} icônes <= 44 px ({k[0][:2]})')
        ok(all(float(c.split(',')[3].strip(' )'))<=0.5 for *_,c in k if c.count(',')==3),f'{name} barre semi-transparente ({k[0][2]})')
        keyvis=E("getComputedStyle(document.querySelector('#k-sac .key')).display!=='none'")
        ok(keyvis==(not mob),f'{name} touche affichée sur l icône : {keyvis}')
        # son / discret : icône on/off
        s0=E("document.querySelector('#k-son .ic').dataset.ic"); E("document.getElementById('k-son').click()"); s1=E("document.querySelector('#k-son .ic').dataset.ic"); E("document.getElementById('k-son').click()")
        ok({s0,s1}=={'son_on','son_off'},f'{name} son bascule {s0} -> {s1}')
        d0=E("document.querySelector('#k-mini .ic').dataset.ic"); E("document.getElementById('k-mini').click()"); time.sleep(.2); d1=E("document.querySelector('#k-mini .ic').dataset.ic"); E("document.getElementById('k-mini').click()"); time.sleep(.2)
        ok({d0,d1}=={'discret_on','discret_off'},f'{name} discret bascule {d0} -> {d1}')
        # repli : Tab (ordinateur) ou bouton, mémorisé au rechargement
        if not mob: pg.keyboard.press('Tab')
        else: E("document.getElementById('k-fold').click()")
        time.sleep(.2); n=E("[...document.querySelectorAll('#keys button')].filter(b=>b.getClientRects().length).length"); st=E("localStorage.getItem('nml_barre_repliee')")
        ok(n==1 and st=='1',f'{name} barre repliée : {n} bouton visible, mémoire {st}')
        if name=='desktop': pg.screenshot(path=OUT+'apres_desktop_repliee.png')
        E("document.getElementById('k-fold').click()"); time.sleep(.2)
        ok(E("[...document.querySelectorAll('#keys button')].filter(b=>b.getClientRects().length).length")==7,f'{name} barre dépliée')
        # bouton entrer : devant chaque porte de bâtiment de plusieurs lieux, jamais sur la barre
        worst=0; nd=0
        for loc in ['steel_china','steel_asia','steel_lower','dusk_q1']:
            ds=E(f"window.__nml.doors.filter(d=>d.location==='{loc}').map(d=>[d.threshold.x,d.threshold.z,d.id])")
            for x,z,i in ds[:6]:
                go(loc,x,z); time.sleep(.3)
                if E("document.getElementById('act').hidden"): continue
                nd+=1; a=E("(()=>{const r=document.getElementById('act').getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]})()")
                kb=E("[...document.querySelectorAll('#keys button')].filter(b=>b.getClientRects().length).map(b=>{const r=b.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]})")
                inside=a[0]>=0 and a[2]<=vp[0]+.5 and a[3]<=vp[1]+.5
                if any(X(a,b) for b in kb) or not inside: worst+=1; print('   chevauche',loc,i,a)
                if nd==1: pg.screenshot(path=OUT+f'apres_{name}_porte.png')
        ok(nd>0 and worst==0,f'{name} bouton entrer : {nd} portes, {worst} chevauchement(s) avec la barre')
        ok(E("document.querySelector('#act .ic').dataset.ic")=='entrer','bouton contextuel avec icône entrer')
        # étiquettes citées par Régie
        if name in('desktop','mobile'):
            for loc,x,z,npc,labs in [('steel_asia',15.2,13.4,'ag_mei',['Vers Lower-Town','Le Barrage (China Lake)']),('steel_asia',8,2,None,['Ah-Lam']),('steel_china',24,10,'cl_m_nord',['Ruelle (Lower-Town)']),('steel_lower',30,33,None,['La Descente (vers Center-Town)']),('steel_center',30,17,'patrouilleur',['Vers la douane'])]:
                go(loc,x,z)
                if npc: E(f"window.__nml.state.dialogue={{npc:'{npc}',node:'start',tree:null}}"); time.sleep(1.2)
                for t in labs:
                    r=E(LAB+f"({t!r})")
                    if r is None: print('   absent',t); continue
                    ok(not r['under'] and (r['shown'] or name=='desktop'),f"{name} « {t} » visible={r['shown']} hors HUD={not r['under']}")
                E("window.__nml.state.dialogue=null"); time.sleep(.3)
            # établi / technicien écartés
            go('steel_china',24.5,29.5)
            a=E(LAB+"('Établi du technicien')"); b=E(LAB+"('Le technicien')")
            if a and b and a['shown'] and b['shown']:
                ra,rb=a['r'],b['r']; gap=max(rb[1]-ra[3],ra[1]-rb[3],rb[0]-ra[2],ra[0]-rb[2]); ok(gap>=3,f'{name} établi / technicien écartés de {gap:.0f} px')
            # étiquette de Mei pas sur sa tête ; en mobile Mei visible depuis (24;34)
            for (x,z) in [(24,34),(15.2,20),(15.2,13.4)]:
                go('steel_asia',x,z)
                m=E("(()=>{const r=window.__nml.view.actorRect('ag_mei');const l=[...document.querySelectorAll('.wlabel')].find(l=>l.dataset.npc==='ag_mei');const a=l.getBoundingClientRect();return {r,l:[a.left,a.top,a.right,a.bottom],shown:!l.hidden&&l.style.visibility!=='hidden'}})()")
                r=m['r']; head=[r['x'],r['y'],r['x']+r['w'],r['y']+r['h']*0.85]
                ok(not(m['shown'] and X(m['l'],head)),f'{name} ({x};{z}) étiquette de Mei hors de son corps')
                if (x,z)==(24,34):
                    vis=r['y']+r['h']>0 and r['y']<vp[1] and r['x']+r['w']>0 and r['x']<vp[0]
                    R=E(HUD); cov=max([max(0,min(r['x']+r['w'],q['right'])-max(r['x'],q['left']))*max(0,min(r['y']+r['h'],q['bottom'])-max(r['y'],q['top'])) for q in R]+[0])/max(1,r['w']*r['h'])
                    if name=='mobile': ok(vis and cov<0.2,f'mobile Mei visible depuis (24;34) (à l écran={vis}, couverte {cov:.0%})')
                    pg.screenshot(path=OUT+f'apres_{name}_asia.png')
        # [Régie 29/10] aucune étiquette sur le corps (tête aux pieds) d'un PNJ visible, quel qu'il soit
        if name in('desktop','mobile'):
            BODY="""(()=>{const v=window.__nml.view,out=[];const npcs=window.__nml.npcs.filter(n=>n.location===window.__nml.state.location);
              const B=npcs.map(n=>{const r=v.actorRect(n.id);if(!r)return null;const cx=r.x+r.w/2,hw=Math.max(8,r.h*0.18);return {id:n.id,l:cx-hw,r:cx+hw,t:r.y+r.h*0.06,b:r.y+r.h*0.97}}).filter(q=>q&&q.b>0&&q.t<innerHeight&&q.r>0&&q.l<innerWidth);
              for(const el of document.querySelectorAll('.wlabel')){if(el.hidden||el.style.visibility==='hidden')continue;const a=el.getBoundingClientRect();if(!a.width)continue;
                for(const q of B)if(a.left<q.r&&a.right>q.l&&a.top<q.b&&a.bottom>q.t)out.push([el.textContent,q.id])}return {out,n:B.length}})()"""
            for loc,x,z,cas in [('steel_asia',24,34,[('Vers Lower-Town','ag_mei')]),('steel_lower',30,33,[('La Descente (vers Center-Town)','lt_dorn')]),('steel_china',24,29,[('Pavillon du Dragon','cl_tech'),('Implants « garantis »','cl_m_nord')])]:
                go(loc,x,z); time.sleep(.5); r=E(BODY)
                for t,npc in cas: ok([t,npc] not in r['out'],f'{name} {loc} ({x};{z}) « {t} » pas sur {npc}')
                ok(not r['out'],f'{name} {loc} ({x};{z}) aucune étiquette sur un corps de PNJ ({r["n"]} PNJ à l écran) '+str(r['out']))
                pg.screenshot(path=OUT+f'apres_{name}_corps_{loc}.png')
        # OBJECTIF : une ligne en mobile
        if name=='mobile':
            go('dusk_q1',20,20)
            h=E("(()=>{const o=document.getElementById('obj');o.hidden=false;if(document.getElementById('obj-text').textContent.length<40)document.getElementById('obj-text').textContent='Trouver un moyen de passer la douane de Center-Town sans papiers, ou en obtenir chez le faussaire';return [o.getBoundingClientRect().height,parseFloat(getComputedStyle(o).lineHeight)||16,o.textContent.length]})()")
            ok(h[0]<=h[1]*1.6+10,f'mobile OBJECTIF sur une ligne : {h[0]:.0f} px ({h[2]} car.)')
            h2=E("(()=>{const o=document.getElementById('obj');o.click();const h=o.getBoundingClientRect().height;o.click();return h})()")
            pg.screenshot(path=OUT+'apres_mobile_objectif.png')
            print('   objectif déplié :',h2,'px')
        ctx.close()
    ok(not errs,f'erreurs JS : {errs[:3]}')
    print('ECHECS',len(fails)); sys.exit(1 if fails else 0)
