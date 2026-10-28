# Argent minimal : pour chaque race, origine Errant (15 $) ou, à défaut, l'origine au plus faible argent ; aucun gain d'argent.
# De la route de Steel à Center-Town par le seul chemin de la race : implant -> douane (change réduit 10 $ -> 5 cr, Odile : « Bon. Je signe. ») ;
# sans implant -> Sol, Bruno, trappe, Sous-Ville, Elio « Je n'ai pas vingt dollars » -> porter la caisse -> monte-charge. Mise en place reprise de steel_l1/l2.
import sys, os, time, io, json, base64, re
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8799/'); OUT = os.environ.get('OUT', '/tmp/nml-test-out/argent_dusk/'); os.makedirs(OUT, exist_ok=True)
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

# Argent à Dusk-Town (docs/ARGENT_DUSKTOWN.md) : quêtes A (Sol, 12 $ / 8 $) et B (Hector/Ezequiel : intimidation, clés, paiement, échec),
# ferraille (7 points, 22 $, une seule fois), Trois Os (RNG forcé, plafond 15 $ persistant), total hors dés = 49 $. Desktop 1280x800 et mobile.
CAP = os.environ.get('CAP', '/tmp/nml-test-out/argent_dusk/'); os.makedirs(CAP, exist_ok=True)
GAINS = {}
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for prof in os.environ.get('PROFILES', 'desktop,mobile').split(','):
        mob = prof == 'mobile'; VW, VH = (390, 844) if mob else (1280, 800); T = prof
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
        def option(label, t=8):
            # Cause réelle des échecs 1 sur 5 (rôdeur raté) : game.state.dialogue est posé avant que renderDialogue (frame suivante, lente
            # juste après la construction d'une scène sous swiftshader) n'ait créé les boutons ; l'ancien option() trouvait 0 bouton et
            # renvoyait False sans cliquer. On attend donc le bouton, puis on attend que l'état du dialogue change (pas de sleep fixe, pas de second clic).
            loc = pg.locator('#dlg-options button', has_text=label)
            if not waitjs(f"[...document.querySelectorAll('#dlg-options button')].some(b=>b.textContent.includes({json.dumps(label)}))", t): return False
            b = loc.first.bounding_box()
            if not b: return False
            SIG = "(()=>{const s=window.__nml.state;return JSON.stringify([s.dialogue,s.os,s.player.money,s.player.credits,s.player.hp,s.player.inv,s.flags])})()"
            n0 = E(SIG)
            gesture(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2)
            # sous charge (swiftshader, plusieurs navigateurs), une frame peut durer plusieurs secondes : le clic est traité en retard, pas perdu.
            # On attend donc l'effet du clic sur l'état (10 s), sans second clic ; un clic resté sans effet est signalé (DIAG).
            if not waitjs(f"{SIG} !== {json.dumps(n0)}", 10): print('DIAG clic sans effet après 10 s', label, flush=True)
            waitjs("(()=>{const g=window.__nml.game,n=g.currentNode();if(!n)return true;const dom=[...document.querySelectorAll('#dlg-options button')].map(b=>b.textContent);"
                   "return document.getElementById('dialogue').hidden===false&&JSON.stringify(dom)===JSON.stringify(n.options.map(o=>o.label))})()", t); time.sleep(0.1)  # DOM = nœud courant
            return True
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

        def cap(name): time.sleep(0.4); pg.screenshot(path=CAP + f'{prof}-{name}.png')
        def place(loc, x, z, money=None, flags=None, inv=None, vol=None, hp=None, osg=None, clear=None):
            js = f"""(()=>{{const g=window.__nml.game,s=g.snapshot();s.location='{loc}';s.player.x={x};s.player.z={z};
              {'' if money is None else f's.player.money={money};'} {'' if hp is None else f's.player.hp={hp};'} {'' if osg is None else f's.osGains={osg};'}
              {'' if inv is None else 's.player.inv=' + json.dumps(inv) + ';'} Object.assign(s.flags,{json.dumps(flags or {})});
              {'' if clear is None else 's.flags={};'} {'' if vol is None else f's.character.attrs.volonte={vol};'} g.restore(s,true)}})()"""
            if clear: js = js.replace("Object.assign(s.flags", "s.flags={}; Object.assign(s.flags")
            E(js); time.sleep(0.9)
        def near_door(did, back=0.8):
            d = E(f"window.__nml.game.doorById('{did}')"); t, o = d['threshold'], d['opening']
            vx, vz = t['x'] - o['x'], t['z'] - o['z']; n = max(1e-6, np.hypot(vx, vz)); return t['x'] + vx / n * back, t['z'] + vz / n * back
        def at_npc(nid, loc, did):
            x, z = near_door(did); return x, z
        def money(): return st()['player']['money']
        def inv(k): return st()['player']['inv'].get(k, 0)
        def rng(vals): E(f"(()=>{{window.__q={json.dumps(vals)};window.__nml.game.setRng(()=>window.__q.length?window.__q.shift():Math.random())}})()")
        die = lambda *v: [(x - 1) / 6 + 0.05 for x in v]
        def talk(nid, loc, did, **kw):
            x, z = near_door(did); place(loc, x, z, **kw); return tap_npc(nid)
        def spot(sid):  # au geste : tap sur le point au sol ; repli API signalé si le tap ne vise pas le sol du point
            sp = E(f"window.__nml.world.SPOTS.find(s=>s.id==='{sid}')"); pt = P(sp['x'], 0, sp['z']); used = 'geste'
            if onscreen(pt): gesture(pt['x'], pt['y'])
            time.sleep(0.4)
            if not (st()['player']['path'] or st()['player']['pending'] or st()['dialogue']): E(f"window.__nml.game.useSpot('{sid}')"); used = 'api'
            idle(); return used
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=60000); time.sleep(1.5)
        E("import('./src/core/path.js').then(m => window.__findPath = m.findPath)")
        press('#m-new', 0.6); press('[data-race="humain"]'); press('#cr-next', 0.5); press('#cr-enter', 1.2)
        check(f'{T}: perso créé', st()['character'] is not None)
        E("(()=>{window.__msgs=[];const m=document.getElementById('msg');new MutationObserver(()=>window.__msgs.push(m.textContent)).observe(m,{childList:true,characterData:true,subtree:true})})()")
        E("window.__S0 = window.__nml.game.snapshot()")
        reset = lambda: (E("window.__nml.game.restore(window.__S0, true)"), time.sleep(0.5))
        # ---------- Quête A : Sol -> rôdeur -> poste (12 $) ----------
        check(f'{T}: A: Sol parle', talk('sol', 'citerne_in', 'citerne_in_door', money=20, vol=10))
        check(f'{T}: A: option « Tu as du travail ? »', option('Tu as du travail'), opts()); cap('a1-sol-travail')
        option('Combien'); option('accord, donne'); check(f'{T}: A: 4 bidons reçus', inv('bidon') == 4, st()['player']['inv']); close_dlg()
        check(f'{T}: A: option travail disparue', not (tap_npc('sol') and any('du travail' in o for o in opts())), opts()); close_dlg()
        x, z = near_door('j_q4_nord', 2.5); place('dusk_q4', x, z); rng([0.99] * 4)
        enter_door('j_q4_nord'); ok = waitjs("window.__nml.state.dialogue && window.__nml.state.dialogue.npc==='rodeur'", 10)
        check(f'{T}: A: scène du rôdeur à l\'entrée de La Pompe', ok, st()['location']); cap('a2-rodeur')
        option('Le regarder en face'); check(f'{T}: A: rôdeur : Volonté réussie (recule)', (st()['dialogue'] or {}).get('node') == 'recule' and 'Il hésite' in dtext(), (st()['dialogue'], dtext()[:40])); option('Continuer'); close_dlg()
        rng([0.99]); x, z = near_door('j_q1_est', 2.5); place('dusk_q1', x, z); enter_door('j_q1_est'); time.sleep(0.8)
        check(f'{T}: A: pas de raid (tirage forcé), arrivé au Transit', st()['location'] == 'dusk_q2' and not st()['dialogue'], st()['dialogue'])
        place('dusk_q2', 42, 14.5); m0 = money(); how = spot('poste')
        check(f'{T}: A: voix du poste ({how})', waitjs("window.__nml.state.dialogue && window.__nml.state.dialogue.npc==='poste'", 8)); cap('a3-poste')
        option('Poser les quatre'); check(f'{T}: A: livraison 4 bidons = +12 $', money() == m0 + 12 and inv('bidon') == 0, (m0, money())); GAINS['A'] = money() - m0; cap('a4-poste-paye'); close_dlg()
        talk('sol', 'citerne_in', 'citerne_in_door'); option('Le poste a eu son eau'); check(f'{T}: A: retour chez Sol', 'Merci' in dtext(), dtext()[:40]); close_dlg()
        # variante : rôdeur payé d'un bidon -> 8 $
        reset(); x, z = near_door('j_q4_nord', 2.5); place('dusk_q4', x, z, flags={'a_debut': True}, inv={'bidon': 4}, vol=10); enter_door('j_q4_nord'); waitjs("window.__nml.state.dialogue", 10)
        option('Poser un bidon'); option('Continuer'); close_dlg(); check(f'{T}: A/rôdeur payé : 3 bidons', inv('bidon') == 3)
        place('dusk_q2', 42, 14.5); m0 = money(); spot('poste'); o = opts()
        check(f'{T}: A/rôdeur payé : option « Un rôdeur m\'en a pris un »', any('rôdeur' in x for x in o) and not any('quatre' in x for x in o), o)
        option('rôdeur'); check(f'{T}: A/rôdeur payé : +8 $', money() == m0 + 8, (m0, money())); close_dlg()
        # variante : rôdeur raté (-5 PV, hook) puis raid raté (bidon crevé) -> 8 $
        reset(); x, z = near_door('j_q4_nord', 2.5); place('dusk_q4', x, z, flags={'a_debut': True}, inv={'bidon': 4}, vol=0, hp=30); rng([0.0] * 4); enter_door('j_q4_nord'); waitjs("window.__nml.state.dialogue", 10)
        option('Le regarder en face'); s = st(); check(f'{T}: A/rôdeur raté : frappe', (st()['dialogue'] or {}).get('node') == 'frappe', st()['dialogue']); option('Ramasser'); s = st()
        check(f'{T}: A/rôdeur raté : -5 PV, combat_rodeur + hook', s['player']['hp'] == 25 and s['flags'].get('combat_rodeur') and 'combat_rodeur' in (s.get('hooks') or []), (s['player']['hp'], s.get('hooks')))
        close_dlg(); rng([0.0, 0.0]); x, z = near_door('j_q1_est', 2.5); place('dusk_q1', x, z); enter_door('j_q1_est')
        check(f'{T}: A/raid déclenché (tirage forcé)', waitjs("window.__nml.state.dialogue && window.__nml.state.dialogue.npc==='raid'", 10)); cap('a5-raid')
        option('Ne plus bouger'); option('Attendre'); close_dlg(); check(f'{T}: A/raid raté : un bidon perdu, -3 PV', inv('bidon') == 3 and st()['player']['hp'] == 22, (inv('bidon'), st()['player']['hp']))
        place('dusk_q2', 42, 14.5); m0 = money(); spot('poste'); option('soldats'); check(f'{T}: A/raid : +8 $', money() == m0 + 8, (m0, money())); close_dlg()
        # variante : garder un bidon -> 8 $ + eau qui rend 4 PV ; Sol méfiante
        reset(); place('dusk_q2', 42, 14.5, flags={'a_debut': True, 'a_rodeur_fait': True}, inv={'bidon': 4}, hp=20); m0 = money(); spot('poste'); option('Garder le dernier')
        check(f'{T}: A/garde : +8 $ et une eau', money() == m0 + 8 and inv('water') == 1 and inv('bidon') == 0, (money(), st()['player']['inv'])); close_dlg()
        press('#k-inv' if E("!!document.getElementById('k-inv')") else '#k-sac', 0.5); cap('a6-sac-eau')
        if E("!!document.querySelector('[data-use=water]')"): press('[data-use=water]', 0.5); how = 'geste'
        else: E("window.__nml.game.useItem('water')"); how = 'api'
        check(f'{T}: A/garde : boire le bidon gardé = +4 PV ({how})', st()['player']['hp'] == 24 and inv('water') == 0, st()['player']['hp'])
        if E("!document.getElementById('panel').hidden"): press('#panel-close', 0.3)
        talk('sol', 'citerne_in', 'citerne_in_door'); option('Le poste a eu son eau'); check(f'{T}: A/garde : Sol méfiante', 'Il manquait un bidon' in dtext(), dtext()[:40]); cap('a7-sol-mefiante'); close_dlg()
        # ---------- Quête B : Hector / Ezequiel ----------
        def b_start():
            reset(); talk('hector', 'bar_in', 'bar_in_door', money=20, vol=10); option('Du travail pour moi'); option('J\'y vais'); close_dlg()
        b_start(); cap('b1-hector-bar'); check(f'{T}: B: b_debut', st()['flags'].get('b_debut'))
        talk('ezequiel', 'atelier_in', 'atelier_in_door'); check(f'{T}: B: option chez Ezequiel', option('Hector m'), opts()); cap('b2-ezequiel')
        rng([0.99]); m0 = money(); option('quinze dollars. Sors'); check(f'{T}: B/intimidation réussie (cède)', 'boîte de conserve' in dtext(), dtext()[:40]); option('Prendre'); check(f'{T}: B/intimidation : +15 $ d\'Ezequiel', money() == m0 + 15, (m0, money())); close_dlg()
        talk('hector', 'bar_in', 'bar_in_door'); option('Ezequiel a payé'); m1 = money(); option('Merci, Hector')
        check(f'{T}: B/intimidation : Hector rend 15 (net +15 $)', money() == m0 + 15 and st()['flags'].get('b_fini'), (m0, money())); GAINS['B'] = money() - m0; close_dlg()
        b_start(); talk('ezequiel', 'atelier_in', 'atelier_in_door', vol=0, hp=30); option('Hector m'); rng([0.0]); option('quinze dollars. Sors'); cap('b3-canne'); option('Sortir')
        check(f'{T}: B/intimidation ratée : -4 PV, b_echec', st()['player']['hp'] == 26 and st()['flags'].get('b_echec')); close_dlg()
        m0 = money(); talk('hector', 'bar_in', 'bar_in_door'); o = opts(); check(f'{T}: B/échec : option chez Hector', any('chassé' in x for x in o), o)
        option('chassé'); check(f'{T}: B/échec : réplique de la soupe', 'soupe' in dtext()); cap('b4-hector-echec'); option('soupe'); check(f'{T}: B/échec : b_fini, 0 $', st()['flags'].get('b_fini') and money() == m0); close_dlg()
        b_start(); talk('ezequiel', 'atelier_in', 'atelier_in_door'); option('Hector m'); option('autre'); option('Je prends les clés'); close_dlg()
        check(f'{T}: B/clés : jeu de clés reçu', inv('cles') == 1); m0 = money()
        talk('anselme', 'grocery_in', 'grocery_in_door2'); option('ferraille'); option('clés'); check(f'{T}: B/clés vendues 8 $ chez Anselme', money() == m0 + 8 and inv('cles') == 0, (m0, money())); close_dlg()
        talk('hector', 'bar_in', 'bar_in_door'); option('clés'); option('Tant pis'); check(f'{T}: B/clés : Hector clôt (b_fini, rien de plus)', st()['flags'].get('b_fini') and money() == m0 + 8); close_dlg()
        b_start(); talk('ezequiel', 'atelier_in', 'atelier_in_door', money=20); option('Hector m'); option('Je la paie'); m0 = money(); option('Parce que tu répares')
        check(f'{T}: B/paiement : -15 $, allié', money() == m0 - 15 and st()['flags'].get('ezequiel_allie'), (m0, money())); close_dlg()
        talk('hector', 'bar_in', 'bar_in_door'); option('payé pour lui'); option('Elle l'); check(f'{T}: B/paiement : b_fini', st()['flags'].get('b_fini')); close_dlg()
        b_start(); talk('ezequiel', 'atelier_in', 'atelier_in_door', money=5); option('Hector m'); option('Je la paie'); option('Parce que tu répares')
        check(f'{T}: B/paiement sans 15 $ : nœud pauvre, rien ne bouge', 'pleurer' in dtext() and money() == 5 and not st()['flags'].get('b_regle'), dtext()[:40]); close_dlg()
        # ---------- Ferraille : 7 points, une fois chacun, 22 $ ----------
        reset(); INV0 = dict(st()['player']['inv']); FER = E("window.__nml.world.SPOTS.filter(s=>s.kind==='pickup')"); check(f'{T}: F: 7 points de ferraille', len(FER) == 7, len(FER))
        hows = []
        for i, f in enumerate(FER):
            place(f['location'], f['x'] + 1.5, f['z'] + 1.5); n0 = inv(f['item']); hows.append(spot(f['id']))
            ok1 = inv(f['item']) == n0 + 1 and st()['flags'].get('ramasse_' + f['id'])
            if i == 0: cap('f1-ferraille-ramassee')
            spot(f['id']); check(f'{T}: F: {f["id"]} ramassé une seule fois', ok1 and inv(f['item']) == n0 + 1, (n0, inv(f['item'])))
        check(f'{T}: F: inventaire 4 pièces, 2 circuits, 1 batterie', (inv('piece'), inv('circuit'), inv('batterie')) == (4, 2, 1), st()['player']['inv'])
        m0 = money(); talk('anselme', 'grocery_in', 'grocery_in_door2'); option('ferraille'); cap('f2-anselme')
        for _ in range(10):
            o = opts(); lab = next((x for x in o if '$)' in x), None)
            if not lab: break
            option(lab); option('autre chose')
        check(f'{T}: F: vente totale = +22 $', money() == m0 + 22, (m0, money())); GAINS['F'] = money() - m0
        o = opts(); check(f'{T}: F: plus rien à vendre', not any('$)' in x for x in o), o); close_dlg()
        for f in FER: place(f['location'], f['x'] + 1.5, f['z'] + 1.5); spot(f['id'])
        check(f'{T}: F: rien à re-ramasser ni revendre', st()['player']['inv'] == INV0 and money() == m0 + 22, st()['player']['inv'])
        # ---------- Les Trois Os (RNG forcé) ----------
        reset(); msgs0 = len(E('window.__msgs'))
        def teo(**kw): talk('teo', 'guet_in', 'guet_in_door', **kw); option('Tu joues')
        teo(money=50, vol=10); cap('o1-teo-start')
        rng(die(6, 6, 5)); m0 = money(); option('Miser 1'); check(f'{T}: O: mise 1 $ retenue, dés affichés', money() == m0 - 1 and '6, 6, 5 (17)' in dtext(), dtext()); cap('o2-lance')
        rng(die(1, 1, 2)); option('Vas-y'); check(f'{T}: O: {{maison}} affiché', '1, 1, 2 (4)' in dtext(), dtext()); option('Alors')
        check(f'{T}: O: gagné : +1 $ net', 'billets' in dtext() and money() == m0 + 1, (m0, money())); option('Encore')
        rng(die(2, 3, 4)); option('Miser 3'); rng(die(6, 5, 6)); option('Vas-y'); option('Alors'); check(f'{T}: O: perdu : -3 $', 'chaussure' in dtext() and money() == m0 - 2, money()); option('Encore')
        rng(die(3, 4, 5)); option('Miser 1'); rng(die(4, 4, 4)); option('Vas-y'); option('Alors'); check(f'{T}: O: brelan de Teo bat 12', money() == m0 - 3); option('Encore')
        rng(die(2, 2, 2)); option('Miser 1'); rng(die(6, 6, 5)); option('Vas-y'); option('Alors'); check(f'{T}: O: brelan bat 17', money() == m0 - 2); option('Encore')
        rng(die(3, 3, 4)); option('Miser 3'); rng(die(4, 4, 2)); option('Vas-y'); option('Alors'); check(f'{T}: O: égalité : mise rendue', 'Pareil' in dtext() and money() == m0 - 2); option('Encore')
        rng(die(1, 1, 2) + [0.99] + die(6, 6, 6)); option('Miser 1'); option('Ta manche')
        check(f'{T}: O: bluff réussi, relance affichée', '6, 6, 6 (18)' in dtext(), dtext()); cap('o3-bluff')
        rng(die(1, 2, 3)); option('À toi'); check(f'{T}: O: après bluff, les dés relancés comptent (pas de 2e relance)', E("JSON.stringify(window.__nml.state.os.joueur)") == '[6,6,6]', E("JSON.stringify(window.__nml.state.os)"))
        option('Alors'); check(f'{T}: O: bluff gagné +1', money() == m0 - 1, money()); option('Encore')
        rng(die(1, 1, 2)); option('Miser 1'); check(f'{T}: O: un seul bluff par partie', not any('manche' in x for x in opts()), opts()); rng(die(1, 1, 3)); option('Vas-y'); option('Alors'); option('J\'arrête'); option('Salut'); close_dlg()
        teo(vol=0); rng(die(1, 1, 2) + [0.0]); m1 = money(); option('Miser 5'); option('Ta manche'); check(f'{T}: O: bluff raté', 'manche' in dtext()); option('Bon')
        check(f'{T}: O: bluff raté : mise perdue', money() == m1 - 5, (m1, money())); option('Salut'); close_dlg()
        g = E('window.__nml.state.osGains'); check(f'{T}: O: compteur de gains nets', g == -7, g)
        # plafond : 15 $ nets ; gain tronqué ; persistant à la sauvegarde
        teo(money=50, osg=0); m0 = money()
        for k in range(3):
            rng(die(6, 6, 5)); option('Miser 5'); rng(die(1, 1, 2)); option('Vas-y'); option('Alors')
            if k < 2: option('Encore')
        check(f'{T}: O: plafond atteint à +15 $ (refus de Teo)', 'C\'est fini' in dtext() and money() == m0 + 15, (money(), dtext()[:30])); cap('o4-plafond'); option('Salut, Teo'); close_dlg()
        E("window.__snapO = window.__nml.game.snapshot()"); E("window.__nml.game.restore(window.__S0, true)"); E("window.__nml.game.restore(window.__snapO, true)"); time.sleep(0.5)
        check(f'{T}: O: plafond persistant (sauvegarde/chargement)', E('window.__nml.state.osGains') == 15 and st()['flags'].get('os_plafond'))
        teo(); check(f'{T}: O: Teo ne joue plus', 'Jamais' in dtext() and not any('Miser' in x for x in opts()), opts()); cap('o5-teo-refuse'); close_dlg()
        teo(money=50, osg=12, clear=True); m0 = money(); rng(die(6, 6, 5)); option('Miser 5'); rng(die(1, 1, 2)); option('Vas-y'); option('Alors')
        check(f'{T}: O: gain tronqué (12 -> 15 : +3 $ et non +5)', money() == m0 + 3 and E('window.__nml.state.osGains') == 15 and 'C\'est fini' in dtext(), (m0, money())); close_dlg()
        teo(money=0, clear=True, osg=0); option('Miser 1'); check(f'{T}: O: sans argent : pauvre', 'Pas d\'argent' in dtext() and money() == 0, dtext()[:30]); close_dlg()
        msgs = E('window.__msgs')[msgs0:]; check(f'{T}: O: aucun « piste notée » pour les drapeaux os_*', not any('piste notée' in m for m in msgs), [m for m in msgs if 'Journal' in m][:3])
        press('#k-journal', 0.5); h = E("document.getElementById('panel-body').innerText"); press('#panel-close', 0.3)
        check(f'{T}: journal sans drapeau technique', 'os_' not in h and 'ramasse_' not in h)
        # ---------- Hector : sa place ----------
        reset(); x, z = near_door('bar_in_door'); place('bar_in', x, z); cap('h1-hector-place')
        check(f'{T}: Hector placé à Dusk-Town (bar_in, sprite gen_hector)', E("window.__nml.npcs.find(n=>n.id==='hector').location") == 'bar_in')
        tot = GAINS.get('A', 0) + GAINS.get('B', 0) + GAINS.get('F', 0)
        check(f'{T}: total gagnable hors dés = 49 $ (A {GAINS.get("A")} + B {GAINS.get("B")} + ferraille {GAINS.get("F")})', tot == 49, tot)
        check(f'{T}: aucune erreur console / réseau', not errs, errs[:3])
        ctx.close()
    br.close()
ok = sum(r['ok'] for r in R); print(f'{ok}/{len(R)}'); os.makedirs(OUT, exist_ok=True); json.dump(R, open(OUT + 'resultats.json', 'w'), ensure_ascii=False, indent=1); sys.exit(0 if ok == len(R) else 1)
