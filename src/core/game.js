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
    companion: { x: sp.companion.x, z: sp.companion.z, path: [], mode: 'follow', location: START.location, name: COMPANION?.name },
    dialogue: null, flags: {}, discovered: {},
    npcs: Object.fromEntries(NPCS.map(n => [n.id, { heading: n.faceTo ? Math.atan2(n.faceTo[0] - n.x, n.faceTo[1] - n.z) : 0 }])), log: [], transitions: 0
  };
  const listeners = new Set();
  const emit = ev => { state.log.push(ev); if (state.log.length > 80) state.log.shift(); listeners.forEach(f => f(ev)); };
  const grid = () => grids[state.location];
  const doorById = id => DOORS.find(d => d.id === id);
  const doorOfBuilding = bid => DOORS.find(d => d.buildingId === bid && d.location === state.location);
  const npcById = id => NPCS.find(n => n.id === id);
  const refuse = (reason, text) => { emit({ type: 'refus', reason, text }); return { ok: false, reason }; };
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
    if (p.kind === 'door') enter(doorById(p.id));
    if (p.kind === 'talk') openDialogue(p.id);
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
    return { npc: npcById(state.dialogue.npc), text: node.text,
      options: node.options.map((o, i) => ({ ...o, index: i })).filter(o => !o.if || cond(o.if)) };
  }
  const cond = c => c === 'hurt' ? state.player.hp < state.player.maxHp : !!state.flags[c];
  function choose(index) {
    const node = currentNode(); if (!node) return { ok: false };
    const opt = node.options.find(o => o.index === index); if (!opt) return { ok: false };
    let next = opt.next;
    if (opt.action) { const r = act(opt.action); if (!r.ok) next = r.next || next; }
    if (!next || next === 'end') { closeDialogue(); return { ok: true, closed: true }; }
    state.dialogue.node = next; return { ok: true };
  }
  function act(a) {
    const [k, x, y] = a.split(':'), pl = state.player;
    if (k === 'reveal') { if (!state.discovered[x]) { state.discovered[x] = true; emit({ type: 'discover', building: x, how: 'dialogue', text: 'Lieu repéré.' }); } return { ok: true }; }
    if (k === 'flag') { state.flags[x] = true; emit({ type: 'flag', flag: x, text: 'Journal : piste notée.' }); return { ok: true }; }
    if (k === 'heal') { const cost = +x; if (pl.money < cost) return { ok: false, next: 'pauvre' };
      pl.money -= cost; pl.hp = pl.maxHp; emit({ type: 'service', what: 'heal', text: `Soigné. −${cost} $` }); return { ok: true }; }
    if (k === 'buy') { const cost = +y, it = ITEMS[x]; if (pl.money < cost) return { ok: false, next: 'pauvre' };
      pl.money -= cost;
      if (it.consumeNow) pl.hp = Math.min(pl.maxHp, pl.hp + (it.heal || 0)); else pl.inv[x] = (pl.inv[x] || 0) + 1;
      emit({ type: 'service', what: x, text: `${it.name} : −${cost} $` }); return { ok: true }; }
    return { ok: false };
  }
  function closeDialogue() { if (state.dialogue) { const n = npcById(state.dialogue.npc); if (n.faceTo) state.npcs[n.id].heading = Math.atan2(n.faceTo[0] - n.x, n.faceTo[1] - n.z); emit({ type: 'dialogue_close', npc: state.dialogue.npc }); state.dialogue = null; } }

  // Transition de groupe atomique.
  function enter(door) {
    const target = doorById(door.target.doorId), dest = target.location, c = state.companion;
    const withCompanion = c.mode === 'follow' && Math.hypot(c.x - state.player.x, c.z - state.player.z) <= UNITS.companion.maxDoorDistance;
    const t = target.threshold, o = target.opening, dl = Math.hypot(t.x - o.x, t.z - o.z) || 1, dir = { x: (t.x - o.x) / dl, z: (t.z - o.z) / dl };
    if (door.buildingId) state.discovered[door.buildingId] = true; // découverte en entrant
    state.location = dest; Object.assign(state.player, { x: t.x, z: t.z, path: [], pending: null });
    if (withCompanion) {
      const g = grids[dest]; let pos = null;
      for (const cand of [{ x: t.x + dir.x, z: t.z + dir.z }, { x: t.x + dir.z, z: t.z + dir.x }, { x: t.x - dir.z, z: t.z - dir.x }, { x: t.x + dir.x * 0.5 + 0.5, z: t.z + dir.z * 0.5 }]) {
        const [i, j] = g.toCell(cand.x, cand.z); if (g.free(i, j)) { pos = g.toWorld(i, j); break; } }
      pos = pos || { x: t.x, z: t.z };
      Object.assign(c, { x: pos.x, z: pos.z, path: [], location: dest });
    } else c.mode = 'left_behind';
    state.transitions++;
    emit({ type: 'transition', from: door.location, to: dest, withCompanion, text: LOCATIONS[dest].name + (withCompanion ? '' : ' (compagnon resté derrière)') });
  }

  function step(dt) {
    const pl = state.player, sp = UNITS.walkSpeed * dt;
    advance(pl, sp);
    if (!pl.path.length && pl.pending) finishPending();
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
  return { state, step, moveTo, useDoor, talkTo, choose, closeDialogue, currentNode, doorOfBuilding, doorById, grids, world,
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
