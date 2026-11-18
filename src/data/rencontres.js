// Rencontres aléatoires des No Man's Land (jalon 1) : catalogue au format de docs/rencontres/ARCHI.md §4.
// Pilote « L'appât de la piste » d'après docs/rencontres/PILOTE.md (Ocre, 2b2013c + e964aa1) : plan 30 × 24 m, poses du §15, dialogues du §6,
// combat du §8, butin du §9. Gestionnaire : src/core/rencontres.js. Les taux de TERRAINS (data/nml.js) ne sont pas touchés.
// Repère de la scène : x vers l'est, z vers le sud, mètres, origine au coin nord-ouest. Décor : emprise x, z, w, d ; ancre du sprite au coin sud-est.
// etage: 1 = posé sur la crête (passe après le talus qui le porte) ; fond: true = couche sol (décalques, berges) sous tout le reste.
const CRETE = [-2.576, -3.748]; // ancre décalée de y 2,5 m (fiche d'Ocre : un sprite de décor n'a pas de champ y)
const D = (id, sprite, x, z, w, d, extra = {}) => ({ id, label: '', sprite, x, z, w, d, visitable: false, cue: null, named: false, solid: [], ...extra });

export const ITEMS_RENCONTRES = {
  carnet_chauffeur: { name: 'Carnet du chauffeur' }, // lore : « Livraison Anselme, Dusk-Town : 12 bidons filtrés… »
  fusil: { name: 'Fusil' }, pistolet: { name: 'Pistolet' }, poignard: { name: 'Poignard' }, barre: { name: 'Barre de fer' }, // armes du combat (data/combat.js ARMES) gardées au Sac
};

const PEAGE = (prix, si = '') => [
  { label: `« Voilà ${prix} dollars. »`, action: `pay:${prix};flag:emb_regle;flag:emb_paye`, next: 'paye' },
  { label: '« Deux bidons d\'eau. »', if: 'inv:water>=2', action: 'take:water;take:water;flag:emb_regle;flag:emb_paye', next: 'paye' },
  { label: `« ${prix}, pour un bout de sable ? Parlons-en. »`, test: 'parole:5', partialAt: 4, pass: 'neg_ok', partial: 'neg_moitie', fail: 'neg_rate' },
  { label: '« Un convoi du Service roule une heure derrière moi. »', test: 'parole:6', pass: 'bluff_ok', fail: 'bluff_rate' },
  { label: 'Montrer la plaque de camion du Service. « Ce convoi-là. »', if: 'inv:plaque>=1', test: 'parole:4', pass: 'bluff_ok', fail: 'bluff_rate' },
  // Quilla seule (Pibe chassé, assommé ou acheté) devant un joueur armé : intimider à 4 au lieu de 6 [proposition d'Ocre, §7]
  { label: '« Recule. Maintenant. »', if: '!emb_pibe_parti&!emb_pibe_ko&!emb_pibe_achete', test: 'intimider:6', opposed: true, pass: 'peur_ok', fail: 'peur_rate' },
  { label: '« Ton gamin est parti. Recule. Maintenant. »', if: 'emb_pibe_parti|emb_pibe_ko|emb_pibe_achete', test: 'intimider:4', opposed: true, pass: 'peur_ok', fail: 'peur_rate' },
  { label: '« Non. »', next: 'refus' },
];
const FIN = [{ label: 'Partir.', next: 'end' }];
const DIALOGUES_RENCONTRES = {
  rc_quilla: {
    start: { text: '« Doucement, voyageur. Tu ne poses rien, tu ne lèves rien. Tu marches sur ma route. »', options: [
      { label: '« Ta route ? »', next: 'route' },
      { label: '« Je veux juste passer. »', next: 'peage' },
      { label: '« Ton chauffeur est en chiffons. »', if: 'emb_mannequin_vu', next: 'trapo' },
      { label: '« Le chauffeur du pick-up a besoin d\'aide. »', if: '!emb_mannequin_vu', next: 'trapo_naif' },
      { label: '« Le gamin sur la crête, celui sur l\'épave. Ça fait deux. Il t\'en reste combien ? »', if: 'emb_vu_talus&emb_vu_epave', next: 'compte' },
      { label: '« Je fais demi-tour. »', next: 'demi' },
      { label: '[Attaquer] « Dégaine. »', action: 'combat:embuscade_piste', next: 'end' } ] },
    alerte: { text: '« Tu as marché sur la sonnette. Ça arrive. Mais maintenant, tout le monde est réveillé, et le prix aussi : vingt. »', options: [...PEAGE(20), { label: '[Attaquer] « Dégaine. »', action: 'combat:embuscade_piste', next: 'end' }] },
    route: { text: '« Celle-là, oui. La poussière est à tout le monde. La piste est à qui la tient, et aujourd\'hui c\'est moi. Péage : quinze dollars. Ou deux bidons d\'eau, je ne suis pas difficile. »', options: [{ label: '…', next: 'peage' }] },
    trapo_naif: { text: '« Il a surtout besoin qu\'on le laisse tranquille. Il s\'appelle Don Trapo. Il ne boit pas, il ne parle pas, et il arrête tout le monde. Le meilleur employé que j\'aie jamais eu. »', options: [{ label: '…', next: 'peage' }] },
    trapo: { text: '« Bien vu. Ça te fait un point. Les gens ont bon cœur, c\'est ça qui les perd. Toi, tu es juste curieux. »', options: [{ label: '…', next: 'peage' }] },
    peage: { text: '« Quinze dollars, et la piste est à toi jusqu\'à la douane. »', options: PEAGE(15) },
    paye: { text: '« Voilà un voyageur qui veut vieillir. Passe. Et ne touche pas au pick-up : il travaille. »', options: [{ label: '« D\'où il vient, ce pick-up ? »', next: 'appat' }, { label: '« Je passe. »', next: 'end' }] },
    appat: { text: '« De Dusk-Town, avec douze bidons et un gars qui roulait trop vite. Le gars est reparti à pied, sans ses bidons. Le pick-up, je l\'ai gardé. Un camion en panne, ça arrête tout le monde. »', options: [{ label: '« Et le gars ? »', next: 'appat2' }, { label: '« Je vois. »', next: 'end' }] },
    appat2: { text: '« Vivant. Je ne suis pas le Service. Moi, je ne ramasse que ce qui roule. »', options: FIN },
    neg_ok: { text: '« Huit. Parce que tu parles bien et que la journée est longue. »', options: [{ label: '« Huit, d\'accord. »', action: 'pay:8;flag:emb_regle;flag:emb_paye', next: 'paye' }, { label: '« Toujours trop. »', next: 'refus' }] },
    neg_moitie: { text: '« Douze. Et je n\'ai pas envie de compter plus loin. »', options: [{ label: '« Douze. »', action: 'pay:12;flag:emb_regle;flag:emb_paye', next: 'paye' }, { label: '« Non. »', next: 'refus' }] },
    neg_rate: { text: '« Tu parles trop. Vingt, maintenant. »', options: [{ label: '« Vingt… Tiens. »', action: 'pay:20;flag:emb_regle;flag:emb_paye', next: 'paye' }, { label: '« Non. »', next: 'refus' }] },
    bluff_ok: { text: '(Elle lève les yeux vers le miroir.) « Pibe ! Tu vois quelque chose ? » — Pibe, de la crête : « De la poussière, Quilla ! » — « De la poussière. Ça peut être n\'importe quoi. Passe. Vite. »', enter: 'flag:emb_regle;flag:emb_bluff', options: FIN },
    bluff_rate: { text: '« Le Service, ça s\'entend à dix kilomètres. Là, je n\'entends que toi. Le prix vient de monter : vingt. »', options: [{ label: '…', next: 'neg_rate' }] },
    peur_ok: { text: '(Elle recule d\'un pas.) « Tu as les yeux de quelqu\'un qui a déjà enterré du monde. Passe. On n\'a rien vu, tu n\'as rien vu. »', enter: 'flag:emb_regle;flag:emb_intimide', options: FIN },
    peur_rate: { text: '« Ah. Tu veux jouer. Pibe ! »', enter: 'combat:embuscade_piste', options: [{ label: '…', next: 'end' }] },
    refus: { text: '« Comme tu veux. Le désert est plein de gens qui ont dit non. »', options: [
      { label: '« J\'ai changé d\'avis. »', next: 'peage' }, { label: '[Attaquer]', action: 'combat:embuscade_piste', next: 'end' }, { label: '« Je fais demi-tour. »', next: 'demi' }] },
    compte: { text: '(Un silence.) « Personne ne compte jamais jusqu\'à deux. »', options: [
      { label: '« Tout le monde repart entier. Je passe, gratis. »', test: 'parole:4', pass: 'compte_ok', fail: 'peage' },
      { label: '« Et c\'est vous qui payez. Dix dollars, et vous changez de route. »', test: 'intimider:5', opposed: true, pass: 'racket_ok', fail: 'peur_rate' }] },
    compte_ok: { text: '« Gratis. Ne le répète pas, ça me ferait une mauvaise réputation. »', enter: 'flag:emb_regle;flag:emb_bluff', options: FIN },
    racket_ok: { text: '(Elle jette quelques billets dans le sable.) « Garde-les. Et ne reviens pas sur cette piste. »', enter: 'gain:10;flag:emb_regle;flag:emb_racket', options: FIN },
    demi: { text: '« Sage. La piste sera encore là demain. Moi aussi. »', enter: 'flag:emb_demi', options: FIN },
    pauvre: { text: '« Tu n\'as pas de quoi. Alors trouve autre chose. »', options: [{ label: '…', next: 'peage' }] },
  },
  rc_pibe: {
    start: { text: '« Bouge pas ! Bouge pas, je… je tire ! » (Le canon tremble.)', options: [
      { label: '« Tu as quel âge ? »', next: 'age' },
      { label: '« Lâche ce fusil et rentre chez toi. »', test: 'intimider:3', opposed: true, pass: 'pibe_fuit', fail: 'crie' },
      { label: '« Cinq dollars, et tu n\'as rien vu. »', action: 'pay:5;flag:emb_pibe_achete', next: 'achete' },
      { label: 'Le désarmer d\'un coup sec.', test: 'melee:4', pass: 'pibe_ko', fail: 'crie' } ] },
    age: { text: '« Seize. Presque. Quilla dit que l\'âge, ça ne compte pas sur la piste. »', options: [{ label: '…', next: 'start' }] },
    pibe_fuit: { text: '« Je… d\'accord. D\'accord ! » (Il lâche le fusil et dévale la sente.)', enter: 'give:fusil;flag:emb_pibe_parti', options: FIN },
    achete: { text: '« J\'ai rien vu. J\'ai jamais rien vu, moi. »', options: FIN },
    pibe_ko: { text: '(Il s\'assoit dans la poussière, le souffle coupé.)', enter: 'give:fusil;flag:emb_pibe_ko', options: FIN },
    crie: { text: '« QUILLA ! »', enter: 'combat:embuscade_piste', options: [{ label: '…', next: 'end' }] },
    pauvre: { text: '(Il renifle.) « T\'as même pas cinq dollars ? »', options: [{ label: '…', next: 'start' }] },
  },
  rc_morsa: {
    start: { text: '(Morsa ronfle doucement, le fusil sur le ventre.)', options: [
      { label: 'Prendre son fusil sans le réveiller.', test: 'discretion:5', pass: 'vol_ok', fail: 'reveil' },
      { label: 'Le réveiller doucement.', next: 'reveil' },
      { label: 'L\'assommer.', test: 'melee:3', pass: 'morsa_ko', fail: 'reveil' } ] },
    vol_ok: { text: '(Le fusil glisse. Morsa grogne et se retourne.)', enter: 'give:fusil;flag:emb_morsa_desarme', options: FIN },
    morsa_ko: { text: '(Un coup sec. Morsa s\'affaisse sur le plateau sans un bruit.)', enter: 'flag:emb_morsa_ko', options: FIN },
    reveil: { text: '« Mmh. Si tu es là, c\'est que le gamin dort aussi. »', options: [{ label: '« Combien Quilla te paie ? »', next: 'paie' }, { label: '[Attaquer]', action: 'combat:embuscade_piste', next: 'end' }] },
    paie: { text: '« Une part sur quatre. Une part de rien, ça fait rien. »', options: [{ label: '« Je double. Dix dollars, et tu regardes la piste. »', action: 'pay:10;flag:emb_morsa_achete', next: 'achete' }, { label: '« Dommage pour toi. »', next: 'end' }] },
    achete: { text: '« La piste. Je regarde la piste. Elle est très jolie aujourd\'hui. »', options: FIN },
    pauvre: { text: '« Dix. Pas un de moins. »', options: [{ label: '…', next: 'reveil' }] },
  },
  rc_tuerto: {
    start: { text: '« Tiens. Le lit, c\'est aussi ma route. »', options: [
      { label: '« Je ne fais que passer. »', next: 'retour' },
      { label: '« Un dollar par pas, et tu me montres le chemin ? »', test: 'troc:5', pass: 'guide', fail: 'retour' },
      { label: '[Attaquer]', action: 'combat:embuscade_piste', next: 'end' } ] },
    retour: { text: '« Alors passe par la piste, comme tout le monde. Quilla t\'attend. » (Il te raccompagne jusqu\'à la berge.)', enter: 'flag:emb_tuerto_vu;warp:rc_embuscade_piste:10:16.5', options: FIN },
    guide: { text: '« Six dollars. Et tu ne m\'as jamais vu. » (Il se rassoit ; le lit est libre.)', enter: 'pay:6;flag:emb_tuerto_achete', options: FIN },
  },
  rc_trapo: {
    start: { text: 'Des chiffons bourrés de paille, une chemise cousue sur un sac. Le chapeau est vissé sur un manche à balai.', options: [{ label: 'Laisser Don Trapo.', next: 'end' }] },
  },
};

export const RENCONTRES = {
  embuscade_piste: {
    nom: "L'appât de la piste", famille: 'pillards', terrains: ['piste'], biomes: ['desert', 'rock'], poids: 1, duree: 1, lieu: 'rc_embuscade_piste',
    prefixe: 'emb_', // drapeaux de la scène, gardés au journal de la case puis retirés de la partie à la sortie
    arrivee: 'La piste file droit vers l\u2019est. Au milieu, un pick-up arrêté, capot ouvert. Quelqu\u2019un est affalé contre la portière.',
    scene: { size: { w: 30, d: 24 }, city: 'nml',
      ground: { base: '#a8875a', skin: 'g_rc_sable', tileM: 4, clean: true, marge: { skin: 'g_rc_sable', tileM: 4, m: 30, voile: 'rgba(14,10,6,.18)' }, // voile de jour : remplacé à l'entrée par celui de l'ambiance ; hors scène : le sable continue, voilé (pas de vide)
        paint: [
        { x: 0, z: 10, w: 30, d: 6, skin: 'g_rc_piste', tileM: 4 }, { x: 8, z: 10, w: 4, d: 4, skin: 'g_rc_piste_b', tileM: 4 }, { x: 20, z: 10, w: 4, d: 4, skin: 'g_rc_piste_c', tileM: 4 },
        { x: 0, z: 17, w: 30, d: 7, skin: 'g_rc_lit', tileM: 4 }, { x: 12, z: 17, w: 4, d: 4, skin: 'g_rc_lit_b', tileM: 4 }, { x: 24, z: 21, w: 4, d: 3, skin: 'g_rc_lit_b', tileM: 4 },
        { x: 0, z: 4, w: 4, d: 4, skin: 'g_rc_sable_b', tileM: 4 }, { x: 24, z: 8, w: 4, d: 2, skin: 'g_rc_sable_c', tileM: 4 } ] },
      // lumière : suit l'heure du voyage, ambiance du biome désert (data/ambiances.js : ambre franc de la maquette en plein jour, nuit sombre) — jamais figée ici [Ocre + Régie 18/11]
      ambiance: 'desert',
      // cadre : à l'arrivée, la caméra vise entre le joueur et le pick-up ; butée : pas de vide ni de sable voilé aux bords (comme le terminus) [Régie 18/11]
      cadre: { desktop: { x: [12, 22], z: [13.5, 15] }, mobile: { x: [11.5, 24], z: [16, 16] } },
      niveaux: [{ x: 5, z: 0, w: 25, d: 5, y: 2.5 }, { x: 2, z: 3, w: 3, d: 7, y0: 2.5, y1: 0, axe: 'z' }],
      buildings: [ // PILOTE §15, dans l'ordre de la table
        D('rc_traces', 'rc_emb_traces_3q', 11, 8.6, 2, 1, { fond: true }), D('rc_trainees', 'rc_emb_trainees_3q', 18, 15.5, 9, 6, { fond: true }),
        D('rc_berge1', 'rc_ds_berge_3q', 0, 16, 10, 1, { fond: true }), D('rc_berge2', 'rc_ds_berge_b_3q', 10, 16, 10, 1, { fond: true }), D('rc_berge3', 'rc_ds_berge_3q', 20, 16, 10, 1, { fond: true }),
        D('rc_sente', 'rc_ds_sente_3q', 0, 0, 5, 10, { solid: [{ x: 0, z: 0, w: 5, d: 3, couv: 2 }, { x: 0, z: 3, w: 2, d: 5, couv: 1 }] }),
        D('rc_talus_a', 'rc_ds_talus_a_3q', 5, 0, 10, 8.5, { solid: [{ x: 5, z: 5, w: 10, d: 3.5, couv: 1 }] }),
        D('rc_talus_b', 'rc_ds_talus_b_3q', 15, 0, 10, 8.5, { solid: [{ x: 15, z: 5, w: 10, d: 3.5, couv: 1 }] }),
        D('rc_talus_fin', 'rc_ds_talus_fin_3q', 25, 0, 5, 8.5, { solid: [{ x: 25, z: 5, w: 5, d: 3.5, couv: 1 }] }),
        D('rc_r1', 'rc_ds_rochers_3q', 15, 2, 3, 1.5, { ancre: CRETE, etage: 1, solid: [{ x: 15, z: 2, w: 3, d: 1.5, couv: 1 }] }),
        D('rc_r2', 'rc_ds_rochers_b_3q', 22, 2.5, 3, 1.5, { ancre: CRETE, etage: 1, solid: [{ x: 22, z: 2.5, w: 3, d: 1.5, couv: 1 }] }),
        D('rc_r3', 'rc_ds_rochers_3q', 27, 1.5, 3, 1.5, { ancre: CRETE, etage: 1, solid: [{ x: 27, z: 1.5, w: 3, d: 1.5, couv: 1 }] }),
        D('rc_miroir', 'rc_emb_miroir_3q', 19.85, 3.05, 0.3, 0.3, { ancre: CRETE, etage: 1 }),
        D('rc_panneau', 'rc_ds_panneau_ufsa_3q', 3.2, 9.2, 0.6, 0.2, { solid: [{ x: 3.4, z: 9.2, w: 0.2, d: 0.2, couv: 0 }] }),
        D('rc_pickup', 'rc_emb_pickup_appat_3q', 12, 11, 5.2, 2.2, { solid: [{ x: 12, z: 11, w: 5.2, d: 2.2, couv: 1 }] }),
        D('rc_c1', 'rc_emb_caisses_eventrees_3q', 8.5, 14.8, 1.2, 0.8, { solid: [{ x: 8.5, z: 14.8, w: 1.2, d: 0.8, couv: 1 }] }),
        D('rc_c2', 'rc_emb_caisses_eventrees_b_3q', 10.2, 15.6, 1.2, 0.8, { solid: [{ x: 10.2, z: 15.6, w: 1.2, d: 0.8, couv: 1 }] }),
        D('rc_c3', 'rc_emb_caisses_eventrees_3q', 17.8, 15, 1.2, 0.8, { solid: [{ x: 17.8, z: 15, w: 1.2, d: 0.8, couv: 1 }] }),
        D('rc_fil', 'rc_emb_fil_boites_3q', 20.9, 10, 0.2, 6),
        D('rc_epave', 'rc_emb_epave_service_3q', 17, 18, 9, 2.8, { solid: [{ x: 17, z: 18, w: 9, d: 1, couv: 2 }, { x: 17, z: 19, w: 4, d: 1.8, couv: 2 }, { x: 22.5, z: 19, w: 3.5, d: 1.8, couv: 2 }] }),
        D('rc_bache', 'rc_emb_bache_cache_3q', 26.5, 20.5, 3.5, 3.5, { solid: [{ x: 26.5, z: 20.5, w: 3.5, d: 0.5, couv: 1 }, { x: 29.5, z: 21, w: 0.5, d: 3, couv: 1 }] }),
      ],
      props: [{ sprite: 'tires', x: 6.25, z: 20, fp: [2.5, 2] }], // tas de pneus du lit (assets/reused, réutilisé tel quel)
      entree: { x: 1.5, z: 13, heading: Math.PI / 2 },
      sorties: [
        { id: 'ouest', label: 'Demi-tour (carte)', x: 0.6, z: 13, zone: { x0: 0, x1: 0.9, z0: 9, z1: 17 }, effet: 'halte' },
        { id: 'est_route', label: 'Reprendre la piste', x: 29.4, z: 13, zone: { x0: 29.1, x1: 30, z0: 9, z1: 16.5 }, effet: 'reprise', si: 'emb_regle', refus: 'Quilla tient la piste. Il faut d\u2019abord régler le péage, ou la bande.' },
        { id: 'est_lit', label: 'Par le lit (reprendre)', x: 29.4, z: 18.75, zone: { x0: 29.1, x1: 30, z0: 16.5, z1: 20.5 }, effet: 'reprise' } ] },
    declencheurs: [ // zones au sol : une fois à l'entrée dans la zone, si la condition tient
      { id: 'T1', zone: { x: 10, z: 9, w: 13, d: 8 }, si: '!emb_t1&!emb_regle', enter: 'flag:emb_t1', dialogue: 'rc_quilla' },
      { id: 'T2', zone: { x: 20.7, z: 10, w: 0.6, d: 6 }, si: '!emb_vu_fil&!emb_regle&!emb_alerte', enter: 'flag:emb_alerte;flag:emb_t1;flag:emb_vu_talus;flag:emb_vu_epave', dialogue: 'rc_quilla:alerte', texte: 'Des boîtes de conserve claquent sous ton pied.' },
      { id: 'T3', zone: { x: 4, z: 17, w: 6, d: 7 }, si: '!emb_t3&!emb_regle', enter: 'flag:emb_t3', dialogue: 'rc_tuerto' },
      { id: 'garde', zone: { x: 23, z: 9, w: 1, d: 7.5 }, si: '!emb_regle', dialogue: 'rc_quilla:refus', siDeja: 'emb_parle', combat: 'embuscade_piste', enter: 'flag:emb_t1' },
      { id: 'pres_pibe', zone: { x: 10.5, z: 0, w: 12, d: 9 }, enter: 'flag:emb_vu_talus' },
      { id: 'pres_morsa', zone: { x: 15.75, z: 17, w: 12, d: 7 }, enter: 'flag:emb_vu_epave' },
      // contournement par le lit, sous l'épave : Discrétion 4 (6 si le fil a sonné) ; échec : Morsa crie, combat
      { id: 'lit', zone: { x: 12, z: 20.8, w: 14, d: 3.2 }, si: '!emb_regle&!emb_lit_ok&!emb_morsa_ko&!emb_morsa_achete', test: 'discretion:4', testSi6: 'emb_alerte', pass: 'flag:emb_lit_ok', fail: 'flag:emb_vu_epave;combat:embuscade_piste', texte: 'Tu longes l\u2019épave, courbé sous la ridelle.', echec: 'Morsa se redresse sur le plateau : « QUILLA ! »' },
    ],
    pnj: [
      { id: 'rc_quilla_assise', name: 'Quilla', sprite: 'gen_rc_quilla_assise', portraitDe: 'gen_rc_quilla', x: 24.5, z: 9.0, faceTo: [1.5, 13], si: '!emb_t1&!emb_vaincue', dialogue: 'rc_quilla', cacheCombat: true, bloque: false },
      { id: 'rc_quilla', name: 'Quilla', sprite: 'gen_rc_quilla', x: 19, z: 12, faceTo: [1.5, 13], si: 'emb_t1&!emb_vaincue', dialogue: 'rc_quilla', cacheCombat: true, bloque: false },
      { id: 'rc_pibe', name: 'Pibe', sprite: 'gen_rc_pibe', x: 16.5, z: 4.5, faceTo: [16.5, 13], si: 'emb_vu_talus&!emb_pibe_parti&!emb_pibe_ko&!emb_vaincue', dialogue: 'rc_pibe', cacheCombat: true, bloque: false }, // y 2,5 : donné par le niveau de crête
      { id: 'rc_morsa', name: 'Morsa', sprite: 'gen_rc_morsa_couche', portraitDe: 'gen_rc_morsa', x: 21.75, z: 19.9, y: 1.3, faceTo: [30, 19.9], fige: true, sansMiroir: true, si: 'emb_vu_epave&!emb_morsa_ko&!emb_vaincue', dialogue: 'rc_morsa', cacheCombat: true, bloque: false }, // couché : tête à l'ouest, jamais retourné
      { id: 'rc_tuerto', name: 'Tuerto', sprite: 'gen_rc_tuerto', x: 6, z: 22, faceTo: [12, 22], si: 'emb_t3&!emb_vaincue', dialogue: 'rc_tuerto', cacheCombat: true, bloque: false },
      { id: 'rc_trapo', name: 'Don Trapo', sprite: 'gen_rc_trapo', x: 13.5, z: 13.7, faceTo: [1.5, 13], fige: true, dialogue: 'rc_trapo', portrait: false },
    ],
    // fouilles et examens (§3, §9) : point au sol, anneau comme les portes ; clic sur ordinateur, appui sur mobile (pas de survol)
    points: [
      { id: 'rc_boite_gants', x: 11.6, z: 12.1, si: '!emb_f_gants', enter: 'gain:4;give:carnet_chauffeur;flag:emb_f_gants', text: 'Boîte à gants : quatre dollars et un carnet. « Livraison Anselme, Dusk-Town : 12 bidons filtrés. Ne pas s\u2019arrêter avant la douane. Ne s\u2019arrêter pour personne. »', empty: 'La boîte à gants est vide.' },
      { id: 'rc_ex_pickup', x: 16.4, z: 13.9, text: 'Les quatre pneus sont tranchés net, au couteau. Capot ouvert, mais pas un outil par terre : personne n\u2019a essayé de réparer.' },
      { id: 'rc_reservoir', x: 17.7, z: 12.1, text: 'Le réservoir : percé. Même le sable n\u2019y reste pas.' },
      { id: 'rc_caisse1', x: 9.1, z: 14.3, text: 'Vides. Le sable a déjà fait une petite dune au fond : pillées depuis des jours, pas aujourd\u2019hui.' },
      { id: 'rc_caisse3', x: 18.4, z: 14.5, text: 'Vides. Le sable a déjà fait une petite dune au fond : pillées depuis des jours, pas aujourd\u2019hui.' },
      { id: 'rc_caisse2', x: 10.8, z: 15.2, si: 'observation>=4&!emb_f_c2', enter: 'give:ration;give:water;flag:emb_f_c2', text: 'Un double fond, sous le sable : une ration et un bidon d\u2019eau.', empty: 'Vide. Le sable a déjà fait une petite dune au fond.' },
      { id: 'rc_traces', x: 11.8, z: 8.9, enter: 'flag:emb_vu_talus', text: s => 'Des empreintes fraîches montent vers la crête.' + ((s.character?.skills?.observation ?? 0) >= 40 ? ' Aucune ne redescend.' : '') },
      { id: 'rc_miroir_ex', x: 20, z: 9, enter: 'flag:emb_vu_talus', text: 'Un éclat sur la crête, toujours au même endroit. Un miroir, posé pour faire signe.' },
      { id: 'rc_trainees_ex', x: 19.2, z: 16.4, enter: 'flag:emb_vu_epave', text: 'Quelque chose de lourd a été traîné vers le lit asséché. Les sillons passent au pied de l\u2019épave.' },
      { id: 'rc_epave_ex', x: 19, z: 21.3, enter: 'flag:emb_vu_epave', text: s => 'Un camion du Service, ensablé depuis des années.' + ((s.character?.skills?.observation ?? 0) >= 50 ? ' Sur le plateau, des mégots récents, et une forme qui ne bouge pas assez pour être un sac.' : '') },
      { id: 'rc_fil_ex', x: 20.3, z: 9.4, si: 'observation>=3', enter: 'flag:emb_vu_fil', text: 'Un fil de fer tendu en travers de la piste, quatre boîtes de conserve dessus. Un piège à bruit : tu l\u2019enjamberas sans bruit.', empty: 'Rien de particulier sur la piste.' },
      { id: 'rc_panneau_ex', x: 3.6, z: 9.9, text: 'Le panneau a perdu ses lettres. Il reste les trous des balles, en forme de flèche vers l\u2019est.' },
      { id: 'rc_pneus_ex', x: 6.25, z: 21.6, enter: 'flag:emb_vu_lit', text: 'Un tas de pneus. Derrière, quelqu\u2019un a tassé le sable pour s\u2019asseoir.' },
      // cache sous la bâche : libre après une victoire ou un racket ; avant, Discrétion 6 (échec = combat)
      { id: 'rc_cache', x: 26.2, z: 22.2, si: '!emb_f_cache&!emb_regle|!emb_f_cache&emb_vaincue|!emb_f_cache&emb_racket', test: 'discretion:6', testSi: '!emb_regle',
        enter: 'gain:22;give:water:3;give:ration;give:poignard;flag:emb_f_cache', pass: 'gain:22;give:water:3;give:ration;give:poignard;flag:emb_f_cache;flag:emb_vole', fail: 'combat:embuscade_piste',
        text: (s, ok) => ok ? 'Sous la bâche : trois bidons bleus de Dusk-Town, une ration, 22 dollars et un poignard.' : 'Une boîte de conserve roule. Sur l\u2019épave, quelqu\u2019un se redresse.', empty: 'La cache est vide, ou gardée.' },
      { id: 'rc_plateau', x: 21.75, z: 21.2, si: '!emb_f_plateau&!emb_morsa_desarme&emb_morsa_ko|!emb_f_plateau&!emb_morsa_desarme&emb_vaincue', enter: 'give:fusil;flag:emb_f_plateau', text: 'Sur le plateau : le fusil de Morsa, une gourde vide, des mégots.', empty: 'Rien à prendre sur le plateau.' },
    ],
    dialogues: DIALOGUES_RENCONTRES,
    combat: { nom: 'Embuscade de la piste', centre: { x: 18, z: 13 }, prefixe: 'emb_',
      ennemis: [
        { id: 'quilla', nom: 'Quilla', sprite: 'gen_rc_quilla', x: 19, z: 12, pv: 18, pa: 7, initiative: 7, arme: 'pistolet', competences: { melee: 40, armes: 55 }, rendSous: 0.25 },
        { id: 'pibe', nom: 'Pibe', sprite: 'gen_rc_pibe', x: 16.5, z: 4.5, pv: 10, pa: 6, initiative: 8, arme: 'fusil', competences: { melee: 10, armes: 35 }, fuitTour: 2, si: '!emb_pibe_parti&!emb_pibe_ko&!emb_pibe_achete' },
        { id: 'morsa', nom: 'Morsa', sprite: 'gen_rc_morsa', x: 21.75, z: 19.9, pv: 14, pa: 6, initiative: 5, arme: 'fusil', armeSi: { emb_morsa_desarme: 'mains' }, competences: { melee: 30, armes: 50 }, si: '!emb_morsa_ko&!emb_morsa_achete' },
        { id: 'tuerto', nom: 'Tuerto', sprite: 'gen_rc_tuerto', x: 10, z: 20.5, pv: 14, pa: 6, initiative: 6, arme: 'barre', competences: { melee: 45, armes: 20 }, entreTour: 2, si: '!emb_tuerto_achete' } ],
      issues: { victoire: 'flag:emb_regle;flag:emb_vaincue', fuite: 'rencontre:quitter', reddition: 'payMax:20;flag:emb_regle', defaite: 'payMax:20;take:water;flag:emb_regle;warp:rc_embuscade_piste:1.5:13' },
      textes: { debut: 'Quilla siffle entre ses dents. Sur la crête et sur l\u2019épave, des fusils se lèvent.',
        entrees: { morsa: 'Morsa saute de l\u2019épave.' }, // ligne de récit quand l'unité est engagée (Morsa reste au sol en (19 ; 17), niche inchangée) [retours Ocre 18/11]
        victoire: 'Quilla crache dans le sable. « Garde la piste, alors. Elle ne te gardera pas. » Ils s\u2019en vont par le lit.',
        fuite: 'Tu cours jusqu\u2019à ne plus entendre les boîtes de conserve.',
        reddition: 'Tu jettes les billets dans le sable. Quilla les compte sans se presser.',
        defaite: 'Le ciel. Le sable. Don Trapo, qui te regarde.' } },
  },
};
