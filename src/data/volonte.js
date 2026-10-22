// Réglages de la Volonté (validés par Valentin le 2026-10-22). Toutes les valeurs de règle sont ici.
export const VOLONTE = {
  jet: { min: -2, max: 2 },          // test réussi si Volonté + jet >= seuil
  panique: { seuilPv: 0.25, perteAp: 2, seuil: 6 }, // combat : PV < 25 % ou allié mort
  intimidation: { reductionParPoint: 0.1, max: 0.6 }, // part de l'effet ennemi absorbée par point au-dessus de 5
  blessures: { reductionParPoint: 0.15, max: 0.75 }   // malus des blessures graves
};
export const rollVolonte = (val, seuil, rnd = Math.random) => {
  const { min, max } = VOLONTE.jet, d = min + Math.floor(rnd() * (max - min + 1));
  return { ok: val + d >= seuil, total: val + d, d };
};
