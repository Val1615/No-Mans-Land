// Chargement par lieu (optimisation du lancement, 12/11) : au lieu de charger toutes les images du catalogue (bâtiments, intérieurs,
// sols, décors de tous les quartiers de Steel) avant de pouvoir jouer, on charge d'abord celles du lieu où le joueur entre,
// puis le reste en arrière-plan, sans bloquer. Les fichiers ne sont jamais transformés : mêmes URL, mêmes images (SKIN).
import { SKIN } from '../render/textures.js?v=editor2';
import { VUES_VEHICULES } from '../data/vehicules.js';
import { SOLS_BASE, SOLS_GENERES } from './catalogue.js';

// porte d'intérieur par défaut et sols de base (view.js / textures.js les prennent par défaut, sans les nommer dans le lieu) : < 1 Mo
const TOUJOURS = ['door_in', ...SOLS_BASE, ...SOLS_GENERES];

// Clés d'images utilisées par un lieu : toute chaîne du lieu (bâtiments, sols, décors, véhicules, portes, PNJ du lieu) qui est une clé
// du catalogue ; puis, par fermeture, ce que ces clés appellent (calques _fenetres / _neon / _texte / _mobile..., vues de dos des véhicules,
// champs du manifeste qui pointent sur une autre clé).
export function clesDuLieu(world, locId, urls, entree = () => null) {
  const L = world.LOCATIONS[locId]; if (!L) return [];
  const out = new Set(TOUJOURS.filter(k => urls[k])), vus = new WeakSet();
  const scan = (v, prof = 0) => {
    if (prof > 12 || v == null) return;
    if (typeof v === 'string') { if (urls[v]) out.add(v); return; }
    if (typeof v !== 'object' || vus.has(v)) return; vus.add(v);
    if (Array.isArray(v)) { for (const x of v) scan(x, prof + 1); return; }
    for (const k in v) scan(v[k], prof + 1);
  };
  scan(L);
  for (const d of world.DOORS || []) if (d.location === locId) scan(d);
  for (const n of world.NPCS || []) if (n.location === locId) scan(n);
  // fermeture : calques et vues liées
  const parPrefixe = Object.keys(urls).sort();
  const file = [...out];
  while (file.length) {
    const k = file.pop();
    const ajoute = x => { if (urls[x] && !out.has(x)) { out.add(x); file.push(x); } };
    const e = entree(k); if (e) for (const v of Object.values(e)) if (typeof v === 'string') ajoute(v);
    const vv = VUES_VEHICULES[k]; if (vv) for (const v of Object.values(vv)) if (typeof v === 'string') ajoute(v);
    // clés dérivées : k + '_…' (recherche dichotomique dans la liste triée)
    const p = k + '_'; let lo = 0, hi = parPrefixe.length;
    while (lo < hi) { const m = (lo + hi) >> 1; if (parPrefixe[m] < p) lo = m + 1; else hi = m; }
    for (let i = lo; i < parPrefixe.length && parPrefixe[i].startsWith(p); i++) ajoute(parPrefixe[i]);
  }
  return [...out];
}

// Chargeur : une image par clé, jamais deux fois. Priorité au lieu demandé ; le reste passe ensuite, 6 à la fois.
export function createChargeur({ world, urls, entree }) {
  const enCours = new Map(), lieux = new Map(), ecoute = new Set();
  let fond = null, fondArret = false;
  const une = k => {
    if (SKIN[k]) return Promise.resolve(true);
    if (enCours.has(k)) return enCours.get(k);
    const p = new Promise(ok => { const i = new Image(); i.decoding = 'async';
      // decode() : l'image est décodée hors du fil principal pendant le chargement, pas au premier dessin du lieu (gros gain à l'entrée)
      i.onload = () => { const pose = () => { SKIN[k] = i; ok(true); }; if (i.decode) i.decode().then(pose, pose); else pose(); }; i.onerror = () => { console.warn('Image introuvable :', urls[k]); ok(false); }; i.src = urls[k]; });
    enCours.set(k, p); return p;
  };
  const cles = id => { if (!lieux.has(id)) lieux.set(id, { cles: clesDuLieu(world, id, urls, entree), pret: false, p: null }); return lieux.get(id); };
  function lieu(id, progres) {
    const l = cles(id); if (l.pret) return Promise.resolve();
    if (!l.p) { let n = 0; const tot = l.cles.length;
      const emit = () => { for (const f of ecoute) f({ lieu: id, fait: n, total: tot }); };
      emit();
      l.p = Promise.all(l.cles.map(k => une(k).then(() => { n++; emit(); }))).then(() => { l.pret = true; emit(); }); }
    if (progres) { const f = e => { if (e.lieu === id) progres(e); }; ecoute.add(f); l.p.then(() => ecoute.delete(f)); }
    return l.p;
  }
  const pret = id => cles(id).pret || cles(id).cles.every(k => SKIN[k]) && (cles(id).pret = true);
  // Arrière-plan : tout le reste du catalogue, lieu par lieu (les sorties du lieu courant d'abord), sans bloquer le jeu.
  function arrierePlan(depuis) {
    if (fond) return fond;
    const ordre = [], vu = new Set();
    const pousse = id => { if (id && !vu.has(id) && world.LOCATIONS[id]) { vu.add(id); ordre.push(id); } };
    pousse(depuis);
    const parId = new Map((world.DOORS || []).map(d => [d.id, d]));
    for (const d of world.DOORS || []) if (d.location === depuis && d.target) pousse(d.target.location || parId.get(d.target.doorId)?.location); // lieux voisins d'abord
    for (const id of Object.keys(world.LOCATIONS)) pousse(id);
    const reste = []; for (const id of ordre) for (const k of cles(id).cles) reste.push(k);
    for (const k of Object.keys(urls)) reste.push(k); // le catalogue entier finit chargé, comme avant
    const file = [...new Set(reste)].filter(k => !SKIN[k]);
    fond = new Promise(fin => {
      let actifs = 0;
      const suivant = () => {
        if (fondArret) return;
        while (actifs < 6 && file.length) { const k = file.shift(); if (SKIN[k]) continue; actifs++; une(k).then(() => { actifs--; if (!file.length && !actifs) fin(); else suivant(); }); }
        if (!file.length && !actifs) fin();
      };
      suivant();
    });
    return fond;
  }
  return { lieu, pret, arrierePlan, cles: id => cles(id).cles.slice(), charge: k => !!SKIN[k] };
}
