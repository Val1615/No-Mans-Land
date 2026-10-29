// Pulse Plaza (zone steel_pulse, quartier de Center-Town). Pack d'Ocre : docs/villes/steel/quartiers/pulse_plaza/PULSE_PLAZA.md et ASSETS.md.
// [décision Valentin] zone à part, porte vers Center-Town (comme Lower-Town), sortie sud vers la grille c_sud. Groovy Vibes et Groovy-Tron
// n'apparaissent que sur les écrans et les médias (écran du feed, billboard, hologramme) : jamais rencontrés, aucun sosie qui parle.
// Le nom civil de Vibes n'apparaît nulle part. Sprites : placeholders d'Ocre (assets/steel/pulse_plaza/manifest.json), ancres provisoires.
// Plan [proposition d'Ocre] : 24 x 18 cases de 2 m ; x = 2 x colonne, z = 2 x rangée.
const PULSE = { bg: '#060a10', hemi: ['#b48cff', '#2b1a4a', 1.3], sun: ['#a9d2e6', 0.6], tint: '#a898d0', actor: '#d8d0f0' }; // nuit éclairée par les écrans
const VIOLET = '#8a3cff', MAGENTA = '#e03ca8', CYAN = '#a9d2e6', CHAUD = '#ffae55', ROUGE = '#c8323c';
const B = (id, label, sprite, x, z, w, d, extra = {}) => ({ id, label, sprite, x, z, w, d, visitable: false, cue: null, named: !!label, ...extra });
const CAMS = [[9, 7], [35, 7], [17, 25], [35, 25]];
export const BUILDINGS_PULSE = [
  B('pp_arcadius', 'Arcadius Center', 'pp_arcadius', 12, 0, 24, 4, { tint: '#ffffff' }),
  B('pp_portique', 'Portique IO', 'pp_portique', 20, 4, 4, 2),
  B('pp_ecran_feed', 'Écran du Feed 24/7', 'pp_ecran_feed', 12, 8, 20, 4, { sign: true }),
  B('pp_holo', 'Projection Holo-Tron', 'pp_holo_socle', 20, 14, 8, 8),
  B('pp_holo_tron', '', 'pp_holo_tron', 23.7, 17.7, 0.6, 0.6, { solid: [], named: false }),
  B('pp_billboard', 'Billboard HCM-88X', 'pp_billboard', 0, 6, 4, 6),
  B('pp_kiosque', 'Kiosque merch officiel', 'pp_kiosque', 44, 6, 4, 6),
  B('pp_guerite', 'Guérite SMPD', 'pp_guerite', 0, 24, 4, 6),
  B('pp_nouilles', 'Stand de nouilles', 'pp_nouilles', 44, 24, 4, 6),
  B('pp_distrib', 'Distributeur « sourire calibré »', 'pp_distrib', 40, 20, 2, 2),
  B('pp_banc1', '', 'pp_banc', 4, 20, 2, 1, { named: false }), B('pp_banc2', '', 'pp_banc', 4, 23, 2, 1, { named: false }),
  ...CAMS.map(([x, z], i) => B(`pp_cam${i}`, '', 'pp_camera', x - 0.2, z - 0.2, 0.4, 0.4, { named: false })),
  B('pp_escalier', 'Escalier de service', 'pp_escalier', 22, 28, 4, 4, { solid: [] }),
];
export const CLOSED_PULSE = { // textes des écrans et façades (aucun nom civil)
  pp_arcadius: 'L\u2019Arcadius Center. Verre noir, structure blanche, le logo d\u2019IO. L\u2019entrée est gardée et ne s\u2019ouvre pas pour toi.',
  pp_portique: 'Le portique d\u2019IO. Il lit les implants de ceux qui passent. Le tien, il le lit un peu trop longtemps.',
  pp_ecran_feed: '« L\u2019idole démasquée. Qui est vraiment Groovy Vibes ? » Puis le bandeau : « 100% connection stable. Jusqu\u2019à la prochaine alerte. » Puis « Audience sync » : la place applaudit d\u2019un seul coup, et s\u2019arrête net.',
  pp_holo: 'Groovy-Tron, en hologramme à taille double, tourne lentement sur son socle chromé. C\u2019est une image. Il ne te voit pas.',
  pp_billboard: 'Billboard HCM-88X. Groovy Vibes, sourire figé : « Status : Optimum. Le sourire est une mise à jour. »',
  pp_guerite: 'La guérite du SMPD. Une vitre, une lampe, et quelqu\u2019un derrière qui te regarde déjà.',
  pp_distrib: 'Une borne violette : passes pour la soirée Next Drop du Club Neon-7. Paiement en crédits, sourire conseillé.',
  pp_kiosque: 'Kiosque Human Corp : casquette pixel, stickers holo, pack EXE, poster Error 404.',
  pp_nouilles: 'Le stand de l\u2019oncle Pham. Le seul coin de la place sans écran.',
};
export const LOCATIONS_PULSE = {
  steel_pulse: { id: 'steel_pulse', name: 'Steel-Megalopolis · Pulse Plaza', kind: 'exterior', size: { w: 48, d: 36 }, light: PULSE,
    ground: { base: '#141826', skin: 'g_pp_dalle_mouillee', tileM: 4, clean: true, zones: [ { x: 20, z: 30, w: 8, d: 6, kind: 'plate', tint: 'rgba(10,12,22,.55)' } ] },
    buildings: BUILDINGS_PULSE, props: [],
    glows: [ // l'écran et les médias du groupe en violet et magenta ; IO en blanc froid ; le stand de nouilles en chaud ; caméras en rouge discret
      { x: 22, z: 13, rx: 11, rz: 4, color: VIOLET, i: 0.95, flicker: true }, { x: 22, z: 13.5, rx: 6, rz: 2.4, color: MAGENTA, i: 0.6, flicker: true },
      { x: 24, z: 18, rx: 4.5, rz: 4.5, color: CYAN, i: 0.7, flicker: true }, { x: 2, z: 12.5, rx: 2.6, rz: 2, color: MAGENTA, i: 0.75 },
      { x: 46, z: 12.5, rx: 2.4, rz: 1.8, color: VIOLET, i: 0.7 }, { x: 41, z: 22.6, rx: 1.6, rz: 1.2, color: VIOLET, i: 0.7, flicker: true },
      { x: 24, z: 5, rx: 6, rz: 1.6, color: '#e8eef2', i: 0.5 }, { x: 46, z: 30.5, rx: 2.6, rz: 1.8, color: CHAUD, i: 0.7 }, { x: 2, z: 30.5, rx: 2, rz: 1.4, color: '#e8eef2', i: 0.45 },
      ...CAMS.map(([x, z]) => ({ x, z: z + 0.4, rx: 0.6, rz: 0.4, color: ROUGE, i: 0.5 })) ],
    extras: [ ...[[15, 14.5], [17.5, 15.2], [19, 13.6], [27, 13.8], [29, 15], [31, 14.2], [14, 16.6], [30.5, 16.8], [26, 23.4], [18, 23.2]].map(([x, z], i) => ({ sprite: i % 2 ? 'gen_pp_foule_b' : 'gen_pp_foule_a', x, z, face: x < 24 ? 1 : -1, role: 'foule' })) ],
    walkers: [ { sprite: 'gen_pp_foule_a', path: [[2, 15], [46, 15]], speed: 0.7, t0: 4 }, { sprite: 'gen_pp_foule_b', path: [[8, 33], [8, 27], [40, 27]], speed: 0.6, t0: 11 } ],
    spawn: { player: { x: 1, z: 16 }, companion: { x: 1, z: 17 } }, city: 'steel',
    arrive: { from: 'steel_center', text: 'Pulse Plaza. Les écrans éclairent tout ; la nuit n\u2019a plus le droit de tomber ici. La foule applaudit en même temps, puis se tait en même temps.' } },
};
const J = (id, loc, ox, oz, tx, tz, to, label, conditions = []) => ({ id, location: loc, junction: true, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: { doorId: to }, conditions });
export const DOORS_PULSE = [
  J('pp_ouest', 'steel_pulse', 0, 16, 1, 16, 'c_nord', 'Vers Center-Town (rue d\u2019arrivée)'),
  J('pp_sud', 'steel_pulse', 24, 36, 24, 35, 'c_pp_sud', 'Escalier de service (vers Center-Town)'),
  J('c_pp_sud', 'steel_center', 26, 36, 26, 35, 'pp_sud', 'Escalier de Pulse Plaza'), // [décision Valentin] distincte de la grille c_sud (Sous-Ville), sans condition
  J('c_nord', 'steel_center', 33, 0, 33, 1, 'pp_ouest', 'Pulse Plaza'),
];
export const NPCS_PULSE = [ // positions de la fiche (x, z en m) ; aucun n'est Vibes ni Tron
  { id: 'pp_maelle', name: 'Maëlle', sprite: 'gen_pp_maelle', location: 'steel_pulse', x: 16, z: 13.4, faceTo: [22, 10], dialogue: 'pp_maelle' },
  { id: 'pp_dorian', name: 'Dorian', sprite: 'gen_pp_dorian', location: 'steel_pulse', x: 42.8, z: 9, faceTo: [36, 9], dialogue: 'pp_dorian' },
  { id: 'pp_brisset', name: 'Agente Brisset', sprite: 'gen_pp_brisset', location: 'steel_pulse', x: 5, z: 27, faceTo: [12, 27], dialogue: 'pp_brisset' },
  { id: 'pp_pham', name: 'Oncle Pham', sprite: 'gen_pp_pham', location: 'steel_pulse', x: 42.8, z: 27, faceTo: [36, 27], dialogue: 'pp_pham' },
  { id: 'pp_isaure', name: 'Isaure', sprite: 'gen_pp_isaure', location: 'steel_pulse', x: 24, z: 12.8, faceTo: [24, 18], dialogue: 'pp_isaure' },
  { id: 'pp_clone', name: 'Le Clone 7', sprite: 'gen_pp_clone_gt', location: 'steel_pulse', x: 19, z: 22.8, faceTo: [14, 24], dialogue: 'pp_clone' },
  { id: 'pp_gaspard', name: 'Gaspard', sprite: 'gen_pp_gaspard', location: 'steel_pulse', x: 7, z: 22, faceTo: [12, 22], dialogue: 'pp_gaspard' },
  { id: 'pp_noor', name: 'Noor', sprite: 'gen_pp_noor', location: 'steel_pulse', x: 27, z: 31, faceTo: [24, 31], dialogue: 'pp_noor' },
  { id: 'pp_vasseur', name: 'Monsieur Vasseur', sprite: 'gen_pp_vasseur', location: 'steel_pulse', x: 25.5, z: 7, faceTo: [22, 10], dialogue: 'pp_vasseur' },
];
// Répliques de la fiche d'Ocre. Les variantes (Repérage, clandestin) attendent le système de Repérage : proposées en option « Et sinon ? ».
const D = (t1, t2) => ({ start: { text: t1, options: [ { label: 'Et sinon ?', next: 'b' }, { label: 'Au revoir.', next: 'end' } ] }, b: { text: t2, options: [ { label: 'Au revoir.', next: 'end' } ] } });
export const DIALOGUES_PULSE = {
  pp_maelle: D('Tu l\u2019as vue hier, sur le feed ? Elle a regardé la caméra une demi-seconde de trop. Moi j\u2019appelle ça un message.', 'Personne ne sait qui elle est vraiment. Et franchement, je préfère. Si on savait, elle serait comme nous.'),
  pp_dorian: D('Pack EXE, la clé chrome est vide, mais c\u2019est la vraie. C\u2019est écrit sur la boîte.', 'Le poster Error 404 part mieux que tout le reste. Les gens aiment bien qu\u2019on leur dise qu\u2019ils sont introuvables.'),
  pp_brisset: D('Implant, s\u2019il vous plaît. Simple routine. Ici, tout est simple routine.', 'Ne restez pas sur la place trop longtemps, d\u2019accord ?'),
  pp_pham: D('Assieds-toi de ce côté. La caméra du coin voit tout sauf mes casseroles.', 'Moi, la musique, je ne l\u2019entends plus. Je ne remarque que quand elle s\u2019arrête. Là, je regarde l\u2019écran.'),
  pp_isaure: D('L\u2019audience sync, c\u2019est un signal. Il part de l\u2019écran et les implants font le reste. Les mains suivent.', 'Tu crois qu\u2019ils applaudissent parce qu\u2019ils veulent ? Moi, ça fait trois ans que je ne pose plus la question.'),
  pp_clone: D('Bonsoir. Je suis un modèle de démonstration. On me pose ici pour que vous voyiez à quoi ressemble un modèle réussi.', 'Question non prévue. Je vous renvoie au refrain.'),
  pp_gaspard: D('Chaque semaine quelqu\u2019un jure avoir trouvé qui elle est. Chaque semaine le feed passe à autre chose. Drôle de hasard.', 'Si un jour tu entends son vrai nom, garde-le pour toi. Les gens qui le disent trop fort ne reviennent plus sur la place.'),
  pp_noor: D('Pas d\u2019implant, pas d\u2019applaudissement. Du coup on me regarde. C\u2019est bête, non ?', 'Si tu veux descendre sans passer devant la guérite, l\u2019escalier de service ne ferme jamais vraiment.'),
  pp_vasseur: D('Je travaille juste là. Non, je ne sais pas ce qu\u2019on y fait. Je sais seulement ce que je fais, moi.', 'L\u2019écran ? C\u2019est nous qui louons la place. Le groupe chante, nous on comptera les mains.'),
};
