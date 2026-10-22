// v12 Steel-Megalopolis, lot L1 : la route et la douane (S0), puis Center-Town (S1). Voir docs/villes/STEEL_MEGALOPOLIS_PLAN.md.
// [décision] Valentin : entrée selon la race (augmenté / cyborg passent avec l'implant, humain refusé, mutant attaqué à vue) ;
// premier quartier = Center-Town ; la quête s'arrête une fois en ville. Le reste (PNJ, textes, plan, taux) = [proposition].
import { BUILDINGS_ROUTE, PAINTED_DOORS_ROUTE, BUILDINGS_CENTER, PAINTED_DOORS_CENTER } from './buildings_steel.js';

const named = list => list.map(b => ({ ...b, named: true }));
export const LOCATIONS = {
  // S0 : la route finit au pied du sarcophage. Douane devant la porte ; au sud-est, une trappe dans le sable.
  steel_route: { id: 'steel_route', name: 'Steel-Megalopolis · La douane', kind: 'exterior', size: { w: 48, d: 36 },
    ground: { base: '#8d7a5e', skin: 'g_sand', zones: [
      { x: 28, z: 20, w: 4, d: 16, kind: 'asphalt' }, { x: 8, z: 18, w: 24, d: 4, kind: 'asphalt' }, { x: 20, z: 18, w: 8, d: 3, kind: 'concrete' } ] },
    buildings: named(BUILDINGS_ROUTE), props: [
      { sprite: 'sandbags', x: 18.5, z: 22.6 }, { sprite: 'sandbags', x: 27.4, z: 15.6 }, { sprite: 'lamp', x: 27.2, z: 21.4, solid: 0.3 },
      { sprite: 'lamp', x: 12.5, z: 22.4, solid: 0.3 }, { sprite: 'barrel', x: 33.4, z: 14.6 }, { sprite: 'wreck', x: 38, z: 22.5, fp: [4.6, 2.4] },
      { sprite: 'rubble', x: 44, z: 9 }, { sprite: 'tires', x: 35.5, z: 31.2 }, { sprite: 'bush', x: 46, z: 33 }, { sprite: 'rubble', x: 15, z: 32 } ],
    spawn: { player: { x: 30, z: 34 }, companion: { x: 31, z: 34 } }, city: null,
    arrive: { from: 'dusk_q2', text: 'Une journée de marche vers l\u2019est. Le dôme grandit pendant des heures, puis il n\u2019y a plus que lui.' } },
  douane_in: { id: 'douane_in', name: 'Steel-Megalopolis · Poste de douane', kind: 'interior', size: { w: 8, d: 6 },
    ground: { base: '#6d6a66', skin: 'f_tiles', tileM: 2 }, wall: '#9aa0a4', wallSkin: 'w_plaster', buildings: [], props: [
      { furn: 'shop_counter', x: 2.6, z: 0.3 }, { furn: 'm_archive_shelf', x: 0.3, z: 0.25 }, { furn: 'm_desk', x: 5.6, z: 0.3 } ], city: null },
  // S1 : sous le dôme. Béton, néons, tours ; le ciel est un plafond. Aucun personnage du roman (2175).
  steel_center: { id: 'steel_center', name: 'Steel-Megalopolis · Center-Town', kind: 'exterior', size: { w: 48, d: 36 },
    ground: { base: '#55524f', skin: 'g_concrete', zones: [ { x: 0, z: 14, w: 48, d: 8, kind: 'asphalt' }, { x: 21, z: 13, w: 4, d: 11, kind: 'asphalt' } ] },
    buildings: named(BUILDINGS_CENTER), props: [
      { sprite: 'lamp', x: 9, z: 14.3, solid: 0.3 }, { sprite: 'lamp', x: 33, z: 14.3, solid: 0.3 }, { sprite: 'lamp', x: 20, z: 21.7, solid: 0.3 },
      { sprite: 'bench', x: 27.5, z: 22.6 }, { sprite: 'crate', x: 44.5, z: 22.8 }, { sprite: 'barrel', x: 0.8, z: 23.2 } ],
    spawn: { player: { x: 1, z: 18 }, companion: { x: 1, z: 19 } }, city: 'steel' },
  change_in: { id: 'change_in', name: 'Center-Town · Change de Teng', kind: 'interior', size: { w: 6, d: 5 },
    ground: { base: '#5b4f45', skin: 'f_concrete', tileM: 3 }, wall: '#5e5650', wallSkin: 'w_brick', buildings: [], props: [
      { furn: 'shop_counter', x: 1.6, z: 0.3 }, { furn: 'shop_shelf', x: 4.0, z: 0.25 } ], city: 'steel' },
};
const painted = (list, loc, T) => list.map(d => ({ id: d.id, buildingId: d.buildingId, location: loc, opening: { x: d.opening[0], z: d.opening[1], side: d.face === 's' ? 'south' : 'east' },
  threshold: { x: d.threshold[0], z: d.threshold[1] }, target: { doorId: T[d.id] }, conditions: [] }));
const J = (id, loc, ox, oz, tx, tz, to, label, conditions = []) => ({ id, location: loc, junction: true, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: { doorId: to }, conditions });
const E = (id, loc, ox, oz, tx, tz, label, text) => ({ id, location: loc, edge: text, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: null, conditions: [] });
export const ROUTE_TEXT = 'La route file vers l\'est, celle des camions. Personne ne la prend à pied.';
export const DOORS = [
  // La route des patrouilles (bord est du Transit) s'ouvre quand la porte d'acier est derrière toi [proposition, plan §2]
  J('j_q2_est', 'dusk_q2', 48, 18, 47, 18, 'j_route_sud', 'Route des patrouilles', [{ test: s => !!s.flags.q_fin, reason: 'route', text: ROUTE_TEXT }]),
  J('j_route_sud', 'steel_route', 30, 36, 30, 35, 'j_q2_est', 'Vers Dusk-Town'),
  ...painted(PAINTED_DOORS_ROUTE, 'steel_route', { r_douane_door: 'douane_in_sud' }).map(d => ({ ...d,
    conditions: [{ test: s => !s.flags.race_mutant, reason: 'mutant', text: 'Le soldat lève son arme avant que tu touches la porte.' }] })),
  { id: 'douane_in_sud', location: 'douane_in', opening: { x: 2, z: 6, side: 'south' }, threshold: { x: 2, z: 5 }, target: { doorId: 'r_douane_door' }, conditions: [] },
  { id: 'douane_in_est', location: 'douane_in', label: 'Vers Center-Town', opening: { x: 8, z: 4, side: 'east' }, threshold: { x: 7, z: 4 }, target: { doorId: 'c_ouest' },
    conditions: [{ test: s => !!s.flags.steel_passe, reason: 'douane', text: 'La barrière reste baissée. Il faut d\u2019abord passer au guichet.' }] },
  J('c_ouest', 'steel_center', 0, 18, 1, 18, 'douane_in_est', 'Vers la douane'),
  ...painted(PAINTED_DOORS_CENTER, 'steel_center', { c_change_door: 'change_in_door' }),
  { id: 'change_in_door', location: 'change_in', opening: { x: 3, z: 5, side: 'south' }, threshold: { x: 3, z: 4 }, target: { doorId: 'c_change_door' }, conditions: [] },
  E('c_est', 'steel_center', 48, 18, 47, 18, 'Vers les autres quartiers', 'L\u2019avenue continue vers Lower-Town et Asia-Ground. Plus tard. D\u2019abord, apprendre celui-ci.'),
  E('r_ouest', 'steel_route', 0, 26, 1, 26, 'Désert', 'Du sable, et le mur du dôme qui ne finit pas.'),
];
export const NPCS = [
  { id: 'odile', name: 'Odile Varga', sprite: 'gen_odile', location: 'douane_in', x: 3.8, z: 1.7, faceTo: [3.8, 6], dialogue: 'odile' },
  { id: 'halloran', name: 'Sergent Halloran', sprite: 'gen_halloran', location: 'steel_route', x: 25.2, z: 20.6, faceTo: [30, 34], dialogue: 'halloran' },
  { id: 'teng', name: 'Teng', sprite: 'gen_teng', location: 'change_in', x: 2.8, z: 2.0, faceTo: [3, 5], dialogue: 'teng' },
  { id: 'patrouilleur', name: 'Patrouilleur', sprite: 'gen_halloran', location: 'steel_center', x: 30.5, z: 19.8, faceTo: [22, 18], dialogue: 'patrouilleur' },
];
export const CLOSED_TEXT = {
  r_porte: 'La route entre dans le noir entre deux battants grands comme des immeubles. Sans passer la douane, les tourelles s\u2019en chargent.',
  r_service: s => s.flags.sol_passage ? 'La trappe dont parlait Sol. Chaîne neuve, cadenas neuf. Celui qui passe par là ne passe pas par le dessus.' : 'Une trappe de service à moitié ensablée, chaîne et cadenas. Des traces de pas fraîches, qui n\u2019en reviennent pas.',
  c_arcadius: 'Arcadius Center. Les portes s\u2019ouvrent pour les implants qu\u2019elles reconnaissent, pas pour les autres.',
  c_blanc: 'Bureau des permis. Un écran annonce un délai d\u2019attente qui ne veut rien dire.',
  c_neon: 'Une galerie de néons. Tout y est à vendre, en crédits.',
};
// Crochet du futur combat [décision : mutant à la douane = premier combat ; fuite vers le désert ; 0 PV = capture, Sous-Ville].
// Le combat n'existe pas encore : la scène « halloran » le remplace par deux choix scriptés (provisoire, documenté).
// Le jour où le combat existe : l'action « hook:douane_mutant » lancera le combat, et ses deux issues remplaceront ces choix.
export const COMBAT_HOOKS = { douane_mutant: { status: 'provisoire', fuite: 'warp:steel_route:30:34', capture: 'warp:steel_route:42:34', note: 'L2 : la capture mènera dans la Sous-Ville' } };
export const DIALOGUES = {
  odile: {
    start: { text: 'Suivant. Motif ?', options: [
      { label: 'Entrer. Je cherche du travail.', next: 'lu', if: 'implant&!steel_passe' },
      { label: 'Entrer. Je cherche du travail.', next: 'refus', if: '!implant', action: 'flag:steel_refuse' },
      { label: 'Changer des dollars (20 $ contre 11 cr)', action: 'change:20:11', next: 'change', if: 'implant' },
      { label: 'Je repasse la barrière.', next: 'passe', if: 'steel_passe' },
      { label: 'Rien. Je regardais.', next: 'end' } ] },
    lu: { text: 'Poignet. Plus près. Voilà. Implant lu, aucune dette, aucun signalement. Entrée de transit, sept jours, renouvelable au bureau des permis. Le change est ici ou chez les changeurs de la place. Ici, au moins, on ne vous vole qu\u2019officiellement.', options: [
      { label: 'Merci.', action: 'flag:steel_passe;flag:q_douane', next: 'passe' } ] },
    passe: { text: 'Barrière à votre droite. Ne courez pas dans le couloir, les caméras n\u2019aiment pas ça.', options: [ { label: 'J\u2019y vais.', next: 'end' } ] },
    refus: { text: 'Je ne lis rien. Pas d\u2019implant, pas de fiche. Pour IO, vous n\u2019êtes personne, et personne ne passe cette barrière.', options: [
      { label: 'Je peux payer.', next: 'payer' }, { label: 'Et si je reviens demain ?', next: 'demain' }, { label: 'Je m\u2019en vais.', next: 'end' } ] },
    payer: { text: 'Je n\u2019ai rien entendu, et vous n\u2019avez rien dit. Suivant.', options: [ { label: 'Je m\u2019en vais.', next: 'end' } ] },
    demain: { text: 'Demain, je lirai la même chose. Moi ou une autre.', options: [ { label: 'Je m\u2019en vais.', next: 'end' } ] },
    change: { text: 'Vingt dollars, onze crédits. Le taux est affiché derrière moi. Personne ne le lit non plus.', options: [ { label: 'Merci.', next: 'start' } ] },
    pauvre: { text: 'Il manque des dollars. Le taux, lui, ne bouge pas.', options: [ { label: 'Tant pis.', next: 'end' } ] },
  },
  halloran: {
    start: { text: 'La douane, c\u2019est le guichet, là. Moi, je regarde.', alt: [
        { if: 'race_mutant&steel_fui', text: 'Encore toi. Tu as eu de la chance une fois. Le col.' },
        { if: 'race_mutant', text: 'Hé. Toi. Les mains où je les vois. Non. Le col. Baisse le col.' },
        { if: 'steel_refuse', text: 'Refoulé ? Alors la route, c\u2019est par là. Ne traîne pas sous les tourelles.' },
        { if: 'steel_passe', text: 'Implant lu, tu es en règle. Avance.' } ], options: [
      { label: 'Courir vers le désert.', if: 'race_mutant', action: 'hook:douane_mutant;hurt:9;flag:steel_attaque;flag:steel_fui;warp:steel_route:30:34', next: 'fui' },
      { label: 'Rester. Lever les mains.', if: 'race_mutant', next: 'insiste' },
      { label: 'Je passe juste.', if: '!race_mutant', next: 'end' } ] },
    fui: { text: 'Deux tirs. Le premier soulève le sable, le second t\u2019ouvre l\u2019épaule. Tu cours jusqu\u2019à n\u2019entendre plus que ton souffle.', options: [ { label: 'Reprendre mon souffle.', next: 'end' } ] },
    insiste: { text: 'Il ne tire pas. Il parle dans son col, et deux autres arrivent avec une cagoule et des liens.', options: [
      { label: 'Ne pas résister.', action: 'hook:douane_mutant;hurt:15;flag:steel_attaque;flag:steel_capture;reveal:r_service;warp:steel_route:42:34', next: 'capture' } ] },
    capture: { text: 'Le noir. Des marches. Une odeur d\u2019huile chaude et de machines. Puis on te jette dehors, à côté d\u2019une trappe enchaînée, avec une côte qui craque. Quelqu\u2019un a dit « Sous-Ville ». Ce sera pour une autre fois.', options: [ { label: 'Me relever.', next: 'end' } ] },
  },
  teng: {
    start: { text: 'Des dollars ? J\u2019adore les dollars. Personne n\u2019en veut ici, alors je les prends tous. Dix dollars, six crédits, et je souris en prime.', options: [
      { label: 'Changer 10 $ (6 cr)', action: 'change:10:6', next: 'merci' },
      { label: 'Ce bâtiment de verre, en face ?', action: 'reveal:c_arcadius', next: 'arcadius' },
      { label: 'Où on fait ses papiers ?', action: 'reveal:c_blanc', next: 'permis' },
      { label: 'Plus tard.', next: 'end' } ] },
    merci: { text: 'Six, sept... non, six. Un plaisir. Reviens quand tu veux, je ne ferme jamais, je dors debout.', options: [ { label: 'Autre chose.', next: 'start' }, { label: 'Au revoir.', next: 'end' } ] },
    arcadius: { text: 'Arcadius Center. Tout ce qui porte un implant y a une fiche. La tienne aussi. N\u2019y entre pas sans y être appelé.', options: [ { label: 'Autre chose.', next: 'start' } ] },
    permis: { text: 'Le bureau blanc, de l\u2019autre côté de l\u2019avenue. Ils ouvrent quand l\u2019écran le décide. Prends un livre.', options: [ { label: 'Autre chose.', next: 'start' } ] },
    pauvre: { text: 'Pas de dollars, pas de sourire. C\u2019est la règle, désolé.', options: [ { label: 'Tant pis.', next: 'end' } ] },
  },
  patrouilleur: {
    start: { text: 'Circulez. L\u2019avenue est à tout le monde, mais pas pour longtemps.', options: [
      { label: 'Il y a un change, par ici ?', action: 'reveal:c_change', next: 'change' }, { label: 'Je circule.', next: 'end' } ] },
    change: { text: 'Chez Teng, les boutiques en face. Compte ta monnaie deux fois.', options: [ { label: 'Merci.', next: 'end' } ] },
  },
};
