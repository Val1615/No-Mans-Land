# Test rapide des rencontres de route, jalon 2, lot 3 (docs/rencontres/SURVIVANT.md §12.8) : « Le témoin sous les pins ».
# Catalogue et grille : terrain forêt, biome forest (F08, G08, F09), jamais G09 (Temple) ; unique (monde_sur_vu).
# 1280 x 800 : forcer survivant_pins, arrivée (Roque, Paca, lanterne, mulet, décalques et sols d'Ocre ; forêt en gabarits gris), cadrage, Roque appelle une fois,
# besace (ration, soulier), ornières (Observation 3), récit de Roque, soin (eau), variante Remedios, Paca s'en va, escorte (8 $, couteau, +1 h),
# texte de sortie, drapeaux de monde à la sortie (sauvé, escorté, Mateo pris), sur_* purgés, unique, rechargement.
# 390 x 844 : cadrage, Paca au fourré (pres_paca), « Fais ce que tu veux », eau laissée, dépouiller avec la gourde (laissé mourir), combat contre Paca
# (unités, zone, bâton, Roque hors combat, victoire, sac de Paca), reddition, défaite, fuite (halte, drapeaux : dépouillé, pas sauvé), retour sur la case,
# frapper Roque (pas de combat), sortie ouest (texte du Temple). Nuit / jour : lanterne seule lumière (flaque générique, nuit seulement), courbe forest,
# décors assombris la nuit, liseré. Garde-fou : aucun monde_* n'entre dans une condition de quête. Aucune erreur console.
# Env : URL (défaut http://127.0.0.1:8915/), OUT (défaut /tmp/nml-test-out/rencontres_j2_survivant/). Captures jpg dans OUT/livraison/.
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); from nml_boot import passer_boot
import time, os, json, sys, io
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8915/')
if not URL.endswith('/'): URL += '/'
OUT = os.environ.get('OUT', '/tmp/nml-test-out/rencontres_j2_survivant/'); OUT = OUT if OUT.endswith('/') else OUT + '/'; os.makedirs(OUT + 'livraison', exist_ok=True)
fails = []; n = 0
def ok(c, m, d=''):
    global n; print(('OK   ' if c else 'ECHEC ') + m + ('' if c else f'  {d}'), flush=True); n += bool(c); c or fails.append(m)
LIEU, RID = 'rc_survivant_pins', 'survivant_pins'
FORET = {'sur_pin_1', 'sur_pin_2', 'sur_pin_3', 'sur_pin_4', 'sur_pin_5', 'sur_pin_6', 'sur_pin_7', 'sur_pin_8', 'sur_pin_mort', 'sur_fourre'}
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
        S = lambda: E("(()=>{const s=window.__nml.state,R=s.region||{};return {loc:s.location,st:R.statut,case:R.case,trajet:R.trajet,x:s.player.x,z:s.player.z,dlg:s.dialogue,cbt:!!s.combat,money:s.player.money,inv:s.player.inv,rc:R.rencontre||null,journal:R.rencontres||{},h:s.heures,hp:s.player.hp,carte:!document.getElementById('nml').hidden,flags:Object.keys(s.flags).filter(f=>s.flags[f]&&/^sur_|^monde_|^combat_survivant|^race_/.test(f))}})()")
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
            # 0) catalogue et grille : forêt seulement, jamais G09 (Temple), unique
            T = E("""(()=>{const n=window.__nml,R=n.rencontres.RENCONTRES,D=R.survivant_pins,cells=[...n.voyage.cells.values()];
              const elig=c=>Object.entries(R).filter(([id,d])=>d.terrains.includes(c.terrain)&&(!d.biomes||d.biomes.includes(c.biome))&&(!d.si||d.si(n.state,c))).map(([id])=>id);
              const lab=c=>String.fromCharCode(65+c.col)+String(c.row+1).padStart(2,'0');
              const foret=cells.filter(c=>c.biome==='forest').map(c=>({l:lab(c),t:c.terrain,e:elig(c),lieu:!!n.voyage.lieuAt(c.col,c.row)}));
              const autres=cells.filter(c=>c.biome!=='forest').filter(c=>elig(c).includes('survivant_pins')).length;
              return {D:{t:D.terrains,b:D.biomes,pre:D.prefixe,arr:D.drapeauArrivee},foret,autres,g09:D.si(n.state,{col:6,row:8}),f08:D.si(n.state,{col:5,row:7})}})()""")
            ok(T['D']['t'] == ['foret'] and T['D']['b'] == ['forest'] and T['D']['pre'] == 'sur_' and T['D']['arr'] == 'monde_sur_vu', 'catalogue : terrains [foret], biomes [forest], préfixe sur_, drapeauArrivee monde_sur_vu', T['D'])
            g = {c['l']: c for c in T['foret']}
            ok(all(g.get(k, {}).get('t') == 'foret' and 'survivant_pins' in g[k]['e'] for k in ('F08', 'G08', 'F09')), 'grille : F08, G08 et F09 sont de la forêt et tirent le témoin', g)
            ok(not T['g09'] and T['f08'] and 'survivant_pins' not in g.get('G09', {}).get('e', []), 'grille : jamais sur G09, case du Temple du couchant', (T['g09'], g.get('G09')))
            ok(T['autres'] == 0, 'grille : aucune case hors forêt ne tire le témoin', T['autres'])
        # 1) forcer depuis la carte
        ok(forcer(), f'{name} témoin forcé depuis la carte', S()['st'])
        s = S(); ok(s['loc'] == LIEU and not s['carte'] and s['rc'], f'{name} entrée : scène {LIEU}, carte fermée', s['loc'])
        ok(abs(s['x'] - 30.5) < 0.6 and abs(s['z'] - 17) < 0.6, f'{name} arrivée à l\u2019est de la piste (30,5 ; 17)', (s['x'], s['z']))
        ok('monde_sur_vu' in s['flags'], f'{name} drapeau monde_sur_vu posé à l\u2019arrivée', s['flags'])
        pret()
        W = E("""(()=>{const n=window.__nml,L=n.world.LOCATIONS['%s'];return {w:L.size.w,d:L.size.d,niv:(L.niveaux||[]).length,manque:L.buildings.filter(x=>!n.bman[x.sprite]).map(x=>x.id),
          gab:L.buildings.filter(b=>b.gabarit).map(b=>b.id),poses:L.buildings.filter(b=>!b.gabarit).map(b=>b.sprite),
          pnj:n.world.NPCS.filter(q=>q.location==='%s'),spots:n.world.SPOTS.filter(q=>q.location==='%s').length,portes:n.world.DOORS.filter(d=>d.location==='%s').map(d=>[d.id,d.effet]),
          ens:L.enseignes,light:L.light,amb:n.rencontres.RENCONTRES.survivant_pins.scene.ambiance,sols:[L.ground.skin,...L.ground.paint.map(p=>p.skin)]}})()""" % ((LIEU,) * 4))
        gabp = [q['id'] for q in W['pnj'] if q.get('gabarit')]
        ok(W['w'] == 32 and W['d'] == 26 and not W['niv'], f'{name} scène 32 × 26, sans niveaux', (W['w'], W['d'], W['niv']))
        ok(len(W['portes']) == 2 and {q[0].split('_')[-1]: q[1] for q in W['portes']} == {'ouest': 'halte', 'est': 'reprise'}, f'{name} 2 sorties : ouest vers le Temple (halte), est (reprise, jamais gardée)', W['portes'])
        ok(vis() == {'sur_roque', 'sur_paca'}, f'{name} à l\u2019arrivée : Roque et Paca', vis())
        ok(not gabp and not W['manque'], f'{name} Roque et Paca : sprites d\u2019Ocre (aucun gabarit de PNJ), aucune clé manquante', (gabp, W['manque']))
        ok(set(W['gab']) == FORET and not any(k.startswith('rc_fo_pin') or k == 'rc_fo_fourre_3q' for k in W['poses']), f'{name} forêt en gabarits gris : les 8 pins, le pin foudroyé et le fourré (aucun pin d\u2019Ocre posé)', (W['gab'], W['poses']))
        ok({'rc_sur_lanterne_3q', 'rc_sur_mulet_3q', 'rc_sur_besace_3q', 'rc_sur_soulier_3q', 'rc_sur_trainee_3q', 'rc_sur_ornieres_3q', 'rc_fo_borne_3q'} <= set(W['poses']), f'{name} lanterne, mulet, besace, soulier, traînée, ornières et borne : clés d\u2019Ocre', W['poses'])
        ok(W['sols'][0] == 'g_rc_aiguilles' and 'g_rc_piste_foret' in W['sols'] and 'g_rc_aiguilles_b' in W['sols'], f'{name} sols : aiguilles, piste de forêt (z 15-20), variantes semées', W['sols'])
        ok(W['spots'] == 10, f'{name} {W["spots"]} points d\u2019examen et de fouille', W['spots'])
        e0 = (W['ens'] or [{}])[0]
        ok(e0.get('id') == 'sur_lampe' and e0.get('building') == 'sur_lanterne' and e0.get('effet') == 'pulse' and e0.get('flaque', {}).get('r') == 1.5 and not e0['flaque'].get('cle'),
           f'{name} lanterne : enseigne sur_lampe (pulse lent) et flaque générique r 1,5 au sol (pas un décalque)', e0)
        ok(W['amb'] == 'forest' and W['light'] and W['light'].get('tint') == '#efe9d4' and W['light'].get('lune', 1) == 0, f'{name} ambiance forest de jour (plus douce et plus olive que le désert), liseré éteint', W['light'])
        A = {a['id']: a for a in E("window.__nml.view.acteurs()")}
        ok('sur_roque' in A and 'sur_paca' in A, f'{name} Roque et Paca rendus', list(A))
        CAD = """(()=>{const n=window.__nml,s=n.state,W=innerWidth,H=innerHeight,r=e=>{const q=e.getBoundingClientRect();return [q.left,q.top,q.right,q.bottom]};
          const ex=[...document.querySelectorAll('#labels .wlabel.edge,#labels .wlabel.junction')].filter(e=>!e.hidden&&e.style.visibility!=='hidden'&&e.getClientRects().length).map(e=>({t:e.textContent,r:r(e)}));
          const P=(x,z)=>{const p=n.project(x,0,z);return [p.x,p.y]},m=document.getElementById('msg');
          return {W,H,ex,joueur:P(s.player.x,s.player.z),roque:P(15.8,13.3),mulet:P(21.4,16.6),paca:P(25.8,8.9),msg:m.textContent&&m.getClientRects().length?r(m):null,loc:r(document.getElementById('locbox')),zoom:r(document.getElementById('zoom'))}})()"""
        inter = lambda a, b: a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]
        K0 = E(CAD); Wv, Hv = K0['W'], K0['H']
        ok(len(K0['ex']) == 2 and all(e['r'][0] >= 6 and e['r'][2] <= Wv - 6 and e['r'][1] >= 0 and e['r'][3] <= Hv for e in K0['ex']), f'{name} cadrage : les 2 étiquettes de sortie entières, à 6 px au moins du bord', K0['ex'])
        cibles = (K0['joueur'], K0['roque'], K0['mulet'], K0['paca'])
        ok(all(8 <= q[0] <= Wv - 8 and 60 <= q[1] <= Hv - 150 for q in cibles), f'{name} cadrage : joueur, mulet, Roque et Paca dans le cadre', cibles)
        ok(not inter(K0['loc'], K0['zoom']), f'{name} titre du lieu hors des boutons de zoom', (K0['loc'], K0['zoom']))
        ARR = E(f"window.__nml.rencontres.RENCONTRES.{RID}.arrivee")
        for _ in range(4):
            E("t=>{document.getElementById('msg').textContent=t}", ARR); time.sleep(.4); K1 = E(CAD)
            if K1['msg']: break
        ok(K1['msg'] and not any(inter(K1['msg'], e['r']) for e in K1['ex']), f'{name} encart d\u2019arrivée : ne chevauche aucune étiquette de sortie', (K1['msg'], K1['ex']))
        time.sleep(.6); shot(f'{name}_survivant_arrivee.jpg')
        E("window.__nml.state.player.inv.water=2")

        if not mob:
            # 2) passer sur la piste : Roque appelle une fois
            walk(19.5, 17.8); time.sleep(.4); m1 = msg()
            ok('De l' in m1 and 'sur_appel' in S()['flags'] and not S()['dlg'], f'{name} sur la piste : Roque appelle une fois (« De l\u2019eau »), sans ouvrir de dialogue', m1)
            walk(23, 18.2); walk(19.5, 17.8); time.sleep(.3); ok(msg() != m1 or not S()['dlg'], f'{name} Roque n\u2019insiste pas')
            # 3) besace : ration, soulier ; vide ensuite
            r0 = inv('ration'); fouiller('sur_besace_ex', 'sur_f_besace'); s = S()
            ok(s['inv'].get('ration', 0) == r0 + 1 and 'sur_vu_soulier' in s['flags'], f'{name} besace : le pain dur (1 ration), le soulier d\u2019enfant', (s['inv'], s['flags']))
            time.sleep(.6); fouiller('sur_besace_ex'); time.sleep(.6); ok(inv('ration') == r0 + 1 and 'vide' in msg(), f'{name} besace vide ensuite', msg())
            # 4) ornières (Observation 3) : les pas qui s'arrêtent
            stats(observation=30); fouiller('sur_ornieres_ex', 'sur_vu_pas'); time.sleep(.4)
            ok({'sur_vu_ornieres', 'sur_vu_pas'} <= set(S()['flags']) and 'Ils ne repartent pas' in E("window.__nml.world.SPOTS.find(q=>q.id==='sur_ornieres_ex').text"), f'{name} ornières (Observation 3) : étuis du Service, pas d\u2019enfant', msg())
            fouiller('sur_trainee_ex', 'sur_vu_trainee'); ok('sur_vu_trainee' in S()['flags'], f'{name} traînée de sang examinée')
            # 5) Roque : récit, soin (eau), variante Remedios, soulier ; Paca s'en va après le soin
            poser('monde_remedios_vue'); parler('sur_roque'); ok(E("window.__nml.state.dialogue?.npc") == 'sur_roque' and 'De l' in noeud(), f'{name} Roque : « De l\u2019eau. S\u2019il t\u2019en reste. »', noeud())
            L = labels(); ok(any('Tiens, bois' in l for l in L) and not any('ration' in l for l in L), f'{name} avec de l\u2019eau : « Tiens, bois », pas l\u2019option ration', L)
            shot(f'{name}_survivant_roque.jpg')
            choisir('Quel enfant'); ok('Mateo' in noeud() and 'sur_recit' in S()['flags'], f'{name} récit : Mateo, les plaques, le Service', noeud())
            w0 = inv('water'); choisir('Tiens, bois'); s = S()
            ok(s['inv'].get('water', 0) == w0 - 1 and 'sur_soigne' in s['flags'] and 'citerne' in noeud(), f'{name} soin : une eau ; variante Remedios (« la caravane, celle de la citerne »)', noeud())
            choisir('soulier'); ok('treize ans' in noeud(), f'{name} le soulier : « Il a treize ans »', noeud()); fermer()
            parler('sur_paca'); ok('se relèvera' in noeud() and 'sur_paca_partie' in S()['flags'], f'{name} Paca après le soin : « Alors il se relèvera »', noeud()); fermer(); time.sleep(.5)
            ok('sur_paca' not in vis(), f'{name} Paca partie', vis())
            ok(E("(()=>{const D=window.__nml.rencontres.RENCONTRES.survivant_pins.dialogues;return !JSON.stringify(D).match(/\\bq_|quete/)})()"), f'{name} garde-fou : aucun drapeau de quête dans les dialogues')
            # 6) escorte : 8 $, le couteau, sortie est (+1 h), texte de sortie, drapeaux de monde
            m0, k0 = S()['money'], inv('poignard'); parler('sur_roque'); ok('moins froid' in noeud(), f'{name} Roque, soigné : « J\u2019ai moins froid »', noeud())
            choisir('emmener'); choisir('Viens'); ok(S()['money'] == m0 + 8 and 'sur_escorte' in S()['flags'], f'{name} escorte acceptée : 8 $', S()['money'] - m0)
            choisir('Je prends le couteau'); ok(inv('poignard') == k0 + 1, f'{name} le couteau de Roque', inv('poignard'))
            h1 = S()['h']; choisir('On y va'); ok(wait("window.__nml.state.region.statut!=='rencontre'", 20), f'{name} « On y va » : la scène est quittée avec Roque', S()['st']); time.sleep(.3)
            m2 = msg(); s = S()
            ok('sous le bras' in m2, f'{name} texte de sortie : « Tu prends Roque sous le bras »', m2)
            dh = s['h'] - h1; hc = E("(()=>{const n=window.__nml,R=n.state.region,c=R.case;try{return n.voyage.heures(n.voyage.cellAt(c[0],c[1]))||0}catch(e){return null}})()")
            ok(abs(dh - 2 - (hc or 0)) < 0.01 or dh == 2, f'{name} durée : +1 h, +1 h d\u2019escorte ({dh} h dont {hc} h de piste)', (dh, hc))
            ok(not any(f.startswith('sur_') for f in s['flags']) and {'monde_sur_vu', 'monde_roque_sauve', 'monde_roque_escorte', 'monde_mateo_pris'} <= set(s['flags']) and 'monde_roque_depouille' not in s['flags'],
               f'{name} sortie : sur_* purgés ; monde_roque_sauve, monde_roque_escorte, monde_mateo_pris posés', s['flags'])
            r = E("""(()=>{const n=window.__nml,h=n.voyage.crochets.onCaseEntree,out=[];for(const v of [0,0.02,0.05,0.09]){n.rencontres.setRng(()=>v);const t=h({col:5,row:7,terrain:'foret',biome:'forest'},n.state);out.push(t&&(t.rencontre||t.id)||null)}n.rencontres.setRng(null);return out})()""")
            ok(r is not None and 'survivant_pins' not in r, f'{name} témoin unique : plus jamais tiré (monde_sur_vu)', r)
            E("window.__nml.game.save && window.__nml.game.save()"); pg.reload(); demarrer(); passer_boot(E); E("document.getElementById('m-continue').click()"); time.sleep(1.5); pret(); s = S()
            ok({'monde_sur_vu', 'monde_roque_sauve', 'monde_roque_escorte', 'monde_mateo_pris'} <= set(s['flags']), f'{name} rechargement : drapeaux de monde sauvegardés', s['flags'])
        else:
            # 1') Paca au fourré : pres_paca, « Fais ce que tu veux »
            walk(24.5, 11.2); wait("window.__nml.state.dialogue", 10)
            ok(E("window.__nml.state.dialogue?.npc") == 'sur_paca' and 'rien pris' in noeud() and 'sur_vu_paca' in S()['flags'], f'{name} pres_paca : Paca sort du fourré (« Je n\u2019ai encore rien pris »)', noeud())
            choisir('Tu comptes'); ok('pas celle qui a tiré' in noeud(), f'{name} Paca : « Je ne suis pas celle qui a tiré »', noeud()); choisir('Fais ce que tu veux')
            ok('sur_paca_libre' in S()['flags'], f'{name} « Fais ce que tu veux » : sur_paca_libre'); fermer()
            # 2') Roque : refus, eau laissée
            w0 = inv('water'); parler('sur_roque'); choisir('Je ne peux rien'); ok('gourde' in noeud(), f'{name} refus : « laisse-moi au moins la gourde »', noeud())
            choisir('laisse de l'); ok(inv('water') == w0 - 1 and 'sur_laisse_eau' in S()['flags'], f'{name} eau laissée', S()['flags']); fermer()
            # 3') dépouiller, avec la dernière eau : laissé mourir
            parler('sur_roque'); ok('gourde est encore là' in noeud(), f'{name} Roque : « Ta gourde est encore là »', noeud())
            m0, k0, w0 = S()['money'], inv('poignard'), inv('water'); choisir('Je prends ce que tu as'); ok('laisse-moi l' in noeud(), f'{name} dépouiller : « L\u2019eau d\u2019abord »', noeud())
            choisir('aussi la gourde'); s = S()
            ok(s['money'] == m0 + 8 and s['inv'].get('poignard', 0) == k0 + 1 and s['inv'].get('water', 0) == w0 + 1 and {'sur_depouille', 'sur_laisse_mourir'} <= set(s['flags']), f'{name} dépouillé : 8 $, le couteau, la gourde ; sur_laisse_mourir', (s['money'] - m0, s['inv'], s['flags']))
            ok('ne le retrouves pas' in noeud(), f'{name} « Que tu ne le retrouves pas, l\u2019enfant »', noeud()); fermer()
            parler('sur_roque'); ok('regarde la piste' in noeud(), f'{name} Roque ne te regarde plus', noeud()); fermer()
            # 4') combat contre Paca : unités, zone, bâton, Roque hors combat ; victoire, sac de Paca
            oter('sur_paca_libre'); ouvrir('sur_paca'); choisir('Attaquer'); fermer(); ok(wait("window.__nml.state.combat", 15), f'{name} [Attaquer] chez Paca : combat')
            Cb = E("(()=>{const c=window.__nml.state.combat;return {z:c.zone,u:c.units.map(u=>({id:u.id,arme:u.arme,rs:u.rendSous||0,ft:u.fuitTour||0}))}})()"); ids = {u['id'] for u in Cb['u']}
            ok(ids == {'joueur', 'paca'}, f'{name} unités : Paca seule (Roque jamais au combat)', Cb['u'])
            z = Cb['z']; ok(z and abs((z['i0'] + z['i1']) / 2 - 18) <= 1 and abs((z['j0'] + z['j1']) / 2 - 15) <= 1, f'{name} zone de combat centrée sur (18 ; 15)', z)
            pc = [u for u in Cb['u'] if u['id'] == 'paca'][0]; ok(pc['arme'] == 'baton' and pc['rs'] == 0.5 and pc['ft'] == 2, f'{name} Paca : bâton, se rend sous 50 %, fuit au tour 2', pc)
            ok('sur_paca' not in vis() and 'sur_roque' in vis(), f'{name} en combat : Paca remplacée par son unité, Roque reste contre le pin', vis())
            wait("window.__nml.state.combat && window.__nml.state.combat.phase==='joueur'", 40); time.sleep(1); shot(f'{name}_survivant_combat.jpg')
            r = E("""(()=>{const g=window.__nml.game,c=window.__nml.state.combat;if(!c)return null;const p=c.units.find(u=>u.joueur),t=c.units.find(u=>u.id==='paca');
               p.i=t.i-1;p.j=t.j;p.x=p.i+.5;p.z=p.j+.5;p.pa=10;p.arme='mains';t.pv=Math.floor(t.pvMax*0.5)+1;g.setRng(()=>0);return g.combat.attack('paca')})()""")
            ok(wait("!window.__nml.state.combat", 10) and {'sur_paca_partie', 'sur_vaincue'} <= set(S()['flags']), f'{name} victoire : Paca se rend sous 50 %', (r, S()['flags']))
            ok(E("window.__ev.some(e=>e.type==='combat_fin'&&/La piste est grande/.test(e.text||''))"), f'{name} texte de victoire : « La piste est grande »'); fermer()
            r0, m0 = inv('ration'), S()['money']; fouiller('sur_sac_paca', 'sur_f_paca'); ok(inv('ration') == r0 + 1 and S()['money'] == m0 + 4, f'{name} sac de Paca : 1 ration, 4 $', (inv('ration') - r0, S()['money'] - m0))
            # reddition (payMax 8) et défaite (réveil plus bas sur la piste)
            oter('sur_paca_partie', 'sur_vaincue'); time.sleep(.3); m0 = S()['money']; ouvrir('sur_paca'); choisir('Attaquer'); fermer(); wait("window.__nml.state.combat", 15)
            wait("window.__nml.state.combat && window.__nml.state.combat.phase==='joueur'", 40); E("window.__nml.game.combat.surrender()"); time.sleep(1); fermer(); s = S()
            ok(not s['cbt'] and s['loc'] == LIEU and s['money'] == m0 - 8 and 'sur_paca_partie' in s['flags'], f'{name} reddition : Paca ramasse 8 $ et s\u2019en va', (s['money'] - m0, s['flags']))
            oter('sur_paca_partie'); ouvrir('sur_paca'); choisir('Attaquer'); fermer(); wait("window.__nml.state.combat", 15); E("window.__nml.game.combat.finish('defaite')"); time.sleep(1); fermer(); s = S()
            ok(not s['cbt'] and s['loc'] == LIEU and abs(s['x'] - 30.5) < 1.6 and abs(s['z'] - 17) < 1.6, f'{name} défaite : réveil plus bas sur la piste', (s['x'], s['z']))
            # fuite : halte ; drapeaux de monde : dépouillé, pas sauvé (laissé mourir), Mateo pas encore pris
            h1 = S()['h']; ouvrir('sur_paca'); choisir('Attaquer'); fermer(); wait("window.__nml.state.combat", 15); E("window.__nml.game.combat.finish('fuite')")
            ok(wait("window.__nml.state.region.statut==='halte'", 20), f'{name} fuite : retour à la carte en halte', S()['st']); s = S()
            ok(abs(s['h'] - h1 - 1) < 0.01, f'{name} durée : +1 h', s['h'] - h1)
            ok(not any(f.startswith('sur_') for f in s['flags']) and 'monde_roque_depouille' in s['flags'] and 'monde_roque_sauve' not in s['flags'] and 'monde_mateo_pris' not in s['flags'],
               f'{name} hors scène : sur_* purgés ; monde_roque_depouille, pas de monde_roque_sauve (eau reprise), pas de monde_mateo_pris', s['flags'])
            E(f"window.__nml.rencontres.entrer('{RID}')"); wait("window.__nml.state.location==='%s'" % LIEU, 20); pret(); s = S()
            ok(s['loc'] == LIEU and {'sur_laisse_mourir', 'sur_depouille', 'sur_f_paca', 'sur_laisse_eau'} <= set(s['flags']), f'{name} retour sur la case : journal restauré', s['flags'])
            # 5') frapper Roque : il se rend au premier coup, pas de combat
            oter('sur_laisse_mourir', 'sur_depouille'); time.sleep(.3); m0 = S()['money']; ouvrir('sur_roque', 'start'); choisir('Attaquer'); s = S()
            ok('ne le retrouveras pas' in noeud() and {'sur_frappe', 'sur_laisse_mourir', 'sur_depouille'} <= set(s['flags']) and s['money'] == m0 + 8, f'{name} frapper Roque : il ne se défend pas (dépouillé, laissé mourir)', noeud())
            fermer(); time.sleep(.5); ok(not S()['cbt'] and not E("window.__nml.state.combatPending"), f'{name} frapper Roque : aucun combat')
            # 6') sortie ouest : texte du Temple, halte
            E(f"window.__nml.game.useDoor('{LIEU}_ouest')"); ok(wait("window.__nml.state.region.statut==='halte'", 40), f'{name} sortie ouest : halte', S()['st']); time.sleep(.3)
            ok('Temple du couchant' in msg(), f'{name} texte de sortie ouest : « vers le Temple du couchant »', msg())
            ok('monde_roque_depouille' in S()['flags'] and 'monde_roque_sauve' not in S()['flags'], f'{name} drapeaux de monde gardés', S()['flags'])
        ok(not errs, f'{name} aucune erreur console', errs[:6])
        ctx.close()
    # nuit et jour : la lanterne, seule lumière (flaque générique, nuit seulement), courbe forest, décors assombris, liseré
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
        fq, loin = P(16.6, 0, 13.2), P(19.5, 0, 12.5)
        ech = []
        for _ in range(6):
            im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); ech.append((moy(im, fq), moy(im, loin))); time.sleep(.9)
        nuit[h] = {'fl': E("window.__nml.flaquesNuit()"), 'tint': E(f"window.__nml.world.LOCATIONS['{LIEU}'].light.tint"), 'fl_min': min(lumi(a) - lumi(b) for a, b in ech),
                   'chaud': min(a[0] - a[2] for a, b in ech), 'loin': max(lumi(b) for a, b in ech), 'errs': errs[:3], 'op': E("window.__nml.liseres().opacite"),
                   'decor': E(f"(()=>{{const L=window.__nml.world.LOCATIONS['{LIEU}'];return {{b:L.buildings.length,bn:L.buildings.filter(b=>b.nuit).length}}}})()")}
        if h == 23: pg.screenshot(path=OUT + 'livraison/desktop_survivant_nuit_23h.jpg', type='jpeg', quality=88)
        else: pg.screenshot(path=OUT + 'livraison/desktop_survivant_jour_10h.jpg', type='jpeg', quality=88)
        ctx.close()
    J, N = nuit[10], nuit[23]
    ok(not J['fl'] and len(N['fl']) == 1 and N['fl'][0]['id'] == 'sur_lampe' and not N['fl'][0]['cle'], 'flaque de la lanterne : générique (gradient), posée la nuit, absente le jour', (J['fl'], N['fl']))
    ok(N['fl_min'] > 3 and N['chaud'] > 0, f'flaque de la lanterne visible la nuit et chaude ({N["fl_min"]:.0f} au-dessus du sol voisin)', N)
    ok(N['loin'] < 45, f'la lanterne n\u2019éclaire pas toute la clairière : sol sombre à 3 m (luminance {N["loin"]:.0f})', N)
    ok(J['tint'] == '#efe9d4' and N['tint'] == '#5c6688', 'courbe forest : jour olive doux, nuit bleu-gris commune', (J['tint'], N['tint']))
    ok(N['decor']['bn'] == N['decor']['b'], f'nuit : tous les décors suivent la courbe de nuit ({N["decor"]})', N['decor'])
    ok(0 < N['op'] <= 0.5 and J['op'] == 0, f'liseré de lune : opacité {N["op"]:.2f} ≤ 0,5 la nuit ; nul le jour', (N['op'], J['op']))
    ok(not N['errs'] and not J['errs'], 'nuit et jour : aucune erreur console', (N['errs'], J['errs']))
    br.close()
print(f'\n{n} OK, {len(fails)} échec(s)'); [print('  -', f) for f in fails]; sys.exit(1 if fails else 0)
