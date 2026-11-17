# Test rapide Mega-Line v2 (64 x 40 m) et terminus v2 (40 x 28 m), plan du 17/11 (docs/villes/steel/quartiers/mega_line/MEGALINE_V2_IMPL.md).
# Vérifie : chargement des deux lieux, passages de portes (c_mega <-> ml_sud, ml_passerelle <-> tm_sud), quai à +6 m atteint seulement par les
# escaliers (chemins, bande d'embarquement fermée, aucun saut de niveau), portes du sas jamais ouvrables, PNJ présents et abordables, gabarits en
# modules d'Ocre posés (lots 1 et 2) sur la ligne, gabarits du terminus, rame avant/dos qui passe sans s'arrêter, tri du peintre (poutres _avant),
# écrans Vibes O / Tron E dans les cadres, migration des sauvegardes de l'ancien plan, aucune erreur console. Captures 1280x800 et 390x844.
# Env : URL (défaut http://127.0.0.1:8915/), OUT (défaut /tmp/nml-test-out/megaline_plan/). Intro sautée (navigateur piloté) ; ?dev=1&map=... possible via MAP=1.
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from nml_boot import passer_boot
import time, os, sys, json
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8915/')
if not URL.endswith('/'): URL += '/'
OUT = os.environ.get('OUT', '/tmp/nml-test-out/megaline_lots12/'); OUT = OUT if OUT.endswith('/') else OUT + '/'; os.makedirs(OUT + 'livraison', exist_ok=True)
fails = []; n = 0
def ok(c, m, d=''):
    global n; print(('OK   ' if c else 'ECHEC ') + m + ('' if c else f'  {d}'), flush=True); n += bool(c); c or fails.append(m)
def hsol(niv, x, z):
    h = 0
    for q in niv or []:
        if x < q['x'] or x > q['x'] + q['w'] or z < q['z'] or z > q['z'] + q['d']: continue
        y = q['y'] if 'y' in q else (q['y0'] + (q['y1'] - q['y0']) * ((x - q['x']) / q['w'] if q.get('axe') == 'x' else (z - q['z']) / q['d']))
        h = max(h, y)
    return h
ESC = [(18, 22, 3, 10), (43, 22, 3, 10)]
dans = lambda r, x, z: r[0] <= x <= r[0] + r[2] and r[1] <= z <= r[1] + r[3]
NPC_LIGNE = ['ml_controleuse', 'ml_navetteur', 'ml_vigile', 'ml_etudiante', 'ml_fan', 'ml_pancarte', 'ml_entretien', 'ml_nouilles', 'ml_rivet']
NPC_TERM = ['ml_regie', 'ml_cheffe', 'ml_docker']
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for name, vp, mob in [('desktop', (1280, 800), False), ('mobile', (390, 844), True)]:
        errs = []; ctx = br.new_context(viewport={'width': vp[0], 'height': vp[1]}, has_touch=mob, is_mobile=mob); pg = ctx.new_page(); E = pg.evaluate
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=90000); time.sleep(1)
        E("localStorage.removeItem('nml_save_auto')"); passer_boot(E); E("document.getElementById('m-new').click()"); time.sleep(.5)
        E("document.querySelector('[data-race=\"humain\"]').click()"); time.sleep(.3); E("document.getElementById('cr-next').click()"); time.sleep(.3); E("document.getElementById('cr-enter').click()"); time.sleep(1.5)
        loc = lambda: E("window.__nml.state.location"); pos = lambda: E("[window.__nml.state.player.x, window.__nml.state.player.z]")
        def tp(l, x, z, plans=True):
            E(f"(()=>{{const g=window.__nml.game,s=g.snapshot();s.location='{l}';s.player.x={x};s.player.z={z};{'' if plans else 'delete s.plans;'}g.restore(s,true)}})()")
        def pret(l, t=40):
            t0 = time.time()
            while time.time() - t0 < t and not E(f"window.__nml.lieuPret('{l}')"): time.sleep(.3)
            time.sleep(1.2)
        def walk(x, z, t=60):
            r = E(f"window.__nml.game.moveTo({x},{z})"); t0 = time.time()
            while time.time() - t0 < t and E("window.__nml.state.player.path.length>0"): time.sleep(.3)
            q = pos(); return abs(q[0] - x) < 1.3 and abs(q[1] - z) < 1.3, q, r
        W = E("(()=>{const L=window.__nml.world.LOCATIONS;return {ml:{size:L.steel_megaline.size,niv:L.steel_megaline.niveaux,plan:L.steel_megaline.plan},tm:{size:L.steel_terminus.size,niv:L.steel_terminus.niveaux}}})()")
        ok(W['ml']['size'] == {'w': 64, 'd': 40} and W['tm']['size'] == {'w': 40, 'd': 28}, f'{name} emprises 64 x 40 et 40 x 28', W)
        # 1) Center-Town -> Mega-Line (c_mega), arrivée au centre du bord sud
        tp('steel_center', 1, 50); pret('steel_center'); E("window.__nml.game.useDoor('c_mega')"); time.sleep(2); pret('steel_megaline')
        q = pos(); ok(loc() == 'steel_megaline' and abs(q[0] - 32) < 1.5 and q[1] > 37, f'{name} Center-Town (c_mega) -> Mega-Line, arrivée au parvis sud', (loc(), q))
        time.sleep(1.5); pg.screenshot(path=OUT + f'{name}_ligne_arrivee.png')
        # 2) quai à +6 m : chemin depuis la rue par un escalier, jamais de saut de niveau
        r = E("window.__nml.game.moveTo(31,20.4)"); P = E("window.__nml.state.player.path.map(p=>[p.x,p.z])")
        hs = [hsol(W['ml']['niv'], x, z) for x, z in P]
        inter = [(x, z) for (x, z), h in zip(P, hs) if 0.05 < h < 5.95]
        sauts = [i for i in range(1, len(hs)) if abs(hs[i] - hs[i - 1]) > 0.9]
        ok(bool(r.get('ok')) and hs and hs[-1] == 6, f'{name} quai : chemin depuis le parvis jusqu au quai (+6 m)', (r, hs[-3:] if hs else None))
        ok(inter and all(any(dans(e, x, z) for e in ESC) for x, z in inter), f'{name} quai : montée uniquement dans un escalier ({len(inter)} pas en pente)', inter[:5])
        ok(not sauts, f'{name} quai : aucun saut de niveau (> 0,9 m entre deux pas)', [(P[i - 1], P[i], hs[i - 1], hs[i]) for i in sauts[:3]])
        E("window.__nml.state.player.path.length=0")
        # depuis la rue latérale ouest, juste sous le bord du quai : le chemin fait le détour par l'escalier
        tp('steel_megaline', 15.5, 18); time.sleep(.5); r = E("window.__nml.game.moveTo(20,18.5)"); P = E("window.__nml.state.player.path.map(p=>[p.x,p.z])")
        ok(bool(r.get('ok')) and any(dans(ESC[0], x, z) or dans(ESC[1], x, z) for x, z in P) and len(P) > 20, f'{name} quai : depuis la rue sous le quai, détour par l escalier ({len(P)} pas)', P[:4])
        E("window.__nml.state.player.path.length=0")
        # bande d'embarquement : fermée (barrières + portique), même depuis le quai
        tp('steel_megaline', 30, 20); time.sleep(.5); r = E("window.__nml.game.moveTo(28,15.6)"); P = E("window.__nml.state.player.path.map(p=>[p.x,p.z])")
        ok(not any(18 < x < 46 and z < 17.35 for x, z in P), f'{name} quai : bande d embarquement inaccessible à pied', (r, P[-3:]))
        E("window.__nml.state.player.path.length=0")
        # marche réelle : parvis -> quai par l'escalier, rendu à +6 m
        tp('steel_megaline', 32, 38.2); time.sleep(.5); rr, q, _ = walk(30.5, 20.6, 60)
        hy = E("(()=>{const v=window.__nml.view; return v.project ? null : null})()")
        ok(rr and hsol(W['ml']['niv'], *q) == 6, f'{name} quai : le joueur monte sur le quai à pied', q)
        t0 = time.time()
        while time.time() - t0 < 32 and not (E("window.__nml.view.rameEtat()[0]||{}").get('passe') and 14 < E("window.__nml.view.rameEtat()[0].x") < 70): time.sleep(.4)
        time.sleep(.3); pg.screenshot(path=OUT + f'{name}_ligne_quai.png')
        lab = E("[...document.querySelectorAll('#labels [data-npc]')].filter(e=>!e.hidden).map(e=>e.dataset.npc)")
        # 3) PNJ présents et abordables (chemin à leur niveau)
        pres = E("window.__nml.world.NPCS.filter(n=>n.location==='steel_megaline').map(n=>n.id)")
        ok(all(i in pres for i in NPC_LIGNE), f'{name} ligne : 9 PNJ aux places du plan', pres)
        bad = []
        for i in NPC_LIGNE:
            r = E(f"(()=>{{const g=window.__nml.game,r=g.talkTo('{i}');window.__nml.state.player.path.length=0;window.__nml.state.player.pending=null;return r}})()")
            if not r.get('ok'): bad.append((i, r))
        ok(not bad, f'{name} ligne : chaque PNJ est abordable depuis le quai', bad)
        ok(E("!window.__nml.world.NPCS.some(n=>/vibes|tron/i.test(n.id+n.name))"), f'{name} aucun PNJ Vibes ni Tron (écrans seulement)')
        # 4) modules d'Ocre posés (lots 1 et 2), rame avant / dos qui passe sans s'arrêter, tri du peintre, écrans dans leurs cadres
        LOTS = E("(()=>{const M=window.__nml.bman,dos=new Set(Object.values(M).map(v=>v.vue_dos).filter(Boolean));return Object.entries(M).filter(([k,v])=>/_v2_3q$/.test(k)&&v.footprint_m&&/^lot [12] /.test(v.lot||'')&&!dos.has(k)).map(([k])=>k)})()")
        B = E("window.__nml.world.LOCATIONS.steel_megaline.buildings.map(b=>b.sprite)"); manque = [k for k in LOTS if k not in B]
        ok(len(LOTS) >= 21 and not manque, f'{name} ligne : {len(LOTS)} modules des lots 1 et 2 posés', manque)
        ok(not E("window.__nml.world.LOCATIONS.steel_megaline.buildings.some(b=>b.attente||!window.__nml.bman[b.sprite])"), f'{name} ligne : plus aucun gabarit')
        R = [E(f"window.__nml.view.rameEtat({t})[0]") for t in range(0, 61)]
        av = [r for r in R if r['passe'] and r['sens'] > 0]; ds = [r for r in R if r['passe'] and r['sens'] < 0]
        ok(av and ds and all(r['cle'] == 'ml_rame_3v_v2_3q' for r in av) and all(r['cle'] == 'ml_rame_3v_dos_v2_3q' for r in ds), f'{name} rame : vue avant vers +x, vue dos vers −x', (av[:1], ds[:1]))
        mono = all(R[i + 1]['x'] != R[i]['x'] for i in range(60) if R[i]['passe'] and R[i + 1]['passe'] and R[i]['sens'] == R[i + 1]['sens'])
        ok(mono and min(r['x'] for r in av) < 8 and max(r['x'] for r in av) > 84, f'{name} rame : traverse tout le viaduc sans s arrêter', [r['x'] for r in av][:5])
        ok(E("!window.__nml.doors.some(d=>d.location==='steel_megaline'&&/rame/.test(d.id)&&d.id!=='ml_rame_quai')"), f'{name} rame : seule porte = portique')
        O = E("(()=>{const v=window.__nml.view;return Object.fromEntries(['ml_v_seg1','ml_rame','ml_v_av1','ml_quai','ml_ech_tran','ml_hc','ml_ecran_vibes','ml_esc_o','ml_v_pile2'].map(i=>[i,v.ordreBat(i)]))})()")
        ok(all(O.values()) and O['ml_v_pile2'] < O['ml_v_seg1'] < O['ml_rame'] < O['ml_v_av1'] and O['ml_ech_tran'] < O['ml_quai'] and O['ml_hc'] < O['ml_quai'] < O['ml_ecran_vibes'], f'{name} tri : piles < viaduc < rame < poutres _avant ; échoppes < tablier < écrans', O)
        D = E("window.__nml.view.dalles()")
        ev = [d for d in D if d['image'] == 'ml_ens_ecran_vibes']; et = [d for d in D if d['image'] == 'ml_ens_ecran_tron']
        ok(ev and et and ev[0]['x'] < 32 < et[0]['x'] and all(abs(d['w'] - 5.12) < 0.01 and abs(d['h'] - 2.88) < 0.01 and abs(d['quad'][0] - 5.12) < 0.08 and abs(d['quad'][1] - 2.88) < 0.08 and 11.5 < d['y'] < 12.4 for d in ev + et), f'{name} écrans : Vibes à l ouest, Tron à l est, 5,12 x 2,88 m dans le cadre (+10,5-13,4)', D)
        ok(any(d['image'] == 'ml_ens_human_corp' for d in D), f'{name} logo Human Corp dans son caisson', D)
        a = E("({...window.__nml.view.animStats})"); print(f'   {name} ligne {a}'); ok(a['on'] <= 5, f'{name} ligne : {a["on"]} animations (<= 5)', a)
        tp('steel_megaline', 20, 12.2); pret('steel_megaline', 10); time.sleep(1.2); pg.screenshot(path=OUT + f'{name}_ligne_sous_viaduc.png')
        tp('steel_megaline', 30, 23.6); time.sleep(1.4); pg.screenshot(path=OUT + f'{name}_ligne_echoppes.png')
        # 5) ligne -> terminus par la passerelle de service (bord nord)
        tp('steel_megaline', 46, 3); time.sleep(.5); E("window.__nml.game.useDoor('ml_passerelle')"); time.sleep(2.5); pret('steel_terminus')
        q = pos(); ok(loc() == 'steel_terminus' and q[1] > 25, f'{name} passerelle -> terminus (arrivée sud-ouest)', (loc(), q))
        time.sleep(1.5); pg.screenshot(path=OUT + f'{name}_terminus_arrivee.png')
        pres = E("window.__nml.world.NPCS.filter(n=>n.location==='steel_terminus').map(n=>n.id)")
        ok(all(i in pres for i in NPC_TERM), f'{name} terminus : Régie, Odile, Bruno présents', pres)
        bad = []
        for i in NPC_TERM:
            r = E(f"(()=>{{const g=window.__nml.game,r=g.talkTo('{i}');window.__nml.state.player.path.length=0;window.__nml.state.player.pending=null;return r}})()")
            if not r.get('ok'): bad.append((i, r))
        ok(not bad, f'{name} terminus : chaque PNJ est abordable', bad)
        # 6) portes du sas : aucune porte, aucun passage, clic = « ne s'ouvriront pas »
        D = E("window.__nml.doors.filter(d=>d.location==='steel_terminus').map(d=>({id:d.id,x:d.opening.x,z:d.opening.z,b:d.buildingId||null}))")
        ok(not any(d['z'] < 4 or d['b'] == 'ml_sas' for d in D), f'{name} sas : aucune porte vers le sas', D)
        rr, q, r = walk(20, 1.0, 30)
        ok(q[1] > 2.2, f'{name} sas : on ne passe jamais les portes (bloqué devant, z = {q[1]:.1f})', (q, r))
        rr, q, _ = walk(18.6, 8, 40); ok(rr and abs(hsol(W['tm']['niv'], *q) - 1.1) < 0.01, f'{name} terminus : quai à l est de la voie (+1,1 m)', q)
        time.sleep(1.2); pg.screenshot(path=OUT + f'{name}_terminus_sas.png')
        a = E("({...window.__nml.view.animStats})"); print(f'   {name} terminus {a}'); ok(a['on'] <= 3, f'{name} terminus : {a["on"]} animations (<= 3)', a)
        labs = E("[...document.querySelectorAll('#labels *')].map(e=>e.textContent).filter(t=>t.includes('Dernier arrêt'))"); ok(bool(labs), f'{name} panneau « Dernier arrêt avant No Man\u2019s Land » affiché par le code', labs)
        # 7) retours : terminus -> ligne -> Center-Town
        tp('steel_terminus', 10, 26.4); time.sleep(.5); E("window.__nml.game.useDoor('tm_sud')"); time.sleep(2.5); pret('steel_megaline')
        q = pos(); ok(loc() == 'steel_megaline' and abs(q[0] - 46) < 1.5 and q[1] < 3, f'{name} terminus -> ligne (débouché de la passerelle nord)', (loc(), q))
        tp('steel_megaline', 32, 38.4); time.sleep(.5); E("window.__nml.game.useDoor('ml_sud')"); time.sleep(2.5)
        ok(loc() == 'steel_center', f'{name} ligne -> Center-Town (ml_sud -> c_mega)', loc())
        # 8) sauvegardes : coordonnées de l'ancien plan (sans version) -> arrivée ; îlot fermé (bande) -> arrivée
        tp('steel_megaline', 13, 14, plans=False); time.sleep(.3); q = pos()
        ok(abs(q[0] - 32) < 0.1 and abs(q[1] - 38.2) < 0.1, f'{name} sauvegarde de l ancien plan (48 x 24) : reprise à l arrivée', q)
        tp('steel_megaline', 30, 16); time.sleep(.3); q = pos()
        ok(abs(q[0] - 32) < 0.1 and abs(q[1] - 38.2) < 0.1, f'{name} sauvegarde dans la bande fermée : reprise à l arrivée', q)
        tp('steel_megaline', 30, 20.5); time.sleep(.3); q = pos()
        ok(abs(q[0] - 30) < 0.6 and abs(q[1] - 20.5) < 0.6, f'{name} sauvegarde du plan v2 sur le quai : gardée telle quelle', q)
        ok(E("window.__nml.game.snapshot().plans.steel_megaline")==2, f'{name} instantané : version de plan enregistrée')
        tp('steel_terminus', 15, 19, plans=False); time.sleep(.3); q = pos()
        ok(abs(q[0] - 10) < 0.1 and abs(q[1] - 26.4) < 0.1, f'{name} terminus : sauvegarde de l ancien plan -> arrivée', q)
        ok(not errs, f'{name} aucune erreur console', errs[:3]); ctx.close()
    # cadrage de la maquette d'Ocre (lot2_maquette_ligne.png, 3850 x 2535 à 50 px/m) : vue entière à 25 px/m, mise côte à côte
    ctx = br.new_context(viewport={'width': 1925, 'height': 1268}); pg = ctx.new_page(); E = pg.evaluate
    pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=90000); time.sleep(1)
    E("localStorage.removeItem('nml_save_auto')"); passer_boot(E); E("document.getElementById('m-new').click()"); time.sleep(.5)
    E("document.querySelector('[data-race=\"humain\"]').click()"); time.sleep(.3); E("document.getElementById('cr-next').click()"); time.sleep(.3); E("document.getElementById('cr-enter').click()"); time.sleep(1.5)
    E("(()=>{const g=window.__nml.game,s=g.snapshot();s.location='steel_megaline';s.player.x=32;s.player.z=38.2;g.restore(s,true)})()")
    t0 = time.time()
    while time.time() - t0 < 60 and not E("window.__nml.lieuPret('steel_megaline')"): time.sleep(.3)
    CX, CZ = float(os.environ.get('ISO_X', '30.5')), float(os.environ.get('ISO_Z', '17'))
    E(f"window.__nml.view.setCamera({{x:{CX},z:{CZ},ppm:25}})"); E("for(const id of ['hud','locbox','obj','keys','zoom','act','mini','labels']){const e=document.getElementById(id);if(e)e.style.visibility='hidden'}")
    t0 = time.time()
    while time.time() - t0 < 32 and not (E("window.__nml.view.rameEtat()[0]||{}").get('passe') and 30 < E("window.__nml.view.rameEtat()[0].x") < 60): time.sleep(.4)
    time.sleep(.3); pg.screenshot(path=OUT + 'iso_cadrage_maquette.png'); ctx.close()
    try:
        from PIL import Image
        a = Image.open(OUT + 'iso_cadrage_maquette.png').convert('RGB'); m = Image.open('/workspace/nml-shots/megaline_sprites/lot2_maquette_ligne.png').convert('RGB').resize(a.size, Image.LANCZOS)
        c = Image.new('RGB', (a.width * 2 + 20, a.height), '#000'); c.paste(m, (0, 0)); c.paste(a, (a.width + 20, 0)); c.save(OUT + 'livraison/comparaison_maquette_jeu.jpg', quality=85)
    except Exception as e: print('comparaison :', e)
    # sélection 1x (jpg) pour la livraison
    try:
        from PIL import Image
        for f in ['desktop_ligne_arrivee', 'desktop_ligne_quai', 'desktop_ligne_sous_viaduc', 'desktop_ligne_echoppes', 'mobile_ligne_arrivee', 'mobile_ligne_quai', 'mobile_ligne_sous_viaduc', 'mobile_ligne_echoppes', 'desktop_terminus_arrivee', 'iso_cadrage_maquette']:
            if os.path.exists(OUT + f + '.png'): Image.open(OUT + f + '.png').convert('RGB').save(OUT + 'livraison/' + f + '.jpg', quality=88)
    except Exception as e: print('livraison jpg :', e)
    print(f'{n}/{n + len(fails)} OK'); print('ECHECS', len(fails)); sys.exit(1 if fails else 0)
