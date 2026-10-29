// Placement générique des libellés de carte : chaque icône reste sur son point ; son libellé prend la première position
// (droite, gauche, dessous, dessus, diagonales) qui ne recouvre ni une icône ni un libellé déjà placé et reste dans le plan.
// Faute de place libre : la position au moindre recouvrement. Recalculé à chaque redimensionnement du plan (zoom, rotation).
const inter = (a, b) => Math.max(0, Math.min(a.r, b.r) - Math.max(a.l, b.l)) * Math.max(0, Math.min(a.b, b.b) - Math.max(a.t, b.t));
const box = r => ({ l: r.left, t: r.top, r: r.right, b: r.bottom });
export function placeLabels(plan, sel = 'button') {
  if (!plan) return; if (!plan.__ro && window.ResizeObserver) { plan.__ro = new ResizeObserver(() => placeLabels(plan, sel)); plan.__ro.observe(plan); }
  const P = box(plan.getBoundingClientRect()), items = [...plan.querySelectorAll(sel)].map(b => ({ b, i: b.querySelector('img'), s: b.querySelector('span') })).filter(x => x.i);
  for (const x of items) if (x.s) { x.s.style.position = 'absolute'; x.s.style.left = '0px'; x.s.style.top = '0px'; }
  for (const x of items) x.ib = box(x.i.getBoundingClientRect()); const obst = items.map(x => x.ib).filter(r => r.r > r.l);
  for (const x of items) { if (!x.s || !x.s.offsetWidth) continue;
    const I = x.ib, B = x.b.getBoundingClientRect(), w = x.s.offsetWidth, h = x.s.offsetHeight, iw = I.r - I.l, cy = I.t + (iw - h) / 2, cx = I.l + (iw - w) / 2, g = 3;
    let C = [[I.r + g, cy], [I.l - w - g, cy], [cx, I.b + 1], [cx, I.t - h - 1], [I.r + g, I.t - h + 4], [I.r + g, I.b - 4], [I.l - w - g, I.t - h + 4], [I.l - w - g, I.b - 4],
      [I.r + g, I.b + 1], [I.l - w - g, I.b + 1], [I.r + g, I.t - h - 1], [I.l - w - g, I.t - h - 1]];
    if (x.b.classList.contains('gauche')) [C[0], C[1]] = [C[1], C[0]];
    let best = null, cost = Infinity;
    for (const [l, t] of C) { const R = { l, t, r: l + w, b: t + h }, out = (R.r - R.l) * (R.b - R.t) - inter(R, P);
      const c = out * 4 + obst.reduce((a, o) => a + (o === I ? 0 : inter(R, o)), 0); if (c < cost - 0.5) { cost = c; best = R; } if (c < 0.5) break; }
    x.s.style.left = (best.l - B.left) + 'px'; x.s.style.top = (best.t - B.top) + 'px'; x.s.dataset.place = cost < 0.5 ? 'libre' : 'force'; obst.push(best); }
}
