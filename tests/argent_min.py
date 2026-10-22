# Argent minimal : pour chaque race, origine Errant (15 $) ou, à défaut, l'origine au plus faible argent ; aucun gain d'argent.
# De la route de Steel à Center-Town par le seul chemin de la race : implant -> douane (change réduit 10 $ -> 5 cr, Odile : « Bon. Je signe. ») ;
# sans implant -> Sol, Bruno, trappe, Sous-Ville, Elio « Je n'ai pas vingt dollars » -> porter la caisse -> monte-charge. Mise en place reprise de steel_l1/l2.
import sys, os, time, io, json, base64, re
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8799/'); OUT = os.environ.get('OUT', '/tmp/nml-test-out/argent_min/'); os.makedirs(OUT, exist_ok=True)
R = []
def check(n, ok, d=''): R.append({'test': n, 'ok': bool(ok), 'detail': str(d)}); print(('OK    ' if ok else 'ECHEC ') + n, d, flush=True)
def png(u): return np.asarray(Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB')).astype(int)
MAG = lambda a: np.abs(a - [255, 0, 255]).sum(2) > 90
def content(a):
    m = MAG(a); ys, xs = np.nonzero(m); return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
def aligned(A, B, r=4):  # même mesure que flip_pixels (recalage ±r px), pour direct et miroir
    A, B = content(A), content(B); H, W = max(len(A), len(B)) + 2 * r, max(A.shape[1], B.shape[1]) + 2 * r
    def pad(I, dx=0, dy=0): c = np.zeros((H, W, 3)) + [255, 0, 255]; c[r + dy:r + dy + len(I), r + dx:r + dx + I.shape[1]] = I; return c
    a = pad(A)
    def best(I): return min(np.abs(a - pad(I, dx, dy)).sum(2)[MAG(a) | MAG(pad(I, dx, dy))].mean() for dx in range(-r, r + 1) for dy in range(-r, r + 1))
    return round(best(B), 1), round(best(B[:, ::-1]), 1)
# v13 : mesures d'image (canvas rendu, bandeaux HUD exclus) : saturation moyenne, part de pixels néon, luminance des zones éclairées
def hsv(a):
    a = a / 255.0; mx, mn = a.max(2), a.min(2); return mx, np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
def mood(a):
    v, sat = hsv(a); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    neon = (sat > 0.45) & (v > 0.45) & ((b > r + 10) | ((b > g) & (r > g + 10)))  # néons froids : cyan, bleu, violet (le sable orangé n'en est pas)
    return {'sat': round(float(sat.mean()), 3), 'neon': round(float(neon.mean()), 4), 'v95': round(float(np.percentile(v, 95)), 3), 'v': round(float(v.mean()), 3)}
def crop_hud(a): h = a.shape[0]; return a[int(h * 0.1):int(h * 0.9)]
REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../docs/captures/steel-l1-v12/live/')
def rgb_file(p): return np.asarray(Image.open(p).convert('RGB')).astype(int)
def centroid(u):
    a = png(u); m = MAG(a); ys, xs = np.nonzero(m); return (float(xs.mean()), float(ys.mean()), int(m.sum())) if len(xs) else (0, 0, 0)
RACES = os.environ.get('RACES', 'humain,mutant,augmente,cyborg').split(',')
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for prof in os.environ.get('PROFILES', 'desktop,mobile').split(','):
      mob = prof == 'mobile'; dpr = 2 if mob else 1; VW, VH = (390, 844) if mob else (1280, 800)
      for race in RACES:
        T = f'{prof}/{race}'
        ctx = br.new_context(viewport={'width': VW, 'height': VH}, has_touch=True, is_mobile=True, device_scale_factor=2) if mob else br.new_context(viewport={'width': VW, 'height': VH})
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('response', lambda r: r.status >= 400 and errs.append(f'{r.status} {r.url}'))
        gesture = pg.touchscreen.tap if mob else pg.mouse.click
        E = pg.evaluate; st = lambda: E('JSON.parse(JSON.stringify(window.__nml.state))'); P = lambda x, y, z: E(f'window.__nml.project({x},{y},{z})')
        onscreen = lambda pt: 20 < pt['x'] < VW - 20 and 130 < pt['y'] < VH - 120
        shot = lambda: np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert('RGB')).astype(int)
        def waitjs(js, t=25):
            t0 = time.time()
            while time.time() - t0 < t:
                if E(js): return True
                time.sleep(0.1)
            return False
        def idle(): waitjs('(()=>{const s=window.__nml.state;return !s.player.path.length && !s.player.pending})()', 30); time.sleep(0.3)
        def press(sel, wait=0.4):
            E(f'(()=>{{const e=document.querySelector({json.dumps(sel)}); if(e&&e.closest("#creation")&&!e.closest(".cr-foot")) e.scrollIntoView({{block:"center"}})}})()'); time.sleep(0.1)
            b = pg.locator(sel).first.bounding_box(); assert b, sel; gesture(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2); time.sleep(wait)
        def option(label):
            loc = pg.locator('#dlg-options button', has_text=label)
            if not loc.count(): return False
            b = loc.first.bounding_box()
            if not b: return False
            gesture(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2); time.sleep(0.5); return True
        def opts(): return E("[...document.querySelectorAll('#dlg-options button')].map(b=>b.textContent)")
        def dtext(): return E("document.getElementById('dlg-text').textContent")
        def close_dlg():
            for _ in range(6):
                if not st()['dialogue']: return
                press('#dlg-close', 0.3)
        def walk(x, z, tol=0.8):  # marche par taps successifs sur le sol visible, le long du chemin
            loc0 = st()['location']
            for _ in range(25):
                s = st()
                if s['location'] != loc0 or s['dialogue']: return True
                if np.hypot(x - s['player']['x'], z - s['player']['z']) < tol: return True
                path = E(f"(()=>{{const g=window.__nml.game; return window.__findPath(g.grids[g.state.location], g.state.player, {{x:{x},z:{z}}})}})()")
                if not path: return False
                tapped = False
                for q in reversed(path[1:]):
                    pt = P(q['x'], 0, q['z'])
                    if not onscreen(pt): continue
                    k = E(f'window.__nml.pick({pt["x"]},{pt["y"]})')
                    if not k or k['kind'] != 'ground' or np.hypot(k['x'] - q['x'], k['z'] - q['z']) > 1.0: continue
                    gesture(pt['x'], pt['y']); tapped = True; break
                if not tapped: return False
                idle()
            return False
        def tap_npc(nid):
            n = E(f"window.__nml.npcs.find(n=>n.id==='{nid}')"); pt = P(n['x'], 1.0, n['z']); gesture(pt['x'], pt['y'])
            return waitjs(f"window.__nml.state.dialogue && window.__nml.state.dialogue.npc==='{nid}' && !document.getElementById('dialogue').hidden", 20)
        def enter_door(did):  # marcher près du seuil puis le bouton d'action (« Entrer », « Sortir », « Vers... ») au geste
            d = E(f"window.__nml.game.doorById('{did}')"); loc0 = st()['location']
            walk(d['threshold']['x'], d['threshold']['z'], tol=1.6)
            if st()['location'] != loc0: return True
            if E("!document.getElementById('act').hidden"): press('#act', 0.3)
            return waitjs(f"window.__nml.state.location !== '{loc0}'", 20)
        def bvis(bid):  # part du sprite du bâtiment réellement visible à l'écran
            u = E(f"window.__nml.view.isolateBuilding('{bid}')")
            if not u: return 0, 0
            iso = png(u); m = MAG(iso); full = shot(); return round(float(((np.abs(full - iso).sum(2) < 60) & m).sum() / max(1, m.sum())), 2), int(m.sum())
        def journal():
            press('#k-journal', 0.5); h = E("document.getElementById('panel-body').innerText"); press('#panel-close', 0.3); return h
        # --- création : race + origine au plus faible argent (Errant si la race le permet), au geste ---
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=60000); time.sleep(1.5)
        E("import('./src/core/path.js').then(m => window.__findPath = m.findPath)")
        ORI = E(f"import('./src/data/character.js').then(m => m.ORIGINS['{race}'].map(o => ({{id:o.id, money:o.money}})))")
        ori = 'errant' if any(o['id'] == 'errant' for o in ORI) else min(ORI, key=lambda o: o['money'])['id']
        M0 = [o['money'] for o in ORI if o['id'] == ori][0]
        if ori != 'errant': print(f'NOTE  {T}: Errant non disponible pour {race} ; origine au plus faible argent : {ori} ({M0} $)', flush=True)
        press('#m-new', 0.6); press(f'[data-race="{race}"]'); press(f'[data-origin="{ori}"]'); press('#cr-next', 0.5); press('#cr-enter', 1.2)
        c = st()['character']; s = st()['player']
        check(f'{T}: perso créé ({race}, {ori})', c and c['race'] == race and c['origin'] == ori and not E('document.body.classList.contains("menu-open")'), c and (c['race'], c['origin']))
        check(f'{T}: argent de départ = {M0} $, 0 cr', s['money'] == M0 and not s.get('credits'), (s['money'], s.get('credits')))
        def money_ok(step, m=None, cr=0):  # aucun gain : dollars et crédits exactement attendus
            s = st()['player']; check(f'{T}: argent inchangé après {step} ({m if m is not None else M0} $, {cr} cr)', s['money'] == (M0 if m is None else m) and (s.get('credits') or 0) == cr, (s['money'], s.get('credits')))
        E("(()=>{window.__msgs=[];const m=document.getElementById('msg');new MutationObserver(()=>window.__msgs.push(m.textContent)).observe(m,{childList:true,characterData:true,subtree:true})})()")
        E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='dusk_q2';s.player.x=42;s.player.z=18;Object.assign(s.flags,{q_start:true,q_cric:true,q_signal:true,q_fin:true});g.restore(s,true)})()"); time.sleep(1.2)
        money_ok('mise en place (q_fin, bout du Transit)')
        j = E("window.__nml.game.doorById('j_q2_est').threshold"); walk(j['x'], j['z'], tol=0.5)
        check(f'{T}: Dusk-Town -> route de Steel à pied', waitjs("window.__nml.state.location==='steel_route'", 15)); time.sleep(1)
        money_ok('arrivée sur la route')
        implant = race in ('augmente', 'cyborg')
        if implant:
            ok = enter_door('r_douane_door'); check(f'{T}: entrée au poste de douane', ok and st()['location'] == 'douane_in', st()['location'])
            check(f'{T}: Odile parle par geste', tap_npc('odile') and 'Motif' in dtext())
            option('Entrer. Je cherche du travail.'); check(f'{T}: implant lu (gratuit)', 'Implant lu' in dtext(), dtext()[:60])
            option('Merci.'); close_dlg(); check(f'{T}: drapeau steel_passe', st()['flags'].get('steel_passe')); money_ok('lecture de l\'implant')
            # change plein (20 $) impossible à 15 $ : refus propre, rien ne bouge ; change réduit 10 $ -> 5 cr possible
            # change à 15 $ exactement (Errant), essayé sur une copie de l'état, puis l'état réel est rétabli
            E("window.__snap0 = window.__nml.game.snapshot()")
            E("(()=>{const g=window.__nml.game,s=g.snapshot();s.player.money=15;s.player.credits=0;g.restore(s,true)})()"); time.sleep(1)
            tap_npc('odile'); option('Changer des dollars'); time.sleep(0.3); s = st()['player']
            check(f'{T}: à 15 $ : change 20 $ refusé, rien ne bouge', s['money'] == 15 and not s.get('credits') and not errs, (s['money'], s.get('credits'), errs[:2], dtext()[:50]))
            close_dlg(); tap_npc('odile'); option('Changer moins'); s = st()['player']
            check(f'{T}: à 15 $ : change réduit -> 5 $ + 5 cr', s['money'] == 5 and s.get('credits') == 5, (s['money'], s.get('credits')))
            close_dlg(); E("window.__nml.game.restore(window.__snap0, true)"); time.sleep(1); money_ok('retour à l\'état réel')
            tap_npc('odile'); o = opts()
            check(f'{T}: options de change proposées (20 $ et 10 $)', any('20 $ contre 11' in x for x in o) and any('10 $ contre 5' in x for x in o), o)
            if M0 < 20:
                option('Changer des dollars'); time.sleep(0.3); money_ok('tentative de change 20 $ (refusée faute d\'argent)')
                check(f'{T}: change 20 $ refusé sans casser le dialogue', not errs, errs[:2]); close_dlg(); tap_npc('odile')
            check(f'{T}: option « Changer moins » cliquée', option('Changer moins')); s = st()['player']
            check(f'{T}: change réduit {M0} $ -> {M0 - 10} $ + 5 cr', s['money'] == M0 - 10 and s.get('credits') == 5, (s['money'], s.get('credits')))
            close_dlg(); MF, CF = M0 - 10, 5
            ok = enter_door('douane_in_est'); time.sleep(1.5); s = st()
            check(f'{T}: Odile interpelle au passage de la barrière', (s['dialogue'] or {}).get('tree') == 'odile_volonte' and s['location'] == 'douane_in', s['dialogue'])
            for l in ('Je veux juste passer.', 'Ça ne vous regarde pas.', 'Bon. Je signe.'): check(f'{T}: option Odile « {l} »', option(l), opts())
            for _ in range(4):
                if not st()['dialogue']: break
                o = opts(); option(o[0]) if o else close_dlg()
            check(f'{T}: Odile : signé, sans payer (odile_signe, pas odile_payee)', st()['flags'].get('odile_signe') and not st()['flags'].get('odile_payee'))
            money_ok('scène d\'Odile', MF, CF)
            ok = enter_door('douane_in_est'); time.sleep(1.5); s = st()
        else:
            if race == 'humain':
                enter_door('r_douane_door'); tap_npc('odile'); o = opts()
                check(f'{T}: pas de change à la douane sans implant', not any('Changer' in x for x in o), o)
                option('Entrer. Je cherche du travail.'); check(f'{T}: refoulé à la douane', st()['flags'].get('steel_refuse')); close_dlg(); enter_door('douane_in_sud'); time.sleep(0.8)
            else:
                h = E("window.__nml.npcs.find(n=>n.id==='halloran')"); walk(h['x'] + 3, h['z'] + 5, tol=1.2)
                check(f'{T}: interpellé par le soldat', waitjs("window.__nml.state.dialogue && window.__nml.state.dialogue.npc==='halloran'", 15))
                option('Courir vers le désert.'); close_dlg(); check(f'{T}: fuite (steel_fui)', st()['flags'].get('steel_fui'))
            money_ok('douane')
            E("(()=>{const g=window.__nml.game,s=g.snapshot(),d=g.doorById('citerne_in_door');s.location='citerne_in';s.player.x=d.threshold.x-0.6;s.player.z=d.threshold.z;g.restore(s,true)})()"); time.sleep(1)
            tap_npc('sol'); option("Steel. Ils m'ont refoulé" if race == 'humain' else "Steel. Ils m'ont tiré dessus"); option('Merci, Sol.'); close_dlg()
            E("(()=>{const g=window.__nml.game,s=g.snapshot(),d=window.__nml.doors.find(d=>d.location==='mara_in');s.location='mara_in';s.player.x=d.threshold.x;s.player.z=d.threshold.z-0.6;g.restore(s,true)})()"); time.sleep(1)
            tap_npc('bruno'); option('Sol m'); option('Quatorze poutres'); close_dlg()
            check(f'{T}: Sol puis Bruno, gratuits (sol_passage, bruno_frere)', st()['flags'].get('sol_passage') and st()['flags'].get('bruno_frere')); money_ok('Sol et Bruno')
            E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_route';s.player.x=38;s.player.z=34.4;g.restore(s,true)})()"); time.sleep(1)
            ok = enter_door('r_trappe'); time.sleep(1.2); check(f'{T}: trappe -> Sous-Ville (Poutres)', ok and st()['location'] == 'sv_poutres', st()['location'])
            n = E("window.__nml.npcs.find(n=>n.id==='guetteuse')"); walk(n['x'] + 2, n['z'] + 0.6, tol=1.0); time.sleep(0.4)
            check(f'{T}: la guetteuse parle par geste', tap_npc('guetteuse')); check(f'{T}: mot « Quatorze poutres. »', option('Quatorze poutres.'), opts()); close_dlg(); money_ok('guetteuse')
            ok = enter_door('v_est'); time.sleep(1); check(f'{T}: -> la Cuve', ok and st()['location'] == 'sv_cuve', st()['location'])
            check(f'{T}: entrée chez Elio', enter_door('v_atelier_door') and st()['location'] == 'elio_in')
            check(f'{T}: Elio parle par geste', tap_npc('elio')); option('Il faut que je monte'); check(f'{T}: Elio demande 20 $', 'Vingt dollars' in dtext(), dtext()[:60])
            hp0 = st()['player']['hp']
            check(f'{T}: option « Je n\'ai pas vingt dollars »', option('Je n'), opts()); check(f'{T}: option « Porter la caisse. »', option('Porter la caisse.'), opts())
            s = st(); check(f'{T}: caisse portée : -6 PV, passage accordé', s['player']['hp'] == max(1, hp0 - 6) and s['flags'].get('sv_passage') and s['discovered'].get('v_lift'), (hp0, s['player']['hp']))
            close_dlg(); money_ok('Elio (caisse portée)'); MF, CF = M0, 0
            enter_door('elio_in_door'); time.sleep(0.8)
            ok = enter_door('v_lift_door'); time.sleep(1.5); s = st()
        check(f'{T}: arrivé à Center-Town (steel_center)', ok and s['location'] == 'steel_center', s['location'])
        check(f'{T}: quête : arrivé à Steel (q_steel)', s['flags'].get('q_steel'))
        money_ok('arrivée à Center-Town', MF, CF)
        pg.screenshot(path=OUT + f'{prof}-{race}-{ori}-center.png')
        check(f'{T}: aucune erreur console / réseau', not errs, errs[:3])
        ctx.close()
    br.close()
ok = sum(r['ok'] for r in R); print(f'{ok}/{len(R)}'); json.dump(R, open(OUT + 'resultats.json', 'w'), ensure_ascii=False, indent=1); sys.exit(0 if ok == len(R) else 1)
