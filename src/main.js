import * as world from './data/dusk_town.js'; // v7 : toute la ville (Q1 + Q2-Q4)
import { DIALOGUES, ITEMS } from './data/dialogues_town.js';
import { createGame } from './core/game.js';
import { QUESTS, QUEST_NOTES } from './data/quests.js';
import { createView } from './render/view.js';
import { bindPointer } from './input/pointer.js';
import { loadSkins } from './render/textures.js';
import { createShell } from './ui/shell.js';
import { buildCharacter, derived, raceFlags, ORIGIN_ITEMS, originOf } from './data/character.js';
import { portraitUrl } from './ui/creation.js';
Object.assign(ITEMS, ORIGIN_ITEMS); // v11 : objets d'origine

const sprites = await (await fetch('./assets/reused/manifest.json')).json();
// v6 : mobilier et textures d'intérieur (tools_interiors.py : maquette d'abord, sinon générés ; angle v4 contrôlé)
const iman = await (await fetch('./assets/interiors/manifest.json')).json();
Object.assign(sprites, iman);
const game = createGame({ ...world, DIALOGUES, ITEMS }, sprites);
await loadSkins(['g_sand','g_asphalt','g_dirt','g_gravel','g_grass','g_concrete','g_wood']);
await loadSkins(['g_wet', 'g_sv'], n => `./assets/generated/${n}.webp`); // v13 : chaussée mouillée de Steel (générée)
const bman = await (await fetch('./assets/buildings/manifest.json')).json();
await loadSkins(Object.keys(bman), n => './assets/' + bman[n].file);
await loadSkins(Object.keys(iman), n => './assets/' + iman[n].file);
const view = createView(document.getElementById('view'), game, sprites, bman, document.getElementById('labels'));
const $ = id => document.getElementById(id);
let msgTimer;
const say = t => { $('msg').textContent = t; clearTimeout(msgTimer); msgTimer = setTimeout(() => $('msg').textContent = '', 3500); };
game.on(ev => { if (ev.text) say(ev.text); });

bindPointer($('view'), (x, y) => {
  if (game.state.dialogue || shell?.isOpen()) return;
  const p = view.pick(x, y); if (!p) return;
  if (p.x !== undefined || p.kind === 'ground') { // v15 : ferraille / sacs du poste près du point visé
    const sp = (world.SPOTS || []).find(q => q.location === game.state.location && Math.hypot(q.x - p.x, q.z - p.z) < (q.r || 1.4)); if (sp) { game.useSpot(sp.id); return; } }
  if (p.kind === 'npc') game.talkTo(p.npcId);
  else if (p.kind === 'door') game.useDoor(p.doorId);
  else if (p.kind === 'building') { const d = game.doorOfBuilding(p.buildingId); if (d) game.useDoor(d.id); }
  else if (p.kind === 'closed' && p.buildingId === 's_lab' && game.state.flags.q_start) { // v9 : la porte d'acier
    const f = game.state.flags;
    if (f.q_fin || (f.q_cric && f.q_signal)) game.startScene('porte', { x: 28, z: 5.8 });
    else say(!f.q_cric && !f.q_signal ? 'Pas à mains nues, et pas sans savoir où sont les camions.' : !f.q_cric ? 'Pas à mains nues. Le cric d\u2019Anselme.' : 'Pas sans savoir où sont les camions. Teo, au guet.'); }
  else if (p.kind === 'closed') { const t = world.CLOSED_TEXT[p.buildingId]; say((typeof t === 'function' ? t(game.state) : t) || `${p.label} : fermé.`); }
  else if (p.kind === 'ground') { // v7 : un tap au bout d'une rue vise la jonction (on marche jusqu'au seuil)
    const j = world.DOORS.find(d => (d.junction || d.edge) && d.location === game.state.location && Math.hypot(d.threshold.x - p.x, d.threshold.z - p.z) < 1.6);
    if (j) game.useDoor(j.id); else game.moveTo(p.x, p.z); }
});

let nearDoor = null;
$('act').addEventListener('click', () => nearDoor && game.useDoor(nearDoor.id));
$('dlg-close').addEventListener('click', () => game.closeDialogue());
let shownNode = null;
function renderDialogue() {
  const n = game.currentNode(), key = n && [game.state.dialogue.npc, game.state.dialogue.tree, game.state.dialogue.node, game.state.player.money, n.text, n.options.length].join(':'); // v15 : sous-arbres (tree) et textes à gabarit
  $('dialogue').hidden = !n; if (!n || key === shownNode) { if (!n) shownNode = null; return; }
  shownNode = key;
  $('dlg-portrait').hidden = n.npc.portrait === false; if (n.npc.portrait !== false) $("dlg-portrait").src = n.npc.sprite.startsWith("gen_") ? `./assets/generated/portrait-${n.npc.sprite}.webp` : `./assets/reused/portrait-${n.npc.sprite}.webp`; $('dlg-portrait').alt = n.npc.name;
  $('dlg-name').textContent = n.npc.name; typeText(n.text);
  const box = $('dlg-options'); box.replaceChildren();
  for (const [k, o] of n.options.entries()) { const b = document.createElement('button'); b.textContent = o.label; b.dataset.index = o.index; b.dataset.n = k + 1; b.addEventListener('click', () => game.choose(o.index)); box.appendChild(b); }
}
// v10 : texte défilant (option), un tap sur le texte l'affiche en entier
let typeTimer = null;
function typeText(t) {
  clearInterval(typeTimer); const el = $('dlg-text');
  if (!shell || shell.options.textMode !== 'defilant') { el.textContent = t; return; }
  let i = 0; el.textContent = ''; typeTimer = setInterval(() => { i += 2; el.textContent = t.slice(0, i); if (i >= t.length) clearInterval(typeTimer); }, 16);
  el.onclick = () => { clearInterval(typeTimer); el.textContent = t; };
}
let last = performance.now();
function frame(now) {
  const dt = Math.min(0.05, (now - last) / 1000); last = now;
  if (!shell?.isOpen()) game.step(dt);
  const s = game.state, D = world.DOORS;
  nearDoor = s.dialogue ? null : D.find(d => d.location === s.location && Math.hypot(d.threshold.x - s.player.x, d.threshold.z - s.player.z) < 2.5) || null;
  $('act').hidden = !nearDoor; if (nearDoor) $('act').textContent = game.location.kind === 'interior' ? 'Sortir' : nearDoor.junction ? nearDoor.label : nearDoor.edge ? nearDoor.label : 'Entrer : ' + game.location.buildings.find(b => b.id === nearDoor.buildingId).label;
  $('loc').textContent = game.location.name;
  $('hp').textContent = `${s.player.hp}/${s.player.maxHp}`; $('hpbar').style.width = (100 * s.player.hp / s.player.maxHp) + '%'; const inSteel = game.location.city === 'steel'; // v12 : crédit dans Steel, dollar ailleurs
  $('money').textContent = inSteel ? `${s.player.credits || 0} cr` : `${s.player.money} $`; $('money-lbl').textContent = inSteel ? 'Crédits' : 'Dollars';
  $('inv').textContent = Object.entries(s.player.inv).map(([k, v]) => `${ITEMS[k].name} ×${v}`).join(' · ');
  const c = s.companion; $('nilo').closest('.cell').hidden = c.mode === 'absent'; if (c.mode !== 'absent') $('nilo').textContent = c.mode === 'follow' && c.location === s.location ? 'NILO · suit' : 'NILO · resté en arrière';
  $('mini').textContent = `PV ${s.player.hp}/${s.player.maxHp} · ` + (inSteel ? `${s.player.credits || 0} cr` : `${s.player.money} $`);
  const q = currentObjective(); $('obj').hidden = !q; if (q) $('obj-text').textContent = q;
  music.update();
  s.seen[s.location] = true; if (panelOpen) renderPanel();
  renderDialogue();
  view.render();
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
window.__nml = { game, state: game.state, project: view.project, pick: view.pick, opacityOf: view.opacityOf, setCamera: view.setCamera, view, doors: world.DOORS, npcs: world.NPCS, world };

// ---------- v8 : menus Sac / Journal / Carte, interface minimale (direction A) ----------
let panelOpen = null, panelKey = '';
const QUARTERS = [['dusk_q3', 1, 0], ['dusk_q1', 1, 1], ['dusk_q2', 2, 1], ['dusk_q4', 1, 2]];
const short = id => world.LOCATIONS[id].name.split('· ')[1] || world.LOCATIONS[id].name;
const allBuildings = () => Object.values(world.LOCATIONS).flatMap(l => (l.buildings || []).map(b => ({ ...b, loc: l.id })));
const FLAGS = { teo_secret: 'Teo : la nuit où il dormait. Promis de me taire.', ezequiel_toit: 'Ezequiel : la jambe, le toit du blockhaus. Je n\u2019en dirai rien.', sol_vue: 'Sol : le foulard. Je n\u2019en dirai rien.' };
function renderPanel() {
  const s = game.state, n = game.currentNode();
  const key = panelOpen + JSON.stringify([s.flags, s.player.inv, s.player.money, s.discovered, s.flags, s.location, n && n.options.length, Object.keys(s.seen)]);
  if (key === panelKey) return; panelKey = key; const B = $('panel-body');
  if (panelOpen === 'sac') {
    const items = Object.entries(s.player.inv);
    const offers = n ? n.options.filter(o => o.action && o.action.startsWith('buy:')) : [];
    const ch = s.character, RN = { humain: 'Humain', mutant: 'Mutant', augmente: 'Augmenté', cyborg: 'Cyborg' };
    const fiche = ch ? `<div class="fiche"><img src="${portraitUrl(ch.portrait)}" alt=""><div><h3>${ch.name.toUpperCase()}</h3><span class="muted">${RN[ch.race]} · PA ${ch.ap} · ${ch.implant ? 'implant d\u2019IO' : 'sans implant'}</span><div class="attrs">${Object.entries(ch.attrs).map(([k, v]) => `<span>${k.slice(0, 3).toUpperCase()} <b>${v}</b></span>`).join('')}</div></div></div>` : '';
    B.innerHTML = fiche + `<div class="cols"><div><h3>SAC · ${s.player.money} $${s.player.credits ? ' · ' + s.player.credits + ' cr' : ''}</h3><ul>${items.length ? items.map(([k, v]) => `<li><span>${ITEMS[k].name}</span><span>×${v}${ITEMS[k].use ? ` <button data-use="${k}">${ITEMS[k].use.verb || 'Utiliser'}</button>` : ''}</span></li>`).join('') : '<li class="muted">Vide. De quoi acheter : 4 $ l\u2019eau chez Anselme, 3 $ chez Sol.</li>'}</ul></div>
      <div><h3>${n ? 'ACHAT · ' + n.npc.name.toUpperCase() : 'ACHAT'}</h3>${offers.length ? '<ul>' + offers.map(o => `<li><button data-buy="${o.index}"><span>${o.label.replace(/ \(\d+ \$\)/, '')}</span><span>${o.action.split(':')[2]} $</span></button></li>`).join('') + '</ul>' : '<p class="muted">Parle à un marchand pour voir ses prix. Le troc d\u2019objets n\u2019existe pas encore.</p>'}</div></div>
      <div class="desc">${items.length ? 'Ce que tu portes reste avec toi d\u2019un quartier à l\u2019autre.' : 'Rien à porter pour l\u2019instant.'}</div>`;
    B.querySelectorAll('[data-use]').forEach(b => b.addEventListener('click', () => { game.useItem(b.dataset.use); panelKey = ''; }));
    B.querySelectorAll('[data-buy]').forEach(b => b.addEventListener('click', () => { game.choose(+b.dataset.buy); panelKey = ''; }));
  } else if (panelOpen === 'journal') {
    const places = allBuildings().filter(b => s.discovered[b.id]);
    const notes = Object.keys(s.flags).filter(f => FLAGS[f]);
    const qs = QUESTS.filter(qq => qq.visible(s)).map(qq => { let cur = false; return `<div class="lbl">Quête · ${qq.title}</div><ul class="quest">` + qq.steps.filter(st => !st.show || st.show(s)).map(st => {
        const done = st.done && s.flags[st.done], isCur = !done && !cur; if (isCur) cur = true;
        return `<li class="${done ? 'done' : isCur ? 'cur' : ''} ${st.blocked ? 'blk' : ''}"><span>${done ? '[x]' : isCur ? '>' : '[ ]'} ${st.text}</span>${st.blocked && isCur ? `<span class="muted">${st.blocked}</span>` : ''}</li>`; }).join('') + '</ul>'; }).join('');
    notes.push(...Object.keys(QUEST_NOTES).filter(f => s.flags[f]));
    B.innerHTML = `<h3>JOURNAL</h3>${qs}<div class="lbl">Lieux repérés</div><ul>${places.length ? places.map(b => `<li><span>${b.label}</span><span class="muted">${short(b.loc)}</span></li>`).join('') : '<li class="muted">Aucun. Les entrées sont cachées derrière les façades.</li>'}</ul>
      <div class="desc"><div class="lbl">Notes</div>${notes.length ? notes.map(f => FLAGS[f] || QUEST_NOTES[f]).join('<br>') : '<span class="muted">Rien de noté.</span>'}</div>`;
  } else if (panelOpen === 'carte') {
    const cells = Array(9).fill('<div></div>');
    for (const [id, c, r] of QUARTERS) { const here = s.location === id || world.LOCATIONS[s.location].kind === 'interior' && false, known = s.seen[id];
      const pl = allBuildings().filter(b => b.loc === id && s.discovered[b.id]).map(b => b.label);
      cells[r * 3 + c] = `<div class="q ${s.location === id ? 'here' : ''} ${known ? '' : 'unk'}"><b>${known ? short(id) : '?'}</b>${s.location === id ? '> ici<br>' : ''}${pl.join('<br>')}</div>`; }
    B.innerHTML = `<h3>CARTE · DUSK-TOWN</h3><div class="map">${cells.join('')}</div><div class="desc muted">Nord en haut. Les quartiers se rejoignent par les bouts de rue. Au sud des Sables : les terres dévastées.</div>`;
  }
}
function openPanel(name) {
  panelOpen = panelOpen === name ? null : name; panelKey = '';
  $('panel').hidden = !panelOpen; document.body.classList.toggle('panel-open', !!panelOpen); document.querySelectorAll('#keys [data-panel]').forEach(b => b.classList.toggle('on', b.dataset.panel === panelOpen));
  if (panelOpen) renderPanel();
}
function toggleMini() { document.body.classList.toggle('mini'); const on = document.body.classList.contains('mini'); $('mini').hidden = !on; $('k-mini').classList.toggle('on', on); if (on && panelOpen) openPanel(panelOpen); }
document.querySelectorAll('#keys [data-panel]').forEach(b => b.addEventListener('click', () => openPanel(b.dataset.panel)));
$('k-mini').addEventListener('click', toggleMini); $('panel-close').addEventListener('click', () => openPanel(panelOpen));
addEventListener('keydown', e => {
  const k = e.key.toLowerCase();
  if (game.state.dialogue && /^[1-9]$/.test(k)) { const b = document.querySelector(`#dlg-options button[data-n="${k}"]`); if (b) b.click(); return; }
  if (shell?.isOpen()) return;
  if (k === 'escape') { if (panelOpen) openPanel(panelOpen); else if (game.state.dialogue) game.closeDialogue(); else shell.pause(); }
  if (k === 'i') openPanel('sac'); if (k === 'j') openPanel('journal'); if (k === 'm') openPanel('carte'); if (k === 'h') toggleMini();
});

// ---------- v9 : objectif suivi, musique de Dusk-Town ----------
function currentObjective() {
  const s = game.state; for (const q of QUESTS) { if (!q.visible(s)) continue;
    const st = q.steps.filter(x => !x.show || x.show(s)).find(x => !x.done || !s.flags[x.done]); if (st) return st.text + (st.blocked ? ' (hors de portée pour l\u2019instant)' : ''); }
  return null;
}
// Un seul élément <audio> pour toute la partie : jamais recréé au changement de quartier, donc aucune coupure.
// Démarre au premier geste (règles autoplay). Atténuée en intérieur. Coupure mémorisée (localStorage).
var music = (() => {
  const a = $('music'), KEY = 'nml_muted'; let started = false;
  const muted = () => localStorage.getItem(KEY) === '1';
  const sync = () => { a.muted = muted(); $('k-son').classList.toggle('on', a.muted); $('k-son').setAttribute('aria-pressed', a.muted); $('k-son').querySelector('span').textContent = a.muted ? 'Muet' : 'Son'; };
  const start = () => { if (started) return; started = true; a.play().catch(() => { started = false; }); };
  addEventListener('pointerdown', start, true); addEventListener('keydown', start, true); addEventListener('touchstart', start, { capture: true, passive: true });
  $('k-son').addEventListener('click', () => { localStorage.setItem(KEY, muted() ? '0' : '1'); sync(); });
  addEventListener('keydown', e => { if (e.key.toLowerCase() === 's' && !e.repeat && !shell?.isOpen()) $('k-son').click(); });
  sync();
  return { el: a, update() { const v = (game.location.kind === 'interior' ? 0.25 : 0.55) * (shell ? shell.options.music / 100 : 1); if (Math.abs(a.volume - v) > 0.01) a.volume += Math.sign(v - a.volume) * 0.01; } };
})();
window.__nml.music = music.el;

// ---------- v10 lot 1 : menu principal, pause, sauvegardes, options ----------
const START_SNAP = game.snapshot(); // « Nouveau jeu » : état de départ (perso par défaut, Dusk-Town ; la création viendra au lot 2)
var shell = null;
function applyOptions(o) {
  const B = document.body.classList;
  B.toggle('contrast', o.contrast); B.toggle('readable', o.readable); B.toggle('reduce-motion', o.reduceMotion);
  B.toggle('ts-115', o.textSize === 115); B.toggle('ts-130', o.textSize === 130);
}
shell = createShell({ game, world, $, applyOptions, onStart(rec, draft) {
  if (!rec) { // nouveau jeu : création -> Dusk-Town ; PV, PA et dollars dérivés du personnage
    game.restore(START_SNAP, true);
    if (draft) { const c = buildCharacter(draft), dv = derived(draft), s = game.state;
      s.character = c; Object.assign(s.player, { maxHp: dv.maxHp, hp: dv.hp, money: dv.money, inv: { [originOf(draft).item]: 1 } }); Object.assign(s.flags, raceFlags(c)); }
  }
  if (panelOpen) openPanel(panelOpen); shownNode = null;
  const wantMini = shell.options.minimal; if (wantMini !== document.body.classList.contains('mini')) toggleMini();
} });
game.on(ev => {
  if (ev.type !== 'transition') return;
  const L = world.LOCATIONS[ev.to];
  if (ev.from === 'sv_poutres' && ev.to === 'steel_lower') game.state.flags.lt_fosse_ouverte = true; // Lower-Town : la Fosse s'ouvre depuis le bas [plan]
  if (L.arrive && L.arrive.from === ev.from) setTimeout(() => say(L.arrive.text), 50);
  if (ev.to === 'steel_center' && !game.state.flags.q_steel) { game.state.flags.q_steel = true; setTimeout(() => say('Journal : quête mise à jour. Tu es dans Steel-Megalopolis.'), 3600); }
  if (!shell.isOpen()) shell.autosave();
});
// v12 : mutant à la douane de Steel. Le soldat le repère à vue et l'interpelle [décision] ; le combat n'existe pas : scène provisoire (steel.js, COMBAT_HOOKS)
function steelWatch() {
  const s = game.state; if (s.location !== 'steel_route' || !s.flags.race_mutant || s.dialogue || shell.isOpen()) return;
  const h = world.NPCS.find(n => n.id === 'halloran'), d = Math.hypot(s.player.x - h.x, s.player.z - h.z);
  if (d < 8 && !s.flags._halloran_near) { s.flags._halloran_near = true; s.player.path = []; s.player.pending = null; game.startScene('halloran', { x: s.player.x, z: s.player.z }); }
  if (d > 11) s.flags._halloran_near = false;
}
setInterval(steelWatch, 200);
$('k-menu').addEventListener('click', () => { if (game.state.dialogue) game.closeDialogue(); if (panelOpen) openPanel(panelOpen); shell.pause(); });
window.__nml.shell = shell;
