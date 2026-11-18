// Rencontre du jalon 2 : « Le témoin sous les pins » (survivant blessé, biome forêt), d’après docs/rencontres/SURVIVANT.md (Ocre, 3b85a96 + 81e4adb ;
// sprites 014db7e + 98a6fd2) : plan 32 × 26 m (§4), sans niveaux, dialogues du §6, manières d’agir du §7, combat du §8 (Paca seulement, si on l’attaque),
// butin du §9, entrée du §14, poses du §15, accroches du §12. Aucun ennemi d’office : Roque n’est jamais au combat (le frapper se règle en dialogue).
// FORÊT EN GABARITS GRIS : Ocre refait les pins (vraie iso, massifs, troncs couchés, souches, ombres) ; pins, pin foudroyé et fourré restent des volumes
// gris (gabarit: true) jusqu’à son nouveau SHA ; Roque, Paca, la lanterne, le mulet, la besace, le soulier, les décalques et les sols gardent leurs clés.
// Drapeaux de scène sur_* purgés à la sortie (journal de la case) ; drapeaux de monde monde_sur_vu, monde_roque_*, monde_mateo_pris jamais purgés.
// Garde-fou de Régie (§13) : les monde_* ne servent qu’à des répliques et à des indices, jamais à une conséquence de quête.
const D = (id, sprite, x, z, w, d, extra = {}) => ({ id, label: '', sprite, x, z, w, d, visitable: false, cue: null, named: false, solid: [], ...extra });
const R = (x, z, w, d, couv = 1) => ({ x, z, w, d, couv });
const FIN = [{ label: 'Partir.', next: 'end' }];
const SUITE = next => [{ label: '…', next }];
const cap = (x, z, [fx, fz]) => Math.atan2(fx - x, fz - z);
// gabarit gris de la forêt (en attendant la refonte d’Ocre) : volume simple, olive-gris (§11), même emprise et mêmes solides que la pose du §15.1
const PIN = { kind: 'arbre', h: 5.5, color: '#55553e' }, PIN_B = { kind: 'arbre', h: 4.8, color: '#55553e' };
const ARBRE = (id, sprite, x, z, w, d, ph) => D(id, sprite, x, z, w, d, { gabarit: true, ph, solid: [R(x, z, w, d, 2)] });

const ATTAQUER_ROQUE = { label: '[Attaquer]', if: '!sur_depouille', next: 'frappe' };
const DEPOUILLER = { label: '« Je prends ce que tu as. »', if: '!sur_depouille', next: 'depouille' };
const BOIRE = [
  { label: '« Tiens, bois. »', if: 'inv:water>=1&!sur_soigne', action: 'take:water;flag:sur_soigne;flag:sur_parle', next: 'soigne' },
  { label: '« Je n’ai plus d’eau, mais j’ai une ration. »', if: 'inv:ration>=1&inv:water<1&!sur_soigne', action: 'take:ration;flag:sur_soigne;flag:sur_parle', next: 'soigne' } ];

export const DIALOGUES_SURVIVANT = {
  sur_roque: {
    start: { text: '« …De l’eau. S’il t’en reste. Je… je me relèverai. L’enfant. Tu l’as vu, sur la piste ? »', enter: 'flag:sur_appel', options: [
      ...BOIRE,
      { label: '« Quel enfant ? »', action: 'flag:sur_parle', next: 'recit' },
      { label: '« Qu’est-ce qui s’est passé ? »', action: 'flag:sur_parle', next: 'recit' },
      { label: '« Je ne peux rien pour toi. »', action: 'flag:sur_parle', next: 'refus' },
      DEPOUILLER, ATTAQUER_ROQUE,
      { label: '(T’éloigner.)', next: 'end' } ] },
    soigne: { text: '« Merci. Ça… ça tient. Je m’appelle Roque. C’est mon neveu, Mateo. On allait à la Station. Il y avait quelqu’un, pour lui. Pour le faire passer. Un contact, à la Station. Il fait passer les gens comme lui. Plus au nord. Plus à l’abri. »',
      alt: [{ if: 'monde_remedios_vue', text: '« Merci. Ça… ça tient. Je m’appelle Roque. C’est mon neveu, Mateo. On allait à la Station. Il y avait quelqu’un, pour lui. Pour le faire passer. La caravane. Celle de la citerne. Tu la connais, toi aussi. »' }],
      options: [
        { label: '« Le Service est venu ? »', next: 'recit' },
        { label: '« Je peux te relever. On marche jusqu’à la Station. »', if: '!sur_escorte', next: 'escorte_offre' },
        { label: '« J’ai vu un soulier, près du mulet. »', if: 'sur_vu_soulier', next: 'soulier' },
        { label: '« Il y a des ornières, plus à l’est. »', if: 'sur_vu_ornieres', next: 'ornieres' },
        { label: '« Repose-toi. Je reviens. »', next: 'end' } ] },
    // enfant / récit : même nœud ; sur_recit = Roque a raconté l’enfant (monde_mateo_pris à la sortie, §7)
    recit: { text: '« Mateo. Le fils de ma sœur. Il a… la peau, tu vois, les plaques, comme certains, au bord du fleuve. À Dusk-Town ils baissent les cols, pour ça. On se levait avant le jour, pour ne pas les croiser. Ils nous ont eus quand même. Deux hommes, un véhicule. Ils ont pris l’enfant. Ils m’ont tiré dessus comme à un chien. Le mulet aussi. »',
      enter: 'flag:sur_recit',
      alt: [{ if: 'race_mutant', text: '« Mateo. Le fils de ma sœur. Il a… la peau, tu vois, les plaques, comme certains, au bord du fleuve. À Dusk-Town ils baissent les cols, pour ça. On se levait avant le jour, pour ne pas les croiser. Ils nous ont eus quand même. Deux hommes, un véhicule. Ils ont pris l’enfant. Ils m’ont tiré dessus comme à un chien. Le mulet aussi. » (Il te regarde mieux.) « Toi aussi, tu… Oui. Je vois. Alors tu comprends pourquoi je le menais là-bas. »' }],
      options: [
        ...BOIRE,
        { label: '« Je vais suivre la piste. »', action: 'flag:sur_promet', next: 'promet' },
        { label: '« Je peux t’emmener à la Station. »', if: '!sur_escorte', next: 'escorte_offre' },
        { label: '« Je n’ai rien à te donner. »', next: 'refus' } ] },
    soulier: { text: '« C’est le sien. L’autre est… je ne sais pas. Il l’a perdu quand ils l’ont fait monter. Il a treize ans. Il ne pèse pas lourd. »', enter: 'flag:sur_recit', options: SUITE('reprise') },
    ornieres: { text: '« Je les ai entendus. Le moteur. Ils sont repartis vers la Station, ou vers la douane. Si tu vas de ce côté-là… si tu vois un enfant, les plaques sur les bras, un soulier à un pied… » (Il s’arrête.) « Dis-lui que son oncle n’a pas couru. »', enter: 'flag:sur_recit', options: SUITE('reprise') },
    escorte_offre: { text: '« Tu ferais ça ? C’est une heure, peut-être deux, et je pèse. Mais j’arriverai. À la Station, je sais qui voir. Je te paierai ce que j’ai : huit dollars, et mon couteau, s’il te sert. »', options: [
      { label: '« Viens. »', action: 'flag:sur_escorte;flag:sur_soigne;flag:sur_regle;gain:8', next: 'escorte_ok' },
      { label: '« Je ne peux pas m’attarder. »', next: 'refus' } ] },
    // escorte : +1 h à la sortie (dureeSi), monde_roque_sauve + monde_roque_escorte (drapeauxSortie) ; le couteau, s’il l’offre, est optionnel
    escorte_ok: { text: '« Bien. Aide-moi à me mettre debout. On avance doucement. S’il est encore à la Station… on verra. »', options: [
      { label: '« Garde ton couteau. »', if: '!sur_couteau&!sur_couteau_laisse', action: 'flag:sur_couteau_laisse', next: 'escorte_ok' },
      { label: '« Je prends le couteau. »', if: '!sur_couteau&!sur_couteau_laisse', action: 'give:poignard;flag:sur_couteau', next: 'escorte_ok' },
      { label: '« On y va. » (reprendre la piste avec Roque)', action: 'rencontre:quitter:reprise', next: 'end' },
      { label: '« Attends-moi. Je regarde encore. »', next: 'end' } ] },
    promet: { text: '« Merci. Même si tu ne le trouves pas. Merci d’avoir dit ça. »', options: SUITE('reprise') },
    refus: { text: '« Alors laisse-moi au moins la gourde, si tu en as une. Ou pars, et que Paca attende encore un peu. »',
      alt: [{ if: 'sur_soigne|sur_laisse_eau', text: '« Va. Tu as déjà fait plus que les autres. »' }], options: [
        { label: '« Je te laisse de l’eau. »', if: 'inv:water>=1&!sur_soigne&!sur_laisse_eau', action: 'take:water;flag:sur_laisse_eau', next: 'eau' },
        { label: '(Partir.)', next: 'end' } ] },
    eau: { text: '« Elle est là. Merci. »', options: FIN },
    // reprise (déjà parlé) : soigné, eau laissée, sinon plus faible
    reprise: { text: '« Tu… tu as de l’eau, cette fois ? »',
      alt: [{ if: 'sur_soigne', text: '« Tu reviens. J’ai moins froid. »' }, { if: 'sur_laisse_eau', text: '« Ta gourde est encore là. J’en ai pris une gorgée. »' }], options: [
        ...BOIRE,
        { label: '« Je te laisse de l’eau. »', if: 'inv:water>=1&!sur_soigne&!sur_laisse_eau', action: 'take:water;flag:sur_laisse_eau', next: 'eau' },
        { label: '« Qu’est-ce qui s’est passé ? »', if: '!sur_recit', next: 'recit' },
        { label: '« Je peux t’emmener à la Station. »', if: 'sur_soigne&!sur_escorte', next: 'escorte_offre' },
        { label: '« J’ai vu un soulier, près du mulet. »', if: 'sur_vu_soulier', next: 'soulier' },
        { label: '« Il y a des ornières, plus à l’est. »', if: 'sur_vu_ornieres', next: 'ornieres' },
        DEPOUILLER, ATTAQUER_ROQUE,
        { label: '« Repose-toi. »', next: 'end' } ] },
    // dépouiller (§6.1, §9) : 8 $ et le couteau ; la dernière eau en plus = sur_laisse_mourir (pas de monde_roque_sauve) ; après le soin, il ne résiste pas
    depouille: { text: '« Prends. L’eau d’abord, je t’en prie, laisse-moi l’eau. »', alt: [{ if: 'sur_soigne', text: '(Il ne résiste pas.) « Je ne t’aurais pas demandé ça. »' }], options: [
      { label: '(Prendre l’argent et le couteau.)', if: '!sur_soigne', action: 'gain:8;give:poignard;flag:sur_depouille', next: 'depouille_fin' },
      { label: '(Prendre aussi la gourde.)', if: '!sur_soigne', action: 'gain:8;give:poignard;give:water;flag:sur_depouille;flag:sur_laisse_mourir', next: 'laisse_mourir' },
      { label: '(Prendre l’argent, le couteau et la gourde.)', if: 'sur_soigne', action: 'gain:8;give:poignard;give:water;flag:sur_depouille', next: 'depouille_fin' },
      { label: '« Non. Garde tout. »', next: 'end' } ] },
    depouille_fin: { text: '(Il ferme les yeux. Il ne dit plus rien.)', options: FIN },
    laisse_mourir: { text: '« Va. Que tu ne le retrouves pas, l’enfant. »', options: FIN },
    // frapper Roque (§8) : il se rend au premier coup, pas de combat ; même butin que dépouillé
    frappe: { text: '(Il ne se défend pas. Il tourne la tête vers le pin.) « Vas-y. Mais l’enfant, toi, tu ne le retrouveras pas. »', enter: 'gain:8;give:poignard;give:water;flag:sur_depouille;flag:sur_laisse_mourir;flag:sur_frappe', options: FIN },
    mourant: { text: '(Il ne te regarde plus. Il regarde la piste, vers l’est.)', options: FIN },
  },
  sur_paca: {
    start: { text: '« Je n’ai encore rien pris. Tu peux vérifier. J’attendais de voir s’il se relevait, ou si quelqu’un passait. Ça tombe bien : quelqu’un passe. »', enter: 'flag:sur_vu_paca;flag:sur_paca_dit', options: [
      { label: '« Tu l’as vu, ce qui s’est passé ? »', next: 'temoin' },
      { label: '« Tu comptes le dépouiller. »', next: 'aveu' },
      { label: '« Laisse-le. Tu t’en vas. »', if: '!sur_soigne', test: 'intimider:5', pass: 'degage', fail: 'reste' },
      { label: '« Laisse-le. Tu t’en vas. »', if: 'sur_soigne', next: 'degage' },
      { label: '« On peut partager, s’il meurt. »', if: '!sur_paca_pacte', action: 'flag:sur_paca_pacte', next: 'pacte' },
      { label: '[Attaquer]', action: 'combat:survivant_pins', next: 'end' },
      { label: '(T’éloigner.)', next: 'end' } ] },
    temoin: { text: '« J’étais plus bas, vers la borne. J’ai entendu le moteur, les voix, un coup. Quand je suis remontée, l’enfant n’y était plus, et l’homme était déjà contre le pin. Les hommes du Service ne s’attardent pas sous les arbres. Ils n’aiment pas ce bois. Mais ils y entrent, quand il le faut. »', options: [
      { label: '« Que vas-tu faire ? »', next: 'aveu' },
      { label: '(T’éloigner.)', next: 'end' } ] },
    aveu: { text: '« Ce qu’on fait tous, sur la piste. J’attends. S’il se relève, je n’ai rien vu. S’il ne se relève pas, le mulet a encore un harnais, et l’homme a un couteau. Je ne suis pas celle qui a tiré. »', options: [
      { label: '« Touche-le, et on a un problème. »', next: 'degage' },
      { label: '« Fais ce que tu veux. »', action: 'flag:sur_paca_libre', next: 'end' },
      { label: '[Attaquer]', action: 'combat:survivant_pins', next: 'end' } ] },
    degage: { text: '« Bien. Tu l’as dit clairement. Je rentre vers la Station. Il y a d’autres pistes. »', enter: 'flag:sur_paca_partie', options: FIN },
    reste: { text: '(Elle ne bouge pas.) « Je n’ai rien fait. Toi non plus, pour l’instant. »', options: [
      { label: '[Attaquer]', action: 'combat:survivant_pins', next: 'end' },
      { label: '(T’éloigner.)', next: 'end' } ] },
    pacte: { text: '« D’accord. Toi l’eau et le couteau, moi le harnais et les semelles, si tu veux. On n’est pas des bêtes. »', options: FIN },
    soigne: { text: '« Alors il se relèvera. Tant mieux. J’irai voir plus loin. »', enter: 'flag:sur_paca_partie', options: FIN },
  },
};

const ORNIERES = 'La terre a été labourée par un véhicule lourd, pas un mulet. Deux paires d\u2019ornières, récentes, qui repartent vers l\u2019est. Dans la poussière : trois étuis de fusil du Service, encore brillants.';
const SOULIER = 'un soulier d\u2019enfant, trop petit pour l\u2019homme du pin, trop propre pour avoir longtemps traîné ici.';

export const SURVIVANT = {
  nom: 'Le témoin sous les pins', famille: 'survivant', terrains: ['foret'], biomes: ['forest'], poids: 1, lieu: 'rc_survivant_pins', prefixe: 'sur_',
  duree: 1, dureeSi: { sur_escorte: 1 }, // +1 h si Roque a été escorté (§1, §12.3)
  // unique (monde_sur_vu, jamais purgé) ; jamais tirée sur G09, case du Temple du couchant (§12.1)
  si: (etat, kase) => !etat.flags.monde_sur_vu && !(kase && kase.col === 6 && kase.row === 8), drapeauArrivee: 'monde_sur_vu',
  arrivee: 'Un bois de pins secs. Un mulet mort sur la piste, un homme contre un arbre foudroyé. Une lanterne brûle encore.',
  arriveeRetour: 'Le bois de pins. La lanterne, contre le pin foudroyé.',
  // drapeaux de monde posés à la sortie (§7), avant la purge des sur_* ; répliques et indices seulement (garde-fou de Régie)
  drapeauxSortie: {
    monde_roque_sauve: 'sur_soigne&!sur_laisse_mourir|sur_laisse_eau&!sur_laisse_mourir|sur_escorte&!sur_laisse_mourir',
    monde_roque_escorte: 'sur_escorte', monde_roque_depouille: 'sur_depouille', monde_mateo_pris: 'sur_vu_ornieres|sur_recit' },
  scene: { size: { w: 32, d: 26 }, city: 'nml', ambiance: 'forest', // courbe forest (ambiances.js, §11) ; nuit commune bleu-gris
    ground: { base: '#8a5a32', skin: 'g_rc_aiguilles', tileM: 4, clean: true, marge: { skin: 'g_rc_aiguilles_c', tileM: 4, m: 30, voile: 'rgba(12,10,6,.20)' },
      paint: [ { x: 4, z: 4, w: 4, d: 4, skin: 'g_rc_aiguilles_b', tileM: 4 }, { x: 20, z: 8, w: 4, d: 4, skin: 'g_rc_aiguilles_b', tileM: 4 }, { x: 8, z: 20, w: 4, d: 4, skin: 'g_rc_aiguilles_c', tileM: 4 },
        { x: 24, z: 20, w: 4, d: 4, skin: 'g_rc_aiguilles_b', tileM: 4 }, { x: 12, z: 0, w: 4, d: 4, skin: 'g_rc_aiguilles_c', tileM: 4 },
        { x: 0, z: 15, w: 32, d: 5, skin: 'g_rc_piste_foret', tileM: 4 }, { x: 12, z: 15, w: 4, d: 5, skin: 'g_rc_piste_foret_b', tileM: 4 }, { x: 24, z: 15, w: 4, d: 5, skin: 'g_rc_piste_foret_b', tileM: 4 } ] },
    cadre: { desktop: { x: [15, 24], z: [11, 16] }, mobile: { x: [16, 24], z: [13, 17] } },
    buildings: [ // table de poses du §15.1 (ancre au coin sud-est de l’emprise) ; décalques en fond d’abord
      D('sur_trainee', 'rc_sur_trainee_3q', 21.5, 16.2, 8, 1.5, { fond: true }),
      D('sur_ornieres', 'rc_sur_ornieres_3q', 26.2, 15.4, 4, 3, { fond: true }),
      ARBRE('sur_pin_1', 'rc_fo_pin_3q', 2, 1, 2.2, 2.2, PIN),
      ARBRE('sur_pin_2', 'rc_fo_pin_b_3q', 7, 2, 2, 2, PIN_B),
      D('sur_borne', 'rc_fo_borne_3q', 2.5, 12, 1.2, 1.2, { ph: { h: 0.8 }, solid: [R(2.5, 12, 1.2, 1.2, 1)] }),
      ARBRE('sur_pin_3', 'rc_fo_pin_3q', 22, 1.5, 2.2, 2.2, PIN),
      ARBRE('sur_pin_mort', 'rc_fo_pin_mort_3q', 13.5, 9, 4, 3.5, { kind: 'arbre', h: 5.5, houppier: 0, fut: 0.9, futColor: '#8a8272' }),
      D('sur_lanterne', 'rc_sur_lanterne_3q', 15.6, 12.0, 0.25, 0.25, { editorDepth: 1 }), // accrochée à la branche sud : après le pin
      ARBRE('sur_pin_4', 'rc_fo_pin_3q', 4, 22.5, 2.2, 2.2, PIN),
      ARBRE('sur_pin_5', 'rc_fo_pin_b_3q', 28, 2, 2, 2, PIN_B),
      D('sur_fourre', 'rc_fo_fourre_3q', 24.5, 6.5, 2.5, 2.2, { gabarit: true, ph: { h: 1.6, color: '#5c5a3c' }, solid: [R(24.5, 6.5, 2.5, 2.2, 1)] }),
      D('sur_besace', 'rc_sur_besace_3q', 18.4, 15.6, 0.8, 0.6, {}),
      ARBRE('sur_pin_6', 'rc_fo_pin_b_3q', 12, 23, 2, 2, PIN_B),
      D('sur_soulier', 'rc_sur_soulier_3q', 22.2, 16.8, 0.3, 0.3, {}),
      D('sur_mulet', 'rc_sur_mulet_3q', 20.2, 16.0, 2.4, 1.3, { ph: { h: 0.9 }, solid: [R(20.2, 16.0, 2.4, 1.3, 1)] }),
      ARBRE('sur_pin_7', 'rc_fo_pin_3q', 24, 22.8, 2.2, 2.2, PIN),
      ARBRE('sur_pin_8', 'rc_fo_pin_b_3q', 29, 22.5, 2, 2, PIN_B),
    ],
    // la lanterne, seule lumière (§3, §11) : calque _neon serré sur la flamme, pulse lent ; flaque générique au sol la nuit seulement (comme le bivouac), sans halo
    enseignes: [{ id: 'sur_lampe', building: 'sur_lanterne', effet: 'pulse', periode: 6, intensite: 0.6,
      flaque: { r: 1.5, x: 15.8, z: 12.6, couleur: '#ff9a48', i: 0.55 } }],
    props: [],
    entree: { x: 30.5, z: 17, heading: -Math.PI / 2 }, // depuis la Station, face à l’ouest
    sorties: [
      { id: 'ouest', label: 'Vers le Temple (carte)', x: 0.6, z: 17.5, zone: { x0: 0, x1: 0.9, z0: 15, z1: 20 }, effet: 'halte',
        texte: 'La piste descend vers l\u2019ouest, vers le Temple du couchant.' },
      { id: 'est', label: 'Reprendre la piste', x: 31.4, z: 17.5, zone: { x0: 31.1, x1: 32, z0: 15, z1: 20 }, effet: 'reprise', // jamais gardée (§12.2)
        texte: 'Tu reprends la piste.', textes: [{ si: 'sur_escorte', texte: 'Tu prends Roque sous le bras. Une heure de plus, à son pas.' }] } ] },
  declencheurs: [
    // Roque appelle une fois quand on passe sur la piste (§7 « Passer ») ; à 3 m, son dialogue s’ouvre (pres_roque)
    { id: 'appel', zone: { x: 12, z: 15, w: 9, d: 5 }, si: '!sur_appel&!sur_parle', enter: 'flag:sur_appel', texte: 'Une voix, contre le pin foudroyé : « …De l\u2019eau. S\u2019il t\u2019en reste. »' },
    { id: 'pres_roque', zone: { x: 13, z: 12.5, w: 5.6, d: 2.5 }, si: '!sur_parle&!sur_roque_vu', enter: 'flag:sur_roque_vu', dialogue: 'sur_roque' },
    { id: 'pres_paca', zone: { x: 22.8, z: 8.7, w: 6, d: 3.2 }, si: '!sur_paca_dit&!sur_paca_partie', dialogue: 'sur_paca' } ],
  pnj: [
    { id: 'sur_roque', name: 'Roque', sprite: 'gen_rc_roque', x: 15.8, z: 13.3, faceTo: [30.5, 17], fige: true, dialogue: 'sur_roque', bloque: false, // assis contre le pin (pivot 0)
      entrees: [{ si: 'sur_laisse_mourir|sur_frappe', node: 'mourant' }, { si: 'sur_escorte', node: 'escorte_ok' }, { si: 'sur_parle', node: 'reprise' }] },
    { id: 'sur_paca', name: 'Paca', sprite: 'gen_rc_paca', x: 25.8, z: 8.9, faceTo: [20, 16], dialogue: 'sur_paca', si: '!sur_paca_partie', cacheCombat: true, bloque: false,
      entrees: [{ si: 'sur_soigne', node: 'soigne' }] },
  ],
  // examens et fouilles (§3, §9) ; ★ = indices de ce qui est arrivé à Mateo
  points: [
    { id: 'sur_pin_ex', x: 13.6, z: 13.1, text: 'Un pin foudroyé, mort depuis des années. Quelqu\u2019un a accroché une lanterne à la branche la plus basse : elle brûle encore. Au pied, côté piste, la terre est piétinée et tachée.' },
    { id: 'sur_lanterne_ex', x: 17.0, z: 12.9, text: 'Une lanterne de piste, le réservoir à moitié. C\u2019est une vraie flamme.' },
    { id: 'sur_mulet_ex', x: 21.2, z: 17.7, text: 'Un mulet de bât, tué d\u2019un coup net au flanc. Le harnais est encore bouclé : on n\u2019a pas eu le temps de le décharger, ou on ne voulait pas. Le sang est déjà sombre.',
      alt: [{ si: 'sur_laisse_mourir|sur_vaincue|sur_paca_pacte', text: 'Un mulet de bât, tué d\u2019un coup net au flanc. Le harnais viendrait, à qui voudrait le couper. Tu le laisses.' }] },
    // ★ besace : le soulier ; fouille : la ration (le pain dur), la gourde est vide
    { id: 'sur_besace_ex', x: 18.8, z: 16.4, text: 'Une besace ouverte. Une gourde presque vide, un morceau de pain dur, et à deux pas, dans les aiguilles : ' + SOULIER, enter: 'give:ration;flag:sur_vu_soulier;flag:sur_f_besace',
      alt: [{ si: 'sur_f_besace', text: 'La besace est vide. Le soulier est toujours là.', enter: '' }] },
    { id: 'sur_soulier_ex', x: 22.9, z: 17.4, text: 'Dans les aiguilles, ' + SOULIER, enter: 'flag:sur_vu_soulier' },
    { id: 'sur_trainee_ex', x: 24.8, z: 16.9, enter: 'flag:sur_vu_trainee', text: 'Une traînée part du mulet et suit la piste vers l\u2019est. Elle n\u2019est pas d\u2019un corps qu\u2019on a traîné : trop étroite, trop interrompue. Quelqu\u2019un a marché, en saignant, jusqu\u2019à là-bas.' },
    { id: 'sur_ornieres_ex', x: 28.2, z: 16.4, enter: 'flag:sur_vu_ornieres', text: ORNIERES,
      alt: [{ si: 'observation>=3', enter: 'flag:sur_vu_ornieres;flag:sur_vu_pas', text: ORNIERES + ' Des pas d\u2019enfant, à côté des bottes, s\u2019arrêtent pile au bord des ornières. Ils ne repartent pas.' }] },
    { id: 'sur_borne_ex', x: 3.1, z: 13.7, text: 'Une borne de pierre, plus ancienne que la piste. Une flèche vers l\u2019ouest, et ce qui reste d\u2019un mot : …CHANT. Le Temple du couchant n\u2019est plus très loin. Personne n\u2019a déposé grand-chose au pied : une pierre posée sur une pierre, c\u2019est tout.' },
    { id: 'sur_fourre_ex', x: 24.0, z: 9.4, si: '!sur_paca_partie&!sur_paca_dit', enter: 'flag:sur_vu_paca', text: 'Quelqu\u2019un est là, dans le fourré, et ne vient pas.' },
    // sac de Paca, après la victoire (§9) : 1 ration, 4 $
    { id: 'sur_sac_paca', x: 25.2, z: 9.6, si: 'sur_vaincue&!sur_f_paca', enter: 'give:ration;gain:4;flag:sur_f_paca', text: 'Paca a laissé tomber son sac en partant. Dedans : une ration et quatre dollars.' },
  ],
  dialogues: DIALOGUES_SURVIVANT,
  // combat optionnel (§8) : Paca seulement, si le joueur l’attaque ; Roque jamais (il se rend au premier coup : dialogue « frappe »)
  combat: { nom: 'Paca, sous les pins', centre: { x: 18, z: 15 }, prefixe: 'sur_', drapeauxDebut: ['combat'],
    ennemis: [
      { id: 'paca', nom: 'Paca', sprite: 'gen_rc_paca', heading: cap(25.8, 8.9, [20, 16]), x: 25.8, z: 8.9, pv: 10, pa: 6, initiative: 6, arme: 'baton', competences: { melee: 35, armes: 15 }, rendSous: 0.5, fuitTour: 2, si: '!sur_paca_partie' } ],
    issues: { victoire: 'flag:sur_paca_partie;flag:sur_vaincue', fuite: 'rencontre:quitter', reddition: 'payMax:8;flag:sur_paca_partie', defaite: 'warp:rc_survivant_pins:30.5:17' },
    textes: { debut: 'Paca lève son bâton. Elle ne recule pas.',
      rend: { paca: 'Paca lève les mains.' },
      victoire: 'Paca lève les mains. « D\u2019accord. La piste est grande. » Elle rentre dans les pins, vers le sud.',
      fuite: 'Tu cours. Personne ne te poursuit.',
      reddition: 'Paca ramasse ce qui tombe. « Je t\u2019avais dit que j\u2019attendais. Voilà, j\u2019attends plus. »',
      defaite: 'Tu te réveilles plus bas sur la piste, la tête lourde. La lanterne, au loin, brûle encore \u2014 ou plus.' } },
};
