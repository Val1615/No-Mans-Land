import { UNITS } from '../data/units.js';
import { buildGrid } from './grid.js';
import { findPath } from './path.js';

// État sérialisable + commandes à résultat typé. Aucune dépendance au rendu.
export function createGame(world, sprites) {
  const { LOCATIONS, DOORS, NPCS = [], DIALOGUES = {}, ITEMS = {}, START, COMPANION } = world;
  const npcBox = n => ({ x: n.x - 0.3, z: n.z - 0.3, w: 0.6, d: 0.6 });
  const grids = Object.fromEntries(Object.keys(LOCATIONS).map(k => [k, buildGrid(LOCATIONS[k], DOORS, sprites, NPCS.filter(n => n.location === k).map(npcBox))]));
  const L0 = LOCATIONS[START.location], sp = L0.spawn;
  const state = {
    location: START.location,
    player: { x: sp.player.x, z: sp.player.z, path: [], pending: null, hp: START.hp, maxHp: START.maxHp, money: START.money, inv: {} },
    // v10 : Nilo retiré du début (décision). Son code reste : COMPANION.enabled = true le réactivera (future quête).
    companion: COMPANION?.enabled ? { x: sp.companion.x, z: sp.companion.z, path: [], mode: 'follow', location: START.location, name: COMPANION?.name }
                                  : { x: -99, z: -99, path: [], mode: 'absent', location: '_none', name: COMPANION?.name },
    dialogue: null, flags: {}, discovered: {}, seen: {}, junctionLock: null,
    npcs: Object.fromEntries(NPCS.map(n => [n.id, { heading: n.faceTo ? Math.atan2(n.faceTo[0] - n.x, n.faceTo[1] - n.z) : 0 }])), log: [], transitions: 0
  };
  const listeners = new Set();
  const emit = ev => { state.log.push(ev); if (state.log.length > 80) state.log.shift(); listeners.forEach(f => f(ev)); };
  const grid = () => grids[state.location];
  const doorById = id => DOORS.find(d => d.id === id);
  const doorOfBuilding = bid => DOORS.filter(d => d.buildingId === bid && d.location === state.location).sort((a, b) => Math.hypot(a.threshold.x - state.player.x, a.threshold.z - state.player.z) - Math.hypot(b.threshold.x - state.player.x, b.threshold.z - state.player.z))[0];
  const npcById = id => NPCS.find(n => n.id === id);
  const refuse = (reason, text) => { if (typeof text === 'function') text = text(state); /* v14 : texte selon l'état */ emit({ type: 'refus', reason, text }); return { ok: false, reason }; };
  const busy = () => state.dialogue ? refuse('dialogue_ouvert', 'Termine la conversation d\'abord.') : null;

  function moveTo(x, z) {
    const b = busy(); if (b) return b;
    state.player.pending = null;
    const g = grid(); let [i, j] = g.toCell(x, z);
    if (!g.free(i, j)) { // case occupée : on vise la case libre la plus proche (1,5 m max), sinon refus explicite
      let best = null, bd = Infinity;
      for (let di = -3; di <= 3; di++) for (let dj = -3; dj <= 3; dj++) if (g.free(i + di, j + dj)) {
        const w = g.toWorld(i + di, j + dj), d = Math.hypot(w.x - x, w.z - z); if (d < bd) { bd = d; best = w; } }
      if (best) ({ x, z } = best);
    }
    const p = findPath(g, state.player, { x, z });
    if (!p) return refuse('chemin_bloque', 'Impossible d\'aller là.');
    state.player.path = p.slice(1); return { ok: true };
  }
  function goThen(target, pending) {
    if (Math.hypot(state.player.x - target.x, state.player.z - target.z) < 0.05) { state.player.pending = pending; finishPending(); return { ok: true }; }
    const p = findPath(grid(), state.player, target);
    if (!p) return null;
    state.player.path = p.slice(1); state.player.pending = pending; return { ok: true, pending: true };
  }
  // Commande d'accès unique, quel que soit le geste.
  function useDoor(doorId) {
    const b = busy(); if (b) return b;
    const door = doorById(doorId);
    if (!door || door.location !== state.location) return refuse('porte_absente', 'Aucune porte ici.');
    for (const c of door.conditions) if (!c.test(state)) return refuse(c.reason, c.text);
    return goThen(door.threshold, { kind: 'door', id: doorId }) || refuse('chemin_bloque', 'Le seuil est inaccessible.');
  }
  function talkTo(npcId) {
    const b = busy(); if (b) return b;
    const n = npcById(npcId);
    if (!n || n.location !== state.location) return refuse('absent', 'Personne ici.');
    const g = grid(); const [ci, cj] = g.toCell(n.x, n.z); let best = null, bd = Infinity;
    for (let di = -5; di <= 5; di++) for (let dj = -5; dj <= 5; dj++) {
      if (!g.free(ci + di, cj + dj)) continue; const w = g.toWorld(ci + di, cj + dj);
      if (Math.hypot(w.x - n.x, w.z - n.z) > 2.6) continue;
      const d = Math.hypot(w.x - state.player.x, w.z - state.player.z); if (d < bd) { bd = d; best = w; }
    }
    if (!best) return refuse('chemin_bloque', 'Impossible d\'approcher.');
    return goThen(best, { kind: 'talk', id: npcId }) || refuse('chemin_bloque', 'Impossible d\'approcher.');
  }
  function finishPending() {
    const p = state.player.pending; state.player.pending = null; if (!p) return;
    if (p.kind === 'door') { const d = doorById(p.id), bad = (d.conditions || []).find(c => !c.test(state)); if (d.edge || bad) { state.junctionLock = d.id; refuse(bad ? bad.reason : 'bord', bad ? bad.text : d.edge); } else enter(d); }
    if (p.kind === 'talk') openDialogue(p.id);
    if (p.kind === 'scene') openDialogue(p.id);
  }
  // v9 : scène sans PNJ visible (ex. la voix derrière la porte d'acier) : marcher jusqu'au point, puis ouvrir le dialogue
  function startScene(npcId, at) {
    const b = busy(); if (b) return b;
    return goThen(at, { kind: 'scene', id: npcId }) || refuse('chemin_bloque', 'Impossible d\'approcher.');
  }
  function openDialogue(npcId) {
    const n = npcById(npcId);
    state.dialogue = { npc: npcId, node: 'start' };
    state.player.heading = Math.atan2(n.x - state.player.x, n.z - state.player.z);
    state.npcs[npcId].heading = Math.atan2(state.player.x - n.x, state.player.z - n.z); // le PNJ se tourne vers le joueur
    emit({ type: 'dialogue_open', npc: npcId });
  }
  function currentNode() {
    if (!state.dialogue) return null;
    const tree = DIALOGUES[npcById(state.dialogue.npc).dialogue]; const node = tree[state.dialogue.node];
    const alt = (node.alt || []).find(a => cond(a.if));
    return { npc: npcById(state.dialogue.npc), text: alt ? alt.text : node.text,
      options: node.options.map((o, i) => ({ ...o, index: i })).filter(o => !o.if || cond(o.if)) };
  }
  // v9 : conditions composées « a&!b » ; « hurt » = blessé
  const cond1 = c => c.startsWith('!') ? !cond1(c.slice(1)) : c === 'hurt' ? state.player.hp < state.player.maxHp : !!state.flags[c];
  const cond = c => c.split('&').every(cond1);
  function choose(index) {
    const node = currentNode(); if (!node) return { ok: false };
    const opt = node.options.find(o => o.index === index); if (!opt) return { ok: false };
    let next = opt.next;
    if (opt.action) { // v9 : plusieurs actions « a;b », on s'arrête au premier refus (pas assez de $)
      const acts = opt.action.split(';');
      if (acts.some(a => /^(buy|pay|heal)/.test(a))) { const cost = acts.reduce((t, a) => t + (/^(pay|heal)/.test(a) ? +a.split(':')[1] : /^buy/.test(a) ? +a.split(':')[2] : 0), 0);
        if (state.player.money < cost) { next = 'pauvre'; acts.length = 0; } }
      for (const a of acts) { const r = act(a); if (!r.ok) { next = r.next || next; break; } } }
    if (!next || next === 'end') { closeDialogue(); return { ok: true, closed: true }; }
    state.dialogue.node = next; return { ok: true };
  }
  function act(a) {
    const [k, x, y] = a.split(':'), pl = state.player;
    if (k === 'reveal') { if (!state.discovered[x]) { state.discovered[x] = true; emit({ type: 'discover', building: x, how: 'dialogue', text: 'Lieu repéré.' }); } return { ok: true }; }
    if (k === 'flag') { state.flags[x] = true; emit({ type: 'flag', flag: x, text: x.startsWith('q_') ? 'Journal : quête mise à jour.' : 'Journal : piste notée.' }); return { ok: true }; }
    if (k === 'pay') { const cost = +x; if (pl.money < cost) return { ok: false, next: 'pauvre' }; pl.money -= cost; emit({ type: 'service', what: 'pay', text: `−${cost} $` }); return { ok: true }; }
    if (k === 'heal') { const cost = +x; if (pl.money < cost) return { ok: false, next: 'pauvre' };
      pl.money -= cost; pl.hp = Math.min(pl.maxHp, pl.hp + Math.ceil((pl.maxHp - pl.hp) * (state.character?.effects?.healFactor ?? 1))); emit({ type: 'service', what: 'heal', text: `Soigné. −${cost} $` }); return { ok: true }; }
    if (k === 'buy') { const cost = +y, it = ITEMS[x]; if (pl.money < cost) return { ok: false, next: 'pauvre' };
      pl.money -= cost;
      if (it.consumeNow) pl.hp = Math.min(pl.maxHp, pl.hp + (it.heal || 0)); else pl.inv[x] = (pl.inv[x] || 0) + 1;
      emit({ type: 'service', what: x, text: `${it.name} : −${cost} $` }); return { ok: true }; }
    if (k === 'hurt') { pl.hp = Math.max(1, pl.hp - +x); emit({ type: 'hurt', text: `−${x} PV` }); return { ok: true }; }
    // v12 : change dollars -> crédits (Steel) ; « change:20:11 » = 20 $ contre 11 cr
    if (k === 'change') { const cost = +x; if (pl.money < cost) return { ok: false, next: 'pauvre' }; pl.money -= cost; pl.credits = (pl.credits || 0) + +y; emit({ type: 'service', what: 'change', text: `−${cost} $ · +${y} cr` }); return { ok: true }; }
    // v12 : déplacement scripté (fuite, capture) : « warp:lieu:x:z » ; compte comme un changement de lieu
    if (k === 'warp') { const [, loc, wx, wz] = a.split(':'); if (!LOCATIONS[loc]) return { ok: false }; const from = state.location;
      state.location = loc; Object.assign(pl, { x: +wx, z: +wz, path: [], pending: null }); const g = grids[loc], [i, j] = g.toCell(pl.x, pl.z); if (!g.free(i, j)) { const w = nearestFree(g, pl, pl); if (w) Object.assign(pl, w); }
      state.junctionLock = null; state.transitions++; emit({ type: 'transition', from, to: loc, warp: true }); return { ok: true }; }
    // v12 : crochet pour un système futur (combat) : signalé, sans effet propre
    if (k === 'hook') { state.hooks = state.hooks || []; state.hooks.push(x); emit({ type: 'hook', id: x }); return { ok: true }; }
    return { ok: false };
  }
  function closeDialogue() { if (state.dialogue) { const n = npcById(state.dialogue.npc); if (n.faceTo) state.npcs[n.id].heading = Math.atan2(n.faceTo[0] - n.x, n.faceTo[1] - n.z); emit({ type: 'dialogue_close', npc: state.dialogue.npc }); state.dialogue = null; } }

  // Transition de groupe atomique.
  function enter(door) {
    const target = doorById(door.target.doorId), dest = target.location, c = state.companion;
    const withCompanion = c.mode === 'follow' && c.location === state.location && Math.hypot(c.x - state.player.x, c.z - state.player.z) <= (door.junction ? 8 : UNITS.companion.maxDoorDistance);
    state.junctionLock = target.junction ? target.id : null; // pas de rebond immédiat sur la jonction d'arrivée
    const t = target.threshold, o = target.opening, dl = Math.hypot(t.x - o.x, t.z - o.z) || 1, dir = { x: (t.x - o.x) / dl, z: (t.z - o.z) / dl };
    if (door.buildingId) state.discovered[door.buildingId] = true; // découverte en entrant
    state.location = dest; Object.assign(state.player, { x: t.x, z: t.z, path: [], pending: null });
    if (withCompanion) {
      const g = grids[dest]; let pos = null;
      for (const cand of [{ x: t.x + dir.x, z: t.z + dir.z }, { x: t.x + dir.z, z: t.z + dir.x }, { x: t.x - dir.z, z: t.z - dir.x }, { x: t.x + dir.x * 0.5 + 0.5, z: t.z + dir.z * 0.5 }]) {
        const [i, j] = g.toCell(cand.x, cand.z); if (g.free(i, j)) { pos = g.toWorld(i, j); break; } }
      pos = pos || { x: t.x, z: t.z };
      Object.assign(c, { x: pos.x, z: pos.z, path: [], location: dest });
    } else if (c.mode !== 'absent') c.mode = 'left_behind';
    state.transitions++;
    emit({ type: 'transition', from: door.location, to: dest, withCompanion, text: LOCATIONS[dest].name + (withCompanion || c.mode === 'absent' ? '' : ' (compagnon resté derrière)') });
  }

  function step(dt) {
    const pl = state.player, sp = UNITS.walkSpeed * dt;
    advance(pl, sp);
    if (!pl.path.length && pl.pending) finishPending();
    // Jonctions de rue : franchies dès que le joueur s'arrête sur le seuil (marche réelle).
    if (state.junctionLock) { const l = doorById(state.junctionLock); if (!l || l.location !== state.location || Math.hypot(l.threshold.x - pl.x, l.threshold.z - pl.z) > 1.5) state.junctionLock = null; }
    if (!pl.path.length && !state.dialogue) for (const d of DOORS) if ((d.junction || d.edge) && d.location === state.location && d.id !== state.junctionLock && Math.hypot(d.threshold.x - pl.x, d.threshold.z - pl.z) < 0.8) {
      const bad = (d.conditions || []).find(c => !c.test(state)); if (d.edge || bad) { state.junctionLock = d.id; refuse(bad ? bad.reason : 'bord', bad ? bad.text : d.edge); } else enter(d); break; }
    const c = state.companion;
    if (c.mode === 'follow' && c.location === state.location) {
      c._t = (c._t || 0) + dt;
      const dist = Math.hypot(c.x - pl.x, c.z - pl.z);
      if (dist > UNITS.companion.followDistance + 0.6 && (!c.path.length || c._t > 0.5)) {
        c._t = 0; const goal = nearestFree(grid(), pl, c); const p = goal && findPath(grid(), c, goal); c.path = p ? p.slice(1) : [];
      }
      if (dist > UNITS.companion.followDistance) advance(c, sp * 1.15); else c.path = [];
    }
  }
  function advance(a, sp) {
    while (sp > 0 && a.path.length) {
      const n = a.path[0], dx = n.x - a.x, dz = n.z - a.z, d = Math.hypot(dx, dz);
      if (d > 1e-6) a.heading = Math.atan2(dx, dz);
      if (d <= sp) { a.x = n.x; a.z = n.z; a.path.shift(); sp -= d; } else { a.x += dx / d * sp; a.z += dz / d * sp; sp = 0; }
    }
  }
  // v10 : sauvegarde. Instantané de tout l'état durable (jamais chemins, attentes, dialogue en cours).
  function snapshot() {
    const p = state.player, c = state.companion;
    return JSON.parse(JSON.stringify({ location: state.location, player: { x: p.x, z: p.z, heading: p.heading || 0, hp: p.hp, maxHp: p.maxHp, money: p.money, credits: p.credits || 0, inv: p.inv },
      companion: { x: c.x, z: c.z, mode: c.mode, location: c.location }, flags: state.flags, discovered: state.discovered, seen: state.seen, transitions: state.transitions, character: state.character || null }));
  }
  function restore(snap, quiet) {
    if (!snap || !LOCATIONS[snap.location]) return false;
    closeDialogue();
    const p = state.player, sp0 = snap.player || {};
    state.location = snap.location;
    Object.assign(p, { x: +sp0.x || 0, z: +sp0.z || 0, heading: +sp0.heading || 0, hp: sp0.hp ?? START.hp, maxHp: sp0.maxHp ?? START.maxHp, money: sp0.money ?? START.money, credits: sp0.credits || 0, inv: { ...(sp0.inv || {}) }, path: [], pending: null });
    const g = grids[state.location], [i, j] = g.toCell(p.x, p.z); if (!g.free(i, j)) { const w = nearestFree(g, p, p); if (w) Object.assign(p, w); }
    Object.assign(state.companion, { ...(snap.companion || {}), path: [] });
    state.flags = { ...(snap.flags || {}) }; state.discovered = { ...(snap.discovered || {}) }; state.seen = { ...(snap.seen || {}) }; state.transitions = snap.transitions || 0;
    state.character = snap.character ? JSON.parse(JSON.stringify(snap.character)) : null; // v11 : personnage créé (lot 2)
    // pas de franchissement immédiat si l'on a sauvegardé sur un seuil de jonction
    const jd = DOORS.find(d => (d.junction || d.edge) && d.location === state.location && Math.hypot(d.threshold.x - p.x, d.threshold.z - p.z) < 1.5); state.junctionLock = jd ? jd.id : null;
    if (!quiet) emit({ type: 'restore', text: 'Partie chargée : ' + LOCATIONS[state.location].name });
    return true;
  }
  return { state, step, snapshot, restore, moveTo, useDoor, talkTo, startScene, cond, choose, closeDialogue, currentNode, doorOfBuilding, doorById, grids, world,
    on: f => listeners.add(f), get location() { return LOCATIONS[state.location]; } };
}
function nearestFree(g, target, from) {
  const [ti, tj] = g.toCell(target.x, target.z); let best = null, bd = Infinity;
  for (let r = 1; r <= 4 && !best; r++) for (let di = -r; di <= r; di++) for (let dj = -r; dj <= r; dj++) {
    if (Math.max(Math.abs(di), Math.abs(dj)) !== r || !g.free(ti + di, tj + dj)) continue;
    const w = g.toWorld(ti + di, tj + dj), d = Math.hypot(w.x - from.x, w.z - from.z); if (d < bd) { bd = d; best = w; }
  }
  return best;
}
