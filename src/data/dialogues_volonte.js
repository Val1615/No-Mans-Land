// v15 [proposition] Scènes de menace avec test de Volonté (peur, douleur, intimidation).
// paycr:N = paiement en crédits (Steel, côté ville). [proposition] action à créer dans game.js, sur le modèle de pay.
// Format : test 'attribut:seuil' sur 10, pass/fail remplacent next ; if 'volonte>=7' = réplique sans jet.
// Personnages : Odile (douane de Steel), Nane (guetteuse, Les Poutres), Pic (dealer, Le Tripot). Monnaie Sous-Ville : dollar.
export const DIALOGUES_VOLONTE = {
  // Odile Varga : phrases de formulaire, « motif ? ». Peur : une erreur à son nom. Secret : un cousin par mois contre des dollars.
  odile_volonte: {
    start: { text: 'Attendez. Restez au guichet. Votre implant sort en orange. Motif de l\'entrée ?', options: [
      { label: 'Du travail. Il y a un problème ?', next: 'anomalie' },
      { label: 'Je veux juste passer.', next: 'anomalie' } ] },
    anomalie: { text: 'Votre fiche dit que vous êtes entré il y a trois jours. Par cette porte. Je n\'ai aucune sortie. Alors soit vous êtes encore dedans, soit quelqu\'un porte votre poignet.', options: [
      { label: 'J\'ai marché. J\'ai regardé les vitrines.', next: 'formulaire' },
      { label: 'Ça ne vous regarde pas.', next: 'formulaire' } ] },
    formulaire: { text: 'Voilà le formulaire 12-B. Vous déclarez une sortie non enregistrée. Vous signez, je classe, vous passez. Vous ne signez pas, j\'appelle le poste.', options: [
      { label: 'Je ne signerai rien.', test: 'volonte:6', pass: 'tient', fail: 'cede' },
      { label: 'Appelez le poste. Et dites-leur pour votre cousin.', if: 'info_cousin_odile&volonte>=7', next: 'cousin' },
      { label: 'Bon. Je signe.', action: 'flag:odile_signe;flag:steel_fiche', next: 'signe' },
      { label: 'Il y a des frais pour éviter le poste ?', next: 'frais' } ] },
    tient: { text: 'Elle vous regarde longtemps. Puis elle regarde l\'heure. Il est seize heures cinquante.', options: [
      { label: 'Attendre sans rien dire.', next: 'tient2' } ] },
    tient2: { text: 'Le 12-B, il faut le saisir en trois exemplaires. J\'ai dix minutes. Vous avez eu un faux contact. Ça arrive. Barrière à votre droite.', options: [
      { label: 'Bonne soirée.', action: 'flag:odile_tenu', next: 'end' } ] },
    cede: { text: 'Elle décroche le combiné sans vous quitter des yeux. Votre main signe avant que vous ayez fini d\'y penser.', options: [
      { label: 'Rendre le stylo.', action: 'flag:odile_signe;flag:steel_fiche', next: 'signe' } ] },
    signe: { text: 'Merci. Ça vous fait un signalement mineur. Rien de grave. Ça veut dire que la prochaine fois, ce sera moi ou une autre, et l\'autre lira le signalement.', options: [
      { label: 'Super.', next: 'end' } ] },
    cousin: { text: 'Elle repose le combiné. Très doucement, comme s\'il était chaud.', options: [
      { label: 'Une fois par mois, c\'est ça ?', next: 'cousin2' } ] },
    cousin2: { text: 'Je ne sais pas de quoi vous parlez. Faux contact. Ça arrive. Passez avant que je sache de quoi vous parlez.', options: [
      { label: 'Je pars.', action: 'flag:odile_tenu;flag:odile_menacee', next: 'end' } ] },
    frais: { text: 'Il y a des frais de régularisation. Huit crédits. Il n\'y a pas de reçu, parce que le formulaire de reçu, c\'est aussi le 12-B.', options: [
      { label: 'Payer 8 cr.', action: 'paycr:8;flag:odile_payee', next: 'payee' },
      { label: 'Non. Faites votre 12-B.', test: 'volonte:6', pass: 'tient', fail: 'cede' } ] },
    payee: { text: 'Faux contact. Ça arrive. Barrière à votre droite. Et évitez mon guichet pendant un moment.', options: [
      { label: 'Compris.', next: 'end' } ] },
    pauvre: { text: 'Il manque des crédits. Le 12-B, lui, ne manque jamais.', options: [
      { label: 'Je signe.', action: 'flag:odile_signe;flag:steel_fiche', next: 'signe' } ] },
  },

  // Nane : la guetteuse. Tutoie, rapide, garde le passage. Elle vit de ce qu'elle voit.
  guetteuse_volonte: {
    start: { text: 'Hé. Toi. Tu es passé chez Elio hier soir. Je t\'ai vu ressortir avec une caisse.', options: [
      { label: 'Et alors ?', next: 'alors' },
      { label: 'Tu te trompes de personne.', next: 'trompe' } ] },
    trompe: { text: 'J\'ai un seul travail, c\'est de pas me tromper de personne.', options: [
      { label: 'D\'accord. Et alors ?', next: 'alors' } ] },
    alors: { text: 'Alors la caisse, c\'était pour les gens d\'en face. Et Pic aimerait bien savoir qui livre ses voisins. Il paie bien pour ça. Toi, tu peux payer mieux.', options: [
      { label: 'Combien ?', next: 'combien' },
      { label: 'Va le lui dire. On verra.', test: 'volonte:7', pass: 'tient', fail: 'cede' },
      { label: 'Pic sait déjà que tu lui vends des gens deux fois ?', if: 'volonte>=7', next: 'retourne' },
      { label: 'Je n\'ai rien à te dire.', next: 'partir' } ] },
    combien: { text: 'Dix dollars. Et le mois prochain, dix dollars. Je suis pas gourmande, je suis régulière.', options: [
      { label: 'Payer 10 $.', action: 'pay:10;flag:nane_paie', next: 'paye' },
      { label: 'Non. Pas un dollar.', test: 'volonte:7', pass: 'tient', fail: 'cede' } ] },
    tient: { text: 'Elle attend que tu baisses les yeux. Tu ne les baisses pas. Elle crache à côté de ta chaussure, pas dessus.', options: [
      { label: 'Autre chose ?', next: 'tient2' } ] },
    tient2: { text: 'Laisse tomber. Si je balance tous ceux qui livrent pour Elio, il me reste plus personne à surveiller. Passe.', options: [
      { label: 'C\'est ça.', action: 'flag:nane_tenu', next: 'end' } ] },
    cede: { text: 'Elle siffle deux notes. Au fond, près du tripot, deux types se lèvent. Tu as déjà la main dans la poche.', options: [
      { label: 'Donner 10 $.', action: 'pay:10;flag:nane_paie;flag:nane_cede', next: 'paye' } ] },
    paye: { text: 'Merci. Je me souviens plus de rien. Je me souviendrai plus de rien le mois prochain non plus, si tu reviens.', options: [
      { label: 'Charmant.', next: 'end' } ] },
    retourne: { text: 'Elle rit, mais pas longtemps. Qui t\'a raconté ça ?', options: [
      { label: 'Personne. Tu viens de me le dire.', next: 'retourne2' } ] },
    retourne2: { text: 'Bon. On s\'est rien dit, ni toi ni moi. Et la prochaine fois que tu passes, je regarde ailleurs.', options: [
      { label: 'Ça me va.', action: 'flag:nane_tenu;flag:nane_doit', next: 'end' } ] },
    partir: { text: 'Tu tournes le dos. Elle reste assise. Elle a le temps, elle.', options: [
      { label: 'Partir.', action: 'flag:nane_rancune', next: 'end' } ] },
    pauvre: { text: 'T\'as même pas dix dollars ? Alors file-moi ta montre. Ou tes chaussures, je suis pas difficile.', options: [
      { label: 'Donner ce que j\'ai sur moi.', action: 'flag:nane_paie;flag:nane_depouille', next: 'paye' } ] },
  },

  // Pic : dealer du Tripot. Commerçant, aimable, menace en parlant de prix.
  dealer_volonte: {
    start: { text: 'Assieds-toi. Non, vraiment, assieds-toi. Tu as joué à ma table la semaine dernière.', options: [
      { label: 'J\'ai regardé. Je n\'ai pas joué.', next: 'dette' },
      { label: 'Je ne m\'assieds pas.', next: 'debout' } ] },
    debout: { text: 'Comme tu veux. Le gars derrière toi, lui, il est debout tout le temps. Il a mal au dos, ça le rend nerveux.', options: [
      { label: 'Abrège.', next: 'dette' } ] },
    dette: { text: 'Regarder, c\'est payant. La chaise, l\'éclairage, l\'ambiance. Vingt-cinq dollars. Je t\'ai fait le prix des habitués.', options: [
      { label: 'Je ne te dois rien.', test: 'volonte:6', pass: 'tient', fail: 'cede' },
      { label: 'Tu veux vraiment te faire une réputation sur vingt-cinq dollars ?', if: 'volonte>=7', next: 'reputation' },
      { label: 'Payer 25 $.', action: 'pay:25;flag:pic_paie', next: 'paye' },
      { label: 'Je m\'en vais.', test: 'volonte:5', pass: 'sortie', fail: 'cede' } ] },
    tient: { text: 'Le gars derrière toi pose la main sur ton épaule. Elle pèse. Tu ne bouges pas.', options: [
      { label: 'Tu regardais Pic, pas sa main.', next: 'tient2' } ] },
    tient2: { text: 'Lâche-le. Il a une tête à ne rien avoir sur lui de toute façon. Va, et reviens jouer pour de vrai. Je t\'aime bien, c\'est mauvais signe pour toi.', options: [
      { label: 'Salut, Pic.', action: 'flag:pic_tenu', next: 'end' } ] },
    sortie: { text: 'Tu sors. Personne ne te suit. Derrière toi, Pic dit à quelqu\'un : « Il reviendra. Ils reviennent tous. »', options: [
      { label: 'Continuer.', action: 'flag:pic_rancune', next: 'end' } ] },
    cede: { text: 'La main du gars se referme sur ta nuque. Ton front rencontre la table, poliment, une fois.', options: [
      { label: 'Payer 25 $.', action: 'hurt:3;pay:25;flag:pic_paie;flag:pic_cede', next: 'paye' } ] },
    paye: { text: 'Merci. Tu vois, ça s\'est bien passé. La prochaine fois, joue, au moins tu perdras ton argent en t\'amusant.', options: [
      { label: 'C\'est ça.', next: 'end' } ] },
    reputation: { text: 'Il compte sur ses doigts. Il arrive à vingt-cinq, il se lasse.', options: [
      { label: 'Attendre.', next: 'reputation2' } ] },
    reputation2: { text: 'T\'as raison. Pour vingt-cinq dollars, j\'ai déjà une réputation. Offre-lui un verre, au gars du dos, et on n\'en parle plus.', options: [
      { label: 'Un verre, d\'accord (2 $).', action: 'pay:2;flag:pic_tenu', next: 'end' },
      { label: 'Non. Salut.', action: 'flag:pic_tenu;flag:pic_rancune', next: 'end' } ] },
    pauvre: { text: 'Pas les dollars ? Alors on prend le manteau. Il te va mal, de toute façon.', options: [
      { label: 'Donner le manteau.', action: 'flag:pic_paie;flag:pic_depouille', next: 'end' } ] },
  },
};

// Source de l'info sur le cousin d'Odile : Halloran, au poste de la douane. Option à ajouter à halloran.start, par ex. if: '!race_mutant&!info_cousin_odile'.
export const DIALOGUES_INFO = {
  halloran_cousin: {
    start: { text: 'La guichetière ? Elle compte tout. Sauf un gars, le premier du mois. Il passe sans faire la queue, et il repart avec le même sourire qu\'elle.', options: [
      { label: 'Un parent ?', next: 'cousin' },
      { label: 'Ça ne me regarde pas.', next: 'end' } ] },
    cousin: { text: 'Un cousin, d\'après elle. Moi, je regarde. Je ne fais pas de rapport sur ce que je regarde, sinon j\'écrirais toute la journée.', options: [
      { label: 'Merci, sergent.', action: 'flag:info_cousin_odile', next: 'end' } ] },
  },
};
