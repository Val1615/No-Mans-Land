// Dialogues du quartier 1 (v2). Statut : proposition, à relire avec Valentin.
// L'histoire des rafles s'apprend par fragments, selon qui parle. Chaque nœud : text, options [{ label, next?, action?, if? }].
export const DIALOGUES = {
  mara: {
    start: { text: 'Ferme derrière toi. Doucement, elle grince. Tu es venu par l\'avenue ? En plein jour ?', options: [
      { label: 'Il n\'y avait personne.', next: 'personne', action: 'reveal:clinic' },
      { label: 'C\'est toi qui t\'occupes de la pompe ?', next: 'pompe' },
      { label: 'Je ne fais que passer.', next: 'end' } ] },
    personne: { text: 'Il n\'y a jamais personne. C\'est comme ça qu\'on reste en vie. La prochaine fois, longe les murs et entre par l\'arrière quand tu peux. Et si tu te blesses, Vera recoud à côté, derrière la porte marquée d\'une croix.', options: [
      { label: 'Vous vous cachez de qui ?', next: 'qui' }, { label: 'Compris.', next: 'end' } ] },
    qui: { text: 'Des soldats de la capitale. Ils passent par ici pour aller plus loin, et ils ne repartent jamais les mains vides. Demande à Bruno, si tu veux savoir. Ou ne lui demande pas.', options: [
      { label: 'D\'accord.', next: 'end' } ] },
    pompe: { text: 'Je pompe la nuit. Le joint du piston est fichu, ça siffle, et un sifflement la nuit s\'entend jusqu\'au bout de la rue. Nilo pourrait le refaire avec du caoutchouc qui n\'a pas cuit au soleil.', options: [
      { label: 'Je peux en chercher.', next: 'aide', action: 'flag:pompe_aide' }, { label: 'Bonne chance.', next: 'end' } ] },
    aide: { text: 'Les pneus devant l\'atelier, peut-être. Fais vite et ne reste pas planté au milieu de l\'avenue.', options: [ { label: 'Promis.', next: 'end' } ] }
  },
  bruno: {
    start: { text: '...Mara t\'a laissé entrer. Bon. Ne reste pas devant le rideau, on te voit de la fenêtre.', options: [
      { label: 'Tu vis ici ?', next: 'ici' }, { label: 'Pardon. Je te laisse.', next: 'end' } ] },
    ici: { text: 'Depuis deux saisons. Avant, j\'étais au nord, avec mon frère. Une patrouille est arrivée avant l\'aube. Ils avaient des lampes qui voient sous la peau. Lui, ils l\'ont trouvé.', options: [
      { label: 'Ils l\'ont emmené où ?', next: 'ou' }, { label: 'Je suis désolé.', next: 'desole' } ] },
    ou: { text: 'Personne ne pose la question deux fois. Mara dit qu\'ils ont aussi pris deux hommes d\'ici qui n\'avaient rien de mutant. Ils ont mal regardé. Ou ils s\'en fichaient.', options: [
      { label: 'Et toi, tu restes caché ici ?', next: 'reste' }, { label: 'Merci de m\'avoir dit ça.', next: 'end' } ] },
    desole: { text: 'Tout le monde l\'est. Ça ne fait pas revenir les gens, mais ça se dit.', options: [ { label: 'Je m\'en vais.', next: 'end' } ] },
    reste: { text: 'Je sors la nuit, je porte l\'eau pour Mara. Le jour, je compte les poutres du plafond. Il y en a quatorze.', options: [ { label: 'À bientôt, Bruno.', next: 'end' } ] }
  },
  vera: {
    start: { text: 'Pas de bruit dans le couloir. Assieds-toi là. Tu saignes encore, ou c\'est de la vieille poussière ?', options: [
      { label: 'Tu peux me remettre d\'aplomb ?', next: 'soin', if: 'hurt' },
      { label: 'Tu soignes qui, en général ?', next: 'qui' }, { label: 'Juste de passage.', next: 'end' } ] },
    soin: { text: 'Quinze dollars. Désinfection, deux points, et tu ne racontes à personne où tu as été recousu.', options: [
      { label: 'Payer 15 $', action: 'heal:15', next: 'apres' }, { label: 'Plus tard.', next: 'end' } ] },
    apres: { text: 'Voilà. Tu tiendras jusqu\'à la prochaine bêtise.', options: [ { label: 'Merci, Vera.', next: 'end' } ] },
    pauvre: { text: 'Je ne fais pas crédit. Le fil coûte plus cher que toi, ici.', options: [ { label: 'Compris.', next: 'end' } ] },
    qui: { text: 'Ceux qui ont couru trop tard. Après une descente, j\'ai des coupures, des chevilles tordues, et des gens qui ne disent plus rien pendant trois jours.', options: [
      { label: 'Il y en a souvent, des descentes ?', next: 'souvent' }, { label: 'Je vois.', next: 'end' } ] },
    souvent: { text: 'Assez pour que je garde toujours une civière pliée derrière la porte.', options: [ { label: 'Merci.', next: 'end' } ] }
  },
  hector: {
    start: { text: 'Parle bas. Les murs ont des trous, et les trous ont des oreilles. Tu bois, tu manges, ou tu poses des questions ?', options: [
      { label: 'Un repas (6 $)', action: 'buy:meal:6', next: 'repas' }, { label: 'Un verre (3 $)', action: 'buy:drink:3', next: 'verre' },
      { label: 'Pourquoi tout le monde se terre ?', next: 'terre' }, { label: 'Rien pour l\'instant.', next: 'end' } ] },
    repas: { text: 'Ragoût de lézard. Ne demande pas lequel.', options: [ { label: 'Autre chose ?', next: 'start' }, { label: 'Merci.', next: 'end' } ] },
    verre: { text: 'Distillé à l\'arrière. Ça brûle en descendant, et ça aide à dormir quand les camions passent.', options: [ { label: 'Autre chose ?', next: 'start' }, { label: 'Santé.', next: 'end' } ] },
    terre: { text: 'On est sur leur route. Les soldats de Steel font halte ici avant d\'aller fouiller les terres. Ils remplissent leurs gourdes, ils fouillent deux ou trois maisons, et ils repartent avec qui leur plaît.', options: [
      { label: 'Et personne ne se défend ?', next: 'defense' }, { label: 'Merci, Hector.', next: 'end' } ] },
    defense: { text: 'Avec quoi ? La seule défense qui marche, c\'est qu\'ils trouvent une ville morte. Alors on la leur montre. Tu as vu la façade de mon bar ? J\'ai mis un an à la rendre aussi moche.', options: [ { label: 'Elle est réussie.', next: 'end' } ] },
    pauvre: { text: 'Ta bourse sonne creux. Reviens quand elle chantera.', options: [ { label: 'D\'accord.', next: 'end' } ] }
  },
  ileana: {
    start: { text: 'Assieds-toi si tu veux, mais ne me demande pas mon nom deux fois. Ileana. Voilà.', options: [
      { label: 'Tu n\'es pas d\'ici.', next: 'pasici' }, { label: 'Je te laisse tranquille.', next: 'end' } ] },
    pasici: { text: 'Ranch Liberté, avant. Les Invictos. On m\'a laissée partir, ou on ne m\'a pas retenue, selon qui raconte.', options: [
      { label: 'Et tu fais quoi à Dusk-Town ?', next: 'quoi' }, { label: 'Pourquoi être partie ?', next: 'pourquoi' } ] },
    quoi: { text: 'J\'attends une caravane qui ne vient pas. Au ranch, on dit que les gens d\'ici sont fous de vivre sur la route des soldats. Ici, on dit que ceux du ranch sont fous de vivre sans portes. Je n\'ai pas encore choisi.', options: [ { label: 'Bonne attente.', next: 'end' } ] },
    pourquoi: { text: 'Ça ne te regarde pas. Bois ton verre.', options: [ { label: 'Pardon.', next: 'end' } ] }
  },
  anselme: {
    start: { text: 'Entre, entre, et ferme. Eau filtrée, quatre dollars. Rations, cinq. Je compte devant toi, comme ça personne ne se fâche.', options: [
      { label: 'Une bouteille d\'eau (4 $)', action: 'buy:water:4', next: 'ok' }, { label: 'Une ration (5 $)', action: 'buy:ration:5', next: 'ok' },
      { label: 'Ta boutique a l\'air fermée depuis des années.', next: 'fermee' }, { label: 'Au revoir.', next: 'end' } ] },
    ok: { text: 'Un, deux, trois, quatre... c\'est bon. Autre chose ?', options: [ { label: 'Oui.', next: 'start' }, { label: 'Non, merci.', next: 'end' } ] },
    fermee: { text: 'Merci, ça me fait plaisir. Rien dehors, pas de linge, pas de pot de fleurs, pas de fumée le jour. Ma femme avait un géranium sur le rebord. C\'est le géranium qu\'ils ont vu en premier.', options: [ { label: 'Je suis désolé.', next: 'start' }, { label: 'Au revoir.', next: 'end' } ] },
    pauvre: { text: 'Il te manque de quoi. Je ne fais pas crédit, même aux gens polis.', options: [ { label: 'Tant pis.', next: 'end' } ] }
  }
};
export const ITEMS = { meal: { name: 'Repas', heal: 5, consumeNow: true }, drink: { name: 'Verre', heal: 1, consumeNow: true }, water: { name: 'Eau filtrée' }, ration: { name: 'Ration' } };
