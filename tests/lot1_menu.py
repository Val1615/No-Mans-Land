# v10 lot 1 : menu principal, pause, sauvegardes, options. Gestes réels (clic bureau 1280x800, tap mobile 390x844 dpr2), vérifs sur pixels.
import sys, os, time, io, json
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8765/'); OUT = os.environ.get('OUT', '/tmp/nml-test-out/lot1_menu/'); os.makedirs(OUT, exist_ok=True)
R = []
def check(n, ok, d=''): R.append({'test': n, 'ok': bool(ok), 'detail': str(d)}); print(('OK    ' if ok else 'ECHEC ') + n, d, flush=True)
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for prof in os.environ.get('PROFILES', 'desktop,mobile').split(','):
        mob = prof == 'mobile'; dpr = 2 if mob else 1
        ctx = br.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2) if mob else br.new_context(viewport={'width': 1280, 'height': 800})
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('response', lambda r: r.status >= 400 and errs.append(f'{r.status} {r.url}'))
        gesture = pg.touchscreen.tap if mob else pg.mouse.click
        E = pg.evaluate; st = lambda: E('JSON.parse(JSON.stringify(window.__nml.state))')
        shot = lambda: np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert('RGB')).astype(int)
        def press(sel, wait=0.5):
            bb = pg.locator(sel).first.bounding_box(); assert bb, sel; gesture(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2); time.sleep(wait)
        def menu_open(): return E('document.body.classList.contains("menu-open") && !document.getElementById("menu").hidden')
        def boot():
            pg.wait_for_function('window.__nml && window.__nml.shell', timeout=60000); time.sleep(2)
        def topel(sel):  # l'élément est-il réellement au premier plan à son centre (rien ne le masque)
            return E(f'(()=>{{const e=document.querySelector("{sel}"),r=e.getBoundingClientRect(),t=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return !!t&&(t===e||e.contains(t))}})()')
        pg.goto(URL); boot()
        # 1. écran titre rendu
        check(f'{prof}: écran titre affiché au lancement', menu_open())
        S = shot(); mb = E('(()=>{const r=document.querySelector("#menu .m-bg").getBoundingClientRect();return [r.width,r.height]})()')
        check(f'{prof}: fond de menu (image) rendu plein écran, pixels variés', mb[0] >= (390 if mob else 1280) - 1 and S.std() > 20, (mb, round(S.std(), 1)))
        amber = ((S[..., 0] > 200) & (S[..., 1] > 140) & (S[..., 1] < 200) & (S[..., 2] < 110)).sum()
        check(f'{prof}: titre ambre v8 visible (pixels)', amber > 200 * dpr * dpr, amber)
        for b in ['m-continue', 'm-new', 'm-load', 'm-options', 'm-codex', 'm-credits', 'm-quit']: check(f'{prof}: bouton {b} accessible au geste', topel('#' + b))
        check(f'{prof}: Continuer désactivé sans sauvegarde', E('document.getElementById("m-continue").disabled'))
        pg.screenshot(path=OUT + f'{prof}-01-titre.png')
        # codex / crédits
        press('#m-codex'); check(f'{prof}: Codex : panneau propre (placeholder)', 'se remplira en jouant' in E('document.getElementById("menu-sub").textContent'))
        pg.screenshot(path=OUT + f'{prof}-02-codex.png')
        if mob: press('#menu-sub .m-back')
        press('#m-credits'); check(f'{prof}: Crédits', 'Valentin Sartorius' in E('document.getElementById("menu-sub").textContent'))
        pg.screenshot(path=OUT + f'{prof}-03-credits.png')
        if mob: press('#menu-sub .m-back')
        # 2. options : modification par geste
        press('#m-options'); pg.screenshot(path=OUT + f'{prof}-04-options.png')
        for sel in ['[data-opt="textSize"][data-val="130"]', '[data-opt="contrast"][data-val="true"]', '[data-opt="readable"][data-val="true"]', '[data-opt="textMode"][data-val=\'"defilant"\']', '[data-opt="reduceMotion"][data-val="true"]']:
            press('#menu-sub ' + sel, 0.3)
        r = pg.locator('#menu-sub [data-range="music"]').bounding_box(); gesture(r['x'] + r['width'] * 0.5, r['y'] + r['height'] / 2); time.sleep(0.4)
        o = E('JSON.parse(localStorage.getItem("nml_options"))')
        check(f'{prof}: options enregistrées (versionnées)', o and o['v'] == 1 and o['textSize'] == 130 and o['contrast'] and o['readable'] and o['textMode'] == 'defilant' and o['reduceMotion'] and 35 <= o['music'] <= 65, o)
        cls = E('document.body.className'); check(f'{prof}: options appliquées (classes)', all(c in cls for c in ['ts-130', 'contrast', 'readable', 'reduce-motion']), cls)
        pg.screenshot(path=OUT + f'{prof}-05-options-modifiees.png')
        if mob: press('#menu-sub .m-back')
        # 3. nouveau jeu : Dusk-Town direct, perso par défaut, sans Nilo
        press('#m-new', 0.8); press('#cr-next'); press('#cr-enter', 1.2); s = st()
        check(f'{prof}: Nouveau jeu : Dusk-Town, perso par défaut', not menu_open() and s['location'] == 'dusk_q1' and s['player']['money'] == 40 and s['player']['hp'] == 27, (s['location'], s['player']['money']))
        check(f'{prof}: Nilo absent (état + case HUD masquée)', s['companion']['mode'] == 'absent' and E('getComputedStyle(document.getElementById("nilo").closest(".cell")).display==="none"'))
        iso = np.asarray(Image.open(io.BytesIO(__import__('base64').b64decode(E("window.__nml.view.isolate('companion')").split(',')[1]))).convert('RGB')).astype(int)
        check(f'{prof}: Nilo : 0 pixel rendu', (np.abs(iso - [255, 0, 255]).sum(2) > 90).sum() == 0)
        vol = E('window.__nml.music.volume'); time.sleep(3); vol = E('window.__nml.music.volume')
        check(f'{prof}: volume musique = base x option (≈0.55 x 0.5)', abs(vol - 0.55 * o['music'] / 100) < 0.05, round(vol, 3))
        # 4. jouer : dialogue (texte défilant), argent, drapeau ; puis changement de lieu -> autosave
        # (mise en place : on se place au seuil d'un intérieur habité, puis on lui parle par un vrai geste)
        npc = E("(()=>{const g=window.__nml.game,n=window.__nml.npcs.find(n=>n.dialogue&&g.world.LOCATIONS[n.location].kind==='interior');const s=g.snapshot();s.location=n.location;const d=window.__nml.doors.find(d=>d.location===n.location);s.player.x=d.threshold.x;s.player.z=d.threshold.z;g.restore(s,true);return n.id})()"); time.sleep(1.2)
        pt = E(f"(()=>{{const n=window.__nml.npcs.find(n=>n.id==='{npc}');return window.__nml.project(n.x,0.9,n.z)}})()")
        gesture(pt['x'], pt['y']); pg.wait_for_function('window.__nml.state.dialogue', timeout=20000); time.sleep(0.05)
        t0 = E('document.getElementById("dlg-text").textContent.length'); time.sleep(1.5); t1 = E('document.getElementById("dlg-text").textContent.length')
        check(f'{prof}: texte défilant actif (option)', t0 < t1, (t0, t1))
        pg.screenshot(path=OUT + f'{prof}-06-dialogue-options.png')
        press('#dlg-close')
        # état distinctif pour vérifier la restauration complète
        E("(()=>{const s=window.__nml.state;s.player.money=73;s.player.inv={cric:1};s.flags.q_start=true;s.flags.q_cric=true;})()")
        j = E("(()=>{const g=window.__nml.game;const d=window.__nml.doors.find(d=>d.location===g.state.location&&!d.edge);const G=g.grids[g.state.location];let b=null;for(let dx=-2;dx<=2;dx+=0.25)for(let dz=-2;dz<=2;dz+=0.25){const x=d.threshold.x+dx,z=d.threshold.z+dz,[i,k]=G.toCell(x,z);if(G.free(i,k)){const w=Math.hypot(dx,dz);if(!b||w<b.w)b={x,z,w}}}const p=window.__nml.project(b.x,0,b.z);return {id:d.id,x:p.x,y:p.y}})()")
        loc0 = st()['location']
        gesture(j['x'], j['y']); time.sleep(0.4); pg.wait_for_function('window.__nml.state.player.path.length===0', timeout=20000); time.sleep(0.4)
        if st()['location'] == loc0: press('#act')  # bouton « Sortir » au seuil, par geste
        pg.wait_for_function(f"window.__nml.state.location !== '{loc0}'", timeout=40000); time.sleep(1)
        a = E('JSON.parse(localStorage.getItem("nml_save_auto"))'); s = st()
        check(f'{prof}: autosave au changement de lieu', a and a['v'] == 2 and a['state']['location'] == s['location'] and a['state']['player']['money'] == 73, a and a['state']['location'])
        # 5. pause (Échap au bureau, bouton Menu sur mobile) -> sauvegarde emplacement 1
        E("(()=>{const g=window.__nml.game;g.moveTo(g.state.player.x+1.5,g.state.player.z)})()"); pg.wait_for_function('window.__nml.state.player.path.length===0', timeout=20000); time.sleep(0.5)
        if mob: press('#k-menu')
        else: pg.keyboard.press('Escape'); time.sleep(0.5)
        check(f'{prof}: pause ouverte ({"bouton Menu" if mob else "Échap"})', menu_open() and E('document.getElementById("menu").classList.contains("pause")') and topel('#m-resume'))
        x0 = st()['player']['x']; time.sleep(0.6); check(f'{prof}: jeu figé en pause', st()['player']['x'] == x0)
        pg.screenshot(path=OUT + f'{prof}-07-pause.png')
        press('#m-load'); press('#menu-sub [data-act="save"][data-slot="1"]')
        sv = E('JSON.parse(localStorage.getItem("nml_save_1"))'); ref = st()
        check(f'{prof}: sauvegarde emplacement 1', sv and sv['v'] == 2 and sv['state']['location'] == ref['location'] and abs(sv['state']['player']['x'] - ref['player']['x']) < 1e-6, sv and sv['label'])
        pg.screenshot(path=OUT + f'{prof}-08-sauvegarde.png')
        if mob: press('#menu-sub .m-back')
        if not mob: pg.keyboard.press('Escape'); time.sleep(0.3); pg.keyboard.press('Escape'); time.sleep(0.4)
        else: press('#m-resume')
        check(f'{prof}: reprise', not menu_open())
        # 6. modifier l'état puis recharger la page : Continuer restaure tout
        E("(()=>{const s=window.__nml.state;s.player.money=1;s.player.inv={};s.flags={};})()")
        pg.reload(); boot()
        check(f'{prof}: après rechargement : écran titre, Continuer actif', menu_open() and not E('document.getElementById("m-continue").disabled'), E('document.getElementById("m-continue-info").textContent'))
        o2 = E('window.__nml.shell.options'); check(f'{prof}: options persistées après rechargement', o2['textSize'] == 130 and o2['contrast'] and 'ts-130' in E('document.body.className'), o2)
        pg.screenshot(path=OUT + f'{prof}-09-titre-continuer.png')
        press('#m-continue', 1.5); s = st()
        same = s['location'] == ref['location'] and s['player']['money'] == 73 and s['player']['inv'] == {'cric': 1} and s['flags'].get('q_cric') and s['flags'].get('q_start') \
            and s['discovered'] == ref['discovered'] and s['seen'] == ref['seen'] and abs(s['player']['x'] - ref['player']['x']) < 0.6 and abs(s['player']['z'] - ref['player']['z']) < 0.6
        check(f'{prof}: Continuer restaure tout ($, inventaire, drapeaux, lieux, quartier, position)', same, (s['location'], s['player']['money'], s['player']['inv'], round(s['player']['x'], 2), round(ref['player']['x'], 2)))
        hud = E('[document.getElementById("money").textContent, document.getElementById("loc").textContent, document.getElementById("inv").textContent]')
        check(f'{prof}: HUD restauré (pixels du texte rendus)', hud[0] == '73 $' and E(f'window.__nml.game.world.LOCATIONS["{ref["location"]}"].name') == hud[1] and hud[2], hud)
        pv = E("window.__nml.project(window.__nml.state.player.x,0.9,window.__nml.state.player.z)"); S = shot()
        iso = np.asarray(Image.open(io.BytesIO(__import__('base64').b64decode(E("window.__nml.view.isolate('player')").split(',')[1]))).convert('RGB')).astype(int)
        m = np.abs(iso - [255, 0, 255]).sum(2) > 90; vis = ((np.abs(S - iso).sum(2) < 60) & m).sum() / max(1, m.sum())
        check(f'{prof}: joueur rendu à la position restaurée (pixels)', m.sum() > 50 and vis > 0.5, round(vis, 2))
        pg.screenshot(path=OUT + f'{prof}-10-partie-restauree.png')
        # 7. migration sûre : sauvegarde abîmée ou d'une version future ignorée sans planter
        E('localStorage.setItem("nml_save_2","{abîmé");localStorage.setItem("nml_save_3",JSON.stringify({v:99,state:{location:"dusk_q1",player:{}}}))')
        if mob: press('#k-menu')
        else: pg.keyboard.press('Escape'); time.sleep(0.5)
        press('#m-load'); txt = E('document.getElementById("menu-sub").textContent')
        check(f'{prof}: sauvegardes abîmée / version future ignorées proprement', txt.count('Vide') == 2 and not errs, txt[:120])
        if mob: press('#menu-sub .m-back')
        # 8. Quitter -> écran titre
        press('#m-quit'); check(f'{prof}: Quitter -> écran titre', menu_open() and not E('document.getElementById("menu").classList.contains("pause")') and E('document.getElementById("m-resume").hidden'))
        check(f'{prof}: aucune erreur console / réseau', not errs, errs[:3])
        ctx.close()
    br.close()
ok = sum(r['ok'] for r in R); print(f'{ok}/{len(R)}'); json.dump(R, open(OUT + 'resultats.json', 'w'), ensure_ascii=False, indent=1); sys.exit(0 if ok == len(R) else 1)
