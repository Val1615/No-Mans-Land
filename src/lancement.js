// Lancement : ouvrir le menu Terminal dès que son code et ses calques sont prêts,
// sans attendre le catalogue ni le rendu de Center-Town (chargés ensuite par main.js).
// Optimisation (12/11) : le menu ne dépend plus de main.js pour son visage. Dès l'ouverture :
// - la ligne sous CONTINUER est lue dans localStorage (même format que shell.js) ;
// - la musique du menu part au premier geste, sur l'<audio id="music"> du HTML (autoplay navigateur respecté) ;
// - un choix cliqué avant que main.js soit prêt garde le Terminal à l'écran avec le sceau de chargement NML, puis est rejoué.
import { createTerminal, LIGNES } from './ui/menu_terminal.js';
import { sceau, echelleTerminal, placeTerminal } from './ui/monogramme.js';

function optionsLancement() {
  if (window.__nml && window.__nml.shell && window.__nml.shell.options) return window.__nml.shell.options;
  try {
    const o = JSON.parse(localStorage.getItem('nml_options') || 'null');
    return { reduceMotion: !!(o && o.reduceMotion), music: o && typeof o.music === 'number' ? Math.max(0, Math.min(100, o.music)) : 100 };
  } catch { return { reduceMotion: false, music: 100 }; }
}

// ---------- sauvegardes : même lecture que shell.js (latest / render), sans importer le jeu ----------
const DEV = new URLSearchParams(location.search).get('dev') === '1'; // sauvegardes DEV séparées
const SAVE_VERSION = 2;
function lireSauvegarde(s) {
  let o; try { o = JSON.parse(localStorage.getItem((DEV ? 'nml_dev_save_' : 'nml_save_') + s)); } catch { return null; }
  if (!o || typeof o !== 'object') return null;
  if (o.v === undefined && o.location && o.player) o = { v: 1, t: 0, label: '', state: o };
  if (o.v > SAVE_VERSION || !o.state || typeof o.state.location !== 'string' || !o.state.player) return null;
  return o;
}
export function derniereSauvegarde() {
  return ['auto', '1', '2', '3'].map(s => ({ s, r: lireSauvegarde(s) })).filter(x => x.r).sort((a, b) => b.r.t - a.r.t)[0] || null;
}
const fmt = t => t ? new Date(t).toLocaleString('fr-FR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' }).replace(',', '') : '';
function remplirTitre() {
  if (window.__nml && window.__nml.shell) return; // le shell tient le menu
  const last = derniereSauvegarde(), $ = id => document.getElementById(id);
  $('m-continue').disabled = !last;
  $('m-continue-info').textContent = last ? `${last.s === 'auto' ? 'Auto' : 'Emplacement ' + last.s} · ${last.r.label} · ${fmt(last.r.t)}` : 'AUCUNE SESSION ANTERIEURE';
  $('m-quit').disabled = true; $('m-quit-info').textContent = 'aucune session ouverte';
  return last;
}

const M = document.getElementById('menu');
document.body.classList.add('menu-open');
M.hidden = false;
M.classList.add('term');
const derniere = remplirTitre();

// ---------- musique du menu au premier geste (main.js / ost_centre.js reprend le même élément, sans coupure) ----------
const musique = document.getElementById('music');
function gesteMusique(e) {
  if (e && e.type === 'pointerdown' && e.pointerType && e.pointerType !== 'mouse') return; // tactile : l'activation vient au pointerup
  if (window.__nmlMusiqueLancee) return fin();
  if (window.__nml && window.__nml.music) return fin(); // ost_centre.js a la main
  const o = optionsLancement();
  musique.muted = localStorage.getItem('nml_muted') === '1';
  musique.volume = Math.max(0, Math.min(1, 0.55 * ((o.music ?? 100) / 100)));
  musique.preload = 'auto';
  const p = musique.play();
  window.__nmlMusiqueLancee = true;
  if (p && p.catch) p.catch(() => { window.__nmlMusiqueLancee = false; });
  fin();
}
const GESTES = ['pointerdown', 'pointerup', 'touchend', 'keydown', 'click'];
function fin() { if (window.__nmlMusiqueLancee || (window.__nml && window.__nml.music)) for (const g of GESTES) removeEventListener(g, gesteMusique, true); }
for (const g of GESTES) addEventListener(g, gesteMusique, g === 'touchend' ? { capture: true, passive: true } : true);

const term = createTerminal({
  M,
  getOptions: optionsLancement,
  note: t => { const n = document.getElementById('menu-note'); if (n) n.textContent = t; },
});

let resoudreCadre; const cadrePret = new Promise(r => { resoudreCadre = r; });
window.__nmlMenu = { terminal: term, derniere: derniere ? { slot: derniere.s, location: derniere.r.state.location } : null, cadrePret, derniereSauvegarde };
// Le cadre et le fond du Terminal passent d'abord, seuls sur la ligne ; main.js (three.js, données, manifestes) est importé juste après.
await term.pret;
resoudreCadre(true);
const principal = import('./main.js');
term.open('title');
window.__nmlMenuPret = true;

// Un choix cliqué avant que main.js ait branché le shell : le Terminal reste là, sceau NML (anneau à 0 %), puis le choix est rejoué.
let choixAttendu = null;
M.addEventListener('pointerdown', e => {
  if (window.__nml && window.__nml.shell) return;
  const b = e.target.closest('.t-list button'); if (!b || !b.disabled) return;
  const n = document.getElementById('menu-note'); if (n) n.textContent = b.id === 'm-continue' ? LIGNES.continuerVide : b.id === 'm-quit' ? LIGNES.nonPrevue : LIGNES.refus;
}, true);
M.addEventListener('click', e => {
  if (window.__nml && window.__nml.shell) return;
  const b = e.target.closest('.t-list button');
  if (!b || b.disabled) return;
  choixAttendu = b.id;
  if (b.dataset.sub) return; // sous-menus (Charger, Options, Crédits) : rejoués dès que le shell est prêt, sans geler le Terminal
  term.confirmer(b);
  M.classList.add('t-charge'); M.querySelectorAll('.t-choisi').forEach(x => x.classList.remove('t-choisi')); b.classList.add('t-choisi');
  const n = document.getElementById('menu-note'), d = b.id === 'm-continue' ? derniereSauvegarde() : null;
  if (n) { const s = sceau(n, { id: d ? d.r.state.location : '', nom: d ? (d.r.label || '').split('· ').pop().toUpperCase() : '', p: 0, echelle: echelleTerminal(M) }); placeTerminal(n, s); }
}, true);

principal.then(() => {
  const id = choixAttendu; choixAttendu = null;
  if (id && window.__nml && window.__nml.shell) { M.classList.remove('t-charge'); document.getElementById(id)?.click(); }
});
