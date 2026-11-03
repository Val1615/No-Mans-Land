// Steel Arena (zone steel_arena, 96 x 64 m, quartier de Center-Town). Pack d'Ocre : docs/villes/steel/quartiers/steel_arena/ (STEEL_ARENA.md, ASSETS.md, compléments 1 et 2).
// [décision] entrée ouest par la grille du bout est du Fréquence Strip (aller-retour) ; le parvis se visite, l'enceinte reste fermée (réplique au clic).
// Vibes et Tron n'apparaissent que sur les écrans géants dessinés par le code (pages tournantes). Aucun nom civil.
// Enceinte (moitié nord, x 4 à 92, z 0 à 30) : façades courbes de 28 m d'Ocre bord à bord, entrée à portiques au milieu, angle sud-est, façade est.
// Animations au code (anime_par_code du manifeste) : faisceaux des 4 pylônes, écrans géants et fronton (pages), file qui avance aux portiques ; hors plafond mobile de 8.
// Planches peintes restantes : guichet, Human Corp, un cœur dans la file (les 4 ar_ens_faisceau, Vibes, Tron et le fronton peints sont retirés).
export const ARENA_TAILLE_PROPOSEE = { w: 96, d: 64 }; // proposé à la préparation, appliqué au lot construction
const ARENA = { bg: '#060a10', hemi: ['#7a90ff', '#1a1030', 1.2], sun: ['#5fd3f0', 0.6], tint: '#a0a8d0', actor: '#d8dcf0' };
const VIOLET = '#8a3cff', CYAN = '#5fd3f0', MAGENTA = '#e03ca8', BLANC = '#e8eef2', ROUGE = '#c8323c';
const B = (id, label, sprite, x, z, w, d, extra = {}) => ({ id, label, sprite, x, z, w, d, visitable: false, cue: null, named: !!label, ...extra });
const ENS = (id, sprite, x, z, y, extra = {}) => B(id, '', sprite, x - 0.1, z - 0.1, 0.2, 0.2, { y, solid: [], named: false, ...extra });
const AP = (id, sprite, ax, az, w, d, extra = {}) => B(id, '', sprite, ax - w, az - d, w, d, { named: false, ...extra }); // posé par son ancre (coin avant)
// écrans géants et fronton : pages tournantes dessinées par le code dans ecran_coins / fronton_coins, comme le Feed de Pulse Plaza
const BATTLE = [
  { fond: ['#2a0c4a', '#6a24b0'], image: 'ar_ens_ecran_vibes', crop: [0, 0, 256, 144], titre: 'GROOVY VIBES', sous: 'Battle du 31 · côté gauche', bandeau: 'Votez avec vos applaudissements. Ils sont mesurés.' },
  { fond: ['#061a2a', '#1a6a9a'], image: 'ar_ens_ecran_tron', crop: [0, 0, 256, 144], titre: 'GROOVY-TRON', sous: 'Battle du 31 · côté droit', bandeau: 'Statut : invaincu. Statut : mis à jour.' },
  { fond: ['#300818', '#a0203a'], titre: 'ROUND 3', sous: 'Vibes 48 % · Tron 52 %', bandeau: 'Le public décide. Human Corp arbitre.' },
  { fond: ['#101018', '#3a3a5a'], titre: 'PULSE OF STEEL', sous: 'Festival · 14/11 · complet', bandeau: 'Human Corp sponsorise le sourire.' },
];
const FRONTON = [ { fond: ['#0a0a14', '#20204a'], titre: 'STEEL ARENA', sous: 'Live tonight', bandeau: 'Portiques ouverts' },
  { fond: ['#2a0c4a', '#5a1c9a'], titre: 'VIBES × TRON', sous: 'Battle du 31', bandeau: 'Billet, implant, sourire' } ];
const PYL = [[10, 40], [86, 40], [24, 58], [72, 58]], LAMP = [[4, 34], [92, 34], [36, 60], [60, 60]];
export const BUILDINGS_ARENA = [
  // enceinte : façade est, segments sud d'ouest en est, angle, écrans (ordre conseillé par Ocre)
  AP('ar_f_est', 'ar_facade_courbe_z', 92, 22, 1, 16, { solid: [{ x: 91, z: 0, w: 1, d: 22 }] }),
  AP('ar_f_s0', 'ar_facade_courbe_x', 20, 30, 16, 1), AP('ar_f_s1', 'ar_facade_courbe_x', 36, 30, 16, 1),
  AP('ar_entree', 'ar_facade_entree', 52, 30, 16, 1, { label: 'Entrée de l\u2019Arena', named: true, ecran: { coins: [[135, 1026], [627, 1189], [627, 1291], [135, 1128]], periode: 7, marque: 'STEEL ARENA', pages: FRONTON } }),
  AP('ar_f_s2', 'ar_facade_courbe_x', 68, 30, 16, 1), AP('ar_f_s3', 'ar_facade_courbe_x', 84, 30, 16, 1),
  B('ar_f_angle', '', 'ar_facade_angle', 84, 22, 8, 8, { named: false, ancre: [-8, 0] }), // ancre au raccord sud (84 ; 30), emprise x 84-92 z 22-30
  AP('ar_ecran_s', 'ar_ecran_geant_x', 18, 30.8, 12, 0.5, { solid: [], ecran: { periode: 9, marque: 'ARENA LIVE', pages: BATTLE } }),
  AP('ar_ecran_e', 'ar_ecran_geant_z', 92.8, 19, 0.5, 10, { solid: [], ecran: { periode: 11, decale: 1, marque: 'ARENA LIVE', pages: BATTLE } }),
  // masse de l'enceinte : le dôme d'origine derrière les façades (caché : les façades de 28 m le dépassent) ; bloque tout l'arrière
  B('ar_arena', 'Steel Arena', 'ar_arena', 24, 4, 48, 12, { tint: '#ffffff', solid: [{ x: 0, z: 0, w: 96, d: 29 }] }),
  // parvis : serpentin de file devant l'entrée (ouvert en bout alterné), portiques peints sur l'entrée
  B('ar_bar_l1', '', 'ar_barriere_file', 36, 34, 4, 0.4, { named: false }), B('ar_bar_l2', '', 'ar_barriere_file', 40, 34, 4, 0.4, { named: false }), B('ar_bar_l3', '', 'ar_barriere_file', 44, 34, 4, 0.4, { named: false }),
  B('ar_bar_m1', '', 'ar_barriere_file', 40, 37, 4, 0.4, { named: false }), B('ar_bar_m2', '', 'ar_barriere_file', 44, 37, 4, 0.4, { named: false }), B('ar_bar_m3', '', 'ar_barriere_file', 48, 37, 4, 0.4, { named: false }),
  B('ar_bar_s1', '', 'ar_barriere_file', 36, 40, 4, 0.4, { named: false }), B('ar_bar_s2', '', 'ar_barriere_file', 40, 40, 4, 0.4, { named: false }), B('ar_bar_s3', '', 'ar_barriere_file', 44, 40, 4, 0.4, { named: false }),
  B('ar_bar_e', '', 'ar_barriere_file_o', 51.6, 33, 0.4, 4, { named: false }), B('ar_bar_o', '', 'ar_barriere_file_o', 36, 36, 0.4, 4, { named: false }),
  B('ar_merch_b', 'Merch officiel', 'ar_stand_merch_b', 27, 40, 3, 2), B('ar_merch_c', 'Chariot de merch', 'ar_stand_merch_c', 55, 40, 3, 2),
  B('ar_truck_n', 'Nouilles du parvis', 'ar_foodtruck_nouilles', 16, 47.5, 6, 2.5), B('ar_truck_b', 'Boissons', 'ar_foodtruck_boissons', 68, 47.5, 6, 2.5),
  ...PYL.map(([x, z], i) => AP(`ar_pyl${i}`, 'ar_pylone_projecteur', x + 0.75, z + 0.75, 1.5, 1.5)),
  ...LAMP.map(([x, z], i) => B(`ar_lamp${i}`, '', 'ar_lampadaire', x - 0.3, z - 0.3, 0.6, 0.6, { named: false })),
  B('ar_guichets', 'Guichets', 'ar_guichets', 6, 44, 4, 4),
  B('ar_securite', 'Poste Human Corp', 'ar_securite', 14, 52, 4, 4),
  B('ar_regie', 'Camion régie', 'ar_regie', 78, 50, 6, 4),
  B('ar_panneau', 'Panneau', 'ar_panneau_nml', 90, 60, 2, 0.5),
  B('ar_cam', '', 'pp_camera', 33.8, 31.8, 0.4, 0.4, { named: false }),
  // planches peintes restantes : Human Corp, guichet, cœurs de la file (un seul animé)
  ENS('ar_e_hc', 'ar_ens_human_corp', 17.6, 56.2, 2.6), ENS('ar_e_guichet', 'ar_ens_guichet', 9.6, 48.2, 2.0),
  ...[[35.4, 40.8], [35.4, 33.6]].map(([x, z], i) => ENS(`ar_e_coeur${i}`, 'ar_ens_coeurs', x, z, 1.5, { fige: i > 0, ph: 0 })), // aux bouts ouest du serpentin, hors de la file
];
export const CLOSED_ARENA = {
  ar_arena: 'Le dôme de la Steel Arena. « Live tonight. » Une basse sourde fait vibrer les barrières. Les portes ne s\u2019ouvrent pas pour toi ce soir.',
  ar_entree: 'L\u2019entrée vitrée et ses six portiques blancs de Human Corp. « Building a better tomorrow. » Derrière, une clameur monte et s\u2019arrête net.',
  ar_guichets: 'Les guichets. L\u2019écran annonce le Festival Pulse of Steel, le 14/11. Complet.',
  ar_merch_b: 'Merch officiel Human Corp. Les prix s\u2019affichent selon ton score d\u2019engagement.',
  ar_merch_c: 'Un chariot de merch qui roule là où va la file. Les t-shirts sont unis : le motif se télécharge après paiement.',
  ar_truck_n: 'Nouilles du parvis. Le bouillon a le goût de la file : long, tiède, et on y revient.',
  ar_truck_b: 'Boissons. « Hydratation sponsorisée. » La paille est en option, le logo non.',
  ar_securite: 'Le poste de sécurité Human Corp. Une vitre teintée qui te regarde.',
  ar_regie: 'Le camion régie. Des câbles partent vers le dôme comme des racines.',
  ar_panneau: '« Au-delà de ce point : pas de droits, pas de loi, pas de retour. »',
};
// sol : grandes dalles usées partout ; marquages de file et grilles d'évacuation peints dans le sol (ground.decals)
const MARQ = [...[39, 43, 47].map(x => [x, 32.4]), ...[39, 43, 47].map(x => [x, 35.7]), ...[39, 43, 47].map(x => [x, 38.7])].map(([x, z]) => ({ image: 'ar_marquage_file', x, z, a: 0.8 }));
const GRILLES = [[30, 36], [58, 36], [30, 48], [44, 46], [58, 48], [12, 38], [80, 38], [44, 58], [20, 31.4], [68, 31.4]].map(([x, z]) => ({ image: 'ar_grille_evacuation', x, z }));
export const LOCATIONS_ARENA = {
  steel_arena: { id: 'steel_arena', name: 'Steel-Megalopolis · Steel Arena', kind: 'exterior', size: { ...ARENA_TAILLE_PROPOSEE }, light: ARENA,
    ground: { base: '#10121a', skin: 'g_ar_dalles_usees', tileM: 10.24, clean: true, decals: [...MARQ, ...GRILLES], zones: [] },
    buildings: BUILDINGS_ARENA, props: [],
    glows: [
      { x: 44, z: 31.6, rx: 7, rz: 2, color: BLANC, i: 0.5 }, { x: 44, z: 36.5, rx: 9, rz: 5, color: CYAN, i: 0.3 },
      { x: 12, z: 32, rx: 7, rz: 2.4, color: VIOLET, i: 0.6, flicker: true }, { x: 93.5, z: 14, rx: 2, rz: 6, color: CYAN, i: 0.5, flicker: true },
      ...PYL.map(([x, z]) => ({ x, z: z + 1.2, rx: 2.6, rz: 1.6, color: CYAN, i: 0.55, flicker: true })),
      ...LAMP.map(([x, z]) => ({ x, z: z + 0.6, rx: 2.4, rz: 1.8, color: VIOLET, i: 0.6 })),
      { x: 44, z: 36, rx: 3, rz: 3, color: MAGENTA, i: 0.35, flicker: true }, { x: 16, z: 56.6, rx: 2.2, rz: 1.2, color: BLANC, i: 0.5 },
      { x: 19, z: 50.6, rx: 3.2, rz: 1.4, color: ROUGE, i: 0.4 }, { x: 71, z: 50.6, rx: 3.2, rz: 1.4, color: CYAN, i: 0.4 },
      { x: 34, z: 32.4, rx: 0.6, rz: 0.4, color: ROUGE, i: 0.5 }, { x: 91, z: 61, rx: 2, rz: 1.4, color: ROUGE, i: 0.3 } ],
    // projecteurs : les 4 pylônes tirent leur faisceau depuis source_faisceau_px (automatique) ; ici seulement le réglage (balayage lent décalé, vers le ciel au-dessus du dôme)
    projecteurs: PYL.map((_, i) => ({ building: `ar_pyl${i}`, couleur: CYAN, longueur: 42, ouverture: 3.5, inclinaison: 28, cap: [24, -24, 10, -10][i], balayage: 26,
      periode: [17, 19, 23, 21][i], decale: [0, 6, 11, 3][i], intensite: 0.2 })),
    // figurants : 4 fans d'Ocre (deux dans la file, un qui fait signe près des food trucks, un bras croisés au pied d'un pylône) ; la file qui avance = passants en aller simple
    extras: [ { sprite: 'gen_ar_fan_chignons', x: 40.4, z: 37.9, face: 1, role: 'fan' }, { sprite: 'gen_ar_techwear', x: 46, z: 34.8, face: -1, role: 'fan' },
      { sprite: 'gen_ar_manteau', x: 62, z: 48, face: -1, role: 'fan' }, { sprite: 'gen_ar_cuir', x: 25.6, z: 56.4, face: 1, role: 'fan' } ],
    walkers: [ ...[0, 9, 18, 27, 36].map((t0, i) => ({ sprite: i % 2 ? 'gen_ar_foule_b' : 'gen_ar_foule_a', path: [[50, 46], [50, 38.4], [38, 38.4], [38, 35.4], [49.4, 35.4], [49.4, 32.8], [44, 32.8]], speed: 0.3, t0, aller: true, role: 'file' })),
      { sprite: 'gen_ar_foule_a', path: [[3, 61], [46, 61]], speed: 0.6, t0: 3 }, { sprite: 'gen_ar_foule_b', path: [[93, 62.4], [50, 62.4]], speed: 0.6, t0: 10 } ],
    spawn: { player: { x: 1, z: 44 }, companion: { x: 1, z: 45 } }, city: 'steel',
    arrive: { from: 'steel_strip', text: 'La Steel Arena. L\u2019enceinte noire mange tout le nord ; quatre faisceaux cyan balaient le plafond du sarcophage. « Human Corp sponsorise le sourire. »' } },
};
const J = (id, loc, ox, oz, tx, tz, to, label, conditions = []) => ({ id, location: loc, junction: true, label, opening: { x: ox, z: oz, side: 'edge' }, threshold: { x: tx, z: tz }, target: { doorId: to }, conditions });
export const DOORS_ARENA = [
  J('ar_ouest', 'steel_arena', 0, 44, 1, 44, 'fs_est', 'Fréquence Strip'),
  J('fs_est', 'steel_strip', 80, 13, 79, 13, 'ar_ouest', 'La grille de l\u2019Arena'),
];
export const NPCS_ARENA = [ // mêmes PNJ et dialogues, recalés sur le parvis agrandi ; aucun n'est Vibes ni Tron
  { id: 'ar_ferrand', name: 'Ferrand', sprite: 'gen_ar_ferrand', location: 'steel_arena', x: 53.4, z: 32.2, faceTo: [44, 34], dialogue: 'ar_ferrand' },
  { id: 'ar_anouk', name: 'Anouk', sprite: 'gen_ar_anouk', location: 'steel_arena', x: 8, z: 48.8, faceTo: [8, 52], dialogue: 'ar_anouk' },
  { id: 'ar_zelie', name: 'Zélie', sprite: 'gen_ar_zelie', location: 'steel_arena', x: 9, z: 52.4, faceTo: [14, 48], dialogue: 'ar_zelie' },
  { id: 'ar_malik', name: 'Malik', sprite: 'gen_ar_malik', location: 'steel_arena', x: 79, z: 55, faceTo: [74, 50], dialogue: 'ar_malik' },
  { id: 'ar_ines', name: 'Inès', sprite: 'gen_ar_ines', location: 'steel_arena', x: 39, z: 31.9, faceTo: [44, 31], dialogue: 'ar_ines' },
  { id: 'ar_clem', name: 'Clém', sprite: 'gen_ar_clem', location: 'steel_arena', x: 54.6, z: 43.4, faceTo: [50, 40], dialogue: 'ar_clem' },
  { id: 'ar_garnier', name: 'Agent Garnier', sprite: 'gen_ar_garnier', location: 'steel_arena', x: 19, z: 57, faceTo: [24, 54], dialogue: 'ar_garnier' },
  { id: 'ar_bastien', name: 'Bastien', sprite: 'gen_ar_bastien', location: 'steel_arena', x: 84.4, z: 42.4, faceTo: [86, 40], dialogue: 'ar_bastien' },
  { id: 'ar_laure', name: 'Madame Laure', sprite: 'gen_ar_laure', location: 'steel_arena', x: 89, z: 61.6, faceTo: [84, 58], dialogue: 'ar_laure' },
  // compléments d'Ocre : revendeurs de billets, hors du couloir des portiques
  { id: 'ar_revendeur', name: 'Le revendeur', sprite: 'gen_ar_revendeur', location: 'steel_arena', x: 33, z: 44, faceTo: [40, 40], dialogue: 'ar_revendeur' },
  { id: 'ar_revendeuse', name: 'La revendeuse', sprite: 'gen_ar_revendeuse', location: 'steel_arena', x: 60, z: 46.4, faceTo: [56, 42], dialogue: 'ar_revendeuse' },
];
const D = (t1, t2) => ({ start: { text: t1, options: [ { label: 'Et sinon ?', next: 'b' }, { label: 'Au revoir.', next: 'end' } ] }, b: { text: t2, options: [ { label: 'Au revoir.', next: 'end' } ] } });
const D1 = t1 => ({ start: { text: t1, options: [ { label: 'Au revoir.', next: 'end' } ] } });
export const DIALOGUES_ARENA = {
  ar_ferrand: D('Billet, implant, sourire. Dans cet ordre, s\u2019il vous plaît.', 'Vous n\u2019êtes pas dans la liste. Personne n\u2019est pas dans la liste. Reculez.'),
  ar_anouk: D('Ce soir c\u2019est complet. Demain aussi. Pour le Festival du 14, il reste des places debout derrière les places debout.', 'Le prix change selon votre score d\u2019engagement. Ne me demandez pas comment, c\u2019est l\u2019écran qui calcule.'),
  ar_zelie: D('Vrai billet, vraie puce, faux nom. Ça passe neuf fois sur dix. La dixième, tu cours.', 'Tu es grillé, toi. Je ne te connais pas.'),
  ar_malik: D('Trois mille personnes à l\u2019intérieur, et le show tient sur une seule console. Si elle plante, je deviens célèbre.', 'Les cris du public sont mixés, comme le reste. Ce soir, on en a ajouté vingt pour cent.'),
  ar_ines: D('Je n\u2019ai pas de billet. Je viens pour la file. Ici, au moins, on est ensemble.', 'Personne ne sait qui elle est sous le chapeau. Moi je dis qu\u2019elle est comme nous, et qu\u2019elle a juste eu de la chance. Ou pas.'),
  ar_clem: D('Je fais le direct de la file. Les gens adorent regarder d\u2019autres gens attendre.', 'On m\u2019a demandé de ne pas filmer le panneau du fond. Alors évidemment, tout le monde le filme.'),
  ar_garnier: D('Ici c\u2019est Human Corp qui garde la porte. Nous, on garde ceux qui restent dehors.', 'Le panneau là-bas ? Une blague de mauvais goût. Ou un avertissement. Je ne suis pas payé pour choisir.'),
  ar_bastien: D1('Quatre faisceaux, et ils doivent rester synchrones avec la musique. Le jour où ils se décalent, ça fait une prière ratée.'),
  ar_laure: D('J\u2019ai placé des gens ici pendant trente ans. Avant, on voyait les visages des chanteurs. Maintenant on voit les écrans.', 'Ce panneau était là avant l\u2019Arena. On a construit autour, et on n\u2019a jamais osé l\u2019enlever.'),
  ar_revendeur: D('Places debout, places assises, places imaginaires. Les dernières sont les moins chères.', 'Le billet est vrai. C\u2019est la date qui est approximative.'),
  ar_revendeuse: D('Tu veux entrer, ou tu veux pouvoir dire que tu étais là ? La deuxième option coûte moins cher.', 'Je ne rembourse pas. Les concerts non plus.'),
};
