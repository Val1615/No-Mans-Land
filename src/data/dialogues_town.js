// v7 : dialogues des quartiers 2 à 4. Fiches (désir, peur, secret) dans docs/quartiers/DUSK_TOWN_PLAN.md.
import { DIALOGUES as D1, ITEMS as I1 } from './dialogues_q1.js';
export const DIALOGUES = {
  ...D1,
  // Teo, 17 ans, guetteur du Transit. Phrases courtes, il parle en regardant la fente du volet.
  teo: {
    start: { text: 'Ferme. Doucement. Si tu viens de l\'ouest, tu as marché au milieu de l\'avenue, je t\'ai vu. Ne refais pas ça.', options: [
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
    pauvre: { text: 'Pas de dollars, pas de nouvelles. C\'est la règle, elle est de moi.', options: [ { label: 'D\'accord.', next: 'end' } ] }
  },
  // Ezequiel, récupérateur, la cinquantaine. Lent, sec, appelle tout le monde « petit ».
  ezequiel: {
    start: { text: 'Si tu viens pour la porte, petit, fais la queue derrière moi. Ça fait trois semaines que je suis le premier.', options: [
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
export const ITEMS = { ...I1, tip: { name: 'Tuyau', consumeNow: true } };
