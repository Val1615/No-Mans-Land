// Rencontre du jalon 2 : « La citerne qui respire » (caravane marchande), d'après docs/rencontres/CARAVANE.md (Ocre, 7b5ba7a) :
// plan coté 35 × 26 m (§4), sans niveaux (tout au sol), dialogues du §6, combat du §8, butin du §9, entrée du §14, accroches du §12.
// Gabarits gris tant que les sprites d'Ocre (§10 : rc_car_*, rc_ds_relais_ufsa_3q, rc_ds_puits_3q, gen_rc_fierro/remedios/ciro/lena) ne sont pas
// dans assets/rencontres/manifest.json : décor absent -> volume gris (ph.h), PNJ absent -> silhouette grise (gestionnaire, core/rencontres.js).
// Drapeaux de scène car_* purgés à la sortie (journal de la case) ; drapeaux de monde monde_remedios_* jamais purgés, sauvegardés.
const D = (id, sprite, x, z, w, d, extra = {}) => ({ id, label: '', sprite, x, z, w, d, visitable: false, cue: null, named: false, solid: [], ...extra });
const R = (x, z, w, d, couv = 1) => ({ x, z, w, d, couv });
const FIN = [{ label: 'Partir.', next: 'end' }];

export const ITEMS_CARAVANE = { lame_ressort: { name: 'Lame de ressort', icon: 'rencontres/icone_lame_ressort_64.webp', icon128: 'rencontres/icone_lame_ressort_128.webp' } }; // objet de quête, sans valeur marchande (§9, §12.12)

// --- commerce (§6.2, §12.5) : stock limité par drapeaux, prix selon car_remise_ami > car_remise > car_remise_eau > base (if exclusifs) ---
const PALIERS = [['car_remise_ami', 'ami'], ['!car_remise_ami&car_remise', 'remise'], ['!car_remise_ami&!car_remise&car_remise_eau', 'eau'], ['!car_remise_ami&!car_remise&!car_remise_eau', 'base']];
const PRIX = { water: { base: 6, eau: 5, remise: 5, ami: 4 }, ration: { base: 8, remise: 7, ami: 6 }, poignard: { base: 15, remise: 14, ami: 12 }, pistolet: { base: 40, remise: 36, ami: 32 } };
const STOCK = { water: [['!car_eau1', 'car_eau1'], ['car_eau1&!car_eau2', 'car_eau2'], ['car_eau2&!car_eau3', 'car_eau3']], ration: [['!car_ration1', 'car_ration1'], ['car_ration1&!car_ration2', 'car_ration2']],
  poignard: [['!car_poignard', 'car_poignard']], pistolet: [['!car_pistolet', 'car_pistolet']] };
const NOMS = { water: 'Une eau', ration: 'Une ration', poignard: 'Le poignard', pistolet: 'Le pistolet' };
const prixDe = (it, p) => PRIX[it][p] ?? PRIX[it].base;
const VENTE = Object.keys(PRIX).flatMap(it => STOCK[it].flatMap(([si, fl]) => PALIERS.map(([pc, p]) => {
  const c = it === 'water' ? pc : pc.replace('&!car_remise_eau', '').replace('&car_remise_eau', ''); // car_remise_eau ne touche que l'eau
  if (it !== 'water' && p === 'eau') return null;
  return { label: `${NOMS[it]} (${prixDe(it, p)} $).`, if: `${si}&${c}`, action: `buy:${it}:${prixDe(it, p)};flag:${fl}`, next: 'vente' }; }).filter(Boolean)));
const tarif = p => `Eau filtrée, ${prixDe('water', p)} dollars${p === 'base' ? ' : c\u2019est l\u2019eau qui a fait la route' : ''}. Rations, ${prixDe('ration', p)}. Un poignard, ${prixDe('poignard', p)}. Et un pistolet, un seul, ${prixDe('pistolet', p)}, avec sa graisse.`;

export const DIALOGUES_CARAVANE = {
  rc_fierro: {
    start: { text: '(Il se lève à moitié.) « Halte. Les mains loin de la ceinture. » (Il ne lève pas son fusil. Il n\u2019en a pas besoin.)', options: [
      { label: '« Je suis de passage. »', next: 'passage' },
      { label: '« Vous vendez quelque chose ? »', next: 'vente' },
      { label: '« Je ne cherche pas d\u2019ennuis. Le Service les trouve tout seul. »', if: 'race_mutant', next: 'mutant' },
      { label: '« Joli fusil. Il est à vendre ? »', next: 'fusil' },
      { label: '[Attaquer]', action: 'combat:caravane_relais', next: 'end' } ] },
    passage: { text: '« La piste est à tout le monde. Passe au large du camp, pas entre les camions. »', enter: 'flag:car_salue', options: FIN },
    vente: { text: '« La Doña vend. À la remorque. Tu achètes, tu paies, tu repars. Tu traînes, je te regarde traîner. »', enter: 'flag:car_salue', options: FIN },
    mutant: { text: '(Il te regarde plus longtemps que les autres.) « Ici, personne ne pose la question. Va voir la Doña. Dis-lui que je t\u2019envoie. »', enter: 'flag:car_salue;flag:car_recommande', options: FIN },
    fusil: { text: '« Il est à moi depuis plus longtemps que toi tu marches. Non. »', options: [{ label: '…', next: 'start' }] },
    encore: { text: '« Tu es encore là. »', options: [
      { label: '« Une caravane a besoin d\u2019un garde comme toi ? »', next: 'garde' },
      { label: '« La piste est sûre, vers le nord ? »', next: 'nord' },
      { label: '« Il y avait une gourde dans le puits. »', if: 'car_gourde&!car_gourde_rendue&!car_fierro_froid', next: 'gourde' },
      { label: '[Attaquer]', action: 'combat:caravane_relais', next: 'end' },
      { label: '« Rien. »', next: 'end' } ] },
    garde: { text: '« Parce que les pistes ont des péages, et que je n\u2019aime pas payer. »', options: [{ label: '…', next: 'encore' }] },
    nord: { text: '« Une femme avec des lunettes de soudeur prend quinze dollars entre la douane et Dusk-Town. Elle prend, et elle laisse vivre. Plus au nord, le Service ne prend rien. Il emmène. »', options: [{ label: '…', next: 'encore' }] },
    gourde: { text: '« Il y avait. » (Il attend.)', options: [
      { label: 'Lui rendre une eau.', if: 'inv:water>=1', action: 'take:water;flag:car_gourde_rendue', next: 'gourde_ok' },
      { label: '« Je n\u2019ai rien vu. »', action: 'flag:car_fierro_froid', next: 'gourde_ko' } ] },
    gourde_ok: { text: '« Bien. Tu peux rester. »', options: FIN },
    gourde_ko: { text: '« Alors tu ne vois pas grand-chose. Fais attention où tu marches. »', options: FIN },
  },
  rc_remedios: {
    start: { text: '« Approche, approche. Pas trop près du comptoir, Fierro devient nerveux quand on touche à la marchandise. Je suis Remedios. Ici on vend, on achète, on troque, et on ne pose pas de questions. Toi, tu en as, des questions ? »', options: [
      { label: '« Montre-moi ce que tu vends. »', next: 'vente' },
      { label: '« J\u2019ai des choses à vendre. »', next: 'achat' },
      { label: '« Tes prix sont raides pour du sable. »', if: '!car_remise&!car_remise_eau&!car_remise_ami&!car_troc&!car_fierro_froid', test: 'troc:5', partialAt: 4, pass: 'remise', partial: 'remise_moitie', fail: 'remise_rate' },
      { label: '« Qu\u2019est-ce qui se passe sur les pistes ? »', next: 'nouvelles' },
      { label: '« Ta citerne penche. »', if: '!car_repare', next: 'panne' },
      { label: '« Fierro m\u2019envoie. »', if: 'car_recommande&!car_remise_ami', next: 'recommande' },
      { label: '« Ta citerne respire. »', if: 'car_vu_lena&!car_lena_secret&!car_regle', next: 'secret' },
      { label: '« Ciro dit que la citerne tient. »', if: 'car_repare&!car_merci', next: 'merci' },
      { label: '« Ton offre tient toujours ? »', if: 'car_merci&!car_escorte_dit', next: 'escorte' },
      { label: '[Attaquer]', action: 'combat:caravane_relais', next: 'end' },
      { label: '« Bonne route. »', next: 'end' } ] },
    vente: { text: `« ${tarif('base')} »`, alt: PALIERS.slice(0, 3).map(([si, p]) => ({ if: si, text: `« ${tarif(p)} »` })), options: [
      ...VENTE,
      { label: '« Plus d\u2019eau ? »', if: 'car_eau3', next: 'rupture' },
      { label: '« Ça ira. »', next: 'start' } ] },
    rupture: { text: '« Le reste est pour Dusk-Town. Tu veux qu\u2019Anselme me tire les oreilles ? »', options: [{ label: '…', next: 'vente' }] },
    pauvre: { text: '« Reviens quand tu auras de quoi. Le sable, lui, est gratuit. »', options: [{ label: '…', next: 'vente' }] },
    achat: { text: '« Je prends les armes et ce qui se mange. Pas les histoires. »', options: [
      { label: 'Le fusil (18 $).', if: 'inv:fusil>=1', action: 'sell:fusil:18', next: 'achat' },
      { label: 'Le pistolet (15 $).', if: 'inv:pistolet>=1', action: 'sell:pistolet:15', next: 'achat' },
      { label: 'Le poignard (5 $).', if: 'inv:poignard>=1', action: 'sell:poignard:5', next: 'achat' },
      { label: 'La barre (3 $).', if: 'inv:barre>=1', action: 'sell:barre:3', next: 'achat' },
      { label: 'Une ration (4 $).', if: 'inv:ration>=1', action: 'sell:ration:4', next: 'achat' },
      { label: '« Un carnet de livreur. »', if: 'inv:carnet_chauffeur>=1', next: 'carnet' },
      { label: '« Un cric de camion. »', if: 'inv:cric>=1', next: 'cric' },
      { label: '« C\u2019est tout. »', next: 'start' } ] },
    carnet: { text: '(Elle lit, lèvres serrées.) « "Ne s\u2019arrêter pour personne." C\u2019est Benito, il roule pour Anselme. Il s\u2019est arrêté quand même, hein ? Garde-le, Anselme voudra savoir. Benito est passé ici à pied il y a trois jours, vers la douane. Vivant, et très en colère. »', options: [{ label: '…', next: 'achat' }] },
    cric: { text: '« Ciro te l\u2019arracherait des mains. Va le lui montrer avant de me le vendre : il en a plus besoin que moi. »', options: [{ label: '…', next: 'achat' }] },
    remise: { text: '« Tu comptes comme ma mère. Bon : un dollar de moins sur tout, quatre sur le pistolet. »', enter: 'flag:car_remise;flag:car_troc', options: [{ label: '…', next: 'vente' }] },
    remise_moitie: { text: '« Un dollar de moins sur l\u2019eau, et c\u2019est parce que tu as de beaux yeux. »', enter: 'flag:car_remise_eau;flag:car_troc', options: [{ label: '…', next: 'vente' }] },
    remise_rate: { text: '« Le prix est le prix. Le sable, lui, est gratuit : regarde, il y en a partout. »', enter: 'flag:car_troc', options: [{ label: '…', next: 'start' }] },
    nouvelles: { text: '« Ce que j\u2019ai vu, ou ce qu\u2019on raconte ? »', options: [
      { label: '« Ce que tu as vu. »', next: 'vu' }, { label: '« Ce qu\u2019on raconte. »', next: 'raconte' }, { label: '« Et Dusk-Town ? »', next: 'dusk' } ] },
    vu: { text: '« Au nord, entre la douane et Dusk-Town, une femme avec des lunettes de soudeur fait payer le passage. Quinze dollars. Paie, ou passe par le lit à sec, mais ne discute pas trop : elle a des gamins sur les talus, et un mannequin qui arrête tout le monde. »', options: [{ label: '…', next: 'nouvelles' }] },
    raconte: { text: '« La Station de répartition, au sud, trie des conteneurs que personne ne vient chercher. Les machines d\u2019IO n\u2019ont pas de bras pour te voler, mais elles comptent les visages. Et à la douane ouest, les implants passent ; les autres font demi-tour, ou un détour par en dessous. »', options: [{ label: '…', next: 'nouvelles' }] },
    dusk: { text: '« On y monte. On y est attendus depuis un mois : une femme du ranch qui boit chez Hector, un gamin qui veut une place à n\u2019importe quel prix. Et des gens qui ne sortent pas le jour. Ceux-là aussi attendent. »', options: [{ label: '…', next: 'start' }] },
    panne: { text: '« Le ressort arrière. La lame maîtresse a cassé net sur une ornière. Ciro est dessous depuis ce matin. Si tu sais tenir une clé, va le voir. Si tu sais où trouver une lame de ressort, va le voir plus vite. »', enter: 'flag:car_q_panne', options: [{ label: '…', next: 'start' }] },
    recommande: { text: '(Elle jette un œil vers le puits, puis vers toi.) « Fierro n\u2019envoie jamais personne. Bon. Pour toi, l\u2019eau est à quatre, comme à Dusk-Town. Et si un jour tu dois partir loin sans qu\u2019on te demande tes papiers, cherche la caravane. Demande Remedios, partout où il y a de l\u2019ombre. »', enter: 'flag:car_remise_ami', options: [{ label: '…', next: 'start' }] },
    secret: { text: '(Elle pose son crayon.) « Une citerne, ça travaille quand il fait chaud. Le métal. »', options: [
      { label: '« Le métal ne frappe pas trois coups. »', next: 'secret2' }, { label: '« Si tu le dis. »', next: 'start' } ] },
    secret2: { text: '« … Bon. Écoute. À Dusk-Town, le Service passe et ramasse. Ceux qu\u2019il ramasse, on ne les revoit pas, ou on les revoit en bas, sous Steel. Moi, je transporte des gens qui ne veulent pas être ramassés, dans un sens ou dans l\u2019autre. Ils paient comme ils peuvent. Et toi, tu vas faire quoi de ça ? »', options: [
      { label: '« Rien. Je n\u2019ai rien entendu. »', action: 'flag:car_lena_secret;flag:car_remise_ami', next: 'client' },
      { label: '« Tu as encore de la place ? »', if: 'race_mutant', action: 'flag:car_lena_secret;flag:car_remise_ami', next: 'place' },
      { label: '« Combien vaut mon silence ? »', test: 'intimider:6', opposed: true, pass: 'racket_ok', fail: 'racket_rate' },
      { label: '« Le Service paie bien pour ce genre de cargaison. »', next: 'menace' } ] },
    client: { text: '« Alors tu es un client. Les clients, je les aime. L\u2019eau est à quatre pour toi. »', options: [{ label: '…', next: 'start' }] },
    place: { text: '« Pour toi, toujours. Pas aujourd\u2019hui : on monte vers Dusk-Town, et la place est prise. Mais la caravane repasse. »', options: [{ label: '…', next: 'start' }] },
    menace: { text: '« Le Service paie en balles, comme toujours. Fierro ! »', enter: 'combat:caravane_relais', options: [{ label: '…', next: 'end' }] },
    racket_ok: { text: '(Elle compte des billets, lentement, sans te regarder.) « Vingt-cinq. Prends-les, et prends la piste. Et sache une chose : la piste est longue, et Fierro a une très bonne mémoire. »', enter: 'gain:25;flag:car_regle;flag:car_racket;flag:monde_remedios_rackettee', options: FIN },
    racket_rate: { text: '« Non. Tu n\u2019as pas la tête de quelqu\u2019un qui va jusqu\u2019à la douane pour vendre une gamine. Tu as la tête de quelqu\u2019un qui part. Pars. »', options: [
      { label: '« Je pars. »', action: 'flag:car_regle;flag:car_menace', next: 'end' }, { label: '[Attaquer]', action: 'combat:caravane_relais', next: 'end' } ] },
    merci: { text: '« Ciro dit que tu as les mains propres et la tête dure. Chez lui, c\u2019est un compliment. Voilà quinze dollars, et deux bidons pour la route. Et j\u2019ai une autre offre. »', enter: 'gain:15;give:water:2;flag:car_merci', options: [{ label: '…', next: 'escorte' }] },
    escorte: { text: '« On repart dans une heure, vers la douane ouest, puis Dusk-Town. Un fusil de plus sur le toit, ça décourage les péages. Douze dollars à l\u2019arrivée, et la soupe en route. Tu viens ? »', options: [
      { label: '« Je viens. »', action: 'flag:car_escorte_dit', next: 'escorte_ok' }, { label: '« Pas ma direction. »', action: 'flag:car_escorte_dit', next: 'escorte_non' } ] },
    // extension « escorte » complète (§12.7) : rencontre:quitter:escorte = reprise du trajet + 12 $ + 3 cases sans tirage + 1 h (gestionnaire)
    escorte_ok: { text: '« Fierro te fera une place sur le toit du tracteur. Ne marche pas sur la bâche. »', options: [{ label: 'Monter sur le toit.', action: 'flag:car_regle;flag:car_escorte;rencontre:quitter:escorte', next: 'end' }] },
    escorte_non: { text: '« Comme tu veux. On te doit un service. La caravane a de la mémoire, elle aussi. »', enter: 'flag:car_regle', options: FIN },
  },
  rc_ciro: {
    start: { text: '(Deux jambes dépassent de sous la citerne. Une voix sort du dessous.) « Si tu viens pour regarder, il y a de meilleurs spectacles à Steel. Si tu viens pour aider, passe-moi la clé de dix-sept. Non, l\u2019autre. »', options: [
      { label: 'Passer la clé.', if: '!car_q_lame', next: 'cle' },
      { label: '« Ressort à lames. Lame maîtresse fendue à l\u2019œil, je parie. »', if: 'mecanique>=4&!car_q_lame', next: 'expert' },
      { label: '« Pour la lame… »', if: 'car_q_lame', next: 'besoin' },
      { label: '« Bon courage. »', next: 'end' } ] },
    cle: { text: '« Merci. (Un temps.) La lame maîtresse a cassé. Je peux serrer ce que je veux, sans lame la citerne repose sur l\u2019essieu, et l\u2019essieu ne va pas aimer la piste. »', enter: 'flag:car_q_lame', options: [{ label: '…', next: 'besoin' }] },
    expert: { text: '« Enfin quelqu\u2019un qui parle la langue. Oui. Il me faut une lame de la même largeur. Une lame de camion du Service ferait l\u2019affaire : ils roulent sur les mêmes essieux que nous, de vieux essieux de l\u2019UFSA. »', enter: 'flag:car_q_lame', options: [{ label: '…', next: 'besoin' }] },
    besoin: { text: '« Le relais avait un atelier, juste à côté. Les ateliers gardent tout. Fouille la ferraille. Une lame de la largeur de ta main, rapporte-la, et la Doña te paiera. Elle pleure en payant, mais elle paie. »', options: [
      { label: '« Comme celle-là ? »', if: 'inv:lame_ressort>=1', next: 'lame' },
      { label: '« J\u2019ai un cric de camion, si le tien s\u2019enfonce. »', if: 'inv:cric>=1&!car_cric', next: 'cric' },
      { label: '« Je vais voir. »', next: 'end' } ] },
    cric: { text: '(Il sort la tête : un visage rond, noir de graisse.) « Un cric à semelle large ! Le mien s\u2019enfonce dans le sable depuis ce matin. Je connais cette soudure : c\u2019est le cric d\u2019Anselme. Prête-le-moi, je te le rends à la fin. »', enter: 'flag:car_cric', options: [{ label: '…', next: 'besoin' }] },
    lame: { text: '« Bon acier. Rouillé dehors, sain dedans. Bon. Il faut soulever la citerne pendant que je serre. »', options: [
      { label: 'Glisser le cric d\u2019Anselme sous le châssis.', if: 'car_cric', next: 'repare' },
      { label: 'Tenir la citerne à l\u2019épaule.', test: 'force:5', pass: 'repare', fail: 'repare_mal' },
      { label: '« Je reviens avec de l\u2019aide. »', next: 'end' } ] },
    repare: { text: '(Une heure de jurons et de clés plus tard, la citerne se redresse.) « Elle tiendra jusqu\u2019à Dusk-Town. Après, Dieu et la piste décident. Va voir la Doña, elle te doit quelque chose. »', enter: 'take:lame_ressort;flag:car_repare;flag:monde_remedios_repartie', options: FIN },
    repare_mal: { text: '(La citerne glisse, retombe sur ta botte, se relève.) « Ça va, ta jambe ? … Elle tiendra. Toi, je ne sais pas. »', enter: 'hurt:2;take:lame_ressort;flag:car_repare;flag:monde_remedios_repartie', options: FIN },
    debout: { text: '« Elle tient. Toi aussi, apparemment. »', options: [
      { label: '« Pourquoi des trous sur le dessus de ta citerne ? »', if: 'car_vu_citerne&!car_vu_lena', next: 'trous' },
      { label: '« Bonne route. »', next: 'end' } ] },
    trous: { text: '« Pour que l\u2019eau respire. » (Il ne rit pas de sa propre blague.) « Demande à la Doña. Moi, je répare. »', options: FIN },
  },
  // examen de la citerne, une fois les trous vus : frapper (voix sans visage, aucun portrait)
  rc_citerne: {
    frapper: { text: '(Tu frappes deux coups sur la tôle.)', options: [{ label: 'Attendre.', next: 'reponse' }, { label: 'Laisser tomber.', next: 'end' }] },
    reponse: { text: '(Trois coups répondent, de l\u2019intérieur. Puis une trappe grince à l\u2019avant de la citerne.)', enter: 'flag:car_vu_lena;flag:monde_lena_connue', options: FIN },
  },
  rc_lena: {
    start: { text: '« Ne crie pas. Je sors juste respirer. Il fait cinquante degrés là-dedans. »', options: [
      { label: '« Tu voyages comme ça depuis longtemps ? »', next: 'voyage' },
      { label: '« Où vas-tu ? »', next: 'but' },
      { label: '« Moi aussi, ils me cherchent. »', if: 'race_mutant', next: 'pareil' },
      { label: 'Lui tendre une eau.', if: 'inv:water>=1&!car_lena_eau', action: 'take:water;flag:car_lena_aidee;flag:car_remise_ami;flag:car_lena_eau', next: 'eau' },
      { label: '« Retourne te cacher. »', next: 'end' } ] },
    voyage: { text: '« Depuis Novo Córdoba. Neuf jours. On s\u2019habitue. Non, on ne s\u2019habitue pas. »', options: [{ label: '…', next: 'start' }] },
    but: { text: '« À Dusk-Town. Et après, plus bas que Dusk-Town. Mon père a été pris dans une rafle il y a deux mois. Ceux qu\u2019ils prennent, ils les jettent sous Steel, dans la Sous-Ville. On dit qu\u2019à Dusk-Town, quelqu\u2019un connaît un chemin par en dessous. »', options: [
      { label: '« Je connais Dusk-Town. »', next: 'dusk' }, { label: '« Bonne chance. »', next: 'end' } ] },
    dusk: { text: '« Alors dis-moi une chose vraie sur Dusk-Town. »', options: [
      { label: '« Personne dans les rues. Tout le monde derrière les murs. »', next: 'dusk_ok' }, { label: '« Le Service y passe souvent. Très souvent. »', next: 'dusk_ok' } ] },
    dusk_ok: { text: '« Comme moi dans la citerne. Bien. Je saurai me cacher. »', enter: 'flag:car_lena_aidee', options: FIN },
    pareil: { text: '(Elle te regarde, longtemps, puis sourit pour la première fois.) « Alors tu sais. Un conseil, entre nous : si tu passes par la douane ouest, ne passe pas par la douane ouest. »', enter: 'flag:car_lena_aidee', options: [{ label: '…', next: 'start' }] },
    eau: { text: '« … Merci. Là-dedans, on boit la même eau que la citerne : aucune. »', options: [{ label: '…', next: 'start' }] },
  },
};

const COFFRE = 'gain:35;give:water:2;give:ration:2';
export const CARAVANE = {
  nom: 'La citerne qui respire', famille: 'caravane', terrains: ['piste'], biomes: ['desert'], poids: 1, lieu: 'rc_caravane_relais', prefixe: 'car_',
  duree: 1, dureeSi: { car_repare: 1 }, // heures ajoutées à la sortie : 1 h, +1 h si la citerne a été réparée (§1, §12.8)
  si: etat => !etat.flags.monde_remedios_vue, // caravane unique (§12.1) ; une case réglée ne tire plus (journal, gestionnaire)
  drapeauArrivee: 'monde_remedios_vue', // drapeau de monde : jamais purgé
  arrivee: 'Un camp de caravane, au pied du talus. Une citerne penche, une marmite fume.',
  arriveeRetour: 'Le camp de la caravane, au pied du talus.',
  scene: { size: { w: 35, d: 26 }, city: 'nml', ambiance: 'desert',
    ground: { base: '#a8875a', skin: 'g_rc_sable', tileM: 4, clean: true, marge: { skin: 'g_rc_sable', tileM: 4, m: 30, voile: 'rgba(14,10,6,.18)' },
      paint: [ { x: 0, z: 18, w: 35, d: 6, skin: 'g_rc_piste', tileM: 4 }, { x: 6, z: 18, w: 4, d: 4, skin: 'g_rc_piste_b', tileM: 4 }, { x: 22, z: 20, w: 4, d: 4, skin: 'g_rc_piste_c', tileM: 4 },
        { x: 8, z: 12, w: 8, d: 4, skin: 'g_rc_lit', tileM: 4 }, { x: 12, z: 12, w: 4, d: 4, skin: 'g_rc_lit_b', tileM: 4 },
        { x: 20, z: 8.5, w: 4, d: 4, skin: 'g_rc_sable_b', tileM: 4 }, { x: 4, z: 24, w: 4, d: 2, skin: 'g_rc_sable_c', tileM: 4 } ] },
    cadre: { desktop: { x: [14, 22], z: [17, 19] }, mobile: { x: [6.5, 28], z: [18, 20] } },
    buildings: [ // §14 + table de poses d'Ocre (manifeste) ; ph : volume gris de repli si une clé manquait
      D('car_traces', 'rc_car_traces_3q', 21, 13, 9, 5, { fond: true, ph: { h: 0.05 } }),
      D('car_talus1', 'rc_ds_talus_b_3q', 0, 0, 10, 8.5, { solid: [R(0, 5, 10, 3.5, 1), R(0, 0, 10, 5, 2)] }),
      D('car_talus2', 'rc_ds_talus_a_3q', 10, 0, 10, 8.5, { solid: [R(10, 5, 10, 3.5, 1), R(10, 0, 10, 5, 2)] }),
      D('car_talus3', 'rc_ds_talus_b_3q', 20, 0, 10, 8.5, { solid: [R(20, 5, 10, 3.5, 1), R(20, 0, 10, 5, 2)] }),
      D('car_talus4', 'rc_ds_talus_fin_3q', 30, 0, 5, 8.5, { solid: [R(30, 5, 5, 3.5, 1), R(30, 0, 5, 5, 2)] }),
      D('car_relais', 'rc_ds_relais_ufsa_3q', 1, 9.5, 7, 5, { ph: { h: 3.2 }, solid: [R(1.3, 9.7, 6.6, 4, 2), R(6.3, 14, 0.7, 0.5, 1)] }), // murs, pompe ; banc non solide (table de poses d'Ocre),
      D('car_ferraille', 'rc_car_ferraille_3q', 8.5, 10, 3, 2, { ph: { h: 1 }, solid: [R(8.5, 10, 3, 2, 1)] }),
      D('car_ballots_b', 'rc_car_ballots_b_3q', 12, 9.6, 2, 1.2, { ph: { h: 1.1 }, solid: [R(12, 9.6, 2, 1.2, 1)] }),
      D('car_tracteur', 'rc_car_tracteur_3q', 14, 9.5, 7.5, 2.6, { ph: { h: 3.3 }, solid: [R(14, 9.5, 7.5, 2.6, 2)] }),
      D('car_tracteur_texte', 'rc_car_tracteur_3q_texte', 14, 9.5, 7.5, 2.6, { etage: 1 }), // lettrage : calque normal (ni additif ni retourné), sur l'emprise du tracteur
      D('car_remorque', 'rc_car_remorque_etal_3q', 22.5, 9.8, 6, 3.2, { ph: { h: 3 }, solid: [R(22.5, 9.8, 6, 2.5, 2), R(22.5, 12.3, 6, 0.7, 1)] }),
      D('car_citerne', 'rc_car_citerne_3q', 29, 10.5, 5.5, 2.4, { ph: { h: 2.6 }, solid: [R(29, 10.5, 5.5, 2.4, 2)] }),
      D('car_ballots', 'rc_car_ballots_3q', 20.4, 12.4, 2, 1.2, { ph: { h: 1.2 }, solid: [R(20.4, 12.4, 2, 1.2, 1)] }),
      D('car_puits', 'rc_ds_puits_3q', 12.5, 13, 2, 2, { ph: { h: 2.6 }, solid: [R(12.6, 13.1, 1.8, 1.8, 1)] }),
      D('car_bivouac', 'rc_car_bivouac_3q', 16, 13.5, 3, 3, { ph: { h: 0.6 }, solid: [R(17, 14.5, 1, 1, 0)] }),
      D('car_bache', 'rc_emb_bache_cache_3q', 30, 14.5, 3.5, 3.5, { solid: [R(30, 14.5, 3.5, 0.5, 1), R(33, 15, 0.5, 3, 1)] }),
      D('car_panneau', 'rc_ds_panneau_ufsa_3q', 1.2, 17, 0.6, 0.2, { solid: [R(1.4, 17, 0.2, 0.2, 0)] }),
      D('car_rochers_b', 'rc_ds_rochers_b_3q', 6, 24.4, 3, 1.5, { solid: [R(6, 24.4, 3, 1.5, 1)] }),
      D('car_rochers', 'rc_ds_rochers_3q', 24, 24.3, 3, 1.5, { solid: [R(24, 24.3, 3, 1.5, 1)] }),
    ],
    enseignes: [{ id: 'car_feu', building: 'car_bivouac', effet: 'pulse', periode: 5.5, intensite: 0.8,
      flaque: { r: 3, x: 17.5, z: 15, couleur: '#ff963c', i: 0.7 } }], // flaque nocturne liée à l'enseigne (ARCHI « Flaque nocturne ») : 3 m sous le foyer, même pulse, nulle le jour
    props: [{ sprite: 'barrel', x: 12, z: 16.6, fp: [0.6, 0.6] }], // fût vide près du puits (assets/reused, réutilisé tel quel)
    entree: { x: 1.5, z: 21, heading: Math.PI / 2 },
    sorties: [
      { id: 'ouest', label: 'Demi-tour (carte)', x: 0.6, z: 21, zone: { x0: 0, x1: 0.9, z0: 18, z1: 24 }, effet: 'halte' },
      { id: 'est', label: 'Reprendre la piste', x: 34.4, z: 21, zone: { x0: 34.1, x1: 35, z0: 18, z1: 24 }, effet: 'reprise' } ] }, // jamais gardée (§12.2)
  declencheurs: [{ id: 'T1', zone: { x: 7, z: 9, w: 2, d: 15 }, si: '!car_t1&!car_salue&!car_regle', enter: 'flag:car_t1', dialogue: 'rc_fierro' }],
  pnj: [
    { id: 'rc_fierro', name: 'Fierro', sprite: 'gen_rc_fierro', x: 13.2, z: 16.8, faceTo: [1.5, 21], dialogue: 'rc_fierro', entrees: [{ si: 'car_salue', node: 'encore' }], si: '!car_vaincue', cacheCombat: true, bloque: false },
    { id: 'rc_remedios', name: 'Remedios', sprite: 'gen_rc_remedios', x: 25.5, z: 14.3, faceTo: [1.5, 21], dialogue: 'rc_remedios', si: '!car_vaincue', cacheCombat: true, bloque: false },
    { id: 'rc_ciro_dessous', name: 'Ciro', sprite: 'gen_rc_ciro_dessous', gabaritH: 0.35, x: 31.83, z: 13.75, /* ancre = bas du sprite : talons en (31,5 ; 13,27) */ faceTo: [31.5, 20], fige: true, sansMiroir: true, dialogue: 'rc_ciro', si: '!car_repare&!car_vaincue', cacheCombat: true, bloque: false, portraitDe: 'gen_rc_ciro' },
    { id: 'rc_ciro', name: 'Ciro', sprite: 'gen_rc_ciro', x: 30, z: 14.2, faceTo: [25.5, 14.3], dialogue: 'rc_ciro', entrees: [{ si: 'car_repare', node: 'debout' }], si: 'car_repare&!car_vaincue', cacheCombat: true, bloque: false },
    { id: 'rc_lena', name: 'Lena', sprite: 'gen_rc_lena', x: 28.75, z: 14.2, faceTo: [1.5, 21], dialogue: 'rc_lena', si: 'car_vu_lena&!car_vaincue', cacheCombat: true, bloque: false },
    { id: 'rc_citerne', name: 'La citerne', sprite: 'gen_rc_lena', x: 31.5, z: 13.2, dialogue: 'rc_citerne', si: 'car_jamais', fige: true, portrait: false, bloque: false }, // voix de la citerne : jamais visible
  ],
  // examens et fouilles (§3, §9) ; alt [{ si, text, enter }] : variante selon l'état (premier qui tient), sinon text / enter
  points: [
    { id: 'car_relais_ex', x: 4.5, z: 15, text: 'Un relais de l\u2019UFSA. Sur le mur, à hauteur d\u2019homme, des centaines de traits gravés au couteau, par paquets de cinq. Chaque caravane qui passe en ajoute un. Les plus vieux sont presque effacés par le sable ; il y a un long blanc, puis les traits reprennent, plus espacés. Le dernier est frais.',
      alt: [{ si: 'observation>=4', enter: 'flag:car_indice_cercles', text: 'Un relais de l\u2019UFSA. Sur le mur, des centaines de traits gravés au couteau, par paquets de cinq : un par caravane. Le dernier est frais. À côté du dernier trait, un petit cercle. Puis un deuxième, plus ancien. Et d\u2019autres, en remontant. Pas à chaque caravane.' }] },
    { id: 'car_panneau_ex', x: 1.5, z: 17.6, text: 'Le panneau a perdu ses lettres. Quelqu\u2019un y a peint à la chaux un seau et une flèche vers le relais. Le seau a été barré, plus tard, d\u2019un trait noir.' },
    { id: 'car_puits_ex', x: 13.5, z: 15.5, text: 'Un puits sec. Le treuil tourne encore. Au bout de la corde, le seau remonte plein de sable fin. Les caravanes ne s\u2019arrêtent plus ici pour l\u2019eau, mais pour l\u2019ombre du talus et le seul sol plat à dix kilomètres.',
      alt: [{ si: 'observation>=4&!car_gourde', enter: 'give:water;flag:car_gourde', text: 'Un puits sec ; le seau remonte plein de sable. Accrochée à un clou, juste sous la margelle : une gourde pleine. Quelqu\u2019un garde sa réserve là où personne ne cherche plus d\u2019eau. Tu la prends.' }] },
    { id: 'car_ferraille', x: 10, z: 12.6, si: 'car_q_lame&!inv:lame_ressort>=1&!car_repare', tests: ['mecanique:4', 'force:6'], pass: 'give:lame_ressort', fail: '',
      text: (s, ok) => ok ? 'Sous la rouille, une lame de ressort de la largeur de ta main. Elle vient.' : 'Des lames trop étroites, des jantes, du sable.',
      empty: 'L\u2019ancien atelier du relais : jantes, un demi-essieu, un paquet de lames de ressort soudées par la rouille.' },
    { id: 'car_portiere_ex', x: 15.2, z: 12.6, text: 'Sur la portière : TRANSPORTES REMEDIOS — NOVO CÓRDOBA · DUSK-TOWN. Le nom de Dusk-Town a été repeint plus récemment que le reste.' },
    { id: 'car_bivouac_ex', x: 17.5, z: 17, text: 'Des haricots qui mijotent sur trois pierres. Une fumée mince monte droit : pas de vent.',
      alt: [{ si: 'observation>=3', enter: 'flag:car_indice_cuilleres', text: 'Des haricots qui mijotent sur trois pierres. Une fumée mince monte droit : pas de vent. Quatre gamelles, cinq cuillères. Trois personnes en vue.' }] },
    { id: 'car_traces_ex', x: 24, z: 16.5, text: 'Les camions sont entrés en arc, comme on range des chariots. Sous la citerne, trois trous de cric : trois essais, le sable n\u2019a pas tenu.' },
    // citerne : Observation 5, ou 3 avec un indice (cercles, cuillères) ; trous vus -> frapper (§6.4, §12.6)
    { id: 'car_citerne_ex', x: 33.5, z: 13.6, text: 'Une citerne d\u2019eau sur remorque, penchée vers l\u2019arrière : le ressort a lâché. Sous la vanne, le sable est sec. Pas une goutte.',
      alt: [{ si: 'observation>=5|observation>=3&car_indice_cercles|observation>=3&car_indice_cuilleres|car_vu_citerne', enter: 'flag:car_vu_citerne', text: 'Une citerne d\u2019eau sur remorque, penchée vers l\u2019arrière. Sous la vanne, le sable est sec. Sur le dessus, une rangée de petits trous percés à la mèche, propres, récents. On n\u2019aère pas de l\u2019eau.' }],
      dialogue: 'rc_citerne:frapper', dialogueSi: 'car_vu_citerne&!car_vu_lena&!car_vaincue' },
    // comptoir et coffre : vol (Discrétion 7, échec = combat) avant tout règlement ; libre après une victoire
    { id: 'car_coffre', x: 25.5, z: 13.6, test: 'discretion:7', testSi: '!car_regle&!car_f_coffre', pass: COFFRE + ';flag:car_vole;flag:car_f_coffre', fail: 'combat:caravane_relais',
      text: (s, ok) => ok ? 'Le cadenas cède sans bruit. 35 dollars, deux bidons, deux rations.' : 'Le cadenas claque. Remedios se retourne : « Fierro ! »',
      alt: [{ si: 'car_vaincue&!car_f_coffre&!car_pistolet', enter: COFFRE + ';give:pistolet;flag:car_f_coffre;flag:car_pistolet', text: 'Le coffre : 35 dollars, deux bidons, deux rations et le pistolet, dans sa graisse.' },
        { si: 'car_vaincue&!car_f_coffre', enter: COFFRE + ';flag:car_f_coffre', text: 'Le coffre : 35 dollars, deux bidons, deux rations.' },
        { si: 'car_regle|car_f_coffre', enter: '', text: 'Le flanc de la remorque, rabattu sur deux chaînes, fait comptoir. Dessous, un coffre cadenassé. Remedios ne s\u2019en éloigne jamais de plus de deux pas.' }] },
    { id: 'car_bache_ex', x: 29.8, z: 16.2, text: 'Les bidons bleus de la caravane, les mêmes qu\u2019on voit partout entre Dusk-Town et la douane. Fierro a posé sa couverture juste à côté.',
      alt: [{ si: 'car_vaincue&!car_f_bache', enter: 'give:water:3;flag:car_f_bache', text: 'Sous la bâche : trois bidons bleus. Personne ne t\u2019en empêche.' }] },
  ],
  dialogues: DIALOGUES_CARAVANE,
  combat: { nom: 'Le camp de la caravane', centre: { x: 22, z: 16.5 }, prefixe: 'car_', drapeauxDebut: ['t1', 'combat'],
    ennemis: [
      { id: 'fierro', nom: 'Fierro', sprite: 'gen_rc_fierro', x: 13.2, z: 16.8, pv: 16, pa: 7, initiative: 7, arme: 'fusil', competences: { melee: 35, armes: 60 } },
      { id: 'remedios', nom: 'Remedios', sprite: 'gen_rc_remedios', x: 25.5, z: 14.3, pv: 12, pa: 6, initiative: 4, arme: 'pistolet', competences: { melee: 20, armes: 40 }, rendSous: 0.5 },
      { id: 'ciro', nom: 'Ciro', sprite: 'gen_rc_ciro', x: 31, z: 14.2, pv: 12, pa: 6, initiative: 6, arme: 'barre', competences: { melee: 40, armes: 15 }, fuitTour: 2 } ], // Lena jamais au combat
    issues: { victoire: 'flag:car_regle;flag:car_vaincue;flag:monde_remedios_vaincue', fuite: 'rencontre:quitter', reddition: 'payMax:15;flag:car_regle', defaite: 'payMax:15;give:water;flag:car_regle;warp:rc_caravane_relais:1.5:21' },
    textes: { debut: 'Fierro relève son fusil. « Tout le monde à couvert ! »',
      victoire: 'Remedios lève les mains, le crayon toujours entre les doigts. « Prends le coffre. Laisse-nous la citerne. » Fierro ne dit rien. Il te regarde, et il retient ton visage.',
      fuite: 'Tu cours. Derrière toi, personne ne te poursuit : une caravane ne quitte pas ses camions.',
      reddition: 'Fierro ramasse tes billets du bout du canon. « Maintenant, la piste. »',
      defaite: 'Tu te réveilles à l\u2019ombre du panneau. Quelqu\u2019un a laissé un bidon près de ta main. La caravane ne laisse personne sans eau, même ceux qui l\u2019ont attaquée.' } },
};
