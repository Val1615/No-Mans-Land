// Combat C1 : machine à états pure (aucune dépendance au rendu). Voir src/data/combat.js et docs/design/COMBAT.md.
// state.combat = { id, phase: 'joueur'|'ennemi'|'fin', tour, ordre, actif, units, zone, issue } ; jamais sauvegardé (snapshot l'ignore).
import { COMBAT, ENCOUNTERS } from '../data/combat.js';
import { UNITS } from '../data/units.js';

export function createCombat(ctx) { // ctx = { state, grids, emit, act }
  const { state, emit } = ctx;
  const C = () => state.combat;
  const sub = () => ctx.grids[state.location];
  // case de 1 m libre si ses 4 sous-cases de 0,5 m le sont (COMBAT.md §5)
  const cellFree = (i, j) => { const g = sub(); return [[0, 0], [1, 0], [0, 1], [1, 1]].every(([a, b]) => g.free(2 * i + a, 2 * j + b)); };
  const inZone = (i, j) => { const z = C().zone; return i >= z.i0 && i <= z.i1 && j >= z.j0 && j <= z.j1; };
  const isExit = (i, j) => { const z = C().zone; return i === z.i0 || i === z.i1 || j === z.j0 || j === z.j1; };
  const unitAt = (i, j, except) => C().units.find(u => u.actif && u !== except && u.i === i && u.j === j);
  const walkable = (i, j, who) => inZone(i, j) && cellFree(i, j) && !unitAt(i, j, who);
  const cellOf = (x, z) => [Math.floor(x), Math.floor(z)];
  const center = (i, j) => ({ x: i + 0.5, z: j + 0.5 });
  const pa = half => Math.ceil(half / 2);
  // A* 8 directions sans couper les coins, coût 1 / 1,5 PA (demi-PA entiers : 2 / 3)
  function path(who, ti, tj) {
    if (!walkable(ti, tj, who)) return null;
    const key = (i, j) => i + ',' + j, open = new Map(), g = new Map(), came = new Map(), closed = new Set();
    const h = (i, j) => { const dx = Math.abs(i - ti), dz = Math.abs(j - tj); return COMBAT.coutOrtho * Math.abs(dx - dz) + COMBAT.coutDiag * Math.min(dx, dz); };
    const k0 = key(who.i, who.j); open.set(k0, [who.i, who.j, h(who.i, who.j)]); g.set(k0, 0);
    while (open.size) {
      let best = null; for (const [k, v] of open) if (!best || v[2] < best[1][2]) best = [k, v];
      const [k, [i, j]] = best; open.delete(k);
      if (i === ti && j === tj) { const cells = []; let c = k; while (c != null) { const [a, b] = c.split(',').map(Number); cells.push([a, b]); c = came.get(c); }
        cells.reverse(); return { cells, half: g.get(k), pa: pa(g.get(k)) }; }
      closed.add(k);
      for (let di = -1; di <= 1; di++) for (let dj = -1; dj <= 1; dj++) {
        if (!di && !dj) continue; const ni = i + di, nj = j + dj, nk = key(ni, nj);
        if (closed.has(nk) || !walkable(ni, nj, who)) continue;
        if (di && dj && (!walkable(i + di, j, who) || !walkable(i, j + dj, who))) continue;
        const ng = g.get(k) + (di && dj ? COMBAT.coutDiag : COMBAT.coutOrtho);
        if (ng < (g.get(nk) ?? Infinity)) { g.set(nk, ng); came.set(nk, k); open.set(nk, [ni, nj, ng + h(ni, nj)]); }
      }
    }
    return null;
  }
  // toutes les cases atteignables avec les PA restants (Dijkstra borné)
  function reachable(who = player()) {
    const out = new Map([[who.i + ',' + who.j, 0]]), q = [[who.i, who.j, 0]], max = who.pa * 2;
    while (q.length) { q.sort((a, b) => a[2] - b[2]); const [i, j, c] = q.shift();
      for (let di = -1; di <= 1; di++) for (let dj = -1; dj <= 1; dj++) { if (!di && !dj) continue; const ni = i + di, nj = j + dj, k = ni + ',' + nj;
        if (!walkable(ni, nj, who) || (di && dj && (!walkable(i + di, j, who) || !walkable(i, j + dj, who)))) continue;
        const nc = c + (di && dj ? COMBAT.coutDiag : COMBAT.coutOrtho); if (nc > max || nc >= (out.get(k) ?? Infinity)) continue; out.set(k, nc); q.push([ni, nj, nc]); } }
    return [...out].map(([k, c]) => { const [i, j] = k.split(',').map(Number); return { i, j, pa: pa(c) }; });
  }
  const player = () => C()?.units.find(u => u.joueur);
  const actif = () => C()?.units[C().actif];
  function start(id) {
    const E = ENCOUNTERS[id]; if (!E) return { ok: false, reason: 'combat_inconnu' };
    emit({ type: 'combat_autosave', id }); // main.js écrit l'autosave AVANT que le combat n'existe (COMBAT.md §1)
    const p = state.player, [pi, pj] = cellOf(p.x, p.z), R = COMBAT.zoneRayon;
    state.combat = { id, phase: 'joueur', tour: 1, actif: 0, issue: null, preview: null, zone: { i0: pi - R, i1: pi + R, j0: pj - R, j1: pj + R }, units: [] };
    const ch = state.character || {};
    const pu = { id: 'joueur', nom: ch.name || 'Toi', joueur: true, actif: true, i: pi, j: pj, x: pi + 0.5, z: pj + 0.5, path: [], paMax: ch.ap || 5, pa: ch.ap || 5, initiative: ch.initiative ?? 5 };
    if (!cellFree(pi, pj)) { const f = nearestFree(pi, pj); if (f) Object.assign(pu, { i: f[0], j: f[1], x: f[0] + 0.5, z: f[1] + 0.5 }); }
    state.combat.units.push(pu);
    for (const e of E.ennemis) { let [i, j] = [pu.i + e.dx, pu.j + e.dz]; if (!walkable(i, j, null)) { const f = nearestFree(i, j); if (f) [i, j] = f; }
      state.combat.units.push({ ...e, joueur: false, actif: true, i, j, x: i + 0.5, z: j + 0.5, path: [], paMax: e.pa, pa: e.pa, pvMax: e.pv }); }
    state.combat.units.sort((a, b) => b.initiative - a.initiative || (a.joueur ? -1 : 1)); // initiative décroissante ; égalité : le joueur d'abord
    Object.assign(p, { x: pu.x, z: pu.z, path: [], pending: null });
    emit({ type: 'combat_start', id, text: E.textes?.debut });
    beginTurn(); return { ok: true };
  }
  function nearestFree(i, j) { for (let r = 1; r <= 4; r++) for (let di = -r; di <= r; di++) for (let dj = -r; dj <= r; dj++) if (walkable(i + di, j + dj, null)) return [i + di, j + dj]; return null; }
  function beginTurn() {
    const c = C(), u = actif(); u.pa = u.paMax; c.phase = u.joueur ? 'joueur' : 'ennemi'; c.preview = null; c._ai = 0;
    if (!u.joueur && u.fuitTour && c.tour >= u.fuitTour) { u.actif = false; emit({ type: 'combat_fuite_ennemi', id: u.id, text: `${u.nom} s\u2019enfuit.` }); if (!checkEnd()) next(); return; }
    emit({ type: 'combat_tour', tour: c.tour, qui: u.id });
  }
  function next() {
    const c = C(); if (!c || c.phase === 'fin') return;
    let n = c.actif; for (let k = 0; k < c.units.length; k++) { n = (n + 1) % c.units.length; if (n === 0) c.tour++; if (c.units[n].actif) break; }
    c.actif = n; beginTurn();
  }
  function checkEnd() { if (!C().units.some(u => !u.joueur && u.actif)) { finish('victoire'); return true; } return false; }
  // --- commandes du joueur ---
  const mine = () => C() && C().phase === 'joueur' && actif()?.joueur && !player().path.length;
  function previewTo(x, z) { if (!mine()) return null; const [i, j] = cellOf(x, z), u = player(), p = path(u, i, j);
    C().preview = p ? { i, j, cells: p.cells, pa: p.pa, ok: p.pa <= u.pa } : { i, j, cells: [], pa: null, ok: false }; return C().preview; }
  function moveTo(x, z) {
    if (!mine()) return { ok: false, reason: 'pas_ton_tour' };
    const [i, j] = cellOf(x, z), u = player(), p = path(u, i, j);
    if (!p || p.cells.length < 2) return { ok: false, reason: 'case_inaccessible' };
    if (p.pa > u.pa) return { ok: false, reason: 'pa_insuffisants', cout: p.pa, pa: u.pa };
    u.pa -= p.pa; u.path = p.cells.slice(1).map(([a, b]) => center(a, b)); u.i = i; u.j = j; C().preview = null; C()._arrive = true;
    emit({ type: 'combat_move', qui: 'joueur', cout: p.pa }); return { ok: true, cout: p.pa, pa: u.pa };
  }
  function endTurn() { if (!mine()) return { ok: false, reason: 'pas_ton_tour' }; emit({ type: 'combat_fin_tour', tour: C().tour }); next(); return { ok: true }; }
  function surrender() { if (!mine()) return { ok: false, reason: 'pas_ton_tour' }; finish('reddition'); return { ok: true }; }
  // --- tour ennemi (C1 : avancer vers le joueur, frapper au contact d'un coup fixe ; IA réelle au lot C4) ---
  function aiStep() {
    const c = C(), u = actif(), pl = player();
    const adj = Math.max(Math.abs(u.i - pl.i), Math.abs(u.j - pl.j)) <= 1;
    if (adj && u.frappe && u.pa >= u.frappe.pa) { u.pa -= u.frappe.pa; const hp = state.player.hp; state.player.hp = Math.max(0, hp - u.frappe.degats);
      emit({ type: 'combat_frappe', qui: u.id, degats: u.frappe.degats, text: `${u.nom} frappe : \u2212${u.frappe.degats} PV` });
      if (state.player.hp <= 0) { finish('defaite'); return; } c._ai = 0.6; return; }
    if (!adj) { let best = null;
      for (let di = -1; di <= 1; di++) for (let dj = -1; dj <= 1; dj++) { if (!di && !dj) continue; const p = path(u, pl.i + di, pl.j + dj); if (p && (!best || p.half < best.half)) best = p; }
      if (best && best.cells.length > 1) { let half = 0, k = 1; // avance autant que les PA le permettent
        for (; k < best.cells.length; k++) { const [a, b] = best.cells[k], [pa0, pb0] = best.cells[k - 1]; const h = (a !== pa0 && b !== pb0) ? COMBAT.coutDiag : COMBAT.coutOrtho; if (pa(half + h) > u.pa) break; half += h; }
        if (k > 1) { u.pa -= pa(half); u.path = best.cells.slice(1, k).map(([a, b]) => center(a, b)); [u.i, u.j] = best.cells[k - 1]; emit({ type: 'combat_move', qui: u.id, cout: pa(half) }); return; } } }
    next();
  }
  function step(dt) {
    const c = C(); if (!c) return;
    const sp = UNITS.walkSpeed * dt, speed = state.combatSpeed || 1;
    for (const u of c.units) advance(u, sp * speed);
    const pu = player(); Object.assign(state.player, { x: pu.x, z: pu.z }); if (pu.heading !== undefined) state.player.heading = pu.heading;
    if (c.phase === 'fin') return;
    if (!pu.path.length && c._arrive) { c._arrive = false; if (isExit(pu.i, pu.j)) { finish('fuite'); return; } } // fuite : fin d'un déplacement sur une case de bord
    if (c.phase === 'ennemi' && !c.units.some(u => u.path.length)) { c._ai -= dt * speed; if (c._ai <= 0) aiStep(); }
  }
  function advance(a, sp) { while (sp > 0 && a.path.length) { const n = a.path[0], dx = n.x - a.x, dz = n.z - a.z, d = Math.hypot(dx, dz); if (d > 1e-6) a.heading = Math.atan2(dx, dz);
    if (d <= sp) { a.x = n.x; a.z = n.z; a.path.shift(); sp -= d; } else { a.x += dx / d * sp; a.z += dz / d * sp; sp = 0; } } }
  function finish(issue) {
    const c = C(), E = ENCOUNTERS[c.id]; c.phase = 'fin'; c.issue = issue;
    state.flags[`combat_${c.id}_${issue}`] = true;
    for (const a of (E.issues[issue] || '').split(';').filter(Boolean)) ctx.act(a);
    if (state.player.hp < COMBAT.pvMinApres) state.player.hp = COMBAT.pvMinApres;
    const pu = player(); Object.assign(state.player, { x: pu.i + 0.5, z: pu.j + 0.5, path: [], pending: null });
    emit({ type: 'combat_fin', id: c.id, issue, text: E.textes?.[issue] });
    state.combatLast = { id: c.id, issue, tour: c.tour }; state.combat = null;
  }
  return { start, previewTo, moveTo, endTurn, surrender, step, reachable, path: (i, j) => C() && path(player(), i, j), cellFree, isExit: (i, j) => C() && isExit(i, j), player, actif, finish };
}
