// Mode DEV minimaliste (?dev=1) : Déplacement (zone, porte, PNJ) et Réinitialisation (instantané, restauration en mémoire).
// Chargé à la demande par main.js. N'écrit jamais dans les sauvegardes du joueur : l'instantané reste en mémoire, l'autosave DEV va dans nml_dev_save_*.
// À venir : Préparation, Combats, Inspection ; les accès existants (?dome=1, ?race=, __nml.debugMega, __nml.ouvrirDome) restent disponibles.
export function createDev({ game, world, say }) {
  const L = world.LOCATIONS, esc = t => String(t).replace(/[&<>"]/g, c => `&#${c.charCodeAt(0)};`);
  const nom = id => (L[id]?.name || id).replace(/^.*· /, '');
  function tp(loc, x, z) { const g = game.grids[loc]; if (!g) return false;
    let p = { x, z }; const [i, j] = g.toCell(x, z);
    if (!g.free(i, j)) { let best = null, bd = 1e9; for (let di = -6; di <= 6; di++) for (let dj = -6; dj <= 6; dj++) if (g.free(i + di, j + dj)) { const d = di * di + dj * dj; if (d < bd) { bd = d; best = g.toWorld(i + di, j + dj); } } if (best) p = best; }
    if (game.state.dialogue) game.closeDialogue();
    const s = game.snapshot(); s.location = loc; s.player.x = p.x; s.player.z = p.z; game.restore(s, true); return true; }
  const zones = Object.keys(L).filter(k => game.grids[k]).sort((a, b) => nom(a).localeCompare(nom(b)));
  const cibles = {
    zone: zones.map(k => ({ v: k, t: nom(k), go: () => { const sp = L[k].spawn?.player || { x: L[k].size.w / 2, z: L[k].size.d / 2 }; return tp(k, sp.x, sp.z); } })),
    porte: world.DOORS.filter(d => L[d.location] && d.threshold).map(d => ({ v: d.id, t: `${nom(d.location)} · ${d.label || d.id}`, go: () => tp(d.location, d.threshold.x, d.threshold.z) })),
    pnj: world.NPCS.filter(n => L[n.location]).map(n => ({ v: n.id, t: `${n.name} · ${nom(n.location)}`, go: () => tp(n.location, n.x, n.z + 1.2) })),
  };
  let instantane = null;
  const el = document.createElement('div'); el.id = 'dev';
  el.innerHTML = `<button id="dev-tog" class="mono">DEV</button><div id="dev-box" hidden>
    <a href="./editor/" target="_blank" style="color:#f2b44a">Éditeur de cartes ↗</a><b class="mono">Déplacement</b>
    <div class="dev-row"><select id="dev-type"><option value="zone">Zone</option><option value="porte">Porte</option><option value="pnj">PNJ</option></select><select id="dev-cible"></select></div>
    <button id="dev-go">Aller</button>
    <b class="mono">Réinitialisation</b>
    <div class="dev-row"><button id="dev-snap">Instantané</button><button id="dev-rest" disabled>Restaurer</button></div>
    <button id="dev-oublier">Oublier le mode DEV</button>
    <small id="dev-info" class="muted"></small></div>`;
  document.body.appendChild(el);
  const $ = id => el.querySelector('#' + id), info = t => { $('dev-info').textContent = t; };
  const remplir = () => { $('dev-cible').innerHTML = cibles[$('dev-type').value].map(c => `<option value="${esc(c.v)}">${esc(c.t)}</option>`).join(''); };
  remplir(); $('dev-type').onchange = remplir;
  $('dev-tog').onclick = () => { $('dev-box').hidden = !$('dev-box').hidden; };
  const aller = (type, v) => { const c = cibles[type].find(c => c.v === v); const ok = !!c && c.go(); info(ok ? `→ ${c.t}` : 'Cible introuvable'); return ok; };
  $('dev-go').onclick = () => aller($('dev-type').value, $('dev-cible').value);
  const snap = () => { instantane = game.snapshot(); $('dev-rest').disabled = false; info(`Instantané : ${nom(instantane.location)}`); return true; };
  const rest = () => { if (!instantane) return false; if (game.state.dialogue) game.closeDialogue(); game.restore(JSON.parse(JSON.stringify(instantane)), true); info('Instantané restauré'); return true; };
  $('dev-oublier').onclick = () => { localStorage.removeItem('nml_dev_unlocked'); info('Mode DEV oublié : le bouton d\u2019Options disparaît.'); };
  if (new URLSearchParams(location.search).get('devpanel') === '1') $('dev-box').hidden = false; // ouvert depuis Options
  $('dev-snap').onclick = snap; $('dev-rest').onclick = rest;
  for (const e of ['pointerdown', 'pointerup', 'click', 'wheel', 'touchstart']) el.addEventListener(e, ev => ev.stopPropagation());
  const st = document.createElement('style'); st.textContent = `
#dev{position:fixed;right:8px;top:calc(50% - 20px);z-index:70;font-size:12px;color:#e8dcc0}
#dev-tog{display:block;margin-left:auto;background:rgba(8,6,3,.55);color:#f2b44a;border:1px solid rgba(242,180,74,.5);padding:3px 7px;font-size:11px;cursor:pointer}
#dev-box{margin-top:4px;width:min(260px,calc(100vw - 16px));background:rgba(8,6,3,.72);border:1px solid rgba(242,180,74,.35);padding:8px;display:flex;flex-direction:column;gap:6px}
#dev-box[hidden]{display:none}
#dev-box b{color:#f2b44a;font-size:11px;letter-spacing:.08em;text-transform:uppercase}
#dev .dev-row{display:flex;gap:6px}#dev select{flex:1;min-width:0;max-width:100%}
#dev select,#dev-box button{background:rgba(20,16,10,.85);color:#e8dcc0;border:1px solid rgba(242,180,74,.35);padding:4px;font:inherit;min-height:28px}
#dev-box button{cursor:pointer;flex:1}#dev-box button:disabled{opacity:.4}`;
  document.head.appendChild(st);
  return { tp, aller, cibles, instantane: snap, restaurer: rest };
}
