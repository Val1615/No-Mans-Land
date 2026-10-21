// v9 : quête test « La porte d'acier ». Déroulé et canon : docs/quetes/QUETE_TEST_LABO.md. Les étapes se lisent dans state.flags.
export const QUESTS = [{
  id: 'porte', title: 'La porte d\'acier',
  visible: s => s.discovered.s_atelier || s.flags.q_start,
  steps: [
    { done: 'q_start', text: 'Demander à Ezequiel (l\'atelier, Le Scellé) qui a tenté la porte' },
    { done: 'q_cric', text: 'Trouver de quoi forcer : le cric d\'Anselme (épicerie, La Pompe)' },
    { done: 'q_signal', text: 'Choisir le moment : Teo (le guet, Le Transit)' },
    { done: 'q_fin', text: 'Forcer la porte d\'acier du Scellé' },
    { done: null, text: 'Aller à Steel-Megalopolis', blocked: 'Hors de portée pour l\'instant : la route n\'existe pas encore.' } ]
}];
export const QUEST_NOTES = { q_battant: 'Ezequiel : seul le bas du battant gauche bouge.', q_menti_anselme: 'Anselme : je lui ai dit que le cric était pour Mara.', q_trahi: 'Teo : je lui ai vendu le secret d\u2019Ezequiel.' };
