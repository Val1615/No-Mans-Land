// Catalogue des ressources du jeu, partagé par le jeu (src/main.js) et l'éditeur de cartes (editor/source.js) :
// tous les manifestes d'assets, fusionnés selon les mêmes règles, et la liste des sols (textures g_*) avec leur chemin.
// Ajouter un quartier de Steel = ajouter son dossier ici ; aucun manifeste n'est modifié.
export const QUARTIERS_STEEL = ['pulse_plaza', 'frequence_strip', 'steel_arena', 'dome_frequence', 'mega_line'];
export const SOLS_BASE = ['g_sand', 'g_asphalt', 'g_dirt', 'g_gravel', 'g_grass', 'g_concrete', 'g_wood']; // assets/mockup/
export const SOLS_GENERES = ['g_wet', 'g_sv', 'g_cl_eau', 'g_cl_lac']; // assets/generated/ (chaussée mouillée de Steel, Sous-Ville, China Lake)
export async function chargerCatalogue(get = async p => { const r = await fetch(p); if (!r.ok) throw Error('Manifeste introuvable : ' + p); return r.json(); }) {
  const sprites = await get('./assets/reused/manifest.json');
  const iman = await get('./assets/interiors/manifest.json'); Object.assign(sprites, iman); // v6 : mobilier et textures d'intérieur
  const ppMan = {}; for (const q of QUARTIERS_STEEL) Object.assign(ppMan, await get(`./assets/steel/${q}/manifest.json`)); // manifestes d'Ocre (chemins relatifs à assets/)
  for (const [k, v] of Object.entries(ppMan)) if (!v.obsolete && (k.startsWith('gen_') || k.startsWith('portrait-'))) sprites[k] = v; // PNJ et portraits -> sprites
  const bman = await get('./assets/buildings/manifest.json');
  for (const [k, v] of Object.entries(ppMan)) if (!v.obsolete && /^(pp|fs|ar2?|df|ml)_/.test(k)) bman[k] = v; // décors des quartiers -> bâtiments (ar2_ : enceinte basse de l'Arena ; obsolete exclus)
  const sols = { ...Object.fromEntries(SOLS_BASE.map(n => [n, `./assets/mockup/${n}.webp`])), ...Object.fromEntries(SOLS_GENERES.map(n => [n, `./assets/generated/${n}.webp`])),
    ...Object.fromEntries(Object.keys(ppMan).filter(k => k.startsWith('g_')).map(n => [n, './assets/' + ppMan[n].file])) };
  return { sprites, iman, ppMan, bman, sols };
}
