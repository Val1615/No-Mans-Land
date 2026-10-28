# Ah-Lam au Barrage (a_sud) : Discours (parole:4, palier 3 = 10 cr), Intimider (jet opposé à sa Volonté 4), un seul essai, prix mémorisés, pauvre30 -> ruelle.
# Toutes les branches, tirage forcé (game.setRng). Port dédié 8862 ; captures /tmp/nml-test-out/ahlam/.
import os, sys, json, time
from playwright.sync_api import sync_playwright
URL = os.environ.get('URL', 'http://127.0.0.1:8862/'); OUT = '/tmp/nml-test-out/ahlam/'; os.makedirs(OUT, exist_ok=True)
R = []
def check(n, ok, d=''): R.append({'test': n, 'ok': bool(ok), 'detail': str(d)}); print(('OK    ' if ok else 'ECHEC ') + n, d, flush=True)
# jet de VOLONTE.jet : d = -2 + floor(r * 5) ; r pour d = -2..+2
D = {-2: 0.0, -1: 0.3, 0: 0.5, 1: 0.7, 2: 0.99}
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = br.new_page(viewport={'width': 1280, 'height': 800}); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e))); E = pg.evaluate
    pg.goto(URL); pg.wait_for_function('window.__nml && window.__nml.shell', timeout=60000); time.sleep(1.5)
    for sel in ['#m-new', '[data-race="augmente"]', '#cr-next', '#cr-enter']:
        b = pg.locator(sel).first.bounding_box(); pg.mouse.click(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2); time.sleep(0.6)
    st = lambda: E('JSON.parse(JSON.stringify(window.__nml.state))')
    def setup(cr=25, parole=30, cha=4, force=4):
        E(f"""(()=>{{const g=window.__nml.game,s=g.snapshot();s.location='steel_asia';s.player.x=26.4;s.player.z=30.4;s.player.credits={cr};
          for(const f of ['cl_barrage','cl_barrage_10','cl_barrage_30','ahlam_tente'])delete s.flags[f];g.restore(s,true);
          const c=window.__nml.state.character;c.skills.parole={parole};c.attrs.charisme={cha};c.attrs.force={force}}})()"""); time.sleep(0.6)
    def rng(*ds): E(f"window.__q={json.dumps([D[d] for d in ds])};window.__nml.game.setRng(()=>window.__q.length?window.__q.shift():0.5)")
    def talk(): E("window.__nml.state.dialogue={npc:'ag_ahlam',node:'start'}"); time.sleep(0.4)
    def node(): d = E("window.__nml.state.dialogue"); return d and d['node']
    def labels(): return E("window.__nml.game.currentNode() ? window.__nml.game.currentNode().options.map(o=>o.label) : null") or []
    def text(): return E("window.__nml.game.currentNode() && window.__nml.game.currentNode().text")
    def pick(prefix):
        o = E(f"(window.__nml.game.currentNode()?.options||[]).find(o=>o.label.startsWith({json.dumps(prefix)}))")
        if not o: return False
        E(f"window.__nml.game.choose({o['index']})"); time.sleep(0.2); return True
    def cap(n): time.sleep(0.6); pg.screenshot(path=OUT + n + '.png')
    def barrage_ouvert():
        r = E("(()=>{const d=window.__nml.game.doorById('a_sud');return (d.conditions||[]).every(c=>c.test(window.__nml.state))})()"); return r
    # accueil
    setup(); talk(); L = labels()
    check('accueil : texte d\'Ocre, Payer 20, [Discours], [Intimider], ruelle', text().startswith('Vingt crédits pour passer') and L[0] == 'Payer 20 cr.' and any(l.startswith('[Discours]') for l in L) and any(l.startswith('[Intimider]') for l in L) and 'Et si je ne paie pas ?' in L, L)
    cap('01_accueil')
    # Discours >= 4 : passage gratuit (parole 30 -> score 3, jet +1)
    rng(1); pick('[Discours]'); n = node(); cap('02_discours_ok'); pick('Au revoir'); s = st()
    check('Discours 3 + 1 = 4 : « T\'as pas tort », passage gratuit', n == 'parle_ok' and s['flags'].get('cl_barrage') and s['player']['credits'] == 25 and barrage_ouvert(), (n, s['player']['credits']))
    # Discours exactement 3 : dix crédits
    setup(); talk(); rng(0); pick('[Discours]'); n = node(); cap('03_discours_dix'); pick('Payer 10'); s = st()
    check('Discours total 3 : « Dix, et on n\'en parle plus », payer 10 cr', n == 'dix' and s['flags'].get('cl_barrage') and s['player']['credits'] == 15, (n, s['player']['credits']))
    setup(); talk(); rng(0); pick('[Discours]'); pick('Au revoir'); talk(); L = labels()
    check('prix de 10 mémorisé (cl_barrage_10) ; un seul essai : Discours et Intimider masqués', st()['flags'].get('cl_barrage_10') and 'Payer 10 cr.' in L and 'Payer 20 cr.' not in L and not any(l.startswith('[') for l in L), (text(), L))
    E("window.__nml.state.player.credits=5"); pick('Payer 10'); check('10 cr sans les avoir : « Dix. Pas neuf. »', node() == 'pauvre10' and not st()['flags'].get('cl_barrage'), node())
    # Discours < 3 : vingt
    setup(); talk(); rng(-1); pick('[Discours]'); n = node(); pick('Payer 20'); s = st()
    check('Discours total 2 : « Vingt. », prix inchangé (20 cr)', n == 'parle_rate' and s['flags'].get('cl_barrage') and s['player']['credits'] == 5, (n, s['player']['credits']))
    # Intimider : jet opposé (max(Charisme, Force) + jet) contre (Volonté 4 + jet)
    setup(cha=6); talk(); rng(0, 0); pick('[Intimider]'); n = node(); cap('04_intimider_ok'); pick('Au revoir'); s = st()
    check('Intimider 6 contre 4 : « Ça va, ça va… Entre. », passage gratuit', n == 'peur_ok' and s['flags'].get('cl_barrage') and s['player']['credits'] == 25 and barrage_ouvert(), n)
    setup(force=5, cha=2); talk(); rng(0, 0); pick('[Intimider]'); check('Intimider prend la Force si elle dépasse le Charisme (5 contre 4)', node() == 'peur_ok', node())
    setup(cha=4); talk(); rng(0, 0); pick('[Intimider]'); check('égalité (4 contre 4) : échec, le PNJ gagne', node() == 'trente', node())
    setup(cha=6); talk(); rng(-2, 2); pick('[Intimider]'); n = node(); cap('05_intimider_trente'); pick('Au revoir'); s = st()
    check('Intimider raté (4 contre 6) : « Joli numéro. Maintenant c\'est trente. », cl_barrage_30', n == 'trente' and s['flags'].get('cl_barrage_30') and not s['flags'].get('cl_barrage'), n)
    talk(); L = labels(); check('retour : « Toujours trente », Payer 30 seulement, plus d\'essai', text().startswith('Toujours trente') and 'Payer 30 cr.' in L and 'Payer 20 cr.' not in L and not any(l.startswith('[') for l in L), (text(), L))
    E("window.__nml.state.player.credits=29"); pick('Payer 30'); n = node(); cap('06_pauvre30'); L = labels()
    check('29 cr : « Trente. Pas vingt-neuf. Reviens. » et renvoi vers la ruelle', n == 'pauvre30' and 'Il y a pas un autre chemin ?' in L, (n, L))
    pick('Il y a pas un autre chemin'); check('pauvre30 -> ruelle de Lower-Town (réplique non)', node() == 'non' and 'Lower-Town' in text(), text())
    E("window.__nml.state.player.credits=30"); E("window.__nml.state.dialogue=null"); talk(); pick('Payer 30'); s = st()
    check('payer 30 cr : passage', s['flags'].get('cl_barrage') and s['player']['credits'] == 0 and barrage_ouvert(), s['player']['credits'])
    setup(cr=40, cha=6); talk(); rng(-2, 2); pick('[Intimider]'); pick('Payer 30'); s = st()
    check('trente payé tout de suite (40 -> 10 cr)', s['flags'].get('cl_barrage') and s['player']['credits'] == 10, s['player']['credits'])
    # barrage fermé sans payer ; la ruelle (passages obligatoires) reste sans condition
    setup(); check('Barrage fermé sans cl_barrage', not barrage_ouvert())
    check('ruelle et passages obligatoires toujours gratuits', E("['a_nord','a_escalier','c_sud_est','l_sud'].every(id=>!(window.__nml.game.doorById(id).conditions||[]).length)"))
    check('aucune erreur JS', not errs, errs[:3])
    br.close()
json.dump(R, open(OUT + 'results.json', 'w'), ensure_ascii=False, indent=1)
bad = [r for r in R if not r['ok']]; print(f'{len(R) - len(bad)}/{len(R)} OK'); sys.exit(1 if bad else 0)
