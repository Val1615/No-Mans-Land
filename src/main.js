import * as world from './data/dusk_town.js'; // v7 : toute la ville (Q1 + Q2-Q4)
import { DIALOGUES, ITEMS } from './data/dialogues_town.js';
import { createGame } from './core/game.js';
import { createView } from './render/view.js';
import { bindPointer } from './input/pointer.js';
import { loadSkins } from './render/textures.js';

const sprites = await (await fetch('./assets/reused/manifest.json')).json();
// v6 : mobilier et textures d'intérieur (tools_interiors.py : maquette d'abord, sinon générés ; angle v4 contrôlé)
const iman = await (await fetch('./assets/interiors/manifest.json')).json();
Object.assign(sprites, iman);
const game = createGame({ ...world, DIALOGUES, ITEMS }, sprites);
await loadSkins(['g_sand','g_asphalt','g_dirt','g_gravel','g_grass','g_concrete','g_wood']);
const bman = await (await fetch('./assets/buildings/manifest.json')).json();
await loadSkins(Object.keys(bman), n => './assets/' + bman[n].file);
await loadSkins(Object.keys(iman), n => './assets/' + iman[n].file);
const view = createView(document.getElementById('view'), game, sprites, bman, document.getElementById('labels'));
const $ = id => document.getElementById(id);
let msgTimer;
const say = t => { $('msg').textContent = t; clearTimeout(msgTimer); msgTimer = setTimeout(() => $('msg').textContent = '', 3500); };
game.on(ev => { if (ev.text) say(ev.text); });

bindPointer($('view'), (x, y) => {
  if (game.state.dialogue) return;
  const p = view.pick(x, y); if (!p) return;
  if (p.kind === 'npc') game.talkTo(p.npcId);
  else if (p.kind === 'door') game.useDoor(p.doorId);
  else if (p.kind === 'building') { const d = game.doorOfBuilding(p.buildingId); if (d) game.useDoor(d.id); }
  else if (p.kind === 'closed') say(world.CLOSED_TEXT[p.buildingId] || `${p.label} : fermé.`);
  else if (p.kind === 'ground') { // v7 : un tap au bout d'une rue vise la jonction (on marche jusqu'au seuil)
    const j = world.DOORS.find(d => (d.junction || d.edge) && d.location === game.state.location && Math.hypot(d.threshold.x - p.x, d.threshold.z - p.z) < 1.6);
    if (j) game.useDoor(j.id); else game.moveTo(p.x, p.z); }
});

let nearDoor = null;
$('act').addEventListener('click', () => nearDoor && game.useDoor(nearDoor.id));
$('dlg-close').addEventListener('click', () => game.closeDialogue());
let shownNode = null;
function renderDialogue() {
  const n = game.currentNode(), key = n && game.state.dialogue.npc + ':' + game.state.dialogue.node + ':' + game.state.player.money;
  $('dialogue').hidden = !n; if (!n || key === shownNode) { if (!n) shownNode = null; return; }
  shownNode = key;
  $("dlg-portrait").src = n.npc.sprite.startsWith("gen_") ? `./assets/generated/portrait-${n.npc.sprite}.webp` : `./assets/reused/portrait-${n.npc.sprite}.webp`; $('dlg-portrait').alt = n.npc.name;
  $('dlg-name').textContent = n.npc.name; $('dlg-text').textContent = n.text;
  const box = $('dlg-options'); box.replaceChildren();
  for (const [k, o] of n.options.entries()) { const b = document.createElement('button'); b.textContent = o.label; b.dataset.index = o.index; b.dataset.n = k + 1; b.addEventListener('click', () => game.choose(o.index)); box.appendChild(b); }
}
let last = performance.now();
function frame(now) {
  const dt = Math.min(0.05, (now - last) / 1000); last = now;
  game.step(dt);
  const s = game.state, D = world.DOORS;
  nearDoor = s.dialogue ? null : D.find(d => d.location === s.location && Math.hypot(d.threshold.x - s.player.x, d.threshold.z - s.player.z) < 2.5) || null;
  $('act').hidden = !nearDoor; if (nearDoor) $('act').textContent = game.location.kind === 'interior' ? 'Sortir' : nearDoor.junction ? nearDoor.label : nearDoor.edge ? nearDoor.label : 'Entrer : ' + game.location.buildings.find(b => b.id === nearDoor.buildingId).label;
  $('loc').textContent = game.location.name;
  $('hp').textContent = `${s.player.hp}/${s.player.maxHp}`; $('hpbar').style.width = (100 * s.player.hp / s.player.maxHp) + '%'; $('money').textContent = `${s.player.money} $`;
  $('inv').textContent = Object.entries(s.player.inv).map(([k, v]) => `${ITEMS[k].name} ×${v}`).join(' · ');
  const c = s.companion; $('nilo').textContent = c.mode === 'follow' && c.location === s.location ? 'NILO · suit' : 'NILO · resté en arrière';
  $('mini').textContent = `PV ${s.player.hp}/${s.player.maxHp} · ${s.player.money} $`;
  seen[s.location] = true; if (panelOpen) renderPanel();
  renderDialogue();
  view.render();
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
window.__nml = { game, state: game.state, project: view.project, pick: view.pick, opacityOf: view.opacityOf, setCamera: view.setCamera, view, doors: world.DOORS, npcs: world.NPCS };

// ---------- v8 : menus Sac / Journal / Carte, interface minimale (direction A) ----------
const seen = {}; let panelOpen = null, panelKey = '';
const QUARTERS = [['dusk_q3', 1, 0], ['dusk_q1', 1, 1], ['dusk_q2', 2, 1], ['dusk_q4', 1, 2]];
const short = id => world.LOCATIONS[id].name.split('· ')[1] || world.LOCATIONS[id].name;
const allBuildings = () => Object.values(world.LOCATIONS).flatMap(l => (l.buildings || []).map(b => ({ ...b, loc: l.id })));
const FLAGS = { teo_secret: 'Teo : la nuit où il dormait. Promis de me taire.', ezequiel_toit: 'Ezequiel : la jambe, le toit du blockhaus. Je n\u2019en dirai rien.', sol_vue: 'Sol : le foulard. Je n\u2019en dirai rien.' };
function renderPanel() {
  const s = game.state, n = game.currentNode();
  const key = panelOpen + JSON.stringify([s.player.inv, s.player.money, s.discovered, s.flags, s.location, n && n.options.length, Object.keys(seen)]);
  if (key === panelKey) return; panelKey = key; const B = $('panel-body');
  if (panelOpen === 'sac') {
    const items = Object.entries(s.player.inv);
    const offers = n ? n.options.filter(o => o.action && o.action.startsWith('buy:')) : [];
    B.innerHTML = `<div class="cols"><div><h3>SAC · ${s.player.money} $</h3><ul>${items.length ? items.map(([k, v]) => `<li><span>${ITEMS[k].name}</span><span>×${v}</span></li>`).join('') : '<li class="muted">Vide. De quoi acheter : 4 $ l\u2019eau chez Anselme, 3 $ chez Sol.</li>'}</ul></div>
      <div><h3>${n ? 'ACHAT · ' + n.npc.name.toUpperCase() : 'ACHAT'}</h3>${offers.length ? '<ul>' + offers.map(o => `<li><button data-buy="${o.index}"><span>${o.label.replace(/ \(\d+ \$\)/, '')}</span><span>${o.action.split(':')[2]} $</span></button></li>`).join('') + '</ul>' : '<p class="muted">Parle à un marchand pour voir ses prix. Le troc d\u2019objets n\u2019existe pas encore.</p>'}</div></div>
      <div class="desc">${items.length ? 'Ce que tu portes reste avec toi d\u2019un quartier à l\u2019autre.' : 'Rien à porter pour l\u2019instant.'}</div>`;
    B.querySelectorAll('[data-buy]').forEach(b => b.addEventListener('click', () => { game.choose(+b.dataset.buy); panelKey = ''; }));
  } else if (panelOpen === 'journal') {
    const places = allBuildings().filter(b => s.discovered[b.id]);
    const notes = Object.keys(s.flags).filter(f => FLAGS[f]);
    B.innerHTML = `<h3>JOURNAL</h3><div class="lbl">Lieux repérés</div><ul>${places.length ? places.map(b => `<li><span>${b.label}</span><span class="muted">${short(b.loc)}</span></li>`).join('') : '<li class="muted">Aucun. Les entrées sont cachées derrière les façades.</li>'}</ul>
      <div class="desc"><div class="lbl">Notes</div>${notes.length ? notes.map(f => FLAGS[f]).join('<br>') : '<span class="muted">Rien de noté.</span>'}</div>`;
  } else if (panelOpen === 'carte') {
    const cells = Array(9).fill('<div></div>');
    for (const [id, c, r] of QUARTERS) { const here = s.location === id || world.LOCATIONS[s.location].kind === 'interior' && false, known = seen[id];
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
  if (k === 'escape') { if (panelOpen) openPanel(panelOpen); else game.closeDialogue(); }
  if (k === 'i') openPanel('sac'); if (k === 'j') openPanel('journal'); if (k === 'm') openPanel('carte'); if (k === 'h') toggleMini();
});
