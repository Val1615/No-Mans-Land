// Lancement : ouvrir le menu Terminal dès que son code et ses calques sont prêts,
// sans attendre le catalogue ni le rendu de Center-Town (chargés ensuite par main.js).
import { createTerminal } from './ui/menu_terminal.js';

function optionsLancement() {
  if (window.__nml && window.__nml.shell && window.__nml.shell.options) return window.__nml.shell.options;
  try {
    const o = JSON.parse(localStorage.getItem('nml_options') || 'null');
    return { reduceMotion: !!(o && o.reduceMotion) };
  } catch { return { reduceMotion: false }; }
}

const M = document.getElementById('menu');
document.body.classList.add('menu-open');
M.hidden = false;
M.classList.add('term');

const term = createTerminal({
  M,
  getOptions: optionsLancement,
  note: t => { const n = document.getElementById('menu-note'); if (n) n.textContent = t; },
});

window.__nmlMenu = { terminal: term };
await term.pret;
term.open('title');
window.__nmlMenuPret = true;

// Un choix cliqué avant que main.js ait branché le shell est rejoué une fois le shell prêt.
let choixAttendu = null;
M.addEventListener('click', e => {
  if (window.__nml && window.__nml.shell) return;
  const b = e.target.closest('.t-list button');
  if (!b || b.disabled) return;
  choixAttendu = b.id;
  const n = document.getElementById('menu-note');
  if (n) n.textContent = 'CHARGEMENT DU SECTEUR…';
}, true);

import('./main.js').then(() => {
  const id = choixAttendu; choixAttendu = null;
  if (id && window.__nml && window.__nml.shell) document.getElementById(id)?.click();
});
