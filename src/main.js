import * as world from './data/dusk_q1.js';
import { DIALOGUES, ITEMS } from './data/dialogues_q1.js';
import { createGame } from './core/game.js';
import { createView } from './render/view.js';
import { bindPointer } from './input/pointer.js';
import { loadSkins } from './render/textures.js';

const sprites = await (await fetch('./assets/reused/manifest.json')).json();
const game = createGame({ ...world, DIALOGUES, ITEMS }, sprites);
await loadSkins(['g_sand','g_asphalt','g_dirt','g_gravel','g_grass','g_concrete','g_wood','cottage_s','cottage_e','palazzo_s','palazzo_e','ruin_s','ruin_e','yellow_s','yellow_e','shop_s','shop_e','garage_s','roof_tiles','roof_palazzo','roof_ruin','roof_flat']);
const view = createView(document.getElementById('view'), game, sprites, document.getElementById('labels'));
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
  else if (p.kind === 'closed') say(`${p.label} : fermé.`);
  else if (p.kind === 'ground') game.moveTo(p.x, p.z);
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
  $('act').hidden = !nearDoor; if (nearDoor) $('act').textContent = game.location.kind === 'interior' ? 'Sortir' : 'Entrer : ' + game.location.buildings.find(b => b.id === nearDoor.buildingId).label;
  $('loc').textContent = game.location.name;
  $('hp').textContent = `PV ${s.player.hp}/${s.player.maxHp}`; $('money').textContent = `${s.player.money} $`;
  $('inv').textContent = Object.entries(s.player.inv).map(([k, v]) => `${ITEMS[k].name} ×${v}`).join(' · ');
  renderDialogue();
  view.render();
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
window.__nml = { game, state: game.state, project: view.project, pick: view.pick, opacityOf: view.opacityOf, setCamera: view.setCamera, view, doors: world.DOORS, npcs: world.NPCS };
