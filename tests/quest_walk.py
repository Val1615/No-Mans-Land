# v9 : quête test « La porte d'acier » de bout en bout, par GESTES RÉELS depuis le début de partie (aucune téléportation, aucun choix par commande).
# Deux branches : A = honnête (Ezequiel ment, payer Anselme 15 $, payer Teo 5 $) ; B = connaître le secret d'Ezequiel, mentir à Anselme, vendre le secret à Teo.
# Bureau 1280x800 (clics) et mobile 390x844 (taps). Contrôles au pixel : dialogue rendu, scène et blockhaus visibles, journal rendu.
import sys, os, time, io, base64, json
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8765/'); OUT = os.environ.get('OUT', '/workspace/nml/docs/captures/quete-v9/'); os.makedirs(OUT, exist_ok=True)
R = []
def check(n, ok, d=''): R.append({'test': n, 'ok': bool(ok), 'detail': str(d)[:300]}); print(('OK    ' if ok else 'ECHEC ') + n, str(d)[:300], flush=True)
def png(url): return np.asarray(Image.open(io.BytesIO(base64.b64decode(url.split(',')[1]))).convert('RGB')).astype(int)
def vis(full, iso, ui):
    m = (np.abs(iso - [255, 0, 255]).sum(2) > 90) & ~ui
    return (round(((np.abs(full - iso).sum(2) < 60) & m).sum() / m.sum(), 2) if m.sum() else 0), int(m.sum())
JUN = {('dusk_q1', 'dusk_q2'): 'j_q1_est', ('dusk_q2', 'dusk_q1'): 'j_q2_ouest', ('dusk_q1', 'dusk_q3'): 'j_q1_nord', ('dusk_q3', 'dusk_q1'): 'j_q3_sud',
       ('dusk_q1', 'dusk_q4'): 'j_q1_sud', ('dusk_q4', 'dusk_q1'): 'j_q4_nord'}
HOME = {'teo': ('dusk_q2', 't_guet_door'), 'ezequiel': ('dusk_q3', 's_atelier_door'), 'anselme': ('dusk_q1', 'grocery_door')}
BR = os.environ.get('BRANCHES', 'A,B').split(',')
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=user-gesture-required'])
    for prof in os.environ.get('PROFILES', 'desktop,mobile').split(','):
      for branch in BR:
        T = f'{prof}/{branch}'
        dpr = 1 if prof == 'desktop' else 2
        ctx = br.new_context(viewport={'width': 1280, 'height': 800}) if prof == 'desktop' else br.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.goto(URL); pg.wait_for_function('window.__nml', timeout=60000); [(pg.locator(_s).tap if pg.evaluate('navigator.maxTouchPoints>0') else pg.locator(_s).click)() for _s in ('#m-new', '#cr-next', '#cr-enter')]; pg.wait_for_function('!document.body.classList.contains("menu-open")'); time.sleep(2.5)
        pg.evaluate("import('./src/core/path.js').then(m => window.__findPath = m.findPath)"); time.sleep(0.5)
        VW, VH = (1280, 800) if prof == 'desktop' else (390, 844)
        gesture = pg.touchscreen.tap if prof == 'mobile' else pg.mouse.click
        E = pg.evaluate; st = lambda: E('JSON.parse(JSON.stringify(window.__nml.state))')
        P = lambda x, y, z: E(f'window.__nml.project({x},{y},{z})')
        onscreen = lambda pt: 20 < pt['x'] < VW - 20 and 130 < pt['y'] < VH - 110
        def shot(): return np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert('RGB')).astype(int)
        def ui_mask():
            m = np.zeros((VH * dpr, VW * dpr), bool)
            for r in E('[...document.querySelectorAll(".wlabel:not([hidden]),#hud,#locbox,#obj:not([hidden]),#keys button,#msg,#act:not([hidden]),#dialogue:not([hidden]),#panel:not([hidden])")].map(e=>e.getBoundingClientRect()).filter(r=>r.width>0).map(r=>[r.left,r.top,r.right,r.bottom])'):
                m[max(0, int(r[1]*dpr)):max(0, int(r[3]*dpr)+1), max(0, int(r[0]*dpr)):max(0, int(r[2]*dpr)+1)] = True
            return m
        def waitjs(js, t=25):
            t0 = time.time()
            while time.time() - t0 < t:
                if E(js): return True
                time.sleep(0.1)
            return False
        def idle(): waitjs('(()=>{const s=window.__nml.state;return !s.player.path.length && !s.player.pending})()', 30); time.sleep(0.3)
        def tapel(sel):
            b = pg.locator(sel).first.bounding_box(); gesture(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2); time.sleep(0.35)
        def walk(x, z, tol=0.7):
            loc0 = st()['location']
            for _ in range(20):
                s = st()
                if s['location'] != loc0: return True
                pl = s['player']
                if ((x - pl['x'])**2 + (z - pl['z'])**2) ** 0.5 < tol: return True
                path = E(f"(()=>{{const g=window.__nml.game; return window.__findPath(g.grids[g.state.location], g.state.player, {{x:{x},z:{z}}})}})()")
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
        def walk_away():
            s = st()['player']; walk(s['x'] + (2 if s['x'] < 24 else -2), s['z'] + (2 if s['z'] < 18 else -2), tol=1.2)
        def cross(dest):
            j = E(f"window.__nml.game.doorById('{JUN[(st()['location'], dest)]}').threshold")
            walk(j['x'], j['z']); ok = waitjs(f'window.__nml.state.location==="{dest}"', 6); time.sleep(0.8); walk_away(); return ok
        def goto_loc(loc):
            if E('window.__nml.game.location.kind') == 'interior':  # sortir par geste sur la porte intérieure
                o = E("window.__nml.doors.find(d=>d.location===window.__nml.state.location)"); pt = P(o['opening']['x'], 1.0, o['opening']['z']); gesture(pt['x'], pt['y'])
                waitjs('window.__nml.game.location.kind!=="interior"'); time.sleep(0.5); walk_away()
            if st()['location'] == loc: return True
            if st()['location'] != 'dusk_q1' and not cross('dusk_q1'): return False
            return loc == 'dusk_q1' or cross(loc)
        def visit(npc):
            loc, door = HOME[npc]; goto_loc(loc)
            d = E(f"window.__nml.game.doorById('{door}')"); t = d['threshold']
            walk(t['x'] + (3 if d['opening']['side'] == 'east' else 0), t['z'] + (0 if d['opening']['side'] == 'east' else 3), tol=1.5)
            pt = P(d['opening']['x'], 1.0, d['opening']['z']); gesture(pt['x'], pt['y'])
            inside = E(f"window.__nml.game.doorById(window.__nml.game.doorById('{door}').target.doorId).location")
            if not waitjs(f'window.__nml.state.location==="{inside}"'): return False
            time.sleep(0.6); n = E(f"window.__nml.npcs.find(n=>n.id==='{npc}')"); pt = P(n['x'], 1.0, n['z']); gesture(pt['x'], pt['y'])
            return waitjs(f'window.__nml.state.dialogue && window.__nml.state.dialogue.npc==="{npc}" && !document.getElementById("dialogue").hidden', 20)
        def say_(label):  # choisir une option par geste sur le bouton
            loc = pg.locator('#dlg-options button', has_text=label)
            if not loc.count(): return False
            tapel(f'#dlg-options button:has-text("{label}")'); return True
        def text(): return E("document.getElementById('dlg-text').textContent")
        def talk(npc, labels, tag):
            ok = visit(npc); check(f'{T}: rejoint {npc} par la marche et lui parle par geste', ok, st()['location'])
            got = []
            for l in labels:
                if not say_(l): check(f'{T}: option « {l} » présente chez {npc}', False, E("[...document.querySelectorAll('#dlg-options button')].map(b=>b.textContent)")); return got
                got.append(text() if st()['dialogue'] else '')
            if tag: pg.screenshot(path=OUT + f'{prof}-{branch}-{tag}.png')
            while st()['dialogue']: tapel('#dlg-close')
            return got
        def journal(tag):
            tapel('#k-journal'); time.sleep(0.4); h = E("document.getElementById('panel-body').innerText"); pg.screenshot(path=OUT + f'{prof}-{branch}-journal-{tag}.png'); tapel('#panel-close'); return h
        flags = lambda: st()['flags']
        def find_lab():
            for dy in (1.5, 2.5, 1.0, 3.0):
                for dx in (0, -1.5, 1.5):
                    q = P(28 + dx, dy, 3.5); k = E(f'window.__nml.pick({q["x"]},{q["y"]})')
                    if k and k.get('kind') == 'closed' and k.get('buildingId') == 's_lab': return q
            return None
        # --- Prérequis v7 : Teo vend le chemin de l'atelier
        talk('teo', ['Tu vends des nouvelles', 'Marché conclu', 'Noté.'], None)
        if branch == 'B':  # apprendre le secret de la jambe d'Ezequiel
            talk('ezequiel', ['Ta jambe', 'Six ? Vraiment', 'Ton secret est gardé', 'Merci quand même'], None)
        j0 = journal('0-depart'); check(f'{T}: journal : quête visible, objectif 1 courant', 'la porte d' in j0.lower() and '> Demander à Ezequiel' in j0, j0[:160])
        check(f'{T}: objectif suivi affiché dans le HUD', 'Ezequiel' in E("document.getElementById('obj').innerText") and pg.locator('#obj').is_visible())
        # --- Étape 1 : Ezequiel
        lbl = 'Ceux qui ont tenté la porte'; nxt = 'Et toi, tu as essayé' if branch == 'A' else 'Le toit, je sais déjà'
        got = talk('ezequiel', [lbl, nxt, 'Et pour ne pas finir', ], 'e1-ezequiel')
        check(f'{T}: étape 1 : Ezequiel {"ment (bande de sept)" if branch == "A" else "dit la vérité (battant gauche)"}', got and (('sept' in got[1]) if branch == 'A' else ('battant gauche' in got[1])), got[1:2])
        check(f'{T}: drapeaux étape 1', flags().get('q_start') and bool(flags().get('q_battant')) == (branch == 'B'), flags())
        # porte du labo avant d'être prêt : refus explicite, aucune scène
        goto_loc('dusk_q3'); walk(28, 9, tol=1.2)
        lab = None
        for dy in (1.5, 2.5, 1.0, 3.0):
            for dx in (0, -1.5, 1.5):
                pt = P(28 + dx, dy, 3.5); k = E(f'window.__nml.pick({pt["x"]},{pt["y"]})')
                if k and k.get('kind') == 'closed' and k.get('buildingId') == 's_lab': lab = pt; break
            if lab: break
        check(f'{T}: blockhaus HC cliquable à l\'écran', lab, lab)
        gesture(lab['x'], lab['y']); time.sleep(0.4)
        check(f'{T}: porte avant d\'être prêt : message, pas de scène', 'mains nues' in E("document.getElementById('msg').textContent") and not st()['dialogue'], E("document.getElementById('msg').textContent"))
        # --- Étape 2 : Anselme (choix)
        m0 = st()['player']['money']
        lab2 = 'Payer (15 $)' if branch == 'A' else 'pour la pompe de Mara'
        talk('anselme', ['Le cric sous ton comptoir', lab2], 'e2-anselme')
        m1 = st()['player']['money']; inv = st()['player']['inv']
        check(f'{T}: étape 2 : cric obtenu, coût {"15" if branch == "A" else "5"} $', inv.get('cric') == 1 and m0 - m1 == (15 if branch == 'A' else 5), (m0, m1, inv))
        check(f'{T}: HUD $ à jour', E("document.getElementById('money').textContent") == f'{m1} $')
        # --- Étape 3 : Teo (choix)
        lab3 = 'Cinq dollars, comme' if branch == 'A' else 'Pas d\'argent'
        got = talk('teo', ['Quand passent les camions', lab3], 'e3-teo')
        m2 = st()['player']['money']
        check(f'{T}: étape 3 : signal obtenu, coût {"5" if branch == "A" else "0 (secret vendu)"} $', flags().get('q_signal') and m1 - m2 == (5 if branch == 'A' else 0) and bool(flags().get('q_trahi')) == (branch == 'B'), (m1, m2, got))
        # --- Conséquences visibles (branche B) : accueils changés
        if branch == 'B':
            visit('anselme'); t = text(); check(f'{T}: conséquence : Anselme sait que le cric n\'était pas pour Mara', 'jamais entendu parler de mon cric' in t, t[:90]); pg.screenshot(path=OUT + f'{prof}-B-consequence-anselme.png'); tapel('#dlg-close')
            visit('ezequiel'); t = text(); check(f'{T}: conséquence : Ezequiel, Teo miaule quand il passe', 'miaule' in t, t[:90]); pg.screenshot(path=OUT + f'{prof}-B-consequence-ezequiel.png'); tapel('#dlg-close')
        else:
            visit('anselme'); t = text(); check(f'{T}: pas de conséquence de mensonge chez Anselme', 'jamais entendu' not in t, t[:60]); tapel('#dlg-close')
        jn = journal('1-avant-porte'); check(f'{T}: journal : 3 étapes cochées, objectif courant = forcer la porte', jn.count('[x]') == 3 and '> Forcer la porte' in jn, jn[:300])
        # --- Étape 4 : la porte d'acier
        goto_loc('dusk_q3'); walk(28, 9, tol=1.2)
        pt = None
        for dy in (1.5, 2.5, 1.0, 3.0):
            for dx in (0, -1.5, 1.5):
                q = P(28 + dx, dy, 3.5); k = E(f'window.__nml.pick({q["x"]},{q["y"]})')
                if k and k.get('kind') == 'closed' and k.get('buildingId') == 's_lab': pt = q; break
            if pt: break
        time.sleep(0.5); pt = find_lab(); gesture(pt['x'], pt['y'])
        ok = waitjs('window.__nml.state.dialogue && window.__nml.state.dialogue.npc==="porte" && !document.getElementById("dialogue").hidden', 25)
        pl = st()['player']; check(f'{T}: étape 4 : marche au pied de la porte et scène ouverte', ok and abs(pl['x'] - 28) < 1.2 and pl['z'] < 7.5, (round(pl['x'], 1), round(pl['z'], 1)))
        t0 = text(); check(f'{T}: scène : le signal du miroir{" et le battant gauche (Ezequiel)" if branch == "B" else ""}', 'miroir' in t0 and (('battant gauche' in t0) == (branch == 'B')), t0[:120])
        check(f'{T}: scène : pas de portrait affiché (personne de visible)', not pg.locator('#dlg-portrait').is_visible())
        pg.screenshot(path=OUT + f'{prof}-{branch}-e4-porte.png')
        seq = ['Pomper.', 'Pomper encore.'] + (['Il y a quelqu', 'Oui. Qui', 'Vous êtes combien', 'Je vais vous sortir', 'J\'irai.'] if branch == 'A'
              else ['Frapper sur la porte', 'Il y a quelqu', 'Ça dépend des jours', 'Qui êtes-vous', 'Vous êtes combien', 'Comment vous tenez', 'Je vais vous sortir', 'Et si personne', 'J\'irai.'])
        texts = []
        for l in seq:
            if not say_(l): check(f'{T}: scène : option « {l} »', False, E("[...document.querySelectorAll('#dlg-options button')].map(b=>b.textContent)")); break
            texts.append(text())
            if 'confinement' in texts[-1] and len(texts) == 2: pg.screenshot(path=OUT + f'{prof}-{branch}-e5-message.png')
            if 'Steel-Megalopolis' in texts[-1]:
                pg.screenshot(path=OUT + f'{prof}-{branch}-e6-voix-steel.png'); full = shot(); um = ui_mask()
                u = E("window.__nml.view.isolateBuilding('s_lab')"); bv = vis(full, png(u), um) if u else (0, 0)
                d = pg.locator('#dialogue').bounding_box()
                check(f'{T}: scène finale au pixel : blockhaus visible hors UI, dialogue en bas{" à gauche" if prof == "desktop" else ""}', bv[0] >= 0.6 and d['y'] + d['height'] > VH * 0.75 and (prof != 'desktop' or d['x'] + d['width'] / 2 < VW * 0.42), (bv, d))
                fh = full[int(d['y'] * dpr):int((d['y'] + d['height']) * dpr), int(d['x'] * dpr):int((d['x'] + d['width']) * dpr)]
                check(f'{T}: scène finale au pixel : le dialogue est rendu (texte clair sur voile)', (fh.mean(2) > 200).mean() > 0.01 and np.median(fh.mean(2)) < 90, ((fh.mean(2) > 200).mean(), np.median(fh.mean(2))))
        allt = ' '.join(texts)
        for key in ('confinement', 'mal tourné', 'les autres sont là', 'Steel-Megalopolis', 'La porte reste fermée'):
            check(f'{T}: scène : « {key} »', key.lower() in allt.lower())
        if branch == 'B': check(f'{T}: scène : branche coups / humour', 'Trois coups répondent' in allt and 'rations' in allt)
        check(f'{T}: fin : q_fin, la porte ne s\'ouvre pas', flags().get('q_fin') and st()['location'] == 'dusk_q3', flags())
        while st()['dialogue']: tapel('#dlg-close')
        check(f'{T}: aucune porte vers un intérieur du labo', not E("window.__nml.doors.some(d=>d.buildingId==='s_lab')"))
        jf = journal('2-fin'); check(f'{T}: journal final : 4 étapes cochées, Steel-Megalopolis courant et hors de portée', jf.count('[x]') == 4 and '> Aller à Steel-Megalopolis' in jf and 'Hors de portée' in jf, jf[:400])
        check(f'{T}: HUD : objectif Steel-Megalopolis (hors de portée)', 'Steel-Megalopolis' in E("document.getElementById('obj').innerText"))
        if branch == 'B': check(f'{T}: journal : notes des choix (mensonge, trahison)', 'pour Mara' in jf and 'secret d' in jf)
        # rejouer la porte : elle ne s'ouvre toujours pas
        walk(28, 9, tol=1.2); time.sleep(0.5); pt = find_lab(); gesture(pt['x'], pt['y']); o = waitjs('window.__nml.state.dialogue', 20); t = text()
        check(f'{T}: porte retentée : plus de voix, toujours fermée', o and 'ne grésille plus' in t, t[:80])
        while st()['dialogue']: tapel('#dlg-close')
        check(f'{T}: aucune erreur console', not errs, errs[:2])
        ctx.close()
    br.close()
ok = sum(r['ok'] for r in R); print(f'{ok}/{len(R)}'); json.dump(R, open(OUT + 'quest_walk.json', 'w'), indent=1, ensure_ascii=False)
sys.exit(0 if ok == len(R) else 1)
