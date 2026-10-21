# Recette navigateur réelle du quartier Dusk-Town Q1 (Chrome headless, WebGL logiciel).
# Gestes réels : clics souris (bureau) et taps tactiles (mobile). Captures = rendu réel du jeu.
import json, time, os
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8765/'); OUT = os.environ.get('OUT', '/workspace/nml/docs/captures/dusk-q1-v6/')
R = []
import os
DEBUG = os.environ.get('DEBUG')
PROFILES = os.environ.get('PROFILES','desktop,mobile').split(',')
def check(name, ok, detail=''):
    R.append({'test': name, 'ok': bool(ok), 'detail': str(detail)}); print(('OK    ' if ok else 'ECHEC ') + name, detail)
def st(pg): return pg.evaluate('JSON.parse(JSON.stringify(window.__nml.state))')
def wait(pg, js, t=20):
    t0 = time.time()
    while time.time() - t0 < t:
        if pg.evaluate(js): return True
        time.sleep(0.1)
    return False
def comp_ok(s): c = s['companion']; return c['mode'] == 'follow' and c['location'] == s['location'] and ((c['x']-s['player']['x'])**2+(c['z']-s['player']['z'])**2)**.5 < 2.5

with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for prof in PROFILES:
        ctx = b.new_context(viewport={'width': 1280, 'height': 800}) if prof == 'desktop' else b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2)
        pg = ctx.new_page(); errs = []
        pg.on('response', lambda r: r.status >= 400 and errs.append(f'{r.status} {r.url}')); pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and 'Failed to load resource' not in m.text and errs.append(m.text))
        pg.goto(URL); pg.wait_for_function('window.__nml'); time.sleep(2.5)
        def gesture(x, y): (pg.touchscreen.tap if prof == 'mobile' else pg.mouse.click)(x, y)
        def tap_world(x, y, z): pt = pg.evaluate(f'window.__nml.project({x},{y},{z})'); gesture(pt['x'], pt['y'])
        VW, VH = (1280, 800) if prof == 'desktop' else (390, 844)
        cmd_moves = []
        def walk_to(x, z):
            # Marche par gestes réels au sol, par étapes visibles à l'écran.
            for _ in range(8):
                s = st(pg); px, pz = s['player']['x'], s['player']['z']
                if ((px-x)**2 + (pz-z)**2) ** .5 < 1.0: return True
                for f in (1.0, 0.7, 0.5, 0.35, 0.2):
                    tx, tz = px + (x-px)*f, pz + (z-pz)*f
                    pt = pg.evaluate(f'window.__nml.project({tx},0,{tz})')
                    if 30 < pt['x'] < VW-30 and 120 < pt['y'] < VH-90 and (pg.evaluate(f"(window.__nml.pick({pt['x']},{pt['y']})||{{}}).kind") == 'ground'): break
                gesture(pt['x'], pt['y']); time.sleep(0.2)
                if DEBUG: print('  walk', (round(px,1), round(pz,1)), '->', (round(tx,1), round(tz,1)), pt, st(pg)['player']['path'][:1], st(pg)['log'][-1:] )
                wait(pg, 'window.__nml.state.player.path.length===0', 20); time.sleep(0.3)
            return False
        def press(sel): (pg.locator(sel).first.tap() if prof == 'mobile' else pg.locator(sel).first.click())
        def option(text): press(f'#dlg-options button:has-text("{text}")'); time.sleep(0.3)
        pg.screenshot(path=f'{OUT}{prof}-01-arrivee.png')
        if prof == 'desktop':
            pg.evaluate('window.__nml.setCamera({x:24,z:18,ppm:22})'); time.sleep(0.8); pg.screenshot(path=f'{OUT}desktop-00-vue-ensemble.png')
            pg.evaluate('window.__nml.setCamera(null)'); time.sleep(0.5)
        # --- Étiquettes : aucune avant découverte
        vis = lambda: pg.evaluate('[...document.querySelectorAll(".wlabel.service")].filter(e=>!e.hidden).map(e=>e.dataset.building)')
        check(f'{prof}: aucune étiquette de service avant découverte', vis() == [], vis())
        if prof == 'desktop':
            pg.evaluate('window.__nml.setCamera({x:24,z:18,ppm:22})'); time.sleep(0.8); pg.screenshot(path=f'{OUT}desktop-06-avant-decouverte.png'); pg.evaluate('window.__nml.setCamera(null)'); time.sleep(0.4)
        # --- Orientation : miroir selon le sens de marche à l'écran
        sp = st(pg)['player']; walk_to(sp['x'] + 6, sp['z']); time.sleep(0.6)
        check(f'{prof}: joueur tourné vers la droite en marchant vers la droite', pg.evaluate("window.__nml.view.facingOf('player')") == 1)
        check(f'{prof}: compagnon tourné vers la droite en suivant', pg.evaluate("window.__nml.view.facingOf('companion')") == 1)
        walk_to(sp['x'], sp['z']); time.sleep(0.6)
        check(f'{prof}: joueur retourné (miroir) en marchant vers la gauche', pg.evaluate("window.__nml.view.facingOf('player')") == -1)
        check(f'{prof}: compagnon retourné en marchant vers la gauche', pg.evaluate("window.__nml.view.facingOf('companion')") == -1)
        def npc_faces_player(n):
            s = st(pg); N = pg.evaluate(f'window.__nml.npcs.find(x=>x.id==="{n}")')
            sx = pg.evaluate(f"window.__nml.view.screenRightOf({s['player']['x']-N['x']},{s['player']['z']-N['z']})")
            f = pg.evaluate(f"window.__nml.view.facingOf('{n}')"); return abs(sx) < 0.2 or f == (1 if sx > 0 else -1), (round(sx, 2), f)
        # --- Rues vides (décision de Valentin)
        n_out = pg.evaluate('window.__nml.npcs.filter(n=>n.location==="dusk_q1").length')
        check(f'{prof}: aucun PNJ dans les rues', n_out == 0, f'{n_out} PNJ dehors')
        # --- Services : (bâtiment, point de geste, intérieur, PNJ, action, vérif)
        D = {d['buildingId']: d for d in reversed(pg.evaluate('window.__nml.doors.filter(d=>d.buildingId)'))}
        door_pt = lambda b: (D[b]['opening']['x'], 1.0, D[b]['opening']['z'])  # geste sur la porte peinte
        services = [
            ('mara_house', door_pt('mara_house'), 'mara_in', 'mara', (1.0, 1.0, 2.0), None, None),
            ('grocery', door_pt('grocery'), 'grocery_in', 'anselme', (2.2, 1.0, 4.2), 'bouteille', lambda a, z: z['player']['inv'].get('water') == 1 and z['player']['money'] == a['player']['money'] - 4),
            ('bar', door_pt('bar'), 'bar_in', 'hector', (4.0, 1.0, 1.4), 'Un repas', lambda a, z: z['player']['money'] == a['player']['money'] - 6 and z['player']['hp'] == min(40, a['player']['hp'] + 5)),
            ('clinic', door_pt('clinic'), 'clinic_in', 'vera', (6.2, 1.0, 1.6), None, None)]
        approach = {'mara_house': [(5, 16.5)], 'grocery': [(23.5, 17)], 'bar': [(26, 19), (36, 17)], 'clinic': [(14, 17)]}
        # --- v4 : sprites entiers ; base visible = emprise déclarée ; porte peinte = ouverture monde
        for bb in pg.evaluate('window.__nml.game.location.buildings.map(b=>b.id)'):
            a = pg.evaluate(f"window.__nml.view.baseAlpha('{bb}')"); check(f'{prof}: {bb} base du sprite opaque aux 3 coins de l emprise', min(a) > 0.5, a)
        for d in pg.evaluate('window.__nml.doors.filter(d=>d.painted && d.location==="dusk_q1").map(d=>d.id)'):
            e = pg.evaluate(f"window.__nml.view.paintedDoorError('{d}')"); check(f'{prof}: {d} porte peinte alignée sur l ouverture (< 0,8 m)', e < 0.8, f'{e} m')
        g = pg.evaluate('(()=>{const g=window.__nml.game.grids.dusk_q1;return window.__nml.game.location.buildings.every(b=>{const [i,j]=g.toCell(b.x+b.w/2,b.z+b.d/2);return !g.free(i,j)})})()')
        check(f'{prof}: centre de chaque emprise bloqué (collision = base)', g)
        for bid, pt, inside, npc, npos, opt, verify in services:
            r_ok = all([walk_to(*w) for w in approach[bid]]); (not r_ok) and print('  approche ratée', bid, st(pg)['player']['x'], st(pg)['player']['z'], st(pg)['log'][-2:]); tap_world(*pt)
            ok = wait(pg, f'window.__nml.state.location==="{inside}"', 25)
            s = st(pg); check(f'{prof}: {bid} -> entrée ({"tap porte" if prof=="mobile" else "clic façade"})', ok, s['location'])
            check(f'{prof}: {bid} -> compagnon entré', comp_ok(s))
            time.sleep(0.6)
            tap_world(*npos)
            check(f'{prof}: {bid} -> dialogue {npc} ouvert', wait(pg, f'window.__nml.state.dialogue && window.__nml.state.dialogue.npc==="{npc}"'))
            time.sleep(0.4)
            ok_f, det = npc_faces_player(npc); check(f'{prof}: {npc} tourné vers le joueur pendant le dialogue', ok_f, det)
            if bid == 'clinic': pg.screenshot(path=f'{OUT}{prof}-04-interieur-clinique-dialogue.png')
            if bid == 'mara_house': pg.screenshot(path=f'{OUT}{prof}-02-chez-mara.png')
            before = st(pg)
            if bid == 'mara_house':
                option('Il n\'y avait personne'); option('qui'); txt = pg.locator('#dlg-text').inner_text(); option('accord')
                check(f'{prof}: Mara évoque les soldats de la capitale', 'soldats' in txt and not st(pg)['dialogue'], txt[:50])
                tap_world(1.0, 1.0, 2.0); wait(pg, 'window.__nml.state.dialogue', 10); option('pompe'); option('chercher')
                check(f'{prof}: piste de la pompe notée', st(pg)['flags'].get('pompe_aide') is True); option('Promis')
                time.sleep(0.4); tap_world(3.8, 1.0, 1.6)
                check(f'{prof}: dialogue Bruno (mutant caché) ouvert', wait(pg, 'window.__nml.state.dialogue && window.__nml.state.dialogue.npc==="bruno"'))
                time.sleep(0.3); ok_f, det = npc_faces_player('bruno'); check(f'{prof}: bruno tourné vers le joueur pendant le dialogue', ok_f, det)
                time.sleep(0.3); pg.screenshot(path=f'{OUT}{prof}-02-dialogue-bruno.png')
                option('Tu vis ici'); txt = pg.locator('#dlg-text').inner_text(); option('emmené'); option('Merci')
                check(f'{prof}: Bruno raconte la rafle puis ferme', 'patrouille' in txt and not st(pg)['dialogue'], txt[:50])
            elif bid == 'clinic':
                option('aplomb'); option('Payer 15'); after = st(pg)
                check(f'{prof}: soin Vera payé (PV au max, -15 $)', after['player']['hp'] == 40 and after['player']['money'] == before['player']['money'] - 15, f"PV {before['player']['hp']}->{after['player']['hp']}, {before['player']['money']}->{after['player']['money']} $")
                press('#dlg-close'); check(f'{prof}: fermeture par le bouton ×', wait(pg, '!window.__nml.state.dialogue', 3))
            else:
                option(opt); after = st(pg)
                check(f'{prof}: service {npc} effectué', verify(before, after), f"argent {before['player']['money']}->{after['player']['money']}, PV {after['player']['hp']}, inv {after['player']['inv']}")
                press('#dlg-options button:last-child'); wait(pg, '!window.__nml.state.dialogue', 3)
                check(f'{prof}: dialogue {npc} fermé', not st(pg)['dialogue'])
            if bid == 'bar':
                tap_world(8.9, 1.0, 3.6)
                check(f'{prof}: dialogue Ileana (Invictos) ouvert', wait(pg, 'window.__nml.state.dialogue && window.__nml.state.dialogue.npc==="ileana"'))
                option('pas d\'ici'); txt = pg.locator('#dlg-text').inner_text(); time.sleep(0.3); pg.screenshot(path=f'{OUT}{prof}-03-interieur-bar-ileana.png'); option('Et tu fais quoi'); option('Bonne attente')
                check(f'{prof}: Ileana parcourue puis fermée', 'Invictos' in txt and not st(pg)['dialogue'], txt[:50])
            # sortie
            d = pg.evaluate(f'window.__nml.doors.find(d=>d.location==="{inside}")')
            if prof == 'mobile':
                walk_to(d['threshold']['x'] - (1 if d['opening']['side'] == 'east' else 0), d['threshold']['z'] - (1 if d['opening']['side'] == 'south' else 0))
                wait(pg, '!document.getElementById("act").hidden', 5); press('#act')
            else:
                d = pg.evaluate(f'window.__nml.doors.find(d=>d.location==="{inside}")'); tap_world(d['opening']['x'], 1.0, d['opening']['z'])
            ok = wait(pg, 'window.__nml.state.location==="dusk_q1"', 25); s = st(pg)
            d = pg.evaluate(f'window.__nml.doors.find(d=>d.buildingId==="{bid}")')
            check(f'{prof}: {bid} -> sortie au seuil extérieur', ok and abs(s['player']['x']-d['threshold']['x']) < .05 and abs(s['player']['z']-d['threshold']['z']) < .05, f"({s['player']['x']},{s['player']['z']})")
            check(f'{prof}: {bid} -> compagnon ressorti', comp_ok(s))
            if prof == 'desktop' and bid == 'bar':
                time.sleep(0.5); pg.evaluate(f"window.__nml.setCamera({{x:{d['threshold']['x']},z:{d['threshold']['z']-2},ppm:70}})"); time.sleep(0.8); pg.screenshot(path=f'{OUT}desktop-09-porte-peinte-bar.png'); pg.evaluate('window.__nml.setCamera(null)'); time.sleep(0.4)
            time.sleep(0.2); v = vis()
            check(f'{prof}: étiquette {bid} affichée après être entré', bid in v, v)
            if bid == 'mara_house': check(f'{prof}: étiquette clinique affichée car Mara en a parlé (avant d\'y entrer), épicerie et bar toujours masqués', 'clinic' in v and 'grocery' not in v and 'bar' not in v, v)
        v = vis(); check(f'{prof}: les 4 étiquettes persistent après sortie', sorted(v) == ['bar', 'clinic', 'grocery', 'mara_house'], v)
        if prof == 'desktop':
            pg.evaluate('window.__nml.setCamera({x:24,z:18,ppm:22})'); time.sleep(0.8); pg.screenshot(path=f'{OUT}desktop-07-apres-decouverte.png'); pg.evaluate('window.__nml.setCamera(null)'); time.sleep(0.4)
        # --- Bâtiment non visitable : retour neutre, pas de transition
        walk_to(40, 17); n0 = st(pg)['transitions']; tap_world(44, 2.5, 13.0)
        time.sleep(0.5); check(f'{prof}: immeuble muré non visitable (pas de transition)', st(pg)['transitions'] == n0 and 'fermé' in pg.locator('#msg').inner_text(), pg.locator('#msg').inner_text())
        # --- Restriction : sortie est. v7 : l'épave barre toujours l'avenue ; seul le passage piéton côté sud (z 20) mène au Transit
        pg.evaluate('window.__nml.game.moveTo(45.5, 16.6)'); time.sleep(0.2); wait(pg, 'window.__nml.state.player.path.length===0', 20)
        s = st(pg); inw = 43.2 <= s['player']['x'] <= 47.8 and 15.4 <= s['player']['z'] <= 17.8
        check(f'{prof}: sortie est : épave infranchissable, passage piéton seulement (v7)', not inw and s['location'] == 'dusk_q1', f"final=({s['player']['x']:.1f},{s['player']['z']:.1f}) {s['location']}")
        # --- Occultation derrière le bar
        pg.evaluate('window.__nml.game.moveTo(34, 5)'); wait(pg, 'Math.hypot(window.__nml.state.player.x-34, window.__nml.state.player.z-5)<0.3', 30); time.sleep(1.2)
        op = pg.evaluate("window.__nml.opacityOf('bar')"); check(f'{prof}: bar transparent quand le joueur est derrière', op < 0.5, f'opacité={op:.2f}')
        pg.screenshot(path=f'{OUT}{prof}-05-occultation.png')
        check(f'{prof}: aucune erreur console', not errs, '; '.join(errs)[:300])
        ctx.close()
    b.close()
json.dump(R, open(OUT + 'resultats.json', 'w'), ensure_ascii=False, indent=1)
print(sum(r['ok'] for r in R), '/', len(R))
