// v9 : quête test « La porte d'acier ». Déroulé et canon : docs/quetes/QUETE_TEST_LABO.md. Les étapes se lisent dans state.flags.
// v12 : suite jusqu'à l'entrée dans Steel-Megalopolis [décision : la quête s'arrête une fois en ville]. « show » = étape visible selon l'état.
export const QUESTS = [{
  id: 'porte', title: 'La porte d\'acier',
  visible: s => s.discovered.s_atelier || s.flags.q_start,
  steps: [
    { done: 'q_start', text: 'Demander à Ezequiel (l\'atelier, Le Scellé) qui a tenté la porte' },
    { done: 'q_cric', text: 'Trouver de quoi forcer : le cric d\'Anselme (épicerie, La Pompe)' },
    { done: 'q_signal', text: 'Choisir le moment : Teo (le guet, Le Transit)' },
    { done: 'q_fin', text: 'Forcer la porte d\'acier du Scellé' },
    { done: 'q_steel', text: 'Aller à Steel-Megalopolis : la route des patrouilles, au bout du Transit', show: s => !s.flags.steel_refuse && !s.flags.steel_attaque && !s.flags.sol_passage },
    { done: 'sol_passage', text: 'Refoulé à la douane. Sol (la citerne, Les Sables) connaît peut-être un autre chemin', show: s => !s.flags.q_steel && (s.flags.steel_refuse || s.flags.steel_attaque) && !s.flags.sv_jete },
    { done: 'bruno_frere', text: 'Bruno (chez Mara, La Pompe) : demander le nom de son frère', show: s => !s.flags.q_steel && s.flags.sol_passage && !s.flags.sv_jete },
    { done: 'sv_passage', text: 'Trouver Elio dans la Sous-Ville, par la trappe au sud de la douane', show: s => !s.flags.q_steel && (s.flags.bruno_frere || s.flags.sv_jete) },
    { done: 'q_steel', text: 'Remonter à Center-Town par le monte-charge d\'Elio', show: s => !s.flags.q_steel && s.flags.sv_passage },
    { done: null, text: 'Arrivé à Steel-Megalopolis. La suite attendra : d\'abord, apprendre la ville.', show: s => !!s.flags.q_steel } ]
}];
export const QUEST_NOTES = { q_battant: 'Ezequiel : seul le bas du battant gauche bouge.', q_menti_anselme: 'Anselme : je lui ai dit que le cric était pour Mara.', q_trahi: 'Teo : je lui ai vendu le secret d\u2019Ezequiel.',
  steel_refuse: 'Douane de Steel : pas d\u2019implant, pas d\u2019entrée.', steel_fui: 'Douane de Steel : un soldat m\u2019a tiré dessus.', steel_capture: 'Douane de Steel : capturé, puis jeté dehors près d\u2019une trappe.', sv_jete: 'Jeté dans la Sous-Ville par les soldats.', sv_mot: 'Sous-Ville : la guetteuse m\u2019a laissé passer. Elio est à la Cuve.', sv_passage: 'Elio me fait remonter par le monte-charge.', bruno_frere: 'Le frère de Bruno s\u2019appelle Elio. Le mot : « quatorze poutres ».' };
