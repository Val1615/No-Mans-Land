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
  for (const o of n.options) { const b = document.createElement('button'); b.textContent = o.label; b.dataset.index = o.index; b.addEventListener('click', () => game.choose(o.index)); box.appendChild(b); }
}
let last = performance.now();
function frame(now) {
  const dt = Math.min(0.05, (now - last) / 1000); last = now;
  game.step(dt);
  const s = game.state, D = world.DOORS;
  nearDoor = s.dialogue ? null : D.find(d => d.location === s.location && Math.hypot(d.threshold.x - s.player.x, d.threshold.z - s.player.z) < 2.5) || null;
  $('act').hidden = !nearDoor; if (nearDoor) $('act').textContent = game.location.kind === 'interior' ? 'Sortir' : nearDoor.junction ? nearDoor.label : nearDoor.edge ? nearDoor.label : 'Entrer : ' + game.location.buildings.find(b => b.id === nearDoor.buildingId).label;
  $('loc').textContent = game.location.name;
  $('hp').textContent = `PV ${s.player.hp}/${s.player.maxHp}`; $('money').textContent = `${s.player.money} $`;
  $('inv').textContent = Object.entries(s.player.inv).map(([k, v]) => `${ITEMS[k].name} ×${v}`).join(' · ');
  renderDialogue();
  view.render();
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
window.__nml = { game, state: game.state, project: view.project, pick: view.pick, opacityOf: view.opacityOf, setCamera: view.setCamera, view, doors: world.DOORS, npcs: world.NPCS };
