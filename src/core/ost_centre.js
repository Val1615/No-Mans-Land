// Playlist OST commune des quatre quartiers centraux de Steel-Megalopolis (pack fecc483, Groovy Crew) :
// Center-Town (steel_center + intérieur change_in), Fréquence Strip (steel_strip), Pulse Plaza (steel_pulse), Steel Arena (steel_arena).
// Une seule instance <audio id="music"> partagée avec le reste du jeu : changer de zone parmi les quatre ne coupe ni ne relance le morceau.
// Enchaînement 01 -> 02 -> 03 -> 04 -> 01 en boucle. Analyse de rythme Web Audio (AnalyserNode + détection de kick/basse) branchée sur cette même lecture.

export const AMBIANCE_DUSK = './assets/audio/dusk_town_ambiance.mp3';

export const OST_CENTRE_ZONES = Object.freeze(['steel_center', 'steel_strip', 'steel_pulse', 'steel_arena']);
// change_in est l'intérieur du Change de Teng dans Center-Town : la piste commune continue atténuée à 0,25 sans coupure.
const SHARED_LOCATIONS = new Set([...OST_CENTRE_ZONES, 'change_in']);

export const OST_CENTRE_TRACKS = Object.freeze([
  Object.freeze({ index: 0, id: '01_bad_buzz_protocol_remix', file: './assets/audio/ost_centre/01_bad_buzz_protocol_remix.mp3', title: 'Bad Buzz Protocol (Remix)', artist: 'Groovy Crew' }),
  Object.freeze({ index: 1, id: '02_dance_soit_plus_chrome_16bit', file: './assets/audio/ost_centre/02_dance_soit_plus_chrome_16bit.mp3', title: 'Dance soit plus chrome (16bit)', artist: 'Groovy Crew' }),
  Object.freeze({ index: 2, id: '03_steel_megalopolis_remix', file: './assets/audio/ost_centre/03_steel_megalopolis_remix.mp3', title: 'Steel-Megalopolis (Remix)', artist: 'Groovy Crew' }),
  Object.freeze({ index: 3, id: '04_we_already_knew_remix', file: './assets/audio/ost_centre/04_we_already_knew_remix.mp3', title: 'We Already Knew (Remix)', artist: 'Groovy Crew' }),
]);

export function isOstCentreZone(locationId) {
  return SHARED_LOCATIONS.has(locationId);
}

export function createMusic({ el, kSon, getLocation, getKind, getMusicOption, isMenuOpen }) {
  const KEY = 'nml_muted';
  let started = false;
  let mode = 'ambiance'; // 'ambiance' | 'ost_centre'
  let trackIndex = 0;
  let savedTime = 0;
  let pendingSeek = 0;

  // Graphe Web Audio sur l'unique élément <audio id="music"> (créé au premier geste pour respecter l'autoplay navigateur)
  let audioCtx = null, sourceNode = null, analyser = null, freqBuf = null;
  let beat = 0, energy = 0, bass = 0, mid = 0, high = 0;
  let frameKick = false, pendingFrameKick = false, kickCount = 0, bpm = 0;
  let bassAvg = 0, prevBass = 0, lastKickAt = -10, lastSampleAt = performance.now() / 1000;
  const kickIntervals = [];
  const kickListeners = new Set();

  const muted = () => localStorage.getItem(KEY) === '1';

  function resetBeat() {
    beat = 0; energy = 0; bass = 0; mid = 0; high = 0;
    frameKick = false; pendingFrameKick = false;
    bassAvg = 0; prevBass = 0;
  }

  function syncMute() {
    el.muted = muted();
    if (el.muted) resetBeat();
    if (!kSon) return;
    kSon.classList.toggle('on', el.muted);
    kSon.setAttribute('aria-pressed', el.muted);
    const sr = kSon.querySelector('.sr'); if (sr) sr.textContent = el.muted ? 'Muet' : 'Son';
    const ic = kSon.querySelector('.ic'); if (ic) ic.dataset.ic = el.muted ? 'son_off' : 'son_on';
  }

  function ensureAnalyser() {
    if (analyser) {
      if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume().catch(() => {});
      return analyser;
    }
    const Ctx = window.AudioContext || window.webkitAudioContext;
    if (!Ctx) return null;
    try {
      audioCtx = new Ctx();
      sourceNode = audioCtx.createMediaElementSource(el);
      analyser = audioCtx.createAnalyser();
      analyser.fftSize = 1024;
      analyser.minDecibels = -90;
      analyser.maxDecibels = -10;
      analyser.smoothingTimeConstant = 0.55;
      sourceNode.connect(analyser);
      analyser.connect(audioCtx.destination);
      freqBuf = new Uint8Array(analyser.frequencyBinCount);
      if (audioCtx.state === 'suspended') audioCtx.resume().catch(() => {});
    } catch {
      analyser = null;
    }
    return analyser;
  }

  function safePlay() {
    const p = el.play();
    if (p && typeof p.catch === 'function') {
      p.catch(err => {
        if (err && err.name === 'NotAllowedError') started = false;
      });
    }
  }

  function applyPendingSeek() {
    if (pendingSeek > 0 && mode === 'ost_centre' && Number.isFinite(el.duration) && el.duration > 1) {
      const target = Math.min(pendingSeek, Math.max(0, el.duration - 1));
      if (el.seekable && el.seekable.length && el.seekable.end(el.seekable.length - 1) >= target) {
        try { el.currentTime = target; } catch {}
      }
      pendingSeek = 0;
    }
  }
  el.addEventListener('loadedmetadata', applyPendingSeek);
  el.addEventListener('canplay', applyPendingSeek);

  function mountTrack(idx, resumeTime = 0) {
    trackIndex = ((idx % OST_CENTRE_TRACKS.length) + OST_CENTRE_TRACKS.length) % OST_CENTRE_TRACKS.length;
    pendingSeek = resumeTime > 0 ? resumeTime : 0;
    el.loop = false;
    el.preload = 'auto';
    el.src = OST_CENTRE_TRACKS[trackIndex].file;
    if (started) safePlay();
  }

  function syncZone() {
    const loc = getLocation?.();
    if (!loc) return;
    const want = isOstCentreZone(loc) ? 'ost_centre' : 'ambiance';
    if (want === mode) return; // Déplacement entre Center-Town, Strip, Pulse Plaza et Steel Arena : même instance et position inchangée
    if (mode === 'ost_centre' && want === 'ambiance') {
      savedTime = Number.isFinite(el.currentTime) ? el.currentTime : 0;
      pendingSeek = 0;
      mode = 'ambiance';
      el.loop = true;
      el.preload = 'auto';
      el.src = AMBIANCE_DUSK;
      resetBeat();
      if (started) safePlay();
    } else if (want === 'ost_centre') {
      mode = 'ost_centre';
      mountTrack(trackIndex, savedTime);
    }
  }

  el.addEventListener('ended', () => {
    if (mode !== 'ost_centre') return;
    savedTime = 0;
    mountTrack(trackIndex + 1, 0);
  });

  function onGesture(e) {
    // Sur tactile, pointerdown précède l'activation utilisateur (accordée à pointerup/touchend/click) : éviter un play() rejeté prématurément
    if (e && e.type === 'pointerdown' && e.pointerType && e.pointerType !== 'mouse') return;
    ensureAnalyser();
    if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume().catch(() => {});
    if (started) return;
    started = true;
    syncZone();
    safePlay();
  }

  addEventListener('pointerdown', onGesture, true);
  addEventListener('pointerup', onGesture, true);
  addEventListener('touchend', onGesture, { capture: true, passive: true });
  addEventListener('keydown', onGesture, true);
  addEventListener('click', onGesture, true);

  kSon?.addEventListener('click', () => {
    localStorage.setItem(KEY, muted() ? '0' : '1');
    syncMute();
  });
  addEventListener('keydown', e => {
    if (e.key.toLowerCase() === 's' && !e.repeat && !isMenuOpen?.()) kSon?.click();
  });

  function sampleRhythm() {
    const now = performance.now() / 1000;
    const dt = Math.min(0.25, Math.max(0.001, now - lastSampleAt));
    lastSampleAt = now;
    const playing = mode === 'ost_centre' && !el.paused && !el.ended && !el.muted && el.volume > 0.001;
    if (!playing || !analyser || !freqBuf || (audioCtx && audioCtx.state !== 'running')) {
      if (el.muted || el.paused || mode !== 'ost_centre') resetBeat();
      else {
        const fade = Math.max(0, 1 - dt * 8);
        beat = beat > 0.005 ? beat * fade : 0;
        energy = energy > 0.005 ? energy * fade : 0;
        bass = bass > 0.005 ? bass * fade : 0;
        mid = mid > 0.005 ? mid * fade : 0;
        high = high > 0.005 ? high * fade : 0;
      }
      return;
    }

    analyser.getByteFrequencyData(freqBuf);
    const hz = (audioCtx?.sampleRate || 48000) / analyser.fftSize;
    const b0 = Math.max(1, Math.floor(40 / hz)), b1 = Math.max(b0 + 1, Math.ceil(165 / hz));
    const m0 = b1, m1 = Math.min(freqBuf.length, Math.ceil(2400 / hz));
    const h0 = m1, h1 = Math.min(freqBuf.length, Math.ceil(9600 / hz));
    const dbGain = -20 * Math.log10(Math.max(0.04, el.volume));
    const minDb = analyser.minDecibels, spanDb = analyser.maxDecibels - minDb;

    const band = (i0, i1) => {
      let s = 0, c = 0;
      for (let i = i0; i < i1; i++) {
        const v = freqBuf[i];
        if (v > 0) {
          const n = (minDb + (v / 255) * spanDb + dbGain + 82) / 70;
          if (n > 0) s += n > 1 ? 1 : n;
        }
        c++;
      }
      return c ? s / c : 0;
    };

    const rawBass = band(b0, b1), rawMid = band(m0, m1), rawHigh = band(h0, h1);
    const rawEnergy = 0.45 * rawBass + 0.35 * rawMid + 0.20 * rawHigh;
    const alpha = Math.min(1, dt * 18);
    bass = rawBass;
    mid += (rawMid - mid) * alpha;
    high += (rawHigh - high) * alpha;
    energy += (rawEnergy - energy) * alpha;
    beat = Math.max(0, beat - dt * 4.5);

    const rise = rawBass - prevBass;
    prevBass = rawBass;
    const delta = bassAvg > 0.01 ? rawBass - bassAvg : 0;
    bassAvg = bassAvg > 0.01 ? bassAvg + (rawBass - bassAvg) * Math.min(1, dt * 2.8) : rawBass;

    if (now - lastKickAt >= 0.22 && rawBass > 0.24 && (delta > 0.055 || rise > 0.05)) {
      beat = 1;
      pendingFrameKick = true;
      kickCount++;
      const dtKick = now - lastKickAt;
      lastKickAt = now;
      if (dtKick >= 0.26 && dtKick <= 0.9) {
        kickIntervals.push(dtKick);
        if (kickIntervals.length > 8) kickIntervals.shift();
        if (kickIntervals.length >= 2) {
          const sorted = [...kickIntervals].sort((x, y) => x - y);
          bpm = Math.round(60 / sorted[sorted.length >> 1]);
        }
      }
      if (kickListeners.size) {
        const info = {
          beat: 1,
          bass: +bass.toFixed(3),
          mid: +mid.toFixed(3),
          high: +high.toFixed(3),
          energy: +energy.toFixed(3),
          kickCount,
          bpm,
          trackIndex,
          track: OST_CENTRE_TRACKS[trackIndex],
          currentTime: el.currentTime,
        };
        for (const fn of [...kickListeners]) {
          try { fn(info); } catch {}
        }
      }
    }
  }

  // Échantillonnage régulier (~33 Hz) pour ne manquer aucun transitoire de kick même si le rendu 3D ralentit
  setInterval(() => {
    if (mode === 'ost_centre' && !el.paused && !el.muted) sampleRhythm();
  }, 30);

  syncMute();
  syncZone();

  const ostCentre = {
    zones: OST_CENTRE_ZONES,
    tracks: OST_CENTRE_TRACKS,
    isSharedZone: isOstCentreZone,
    get el() { return el; },
    get active() { return mode === 'ost_centre'; },
    get playing() { return mode === 'ost_centre' && !el.paused && !el.muted && el.volume > 0.001; },
    get trackIndex() { return trackIndex; },
    get track() { return OST_CENTRE_TRACKS[trackIndex]; },
    get currentTime() { return el.currentTime; },
    get duration() { return el.duration; },
    get beat() { return beat; },
    get energy() { return energy; },
    get bass() { return bass; },
    get mid() { return mid; },
    get high() { return high; },
    get kick() { return frameKick; },
    get kickCount() { return kickCount; },
    get bpm() { return bpm; },
    get analyser() { return analyser; },
    ensureAnalyser,
    onKick(fn) {
      if (typeof fn !== 'function') return () => {};
      kickListeners.add(fn);
      return () => kickListeners.delete(fn);
    },
    nextTrack() {
      savedTime = 0;
      if (mode === 'ost_centre') mountTrack(trackIndex + 1, 0);
      else trackIndex = (trackIndex + 1) % OST_CENTRE_TRACKS.length;
      return OST_CENTRE_TRACKS[trackIndex];
    },
    setTrack(idx) {
      savedTime = 0;
      if (mode === 'ost_centre') mountTrack(idx, 0);
      else trackIndex = ((idx % OST_CENTRE_TRACKS.length) + OST_CENTRE_TRACKS.length) % OST_CENTRE_TRACKS.length;
      return OST_CENTRE_TRACKS[trackIndex];
    },
    bands(out) {
      if (!analyser || !freqBuf) return null;
      analyser.getByteFrequencyData(out || freqBuf);
      return out || freqBuf;
    },
  };

  return {
    el,
    ostCentre,
    syncZone,
    update() {
      syncZone();
      const v = (getKind?.() === 'interior' ? 0.25 : 0.55) * ((getMusicOption?.() ?? 100) / 100);
      if (Math.abs(el.volume - v) > 0.01) el.volume += Math.sign(v - el.volume) * 0.01;
      if (performance.now() / 1000 - lastSampleAt >= 0.012) sampleRhythm();
      frameKick = pendingFrameKick;
      pendingFrameKick = false;
    },
  };
}
