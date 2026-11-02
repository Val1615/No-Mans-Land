// Pulse Plaza (zone steel_pulse, quartier de Center-Town). Pack d'Ocre : docs/villes/steel/quartiers/pulse_plaza/PULSE_PLAZA.md et ASSETS.md.
// [décision Valentin] zone à part, porte vers Center-Town (comme Lower-Town), sortie sud vers la grille c_sud. Groovy Vibes et Groovy-Tron
// n'apparaissent que sur les écrans et les médias (écran du feed, billboard, hologramme) : jamais rencontrés, aucun sosie qui parle.
// Le nom civil de Vibes n'apparaît nulle part. Sprites : placeholders d'Ocre (assets/steel/pulse_plaza/manifest.json), ancres provisoires.
// Plan [proposition d'Ocre] : 24 x 18 cases de 2 m ; x = 2 x colonne, z = 2 x rangée.
const PULSE = { bg: '#060a10', hemi: ['#b8a0f0', '#2e2034', 1.3], sun: ['#e6c8a8', 0.6], tint: '#b8aec4', actor: '#ddd4e8' }; // chantier pilote : moins violet, une pointe d'ambre // nuit éclairée par les écrans
const VIOLET = '#8a3cff', MAGENTA = '#e03ca8', CYAN = '#a9d2e6', CHAUD = '#ffae55', ROUGE = '#c8323c';
const B = (id, label, sprite, x, z, w, d, extra = {}) => ({ id, label, sprite, x, z, w, d, visitable: false, cue: null, named: !!label, ...extra });
const CAMS = [[9, 7], [35, 7], [17, 25], [35, 25]];
// [proposition d'Ocre, chantier pilote] façades : emprise (x, z, w, d) et options. L'ancre tombe sur le coin avant (x + w ; z + d).
// Nord (tableau de pose) : pp_facade_b x 0 à 8 puis x 4 à 12 (doublon), pp_facade_a x 36 à 48 contre l'Arcadius.
// Écart au tableau, mesuré en jeu : les variantes _o sont dessinées plus longues que leur emprise le long de z (pp_facade_b_o : environ 12 m pour 8 m ;
// pp_facade_a_o : environ 23,6 m pour 16 m). Posées aux coordonnées du tableau, elles couvriraient l'accès ouest (seuil 1 ; 16) et la jonction
// vers Fréquence Strip (seuil 47 ; 13). Ouest : pp_facade_b_o en quatre pièces, ancres en z 8, 15, 29 et 36 ; z 15 à 17 reste ouvert.
// Est : pp_facade_b_o ancrée en z 26 (dessinée de z 14 à 26), à la place de pp_facade_a_o qui masquerait le kiosque et la jonction ; solide de z 14 à 24 ;
// deux pièces de plus ferment les coins nord-est (derrière le kiosque) et sud-est (derrière le stand de nouilles).
const FACADES = [ // [id, sprite, x, z, w, d, options (solide, échelle)]
  ['pp_fac_n1', 'pp_facade_b', 0, 0, 8, 1.5], ['pp_fac_n2', 'pp_facade_b', 4, 0, 8, 1.5], ['pp_fac_n3', 'pp_facade_a', 36, 0, 12, 2],
  ['pp_fac_o1', 'pp_facade_b_o', 0, 0, 1.5, 8], ['pp_fac_o2', 'pp_facade_b_o', 0, 7, 1.5, 8], ['pp_fac_o3', 'pp_facade_b_o', 0, 21, 1.5, 8, { solid: [{ x: 0, z: 17, w: 1.5, d: 12 }] }], ['pp_fac_o4', 'pp_facade_b_o', 0, 28, 1.5, 8],
  ['pp_fac_e1', 'pp_facade_b_o', 46.5, 18, 1.5, 8, { solid: [{ x: 46.5, z: 14, w: 1.5, d: 10 }] }],
  ['pp_fac_e0', 'pp_facade_b_o', 46.5, -2, 1.5, 8, { solid: [{ x: 46.5, z: 2, w: 1.5, d: 4 }] }],
  ['pp_fac_e2', 'pp_facade_b_o', 46.5, 30, 1.5, 6, { k: 0.5 }], // coins nord-est (z 2 à 6) et sud-est (z 30 à 36) ; au sud-est, échelle 0,5 par le code (6 m dessinés) pour ne pas masquer le stand de nouilles
];
// mobilier : [id, sprite, x de l'ancre, z de l'ancre, w, d] (emprises du manifeste)
// pied des façades et des stands (x, z, w, d) : transition entre le sol et les bâtiments
const PIEDS = [[0, 1.5, 12, 1], [12, 4, 8, 0.8], [24, 4, 12, 0.8], [36, 2, 12, 1], [1.5, 1.5, 0.8, 13.5], [1.5, 17, 0.8, 7], [1.5, 30, 0.8, 6], [45.7, 14, 0.8, 10], [44, 12, 4, 0.6], [0, 12, 4, 0.6], [0, 30, 4, 0.6], [44, 30, 4, 0.6]];
const LAMPES = [[8, 14], [8, 26], [40, 14], [36, 31]], BORNES = [[11, 11], [33, 11]];
const MOBILIER = [
  ...LAMPES.map(([x, z], i) => [`pp_lampe${i}`, 'pp_lampadaire', x, z, 0.6, 0.6]),
  ...[[13, 19], [15, 25], [33, 25]].map(([x, z], i) => [`pp_statue${i}`, 'pp_statue', x, z, 2, 2]),
  ...BORNES.map(([x, z], i) => [`pp_borne${i}`, 'pp_borne_neon', x, z, 0.5, 0.5]),
  ...[[4, 21.5], [40, 24]].map(([x, z], i) => [`pp_jard${i}`, 'pp_jardiniere', x, z, 1.6, 1.6]),
];
// Écran du Feed : l'image d'Ocre est un écran vierge (« contenu animé par le code », ASSETS.md). Le code dessine le contenu dans la dalle
// de l'image (coins en px de la source : haut gauche, haut droit, bas droit, bas gauche) ; une page toutes les `periode` secondes, sans planche animée.
const ECRAN_FEED = { coins: [[247, 52], [712, 264], [712, 562], [247, 350]], periode: 9, pages: [
  { fond: ['#3a1470', '#7a2cc8'], image: 'pp_billboard', crop: [40, 175, 128, 240], titre: 'GROOVY VIBES', sous: 'Clip officiel · Feed 24/7', bandeau: '100% connection stable. Jusqu\u2019à la prochaine alerte.' },
  { fond: ['#200a40', '#5a1c9a'], titre: 'L\u2019IDOLE DÉMASQUÉE', sous: 'Qui est vraiment Groovy Vibes ?', bandeau: '100% connection stable. Jusqu\u2019à la prochaine alerte.' },
  { fond: ['#081a2c', '#2a5a8a'], image: 'pp_holo_tron', crop: [0, 0, 81, 180], titre: 'GROOVY-TRON.EXE', sous: 'Démarrage…', bandeau: 'Status : Optimum. Le sourire est une mise à jour.' },
  { fond: ['#3a0a2a', '#b02a7a'], titre: 'AUDIENCE SYNC', sous: 'Applaudissez maintenant', bandeau: '100% connection stable. Jusqu\u2019à la prochaine alerte.' },
] };
export const BUILDINGS_PULSE = [
  B('pp_arcadius', 'Arcadius Center', 'pp_arcadius', 12, 0, 24, 4, { tint: '#ffffff' }),
  B('pp_portique', 'Portique IO', 'pp_portique', 20, 4, 4, 2),
  B('pp_ecran_feed', 'Écran du Feed 24/7', 'pp_ecran_feed', 12, 8, 20, 4, { sign: true, ecran: ECRAN_FEED }),
  B('pp_holo', 'Projection Holo-Tron', 'pp_holo_socle', 20, 14, 8, 8),
  B('pp_holo_tron', '', 'pp_holo_tron', 23.7, 17.7, 0.6, 0.6, { solid: [], named: false, cover: true /* cover : dessiné par-dessus le socle ; 81 x 180 à la source, ancre au pied [40, 179] (height_m 3,6, fedd3e3), plus d'échelle en code ; transparence de l'image seule */ }),
  B('pp_billboard', 'Billboard HCM-88X', 'pp_billboard', 0, 6, 4, 6),
  B('pp_kiosque', 'Kiosque merch officiel', 'pp_kiosque', 44, 6, 4, 6),
  B('pp_guerite', 'Guérite SMPD', 'pp_guerite', 0, 24, 4, 6),
  B('pp_nouilles', 'Stand de nouilles', 'pp_nouilles', 44, 24, 4, 6),
  B('pp_distrib', 'Distributeur « sourire calibré »', 'pp_distrib', 40, 20, 2, 2),
  B('pp_banc1', '', 'pp_banc', 4, 20, 2, 1, { named: false }), B('pp_banc2', '', 'pp_banc', 4, 23, 2, 1, { named: false }),
  ...CAMS.map(([x, z], i) => B(`pp_cam${i}`, '', 'pp_camera', x - 0.2, z - 0.2, 0.4, 0.4, { named: false })),
  B('pp_escalier', '', 'pp_escalier', 22, 28, 4, 4, { solid: [], named: false }), // chantier pilote : plus d'étiquette posée sur l'accès
  // Chantier pilote (docs/villes/steel/quartiers/pulse_plaza/PILOTE.md) : façades raccordables qui ferment les bords nord, ouest et est.
  // Emprise (x, z, w, d) = celle du tableau de pose ; l'ancre du sprite tombe sur le coin avant (x + w ; z + d), comme tous les bâtiments.
  ...FACADES.map(([id, sprite, x, z, w, d, extra = {}]) => B(id, '', sprite, x, z, w, d, { named: false, ...extra })),
  // mobilier et sources de lumière : l'ancre (pied) est posée sur le point du tableau ; le halo du code est centré sur ce même point
  ...MOBILIER.map(([id, sprite, ax, az, w, d]) => B(id, '', sprite, ax - w, az - d, w, d, { named: false })),
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
    // chantier pilote : dalle sombre de base ; la dalle mouillée reste en zones (devant l'écran et le Holo, où la lumière se reflète) ;
    // transitions sol / bâtiments : bande de grille assombrie au pied des façades et des stands ; allées en dalle d'allée (ground.paint, format de l'éditeur de cartes)
    ground: { base: '#141826', skin: 'g_pp_dalle_sombre', tileM: 4, clean: true, zones: [
      { x: 20, z: 30, w: 8, d: 6, kind: 'plate', tint: 'rgba(10,12,22,.55)' },
      { x: 12, z: 12, w: 20, d: 2, kind: 'wet', skin: 'g_pp_dalle_mouillee', tint: 'rgba(10,10,20,.35)' }, { x: 19, z: 22, w: 10, d: 1.5, kind: 'wet', skin: 'g_pp_dalle_mouillee', tint: 'rgba(10,10,20,.35)' },
      ...PIEDS.map(([x, z, w, d]) => ({ x, z, w, d, kind: 'plate', skin: 'g_pp_grille', tint: 'rgba(6,6,12,.55)' })) ],
      paint: [ { x: 22, z: 4, w: 4, d: 24, skin: 'g_pp_allee' }, { x: 0, z: 15, w: 22, d: 2, skin: 'g_pp_allee' }, { x: 26, z: 15, w: 22, d: 2, skin: 'g_pp_allee' } ] },
    accessLabels: false, // chantier pilote : aucune étiquette ni écran posés sur les accès (les anneaux de seuil restent)
    buildings: BUILDINGS_PULSE, props: [],
    glows: [ // chaque halo a sa source : l'écran du Feed, le Holo, le billboard, le kiosque, le distributeur, le portique, le stand, la guérite, les caméras,
      // les lampadaires (cyan) et les bornes (magenta) centrés sur leur ancre ; ambres chaudes : vitrines éclairées au pied des façades et stand de nouilles
      { x: 22, z: 13, rx: 11, rz: 4, color: VIOLET, i: 0.85, flicker: true }, { x: 22, z: 13.5, rx: 6, rz: 2.4, color: MAGENTA, i: 0.5, flicker: true },
      { x: 24, z: 18, rx: 4.5, rz: 4.5, color: CYAN, i: 0.6, flicker: true }, { x: 2, z: 12.5, rx: 2.6, rz: 2, color: MAGENTA, i: 0.65 },
      { x: 46, z: 12.5, rx: 2.4, rz: 1.8, color: VIOLET, i: 0.6 }, { x: 41, z: 22.6, rx: 1.6, rz: 1.2, color: VIOLET, i: 0.6, flicker: true },
      { x: 22, z: 6.3, rx: 3, rz: 1.2, color: '#e8eef2', i: 0.45 }, { x: 46, z: 30.5, rx: 2.6, rz: 1.8, color: CHAUD, i: 0.8 }, { x: 2, z: 30.5, rx: 2, rz: 1.4, color: '#e8eef2', i: 0.4 },
      ...CAMS.map(([x, z]) => ({ x: x + 0.2, z: z + 0.2, rx: 0.6, rz: 0.4, color: ROUGE, i: 0.5 })),
      ...LAMPES.map(([x, z]) => ({ x, z, rx: 2.2, rz: 1.6, color: CYAN, i: 0.55 })), ...BORNES.map(([x, z]) => ({ x, z, rx: 1.3, rz: 1, color: MAGENTA, i: 0.6, flicker: true })),
      ...[[3, 3], [7, 3], [11, 3], [38.5, 3.6], [42.5, 3.6], [46, 3.6], [3, 4.5], [3, 10], [3, 20], [3, 23], [3, 33], [45, 17], [45, 21]].map(([x, z]) => ({ x, z, rx: 1.6, rz: 1.1, color: CHAUD, i: 0.45 })) ],
    // chantier pilote : 8 figurants distincts (gen_pp_foule_c à j) à la place des clones, groupés devant l'écran et autour du Holo ; foule_a et foule_b ne servent plus qu'aux deux passants
    extras: [ ...[['c', 15, 14.5], ['d', 19, 13.6], ['e', 29, 15], ['f', 14, 16.6], ['g', 26, 23.4], ['h', 18, 23.2], ['i', 30.5, 16.8], ['j', 27, 13.8]].map(([k, x, z]) => ({ sprite: 'gen_pp_foule_' + k, x, z, face: x < 24 ? 1 : -1, role: 'foule' })) ],
    walkers: [ { sprite: 'gen_pp_foule_a', path: [[2, 16], [46, 16]], speed: 0.7, t0: 4 }, { sprite: 'gen_pp_foule_b', path: [[8, 33], [8, 27], [40, 27]], speed: 0.6, t0: 11 } ],
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
