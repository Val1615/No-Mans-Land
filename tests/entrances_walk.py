# v7.1 : trajet RÉEL complet jusqu'à CHAQUE entrée de la ville, depuis le départ de partie, sans aucun placement par commande.
# Les étapes de marche sont des taps/clics au sol le long du chemin calculé (même pathfinder que le jeu) ; l'entrée se fait par
# geste sur la porte peinte (variante A) ou par tap au sol sur le seuil puis bouton « Entrer » (variante B). Bureau 1280x800, mobile 390x844.
import sys, os, time, io, json
from PIL import Image
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8765/'); OUT = os.environ.get('OUT', '/workspace/nml/docs/captures/dusk-v7/entrees/'); os.makedirs(OUT, exist_ok=True)
R = []
def check(n, ok, d=''): R.append({'test': n, 'ok': bool(ok), 'detail': str(d)}); print(('OK    ' if ok else 'ECHEC ') + n, d, flush=True)
# ordre de visite : (quartier, porte extérieure) ; les jonctions s'enchaînent par la marche
ROUTE = ['dusk_q1:mara_house_door', 'dusk_q1:clinic_door', 'dusk_q1:grocery_door', 'dusk_q1:grocery_door2', 'dusk_q1:bar_door',
         'dusk_q2:t_guet_door', 'dusk_q1:-', 'dusk_q3:s_atelier_door', 'dusk_q1:-', 'dusk_q4:d_citerne_door', 'dusk_q1:-']
JUN = {('dusk_q1', 'dusk_q2'): 'j_q1_est', ('dusk_q2', 'dusk_q1'): 'j_q2_ouest', ('dusk_q1', 'dusk_q3'): 'j_q1_nord', ('dusk_q3', 'dusk_q1'): 'j_q3_sud',
       ('dusk_q1', 'dusk_q4'): 'j_q1_sud', ('dusk_q4', 'dusk_q1'): 'j_q4_nord'}
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for prof in os.environ.get('PROFILES', 'desktop,mobile').split(','):
        ctx = br.new_context(viewport={'width': 1280, 'height': 800}) if prof == 'desktop' else br.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2)
        pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(URL); pg.wait_for_function('window.__nml', timeout=60000); [(pg.locator(_s).tap if pg.evaluate('navigator.maxTouchPoints>0') else pg.locator(_s).click)() for _s in ('#m-new', '#cr-next', '#cr-enter')]; pg.wait_for_function('!document.body.classList.contains("menu-open")'); time.sleep(2.5)
        pg.evaluate("import('./src/core/path.js').then(m => window.__findPath = m.findPath)"); time.sleep(0.5)
        VW, VH = (1280, 800) if prof == 'desktop' else (390, 844)
        gesture = pg.touchscreen.tap if prof == 'mobile' else pg.mouse.click
        E = pg.evaluate; st = lambda: E('JSON.parse(JSON.stringify(window.__nml.state))')
        P = lambda x, y, z: E(f'window.__nml.project({x},{y},{z})')
        onscreen = lambda pt: 20 < pt['x'] < VW - 20 and 120 < pt['y'] < VH - 100
        def idle(t=30):
            t0 = time.time()
            while time.time() - t0 < t:
                if E('(()=>{const s=window.__nml.state;return !s.player.path.length && !s.player.pending})()'): time.sleep(0.3); return True
                time.sleep(0.1)
            return False
        def walk(x, z, tol=0.7):
            """Taps au sol vers le point visible le plus lointain du chemin du jeu. Renvoie True si arrivé (ou changement de lieu)."""
            loc0 = st()['location']
            for _ in range(20):
                s = st()
                if s['location'] != loc0: return True
                pl = s['player']
                if ((x - pl['x'])**2 + (z - pl['z'])**2) ** 0.5 < tol: return True
                path = E(f"(()=>{{const g=window.__nml.game; const p=window.__findPath(g.grids[g.state.location], g.state.player, {{x:{x},z:{z}}}); return p}})()")
                if not path: return False
                tapped = False
                for q in reversed(path[1:]):
                    pt = P(q['x'], 0, q['z'])
                    if not onscreen(pt): continue
                    k = E(f'window.__nml.pick({pt["x"]},{pt["y"]})')
                    if not k or k['kind'] != 'ground' or ((k['x'] - q['x'])**2 + (k['z'] - q['z'])**2) ** 0.5 > 1.0: continue
                    if E(f"window.__nml.doors.some(d=>(d.junction||d.edge)&&d.location===window.__nml.state.location&&Math.hypot(d.threshold.x-{k['x']},d.threshold.z-{k['z']})<1.6)") and ((q['x']-x)**2+(q['z']-z)**2)**0.5 > 2: continue
                    gesture(pt['x'], pt['y']); tapped = True; break
                if not tapped: return False
                idle()
            return False
        def cross(dest):
            j = E(f"window.__nml.game.doorById('{JUN[(st()['location'], dest)]}').threshold")
            walk(j['x'], j['z']); ok = E(f'new Promise(r=>{{const t0=Date.now();const f=()=>window.__nml.state.location==="{dest}"?r(true):Date.now()-t0>6000?r(false):setTimeout(f,100);f()}})')
            time.sleep(0.8); walk_away()
            return ok
        def walk_away():  # quitter le seuil d'arrivée (verrou anti-rebond) d'un pas
            s = st()['player']; walk(s['x'] + (2 if s['x'] < 24 else -2), s['z'] + (2 if s['z'] < 18 else -2), tol=1.2)
        def enter(door, variant):
            d = E(f"window.__nml.game.doorById('{door}')"); t = d['threshold']; inside = E(f"window.__nml.game.doorById('{door}').target.doorId").replace('_door2', '_door')
            inside = E(f"window.__nml.game.doorById(window.__nml.game.doorById('{door}').target.doorId).location")
            if variant == 'A':  # approche à ~4 m puis geste sur la porte peinte
                walk(t['x'] + (3 if d['opening']['side'] == 'east' else 0), t['z'] + (0 if d['opening']['side'] == 'east' else 3), tol=1.5)
                pt = P(d['opening']['x'], 1.0, d['opening']['z']); gesture(pt['x'], pt['y'])
            else:  # tap au sol jusqu'au seuil puis bouton
                walk(t['x'], t['z'], tol=0.6); b = pg.locator('#act'); 
                if b.is_visible(): bb = b.bounding_box(); gesture(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2)
            ok = E(f'new Promise(r=>{{const t0=Date.now();const f=()=>window.__nml.state.location==="{inside}"?r(true):Date.now()-t0>25000?r(false):setTimeout(f,100);f()}})')
            s = st(); check(f'{prof}: {door} ({"geste porte peinte" if variant == "A" else "tap seuil + bouton"}) : entré depuis le trajet réel', ok, (s['location'], round(s['player']['x'], 1), round(s['player']['z'], 1)))
            if ok:
                time.sleep(0.8); pg.screenshot(path=OUT + f'{prof}-{door}-{variant}.png')
                o = E(f"window.__nml.doors.find(d=>d.location==='{inside}')"); pt = P(o['opening']['x'], 1.0, o['opening']['z']); gesture(pt['x'], pt['y'])
                E('new Promise(r=>{const l=window.__nml.state.location;const t0=Date.now();const f=()=>!window.__nml.game.world.LOCATIONS[window.__nml.state.location].kind.includes("interior")?r(true):Date.now()-t0>25000?r(false):setTimeout(f,100);f()})')
                time.sleep(0.5); walk_away()
            return ok
        # l'indice de Teo doit désigner sans ambiguïté le lieu révélé (bug v7 : « la maison basse » = nom d'un bâtiment fermé du Transit)
        h = E("""(async()=>{const m=await import('./src/data/dialogues_town.js'); const t=m.DIALOGUES.teo.tuyau; const all=Object.values(window.__nml.game.world.LOCATIONS).flatMap(l=>l.buildings.map(b=>({...b,loc:l.id})));
          const tgt=t.options[0].action.split(':')[1], b=all.find(b=>b.id===tgt), low=t.text.toLowerCase();
          return {named: low.includes(b.label.toLowerCase()), quartier: low.includes('scellé') && b.loc==='dusk_q3', faux: all.filter(o=>o.id!==tgt && low.includes(o.label.toLowerCase())).map(o=>o.label)}})()""")
        check(f'{prof}: indice de Teo : nomme L\'atelier et son quartier, aucun autre bâtiment homonyme', h['named'] and h['quartier'] and not h['faux'], h)
        for step in ROUTE:
            loc, door = step.split(':')
            if st()['location'] != loc:
                if loc != 'dusk_q1' and st()['location'] != 'dusk_q1': cross('dusk_q1')
                ok = cross(loc); check(f'{prof}: jonction vers {loc} par la marche', ok, st()['location'])
            if door != '-':
                for v in ('A', 'B'): enter(door, v)
        check(f'{prof}: aucune erreur page', not errs, errs[:2]); ctx.close()
    br.close()
ok = sum(r['ok'] for r in R); print(f'{ok}/{len(R)}'); json.dump(R, open(OUT + 'entrances_walk.json', 'w'), indent=1, ensure_ascii=False)
sys.exit(0 if ok == len(R) else 1)
