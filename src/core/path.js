// A* 8 directions sans couper les coins. File de priorité en tas binaire et tableaux typés (Center-Town 132 x 116 m = 61 600 cases :
// plus de gel au clic sur les longs trajets ; l'ancienne recherche linéaire du meilleur nœud ouvert coûtait 120-177 ms par diagonale).
export function findPath(grid, from, to) {
  const [si, sj] = grid.toCell(from.x, from.z), [ti, tj] = grid.toCell(to.x, to.z);
  if (!grid.free(ti, tj)) return null;
  const W = grid.w, typed = Number.isFinite(grid.d), N = typed ? W * grid.d : 0, key = (i, j) => j * W + i;
  // g (coût connu), came (parent), closed : tableaux typés si la grille donne sa profondeur, sinon Map (grilles de test)
  const gA = typed ? new Float64Array(N).fill(Infinity) : null, cA = typed ? new Int32Array(N).fill(-1) : null, xA = typed ? new Uint8Array(N) : null;
  const gM = new Map(), cM = new Map(), xM = new Set();
  const getG = k => typed ? gA[k] : (gM.get(k) ?? Infinity), setG = (k, v) => typed ? (gA[k] = v) : gM.set(k, v);
  const getC = k => typed ? (cA[k] < 0 ? null : cA[k]) : (cM.get(k) ?? null), setC = (k, v) => typed ? (cA[k] = v) : cM.set(k, v);
  const isX = k => typed ? xA[k] === 1 : xM.has(k), setX = k => typed ? (xA[k] = 1) : xM.add(k);
  const h = (i, j) => Math.hypot(i - ti, j - tj);
  const heap = []; // [f, i, j, k] ; entrées périmées ignorées au retrait (nœud déjà fermé)
  const push = e => { let c = heap.length; heap.push(e); while (c > 0) { const p = (c - 1) >> 1; if (heap[p][0] <= e[0]) break; heap[c] = heap[p]; c = p; } heap[c] = e; };
  const pop = () => { const top = heap[0], last = heap.pop(), n = heap.length; if (n) { let c = 0;
    for (;;) { const l = 2 * c + 1, r = l + 1; let m = c, mv = last; if (l < n && heap[l][0] < mv[0]) { m = l; mv = heap[l]; } if (r < n && heap[r][0] < mv[0]) { m = r; mv = heap[r]; }
      if (m === c) break; heap[c] = heap[m]; c = m; } heap[c] = last; } return top; };
  const k0 = key(si, sj); setG(k0, 0); push([h(si, sj), si, sj, k0]);
  while (heap.length) {
    const [, i, j, k] = pop();
    if (isX(k)) continue;
    if (i === ti && j === tj) { const p = []; let c = k; while (c != null) { p.push(grid.toWorld(c % W, Math.floor(c / W))); c = getC(c); } return p.reverse(); }
    setX(k);
    const gk = getG(k);
    for (let di = -1; di <= 1; di++) for (let dj = -1; dj <= 1; dj++) {
      if (!di && !dj) continue; const ni = i + di, nj = j + dj, nk = key(ni, nj);
      if (!grid.free(ni, nj) || isX(nk)) continue;
      if (di && dj && (!grid.free(i + di, j) || !grid.free(i, j + dj))) continue;
      const ng = gk + (di && dj ? Math.SQRT2 : 1);
      if (ng < getG(nk)) { setG(nk, ng); setC(nk, k); push([ng + h(ni, nj), ni, nj, nk]); }
    }
  }
  return null;
}
