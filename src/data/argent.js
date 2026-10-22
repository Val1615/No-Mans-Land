// Réglages de l'argent à Dusk-Town (Développement). Contenu narratif : dialogues_argent.js (Création).
export const ARGENT = {
  trois_os: { mises: [1, 3, 5], miseMax: 5, plafondGains: 15, bluffSeuil: 6, des: 3, faces: 6 }, // plafond : gains nets sur TOUTE la partie (sauvegardé)
  raid: { chance: 0.5 },          // tirage du camion au premier passage dans dusk_q2 pendant la livraison
  // Drapeaux purement techniques : posés sans message « Journal : piste notée »
  flagsTechniques: [/^os_/, /^ramasse_/, /_fait$/, /^combat_/, /^a_rodeur_paye$/, /^b_regle$/]
};
