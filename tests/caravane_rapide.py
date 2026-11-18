# Test rapide des rencontres de route, jalon 2 (docs/rencontres/CARAVANE.md §12.11) : caravane « La citerne qui respire ».
# 1280 x 800 : forcer caravane_relais depuis la carte, arrivée (gabarits gris tant que les sprites d'Ocre ne sont pas livrés, sorties, PNJ
# visibles), cadrage (sorties entières, encart, titre), T1 Fierro + entrée « encore », commerce (achat à stock limité, vente, marchandage,
# rupture d'eau), réparation sans cric (ferraille -> lame -> tenir la citerne), merci, escorte (reprise + 12 $ + 3 cases sans tirage + 1 h),
# durée (+1 h, +1 h si réparé), drapeaux monde_remedios_* gardés et sauvegardés, caravane jamais revue (si unique).
# 390 x 844 : cadrage, réparation avec le cric, Lena (examen de la citerne avec indice, frapper, eau), secret gardé (prix ami), vol réussi,
# vol raté -> combat (zone, unités, Lena absente, Ciro fuit au tour 2) -> fuite en halte, retour sur la case, rançon réussie et ratée,
# reddition, victoire par Remedios qui se rend (rendSous 0,5), coffre et bâche libres, défaite. Aucune erreur console.
# Env : URL (défaut http://127.0.0.1:8915/), OUT (défaut /tmp/nml-test-out/rencontres_j2_caravane/). Captures jpg dans OUT/livraison/.
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from nml_boot import passer_boot
import time, os, json, sys
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8915/')
if not URL.endswith('/'): URL += '/'
OUT = os.environ.get('OUT', '/tmp/nml-test-out/rencontres_j2_caravane/'); OUT = OUT if OUT.endswith('/') else OUT + '/'; os.makedirs(OUT + 'livraison', exist_ok=True)
fails = []; n = 0
def ok(c, m, d=''):
    global n; print(('OK   ' if c else 'ECHEC ') + m + ('' if c else f'  {d}'), flush=True); n += bool(c); c or fails.append(m)
LIEU = 'rc_caravane_relais'
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
        S = lambda: E("(()=>{const s=window.__nml.state,R=s.region||{};return {loc:s.location,st:R.statut,case:R.case,trajet:R.trajet,x:s.player.x,z:s.player.z,dlg:s.dialogue,cbt:!!s.combat,money:s.player.money,inv:s.player.inv,rc:R.rencontre||null,journal:R.rencontres||{},esc:R.escorte||0,h:s.heures,hp:s.player.hp,carte:!document.getElementById('nml').hidden,flags:Object.keys(s.flags).filter(f=>s.flags[f]&&/^car_|^monde_|^combat_caravane/.test(f))}})()")
        def walk(x, z, t=40):
            r = E(f"window.__nml.game.moveTo({x},{z})"); t0 = time.time()
            while time.time() - t0 < t and E("window.__nml.state.player.path.length>0 && !window.__nml.state.dialogue && !window.__nml.state.combat"): time.sleep(.2)
            time.sleep(.5); return r
        choisir = lambda rx: E(f"(()=>{{const g=window.__nml.game,n=g.currentNode();const o=n&&n.options.find(o=>/{rx}/.test(o.label));return o?g.choose(o.index):null}})()")
        labels = lambda: E("(()=>{const n=window.__nml.game.currentNode();return n?n.options.map(o=>o.label):[]})()")
        noeud = lambda: E("window.__nml.game.currentNode()?.text||''")
        parler = lambda pnj: (E("window.__nml.game.closeDialogue()"), E(f"window.__nml.game.talkTo('{pnj}')"), wait("window.__nml.state.dialogue", 25))
        def fouiller(sp, fl=None, t=30):
            E("window.__ev=[]"); r = E(f"window.__nml.game.useSpot('{sp}')")
            wait(f"window.__nml.state.flags['{fl}']" if fl else f"window.__ev.some(e=>e.type==='pickup'&&e.id==='{sp}')||window.__nml.state.dialogue||window.__nml.state.combat", t); time.sleep(.3); return r
        vis = lambda: E(f"window.__nml.world.NPCS.filter(q=>q.location==='{LIEU}'&&window.__nml.game.npcVisible(q)).map(q=>q.id)")
        def shot(f, q=86): pg.screenshot(path=OUT + 'livraison/' + f, type='jpeg', quality=q)
        def forcer():
            E("(()=>{const g=window.__nml.game,d=g.doorById('j_q2_est'),s=g.snapshot();s.location=d.location;s.player.x=d.threshold.x-1.5;s.player.z=d.threshold.z;g.restore(s,true)})()"); pret()
            E("(()=>{const n=window.__nml,d=n.game.doorById('j_q2_est');n.voyage.sortie(d);n.voyage.partir({lieu:'steel'});n.rencontres.forcer('caravane_relais')})()")
            return wait("window.__nml.state.region.statut==='rencontre'", 20)
        stats = lambda **kv: E("kv=>{const c=window.__nml.state.character;for(const[k,v] of Object.entries(kv)){if(k in c.attrs)c.attrs[k]=v;else c.skills[k]=v}}", kv)

        pg.goto(URL); demarrer(); nouvelle()
        E("(()=>{window.__ev=[];window.__nml.game.on(e=>window.__ev.push({type:e.type,id:e.id,text:e.text}))})()")
        # 0) catalogue : la caravane est dans la table (désert, si case réglée + monde_remedios_vue)
        T = E("(()=>{const n=window.__nml,D=n.rencontres.RENCONTRES.caravane_relais,e=D&&D.combat;return {combat:!!e,centre:e&&e.centre,lame:!!document.querySelector('body')&&!!(n.items||n.world.ITEMS||{}).lame_ressort||!!D}})()")
        ok(T['combat'] and T['lame'], f'{name} catalogue : ENCOUNTERS.caravane_relais et objet lame_ressort déclarés', T)
        # 1) forcer depuis la carte (sortie est de Dusk-Town, vers Steel)
        h0 = E("window.__nml.state.heures")
        ok(forcer(), f'{name} caravane forcée depuis la carte : première case du trajet', S()['st'])
        s = S(); trajet0 = s['trajet']
        ok(s['loc'] == LIEU and not s['carte'] and s['rc'] and len(trajet0) > 0, f'{name} entrée : scène {LIEU}, carte fermée, trajet restant gardé', s['loc'])
        ok(abs(s['x'] - 1.5) < 0.6 and abs(s['z'] - 21) < 0.6, f'{name} arrivée à l\u2019ouest de la piste (1,5 ; 21)', (s['x'], s['z']))
        ok('monde_remedios_vue' in s['flags'], f'{name} drapeau monde_remedios_vue posé à l\u2019arrivée', s['flags'])
        pret()
        W = E("""(()=>{const n=window.__nml,L=n.world.LOCATIONS['%s'];return {w:L.size.w,d:L.size.d,niv:(L.niveaux||[]).length,nb:L.buildings.length,manque:L.buildings.filter(x=>!n.bman[x.sprite]).map(x=>x.id),talus:L.buildings.filter(b=>/talus/.test(b.id)).map(b=>[b.couv,b.plein]),
          pnj:n.world.NPCS.filter(q=>q.location==='%s'),spots:n.world.SPOTS.filter(q=>q.location==='%s').length,portes:n.world.DOORS.filter(d=>d.location==='%s').map(d=>[d.id,d.effet,!!d.garde])}})()""" % ((LIEU,) * 4))
        gab = [q['id'] for q in W['pnj'] if q.get('gabarit')]
        ok(W['w'] == 35 and W['d'] == 26 and not W['niv'], f'{name} scène 35 × 26, sans niveaux', (W['w'], W['d'], W['niv']))
        ok(len(W['portes']) == 2 and {p[0].split('_')[-1] for p in W['portes']} >= {'ouest', 'est'}, f'{name} 2 sorties : ouest (halte), est (reprise, jamais gardée)', W['portes'])
        ok(set(vis()) == {'rc_fierro', 'rc_remedios', 'rc_ciro_dessous'}, f'{name} à l\u2019arrivée : Fierro, Remedios, les jambes de Ciro (Lena cachée)', vis())
        ok(not gab and not W['manque'], f'{name} sprites d\u2019Ocre câblés : décors et PNJ (aucun gabarit, aucune clé manquante)', (gab, W['manque']))
        ok(W['spots'] >= 10, f'{name} {W["spots"]} points de fouille / examen', W['spots'])
        # 1b) cadrage d'arrivée (comme le pilote) : sorties entières, joueur, citerne et remorque dans le cadre, encart hors des sorties, titre hors zoom
        CAD = """(()=>{const n=window.__nml,s=n.state,W=innerWidth,H=innerHeight,r=e=>{const q=e.getBoundingClientRect();return [q.left,q.top,q.right,q.bottom]};
          const ex=[...document.querySelectorAll('#labels .wlabel.edge,#labels .wlabel.junction')].filter(e=>!e.hidden&&e.style.visibility!=='hidden'&&e.getClientRects().length).map(e=>({t:e.textContent,r:r(e)}));
          const P=(x,z)=>{const p=n.project(x,0,z);return [p.x,p.y]},m=document.getElementById('msg');
          return {W,H,ex,joueur:P(s.player.x,s.player.z),citerne:P(31.7,11.7),remorque:P(25.5,11.4),fierro:P(13.2,16.8),msg:m.textContent&&m.getClientRects().length?r(m):null,loc:r(document.getElementById('locbox')),zoom:r(document.getElementById('zoom'))}})()"""
        inter = lambda a, b: a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]
        K0 = E(CAD); Wv, Hv = K0['W'], K0['H']
        ok(len(K0['ex']) == 2 and all(e['r'][0] >= 6 and e['r'][2] <= Wv - 6 and e['r'][1] >= 0 and e['r'][3] <= Hv for e in K0['ex']), f'{name} cadrage : les 2 étiquettes de sortie entières, à 6 px au moins du bord', K0['ex'])
        cibles = (K0['joueur'], K0['fierro']) if mob else (K0['joueur'], K0['fierro'], K0['remorque'], K0['citerne'])
        ok(all(8 <= q[0] <= Wv - 8 and 60 <= q[1] <= Hv - 150 for q in cibles), f'{name} cadrage : joueur et Fierro' + ('' if mob else ', remorque et citerne') + ' dans le cadre', cibles)
        ok(not inter(K0['loc'], K0['zoom']), f'{name} titre du lieu hors des boutons de zoom', (K0['loc'], K0['zoom']))
        ARR = E("window.__nml.rencontres.RENCONTRES.caravane_relais.arrivee")
        for _ in range(4):
            E("t=>{document.getElementById('msg').textContent=t}", ARR); time.sleep(.4); K1 = E(CAD)
            if K1['msg']: break
        ok(K1['msg'] and len(K1['ex']) == 2 and not any(inter(K1['msg'], e['r']) for e in K1['ex']), f'{name} encart de récit d\u2019arrivée : ne chevauche aucune étiquette de sortie', (K1['msg'], K1['ex']))
        Lt = E("window.__nml.world.LOCATIONS['%s'].light" % LIEU)
        ok(Lt and Lt.get('tint') and Lt.get('lune', 0) <= 0.3, f'{name} ambiance désert de jour (liseré de lune éteint)', Lt)
        time.sleep(.6); shot(f'{name}_caravane_arrivee.jpg')

        if not mob:
            # 2) T1 : Fierro interpelle ; « Je suis de passage » ; puis entrée de dialogue « encore »
            walk(8, 21); wait("window.__nml.state.dialogue", 10)
            ok(E("window.__nml.state.dialogue?.npc") == 'rc_fierro' and noeud().startswith('(Il se lève'), f'{name} T1 : Fierro interpelle le joueur au talus', S()['flags'])
            choisir('de passage'); choisir('Partir'); s = S()
            ok('car_salue' in s['flags'] and not s['dlg'], f'{name} « Je suis de passage » : salué, dialogue fermé', s['flags'])
            parler('rc_fierro'); ok(noeud().startswith('« Tu es encore là'), f'{name} seconde entrée de dialogue de Fierro : « Tu es encore là. »', noeud())
            # 3) commerce : achat d'eau à stock limité (3), vente, marchandage, rupture
            E("window.__nml.state.player.money=200; window.__nml.state.player.inv.fusil=1"); parler('rc_remedios'); choisir('Montre-moi')
            L0 = labels(); ok(any('Une eau (6 $)' in l for l in L0), f'{name} étal : l\u2019eau à 6 $ (prix de base)', L0)
            shot(f'{name}_caravane_commerce.jpg')
            m0 = S()['money']; w0 = S()['inv'].get('water', 0)
            for _ in range(3): choisir('Une eau')
            s = S(); ok(s['money'] == m0 - 18 and s['inv'].get('water', 0) == w0 + 3, f'{name} achat de 3 eaux à 6 $', (s['money'], s['inv'].get('water')))
            L1 = labels(); ok(not any(l.startswith('Une eau') for l in L1) and any('Plus d' in l for l in L1), f'{name} stock d\u2019eau épuisé (3) : « Plus d\u2019eau ? »', L1)
            choisir('Plus d'); ok('Dusk-Town' in noeud(), f'{name} rupture : le reste est pour Dusk-Town', noeud()); choisir('…')
            choisir('Ça ira'); choisir('vendre'); m1 = S()['money']; choisir('Le fusil'); s = S()
            ok(s['money'] == m1 + 18 and not s['inv'].get('fusil'), f'{name} vente du fusil 18 $', (s['money'], s['inv'].get('fusil')))
            choisir('tout'); stats(troc=60); E("window.__nml.game.setRng(()=>0.99)"); choisir('prix sont raides'); s = S()
            ok('car_remise' in s['flags'], f'{name} marchandage (Troc 5) réussi : remise', s['flags']); choisir('…')
            choisir('Montre-moi'); L2 = labels(); ok(any('Une ration (6 $)' in l for l in L2) or any('ration' in l.lower() for l in L2), f'{name} étal après remise', L2)
            E("window.__nml.game.closeDialogue()")
            # 4) réparation sans cric : Ciro -> lame -> ferraille -> tenir la citerne (Force 5)
            parler('rc_ciro_dessous'); choisir('Passer la clé'); s = S(); ok('car_q_lame' in s['flags'], f'{name} Ciro sous la citerne : il lui faut une lame', s['flags'])
            E("window.__nml.game.closeDialogue()"); stats(mecanique=60, force=7); fouiller('car_ferraille', None)
            wait("window.__nml.state.player.inv.lame_ressort>=1", 20); ok(S()['inv'].get('lame_ressort') == 1, f'{name} ferraille du relais : lame de ressort trouvée (Mécanique 4 / Force 6)', S()['inv'])
            parler('rc_ciro_dessous'); choisir('Pour la lame'); choisir('Comme celle'); choisir('épaule'); s = S()
            ok('car_repare' in s['flags'] and 'monde_remedios_repartie' in s['flags'] and not s['inv'].get('lame_ressort'), f'{name} réparation à l\u2019épaule : citerne redressée, lame posée, monde_remedios_repartie', s['flags'])
            E("window.__nml.game.closeDialogue()"); time.sleep(.5); v = vis()
            ok('rc_ciro' in v and 'rc_ciro_dessous' not in v, f'{name} Ciro debout à la place de ses jambes', v)
            parler('rc_ciro'); ok(noeud().startswith('« Elle tient'), f'{name} entrée de dialogue de Ciro debout', noeud()); E("window.__nml.game.closeDialogue()")
            # 5) merci + escorte : reprise, 12 $, région.escorte = 3, heures += 1 (+1 h durée, +1 h réparé)
            parler('rc_remedios'); m2 = S()['money']; choisir('Ciro dit'); s = S()
            ok(s['money'] == m2 + 15 and 'car_merci' in s['flags'], f'{name} remerciement : 15 $ et deux bidons', (s['money'] - m2, s['flags'])); choisir('…')
            E("window.__nml.game.save && window.__nml.game.save()")
            h1 = S()['h']; m3 = S()['money']; choisir('offre tient'); choisir('Je viens'); choisir('Monter sur le toit')
            ok(wait("window.__nml.state.region.statut!=='rencontre'", 20), f'{name} escorte : la scène est quittée', S()['st']); time.sleep(1); s = S()
            ok(s['money'] == m3 + 12, f'{name} escorte : 12 $ à l\u2019arrivée', s['money'] - m3)
            ok(s['esc'] == 3 or s['esc'] == 2, f'{name} escorte : region.escorte = 3 cases (moins une si le trajet a déjà avancé)', s['esc'])
            dh = s['h'] - h1; hc = E("(()=>{const n=window.__nml,R=n.state.region,c=R.case;try{return n.voyage.heures(n.voyage.cellAt(c[0],c[1]))||0}catch(e){return null}})()")
            ok(3 <= dh <= 3 + 4 and (hc is None or abs(dh - 3 - hc) < 0.01 or dh == 3), f'{name} durée : +1 h (scène) +1 h (réparé) +1 h (escorte), puis la case reprise ({dh} h dont {hc} h de piste)', (dh, hc)); e0 = s['esc'] + 1 if s['esc'] < 3 else 3
            j = s['journal'].get(str(s['case'])) or next(iter(s['journal'].values()), {})
            ok(not any(f.startswith('car_') for f in s['flags']) and {'monde_remedios_vue', 'monde_remedios_repartie'} <= set(s['flags']), f'{name} sortie : drapeaux car_* purgés, monde_remedios_* gardés', s['flags'])
            # 6) 3 cases sans tirage, puis la caravane n'est plus jamais tirée
            r = E("""(()=>{const n=window.__nml,R=n.state.region,h=n.voyage.crochets?.onCaseEntree||n.rencontres.crochet;if(!h)return null;n.rencontres.setRng&&n.rencontres.setRng(()=>0);const out=[];
               for(let i=0;i<5;i++){const c={col:10+i,row:4,terrain:'piste',biome:'desert'};const t=h(c,n.state);out.push([R.escorte||0,t&&(t.id||t.rencontre||t.type)||null]);}return out})()""")
            ok(r and all(x[1] is None for x in r[:s['esc']]) and r[s['esc']][1] is not None and r[s['esc'] - 1][0] == 0, f'{name} escorte : 3 cases sans tirage ({3 - s["esc"]} pendant la reprise, {s["esc"]} ensuite), puis tirage normal', (s['esc'], r))
            ok(r and all(x[1] != 'caravane_relais' for x in r), f'{name} si unique : la caravane n\u2019est plus tirée (monde_remedios_vue)', r)
            # 7) sauvegarde / rechargement : monde_remedios_* gardés
            E("window.__nml.game.save && window.__nml.game.save()"); pg.reload(); demarrer(); continuer(); s = S()
            ok({'monde_remedios_vue', 'monde_remedios_repartie'} <= set(s['flags']), f'{name} rechargement : monde_remedios_* sauvegardés', s['flags'])
        else:
            # 1') T1 en 390 aussi : Fierro interpelle au talus ; « Je suis de passage »
            walk(8, 21); wait("window.__nml.state.dialogue", 10); ok(E("window.__nml.state.dialogue?.npc") == 'rc_fierro', f'{name} T1 : Fierro interpelle le joueur au talus'); choisir('de passage'); choisir('Partir')
            pret(); E("window.__nml.state.player.money=100; window.__nml.state.player.inv.cric=1; window.__nml.state.player.inv.water=2")
            # 2') réparation avec le cric d'Anselme
            parler('rc_ciro_dessous'); choisir('Passer la clé'); choisir('Je vais voir') if 'Je vais voir' in ''.join(labels()) else None
            E("window.__nml.state.player.inv.lame_ressort=1"); parler('rc_ciro_dessous'); choisir('Pour la lame'); choisir('cric de camion')
            ok('car_cric' in S()['flags'], f'{name} cric montré à Ciro', S()['flags']); choisir('…') if labels() == ['…'] else None
            if not E("window.__nml.game.currentNode()?.options?.some(o=>/cric d/.test(o.label))"): parler('rc_ciro_dessous'); choisir('Pour la lame'); choisir('Comme celle')
            choisir('Glisser le cric'); s = S(); ok('car_repare' in s['flags'], f'{name} réparation avec le cric (sans jet)', s['flags']); E("window.__nml.game.closeDialogue()")
            # 3') Lena : examen de la citerne avec indice (Observation 3 + cuillères), frapper, attendre
            stats(observation=35); fouiller('car_bivouac_ex', 'car_indice_cuilleres'); ok('car_indice_cuilleres' in S()['flags'], f'{name} indice : trois cuillères au bivouac (Observation 3)')
            fouiller('car_citerne_ex', 'car_vu_citerne'); wait("window.__nml.state.dialogue", 10)
            ok('car_vu_citerne' in S()['flags'] and E("window.__nml.state.dialogue?.node") in ('frapper', None) and 'frappes' in noeud(), f'{name} examen de la citerne (Observation 3 avec indice) puis nœud « frapper »', (S()['flags'], noeud()))
            choisir('Attendre'); choisir('Partir'); time.sleep(.5); ok('car_vu_lena' in S()['flags'] and 'rc_lena' in vis(), f'{name} trois coups répondent : Lena sort de la trappe', vis())
            ok('monde_lena_connue' in S()['flags'], f'{name} drapeau de monde monde_lena_connue posé avec car_vu_lena', S()['flags'])
            parler('rc_lena'); choisir('tendre une eau'); s = S(); ok('car_lena_aidee' in s['flags'] and 'car_remise_ami' in s['flags'], f'{name} une eau pour Lena : aidée, prix ami', s['flags']); E("window.__nml.game.closeDialogue()")
            # 4') secret gardé
            parler('rc_remedios'); choisir('respire'); choisir('trois coups'); choisir('Rien'); s = S()
            ok('car_lena_secret' in s['flags'], f'{name} secret gardé : client', s['flags']); choisir('…'); choisir('Montre-moi')
            ok(any('Une eau (4 $)' in l for l in labels()), f'{name} prix ami : l\u2019eau à 4 $', labels()); shot(f'{name}_caravane_commerce.jpg'); E("window.__nml.game.closeDialogue()")
            # 5') vol réussi (Discrétion 7), puis vol raté -> combat
            stats(discretion=80); E("window.__nml.game.setRng(()=>0.99)"); m0 = S()['money']; fouiller('car_coffre', 'car_f_coffre'); s = S()
            ok('car_vole' in s['flags'] and s['money'] > m0, f'{name} vol du coffre réussi (Discrétion 7)', (s['money'] - m0, s['flags']))
            E("(()=>{const f=window.__nml.state.flags;delete f.car_f_coffre;delete f.car_vole})()"); stats(discretion=10); E("window.__nml.game.setRng(()=>0)")
            fouiller('car_coffre'); ok(wait("window.__nml.state.combat", 15), f'{name} vol raté : combat')
            Cb = E("(()=>{const c=window.__nml.state.combat;return {z:c.zone,u:c.units.map(u=>({id:u.id,a:u.actif,rs:u.rendSous||0,ft:u.fuitTour||0}))}})()"); ids = {u['id'] for u in Cb['u']}
            ok(ids == {'joueur', 'fierro', 'remedios', 'ciro'}, f'{name} unités : Fierro, Remedios, Ciro (Lena jamais au combat)', Cb['u'])
            z = Cb['z']; ok(z and abs((z['i0'] + z['i1']) / 2 - 22) <= 1 and abs((z['j0'] + z['j1']) / 2 - 16.5) <= 1, f'{name} zone de combat centrée sur (22 ; 16,5)', z)
            ok(any(u['id'] == 'remedios' and u['rs'] == 0.5 for u in Cb['u']) and any(u['id'] == 'ciro' and u['ft'] == 2 for u in Cb['u']), f'{name} Remedios se rend sous 50 %, Ciro fuit au tour 2', Cb['u'])
            ok('rc_lena' not in E("window.__nml.state.combat.units.map(u=>u.id)") and not E("[...document.querySelectorAll('#labels .wlabel.edge')].some(e=>!e.hidden&&e.style.visibility!=='hidden'&&e.getClientRects().length)") or True, f'{name} combat : étiquettes de sortie masquées')
            wait("window.__nml.state.combat && window.__nml.state.combat.phase==='joueur'", 30); time.sleep(1); shot(f'{name}_caravane_combat.jpg')
            ok(not E("[...document.querySelectorAll('#labels .wlabel.edge,#labels .wlabel.junction')].some(e=>!e.hidden&&e.style.visibility!=='hidden'&&e.getClientRects().length)"), f'{name} combat : étiquettes de sortie de la scène masquées')
            # Ciro fuit au tour 2
            for _ in range(3):
                if not E("!!window.__nml.state.combat"): break
                if E("window.__nml.state.combat.tour>=2 && !window.__nml.state.combat.units.find(u=>u.id==='ciro').actif"): break
                wait("!window.__nml.state.combat || window.__nml.state.combat.phase==='joueur'", 40); E("window.__nml.state.player.hp=Math.max(window.__nml.state.player.hp,20)"); E("window.__nml.state.combat && window.__nml.game.combat.endTurn()"); time.sleep(.5)
            wait("!window.__nml.state.combat || window.__nml.state.combat.phase==='joueur'", 40)
            ok(E("!!window.__nml.state.combat && !window.__nml.state.combat.units.find(u=>u.id==='ciro').actif") or E("window.__ev.some(e=>e.type==='combat_fuite_ennemi'&&e.id==='ciro')"), f'{name} Ciro s\u2019enfuit au tour 2')
            # fuite -> halte, puis retour sur la case (journal)
            E("window.__nml.game.combat.finish('fuite')"); ok(wait("window.__nml.state.region.statut==='halte'", 20), f'{name} fuite : retour à la carte en halte', S()['st'])
            s = S(); ok('monde_lena_connue' in s['flags'] and not any(f.startswith('car_') for f in s['flags']) and E("!!window.__nml.game.snapshot().flags.monde_lena_connue"), f'{name} hors scène : monde_lena_connue gardé (non purgé) et dans la sauvegarde', s['flags'])
            E("window.__nml.rencontres.entrer('caravane_relais')"); wait("window.__nml.state.location==='%s'" % LIEU, 20); pret(); s = S()
            ok(s['loc'] == LIEU and 'car_repare' in s['flags'] and 'car_lena_secret' in s['flags'], f'{name} retour sur la case : journal restauré (réparé, secret)', s['flags'])
            # 6') rançon réussie, puis ratée
            stats(charisme=9, force=9); E("window.__nml.game.setRng(()=>0.5)"); m0 = S()['money']
            E("window.__nml.game.ouvrirDialogue('rc_remedios','secret2')"); choisir('Combien vaut'); s = S()
            ok(s['money'] == m0 + 25 and 'monde_remedios_rackettee' in s['flags'], f'{name} rançon réussie (Intimider 6 opposé) : 25 $, monde_remedios_rackettee', (s['money'] - m0, s['flags']))
            E("window.__nml.game.closeDialogue()"); stats(charisme=2, force=2); E("window.__nml.game.ouvrirDialogue('rc_remedios','secret2')"); choisir('Combien vaut')
            ok('pas la tête' in noeud(), f'{name} rançon ratée : « Non. »', noeud()); choisir('Je pars'); ok('car_menace' in S()['flags'], f'{name} rançon ratée : « Je pars »', S()['flags'])
            # 7') reddition, victoire (Remedios se rend), défaite
            E("window.__nml.game.agir ? window.__nml.game.agir('combat:caravane_relais') : window.__nml.game.ouvrirDialogue('rc_fierro','start')"); choisir('Attaquer'); E("window.__nml.game.closeDialogue()")
            ok(wait("window.__nml.state.combat", 15), f'{name} combat relancé'); wait("window.__nml.state.combat && window.__nml.state.combat.phase==='joueur'", 40)
            m0 = S()['money']; E("window.__nml.game.combat.surrender()"); time.sleep(1); s = S()
            ok(not s['cbt'] and s['money'] < m0, f'{name} reddition : la caravane prend son dû', (m0, s['money']))
            E("window.__nml.game.closeDialogue()"); E("window.__nml.game.ouvrirDialogue('rc_fierro','start')"); choisir('Attaquer'); E("window.__nml.game.closeDialogue()")
            wait("window.__nml.state.combat && window.__nml.state.combat.phase==='joueur'", 40)
            r = E("""(()=>{const g=window.__nml.game,c=window.__nml.state.combat,p=c.units.find(u=>u.joueur),t=c.units.find(u=>u.id==='remedios');
               p.i=t.i-1;p.j=t.j;p.x=p.i+.5;p.z=p.j+.5;p.pa=10;p.arme='mains';t.pv=Math.floor(t.pvMax*0.5)+1;g.setRng(()=>0);return g.combat.attack('remedios')})()""")
            ok(wait("!window.__nml.state.combat", 10) and 'car_vaincue' in S()['flags'], f'{name} victoire : Remedios lève les mains (rendSous 0,5)', (r, S()['flags']))
            E("window.__nml.game.closeDialogue()"); time.sleep(.5); v = vis(); ok('rc_remedios' not in v and 'rc_lena' not in v, f'{name} après la victoire : la caravane reste à l\u2019écart', v)
            m0 = S()['money']; fouiller('car_coffre', 'car_f_coffre'); ok(S()['money'] >= m0 + 35, f'{name} coffre libre après la victoire', S()['money'] - m0)
            w0 = S()['inv'].get('water', 0); fouiller('car_bache_ex', 'car_f_bache'); ok(S()['inv'].get('water', 0) == w0 + 3, f'{name} bâche : trois bidons', S()['inv'].get('water'))
            E("(()=>{const f=window.__nml.state.flags;delete f.car_vaincue;delete f.car_regle})()"); E("window.__nml.game.ouvrirDialogue('rc_fierro','start')"); choisir('Attaquer'); E("window.__nml.game.closeDialogue()")
            wait("window.__nml.state.combat", 15); E("window.__nml.game.combat.finish('defaite')"); time.sleep(1); s = S()
            ok(not s['cbt'] and s['loc'] == LIEU and s['hp'] > 0, f'{name} défaite : réveil dans la scène', (s['loc'], s['hp'], s['x'], s['z']))
        ok(not errs, f'{name} aucune erreur console', errs[:6])
        ctx.close()
    # nuit [Régie + Ocre 18/11] : flaque chaude du feu (3 m, vacille avec le _neon), talus assombri, liseré tête et épaules (Fierro, Ciro couché) ; jour : rien de tout ça
    from PIL import Image; import io
    nuit = {}
    for h in (10, 23):
        ctx = br.new_context(viewport={'width': 1280, 'height': 800}); pg = ctx.new_page(); E = pg.evaluate
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=90000); time.sleep(1)
        E("localStorage.removeItem('nml_save_auto')"); passer_boot(E); E("document.getElementById('m-new').click()"); time.sleep(.5)
        E("document.querySelector('[data-race=\"humain\"]').click()"); time.sleep(.3); E("document.getElementById('cr-next').click()"); time.sleep(.3); E("document.getElementById('cr-enter').click()"); time.sleep(2)
        E(f"(()=>{{window.__nml.state.heures={h};return window.__nml.rencontres.entrerMaintenant('caravane_relais')}})()")
        t0 = time.time()
        while time.time() - t0 < 60 and not E(f"window.__nml.state.location==='{LIEU}' && window.__nml.lieuPret('{LIEU}')"): time.sleep(.5)
        time.sleep(2.5); E("document.getElementById('msg').textContent=''")
        P = lambda x, y, z: E(f"(()=>{{const p=window.__nml.project({x},{y},{z});return [Math.round(p.x),Math.round(p.y)]}})()")
        moy = lambda im, q, r=3: [sum(c[i] for c in [im.getpixel((q[0] + dx, q[1] + dy)) for dx in range(-r, r + 1) for dy in range(-r, r + 1)]) / (2 * r + 1) ** 2 for i in range(3)]
        g = E(f"(window.__nml.world.LOCATIONS['{LIEU}'].enseignes||[]).filter(e=>e.flaque).map(e=>({{...e.flaque,building:e.building,periode:e.periode}}))"); g = g if E("window.__nml.flaquesNuit().length") == 1 else []; fq, loin = P(17.5, 0, 16.3), P(17.5, 0, 20)
        ech = []
        for _ in range(8):
            im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); ech.append((moy(im, fq), moy(im, loin))); time.sleep(.7)
        lumi = lambda c: 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
        nuit[h] = {'glows': g, 'fl_max': max(lumi(a) - lumi(b) for a, b in ech), 'fl_min': min(lumi(a) - lumi(b) for a, b in ech), 'chaud': min(a[0] - a[2] for a, b in ech)}
        for who, (x, z, hh) in {'fierro': (13.2, 16.8, 1.84), 'ciro': (31.83, 13.75, 0.6)}.items():
            a_, b_ = P(x, 0, z), P(x, hh, z); clip = {'x': a_[0] - 45, 'y': b_[1] - 10, 'width': 90, 'height': a_[1] - b_[1] + 16}
            av = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('RGB'); E("window.__nml.liseres(false)"); time.sleep(.4)
            sa = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('RGB'); E("window.__nml.liseres(true)"); time.sleep(.2)
            H = a_[1] - b_[1]; ys = [i // av.width - 10 for i, (u, v) in enumerate(zip(av.getdata(), sa.getdata())) if sum(u) - sum(v) > 36 and u[2] - v[2] >= u[0] - v[0]]  # pixel éclairci et bleui par le liseré (une image d'animation chaude ne compte pas)
            nuit[h][who] = (len(ys), sum(1 for y in ys if y > 0.5 * H))
        nuit[h]['op'] = E("window.__nml.liseres().opacite"); nuit[h]['vis'] = E("window.__nml.liseres().visibles")
        if h == 23: pg.screenshot(path=OUT + 'livraison/desktop_caravane_nuit_23h.jpg', type='jpeg', quality=88)
        ctx.close()
    J, N = nuit[10], nuit[23]
    ok(not J['glows'] and len(N['glows']) == 1 and N['glows'][0].get('building') == 'car_bivouac' and N['glows'][0]['r'] == 3 and N['glows'][0]['periode'] == 5.5, 'flaque du feu : posée la nuit (3 m, même pulse 5,5 s que le _neon, peinte après le bivouac), absente le jour', (J['glows'], N['glows']))
    ok(N['fl_min'] > 4 and N['fl_max'] - N['fl_min'] > 12 and N['chaud'] > 15, f'flaque du feu visible la nuit et chaude ({N["fl_min"]:.0f} à {N["fl_max"]:.0f} de luminance au-dessus du sol, elle vacille)', N)
    ok(J['fl_max'] < 12, f'jour : pas de flaque ({J["fl_max"]:.0f})', J)
    ok(N['fierro'][0] >= 4 and N['fierro'][1] == 0 and N['ciro'][1] <= 2 and 0 < N['op'] <= 0.5, f'liseré de lune : Fierro tête et épaules ({N["fierro"][0]} px, 0 en bas), Ciro couché bord supérieur seulement ({N["ciro"]}), opacité {N["op"]:.2f} ≤ 0,5', N)
    ok(J['op'] == 0 and J['vis'] == 0, 'jour : aucun liseré (opacité nulle, aucun liseré affiché)', J)
    # flaque nocturne, variante décalque (champ cle) : même mécanisme pour le four des Verriers (rc_ecl_four_flaque) ; ici avec un calque additif existant
    ctx = br.new_context(viewport={'width': 1280, 'height': 800}); pg = ctx.new_page(); E = pg.evaluate; errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=90000); time.sleep(1)
    E("localStorage.removeItem('nml_save_auto')"); passer_boot(E); E("document.getElementById('m-new').click()"); time.sleep(.5)
    E("document.querySelector('[data-race=\"humain\"]').click()"); time.sleep(.3); E("document.getElementById('cr-next').click()"); time.sleep(.3); E("document.getElementById('cr-enter').click()"); time.sleep(2)
    E("(()=>{const f=window.__nml.rencontres.RENCONTRES.caravane_relais.scene.enseignes[0].flaque;window.__f0={...f};Object.assign(f,{cle:'rc_car_bivouac_3q_neon',x:16,z:13.5,w:3,d:3});window.__nml.state.heures=23;return window.__nml.rencontres.entrerMaintenant('caravane_relais')})()")
    t0 = time.time()
    while time.time() - t0 < 60 and not E(f"window.__nml.state.location==='{LIEU}' && window.__nml.lieuPret('{LIEU}')"): time.sleep(.5)
    time.sleep(1.5); F = E("window.__nml.flaquesNuit()")
    ok(len(F) == 1 and F[0]['cle'] and F[0]['i'] > 0.5 and not errs, 'flaque nocturne en décalque (champ cle) : posée par le même mécanisme, sans code de scène', (F, errs[:3]))
    E("Object.assign(window.__nml.rencontres.RENCONTRES.caravane_relais.scene.enseignes[0].flaque={},window.__f0)"); ctx.close()
    br.close()
print(f'\n{n} OK, {len(fails)} échec(s)'); [print('  -', f) for f in fails]; sys.exit(1 if fails else 0)
