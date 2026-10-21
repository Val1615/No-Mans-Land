// v7 : dialogues des quartiers 2 à 4. Fiches (désir, peur, secret) dans docs/quartiers/DUSK_TOWN_PLAN.md.
import { DIALOGUES as D1, ITEMS as I1 } from './dialogues_q1.js';
export const DIALOGUES = {
  ...D1,
  // Teo, 17 ans, guetteur du Transit. Phrases courtes, il parle en regardant la fente du volet.
  teo: {
    start: { text: 'Ferme. Doucement. Si tu viens de l\'ouest, tu as marché au milieu de l\'avenue, je t\'ai vu. Ne refais pas ça.', options: [
      { label: 'Quand passent les camions ? J\'ai une porte à forcer.', next: 'q_quand', if: 'q_start&!q_signal' },
      { label: 'Tu surveilles quoi ?', next: 'quoi' }, { label: 'Tu vends des nouvelles ?', next: 'vente' }, { label: 'Je m\'en vais.', next: 'end' } ] },
    quoi: { text: 'La route. Les camions arrivent par là, toujours. Je vois la poussière avant d\'entendre le moteur. Alors je tourne le miroir vers La Pompe, deux éclats, et tout le monde rentre le linge.', options: [
      { label: 'Et la nuit ?', next: 'nuit' }, { label: 'On te paie pour ça ?', next: 'paie' }, { label: 'Merci, Teo.', next: 'end' } ] },
    nuit: { text: 'La nuit je dors. Enfin. Presque jamais.', options: [ { label: 'Presque ?', next: 'secret' }, { label: 'Courage.', next: 'end' } ] },
    secret: { text: 'Une fois. Une seule. Je me suis réveillé avec le bruit des portières. Ils ont pris les deux fils Ortega. Personne ne sait que j\'étais là-haut. Toi non plus, d\'accord ?', options: [
      { label: 'Je ne dirai rien.', action: 'flag:teo_secret', next: 'merci' }, { label: 'Ça aurait pu arriver à n\'importe qui.', next: 'merci' } ] },
    merci: { text: 'Ouais. Va. Et marche à l\'ombre des façades.', options: [ { label: 'À plus.', next: 'end' } ] },
    paie: { text: 'Hector me donne à manger. Mara me recoud. Moi je voudrais des dollars, des vrais, comme un adulte. Un jour je me paierai la place sur une caravane, et quelqu\'un d\'autre tiendra le miroir.', options: [ { label: 'Ça viendra.', next: 'end' } ] },
    vente: { text: 'Cinq dollars, je te dis où il y a quelqu\'un de vivant au nord. Pas de remise, j\'ai des projets.', options: [
      { label: 'Marché conclu (5 $)', action: 'buy:tip:5', next: 'tuyau' }, { label: 'Non.', next: 'end' } ] },
    tuyau: { text: 'Au Scellé. À La Pompe, tu prends la ruelle de la pompe vers le nord, tout droit. Tu tombes sur une place devant une porte d\'acier. La maison au toit de tuiles juste à gauche de la place, porte sur le chemin, une clé gravée au-dessus : l\'atelier. Ezequiel. Il boite. Dis-lui que tu viens de ma part.', options: [
      { label: 'Noté.', action: 'reveal:s_atelier', next: 'end' } ] },
    // v9 quête, étape 3 : le moment. Choix : payer, ou vendre le secret d'Ezequiel.
    q_quand: { text: 'La porte d\'acier ? Tu es le quatrième ce mois-ci. Les trois autres, je les ai vus partir à l\'arrière d\'un camion, et pas à l\'avant. Je peux te faire signe depuis le toit quand la route est vide. Ça a un prix.', options: [
      { label: 'Cinq dollars, comme d\'habitude (5 $)', action: 'pay:5;flag:q_signal', next: 'q_ok' },
      { label: 'Pas d\'argent. Mais je sais comment Ezequiel s\'est vraiment cassé la jambe.', action: 'flag:q_signal;flag:q_trahi', next: 'q_trahi', if: 'ezequiel_toit' },
      { label: 'Plus tard.', next: 'end' } ] },
    q_ok: { text: 'Un seul éclat de miroir : la route est vide, tu y vas. Deux éclats : tu rentres le linge et toi avec.', options: [ { label: 'Un éclat, j\'y vais.', next: 'end' } ] },
    q_trahi: { text: 'Tombé du toit ? Tout seul ? Et le combat à six ? (Il se mord la manche pour ne pas rire.) D\'accord. Ça vaut cinq dollars, ça vaut même plus. Un seul éclat de miroir : la route est vide.', options: [ { label: 'Un éclat, j\'y vais.', next: 'end' } ] },
    pauvre: { text: 'Pas de dollars, pas de nouvelles. C\'est la règle, elle est de moi.', options: [ { label: 'D\'accord.', next: 'end' } ] }
  },
  // Ezequiel, récupérateur, la cinquantaine. Lent, sec, appelle tout le monde « petit ».
  ezequiel: {
    start: { text: 'Si tu viens pour la porte, petit, fais la queue derrière moi. Ça fait trois semaines que je suis le premier.',
      alt: [ { if: 'q_fin', text: 'Alors, cette porte ? Non, ne dis rien. À ta tête, elle est toujours fermée et tu as entendu quelque chose que tu n\'aurais pas voulu.' },
             { if: 'q_trahi', text: 'Le gamin du Transit miaule quand je passe sous son volet. Un chat qui tombe d\'un toit, il appelle ça. Tu ne saurais pas d\'où il sort ça, petit ?' } ], options: [
      { label: 'Ceux qui ont tenté la porte, tu les connais ?', next: 'q_porte', if: '!q_start' },
      { label: 'Qu\'est-ce qu\'il y a derrière ?', next: 'derriere' }, { label: 'Ta jambe ?', next: 'jambe' }, { label: 'Je ne fais que passer.', next: 'end' } ] },
    derriere: { text: 'Je n\'en sais rien. Personne n\'en sait rien. C\'est pour ça que ça vaut quelque chose. Tout ce qui est ouvert dans ce pays a déjà été vidé.', options: [
      { label: 'D\'autres ont essayé ?', next: 'autres' }, { label: 'Bonne chance.', next: 'end' } ] },
    autres: { text: 'Des dizaines. Regarde la peinture autour de la serrure, on dirait qu\'un chien l\'a mâchée. Et quand deux bandes arrivent le même jour, on ne force plus la porte. On se force entre nous.', options: [
      { label: 'Tu as peur qu\'ils reviennent.', next: 'peur' }, { label: 'Je vois.', next: 'end' } ] },
    peur: { text: 'J\'ai peur de les entendre et de ne pas pouvoir courir. Le reste, je m\'en arrange.', options: [ { label: 'Je repasserai.', next: 'end' } ] },
    jambe: { text: 'Une bande de récupérateurs. Six contre un. J\'en ai laissé deux par terre.', options: [
      { label: 'Six ? Vraiment ?', next: 'vrai' }, { label: 'Tu as eu de la chance.', next: 'end' } ] },
    vrai: { text: 'Bon. Il y a une grille d\'aération sur le toit du bloc. J\'ai voulu la desceller tout seul, de nuit. Le toit est plus glissant que la fierté. Si tu racontes ça, petit, je raconterai que tu mens.', options: [
      { label: 'Ton secret est gardé.', action: 'flag:ezequiel_toit', next: 'garde' }, { label: 'Tu devrais voir Vera, à la clinique.', next: 'vera' } ] },
    garde: { text: 'Tu es moins bête que tu en as l\'air. Ça ne dit pas grand-chose, remarque.', options: [ { label: 'Merci quand même.', next: 'end' } ] },
    // v9 quête « La porte d'acier », étape 1
    q_porte: { text: 'Tous. Les malins viennent la nuit avec des barres à mine. Les très malins viennent le jour avec un camion, et ceux-là oublient la porte dès qu\'ils voient qu\'il y a des gens à ramasser dans les maisons.', options: [
      { label: 'Et toi, tu as essayé comment ?', next: 'q_ment', if: '!ezequiel_toit' }, { label: 'Et toi ? Le toit, je sais déjà.', next: 'q_vrai', if: 'ezequiel_toit' } ] },
    q_ment: { text: 'Au cric. On était sept dessus, la porte commençait à céder, et une bande est arrivée par l\'est. La suite, tu la connais, je t\'ai parlé de ma jambe. Il te faut un cric de camion. Anselme en cache un sous son comptoir, pour les jours de pneu crevé. Il n\'a pas de camion.', options: [
      { label: 'Et pour ne pas finir comme toi ?', action: 'flag:q_start', next: 'q_moment' } ] },
    q_vrai: { text: 'Toi, je ne vais pas te raconter la bande de sept. La grille du toit est un leurre, elle donne sur un puits bouché. J\'y ai laissé un genou pour rien. Le seul endroit qui bouge, c\'est le bas du battant gauche. Un cric de camion glissé dessous. Anselme en cache un sous son comptoir.', options: [
      { label: 'Et pour ne pas finir comme toi ?', action: 'flag:q_start;flag:q_battant', next: 'q_moment' } ] },
    q_moment: { text: 'Ne force pas quand les camions sont sur la route. Le cric chante, ça s\'entend jusqu\'au Transit. Teo sait quand ils passent. Teo sait tout, et il le vend.', options: [ { label: 'J\'y vais.', next: 'end' } ] },
    vera: { text: 'La clinique de La Pompe ? Elle prend des dollars et pose des questions. Je n\'ai ni les uns ni l\'envie des autres.', options: [ { label: 'Comme tu veux.', next: 'end' } ] }
  },
  // Sol, gardienne de la citerne des Sables. Calme, ironique, ne lâche rien sur elle-même.
  sol: {
    start: { text: 'Tu as soif ou tu es curieux ? Les deux coûtent, mais l\'eau coûte moins cher.', options: [
      { label: 'De l\'eau (3 $)', action: 'buy:water:3', next: 'eau' }, { label: 'Anselme la vend quatre.', next: 'anselme' },
      { label: 'Ton foulard, tu ne l\'enlèves jamais ?', next: 'foulard' }, { label: 'Rien, merci.', next: 'end' } ] },
    eau: { text: 'Tirée ce matin sous le garage. Elle a un goût de fer. Le fer, ça ne tue personne.', options: [ { label: 'Autre chose ?', next: 'start' }, { label: 'Merci, Sol.', next: 'end' } ] },
    anselme: { text: 'Anselme filtre deux fois et compte trois fois. Moi je remonte un seau et je te le donne. Chacun sa religion.', options: [ { label: 'Tu t\'en sors comme ça ?', next: 'desir' }, { label: 'D\'accord.', next: 'start' } ] },
    desir: { text: 'La pompe à main grince. Si elle casse, les Sables n\'ont plus d\'eau, et ceux qui vivent dans le sable, il faudra qu\'ils remontent à La Pompe. Ça ferait du monde dehors. Personne ne veut ça.', options: [ { label: 'Je comprends.', next: 'end' } ] },
    foulard: { text: 'Le sable rentre partout. Dans les yeux, dans les dents. Dans les questions aussi, on dirait.', options: [
      { label: 'Pardon. Je ne dirai rien à personne.', action: 'flag:sol_vue', next: 'confiance' }, { label: 'Je demandais pour rien.', next: 'end' } ] },
    confiance: { text: 'Quand les camions passent, ils regardent les mains, le cou, les yeux. Après, ils ne regardent plus rien. Alors oui, je garde le foulard. Tu reviendras boire. Seul, de préférence.', options: [ { label: 'Promis.', next: 'end' } ] },
    pauvre: { text: 'Le seau est gratuit à remonter. Pas à boire.', options: [ { label: 'Tant pis.', next: 'end' } ] }
  }
};
export const ITEMS = { ...I1, tip: { name: 'Tuyau', consumeNow: true }, cric: { name: 'Cric de camion' } };
// v9 : Anselme (étape 2, choix : payer ou mentir) et la voix derrière la porte (scène finale, sans PNJ visible)
DIALOGUES.anselme = { ...DIALOGUES.anselme,
  start: { ...DIALOGUES.anselme.start, alt: [ { if: 'q_menti_anselme', text: 'Entre, et ferme. J\'ai croisé Mara à la pompe. Elle n\'a jamais entendu parler de mon cric, et la pompe siffle toujours. Je compte devant toi quand même. Je compte surtout ce que tu me dois.' } ],
    options: [ { label: 'Le cric sous ton comptoir.', next: 'q_cric', if: 'q_start&!q_cric' }, ...DIALOGUES.anselme.start.options ] },
  q_cric: { text: 'Quel cric ? Ah, celui-là. Il soulevait la camionnette de ma femme. Plus de camionnette, plus de femme, il reste le cric. Quinze dollars.', options: [
    { label: 'Payer (15 $)', action: 'buy:cric:15;flag:q_cric', next: 'q_paye' },
    { label: 'C\'est pour la pompe de Mara. Elle te le rendra.', action: 'buy:cric:5;flag:q_cric;flag:q_menti_anselme', next: 'q_mara' },
    { label: 'Trop cher.', next: 'end' } ] },
  q_paye: { text: 'Un, deux... quinze. Ne le rapporte pas tordu, je ne le reprendrai pas.', options: [ { label: 'Merci.', next: 'end' } ] },
  q_mara: { text: 'Pour Mara ? Alors cinq dollars, le prix entre voisins. Dis-lui qu\'elle me doit un sourire. Un vrai, pas celui qu\'elle fait aux soldats.', options: [ { label: 'Je lui dirai.', next: 'end' } ] }
};
DIALOGUES.porte = {
  start: { text: 'Au loin, sur le toit du guet, un seul éclat de miroir : la route est vide. Le cric tient tout juste sous le bas du battant.',
    alt: [ { if: 'q_fin', text: 'La porte d\'acier. La grille au-dessus ne grésille plus. Tu attends. Rien.' },
           { if: 'q_battant', text: 'Au loin, sur le toit du guet, un seul éclat de miroir : la route est vide. Le cric tient sous le bas du battant gauche, là où Ezequiel a dit que ça bougeait.' } ], options: [
    { label: 'Pomper.', next: 'p1', if: '!q_fin' }, { label: 'Frapper trois coups.', next: 'apres', if: 'q_fin' }, { label: 'Laisser tomber.', next: 'end' } ] },
  apres: { text: 'Personne ne répond. Ou quelqu\'un écoute sans répondre. Steel-Megalopolis est loin.', options: [ { label: 'Partir.', next: 'end' } ] },
  p1: { text: 'Le cric grince. Le battant gémit, bouge d\'un doigt, puis plus rien. Le métal reprend sa place comme s\'il s\'était seulement étiré.', options: [
    { label: 'Pomper encore.', next: 'p2' }, { label: 'Laisser tomber.', next: 'end' } ] },
  p2: { text: 'Un claquement sec à l\'intérieur. Puis un grésillement, au-dessus de la porte, dans une grille que tu avais prise pour de la rouille. « ...ttention... confinement... ttention... » Le message boucle, se tord, s\'arrête.', options: [
    { label: 'Il y a quelqu\'un ?', next: 'v1' }, { label: 'Frapper sur la porte.', next: 'coups' } ] },
  coups: { text: 'Tu frappes trois coups. Trois coups répondent, plus faibles, de l\'autre côté. Puis le grésillement revient, et cette fois quelqu\'un respire dedans.', options: [ { label: 'Il y a quelqu\'un ?', next: 'v1' } ] },
  v1: { text: '« Ne tire plus sur la porte. S\'il te plaît. Chaque fois qu\'elle bouge, l\'air s\'arrête. » Une toux, longue. « Tu es vivant, toi ? Vraiment vivant ? »', options: [
    { label: 'Oui. Qui êtes-vous ?', next: 'v2' }, { label: 'Ça dépend des jours.', next: 'v2h' } ] },
  v2h: { text: 'Un rire, ou ce qu\'il en reste. « Moi aussi. Aujourd\'hui, c\'est un mauvais. »', options: [ { label: 'Qui êtes-vous ?', next: 'v2' } ] },
  v2: { text: '« Mon nom ? Il n\'a plus d\'importance. Ça a mal tourné, ici. Très mal. On attendait quelqu\'un d\'en haut. Personne n\'est descendu. »', options: [
    { label: 'Vous êtes combien ?', next: 'v3' } ] },
  v3: { text: 'Un long silence dans la grille. « Je suis le seul à répondre. Les autres sont là, je les vois d\'ici. Ils ne réclament plus rien. C\'est la seule qualité qui leur reste. »', options: [
    { label: 'Je vais vous sortir de là.', next: 'v4' }, { label: 'Comment vous tenez ?', next: 'v3b' } ] },
  v3b: { text: '« Il reste des rations prévues pour durer plus longtemps que nous. Elles ont gagné. »', options: [ { label: 'Je vais vous sortir de là.', next: 'v4' } ] },
  v4: { text: '« Pas avec ça. Cette porte s\'ouvre d\'ici, et d\'ici je n\'ai plus la main. » Le grésillement monte, retombe. « Steel-Megalopolis. Va à Steel-Megalopolis. Là-bas ils savent ouvrir ce qui est fermé. Dis-leur que quelqu\'un répond encore sous Dusk-Town. »', options: [
    { label: 'J\'irai.', action: 'flag:q_fin', next: 'v5' }, { label: 'Et si personne ne m\'écoute ?', next: 'v4b' } ] },
  v4b: { text: '« Alors dis-le plus fort. Moi, il me reste cette grille et ta voix. »', options: [ { label: 'J\'irai.', action: 'flag:q_fin', next: 'v5' } ] },
  v5: { text: 'Le grésillement se coupe. Le cric glisse, le battant retombe avec un bruit sourd, à sa place. La porte reste fermée.', options: [ { label: 'Partir.', next: 'end' } ] }
};
