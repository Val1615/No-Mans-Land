import { placeLabels } from './placement.js';
// Lot 3 interface : carte des No Man's Land (fond, brouillard et icônes ambre d'Ocre), choix de destination, trajet case par case animé,
// halte et reprise. Logique du voyage : core/voyage.js ; terrains et réglages : data/nml.js.
const ICO = k => `./assets/ui/maps/icones/${k}_48.png`;
export function createCarteNml({ $, voyage, manifest, say, onOpenChange }) {
  const el = $('nml'), plan = $('nml-plan'), vue = $('nml-vue'), fog = $('nml-fog'), svg = $('nml-svg'), lieuxEl = $('nml-lieux'), moi = $('nml-moi');
  const N = manifest.nml_fond, F = manifest.brouillard_nml, COLS = N.grille.cols, ROWS = N.grille.rows;
  let open = false, zoom = 1, key = '', mobile = innerWidth < 700, fogImg = {}, fogKey = '';
  const img = src => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.onerror = () => r(null); i.src = src; });
  async function loadFog() { const m = mobile ? 'mobile' : 'desk'; if (fogImg[m]) return fogImg[m];
    const [t, k] = await Promise.all([img('./assets/' + (mobile ? F.texture.mobile.fichier : F.texture.fichier)), img('./assets/' + (mobile ? F.masque.mobile.fichier : F.masque.fichier))]); return fogImg[m] = { t, k }; }
  const pct = (c, r) => ({ x: 100 * (c + 0.5) / COLS, y: 100 * (r + 0.5) / ROWS });
  function size() { mobile = innerWidth < 700; $('nml-fond').src = './assets/' + (mobile ? N.mobile.fichier : N.fichier);
    const r = vue.getBoundingClientRect(), base = Math.max(200, Math.min(r.width - 4, (r.height - 4) * N.px[0] / N.px[1]));
    plan.style.width = Math.round(base * zoom) + 'px'; key = ''; fogKey = ''; }
  // brouillard : texture répétée (opacité conseillée), effacée en destination-out par le masque centré sur chaque case vue
  async function drawFog() { const R = voyage.region(), k = R.vues.join(';') + mobile; if (k === fogKey) return; fogKey = k;
    const f = await loadFog(); const s = mobile ? 50 : 100, W = COLS * s, H = ROWS * s; fog.width = W; fog.height = H; const x = fog.getContext('2d');
    x.clearRect(0, 0, W, H); x.globalCompositeOperation = 'source-over'; x.globalAlpha = F.opacite_conseillee ?? 0.94;
    if (f.t) { x.fillStyle = x.createPattern(f.t, 'repeat'); } else x.fillStyle = '#120d08'; x.fillRect(0, 0, W, H);
    x.globalAlpha = 1; x.globalCompositeOperation = 'destination-out';
    for (const v of R.vues) { const [c, r] = v.split(',').map(Number); if (c < 0 || r < 0 || c >= COLS || r >= ROWS) continue; const cx = (c + 0.5) * s, cy = (r + 0.5) * s;
      if (f.k) x.drawImage(f.k, cx - f.k.width / 2, cy - f.k.height / 2); else x.clearRect(cx - s, cy - s, 2 * s, 2 * s); }
    x.globalCompositeOperation = 'source-over'; fog.dataset.vues = R.vues.length; }
  function render() {
    const R = voyage.region(), st = R.statut, l = voyage.lieuJouableIci();
    const k = JSON.stringify([R.case, st, R.trajet, R.dest, R.connus, zoom, mobile]); if (k === key) return; key = k; drawFog();
    // lieux connus (les autres restent sous le brouillard : ni icône ni nom)
    lieuxEl.innerHTML = voyage.lieux.filter(q => R.connus[q.key]).map(q => { const p = { x: 100 * q.px[0] / N.px[0], y: 100 * q.px[1] / N.px[1] };
      return `<button class="nl ${q.jeu ? 'jeu' : ''} ${R.dest?.lieu === q.key ? 'dest' : ''} ${q.px[0] / N.px[0] > 0.7 ? 'gauche' : ''}" data-lieu="${q.key}" style="left:${p.x}%;top:${p.y}%"><img src="${ICO('lieu_decouvert')}" alt=""><span>${q.nom}</span></button>`; }).join(''); placeLabels(lieuxEl, '.nl');
    // trajet restant (pointillés) et case visée
    const pts = [R.case, ...R.trajet].map(([c, r]) => `${(c + 0.5) * 100},${(r + 0.5) * 100}`).join(' '), d = R.trajet[R.trajet.length - 1];
    svg.innerHTML = (R.trajet.length ? `<polyline points="${pts}" class="route"/>` : '') + (d ? `<rect x="${d[0] * 100 + 8}" y="${d[1] * 100 + 8}" width="84" height="84" class="cible"/>` : '');
    const H = R.trajet.reduce((a, [c, r]) => a + voyage.heures(voyage.cellAt(c, r)), 0), here = voyage.cellAt(R.case[0], R.case[1]), lh = voyage.lieuAt(R.case[0], R.case[1]);
    const nomDest = R.dest?.lieu ? voyage.lieux.find(q => q.key === R.dest.lieu).nom : R.dest?.case ? 'case ' + voyage.cellAt(...R.dest.case)?.label : '';
    $('nml-etat').textContent = st === 'route' ? `En route vers ${nomDest}` : st === 'halte' ? `Halte · ${lh && R.connus[lh.key] ? lh.nom : 'case ' + here.label} (${voyage.lieux && here ? { cote: 'côte', desert: 'désert', foret: 'forêt', rocher: 'rocher', verre: 'verre vitrifié', piste: 'piste' }[here.terrain] : ''})` : st === 'depart' ? `Sortie de ${voyage.lieux.find(q => q.key === R.lieu).nom}` : 'Carte consultative';
    $('nml-dest').textContent = st === 'lieu' ? 'Pour voyager, quitte la ville par sa route.' : R.trajet.length ? `${nomDest} · ${R.trajet.length} case${R.trajet.length > 1 ? 's' : ''} · ${H} h` : st === 'route' ? '' : 'Choisis une destination : un lieu connu ou une case.';
    $('nml-partir').hidden = !(st === 'depart' || st === 'halte'); $('nml-partir').disabled = !R.trajet.length; $('nml-partir').textContent = st === 'halte' ? 'Reprendre' : 'Partir';
    $('nml-halte').hidden = st !== 'route'; $('nml-entrer').hidden = !(l && (st === 'halte' || st === 'depart')); if (l) $('nml-entrer').textContent = (st === 'depart' ? 'Rester à ' : 'Entrer dans ') + l.nom;
    $('nml-close').disabled = st === 'route' || st === 'halte'; $('nml-close').title = st === 'depart' ? 'Rester en ville' : 'Fermer';
  }
  function frame() { if (!open) return; render(); $('nml-heure').textContent = voyage.heureTexte();
    const R = voyage.region(), a = R.case, b = R.statut === 'route' && R.trajet[0], t = b ? Math.min(1, voyage.prog) : 0, p = pct(a[0] + (b ? (b[0] - a[0]) * t : 0), a[1] + (b ? (b[1] - a[1]) * t : 0));
    moi.style.left = p.x + '%'; moi.style.top = p.y + '%';
    if (zoom > 1 && R.statut === 'route') { const r = moi.getBoundingClientRect(), v = vue.getBoundingClientRect(); if (r.left < v.left + 40 || r.right > v.right - 40 || r.top < v.top + 40 || r.bottom > v.bottom - 40) centrer(); } }
  function centrer() { const r = moi.getBoundingClientRect(), v = vue.getBoundingClientRect(); vue.scrollLeft += r.left - v.left - v.width / 2; vue.scrollTop += r.top - v.top - v.height / 2; }
  function show(o) { if (o === open) return; open = o; el.hidden = !o; document.body.classList.toggle('nml-open', o); onOpenChange?.(o); if (o) { requestAnimationFrame(() => { size(); render(); frame(); centrer(); }); } }
  plan.addEventListener('click', e => { const R = voyage.region(); if (!(R.statut === 'depart' || R.statut === 'halte')) return;
    const b = e.target.closest('.nl'); let dest;
    if (b) dest = { lieu: b.dataset.lieu }; else { const r = plan.getBoundingClientRect(), c = Math.floor((e.clientX - r.left) / r.width * COLS), w = Math.floor((e.clientY - r.top) / r.height * ROWS);
      const q = voyage.lieuAt(c, w); dest = q && R.connus[q.key] ? { lieu: q.key } : { case: [c, w] }; }
    const v = voyage.viser(dest); if (!v.ok) say(v.reason === 'mer' ? 'La mer : on ne passe pas.' : 'Impossible.'); else if (!v.cases) say('Tu y es déjà.'); key = ''; render(); });
  $('nml-partir').addEventListener('click', () => { voyage.partir(); key = ''; });
  $('nml-halte').addEventListener('click', () => { voyage.halte(); key = ''; });
  $('nml-entrer').addEventListener('click', () => { const R = voyage.region(); if (R.statut === 'depart') voyage.annuler(); else voyage.entrer(); key = ''; });
  $('nml-close').addEventListener('click', () => close());
  $('nml-zoom').addEventListener('click', () => { zoom = zoom >= 2 ? 1 : zoom + 0.5; $('nml-zoom').textContent = zoom >= 2 ? '−' : '+'; size(); render(); frame(); centrer(); });
  addEventListener('resize', () => open && size());
  function close() { const R = voyage.region(); if (R.statut === 'route' || R.statut === 'halte') return false; if (R.statut === 'depart') voyage.annuler(); show(false); return true; }
  voyage.on(ev => { key = ''; if (ev.type === 'ouvrir') show(true); if (ev.type === 'arrivee' || ev.type === 'annule') show(false);
    if (ev.type === 'arret') say(ev.lieu ? 'Halte. Ce lieu n\u2019a pas encore de terrain à explorer (prototype).' : 'Halte. Rien à explorer ici pour l\u2019instant.'); });
  return { get open() { return open; }, show, close, frame, render: () => { key = ''; render(); } };
}
