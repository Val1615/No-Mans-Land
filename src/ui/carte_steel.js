// Lot 2 interface : carte de Steel-Megalopolis, 4 couches empilées (Sous-Ville en bas, Upper-Town en haut, verrouillée).
// Carte consultative : aucun déplacement depuis la carte. Fonds et repères : assets/ui/maps (Ocre), données : src/data/cartes.js.
import { STEEL_COUCHES, STEEL_LOC, STEEL_ALIAS } from '../data/cartes.js';

const IC = k => `./assets/ui/maps/icones/${k}_steel_48.png`;
// Lieu extérieur dont dépend un lieu (un intérieur : le quartier où mène sa porte de sortie).
export function exteriorOf(world, loc) {
  const L = world.LOCATIONS[loc]; if (!L || L.kind !== 'interior') return loc;
  for (const d of world.DOORS) if (d.location === loc && d.target) { const t = world.DOORS.find(x => x.id === d.target.doorId); if (t && world.LOCATIONS[t.location]?.kind !== 'interior') return t.location; }
  return loc;
}
export const isSteel = (world, loc) => { const e = exteriorOf(world, loc); return e in STEEL_LOC || (!e.startsWith('dusk_') && world.LOCATIONS[e]?.city === 'steel'); };
export const coucheOf = (world, loc) => { const e = exteriorOf(world, loc); return STEEL_LOC[e] || STEEL_LOC[loc] || 2; };

export function steelMapHtml({ world, state, manifest, couche }) {
  const here = exteriorOf(world, state.location), hereKey = STEEL_ALIAS[here] || STEEL_ALIAS[state.location] || here, mine = coucheOf(world, state.location);
  const C = STEEL_COUCHES.find(c => c.n === couche), M = manifest.steel, mc = M.couches.find(c => c.couche === couche), [W, H] = M.px;
  // Brouillard de guerre [décision Valentin, 29/10] : un repère non découvert n'est pas affiché ; la couche est voilée sauf autour des repères connus.
  const known = r => r.type === 'verrou' || (r.connu ? r.connu(state) : !!state.seen[r.loc]) || r.loc === here;
  const vis = C.reperes.filter(r => r.type !== 'verrou' && (r.px || mc.reperes_px_proposition[r.key]) && known(r)), P = r => r.px || mc.reperes_px_proposition[r.key];
  const marks = vis.map(r => { const px = P(r), isHere = r.loc && (r.loc === hereKey || r.loc === here);
    const ic = r.type === 'verrou' ? 'verrouille' : r.type === 'lien' ? 'lien_couches' : r.type === 'sortie' ? 'sortie' : 'lieu_decouvert';
    const attrs = `data-key="${r.key}" data-type="${r.type}"` + (r.vers ? ` data-vers="${r.vers}"` : '') + (r.region ? ' data-region="1"' : '');
    return `<button class="mk ${r.type} known ${isHere ? 'here' : ''} ${px[0] / W > 0.66 ? 'gauche' : ''}" ${attrs} style="left:${(100 * px[0] / W).toFixed(2)}%;top:${(100 * px[1] / H).toFixed(2)}%" title="${r.nom}">`
      + `<img src="${IC(ic)}" alt=""><span>${r.nom}</span>${isHere ? `<img class="me" src="${IC('joueur')}" alt="Tu es ici">` : ''}</button>`; }).join('');
  const holes = vis.map(r => [P(r)[0], P(r)[1], r.type === 'lieu' ? 520 : 320]); // [x, y, taille du masque d'Ocre en px de planche]
  const fog = C.verrou ? '' : `<canvas class="fog" data-holes='${JSON.stringify(holes)}' aria-hidden="true"></canvas>`;
  const pile = STEEL_COUCHES.slice().reverse().map(c => `<button role="tab" aria-selected="${c.n === couche}" data-couche="${c.n}" class="${c.n === couche ? 'sel' : ''} ${c.n === mine ? 'mine' : ''} ${c.verrou ? 'lock' : ''}" title="${c.nom}${c.verrou ? ' (accès refusé)' : ''}">`
    + `<b>${c.n}</b><span>${c.court}</span>${c.verrou ? `<img src="${IC('verrouille')}" alt="verrouillée">` : c.n === mine ? `<img src="${IC('joueur')}" alt="ici">` : ''}</button>`).join('');
  const cachés = C.reperes.filter(r => r.type !== 'verrou' && !known(r)).length;
  const liste = vis.filter(r => r.type !== 'verrou').map(r => `<li><span>${r.nom}</span><span class="muted">${r.loc && (r.loc === hereKey || r.loc === here) ? 'tu es ici' : r.type === 'lien' ? 'passage vers ' + STEEL_COUCHES.find(c => c.n === r.vers).nom : r.type === 'sortie' ? 'sortie' : ''}</span></li>`).join('')
    + (cachés ? `<li class="unk"><span>Zones inexplorées</span><span class="muted">sous le brouillard</span></li>` : '');
  return `<div class="smap" data-n="${couche}"><h3>CARTE · STEEL-MEGALOPOLIS</h3><div class="smap-sub muted">Couche ${couche} · ${C.nom}${C.verrou ? ' · accès refusé' : ''}${couche === mine ? ' · tu es ici' : ''}</div>
    <div class="smap-body"><div class="smap-pile" role="tablist" aria-label="Couches">${pile}</div>
      <div class="smap-plan ${C.verrou ? 'locked' : ''}" style="aspect-ratio:${W}/${H}"><img class="fond" src="./assets/${mc.fichier}" alt="Plan de la couche ${C.nom}" draggable="false">${fog}${marks}
        ${C.verrou ? `<div class="lockmsg"><img src="${IC('verrouille')}" alt=""><span>UPPER-TOWN · ACCÈS REFUSÉ</span></div>` : ''}</div>
      <div class="smap-nav"><button data-dir="1" aria-label="Couche du dessus" ${couche >= 4 ? 'disabled' : ''}>▲</button><button data-dir="-1" aria-label="Couche du dessous" ${couche <= 1 ? 'disabled' : ''}>▼</button></div></div>
    <ul class="smap-liste">${liste}</ul><div class="desc muted">Carte consultative. Molette, flèches ou onglets : changer de couche. Un passage ouvre la couche reliée.</div></div>`;
}

// Brouillard de guerre de la carte Steel (texture bleu acier d'Ocre, opacité conseillée) : effacé en destination-out par le masque d'Ocre
// centré sur chaque repère connu (mode d'emploi : docs/assets/CARTES.md, section brouillard).
const fogImgs = {};
const loadImg = src => fogImgs[src] ||= new Promise(r => { const i = new Image(); i.onload = () => r(i); i.onerror = () => r(null); i.src = src; });
export async function drawSteelFog(canvas, manifest) {
  if (!canvas) return; const mob = innerWidth < 700, F = manifest.brouillard_steel || {}, Fm = manifest.brouillard_nml?.masque || {}, [W, H] = manifest.steel.px, k = mob ? 0.5 : 1;
  const [t, m] = await Promise.all([loadImg('./assets/' + (mob ? F.texture?.mobile?.fichier : F.texture?.fichier)), loadImg('./assets/' + (mob ? Fm.mobile?.fichier : Fm.fichier))]);
  canvas.width = W * k; canvas.height = H * k; const x = canvas.getContext('2d');
  x.globalAlpha = F.opacite_conseillee ?? 0.94; x.fillStyle = t ? x.createPattern(t, 'repeat') : '#04070b'; x.fillRect(0, 0, canvas.width, canvas.height);
  x.globalAlpha = 1; x.globalCompositeOperation = 'destination-out';
  for (const [hx, hy, sz] of JSON.parse(canvas.dataset.holes || '[]')) { const s = sz * k; if (m) x.drawImage(m, hx * k - s / 2, hy * k - s / 2, s, s); else { x.beginPath(); x.arc(hx * k, hy * k, s / 3, 0, 7); x.fill(); } }
  x.globalCompositeOperation = 'source-over'; canvas.dataset.pret = '1';
}
