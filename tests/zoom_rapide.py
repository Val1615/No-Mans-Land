# Test rapide du zoom caméra (×0,6 … ×1,5) : boutons +/− discrets semi-transparents, molette, pincement 2 doigts, clavier (+/- / 0),
# caméra centrée sur le joueur, HUD et étiquettes à taille fixe, plan d'arrivée de l'Arena préservé, tri de profondeur stable.
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from nml_boot import passer_boot  # menu Terminal : sauter l'allumage
import os, sys, time
from playwright.sync_api import sync_playwright

URL = os.environ.get('URL', 'http://127.0.0.1:8862/')
OUT = os.environ.get('OUT', '/tmp/nml-test-out/zoom/')
os.makedirs(OUT, exist_ok=True)
fails = []; n_ok = 0

def ok(c, m, d=''):
    global n_ok
    print(('OK   ' if c else 'ECHEC ') + m + ('' if c else f'  {d}'), flush=True)
    if c: n_ok += 1
    else: fails.append(m)

X = lambda a, b: a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]

with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for name, vp, mob in [('desktop', (1280, 800), False), ('mobile', (390, 844), True)]:
        errs = []
        ctx = br.new_context(viewport={'width': vp[0], 'height': vp[1]}, has_touch=mob, is_mobile=mob, device_scale_factor=1)
        pg = ctx.new_page(); E = pg.evaluate
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and 'Failed to load resource' not in m.text and errs.append(m.text))
        pg.goto(URL)
        pg.wait_for_function('window.__nml && window.__nml.shell', timeout=60000)
        time.sleep(1.0)

        # 1. Écran titre : boutons de zoom masqués
        ok(E("getComputedStyle(document.getElementById('zoom')).visibility === 'hidden'"), f'{name} écran titre : #zoom masqué')
        E("localStorage.removeItem('nml_save_auto'); localStorage.removeItem('nml_zoom')")
        passer_boot(E); E("document.getElementById('m-new').click()"); time.sleep(0.4)
        E("document.querySelector('[data-race=\"humain\"]').click()"); time.sleep(0.25)
        E("document.getElementById('cr-next').click()"); time.sleep(0.25)
        E("document.getElementById('cr-enter').click()"); time.sleep(1.2)

        # 2. État initial, UI discrète et semi-transparente, sans recouvrement
        base_ppm = 24 if mob else 30
        ok(E("window.__nml.zoom()") == 1 and E("window.__nml.view.zoomBounds()") == [0.6, 1.5], f'{name} défaut ×1,0 et bornes [0,6 ; 1,5]')
        zb = E("""(()=>{const z=document.getElementById('zoom'),rz=z.getBoundingClientRect();
          const bs=[...z.querySelectorAll('button')].map(b=>{const r=b.getBoundingClientRect(),c=getComputedStyle(b).backgroundColor;return [r.width,r.height,c];});
          const others=['hud','locbox','obj','keys','act','dialogue','panel'].map(i=>document.getElementById(i))
            .filter(e=>e&&!e.hidden&&e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden'&&getComputedStyle(e).display!=='none')
            .map(e=>{const r=e.getBoundingClientRect();return [e.id,[r.left,r.top,r.right,r.bottom]];});
          return {zr:[rz.left,rz.top,rz.right,rz.bottom],zc:getComputedStyle(z).backgroundColor,bs,others,vis:getComputedStyle(z).visibility!=='hidden'&&getComputedStyle(z).display!=='none'};})()""")
        ok(zb['vis'] and len(zb['bs']) == 2 and all(w <= 38 and h <= 38 for w, h, _ in zb['bs']), f'{name} 2 boutons +/− discrets <= 38 px', zb['bs'])
        ok(all(float(c.split(',')[3].strip(' )')) <= 0.5 for *_, c in zb['bs'] if c.count(',') == 3), f'{name} boutons semi-transparents', zb['bs'])
        ov_ui = [oid for oid, r in zb['others'] if X(zb['zr'], r)]
        ok(not ov_ui, f'{name} #zoom ne recouvre aucun élément HUD ({ov_ui})', zb)

        # Masquage en mode discret et panneau ouvert
        E("document.getElementById('k-mini').click()"); time.sleep(0.15)
        ok(E("getComputedStyle(document.getElementById('zoom')).display === 'none'"), f'{name} mode discret : #zoom masqué')
        E("document.getElementById('k-mini').click()"); time.sleep(0.15)
        E("document.getElementById('k-journal').click()"); time.sleep(0.15)
        ok(E("getComputedStyle(document.getElementById('zoom')).display === 'none'"), f'{name} panneau ouvert : #zoom masqué')
        E("document.getElementById('panel-close').click()"); time.sleep(0.15)

        # 3. Pulse Plaza : boutons +/−, clamp [0,6 ; 1,5], taille acteur vs taille fixe HUD/étiquettes
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_pulse';s.player.x=24;s.player.z=18;g.restore(s,true)})()")
        time.sleep(1.0)
        h10 = E("window.__nml.view.actorRect('player').h")
        hud10 = E("""(()=>{const h=document.getElementById('hud').getBoundingClientRect(),l=[...document.querySelectorAll('.wlabel')].find(e=>!e.hidden&&e.offsetWidth);
          const lr=l?l.getBoundingClientRect():null; return {hw:round(h.width),hh:round(h.height),lf:l?getComputedStyle(l).fontSize:null,lw:lr?round(lr.width):null,lh:lr?round(lr.height):null};
          function round(v){return Math.round(v*10)/10;}})()""")
        pg.screenshot(path=OUT + f'{name}_pulse_x10.png')

        # Clics + jusqu'au plafond 1,5
        for _ in range(8): E("document.getElementById('zoom-in').click()")
        time.sleep(0.25)
        z_max = E("window.__nml.zoom()"); ppm_max = E("window.__nml.view.ppm()"); h15 = E("window.__nml.view.actorRect('player').h")
        ok(z_max == 1.5 and abs(ppm_max - base_ppm * 1.5) < 0.05 and E("document.getElementById('zoom-in').disabled && !document.getElementById('zoom-out').disabled"),
           f'{name} plafond ×1,5 clampé (ppm={ppm_max})', (z_max, ppm_max))
        ok(abs(h15 / h10 - 1.5) < 0.05, f'{name} taille écran joueur ×1,5 ({h10:.1f} -> {h15:.1f} px)')
        pg.screenshot(path=OUT + f'{name}_pulse_x15.png')

        # Clics − jusqu'au plancher 0,6
        for _ in range(12): E("document.getElementById('zoom-out').click()")
        time.sleep(0.25)
        z_min = E("window.__nml.zoom()"); ppm_min = E("window.__nml.view.ppm()"); h06 = E("window.__nml.view.actorRect('player').h")
        ok(z_min == 0.6 and abs(ppm_min - base_ppm * 0.6) < 0.05 and E("document.getElementById('zoom-out').disabled && !document.getElementById('zoom-in').disabled"),
           f'{name} plancher ×0,6 clampé (ppm={ppm_min})', (z_min, ppm_min))
        ok(abs(h06 / h10 - 0.6) < 0.05, f'{name} taille écran joueur ×0,6 ({h10:.1f} -> {h06:.1f} px)')
        pg.screenshot(path=OUT + f'{name}_pulse_x06.png')

        # HUD et étiquettes : taille strictement fixe entre ×0,6, ×1,0 et ×1,5
        hud06 = E("""(()=>{const h=document.getElementById('hud').getBoundingClientRect(),l=[...document.querySelectorAll('.wlabel')].find(e=>!e.hidden&&e.offsetWidth);
          const lr=l?l.getBoundingClientRect():null; return {hw:Math.round(h.width*10)/10,hh:Math.round(h.height*10)/10,lf:l?getComputedStyle(l).fontSize:null,lw:lr?Math.round(lr.width*10)/10:null,lh:lr?Math.round(lr.height*10)/10:null};})()""")
        ok(hud06['hw'] == hud10['hw'] and hud06['hh'] == hud10['hh'] and hud06['lf'] == hud10['lf'],
           f'{name} HUD et police des étiquettes fixes quel que soit le zoom', (hud10, hud06))
        # Même étiquette mesurée à ×0,6 et ×1,5
        same_lbl = E("""(()=>{const pick=()=>{const l=[...document.querySelectorAll('.wlabel[data-npc]')].find(e=>!e.hidden&&e.offsetWidth);return l?[l.dataset.npc,l.offsetWidth,l.offsetHeight,getComputedStyle(l).fontSize]:null;};
          window.__nml.setZoom(1.0); window.__nml.view.render(); const a=pick();
          window.__nml.setZoom(1.5); window.__nml.view.render();
          const l2=a&&document.querySelector(`.wlabel[data-npc="${a[0]}"]`);
          const b=l2&&!l2.hidden?[l2.dataset.npc,l2.offsetWidth,l2.offsetHeight,getComputedStyle(l2).fontSize]:a;
          window.__nml.setZoom(0.6); window.__nml.view.render();
          const l3=a&&document.querySelector(`.wlabel[data-npc="${a[0]}"]`);
          const c=l3&&!l3.hidden?[l3.dataset.npc,l3.offsetWidth,l3.offsetHeight,getComputedStyle(l3).fontSize]:a;
          window.__nml.setZoom(1.0); window.__nml.view.render();
          return {a,b,c};})()""")
        ok(same_lbl['a'] and same_lbl['a'] == same_lbl['b'] == same_lbl['c'], f'{name} boîte .wlabel identique à ×0,6 / ×1,0 / ×1,5', same_lbl)

        # 4. Molette + clavier (desktop) et centrage joueur strict ; Pincement 2 doigts (mobile + desktop)
        if not mob:
            pg.mouse.move(180, 160)  # curseur volontairement décentré : la caméra doit rester centrée sur le joueur
            pg.mouse.wheel(0, -160); time.sleep(0.2)
            zw1 = E("window.__nml.zoom()")
            cib = E("window.__nml.view.camCible()"); pscr = E("window.__nml.project(window.__nml.state.player.x, 0, window.__nml.state.player.z)")
            ok(zw1 > 1.05 and abs(cib[0] - 24) < 0.05 and abs(cib[1] - 18) < 0.05 and abs(pscr['x'] - vp[0] / 2) < 1.5 and abs(pscr['y'] - vp[1] / 2) < 1.5,
               f'{name} molette hors centre : zoom {zw1} et caméra toujours centrée sur le joueur', (zw1, cib, pscr))
            pg.mouse.wheel(0, 160); pg.mouse.wheel(0, 160); time.sleep(0.2)
            zw2 = E("window.__nml.zoom()")
            ok(zw2 < 1.0, f'{name} molette vers le bas dézoome ({zw2})')
            pg.keyboard.press('0'); time.sleep(0.15)
            ok(E("window.__nml.zoom()") == 1.0, f'{name} touche 0 réinitialise à ×1,0')
            pg.keyboard.press('+'); pg.keyboard.press('-'); time.sleep(0.15)
            ok(E("window.__nml.zoom()") == 1.0, f'{name} touches + / - fonctionnelles')

        # Pincement à deux doigts (PointerEvent multi-touch) : zoom sans déplacement parasite du joueur
        pinch_res = E("""(()=>{
          window.__nml.setZoom(1.0);
          const cv = document.getElementById('view'), p0 = {...window.__nml.state.player};
          const ev = (type, id, x, y) => cv.dispatchEvent(new PointerEvent(type, { bubbles: true, pointerId: id, pointerType: 'touch', clientX: x, clientY: y }));
          ev('pointerdown', 11, 140, 400); ev('pointerdown', 12, 240, 400); // écart 100 px
          ev('pointermove', 11, 120, 400); ev('pointermove', 12, 260, 400); // écart 140 px -> ×1,4
          const zSpread = window.__nml.zoom();
          ev('pointermove', 11, 40, 400); ev('pointermove', 12, 340, 400);  // écart 300 px -> clamp 1,5 + ré-ancrage
          const zClampMax = window.__nml.zoom();
          ev('pointermove', 11, 90, 400); ev('pointermove', 12, 290, 400);  // retour 200 px depuis 300 px -> descend immédiatement (1,5 * 200/300 = 1,0)
          const zReverse = window.__nml.zoom();
          ev('pointermove', 11, 155, 400); ev('pointermove', 12, 225, 400); // écart 70 px -> clamp 0,6
          const zClampMin = window.__nml.zoom();
          ev('pointerup', 12, 225, 400); ev('pointerup', 11, 155, 400);
          const moved = window.__nml.state.player.path.length > 0 || Math.hypot(window.__nml.state.player.x - p0.x, window.__nml.state.player.z - p0.z) > 1e-4;
          window.__nml.setZoom(1.0);
          return { zSpread, zClampMax, zReverse, zClampMin, moved };
        })()""")
        ok(abs(pinch_res['zSpread'] - 1.4) < 0.02 and pinch_res['zClampMax'] == 1.5 and pinch_res['zReverse'] < 1.15 and pinch_res['zClampMin'] == 0.6 and not pinch_res['moved'],
           f'{name} pincement 2 doigts : écartement, clamp, inversion immédiate, aucun pas parasite', pinch_res)

        # 5. Steel Arena : plan d'arrivée intact, vue d'ensemble ×0,6, tri de profondeur invariant
        E("window.__nml.setZoom(0.6)")
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_pulse';s.player.x=46;s.player.z=13;g.restore(s,true)})()")
        time.sleep(0.6)
        E("window.__nml.game.useDoor('pp_est')"); time.sleep(1.2)
        arr_ppm = E("window.__nml.view.ppm()"); exp_arr = 4 if mob else 12
        ok(E("window.__nml.state.location") == 'steel_arena' and abs(arr_ppm - exp_arr) < 0.2,
           f'{name} arrivée Steel Arena : plan d arrivée intact ({arr_ppm} px/m attendu {exp_arr})', arr_ppm)
        pg.screenshot(path=OUT + f'{name}_arena_arrivee.png')

        # Marche sur le parvis -> retour au cadre joueur + vérification ×0,6 / ×1,0 / ×1,5 sans inversion d'ordre
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.x=46;s.player.z=46;g.restore(s,true)})()")
        E("window.__nml.game.moveTo(46.5, 46)"); time.sleep(1.2)
        stab = E("""(()=>{
          const L=window.__nml.world.LOCATIONS.steel_arena, v=window.__nml.view;
          window.__nml.setZoom(1.0); v.render();
          const ids=L.buildings.map(b=>b.id), rel={};
          for(let i=0;i<ids.length;i++)for(let j=i+1;j<ids.length;j++) rel[ids[i]+'/'+ids[j]] = v.orderOf(ids[i]) < v.orderOf(ids[j]);
          const flips=[];
          for(const z of [0.6, 1.5, 1.0]){
            window.__nml.setZoom(z); v.render();
            for(let i=0;i<ids.length;i++)for(let j=i+1;j<ids.length;j++){
              const k=ids[i]+'/'+ids[j];
              if((v.orderOf(ids[i]) < v.orderOf(ids[j])) !== rel[k]) flips.push(z+':'+k);
            }
          }
          return { flips, masques: v.masques() };
        })()""")
        ok(not stab['flips'] and stab['masques'] == [], f'{name} Arena : 0 inversion de profondeur et 0 masque entre ×0,6 et ×1,5', stab)
        for z, tag in [(0.6, 'x06'), (1.0, 'x10'), (1.5, 'x15')]:
            E(f"window.__nml.setZoom({z}); window.__nml.view.render()"); time.sleep(0.15)
            pg.screenshot(path=OUT + f'{name}_arena_{tag}.png')

        # 6. Persistance légère localStorage et robustesse valeurs aberrantes
        E("window.__nml.setZoom(1.3)")
        pg.reload()
        pg.wait_for_function('window.__nml && window.__nml.shell', timeout=60000); time.sleep(0.6)
        ok(E("window.__nml.zoom()") == 1.3, f'{name} persistance localStorage (×1,3 restauré)')
        ok(E("window.__nml.setZoom(99)") == 1.5 and E("window.__nml.setZoom(-3)") == 0.6 and E("window.__nml.setZoom(NaN)") == 0.6,
           f'{name} robustesse bornes / NaN')
        E("window.__nml.setZoom(1.0)")

        ok(not errs, f'{name} aucune erreur JS', errs[:3])
        ctx.close()
    br.close()

print(f'{n_ok}/{n_ok + len(fails)} OK')
print('ECHECS', len(fails))
sys.exit(1 if fails else 0)
