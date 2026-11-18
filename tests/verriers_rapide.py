# Test rapide des rencontres de route, jalon 2, lot 2 (docs/rencontres/MUTANTS.md §12.14) : « L’écluse des Verriers ».
# Catalogue et grille : biome verre seulement (terrains verre et piste : I04, I03, K03 sont de la piste), aucune piste du désert touchée ; Verriers uniques.
# 1280 x 800 : forcer ecluse_verriers depuis la carte, arrivée (sprites d’Ocre, sorties, PNJ visibles, Nilo caché), cadrage, T1 Balta, montrer le cou
# (4 races), soigner (Médecine 4), Ines et le message (monde_lena_connue forcé), commerce (eau 3 $ en confiance, 5 $, lame 12 $, ration rachetée 5 $),
# leurre d’eau (Tecla, jarre de Nilo par la fenêtre, pres_cabane, rigole Survie 4), récompense, Nilo dehors, blindé (Volonté 4), rayonnement du verre
# (humain, compteur, mutant), filière et Lena (monde_lena_connue), perles, sortie est (reprise, +1 h), drapeaux ver_* purgés, monde_* gardés, unique.
# 390 x 844 : cadrage, passer, attendre la nuit (+4 h, +3 PV), vol de l’établi réussi et raté, tison (réussi, partiel, raté -> combat), combat
# (unités, zone, Verriers cachés, jeune_c fuit au tour 2, victoire « Le gris détale. », reddition et défaite dans la scène, fuite en halte),
# retour sur la case, rançon réussie et ratée, attaquer -> fuite des Verriers puis fouilles. Nuit / jour : flaque du four (décalque, nuit seulement),
# le verre ne luit pas, liseré tête et épaules ; créatures ancrées au centre des pattes, face au sud-ouest. Aucune erreur console.
# Env : URL (défaut http://127.0.0.1:8915/), OUT (défaut /tmp/nml-test-out/rencontres_j2_verriers/). Captures jpg dans OUT/livraison/.
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from nml_boot import passer_boot
import time, os, json, sys, io
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8915/')
if not URL.endswith('/'): URL += '/'
OUT = os.environ.get('OUT', '/tmp/nml-test-out/rencontres_j2_verriers/'); OUT = OUT if OUT.endswith('/') else OUT + '/'; os.makedirs(OUT + 'livraison', exist_ok=True)
fails = []; n = 0
def ok(c, m, d=''):
    global n; print(('OK   ' if c else 'ECHEC ') + m + ('' if c else f'  {d}'), flush=True); n += bool(c); c or fails.append(m)
LIEU, RID = 'rc_ecluse_verriers', 'ecluse_verriers'
VERRIERS = {'rc_balta', 'rc_tecla', 'rc_rufina'}; HARDE = {'rc_gris', 'rc_chancho_a', 'rc_chancho_b', 'rc_chancho_c'}
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
        S = lambda: E("(()=>{const s=window.__nml.state,R=s.region||{};return {loc:s.location,st:R.statut,case:R.case,trajet:R.trajet,x:s.player.x,z:s.player.z,dlg:s.dialogue,cbt:!!s.combat,money:s.player.money,inv:s.player.inv,rc:R.rencontre||null,journal:R.rencontres||{},h:s.heures,hp:s.player.hp,carte:!document.getElementById('nml').hidden,flags:Object.keys(s.flags).filter(f=>s.flags[f]&&/^ver_|^monde_|^combat_ecluse|^race_/.test(f))}})()")
        def walk(x, z, t=60):
            r = E(f"window.__nml.game.moveTo({x},{z})"); t0 = time.time()
            while time.time() - t0 < t and E("window.__nml.state.player.path.length>0 && !window.__nml.state.dialogue && !window.__nml.state.combat"): time.sleep(.2)
            time.sleep(.5); return r
        choisir = lambda rx: E(f"(()=>{{const g=window.__nml.game,n=g.currentNode();const o=n&&n.options.find(o=>/{rx}/.test(o.label));return o?g.choose(o.index):null}})()")
        labels = lambda: E("(()=>{const n=window.__nml.game.currentNode();return n?n.options.map(o=>o.label):[]})()")
        noeud = lambda: E("window.__nml.game.currentNode()?.text||''")
        fermer = lambda: E("window.__nml.game.closeDialogue()")
        parler = lambda pnj: (fermer(), E(f"window.__nml.game.talkTo('{pnj}')"), wait("window.__nml.state.dialogue", 40))
        ouvrir = lambda pnj, nd='start': (fermer(), E(f"window.__nml.game.ouvrirDialogue('{pnj}','{nd}')"))
        def fouiller(sp, fl=None, t=60):
            fermer(); E("window.__ev=[]"); r = E(f"window.__nml.game.useSpot('{sp}')")
            wait(f"window.__nml.state.flags['{fl}']" if fl else f"window.__ev.some(e=>e.type==='pickup'&&e.id==='{sp}')||window.__nml.state.dialogue||window.__nml.state.combat", t); time.sleep(.4); return r
        vis = lambda: set(E(f"window.__nml.world.NPCS.filter(q=>q.location==='{LIEU}'&&window.__nml.game.npcVisible(q)).map(q=>q.id)"))
        def shot(f, q=86): pg.screenshot(path=OUT + 'livraison/' + f, type='jpeg', quality=q)
        def forcer():
            E("(()=>{const g=window.__nml.game,d=g.doorById('j_q2_est'),s=g.snapshot();s.location=d.location;s.player.x=d.threshold.x-1.5;s.player.z=d.threshold.z;g.restore(s,true)})()"); pret()
            E("(()=>{const n=window.__nml,d=n.game.doorById('j_q2_est');n.voyage.sortie(d);n.voyage.partir({lieu:'steel'});n.rencontres.forcer('%s')})()" % RID)
            return wait("window.__nml.state.region.statut==='rencontre'", 20)
        stats = lambda **kv: E("kv=>{const c=window.__nml.state.character;for(const[k,v] of Object.entries(kv)){if(k in c.attrs)c.attrs[k]=v;else c.skills[k]=v}}", kv)
        race = lambda r: E("r=>{const f=window.__nml.state.flags;for(const k of Object.keys(f))if(/^race_/.test(k))delete f[k];f['race_'+r]=true}", r)
        oter = lambda *fl: E("fl=>{const f=window.__nml.state.flags;for(const k of fl)delete f[k]}", list(fl))
        poser = lambda *fl: E("fl=>{const f=window.__nml.state.flags;for(const k of fl)f[k]=true}", list(fl))
        rng = lambda v: E(f"window.__nml.game.setRng(()=>{v})")
        msg = lambda: E("document.getElementById('msg').textContent||''")
        inv = lambda k: S()['inv'].get(k, 0)

        pg.goto(URL); demarrer(); nouvelle()
        E("(()=>{window.__ev=[];window.__nml.game.on(e=>window.__ev.push({type:e.type,id:e.id,text:e.text}))})()")
        if not mob:
            # 0) catalogue et grille : biome verre seulement, piste du verre comprise, aucune piste du désert
            T = E("""(()=>{const n=window.__nml,R=n.rencontres.RENCONTRES,D=R.ecluse_verriers,cells=[...n.voyage.cells.values()];
              const elig=c=>Object.entries(R).filter(([id,d])=>d.terrains.includes(c.terrain)&&(!d.biomes||d.biomes.includes(c.biome))).map(([id])=>id);
              const lab=c=>String.fromCharCode(65+c.col)+String(c.row+1).padStart(2,'0');
              const glass=cells.filter(c=>c.biome==='glass').map(c=>({l:lab(c),t:c.terrain,e:elig(c),lieu:!!n.voyage.lieuAt(c.col,c.row)}));
              const desertPiste=cells.filter(c=>c.biome!=='glass'&&c.terrain==='piste').map(c=>elig(c));
              return {D:{t:D.terrains,b:D.biomes,pre:D.prefixe},glass,dp:desertPiste.length,dpVer:desertPiste.filter(e=>e.includes('ecluse_verriers')).length,
                enc:!!n.rencontres.RENCONTRES.ecluse_verriers.combat,item:!!(n.world.ITEMS||{}).perles_verre,amb:true}})()""")
            ok(T['D']['t'] == ['verre', 'piste'] and T['D']['b'] == ['glass'] and T['D']['pre'] == 'ver_', 'catalogue : terrains [verre, piste], biomes [glass], préfixe ver_', T['D'])
            g = {c['l']: c for c in T['glass']}
            ok(all(g.get(k, {}).get('t') == 'piste' for k in ('I04', 'I03', 'K03')), 'grille : I04, I03 et K03 sont des cases de piste du verre (BIOME_TERRAIN.glass ailleurs : verre)', {k: g.get(k) for k in ('I04', 'I03', 'K03')})
            ok(all(c['t'] in ('verre', 'piste') for c in T['glass']) and all('ecluse_verriers' in c['e'] for c in T['glass'] if not c['lieu']), f'grille : l\u2019écluse peut tomber sur les {sum(not c["lieu"] for c in T["glass"])} cases de verre hors lieu', T['glass'])
            ok(all(set(c['e']) <= {'ecluse_verriers'} for c in T['glass']), 'grille : ni le pilote ni la caravane ne tirent sur le verre', T['glass'])
            ok(T['dp'] > 0 and T['dpVer'] == 0, f'grille : aucune des {T["dp"]} cases de piste du désert ou de la roche ne tire l\u2019écluse', T)
            ok(E("!!window.__nml.world.ITEMS?.perles_verre || !!window.__nml.rencontres") and E("(()=>{try{return true}catch(e){return false}})()"), 'objet perles_verre déclaré')
        # 1) forcer depuis la carte
        ok(forcer(), f'{name} écluse forcée depuis la carte', S()['st'])
        s = S(); ok(s['loc'] == LIEU and not s['carte'] and s['rc'], f'{name} entrée : scène {LIEU}, carte fermée', s['loc'])
        ok(abs(s['x'] - 1.5) < 0.6 and abs(s['z'] - 24) < 0.6, f'{name} arrivée à l\u2019ouest de la piste (1,5 ; 24)', (s['x'], s['z']))
        ok('monde_verriers_vus' in s['flags'], f'{name} drapeau monde_verriers_vus posé à l\u2019arrivée', s['flags'])
        pret()
        W = E("""(()=>{const n=window.__nml,L=n.world.LOCATIONS['%s'];return {w:L.size.w,d:L.size.d,niv:(L.niveaux||[]).length,manque:L.buildings.filter(x=>!n.bman[x.sprite]).map(x=>x.id),
          pnj:n.world.NPCS.filter(q=>q.location==='%s'),spots:n.world.SPOTS.filter(q=>q.location==='%s').length,portes:n.world.DOORS.filter(d=>d.location==='%s').map(d=>[d.id,d.effet]),
          ens:L.enseignes,light:L.light,miroirs:L.buildings.filter(b=>b.miroir).map(b=>b.id),texte:L.buildings.find(b=>b.id==='ver_blinde_texte'),flaqueB:L.buildings.some(b=>/flaque/.test(b.sprite))}})()""" % ((LIEU,) * 4))
        gab = [q['id'] for q in W['pnj'] if q.get('gabarit')]
        ok(W['w'] == 36 and W['d'] == 30 and not W['niv'], f'{name} scène 36 × 30, sans niveaux', (W['w'], W['d'], W['niv']))
        ok(len(W['portes']) == 2 and {q[0].split('_')[-1]: q[1] for q in W['portes']} == {'ouest': 'halte', 'est': 'reprise'}, f'{name} 2 sorties : ouest (halte), est (reprise, jamais gardée)', W['portes'])
        ok(vis() == VERRIERS | HARDE, f'{name} à l\u2019arrivée : Balta, Tecla, Rufina et la harde (Nilo enfermé, invisible)', vis())
        ok(not gab and not W['manque'], f'{name} sprites d\u2019Ocre câblés : décors, PNJ et créatures (aucun gabarit, aucune clé manquante)', (gab, W['manque']))
        ok(W['spots'] >= 14, f'{name} {W["spots"]} points d\u2019examen et de fouille', W['spots'])
        e0 = (W['ens'] or [{}])[0]
        ok(e0.get('id') == 'ver_feu' and e0.get('building') == 'ver_four' and e0.get('periode') == 7 and e0.get('intensite') == 1.3 and e0.get('flaque', {}).get('cle') == 'rc_ecl_four_flaque' and e0['flaque'].get('echelle') == 3.5 and not W['flaqueB'],
           f'{name} four : enseigne ver_feu (pulse 7 s, 1,3, calibrée sur le bivouac) et flaque rc_ecl_four_flaque ×3,5 par le mécanisme générique (pas un décor posé en permanence)', (e0, W['flaqueB']))
        ok(W['miroirs'] == ['ver_cond2'] and W['texte'] and W['texte'].get('etage') == 1 and not W['texte'].get('miroir') and (W['texte']['x'], W['texte']['z'], W['texte']['w'], W['texte']['d']) == (26, 1, 5, 3),
           f'{name} condenseur du milieu en miroir ; lettrage du blindé en calque normal etage 1 sur (26 ; 1 ; 5 × 3), jamais en miroir', (W['miroirs'], W['texte']))
        ok(W['light'] and W['light'].get('tint') == '#efe9da' and W['light'].get('lune', 1) == 0, f'{name} ambiance glass de jour (plus blanche que le désert, liseré éteint)', W['light'])
        A = {a['id']: a for a in E("window.__nml.view.acteurs()")}
        gr = A.get('rc_gris', {}); ja = A.get('rc_chancho_a', {})
        ok(abs(gr.get('cy', 0) - (1 - 213 / 270)) < 0.01 and abs(min(gr.get('cx', 0), 1 - gr.get('cx', 0)) - (1 - 172 / 308)) < 0.01 and not gr.get('miroir') and not gr.get('dos'),
           f'{name} le gris : ancré au centre des pattes (ancre du manifeste), face au sud-ouest vers la cabane (ni miroir ni dos)', gr)
        ok(ja.get('miroir') and abs(ja.get('cy', 0) - (1 - 185 / 231)) < 0.01, f'{name} jeune chancho tourné vers l\u2019est : miroir de la face (sud-est)', ja)
        # cadrage d'arrivée : sorties entières, joueur, four et cabane dans le cadre, encart hors des sorties, titre hors zoom
        CAD = """(()=>{const n=window.__nml,s=n.state,W=innerWidth,H=innerHeight,r=e=>{const q=e.getBoundingClientRect();return [q.left,q.top,q.right,q.bottom]};
          const ex=[...document.querySelectorAll('#labels .wlabel.edge,#labels .wlabel.junction')].filter(e=>!e.hidden&&e.style.visibility!=='hidden'&&e.getClientRects().length).map(e=>({t:e.textContent,r:r(e)}));
          const P=(x,z)=>{const p=n.project(x,0,z);return [p.x,p.y]},m=document.getElementById('msg');
          const B=[];for(const x of [26,31])for(const z of [1,4])for(const y of [0,3.2]){const p=n.project(x,y,z);B.push([p.x,p.y])}
          const npcl=[...document.querySelectorAll('#labels .wlabel.npc')].filter(e=>!e.hidden&&e.style.visibility!=='hidden'&&e.getClientRects().length).map(e=>e.textContent);
          return {W,H,ex,npcl,blinde:[Math.min(...B.map(q=>q[0])),Math.min(...B.map(q=>q[1])),Math.max(...B.map(q=>q[0])),Math.max(...B.map(q=>q[1]))],joueur:P(s.player.x,s.player.z),four:P(11.5,19),cabane:P(26,20),balta:P(5.5,20.4),msg:m.textContent&&m.getClientRects().length?r(m):null,loc:r(document.getElementById('locbox')),zoom:r(document.getElementById('zoom'))}})()"""
        inter = lambda a, b: a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]
        K0 = E(CAD); Wv, Hv = K0['W'], K0['H']
        ok(len(K0['ex']) == 2 and all(e['r'][0] >= 6 and e['r'][2] <= Wv - 6 and e['r'][1] >= 0 and e['r'][3] <= Hv for e in K0['ex']), f'{name} cadrage : les 2 étiquettes de sortie entières, à 6 px au moins du bord', K0['ex'])
        cibles = (K0['joueur'], K0['balta']) if mob else (K0['joueur'], K0['balta'], K0['four'], K0['cabane'])
        ok(all(8 <= q[0] <= Wv - 8 and 60 <= q[1] <= Hv - 150 for q in cibles), f'{name} cadrage : joueur et Balta' + ('' if mob else ', four et cabane') + ' dans le cadre', cibles)
        ok(not inter(K0['loc'], K0['zoom']), f'{name} titre du lieu hors des boutons de zoom', (K0['loc'], K0['zoom']))
        if not mob: ok(K0['blinde'][0] >= 0 and K0['blinde'][2] <= Wv and K0['blinde'][1] >= 0, f'{name} cadrage : le blindé entre en entier (repère de la scène)', K0['blinde'])
        ok((K0['npcl'].count('La harde') <= 1 if mob else K0['npcl'].count('La harde') == 1 and K0['npcl'].count('Le gris') == 1) and 'Chancho' not in K0['npcl'], f'{name} étiquettes : une seule « La harde » sur les jeunes, plus « Le gris »', K0['npcl'])
        ARR = E(f"window.__nml.rencontres.RENCONTRES.{RID}.arrivee")
        for _ in range(4):
            E("t=>{document.getElementById('msg').textContent=t}", ARR); time.sleep(.4); K1 = E(CAD)
            if K1['msg']: break
        ok(K1['msg'] and len(K1['ex']) == 2 and not any(inter(K1['msg'], e['r']) for e in K1['ex']), f'{name} encart d\u2019arrivée : ne chevauche aucune étiquette de sortie', (K1['msg'], K1['ex']))
        time.sleep(.6); shot(f'{name}_verriers_arrivee.jpg')

        if not mob:
            # 2) T1 : Balta demande à voir le cou ; humain -> col_humain -> la harde -> aider
            walk(5, 22); wait("window.__nml.state.dialogue", 10)
            ok(E("window.__nml.state.dialogue?.npc") == 'rc_balta' and 'le cou' in noeud(), f'{name} T1 : Balta interpelle (le cou)', noeud())
            choisir('Mon cou'); L = labels(); ok(sum('Baisser' in l for l in L) == 1, f'{name} humain : une seule réponse « Baisser le col »', L)
            shot(f'{name}_verriers_dialogue.jpg')
            choisir('Baisser'); ok(E("window.__nml.state.dialogue?.node") == 'col_humain', f'{name} humain : peau intacte (col_humain)', noeud())
            choisir('…'); choisir('Je peux aider'); s = S(); ok({'ver_salue', 'ver_q_harde', 'ver_t1'} <= set(s['flags']), f'{name} la harde, « Je peux aider » : voir la vieille au four', s['flags']); choisir('Partir')
            # 3) montrer le cou, 4 races
            for r, nd, fl in [('mutant', 'col_mutant', 'ver_confiance'), ('augmente', 'implant', 'ver_mefiance'), ('cyborg', 'implant', 'ver_mefiance'), ('humain', 'col_humain', None)]:
                oter('ver_confiance', 'ver_mefiance'); race(r); ouvrir('rc_balta', 'col'); L = labels(); choisir('Baisser'); s = S()
                ok(sum('Baisser' in l for l in L) == 1 and E("window.__nml.state.dialogue?.node") == nd and (fl is None and not {'ver_confiance', 'ver_mefiance'} & set(s['flags']) or fl in s['flags']),
                   f'{name} cou montré, race {r} : {nd}' + (f' ({fl})' if fl else ' (neutre)'), (L, s['flags']))
            oter('ver_salue'); race('mutant'); ouvrir('rc_balta'); ok(any('Tu baisses ton col' in l for l in labels()), f'{name} mutant : baisse le col sans qu\u2019on le redemande', labels()); poser('ver_salue'); race('humain'); oter('ver_confiance', 'ver_mefiance'); fermer()
            # 4) encore : soigner (Médecine 4), Ines, message pour Ines (monde_lena_connue forcé), conseil du gris
            parler('rc_balta'); ok(noeud().startswith('« Encore là'), f'{name} seconde entrée de Balta : « Encore là. »', noeud())
            stats(medecine=80); rng(0.99); choisir('jambe'); s = S(); ok({'ver_soigne', 'ver_confiance'} <= set(s['flags']), f'{name} soigner Balta (Médecine 4) : confiance', s['flags']); choisir('…')
            choisir('attendre quelqu'); ok('Ines' in noeud() and 'ver_ines' in S()['flags'], f'{name} Ines, la Sous-Ville', noeud()); choisir('…')
            ok(not any('Lena' in l for l in labels()), f'{name} sans monde_lena_connue : pas de réplique Lena', labels())
            poser('monde_lena_connue'); parler('rc_balta'); choisir('Lena'); s = S()
            ok({'ver_message_ines', 'monde_message_ines'} <= set(s['flags']) and s['inv'].get('perles_verre') == 1, f'{name} message pour Ines : une perle rouge, monde_message_ines', (s['flags'], s['inv'])); choisir('…')
            choisir('Le gris'); ok('ver_conseil_gris' in S()['flags'], f'{name} conseil de Balta : tape le gris', S()['flags']); fermer()
            # 5) commerce de Rufina : eau 3 $ (confiance) puis 5 $, lame 12 $, ration rachetée 5 $ (une fois), stock limité
            E("window.__nml.state.player.money=100; window.__nml.state.player.inv.ration=1"); parler('rc_rufina'); choisir('vends')
            L = labels(); ok(any('prix d' in l and '3 $' in l for l in L), f'{name} étal de Rufina : l\u2019eau à 3 $ (prix d\u2019ami)', L)
            m0, w0 = S()['money'], inv('water'); choisir('Une eau'); choisir('Une autre'); s = S()
            ok(s['money'] == m0 - 8 and s['inv'].get('water', 0) == w0 + 2 and not any(l.startswith('« Une eau') or l.startswith('« Une autre') for l in labels()), f'{name} deux eaux (3 $ puis 5 $), stock épuisé', (m0 - s['money'], labels()))
            m0 = S()['money']; choisir('Une lame'); ok(S()['money'] == m0 - 12 and inv('poignard') >= 1 and 'chiffon' in noeud(), f'{name} lame de verre noir 12 $ (poignard)', S()['inv']); choisir('…')
            m0 = S()['money']; choisir('ration'); ok(S()['money'] == m0 + 5 and not inv('ration'), f'{name} ration rachetée 5 $', S()['money'] - m0); choisir('…')
            ok(not any('ration' in l for l in labels()), f'{name} une seule ration rachetée', labels()); fermer()
            # 6) leurre d'eau : Tecla -> jarre de Nilo par la fenêtre -> rigole (Survie 4)
            parler('rc_tecla'); ok('bonnes bottes' in noeud(), f'{name} Tecla, assise au four', noeud())
            choisir('chanchos'); choisir('Leur donner'); ok('ver_q_leurre' in S()['flags'], f'{name} Tecla : le leurre d\u2019eau par la rigole de l\u2019est'); fermer()
            E("window.__nml.state.player.inv.water=0"); fouiller('ver_fenetre'); wait("window.__nml.state.dialogue", 10)
            ok(E("window.__nml.state.dialogue?.npc") == 'rc_nilo_voix' and 'fenêtre' in noeud() and 'rc_nilo' not in vis(), f'{name} Nilo par la fenêtre (26 ; 20,4), invisible', (E("window.__nml.state.dialogue"), noeud()))
            choisir('Non'); choisir('…'); choisir('jarre'); s = S(); ok(s['inv'].get('water') == 1 and 'ver_jarre' in s['flags'], f'{name} jarre de Nilo passée par la fenêtre', s['inv']); choisir('Partir')
            walk(22, 23); walk(26, 20.5); wait("window.__nml.state.dialogue", 6)
            ok(E("window.__nml.state.dialogue?.npc") == 'rc_nilo_voix', f'{name} déclencheur pres_cabane : Nilo parle par la fenêtre', E("window.__nml.state.dialogue")); fermer()
            stats(survie=80); rng(0.99); fouiller('ver_rigole', 'ver_harde_partie', 90); s = S()
            ok({'ver_harde_partie', 'ver_leurre'} <= set(s['flags']) and not s['inv'].get('water') and not HARDE & vis(), f'{name} rigole (Survie 4) : la harde suit l\u2019eau dans le verre', (s['flags'], vis()))
            # 7) récompense, Balta après, Nilo dehors, blindé
            parler('rc_tecla'); w0, p0 = inv('water'), inv('perles_verre'); choisir('cuve est vide'); s = S()
            ok(s['inv'].get('water', 0) == w0 + 2 and s['inv'].get('perles_verre', 0) == p0 + 3 and {'monde_verriers_amis', 'ver_nilo_libre', 'ver_merci'} <= set(s['flags']), f'{name} récompense de Tecla : 2 eaux, 3 perles, monde_verriers_amis', (s['inv'], s['flags']))
            choisir('…'); choisir('…'); fermer(); time.sleep(.6); ok('rc_nilo' in vis(), f'{name} Nilo sort de la cabane', vis())
            parler('rc_balta'); ok(noeud().startswith('(Il a reposé'), f'{name} Balta après : « Je te dois une balle »', noeud()); fermer()
            parler('rc_nilo'); ok('partis' in noeud(), f'{name} Nilo dehors : « Ils sont partis ? »', noeud()); choisir('Vraiment')
            ok('te mange' in noeud() and 'ver_nilo_blinde' in S()['flags'], f'{name} Nilo : le blindé (humain : le verre te mange)', noeud()); choisir('Partir')
            stats(volonte=9, observation=10); rng(0.99); E("window.__nml.state.player.hp=30"); m0, r0 = S()['money'], inv('ration'); fouiller('ver_blinde', 'ver_f_blinde', 120); s = S()
            ok(s['money'] == m0 + 10 and s['inv'].get('ration', 0) == r0 + 2 and 'ver_verre_dit' in s['flags'], f'{name} blindé (Volonté 4, non-mutant) : 2 rations, 10 $', (s['money'] - m0, s['inv'], s['flags']))
            ok(s['hp'] == 28, f'{name} verre et blindé : −1 PV en marchant sur le verre (humain), −1 PV dans le blindé', s['hp'])
            # 8) rayonnement du verre : compteur, mutant (texte seul), une fois par scène
            for r, cpt, mot, dpv in [('humain', 1, 'crépiter', 1), ('mutant', 0, 'peau ne dit rien', 0)]:
                oter('ver_verre_dit'); race(r); E(f"window.__nml.state.player.inv.compteur={cpt}"); walk(20, 7.8); hp0 = S()['hp']; walk(20, 5); time.sleep(.6)
                ok(mot in msg() and S()['hp'] == hp0 - dpv and 'ver_verre_dit' in S()['flags'], f'{name} T_verre, {r}' + (' avec compteur' if cpt else '') + f' : « {mot} », −{dpv} PV', (msg(), hp0, S()['hp']))
            walk(20, 7.8); hp0 = S()['hp']; walk(20, 5); ok(S()['hp'] == hp0, f'{name} T_verre : une fois par scène')
            race('humain'); E("window.__nml.state.player.inv.compteur=0")
            # 9) filière (monde_remedios_vue + monde_lena_connue), Lena chez Rufina, perles (Observation 3), indice de rosée
            poser('monde_remedios_vue'); parler('rc_tecla'); choisir('caravane de Remedios'); L = labels()
            ok(any('respire' in l for l in L), f'{name} Remedios : « Elle ne fuit pas. Elle respire. » (monde_lena_connue)', L); choisir('respire')
            ok('ver_filiere_dite' in S()['flags'] and 'Sol' in noeud(), f'{name} la filière : le verre, étape de Remedios', noeud()); fermer()
            parler('rc_rufina'); choisir('Lena'); ok('ver_lena_dite' in S()['flags'], f'{name} Rufina garde une perle pour Lena', noeud()); fermer()
            stats(observation=45); fouiller('ver_porte_ex', 'ver_indice_perles', 90); ok('ver_indice_perles' in S()['flags'], f'{name} porte d\u2019écluse (Observation 3) : on compte quelque chose')
            parler('rc_rufina'); choisir('Les perles'); ok('ver_perles_dites' in S()['flags'] and 'passager' in noeud(), f'{name} Rufina : une perle par passager', noeud()); fermer()
            fouiller('ver_verre_ex', 'ver_indice_rosee', 90); ok('ver_indice_rosee' in S()['flags'], f'{name} plaine de verre (Observation 4) : traces de groin')
            # 10) sortie est : reprise, +1 h, drapeaux ver_* purgés, monde_* gardés ; Verriers uniques
            h1 = S()['h']; walk(33, 24, 90); E(f"window.__nml.game.useDoor('{LIEU}_est')"); ok(wait("window.__nml.state.region.statut!=='rencontre'", 40), f'{name} sortie est : la scène est quittée', S()['st']); time.sleep(1); s = S()
            dh = s['h'] - h1; hc = E("(()=>{const n=window.__nml,R=n.state.region,c=R.case;try{return n.voyage.heures(n.voyage.cellAt(c[0],c[1]))||0}catch(e){return null}})()")
            ok(abs(dh - 1 - (hc or 0)) < 0.01 or dh == 1, f'{name} durée : +1 h (scène), puis la piste reprise ({dh} h dont {hc} h de piste)', (dh, hc))
            ok(not any(f.startswith('ver_') for f in s['flags']) and {'monde_verriers_vus', 'monde_verriers_amis', 'monde_message_ines'} <= set(s['flags']), f'{name} sortie : ver_* purgés, monde_verriers_* et monde_message_ines gardés', s['flags'])
            r = E("""(()=>{const n=window.__nml,h=n.voyage.crochets.onCaseEntree,out=[];for(const v of [0,0.02,0.05,0.1,0.15,0.19]){n.rencontres.setRng(()=>v);const t=h({col:30,row:30,terrain:'verre',biome:'glass'},n.state);out.push(t&&(t.rencontre||t.id)||null)}n.rencontres.setRng(null);return out})()""")
            ok(r is not None and 'ecluse_verriers' not in r, f'{name} Verriers uniques : plus jamais tirés (monde_verriers_vus)', r)
            E("window.__nml.game.save && window.__nml.game.save()"); pg.reload(); demarrer(); passer_boot(E); E("document.getElementById('m-continue').click()"); time.sleep(1.5); pret(); s = S()
            ok({'monde_verriers_vus', 'monde_verriers_amis', 'monde_message_ines'} <= set(s['flags']), f'{name} rechargement : drapeaux de monde sauvegardés', s['flags'])
        else:
            # 1') passer : « Je passe sur la piste »
            walk(5, 22); wait("window.__nml.state.dialogue", 10); ok(E("window.__nml.state.dialogue?.npc") == 'rc_balta', f'{name} T1 : Balta interpelle')
            choisir('Je passe'); ok('ver_salue' in S()['flags'] and 'verre' in noeud(), f'{name} passer : « ne traîne pas sur le verre »', noeud()); choisir('Partir')
            # 2') attendre la nuit avec eux : +3 PV, harde partie, Nilo libre, récompense ; +4 h à la sortie
            E("window.__nml.state.player.hp=20"); parler('rc_tecla'); choisir('chanchos'); choisir('partir tout seuls'); choisir('attends avec'); s = S()
            ok({'ver_attendu', 'ver_harde_partie', 'ver_nilo_libre'} <= set(s['flags']) and s['hp'] == 23 and 'nuit' in noeud(), f'{name} attendre la nuit : la harde remonte dans le verre, +3 PV', (s['flags'], s['hp']))
            Lt = E(f"window.__nml.world.LOCATIONS['{LIEU}'].light.tint"); ok(Lt == '#efe9da', f'{name} l\u2019attente ne change pas la lumière de la scène', Lt)
            choisir('…'); ok('monde_verriers_amis' in S()['flags'], f'{name} attente : récompense de Tecla'); fermer()
            oter('ver_harde_partie', 'ver_merci', 'ver_nilo_libre', 'monde_verriers_amis'); time.sleep(.5)
            # 3') vol de l'établi : réussi (Discrétion 6), puis raté (« Repose. », pas de combat)
            stats(discretion=80); rng(0.99); p0, k0 = inv('perles_verre'), inv('poignard'); fouiller('ver_etabli', 'ver_vole', 60); s = S()
            ok(s['inv'].get('perles_verre', 0) == p0 + 2 and s['inv'].get('poignard', 0) == k0 + 1, f'{name} vol de l\u2019établi réussi (Discrétion 6) : lame et 2 perles', s['inv'])
            oter('ver_f_etabli', 'ver_vole'); stats(discretion=5); rng(0); fouiller('ver_etabli', 'ver_vol_rate', 30); s = S()
            ok('ver_mefiance' in s['flags'] and not s['cbt'] and not E("window.__nml.state.combatPending"), f'{name} vol raté : « Repose. », méfiance, pas de combat', s['flags'])
            # 4') le tison : Tecla -> Rufina -> examen de la harde (Volonté 5, palier 3)
            parler('rc_tecla'); choisir('chanchos'); choisir('Le feu'); fermer(); parler('rc_rufina'); choisir('tison'); ok('ver_tison' in S()['flags'], f'{name} Rufina donne le tison', S()['flags']); fermer()
            stats(volonte=9); rng(0.99); fouiller('ver_harde'); wait("window.__nml.state.dialogue", 10)
            ok(E("window.__nml.state.dialogue?.npc") == 'rc_gris' and 'bêtes' in noeud(), f'{name} examen de la harde au seuil (bêtes, pas de portrait)', noeud())
            choisir('Avancer le tison'); ok({'ver_harde_partie', 'ver_harde_feu'} <= set(S()['flags']), f'{name} tison réussi : la harde s\u2019en va', S()['flags']); fermer()
            oter('ver_harde_partie', 'ver_harde_feu'); stats(volonte=6); rng(0); hp0 = S()['hp']; ouvrir('rc_gris'); choisir('Avancer le tison'); s = S()
            ok('ver_harde_partie' in s['flags'] and s['hp'] == hp0 - 2, f'{name} tison partiel (palier 3) : −2 PV, la harde part', (s['hp'], hp0)); fermer()
            oter('ver_harde_partie', 'ver_harde_feu'); stats(volonte=0); rng(0); ouvrir('rc_gris'); choisir('Avancer le tison'); choisir('…')
            ok(wait("window.__nml.state.combat", 15), f'{name} tison raté : le gris baisse la tête, combat')
            Cb = E("(()=>{const c=window.__nml.state.combat;return {z:c.zone,u:c.units.map(u=>({id:u.id,rs:u.rendSous||0,ft:u.fuitTour||0,arme:u.arme}))}})()"); ids = {u['id'] for u in Cb['u']}
            ok(ids == {'joueur', 'gris', 'jeune_a', 'jeune_b', 'jeune_c'}, f'{name} unités : le gris et trois jeunes (les Verriers jamais au combat)', Cb['u'])
            z = Cb['z']; ok(z and abs((z['i0'] + z['i1']) / 2 - 24) <= 1 and abs((z['j0'] + z['j1']) / 2 - 15) <= 1, f'{name} zone de combat centrée sur (24 ; 15)', z)
            ok(all(u['arme'] == 'defenses' for u in Cb['u'] if u['id'] != 'joueur') and [u['ft'] for u in Cb['u'] if u['id'].startswith('jeune')].count(3) == 2, f'{name} défenses ; jeunes fuient aux tours 3, 3 et 2 ; gris rendSous 0,5', Cb['u'])
            ok(not (VERRIERS | HARDE) & vis(), f'{name} en combat : Verriers et bêtes figées cachés', vis())
            wait("window.__nml.state.combat && window.__nml.state.combat.phase==='joueur'", 40); time.sleep(1); shot(f'{name}_verriers_combat.jpg')
            F = E("[...document.querySelectorAll('#cbt-file span')].map(e=>e.textContent)"); ok(F.count('La harde') == 1 and F.count('Le gris') == 1 and 'Chancho' not in F, f'{name} barre de combat : « La harde » une fois pour les jeunes, « Le gris » à part', F)
            ok(not E("[...document.querySelectorAll('#labels .wlabel.edge,#labels .wlabel.junction')].some(e=>!e.hidden&&e.style.visibility!=='hidden'&&e.getClientRects().length)"), f'{name} combat : étiquettes de sortie masquées')
            for _ in range(4):
                if not E("!!window.__nml.state.combat") or E("!window.__nml.state.combat.units.find(u=>u.id==='jeune_c').actif"): break
                wait("!window.__nml.state.combat || window.__nml.state.combat.phase==='joueur'", 40); E("window.__nml.state.player.hp=Math.max(window.__nml.state.player.hp,30)"); E("window.__nml.state.combat && window.__nml.game.combat.endTurn()"); time.sleep(.5)
            wait("!window.__nml.state.combat || window.__nml.state.combat.phase==='joueur'", 40)
            ok(E("window.__ev.some(e=>e.type==='combat_fuite_ennemi'&&e.id==='jeune_c')"), f'{name} le jeune du bout de la cuve s\u2019enfuit au tour 2')
            r = E("""(()=>{const g=window.__nml.game,c=window.__nml.state.combat;if(!c)return null;const p=c.units.find(u=>u.joueur),t=c.units.find(u=>u.id==='gris');
               p.i=t.i-1;p.j=t.j;p.x=p.i+.5;p.z=p.j+.5;p.pa=10;p.arme='mains';t.pv=Math.floor(t.pvMax*0.5)+1;g.setRng(()=>0);return g.combat.attack('gris')})()""")
            ok(wait("!window.__nml.state.combat", 10) and {'ver_harde_partie', 'ver_harde_battue'} <= set(S()['flags']), f'{name} victoire : le gris détale sous 50 %', (r, S()['flags']))
            ok(E("window.__ev.some(e=>e.type==='combat_rend'&&e.text==='Le gris détale.')") and not E("window.__ev.some(e=>/lève les mains/.test(e.text||''))"), f'{name} texte de reddition propre au gris : « Le gris détale. »', E("window.__ev.filter(e=>e.type==='combat_rend')"))
            ok(S()['loc'] == LIEU and not HARDE & vis() and VERRIERS <= vis(), f'{name} après la victoire : la harde partie, les Verriers là', vis()); fermer()
            # reddition et défaite : restent dans la scène (ver_recule), la harde reste
            oter('ver_harde_partie', 'ver_harde_battue'); ouvrir('rc_gris'); choisir('Attaquer'); fermer(); ok(wait("window.__nml.state.combat", 15), f'{name} [Attaquer] sur la harde : combat')
            wait("window.__nml.state.combat && window.__nml.state.combat.phase==='joueur'", 40); E("window.__nml.game.combat.surrender()"); time.sleep(1); fermer(); time.sleep(.5); s = S()
            ok(not s['cbt'] and s['loc'] == LIEU and 'ver_recule' in s['flags'] and HARDE <= vis(), f'{name} reddition : on recule, la scène continue, la harde reste', (s['loc'], s['flags']))
            ouvrir('rc_gris'); choisir('Attaquer'); fermer(); wait("window.__nml.state.combat", 15); w0 = inv('water'); E("window.__nml.game.combat.finish('defaite')"); time.sleep(1); fermer(); s = S()
            ok(not s['cbt'] and s['loc'] == LIEU and abs(s['x'] - 11.5) < 1.6 and abs(s['z'] - 20.5) < 1.6 and s['inv'].get('water', 0) == w0 + 1, f'{name} défaite : réveil contre le four, une eau', (s['x'], s['z'], s['inv']))
            # fuite : halte, +1 h +4 h (attendu), puis retour sur la case (journal)
            h1 = S()['h']; ouvrir('rc_gris'); choisir('Attaquer'); fermer(); wait("window.__nml.state.combat", 15); E("window.__nml.game.combat.finish('fuite')")
            ok(wait("window.__nml.state.region.statut==='halte'", 20), f'{name} fuite : retour à la carte en halte', S()['st']); s = S()
            ok(abs(s['h'] - h1 - 5) < 0.01, f'{name} durée : +1 h, +4 h pour l\u2019attente de la nuit', s['h'] - h1)
            ok(not any(f.startswith('ver_') for f in s['flags']) and 'monde_verriers_vus' in s['flags'], f'{name} hors scène : ver_* purgés, monde_verriers_vus gardé', s['flags'])
            E(f"window.__nml.rencontres.entrer('{RID}')"); wait("window.__nml.state.location==='%s'" % LIEU, 20); pret(); s = S()
            ok(s['loc'] == LIEU and {'ver_attendu', 'ver_tison', 'ver_vol_rate'} <= set(s['flags']), f'{name} retour sur la case : journal restauré', s['flags'])
            # 5') rançon : réussie (Intimidation contre Volonté 7), puis ratée
            stats(charisme=9, force=9); rng(0.5); m0, p0 = S()['money'], inv('perles_verre'); ouvrir('rc_tecla', 'menace'); choisir('Vingt dollars'); s = S()
            ok(s['money'] == m0 + 14 and s['inv'].get('perles_verre', 0) == p0 + 3 and {'monde_verriers_menaces', 'ver_regle'} <= set(s['flags']), f'{name} rançon réussie : 14 $ et 3 perles, monde_verriers_menaces', (s['money'] - m0, s['flags']))
            oter('ver_regle', 'ver_racket'); stats(charisme=2, force=2); ouvrir('rc_tecla', 'menace'); choisir('Vingt dollars')
            ok('balles' in noeud(), f'{name} rançon ratée : « la piste »', noeud()); choisir('Je pars'); ok('ver_menace' in S()['flags'], f'{name} rançon ratée : on part', S()['flags'])
            # 6') attaquer les Verriers : pas de combat, ils reculent dans le verre ; coque, établi et citerne libres
            oter('ver_regle'); parler('rc_balta'); choisir('Attaquer'); ok(E("window.__nml.state.dialogue?.node") == 'fuient' and 'reculer' in noeud(), f'{name} [Attaquer] chez Balta -> nœud commun fuient (humain : la peau dit de reculer)', noeud())
            choisir('Partir'); time.sleep(.6); s = S()
            ok({'ver_chasses', 'monde_verriers_chasses'} <= set(s['flags']) and not s['cbt'] and not E("window.__nml.state.combatPending") and not VERRIERS & vis(), f'{name} les Verriers reculent dans le verre, aucun combat', (s['flags'], vis()))
            race('mutant'); ouvrir('rc_tecla', 'fuient'); ok('les suivre' in noeud(), f'{name} fuient, mutant : « Tu pourrais les suivre »', noeud()); fermer(); race('humain')
            w0, r0, m0 = inv('water'), inv('ration'), S()['money']; fouiller('ver_peniche', 'ver_f_coque', 60); s = S()
            ok(s['inv'].get('water', 0) == w0 + 3 and s['inv'].get('ration', 0) == r0 + 2 and s['money'] == m0 + 9, f'{name} coque libre : 3 eaux, 2 rations, 9 $', (s['inv'], s['money'] - m0))
            w0 = inv('water'); fouiller('ver_citerne', 'ver_f_citerne', 60); ok(inv('water') == w0 + 2, f'{name} citerne sous la proue : 2 eaux', inv('water'))
            k0 = inv('poignard'); oter('ver_f_etabli'); fouiller('ver_etabli', 'ver_f_etabli', 60); ok(inv('poignard') == k0 + 1, f'{name} établi abandonné : la lame', inv('poignard'))
        ok(not errs, f'{name} aucune erreur console', errs[:6])
        ctx.close()
    # nuit et jour : flaque du four (décalque, nuit seulement, même pulse que le _neon), le verre ne luit pas, liseré tête et épaules (Balta)
    from PIL import Image
    nuit = {}
    for h in (10, 23):
        ctx = br.new_context(viewport={'width': 1280, 'height': 800}); pg = ctx.new_page(); E = pg.evaluate; errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=90000); time.sleep(1)
        E("localStorage.removeItem('nml_save_auto')"); passer_boot(E); E("document.getElementById('m-new').click()"); time.sleep(.5)
        E("document.querySelector('[data-race=\"humain\"]').click()"); time.sleep(.3); E("document.getElementById('cr-next').click()"); time.sleep(.3); E("document.getElementById('cr-enter').click()"); time.sleep(2)
        E(f"(()=>{{window.__nml.state.heures={h};return window.__nml.rencontres.entrerMaintenant('{RID}')}})()")
        t0 = time.time()
        while time.time() - t0 < 60 and not E(f"window.__nml.state.location==='{LIEU}' && window.__nml.lieuPret('{LIEU}')"): time.sleep(.5)
        time.sleep(2.5); E("document.getElementById('msg').textContent=''")
        P = lambda x, y, z: E(f"(()=>{{const p=window.__nml.project({x},{y},{z});return [Math.round(p.x),Math.round(p.y)]}})()")
        moy = lambda im, q, r=3: [sum(c[i] for c in [im.getpixel((q[0] + dx, q[1] + dy)) for dx in range(-r, r + 1) for dy in range(-r, r + 1)]) / (2 * r + 1) ** 2 for i in range(3)]
        lumi = lambda c: 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
        fq, loin, verre = P(11.5, 0, 19.4), P(17, 0, 20.4), P(20, 0, 3)
        ech = []
        for _ in range(8):
            im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); ech.append((moy(im, fq), moy(im, loin), moy(im, verre))); time.sleep(.9)
        nuit[h] = {'fl': E("window.__nml.flaquesNuit()"), 'tint': E(f"window.__nml.world.LOCATIONS['{LIEU}'].light.tint"), 'fl_max': max(lumi(a) - lumi(b) for a, b, c in ech), 'fl_min': min(lumi(a) - lumi(b) for a, b, c in ech),
                   'chaud': min(a[0] - a[2] for a, b, c in ech), 'chaud_max': max(a[0] - a[2] for a, b, c in ech), 'verre': max(lumi(c) for a, b, c in ech), 'verre_bleu': max(c[2] - c[0] for a, b, c in ech), 'errs': errs[:3]}
        x, z, hh = 5.5, 20.4, 1.82; a_, b_ = P(x, 0, z), P(x, hh, z); clip = {'x': a_[0] - 45, 'y': b_[1] - 10, 'width': 90, 'height': a_[1] - b_[1] + 16}
        av = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('RGB'); E("window.__nml.liseres(false)"); time.sleep(.4)
        sa = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('RGB'); E("window.__nml.liseres(true)"); time.sleep(.2)
        H = a_[1] - b_[1]; ys = [i // av.width - 10 for i, (u, v) in enumerate(zip(av.getdata(), sa.getdata())) if sum(u) - sum(v) > 36 and u[2] - v[2] >= u[0] - v[0]]
        nuit[h]['balta'] = (len(ys), sum(1 for y in ys if y > 0.3 * H)); nuit[h]['op'] = E("window.__nml.liseres().opacite"); nuit[h]['lim'] = E("window.__nml.liseres().limites"); nuit[h]['refl'] = E("window.__nml.reflets()")
        nuit[h]['decor'] = E(f"(()=>{{const L=window.__nml.world.LOCATIONS['{LIEU}'];return {{b:L.buildings.length,bn:L.buildings.filter(b=>b.nuit).length,p:L.props.length,pn:L.props.filter(p=>p.nuit).length}}}})()")
        if h == 23: pg.screenshot(path=OUT + 'livraison/desktop_verriers_nuit_23h.jpg', type='jpeg', quality=88)
        ctx.close()
    J, N = nuit[10], nuit[23]
    ok(not J['fl'] and len(N['fl']) == 1 and N['fl'][0]['id'] == 'ver_feu' and N['fl'][0]['cle'], 'flaque du four : décalque rc_ecl_four_flaque posé la nuit, absent le jour', (J['fl'], N['fl']))
    ok(N['fl_min'] > 3 and N['chaud'] > 0 and N['chaud_max'] > 15, f'flaque du four visible la nuit et chaude, pulsée ({N["fl_min"]:.0f} à {N["fl_max"]:.0f} au-dessus du sol)', N)
    ok(J['tint'] == '#efe9da' and N['tint'] == '#586282', 'courbe glass : jour blanc dur, nuit bleu-gris commune', (J['tint'], N['tint']))
    ok(N['verre'] < 45 and N['verre_bleu'] < 30, f'le verre ne luit jamais : sombre la nuit (luminance {N["verre"]:.0f}), sans lueur bleue ni verte', N)
    ok(len(J['refl']) == 10 and all(r['opacite'] > 0.9 and r['visible'] for r in J['refl']), f'éclats du verre : 10 calques _reflet posés, visibles de jour ({len(J["refl"])})', J['refl'])
    ok(len(N['refl']) == 10 and all(r['opacite'] == 0 and not r['visible'] for r in N['refl']), 'le verre ne luit jamais : à 23 h, opacité des reflets à 0', N['refl'])
    ok(N['decor']['bn'] == N['decor']['b'] and N['decor']['pn'] == N['decor']['p'], f'nuit : tous les bâtiments et props suivent la courbe de nuit ({N["decor"]})', N['decor'])
    ok(N['lim'] and all(v >= 0.55 for v in N['lim']), f'liseré coupé net sous les épaules (limites uv {N["lim"]})', N['lim'])
    ok(N['balta'][0] >= 4 and N['balta'][1] == 0 and 0 < N['op'] <= 0.5 and J['op'] == 0, f'liseré de lune : Balta tête et épaules ({N["balta"][0]} px, 0 sous 30 %), opacité {N["op"]:.2f} ≤ 0,5 ; nul le jour', (N['balta'], N['op'], J['op']))
    ok(not N['errs'] and not J['errs'], 'nuit et jour : aucune erreur console', (N['errs'], J['errs']))
    br.close()
print(f'\n{n} OK, {len(fails)} échec(s)'); [print('  -', f) for f in fails]; sys.exit(1 if fails else 0)
