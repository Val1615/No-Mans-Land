// v7 : Dusk-Town entière. Quatre quartiers reliés à pied par leurs bouts de rue. Voir docs/quartiers/DUSK_TOWN_PLAN.md.
// Q1 La Pompe (centre, inchangé hors passage est) ; Q2 Le Transit (est) ; Q3 Le Scellé (nord) ; Q4 Les Sables (sud).
import * as Q1 from './dusk_q1.js';
import { BUILDINGS_Q2, PAINTED_DOORS_Q2, BUILDINGS_Q3, PAINTED_DOORS_Q3, BUILDINGS_Q4, PAINTED_DOORS_Q4 } from './buildings_town.js';

const ext = (id, name, buildings, zones, props, spawn) => ({ id, name, size: { w: 48, d: 36 }, kind: 'exterior',
  ground: { base: '#8d7a5e', skin: 'g_sand', zones }, buildings, props, spawn });
export const LOCATIONS = {
  ...Q1.LOCATIONS,
  // Q2 : l'avenue continue vers l'est. C'est la route des patrouilles (Ch. I §69) ; tout y est plus vide qu'à La Pompe.
  dusk_q2: ext('dusk_q2', 'Dusk-Town · Le Transit', BUILDINGS_Q2, [
      { x: 0, z: 14, w: 48, d: 8, kind: 'asphalt' }, { x: 44, z: 15, w: 4, d: 6, kind: 'track' },
      { x: 0, z: 32, w: 7, d: 4, kind: 'grass' }, { x: 20, z: 0, w: 4, d: 8.5, kind: 'packed' } ], [
      { sprite: 'wreck', x: 20.5, z: 19.6, fp: [4.6, 2.4] }, { sprite: 'tires', x: 33, z: 15.2 }, { sprite: 'rubble', x: 13, z: 21.2 },
      { sprite: 'sandbags', x: 44.5, z: 13.2 }, { sprite: 'rubble', x: 45.6, z: 23.4 }, { sprite: 'lamp', x: 9.0, z: 14.3, solid: 0.3 },
      { sprite: 'barrel', x: 33.6, z: 12.3 }, { sprite: 'crate', x: 23.2, z: 23.2 }, { sprite: 'bush', x: 2, z: 34 }, { sprite: 'bush', x: 47, z: 2 },
      { sprite: 'bush', x: 13, z: 33 }, { sprite: 'rubble', x: 36, z: 33 } ],
    { player: { x: 2, z: 20 }, companion: { x: 2, z: 18.6 } }),
  // Q3 : la place devant l'accès scellé du laboratoire (Ch. I §75). Une ruelle part vers le sud et La Pompe.
  dusk_q3: ext('dusk_q3', 'Dusk-Town · Le Scellé', BUILDINGS_Q3, [
      { x: 0, z: 14, w: 48, d: 6, kind: 'packed' }, { x: 25, z: 20, w: 6, d: 16, kind: 'packed' },
      { x: 21, z: 5, w: 14, d: 9, kind: 'track' }, { x: 40, z: 31, w: 8, d: 5, kind: 'grass' } ], [
      { sprite: 'rubble', x: 23.2, z: 7.6 }, { sprite: 'board', x: 33.2, z: 4.6 }, { sprite: 'crate', x: 21.6, z: 10.8 },
      { sprite: 'tires', x: 9.8, z: 22.6 }, { sprite: 'rubble', x: 44, z: 22.4 }, { sprite: 'bush', x: 23, z: 33 }, { sprite: 'bush', x: 2, z: 2 },
      { sprite: 'barrel', x: 32, z: 22.4 }, { sprite: 'rubble', x: 1.6, z: 33 } ],
    { player: { x: 28, z: 34 }, companion: { x: 28.8, z: 33 } }),
  // Q4 : la rue sud s'ensable ; au bout, plus de ville (Ch. I §71 « sable, herbes mortes »).
  dusk_q4: ext('dusk_q4', 'Dusk-Town · Les Sables', BUILDINGS_Q4, [
      { x: 25, z: 0, w: 6, d: 26, kind: 'packed' }, { x: 2, z: 30, w: 6, d: 5, kind: 'grass' } ], [
      { sprite: 'rubble', x: 23.6, z: 12.6 }, { sprite: 'cart', x: 31.8, z: 11.8 }, { sprite: 'tires', x: 24, z: 21.5 },
      { sprite: 'rubble', x: 30.4, z: 28.4 }, { sprite: 'bush', x: 10, z: 4 }, { sprite: 'bush', x: 45, z: 12 }, { sprite: 'bush', x: 8, z: 26 },
      { sprite: 'barrel', x: 23.8, z: 4.4 }, { sprite: 'rubble', x: 44, z: 33 }, { sprite: 'bush', x: 26, z: 33.5 } ],
    { player: { x: 28, z: 2 }, companion: { x: 29, z: 3 } }),
  // Intérieurs v7 : mêmes règles qu'en v6 (textures et mobilier contrôlés par tools_interiors.py, posés par emprise).
  guet_in: { id: 'guet_in', name: 'Le guet', kind: 'interior', size: { w: 5, d: 6 }, ground: { base: '#7d6a52', skin: 'f_earth', tileM: 2 },
    wall: '#cfc6b4', wallSkin: 'w_plaster', buildings: [], props: [
      { furn: 'home_mattress_d', x: 0.3, z: 0.3 }, { furn: 'm_desk', x: 3.3, z: 0.3 }, { furn: 'home_water', x: 3.4, z: 3.4 } ] },
  atelier_in: { id: 'atelier_in', name: 'L\'atelier', kind: 'interior', size: { w: 7, d: 6 }, ground: { base: '#857055', skin: 'f_concrete', tileM: 3 },
    wall: '#8d6446', wallSkin: 'w_brick', buildings: [], props: [
      { furn: 'shop_shelf', x: 0.4, z: 0.25 }, { furn: 'm_archive_shelf', x: 4.9, z: 0.25 }, { furn: 'clinic_stretcher_b', x: 0.4, z: 3.0 },
      { furn: 'clinic_table', x: 4.6, z: 3.2 } ] },
  citerne_in: { id: 'citerne_in', name: 'La citerne', kind: 'interior', size: { w: 8, d: 6 }, ground: { base: '#857055', skin: 'f_concrete', tileM: 3 },
    wall: '#b89c74', wallSkin: 'w_planks', buildings: [], props: [
      { furn: 'home_water', x: 0.4, z: 0.4 }, { furn: 'home_water', x: 2.0, z: 0.4 }, { furn: 'home_water', x: 0.4, z: 1.6 },
      { furn: 'bar_table_b', x: 4.6, z: 0.5 }, { furn: 'home_curtain', x: 4.6, z: 3.6 }, { furn: 'home_mattress_d', x: 4.8, z: 4.6 } ] }
};

const painted = (list, loc, T) => list.map(d => ({ id: d.id, buildingId: d.buildingId, location: loc, opening: { x: d.opening[0], z: d.opening[1], side: d.face === 's' ? 'south' : 'east' },
  threshold: { x: d.threshold[0], z: d.threshold[1] }, target: { doorId: T[d.id] }, conditions: [], painted: d.painted_px }));
// Jonction = bout de rue. opening sur le bord, threshold 1 m à l'intérieur ; franchie quand le joueur s'arrête dessus.
const J = (id, loc, ox, oz, tx, tz, to, label) => ({ id, location: loc, junction: true, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: { doorId: to }, conditions: [] });
// Bord = bout de rue sans voisin : la ville s'arrête là. Annoncé, pas de contenu.
const E = (id, loc, ox, oz, tx, tz, label, text) => ({ id, location: loc, edge: text, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: null, conditions: [] });
export const DOORS = [
  ...Q1.DOORS,
  ...painted(PAINTED_DOORS_Q2, 'dusk_q2', { t_guet_door: 'guet_in_door' }),
  ...painted(PAINTED_DOORS_Q3, 'dusk_q3', { s_atelier_door: 'atelier_in_door' }),
  ...painted(PAINTED_DOORS_Q4, 'dusk_q4', { d_citerne_door: 'citerne_in_door' }),
  { id: 'guet_in_door', location: 'guet_in', opening: { x: 2.5, z: 6, side: 'south' }, threshold: { x: 2.5, z: 5 }, target: { doorId: 't_guet_door' }, conditions: [] },
  { id: 'atelier_in_door', location: 'atelier_in', opening: { x: 3.5, z: 6, side: 'south' }, threshold: { x: 3.5, z: 5 }, target: { doorId: 's_atelier_door' }, conditions: [] },
  { id: 'citerne_in_door', location: 'citerne_in', opening: { x: 8, z: 3, side: 'east' }, threshold: { x: 7, z: 3 }, target: { doorId: 'd_citerne_door' }, conditions: [] },
  // Jonctions (chaque paire = même rue, des deux côtés du raccord)
  J('j_q1_est', 'dusk_q1', 48, 20, 47, 20, 'j_q2_ouest', 'Vers Le Transit'),  J('j_q2_ouest', 'dusk_q2', 0, 20, 1, 20, 'j_q1_est', 'Vers La Pompe'),
  J('j_q1_nord', 'dusk_q1', 28, 0, 28, 1, 'j_q3_sud', 'Vers Le Scellé'),      J('j_q3_sud', 'dusk_q3', 28, 36, 28, 35, 'j_q1_nord', 'Vers La Pompe'),
  J('j_q1_sud', 'dusk_q1', 28, 36, 28, 35, 'j_q4_nord', 'Vers Les Sables'),    J('j_q4_nord', 'dusk_q4', 28, 0, 28, 1, 'j_q1_sud', 'Vers La Pompe'),
  // Bords de ville (désert)
  E('b_q1_ouest', 'dusk_q1', 0, 18, 0.8, 18, 'Désert', 'La piste se perd dans le sable. Rien à pied par là.'),
  E('b_q2_est', 'dusk_q2', 48, 18, 47, 18, 'Route des patrouilles', 'La route file vers l\'est, celle des camions. Personne ne la prend à pied.'),
  E('b_q3_ouest', 'dusk_q3', 0, 17, 1, 17, 'Désert', 'Les murs s\'arrêtent, le sable commence.'),
  E('b_q3_est', 'dusk_q3', 48, 17, 47, 17, 'Désert', 'Plus une maison. Du sable jusqu\'à l\'horizon.'),
  E('b_q4_sud', 'dusk_q4', 28, 36, 28, 35, 'Terres dévastées', 'Au-delà, les terres dévastées. Pas sans eau, pas sans arme, pas aujourd\'hui.')
];
export const NPCS = [
  ...Q1.NPCS,
  { id: 'teo', name: 'Teo', sprite: 'gen_teo', location: 'guet_in', x: 3.9, z: 1.6, faceTo: [3.9, 0], dialogue: 'teo' },
  { id: 'ezequiel', name: 'Ezequiel', sprite: 'gen_ezequiel', location: 'atelier_in', x: 2.6, z: 2.2, faceTo: [3.5, 6], dialogue: 'ezequiel' },
  { id: 'sol', name: 'Sol', sprite: 'gen_sol', location: 'citerne_in', x: 3.4, z: 2.6, faceTo: [8, 3], dialogue: 'sol' }
];
export const START = Q1.START, COMPANION = Q1.COMPANION;
// Textes au clic sur les façades fermées qui en disent plus que « fermé ».
export const CLOSED_TEXT = {
  s_lab: 'Porte d\'acier, soudée de l\'intérieur. Des marques de pied-de-biche partout autour. Aucune n\'est allée plus loin que la peinture.',
  t_cinema: 'Cinéma muré. Les affiches ont été arrachées pour faire du feu.'
};
