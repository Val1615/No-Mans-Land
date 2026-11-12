// Monogramme NML : sceau de chargement (proposition B d'Ocre, choisie par Valentin le 12/11).
// Remplace la ligne « CHARGEMENT DU SECTEUR [####----] n % » dans le Terminal (#menu-note, pendant t-charge) et sur l'overlay en jeu (#chargement).
// Dessiné en canvas (devicePixelRatio), aucun calque image : géométrie reprise de mark_mono() (nml-shots/chargement_logo/build.py),
// repère 480 × 360 de la maquette, centre (0, 0) ici. Hexagone extérieur 108 (trait 2), intérieur 96 (trait 1), anneau 118 (trait 3),
// « NML » en VT 78 px, tracking 2 ; légende Plex « SECTEUR   n % » sous l'anneau.
// Mouvement : entrée ~1 s (l'hexagone se trace 0 -> 28 %, l'intérieur paraît une fois l'extérieur clos, les lettres s'allument 15 -> 50 %),
// puis seul l'anneau avance, sur la VRAIE progression du chargement du lieu (fait / total), depuis midi, sens horaire, point vif en tête.
// Mouvement réduit : hexagone et lettres déjà là, seul l'anneau (et le %) avance.
// Le texte pour lecteur d'écran (secteur + %) reste dans l'élément role=status, hors de la vue.
const PH = '242,180,74', VIF = '255,208,120';
const R_OUT = 108, R_IN = 96, R_RING = 118, MARGE = 14; // MARGE : place du halo autour de l'anneau (repère maquette)
const ENTREE_MS = 1000;
const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const hexPts = r => Array.from({ length: 6 }, (_, i) => { const a = (60 * i - 30) * Math.PI / 180; return [r * Math.cos(a), r * Math.sin(a)]; });

export function mouvementReduit(el) {
  try { if (matchMedia('(prefers-reduced-motion: reduce)').matches) return true; } catch { /* vieux navigateur */ }
  return document.body.classList.contains('reduce-motion') || !!(el && el.closest && el.closest('#menu.term.t-reduit'));
}

// polices du sceau : chargées une fois (le canvas ne déclenche pas le chargement d'une @font-face)
let policesPretes = null;
const polices = () => policesPretes || (policesPretes = (document.fonts && document.fonts.load
  ? Promise.all([document.fonts.load('78px VT', 'NML'), document.fonts.load('15px Plex', 'CENTER-TOWN 0 %')]).catch(() => null) : Promise.resolve()));

function creer(hote) {
  const racine = document.createElement('span'); racine.className = 'nml-sceau'; racine.setAttribute('aria-hidden', 'true');
  const cv = document.createElement('canvas'); cv.className = 'nml-sceau-cv';
  const leg = document.createElement('span'); leg.className = 'nml-sceau-leg';
  racine.append(cv, leg);
  const lu = document.createElement('span'); lu.className = 'nml-sceau-lu'; // texte lu (role=status de l'hôte)
  hote.textContent = ''; hote.append(racine, lu);
  const s = { hote, racine, cv, leg, lu, id: null, t0: performance.now(), cible: 0, vu: 0, echelle: 0.5, raf: 0, last: 0, nom: '', pct: -1, luPct: -1, court: false };
  polices().then(() => dessine(s));
  return s;
}

// échelle : taille du sceau (1 = repère de la maquette, en px CSS). Taille CSS du canvas = 2 × (R_RING + MARGE) × échelle.
function taille(s, e) {
  s.echelle = e; const dpr = Math.min(3, window.devicePixelRatio || 1), c = Math.ceil(2 * (R_RING + MARGE) * e);
  for (const x of [s.racine, s.hote]) { x.style.setProperty('--sceau', c + 'px'); x.style.setProperty('--sceau-e', e.toFixed(4)); }
  if (s.cv.width !== Math.round(c * dpr)) { s.cv.width = Math.round(c * dpr); s.cv.height = Math.round(c * dpr); }
  s.cv.style.width = s.cv.style.height = c + 'px';
}

function dessine(s, now = performance.now()) {
  const { cv } = s, g = cv.getContext('2d'); if (!g || !cv.width) return;
  const dpr = cv.width / (parseFloat(cv.style.width) || cv.width), e = s.echelle, k = e * dpr, reduit = mouvementReduit(s.hote);
  const intro = reduit ? 1 : clamp((now - s.t0) / ENTREE_MS);
  const ring = s.vu;
  g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, cv.width, cv.height);
  g.setTransform(k, 0, 0, k, cv.width / 2, cv.height / 2);
  g.lineCap = 'butt'; g.lineJoin = 'miter';
  // trait minimal à l'écran (petits formats : 390, fold) pour que le dessin ne s'efface pas
  const trait = (ref, minPx) => Math.max(ref, minPx / e);
  // halo phosphore (composite_glow de la maquette : flou r puis r/2, puis le trait net) ; shadowBlur est en px du canvas
  const halo = (dessin, col, r, force) => {
    for (const [rr, f] of [[r, force], [Math.max(2, r / 2), force * 0.8]]) {
      g.shadowColor = `rgba(${col},${clamp(f)})`; g.shadowBlur = Math.max(1.5 * dpr, 2 * rr * k); dessin(); }
    g.shadowColor = 'transparent'; g.shadowBlur = 0; dessin();
  };
  // hexagone extérieur : se trace côté après côté ; intérieur une fois l'extérieur clos
  const hexFrac = intro > 0.02 ? clamp(intro / 0.28) : 0;
  const hex = (r, frac, w) => { const p = hexPts(r), n = 6 * frac; g.beginPath(); g.moveTo(...p[0]);
    for (let i = 0; i < 6; i++) { const f = n - i; if (f <= 0) break; const a = p[i], b = p[(i + 1) % 6];
      if (f >= 1) g.lineTo(...b); else g.lineTo(a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f); }
    if (frac >= 1) g.closePath(); g.lineWidth = w; g.strokeStyle = `rgb(${PH})`; g.stroke(); };
  if (hexFrac > 0) halo(() => { hex(R_OUT, hexFrac, trait(2, 1)); if (hexFrac >= 1) hex(R_IN, 1, trait(1, 0.75)); }, PH, 5, 0.6);
  // lettres NML (VT, tracking 2), plus vives en fin de chargement
  const op = clamp((intro - 0.15) / 0.35);
  if (op > 0) {
    const col = intro >= 1 && ring > 0.9 ? VIF : PH;
    g.font = "78px 'VT', monospace"; g.textBaseline = 'alphabetic'; g.textAlign = 'left';
    const lettres = [...'NML'], ws = lettres.map(c => g.measureText(c).width), tot = ws.reduce((a, b) => a + b, 0) + 2 * (lettres.length - 1);
    const m = g.measureText('NML'), haut = (m.actualBoundingBoxAscent || 50) + (m.actualBoundingBoxDescent || 0);
    const y = (m.actualBoundingBoxAscent || 50) - haut / 2 + 4;
    const ecrit = () => { let x = -tot / 2; for (let i = 0; i < lettres.length; i++) { g.fillText(lettres[i], x, y); x += ws[i] + 2; } };
    g.globalAlpha = 0.15 + 0.85 * op; g.fillStyle = `rgb(${col})`;
    halo(ecrit, col, 8 + 6 * op, 0.8 * op);
    g.globalAlpha = 1;
  }
  // anneau de progression : depuis midi, sens horaire, sur le vrai % du chargement
  if (ring > 0.001) {
    const col = ring > 0.97 ? VIF : PH;
    halo(() => { g.beginPath(); g.arc(0, 0, R_RING, -Math.PI / 2, -Math.PI / 2 + 2 * Math.PI * ring); g.lineWidth = trait(3, 1.5); g.strokeStyle = `rgb(${col})`; g.stroke(); }, col, 5, 0.75);
  }
  if (ring > 0.05 && ring < 0.99) {
    const a = -Math.PI / 2 + 2 * Math.PI * ring, x = R_RING * Math.cos(a), y = R_RING * Math.sin(a), r = trait(3, 1.6);
    halo(() => { g.beginPath(); g.arc(x, y, r, 0, 2 * Math.PI); g.fillStyle = `rgb(${VIF})`; g.fill(); }, VIF, 4, 0.8);
  }
}

function anime(s) {
  if (s.raf) return;
  const pas = now => {
    s.raf = 0; if (!s.racine.isConnected) return;
    const dt = Math.min(0.1, (now - (s.last || now)) / 1000); s.last = now;
    const reduit = mouvementReduit(s.hote);
    s.vu = reduit ? s.cible : s.vu + (s.cible - s.vu) * Math.min(1, dt * 9);
    if (Math.abs(s.cible - s.vu) < 0.002) s.vu = s.cible;
    dessine(s, now);
    if (s.vu !== s.cible || (!reduit && now - s.t0 < ENTREE_MS + 50)) s.raf = requestAnimationFrame(pas);
    else s.last = 0;
  };
  s.raf = requestAnimationFrame(pas);
}

// Légende : « SECTEUR   n % » ; forme courte « n % » si la longue dépasse 2,6 fois le diamètre de l'anneau (390 / fold, Terminal portrait)
function legende(s) {
  const pct = `${s.pct}\u00a0%`, longue = p => s.nom ? `${s.nom}\u00a0\u00a0\u00a0${p}\u00a0%` : `${p}\u00a0%`;
  s.leg.textContent = longue(100); // mesurée à 100 % : la forme ne change pas en cours de route
  s.court = !!s.nom && s.leg.offsetWidth > 2.6 * 2 * R_RING * s.echelle;
  s.leg.dataset.forme = s.court ? 'courte' : 'longue';
  s.leg.textContent = s.court ? pct : longue(s.pct);
}

/** Pose ou met à jour le sceau dans `hote` (élément role=status). p : 0..1 (vrai progrès), nom : secteur en capitales. */
export function sceau(hote, { id = '', nom = '', p = 0, echelle = 0.5 } = {}) {
  let s = hote._sceau;
  if (!s || !s.racine.isConnected || s.racine.parentNode !== hote) s = hote._sceau = creer(hote);
  if (s.id !== id) { s.id = id; s.t0 = performance.now(); s.vu = 0; s.pct = -1; s.luPct = -1; }
  const neuf = Math.abs(s.echelle - echelle) > 1e-3 || !s.cv.width; if (neuf) taille(s, echelle);
  s.cible = clamp(p);
  const pct = Math.round(100 * s.cible);
  if (neuf || pct !== s.pct || s.nom !== nom) { s.pct = pct; s.nom = nom; legende(s); }
  // lecteur d'écran : secteur + %, par paliers de 10 % (pas un flot d'annonces)
  const palier = pct >= 100 ? 100 : Math.floor(pct / 10) * 10;
  if (palier !== s.luPct) { s.luPct = palier; s.lu.textContent = `Chargement du secteur${nom ? ' ' + nom : ''} : ${palier} %`; }
  anime(s);
  return s;
}

export function retireSceau(hote) { const s = hote && hote._sceau; if (s) { cancelAnimationFrame(s.raf); s.raf = 0; } if (hote) { hote._sceau = null; hote.textContent = ''; } }

// ---------- placement dans le Terminal : sous les choix gelés, dans la bande libre au-dessus du statut (paysage) ou du bandeau (portrait) ----------
export function echelleTerminal(M) {
  const k = +getComputedStyle(M).getPropertyValue('--k') || 1, portrait = M.classList.contains('t-portrait');
  return portrait ? 0.53 * k : 0.78 * k; // brief d'Ocre : ~0,52 du canvas 480 × 360 à 1280, ~0,38 (px de l'appareil) à 390
}
// Le sceau ne recouvre aucun texte : on ne compte que les boîtes de texte réelles (Range) qui croisent sa colonne (centre de l'écran) ;
// au-dessus, les choix gelés et la ligne EXEC ; au-dessous, le statut, la version et le bandeau. Il prend l'échelle visée si la bande
// le permet, sinon la plus grande qui y tient. Hauteur visible : anneau (± 120) + légende sous l'anneau (+ 128), le halo peut déborder.
const textes = el => { if (!el) return []; const r = document.createRange(); r.selectNodeContents(el); return [...r.getClientRects()].filter(b => b.width > 0 && b.height > 0); };
export function placeTerminal(hote, s) {
  const M = hote.closest('#menu'), main = hote.closest('.m-main'); if (!M || !main || !s) return;
  const Q = q => M.querySelector(q), mr = main.getBoundingClientRect(), cx = mr.left + mr.width / 2, marge = 4;
  // la ligne EXEC se tape après le clic : sa rangée entière est réservée d'emblée (le sceau ne saute pas quand elle se remplit)
  const ex = Q('#m-exec')?.getBoundingClientRect(), dessus = [...M.querySelectorAll('.t-list .btn:not([hidden])')].flatMap(textes);
  if (ex && ex.height > 0) dessus.push({ left: mr.left, right: mr.right, top: ex.top, bottom: ex.bottom });
  const dessous = [...M.querySelectorAll('.t-status span'), Q('#m-version')].flatMap(textes);
  const tk = Q('.t-ticker')?.getBoundingClientRect(); if (tk && tk.height > 0) dessous.push(tk);
  let e = echelleTerminal(M), haut = 0, bas = 0;
  for (let i = 0; i < 3; i++) {
    const capH = s.leg.offsetHeight || 13, demi = Math.max(122 * e, (s.leg.offsetWidth || 0) / 2) + 6;
    const croise = b => b.right > cx - demi && b.left < cx + demi;
    haut = dessus.filter(croise).reduce((a, b) => Math.max(a, b.bottom), mr.top) + marge;
    bas = dessous.filter(b => croise(b) && b.top > haut).reduce((a, b) => Math.min(a, b.top), mr.bottom) - marge;
    const fit = Math.max(0.12, (bas - haut - capH) / 248), cible = Math.min(echelleTerminal(M), fit);
    if (Math.abs(cible - e) < 1e-3 && Math.abs(s.echelle - e) < 1e-3) break;
    e = cible; taille(s, e); legende(s);
  }
  dessine(s);
  const hv = 248 * e + (s.leg.offsetHeight || 13), y0 = haut + Math.max(0, (bas - haut - hv) / 2); // haut visible de l'anneau
  s.racine.style.top = (y0 - (132 - 120) * e - mr.top) + 'px';
}
// ---------- en jeu : badge en bas, centre de l'anneau vers 75,7 % de la hauteur (maquette : 605 / 800, 1280 / 1688, 1390 / 1830) ----------
export function echelleJeu() {
  const W = innerWidth, H = innerHeight;
  return H > W ? clamp(W / 1625, 0.24, 0.43) : clamp(Math.min(W / 2065, H / 1290), 0.24, 0.62);
}
