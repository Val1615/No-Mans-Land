// [proposition] Petits boulots en dollars à Dusk-Town : quêtes A (l'eau du poste), B (la dette d'Ezequiel), ferraille chez Anselme, « Les Trois Os » chez Teo.
// Format de dialogues_volonte.js. Actions nouvelles à brancher (voir docs/ARGENT_DUSKTOWN.md) : gain:N, give:objet[:n], sell:objet:N, os:mise:N, os:bluff.
// Actions existantes réutilisées : pay:N, hurt:N, take:objet, flag:x, hook:x, test, if, next:'arbre/noeud'.
// Total accessible sans le jeu : 12 (A) + 15 (B) + 22 (ferraille) = 49 $.
export const DIALOGUES_ARGENT = {
  // Quête A. Sol, gardienne de la citerne des Sables. Elle ravitaille en douce le vieux poste du bord, au bout du Transit.
  // Option à ajouter à sol.start : { label: 'Tu as du travail ?', next: 'sol_eau/start', if: '!a_debut' }
  sol_eau: {
    start: { text: 'Du travail ? Peut-être. Tu connais le poste du bord, au bout du Transit, derrière les sacs de sable ? Il y a trois personnes dedans. Elles ne sortent pas, et elles n\'ont plus d\'eau depuis hier.', options: [
      { label: 'Qui sont-ils ?', next: 'qui' },
      { label: 'Combien ?', next: 'prix' },
      { label: 'Pas maintenant.', next: 'end' } ] },
    qui: { text: 'Des gens qui ont de bonnes raisons de ne pas venir jusqu\'ici. Ça te suffit, ou tu veux leurs noms pour les vendre à Teo ?', options: [
      { label: 'Ça me suffit.', next: 'prix' } ] },
    prix: { text: 'Quatre bidons. Douze dollars à la livraison, c\'est eux qui paient, ils me remboursent ensuite. Ne passe pas par le milieu de l\'avenue, et ne t\'arrête pas pour causer.', options: [
      { label: 'D\'accord, donne.', action: 'give:bidon:4;flag:a_debut', next: 'parti' },
      { label: 'Quatre bidons, c\'est lourd pour douze dollars.', next: 'lourd' },
      { label: 'Non.', next: 'end' } ] },
    lourd: { text: 'C\'est lourd pour eux aussi, de crever de soif. Douze. Je n\'ai pas d\'autre prix.', options: [
      { label: 'Bon. Donne.', action: 'give:bidon:4;flag:a_debut', next: 'parti' },
      { label: 'Trouve quelqu\'un d\'autre.', next: 'end' } ] },
    parti: { text: 'Les bouchons sont serrés, ne les touche pas. Si un bidon arrive à moitié vide, ils le verront, et moi je le saurai.', options: [
      { label: 'Compris.', next: 'end' } ] },
    // Retour chez Sol (option : if: 'a_fini')
    retour: { text: 'Ils m\'ont fait passer le mot. Merci.', alt: [ { if: 'a_garde', text: 'Il manquait un bidon. Tu croyais que personne ne compterait ? Ils sont trois là-dedans, ils comptent tout. Bois ton eau, tu l\'as payée. Moi, je ne te confie plus rien.' } ], options: [
      { label: 'À la prochaine.', next: 'end' } ] }
  },

  // Rencontre sur le trajet : un rôdeur sorti du désert. Scène sans sprite, lancée par game.startScene (voir doc).
  rodeur: {
    start: { text: 'Un homme sort de derrière l\'épave. Maigre, les lèvres fendues, une barre de fer à la main. Il ne regarde pas ton visage. Il regarde les bidons.', options: [
      { label: 'Poser un bidon par terre et reculer.', action: 'take:bidon;flag:a_rodeur_paye', next: 'cede_eau' },
      { label: 'Le regarder en face. « Recule. »', test: 'volonte:6', pass: 'recule', fail: 'frappe' },
      { label: 'Lâcher rien et courir.', next: 'fuite' } ] },
    recule: { text: 'Il hésite. Tu n\'as pas bougé d\'un centimètre. Il crache dans le sable et repart vers les ruines, sans se presser, pour sauver la face.', options: [
      { label: 'Continuer.', action: 'flag:a_rodeur_fait', next: 'end' } ] },
    frappe: { text: 'Ta voix tremble sur le dernier mot. Il l\'entend. La barre te prend à l\'épaule. Tu te relèves, il est déjà loin, et tes bidons sont toujours là. Il voulait seulement te faire mal.', options: [
      { label: 'Ramasser les bidons.', action: 'hurt:5;flag:combat_rodeur;combat:rodeur', next: 'end' } ] },
    fuite: { text: 'Tu cours avec quatre bidons qui cognent. Il te rattrape au coin, te bouscule contre un mur, puis renonce : il n\'a plus de souffle non plus.', options: [
      { label: 'Repartir en boitant.', action: 'hurt:3;flag:combat_rodeur;combat:rodeur', next: 'end' } ] },
    cede_eau: { text: 'Il prend le bidon à deux mains, boit tout de suite, la moitié lui coule dans le cou. Il ne dit pas merci.', options: [
      { label: 'Continuer.', action: 'flag:a_rodeur_fait', next: 'end' } ] }
  },

  // Variante facultative : un camion du Service Militarisé passe pendant la livraison.
  raid: {
    start: { text: 'Un bruit de moteur, côté est. Pas le temps d\'atteindre une porte. Tu te plaques derrière un tas de pneus avec les bidons. Les bottes descendent du camion à vingt mètres.', options: [
      { label: 'Ne plus bouger. Attendre.', test: 'volonte:5', pass: 'passe', fail: 'bouge' } ] },
    passe: { text: 'Un soldat pisse contre le mur d\'en face en parlant de sa solde. Ils remontent. Le camion repart vers La Pompe. Tu as mal aux genoux à force de ne pas respirer.', options: [
      { label: 'Repartir.', action: 'flag:a_raid_fait', next: 'end' } ] },
    bouge: { text: 'Ta jambe glisse, un bidon roule. Un soldat se retourne, voit un bidon et un tas de pneus. Il tire dans le bidon pour rire. Un éclat te coupe la main.', options: [
      { label: 'Attendre qu\'ils partent.', action: 'hurt:3;take:bidon;flag:a_raid_fait', next: 'end' } ] }
  },

  // Le poste du bord. Une voix derrière les sacs de sable. Pas de sprite (scène, comme la porte d'acier).
  poste: {
    start: { text: 'Une voix basse, derrière les sacs : « C\'est Sol qui t\'envoie ? Pose-les contre le mur et recule de trois pas. »', options: [
      { label: 'Poser les quatre bidons.', if: 'inv:bidon>=4', action: 'take:bidon;take:bidon;take:bidon;take:bidon;gain:12;flag:a_fini', next: 'merci' },
      { label: 'Poser ce que j\'ai. Un rôdeur m\'en a pris un.', if: 'inv:bidon<=3&a_rodeur_paye', action: 'take:bidon;take:bidon;take:bidon;gain:8;flag:a_fini', next: 'excuse' },
      { label: 'Poser ce qu\'il reste. Les soldats en ont crevé un.', if: 'inv:bidon<=3&!a_rodeur_paye', action: 'take:bidon;take:bidon;take:bidon;gain:8;flag:a_fini', next: 'excuse' },
      { label: 'En poser trois. Garder le dernier pour moi.', if: 'inv:bidon>=4', action: 'take:bidon;take:bidon;take:bidon;gain:8;give:water;flag:a_fini;flag:a_garde', next: 'compte' } ] },
    merci: { text: 'Une main passe entre deux sacs et laisse des billets roulés sur le rebord. Douze. « Dis à Sol que la petite va mieux. »', options: [
      { label: 'Je lui dirai.', next: 'end' } ] },
    excuse: { text: 'Un silence. « Trois, alors. On paie ce qui arrive. » Huit dollars sur le rebord.', options: [
      { label: 'Désolé.', next: 'end' } ] },
    compte: { text: 'On les entend compter derrière le mur, deux fois. « Trois. » Huit dollars sur le rebord, et plus un mot.', options: [
      { label: 'Partir.', next: 'end' } ] }
  },

  // Quête B. Hector (bar, La Pompe) fait crédit à Ezequiel depuis des mois. Ezequiel est le seul à réparer quoi que ce soit en ville.
  // Option à ajouter à hector.start : { label: 'Du travail pour moi ?', next: 'dette_hector/start', if: '!b_debut' }
  dette_hector: {
    start: { text: 'Du travail ? Ezequiel. Il me doit trente dollars de ragoût et de verres. Ramène-m\'en la moitié et je te donne quinze. Le reste, je le passe en pertes, comme ma jeunesse.', options: [
      { label: 'Pourquoi tu n\'y vas pas toi-même ?', next: 'pourquoi' },
      { label: 'J\'y vais.', action: 'flag:b_debut', next: 'end' } ] },
    pourquoi: { text: 'Parce que si je monte au Scellé lui réclamer de l\'argent, il ne remettra plus les pieds ici. Et c\'est lui qui me répare l\'alambic. Toi, il peut te détester, ça ne me coûte rien.', options: [
      { label: 'Merci pour moi.', action: 'flag:b_debut', next: 'end' } ] },
    // Retours (options à ajouter à hector.start selon les drapeaux ; echec : if 'b_echec&!b_fini')
    paye: { text: 'Quinze. Il a craché ou il a pleuré ? Peu importe. Voilà ta part, quinze aussi. Les comptes sont ronds, j\'aime ça.', options: [
      { label: 'Merci, Hector.', action: 'pay:15;gain:15;flag:b_fini', next: 'end' } ] },
    outils: { text: 'Des clés ? Qu\'est-ce que tu veux que j\'en fasse, que je serre le ragoût ? Garde-les. Va les vendre chez Anselme, il achète tout ce qui brille. Moi, je rouvre l\'ardoise d\'Ezequiel à zéro et je ne te dois rien.', options: [
      { label: 'Tant pis.', action: 'flag:b_fini', next: 'end' } ] },
    toi: { text: 'Tu paies sa dette avec ton argent ? Tu es un saint ou un idiot, et je n\'ai jamais eu besoin de savoir la différence. L\'ardoise est effacée.', options: [
      { label: 'Elle l\'est.', action: 'flag:b_fini', next: 'end' } ] },
    echec: { text: 'Il t\'a eu avec la canne ? Je t\'avais dit qu\'il était rapide. Non, je ne te l\'avais pas dit. Assieds-toi, la soupe est offerte. L\'argent, je l\'oublie, et toi aussi.', options: [
      { label: 'Merci pour la soupe.', action: 'flag:b_fini', next: 'end' } ] }
  },
  // Option à ajouter à ezequiel.start : { label: 'Hector m\'envoie. Pour ton ardoise.', next: 'dette_ezequiel/start', if: 'b_debut&!b_regle' }
  dette_ezequiel: {
    start: { text: 'Hector ? Il t\'envoie, maintenant ? Il a peur de grimper jusqu\'ici avec son ventre. Je n\'ai pas quinze dollars, petit. J\'ai des pièces détachées et une jambe qui ne marche pas.', options: [
      { label: 'Tu as quinze dollars. Sors-les.', test: 'volonte:7', pass: 'cede', fail: 'canne' },
      { label: 'Qu\'est-ce que tu as d\'autre ?', next: 'outils' },
      { label: 'Je la paie pour toi.', next: 'toi' },
      { label: 'Je repasserai.', next: 'end' } ] },
    cede: { text: 'Il soutient ton regard un moment, puis il ouvre une boîte de conserve sous l\'établi et compte quinze dollars en petites coupures. Lentement, pour que tu voies chaque billet.', options: [
      { label: 'Prendre l\'argent.', action: 'gain:15;flag:b_regle;flag:b_argent;flag:ezequiel_rancune', next: 'apres' } ] },
    apres: { text: 'Dis à Hector qu\'il me doit l\'alambic, la prochaine fois qu\'il fuira. Et toi, ne reviens pas me demander où il y a de la ferraille.', options: [
      { label: 'Salut.', next: 'end' } ] },
    canne: { text: 'Tu n\'as pas fini ta phrase que sa canne te prend au tibia. Pour un homme qui boite, il est rapide. « Dehors. Et dis à Hector de venir lui-même. »', options: [
      { label: 'Sortir.', action: 'hurt:4;flag:b_regle;flag:b_echec', next: 'end' } ] },
    outils: { text: 'Mon jeu de clés à cliquet. Il vient d\'un camion de la capitale, il en manque une, la treize. Anselme t\'en donnera huit dollars. Hector n\'en voudra pas, mais ça, c\'est ton problème.', options: [
      { label: 'Je prends les clés.', action: 'give:cles;flag:b_regle;flag:b_outils', next: 'merci' },
      { label: 'Non, je veux l\'argent.', next: 'start' } ] },
    merci: { text: 'Tu es plus arrangeant que ton patron. Prends soin de la clé de dix, c\'est la seule qui tient.', options: [
      { label: 'D\'accord.', next: 'end' } ] },
    toi: { text: 'Toi ? Pourquoi ?', options: [
      { label: 'Parce que tu répares, et que cette ville en a besoin. Je vais voir Hector.', action: 'pay:15;flag:b_regle;flag:b_paye_moi;flag:ezequiel_allie', next: 'allie' },
      { label: 'Laisse tomber.', next: 'start' } ] },
    allie: { text: 'Hm. Je n\'aime pas devoir quelque chose aux gens. Bon. Si un jour tu as un truc cassé, tu viens ici d\'abord. Avant Anselme, avant n\'importe qui.', options: [
      { label: 'Je m\'en souviendrai.', next: 'end' } ] },
    pauvre: { text: 'Tu n\'as pas quinze dollars non plus ? Alors on est deux. Assieds-toi, on va pleurer ensemble.', options: [
      { label: 'Une autre fois.', next: 'end' } ] }
  },

  // Ferraille chez Anselme. Prix fixes. Option à ajouter à anselme.start : { label: 'Tu achètes de la ferraille ?', next: 'ferraille/start' }
  ferraille: {
    start: { text: 'De la ferraille ? J\'achète, si c\'est propre et si ça sert. Pièce mécanique, deux dollars. Circuit, quatre. Batterie qui tient la charge, six. Je ne discute pas, je compte.', options: [
      { label: 'Une pièce (2 $)', if: 'inv:piece>=1', action: 'sell:piece:2', next: 'compte' },
      { label: 'Un circuit (4 $)', if: 'inv:circuit>=1', action: 'sell:circuit:4', next: 'compte' },
      { label: 'Une batterie (6 $)', if: 'inv:batterie>=1', action: 'sell:batterie:6', next: 'compte' },
      { label: 'Un jeu de clés à cliquet (8 $)', if: 'inv:cles>=1', action: 'sell:cles:8', next: 'cles' },
      { label: 'Où est-ce que j\'en trouve ?', next: 'ou' },
      { label: 'Rien pour l\'instant.', next: 'end' } ] },
    compte: { text: 'Un, deux... c\'est bon. Pose, je regarde le reste.', options: [
      { label: 'J\'ai autre chose.', next: 'start' }, { label: 'C\'est tout.', next: 'end' } ] },
    cles: { text: 'Le jeu d\'Ezequiel. Il manque la treize, il manquait déjà la treize il y a dix ans. Huit dollars, et ne lui dis pas que c\'est moi qui l\'ai.', options: [
      { label: 'Autre chose ?', next: 'start' }, { label: 'Merci.', next: 'end' } ] },
    ou: { text: 'Dans ce qui traîne dehors, chez ceux qui n\'ont pas eu le temps de rentrer. Les épaves, les caisses, les pneus. Ramasse vite et rentre. Ce qui est dehors depuis trop longtemps, les soldats l\'ont déjà vu.', options: [
      { label: 'D\'accord.', next: 'start' } ] }
  },

  // « Les Trois Os », chez Teo, au guet. Gains plafonnés à 15 $ sur toute la partie.
  // Option à ajouter à teo.start : { label: 'Tu joues ?', next: 'trois_os/start' }
  trois_os: {
    start: { text: 'Les Trois Os ? Trois dés chacun, je lance après toi. Le plus gros total gagne, un brelan bat tout. Égalité, chacun reprend sa mise. Entre un et cinq dollars, pas plus, je ne suis pas une banque.',
      alt: [ { if: 'os_plafond', text: 'Non. Tu m\'as pris quinze dollars, c\'est ma place sur la caravane qui recule. Je ne joue plus avec toi. Jamais.' } ], options: [
      { label: 'Miser 1 $', if: '!os_plafond', action: 'os:mise:1', next: 'lance' },
      { label: 'Miser 3 $', if: '!os_plafond', action: 'os:mise:3', next: 'lance' },
      { label: 'Miser 5 $', if: '!os_plafond', action: 'os:mise:5', next: 'lance' },
      { label: 'Les règles, encore une fois.', if: '!os_plafond', next: 'regles' },
      { label: 'Pas aujourd\'hui.', next: 'end' } ] },
    regles: { text: 'Tu lances tes trois dés, je lance les miens. Le total le plus haut prend la mise. Trois dés pareils, c\'est un brelan, ça bat n\'importe quel total. Si deux brelans, le plus haut gagne. Et une fois par partie, si tu arrives à me faire croire que mes dés ont triché, tu relances les tiens. Si je ne te crois pas, tu perds ta mise tout de suite.', options: [
      { label: 'Compris.', next: 'start' } ] },
    // Après os:mise, le moteur lance les dés du joueur et remplit {joueur}. Le joueur voit ses dés avant ceux de Teo.
    lance: { text: 'Tu lances : {joueur}. Teo secoue ses dés dans sa paume, longtemps, en te regardant.', options: [
      { label: 'Vas-y, lance.', action: 'os:maison', next: 'resultat' },
      { label: 'Attends. Ta manche. Tu as changé un dé.', if: '!os_bluff_fait', action: 'flag:os_bluff_fait', test: 'volonte:6', pass: 'bluff_ok', fail: 'bluff_rate' } ] },
    bluff_ok: { text: 'Il ouvre la main, vexé. « J\'ai rien changé. » Mais il rougit, et tu ramasses déjà tes dés. Tu relances : {joueur}.', options: [
      { label: 'À toi.', action: 'os:relance;os:maison', next: 'resultat' } ] },
    bluff_rate: { text: 'Il rit. « Ma manche ? Tiens, regarde ma manche. » Elle est vide. « Tricher, c\'est pour ceux qui perdent. Ta mise est à moi. »', options: [
      { label: 'Bon.', action: 'os:perd', next: 'fin' } ] },
    // os:maison choisit le nœud gagne / perd / egal selon les dés (voir doc).
    resultat: { text: 'Teo lance : {maison}.', options: [ { label: 'Alors ?', action: 'os:resout', next: 'egal' } ] },
    gagne: { text: 'Il pousse les billets vers toi du bout du doigt, comme s\'ils étaient sales. « Encore. »', options: [
      { label: 'Encore.', next: 'start' }, { label: 'J\'arrête là.', next: 'fin' } ] },
    perd: { text: 'Il prend ta mise et la plie en quatre dans sa chaussure. « Merci pour la caravane. »', options: [
      { label: 'Encore.', next: 'start' }, { label: 'J\'arrête là.', next: 'fin' } ] },
    egal: { text: 'Pareil. Il grogne. Chacun reprend son argent.', options: [
      { label: 'Encore.', next: 'start' }, { label: 'J\'arrête là.', next: 'fin' } ] },
    plafond: { text: 'Il range ses dés dans une boîte d\'allumettes. « C\'est fini. Tu as gagné assez. Moi, j\'ai perdu assez. Va dépenser ça loin de mon volet. »', options: [
      { label: 'Salut, Teo.', action: 'flag:os_plafond', next: 'end' } ] },
    fin: { text: 'Il remet les dés dans sa poche. « Reviens quand tu veux perdre. »', options: [
      { label: 'Salut.', action: 'os:finpartie', next: 'end' } ] },
    pauvre: { text: 'Pas d\'argent, pas de dés. Tu connais la règle, elle est de moi.', options: [
      { label: 'D\'accord.', next: 'end' } ] }
  }
};

// Objets à ajouter à ITEMS (dialogues_town.js ou fusion côté Développement).
export const ITEMS_ARGENT = {
  bidon: { name: 'Bidon d\'eau (pour le poste)' },
  cles: { name: 'Jeu de clés à cliquet' },
  piece: { name: 'Pièce mécanique' },
  circuit: { name: 'Circuit' },
  batterie: { name: 'Batterie' }
};

// Ferraille ramassable : 7 points, une fois chacun (drapeau ramasse_<id>). Total 22 $ chez Anselme. Positions = props existants.
export const FERRAILLE = [
  { id: 'f_q1_epave', location: 'dusk_q1', x: 45.5, z: 16.6, item: 'circuit', text: 'Sous le tableau de bord de l\'épave, une carte électronique encore propre.' },
  { id: 'f_q1_pneus', location: 'dusk_q1', x: 38.6, z: 23.0, item: 'piece', text: 'Une jante, et coincé dedans, un roulement qui tourne encore.' },
  { id: 'f_q2_epave', location: 'dusk_q2', x: 20.5, z: 19.6, item: 'batterie', text: 'Sous le capot, une batterie. Lourde. Le témoin s\'allume quand tu appuies.' },
  { id: 'f_q2_caisse', location: 'dusk_q2', x: 23.2, z: 23.2, item: 'piece', text: 'Au fond de la caisse, une poignée de boulons et une charnière.' },
  { id: 'f_q3_caisse', location: 'dusk_q3', x: 21.6, z: 10.8, item: 'circuit', text: 'Un boîtier éventré. Le circuit à l\'intérieur n\'a pas brûlé.' },
  { id: 'f_q3_pneus', location: 'dusk_q3', x: 9.8, z: 22.6, item: 'piece', text: 'Une valve en laiton, dévissée à la main.' },
  { id: 'f_q4_charrette', location: 'dusk_q4', x: 31.8, z: 11.8, item: 'piece', text: 'L\'axe de la charrette tient avec un ressort. Le ressort, lui, tient tout seul.' }
];
