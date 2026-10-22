# v11 lot 2 : création de personnage. Gestes réels (clic 1280x800, tap 390x844 dpr2), clavier pour le nom, vérifs sur pixels rendus.
# Bureau : cyborg ; mobile : mutant. Puis : jeu lancé, état dérivé, fiche, sauvegarde v2 + rechargement, migration v1.
import sys, os, time, io, json, re
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8765/'); OUT = os.environ.get('OUT', '/tmp/nml-test-out/lot2_creation/'); os.makedirs(OUT, exist_ok=True)
R = []
def check(n, ok, d=''): R.append({'test': n, 'ok': bool(ok), 'detail': str(d)}); print(('OK    ' if ok else 'ECHEC ') + n, d, flush=True)
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for prof in os.environ.get('PROFILES', 'desktop,mobile').split(','):
        mob = prof == 'mobile'; dpr = 2 if mob else 1; VW, VH = (390, 844) if mob else (1280, 800)
        RACE, ORI, NAME = ('mutant', 'rafle', 'Ysa Corvo') if mob else ('cyborg', 'reconstruit', 'Joaquim Ferro')
        ctx = br.new_context(viewport={'width': VW, 'height': VH}, has_touch=True, is_mobile=True, device_scale_factor=2) if mob else br.new_context(viewport={'width': VW, 'height': VH})
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('response', lambda r: r.status >= 400 and errs.append(f'{r.status} {r.url}'))
        gesture = pg.touchscreen.tap if mob else pg.mouse.click
        E = pg.evaluate; st = lambda: E('JSON.parse(JSON.stringify(window.__nml.state))')
        shot = lambda: np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert('RGB')).astype(int)
        def press(sel, wait=0.35):
            E(f'(()=>{{const e=document.querySelector({json.dumps(sel)}); if(e&&!e.closest(".cr-foot")) e.scrollIntoView({{block:"center"}})}})()'); time.sleep(0.15); loc = pg.locator(sel).first; bb = loc.bounding_box(); assert bb, sel
            gesture(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2); time.sleep(wait)
        def crop(sel):
            r = E(f'(()=>{{const e=document.querySelector({json.dumps(sel)});e.scrollIntoView({{block:"center"}});const r=e.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]}})()'); a = shot()
            return a[max(0, int(r[1]*dpr)):int(r[3]*dpr), max(0, int(r[0]*dpr)):int(r[2]*dpr)]
        def topel(sel):
            return E(f'(()=>{{const e=document.querySelector({json.dumps(sel)});e.scrollIntoView({{block:"center"}});const r=e.getBoundingClientRect(),t=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return !!t&&(t===e||e.contains(t))}})()')
        txt = lambda sel: E(f'document.querySelector({json.dumps(sel)}).textContent')
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=60000); time.sleep(2)
        # 1. Nouveau jeu -> écran 1
        press('#m-new', 0.6)
        check(f'{prof}: Nouveau jeu ouvre la création (écran 1)', E('!document.getElementById("creation").hidden && document.getElementById("creation").dataset.screen==="1"'))
        S = shot(); amber = ((S[..., 0] > 200) & (S[..., 1] > 140) & (S[..., 1] < 200) & (S[..., 2] < 110)).sum()
        check(f'{prof}: titre et cadres ambre rendus (pixels)', amber > 300 * dpr * dpr, amber)
        P0 = crop('#cr-portrait'); check(f'{prof}: portrait rendu (pixels variés)', P0.size > 0 and P0.std() > 25, round(P0.std(), 1))
        for k in ['humain', 'mutant', 'augmente', 'cyborg']: check(f'{prof}: race {k} accessible au geste', topel(f'[data-race="{k}"]'))
        # visages : humain, 4 visages, l'image change
        press('#cr-next-face'); P1 = crop('#cr-portrait')
        check(f'{prof}: visage suivant : image différente (pixels)', P1.shape == P0.shape and np.abs(P1 - P0).mean() > 10 and 'Visage 2/4' in txt('.cr-face'), txt('.cr-face'))
        # nom au clavier
        press('#cr-name'); pg.keyboard.press('Control+A'); pg.keyboard.press('Backspace'); pg.keyboard.type(NAME); time.sleep(0.2)
        check(f'{prof}: nom saisi au clavier', E('document.getElementById("cr-name").value') == NAME)
        # race + origine
        press(f'[data-race="{RACE}"]'); P2 = crop('#cr-portrait')
        check(f'{prof}: race {RACE} : portrait de la race (pixels)', np.abs(P2[:min(len(P2), len(P1)), :min(P2.shape[1], P1.shape[1])] - P1[:min(len(P2), len(P1)), :min(P2.shape[1], P1.shape[1])]).mean() > 10)
        ors = E('[...document.querySelectorAll("[data-origin]")].map(b=>b.dataset.origin)'); check(f'{prof}: 3 origines pour {RACE}', len(ors) == 3, ors)
        eff = txt('.cr-list'); check(f'{prof}: effets de race affichés', ('Implant' in eff) == (RACE == 'cyborg') and ('Service Militarisé' in eff) == (RACE == 'mutant'), eff)
        press(f'[data-origin="{ORI}"]'); check(f'{prof}: origine choisie', E(f'document.querySelector("[data-origin={ORI}]").classList.contains("sel")'))
        check(f'{prof}: nom conservé après choix', E('document.getElementById("cr-name").value') == NAME)
        pg.screenshot(path=OUT + f'{prof}-01-identite.png')
        allt = E('document.getElementById("creation").textContent')
        # 2. écran 2
        press('#cr-next', 0.5); check(f'{prof}: écran 2', E('document.getElementById("creation").dataset.screen') == '2')
        names = E('[...document.querySelectorAll(".cr-attr .n")].map(e=>e.textContent)')
        check(f'{prof}: les 7 attributs exacts de la maquette v0.13', names == ['Force', 'Perception', 'Endurance', 'Charisme', 'Intelligence', 'Agilité', 'Volonté'], names)
        allt += E('document.getElementById("creation").textContent')
        check(f'{prof}: pas d\'Aura dans la création', 'Aura' not in allt and 'aura' not in allt.lower().replace('aurai', ''))
        check(f'{prof}: Volonté = peur, douleur, intimidation', 'peur, douleur, intimidation' in txt('[data-attr-row="volonte"]'))
        check(f'{prof}: 11 compétences', E('document.querySelectorAll("[data-skill]").length') == 11)
        check(f'{prof}: textes sans tiret cadratin ni « ce n\'est pas »', '\u2014' not in allt and not re.search(r"ce n.est pas", allt, re.I))
        left = lambda: int(txt('#cr-left'))
        check(f'{prof}: 40 points, 0 restant au départ', left() == 0)
        press('[data-attr="force"][data-d="-1"]'); check(f'{prof}: − Force : 1 point à répartir, entrée bloquée', left() == 1 and E('document.getElementById("cr-enter").disabled'), txt('#cr-hint'))
        check(f'{prof}: + désactivé seulement quand plus de points', not E('document.querySelector("[data-attr=volonte][data-d=\'1\']").disabled'))
        hp0 = txt('#cr-hp'); press('[data-attr="endurance"][data-d="1"]'); hp1 = txt('#cr-hp')
        check(f'{prof}: + Endurance : PV dérivés +3', int(hp1.split('/')[1]) - int(hp0.split('/')[1]) == 3 and left() == 0, (hp0, hp1))
        check(f'{prof}: + bloqués à 0 point', E('[...document.querySelectorAll("[data-d=\'1\']")].every(b=>b.disabled)'))
        press('[data-profile="technicien"]'); st2 = E('window.__nml.shell.creationDraft.stats')
        check(f'{prof}: profil prêt (Le Technicien) : attributs de la maquette', list(st2.values()) == [4, 7, 5, 4, 9, 6, 5] and left() == 0, st2)
        for t in ['nerfs', 'insomniaque', 'sable']: press(f'[data-trait="{t}"]')
        tr = E('window.__nml.shell.creationDraft.traits'); check(f'{prof}: traits : 2 au maximum', tr == ['nerfs', 'insomniaque'], tr)
        fav0 = E('window.__nml.shell.creationDraft.favs'); lock = E('document.querySelector(".cr-skill.lock").dataset.skill')
        press(f'[data-skill="{lock}"]'); check(f'{prof}: favorite imposée par l\'origine verrouillée', E('window.__nml.shell.creationDraft.favs') == fav0, lock)
        other = [f for f in fav0 if f != lock][0]; press(f'[data-skill="{other}"]')
        check(f'{prof}: 2/3 favorites : entrée bloquée', len(E('window.__nml.shell.creationDraft.favs')) == 2 and E('document.getElementById("cr-enter").disabled'))
        press('[data-skill="crochetage"]'); fv = E('window.__nml.shell.creationDraft.favs')
        check(f'{prof}: 3/3 favorites, entrée possible', len(fv) == 3 and 'crochetage' in fv and not E('document.getElementById("cr-enter").disabled'), fv)
        sk = E('[...document.querySelectorAll("[data-skill=crochetage] b")].map(e=>+e.textContent)[0]')
        hpS, monS = txt('#cr-hp'), txt('#cr-money')
        pg.screenshot(path=OUT + f'{prof}-02-attributs.png')
        # retour et aller : le brouillon est conservé
        press('#cr-back'); press('#cr-next'); check(f'{prof}: retour à l\'identité puis suite : choix conservés', E('window.__nml.shell.creationDraft.traits') == ['nerfs', 'insomniaque'] and E('window.__nml.shell.creationDraft.race') == RACE)
        # 3. entrer dans Dusk-Town
        press('#cr-enter', 1.5); s = st(); c = s['character']
        check(f'{prof}: jeu lancé dans Dusk-Town', E('!document.body.classList.contains("menu-open")') and s['location'] == 'dusk_q1' and E('document.getElementById("creation").hidden'))
        check(f'{prof}: personnage dans l\'état (nom, race, origine)', c and c['name'] == NAME and c['race'] == RACE and c['origin'] == ORI, c and (c['name'], c['race'], c['origin']))
        check(f'{prof}: PV et dollars dérivés = fiche', f"{s['player']['hp']}/{s['player']['maxHp']}" == hpS and f"{s['player']['money']} $" == monS, (hpS, monS, s['player']['hp'], s['player']['money']))
        exp_hp = 25 + 3 * c['attrs']['endurance'] + (5 if RACE == 'cyborg' else 0) - 3
        check(f'{prof}: PV max = 25 + 3 x Endurance (+ race, − Insomniaque)', s['player']['maxHp'] == exp_hp, (s['player']['maxHp'], exp_hp))
        check(f'{prof}: PA = 5 + Agilité/2 + 1 (Pas de nerfs)', c['ap'] == 5 + c['attrs']['agilite'] // 2 + 1, c['ap'])
        check(f'{prof}: Volonté −2 (Pas de nerfs) appliquée', c['attrs']['volonte'] == c['base']['volonte'] - 2 + (1 if ORI == 'reconstruit' else 0), (c['base']['volonte'], c['attrs']['volonte']))
        check(f'{prof}: compétence favorite au bon score', c['skills']['crochetage'] == sk, (c['skills']['crochetage'], sk))
        imp = RACE in ('cyborg', 'augmente')
        check(f'{prof}: implant stocké ({imp})', c['implant'] == imp and bool(s['flags'].get('implant')) == imp)
        check(f'{prof}: drapeaux race/origine pour PNJ et douane', s['flags'].get('race_' + RACE) and s['flags'].get('origine_' + ORI) and c['effects']['steelCustoms'] == ('attaque' if RACE == 'mutant' else 'passe'), c['effects'])
        if RACE == 'cyborg': check(f'{prof}: cyborg : soins réduits stockés', c['effects']['healFactor'] == 0.5)
        if RACE == 'mutant': check(f'{prof}: mutant : résistance aux radiations stockée', c['effects']['radResist'])
        check(f'{prof}: objet d\'origine dans le sac', len(s['player']['inv']) == 1, s['player']['inv'])
        hud = E('[document.getElementById("hp").textContent, document.getElementById("money").textContent, document.getElementById("inv").textContent]')
        check(f'{prof}: HUD dérivé (PV, $, objet)', hud[0] == hpS and hud[1] == monS and hud[2], hud)
        check(f'{prof}: Nilo toujours absent', s['companion']['mode'] == 'absent')
        pg.screenshot(path=OUT + f'{prof}-03-en-jeu.png')
        press('#k-sac', 0.6); F = crop('#panel .fiche img')
        check(f'{prof}: fiche du perso dans le Sac (nom + portrait rendu)', NAME.upper() in txt('#panel .fiche') and F.size > 0 and F.std() > 20, round(F.std(), 1))
        pg.screenshot(path=OUT + f'{prof}-04-fiche-sac.png'); press('#panel-close')
        # 4. sauvegarde v2 + rechargement + Continuer
        if mob: press('#k-menu')
        else: pg.keyboard.press('Escape'); time.sleep(0.4)
        press('#m-load'); press('#menu-sub [data-act="save"][data-slot="1"]')
        sv = E('JSON.parse(localStorage.getItem("nml_save_1"))')
        check(f'{prof}: sauvegarde v2 avec le personnage', sv and sv['v'] == 2 and sv['state']['character']['name'] == NAME and NAME in sv['label'], sv and sv['label'])
        pg.reload(); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=60000); time.sleep(1.5)
        press('#m-continue', 1.2); s2 = st()
        check(f'{prof}: Continuer restaure le personnage', s2['character'] == c and s2['player']['maxHp'] == s['player']['maxHp'] and s2['player']['inv'] == s['player']['inv'])
        # 5. migration v1 -> v2 : sauvegarde du lot 1 sans personnage
        v1 = {'v': 1, 't': 1, 'label': 'La Pompe', 'state': {'location': 'dusk_q1', 'player': {'x': s['player']['x'], 'z': s['player']['z'], 'hp': 20, 'maxHp': 40, 'money': 61, 'inv': {'cric': 1}}, 'companion': {'mode': 'absent', 'location': '_none', 'x': -99, 'z': -99}, 'flags': {'q_start': True}, 'discovered': {}, 'seen': {'dusk_q1': True}, 'transitions': 3}}
        E(f'localStorage.setItem("nml_save_2", {json.dumps(json.dumps(v1))})')
        if mob: press('#k-menu')
        else: pg.keyboard.press('Escape'); time.sleep(0.4)
        press('#m-load'); press('#menu-sub [data-act="load"][data-slot="2"]', 1.0); s3 = st()
        check(f'{prof}: migration v1 -> v2 : perso par défaut, $ / PV / drapeaux gardés', s3['character'] and s3['character']['race'] == 'humain' and s3['player']['money'] == 61 and s3['player']['hp'] == 20 and s3['flags'].get('q_start') and s3['flags'].get('race_humain'), s3['character'] and s3['character']['name'])
        # 6. Échap / bouton Menu depuis la création : retour au menu sans lancer de partie
        if mob: press('#k-menu')
        else: pg.keyboard.press('Escape'); time.sleep(0.4)
        press('#m-new', 0.5); press('#cr-next'); 
        if mob: press('#cr-menu'); press('#m-resume', 0.6)
        else:
            pg.keyboard.press('Escape'); time.sleep(0.3); check(f'{prof}: Échap sur l\'écran 2 : retour à l\'écran 1', E('document.getElementById("creation").dataset.screen') == '1')
            pg.keyboard.press('Escape'); time.sleep(0.3); press('#m-resume', 0.6)
        check(f'{prof}: création abandonnée : partie en cours intacte', st()['player']['money'] == 61 and st()['character']['race'] == 'humain' and E('!document.body.classList.contains("menu-open")'))
        check(f'{prof}: aucune erreur console / réseau', not errs, errs[:3])
        ctx.close()
    br.close()
ok = sum(r['ok'] for r in R); print(f'{ok}/{len(R)}'); json.dump(R, open(OUT + 'resultats.json', 'w'), ensure_ascii=False, indent=1); sys.exit(0 if ok == len(R) else 1)
