// Lot 3 : voyage dans les No Man's Land, case par case (à la Fallout 1 et 2). Aucune dépendance au rendu.
// État durable dans game.state.region (sauvegardé avec la partie) : case du marqueur, statut, destination, trajet restant, brouillard.
//   statut : 'lieu' (dans un grand lieu jouable), 'depart' (sortie régionale prise, carte ouverte, rien parcouru),
//            'route' (en marche), 'halte' (arrêt, trajet restant conservé pour la reprise).
import * as D from '../data/nml.js';

const K = (c, r) => c + ',' + r;
// Point d'accroche à chaque case entrée : tirage (probabilité du terrain) contre la table d'événements (vide pour l'instant).
// Rend l'événement tiré ou null. Remplaçable (voyage.crochets.onCaseEntree) pour brancher les rencontres plus tard.
export function onCaseEntree(c, etat, { rng = Math.random, table = D.EVENEMENTS_ROUTE, terrains = D.TERRAINS } = {}) {
  const t = terrains[c.terrain], tirage = rng();
  if (!t || tirage >= t.p) return null;
  const pool = table.filter(e => (!e.terrains || e.terrains.includes(c.terrain)) && (!e.si || e.si(etat))); if (!pool.length) return null;
  let w = pool.reduce((a, e) => a + (e.poids || 1), 0) * rng(); for (const e of pool) { w -= e.poids || 1; if (w <= 0) return e; } return pool[pool.length - 1];
}

export function createVoyage({ game, manifest, data = D, rng = () => Math.random() }) {
  const { TERRAINS, BIOME_TERRAIN, PISTES_MAQUETTE, LIEUX_JEU, LIEUX_CONNUS_DEPART, HEURE_DEPART, RAYON_VUE } = data;
  const N = manifest.nml_fond, G = N.grille, cells = new Map();
  for (const c of N.cases) cells.set(K(c.col, c.row), { col: c.col, row: c.row, label: c.label, biome: c.biome, piste: false });
  // pistes : polylignes de la maquette (unités, 50 par case) échantillonnées tous les 2 unités
  for (const p of PISTES_MAQUETTE) for (let i = 1; i < p.length; i++) { const [a, b] = [p[i - 1], p[i]], L = Math.hypot(b[0] - a[0], b[1] - a[1]);
    for (let d = 0; d <= L; d += 2) { const x = a[0] + (b[0] - a[0]) * d / L, y = a[1] + (b[1] - a[1]) * d / L, c = cells.get(K(Math.floor(x / 50), Math.floor(y / 50))); if (c) c.piste = true; } }
  for (const c of cells.values()) c.terrain = c.piste ? 'piste' : BIOME_TERRAIN[c.biome];
  const lieux = Object.entries(N.lieux).map(([key, l]) => ({ key, nom: l.nom, col: l.case[0], row: l.case[1], px: l.px, jeu: LIEUX_JEU[key] || null }));
  const cellAt = (c, r) => cells.get(K(c, r)) || null, lieuAt = (c, r) => lieux.find(l => l.col === c && l.row === r) || null;
  const heures = c => TERRAINS[c.terrain].h;
  // Dijkstra 8 voisins ; la diagonale ne coupe pas un angle de mer (règle de la maquette). Coût = heures de la case entrée.
  function chemin(a, b) {
    const s = cellAt(a.col, a.row), t = cellAt(b.col, b.row); if (!s || !t || s === t) return [];
    const dist = new Map([[s, 0]]), prev = new Map(), open = [s], done = new Set();
    while (open.length) { open.sort((x, y) => dist.get(x) - dist.get(y)); const p = open.shift(); if (done.has(p)) continue; done.add(p); if (p === t) break;
      for (let dc = -1; dc <= 1; dc++) for (let dr = -1; dr <= 1; dr++) { if (!dc && !dr) continue; const n = cellAt(p.col + dc, p.row + dr); if (!n || done.has(n)) continue;
        if (dc && dr && (!cellAt(p.col + dc, p.row) || !cellAt(p.col, p.row + dr))) continue;
        const d = dist.get(p) + heures(n) + (dc && dr ? 1e-3 : 0); if (d < (dist.get(n) ?? Infinity)) { dist.set(n, d); prev.set(n, p); open.push(n); } } }
    if (!prev.has(t)) return []; const out = []; for (let n = t; n !== s; n = prev.get(n)) out.unshift(n); return out;
  }
  const S = () => game.state;
  const lieuDuLieuJeu = loc => { const w = game.world, L = w.LOCATIONS[loc]; let e = loc;
    if (L?.kind === 'interior') for (const d of w.DOORS) if (d.location === loc && d.target) { const t = w.DOORS.find(x => x.id === d.target.doorId); if (t && w.LOCATIONS[t.location]?.kind !== 'interior') { e = t.location; break; } }
    return lieux.find(l => l.jeu && l.jeu.prefixe && e.startsWith(l.jeu.prefixe))?.key || 'steel'; };
  function voir(c, r) { const R = S().region, v = new Set(R.vues); for (let dc = -RAYON_VUE; dc <= RAYON_VUE; dc++) for (let dr = -RAYON_VUE; dr <= RAYON_VUE; dr++) v.add(K(c + dc, r + dr));
    R.vues = [...v]; } // le brouillard se dissipe ; un grand lieu ne devient connu qu'en entrant sur sa case
  function region() { // état régional, recréé depuis le lieu courant si absent (nouvelle partie, ancienne sauvegarde)
    const s = S(); if (s.heures == null) s.heures = HEURE_DEPART;
    if (!s.region || !s.region.case) { const k = lieuDuLieuJeu(s.location), l = lieux.find(x => x.key === k);
      s.region = { case: [l.col, l.row], statut: 'lieu', lieu: k, dest: null, trajet: [], sortie: null, connus: {}, vues: [], visitees: [K(l.col, l.row)], parcours: [] };
      for (const key of LIEUX_CONNUS_DEPART) { const q = lieux.find(x => x.key === key); s.region.connus[key] = true; voir(q.col, q.row); } }
    return s.region; }
  const listeners = new Set(), emit = ev => listeners.forEach(f => f(ev));
  let prog = 0; // avancée (0..1) dans la case en cours d'entrée (animation, non sauvegardée)
  const api = {
    cells, lieux, cellAt, lieuAt, chemin, heures, region, crochets: { onCaseEntree: (c, etat) => onCaseEntree(c, etat, { rng }) }, appels: 0,
    on: f => listeners.add(f), get prog() { return prog; },
    // sortie régionale franchie (porte marquée regional) : la carte s'ouvre, destination proposée
    sortie(door) { const R = region(), k = lieuDuLieuJeu(door.location), l = lieux.find(x => x.key === k);
      Object.assign(R, { case: [l.col, l.row], statut: 'depart', lieu: k, sortie: door.id, trajet: [], dest: null });
      if (door.vers) api.viser({ lieu: door.vers }); // destination proposée : l'autre bout de la route
      emit({ type: 'ouvrir', raison: 'sortie' }); },
    // destination : { lieu: clé } ou { case: [col, row] } ; calcule le trajet sans partir
    viser(dest) { const R = region(); if (R.statut === 'lieu') return { ok: false, reason: 'en_ville' };
      const l = dest.lieu && lieux.find(x => x.key === dest.lieu), [c, r] = l ? [l.col, l.row] : dest.case || [];
      if (!cellAt(c, r)) return { ok: false, reason: 'mer' };
      const p = chemin({ col: R.case[0], row: R.case[1] }, { col: c, row: r }); R.dest = l ? { lieu: l.key } : { case: [c, r] }; R.trajet = p.map(x => [x.col, x.row]);
      return { ok: true, cases: p.length, heures: p.reduce((a, x) => a + heures(x), 0) }; },
    partir(dest) { const R = region(); if (dest) { const v = api.viser(dest); if (!v.ok) return v; }
      if (!R.trajet.length) { if (R.dest && api.lieuJouableIci()) return api.entrer(); return { ok: false, reason: 'trajet_vide' }; }
      R.statut = 'route'; prog = 0; emit({ type: 'depart' }); return { ok: true }; },
    halte() { const R = region(); if (R.statut !== 'route') return { ok: false }; R.statut = 'halte'; prog = 0; emit({ type: 'halte' }); return { ok: true }; },
    reprendre() { const R = region(); if (R.statut !== 'halte' || !R.trajet.length) return { ok: false }; R.statut = 'route'; prog = 0; emit({ type: 'reprise' }); return { ok: true }; },
    lieuJouableIci() { const R = region(), l = lieuAt(R.case[0], R.case[1]); return l && l.jeu ? l : null; },
    // entrer dans le grand lieu jouable de la case (arrivée, ou halte sur sa case) : chargement du lieu
    entrer() { const R = region(), l = api.lieuJouableIci(); if (!l || R.statut === 'route' || R.statut === 'lieu') return { ok: false };
      game.arriveVia(l.jeu.entree, R.sortie); Object.assign(R, { statut: 'lieu', lieu: l.key, dest: null, trajet: [], sortie: null }); prog = 0; emit({ type: 'arrivee', lieu: l.key }); return { ok: true }; },
    // fermer la carte au départ (rien parcouru) : on reste en ville, sur la sortie
    annuler() { const R = region(); if (R.statut !== 'depart') return { ok: false }; Object.assign(R, { statut: 'lieu', dest: null, trajet: [], sortie: null }); emit({ type: 'annule' }); return { ok: true }; },
    // une case entrée : temps, brouillard, crochet ; arrivée à la destination
    pas() { const R = region(); if (R.statut !== 'route' || !R.trajet.length) return null;
      const [c, r] = R.trajet.shift(), cell = cellAt(c, r), h = heures(cell); R.case = [c, r]; S().heures += h; R.parcours.push(K(c, r)); if (R.parcours.length > 400) R.parcours.shift();
      if (!R.visitees.includes(K(c, r))) R.visitees.push(K(c, r)); voir(c, r); { const lc = lieuAt(c, r); if (lc) R.connus[lc.key] = true; }
      api.appels++; const ev = api.crochets.onCaseEntree({ col: c, row: r, label: cell.label, terrain: cell.terrain, biome: cell.biome, heures: h, lieu: lieuAt(c, r)?.key || null }, S());
      emit({ type: 'case', col: c, row: r, terrain: cell.terrain, heures: h, evenement: ev });
      if (ev) { R.statut = 'halte'; emit({ type: 'evenement', evenement: ev }); return ev; }
      if (!R.trajet.length) { const l = lieuAt(c, r), visé = R.dest?.lieu;
        if (l && l.jeu && (!visé || visé === l.key)) { R.statut = 'halte'; api.entrer(); } else { R.statut = 'halte'; emit({ type: 'arret', lieu: l?.key || null }); } }
      return cell; },
    tick(ms, pasMs = data.VOYAGE_PAS_MS) { const R = region(); if (R.statut !== 'route') return; prog += ms / pasMs; while (prog >= 1 && R.statut === 'route') { prog -= 1; api.pas(); } if (R.statut !== 'route') prog = 0; },
    // après chargement : une partie sauvegardée en marche reprend en halte sur la dernière case parcourue, trajet conservé
    restaure() { const R = region(); if (R.statut === 'route') R.statut = 'halte'; prog = 0; },
    heureTexte() { const h = Math.round(S().heures ?? HEURE_DEPART); return `Jour ${Math.floor(h / 24) + 1} · ${String(h % 24).padStart(2, '0')} h`; },
  };
  for (const [key, l] of Object.entries(LIEUX_JEU)) for (const id of l.sorties) { const d = game.doorById(id); if (d) { d.regional = key; d.vers = Object.keys(LIEUX_JEU).find(k => k !== key && LIEUX_JEU[k].entree === d.target?.doorId) || null; } }
  game.onRegional(d => api.sortie(d));
  return api;
}
