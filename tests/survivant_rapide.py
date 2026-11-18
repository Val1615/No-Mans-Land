# Test rapide, jalon 2, lot 3 : « Le témoin sous les pins » (SURVIVANT.md §12, forêt v1.1 §15). Version allégée (consigne de Régie) :
# les cinq vérifications essentielles (la scène se charge ; on se déplace ; on interagit et on sort ; une issue de combat se résout ;
# le retour carte garde ressources et itinéraire ; une sauvegarde hors combat se recharge), le fondu partiel des houppiers (mulet et Roque lisibles),
# les ombres de couronne éteintes la nuit, le réglage global de fréquence, la mémoire des rencontres récentes, une passe de captures 1280 et 390.
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
        # 1) la scène se charge (forcée depuis la carte, en route vers Steel)
        ok(forcer(), f'{name} témoin forcé depuis la carte', S()['st']); pret(); s0 = S()
        W = E("""(()=>{const n=window.__nml,L=n.world.LOCATIONS['%s'];return {manque:L.buildings.filter(x=>!n.bman[x.sprite]).map(x=>x.id),gab:L.buildings.filter(b=>b.gabarit).length,
          pins:L.buildings.filter(b=>/^rc_fo_(pin|lisiere|bouquet)/.test(b.sprite)).length,sol:L.buildings.filter(b=>b.solid&&b.solid.length&&/rc_fo_(ombre|litiere)|trainee|ornieres/.test(b.sprite)).length,
          lant:L.buildings.find(b=>b.id==='sur_lanterne')}})()""" % LIEU)
        ok(s0['loc'] == LIEU and not s0['carte'] and vis() == {'sur_roque', 'sur_paca'} and not W['manque'] and not W['gab'] and W['pins'] >= 12 and not W['sol'],
           f'{name} scène chargée : Roque et Paca, forêt v1.1 posée ({W["pins"]} pins), aucun gabarit, aucune clé manquante, décalques non solides', (s0['loc'], vis(), W))
        ok(abs(W['lant']['y'] - 2.65) < 1e-6 and W['lant'].get('apres') == 'sur_pin_mort', f'{name} lanterne accrochée au pin foudroyé (y 2,65, dessinée après lui)', W['lant'])
        if not mob:
            E("window.__nml.game.closeDialogue()"); shot(f'{name}_survivant_arrivee.jpg')
        # houppiers : fondu partiel quand la couronne cache Roque ou le mulet (son point d'examen)
        time.sleep(1.5); Hp = E("window.__nml.houppiers()")
        dev = lambda c: [q for q in Hp if c in q['couvre']]
        ok(Hp and all(q['cible'] >= 0.4 for q in Hp) and all(q['cible'] < 1 for q in Hp if q['couvre']), f'{name} houppiers : fondu partiel (≥ 0,4) dès qu\u2019une couronne cache quelqu\u2019un, jamais effacés', [q for q in Hp if q['couvre']][:4])
        ok(dev('sur_roque') and all(0.4 <= q['cible'] < 1 for q in dev('sur_roque') + dev('sur_mulet_ex')),
           f'{name} Roque et le mulet lisibles : couronnes devant Roque ({len(dev("sur_roque"))}) et devant le mulet ({len(dev("sur_mulet_ex"))}) estompées', (dev('sur_roque'), dev('sur_mulet_ex')))
        shot(f'{name}_survivant_houppiers.jpg')
        # 2) on se déplace
        x0, z0 = S()['x'], S()['z']; walk(24.5, 18.5); s = S()
        ok(abs(s['x'] - 24.5) < 0.8 and abs(s['z'] - 18.5) < 0.8 and abs(s['x'] - x0) > 3, f'{name} déplacement sur la piste', (x0, z0, s['x'], s['z']))
        if not mob:
            # 3) on interagit : la besace (ration), Roque parle
            fermer(); r0 = inv('ration'); fouiller('sur_besace_ex', 'sur_f_besace'); ok(inv('ration') == r0 + 1, f'{name} besace fouillée : une ration', inv('ration') - r0)
            parler('sur_roque'); ok(E("window.__nml.state.dialogue?.npc") == 'sur_roque' and labels(), f'{name} Roque parle', noeud()[:60]); fermer()
            # 6) sauvegarde hors combat, rechargement dans la scène
            m1, r1 = S()['money'], inv('ration')
            E("window.__nml.shell.autosave()"); pg.reload(); demarrer(); passer_boot(E); E("document.getElementById('m-continue').click()"); time.sleep(1.5); pret(); s = S()
            E("(()=>{window.__ev=[];window.__nml.game.on(e=>window.__ev.push({type:e.type,id:e.id,text:e.text}))})()")
            ok(s['loc'] == LIEU and s['st'] == 'rencontre' and 'sur_f_besace' in s['flags'] and s['money'] == m1 and inv('ration') == r1 and vis() == {'sur_roque', 'sur_paca'},
               f'{name} sauvegarde hors combat rechargée : dans la scène, besace vidée, PNJ en place', (s['loc'], s['st'], s['flags']))
            # 4) issue de combat : Paca attaquée, se rend sous 50 %
            ouvrir('sur_paca'); choisir('Attaquer'); fermer(); ok(wait("window.__nml.state.combat", 15), f'{name} [Attaquer] chez Paca : combat')
            wait("window.__nml.state.combat && window.__nml.state.combat.phase==='joueur'", 40); time.sleep(.8)
            r = E("""(()=>{const g=window.__nml.game,c=window.__nml.state.combat;if(!c)return null;const p=c.units.find(u=>u.joueur),t=c.units.find(u=>u.id==='paca');
               p.i=t.i-1;p.j=t.j;p.x=p.i+.5;p.z=p.j+.5;p.pa=10;p.arme='mains';t.pv=Math.floor(t.pvMax*0.5)+1;g.setRng(()=>0);return g.combat.attack('paca')})()""")
            ok(wait("!window.__nml.state.combat", 10) and {'sur_paca_partie', 'sur_vaincue'} <= set(S()['flags']) and S()['loc'] == LIEU, f'{name} combat résolu : Paca se rend, on reste sous les pins', (r, S()['flags']))
            fermer(); E("window.__nml.game.setRng(null)")
            # 3') on sort (est, reprise) ; 5) retour carte : ressources et itinéraire gardés
            m2, r2, tr = S()['money'], inv('ration'), S()['trajet']
            E(f"window.__nml.game.useDoor('{LIEU}_est')"); ok(wait("window.__nml.state.region.statut!=='rencontre'", 40), f'{name} sortie est : la scène est quittée', S()['st']); time.sleep(.5); s = S()
            ok(s['money'] == m2 and inv('ration') == r2 and s['inv'].get('ration', 0) >= 1, f'{name} retour carte : argent et ration conservés', (s['money'], s['inv']))
            ok(s['trajet'] and tr and s['trajet'] == tr[len(tr) - len(s['trajet']):] and s['trajet'][-1] == tr[-1] and s['st'] != 'halte', f'{name} retour carte : itinéraire vers Steel conservé, la route reprend', (s['st'], tr, s['trajet']))
            ok(not any(f.startswith('sur_') for f in s['flags']) and 'monde_sur_vu' in s['flags'], f'{name} sur_* purgés, monde_sur_vu gardé', s['flags'])
            # fréquence globale : 1 par défaut (taux inchangés), 0 coupe tout, 2 double le seuil
            F = E("""(async()=>{const n=window.__nml,h=n.voyage.crochets.onCaseEntree,D=await import(new URL('src/data/rencontres.js',location.href).href),T=await import(new URL('src/data/nml.js',location.href).href);
              const p=T.TERRAINS.foret.p,c={col:5,row:7,terrain:'foret',biome:'forest'},f0=n.state.flags.monde_sur_vu;delete n.state.flags.monde_sur_vu;n.state.region.recentes=[];
              const tire=(v,fq)=>{n.rencontres.frequence=fq;let k=0;n.rencontres.setRng(()=>k++?0:v);const e=h(c,n.state);n.state.region.recentes=[];return e&&e.rencontre||null};
              const r={def:D.RENCONTRES_FREQUENCE,api:n.rencontres.frequence,p,sous:tire(p*0.9,1),dessus:tire(p*1.1,1),zero:tire(0,0),double:tire(p*1.5,2)};
              n.rencontres.frequence=D.RENCONTRES_FREQUENCE;n.rencontres.setRng(null);if(f0)n.state.flags.monde_sur_vu=true;return r})()""")
            ok(F['def'] == 1 and F['api'] == 1, f'{name} RENCONTRES_FREQUENCE = 1 par défaut', F)
            ok(F['sous'] == 'survivant_pins' and F['dessus'] is None and F['zero'] is None and (F['p'] * 1.5 >= 1 or F['double'] == 'survivant_pins'),
               f'{name} fréquence : taux de base inchangés à 1, 0 coupe les rencontres, 2 double le seuil (p forêt {F["p"]})', F)
            # mémoire des rencontres récentes : 3 derniers ids, le dernier exclu ; seul éligible : aucune rencontre
            M = E("""(()=>{const n=window.__nml,h=n.voyage.crochets.onCaseEntree,c={col:5,row:7,terrain:'foret',biome:'forest'},R=n.state.region,f0=n.state.flags.monde_sur_vu;delete n.state.flags.monde_sur_vu;
              const tire=()=>{let k=0;n.rencontres.setRng(()=>0);const e=h(c,n.state);return e&&e.rencontre||null};
              R.recentes=['a','b','c'];const t1=tire(),m1=[...R.recentes];const t2=tire(),m2=[...R.recentes];R.recentes=['survivant_pins','a'];const t3=tire();
              n.rencontres.setRng(null);R.recentes=[];if(f0)n.state.flags.monde_sur_vu=true;return {t1,m1,t2,m2,t3}})()""")
            ok(M['t1'] == 'survivant_pins' and M['m1'] == ['b', 'c', 'survivant_pins'], f'{name} mémoire : le tirage est noté, 3 derniers ids gardés', M)
            ok(M['t2'] is None and M['m2'] == M['m1'] and M['t3'] == 'survivant_pins', f'{name} mémoire : le dernier tiré est exclu (seul éligible en forêt : aucune rencontre), l\u2019avant-dernier ne l\u2019est pas', M)
            E("window.__nml.state.region.recentes=['x','survivant_pins']; window.__nml.shell.autosave()"); pg.reload(); demarrer(); passer_boot(E); E("document.getElementById('m-continue').click()"); time.sleep(1.5)
            ok(E("JSON.stringify(window.__nml.state.region.recentes)") == '["x","survivant_pins"]', f'{name} mémoire sauvegardée avec la région', E("window.__nml.state.region.recentes"))
        else:
            # 3) mobile : on interagit (examen du mulet) et on sort à l'ouest (halte)
            fermer(); E("window.__ev=[]"); E("window.__nml.game.useSpot('sur_mulet_ex')"); wait("window.__ev.some(e=>e.type==='message'||e.type==='spot')||/mulet/.test(document.getElementById('msg').textContent)", 30)
            ok('mulet' in msg().lower() or E("window.__ev.some(e=>/mulet/i.test(e.text||''))"), f'{name} examen du mulet', msg()[:60])
            E(f"window.__nml.game.useDoor('{LIEU}_ouest')"); ok(wait("window.__nml.state.region.statut==='halte'", 40), f'{name} sortie ouest : halte sur la carte', S()['st'])
        ok(not errs, f'{name} aucune erreur console', errs[:6])
        ctx.close()
    # nuit : ombres de couronne éteintes, lanterne seule lumière ; capture 23 h
    for h in (10, 23):
        ctx = br.new_context(viewport={'width': 1280, 'height': 800}); pg = ctx.new_page(); E = pg.evaluate; errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=90000); time.sleep(1)
        E("localStorage.removeItem('nml_save_auto')"); passer_boot(E); E("document.getElementById('m-new').click()"); time.sleep(.5)
        E("document.querySelector('[data-race=\"humain\"]').click()"); time.sleep(.3); E("document.getElementById('cr-next').click()"); time.sleep(.3); E("document.getElementById('cr-enter').click()"); time.sleep(2)
        E(f"(()=>{{window.__nml.state.heures={h};return window.__nml.rencontres.entrerMaintenant('{RID}')}})()")
        t0 = time.time()
        while time.time() - t0 < 60 and not E(f"window.__nml.state.location==='{LIEU}' && window.__nml.lieuPret('{LIEU}')"): time.sleep(.5)
        time.sleep(2.5); E("document.getElementById('msg').textContent=''"); Om = E("window.__nml.ombres()"); fl = E("window.__nml.flaquesNuit()")
        if h == 23:
            ok(Om and not any(o['visible'] for o in Om) and [f['id'] for f in fl] == ['sur_lampe'], f'23 h : ombres de couronne éteintes ({len(Om)}), la lanterne seule lumière', (Om[:3], fl))
            pg.screenshot(path=OUT + 'livraison/desktop_survivant_nuit_23h.jpg', type='jpeg', quality=88)
        else:
            ok(Om and all(o['visible'] and o['opacite'] > 0.5 for o in Om) and not fl, f'10 h : ombres de couronne posées ({len(Om)}), pas de flaque', (Om[:3], fl))
        ok(not errs, f'{h} h : aucune erreur console', errs[:3])
        ctx.close()
    br.close()
print(f'\n{n} OK, {len(fails)} échec(s)'); [print('  -', f) for f in fails]; sys.exit(1 if fails else 0)
