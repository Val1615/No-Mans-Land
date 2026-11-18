// Ambiances jour/nuit par biome (scènes de rencontre) : la lumière suit l'heure du voyage (state.heures), elle n'est jamais figée par scène.
// lune (0-1) : intensité du liseré de lune sur les personnages (view.js), nulle le jour.
// Clés : heure (0-24) -> lumière au format view.applyLight ({ bg, hemi:[ciel, sol, intensité], sun:[couleur, intensité], tint, actor }) + voile de la marge hors scène.
// Interpolation linéaire entre clés (couleurs et intensités). Désert de jour : ambre franc de la maquette d'Ocre (pilote_maquette.png) [Ocre + Régie 18/11].
const NUIT_DESERT = { bg: '#0b0d16', hemi: ['#5c6a94', '#16121c', 0.6], sun: ['#8494c8', 0.35], tint: '#5c6688', actor: '#8e96b4', voile: 'rgba(6,8,16,.62)', lune: 1 };
const AUBE_DESERT = { bg: '#2a1c14', hemi: ['#f2b88a', '#3a2618', 1.05], sun: ['#ff9c58', 0.95], tint: '#ecc6a0', actor: '#f2d8bc', voile: 'rgba(20,12,8,.32)', lune: 0.25 };
const JOUR_DESERT = { bg: '#3a2c1c', hemi: ['#fff0d8', '#5a4630', 1.5], sun: ['#ffd890', 1.6], tint: '#f7efdf', actor: '#fcf7ee', voile: 'rgba(14,10,6,.18)', lune: 0 };
export const AMBIANCES = {
  desert: [[0, NUIT_DESERT], [5, NUIT_DESERT], [7, AUBE_DESERT], [8.5, JOUR_DESERT], [17.5, JOUR_DESERT], [19, AUBE_DESERT], [21, NUIT_DESERT], [24, NUIT_DESERT]],
};

const hex = c => [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16)), toHex = a => '#' + a.map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
const mixC = (a, b, k) => toHex(hex(a).map((v, i) => v + (hex(b)[i] - v) * k)), mixN = (a, b, k) => a + (b - a) * k;
const rgba = s => s.match(/[\d.]+/g).map(Number), mixRgba = (a, b, k) => { const x = rgba(a), y = rgba(b); return `rgba(${x.slice(0, 3).map((v, i) => Math.round(mixN(v, y[i], k))).join(',')},${mixN(x[3], y[3], k).toFixed(2)})`; };

// ambiance(biome, heures) : lumière du biome à l'heure du voyage (heures écoulées depuis le jour 1, 0 h) ; null si biome inconnu
export function ambiance(biome, heures) {
  const K = AMBIANCES[biome]; if (!K) return null;
  const h = (((heures ?? 9) % 24) + 24) % 24; let i = 0; while (i < K.length - 2 && K[i + 1][0] <= h) i++;
  const [h0, a] = K[i], [h1, b] = K[i + 1], k = h1 > h0 ? Math.min(1, Math.max(0, (h - h0) / (h1 - h0))) : 0;
  return { bg: mixC(a.bg, b.bg, k), hemi: [mixC(a.hemi[0], b.hemi[0], k), mixC(a.hemi[1], b.hemi[1], k), mixN(a.hemi[2], b.hemi[2], k)], sun: [mixC(a.sun[0], b.sun[0], k), mixN(a.sun[1], b.sun[1], k)],
    tint: mixC(a.tint, b.tint, k), actor: mixC(a.actor, b.actor, k), voile: mixRgba(a.voile, b.voile, k), lune: mixN(a.lune || 0, b.lune || 0, k) };
}
