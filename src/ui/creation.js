// v11 lot 2 : création de personnage, 2 écrans (maquettes creation-1 / creation-2). UI A ambre, panneaux semi-transparents.
import { ATTRS, POINTS, ATTR_MIN, ATTR_MAX, SKILLS, FAV_COUNT, RACES, ORIGINS, ORIGIN_ITEMS, TRAITS, MAX_TRAITS, PROFILES, DEFAULT_DRAFT,
  originOf, finalAttrs, skillsOf, derived, spent, valid } from '../data/character.js';

const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const clone = d => JSON.parse(JSON.stringify(d));
export const portraitUrl = id => `./assets/portraits/${id}.webp`;

export function createCreation({ $, onDone, onCancel }) {
  const C = $('creation');
  let d = clone(DEFAULT_DRAFT), screen = 1;
  const RN = Object.keys(RACES);
  function setOrigin(id) {
    const old = originOf(d); d.origin = id; const o = originOf(d);
    if (!d.favs.includes(o.fav)) { const i = d.favs.indexOf(old.fav); if (i >= 0) d.favs[i] = o.fav; else d.favs = [o.fav, ...d.favs].slice(0, FAV_COUNT); }
    d.favs = [...new Set(d.favs)];
  }
  function setRace(r) { if (r === d.race) return; d.race = r; d.portrait = 0; setOrigin(ORIGINS[r][0].id); }
  function applyProfile(k) {
    const p = PROFILES[k]; d.profile = k; ATTRS.forEach(([a], i) => d.stats[a] = p.stats[i]);
    const o = originOf(d); d.favs = [o.fav, ...p.tags.filter(t => t !== o.fav)].slice(0, FAV_COUNT);
  }
  const bar = v => `<span class="cr-bar">${Array.from({ length: 10 }, (_, i) => `<i class="${i < v ? 'on' : ''}"></i>`).join('')}</span>`;
  function head(title) {
    const o = originOf(d);
    return `<header class="cr-head rp"><b>${title}</b><span class="muted">${screen === 2 ? esc(d.name || 'Sans nom') + ' · ' + RACES[d.race].name + ' · ' + o.name : ''}</span><button class="btn" id="cr-menu" title="Échap">‹ Menu</button></header>`;
  }
  function render() {
    const r = RACES[d.race], o = originOf(d), por = r.portraits[d.portrait % r.portraits.length];
    C.dataset.screen = screen;
    if (screen === 1) {
      C.innerHTML = head('CRÉATION · 1/2 · IDENTITÉ') + `<div class="cr-cols">
        <section class="rp cr-col cr-id"><div class="lbl">Aperçu</div><img id="cr-portrait" src="${portraitUrl(por)}" alt="Portrait">
          <div class="cr-face"><button class="btn" id="cr-prev" aria-label="Visage précédent">‹</button><span>Visage ${d.portrait % r.portraits.length + 1}/${r.portraits.length}</span><button class="btn" id="cr-next-face" aria-label="Visage suivant">›</button></div>
          <label class="lbl" for="cr-name">Nom</label><input id="cr-name" maxlength="16" autocomplete="off" spellcheck="false" value="${esc(d.name)}"></section>
        <section class="rp cr-col"><div class="lbl">Race</div><div class="cr-races">${RN.map(k => `<button class="btn card ${k === d.race ? 'sel' : ''}" data-race="${k}"><b>${RACES[k].name}</b><small>${RACES[k].short}</small></button>`).join('')}</div>
          <div class="lbl">Effets · ${r.name}</div><ul class="cr-list">${r.effects.map(e => `<li>${e}</li>`).join('')}</ul></section>
        <section class="rp cr-col"><div class="lbl">Origine · ${r.name}</div>${ORIGINS[d.race].map(x => `<button class="btn card ${x.id === o.id ? 'sel' : ''}" data-origin="${x.id}"><b>${x.name}</b><small>${x.desc}</small></button>`).join('')}
          <div class="lbl">Apporte</div><ul class="cr-list"><li>${ATTRS.find(a => a[0] === o.attr)[1]} +1 · ${SKILLS.find(s => s[0] === o.fav)[1]} favorite</li><li>${ORIGIN_ITEMS[o.item].name} · ${o.money} $</li></ul></section></div>
        <footer class="cr-foot rp"><button class="btn" id="cr-profile">Profil prêt</button><span class="muted">Race et origine ne changent plus en cours de partie.</span><button class="btn go" id="cr-next">Suivant ›</button></footer>`;
    } else {
      const left = POINTS - spent(d), fa = finalAttrs(d), sk = skillsOf(d), dv = derived(d), ok = valid(d);
      C.innerHTML = head('CRÉATION · 2/2 · ATTRIBUTS ET COMPÉTENCES') + `<div class="cr-cols">
        <section class="rp cr-col"><div class="cr-row"><span class="lbl">Attributs</span><span>Points restants <b id="cr-left" class="${left ? 'warn' : ''}">${left}</b> / ${POINTS}</span></div>
          <div class="cr-profiles">${Object.entries(PROFILES).map(([k, p]) => `<button class="btn ${d.profile === k ? 'sel' : ''}" data-profile="${k}" title="${esc(p.desc)}">${p.name}</button>`).join('')}</div>
          ${ATTRS.map(([k, n, def]) => `<div class="cr-attr" data-attr-row="${k}"><span class="n">${n}</span><button class="btn pm" data-attr="${k}" data-d="-1" ${d.stats[k] <= ATTR_MIN ? 'disabled' : ''} aria-label="Réduire ${n}">−</button>
            <span class="v">${bar(d.stats[k])}<b>${d.stats[k]}</b>${fa[k] !== d.stats[k] ? `<small class="muted">→ ${fa[k]}</small>` : ''}</span><button class="btn pm" data-attr="${k}" data-d="1" ${d.stats[k] >= ATTR_MAX || left <= 0 ? 'disabled' : ''} aria-label="Augmenter ${n}">+</button><small class="def">${def}</small></div>`).join('')}
          <div class="lbl">Traits · 0 à ${MAX_TRAITS}</div><div class="cr-traits">${Object.entries(TRAITS).map(([k, t]) => `<button class="btn ${d.traits.includes(k) ? 'sel' : ''}" data-trait="${k}">${t.name}</button>`).join('')}</div>
          <p class="muted cr-tdesc">${d.traits.length ? d.traits.map(t => TRAITS[t].desc).join(' ') : 'Aucun trait. Chacun a sa contrepartie.'}</p></section>
        <section class="rp cr-col"><div class="cr-row"><span class="lbl">Compétences</span><span>Favorites <b class="${d.favs.length !== FAV_COUNT ? 'warn' : ''}">${d.favs.length}/${FAV_COUNT}</b></span></div>
          ${SKILLS.map(([k, n]) => `<button class="cr-skill ${d.favs.includes(k) ? 'fav' : ''} ${k === o.fav ? 'lock' : ''}" data-skill="${k}" aria-pressed="${d.favs.includes(k)}"><span class="star">${d.favs.includes(k) ? '★' : ''}</span><span class="n">${n}</span><span class="sb"><i style="width:${sk[k]}%"></i></span><b>${sk[k]}</b></button>`).join('')}
          <p class="muted">★ favorite : +15 au départ, progresse plus vite. ${SKILLS.find(s => s[0] === o.fav)[1]} est imposée par ton origine.</p></section>
        <section class="rp cr-col cr-sheet"><div class="lbl">Fiche</div><img src="${portraitUrl(por)}" alt="">
          <p>PV <b id="cr-hp">${dv.hp}/${dv.maxHp}</b><br>PA <b>${dv.ap}</b> · Initiative ${dv.initiative}<br>Implant : ${dv.implant ? 'IO, sous la peau' : 'aucun'}<br>Dollars : <b id="cr-money">${dv.money} $</b><br>${ORIGIN_ITEMS[o.item].name}</p>
          <div class="lbl">À Dusk-Town</div><p class="muted">${o.note}</p></section></div>
        <footer class="cr-foot rp"><button class="btn" id="cr-back">‹ Identité</button><span class="muted" id="cr-hint">${ok ? 'Tu pourras monter tes compétences en jouant.' : left > 0 ? `Encore ${left} point${left > 1 ? 's' : ''} à répartir.` : left < 0 ? 'Trop de points dépensés.' : d.favs.length !== FAV_COUNT ? `Choisis ${FAV_COUNT} favorites.` : 'Il te faut un nom.'}</span><button class="btn go" id="cr-enter" ${ok ? '' : 'disabled'}>Entrer dans Dusk-Town ›</button></footer>`;
    }
  }
  C.addEventListener('input', e => { if (e.target.id === 'cr-name') d.name = e.target.value.slice(0, 16); });
  C.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b || b.disabled) return;
    if (b.dataset.race) setRace(b.dataset.race);
    else if (b.dataset.origin) setOrigin(b.dataset.origin);
    else if (b.id === 'cr-prev' || b.id === 'cr-next-face') { const n = RACES[d.race].portraits.length; d.portrait = (d.portrait + (b.id === 'cr-prev' ? n - 1 : 1)) % n; }
    else if (b.id === 'cr-next') { screen = 2; }
    else if (b.id === 'cr-profile') { if (!d.profile) applyProfile('vagabond'); screen = 2; }
    else if (b.id === 'cr-back') screen = 1;
    else if (b.dataset.profile) applyProfile(b.dataset.profile);
    else if (b.dataset.attr) { const k = b.dataset.attr; d.stats[k] = Math.max(ATTR_MIN, Math.min(ATTR_MAX, d.stats[k] + +b.dataset.d)); d.profile = null; }
    else if (b.dataset.trait) { const t = b.dataset.trait, i = d.traits.indexOf(t); if (i >= 0) d.traits.splice(i, 1); else if (d.traits.length < MAX_TRAITS) d.traits.push(t); }
    else if (b.dataset.skill) { const k = b.dataset.skill, i = d.favs.indexOf(k); if (k === originOf(d).fav) return; if (i >= 0) d.favs.splice(i, 1); else if (d.favs.length < FAV_COUNT) d.favs.push(k); }
    else if (b.id === 'cr-menu') { close(); onCancel(); return; }
    else if (b.id === 'cr-enter') { if (valid(d)) { close(); onDone(clone(d)); } return; }
    else return;
    const f = document.activeElement?.id; render(); if (f === 'cr-name') $('cr-name').focus();
  });
  C.addEventListener('keydown', e => { if (e.key === 'Enter' && e.target.id === 'cr-name') { screen = 2; render(); } });
  function open() { d = clone(DEFAULT_DRAFT); screen = 1; C.hidden = false; render(); }
  function close() { C.hidden = true; }
  function back() { if (screen === 2) { screen = 1; render(); } else { close(); onCancel(); } }
  return { open, close, back, isOpen: () => !C.hidden, get draft() { return d; } };
}
