// Niveaux praticables (Mega-Line v2, 17/11) : le moteur n'a qu'un niveau de marche par point (x, z) ; un lieu peut donner une hauteur de sol
// par zone (loc.niveaux) : { x, z, w, d, y } (plancher plat, ex. quai à +6 m) ou { x, z, w, d, y0, y1, axe: 'x'|'z' } (rampe ou escalier :
// y0 au bord min de l'axe, y1 au bord max). Hauteur au point = maximum des zones qui le contiennent, 0 ailleurs.
// L'accès d'un niveau à l'autre est réglé par les solides du lieu (garde-corps, bords de quai) : seuls les escaliers et rampes raccordent.
// Utilisé par le rendu (hauteur des personnages, clic sur le quai, anneaux de porte) et par le jeu (approche d'un PNJ au même niveau).
export function hauteurSol(loc, x, z) {
  const N = loc?.niveaux; if (!N) return 0;
  let h = 0;
  for (const n of N) {
    if (x < n.x || x > n.x + n.w || z < n.z || z > n.z + n.d) continue;
    const y = n.y ?? (n.axe === 'x' ? n.y0 + (n.y1 - n.y0) * (x - n.x) / n.w : n.y0 + (n.y1 - n.y0) * (z - n.z) / n.d);
    if (y > h) h = y;
  }
  return h;
}
export const hauteurMax = loc => Math.max(0, ...(loc?.niveaux || []).map(n => Math.max(n.y ?? 0, n.y0 ?? 0, n.y1 ?? 0)));
