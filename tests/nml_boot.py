# Aide commune des tests : sauter la séquence d'allumage du menu Terminal (un geste pendant l'allumage ne fait que la sauter).
# Usage : passer_boot(pg) ou passer_boot(E) juste avant le premier clic sur #m-new.
SAUTE_JS = """async () => { for (let i = 0; i < 1200 && !(window.__nml && window.__nml.shell && window.__nml.shell.terminal); i++) await new Promise(r => setTimeout(r, 50));
  const t = window.__nml && window.__nml.shell && window.__nml.shell.terminal; if (t) t.saute(); return !!t; }"""
def passer_boot(pg_ou_E):
    import time
    ev = pg_ou_E.evaluate if hasattr(pg_ou_E, 'evaluate') else pg_ou_E
    ok = ev(SAUTE_JS); time.sleep(0.15); return ok
