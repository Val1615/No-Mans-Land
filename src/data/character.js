// v11 lot 2 : création de personnage. Légende : [décision] Valentin, [proposition] à valider, [maquette] repris de src/a runtime-v13 (data.js / app.js).
// Attributs : les 7 de la maquette v0.13, mêmes clés, mêmes noms, 1 à 10, 40 points [décision + maquette].
export const ATTRS = [
  ['force', 'Force', 'dégâts de mêlée, effraction'],
  ['perception', 'Perception', 'précision'],
  ['endurance', 'Endurance', 'santé'],
  ['charisme', 'Charisme', 'négociation'],
  ['intelligence', 'Intelligence', 'technologie et points de compétence'],
  ['agilite', 'Agilité', 'PA et discrétion'],
  // [décision provisoire] maquette : « sensibilité à l'Aura ». L'Aura est absente de la création.
  ['volonte', 'Volonté', 'peur, douleur, intimidation'],
];
export const POINTS = 40, ATTR_MIN = 1, ATTR_MAX = 10;
// 11 compétences [proposition, MENU_CREATION_COMBAT §5] ; base = 5 + 2 x (attribut A + attribut B) [proposition]
export const SKILLS = [
  ['armes', 'Armes à feu', 'perception', 'agilite'],
  ['melee', 'Corps à corps', 'force', 'agilite'],
  ['discretion', 'Discrétion', 'agilite', 'perception'],
  ['crochetage', 'Crochetage', 'agilite', 'intelligence'],
  ['parole', 'Parole', 'charisme', 'intelligence'],
  ['troc', 'Troc', 'charisme', 'perception'],
  ['medecine', 'Médecine', 'intelligence', 'perception'],
  ['mecanique', 'Mécanique', 'intelligence', 'force'],
  ['survie', 'Survie', 'endurance', 'volonte'],
  ['electronique', 'Électronique', 'intelligence', 'intelligence'],
  ['observation', 'Observation', 'perception', 'volonte'],
];
export const FAV_COUNT = 3, FAV_BONUS = 15;
// Races [décision : race à la création, implant pour augmenté et cyborg, réactions de douane] ; effets chiffrés [proposition]
export const RACES = {
  humain: { name: 'Humain', short: 'Ni implant ni mutation. Refusé à la douane de Steel.', implant: false, attrs: { charisme: 1 }, skills: {}, hp: 0,
    effects: ['Charisme +1', 'Pas d\u2019implant : inconnu d\u2019IO', 'Douane de Steel : refusé', 'Dusk-Town se sent chez elle avec toi'],
    portraits: ['portraits-v2-0', 'portraits-v2-1', 'portraits-v2-2', 'portraits-v2-4'] },
  mutant: { name: 'Mutant', short: 'Changé par les radiations. Abattu à vue par le Service.', implant: false, attrs: { endurance: 1 }, skills: {}, hp: 0, radResist: true,
    effects: ['Endurance +1, résiste aux radiations', 'Pas d\u2019implant : inconnu d\u2019IO', 'Service Militarisé : tire à vue', 'Certains, à Dusk-Town, te parlent plus volontiers'],
    portraits: ['portrait-2', 'portraits-v3-mutant-0', 'portraits-v3-mutant-1', 'portraits-v3-mutant-2'] },
  augmente: { name: 'Augmenté', short: 'Implant d\u2019IO sous la peau. Passe la douane.', implant: true, attrs: {}, skills: { electronique: 15 }, hp: 0,
    effects: ['Électronique +15', 'Implant d\u2019IO : reconnu aux portiques', 'Douane de Steel : passe', 'Dusk-Town se méfie du matériel d\u2019IO'],
    portraits: ['portraits-v2-3', 'portraits-v2-5', 'portrait-0', 'portrait-1'] },
  cyborg: { name: 'Cyborg', short: 'Corps en partie mécanique, implant. Passe la douane.', implant: true, attrs: { force: 1 }, skills: {}, hp: 5, healFactor: 0.5,
    effects: ['Force +1, PV +5', 'Implant d\u2019IO, pièces de série', 'Douane de Steel : passe', 'Les soins d\u2019un médecin te réparent moins', 'Les gens des Sables t\u2019évitent'],
    portraits: ['portrait-3', 'portraits-v3-cyborg-0', 'portraits-v3-cyborg-1', 'portraits-v3-cyborg-2'] },
};
// Origines, 3 par race, en 2175 [proposition] : +1 attribut, 1 favorite imposée, 1 objet, des dollars, 1 PNJ qui s'en souviendra (réplique à écrire)
export const ORIGINS = {
  humain: [
    { id: 'recuperatrice', name: 'Récupératrice des ruines', desc: 'Tu as appris à lire un mur avant de l\u2019abattre. Les ruines te nourrissent depuis l\u2019enfance.', attr: 'perception', fav: 'observation', item: 'pince', money: 40, npc: 'anselme', note: 'Anselme t\u2019a déjà racheté de la ferraille.' },
    { id: 'caravanier', name: 'Caravanier sans caravane', desc: 'Les bêtes sont mortes au deuxième puits. Il te reste la route et l\u2019habitude de compter l\u2019eau.', attr: 'endurance', fav: 'troc', item: 'boussole', money: 30, npc: 'sol', note: 'Sol connaît le nom de ton ancien patron.' },
    { id: 'fermiere', name: 'Fille de fermiers de l\u2019oasis', desc: 'Des serres, des pompes, des voisins qui partent. Tu es partie aussi, avec ce que tu savais réparer.', attr: 'intelligence', fav: 'mecanique', item: 'gourde', money: 25, npc: 'mara', note: 'Mara a connu ta mère.' },
  ],
  mutant: [
    { id: 'sables', name: 'Né dans les Sables', desc: 'Tu as grandi caché à Dusk-Town, sous un foulard. Sol te connaît depuis toujours.', attr: 'perception', fav: 'discretion', item: 'foulard', money: 25, npc: 'sol', note: 'Sol te reconnaît. Teo te prévient deux fois avant les camions.' },
    { id: 'rafle', name: 'Rescapé d\u2019une rafle', desc: 'Ils t\u2019ont pris une fois. Tu as sauté du camion avant la capitale, avec une plaque arrachée.', attr: 'agilite', fav: 'survie', item: 'plaque', money: 20, npc: 'teo', note: 'Teo a vu ce camion passer.' },
    { id: 'errant', name: 'Errant des terres brûlées', desc: 'Tu viens de plus loin que la carte. L\u2019eau, tu la sens. Les gens, tu les évites.', attr: 'volonte', fav: 'survie', item: 'compteur', money: 15, npc: 'vera', note: 'Vera veut voir ta peau de près.' },
  ],
  augmente: [
    { id: 'ouvrier', name: 'Ouvrier de Lower-Town congédié', desc: 'Douze ans à la même chaîne, puis une lettre. Ton bras sait encore serrer un boulon au quart de tour.', attr: 'force', fav: 'mecanique', item: 'badge', money: 35, npc: 'ezequiel', note: 'Ezequiel a travaillé dans la même usine.' },
    { id: 'flic', name: 'Ancien flic de la ville basse', desc: 'Tu portais l\u2019insigne du SMPD. Tu ne racontes pas pourquoi tu l\u2019as rendu.', attr: 'charisme', fav: 'parole', item: 'insigne', money: 30, npc: 'hector', note: 'Hector a reconnu ta façon de te tenir.' },
    { id: 'coursier', name: 'Coursier d\u2019IO perdu dans le désert', desc: 'Un colis, un itinéraire, une tempête. Le colis est toujours scellé. L\u2019itinéraire, lui, est perdu.', attr: 'agilite', fav: 'electronique', item: 'colis', money: 20, npc: 'teo', note: 'Teo voudrait savoir ce qu\u2019il y a dans le colis.' },
  ],
  cyborg: [
    { id: 'veteran', name: 'Vétéran réformé du Service Militarisé', desc: 'Ils ont gardé tes médailles et t\u2019ont laissé le bras. Tu connais leurs camions mieux que personne.', attr: 'endurance', fav: 'armes', item: 'matricule', money: 30, npc: 'teo', note: 'Teo te demande les horaires des patrouilles.' },
    { id: 'reconstruit', name: 'Corps reconstruit après un accident de machine', desc: 'Une presse a pris la moitié de toi. On t\u2019a rendu le reste en pièces de série.', attr: 'volonte', fav: 'mecanique', item: 'burette', money: 25, npc: 'ezequiel', note: 'Ezequiel regarde tes articulations avec envie.' },
    { id: 'convoi', name: 'Gardien de convoi au bras de série', desc: 'Tu escortais l\u2019eau entre deux villes. Le convoi est passé. Toi, on t\u2019a oublié au relais.', attr: 'force', fav: 'melee', item: 'cle', money: 35, npc: 'anselme', note: 'Anselme te doit une caisse depuis ce relais.' },
  ],
};
export const ORIGIN_ITEMS = {
  pince: { name: 'Pince à levier' }, boussole: { name: 'Boussole fêlée' }, gourde: { name: 'Gourde cabossée' },
  foulard: { name: 'Foulard de sable' }, plaque: { name: 'Plaque de camion du Service' }, compteur: { name: 'Compteur de radiations' },
  badge: { name: 'Badge d\u2019usine périmé' }, insigne: { name: 'Insigne terni du SMPD' }, colis: { name: 'Colis scellé d\u2019IO' },
  matricule: { name: 'Plaque matricule' }, burette: { name: 'Burette d\u2019huile' }, cle: { name: 'Clé de convoi' },
};
// Traits, 0 à 2 [proposition, §5]
export const TRAITS = {
  nerfs: { name: 'Pas de nerfs', desc: 'Tu agis vite. PA +1, Volonté −2.', ap: 1, attrs: { volonte: -2 } },
  pillard: { name: 'Œil de pillard', desc: 'Tu trouves plus. On te fait payer plus : prix +10 %.', priceMult: 1.1 },
  gueule: { name: 'Gueule cassée', desc: 'On t\u2019écoute quand tu menaces. Charisme −1 en commerce.', intimidate: true, tradeCharisme: -1 },
  insomniaque: { name: 'Insomniaque', desc: 'Tu tiens la garde toute la nuit. PV max −3.', hp: -3 },
  sable: { name: 'Pieds de sable', desc: 'Le désert ne te fatigue pas. En ville, Discrétion −10.', desertWalk: true, skills: { discretion: -10 } },
};
export const MAX_TRAITS = 2;
// Profils prêts à jouer : les 4 de la maquette (mêmes attributs), compétences ramenées aux 11 ; « Aura » remplacée par Observation [proposition]
export const PROFILES = {
  vagabond: { name: 'Le Vagabond', stats: [6, 6, 6, 4, 5, 7, 6], tags: ['armes', 'survie', 'discretion'], desc: 'Un fusil, de bonnes jambes et le sens des mauvaises rencontres.' },
  negociateur: { name: 'La Négociatrice', stats: [3, 5, 5, 9, 7, 5, 6], tags: ['parole', 'troc', 'medecine'], desc: 'Les morts ne négocient pas. Tu préfères qu\u2019ils restent vivants.' },
  technicien: { name: 'Le Technicien', stats: [4, 7, 5, 4, 9, 6, 5], tags: ['electronique', 'mecanique', 'armes'], desc: 'Toute machine a une faiblesse. Toute serrure est une proposition.' },
  egaree: { name: 'L\u2019Égarée', stats: [4, 6, 5, 6, 6, 5, 8], tags: ['observation', 'parole', 'survie'], desc: 'Tu entends quelque chose sous le bruit du vieux monde.' },
};
// Perso par défaut [proposition] : humain, récupératrice ; donne 27/40 PV et 40 $, comme le prototype
export const DEFAULT_DRAFT = { name: 'Rafael Quintero', race: 'humain', origin: 'recuperatrice', portrait: 0, stats: { force: 6, perception: 6, endurance: 5, charisme: 4, intelligence: 6, agilite: 7, volonte: 6 }, favs: ['observation', 'discretion', 'armes'], traits: [], profile: null };

// Dérivés [proposition] : PV max = 25 + 3 x Endurance (+ race, traits) ; on se réveille blessé : PV = 68 % ; PA = 5 + Agilité / 2 (maquette) ; dollars = origine
export function originOf(d) { return ORIGINS[d.race].find(o => o.id === d.origin) || ORIGINS[d.race][0]; }
export function finalAttrs(d) {
  const r = RACES[d.race], o = originOf(d), a = { ...d.stats };
  for (const [k, v] of Object.entries(r.attrs)) a[k] += v;
  a[o.attr] += 1;
  for (const t of d.traits) for (const [k, v] of Object.entries(TRAITS[t].attrs || {})) a[k] += v;
  for (const k in a) a[k] = Math.max(1, Math.min(12, a[k]));
  return a;
}
export function skillsOf(d) {
  const a = finalAttrs(d), r = RACES[d.race], out = {};
  for (const [k, , A, B] of SKILLS) {
    let v = 5 + 2 * (a[A] + a[B]) + (d.favs.includes(k) ? FAV_BONUS : 0) + (r.skills[k] || 0);
    for (const t of d.traits) v += (TRAITS[t].skills || {})[k] || 0;
    out[k] = Math.max(0, Math.min(100, v));
  }
  return out;
}
export function derived(d) {
  const a = finalAttrs(d), r = RACES[d.race], o = originOf(d);
  const maxHp = 25 + 3 * a.endurance + r.hp + d.traits.reduce((s, t) => s + (TRAITS[t].hp || 0), 0);
  const ap = 5 + Math.floor(a.agilite / 2) + d.traits.reduce((s, t) => s + (TRAITS[t].ap || 0), 0);
  return { maxHp, hp: Math.round(maxHp * 0.68), ap, initiative: Math.round((a.agilite + a.perception) / 2), money: o.money, implant: r.implant };
}
export const spent = d => Object.values(d.stats).reduce((s, v) => s + v, 0);
export function valid(d) {
  const o = ORIGINS[d.race]?.find(x => x.id === d.origin);
  return !!o && d.name.trim().length > 0 && spent(d) === POINTS && Object.values(d.stats).every(v => v >= ATTR_MIN && v <= ATTR_MAX)
    && d.favs.length === FAV_COUNT && d.favs.includes(o.fav) && d.traits.length <= MAX_TRAITS;
}
// Personnage stocké dans l'état de jeu (sauvegardé) + drapeaux de race pour les réactions futures (PNJ, douane de Steel)
export function buildCharacter(d) {
  const o = originOf(d), r = RACES[d.race], dv = derived(d);
  return {
    name: d.name.trim().slice(0, 16), race: d.race, origin: o.id, portrait: r.portraits[d.portrait % r.portraits.length],
    base: { ...d.stats }, attrs: finalAttrs(d), skills: skillsOf(d), favs: [...d.favs], traits: [...d.traits], profile: d.profile,
    ap: dv.ap, initiative: dv.initiative, implant: r.implant,
    effects: { radResist: !!r.radResist, healFactor: r.healFactor || 1, priceMult: d.traits.includes('pillard') ? 1.1 : 1, intimidate: d.traits.includes('gueule'), desertWalk: d.traits.includes('sable'),
      steelCustoms: d.race === 'humain' ? 'refuse' : d.race === 'mutant' ? 'attaque' : 'passe' },
  };
}
export function raceFlags(c) {
  const f = { ['race_' + c.race]: true, ['origine_' + c.origin]: true };
  if (c.implant) f.implant = true;
  return f;
}
