// Rencontre du jalon 2, lot 2 : « L’écluse des Verriers » (créatures mutantes, biome verre), d’après docs/rencontres/MUTANTS.md (Ocre, 84d7f40 + 1bafb18 + d55b630 + d6a3755) :
// plan coté 36 × 30 m (§4), sans niveaux (canal ensablé, tout au sol), dialogues du §6, combat du §8 (contre la harde seulement), butin du §9, entrée du §14,
// poses du §15, accroches du §12. Les Verriers ne se battent jamais : [Attaquer] chez eux mène au nœud commun fuient (rc_tecla). Le lore est câblé tel quel.
// Drapeaux de scène ver_* purgés à la sortie (journal de la case) ; drapeaux de monde monde_verriers_* et monde_message_ines jamais purgés, sauvegardés.
const D = (id, sprite, x, z, w, d, extra = {}) => ({ id, label: '', sprite, x, z, w, d, visitable: false, cue: null, named: false, solid: [], ...extra });
const R = (x, z, w, d, couv = 1) => ({ x, z, w, d, couv });
const FIN = [{ label: 'Partir.', next: 'end' }];
const SUITE = next => [{ label: '…', next }];
const cap = (x, z, [fx, fz]) => Math.atan2(fx - x, fz - z); // cap initial d’une unité de combat (même formule que faceTo)
const BETE = [-1, 1]; // chanchos : l’image de face regarde au sud-ouest (gauche de l’écran), celle de dos au nord-est (droite)

export const ITEMS_VERRIERS = { perles_verre: { name: 'Perles de verre' } }; // objet d’échange, sans prix de vente au jalon 2 (§9, §12.13) : il se montre, il ne se vend pas

const ATTAQUER = { label: '[Attaquer]', next: 'rc_tecla/fuient' }; // §6 : pas de combat contre les Verriers

export const DIALOGUES_VERRIERS = {
  rc_balta: {
    start: { text: '(Il tient son fusil canon vers le sol. Il ne te regarde qu’à moitié : l’autre moitié surveille l’écluse.) « Pas plus loin. Pas avant que je t’aie vu le cou. »', options: [
      { label: '« Mon cou ? »', next: 'col' },
      { label: '(Tu baisses ton col sans qu’il le redemande.)', if: 'race_mutant', next: 'col_mutant' },
      { label: '« Je passe sur la piste. Je ne m’arrête pas. »', next: 'passe' },
      { label: '« Je m’en vais. »', next: 'end' } ] },
    col: { text: '« À Dusk-Town, le Service fait baisser les cols. Ici aussi on regarde. Pas pour la même raison. Baisse-le. »', options: [
      { label: '(Baisser le col.)', if: 'race_humain', next: 'col_humain' },
      { label: '(Baisser le col.)', if: 'race_augmente|race_cyborg', next: 'implant' },
      { label: '(Baisser le col.)', if: 'race_mutant', next: 'col_mutant' },
      { label: '« Non. »', next: 'refus' } ] },
    col_mutant: { text: '(Il regarde, longtemps. Puis il remet le fusil à l’épaule.) « Bon. Ça t’a pris où, à toi ? … Laisse. On ne se demande pas ça. »', enter: 'flag:ver_salue;flag:ver_confiance', options: SUITE('harde_intro') },
    col_humain: { text: '(Il regarde ta peau intacte, puis tes mains, puis tes bottes.) « Rien. Alors tu viens de chez les gens de bonne peau. Tu ne portes pas leur gris. C’est déjà ça. »', enter: 'flag:ver_salue', options: SUITE('harde_intro') },
    implant: { text: '(Il voit la cicatrice de l’implant et recule d’un pas, sans lever son arme.) « Un implant d’IO parle à qui l’écoute. Et le Service écoute. Reste là où je te vois. »', enter: 'flag:ver_salue;flag:ver_mefiance', options: SUITE('harde_intro') },
    refus: { text: '« Alors la piste est par là. Elle est large. »', enter: 'flag:ver_salue;flag:ver_mefiance', options: FIN },
    passe: { text: '« Bien. Continue. Et ne traîne pas sur le verre : il ne fait pas de cadeau aux gens de bonne peau. »', enter: 'flag:ver_salue', options: FIN },
    harde_intro: { text: '(Un grognement, de l’autre côté du parapet. Puis un choc sourd contre une porte.) « Les chanchos. Ils sont descendus dans la cuve à l’aube. Le petit s’est enfermé dans la cabane, avec toute notre eau. Ils sentent l’eau. Moi, j’ai trois balles. L’an dernier, le gris en a pris deux sans ralentir. »', options: [
      { label: '« Je peux aider. »', next: 'aider' },
      { label: '« Des chanchos ? »', next: 'chanchos' },
      { label: '« Ce n’est pas mon problème. »', next: 'pasmon' } ] },
    chanchos: { text: '« Des cochons de cendre. Ils vivent dans le verre, comme nous, et ils mangent ce que le verre laisse pousser, c’est-à-dire presque rien. Ils boivent la rosée sur les dalles, la nuit. Ce sont des bêtes, et ils ont soif. Je ne leur en veux pas. Mais c’est notre eau qu’ils veulent. »', options: [
      { label: '« Je peux aider. »', next: 'aider' },
      { label: '« Ce n’est pas mon problème. »', next: 'pasmon' } ] },
    aider: { text: '« Va voir la vieille, au four. C’est elle qui décide comment on fait. Moi, je tiens la cale. »', enter: 'flag:ver_q_harde', options: FIN },
    pasmon: { text: '« Personne ne te l’a demandé. »', options: FIN },
    encore: { text: '« Encore là. »', options: [
      { label: '« Je peux aider, pour les bêtes. »', if: '!ver_q_harde', next: 'aider' },
      { label: '« Le gris. Il se bat comment ? »', if: 'ver_q_harde&!ver_conseil_gris', next: 'gris' },
      { label: '« Ta jambe saigne. Montre. »', if: '!ver_soigne&!ver_soin_dit', test: 'medecine:4', pass: 'soin', fail: 'soin_rate' },
      { label: '« Tu as l’air d’attendre quelqu’un. »', if: '!ver_ines', next: 'ines' },
      { label: '« J’ai croisé une fille de Novo Córdoba qui cherche son père dans la Sous-Ville. Lena. »', if: 'ver_ines&monde_lena_connue&!ver_message_ines', next: 'lena' },
      ATTAQUER,
      { label: '« Plus tard. »', next: 'end' } ] },
    gris: { text: '« Il charge droit, comme un camion. Il s’arrête quand il a mal, et les autres s’arrêtent quand il s’arrête. Tape le gris. Laisse les jeunes. »', enter: 'flag:ver_conseil_gris', options: SUITE('encore') },
    soin: { text: '(Tu laves la morsure au mauvais alcool de Rufina et tu serres un vrai pansement. Il ne bronche pas.) « … Tu as des mains, toi. »', enter: 'flag:ver_soigne;flag:ver_confiance', options: SUITE('encore') },
    soin_rate: { text: '« Laisse. Ça a vu pire. »', enter: 'flag:ver_soin_dit', options: SUITE('encore') },
    ines: { text: '« Ma femme. Ines. Ils l’ont prise au marché de Dusk-Town, il y a trois hivers, avec douze autres. Le Service appelle ça un "transfert". En bas, on dit "la Sous-Ville". Personne n’en revient. Moi, j’attends au bord du verre, parce que c’est le seul endroit où ils ne viennent pas me chercher. »', enter: 'flag:ver_ines', options: SUITE('encore') },
    lena: { text: '(Il se tait un moment.) « La Sous-Ville. Toujours la Sous-Ville. » (Il fouille sa poche, en sort une perle rouge.) « Si tu la revois : Ines, de Dusk-Town, celle qui chante faux. Qu’elle demande, en bas. Donne-lui ça, Ines la reconnaîtra. »', enter: 'give:perles_verre;flag:ver_message_ines;flag:monde_message_ines', options: SUITE('encore') },
    apres: { text: '(Il a reposé le fusil contre le parapet.) « Le petit est dehors. L’eau aussi. Je te dois une balle. Je n’en ai que trois, alors c’est beaucoup. »', options: [
      { label: '« Tu as l’air d’attendre quelqu’un. »', if: '!ver_ines', next: 'ines' },
      { label: '« Lena, de Novo Córdoba, cherche son père dans la Sous-Ville. »', if: 'ver_ines&monde_lena_connue&!ver_message_ines', next: 'lena' },
      { label: '« Garde tes balles. »', next: 'end' } ] },
  },
  rc_tecla: {
    start: { text: '(Elle tourne la tête vers ta voix avant que tu aies parlé.) « Tu marches comme quelqu’un qui a de bonnes bottes. Assieds-toi, ou pas. Le four ne fait pas la différence. »', options: [
      { label: '« Je suis des vôtres. »', if: 'race_mutant&!ver_eau_offerte', next: 'mutant' },
      { label: '« Qui êtes-vous ? »', next: 'qui' },
      { label: '« Les chanchos. Comment je peux aider ? »', if: '!ver_harde_partie', next: 'harde' },
      { label: '« La cuve est vide. Le petit peut sortir. »', if: 'ver_harde_partie&!ver_merci', next: 'merci' },
      { label: '« Le verre, là-haut. Qu’est-ce que c’est ? »', next: 'verre' },
      { label: '« J’ai croisé la caravane de Remedios. »', if: 'monde_remedios_vue', next: 'remedios' },
      { label: '« Les perles, sur la porte de l’écluse. »', if: 'ver_indice_perles&!ver_perles_dites', next: 'perles' },
      { label: '« Je connais un sergent à Big Larry qui paierait cher pour savoir où vous dormez. »', if: '!ver_regle', next: 'menace' },
      { label: '[Attaquer]', next: 'fuient' },
      { label: '« Je m’en vais. »', next: 'end' } ] },
    mutant: { text: '« Des vôtres. » (Elle tend la main, paume ouverte, et attend.) « Ici, on ne dit pas ça. On dit : "Tu as soif ?" Et l’autre répond. »', options: [
      { label: '« J’ai soif. »', next: 'mutant_eau' },
      { label: '« Ils m’ont pris, une fois. J’ai sauté du camion. »', if: 'origine_rafle', next: 'rafle' },
      { label: '« J’ai grandi sous un foulard, à Dusk-Town. »', if: 'origine_sables', next: 'sables' },
      { label: '« Je viens de plus loin que la carte. »', if: 'origine_errant', next: 'errant' } ] },
    mutant_eau: { text: '« Bois. » (Une gourde de terre, l’eau tiède et propre.) « Si un jour il te faut un endroit où le Service ne vient pas, il y a de la place dans la coque. Pas de lit, mais pas de camion non plus. »', enter: 'give:water;flag:ver_eau_offerte;flag:ver_confiance', options: SUITE('start') },
    rafle: { text: '« Alors tu as sauté au-dessus du verre, ou pas loin : leurs camions passent par la piste du cratère. On en a ramassé, des sauteurs. Certains avaient arraché la plaque du camion, comme un trophée. Garde la tienne. Elle te rappellera la route. »', enter: 'flag:ver_eau_offerte;flag:ver_confiance', options: SUITE('start') },
    sables: { text: '« Alors Sol t’a vu grandir. Sol nous monte du fil et des aiguilles, une fois par saison. Dis-lui que la vieille du four a encore ses dix doigts. »', enter: 'flag:ver_eau_offerte;flag:ver_confiance', options: SUITE('start') },
    errant: { text: '« Tu sens l’eau, alors, comme Nilo. Dis-moi où elle est, ici. »', options: [{ label: '(Tu fermes les yeux. Sous la proue de la péniche, à l’ouest. Profond.)', next: 'errant_ok' }] },
    errant_ok: { text: '(Elle rit, pour la première fois.) « La citerne sous la proue. Même Balta ne la trouve pas sans moi. Prends un bidon, pour le nez. Et ne le dis à personne d’autre. »', enter: 'give:water;flag:ver_eau_offerte;flag:ver_confiance;flag:ver_citerne_dite', options: SUITE('start') },
    qui: { text: '« Ceux qui vivent ici. À Dusk-Town, on nous appelait les Verriers, parce qu’on fond le verre. Le Service, lui, ne nous appelle pas : il ne vient pas jusqu’ici. »', options: SUITE('start') },
    verre: { text: '« Il y a eu un feu dans le ciel, il y a très longtemps. Le sable a fondu. Big Larry, le trou, c’est par là. Le verre garde au fond de lui une chaleur qu’on ne sent pas. Les gens de bonne peau y laissent leurs cheveux en une saison. Nous, en dix ans. C’est toute la différence, et cette différence, c’est une maison. »', options: SUITE('start') },
    harde: { text: '« Trois jeunes et le gris. Ils ont soif, ils ont senti les jarres. Balta veut les tirer, avec ses trois balles. Il y a d’autres façons. »', options: [
      { label: '« Leur donner de l’eau, ailleurs. »', next: 'leurre' },
      { label: '« Le feu. Les bêtes ont peur du feu. »', next: 'feu' },
      { label: '« Ils finiront par partir tout seuls ? »', next: 'attendre' },
      { label: '« Je m’en occupe. À ma façon. »', next: 'combat_dit' },
      { label: '« Plus tard. »', next: 'start' } ] },
    leurre: { text: '« De l’eau, au bout de la cuve. Monte sur le quai nord par l’escalier, va jusqu’à la rigole de l’est et verse-la dedans, doucement. Le vent vient de l’ouest : ils la sentiront, et la rigole les mènera dans le verre. Un bidon suffit, si tu le fais bien. Le petit peut t’en passer un par la fenêtre, si tu n’en as pas. »', enter: 'flag:ver_q_leurre', options: SUITE('harde') },
    feu: { text: '« Celles-là aussi ont peur du feu, si on le leur met sous le groin. Rufina te donnera un tison. Mais le gris ne recule pas devant une flamme qui tremble. »', enter: 'flag:ver_q_tison', options: SUITE('harde') },
    attendre: { text: '« À la nuit, quand le verre refroidit, ils retournent lécher la rosée sur les dalles. Si tu restes, tu attends avec nous. Quatre heures, peut-être cinq. Le petit aura chaud, mais il a toute l’eau. »', options: [
      { label: '« J’attends avec vous. »', next: 'attendu' },
      { label: '« Pas le temps. »', next: 'harde' } ] },
    // l’attente ne change pas la lumière de la scène : le texte raconte la nuit, l’heure avance à la sortie (dureeSi ver_attendu : +4 h, §12.11)
    attendu: { text: '(Le soleil descend sur le verre. Balta ne lâche pas la cuve des yeux. Rufina fait cuire des galettes sur la sole du four, et Tecla te raconte Dusk-Town avant les rafles, quand on ne baissait pas les cols. À la nuit, le gris lève le groin, renifle vers le nord, et la harde remonte dans le verre. Nilo sort de la cabane en clignant des yeux.)', enter: 'flag:ver_attendu;flag:ver_harde_partie;flag:ver_nilo_libre;pv:3', options: SUITE('merci') },
    combat_dit: { text: '« Alors vise le gris. Et ne tue que si tu ne peux pas faire autrement : un chancho mort, c’est de la viande, mais c’est aussi une mère qui ne revient pas l’année d’après. »', enter: 'flag:ver_q_harde', options: FIN },
    merci: { text: '(Nilo a couru jusqu’au four, puis il s’est arrêté net à deux pas : il a quatorze ans et ne veut pas qu’on le voie courir.) « Il est entier. L’eau aussi. »', enter: 'give:water:2;give:perles_verre:3;flag:ver_merci;flag:ver_nilo_libre;flag:monde_verriers_amis', options: SUITE('merci2') },
    merci2: { text: '« Les perles, c’est Rufina qui les fait. Celles-là, on ne les compte pas : elles sont pour toi. Montre-les sur la piste de Novo Córdoba, à qui il faut. Ceux qui savent sauront. »', options: SUITE('start') },
    remedios: { text: '(Elle sourit.) « Remedios. Sa citerne fuit toujours par le haut ? »', options: [
      { label: '« Elle ne fuit pas. Elle respire. »', if: 'monde_lena_connue', next: 'filiere' },
      { label: '« Elle a réparé. Elle monte vers Dusk-Town. »', if: 'monde_remedios_repartie', next: 'remedios_ok' },
      { label: '« Je ne sais pas. »', next: 'remedios_non' } ] },
    filiere: { text: '« Alors tu sais. Ce qui monte dans sa citerne descend parfois ici. On garde les gens quelques jours au bord du verre, le temps que les camions du Service se lassent. Ensuite, Remedios les reprend, ou Sol les fait entrer à Dusk-Town par en dessous. Rufina est arrivée comme ça. »', enter: 'flag:ver_filiere_dite;flag:ver_confiance', options: SUITE('start') },
    remedios_ok: { text: '« Bien. Elle passera par ici avant la ville. Elle passe toujours par ici avant la ville. »', options: SUITE('start') },
    remedios_non: { text: '« Alors c’est que tu ne sais pas. C’est très bien comme ça. »', options: SUITE('start') },
    perles: { text: '« Demande à Rufina. Ce sont ses perles, et c’est son compte. »', options: SUITE('start') },
    menace: { text: '(Tecla ne bouge pas. Balta, lui, a bougé.) « Un sergent à Big Larry. Ils ont tous un sergent à Big Larry. »', options: [
      { label: '« Vingt dollars, et je l’oublie. »', test: 'intimider:7', opposed: true, pass: 'menace_ok', fail: 'menace_rate' },
      { label: '« C’était une façon de parler. »', next: 'parler' } ] },
    parler: { text: '« Au bord du verre, les façons de parler font des morts. »', enter: 'flag:ver_mefiance', options: SUITE('start') },
    menace_ok: { text: '« Rufina, donne-lui la boîte. » (Rufina compte. Ça ne fait pas vingt : quatorze dollars et trois perles.) « C’est tout ce qu’on a. Prends-le. Demain, il n’y aura plus personne ici à vendre : on a l’habitude. »', enter: 'gain:14;give:perles_verre:3;flag:ver_regle;flag:ver_racket;flag:monde_verriers_menaces', options: FIN },
    menace_rate: { text: '« Non. Tu n’iras pas à Big Larry : le Service paie les dénonciateurs en balles, et tu le sais. » (Balta épaule.) « La piste. »', options: [
      { label: '« Je pars. »', action: 'flag:ver_regle;flag:ver_menace', next: 'end' },
      { label: '[Attaquer]', next: 'fuient' } ] },
    // nœud commun (§12.4) : appelé depuis Balta et Rufina ; aucun combat
    fuient: { text: '(Tecla se lève sans aide. Ils ne courent pas. Ils reculent ensemble vers l’escalier du quai, puis dans le verre, Balta le dernier, le canon sur toi. Nilo saute par la fenêtre de la cabane et les rejoint.) (Tu fais trois pas derrière eux. Le verre craque sous tes semelles, et ta peau te dit de reculer.) « Le verre est à nous. Prends ce que tu veux dans la coque. Tu ne le garderas pas longtemps. »',
      alt: [{ if: 'race_mutant', text: '(Tecla se lève sans aide. Ils ne courent pas. Ils reculent ensemble vers l’escalier du quai, puis dans le verre, Balta le dernier, le canon sur toi. Nilo saute par la fenêtre de la cabane et les rejoint.) (Tu pourrais les suivre. Personne ne t’attend, là-bas.) « Le verre est à nous. Prends ce que tu veux dans la coque. Tu ne le garderas pas longtemps. »' }],
      enter: 'flag:ver_regle;flag:ver_chasses;flag:monde_verriers_chasses', options: FIN },
  },
  rc_rufina: {
    start: { text: '(Elle tire du four un fil de verre rouge sombre au bout d’une canne de fer, le tourne, le coupe. Une perle tombe dans une boîte.) « Si tu viens pour la vitrine, elle est sur l’établi. Si c’est pour moi, je travaille. »', options: [
      { label: '« Qu’est-ce que tu vends ? »', next: 'vente' },
      { label: '« Tes bras. »', if: '!race_mutant&!ver_vu_bras', next: 'bras' },
      { label: '« Tes bras. Ça t’a prise jeune ? »', if: 'race_mutant&!ver_vu_bras', next: 'bras_mutant' },
      { label: '« Tecla dit que tu as un tison pour moi. »', if: 'ver_q_tison&!ver_tison', next: 'tison' },
      { label: '« Les perles, sur la porte de l’écluse. »', if: 'ver_indice_perles&!ver_perles_dites', next: 'perles' },
      { label: '« Tu connais Lena, de Novo Córdoba ? »', if: 'monde_lena_connue&!ver_lena_dite', next: 'lena' },
      ATTAQUER,
      { label: '« Rien. »', next: 'end' } ] },
    // §12.12 : eau 5 $ (3 $ si ver_confiance), lame 12 $ (= poignard), rachat d’une ration 5 $ (une fois) ; stock limité par drapeaux
    vente: { text: '« De l’eau du condenseur, cinq. Des lames de verre noir, douze : ça coupe mieux que ton acier et ça casse plus vite, comme tout ce qui coupe bien. Je prends les rations : ici, rien ne pousse. »', options: [
      { label: '« Une eau. » (5 $)', if: '!ver_eau1&!ver_confiance', action: 'buy:water:5;flag:ver_eau1', next: 'vente' },
      { label: '« Une eau. » (prix d’ami, 3 $)', if: '!ver_eau1&ver_confiance', action: 'buy:water:3;flag:ver_eau1', next: 'vente' },
      { label: '« Une autre. » (5 $)', if: 'ver_eau1&!ver_eau2', action: 'buy:water:5;flag:ver_eau2', next: 'vente' },
      { label: '« Une lame. » (12 $)', if: '!ver_lame', action: 'buy:poignard:12;flag:ver_lame', next: 'lame' },
      { label: '« Je te vends une ration. » (5 $)', if: 'inv:ration>=1&!ver_ration_v', action: 'sell:ration:5;flag:ver_ration_v', next: 'ration' },
      { label: '« Rien. »', next: 'start' } ] },
    pauvre: { text: '« Le verre ne fait pas crédit. Moi non plus. »', options: SUITE('vente') },
    lame: { text: '« Enveloppe-la dans un chiffon. La première fois, elle coupe celui qui la porte. »', options: SUITE('vente') },
    ration: { text: '« Cinq. Plus que la caravane, je sais. Ici, une ration, c’est une semaine de rosée. »', options: SUITE('vente') },
    bras: { text: '« Des plaques, oui. Ça ne se lave pas et ça ne s’attrape pas, si c’est ta question. Chez nous, à Novo Córdoba, ça vient dans certaines familles, au bord du fleuve. Ailleurs, c’est autre chose : les os de Balta, la peau de Nilo, les yeux de Tecla. Le verre ne fait jamais deux fois la même chose. »', enter: 'flag:ver_vu_bras', options: SUITE('start') },
    bras_mutant: { text: '« À dix ans. Toi aussi, je le vois, mais je ne vois pas où. C’est bien : ça veut dire que tu as appris à le cacher. Ici, tu n’en as pas besoin. »', enter: 'flag:ver_vu_bras', options: SUITE('start') },
    tison: { text: '(Elle sort du four un morceau de poutre qui brûle par un bout.) « Tiens-le par le manche, pas par le feu. Et ne le tends pas : avance avec. Une bête recule devant ce qui avance. »', enter: 'flag:ver_tison', options: SUITE('start') },
    perles: { text: '« Une perle par passager. Quand quelqu’un arrive par la citerne de Remedios et repart vivant vers Dusk-Town, je fais une perle et je l’enfile sur la porte. Va compter, si tu veux. Moi, je ne compte plus. »', enter: 'flag:ver_perles_dites', options: SUITE('start') },
    lena: { text: '(Elle pose la canne.) « La petite qui cherche son père ? À Novo Córdoba, tout le monde cherche un père ou un frère. Si elle monte vers Dusk-Town, elle passera par ici. Je lui garde une perle. »', enter: 'flag:ver_lena_dite', options: SUITE('start') },
  },
  rc_nilo: {
    start: { text: '(Entre les planches de la fenêtre, un œil, et une main marbrée de taches brunes.) « T’es du Service ? »', options: [
      { label: '« Non. »', next: 'non' },
      { label: '(Tu remontes ta manche, ou tu baisses ton col.)', if: 'race_mutant', next: 'mutant' },
      { label: '« Et si je l’étais ? »', next: 'si' } ] },
    non: { text: '« Le Service aussi, il dit toujours non. » (Un temps.) « Mais le Service ne viendrait pas jusqu’au verre pour trois cochons. »', options: SUITE('harde') },
    mutant: { text: '(Il regarde.) « Ah. Comme Tecla, en moins vieux. »', enter: 'flag:ver_confiance', options: SUITE('harde') },
    si: { text: '« Alors t’aurais déjà tiré. »', options: SUITE('harde') },
    harde: { text: '(Un choc fait trembler toute la cabane, de l’autre côté.) « Le gris tape dans la porte. Toutes les dix minutes, je compte. J’ai toute l’eau ici, les jarres. Si je sors, ils entrent. Si je reste, ils cassent la porte. Moi, je passe par la fenêtre, mais l’eau, elle ne passe pas. »', options: [
      { label: '« Tiens bon. »', next: 'tiens' },
      { label: '« Passe-moi une jarre par la fenêtre. Je vais les attirer ailleurs. »', if: 'ver_q_leurre&!ver_jarre', next: 'jarre' },
      { label: '« Ils boivent où, d’habitude ? »', if: 'observation>=5|ver_indice_rosee', next: 'rosee' } ] },
    tiens: { text: '« Je tiens. Je tiens depuis l’aube. »', enter: 'flag:ver_nilo_vu', options: FIN },
    jarre: { text: '« Une seule. Tecla va me tuer. » (Une petite jarre bouchée passe entre deux barreaux.)', enter: 'give:water;flag:ver_jarre;flag:ver_nilo_vu', options: FIN },
    rosee: { text: '« Sur les dalles, la nuit. Le verre fait de la rosée quand il refroidit, et ils la lèchent. Mais là, il fait chaud, et ils ont senti l’eau. »', enter: 'flag:ver_nilo_vu', options: SUITE('harde') },
    dehors: { text: '« Ils sont partis ? Vraiment partis ? »', options: [
      { label: '« Vraiment. »', next: 'blinde' },
      { label: '« Tu as été courageux. »', next: 'courage' } ] },
    courage: { text: '« J’avais peur. Mais courageux et peur, Tecla dit que c’est pareil, vu de dehors. »', options: SUITE('blinde') },
    blinde: { text: '« Tu veux voir le verre ? Pas trop longtemps : toi, il te mange. Va voir le blindé, au nord. Il y a des gens du Service dedans, depuis longtemps. Personne n’est venu les chercher. C’est comme ça qu’on sait qu’ils ne viendront pas. »',
      alt: [{ if: 'race_mutant', text: '« Toi, le verre te mange moins. Va voir le blindé, au nord. Il y a des gens du Service dedans, depuis longtemps. Personne n’est venu les chercher. »' }],
      enter: 'flag:ver_nilo_blinde', options: FIN },
  },
  // la harde (§6.5) : des bêtes, examen et non dialogue (pas de portrait)
  rc_harde: {
    start: { text: '« Quatre bêtes grises dans la cuve de l’écluse. Des pécaris, ou ce qu’il en reste : le cuir pelé, croûté de poussière de verre qui brille quand ils bougent, des défenses trop longues qui leur relèvent les babines. Le plus gros, presque blanc, une oreille fendue, cogne la porte de la cabane du front, recule, et recommence. Ce ne sont pas des gens. Ce sont des bêtes, et elles ont soif. »', options: [
      { label: '(Avancer le tison vers le gris.)', if: 'ver_tison&!ver_harde_partie', test: 'volonte:5', partialAt: 3, pass: 'tison_ok', partial: 'tison_mal', fail: 'tison_rate' },
      { label: '[Attaquer]', if: '!ver_harde_partie', action: 'combat:ecluse_verriers', next: 'end' },
      { label: '(Reculer.)', next: 'end' } ] },
    tison_ok: { text: '(Tu avances, sans t’arrêter. Le gris souffle, gratte le limon, puis tourne. Il s’en va par le bout de la cuve, les jeunes derrière lui, et la harde remonte dans le verre.)', enter: 'flag:ver_harde_partie;flag:ver_harde_feu', options: FIN },
    tison_mal: { text: '(Le gris charge, dévie au dernier moment et te laboure la cuisse au passage. Puis il file, et les jeunes avec lui.)', enter: 'hurt:2;flag:ver_harde_partie;flag:ver_harde_feu', options: FIN },
    tison_rate: { text: '(Ta main tremble, la flamme tremble avec. Le gris baisse la tête.)', enter: 'combat:ecluse_verriers', options: SUITE('end') },
  },
};

// fouilles (§9)
const BLINDE_LOOT = 'give:ration:2;gain:10;flag:ver_f_blinde';
const BLINDE_OK = '!ver_f_blinde&ver_nilo_blinde|!ver_f_blinde&observation>=5'; // ◆ Nilo en a parlé, ou Observation 5
const BLINDE_EX = 'Un blindé du Service, enfoncé dans le verre jusqu’aux essieux, comme dans de la boue qui aurait pris. La peinture grise a cloqué. L’écoutille est ouverte. Personne n’est venu le chercher.';
const BLINDE_CRAIE = ' Sur le flanc, à la craie : un cercle. Puis les mots « ILS NE VIENNENT PAS ».';
const LEURRE = s => s.flags.ver_q_leurre && !s.flags.ver_harde_partie && (s.player.inv.water || 0) >= 1;
const scoreObs = s => Math.round((s.character?.skills?.observation ?? 0) / 10);

export const VERRIERS = {
  nom: 'L\u2019écluse des Verriers', famille: 'creatures', terrains: ['verre', 'piste'], biomes: ['glass'], poids: 1, lieu: 'rc_ecluse_verriers', prefixe: 'ver_',
  duree: 1, dureeSi: { ver_attendu: 4 }, // attendre la nuit avec eux (§6.2) : +4 h à la sortie, la lumière de la scène ne change pas
  si: etat => !etat.flags.monde_verriers_vus, drapeauArrivee: 'monde_verriers_vus', // Verriers uniques (§1) : drapeau de monde, jamais purgé
  arrivee: 'Un canal mort au bord du verre. Une écluse noire, un four qui rougeoie. Dans la cuve, des bêtes grises.',
  arriveeRetour: 'L\u2019écluse, au bord du verre.',
  scene: { size: { w: 36, d: 30 }, city: 'nml', ambiance: 'glass', // courbe glass (ambiances.js, §11) ; repli desert si elle manquait
    // nuitDecor par défaut : tous les décors suivent la nuit (le verre ne luit jamais, §3)
    ground: { base: '#8a8270', skin: 'g_rc_cendre', tileM: 4, clean: true, marge: { skin: 'g_rc_verre', tileM: 4, m: 30, voile: 'rgba(14,12,8,.20)' },
      paint: [ { x: 0, z: 0, w: 36, d: 7, skin: 'g_rc_verre', tileM: 4 }, { x: 12, z: 0, w: 4, d: 4, skin: 'g_rc_verre_b', tileM: 4 }, { x: 28, z: 4, w: 4, d: 3, skin: 'g_rc_verre_c', tileM: 4 },
        { x: 0, z: 7, w: 36, d: 2, skin: 'g_rc_quai', tileM: 4 },
        { x: 0, z: 9, w: 36, d: 6.5, skin: 'g_rc_limon', tileM: 4 }, { x: 16, z: 9, w: 4, d: 4, skin: 'g_rc_limon_b', tileM: 4 },
        { x: 0, z: 21, w: 36, d: 6, skin: 'g_rc_piste', tileM: 4 }, { x: 8, z: 21, w: 4, d: 4, skin: 'g_rc_piste_b', tileM: 4 }, { x: 26, z: 23, w: 4, d: 4, skin: 'g_rc_piste_c', tileM: 4 },
        { x: 20, z: 27, w: 4, d: 3, skin: 'g_rc_cendre_b', tileM: 4 } ] },
    cadre: { desktop: { x: [18.5, 32.5], z: [12, 20] }, // 1280 : 6,5 m vers l'est (2 m ne suffisaient pas) : blindé en entier, « Demi-tour » à plus de 20 px du bord [Régie + Ocre 18/11]
    mobile: { x: [6, 28], z: [16, 22] } },
    buildings: [ // §14 + table de poses du §15 (ancre au coin sud-est de l’emprise) ; ph : volume gris de repli si une clé manquait
      D('ver_cuve', 'rc_ecl_cuve_3q', 22, 10, 9, 4, { fond: true, ph: { h: 0.05 } }), // décalque sol : boue, tessons, sabots
      D('ver_dalles', 'rc_vr_dalles_3q', 5, 2, 2, 2, { ph: { h: 1.2 }, solid: [R(5, 2, 2, 2, 1)] }),
      D('ver_dalles_b', 'rc_vr_dalles_b_3q', 14, 3, 2, 2, { ph: { h: 0.9 }, solid: [R(14, 3, 2, 2, 1)] }),
      D('ver_blinde', 'rc_vr_blinde_vitrifie_3q', 26, 1, 5, 3, { ph: { h: 2.4 }, solid: [R(26, 1, 5, 3, 2)] }),
      D('ver_blinde_texte', 'rc_vr_blinde_vitrifie_3q_texte', 26, 1, 5, 3, { etage: 1, sansMiroir: true }), // lettrage : calque normal, jamais en miroir
      // parapet nord (passage x 12-15 : escalier)
      D('ver_par_n1', 'rc_vr_parapet_3q', 0, 8.5, 6, 0.5, { solid: [R(0, 8.5, 6, 0.5, 1)] }), D('ver_par_n2', 'rc_vr_parapet_3q', 6, 8.5, 6, 0.5, { solid: [R(6, 8.5, 6, 0.5, 1)] }),
      D('ver_escalier', 'rc_vr_escalier_quai_3q', 12, 8.5, 3, 0.5, {}),
      D('ver_par_n3', 'rc_vr_parapet_3q', 15, 8.5, 6, 0.5, { solid: [R(15, 8.5, 6, 0.5, 1)] }), D('ver_par_n4', 'rc_vr_parapet_3q', 21, 8.5, 6, 0.5, { solid: [R(21, 8.5, 6, 0.5, 1)] }),
      D('ver_par_n5', 'rc_vr_parapet_3q', 27, 8.5, 6, 0.5, { solid: [R(27, 8.5, 6, 0.5, 1)] }), D('ver_par_n6', 'rc_vr_parapet_b_3q', 33, 8.5, 3, 0.5, { solid: [R(33, 8.5, 3, 0.5, 1)] }),
      D('ver_peniche', 'rc_ecl_peniche_3q', 2, 9.5, 11, 4.5, { ph: { h: 3 }, solid: [R(2, 9.5, 11, 4.5, 2)] }),
      D('ver_porte_n', 'rc_ecl_porte_nord_3q', 19, 9, 1.5, 3, { ph: { h: 3.4 }, solid: [R(19, 9, 1.5, 3, 2)] }),
      D('ver_porte_s', 'rc_ecl_porte_sud_3q', 20.5, 14, 3, 1, { ph: { h: 3.4 }, solid: [R(20.5, 14, 3, 1, 2)] }),
      // parapet sud (passages x 3-6 : cale ; x 24-27 : seuil de la cabane)
      D('ver_par_s1', 'rc_vr_parapet_b_3q', 0, 15, 3, 0.5, { solid: [R(0, 15, 3, 0.5, 1)] }),
      D('ver_par_s2', 'rc_vr_parapet_3q', 6, 15, 6, 0.5, { solid: [R(6, 15, 6, 0.5, 1)] }), D('ver_par_s3', 'rc_vr_parapet_3q', 12, 15, 6, 0.5, { solid: [R(12, 15, 6, 0.5, 1)] }),
      D('ver_par_s4', 'rc_vr_parapet_3q', 18, 15, 6, 0.5, { solid: [R(18, 15, 6, 0.5, 1)] }),
      D('ver_par_s5', 'rc_vr_parapet_3q', 27, 15, 6, 0.5, { solid: [R(27, 15, 6, 0.5, 1)] }), D('ver_par_s6', 'rc_vr_parapet_b_3q', 33, 15, 3, 0.5, { solid: [R(33, 15, 3, 0.5, 1)] }),
      D('ver_etabli', 'rc_ecl_etabli_3q', 6, 17.2, 3, 0.8, { ph: { h: 0.9 }, solid: [R(6, 17.2, 3, 0.8, 1)] }),
      D('ver_four', 'rc_ecl_four_3q', 10, 16.3, 3, 2.7, { ph: { h: 2.2 }, solid: [R(10, 16.3, 3, 2.7, 2)] }), // en buildings pour son _neon (gueule au sud en 11,5 ; 19)
      D('ver_cond1', 'rc_ecl_condenseur_3q', 14, 16.3, 1.5, 2, { ph: { h: 1.8 }, solid: [R(14, 16.3, 1.5, 2, 1)] }),
      D('ver_cond2', 'rc_ecl_condenseur_3q', 16, 16.3, 1.5, 2, { ph: { h: 1.8 }, solid: [R(16, 16.3, 1.5, 2, 1)], miroir: true }), // celui du milieu en miroir
      D('ver_cond3', 'rc_ecl_condenseur_3q', 18, 16.3, 1.5, 2, { ph: { h: 1.8 }, solid: [R(18, 16.3, 1.5, 2, 1)] }),
      D('ver_cabane', 'rc_ecl_cabane_3q', 24, 16.2, 4, 3.8, { ph: { h: 3 }, solid: [R(24, 16.2, 4, 3.8, 2)] }), // porte au nord (face cachée), fenêtre au sud
      D('ver_panneau', 'rc_ds_panneau_ufsa_3q', 1.2, 16.4, 0.6, 0.2, { solid: [R(1.4, 16.4, 0.2, 0.2, 0)] }),
      D('ver_rochers_b', 'rc_ds_rochers_b_3q', 8, 27.8, 3, 1.5, { solid: [R(8, 27.8, 3, 1.5, 1)] }),
      D('ver_rochers', 'rc_ds_rochers_3q', 29, 27.9, 3, 1.5, { solid: [R(29, 27.9, 3, 1.5, 1)] }),
    ],
    // gueule du four : seule lumière (§3) ; flaque rc_ecl_four_flaque = décalque additif au sol en (10 ; 19 ; 3 × 2), la nuit seulement,
    // par le mécanisme générique de flaque nocturne (ARCHI §4 bis, le même que le feu du bivouac) ; le verre ne luit jamais
    // four = seule lumière (§3) : gueule et flaque calibrées sur le feu du bivouac (mesure : bivouac 8 à 15 m² de sol réchauffé, four 6 à 10 m² ; Régie + Ocre 18/11)
    enseignes: [{ id: 'ver_feu', building: 'ver_four', effet: 'pulse', periode: 7, intensite: 1.3,
      flaque: { cle: 'rc_ecl_four_flaque', x: 10, z: 19, w: 3, d: 2, i: 2, echelle: 3.5 } }],
    props: [{ sprite: 'barrel', x: 20.7, z: 17, fp: [0.6, 0.6] }], // fût (réutilisé)
    entree: { x: 1.5, z: 24, heading: Math.PI / 2 },
    sorties: [
      { id: 'ouest', label: 'Demi-tour (carte)', x: 0.6, z: 24, zone: { x0: 0, x1: 0.9, z0: 21, z1: 27 }, effet: 'halte' },
      { id: 'est', label: 'Reprendre la piste', x: 35.4, z: 24, zone: { x0: 35.1, x1: 36, z0: 21, z1: 27 }, effet: 'reprise' } ] }, // jamais gardée (§12.2)
  declencheurs: [
    { id: 'T1', zone: { x: 4, z: 15.5, w: 2, d: 11.5 }, si: '!ver_t1&!ver_salue&!ver_regle', enter: 'flag:ver_t1', dialogue: 'rc_balta' },
    // rayonnement du verre (§6.6), une fois par scène : mutant texte seul ; compteur ; sinon goût de métal ; non-mutant −1 PV
    { id: 'T_verre', zone: { x: 0, z: 0, w: 36, d: 7 }, si: '!ver_verre_dit', enter: 'flag:ver_verre_dit', alt: [
      { si: 'race_mutant', texte: '« Le verre est tiède sous les semelles, d\u2019une tiédeur qui ne vient pas du soleil. Ta peau ne dit rien. Elle a l\u2019habitude. »' },
      { si: 'inv:compteur>=1', texte: '« Le compteur se met à crépiter, de plus en plus vite. Tu sais ce que ça veut dire. Pas longtemps, ici. »', enter: 'hurt:1' },
      { texte: '« Le verre est tiède sous les semelles, d\u2019une tiédeur qui ne vient pas du soleil. Au bout de quelques pas, un goût de métal dans la bouche. »', enter: 'hurt:1' } ] },
    // Nilo par la fenêtre sud : le long de la façade, sur mobile, sans viser la petite fenêtre
    { id: 'pres_cabane', zone: { x: 24, z: 20, w: 4, d: 1 }, si: '!ver_nilo_libre&!ver_chasses', dialogue: 'rc_nilo_voix' } ],
  pnj: [
    { id: 'rc_balta', name: 'Balta', sprite: 'gen_rc_balta', x: 5.5, z: 20.4, faceTo: [1.5, 24], dialogue: 'rc_balta',
      entrees: [{ si: 'ver_harde_partie', node: 'apres' }, { si: 'ver_salue', node: 'encore' }], si: '!ver_chasses', cacheCombat: true, bloque: false },
    { id: 'rc_tecla', name: 'Tecla', sprite: 'gen_rc_tecla', x: 13.2, z: 19.6, faceTo: [1.5, 24], fige: true, dialogue: 'rc_tecla', si: '!ver_chasses', cacheCombat: true, bloque: false }, // assise contre le four
    { id: 'rc_rufina', name: 'Rufina', sprite: 'gen_rc_rufina', x: 7.5, z: 18.8, faceTo: [11.5, 19], dialogue: 'rc_rufina', si: '!ver_chasses', cacheCombat: true, bloque: false },
    { id: 'rc_nilo_voix', name: 'Nilo', sprite: 'gen_rc_nilo', x: 26, z: 19.8, dialogue: 'rc_nilo', si: 'ver_jamais', fige: true, bloque: false }, // voix par la fenêtre : jamais visible
    { id: 'rc_nilo', name: 'Nilo', sprite: 'gen_rc_nilo', x: 25.5, z: 20.6, faceTo: [11.5, 19], dialogue: 'rc_nilo', entrees: [{ si: 'ver_nilo_libre', node: 'dehors' }], si: 'ver_nilo_libre&!ver_chasses', cacheCombat: true, bloque: false },
    // la harde hors combat : bêtes figées, ancre au centre des pattes (manifeste), face au sud-ouest et dos au nord-est (sens), examen rc_harde
    { id: 'rc_gris', name: 'Le gris', sprite: 'gen_rc_chancho_gris', x: 29.5, z: 12, faceTo: [26, 16], sens: BETE, fige: true, portrait: false, dialogue: 'rc_harde', si: '!ver_harde_partie', cacheCombat: true },
    { id: 'rc_chancho_a', name: 'Chancho', groupe: 'La harde', sprite: 'gen_rc_chancho', x: 24.5, z: 10.5, faceTo: [27, 12], sens: BETE, fige: true, portrait: false, dialogue: 'rc_harde', si: '!ver_harde_partie', cacheCombat: true },
    { id: 'rc_chancho_b', name: 'Chancho', groupe: 'La harde', sprite: 'gen_rc_chancho', x: 26.5, z: 13.5, faceTo: [26, 16], sens: BETE, fige: true, portrait: false, dialogue: 'rc_harde', si: '!ver_harde_partie', cacheCombat: true },
    { id: 'rc_chancho_c', name: 'Chancho', groupe: 'La harde', sprite: 'gen_rc_chancho', x: 33, z: 11.5, faceTo: [28, 11], sens: BETE, fige: true, portrait: false, dialogue: 'rc_harde', si: '!ver_harde_partie', cacheCombat: true },
  ],
  // examens et fouilles (§3, §9) ; alt [{ si, text, enter }] : variante selon l’état (premier qui tient), sinon text / enter
  points: [
    { id: 'ver_verre_ex', x: 14, z: 5.5, text: 'Le sable a fondu ici, il y a longtemps, et il a refroidi en dalles. Brun, noir, vert de bouteille sale. Ça craque sous la semelle comme de la glace sale. Rien ne pousse, sauf un lichen orange dans les fentes.',
      alt: [{ si: 'observation>=4', enter: 'flag:ver_indice_rosee', text: 'Le sable a fondu ici, il y a longtemps, et il a refroidi en dalles. Brun, noir, vert de bouteille sale. Ça craque sous la semelle comme de la glace sale. Rien ne pousse, sauf un lichen orange dans les fentes. Dans les creux des dalles, des traces de groin dans le sel. Des bêtes viennent lécher quelque chose ici, la nuit.' }] },
    // ◆ blindé (§9) : fouille si Nilo en a parlé ou Observation 5 ; mutant : libre ; non-mutant : Volonté 4 pour fouiller vite, −1 PV de toute façon
    { id: 'ver_blinde', x: 27.5, z: 4.5, test: 'volonte:4', testSi: `!race_mutant&${BLINDE_OK.split('|').join('|!race_mutant&')}`, pass: BLINDE_LOOT + ';hurt:1', fail: 'hurt:1',
      alt: [{ si: `race_mutant&${BLINDE_OK.split('|').join('|race_mutant&')}`, enter: BLINDE_LOOT }, { si: 'observation>=5', enter: '' }],
      text: (s, ok) => { const f = s.flags, peut = !f.ver_f_blinde && (f.ver_nilo_blinde || scoreObs(s) >= 5), craie = scoreObs(s) >= 5 ? BLINDE_CRAIE : '';
        if (f.ver_f_blinde) return 'Le blindé, vidé. L\u2019écoutille bâille sur le verre.';
        if (!peut) return BLINDE_EX + craie;
        const butin = ' Dedans, deux rations militaires scellées, qui se mangent encore, et dix dollars en vieux billets du Service, qui passent encore à Dusk-Town.';
        if (s.flags.race_mutant) return BLINDE_EX + craie + ' Tu te glisses par l\u2019écoutille.' + butin;
        return ok ? BLINDE_EX + craie + ' Tu te glisses par l\u2019écoutille, vite, la bouche fermée.' + butin + ' En ressortant, un goût de métal sur la langue.'
          : BLINDE_EX + craie + ' Tu passes la tête par l\u2019écoutille. L\u2019air a un goût de métal, ta peau te dit de reculer. Tu ressors les mains vides.'; } },
    { id: 'ver_panneau_ex', x: 1.5, z: 17.2, text: 'Le panneau a perdu presque toutes ses lettres. On lit encore : CANAL … ÉCLUSE 7. Quelqu\u2019un a gratté le reste.' },
    { id: 'ver_peniche', x: 7.5, z: 14.5, text: 'Une péniche, la quille en l\u2019air, ensablée jusqu\u2019au plat-bord. Ils ont découpé une porte dans la coque et tendu une toile devant. Dedans, il fait plus frais qu\u2019ailleurs. C\u2019est la maison.',
      alt: [{ si: 'ver_chasses&!ver_f_coque', enter: 'give:water:3;give:ration:2;gain:9;flag:ver_f_coque', text: 'La coque, vide de ses gens. Sous la toile : trois bidons, deux rations, neuf dollars dans une boîte de fer.' }] },
    { id: 'ver_porte_ex', x: 20.9, z: 12.5, text: 'La porte nord de l\u2019écluse est soudée par la rouille. Autour du montant, un fil de fer, et sur le fil, des perles de verre sombre, rouge et vert. Des dizaines. Certaines sont ternies par le sable, d\u2019autres brillent encore.',
      alt: [{ si: 'observation>=3', enter: 'flag:ver_indice_perles', text: 'La porte nord de l\u2019écluse est soudée par la rouille. Autour du montant, un fil de fer, et sur le fil, des perles de verre sombre, rouge et vert. Des dizaines. Certaines sont ternies par le sable, d\u2019autres brillent encore. Les plus vieilles sont en bas. Il y en a une neuve tout en haut, encore tranchante. Ce n\u2019est pas un ornement : on compte quelque chose.' }] },
    { id: 'ver_four_ex', x: 12.2, z: 19.5, text: 'Un four de terre crue et de briques sauvées du canal. La gueule rougeoie. À côté, une canne de fer, des moules, et un tas de dalles de verre brisées en morceaux, prêtes à refondre.' },
    { id: 'ver_condens_ex', x: 17, z: 19, enter: 'flag:ver_indice_condens', text: 'Trois toiles tendues en pente sur des cadres. La nuit, le verre refroidit et la rosée coule le long de la toile jusqu\u2019aux jarres. Les jarres sont renversées. Des traces de sabots, partout autour. La harde est passée ici avant l\u2019écluse.' },
    // établi de Rufina (§9) : vol Discrétion 6 avant tout règlement (échec : « Repose. », méfiance, pas de combat) ; libre après ver_chasses
    { id: 'ver_etabli', x: 7.5, z: 18.6, test: 'discretion:6', testSi: '!ver_regle&!ver_f_etabli&!ver_vol_rate', pass: 'give:poignard;give:perles_verre:2;flag:ver_vole;flag:ver_f_etabli', fail: 'flag:ver_mefiance;flag:ver_vol_rate',
      text: (s, ok) => ok ? 'Une lame de verre noir et deux perles glissent dans ta manche. Rufina ne lève pas les yeux.' : 'Rufina pose la canne : « Repose. »',
      alt: [{ si: 'ver_chasses&!ver_f_etabli', enter: 'give:poignard;give:perles_verre:2;flag:ver_f_etabli', text: 'L\u2019établi, abandonné. Une lame de verre noir et deux perles sont restées sur la plaque.' },
        { si: 'ver_regle|ver_f_etabli|ver_vol_rate', enter: '', text: 'Des perles qui refroidissent sur une plaque de tôle, une rangée de lames de verre noir taillées en feuille, des pinces.' }] },
    { id: 'ver_cuve_ex', x: 28.5, z: 14.3, text: 'La cuve de l\u2019écluse, comblée de limon jusqu\u2019à un mètre du bord. Une flaque de boue rouille au milieu, des tessons de jarres.' },
    { id: 'ver_porte_cabane_ex', x: 26.8, z: 15.9, text: 'La porte de la cabane de la pompe. La tôle est enfoncée à hauteur de genou, en trois endroits. Quelqu\u2019un a coincé une poutre derrière.' },
    { id: 'ver_harde', x: 25.2, z: 15.9, si: '!ver_harde_partie', text: '', dialogue: 'rc_gris', dialogueSi: '!ver_harde_partie' }, // examen de la harde, au seuil (§6.5)
    { id: 'ver_fenetre', x: 26, z: 20.6, text: '', dialogue: 'rc_nilo_voix', dialogueSi: '!ver_nilo_libre&!ver_chasses',
      alt: [{ si: 'ver_nilo_libre|ver_chasses', text: 'La fenêtre à barreaux de la cabane. Plus personne derrière les planches.' }] },
    // ◆ leurre d’eau (§6.6) : au bout du quai nord, si Tecla l’a proposé et qu’on a un bidon ; Survie 4 ; raté : l’eau est perdue, on peut recommencer
    { id: 'ver_rigole', x: 34.5, z: 8.0, test: 'survie:4', testSi: 'ver_q_leurre&!ver_harde_partie&inv:water>=1', pass: 'take:water;flag:ver_harde_partie;flag:ver_leurre', fail: 'take:water',
      text: (s, ok) => !LEURRE(s) ? 'Une rigole de pierre part du bout de la cuve vers l\u2019est et se perd dans le verre. Le vent vient de l\u2019ouest.'
        : ok ? 'Tu verses l\u2019eau en filet dans la rigole, tout au bout, sous le vent. Il ne se passe rien. Puis le gris lève le groin. Il quitte la porte, trotte vers l\u2019est, lèche la pierre, et suit la rigole jusque dans le verre. Les jeunes suivent.'
        : 'L\u2019eau file dans le sable avant d\u2019atteindre la rigole. Le gris lève la tête, te regarde, et ne bouge pas.' },
    { id: 'ver_citerne', x: 2.5, z: 14.5, si: 'ver_citerne_dite|ver_chasses', text: 'Sous la proue, une trappe de bois dans le limon. Dessous, l\u2019eau, profond. Tecla t\u2019a déjà donné ta part.',
      alt: [{ si: 'ver_chasses&!ver_f_citerne', enter: 'give:water:2;flag:ver_f_citerne', text: 'Sous la proue, la trappe de la citerne. Tu remontes deux bidons.' }] },
  ],
  dialogues: DIALOGUES_VERRIERS,
  combat: { nom: 'La harde de l\u2019écluse', centre: { x: 24, z: 15 }, prefixe: 'ver_', drapeauxDebut: ['t1', 'combat'],
    ennemis: [ // les Verriers jamais au combat (cacheCombat) ; positions absolues de la harde, mêmes cases que hors combat
      { id: 'gris', nom: 'Le gris', sprite: 'gen_rc_chancho_gris', sens: BETE, heading: cap(29.5, 12, [26, 16]), x: 29.5, z: 12, pv: 18, pa: 6, initiative: 5, arme: 'defenses', competences: { melee: 55, armes: 0 }, rendSous: 0.5, si: '!ver_conseil_gris' },
      { id: 'gris_c', nom: 'Le gris', sprite: 'gen_rc_chancho_gris', sens: BETE, heading: cap(29.5, 12, [26, 16]), x: 29.5, z: 12, pv: 18, pa: 6, initiative: 5, arme: 'defenses', competences: { melee: 55, armes: 0 }, rendSous: 0.6, si: 'ver_conseil_gris' },
      { id: 'jeune_a', nom: 'Chancho', groupe: 'La harde', sprite: 'gen_rc_chancho', sens: BETE, heading: cap(24.5, 10.5, [27, 12]), x: 24.5, z: 10.5, pv: 8, pa: 7, initiative: 7, arme: 'defenses', competences: { melee: 40, armes: 0 }, fuitTour: 3 },
      { id: 'jeune_b', nom: 'Chancho', groupe: 'La harde', sprite: 'gen_rc_chancho', sens: BETE, heading: cap(26.5, 13.5, [26, 16]), x: 26.5, z: 13.5, pv: 8, pa: 7, initiative: 6, arme: 'defenses', competences: { melee: 40, armes: 0 }, fuitTour: 3 },
      { id: 'jeune_c', nom: 'Chancho', groupe: 'La harde', sprite: 'gen_rc_chancho', sens: BETE, heading: cap(33, 11.5, [28, 11]), x: 33, z: 11.5, pv: 8, pa: 7, initiative: 6, arme: 'defenses', competences: { melee: 35, armes: 0 }, fuitTour: 2 } ],
    // aucune mort (§8) ; reddition et défaite ne quittent pas la scène (ver_recule), la harde reste
    issues: { victoire: 'flag:ver_harde_partie;flag:ver_harde_battue', fuite: 'rencontre:quitter',
              reddition: 'flag:ver_recule', defaite: 'flag:ver_recule;give:water;warp:rc_ecluse_verriers:11.5:20.5' },
    textes: { debut: 'Le gris lève la tête de la porte. Derrière toi, Balta crie : « Le gris ! Tape le gris ! » Il ne tire pas.',
      rend: { gris: 'Le gris détale.', gris_c: 'Le gris détale.' }, // §12.7 : texte de reddition par ennemi (extension de combat.js)
      victoire: 'Le gris s\u2019arrête, souffle, et te tourne le dos. Il ne court pas : il s\u2019en va. Les jeunes le suivent par le bout de la cuve, dans le verre. Balta abaisse son fusil. Il n\u2019a pas tiré.',
      fuite: 'Tu enjambes le parapet et tu cours. Le gris ne te suit pas : ce n\u2019est pas toi qu\u2019il veut, c\u2019est l\u2019eau.',
      reddition: 'Tu recules, mains vides, jusqu\u2019au parapet. Le gris te laisse partir. Derrière toi, la porte de la cabane craque encore.',
      defaite: 'Tu te réveilles contre le four. Tecla te tient la tête. « Le gris t\u2019a fait voler. Bois. »' } },
};
