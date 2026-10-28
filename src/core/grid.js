import { UNITS } from '../data/units.js';
const C = UNITS.cell;
// Grille de collision dérivée des mêmes volumes que le rendu. Centre de case i = i * C.
export function solidsOf(loc, doors, sprites) {
  const out = [...loc.buildings.flatMap(b => b.solid || [{ x: b.x, z: b.z, w: b.w, d: b.d }])]; // Lower-Town v1 : b.solid = parties pleines (portique, dalle)
  out.push(...propSolids(loc, sprites));
  return out.concat(loc.ground?.water || [], wallsOf(loc, doors)); // China Lake : eau non praticable (ground.water)
}
function propSolids(loc, sprites) {
  const out = [];
  for (const p of loc.props) {
    if (p.box) out.push(p);
    else if (p.furn) { const [w, d] = sprites[p.furn].footprint_m; out.push({ x: p.x, z: p.z, w, d }); } // mobilier : x, z = coin min de l'emprise
    else if (p.sprite) { const m = sprites[p.sprite]; const s = p.solid ?? null;
      const [w, d] = p.fp || (s ? [s, s] : m.footprint_m); out.push({ x: p.x - w / 2, z: p.z - d / 2, w, d }); }
  }
  return out;
}
// Combat C2 (COMBAT.md §8) : solides avec leur hauteur de couverture. Bâtiments et murs = 2, props = 1 ; l'eau ne coupe pas la vue.
export function coverSolids(loc, doors, sprites) {
  return [...loc.buildings.flatMap(b => b.solid || [{ x: b.x, z: b.z, w: b.w, d: b.d }]), ...wallsOf(loc, doors)].map(s => ({ ...s, h: 2 }))
    .concat(propSolids(loc, sprites).map(s => ({ ...s, h: 1 })));
}
export function buildGrid(loc, doors, sprites, extraBlocked = []) {
  const w = Math.round(loc.size.w / C) + 1, d = Math.round(loc.size.d / C) + 1;
  const blocked = new Uint8Array(w * d), r = UNITS.character.radius;
  const solids = solidsOf(loc, doors, sprites).concat(extraBlocked);
  for (let j = 0; j < d; j++) for (let i = 0; i < w; i++) {
    const x = i * C, z = j * C;
    if (x < r || z < r || x > loc.size.w - r || z > loc.size.d - r) { blocked[j * w + i] = 1; continue; }
    for (const s of solids) if (x > s.x - r && x < s.x + s.w + r && z > s.z - r && z < s.z + s.d + r) { blocked[j * w + i] = 1; break; }
  }
  return { w, d, blocked, toCell: (x, z) => [Math.round(x / C), Math.round(z / C)], toWorld: (i, j) => ({ x: i * C, z: j * C }),
    free(i, j) { return i >= 0 && j >= 0 && i < w && j < d && !blocked[j * w + i]; } };
}
// Murs d'intérieur. Nord et ouest pleine hauteur ; sud et est bas (vue en coupe vers la caméra). Ouvertures aux portes.
export function wallsOf(loc, doors = []) {
  if (loc.kind !== 'interior') return [];
  const t = UNITS.wall, W = loc.size.w, D = loc.size.d, half = UNITS.door.width / 2, H = UNITS.storey, low = 0.9;
  const ds = doors.filter(d => d.location === loc.id);
  const seg = (side, fixed, len, h) => {
    const gaps = ds.filter(d => d.opening.side === side).map(d => side === 'south' || side === 'north' ? d.opening.x : d.opening.z).sort((a, b) => a - b);
    const parts = []; let a = 0;
    for (const g of gaps) { parts.push([a, g - half]); a = g + half; } parts.push([a, len]);
    return parts.filter(([p, q]) => q - p > 0.01).map(([p, q]) => (side === 'south' || side === 'north')
      ? { x: p, z: fixed, w: q - p, d: t, h } : { x: fixed, z: p, w: t, d: q - p, h });
  };
  return [...seg('north', 0, W, H), ...seg('west', 0, D, H), ...seg('south', D - t, W, low), ...seg('east', W - t, D, low)]
    .map((s, k) => ({ ...s, id: 'wall' + k, isWall: true }));
}
