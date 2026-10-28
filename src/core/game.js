import { rollVolonte } from '../data/volonte.js';
import { UNITS } from '../data/units.js';
import { ARGENT } from '../data/argent.js';
import { buildGrid } from './grid.js';
import { findPath } from './path.js';
import { createCombat } from './combat.js';

// État sérialisable + commandes à résultat typé. Aucune dépendance au rendu.
export function createGame(world, sprites) {
  const { LOCATIONS, DOORS, NPCS = [], DIALOGUES = {}, ITEMS = {}, START, COMPANION, SPOTS = [], TRIGGERS = [] } = world;
  let rng = Math.random; // v15 : tirage injectable (tests : setRng)
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
    npcs: Object.fromEntries(NPCS.map(n => [n.id, { heading: n.faceTo ? Math.atan2(n.faceTo[0] - n.x, n.faceTo[1] - n.z) : 0 }])), log: [], transitions: 0, osGains: 0, os: null
  };
  const listeners = new Set();
  const emit = ev => { state.log.push(ev); if (state.log.length > 80) state.log.shift(); listeners.forEach(f => f(ev)); };
  const grid = () => grids[state.location];
  const doorById = id => DOORS.find(d => d.id === id);
  const doorOfBuilding = bid => DOORS.filter(d => d.buildingId === bid && d.location === state.location).sort((a, b) => Math.hypot(a.threshold.x - state.player.x, a.threshold.z - state.player.z) - Math.hypot(b.threshold.x - state.player.x, b.threshold.z - state.player.z))[0];
  const npcById = id => NPCS.find(n => n.id === id);
  const refuse = (reason, text) => { if (typeof text === 'function') text = text(state); /* v14 : texte selon l'état */ emit({ type: 'refus', reason, text }); return { ok: false, reason }; };
  const busy = () => state.dialogue ? refuse('dialogue_ouvert', 'Termine la conversation d\'abord.') : state.combat ? refuse('combat', 'Pas pendant le combat.') : null;

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
    if (p.kind === 'door') { const d = doorById(p.id), bad = (d.conditions || []).find(c => !c.test(state)); if (d.edge || bad) { state.junctionLock = d.id; refuse(bad ? bad.reason : 'bord', bad ? bad.text : d.edge); } else if (!interrupt(d)) enter(d); }
    if (p.kind === 'talk') openDialogue(p.id);
    if (p.kind === 'scene') openDialogue(p.id);
    if (p.kind === 'spot') doSpot(SPOTS.find(s => s.id === p.id));
  }
  // v9 : scène sans PNJ visible (ex. la voix derrière la porte d'acier) : marcher jusqu'au point, puis ouvrir le dialogue
  function startScene(npcId, at) {
    const b = busy(); if (b) return b;
    return goThen(at, { kind: 'scene', id: npcId }) || refuse('chemin_bloque', 'Impossible d\'approcher.');
  }
  // Scène qui coupe un passage une seule fois (door.interrupt = { npc, tree, if: s => bool }).
  function interrupt(d) { const it = d.interrupt; if (!it || !it.if(state)) return false; openDialogue(it.npc); if (it.tree) state.dialogue.tree = it.tree; return true; }
  function openDialogue(npcId) {
    const n = npcById(npcId);
    state.dialogue = { npc: npcId, node: 'start' };
    if (n.dialogue === 'teo') { delete state.flags.os_bluff_fait; state.os = null; } // v15 : nouvelle visite = nouvelle partie de Trois Os
    state.player.heading = Math.atan2(n.x - state.player.x, n.z - state.player.z);
    state.npcs[npcId].heading = Math.atan2(state.player.x - n.x, state.player.z - n.z); // le PNJ se tourne vers le joueur
    emit({ type: 'dialogue_open', npc: npcId });
  }
  function currentNode() {
    if (!state.dialogue) return null;
    const tree = DIALOGUES[state.dialogue.tree || npcById(state.dialogue.npc).dialogue]; const node = tree[state.dialogue.node];
    const alt = (node.alt || []).find(a => cond(a.if));
    return { npc: npcById(state.dialogue.npc), text: fill(alt ? alt.text : node.text),
      options: node.options.map((o, i) => ({ ...o, index: i })).filter(o => !o.if || cond(o.if)) };
  }
  // v9 : conditions composées « a&!b » ; « hurt » = blessé
  // v15 : {joueur} / {maison} (Trois Os) : « 4, 4, 2 (10) »
  const dice = d => d && d.length ? `${d.join(', ')} (${d.reduce((a, b) => a + b, 0)})` : '?';
  const fill = t => t && t.replace(/\{joueur\}/g, () => dice(state.os?.joueur)).replace(/\{maison\}/g, () => dice(state.os?.maison));
  const attrOf = k => state.character?.attrs?.[k] ?? 0;
  const cond1 = c => {
    let m = /^inv:(\w+)(>=|<=|>|<)(\d+)$/.exec(c) || /^(money|cr)(>=|<=|>|<)(\d+)$/.exec(c); // v15 : inv:objet>=N, money<N, cr<N
    if (m) { const v = m[1] === 'money' ? state.player.money : m[1] === 'cr' ? (state.player.credits || 0) : (state.player.inv[m[1]] || 0), n = +m[3]; return m[2] === '>=' ? v >= n : m[2] === '<=' ? v <= n : m[2] === '>' ? v > n : v < n; }
    m = /^(\w+)(>=|<=|>|<)(\d+)$/.exec(c); if (m) { const v = attrOf(m[1]), n = +m[3]; return m[2] === '>=' ? v >= n : m[2] === '<=' ? v <= n : m[2] === '>' ? v > n : v < n; }
    return c.startsWith('!') ? !cond1(c.slice(1)) : c === 'hurt' ? state.player.hp < state.player.maxHp : !!state.flags[c]; };
  const cond = c => c.split('&').every(cond1);
  function choose(index) {
    const node = currentNode(); if (!node) return { ok: false };
    const opt = node.options.find(o => o.index === index); if (!opt) return { ok: false };
    let next = opt.next;
    if (opt.test) { const [k, n] = opt.test.split(':'), r = rollVolonte(attrOf(k), +n, rng); next = r.ok ? opt.pass : opt.fail;
      emit({ type: 'test', attr: k, ok: r.ok, text: r.ok ? 'Tu tiens bon.' : 'Tu flanches.' });
      if (r.ok && state.dialogue.tree === 'trois_os' && opt.pass === 'bluff_ok') osRoll('joueur', true); } // bluff réussi : la relance est montrée dans bluff_ok
    if (opt.action) { // v9 : plusieurs actions « a;b », on s'arrête au premier refus (pas assez de $)
      const acts = opt.action.split(';');
      if (acts.some(a => /^paycr:/.test(a))) { const cr = acts.reduce((t, a) => t + (/^paycr:/.test(a) ? +a.split(':')[1] : 0), 0);
        if ((state.player.credits || 0) < cr) { next = 'pauvre'; acts.length = 0; } }
      if (acts.some(a => /^(buy|pay:|heal|os:mise:)/.test(a))) { const cost = acts.reduce((t, a) => t + (/^(pay:|heal)/.test(a) ? +a.split(':')[1] : /^(buy|os:mise)/.test(a) ? +a.split(':')[2] : 0), 0);
        if (state.player.money < cost) { next = 'pauvre'; acts.length = 0; } }
      for (const a of acts) { const r = act(a); if (!r.ok) { next = r.next || next; break; } if (r.next) next = r.next; } }
    if (!next || next === 'end') { closeDialogue(); return { ok: true, closed: true }; }
    if (next.includes('/')) { const [t, n] = next.split('/'); if (DIALOGUES[t]) { state.dialogue.tree = t; next = n; } }
    else { const own = npcById(state.dialogue.npc).dialogue, cur = DIALOGUES[state.dialogue.tree || own]; // v15 : nœud absent du sous-arbre (ex. pauvre) -> arbre du PNJ
      if (!cur[next] && DIALOGUES[own]?.[next]) state.dialogue.tree = own; else if (!cur[next]) { closeDialogue(); return { ok: true, closed: true }; } }
    state.dialogue.node = next; return { ok: true };
  }
  function act(a) {
    const [k, x, y] = a.split(':'), pl = state.player;
    if (k === 'reveal') { if (!state.discovered[x]) { state.discovered[x] = true; emit({ type: 'discover', building: x, how: 'dialogue', text: 'Lieu repéré.' }); } return { ok: true }; }
    if (k === 'flag') { state.flags[x] = true; const tech = ARGENT.flagsTechniques.some(r => r.test(x)); // décision (b) : drapeaux techniques silencieux
      emit({ type: 'flag', flag: x, technique: tech, text: tech ? undefined : x.startsWith('q_') ? 'Journal : quête mise à jour.' : 'Journal : piste notée.' }); return { ok: true }; }
    // v15 argent : gain:N, give:objet[:n], sell:objet:N, os:*
    if (k === 'gain') { pl.money += +x; emit({ type: 'service', what: 'gain', text: `+${x} $` }); return { ok: true }; }
    if (k === 'give') { const n = +(y || 1); pl.inv[x] = (pl.inv[x] || 0) + n; emit({ type: 'service', what: 'give', text: `${ITEMS[x]?.name || x}${n > 1 ? ' ×' + n : ''}` }); return { ok: true }; }
    if (k === 'sell') { if (!pl.inv[x]) return { ok: false }; pl.inv[x]--; if (!pl.inv[x]) delete pl.inv[x]; pl.money += +y; emit({ type: 'service', what: 'sell', text: `${ITEMS[x]?.name || x} vendu : +${y} $` }); return { ok: true }; }
    if (k === 'os') return osAct(x, y);
    if (k === 'pay') { const cost = +x; if (pl.money < cost) return { ok: false, next: 'pauvre' }; pl.money -= cost; emit({ type: 'service', what: 'pay', text: `−${cost} $` }); return { ok: true }; }
    if (k === 'paycr') { const cost = +x; if ((pl.credits || 0) < cost) return { ok: false, next: 'pauvre' }; pl.credits -= cost; emit({ type: 'service', what: 'paycr', text: `−${cost} cr` }); return { ok: true }; }
    if (k === 'take') { if (!pl.inv[x]) return { ok: true }; pl.inv[x]--; if (!pl.inv[x]) delete pl.inv[x]; emit({ type: 'service', what: 'take', text: `${ITEMS[x]?.name || x} perdu` }); return { ok: true }; }
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
    if (k === 'combat') { state.combatPending = x; return { ok: true }; } // COMBAT C1 : lancé à la fermeture du dialogue (autosave juste avant)
    if (k === 'hook') { state.hooks = state.hooks || []; state.hooks.push(x); emit({ type: 'hook', id: x }); return { ok: true }; }
    return { ok: false };
  }
  // v15 : Les Trois Os (règles : docs/ARGENT_DUSKTOWN.md ; réglages : data/argent.js)
  const OS = ARGENT.trois_os;
  function osRoll(who, relance) { state.os = state.os || { mise: 0 }; if (who === 'joueur' && relance) { if (state.os.relance) return; state.os.relance = true; }
    state.os[who] = Array.from({ length: OS.des }, () => 1 + Math.floor(rng() * OS.faces)); }
  const osScore = d => { const brelan = d.every(v => v === d[0]); return brelan ? 1000 + d[0] : d.reduce((a, b) => a + b, 0); };
  function osAct(x, y) {
    const pl = state.player;
    if (x === 'mise') { const m = Math.max(1, Math.min(OS.miseMax, +y | 0)); if (pl.money < m) return { ok: false, next: 'pauvre' };
      pl.money -= m; state.os = { mise: m, joueur: null, maison: null, relance: false }; osRoll('joueur'); emit({ type: 'service', what: 'os_mise', text: `Mise : ${m} $` }); return { ok: true }; }
    if (!state.os) return { ok: false };
    if (x === 'relance') { osRoll('joueur', true); return { ok: true }; }
    if (x === 'maison') { osRoll('maison'); return { ok: true }; }
    if (x === 'perd') { emit({ type: 'service', what: 'os_perd', text: `−${state.os.mise} $` }); state.osGains -= state.os.mise; state.os.mise = 0; return { ok: true }; }
    if (x === 'finpartie') { delete state.flags.os_bluff_fait; return { ok: true }; }
    if (x === 'resout') { const a = osScore(state.os.joueur), b = osScore(state.os.maison), m = state.os.mise; state.os.mise = 0;
      if (a === b) { pl.money += m; emit({ type: 'service', what: 'os_egal', text: `Mise rendue` }); return { ok: true, next: 'egal' }; }
      if (a < b) { emit({ type: 'service', what: 'os_perd', text: `−${m} $` }); state.osGains -= m; return { ok: true, next: 'perd' }; }
      const g = Math.max(0, Math.min(m, OS.plafondGains - state.osGains)); state.osGains += g; pl.money += m + g; // gain tronqué au plafond
      emit({ type: 'service', what: 'os_gagne', text: `+${g} $` });
      return { ok: true, next: state.osGains >= OS.plafondGains ? 'plafond' : 'gagne' }; }
    return { ok: false };
  }
  // v15 : points cliquables au sol (ferraille, sacs du poste) : { id, location, x, z, kind:'pickup'|'scene', ... }
  function useSpot(id) { const b = busy(); if (b) return b; const sp = SPOTS.find(s => s.id === id);
    if (!sp || sp.location !== state.location) return refuse('absent', 'Rien ici.');
    if (sp.if && !sp.if(state)) return refuse('rien', typeof sp.empty === 'function' ? sp.empty(state) : sp.empty || 'Rien d\'utile.');
    const g = grid(), w = (() => { const [i, j] = g.toCell(sp.x, sp.z); return g.free(i, j) ? { x: sp.x, z: sp.z } : nearestFree(g, sp, state.player); })();
    return goThen(w || sp, { kind: 'spot', id }) || refuse('chemin_bloque', 'Impossible d\'approcher.'); }
  function doSpot(sp) { if (sp.kind === 'scene') return openDialogue(sp.scene);
    state.flags[sp.flag] = true; act(`give:${sp.item}`); emit({ type: 'pickup', id: sp.id, text: sp.text }); }
  function useItem(id) { const it = ITEMS[id], pl = state.player; if (!it?.use || !pl.inv[id]) return { ok: false };
    pl.inv[id]--; if (!pl.inv[id]) delete pl.inv[id]; const before = pl.hp; pl.hp = Math.min(pl.maxHp, pl.hp + (it.use.heal || 0));
    emit({ type: 'service', what: 'use', text: `${it.name} : +${pl.hp - before} PV` }); return { ok: true, healed: pl.hp - before }; }
  function sceneTriggers() { if (state.dialogue || state.combat) return; for (const t of TRIGGERS) if (t.location.includes(state.location) && t.if(state, rng)) { openDialogue(t.scene); return; } }
  function closeDialogue() { if (state.dialogue) { const n = npcById(state.dialogue.npc); if (n.faceTo) state.npcs[n.id].heading = Math.atan2(n.faceTo[0] - n.x, n.faceTo[1] - n.z); emit({ type: 'dialogue_close', npc: state.dialogue.npc }); state.dialogue = null; }
    if (state.combatPending && !state.combat) { const id = state.combatPending; state.combatPending = null; combat.start(id); } }

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
    sceneTriggers();
  }

  function step(dt) {
    if (state.combat) { combat.step(dt); return; } // combat : seules les unités du combat bougent
    const pl = state.player, sp = UNITS.walkSpeed * dt;
    advance(pl, sp);
    if (!pl.path.length && pl.pending) finishPending();
    // Jonctions de rue : franchies dès que le joueur s'arrête sur le seuil (marche réelle).
    if (state.junctionLock) { const l = doorById(state.junctionLock); if (!l || l.location !== state.location || Math.hypot(l.threshold.x - pl.x, l.threshold.z - pl.z) > 1.5) state.junctionLock = null; }
    if (!pl.path.length && !state.dialogue) for (const d of DOORS) if ((d.junction || d.edge) && d.location === state.location && d.id !== state.junctionLock && Math.hypot(d.threshold.x - pl.x, d.threshold.z - pl.z) < 0.8) {
      const bad = (d.conditions || []).find(c => !c.test(state)); if (d.edge || bad) { state.junctionLock = d.id; refuse(bad ? bad.reason : 'bord', bad ? bad.text : d.edge); } else if (!interrupt(d)) enter(d); break; }
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
  const combat = createCombat({ state, grids, emit, act });
  // v10 : sauvegarde. Instantané de tout l'état durable (jamais chemins, attentes, dialogue en cours).
  function snapshot() {
    const p = state.player, c = state.companion;
    return JSON.parse(JSON.stringify({ location: state.location, player: { x: p.x, z: p.z, heading: p.heading || 0, hp: p.hp, maxHp: p.maxHp, money: p.money, credits: p.credits || 0, inv: p.inv },
      companion: { x: c.x, z: c.z, mode: c.mode, location: c.location }, flags: state.flags, discovered: state.discovered, seen: state.seen, transitions: state.transitions, osGains: state.osGains, character: state.character || null }));
  }
  function restore(snap, quiet) {
    if (!snap || !LOCATIONS[snap.location]) return false;
    closeDialogue();
    const p = state.player, sp0 = snap.player || {};
    state.location = snap.location;
    Object.assign(p, { x: +sp0.x || 0, z: +sp0.z || 0, heading: +sp0.heading || 0, hp: sp0.hp ?? START.hp, maxHp: sp0.maxHp ?? START.maxHp, money: sp0.money ?? START.money, credits: sp0.credits || 0, inv: { ...(sp0.inv || {}) }, path: [], pending: null });
    const g = grids[state.location], [i, j] = g.toCell(p.x, p.z); if (!g.free(i, j)) { const w = nearestFree(g, p, p); if (w) Object.assign(p, w); }
    Object.assign(state.companion, { ...(snap.companion || {}), path: [] });
    state.flags = { ...(snap.flags || {}) }; state.discovered = { ...(snap.discovered || {}) }; state.seen = { ...(snap.seen || {}) }; state.transitions = snap.transitions || 0; state.osGains = snap.osGains || 0; state.os = null; state.combat = null; state.combatPending = null;
    state.character = snap.character ? JSON.parse(JSON.stringify(snap.character)) : null; // v11 : personnage créé (lot 2)
    // pas de franchissement immédiat si l'on a sauvegardé sur un seuil de jonction
    const jd = DOORS.find(d => (d.junction || d.edge) && d.location === state.location && Math.hypot(d.threshold.x - p.x, d.threshold.z - p.z) < 1.5); state.junctionLock = jd ? jd.id : null;
    if (!quiet) emit({ type: 'restore', text: 'Partie chargée : ' + LOCATIONS[state.location].name });
    return true;
  }
  return { combat, startCombat: id => combat.start(id), state, setRng: f => { rng = f || Math.random; }, useSpot, useItem, sceneTriggers, step, snapshot, restore, moveTo, useDoor, talkTo, startScene, cond, choose, closeDialogue, currentNode, doorOfBuilding, doorById, grids, world,
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
