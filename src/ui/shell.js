// v10 lot 1 : menu principal, pause, sauvegardes (3 emplacements + auto), options. Style UI v8 « radio ambre ».
// Stockage localStorage versionné : nml_save_1..3, nml_save_auto ({ v, t, label, state }) ; options : nml_options ({ v, ... }).
export const SAVE_VERSION = 1, OPT_VERSION = 1;
const SLOTS = ['1', '2', '3'], AUTO = 'auto';
export const DEFAULT_OPTIONS = { music: 100, sfx: 100, minimal: false, textSize: 100, contrast: false, readable: false, textMode: 'instant', reduceMotion: false };

// Migration sûre : un format inconnu ou abîmé n'est jamais chargé et ne fait jamais planter le jeu.
export function migrateSave(raw) {
  let o; try { o = typeof raw === 'string' ? JSON.parse(raw) : raw; } catch { return null; }
  if (!o || typeof o !== 'object') return null;
  if (o.v === undefined && o.location && o.player) o = { v: 1, t: 0, label: '', state: o }; // v0 : instantané nu (prototype) -> v1
  if (o.v > SAVE_VERSION || !o.state || typeof o.state.location !== 'string' || !o.state.player) return null;
  return o;
}
export function migrateOptions(raw) {
  let o; try { o = JSON.parse(raw || 'null'); } catch { o = null; }
  const out = { ...DEFAULT_OPTIONS };
  if (o && typeof o === 'object' && !(o.v > OPT_VERSION)) for (const k of Object.keys(DEFAULT_OPTIONS)) if (typeof o[k] === typeof DEFAULT_OPTIONS[k]) out[k] = o[k];
  out.music = Math.max(0, Math.min(100, out.music)); out.sfx = Math.max(0, Math.min(100, out.sfx)); if (![100, 115, 130].includes(out.textSize)) out.textSize = 100;
  return out;
}

export function createShell({ game, world, $, onStart, applyOptions }) {
  const LS = window.localStorage;
  const key = s => 'nml_save_' + s;
  const read = s => migrateSave(LS.getItem(key(s)));
  const fmt = t => t ? new Date(t).toLocaleString('fr-FR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' }).replace(',', '') : '';
  const label = () => world.LOCATIONS[game.state.location].name.replace('Dusk-Town · ', '');
  function write(slot) {
    const rec = { v: SAVE_VERSION, t: Date.now(), label: label(), state: game.snapshot() };
    try { LS.setItem(key(slot), JSON.stringify(rec)); return true; } catch { return false; }
  }
  const latest = () => [AUTO, ...SLOTS].map(s => ({ s, r: read(s) })).filter(x => x.r).sort((a, b) => b.r.t - a.r.t)[0] || null;
  let options = migrateOptions(LS.getItem('nml_options'));
  const saveOptions = () => { LS.setItem('nml_options', JSON.stringify({ v: OPT_VERSION, ...options })); applyOptions(options); };

  let mode = 'title', sub = null; // mode : title | pause | closed
  const M = $('menu'), S = $('menu-sub');
  const open = m => { mode = m; M.hidden = false; document.body.classList.add('menu-open'); M.classList.toggle('pause', m === 'pause'); render(); };
  const close = () => { mode = 'closed'; sub = null; M.hidden = true; document.body.classList.remove('menu-open'); };
  function render() {
    const last = latest(), inGame = mode === 'pause';
    $('m-resume').hidden = !inGame;
    $('m-continue').disabled = !last; $('m-continue-info').textContent = last ? `${last.s === AUTO ? 'Auto' : 'Emplacement ' + last.s} · ${last.r.label} · ${fmt(last.r.t)}` : 'Aucune sauvegarde';
    $('m-load').querySelector('span').textContent = inGame ? 'Charger / Sauvegarder' : 'Charger';
    M.querySelectorAll('.m-main button').forEach(b => b.classList.toggle('sel', b.dataset.sub === sub));
    S.hidden = !sub; M.classList.toggle('sub-open', !!sub); if (!sub) return;
    if (sub === 'load') {
      const canSave = inGame && !game.state.dialogue;
      S.innerHTML = `<button class="btn m-back" data-back="1">‹ Retour</button><h2>${inGame ? 'CHARGER / SAUVEGARDER' : 'CHARGER'}</h2><ul class="slots">` + [AUTO, ...SLOTS].map(s => { const r = read(s);
        return `<li data-slot="${s}"><div><b>${s === AUTO ? 'Auto' : 'Emplacement ' + s}</b><span class="muted">${r ? `${r.label} · ${fmt(r.t)} · ${r.state.player.money} $` : 'Vide'}</span></div>
          <div class="acts">${r ? `<button class="btn" data-act="load" data-slot="${s}">Charger</button>` : ''}${s !== AUTO && canSave ? `<button class="btn" data-act="save" data-slot="${s}">${r ? 'Écraser' : 'Sauvegarder'}</button>` : ''}</div></li>`; }).join('') + '</ul>'
        + `<p class="muted">${inGame ? (canSave ? 'Sauvegarde automatique à chaque changement de lieu.' : 'Termine la conversation pour sauvegarder.') : 'Lance ou continue une partie pour sauvegarder.'}</p>`;
    } else if (sub === 'options') {
      const seg = (k, vals) => `<span class="seg">${vals.map(([v, l]) => `<button class="btn ${options[k] === v ? 'sel' : ''}" data-opt="${k}" data-val='${JSON.stringify(v)}'>${l}</button>`).join('')}</span>`;
      const rng = k => `<input type="range" min="0" max="100" step="5" value="${options[k]}" data-range="${k}" aria-label="${k}"><span class="muted" id="v-${k}">${options[k]}</span>`;
      const row = (l, c) => `<div class="row"><span>${l}</span><span>${c}</span></div>`;
      S.innerHTML = `<button class="btn m-back" data-back="1">‹ Retour</button><h2>OPTIONS</h2><div class="lbl">Son</div>${row('Musique', rng('music'))}${row('Effets', rng('sfx'))}
        <div class="lbl">Interface</div>${row('Mode minimal au démarrage', seg('minimal', [[false, 'Non'], [true, 'Oui']]))}${row('Taille du texte', seg('textSize', [[100, '100 %'], [115, '115 %'], [130, '130 %']]))}${row('Contraste renforcé', seg('contrast', [[false, 'Non'], [true, 'Oui']]))}
        <div class="lbl">Accessibilité</div>${row('Police', seg('readable', [[false, 'Radio'], [true, 'Lisible']]))}${row('Texte des dialogues', seg('textMode', [['instant', 'Instantané'], ['defilant', 'Défilant']]))}${row('Réduire les animations', seg('reduceMotion', [[false, 'Non'], [true, 'Oui']]))}
        <div class="lbl">Langue</div>${row('Langue', '<span class="seg"><button class="btn sel">Français</button></span>')}
        <p class="muted">Réglages gardés sur cet appareil, hors sauvegardes. Les effets sonores arriveront avec le combat.</p>`;
    } else if (sub === 'codex') {
      S.innerHTML = `<button class="btn m-back" data-back="1">‹ Retour</button><h2>CODEX</h2><p>Le codex se remplira en jouant : lieux, factions, peuples, objets.</p><p class="muted">Aucune entrée pour l'instant.</p>`;
    } else if (sub === 'credits') {
      S.innerHTML = `<button class="btn m-back" data-back="1">‹ Retour</button><h2>CRÉDITS</h2><p><span class="lbl">Univers et conception</span><br>Valentin Sartorius · roman <i>No Man's Land, tome 1 : Un réveil tardif</i></p>
        <p><span class="lbl">Musique</span><br>Ambiance de Dusk-Town, fournie par Valentin</p><p><span class="lbl">Polices</span><br>IBM Plex Mono, VT323 (SIL Open Font License)</p><p><span class="lbl">Moteur</span><br>three.js (MIT)</p><p class="muted">Prototype · lot 1 (v10)</p>`;
    }
  }
  function newGame() { onStart(null); close(); }
  function load(slot) { const r = read(slot); if (!r || !game.restore(r.state)) { flash('Sauvegarde illisible : ignorée.'); return; } onStart(r); close(); }
  function flash(t) { $('menu-note').textContent = t; setTimeout(() => $('menu-note').textContent = '', 3000); }
  M.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b || b.disabled) return;
    if (b.id === 'm-resume') return close();
    if (b.dataset.back) { sub = null; return render(); }
    if (b.id === 'm-continue') { const l = latest(); if (l) load(l.s); return; }
    if (b.id === 'm-new') return newGame();
    if (b.id === 'm-quit') { sub = null; return open('title'); }
    if (b.dataset.sub) { sub = sub === b.dataset.sub ? null : b.dataset.sub; return render(); }
    if (b.dataset.act === 'load') return load(b.dataset.slot);
    if (b.dataset.act === 'save') { flash(write(b.dataset.slot) ? `Sauvegardé · emplacement ${b.dataset.slot}` : 'Échec de la sauvegarde (stockage plein ?)'); return render(); }
    if (b.dataset.opt) { options[b.dataset.opt] = JSON.parse(b.dataset.val); saveOptions(); return render(); }
  });
  M.addEventListener('input', e => { const k = e.target.dataset.range; if (!k) return; options[k] = +e.target.value; $('v-' + k).textContent = options[k]; saveOptions(); });
  addEventListener('keydown', e => { if (mode === 'closed' || e.key !== 'Escape') return; e.stopImmediatePropagation(); if (sub) { sub = null; render(); } else if (mode === 'pause') close(); }, true);
  applyOptions(options);
  open('title');
  return { isOpen: () => mode !== 'closed', pause: () => open('pause'), autosave: () => write(AUTO), get options() { return options; }, read, latest };
}
