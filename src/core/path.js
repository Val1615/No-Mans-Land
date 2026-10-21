// A* 8 directions sans couper les coins.
export function findPath(grid, from, to) {
  const [si, sj] = grid.toCell(from.x, from.z), [ti, tj] = grid.toCell(to.x, to.z);
  if (!grid.free(ti, tj)) return null;
  const key = (i, j) => j * grid.w + i, open = new Map(), g = new Map(), came = new Map();
  const h = (i, j) => Math.hypot(i - ti, j - tj);
  open.set(key(si, sj), [si, sj, h(si, sj)]); g.set(key(si, sj), 0);
  const closed = new Set();
  while (open.size) {
    let best = null; for (const [k, v] of open) if (!best || v[2] < best[1][2]) best = [k, v];
    const [k, [i, j]] = best; open.delete(k);
    if (i === ti && j === tj) { const p = []; let c = k; while (c != null) { p.push(grid.toWorld(c % grid.w, Math.floor(c / grid.w))); c = came.get(c); } return p.reverse(); }
    closed.add(k);
    for (let di = -1; di <= 1; di++) for (let dj = -1; dj <= 1; dj++) {
      if (!di && !dj) continue; const ni = i + di, nj = j + dj, nk = key(ni, nj);
      if (!grid.free(ni, nj) || closed.has(nk)) continue;
      if (di && dj && (!grid.free(i + di, j) || !grid.free(i, j + dj))) continue;
      const ng = g.get(k) + Math.hypot(di, dj);
      if (ng < (g.get(nk) ?? Infinity)) { g.set(nk, ng); came.set(nk, k); open.set(nk, [ni, nj, ng + h(ni, nj)]); }
    }
  }
  return null;
}
