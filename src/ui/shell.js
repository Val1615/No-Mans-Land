// v10 lot 1 : menu principal, pause, sauvegardes (3 emplacements + auto), options. Style UI v8 « radio ambre ».
// Stockage localStorage versionné : nml_save_1..3, nml_save_auto ({ v, t, label, state }) ; options : nml_options ({ v, ... }).
import { createCreation } from './creation.js';
import { DEFAULT_DRAFT, buildCharacter, raceFlags } from '../data/character.js';
import { createTerminal, LIGNES } from './menu_terminal.js'; // menu « Terminal Human Corp » (docs/ui/MENU_TERMINAL.md)
// v2 (lot 2) : l'état contient le personnage (state.character). Une sauvegarde v1 (avant la création) reçoit le perso par défaut.
export const SAVE_VERSION = 2, OPT_VERSION = 1;
const SLOTS = ['1', '2', '3'], AUTO = 'auto';
export const DEFAULT_OPTIONS = { music: 100, sfx: 100, minimal: false, textSize: 100, contrast: false, readable: false, textMode: 'instant', reduceMotion: false };

// Migration sûre : un format inconnu ou abîmé n'est jamais chargé et ne fait jamais planter le jeu.
export function migrateSave(raw) {
  let o; try { o = typeof raw === 'string' ? JSON.parse(raw) : raw; } catch { return null; }
  if (!o || typeof o !== 'object') return null;
  if (o.v === undefined && o.location && o.player) o = { v: 1, t: 0, label: '', state: o }; // v0 : instantané nu (prototype) -> v1
  if (o.v > SAVE_VERSION || !o.state || typeof o.state.location !== 'string' || !o.state.player) return null;
  if (o.v < 2) { // v1 -> v2 : perso par défaut, PV / $ / inventaire gardés tels quels
    const c = buildCharacter(DEFAULT_DRAFT);
    o = { ...o, v: 2, state: { ...o.state, character: c, flags: { ...raceFlags(c), ...(o.state.flags || {}) } } };
  }
  return o;
}
export function migrateOptions(raw) {
  let o; try { o = JSON.parse(raw || 'null'); } catch { o = null; }
  const out = { ...DEFAULT_OPTIONS };
  if (o && typeof o === 'object' && !(o.v > OPT_VERSION)) for (const k of Object.keys(DEFAULT_OPTIONS)) if (typeof o[k] === typeof DEFAULT_OPTIONS[k]) out[k] = o[k];
  out.music = Math.max(0, Math.min(100, out.music)); out.sfx = Math.max(0, Math.min(100, out.sfx)); if (![100, 115, 130].includes(out.textSize)) out.textSize = 100;
  return out;
}

export function createShell({ game, world, $, onStart, applyOptions, terminal, prepare = null, pretLieu = null, ligneChargement = null, departNouvelle = null }) {
  const LS = window.localStorage;
  const DEV = new URLSearchParams(location.search).get('dev') === '1'; // mode DEV : emplacements séparés, jamais ceux du joueur
  const key = s => (DEV ? 'nml_dev_save_' : 'nml_save_') + s;
  const read = s => migrateSave(LS.getItem(key(s)));
  const fmt = t => t ? new Date(t).toLocaleString('fr-FR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' }).replace(',', '') : '';
  const label = () => (game.state.character ? game.state.character.name + ' · ' : '') + world.LOCATIONS[game.state.location].name.replace('Dusk-Town · ', '');
  function write(slot) {
    const rec = { v: SAVE_VERSION, t: Date.now(), label: label(), state: game.snapshot() };
    try { LS.setItem(key(slot), JSON.stringify(rec)); return true; } catch { return false; }
  }
  const latest = () => [AUTO, ...SLOTS].map(s => ({ s, r: read(s) })).filter(x => x.r).sort((a, b) => b.r.t - a.r.t)[0] || null;
  let options = migrateOptions(LS.getItem('nml_options'));
  const saveOptions = () => { LS.setItem('nml_options', JSON.stringify({ v: OPT_VERSION, ...options })); applyOptions(options); };

  // 5 appuis sur le numéro de version en ~3 s : débloque le bouton « Mode DEV » d'Options (comme une visite avec ?dev=1)
  { let taps = []; const V = document.getElementById('m-version');
    V?.addEventListener('click', () => { const t = Date.now(); taps = [...taps.filter(x => t - x < 3000), t];
      if (taps.length >= 5) { taps = []; LS.setItem('nml_dev_unlocked', '1'); flash(LIGNES.maintenance + ' Bouton « Mode DEV » dans Options.'); if (sub === 'options') render(); } }); }
  let mode = 'title', sub = null; // mode : title | pause | closed
  const M = $('menu'), S = $('menu-sub');
  const term = terminal || createTerminal({ M, getOptions: () => options, note: t => flash(t) });
  let before = 'title';
  const creation = createCreation({ $, onDone: draft => lancer(departNouvelle && departNouvelle(), $('m-new'), () => { onStart(null, draft); close(); }), onCancel: () => open(before) });
  // Optimisation (12/11) : ouvrir une partie attend que le lieu d'arrivée ait ses images. Pendant ce temps, le Terminal reste à l'écran,
  // choix gelés, avec la ligne de chargement et sa progression ; jamais de menu caché sur du vide.
  let jeton = 0;
  function lancer(loc, bouton, fin) {
    const id = ++jeton;
    if (!prepare || !loc || (pretLieu && pretLieu(loc))) { M.classList.remove('t-charge'); return fin(); }
    if (mode === 'create' || M.hidden) { creation.close(); mode = before === 'pause' ? 'pause' : 'title'; M.hidden = false; document.body.classList.add('menu-open'); M.classList.toggle('pause', mode === 'pause'); sub = null; render(); term.open(mode); term.saute(); }
    sub = null; S.hidden = true; M.classList.remove('sub-open');
    M.classList.add('t-charge'); M.querySelectorAll('.t-choisi').forEach(x => x.classList.remove('t-choisi')); bouton?.classList.add('t-choisi');
    clearTimeout(flashT); const note = $('menu-note'), ligne = (f, t) => { if (ligneChargement) ligneChargement(loc, f, t, note); else note.textContent = 'CHARGEMENT DU SECTEUR…'; };
    ligne(0, 1);
    // lieu prêt : la ligne affiche 100 % et reste peinte pendant la mise en place de la scène (première image du lieu), puis le jeu s'ouvre
    const raf = () => new Promise(r => { requestAnimationFrame(() => r()); setTimeout(r, 120); }); // onglet caché : pas de rAF
    prepare(loc, e => { if (id === jeton) ligne(e.fait, e.total); }).then(async () => { if (id !== jeton) return; ligne(1, 1); await raf(); await raf(); if (id !== jeton) return;
      M.classList.remove('t-charge'); bouton?.classList.remove('t-choisi'); note.textContent = ''; fin(); });
  }
  const open = m => { mode = m; M.hidden = false; document.body.classList.add('menu-open'); M.classList.toggle('pause', m === 'pause'); render(); term.open(m); };
  const close = () => { mode = 'closed'; sub = null; M.hidden = true; creation.close(); document.body.classList.remove('menu-open'); term.close(); };
  function render() {
    const last = latest(), inGame = mode === 'pause';
    $('m-resume').hidden = !inGame;
    $('m-continue').disabled = !last; $('m-continue-info').textContent = last ? `${last.s === AUTO ? 'Auto' : 'Emplacement ' + last.s} · ${last.r.label} · ${fmt(last.r.t)}` : 'AUCUNE SESSION ANTERIEURE';
    $('m-load').querySelector('span').textContent = inGame ? 'CHARGER / SAUVEGARDER' : 'CHARGER';
    // Codex : entrée de partie (pause), hors des six choix de l'écran titre. Quitter : sans action sur l'écran titre (un onglet ne se ferme pas), désactivé.
    $('m-codex').hidden = !inGame; $('m-quit').disabled = !inGame; $('m-quit-info').textContent = inGame ? "retour à l'écran titre" : 'aucune session ouverte';
    M.querySelectorAll('.m-main button').forEach(b => b.classList.toggle('sel', b.dataset.sub === sub));
    S.hidden = !sub; M.classList.toggle('sub-open', !!sub); term.rendu(); if (!sub) return;
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
        ${LS.getItem('nml_dev_unlocked') === '1' ? `<div class="lbl">Développement</div>${row(DEV ? 'Mode DEV actif' : 'Mode DEV inactif', '<span class="seg"><button class="btn' + (DEV ? ' sel' : '') + '" id="m-dev">Mode DEV</button></span>')}` : ''}
        <p class="muted">Réglages gardés sur cet appareil, hors sauvegardes. Les effets sonores arriveront avec le combat.</p>`;
    } else if (sub === 'codex') {
      S.innerHTML = `<button class="btn m-back" data-back="1">‹ Retour</button><h2>CODEX</h2><p>Le codex se remplira en jouant : lieux, factions, peuples, objets.</p><p class="muted">Aucune entrée pour l'instant.</p>`;
    } else if (sub === 'credits') {
      S.innerHTML = `<button class="btn m-back" data-back="1">‹ Retour</button><h2>CRÉDITS</h2><p><span class="lbl">Univers et conception</span><br>Valentin Sartorius · roman <i>No Man's Land, tome 1 : Un réveil tardif</i></p>
        <p><span class="lbl">Musique</span><br>Ambiance de Dusk-Town · OST Center-Town : Groovy Crew (fournies par Valentin)</p><p><span class="lbl">Polices</span><br>IBM Plex Mono, VT323 (SIL Open Font License)</p><p><span class="lbl">Moteur</span><br>three.js (MIT)</p><p class="muted">Prototype · lot 1 (v10)</p>`;
    }
  }
  function newGame() { before = mode; sub = null; mode = 'create'; M.hidden = true; creation.open(); }
  function load(slot, bouton) { const r = read(slot); if (!r) { flash('Sauvegarde illisible : ignorée.'); return; }
    lancer(world.LOCATIONS[r.state.location] ? r.state.location : null, bouton, () => { if (!game.restore(r.state)) { flash('Sauvegarde illisible : ignorée.'); return; } onStart(r); close(); }); }
  let flashT = 0; function flash(t) { $('menu-note').textContent = t; clearTimeout(flashT); flashT = setTimeout(() => $('menu-note').textContent = '', 3000); }
  // choix grisés : un geste dessus affiche la ligne du terminal (fiche §6.4), sans action
  M.addEventListener('pointerdown', e => { const b = e.target.closest('.t-list button'); if (!b || !b.disabled) return;
    flash(b.id === 'm-continue' ? LIGNES.continuerVide : b.id === 'm-quit' ? LIGNES.nonPrevue : LIGNES.refus); });
  M.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b || b.disabled) return;
    if (b.closest('.t-list')) term.confirmer(b);
    // Mode DEV (débloqué par une visite avec ?dev=1) : bascule par rechargement, pour garder les sauvegardes DEV séparées de celles du joueur
    if (b.id === 'm-dev') { const u = new URL(location.href); if (DEV) { u.searchParams.delete('dev'); u.searchParams.delete('devpanel'); } else { u.searchParams.set('dev', '1'); u.searchParams.set('devpanel', '1'); } location.href = u.toString(); return; }
    if (b.id === 'm-resume') return close();
    if (b.dataset.back) { sub = null; return render(); }
    if (b.id === 'm-continue') { const l = latest(); if (l) load(l.s, b); return; }
    if (b.id === 'm-new') return newGame();
    if (b.id === 'm-quit') { sub = null; open('title'); return flash(LIGNES.quitter); }
    if (b.dataset.sub) { sub = sub === b.dataset.sub ? null : b.dataset.sub; return render(); }
    if (b.dataset.act === 'load') return load(b.dataset.slot, $('m-load'));
    if (b.dataset.act === 'save') { flash(write(b.dataset.slot) ? `Sauvegardé · emplacement ${b.dataset.slot}` : 'Échec de la sauvegarde (stockage plein ?)'); return render(); }
    if (b.dataset.opt) { options[b.dataset.opt] = JSON.parse(b.dataset.val); saveOptions(); if (b.dataset.opt === 'reduceMotion') term.appliqueReduit(); return render(); }
  });
  M.addEventListener('input', e => { const k = e.target.dataset.range; if (!k) return; options[k] = +e.target.value; $('v-' + k).textContent = options[k]; saveOptions(); });
  addEventListener('keydown', e => { if (mode === 'closed' || e.key !== 'Escape') return; e.stopImmediatePropagation(); if (mode === 'create') creation.back(); else if (sub) { sub = null; render(); } else if (mode === 'pause') close(); }, true);
  applyOptions(options);
  open('title');
  return { terminal: term, get creationDraft() { return creation.draft; }, isOpen: () => mode !== 'closed', pause: () => open('pause'), autosave: () => write(AUTO), get options() { return options; }, read, latest };
}
