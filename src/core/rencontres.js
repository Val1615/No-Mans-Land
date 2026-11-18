// Rencontres aléatoires des No Man's Land, jalon 1 (docs/rencontres/ARCHI.md, PILOTE.md) : gestionnaire, sans dépendance au rendu.
// - branche voyage.crochets.onCaseEntree : tirage du terrain (data/nml.js, taux inchangés) contre la table des rencontres ;
// - journal par case (region.rencontres['col,row'] = { id, regle, flags }) : une case déjà rencontrée ne se retire pas ; non réglée, la scène
//   se rouvre telle qu'on l'a laissée (butin pris, morts, bande encore là) ; réglée, la case est libre ;
// - scène = lieu ajouté à chaud (game.ajouterLieu), statut de voyage 'rencontre' ; sortie par les portes de bord ou par la fuite -> carte,
//   en halte (demi-tour, fuite) ou trajet repris là où il s'était arrêté (est) ; sauvegarde dans la scène : recréée au chargement.
import { RENCONTRES } from '../data/rencontres.js';
import { ambiance } from '../data/ambiances.js';
import { ENCOUNTERS } from '../data/combat.js';
import { EVENEMENTS_ROUTE } from '../data/nml.js';
import { onCaseEntree } from './voyage.js';

const K = c => c[0] + ',' + c[1];
const dans = (z, x, y) => x >= z.x && x <= z.x + z.w && y >= z.z && y <= z.z + z.d;

// gabarits gris : PNJ ou unité dont le sprite d'Ocre n'est pas encore livré -> silhouette grise d'un PNJ existant (gabarit: true, sans portrait)
const GABARIT_PNJ = 'gen_rc_tuerto';
export function createRencontres({ game, voyage, say = () => {}, msg = () => '', rng = () => Math.random(), sprites = null }) {
  const livre = k => !sprites || !!sprites[k];
  const gabarit = o => livre(o.sprite) ? o : { ...o, sprite: GABARIT_PNJ, gabarit: true, portrait: false, portraitDe: undefined };
  let arrTexte = null; // texte d'arrivée : effacé au premier pas (en 390 l'encart ne reste pas sur les sorties) [Régie 18/11]
  const S = game.state;
  for (const [id, D] of Object.entries(RENCONTRES)) { ENCOUNTERS[id] = { ...D.combat, prefixe: D.prefixe, ennemis: D.combat.ennemis.map(gabarit) }; Object.assign(game.world.DIALOGUES, D.dialogues); }
  // table : événements de route + rencontres (terrains, biomes, si(etat) : caravane unique) ; taux des terrains inchangés (onCaseEntree)
  const TABLE = [...EVENEMENTS_ROUTE, ...Object.entries(RENCONTRES).map(([id, D]) => ({ id, rencontre: id, terrains: D.terrains, biomes: D.biomes, si: D.si, poids: D.poids || 1 }))];
  const evenement = id => TABLE.find(e => e.rencontre === id);
  let forcee = null, quitterApres = null, dedans = {};

  // --- tirage à chaque case entrée ---
  voyage.crochets.onCaseEntree = (c, etat) => {
    const R = etat.region, j = R?.rencontres?.[K([c.col, c.row])];
    if (forcee) { const id = forcee; forcee = null; return evenement(id); } // DEV : rencontre forcée sur la prochaine case
    if (R?.escorte > 0) { R.escorte--; return null; } // escorte de la caravane : cases sans tirage (extension « escorte », CARAVANE §12.7)
    if (!api.actives) return null; // tests du voyage seul (carte_nml.py) : aucune rencontre
    if (j) return j.regle ? null : evenement(j.id); // case déjà rencontrée : jamais de nouveau tirage
    if (c.lieu) return null; // pas d'embuscade sur la case d'une ville
    return onCaseEntree(c, etat, { rng, table: TABLE.filter(e => !e.biomes || !c.biome || e.biomes.includes(c.biome)) });
  };

  // --- construction de la scène (lieu, portes de bord, PNJ, points) ---
  function construire(id, heures = S.heures) {
    const D = RENCONTRES[id], sc = D.scene, L = D.lieu, A = ambiance(sc.ambiance, heures);
    const loc = JSON.parse(JSON.stringify({ id: L, name: 'No Man\u2019s Land · ' + D.nom, kind: 'exterior', size: sc.size, city: sc.city, ground: sc.ground, light: A ? { bg: A.bg, hemi: A.hemi, sun: A.sun, tint: A.tint, actor: A.actor, lune: A.lune } : sc.light, niveaux: sc.niveaux,
      buildings: sc.buildings, props: sc.props || [], spawn: { player: { x: sc.entree.x, z: sc.entree.z }, companion: { x: sc.entree.x, z: sc.entree.z + 1 } }, accessLabels: true, cadre: sc.cadre, enseignes: sc.enseignes || [] }));
    for (const b of loc.buildings) if (new RegExp(sc.nuitDecor || '^rc_ds_(talus|berge|rochers|sente)').test(b.sprite)) b.nuit = true; // décors de terrain : suivent la nuit (view.nuitTerrain)
    if (A && sc.feu) { const i = +(sc.feu.i * A.lune).toFixed(3); if (i > 0.02) (loc.glows ||= []).push({ x: sc.feu.x, z: sc.feu.z, rx: sc.feu.r, rz: sc.feu.r, color: sc.feu.couleur, i, pulse: sc.feu.pulse, building: sc.feu.building }); } // flaque du feu : courbe nocturne, nulle le jour
    loc.rencontre = id; if (A && loc.ground?.marge) loc.ground.marge.voile = A.voile; // la marge hors scène suit aussi l'heure
    const doors = sc.sorties.map(s => ({ id: `${L}_${s.id}`, location: L, junction: true, quitter: s.id, effet: s.effet, label: s.label,
      opening: { x: s.x > sc.size.w / 2 ? sc.size.w : 0, z: s.z, side: 'edge' }, threshold: { x: s.x, z: s.z },
      conditions: s.si ? [{ test: () => game.cond(s.si), reason: 'rencontre_bloquee', text: s.refus }] : [] }));
    const npcs = D.pnj.map(n => ({ location: L, ...gabarit(n), ...(livre(n.sprite) ? {} : { editorScale: n.gabaritH ? n.gabaritH / 1.8 : 1 }) }));
    // points : alt [{ si, text, enter }] = variante selon l'état (premier qui tient), lue au moment de l'action
    const spots = D.points.map(p => { const sp = { location: L, kind: 'actions', r: 0.9, anneau: true, ...p, if: p.si ? () => game.cond(p.si) : null };
      if (p.alt) { const va = () => p.alt.find(a => game.cond(a.si)); delete sp.text; delete sp.enter;
        Object.defineProperty(sp, 'text', { get: () => va()?.text ?? p.text, enumerable: true }); Object.defineProperty(sp, 'enter', { get: () => va() ? va().enter : p.enter, enumerable: true }); }
      return sp; });
    game.ajouterLieu(L, loc, { doors, npcs, spots });
    dedans = {};
  }
  const prefixe = id => RENCONTRES[id].prefixe;
  const purge = id => { for (const f of Object.keys(S.flags)) if (f.startsWith(prefixe(id)) || f.startsWith(`combat_${id}_`)) delete S.flags[f]; };

  // --- entrée : depuis la carte (événement de case) ou forcée (DEV) ---
  function entrer(id, cas) {
    const D = RENCONTRES[id]; if (!D) return { ok: false, reason: 'inconnue' };
    const R = voyage.region(); if (R.statut === 'rencontre') return { ok: false, reason: 'deja' };
    cas = cas || R.case; R.rencontres = R.rencontres || {};
    const j = R.rencontres[K(cas)] = R.rencontres[K(cas)] || { id, regle: false, flags: {} };
    purge(id); Object.assign(S.flags, j.flags); // la scène telle qu'on l'a laissée
    const p = S.player;
    R.rencontre = { id, case: [...cas], retour: { location: S.location, x: p.x, z: p.z } };
    construire(id);
    R.statut = 'rencontre'; // avant le warp : l'autosave de la transition voit la scène
    game.agir(`warp:${D.lieu}:${D.scene.entree.x}:${D.scene.entree.z}`); p.heading = D.scene.entree.heading ?? p.heading;
    dedans = {}; for (const t of D.declencheurs) dedans[t.id] = dans(t.zone, p.x, p.z);
    setTimeout(() => { arrTexte = j.flags[prefixe(id) + 'vu'] ? (D.arriveeRetour || 'La piste. Le pick-up est toujours là.') : D.arrivee; say(arrTexte); }, 60);
    S.flags[prefixe(id) + 'vu'] = true; if (D.drapeauArrivee) S.flags[D.drapeauArrivee] = true; // drapeau de monde (caravane unique) : jamais purgé
    return { ok: true };
  }
  // --- sortie : porte de bord (effet halte | reprise) ou fuite du combat ---
  function quitter(effet = 'halte') {
    const R = voyage.region(), RC = R.rencontre; if (!RC) return { ok: false };
    const D = RENCONTRES[RC.id], pre = prefixe(RC.id), j = R.rencontres[K(RC.case)];
    j.flags = Object.fromEntries(Object.entries(S.flags).filter(([f]) => f.startsWith(pre)));
    j.regle = !!S.flags[pre + 'regle'];
    if (S.dialogue) game.closeDialogue();
    // durée de la scène (heures) : duree + dureeSi { drapeau: h } (caravane : +1 h si la citerne a été réparée) ; escorte : +1 h, 12 $, 3 cases sans tirage
    S.heures = (S.heures ?? 0) + (D.duree || 0) + Object.entries(D.dureeSi || {}).reduce((a, [f, h]) => a + (S.flags[f] ? h : 0), 0);
    const escorte = effet === 'escorte'; if (escorte) { S.heures += 1; R.escorte = 3; game.agir('gain:12'); }
    purge(RC.id); delete R.rencontre; R.statut = 'halte';
    game.agir(`warp:${RC.retour.location}:${RC.retour.x}:${RC.retour.z}`);
    game.retirerLieu(D.lieu);
    const repris = (effet === 'reprise' || escorte) && R.trajet.length ? voyage.reprendre().ok : false;
    say(escorte ? 'La caravane repart. Tu voyages sur le toit du tracteur : douze dollars à l\u2019arrivée, et personne ne t\u2019arrête.' : repris ? 'Tu reprends la piste.' : effet === 'fuite' ? 'Tu as semé la bande. La carte, de nouveau.' : 'Tu rebrousses chemin jusqu\u2019à la carte.');
    return { ok: true, repris, regle: j.regle, escorte };
  }
  game.onQuitter(d => quitter(d.effet));
  game.onRencontre((x, y) => { if (x === 'quitter') quitterApres = y || 'fuite'; }); // issue de combat (fuite) ou dialogue (rencontre:quitter:escorte) : la scène est quittée à l'image suivante (tick)
  // sauvegarde prise dans la scène : le lieu n'existe qu'à chaud, on le recrée avant la restauration
  game.onLieuManquant(snap => { const RC = snap.region?.rencontre; if (RC && RENCONTRES[RC.id]?.lieu === snap.location) construire(RC.id, snap.heures); });

  // --- effets de dialogue et de combat propres à la scène ---
  game.on(ev => {
    const RC = S.region?.rencontre; if (!RC) return; const pre = prefixe(RC.id);
    const D = RENCONTRES[RC.id];
    if (ev.type === 'dialogue_open') for (const r of D.surDialogue || []) if (new RegExp(r.npc).test(ev.npc)) for (const f of r.flags) S.flags[pre + f] = true;
    if (ev.type === 'combat_start') for (const f of D.combat?.drapeauxDebut || ['combat']) S.flags[pre + f] = true;
    // textes.entrees { id: ligne } : récit d'entrée des unités engagées, ajouté au texte de début (say du début passe après ce crochet : micro-tâche)
    if (ev.type === 'combat_start') { const en = RENCONTRES[RC.id]?.combat?.textes?.entrees || {}, l = (S.combat?.units || []).filter(u => !u.joueur && en[u.id]).map(u => en[u.id]);
      if (l.length) { const t = [ev.text, ...l].filter(Boolean).join(' '); queueMicrotask(() => say(t)); } }
  });

  // --- chaque image, dans la scène : déclencheurs au sol, fuite différée, ménage ---
  function tick() {
    const R = S.region;
    if (!R?.rencontre) { for (const [id, D] of Object.entries(RENCONTRES)) if (game.world.LOCATIONS[D.lieu] && S.location !== D.lieu) game.retirerLieu(D.lieu); return; } // scène orpheline (partie chargée ailleurs)
    if (arrTexte && S.player.path.length) { if (msg() === arrTexte) say(''); arrTexte = null; }
    if (quitterApres && !S.combat) { const e = quitterApres; quitterApres = null; quitter(e); return; }
    if (S.dialogue || S.combat || S.combatPending) return;
    const D = RENCONTRES[R.rencontre.id], p = S.player;
    for (const t of D.declencheurs) {
      const inn = dans(t.zone, p.x, p.z); if (!(t.id in dedans)) { dedans[t.id] = inn; continue; } // partie chargée : rien ne se déclenche sous les pieds
      const avant = dedans[t.id]; dedans[t.id] = inn;
      if (!inn || avant || (t.si && !game.cond(t.si))) continue;
      declencher(t); if (S.dialogue || S.combat) return;
    }
  }
  function declencher(t) {
    const p = S.player; game.agir(t.enter);
    if (t.test) { p.path = []; p.pending = null; const spec = t.testSi6 && game.cond(t.testSi6) ? t.test.replace(/:\d+$/, ':6') : t.test, r = game.tester(spec);
      if (t.texte) say(t.texte + ' ' + (r.ok ? '' : t.echec || '')); game.agir(r.ok ? t.pass : t.fail); game.closeDialogue(); return; }
    if (t.combat && t.siDeja && game.cond(t.siDeja)) { p.path = []; p.pending = null; game.agir('combat:' + t.combat); game.closeDialogue(); return; }
    if (t.dialogue) { p.path = []; p.pending = null; if (t.texte) say(t.texte); const [npc, node] = t.dialogue.split(':'); game.ouvrirDialogue(npc, node || 'start'); }
  }

  // --- DEV : forcer la prochaine case, ou entrer tout de suite depuis une ville (sortie régionale, un pas de trajet) ---
  function forcer(id) { if (!RENCONTRES[id]) return false; forcee = id; return true; }
  function entrerMaintenant(id = 'embuscade_piste') {
    if (!RENCONTRES[id]) return { ok: false, reason: 'inconnue' };
    const R = voyage.region();
    if (R.statut === 'rencontre') return { ok: false, reason: 'deja' };
    if (R.statut === 'lieu') { let d = game.world.DOORS.find(x => x.regional && x.location === S.location);
      if (!d) { d = game.doorById('j_q2_est'); game.agir(`warp:${d.location}:${d.threshold.x}:${d.threshold.z}`); }
      if (S.dialogue) game.closeDialogue(); voyage.sortie(d); voyage.partir({ lieu: d.vers || 'steel' }); }
    else if (R.statut === 'depart' || R.statut === 'halte') { if (!voyage.partir().ok) return { ok: false, reason: 'trajet_vide' }; }
    forcer(id); const ev = voyage.pas(); return { ok: !!ev?.rencontre, case: R.case };
  }
  const api = { entrer, quitter, tick, forcer, entrerMaintenant, construire, RENCONTRES, actives: true, setRng: f => { rng = f || (() => Math.random()); },
    get active() { return S.region?.rencontre || null; }, journal: () => S.region?.rencontres || {} };
  return api;
}
