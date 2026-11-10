// Menu principal « Terminal Human Corp » : mise en page (paysage / portrait / repli plein cadre), séquence d'allumage sautable,
// effets CRT, bandeau de surveillance, navigation clavier. Fiche : docs/ui/MENU_TERMINAL.md ; implémentation : docs/ui/MENU_TERMINAL_IMPL.md.
// Aucun asset n'est transformé : les calques sont posés et mis à l'échelle en CSS, toujours de façon uniforme (contain / cover).
const DIR = './assets/ui/menu_terminal/';

// Configuration des cadres, lue dans manifest.json (clés paysage d'origine + objet `portrait`). Repli intégré si le manifeste manque.
// Une variante = { canvas:{w,h}, ecran:{x,y,w,h,rayon}, cadre, fond, masque, tampon:{x,y,w,h,opacite} }.
const DEFAUT = {
  paysage: { canvas: { w: 1920, h: 1080 }, ecran: { x: 168, y: 117, w: 1584, h: 821, rayon: 54 }, cadre: 'cadre.png', fond: 'fond_ecran.png', masque: 'ecran_masque.png',
    tampon: { fichier: 'tampon_acces_non_autorise.png', x: 1286, y: 708, w: 436, h: 232, opacite: 0.85 } },
  portrait: null, // fourni par manifest.json (objet `portrait`) quand les fichiers existent
};
const LARGEUR_MIN_CADRE = 390; // en dessous : repli plein cadre, sans métal (fiche §8.3)
const ECHELLE_MIN = 0.3;       // cadre `contain` trop mince : repli (plaques illisibles)

function variante(m, cle) {
  const src = cle === 'paysage' ? m : m[cle];
  if (!src || !src.canvas || !src.ecran) return null;
  const cal = id => (src.calques || []).find(c => c.id === id) || {};
  const t = cal('tampon');
  return { canvas: src.canvas, ecran: src.ecran, cadre: cal('cadre').fichier, fond: cal('fond_ecran').fichier, masque: src.masque,
    tampon: t.fichier ? { fichier: t.fichier, x: t.x, y: t.y, w: t.w, h: t.h || Math.round(t.w * 539 / 1014), opacite: t.opacite ?? 0.85 } : null };
}

export const BOOT_PAYSAGE = [
  'HUMAN CORP  //  CITIZEN OS v4.7.19', 'TERMINAL CITOYEN  HC-2175-TA', 'HORLOGE INTERNE  2175-04-12  03:42:17', 'IDENTIFIANT  HC-CTZN-8847-2175-TA',
  'CLASSEMENT  OMEGA-7  (PROVISOIRE)', 'SITE  STEEL-MEGALOPOLIS  //  CENTER-TOWN, CARREFOUR ARCADIUS', '-- chargement des privileges residuels...',
  '-- memoire vive      64 Ko     OK', '-- memoire morte     128 Ko    OK', '-- reseau Human Corp           CONNECTE    debit surveille',
  '-- module de conformite        ACTIF', '-- identification citoyen      EN ATTENTE', '-- integrite systeme           OK', '-- pret a recevoir les commandes'];
export const BOOT_PORTRAIT = ['HUMAN CORP  //  CITIZEN OS v4.7.19', 'TERMINAL CITOYEN  HC-2175-TA', 'SITE  STEEL-MEGALOPOLIS  //  CENTER-TOWN',
  '-- module de conformite        ACTIF', '-- identification citoyen      EN ATTENTE', '-- pret a recevoir les commandes'];
export const TICKER = ['HUMAN CORP. BUILDING A BETTER TOMORROW.', 'HUMAN CORP SPONSORISE LE SOURIRE.', "SOURIEZ. C'EST MESURE.",
  'COUVRE-FEU SECTORIEL : 22 H 00 A 05 H 00. LES CONTROLES SONT ALEATOIRES.', "CENTER-TOWN : CIRCULATION FLUIDE AU CARREFOUR ARCADIUS. TEMPS D'ATTENTE ACCEPTABLE.",
  'ORC ENERGIE : AJUSTEMENT DE CHARGE SUR LE RESEAU. ECONOMISEZ, CITOYEN.', 'TENG : LE CHANGE EST OUVERT. COMPTEZ DEUX FOIS.',
  "CONCERT GROOVY CREW, SPONSORISE PAR HUMAN CORP. CONTROLE D'IDENTITE A L'ENTREE.", 'PULSE PLAZA : AFFLUENCE ELEVEE. SOURIEZ, VOUS ETES ENREGISTRES.',
  'FREQUENCE STRIP : PROGRAMMATION CONFORME. NIVEAU SONORE DANS LES LIMITES AUTORISEES.', 'STEEL ARENA : PROCHAINE EPREUVE SOUS PATRONAGE HUMAN CORP. PLACES SOUS QUOTA.',
  'HUMAN CORP VOUS VEILLE. VOUS DORMEZ MIEUX AINSI.'];
export const LIGNES = {
  continuerVide: "AUCUNE SESSION ANTERIEURE. VOUS N'EXISTEZ PAS ENCORE POUR NOUS.", inconnue: 'COMMANDE INCONNUE. CETTE TENTATIVE A ETE CONSIGNEE.',
  aide: "L'AIDE N'EST PAS DISPONIBLE POUR VOTRE CLASSEMENT.", nonPrevue: "CITOYEN, CETTE FONCTION N'EST PAS INCLUSE DANS VOTRE FORFAIT.",
  refus: 'ACCES REFUSE. VEUILLEZ SOURIRE A LA CAMERA ET REESSAYER.', quitter: 'SESSION CONSIGNEE. HUMAN CORP VOUS REMERCIE POUR VOTRE TEMPS.',
  spam: 'LES RACCOURCIS NON DOCUMENTES SONT UNE INFRACTION LEGERE.', maintenance: 'MODE MAINTENANCE DEVERROUILLE.' };
const CPS = 36, PAUSE_LIGNE = 60;

export function createTerminal({ M, getOptions, note }) {
  const Q = s => M.querySelector(s);
  const scr = Q('#t-screen'), cadre = Q('#t-cadre'), fond = Q('.t-fond'), tampon = Q('#t-tampon'), bootEl = Q('#t-boot'), track = Q('#t-ticker-track'), list = Q('.t-list'), execEl = Q('#m-exec');
  const mq = matchMedia('(prefers-reduced-motion: reduce)');
  const reduit = () => mq.matches || !!getOptions()?.reduceMotion;
  let cfg = { ...DEFAUT }, dispo = { paysage: true, portrait: false }, mode = 'plein', ouvert = false, bootFait = false, boot = null, glitchT = 0, tickerT = 0, tickI = 0;

  // ---------- configuration (manifest.json) et préchargement des calques ----------
  const charge = f => new Promise(r => { const i = new Image(); i.onload = () => r(true); i.onerror = () => r(false); i.src = DIR + f; });
  const pret = (async () => {
    try { const m = await (await fetch(DIR + 'manifest.json')).json(); cfg = { paysage: variante(m, 'paysage') || DEFAUT.paysage, portrait: variante(m, 'portrait') }; } catch { /* repli DEFAUT */ }
    for (const k of ['paysage', 'portrait']) { const v = cfg[k]; dispo[k] = !!v && (await Promise.all([v.cadre, v.fond].map(charge))).every(Boolean); }
    layout();
  })();

  // ---------- mise en page : contain uniforme du cadre, rectangle écran converti en px CSS ----------
  function layout() {
    const W = innerWidth, H = innerHeight, portrait = H > W, cle = portrait ? 'portrait' : 'paysage', v = cfg[cle];
    let s = 0; if (v && dispo[cle]) s = Math.min(W / v.canvas.w, H / v.canvas.h);
    mode = v && dispo[cle] && W >= LARGEUR_MIN_CADRE && s >= ECHELLE_MIN ? cle : 'plein';
    M.dataset.cadre = mode; M.classList.toggle('t-portrait', portrait);
    const fondFichier = (portrait && cfg.portrait && dispo.portrait ? cfg.portrait : cfg.paysage).fond;
    if (mode !== 'plein') {
      const ox = (W - v.canvas.w * s) / 2, oy = (H - v.canvas.h * s) / 2, e = v.ecran;
      cadre.hidden = false; if (!cadre.src.endsWith(v.cadre)) cadre.src = DIR + v.cadre;
      Object.assign(cadre.style, { left: ox + 'px', top: oy + 'px', width: v.canvas.w * s + 'px', height: v.canvas.h * s + 'px' });
      Object.assign(scr.style, { left: ox + e.x * s + 'px', top: oy + e.y * s + 'px', width: e.w * s + 'px', height: e.h * s + 'px', borderRadius: e.rayon * s + 'px' });
      // fond : image du canevas entier, posée à la même échelle que le cadre, vue par le trou (alignement exact)
      Object.assign(fond.style, { left: -e.x * s + 'px', top: -e.y * s + 'px', width: v.canvas.w * s + 'px', height: v.canvas.h * s + 'px', backgroundImage: `url(${DIR + v.fond})`, backgroundSize: '100% 100%' });
      const t = v.tampon; if (t) Object.assign(tampon.style, { left: (t.x - e.x) * s + 'px', top: (t.y - e.y) * s + 'px', width: t.w * s + 'px', height: t.h * s + 'px', opacity: '' });
      M.style.setProperty('--k', s.toFixed(4));
    } else { // repli : écran plein cadre, sans métal ; fond en cover (seulement l'image de ville)
      cadre.hidden = true; Object.assign(scr.style, { left: '0px', top: '0px', width: W + 'px', height: H + 'px', borderRadius: '0px' });
      Object.assign(fond.style, { left: '0px', top: '0px', width: '100%', height: '100%', backgroundImage: `url(${DIR + fondFichier})`, backgroundSize: 'cover' });
      const tw = Math.min(W * 0.46, 220); Object.assign(tampon.style, { width: tw + 'px', height: tw * 539 / 1014 + 'px', left: (W - tw) / 2 + 'px', top: 'auto', bottom: Math.max(36, H * 0.05) + 'px' });
      M.style.setProperty('--k', Math.max(0.3, Math.min(W / 1584, H / 821, 1)).toFixed(4));
    }
    requestAnimationFrame(garde); tickerVitesse();
  }
  // Le tampon ne recouvre jamais un choix : réduit, puis retiré si besoin (contrôlé après chaque mise en page / rendu).
  function garde() {
    if (M.hidden) return;
    tampon.classList.remove('t-cache'); tampon.style.transform = '';
    const sub = !Q('#menu-sub').hidden;
    const boites = [...list.querySelectorAll('button:not([hidden])'), Q('#menu-note'), Q('#m-exec'), ...(sub ? [Q('#menu-sub')] : [])].map(b => b.getBoundingClientRect()).filter(r => r.width && r.height);
    const coupe = () => { const t = tampon.getBoundingClientRect(); return boites.some(r => r.left < t.right && r.right > t.left && r.top < t.bottom && r.bottom > t.top); };
    if (coupe()) { tampon.style.transform = 'scale(.7)'; tampon.style.transformOrigin = '50% 100%'; if (coupe()) tampon.classList.add('t-cache'); }
  }
  addEventListener('resize', () => { if (ouvert) layout(); });

  // ---------- bandeau de surveillance : ~45 px/s à l'échelle du terminal ; en mouvement réduit, un message toutes les 4 s ----------
  const ordre = TICKER.slice();
  function tickerRemplit() { const t = ordre.join('  //  ') + '  //  '; track.innerHTML = `<span>${t}</span><span>${t}</span>`; }
  function tickerVitesse() { const half = track.firstElementChild?.offsetWidth || 0, k = +getComputedStyle(M).getPropertyValue('--k') || 1; if (half) track.style.animationDuration = (half / (45 * Math.max(k, 0.5))).toFixed(1) + 's'; }
  function tickerReduit() { clearInterval(tickerT); tickerT = 0; if (!reduit() || !ouvert) return; const show = () => { track.innerHTML = `<span>${ordre[tickI++ % ordre.length]}</span>`; }; show(); tickerT = setInterval(() => { if (!document.hidden) show(); }, 4000); }

  // ---------- glitch : toutes les 8 à 20 s, 120 ms, jamais sur les choix ni pendant une confirmation ----------
  let confirme = false;
  function glitchPlan() { clearTimeout(glitchT); glitchT = 0; if (!ouvert || reduit() || document.hidden || M.hidden) return; glitchT = setTimeout(glitch, 8000 + Math.random() * 12000); }
  function glitch() {
    if (!ouvert || reduit() || document.hidden || M.hidden) return;
    const g = Q('.t-glitch'), sr = scr.getBoundingClientRect(), lr = list.getBoundingClientRect(), h = 8 + Math.random() * 8;
    let y = Math.random() * (sr.height - h);
    if (y + sr.top < lr.bottom + 4 && y + h + sr.top > lr.top - 4) y = Math.random() < 0.5 ? Math.max(0, lr.top - sr.top - h - 6 - Math.random() * 40) : Math.min(sr.height - h, lr.bottom - sr.top + 6 + Math.random() * 40);
    if (!confirme) { g.style.top = y + 'px'; g.style.height = h + 'px'; g.style.setProperty('--dx', (Math.random() < 0.5 ? -1 : 1) * (6 + Math.random() * 10) + 'px'); M.classList.add('t-glitching'); setTimeout(() => M.classList.remove('t-glitching'), 120); }
    glitchPlan();
  }

  // ---------- séquence d'allumage (sautable : toute touche, clic ou tap) ----------
  const phases = ['b-off', 'b-line', 'b-open', 'b-warm', 'b-log', 'b-logout', 'b-title', 'b-items', 'b-status', 'b-stamp'];
  const setPhase = p => { for (const x of phases) M.classList.toggle(x, x === p || (phases.indexOf(x) < phases.indexOf(p) && x !== 'b-off')); M.dataset.boot = p; };
  function bootStart() {
    const lignes = M.classList.contains('t-portrait') ? BOOT_PORTRAIT : BOOT_PAYSAGE, court = M.classList.contains('t-portrait') ? 0.6 : 1;
    M.classList.add('booting'); setPhase('b-off'); bootEl.textContent = '';
    const debut = []; let t = 0; for (const l of lignes) { debut.push(t); t += l.length * 1000 / CPS + PAUSE_LIGNE; }
    const T0 = 80 * court, T1 = 280 * court, T2 = 700 * court, T3 = 1500 * court, TL = T3 + t, TF = TL + 250, TT = TF + 800, TI = TF + 1400, TS = TF + 1700, TE = TF + 1900;
    const t0 = performance.now();
    const step = now => {
      if (!boot) return;
      const dt = now - t0;
      setPhase(dt < T0 ? 'b-off' : dt < T1 ? 'b-line' : dt < T2 ? 'b-open' : dt < T3 ? 'b-warm' : dt < TL ? 'b-log' : dt < TF ? 'b-logout' : dt < TT ? 'b-title' : dt < TI ? 'b-items' : dt < TS ? 'b-status' : 'b-stamp');
      if (dt >= T3 && dt < TF) { const e = dt - T3; let out = ''; for (let i = 0; i < lignes.length; i++) { if (e < debut[i]) break; const n = Math.min(lignes[i].length, Math.floor((e - debut[i]) * CPS / 1000)); out += lignes[i].slice(0, n) + (n < lignes[i].length ? '█' : '\n'); if (n < lignes[i].length) break; }
        if (bootEl.textContent !== out) bootEl.textContent = out; }
      if (dt >= TE) return bootFin();
      boot = requestAnimationFrame(step);
    };
    boot = requestAnimationFrame(step);
  }
  function bootFin() { if (boot) cancelAnimationFrame(boot); boot = null; bootFait = true; M.classList.remove('booting', ...phases); M.dataset.boot = 'repos'; bootEl.textContent = ''; glitchPlan(); requestAnimationFrame(garde); }
  const saute = () => { if (boot) bootFin(); };
  // capture : une touche ou un geste pendant l'allumage le termine ; un geste sur un choix (déjà à sa place) agit aussi, une touche non.
  addEventListener('keydown', e => { if (!ouvert || M.hidden) return; if (boot) { bootFin(); if (e.key !== 'Escape') { e.preventDefault(); e.stopImmediatePropagation(); } } }, true);
  M.addEventListener('pointerdown', () => saute(), true);

  // ---------- navigation clavier : flèches / Début / Fin, Entrée (bouton natif), Échap (géré par shell.js) ----------
  const choix = () => [...list.querySelectorAll('button:not([hidden]):not(:disabled)')];
  let spam = [];
  function cur(b) { list.querySelectorAll('.cur').forEach(x => x !== b && x.classList.remove('cur')); if (b) { b.classList.add('cur'); if (document.activeElement !== b) b.focus({ preventScroll: true }); } }
  addEventListener('keydown', e => {
    if (!ouvert || M.hidden || !Q('#menu-sub').hidden && !list.contains(document.activeElement)) return;
    const c = choix(); if (!c.length) return;
    const i = c.indexOf(document.activeElement), k = e.key;
    if (k === 'ArrowDown' || k === 'ArrowUp' || k === 'Home' || k === 'End') {
      e.preventDefault(); const n = k === 'Home' ? 0 : k === 'End' ? c.length - 1 : i < 0 ? (k === 'ArrowDown' ? 0 : c.length - 1) : (i + (k === 'ArrowDown' ? 1 : -1) + c.length) % c.length; cur(c[n]);
      const t = Date.now(); spam = [...spam.filter(x => t - x < 2000), t]; if (spam.length >= 14) { spam = []; note(LIGNES.spam); }
    } else if (k === 'F1') { e.preventDefault(); note(LIGNES.aide); }
  });
  list.addEventListener('pointerover', e => { const b = e.target.closest('button'); if (b && !b.disabled && e.pointerType === 'mouse') cur(b); });
  list.addEventListener('focusin', e => { const b = e.target.closest('button'); if (b) cur(b); });
  // frappe libre : AIDE / HELP, ou une commande inconnue
  let frappe = '', frappeT = 0;
  addEventListener('keydown', e => { if (!ouvert || M.hidden || !Q('#menu-sub').hidden || e.ctrlKey || e.metaKey || e.altKey || e.key.length !== 1 || !/[a-z]/i.test(e.key)) return;
    frappe = (frappe + e.key.toUpperCase()).slice(-8); clearTimeout(frappeT);
    frappeT = setTimeout(() => { if (frappe.length >= 3) note(/AIDE$|HELP$/.test(frappe) ? LIGNES.aide : LIGNES.inconnue); frappe = ''; }, 900); });

  // ---------- confirmation : flash 100 ms + commande EXEC tapée à 36 car/s (l'action, elle, n'attend pas) ----------
  let execT = 0;
  function confirmer(b) {
    if (!b?.dataset.exec) return; confirme = true; b.classList.add('t-flash'); setTimeout(() => { b.classList.remove('t-flash'); confirme = false; }, 100);
    const cmd = '> EXEC ' + b.dataset.exec; cancelAnimationFrame(execT);
    if (reduit()) { execEl.textContent = cmd; return; }
    const t0 = performance.now(); const tape = now => { const n = Math.min(cmd.length, Math.floor((now - t0) * CPS / 1000)); execEl.textContent = cmd.slice(0, n) + (n < cmd.length ? '█' : ''); if (n < cmd.length && ouvert && !M.hidden) execT = requestAnimationFrame(tape); };
    execT = requestAnimationFrame(tape);
  }

  // ---------- onglet caché / menu masqué : aucune boucle ----------
  const pause = () => { const off = document.hidden || M.hidden || !ouvert; M.classList.toggle('t-paused', off); if (off) { clearTimeout(glitchT); glitchT = 0; if (boot && document.hidden) bootFin(); } else if (!glitchT && !boot) glitchPlan(); };
  document.addEventListener('visibilitychange', pause);
  new MutationObserver(pause).observe(M, { attributes: true, attributeFilter: ['hidden'] });
  const appliqueReduit = () => { M.classList.toggle('t-reduit', reduit()); if (ouvert) { if (reduit()) { saute(); clearTimeout(glitchT); glitchT = 0; } else glitchPlan(); if (reduit()) tickerReduit(); else { clearInterval(tickerT); tickerT = 0; tickerRemplit(); tickerVitesse(); } } };
  mq.addEventListener?.('change', appliqueReduit);

  return {
    pret,
    open(m) { // m : 'title' | 'pause'
      const premier = !ouvert; ouvert = true; M.classList.add('term');
      if (premier) { for (let i = ordre.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [ordre[i], ordre[j]] = [ordre[j], ordre[i]]; } }
      layout(); M.classList.toggle('t-reduit', reduit());
      if (reduit()) tickerReduit(); else { if (premier || !track.children.length) tickerRemplit(); tickerVitesse(); }
      if (m === 'title' && !bootFait && !reduit() && !boot) bootStart(); else if (m !== 'title' || reduit()) { bootFait = true; saute(); }
      pause(); requestAnimationFrame(garde);
    },
    close() { ouvert = false; saute(); clearTimeout(glitchT); glitchT = 0; clearInterval(tickerT); tickerT = 0; cancelAnimationFrame(execT); execEl.textContent = ''; pause(); },
    rendu() { requestAnimationFrame(garde); },
    confirmer, saute, appliqueReduit,
    etat: () => ({ mode, boot: M.dataset.boot || 'repos', booting: !!boot, reduit: reduit(), paused: M.classList.contains('t-paused'), dispo: { ...dispo }, glitch: !!glitchT }),
    rejouer() { bootFait = false; saute(); if (ouvert && !reduit()) bootStart(); },
  };
}
