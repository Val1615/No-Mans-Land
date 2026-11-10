#!/usr/bin/env python3
"""Construit _site/ pour GitHub Pages : uniquement ce que le jeu et l'éditeur servent.

Inclus : index.html, .nojekyll, src/, vendor/, editor/, assets/ et les .md de premier niveau de docs/ (liés depuis l'éditeur).
Exclus : tests/, reference/, art-gen/, sous-dossiers de docs/ (captures, planches), scripts tools_*.py,
et, dans assets/, tous les fichiers des entrées marquées "obsolete" dans les manifestes ainsi que leurs calques
(entrées couche_de / neon / fenetres / ecran ... d'une entrée obsolete), sauf si une entrée active pointe sur le même fichier.
Les fichiers restent dans le repo : seul l'artefact Pages est allégé.
"""
import json, os, re, shutil, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, '_site')
CALQUES = ('neon', 'fenetres', 'ecran', 'pulse', 'pulse_b', 'pulse2', 'faisceau', 'faisceau_fix', 'mobile')
# Seuls les manifestes des quartiers de Steel sont filtrés par src/core/catalogue.js (obsolete exclus) ; les autres
# (buildings, reused, interiors...) sont chargés entiers par le jeu, leurs fichiers obsolete restent donc servis.
FILTRES = os.path.join(ROOT, 'assets', 'steel')

def manifest_files(path):
    d = os.path.dirname(path); m = json.load(open(path, encoding='utf-8'))
    if not isinstance(m, dict): return {}, set(), set()
    ents = {k: v for k, v in m.items() if isinstance(v, dict)}
    base = {k for k, v in ents.items() if v.get('obsolete')}
    obs = set(base)
    for k, v in ents.items():  # calques d'une entrée obsolete (pas les calques _fix d'un calque obsolete d'une entrée active)
        if v.get('couche_de') in base or v.get('parent') in base or any(k == o + '_' + c for o in base for c in CALQUES): obs.add(k)
    for o in base:
        for f in CALQUES:
            ref = ents[o].get(f)
            if isinstance(ref, str) and ref in ents: obs.add(ref)
    def fichier(k, v):
        f = v.get('file')
        if not isinstance(f, str): return None
        for base in (os.path.join(ROOT, 'assets'), d):
            p = os.path.normpath(os.path.join(base, f))
            if os.path.isfile(p): return p
        return None
    files = {k: fichier(k, v) for k, v in ents.items()}
    dead = {files[k] for k in obs if files[k]}
    live = {files[k] for k in ents if k not in obs and files[k]}
    return files, dead, live

dead, live = set(), set()
for dp, dn, fn in os.walk(os.path.join(ROOT, 'assets')):
    for f in fn:
        if f == 'manifest.json' and os.path.normpath(dp).startswith(FILTRES):
            _, d_, l_ = manifest_files(os.path.join(dp, f)); dead |= d_; live |= l_
exclus = dead - live

if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
for f in ('index.html', '.nojekyll'):
    if os.path.exists(os.path.join(ROOT, f)): shutil.copy2(os.path.join(ROOT, f), OUT)
for d in ('src', 'vendor', 'editor'):
    shutil.copytree(os.path.join(ROOT, d), os.path.join(OUT, d), ignore=shutil.ignore_patterns('__pycache__'))
shutil.copytree(os.path.join(ROOT, 'assets'), os.path.join(OUT, 'assets'),
                ignore=lambda dp, names: [n for n in names if os.path.normpath(os.path.join(dp, n)) in exclus or n == '__pycache__'])
os.makedirs(os.path.join(OUT, 'docs'))
for f in os.listdir(os.path.join(ROOT, 'docs')):
    if f.endswith('.md') and os.path.isfile(os.path.join(ROOT, 'docs', f)): shutil.copy2(os.path.join(ROOT, 'docs', f), os.path.join(OUT, 'docs'))
taille = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fn in os.walk(OUT) for f in fn)
nb = sum(len(fn) for _, _, fn in os.walk(OUT))
print(f'_site : {nb} fichiers, {taille / 1e6:.1f} Mo ; {len(exclus)} fichiers d\'assets obsolete exclus')
with open(os.path.join(ROOT, '_site_exclus.txt') if len(sys.argv) > 2 else os.devnull, 'w') as fh:
    fh.write('\n'.join(sorted(os.path.relpath(p, ROOT) for p in exclus)) + '\n')
