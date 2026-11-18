# Test rapide des rencontres de route, jalon 1 (docs/rencontres/ARCHI.md, PILOTE.md) : pilote « L'appât de la piste ».
# Vérifie, en 1280 x 800 puis 390 x 844 : déclenchement forcé depuis la carte des No Man's Land (sortie de Dusk-Town, un pas de trajet),
# entrée dans la scène (lieu à chaud, statut 'rencontre', carte fermée), sprites d'Ocre câblés (aucun gabarit), déplacement, fouille,
# dialogue (déclencheur T1, péage), combat (zone fixe, unités, PNJ cachés), fuite -> carte en halte, journal de la case (butin gardé, pas de
# nouveau tirage, sortie est bloquée tant que la bande tient la piste), sauvegarde dans la scène + rechargement, sortie de bord et reprise du
# trajet là où il s'était arrêté, sauvegarde en route + rechargement ; mobile : victoire, cache, sortie par le lit. Aucune erreur console.
# Env : URL (défaut http://127.0.0.1:8915/), OUT (défaut /tmp/nml-test-out/rencontres_j1/). Captures jpg dans OUT/livraison/.
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from nml_boot import passer_boot
import time, os, json, sys
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8915/')
if not URL.endswith('/'): URL += '/'
OUT = os.environ.get('OUT', '/tmp/nml-test-out/rencontres_j1/'); OUT = OUT if OUT.endswith('/') else OUT + '/'; os.makedirs(OUT + 'livraison', exist_ok=True)
fails = []; n = 0
def ok(c, m, d=''):
    global n; print(('OK   ' if c else 'ECHEC ') + m + ('' if c else f'  {d}'), flush=True); n += bool(c); c or fails.append(m)
LIEU = 'rc_embuscade_piste'
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    for name, vp, mob in [('desktop', (1280, 800), False), ('mobile', (390, 844), True)]:
        errs = []; ctx = br.new_context(viewport={'width': vp[0], 'height': vp[1]}, has_touch=mob, is_mobile=mob); pg = ctx.new_page(); E = pg.evaluate
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        def wait(js, t=20):
            t0 = time.time()
            while time.time() - t0 < t:
                if E(js): return True
                time.sleep(.25)
            return False
        def pret(t=60):
            wait("window.__nml.lieuPret(window.__nml.state.location)", t); time.sleep(1.2)
        def demarrer():
            pg.wait_for_function('window.__nml && window.__nml.shell', timeout=90000); time.sleep(1)
        def nouvelle():
            E("localStorage.removeItem('nml_save_auto')"); passer_boot(E); E("document.getElementById('m-new').click()"); time.sleep(.5)
            E("document.querySelector('[data-race=\"humain\"]').click()"); time.sleep(.3); E("document.getElementById('cr-next').click()"); time.sleep(.3); E("document.getElementById('cr-enter').click()"); time.sleep(1.5)
        def continuer():
            passer_boot(E); E("document.getElementById('m-continue').click()"); time.sleep(1.5); pret()
        S = lambda: E("(()=>{const s=window.__nml.state,R=s.region||{};return {loc:s.location,st:R.statut,case:R.case,trajet:R.trajet,x:s.player.x,z:s.player.z,dlg:s.dialogue,cbt:!!s.combat,money:s.player.money,inv:s.player.inv,rc:R.rencontre||null,journal:R.rencontres||{},carte:!document.getElementById('nml').hidden,flags:Object.keys(s.flags).filter(f=>/^emb_|^combat_embuscade/.test(f))}})()")
        def walk(x, z, t=40):
            r = E(f"window.__nml.game.moveTo({x},{z})"); t0 = time.time()
            while time.time() - t0 < t and E("window.__nml.state.player.path.length>0 && !window.__nml.state.dialogue && !window.__nml.state.combat"): time.sleep(.2)
            time.sleep(.5); return r
        choisir = lambda rx: E(f"(()=>{{const g=window.__nml.game,n=g.currentNode();const o=n&&n.options.find(o=>/{rx}/.test(o.label));return o?g.choose(o.index):null}})()")
        def shot(f, q=86): pg.screenshot(path=OUT + 'livraison/' + f, type='jpeg', quality=q)

        pg.goto(URL); demarrer(); nouvelle()
        # 0) catalogue : sprites d'Ocre (assets/rencontres) dans les bâtiments, PNJ et sols
        C = E("(()=>{const b=window.__nml.bman;return {bat:Object.keys(b).filter(k=>/^rc_/.test(k)).length}})()")
        ok(C['bat'] >= 19, f'{name} catalogue : {C["bat"]} décors rc_* chargés depuis assets/rencontres', C)
        # 1) déclenchement forcé depuis la carte : sortie est de Dusk-Town (dusk_q2), destination Steel, rencontre forcée sur la première case
        E("(()=>{const g=window.__nml.game,d=g.doorById('j_q2_est'),s=g.snapshot();s.location=d.location;s.player.x=d.threshold.x-1.5;s.player.z=d.threshold.z;g.restore(s,true)})()"); pret()
        E("(()=>{const n=window.__nml,d=n.game.doorById('j_q2_est');n.voyage.sortie(d);n.voyage.partir({lieu:'steel'});n.rencontres.forcer('embuscade_piste')})()")
        ok(wait("window.__nml.state.region.statut==='rencontre'", 20), f'{name} rencontre forcée : déclenchée par la carte à la première case du trajet', S()['st'])
        s = S(); trajet0 = s['trajet']
        ok(s['loc'] == LIEU and not s['carte'] and s['rc'] and s['rc']['retour']['location'] == 'dusk_q2' and len(trajet0) > 0, f'{name} entrée : scène {LIEU}, carte fermée, retour et trajet restant gardés', s)
        ok(abs(s['x'] - 1.5) < 0.6 and abs(s['z'] - 13) < 0.6, f'{name} arrivée à l\u2019entrée ouest (1,5 ; 13)', (s['x'], s['z']))
        pret()
        W = E("""(()=>{const n=window.__nml,L=n.world.LOCATIONS['%s'],b=n.bman;return {nb:L.buildings.length,manque:L.buildings.filter(x=>!b[x.sprite]).map(x=>x.id),gab:L.buildings.filter(x=>/gabarit/.test(x.sprite)).length,
          pnj:n.world.NPCS.filter(q=>q.location==='%s').map(q=>q.id),vis:n.world.NPCS.filter(q=>q.location==='%s'&&n.game.npcVisible(q)).map(q=>q.id),
          spots:n.world.SPOTS.filter(q=>q.location==='%s').length,portes:n.world.DOORS.filter(d=>d.location==='%s').map(d=>d.id)}})()""" % ((LIEU,) * 5))
        ok(W['nb'] == 21 and not W['manque'] and not W['gab'], f'{name} 21 décors posés avec les sprites d\u2019Ocre (aucun gabarit, aucune clé manquante)', W)
        ok(set(W['vis']) == {'rc_quilla_assise', 'rc_trapo'}, f'{name} à l\u2019arrivée : seules Quilla (assise) et Don Trapo sont visibles', W['vis'])
        ok(len(W['portes']) == 3 and W['spots'] >= 14, f'{name} 3 sorties de bord, {W["spots"]} points de fouille', W)
        time.sleep(1); shot(f'{name}_rencontre_arrivee.jpg')
        # 2) déplacement, fouille, examen
        r = walk(6, 13); s = S(); ok(r['ok'] and abs(s['x'] - 6) < 0.8 and abs(s['z'] - 13) < 0.8, f'{name} déplacement sur la piste', (r, s['x'], s['z']))
        E("(()=>{window.__ev=[];window.__nml.game.on(e=>window.__ev.push({type:e.type,id:e.id,text:e.text}))})()")
        E("window.__nml.game.useSpot('rc_panneau_ex')"); wait("window.__ev.some(e=>e.type==='pickup'&&e.id==='rc_panneau_ex')", 15)
        ok(E("window.__ev.some(e=>e.type==='pickup'&&e.id==='rc_panneau_ex'&&/flèche/.test(e.text))"), f'{name} examen du panneau UFSA')
        # 3) dialogue : T1, Quilla se lève et interpelle le joueur qui approche du pick-up
        walk(12, 13.5); wait("window.__nml.state.dialogue", 10); s = S()
        ok('emb_t1' in s['flags'] and E("window.__nml.state.dialogue?.npc") == 'rc_quilla' and E("window.__nml.game.currentNode().text").startswith('« Doucement'), f'{name} T1 : Quilla interpelle le joueur près du pick-up', (s['flags'], s['dlg']))
        vis = E(f"window.__nml.world.NPCS.filter(q=>q.location==='{LIEU}'&&window.__nml.game.npcVisible(q)).map(q=>q.id)"); ok('rc_quilla' in vis and 'rc_quilla_assise' not in vis, f'{name} Quilla debout à la place de Quilla assise', vis)
        choisir('Ta route'); ok('Péage' in E("window.__nml.game.currentNode().text") or 'péage' in E("window.__nml.game.currentNode().text").lower(), f'{name} réplique « Ta route ? » : le péage', E("window.__nml.game.currentNode()?.text"))
        choisir('…'); choisir('^« Non'); choisir('demi-tour'); choisir('Partir'); ok(not E("window.__nml.state.dialogue") and 'emb_demi' in S()['flags'], f'{name} refus puis « Je fais demi-tour » : dialogue fermé')
        m0 = S()['money']; E("window.__nml.game.useSpot('rc_boite_gants')"); wait("window.__nml.state.flags.emb_f_gants", 20); s = S()
        ok('emb_f_gants' in s['flags'] and s['money'] == m0 + 4 and s['inv'].get('carnet_chauffeur') == 1, f'{name} fouille de la boîte à gants : 4 $ et le carnet du chauffeur', (s['money'], s['inv']))
        r = E("window.__nml.game.useSpot('rc_boite_gants')"); ok(not r['ok'] and r['reason'] == 'rien', f'{name} boîte à gants vide au second passage', r)
        E("window.__nml.game.talkTo('rc_trapo')"); wait("window.__nml.state.dialogue", 15)
        ok(E("window.__nml.state.dialogue?.npc") == 'rc_trapo' and E("document.getElementById('dlg-portrait').hidden"), f'{name} Don Trapo : chiffons et paille (dialogue sans portrait)', E("window.__nml.state.dialogue"))
        E("window.__nml.game.closeDialogue()"); E("window.__nml.game.talkTo('rc_quilla')"); wait("window.__nml.state.dialogue", 15)
        ok(E("window.__nml.state.dialogue?.npc") == 'rc_quilla' and E("window.__nml.game.currentNode().options.some(o=>/en chiffons/.test(o.label))"), f'{name} option « Ton chauffeur est en chiffons » (mannequin vu)')
        # 4) combat : [Attaquer] ; tirage figé (tout manque) pour un test stable
        E("window.__nml.game.setRng(()=>0.99)"); choisir('Attaquer'); ok(wait("window.__nml.state.combat", 10), f'{name} combat lancé depuis le dialogue')
        Cb = E("(()=>{const c=window.__nml.state.combat;return {z:c.zone,u:c.units.map(u=>({id:u.id,i:u.i,j:u.j,a:u.actif,att:!!u.attend,arme:u.arme}))}})()")
        ids = {u['id'] for u in Cb['u']}; z = Cb['z']
        ok(z == {'i0': 9, 'i1': 27, 'j0': 4, 'j1': 22}, f'{name} zone de combat fixée sur la scène (centre 18 ; 13)', z)
        ok(ids == {'joueur', 'quilla', 'pibe', 'morsa', 'tuerto'} and any(u['id'] == 'tuerto' and u['att'] for u in Cb['u']), f'{name} unités : Quilla, Pibe, Morsa, Tuerto en renfort (entre au tour 2)', Cb['u'])
        q = next(u for u in Cb['u'] if u['id'] == 'quilla'); ok((q['i'], q['j']) == (19, 12), f'{name} Quilla à sa position de la scène (19 ; 12)', q)
        vis = E(f"window.__nml.world.NPCS.filter(q=>q.location==='{LIEU}'&&window.__nml.game.npcVisible(q)).map(q=>q.id)"); ok(vis == ['rc_trapo'], f'{name} PNJ de la bande remplacés par leurs unités pendant le combat', vis)
        ok(wait("window.__nml.state.combat && window.__nml.state.combat.phase==='joueur'", 30), f'{name} tour du joueur')
        time.sleep(1.2); shot(f'{name}_rencontre_combat.jpg')
        # 5) fuite : une case de bord de la zone
        # 5) fuite : vers l'ouest, case par case (PA du tour), jusqu'à une case de bord de la zone ; tours ennemis entre deux
        tours = 0; t0 = time.time()
        while time.time() - t0 < 120 and E("!!window.__nml.state.combat"):
            if not wait("!window.__nml.state.combat || (window.__nml.state.combat.phase==='joueur' && !window.__nml.game.combat.player().path.length)", 30): break
            if not E("!!window.__nml.state.combat"): break
            E(f"""(()=>{{const c=window.__nml.game.combat,r=c.reachable().sort((a,b)=>a.i-b.i||Math.abs(a.j-13)-Math.abs(b.j-13))[0];const m=c.moveTo(r.i+0.5,r.j+0.5);if(!m.ok)c.endTurn();}})()""")
            time.sleep(.4); wait("!window.__nml.state.combat || !window.__nml.game.combat.player().path.length", 10); time.sleep(.3)
            if E("!!window.__nml.state.combat && window.__nml.state.combat.phase==='joueur'"): E("window.__nml.game.combat.endTurn()"); tours += 1
        ok(wait("window.__nml.state.region.statut==='halte'", 20), f'{name} fuite par le bord ouest de la zone ({tours + 1} tours) : retour à la carte en halte', S()['st'])
        s = S(); K = ','.join(map(str, s['case'])); j = s['journal'].get(K, {})
        ok(s['loc'] == 'dusk_q2' and s['carte'] and s['trajet'] == trajet0 and not s['flags'], f'{name} carte rouverte, trajet restant intact, drapeaux de scène rangés au journal', s)
        ok(j.get('regle') is False and j['flags'].get('emb_f_gants') and j['flags'].get('emb_t1'), f'{name} journal de la case {K} : non réglée, butin pris et rencontre gardés', j)
        E("window.__nml.game.setRng(null)")
        time.sleep(1.2); shot(f'{name}_rencontre_retour_carte.jpg')
        ev = E(f"(()=>{{const v=window.__nml.voyage;return [0,1,2,3,4].map(()=>v.crochets.onCaseEntree({{col:{s['case'][0]},row:{s['case'][1]},terrain:'piste'}},window.__nml.state)?.rencontre||null)}})()")
        ok(all(e == 'embuscade_piste' for e in ev), f'{name} case non réglée : la bande tient toujours la piste (pas de nouveau tirage)', ev)
        if name == 'desktop':
            # 6) retour sur la case : scène telle qu'on l'a laissée ; sortie est refusée ; sauvegarde dans la scène + rechargement
            E(f"window.__nml.rencontres.entrer('embuscade_piste',[{s['case'][0]},{s['case'][1]}])"); pret(); s2 = S()
            ok(s2['loc'] == LIEU and 'emb_f_gants' in s2['flags'] and not E("window.__nml.game.useSpot('rc_boite_gants').ok"), f'{name} retour : boîte à gants toujours vide (journal restauré)', s2['flags'])
            r = E(f"window.__nml.game.useDoor('{LIEU}_est_route')"); ok(not r['ok'] and r['reason'] == 'rencontre_bloquee', f'{name} sortie est refusée tant que Quilla tient la piste', r)
            E("window.__nml.shell.autosave()"); pg.reload(); demarrer(); continuer(); s3 = S()
            ok(s3['loc'] == LIEU and s3['st'] == 'rencontre' and 'emb_f_gants' in s3['flags'] and E(f"!!window.__nml.world.LOCATIONS['{LIEU}']"), f'{name} sauvegarde dans la scène rechargée : scène recréée, drapeaux gardés', s3)
            # 7) péage puis sortie est : le trajet reprend là où il s'était arrêté
            E("window.__nml.game.talkTo('rc_quilla')"); wait("window.__nml.state.dialogue", 20); choisir('juste passer'); m1 = S()['money']; choisir('Voilà 15'); E("window.__nml.game.closeDialogue()")
            s = S(); ok('emb_regle' in s['flags'] and s['money'] == m1 - 15, f'{name} péage payé : 15 $', (s['money'], m1))
            walk(28, 13, 60); E(f"window.__nml.game.useDoor('{LIEU}_est_route')")
            ok(wait("['route','halte'].includes(window.__nml.state.region.statut) && window.__nml.state.location!=='%s'" % LIEU, 40), f'{name} sortie est : scène quittée')
            s = S(); ok(s['st'] == 'route' or s['trajet'] != trajet0, f'{name} reprise du trajet vers Steel là où il s\u2019était arrêté', (s['st'], s['trajet'], trajet0))
            ok(s['journal'][K]['regle'] and not E(f"window.__nml.voyage.crochets.onCaseEntree({{col:{K.split(',')[0]},row:{K.split(',')[1]},terrain:'piste'}},window.__nml.state)"), f'{name} case réglée : plus de rencontre ici', s['journal'][K])
            ok(not E(f"!!window.__nml.world.LOCATIONS['{LIEU}']"), f'{name} scène retirée des lieux après la sortie')
            # 8) sauvegarde en route + rechargement : halte sur la dernière case, trajet gardé
            E("window.__nml.voyage.halte()"); s = S(); E("window.__nml.shell.autosave()"); pg.reload(); demarrer(); continuer(); time.sleep(1); s4 = S()
            ok(s4['st'] == 'halte' and s4['case'] == s['case'] and s4['trajet'] == s['trajet'] and K in s4['journal'], f'{name} sauvegarde en route rechargée : halte, trajet et journal des rencontres gardés', s4)
        else:
            # 6') mobile : retour, victoire (fin de combat forcée), cache sous la bâche, sortie par le lit
            E(f"window.__nml.rencontres.entrer('embuscade_piste',[{s['case'][0]},{s['case'][1]}])"); pret()
            E("window.__nml.game.talkTo('rc_quilla')"); wait("window.__nml.state.dialogue", 20); choisir('Ta route'); choisir('…'); choisir('Non'); choisir('Attaquer')
            ok(wait("window.__nml.state.combat", 10), f'{name} combat relancé')
            E("window.__nml.game.combat.finish('victoire')"); time.sleep(.5); s = S()
            ok('emb_vaincue' in s['flags'] and 'emb_regle' in s['flags'], f'{name} victoire : la bande s\u2019en va (piste réglée)', s['flags'])
            vis = E(f"window.__nml.world.NPCS.filter(q=>q.location==='{LIEU}'&&window.__nml.game.npcVisible(q)).map(q=>q.id)"); ok(vis == ['rc_trapo'], f'{name} plus de pillards sur la scène', vis)
            m2 = S()['money']; E("window.__nml.game.useSpot('rc_cache')"); wait("window.__nml.state.flags.emb_f_cache", 30); s = S()
            ok('emb_f_cache' in s['flags'] and s['money'] == m2 + 22 and s['inv'].get('water') == 3 and s['inv'].get('poignard') == 1, f'{name} cache sous la bâche : 22 $, 3 bidons, ration, poignard', (s['money'], s['inv']))
            E(f"window.__nml.game.useDoor('{LIEU}_est_lit')")
            ok(wait("window.__nml.state.location!=='%s'" % LIEU, 60), f'{name} sortie par le lit asséché')
            s = S(); ok(s['st'] in ('route', 'halte', 'lieu') and s['journal'][K]['regle'], f'{name} trajet repris après la sortie est (lit)', (s['st'], s['trajet']))
        errs2 = [e for e in errs if 'favicon' not in e]
        ok(not errs2, f'{name} aucune erreur console', errs2[:5])
        ctx.close()
    br.close()
print(f'\n{n} OK, {len(fails)} échec(s)'); [print(' -', f) for f in fails]
sys.exit(1 if fails else 0)
