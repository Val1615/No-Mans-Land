// Cinématique d'ouverture (fichier de Valentin, assets/video/cinematique_ouverture.mp4, servi tel quel, jamais réencodé).
// Jouée une fois par chargement de page, avant l'allumage du Terminal ; jamais rejouée au retour au menu depuis le jeu.
// - Plein écran sur noir, object-fit: contain (bandes noires en portrait, jamais d'étirement), lecture inline.
// - play() avec son d'emblée ; si le navigateur refuse (autoplay), invite « ▸ TOUCHER POUR COMMENCER » sur noir, le premier geste lance la vidéo avec son.
// - Pendant la lecture : « PASSER ▸ » ; clic / tap / Échap / Entrée / Espace passent.
// - La vidéo finit sur une image claire, sans fondu : un voile CSS noir fait le fondu (0,6 s avant la fin, 0,4 s au passage), puis le Terminal s'allume depuis le noir.
// - Erreur réseau / format, ou rien à l'écran au bout de 8 s : on va directement au Terminal (jamais d'écran noir sans retour).
// - Tant qu'elle est là, tous les gestes sont avalés ici (le menu, la musique et l'allumage ne voient rien).
// La décision de la jouer (et le src) est prise dans index.html avant la première image ; ici, la lecture.
const GESTES = ['pointerdown', 'pointerup', 'touchstart', 'touchend', 'mousedown', 'mouseup', 'click', 'keydown', 'keyup', 'contextmenu'];
const FONDU_FIN = 0.6, FONDU_PASSE = 0.4, FONDU_ENTREE = 0.15, DELAI_IMAGE = 8000, ANTI_REBOND = 450;

export function cinematique() {
  const R = document.getElementById('intro'), etat = window.__nmlIntro || (window.__nmlIntro = {});
  if (!R || !document.documentElement.classList.contains('intro')) { window.__nmlIntroActive = false; return Promise.resolve(etat.fin || 'absente'); }
  const v = R.querySelector('#intro-video'), invite = R.querySelector('#intro-invite'), passer = R.querySelector('#intro-passer');
  let fini = false, fondu = false, dernierGeste = 0, tImage = 0, raf = 0, resoudre;
  const promesse = new Promise(r => { resoudre = r; });
  const pose = e => { etat.etat = e; R.dataset.etat = e; };
  v.muted = false; v.volume = 1;

  function terminer(fin) {
    if (fini) return; fini = true; cancelAnimationFrame(raf); clearTimeout(tImage);
    etat.fin = etat.fin || fin; pose('fini');
    try { v.pause(); } catch {}
    v.removeAttribute('src'); try { v.load(); } catch {} // libère le flux
    for (const g of GESTES) removeEventListener(g, geste, true);
    document.documentElement.classList.remove('intro'); R.remove();
    window.__nmlIntroActive = false;
    resoudre(etat.fin);
  }
  function fonduNoir(duree, fin) {
    if (fondu || fini) return; fondu = true; etat.fin = fin; pose('fondu');
    R.style.setProperty('--fondu', duree + 's'); R.classList.add('fondu');
    passer.hidden = true; invite.hidden = true;
    const t0 = performance.now(), v0 = v.volume;
    const pas = () => { const k = Math.min(1, (performance.now() - t0) / (duree * 1000));
      if (fin === 'passee') { try { v.volume = v0 * (1 - k); } catch {} } // au passage seulement : le son du fichier n'est jamais touché en fin naturelle
      if (k < 1) raf = requestAnimationFrame(pas); };
    raf = requestAnimationFrame(pas);
    setTimeout(() => terminer(fin), duree * 1000 + 60); // onglet caché : pas de rAF, le minuteur conclut quand même
  }
  function surveilleFin() { // fondu au noir sur les 0,6 dernières secondes (timeupdate est trop lâche)
    if (fini || fondu) return;
    if (Number.isFinite(v.duration) && v.duration > 1 && v.currentTime >= v.duration - FONDU_FIN) return fonduNoir(FONDU_FIN, 'naturelle');
    raf = requestAnimationFrame(surveilleFin);
  }
  function lance(parGeste) {
    pose('chargement'); invite.hidden = true; passer.hidden = false;
    clearTimeout(tImage); tImage = setTimeout(() => { if (!fini && !fondu && v.currentTime < 0.05) terminer('erreur'); }, DELAI_IMAGE);
    let p; try { p = v.play(); } catch (e) { p = Promise.reject(e); }
    Promise.resolve(p).then(() => { etat.mode = etat.mode || (parGeste ? 'geste' : 'autoplay'); }, err => {
      if (fini) return;
      if (err && err.name === 'NotAllowedError') { clearTimeout(tImage); pose('invite'); etat.invite = true; invite.hidden = false; passer.hidden = true; return; }
      if (err && err.name === 'AbortError') return; // play() interrompu par un passage ou un nouveau play()
      terminer('erreur');
    });
  }
  v.addEventListener('playing', () => { if (fini || fondu) return; clearTimeout(tImage); pose('lecture'); R.classList.add('lecture'); cancelAnimationFrame(raf); raf = requestAnimationFrame(surveilleFin); });
  v.addEventListener('ended', () => { if (!fondu) fonduNoir(0.05, 'naturelle'); });
  v.addEventListener('error', () => terminer('erreur'));

  R.style.setProperty('--entree', FONDU_ENTREE + 's');

  // Gestes : tout est capté ici, au premier niveau (window, capture), avant le menu et la musique.
  function geste(e) {
    if (fini) return;
    e.stopImmediatePropagation(); if (e.cancelable && e.type !== 'touchstart' && e.type !== 'touchend') e.preventDefault();
    const tactile = e.pointerType && e.pointerType !== 'mouse';
    // Un seul déclencheur par geste : pointerup tactile (activation accordée), pointerdown souris, keydown ; le reste du même geste est avalé.
    const declenche = (e.type === 'pointerup' && tactile) || (e.type === 'pointerdown' && !tactile) || (e.type === 'keydown' && !e.repeat);
    if (!declenche || fondu) return;
    if (e.type === 'keydown' && !['Escape', 'Enter', ' ', 'Spacebar'].includes(e.key) && etat.etat !== 'invite') return;
    const t = performance.now(); if (t - dernierGeste < ANTI_REBOND) return; dernierGeste = t;
    if (etat.etat === 'invite') return lance(true);
    etat.passee = true; fonduNoir(FONDU_PASSE, 'passee');
  }
  for (const g of GESTES) addEventListener(g, geste, g.startsWith('touch') ? { capture: true, passive: true } : true);
  // src posé dès index.html : une erreur (404, format) a pu tomber avant ce module
  if (v.error || v.networkState === 3) { terminer('erreur'); return promesse; }

  lance(false);
  return promesse;
}
