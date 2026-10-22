# Captures réelles (Playwright Chromium/swiftshader) des scènes de Volonté et éléments v15. Usage : python3 tests/volonte_captures.py [glow-avant|glow-apres]
import json, os, sys, time
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8799/'; OUT = 'docs/captures/volonte-v1/'; ONLY = sys.argv[1] if len(sys.argv) > 1 else None
ERR = {}
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    def session(race, name):
        ctx = br.new_context(viewport={'width': 1280, 'height': 800}); pg = ctx.new_page(); errs = []; ERR[name] = errs
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append('console: ' + m.text))
        pg.on('response', lambda r: r.status >= 400 and errs.append(f'{r.status} {r.url}'))
        E = pg.evaluate
        def press(sel, wait=0.4):
            E(f'(()=>{{const e=document.querySelector({json.dumps(sel)}); if(e) e.scrollIntoView({{block:"center"}})}})()'); time.sleep(0.1)
            b = pg.locator(sel).first.bounding_box(); pg.mouse.click(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2); time.sleep(wait)
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=60000); time.sleep(1.5)
        E("import('./src/core/path.js').then(m => window.__findPath = m.findPath)")
        press('#m-new', 0.6); press(f'[data-race="{race}"]', 0.8)
        return ctx, pg, E, press
    def waitjs(E, js, t=20):
        t0 = time.time()
        while time.time() - t0 < t:
            if E(js): return True
            time.sleep(0.1)
        return False
    def place(E, loc, x, z, vol, flags=None):
        E(f"(()=>{{const g=window.__nml.game,s=g.snapshot();s.location='{loc}';s.player.x={x};s.player.z={z};s.character.attrs.volonte={vol};s.money=100;Object.assign(s.flags,{json.dumps(flags or {})});g.restore(s,true)}})()"); time.sleep(1.5)
    def option(pg, label):
        b = pg.locator('#dlg-options button', has_text=label).first.bounding_box(); pg.mouse.click(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2); time.sleep(0.8)
    def shot(pg, n): time.sleep(0.6); pg.screenshot(path=OUT + n); print('capture', n, flush=True)
    if not ONLY:
        # 6. création : portraits mutant / cyborg
        for race in ('mutant', 'cyborg'):
            ctx, pg, E, press = session(race, 'creation-' + race)
            for i in range(4):
                shot(pg, f'06-creation-{race}-visage{i + 1}.png') if i in (1, 2, 3) else None
                press('#cr-next-face', 0.6)
            ctx.close()
        ctx, pg, E, press = session('augmente', 'jeu'); press('#cr-next', 0.5); press('#cr-enter', 1.5)
        # 1. trois scènes réussite / échec
        scenes = [('odile', 'odile_volonte', 'douane_in', 4.2, 3.0, 'formulaire', 'Je ne signerai rien.', {}),
                  ('guetteuse', 'guetteuse_volonte', 'sv_poutres', 30.5, 15.2, 'alors', 'Va le lui dire', {}),
                  ('dealer', 'dealer_volonte', 'tripot_in', 4.4, 3.6, 'dette', 'Je ne te dois rien.', {})]
        for npc, tree, loc, x, z, node, lab, fl in scenes:
            for vol, res in ((10, 'reussi'), (1, 'rate')):
                place(E, loc, x, z, vol, fl)
                E(f"(()=>{{const s=window.__nml.state; s.dialogue={{npc:'{npc}',node:'{node}',tree:'{tree}'}}}})()")
                waitjs(E, "!document.getElementById('dialogue').hidden"); time.sleep(0.5); option(pg, lab)
                got = E('window.__nml.state.dialogue && window.__nml.state.dialogue.node'); print(npc, res, '->', got, flush=True)
                shot(pg, f'01-{npc}-{res}-{got}.png'); E('window.__nml.state.dialogue=null'); time.sleep(0.3)
        # 2. Odile interpelle l'augmenté au passage réel de la porte douane_in_est
        place(E, 'douane_in', 7.5, 4.0, 6, {'race_augmente': True, 'steel_passe': True})
        d = E("window.__nml.game.doorById('douane_in_est').threshold"); pt = E(f"window.__nml.project({d['x']},0,{d['z']})")
        pg.mouse.click(pt['x'], pt['y']); time.sleep(0.4)
        for _ in range(40):
            if E('!!window.__nml.state.dialogue'): break
            if E("!document.getElementById('act').hidden"): press('#act', 0.3)
            time.sleep(0.25)
        print('interruption', E('JSON.stringify(window.__nml.state.dialogue)'), E('window.__nml.state.location'), flush=True)
        time.sleep(1.0); shot(pg, '02-odile-interpelle-augmente.png'); print('joueur', E('JSON.stringify([window.__nml.state.player.x,window.__nml.state.player.z])'), 'ecran', E("JSON.stringify(window.__nml.project(9.5,0,4))")); E('window.__nml.state.dialogue=null')
        # 5. porte du dôme
        place(E, 'steel_route', 34, 20, 6); E("window.__nml.view.setCamera({x:32,z:5,ppm:20})"); shot(pg, '05-steel-route-porte-dome.png')
        ctx.close()
    # 3/4. Tripot avec sv_cardtable_b (glow avant/après)
    ctx, pg, E, press = session('humain', 'tripot'); press('#cr-next', 0.5); press('#cr-enter', 1.5)
    place(E, 'tripot_in', 2.5, 4.5, 6); shot(pg, f'03-tripot-table-b{("-" + ONLY) if ONLY else ""}.png'); ctx.close()
    br.close()
for k, v in ERR.items(): print('ERREURS', k, len(v), v[:5])
