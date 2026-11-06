import * as THREE from 'three';
import { UNITS } from '../data/units.js';
import { wallsOf } from '../core/grid.js';
import { groundTexture, margeTexture, SKIN } from './textures.js?v=editor2';

export const ZOOM_MIN = 0.6, ZOOM_MAX = 1.5;
export function createView(canvas, game, sprites, bman, labelLayer, ostCentre = null) {
  let { LOCATIONS, DOORS, NPCS, COMPANION } = game.world;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene(); scene.background = new THREE.Color('#2a2420');
  const hemi = new THREE.HemisphereLight('#ffe9cf', '#4a3a2a', 1.5); scene.add(hemi);
  const sun = new THREE.DirectionalLight('#ffd2a0', 1.6); sun.position.set(-12, 18, 20); scene.add(sun);
  // v13 : éclairage par lieu (nuit de Steel). Par défaut : celui de Dusk-Town, inchangé.
  const LIGHT0 = { bg: '#2a2420', hemi: ['#ffe9cf', '#4a3a2a', 1.5], sun: ['#ffd2a0', 1.6], tint: null, actor: null };
  function applyLight(l) { l = { ...LIGHT0, ...(l || {}) }; scene.background = new THREE.Color(l.bg); hemi.color.set(l.hemi[0]); hemi.groundColor.set(l.hemi[1]); hemi.intensity = l.hemi[2];
    sun.color.set(l.sun[0]); sun.intensity = l.sun[1]; for (const a of [player, companion]) a.material.color.set(l.actor || '#ffffff'); return l; }
  const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 500);
  const yaw = THREE.MathUtils.degToRad(UNITS.camera.yawDeg), pitch = THREE.MathUtils.degToRad(UNITS.camera.pitchDeg);
  const camDir = new THREE.Vector3(-Math.sin(yaw) * Math.cos(pitch), -Math.sin(pitch), -Math.cos(yaw) * Math.cos(pitch)).normalize();
  const loader = new THREE.TextureLoader(), texCache = {};
  const spriteTex = id => texCache[id] ||= Object.assign(loader.load('./assets/' + (sprites[id].file || `reused/${id}.webp`)), { colorSpace: THREE.SRGBColorSpace });
  const skinTex = key => texCache['skin:' + key] ||= Object.assign(new THREE.Texture(SKIN[key]), { needsUpdate: true, colorSpace: THREE.SRGBColorSpace });
  const layerCache = {};
  function layerTex(key, m) {
    if (layerCache[key]) return layerCache[key];
    const img = SKIN[key];
    if (!img || !img.width || !img.height || img.width * img.height < 65000) {
      return layerCache[key] = { tex: skinTex(key), x0: 0, y0: 0, cw: m.px[0], ch: m.px[1] };
    }
    const mk = maskOf(key);
    if (!mk) return layerCache[key] = { tex: skinTex(key), x0: 0, y0: 0, cw: m.px[0], ch: m.px[1] };
    const w = mk.w, h = mk.h, d = mk.data;
    let x0 = w, y0 = h, x1 = -1, y1 = -1;
    for (let y = 0; y < h; y++) {
      const row = y * w * 4;
      for (let x = 0; x < w; x++) if (d[row + x * 4 + 3] > 4) {
        if (x < x0) x0 = x; if (x > x1) x1 = x;
        if (y < y0) y0 = y; if (y > y1) y1 = y;
      }
    }
    if (x1 < x0) return layerCache[key] = { tex: skinTex(key), x0: 0, y0: 0, cw: w, ch: h };
    const cw = x1 - x0 + 1, ch = y1 - y0 + 1;
    if (cw * ch > w * h * 0.65) return layerCache[key] = { tex: skinTex(key), x0: 0, y0: 0, cw: w, ch: h };
    const c = document.createElement('canvas'); c.width = cw; c.height = ch;
    c.getContext('2d').drawImage(img, x0, y0, cw, ch, 0, 0, cw, ch);
    const tex = Object.assign(new THREE.CanvasTexture(c), { colorSpace: THREE.SRGBColorSpace });
    texCache['layer:' + key] = tex;
    return layerCache[key] = { tex, x0, y0, cw, ch };
  }
  // Personnages : texture propre à chaque sprite, car le miroir se fait par les UV (repeat.x = -1).
  // THREE.Sprite ignore le signe de scale.x (le shader prend la longueur de la colonne de la matrice) : c'était la cause du miroir invisible.
  const actorBase = {};
  const actorTex = id => {
    let b = actorBase[id];
    if (!b) {
      const wait = [];
      const tex = loader.load('./assets/' + (sprites[id].file || `reused/${id}.webp`), () => { for (const c of wait) { c.source = tex.source; c.needsUpdate = true; } wait.length = 0; });
      tex.colorSpace = THREE.SRGBColorSpace; tex.wrapS = THREE.RepeatWrapping;
      b = actorBase[id] = { tex, wait };
    }
    const c = b.tex.clone(); c.colorSpace = THREE.SRGBColorSpace; c.wrapS = THREE.RepeatWrapping;
    if (b.tex.image) { c.source = b.tex.source; c.needsUpdate = true; } else b.wait.push(c);
    return c;
  };
  // pivot (manifeste) : hauteur des pieds en fraction de l'image, quand la pose n'a pas les deux pieds au bas du cadre
  function spriteMesh(id, heightOverride, actor = false) {
    const m = sprites[id], h = (heightOverride || m.height_m) * Math.cos(pitch), w = h * m.px[0] / m.px[1]; // hauteur vue par la caméra
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: actor ? actorTex(id) : spriteTex(id), alphaTest: 0.5, transparent: false }));
    s.center.set(0.5, m.pivot ?? 0.02); s.scale.set(w, h, 1); Object.assign(s.userData, { base: sprites[id].faces || 1, facing: 1, shown: 1, w, h, turn: 1, phase: Math.random() * 6.28 }); return s;
  }
  let world = new THREE.Group(); scene.add(world);
  let solids = [], pickables = [], labels = [], npcSprites = [], bsprites = [], fsprites = [], bills = [], builtFor = null, exterior = false;
  const animStats = { on: 0, total: 0 }; let uniques = [], horloge = 0; let decor = [], walkers = [], drones = [], flick = [], anims = [], movers = [], ecrans = [], neons = [], fenetres = [], pulses = [], beams = [], light = null; // v13 : figurants (file, soldats, passants), drones, néons/hologrammes
  const player = spriteMesh('player', null, true), companion = spriteMesh(COMPANION.sprite, null, true);
  player.userData.actor = 'player'; scene.add(player, companion);

  function mat(map, color) { return new THREE.MeshStandardMaterial({ map, color: map ? '#ffffff' : color, transparent: true, opacity: 1, roughness: 0.95 }); }
  function addLabel(text, cls, getPos, visible) { const el = document.createElement('div'); el.className = 'wlabel ' + cls; el.textContent = text; labelLayer.appendChild(el); labels.push({ el, getPos, visible }); }
  // Bâtiment = sprite entier de la maquette. Ancre (coin de base avant, en px) posée sur le coin monde (x+w, z+d).
  // Une seule échelle : K px d'image par mètre à l'écran. Collision = emprise déclarée (grid.js), jamais l'image.
  const K = UNITS.camera.artPxPerMeter;
  const masks = {};
  function maskOf(name) {
    if (masks[name]) return masks[name]; const img = SKIN[name] || sprites[name]?._img; if (!img) return null;
    const c = document.createElement('canvas'); c.width = img.width; c.height = img.height; const x = c.getContext('2d'); x.drawImage(img, 0, 0);
    return masks[name] = { w: img.width, h: img.height, data: x.getImageData(0, 0, img.width, img.height).data };
  }
  function alphaAt(name, u, v) { const m = maskOf(name); if (!m || u < 0 || u > 1 || v < 0 || v > 1) return 0;
    const px = Math.min(m.w - 1, Math.floor(u * m.w)), py = Math.min(m.h - 1, Math.floor((1 - v) * m.h)); return m.data[(py * m.w + px) * 4 + 3] / 255; }
  function cueTexture(cue) {
    const c = document.createElement('canvas'); c.width = c.height = 64; const x = c.getContext('2d');
    x.fillStyle = 'rgba(30,22,16,.75)'; x.beginPath(); x.arc(32, 32, 26, 0, 7); x.fill(); x.strokeStyle = '#efe3c4'; x.lineWidth = 5; x.beginPath();
    if (cue === 'cross') { x.moveTo(32, 16); x.lineTo(32, 48); x.moveTo(16, 32); x.lineTo(48, 32); }
    if (cue === 'bottle') { x.rect(25, 28, 14, 20); x.moveTo(32, 28); x.lineTo(32, 14); }
    if (cue === 'drop') { x.moveTo(32, 13); x.quadraticCurveTo(48, 36, 32, 48); x.quadraticCurveTo(16, 36, 32, 13); }
    if (cue === 'jar') { x.rect(21, 24, 22, 24); x.moveTo(18, 20); x.lineTo(46, 20); }
    x.stroke(); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
  }
  // PROVISOIRE (Lower-Town v1) : tant que le sprite b.sprite n'existe pas dans le manifeste, le bâtiment est un volume simple
  // (b.ph = { h, color, roof: 'sheds'|'pitched'|'flat', glow, kind }). Dès que le sprite existe, le chemin normal reprend.
  const phOf = [];
  function placeholder(b) {
    const ph = b.ph || {}, h = ph.h || 6, M = c => new THREE.MeshStandardMaterial({ color: c, roughness: 0.95, transparent: true, opacity: 1, depthTest: false, depthWrite: false });
    const add = (w, hh, d, x, y, z, c, geo) => { const m = new THREE.Mesh(geo || new THREE.BoxGeometry(w, hh, d), M(c)); m.position.set(x, y, z); world.add(m); return m; };
    const extra = []; let main;
    if (ph.kind === 'dalle') { // dalle haute de Center-Town : tablier en hauteur, pylônes, feux ambrés en sous-face
      main = add(b.w, 1.6, b.d + 2, b.x + b.w / 2, h, b.z + (b.d + 2) / 2 - 2, '#2a2826');
      for (const s of b.solid || []) extra.push(add(s.w, h, s.d, s.x + s.w / 2, h / 2, s.z + s.d / 2, '#34312d'));
      for (let x = 1.5; x < b.w; x += 3) { const l = add(0.5, 0.15, 0.3, b.x + x, h - 0.9, b.z + b.d - 0.2, '#e8a13a'); extra.push(l); }
      extra.push(add(b.w, 0.5, 0.3, b.x + b.w / 2, h - 1.0, b.z + b.d - 0.6, '#1c1a18'));
    } else if (ph.kind === 'arch') { // portique IO : deux montants, traverse au scanner, voyant ambre, guérite
      const z0 = b.z + 1.6, z1 = b.z + b.d - 0.8;
      main = add(1.8, 2.4, 1.5, b.x + 1, 1.2, b.z + 0.8, '#3a3d40');
      extra.push(add(0.6, h, 0.6, b.x + 1, h / 2, z1 + 0.3, '#45484b'), add(0.6, h, 0.6, b.x + 1, h / 2, z0 + 0.1, '#45484b'),
        add(0.7, 0.6, z1 - z0 + 0.6, b.x + 1, h, (z0 + z1) / 2 + 0.2, '#3a3d40'), add(0.2, 0.25, 0.8, b.x + 1.4, h - 0.2, (z0 + z1) / 2, '#e8a13a'),
        add(0.08, 0.6, 0.9, b.x + 1.92, 1.6, b.z + 0.8, '#c98a3a'));
    } else main = add(b.w, h, b.d, b.x + b.w / 2, h / 2, b.z + b.d / 2, ph.color || '#3a3632');
    main.userData.box = { x0: b.x, x1: b.x + b.w, z0: b.z, z1: b.z + b.d, h: ph.kind === 'dalle' ? h + 1 : h + 2 }; main.userData.buildingId = b.id; main.userData.targetOpacity = 1;
    if (ph.roof === 'sheds') { const n = Math.max(2, Math.round(b.w / 3)), sw = b.w / n; // toit en dents de scie : prismes + vitrage nord
      for (let i = 0; i < n; i++) { const sh = new THREE.Shape(); sh.moveTo(0, 0); sh.lineTo(sw, 0); sh.lineTo(sw, 1.7); sh.lineTo(0, 0);
        const g = new THREE.ExtrudeGeometry(sh, { depth: b.d, bevelEnabled: false }); const t = new THREE.Mesh(g, M(ph.roofColor || '#2b2a28'));
        t.position.set(b.x + sw * i, h, b.z); world.add(t); extra.push(t);
        extra.push(add(0.08, 1.1, b.d * 0.85, b.x + sw * (i + 1) + 0.04, h + 0.75, b.z + b.d / 2, '#7a5226')); } } // vitrage du shed, lueur sodium
    if (ph.roof === 'pitched') extra.push(add(b.w + 0.3, 0.6, b.d + 0.3, b.x + b.w / 2, h + 0.3, b.z + b.d / 2, ph.roofColor || '#4a3a2e'));
    if (ph.chimney) extra.push(add(1.2, h + 6, 1.2, b.x + ph.chimney[0], (h + 6) / 2, b.z + ph.chimney[1], '#5a3a2a'));
    for (const f of ph.floors ? Array.from({ length: ph.floors - 1 }, (_, i) => i + 1) : []) // coursives : dalles en saillie sur la façade sud
      extra.push(add(b.w, 0.18, 0.9, b.x + b.w / 2, f * h / ph.floors, b.z + b.d + 0.45, '#4a4f53'));
    for (const g of ph.lights || []) extra.push(add(g.w || 1.2, g.h || 0.8, 0.08, b.x + g.x, g.y, b.z + b.d + 0.05, g.c || '#e8a13a')); // fenêtres / portes éclairées (face sud)
    for (const g of ph.lightsE || []) extra.push(add(0.08, g.h || 0.8, g.w || 1.2, b.x + b.w + 0.05, g.y, b.z + g.z, g.c || '#e8a13a')); // face est
    for (const e of extra) { const c = e.material.color.getHex(); if ([0xe8a13a, 0xc9541e, 0xc98a3a].includes(c)) e.material.emissive.set(c); }
    bills.push({ obj: main, x0: b.x, x1: b.x + b.w, z0: b.z, z1: b.z + b.d, extra }); phOf.push(main);
    if (b.named) { addLabel(b.label, 'service', () => new THREE.Vector3(b.x + b.w / 2, 3.4, b.z + b.d), () => !!(b.sign || game.state.discovered[b.id])); labels[labels.length - 1].el.dataset.building = b.id; } // b.sign : enseigne lisible de la rue, libellé visible sans y être entré
  }
  function building(b) {
    if (!bman[b.sprite]) return placeholder(b);
    let m = bman[b.sprite]; const mobAnim = m.anime && viewW < 700 && bman[b.sprite + '_mobile'] && SKIN[b.sprite + '_mobile'];
    const skKey = mobAnim ? b.sprite + '_mobile' : b.sprite;
    const t = m.anime ? Object.assign(new THREE.Texture(SKIN[skKey]), { needsUpdate: true, colorSpace: THREE.SRGBColorSpace }) : skinTex(skKey);
    // enseigne animée (planche horizontale, frames x frame_px, fps du manifeste) : une image de la planche, taille monde = image ordinateur ; version _mobile sur petit écran
    if (m.anime) { t.repeat.set(1 / m.frames, 1); m = { ...m, px: m.frame_px }; }
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true, depthTest: false, depthWrite: false, color: b.tint || light?.tint || '#ffffff' }));
    s.center.set(m.anchor[0] / m.px[0], 1 - m.anchor[1] / m.px[1]); s.scale.set(m.px[0] / K * (b.k || 1), m.px[1] / K * (b.k || 1) * (b.sy || 1), 1); // b.k : échelle uniforme corrigée par le code // b.sy : tassement vertical par le code quand le sprite livré est plus haut que l'illustration
    s.position.set(b.x + b.w + (b.ancre?.[0] || 0), b.y || 0, b.z + b.d + (b.ancre?.[1] || 0)); // b.y : hauteur (m) d'une enseigne posée en façade ; b.ancre : décalage (m) de l'ancre du sprite par rapport au coin avant (angle de l'Arena, ancre au raccord ouest)
    Object.assign(s.userData, { buildingId: b.id, visitable: b.visitable, label: b.label, img: b.sprite, targetOpacity: 1 });
    world.add(s); bsprites.push(s); if (b.defile) movers.push({ s, item: null, x0: s.position.x, ...b.defile }); if (m.anime) anims.push({ s, t, n: m.frames, fps: m.fps, ph: b.ph ?? Math.random() * m.frames, g: b.groupe || null, fige: !!b.fige }); // groupe : compte pour une seule animation ; fige : toujours sur l'image 1
    const item = { obj: s, x0: b.x, x1: b.x + b.w, z0: b.z, z1: b.z + b.d, extra: [], cover: !!b.cover, fond: !!b.fond }; bills.push(item); // cover : toit (halle) au-dessus de ce qui est dessous
    if (b.ecran) { const e = ecranSprite(b, m, s); if (e) { world.add(e); item.extra.push(e); if (e.userData.ecran.flash) { world.add(e.userData.ecran.flash); item.extra.push(e.userData.ecran.flash); } } } // écran dessiné par le code (Feed de Pulse Plaza)
    for (const d of DOORS.filter(d => d.buildingId === b.id)) if (b.cue) { // indice discret sur la porte peinte
      const c = new THREE.Sprite(new THREE.SpriteMaterial({ map: cueTexture(b.cue), transparent: true, depthTest: false, depthWrite: false, opacity: 0.9 }));
      c.scale.set(0.42, 0.42, 1); c.position.set(d.opening.x, 2.5, d.opening.z); world.add(c); item.extra.push(c);
    }
    const door = DOORS.find(d => d.buildingId === b.id);
    if (!b.visitable && b.named) { addLabel(b.label, 'service', () => new THREE.Vector3(b.x + b.w / 2, 3.4, b.z + b.d), () => !!(b.sign || game.state.discovered[b.id])); labels[labels.length - 1].el.dataset.building = b.id; } // b.sign : enseigne lisible de la rue, libellé visible sans y être entré // v12 : lieu nommé une fois repéré
    if (b.visitable) { addLabel(b.label, 'service', () => new THREE.Vector3(door.opening.x, 3.4, door.opening.z), () => !!(b.sign || game.state.discovered[b.id])); labels[labels.length - 1].el.dataset.building = b.id; } // b.sign : enseigne lisible de la rue, libellé visible sans y être entré
  }
  // v6 : mur d'intérieur = texture réelle (1 image = 3 m x 3 m de mur), répétée selon la taille de chaque face.
  function wallMats(p, skin) {
    const img = SKIN[skin]; if (!img) return null;
    const face = (u, v) => { const t = new THREE.Texture(img); t.needsUpdate = true; t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(u / 3, v / 3); t.anisotropy = 4;
      return new THREE.MeshStandardMaterial({ map: t, transparent: true, opacity: 1, roughness: 0.95 }); };
    return [face(p.d, p.h), face(p.d, p.h), face(p.w, p.d), face(p.w, p.d), face(p.w, p.h), face(p.w, p.h)]; // +x -x +y -y +z -z
  }
  // v6 : mobilier = sprite contrôlé (angle v4), posé par son emprise. Largeur écran = largeur projetée de l'emprise ;
  // le bas de l'image tombe sur le coin avant (x+w, z+d). Aucune taille ne vient des pixels.
  function furniture(p) {
    const m = sprites[p.furn], [w,d]=m.footprint_m.map(v=>v*(p.editorScale||1));
    const sw = w * Math.abs(screenRight.x) + d * Math.abs(screenRight.z), sh = sw * m.px[1] / m.px[0];
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: spriteTex(p.furn), transparent: true, alphaTest: 0.3, depthTest: false, depthWrite: false }));
    const dyFront = -(w / 2 * camUp.x + d / 2 * camUp.z); // le coin avant est plus bas à l'écran que le centre
    s.center.set(0.5, dyFront / sh); s.scale.set(sw, sh, 1); s.position.set(p.x + w / 2, 0, p.z + d / 2);
    Object.assign(s.userData, { editorId:p.id, furn: p.furn, img: p.furn, targetOpacity: 1 });
    world.add(s); fsprites.push(s); bills.push({ obj: s, x0: p.x, x1: p.x + w, z0: p.z, z1: p.z + d, extra: [] });
  }
  function box(p, color, skin) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(p.w, p.h, p.d), (skin && wallMats(p, skin)) || mat(null, color));
    m.position.set(p.x + p.w / 2, p.h / 2, p.z + p.d / 2); m.userData.targetOpacity = 1; m.userData.solid = true;m.userData.editorId=p.id;m.userData.wall=!!p.isWall;m.userData.propBox=!!p.box;
    world.add(m); solids.push(m); pickables.push(m); return m;
  }
  function build(locId) {
    world.traverse(o => { o.geometry?.dispose(); if(o.material) { for(const m of [].concat(o.material)) { if(m.map && !Object.values(texCache).includes(m.map)) m.map.dispose(); m.dispose(); } } }); scene.remove(world); world = new THREE.Group(); scene.add(world); solids = []; pickables = []; npcSprites = []; bsprites = []; phOf.length = 0; fsprites = []; bills = [];
    labels.forEach(l => l.el.remove()); labels = [];
    const loc = LOCATIONS[locId]; exterior = loc.kind === 'exterior'; light = applyLight(loc.light); decor = []; walkers = []; drones = []; flick = []; anims = []; movers = []; uniques = []; ecrans = []; neons = []; fenetres = []; pulses = []; beams = [];
    for (const a of [player, companion]) { a.material.depthTest = false; a.material.transparent = true; } // v6 : intérieur aussi trié par l'ordre du peintre
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(loc.size.w, loc.size.d), new THREE.MeshStandardMaterial({ map: groundTexture(loc, DOORS), roughness: 1 }));
    ground.rotation.x = -Math.PI / 2; ground.position.set(loc.size.w / 2, 0, loc.size.d / 2); ground.userData.ground = true; groundMesh = ground;
    world.add(ground); pickables.push(ground);
    if (loc.ground.marge) { const m = loc.ground.marge.m || 60; // sol hors zone (non cliquable) : la rue continue au-delà des bords
      const mg = new THREE.Mesh(new THREE.PlaneGeometry(loc.size.w + 2 * m, loc.size.d + 2 * m), new THREE.MeshStandardMaterial({ map: margeTexture(loc), roughness: 1 }));
      mg.rotation.x = -Math.PI / 2; mg.position.set(loc.size.w / 2, -0.02, loc.size.d / 2); mg.renderOrder = -1; world.add(mg); }
    for (const b of loc.buildings) building(b);
    // format d'Ocre : toute façade posée dont le manifeste a un calque <clé>_neon (même taille, même ancre) reçoit son néon additif, fixe par défaut ;
    // loc.enseignes ne fait que régler un bâtiment (effet, couleur, intensité, lettre qui saute). Idem pour les faisceaux : tout bâtiment dont le
    // manifeste donne source_faisceau_px (pylônes, anime_par_code) tire un faisceau depuis ce pixel ; loc.projecteurs règle ou ajoute.
    const ensDe = new Map((loc.enseignes || []).map(e => [e.building, e])), projDe = new Map((loc.projecteurs || []).filter(p => p.building).map(p => [p.building, p]));
    const pulseDe = new Map((loc.pulses || []).map(p => [p.building + ':' + p.calque, p]));
    for (const b of loc.buildings) if (bman[b.sprite + '_fenetres']) fenetre(b);
    for (const b of loc.buildings) for (const calque of ['ecran', 'pulse', 'pulse2', 'pulse_b', 'faisceau']) { const cfg = pulseDe.get(b.id + ':' + calque), ck = cfg?.key || (bman[b.sprite + '_' + calque + '_fix'] ? b.sprite + '_' + calque + '_fix' : b.sprite + '_' + calque); if (bman[ck]) calqueRythme(b, calque, cfg); }
    for (const b of loc.buildings) if (!ensDe.has(b.id) && bman[b.sprite + '_neon']) enseigne({ id: b.id + '_neon', building: b.id }, loc);
    for (const e of loc.enseignes || []) enseigne(e, loc);
    for (const b of loc.buildings) if (!projDe.has(b.id) && bman[b.sprite]?.source_faisceau_px) projecteur({ building: b.id }, loc);
    for (const pr of loc.projecteurs || []) projecteur(pr, loc);
    for (const p of loc.props) {
      if (p.furn) furniture(p);
      else if (p.box) box(p, p.color,loc.wallSkin);
      else { const s = spriteMesh(p.sprite, (sprites[p.sprite].height_m || 1) * (p.editorScale || 1)); s.userData.editorId=p.id; s.position.set(p.x, p.y || 0, p.z); world.add(s);
        if (p.tint || light.tint) s.material.color.set(p.tint || light.tint);
        if (p.glow) { s.material.blending = THREE.AdditiveBlending; s.material.opacity = p.glow; flick.push({ m: s.material, base: p.glow, ph: Math.random() * 6 }); } // hologramme : additif, scintille
        if (p.flip) { s.material.map = actorTex(p.sprite); s.material.map.repeat.x = -1; s.material.map.offset.x = 1; }
        { s.material.depthTest = false; s.material.transparent = true; const [w, d] = p.fp || (p.solid?[p.solid,p.solid]:sprites[p.sprite].footprint_m) || [0.6, 0.6];
          bills.push({ obj: s, x0: p.x - w / 2, x1: p.x + w / 2, z0: p.z - d / 2, z1: p.z + d / 2, extra: [] }); } }
    }
    ground.renderOrder = 0;
    for (const w of wallsOf(loc, DOORS)) { const m = box(w, loc.wall, loc.wallSkin); const front = w.h < UNITS.storey; m.renderOrder = front ? 100000 : 1; m.userData.front = front; }
    for (const d of DOORS.filter(d => d.location === locId)) {
      const o = d.opening, south = o.side === 'south';
      const g = new THREE.Group(); if (exterior) g.visible = false;
      const frame = new THREE.Mesh(new THREE.BoxGeometry(south ? UNITS.door.width + 0.16 : 0.1, UNITS.door.height + 0.08, south ? 0.1 : UNITS.door.width + 0.16), new THREE.MeshStandardMaterial({ color: '#2e2015' }));
      const leaf = new THREE.Mesh(new THREE.PlaneGeometry(UNITS.door.width, UNITS.door.height), loc.kind === 'interior' ? new THREE.MeshStandardMaterial({ color: '#d8b77a', side: THREE.DoubleSide }) : new THREE.MeshStandardMaterial({ color: '#4a3828', side: THREE.DoubleSide }));
      if (!south) leaf.rotation.y = Math.PI / 2;
      leaf.position.set(south ? 0 : 0.07, 0, south ? 0.07 : 0);
      g.add(frame, leaf); g.position.set(o.x, UNITS.door.height / 2, o.z);
      if (loc.kind === 'interior') { frame.visible = false; // v6 : porte de sortie = texture réelle (planches clouées, filet de lumière), comme la porte peinte dehors
        const dimg = SKIN[loc.doorSkin || 'door_in'], dt = dimg && new THREE.Texture(dimg); // v13 : porte IO dans Steel if (dt) { dt.needsUpdate = true; dt.colorSpace = THREE.SRGBColorSpace; leaf.material = new THREE.MeshStandardMaterial({ map: dt, side: THREE.DoubleSide, roughness: 0.9 }); }
        leaf.material.transparent = true; leaf.material.opacity = 1; leaf.renderOrder = 100001; leaf.userData.targetOpacity = 1; solids.push(leaf); }
      frame.userData.doorId = d.id; leaf.userData.doorId = d.id; world.add(g); if (!exterior) pickables.push(frame, leaf);
      const ring = new THREE.Mesh(new THREE.RingGeometry(0.32, 0.4, 28), new THREE.MeshBasicMaterial({ color: '#e0b04a', transparent: true, opacity: 0.7 }));
      ring.rotation.x = -Math.PI / 2; ring.renderOrder = 1; ring.position.set(d.threshold.x, 0.03, d.threshold.z); ring.userData.doorId = d.id; world.add(ring); pickables.push(ring);
      if (d.junction || d.edge) { ring.material.color.set(d.junction ? '#e0b04a' : '#b9a68a'); ring.material.opacity = d.junction ? 0.8 : 0.5; // v7 : bout de rue
        if (loc.accessLabels !== false) addLabel(d.label, d.junction ? 'junction' : 'edge', () => d.labelPos ? new THREE.Vector3(d.labelPos[0], d.labelPos[2] || 0, d.opening.z === 0 && d.threshold.z > 0 ? Math.min(d.labelPos[1], Math.max(-1.6, game.state.player.z - 2.4)) : d.labelPos[1]) : new THREE.Vector3(d.opening.x - (d.threshold.x - d.opening.x) * 1.6, 0, d.opening.z - (d.threshold.z - d.opening.z) * 1.6)); if (loc.accessLabels !== false) labels[labels.length - 1].el.dataset.door = d.id; } // étiquette hors carte (ou débouché de sortie labelPos) : ne cache jamais le joueur au seuil
      if (loc.kind === 'interior') addLabel(d.label || 'Sortie', 'exit', () => new THREE.Vector3(d.opening.x, UNITS.door.height + 0.35, d.opening.z)); // v6 : au-dessus de la porte, plus sur le seuil (cachait le joueur à l'arrivée)
    }
    // v13 : lumières au sol (néons reflétés sur la chaussée mouillée, pinceaux des projecteurs) : disques additifs étirés
    // petite lumière en hauteur (g.y, m) : point additif posé sur sa source (g.building : trié juste après elle, ampoule de comptoir, lampe de truck)
    for (const g of (loc.glows || []).filter(g => g.y != null)) { const p = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex(), color: g.color, transparent: true, opacity: g.i ?? 0.6, blending: THREE.AdditiveBlending, depthWrite: false, depthTest: false }));
      const r = g.r || 0.8; p.scale.set(r * 2, r * 2, 1); p.position.set(g.x, g.y, g.z); p.renderOrder = 3; p.userData.neon = 'lampe'; world.add(p);
      if (g.flicker || g.beat) flick.push({ m: p.material, obj: p, s0: r * 2, base: g.i ?? 0.6, ph: flick.length * 1.13, flicker: !!g.flicker, beat: g.beat || null }); // clignotement lent des ambres ou pulsation rythmique
      const it = g.building && bills.find(i => i.obj.userData.buildingId === g.building); if (it) it.extra.push(p); }
    for (const g of (loc.glows || []).filter(g => g.y == null)) { const m = new THREE.Mesh(new THREE.PlaneGeometry(g.rx * 2, g.rz * 2), new THREE.MeshBasicMaterial({ map: glowTex(), color: g.color, transparent: true, opacity: g.i ?? 0.6, blending: THREE.AdditiveBlending, depthWrite: false, depthTest: false }));
      m.rotation.x = -Math.PI / 2; m.position.set(g.x, 0.02, g.z); m.renderOrder = 2; world.add(m);
      if (g.flicker || g.beat) flick.push({ m: m.material, obj: m, s0: 1, base: g.i ?? 0.6, ph: flick.length * 1.13, flicker: !!g.flicker, beat: g.beat || null }); }
    // v13 : figurants immobiles (file d'attente, soldats) et passants qui marchent : mêmes sprites animés que les PNJ, sans dialogue
    for (const e of loc.extras || []) { const s = spriteMesh(e.sprite, e.h || null, true); s.position.set(e.x, 0, e.z); s.material.depthTest = false; s.material.transparent = true;
      if (light.actor) s.material.color.set(light.actor); s.userData.facing = e.face || 1; s.userData.role = e.role; s.userData.sprite = e.sprite; world.add(s); decor.push(s); }
    for (const w of loc.walkers || []) { const s = spriteMesh(w.sprite, null, true); s.material.depthTest = false; s.material.transparent = true; if (light.actor) s.material.color.set(light.actor);
      s.userData.role = w.role || 'passant'; s.userData.aller = !!w.aller; /* aller : parcours ouvert (file qui avance vers les portiques), repart du début */ s.userData.route = w.path; s.userData.speed = w.speed || 1.1; s.userData.t = w.t0 || 0; world.add(s); decor.push(s); walkers.push(s); }
    for (const d of loc.drones || []) { const s = spriteMesh('st_drone'); s.material.depthTest = false; s.material.transparent = true; s.userData.role = 'drone'; s.userData.orbit = d; world.add(s); drones.push(s); }
    for (const n of NPCS.filter(n => n.location === locId)) {
      const s = spriteMesh(n.sprite, (sprites[n.sprite].height_m||1.8)*(n.editorScale||1), true);s.userData.editorId=n.id; if (light.actor) s.material.color.set(light.actor); s.position.set(n.x, 0, n.z); s.userData.npc = n.id; s.material.depthTest = false; s.material.transparent = true; world.add(s); pickables.push(s); npcSprites.push(s);
      { const gm = s.material.clone(); gm.opacity = 0.62; gm.color.set('#ffd9a0'); gm.alphaTest = 0.2; /* lot 1 : 62 % et teinte ambre clair, lisible sur le toit sombre */ /* alphaTest 0,5 des persos rejetait tout (alpha x 0,45) [Régie A] */ gm.depthTest = false; gm.depthWrite = false; const gh = new THREE.Sprite(gm); // silhouette à travers le toit d'une halle [Régie, 28/10]
        gh.center.copy(s.center); gh.scale.copy(s.scale); gh.position.copy(s.position); gh.visible = false; gh.renderOrder = 900000; gh.userData.ghostOf = n.id; world.add(gh); s.userData.ghost = gh; }
      addLabel(n.name, 'npc', () => new THREE.Vector3(n.x, 2.05, n.z)); labels[labels.length - 1].foot = () => new THREE.Vector3(n.x, 0, n.z); labels[labels.length - 1].npcSprite = s; labels[labels.length - 1].el.dataset.npc = n.id;
    }
    // garde-corps bas (loc.gardeCorps : x, z, w, d, h en m) : pan sombre et liseré néon, dessinés par le code ; triés avec les sprites (ordre du peintre)
    for (const g of loc.gardeCorps || []) { const h = g.h || 1.1, grp = new THREE.Group();
      const pan = new THREE.Mesh(new THREE.BoxGeometry(g.w, h, g.d), new THREE.MeshBasicMaterial({ color: g.color || '#1c1a24', transparent: true, depthTest: false, depthWrite: false }));
      const neon = new THREE.Mesh(new THREE.BoxGeometry(g.w + 0.02, 0.07, g.d + 0.02), new THREE.MeshBasicMaterial({ color: g.neon || '#ffae55', transparent: true, depthTest: false, depthWrite: false }));
      pan.position.set(g.x + g.w / 2, h / 2, g.z + g.d / 2); pan.userData.box = { x0: g.x, x1: g.x + g.w, z0: g.z, z1: g.z + g.d, h }; neon.position.set(g.x + g.w / 2, h - 0.05, g.z + g.d / 2); grp.add(pan, neon); world.add(grp);
      bills.push({ obj: pan, x0: g.x, x1: g.x + g.w, z0: g.z, z1: g.z + g.d, extra: [neon] }); }
    // étiquettes rapprochées (loc.labelsProches : { ids, r }) : visibles seulement à moins de r m du joueur, ou au survol (souris)
    if (loc.labelsProches) { const P = loc.labelsProches, R = P.r || 3;
      for (const l of labels) { const id = l.el.dataset.npc || l.el.dataset.building; if (!P.ids.includes(id)) continue;
        const n = NPCS.find(n => n.id === id), b = loc.buildings.find(b => b.id === id), vis0 = l.visible;
        const dist = () => { const q = game.state.player; if (n) return Math.hypot(q.x - n.x, q.z - n.z);
          return Math.hypot(q.x - Math.max(b.x, Math.min(q.x, b.x + b.w)), q.z - Math.max(b.z, Math.min(q.z, b.z + b.d))); };
        l.proche = true; l.visible = () => (!vis0 || vis0()) && (survol === id || dist() <= R); } }
    builtFor = locId;
  }
  // survol à la souris (étiquettes rapprochées) : PNJ ou bâtiment sous le pointeur, au plus toutes les 150 ms
  let survol = null, survolT = 0;
  canvas.addEventListener?.('pointermove', e => { if (e.pointerType !== 'mouse' || !LOCATIONS[builtFor]?.labelsProches) return; const t = performance.now(); if (t - survolT < 150) return; survolT = t;
    const r = canvas.getBoundingClientRect(); ray.setFromCamera(new THREE.Vector2(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1), cam);
    const nh = ray.intersectObjects(npcSprites, false)[0]; if (nh) { survol = nh.object.userData.npc; return; }
    const c = scr(ray.ray.origin); let top = null; // sprite opaque le plus haut sous le pointeur, quelle que soit son emprise au sol
    for (const s of bsprites) { if (s.material.opacity < 0.5) continue; const q = uvOf(s, c); if (alphaAt(s.userData.img, q.u, q.v) > 0.5 && (!top || s.renderOrder > top.renderOrder)) top = s; }
    survol = top?.userData.buildingId || null; });
  // contrôle (tests) : bâtiments ou garde-corps dessinés devant un personnage (PNJ, figurant, passant) et opaques sur lui
  // bâtiments qui masqueraient un personnage posé en (x, z) (même règle que masques()) : aide à la pose et aux tests
  // pièce basse (height_m < 1,2 m au manifeste : barrières de file) : ne cache pas un personnage, on voit sa tête et son buste au-dessus
  const bas = s => (bman[s.userData.img]?.height_m ?? 99) < 1.2;
  function masqueEn(x, z) { const a = { position: new THREE.Vector3(x, 0, z) }, ai = actorItem(a), out = [];
    for (const s of bsprites) { const bi = bills.find(b => b.obj === s); if (!bi || bi.cover || bas(s) || !inFront(bi, ai)) continue;
      for (const hy of [0.3, 0.9, 1.5]) { const q = uvOf(s, scr(new THREE.Vector3(x, hy, z))); if (alphaAt(s.userData.img, q.u, q.v) > 0.3) { out.push(s.userData.buildingId); break; } } }
    return out; }
  function masques() { const out = [];
    const gens = [...npcSprites.map(s => [s.userData.npc, s]), ...decor.map((s, i) => [(s.userData.role || 'decor') + i, s])];
    for (const [nom, a] of gens) { const ai = actorItem(a);
      for (const s of bsprites) { const bi = bills.find(b => b.obj === s); if (!bi || bi.cover || bas(s) || !inFront(bi, ai)) continue;
        for (const hy of [0.3, 0.9, 1.5]) { const q = uvOf(s, scr(new THREE.Vector3(a.position.x, hy, a.position.z))); if (alphaAt(s.userData.img, q.u, q.v) > 0.3) { out.push([s.userData.buildingId, nom]); break; } } } }
    return out; }
  // Écran dessiné par le code : une toile de la taille de l'image source, le contenu est projeté dans la dalle (parallélogramme b.ecran.coins, px source).
  // Même ancre et même échelle que le sprite du bâtiment ; non teinté par la lumière (un écran éclaire, il n'est pas éclairé). Une page toutes les b.ecran.periode s,
  // redessinée une fois par page (pas de planche animée, hors budget d'animations ; figé sur la première page avec « Réduire les animations »).
  function ecranSprite(b, m, base) {
    const E = b.ecran, c = document.createElement('canvas'); c.width = m.px[0]; c.height = m.px[1]; const x = c.getContext('2d');
    const [tl, tr, , bl] = E.coins || m.ecran_coins, W = Math.hypot(tr[0] - tl[0], tr[1] - tl[1]) | 0, H = bl[1] - tl[1];
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
    const draw = k => { const P = E.pages[k % E.pages.length]; x.setTransform(1, 0, 0, 1, 0, 0); x.clearRect(0, 0, c.width, c.height);
      x.setTransform((tr[0] - tl[0]) / W, (tr[1] - tl[1]) / W, 0, 1, tl[0], tl[1]); // u le long du bord haut, v vers le bas
      const g = x.createLinearGradient(0, 0, W, H); g.addColorStop(0, P.fond[0]); g.addColorStop(1, P.fond[1]); x.fillStyle = g; x.fillRect(0, 0, W, H);
      x.fillStyle = 'rgba(255,255,255,.05)'; for (let i = 0; i < H; i += 4) x.fillRect(0, i, W, 1); // trame d'écran
      const img = P.image && SKIN[P.image]; if (img) { const [sx, sy, sw, sh] = P.crop, ih = H * 0.82, iw = ih * sw / sh; x.globalAlpha = 0.95; x.drawImage(img, sx, sy, sw, sh, W * 0.06, H * 0.06, iw, ih); x.globalAlpha = 1; }
      const tx = img ? W * 0.42 : W * 0.08; x.fillStyle = '#ffffff'; x.font = `bold ${H * 0.13 | 0}px monospace`; x.fillText(P.titre, tx, H * 0.38, W - tx - 10);
      x.fillStyle = '#f2d8ff'; x.font = `${H * 0.075 | 0}px monospace`; x.fillText(P.sous, tx, H * 0.52, W - tx - 10);
      x.fillStyle = 'rgba(10,4,20,.75)'; x.fillRect(0, H * 0.84, W, H * 0.12); x.fillStyle = '#ffb860'; x.font = `${H * 0.06 | 0}px monospace`; x.fillText((E.marque ?? 'FEED 24/7') + ' · ' + P.bandeau, 8, H * 0.92, W - 16);
      x.setTransform(1, 0, 0, 1, 0, 0); t.needsUpdate = true; };
    let flash = null;
    if (E.beat) {
      const cf = document.createElement('canvas'); cf.width = m.px[0]; cf.height = m.px[1]; const xf = cf.getContext('2d');
      xf.setTransform((tr[0] - tl[0]) / W, (tr[1] - tl[1]) / W, 0, 1, tl[0], tl[1]);
      const rg = xf.createRadialGradient(W * 0.5, H * 0.5, H * 0.05, W * 0.5, H * 0.5, Math.max(W, H) * 0.68);
      rg.addColorStop(0, 'rgba(255,235,255,0.92)'); rg.addColorStop(0.55, 'rgba(235,155,255,0.62)'); rg.addColorStop(1, 'rgba(180,90,255,0.28)');
      xf.fillStyle = rg; xf.fillRect(0, 0, W, H);
      xf.strokeStyle = 'rgba(255,250,255,0.98)'; xf.lineWidth = Math.max(4, H * 0.045); xf.strokeRect(xf.lineWidth * 0.5, xf.lineWidth * 0.5, W - xf.lineWidth, H - xf.lineWidth);
      const tf = new THREE.CanvasTexture(cf); tf.colorSpace = THREE.SRGBColorSpace;
      flash = new THREE.Sprite(new THREE.SpriteMaterial({ map: tf, color: E.flash || '#f4a8ff', transparent: true, blending: THREE.AdditiveBlending, depthTest: false, depthWrite: false, opacity: 0 }));
      flash.center.copy(base.center); flash.scale.copy(base.scale); flash.position.copy(base.position);
      flash.userData.neon = 'ecran_flash'; flash.userData.fondu = 1;
    }
    draw(E.decale || 0); const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true, depthTest: false, depthWrite: false, opacity: 0.9 }));
    s.center.copy(base.center); s.scale.copy(base.scale); s.position.copy(base.position); s.userData.ecran = { draw, page: -1, decale: E.decale || 0, periode: E.periode || 9, beat: E.beat ?? null, flash, W: base.scale.x, H: base.scale.y }; ecrans.push(s); return s;
  }
  // Enseignes animées par le code (loc.enseignes, format : docs/villes/steel/ENSEIGNES_CODE.md) : calque « contour lumineux » additif posé
  // sur le support d'un bâtiment (même ancre monde), dont seule la luminosité varie (clignote, grésille, saute, pulse). Une couleur par image :
  // aucun échange de texture, aucune planche, donc hors du plafond view.animStats.on (compté à part dans animStats.enseignes).
  // « saute » : la colonne [u0, u1] du calque (une lettre) est un sprite à part qui grésille seul. dev: true -> visible seulement avec ?dev=1.
  const NEON_DEV = typeof location !== 'undefined' && new URLSearchParams(location.search).get('dev') === '1';
  function enseigne(e, loc) {
    if ((e.dev && !NEON_DEV) || e.effet === 'eteint') return; /* eteint : façade répétée, calque néon non allumé */ const item = bills.find(i => i.obj.userData.buildingId === e.building), b = loc.buildings.find(x => x.id === e.building), key = e.neon || (bman[b?.sprite + '_neon'] ? b.sprite + '_neon' : b?.sprite), m = bman[key]; // calque <clé>_neon d'Ocre, sinon le support lui-même en additif (démo)
    if (!item || !b || !m || !SKIN[key] || m.anime) return; // planche animée : pas de calque code (l'animation d'Ocre reste seule)
    const k = b.k || 1, W = m.px[0] / K * k, H = m.px[1] / K * k * (b.sy || 1), au = m.anchor[0] / m.px[0], av = 1 - m.anchor[1] / m.px[1];
    const cols = e.saute ? [[0, e.saute[0], false], [e.saute[0], e.saute[1], true], [e.saute[1], 1, false]] : [[0, 1, false]];
    for (const [u0, u1, lettre] of cols) { if (u1 - u0 <= 1e-4) continue;
      let t, cx, cy, sw, sh;
      if (u0 === 0 && u1 === 1) { const L = layerTex(key, m); t = L.tex; cx = (m.anchor[0] - L.x0) / L.cw; cy = 1 - (m.anchor[1] - L.y0) / L.ch; sw = L.cw / K * k; sh = L.ch / K * k * (b.sy || 1); }
      else { t = Object.assign(new THREE.Texture(SKIN[key]), { needsUpdate: true, colorSpace: THREE.SRGBColorSpace }); t.repeat.set(u1 - u0, 1); t.offset.set(u0, 0); cx = (au - u0) / (u1 - u0); cy = av; sw = W * (u1 - u0); sh = H; }
      const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true, depthTest: false, depthWrite: false, blending: THREE.AdditiveBlending, color: e.couleur || '#ffffff', opacity: 0 }));
      s.center.set(cx, cy); s.scale.set(sw, sh, 1); s.position.copy(item.obj.position);
      s.userData.neon = { effet: lettre ? 'gresille' : (e.effet === 'saute' ? 'fixe' : e.effet || 'fixe'), periode: e.periode || 3, ph: (e.decale || 0) + (lettre ? 0.37 : 0), i: e.intensite ?? 0.6 };
      s.userData.fondu = 1; world.add(s); item.extra.push(s); neons.push(s); }
  }
  // Calque <clé>_fenetres d'Ocre (même taille et même ancre que le bâtiment) : lueur chaude additive à vacillement lent, hors plafond animStats.on.
  function fenetre(b) {
    const key = b.sprite + '_fenetres', m = bman[key], item = bills.find(i => i.obj.userData.buildingId === b.id);
    if (!item || !m || !SKIN[key] || m.obsolete || m.anime) return;
    const k = b.k || 1, L = layerTex(key, m), W = L.cw / K * k, H = L.ch / K * k * (b.sy || 1);
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: L.tex, transparent: true, depthTest: false, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0 }));
    s.center.set((m.anchor[0] - L.x0) / L.cw, 1 - (m.anchor[1] - L.y0) / L.ch); s.scale.set(W, H, 1); s.position.copy(item.obj.position);
    s.userData.fenetre = { i: 0.34, ph: fenetres.length * 1.37 }; s.userData.fondu = 1;
    world.add(s); item.extra.push(s); fenetres.push(s);
  }
  // Calques rythmiques <clé>_ecran et <clé>_pulse (Pulse Plaza 3/4) : additifs, pilotés par l'analyseur Web Audio ostCentre (kick ~170 BPM ≈ 0,35 s, mid, énergie).
  // Sur mobile (< 700 px), priorité aux calques marqués priorite > 0 dans un plafond de 8 animations rythmiques ; le surplus reste allumé fixe.
  const T_KICK_REF = 60 / 170;
  let kickAnchor = 0, prevOstBeat = 0;
  function calqueRythme(b, calque, cfg = {}) {
    const key = cfg.key || (bman[b.sprite + '_' + calque + '_fix'] ? b.sprite + '_' + calque + '_fix' : b.sprite + '_' + calque), m = bman[key], item = bills.find(i => i.obj.userData.buildingId === b.id);
    if (!item || !m || !SKIN[key] || m.obsolete || m.anime || cfg.mode === 'eteint') return;
    const k = b.k || 1, L = layerTex(key, m), W = L.cw / K * k, H = L.ch / K * k * (b.sy || 1);
    const col = new THREE.Color(cfg.couleur || '#ffffff');
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: L.tex, transparent: true, depthTest: false, depthWrite: false, blending: THREE.AdditiveBlending, color: col.clone(), opacity: 0 }));
    s.center.set((m.anchor[0] - L.x0) / L.cw, 1 - (m.anchor[1] - L.y0) / L.ch); s.scale.set(W, H, 1); s.position.copy(item.obj.position);
    const defMode = calque === 'pulse_b' ? 'mid' : calque === 'ecran' ? 'mid' : 'kick';
    const defI = calque === 'faisceau' ? 1.0 : calque === 'pulse2' ? 1.0 : calque === 'pulse_b' ? 0.85 : calque === 'ecran' ? 0.90 : 0.98;
    const defVeille = calque === 'faisceau' ? 0.02 : (calque === 'pulse' || calque === 'pulse2') ? 0.04 : 0.06;
    const defGain = (calque === 'pulse' || calque === 'pulse2') ? 1.50 : calque === 'faisceau' ? 1.25 : 1.15;
    s.userData.pulse = {
      key,
      building: b.id,
      calque,
      mode: cfg.mode || defMode,
      i: cfg.intensite ?? defI,
      veille: cfg.veille ?? defVeille,
      gain: cfg.gain ?? defGain,
      cr: col.r,
      cg: col.g,
      cb: col.b,
      ph: cfg.decale ?? ((cfg.mode || defMode) === 'kick' ? 0 : pulses.length * 0.17),
      periode: cfg.periode || (calque === 'ecran' ? 9 : 8 * T_KICK_REF),
      priorite: cfg.priorite || 0,
      W,
      H,
      punch: cfg.punch ?? ((calque === 'pulse' || calque === 'pulse2' || calque === 'faisceau') ? 0.026 : 0.012),
    };
    s.userData.fondu = 1;
    world.add(s); item.extra.push(s); pulses.push(s);
  }
  function pulseK(u, t, ost) {
    if (u.mode === 'fixe') return 0.72;
    if (u.mode === 'balise') { const f = ((t / (u.periode || 2.8) + u.ph) % 1 + 1) % 1; return f < 0.28 ? 0.98 : 0.14; }
    const on = !!ost?.playing, tc = on ? (ost.currentTime || t) : t;
    const tk = ost?.bpm >= 95 ? 60 / ost.bpm : T_KICK_REF;
    const v = u.veille ?? 0.04;
    if (!on) {
      return u.mode === 'mesure' ? 0.18 + 0.08 * Math.sin((t / (u.periode || 9) + u.ph) * Math.PI * 2) : v;
    }
    const beat = ost.beat || 0, bass = ost.bass || 0, mid = ost.mid || 0, high = ost.high || 0, nrj = ost.energy || 0;
    const rel = (tc - kickAnchor) / tk;
    if (u.mode === 'kick') {
      const wave = Math.pow(0.5 + 0.5 * Math.cos((rel - (u.ph || 0)) * Math.PI * 2), 8);
      const env = u.ph ? Math.pow(beat, 1.55) * (0.55 + 0.45 * wave) : Math.pow(beat, 1.55);
      const drive = Math.max(env * 1.18, wave * Math.min(1, 0.28 + 0.85 * Math.max(bass, nrj * 0.85)));
      return v + (1 - v) * Math.min(1, drive);
    }
    if (u.mode === 'demi_kick') {
      const sub = Math.pow(0.5 + 0.5 * Math.cos((rel * 0.5 - (u.ph || 0)) * Math.PI * 2), 5);
      const alt = ((ost.kickCount || 0) + (u.ph >= 0.35 ? 1 : 0)) % 2 ? 1 : 0.14;
      return v + (1 - v) * Math.min(1, Math.max(Math.pow(beat, 1.45) * alt, 0.55 * sub * Math.max(0.4, bass)));
    }
    if (u.mode === 'high' || u.mode === 'aigus') {
      const shimmer = Math.pow(0.5 + 0.5 * Math.sin((rel * 2 + u.ph) * Math.PI * 2), 4);
      const eq = Math.max(high * 1.45, mid * 0.65, beat * 0.35, 0.32 * shimmer);
      return v + (1 - v) * Math.min(1, eq);
    }
    if (u.mode === 'mid') {
      const groove = Math.pow(0.5 + 0.5 * Math.sin((rel * 0.5 + u.ph + 0.25) * Math.PI * 2), 3);
      const eq = Math.max(mid * 1.30, nrj * 0.90, 0.32 * groove);
      return v + (1 - v) * Math.min(1, eq);
    }
    if (u.mode === 'mesure') {
      const w = 0.5 + 0.5 * Math.sin(((tc / (u.periode || 9)) + u.ph) * Math.PI * 2);
      return 0.18 + 0.54 * w + 0.28 * Math.min(1, nrj * 0.75 + beat * 0.6);
    }
    return 0.7;
  }
  const hash = n => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
  function neonK(u, t) { const T = u.periode, ph = u.ph, f = ((t / T + ph) % 1 + 1) % 1;
    if (u.effet === 'pulse') return 0.6 + 0.4 * Math.sin(f * Math.PI * 2);
    if (u.effet === 'clignote') return f < 0.7 ? 1 : 0.08;
    if (u.effet === 'gresille') { const n = Math.floor(t * 14 + ph * 97); return hash(n) < 0.14 ? 0.05 + 0.25 * hash(n + 9) : 0.9 + 0.1 * hash(n + 3); }
    return 1; }
  // Projecteurs dessinés par le code (loc.projecteurs) : cône additif ouvert, apex à la source, qui balaie lentement le ciel.
  // Paramètres : x, z (m) ou fx, fz (fraction de loc.size : suit l'agrandissement de la zone), y, couleur, longueur, ouverture (demi-angle, °),
  // inclinaison (° depuis la verticale), cap (° autour de la verticale), balayage (amplitude, °), periode (s), decale (s), intensite. Hors animStats.on.
  function projecteur(p, loc) {
    const L = p.longueur || 18, r = L * Math.tan((p.ouverture || 3.0) * Math.PI / 180), seg = 8, g = new THREE.ConeGeometry(r, L, 20, seg, true);
    g.rotateX(Math.PI); g.translate(0, L / 2, 0); // apex en bas (source), ouverture vers le haut
    const c = new THREE.Color(p.couleur || '#5fd3f0'), col = [], pos = g.attributes.position;
    for (let i = 0; i < pos.count; i++) { const k = Math.pow(1 - pos.getY(i) / L, 2.9); col.push(c.r * k, c.g * k, c.b * k); } // fondu rapide vers le noir = pas de lance blanche diagonale
    g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    const m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ vertexColors: true, transparent: true, opacity: p.intensite ?? 0.16, blending: THREE.AdditiveBlending, depthWrite: false, depthTest: false, side: THREE.DoubleSide }));
    const it = p.building && bills.find(i => i.obj.userData.buildingId === p.building), bm = it && bman[loc.buildings.find(x => x.id === p.building)?.sprite];
    if (p.building && !it) return;
    if (it) { const s = it.obj, src = bm?.source_faisceau_px; m.position.copy(s.position); // pied du bâtiment (ancre), puis pixel source du manifeste dans le plan du sprite
      if (src && bm.px) m.position.addScaledVector(screenRight, (src[0] - bm.anchor[0]) * s.scale.x / bm.px[0]); // le pixel source se lit à la verticale du pied (même point à l'écran) : hauteur = décalage écran / camUp.y
      if (src && bm.px) m.position.y += (bm.anchor[1] - src[1]) * s.scale.y / bm.px[1] / camUp.y;
      else m.position.y += p.y ?? 0.5; }
    else m.position.set(p.fx != null ? p.fx * loc.size.w : p.x, p.y ?? 0.5, p.fz != null ? p.fz * loc.size.d : p.z); m.rotation.order = 'YXZ'; m.renderOrder = 3; m.userData.projecteur = true;
    m.userData.beam = { cap: (p.cap || 0) * Math.PI / 180, bal: (p.balayage ?? 25) * Math.PI / 180, inc: (p.inclinaison ?? 20) * Math.PI / 180, T: p.periode || 14, ph: p.decale || 0, base: p.intensite ?? 0.25, beat: !!loc.pulses?.length };
    m.userData.fondu = 1;
    beamPose(m, 0, null); world.add(m); beams.push(m);
    if (it) { m.userData.neon = 'faisceau'; it.extra.push(m); } // trié avec son pylône : devant ce qui est derrière lui (façade de 28 m), derrière ce qui est devant ; opacité propre
  }
  function beamPose(m, t, ost) {
    const u = m.userData.beam;
    const on = u.beat && !!ost?.playing, beat = on ? (ost.beat || 0) : 0;
    const tk = ost?.bpm >= 95 ? 60 / ost.bpm : T_KICK_REF;
    const wv = on ? Math.pow(0.5 + 0.5 * Math.cos(((ost.currentTime || t) - kickAnchor) / tk * Math.PI * 2), 8) : 0;
    const kKick = on ? Math.min(1, Math.max(Math.pow(beat, 1.45) * 1.15, wv * Math.min(1, 0.25 + 0.85 * (ost.bass || 0)))) : 0;
    m.rotation.y = u.cap + u.bal * Math.sin((t + u.ph) / u.T * Math.PI * 2);
    m.rotation.x = -(u.inc + (u.beat ? 0.045 * kKick : 0));
    const sLat = u.beat ? 1 + 0.14 * kKick : 1;
    m.scale.set(sLat, 1, sLat);
    if (u.beat) m.material.opacity = Math.min(0.38, (m.userData.fondu ?? 1) * (u.base * (on ? 0.18 + 1.15 * kKick : 0.16)));
  }
  let glowT = null;
  function glowTex() { if (glowT) return glowT; const c = document.createElement('canvas'); c.width = c.height = 128; const x = c.getContext('2d'), g = x.createRadialGradient(64, 64, 0, 64, 64, 64);
    g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(0.35, 'rgba(255,255,255,.45)'); g.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = g; x.fillRect(0, 0, 128, 128); return glowT = new THREE.CanvasTexture(c); }
  // v13 : passants le long d'une boucle de points (vitesse m/s), drones en orbite au-dessus de la rue, néons qui scintillent
  function ambient(dt, t) {
    for (const s of walkers) { const u = s.userData, P = u.route, seg = []; let L = 0;
      for (let i = 0; i < P.length - (u.aller ? 1 : 0); i++) { const a = P[i], b = P[(i + 1) % P.length], l = Math.hypot(b[0] - a[0], b[1] - a[1]); seg.push([a, b, l]); L += l; }
      u.t = (u.t + dt * u.speed) % L; let r = u.t;
      for (const [a, b, l] of seg) { if (r <= l) { const k = r / l; s.position.set(a[0] + (b[0] - a[0]) * k, 0, a[1] + (b[1] - a[1]) * k); face(s, Math.atan2(b[0] - a[0], b[1] - a[1])); break; } r -= l; }
      animate(s, true, dt, t); }
    for (const s of decor) if (!walkers.includes(s)) animate(s, false, dt, t);
    for (const s of drones) { const o = s.userData.orbit, a = t * (o.speed || 0.25) + (o.ph || 0); s.position.set(o.x + Math.cos(a) * o.r, (o.y || 5) + Math.sin(t * 2.1 + (o.ph || 0)) * 0.15, o.z + Math.sin(a) * o.r * 0.6); }
    const calme = !!document.body?.classList?.contains('reduce-motion');
    const ostOn = !!ostCentre?.playing;
    if (ostOn) {
      const bNow = ostCentre.beat || 0, tcNow = ostCentre.currentTime || t;
      if (bNow > prevOstBeat + 0.25 || bNow >= 0.96) kickAnchor = tcNow;
      prevOstBeat = bNow;
    } else prevOstBeat = 0;
    const tkNow = ostCentre?.bpm >= 95 ? 60 / ostCentre.bpm : T_KICK_REF;
    const kickWave = ostOn ? Math.pow(0.5 + 0.5 * Math.cos(((ostCentre.currentTime || t) - kickAnchor) / tkNow * Math.PI * 2), 8) : 0;
    const kickEnv = calme || !ostOn ? 0 : Math.min(1, Math.max(Math.pow(ostCentre.beat || 0, 1.45) * 1.15, kickWave * Math.min(1, 0.25 + 0.85 * (ostCentre.bass || 0))));
    const midEnv = calme || !ostOn ? 0 : Math.max((ostCentre.mid || 0) * 1.25, (ostCentre.energy || 0) * 0.90);
    if (ecrans.length && !calme) for (const e of ecrans) {
      const u = e.userData.ecran, k = Math.floor(t / u.periode) + u.decale;
      if (k !== u.page) { u.page = k; u.draw(k); }
      if (u.beat || pulses.length) {
        const hit = ostOn ? Math.min(1, kickEnv * 0.96 + midEnv * 0.08) : 0;
        e.userData.beatOp = ostOn ? 0.66 + 0.34 * hit : 0.68;
        const g = ostOn ? 0.86 + 0.90 * kickEnv : 0.86;
        e.material.color.setRGB(g, g, g);
        const sw = ostOn ? 1 + 0.022 * kickEnv : 1;
        e.scale.set(u.W * sw, u.H * sw, 1);
        if (u.flash) {
          u.flash.material.opacity = ostOn ? Math.min(0.88, (u.flash.userData.fondu ?? 1) * 0.82 * Math.pow(kickEnv, 1.2)) : 0;
          u.flash.scale.set(u.W * sw, u.H * sw, 1);
        }
      }
    }
    animStats.ecrans = ecrans.length;
    // enseignes code et projecteurs : une couleur ou une rotation par image, hors plafond animStats.on (catégories à part) ; figés si mouvement réduit
    for (const s of neons) { const u = s.userData.neon; s.material.opacity = Math.min(1, (s.userData.fondu ?? 1) * u.i * (calme ? 1 : (pulses.length && u.effet === 'pulse' ? (ostOn ? 0.28 + 0.72 * kickEnv : 0.34 * neonK(u, t)) : neonK(u, t)))); }
    for (const s of fenetres) { const u = s.userData.fenetre, k = calme ? 1 : 0.78 + 0.22 * (0.6 * Math.sin(t * 1.25 + u.ph) + 0.4 * Math.sin(t * 2.9 + u.ph * 1.7));
      s.material.opacity = Math.min(1, (s.userData.fondu ?? 1) * u.i * k); }
    let pulsesOn = 0;
    if (pulses.length) {
      const pMax = viewW < 700 ? 8 : 48, pv = new THREE.Vector3(), pl = player.position;
      const ord = pulses.map(s => { pv.copy(s.position).project(cam); return { s, u: s.userData.pulse, in: Math.abs(pv.x) < 1.25 && Math.abs(pv.y) < 1.25, d: s.position.distanceToSquared(pl) }; })
        .sort((a, b) => (b.u.priorite - a.u.priorite) || (b.in - a.in) || (a.d - b.d));
      for (const { s, u, in: inn } of ord) {
        const anim = !calme && u.mode !== 'fixe' && pulsesOn < pMax && (u.priorite > 0 || inn);
        if (anim) pulsesOn++;
        s.userData.pulseOn = anim;
        const k = calme ? 0.55 : anim ? pulseK(u, t, ostCentre) : (ostOn ? 0.26 : (u.veille ?? 0.04));
        s.material.opacity = Math.min(1, (s.userData.fondu ?? 1) * u.i * k);
        const span = Math.max(0.1, 1 - (u.veille ?? 0.04));
        const g = anim && ostOn && u.gain > 1 ? 1 + (u.gain - 1) * Math.max(0, (k - (u.veille ?? 0.04)) / span) : 1;
        s.material.color.setRGB(u.cr * g, u.cg * g, u.cb * g);
        const swell = anim && ostOn && u.punch ? 1 + u.punch * Math.max(0, k - 0.22) : 1;
        s.scale.set(u.W * swell, u.H * swell, 1);
      }
    }
    if (!calme) for (const m of beams) beamPose(m, t, ostCentre);
    else for (const m of beams) if (m.userData.beam?.beat) m.material.opacity = (m.userData.fondu ?? 1) * m.userData.beam.base;
    animStats.enseignes = neons.length; animStats.fenetres = fenetres.length; animStats.pulses = pulses.length; animStats.pulsesOn = pulsesOn; animStats.projecteurs = beams.length;
    for (const f of flick) {
      const flk = f.flicker ? 0.84 + 0.16 * Math.sin(t * 7 + f.ph) * Math.sin(t * 2.3 + f.ph * 2) : 1;
      const bk = !calme && f.beat ? (ostOn ? (f.beat === 'mid' ? 0.30 + 0.95 * midEnv : 0.14 + 1.40 * kickEnv) : 0.18) : 1;
      f.m.opacity = Math.min(1, (f.obj?.userData.fondu ?? 1) * f.base * flk * bk);
      if (f.obj && f.beat && !calme) { const sc = f.s0 * (1 + (ostOn ? (f.beat === 'mid' ? 0.16 * midEnv : 0.30 * kickEnv) : 0)); f.obj.scale.set(sc, sc, 1); }
    }
    // défilement par le code (rame de la Mega-Line) : de dx mètres sur x pendant passage s, toutes les periode s
    // planches jouées une fois (portique de la Mega-Line) : remplacent le sprite de base le temps du passage, hors budget d'animations
    horloge = t; for (const u of [...uniques]) { const i = Math.floor((t - u.t0) * u.fps); if (i >= u.n) { u.s.material.map = u.base; u.s.material.needsUpdate = true; uniques.splice(uniques.indexOf(u), 1); joueEtat.fini = true; } else u.t.offset.x = i / u.n; }
    for (const mv of movers) { const k = ((t + (mv.ph || 0)) % mv.periode) / mv.passage; mv.s.visible = k < 1; if (k < 1) mv.s.position.x = mv.x0 + mv.dx * (k - 0.5); }
    // enseignes animées : seules les visibles à l'écran tournent, au plus ANIM_MAX (8 sur mobile) ; les autres restent sur leur première image
    if (anims.length) { const max = viewW < 700 ? 8 : 16, v = new THREE.Vector3(); let on = 0; const pl = player.position;
      const vis = anims.map(a => { v.copy(a.s.position).project(cam); return { a, in: Math.abs(v.x) < 1.1 && Math.abs(v.y) < 1.1, d: a.s.position.distanceToSquared(pl) }; }).sort((p, q) => (q.in - p.in) || (p.d - q.d));
      const admis = new Set(); let runs = 0;
      for (const { a, in: inn } of vis) { const k = a.g || a; let run = false;
        if (inn && !a.fige) { if (admis.has(k)) run = true; else if (on < max) { admis.add(k); on++; run = true; } }
        if (run) runs++; a.t.offset.x = run ? Math.floor(t * a.fps + a.ph) % a.n / a.n : 0; a.s.userData.animOn = run; }
      animStats.on = on; animStats.sprites = runs; animStats.total = anims.length; } }
  // Miroir horizontal : l'image regarde à droite de l'écran par défaut (manifest.faces = -1 sinon).
  const screenRight = new THREE.Vector3().crossVectors(camDir, new THREE.Vector3(0, 1, 0)).normalize();
  function face(s, heading) {
    if (heading == null) return; const sx = Math.sin(heading) * screenRight.x + Math.cos(heading) * screenRight.z;
    if (Math.abs(sx) > 0.2 && (sx > 0 ? 1 : -1) !== s.userData.facing) { s.userData.facing = sx > 0 ? 1 : -1; s.userData.turn = 0; } // quasi vertical : on garde le sens
  }
  // Animation procédurale légère (aucun asset modifié) : demi-tour rapide (largeur 1 -> 0 -> 1 en 0,14 s, l'image bascule au milieu),
  // pas de marche (rebond, léger tassement, balancement), respiration à l'arrêt. Amplitudes en mètres : identiques sur mobile.
  let tPrev = performance.now() / 1000;
  function animate(s, moving, dt, t) {
    const u = s.userData; u.turn = Math.min(1, u.turn + dt / 0.14);
    if (u.turn >= 0.5) u.shown = u.facing * u.base;
    const map = s.material.map; const flip = u.shown < 0; if ((map.repeat.x < 0) !== flip) { map.repeat.x = flip ? -1 : 1; map.offset.x = flip ? 1 : 0; }
    const width = Math.max(0.08, Math.abs(Math.cos(Math.PI * u.turn)));
    let bob = 0, sy = 1, sx = 1, rot = 0;
    if (moving) { const ph = t * 2 * Math.PI * 1.9 + u.phase; bob = Math.abs(Math.sin(ph)) * 0.045; sy = 1 - 0.025 * Math.cos(2 * ph); sx = 1 + 0.015 * Math.cos(2 * ph); rot = 0.03 * Math.sin(ph); }
    else { const ph = t * 2 * Math.PI * 0.25 + u.phase; sy = 1 + 0.012 * Math.sin(ph); }
    s.scale.set(u.w * width * sx, u.h * sy, 1); s.position.y = bob; s.material.rotation = rot;
  }
  const camUp = new THREE.Vector3().crossVectors(screenRight, camDir).normalize();
  const scr0 = p => p.x * camDir.x + p.y * camDir.y + p.z * camDir.z;
  const scr = p => ({ x: p.x * screenRight.x + p.y * screenRight.y + p.z * screenRight.z, y: p.x * camUp.x + p.y * camUp.y + p.z * camUp.z });
  function rectOf(o) { if (o.userData.box) { const B = o.userData.box, P = [B.x0, B.x1].flatMap(x => [B.z0, B.z1].flatMap(z => [0, B.h].map(y => scr({ x, y, z }))));
      return { x0: Math.min(...P.map(p => p.x)), x1: Math.max(...P.map(p => p.x)), y0: Math.min(...P.map(p => p.y)), y1: Math.max(...P.map(p => p.y)) }; }
    const a = scr(o.position), sx = Math.abs(o.scale.x), sy = o.scale.y; return { x0: a.x - o.center.x * sx, x1: a.x + (1 - o.center.x) * sx, y0: a.y - o.center.y * sy, y1: a.y + (1 - o.center.y) * sy }; }
  function uvOf(o, p) { const r = rectOf(o); let u = (p.x - r.x0) / (r.x1 - r.x0); if (o.material.map?.repeat.x < 0) u = 1 - u; return { u, v: (p.y - r.y0) / (r.y1 - r.y0) }; }
  // Ordre de dessin antisymétrique : A avant B si B est devant. Séparation franche sur x ou z quand l'autre axe ne contredit pas ;
  // en séparation diagonale (NE vs SO) au même pixel écran, le plus grand z est mathématiquement plus proche de la caméra.
  const under = (o, c) => o.x0 < c.x1 - 1e-6 && o.x1 > c.x0 + 1e-6 && o.z0 < c.z1 - 1e-6 && o.z1 > c.z0 + 1e-6;
  function inFront(b, a) {
    if (!!a.cover !== !!b.cover && under(a, b)) return !!b.cover; /* une halle couvre tout ce qui est sous son toit [tour Valentin] */
    if (!!a.fond !== !!b.fond) return !!a.fond; /* une pièce de fond (dalle/toit) reste toujours derrière les façades et acteurs */
    const bx = b.x0 >= a.x1 - 1e-6, ax = a.x0 >= b.x1 - 1e-6, bz = b.z0 >= a.z1 - 1e-6, az = a.z0 >= b.z1 - 1e-6;
    if ((bx || bz) && !(ax || az)) return true;
    if ((ax || az) && !(bx || bz)) return false;
    if (bz !== az) return bz;
    return b.x0 + b.x1 + b.z0 + b.z1 > a.x0 + a.x1 + a.z0 + a.z1;
  }
  const actorItem = a => ({ obj: a, actor: true, x0: a.position.x - 0.3, x1: a.position.x + 0.3, z0: a.position.z - 0.3, z1: a.position.z + 0.3, extra: [] });
  function topoSort(list) {
    const n = list.length, R = list.map(i => rectOf(i.obj)), indeg = new Array(n).fill(0), out = list.map(() => []);
    for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
      const a = R[i], b = R[j]; if (a.x1 < b.x0 || b.x1 < a.x0 || a.y1 < b.y0 || b.y1 < a.y0) continue;
      if (inFront(list[j], list[i])) { out[i].push(j); indeg[j]++; } else { out[j].push(i); indeg[i]++; }
    }
    const key = i => list[i].x0 + list[i].x1 + list[i].z0 + list[i].z1, done = new Array(n).fill(false), res = [];
    for (let k = 0; k < n; k++) {
      let best = -1; for (let i = 0; i < n; i++) if (!done[i] && indeg[i] === 0 && (best < 0 || key(i) < key(best) || (key(i) === key(best) && i < best))) best = i;
      if (best < 0) for (let i = 0; i < n; i++) if (!done[i] && (best < 0 || key(i) < key(best) || (key(i) === key(best) && i < best))) best = i;
      done[best] = true; for (const j of out[best]) indeg[j]--;
      res.push(list[best]);
    }
    return res;
  }
  function painter() {
    // 1) Ordre mutuel des bâtiments/meubles calculé seul : un personnage ou passant mobile ne peut JAMAIS inverser deux bâtiments.
    const statics = topoSort(bills);
    const actors = [player, companion].filter(a => a.visible).concat(npcSprites.filter(n => n.visible), decor, drones).map(actorItem);
    actors.sort((a, b) => (a.x0 + a.x1 + a.z0 + a.z1) - (b.x0 + b.x1 + b.z0 + b.z1));
    // 2) Insertion de chaque acteur juste avant le premier bâtiment devant lui dont le rectangle écran le recouvre.
    const merged = [...statics];
    const rectCache = new Map(merged.map(it => [it, rectOf(it.obj)]));
    for (const ac of actors) {
      const ra = rectOf(ac.obj); rectCache.set(ac, ra);
      let lo = 0, hi = merged.length;
      for (let i = 0; i < merged.length; i++) {
        const it = merged[i], rb = rectCache.get(it);
        if (ra.x1 < rb.x0 || rb.x1 < ra.x0 || ra.y1 < rb.y0 || rb.y1 < ra.y0) continue;
        if (inFront(ac, it)) lo = Math.max(lo, i + 1);
        else if (inFront(it, ac) && i < hi) hi = i;
      }
      const pos = lo <= hi ? hi : lo;
      merged.splice(pos, 0, ac);
    }
    let ord = 10;
    for (const it of merged) {
      it.obj.renderOrder = ord; for (const e of it.extra) e.renderOrder = ord + 1; ord += 2;
    }
    return merged;
  }
  // Règle d'occultation : un bâtiment passe à 30 % d'opacité quand un acteur est derrière lui (ordre du peintre)
  // et qu'un point du corps de l'acteur (0,3 à 1,5 m) tombe sur un pixel opaque du sprite.
  function npcGhosts() { // PNJ sous une halle opaque : second rendu sans test de profondeur à 45 %, au-dessus du toit (repérable de loin)
    for (const n of npcSprites) { const gh = n.userData.ghost; if (!gh) continue; const ai = actorItem(n);
      gh.visible = n.visible && bills.some(b => b.cover && b.obj.material.opacity > 0.5 && under(ai, b)); gh.position.copy(n.position);
      if (n.material.map !== gh.material.map) gh.material.map = n.material.map; }
  }
  function spriteOcclusion() {
    for (const s of bsprites) s.userData.targetOpacity = 1;
    for (const a of [player, companion]) { if (!a.visible) continue; const ai = actorItem(a);
      for (const s of bsprites) { const bi = bills.find(b => b.obj === s);
        if (bi.cover) { const m = 1.5; if (a.position.x > bi.x0 - m && a.position.x < bi.x1 + m && a.position.z > bi.z0 - m && a.position.z < bi.z1 + m) s.userData.targetOpacity = 0.3; continue; } // halle : transparente dès l'emprise ou à 1,5 m
        if (!inFront(bi, ai)) continue;
        for (const hy of [0.3, 0.9, 1.5]) { const q = uvOf(s, scr(new THREE.Vector3(a.position.x, hy, a.position.z))); if (alphaAt(s.userData.img, q.u, q.v) > 0.3) { s.userData.targetOpacity = 0.3; break; } } } }
    for (const o of phOf) { o.userData.targetOpacity = 1; const bi = bills.find(b => b.obj === o), r = rectOf(o);
      for (const a of [player, companion]) { if (!a.visible || !inFront(bi, actorItem(a))) continue; const q = scr(new THREE.Vector3(a.position.x, 0.9, a.position.z));
        if (q.x > r.x0 && q.x < r.x1 && q.y > r.y0 && q.y < r.y1) o.userData.targetOpacity = 0.3; }
      const m = o.material; m.opacity += (o.userData.targetOpacity - m.opacity) * 0.3; for (const e of bi.extra) if (e.userData.neon || e.userData.fenetre || e.userData.pulse) e.userData.fondu = m.opacity; else e.material.opacity = m.opacity; }
    for (const s of bsprites) { const m = s.material; m.opacity += (s.userData.targetOpacity - m.opacity) * 0.3; for (const b of bills) if (b.obj === s) for (const e of b.extra) if (e.userData.neon || e.userData.fenetre || e.userData.pulse || e.userData.projecteur) e.userData.fondu = m.opacity; else if (e.userData.ecran) e.material.opacity = Math.min(1, m.opacity * (e.userData.beatOp ?? 0.9)); else e.material.opacity = Math.min(0.9, m.opacity); }
  }
  // v6 : un meuble devant un personnage (joueur, compagnon, PNJ en dialogue) qui le cache au pixel passe à 35 %.
  function furnitureOcclusion() {
    const who = [player, companion].filter(a => a.visible); const dn = game.state.dialogue && npcSprites.find(n => n.userData.npc === game.state.dialogue.npc); if (dn) who.push(dn);
    for (const s of fsprites) { s.userData.targetOpacity = 1; const bi = bills.find(b => b.obj === s);
      for (const a of who) { if (!inFront(bi, actorItem(a))) continue; let hit = false;
        for (const hy of [0.3, 0.9, 1.5]) { const q = uvOf(s, scr(new THREE.Vector3(a.position.x, hy, a.position.z))); if (alphaAt(s.userData.img, q.u, q.v) > 0.3) { hit = true; break; } }
        if (hit) { s.userData.targetOpacity = 0.35; break; } }
      s.material.opacity += (s.userData.targetOpacity - s.material.opacity) * 0.3; }
  }
  const ray = new THREE.Raycaster();
  function updateOcclusion() {
    for (const m of solids) m.userData.targetOpacity = 1;
    for (const a of [player, companion]) {
      if (!a.visible) continue;
      for (const hy of [0.5, 1.0, 1.6]) for (const lat of [-0.25, 0, 0.25]) { // v6 : aussi sur les bords du sprite (porte de sortie devant le joueur)
        const p = a.position.clone(); p.y = hy; p.addScaledVector(screenRight, lat); ray.set(p.clone().addScaledVector(camDir, -200), camDir);
        for (const hit of ray.intersectObjects(solids, false)) if (hit.distance < 199.9) hit.object.userData.targetOpacity = 0.15;
      }
    }
    for (const m of solids) for (const mt of [].concat(m.material)) { const o = mt.opacity; mt.opacity = o + (m.userData.targetOpacity - o) * 0.3; mt.depthWrite = mt.opacity > 0.9; }
  }
  let ppm = 30, viewW = innerWidth, viewH = innerHeight, camCible = null, plan = 0, planLoc = null, planSort = false, planPos = [0, 0], planLarge = false; // plan : poids du plan d'arrivée (1 à l'arrivée, 0 après les premiers pas) // camCible : point du sol au centre de l'écran (contrôle des tests)
  function measureView() {
    const vv = typeof visualViewport !== 'undefined' ? visualViewport : null;
    const w = Math.round(vv?.width || innerWidth || canvas.clientWidth || 1);
    const h = Math.round(vv?.height || innerHeight || canvas.clientHeight || 1);
    return [Math.max(1, w), Math.max(1, h)];
  }
  function resize() {
    const [w, h] = measureView();
    viewW = w; viewH = h;
    renderer.setPixelRatio(Math.min((typeof devicePixelRatio !== 'undefined' && devicePixelRatio) || 1, 2));
    renderer.setSize(w, h, !!canvas.style);
    ppm = w < 700 ? UNITS.camera.pxPerMeterMobile : UNITS.camera.pxPerMeterDesktop;
    cam.userData.zoom = null;
  }
  addEventListener('resize', resize);
  addEventListener('orientationchange', () => { resize(); if (typeof setTimeout === 'function') setTimeout(resize, 80); });
  if (typeof visualViewport !== 'undefined' && visualViewport) visualViewport.addEventListener('resize', resize);
  resize();
  let camOverride = null, camShift = 0, userZoom = 1;
  function setZoom(z, { user = true } = {}) {
    if (!Number.isFinite(z)) return userZoom;
    userZoom = Math.round(Math.min(ZOOM_MAX, Math.max(ZOOM_MIN, z)) * 1000) / 1000;
    if (user && plan > 0) { planSort = true; plan = 0; }
    cam.userData.zoom = null;
    return userZoom;
  }
  let groundMesh = null, cbt = null; // combat C1 : grille, cases atteignables, chemin, unités ennemies
  function render() {
    const [mw, mh] = measureView(); if (mw !== viewW || mh !== viewH) resize();
    ({ LOCATIONS, DOORS, NPCS } = game.world);
    const s = game.state;
    if (builtFor !== s.location) build(s.location);
    const visible=kind=>game.world.testing||game.world.editorLayers?.[kind]?.visible!==false;
    if(groundMesh)groundMesh.visible=visible('zone');
    for(const b of bsprites){b.visible=visible('building');const item=bills.find(i=>i.obj===b);for(const e of item?.extra||[])e.visible=b.visible;}
    for(const i of bills)if(i.obj.userData.editorId)i.obj.visible=visible('prop');
    for(const n of npcSprites)n.visible=visible('actor');
    player.visible=visible('actor');player.userData.editorId=s.player.editorId;
    const playerScale=game.world.testing?1:(s.player.editorScale||1), playerH=sprites.player.height_m*Math.cos(pitch)*playerScale;
    player.userData.h=playerH;player.userData.w=playerH*sprites.player.px[0]/sprites.player.px[1];
    player.position.set(s.player.x, 0, s.player.z);
    companion.visible = s.companion.mode === 'follow' && s.companion.location === s.location;
    companion.position.set(s.companion.x, 0, s.companion.z);
    face(player, s.player.heading); face(companion, s.companion.heading);
    for (const n of npcSprites) face(n, s.npcs[n.userData.npc]?.heading);
    const tNow = performance.now() / 1000, dt = Math.min(0.1, tNow - tPrev); tPrev = tNow;
    animate(player, s.player.path.length > 0, dt, tNow); animate(companion, s.companion.path.length > 0 && s.companion.location === s.location, dt, tNow);
    for (const n of npcSprites) animate(n, false, dt, tNow);
    ambient(dt, tNow);
    const loc = LOCATIONS[s.location];
    const target = camOverride ? new THREE.Vector3(camOverride.x, 0, camOverride.z) : new THREE.Vector3(s.player.x, 0, s.player.z);
    if (loc.kind === 'interior' && !camOverride) target.set(loc.size.w / 2, 0, loc.size.d / 2);
    // loc.cadre : { mobile|desktop: { x: [min, max], z: [min, max] } } : le cadre suit le joueur mais reste sur la rue (pas de vide aux arrivées par les bouts)
    // loc.cadre.arrivee : { mobile|desktop: { ppm, avance, u, w } } : plan d'arrivée (plan large qui montre le lieu : toit de l'Arena), tenu tant que le joueur n'a pas bougé, puis retour en douceur au cadre de jeu
    //   ppm (zoom), avance (m : le cadre regarde devant le joueur, vers le haut de l'écran), u et w (bornes en mètres dans les axes de l'écran : droite, profondeur), le joueur restant toujours dans le cadre
    const mob = viewW < 700, pick = c => c && ((mob ? c.mobile : c.desktop) || (c.mobile || c.desktop ? null : c));
    if (planLoc !== s.location) { planLoc = s.location; plan = 1; planSort = false; planPos = [s.player.x, s.player.z]; }
    if (!planSort && (s.player.path.length > 0 || Math.hypot(s.player.x - planPos[0], s.player.z - planPos[1]) > 0.3)) planSort = true;
    if (planSort) plan = Math.max(0, plan - dt * 1.2);
    const CA = loc.cadre && !camOverride ? pick(loc.cadre) : null, PA = loc.cadre?.arrivee && !camOverride && plan > 0 ? pick(loc.cadre.arrivee) : null;
    const cl = (v, a, b) => Math.min(b, Math.max(a, v)), f = new THREE.Vector3(camDir.x, 0, camDir.z).normalize(), R = new THREE.Vector3(-f.z, 0, f.x);
    const zPpm = ppm * userZoom, baseInt = Math.min(ppm * 1.8, viewW / (loc.size.w * 1.6));
    const cadrer = (t, C, z0) => { const up = t.dot(R), wp = t.dot(f); if (C.avance) t.addScaledVector(f, C.avance);
      if (C.u || C.w) { const u = t.dot(R), w = t.dot(f), lu = Math.max(1, viewW / 2 / z0 - 1.5), lw = Math.max(1, (viewH / 2 / z0 - 2) / Math.sin(pitch));
        const u2 = cl(C.u ? cl(u, C.u[0], C.u[1]) : u, up - lu, up + lu), w2 = cl(C.w ? cl(w, C.w[0], C.w[1]) : w, wp - lw, wp + lw); t.addScaledVector(R, u2 - u).addScaledVector(f, w2 - w); }
      if (C.x) t.x = cl(t.x, C.x[0], C.x[1]); if (C.z) t.z = cl(t.z, C.z[0], C.z[1]);
      if ((C.x || C.z) && userZoom > 1) { const u = t.dot(R), w = t.dot(f), lu = Math.max(1, viewW / 2 / z0 - 1.5), lw = Math.max(1, (viewH / 2 / z0 - 2) / Math.sin(pitch));
        t.addScaledVector(R, cl(u, up - lu, up + lu) - u).addScaledVector(f, cl(w, wp - lw, wp + lw) - w); }
      return t; };
    let zoomCadre = null;
    if (CA) { const zC = (CA.ppm || ppm) * userZoom; cadrer(target, CA, zC); zoomCadre = CA.ppm ? zC : null; }
    if (PA) { const k = plan * plan * (3 - 2 * plan), zA = PA.ppm || zPpm, tA = cadrer(new THREE.Vector3(s.player.x, 0, s.player.z), PA, zA);
      target.lerp(tA, k); zoomCadre = 1 / ((1 - k) / (zoomCadre || zPpm) + k / zA); }
    if (loc.kind === 'interior' && !camOverride && userZoom > 1) {
      const zI = baseInt * userZoom, p0 = new THREE.Vector3(s.player.x, 0, s.player.z), up = p0.dot(R), wp = p0.dot(f);
      const u = target.dot(R), w = target.dot(f), lu = Math.max(1, viewW / 2 / zI - 1.5), lw = Math.max(1, (viewH / 2 / zI - 2) / Math.sin(pitch));
      target.addScaledVector(R, cl(u, up - lu, up + lu) - u).addScaledVector(f, cl(w, wp - lw, wp + lw) - w);
    }
    planLarge = !!PA && plan > 0.5; // plan large d'arrivée : les noms (PNJ, services) sont masqués, seules les sorties restent ; ils reviennent au premier pas
    camCible = [+target.x.toFixed(2), +target.z.toFixed(2)];
    // mobile : quand le dialogue est ouvert, le cadre remonte pour garder joueur et PNJ visibles au-dessus du panneau
    const dlg = document.getElementById('dialogue');
    let wantShift = 0;
    if (!camOverride && viewW <= 600 && dlg && !dlg.hidden && dlg.offsetHeight) {
      const top = dlg.getBoundingClientRect().top;
      wantShift = Math.max(0, viewH / 2 - top / 2 - 20);
      if (loc.kind === 'interior') target.set((target.x + s.player.x) / 2, 0, (target.z + s.player.z) / 2);
    }
    camShift += (wantShift - camShift) * Math.min(1, dt * 8); if (Math.abs(wantShift - camShift) < 0.5) camShift = wantShift;
    cam.position.copy(target).addScaledVector(camDir, -80); cam.lookAt(target);
    const zoom = camOverride?.ppm || zoomCadre || (loc.kind === 'interior' ? baseInt * userZoom : zPpm);
    if (zoom !== cam.userData.zoom || camShift !== cam.userData.shift || cam.userData.cx!==camOverride?.cx || cam.userData.cy!==camOverride?.cy) { cam.userData.shift = camShift; cam.userData.zoom = zoom; const w = viewW, h = viewH; const cx=camOverride?.cx??w/2,cy=camOverride?.cy??h/2;cam.userData.cx=camOverride?.cx;cam.userData.cy=camOverride?.cy;cam.left=-cx/zoom;cam.right=(w-cx)/zoom;cam.top=(cy-camShift)/zoom;cam.bottom=-(h-cy+camShift)/zoom; cam.updateProjectionMatrix(); }
    if (exterior) { painter(); spriteOcclusion(); npcGhosts(); } else { painter(); furnitureOcclusion(); updateOcclusion(); }
    combatOverlay();
    for(const n of npcSprites)if(n.userData.ghost&&!visible('actor'))n.userData.ghost.visible=false;
    world.traverse(o=>{if(o.userData.wall)o.visible=visible('building');if(o.userData.propBox)o.visible=visible('prop');if(o.isMesh&&o.geometry.type==='RingGeometry'&&o.userData.doorId)o.visible=visible('building');});
    for(const s of bsprites) { const b=LOCATIONS[game.state.location].buildings.find(b=>b.id===s.userData.buildingId); if(b) { const sh=(b.editorLayer||0)*10000+(b.editorDepth||0)+(b.fond?-100000:0); s.renderOrder += sh;/* b.fond : masse de fond (toit de l'Arena, dalles) peinte avant tout, derrière façades et acteurs, y compris ses calques _pulse */ if (sh) { const it = bills.find(i => i.obj === s); for (const e of it?.extra || []) e.renderOrder += sh; } if(b.editorGhost) s.material.opacity=.45; } } renderer.render(scene, cam);
    const r = canvas.getBoundingClientRect();
    const placed = []; // étiquettes : bornées à l'écran (les deux axes), puis écartées des panneaux d'interface et entre elles
    const toScr = p => { const v = p.clone().project(cam); return { x: r.left + (v.x + 1) / 2 * r.width, y: r.top + (1 - v.y) / 2 * r.height }; };
    for (const l of labels) { const vis = !l.visible || l.visible(); l.el.hidden = !vis; l.el.dataset.off = ''; if (!vis) continue; const q = toScr(l.getPos()); const lw = l.el.offsetWidth || 0, lh = l.el.offsetHeight || 0; let lx = q.x, ly = q.y;
      const sortie = l.el.classList.contains('edge') || l.el.classList.contains('junction'), npc = l.el.classList.contains('npc');
      if (planLarge && !sortie) { l.el.hidden = true; continue; }
      if (!sortie && (lx < 0 || lx > viewW)) { l.el.hidden = true; l.el.dataset.off = '1'; continue; }
      if (lw && lw + 8 < viewW) lx = Math.min(viewW - 4 - lw / 2, Math.max(4 + lw / 2, lx));
      let foot = null; if (npc && l.foot) foot = toScr(l.foot());
      if (!sortie && !(npc && foot && foot.y > 0 && ly - lh < 4) && (ly - lh > viewH || ly < 0)) { l.el.hidden = true; l.el.dataset.off = '1'; continue; } // hors écran vertical : masqué (sorties : marqueur gardé au bord)
      if (sortie && lh) ly = Math.min(viewH - 4, Math.max(lh + 4, ly));
      let below = false; if (npc && foot && lh && ly - lh < 4) { if (foot.y < 0 || foot.y + lh + 6 > viewH) { l.el.hidden = true; continue; } ly = foot.y + lh + 6; below = true; } // PNJ en haut du cadre : libellé sous ses pieds, jamais sur sa tête [Régie B]
      placed.push({ l, lx, ly, lw, lh, npc, below, foot }); }
    const hudRects = ['hud', 'locbox', 'obj', 'msg', 'dialogue', 'panel', 'keys', 'zoom', 'act', 'mini', 'cbt-file', 'cbt-res', 'cbt-actions'].map(id => document.getElementById(id))
      .filter(e => e && !e.hidden && e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden')
      .map(e => e.getBoundingClientRect()).filter(q => q.width > 0 && q.height > 0); // barre : son cadre entier (fond semi-transparent)
    const hits = (a, q, m = 2) => a.lx - a.lw / 2 < q.right + m && a.lx + a.lw / 2 > q.left - m && a.ly - a.lh < q.bottom + m && a.ly > q.top - m;
    const overHud = a => hudRects.find(q => hits(a, q));
    placed.sort((a, b) => (b.npc - a.npc) || (b.ly - a.ly)); // PNJ d'abord (prioritaires), puis de bas en haut
    const done = [], free = (a, x, y, extra) => { const t = { lx: x, ly: y, lw: a.lw, lh: a.lh }; return !hudRects.some(q => hits(t, q)) && !(extra || []).some(q => hits(t, q, 0)); };
    const clash = (a, x, y) => done.some(b => Math.abs(x - b.lx) < (a.lw + b.lw) / 2 + 3 && y > b.ly - b.lh - 3 && y - a.lh < b.ly + 3);
    // corps (tête aux pieds) de TOUS les PNJ visibles : aucun libellé ne s'y pose, ni le leur ni un autre [Régie B ; Régie 29/10 : Mei, Dorn, technicien, marchande]
    const bodies = labels.filter(l => l.foot && l.npcSprite?.visible !== false).map(l => { const f = toScr(l.foot()), h = toScr(l.getPos()), hw = Math.max(10, 0.22 * (f.y - h.y));
      return { left: f.x - hw, right: f.x + hw, top: h.y + 2, bottom: f.y }; }).filter(q => q.bottom > 0 && q.top < viewH && q.right > 0 && q.left < viewW);
    for (const a of placed) {
      const ok = (x, y, strict) => y - a.lh >= 2 && y <= viewH - 2 && free(a, x, y, bodies) && (!strict || !clash(a, x, y));
      if (!ok(a.lx, a.ly, true)) { // positions candidates : bords des panneaux, sous les pieds du PNJ, voisinage des autres libellés ; la plus proche gagne
        const ys = [a.ly], xs = [a.lx];
        for (const q of hudRects) { ys.push(q.top - 3, q.bottom + a.lh + 3); xs.push(q.left - a.lw / 2 - 3, q.right + a.lw / 2 + 3); }
        if (a.foot) ys.push(a.foot.y + a.lh + 6);
        for (const b of done) ys.push(b.ly - b.lh - 4, b.ly + a.lh + 4);
        for (const q of bodies) { ys.push(q.top - 3, q.bottom + a.lh + 3); xs.push(q.left - a.lw / 2 - 3, q.right + a.lw / 2 + 3); } // contourner les corps des PNJ
        let best = null, bd = Infinity;
        for (const strict of [true, false]) { for (const x of xs) { if (x - a.lw / 2 < 2 || x + a.lw / 2 > viewW - 2) continue; for (const y of ys) { if (!ok(x, y, strict)) continue;
          const d = Math.abs(y - a.ly) + 1.5 * Math.abs(x - a.lx); if (d < bd) { bd = d; best = [x, y]; } } } if (best) break; }
        if (best) [a.lx, a.ly] = best; }
      done.push(a); a.l.el.style.transform = `translate(-50%,-100%) translate(${a.lx}px,${a.ly}px)`;
      // filet : un libellé qu'on n'a pas pu sortir d'un panneau d'interface est masqué, jamais coupé
      const under = !!hudRects.find(q => hits(a, q, 0)); a.l.el.style.visibility = under ? 'hidden' : ''; a.l.el.dataset.underHud = under ? '1' : ''; a.l.el.dataset.below = a.below ? '1' : ''; }
  }
  // ---------- Combat C1 : grille de 1 m semi-transparente (seulement en combat), cases atteignables, aperçu du chemin et coût ----------
  function combatOverlay() {
    const c = game.state.combat;
    if (!c) { if (cbt) { scene.remove(cbt.group); for (const e of cbt.enemies) { world.remove(e); npcSprites.splice(npcSprites.indexOf(e), 1); } cbt.cost.remove(); cbt = null; } return; }
    if (!cbt || cbt.id !== c) { if (cbt) { scene.remove(cbt.group); cbt.cost.remove(); }
      const group = new THREE.Group(); scene.add(group); const z = c.zone, pts = [];
      for (let i = z.i0; i <= z.i1; i++) for (let j = z.j0; j <= z.j1; j++) if (game.combat.cellFree(i, j)) pts.push(i, 0.03, j, i + 1, 0.03, j, i, 0.03, j, i, 0.03, j + 1, i + 1, 0.03, j, i + 1, 0.03, j + 1, i, 0.03, j + 1, i + 1, 0.03, j + 1);
      const gg = new THREE.BufferGeometry(); gg.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
      const lines = new THREE.LineSegments(gg, new THREE.LineBasicMaterial({ color: '#1a1208', transparent: true, opacity: 0.32, depthTest: false, depthWrite: false })); lines.renderOrder = 3; group.add(lines);
      const mk = (col, op) => new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: op, depthTest: false, depthWrite: false });
      const reach = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.92, 0.92).rotateX(-Math.PI / 2), mk('#f2b44a', 0.10), (2 * z.i1 - 2 * z.i0 + 3) ** 2); reach.renderOrder = 3; group.add(reach);
      const exitM = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.92, 0.92).rotateX(-Math.PI / 2), mk('#b8d0a0', 0.10), 4 * (z.i1 - z.i0 + 1)); exitM.renderOrder = 3; group.add(exitM);
      let ne = 0; const m4 = new THREE.Matrix4(); for (let i = z.i0; i <= z.i1; i++) for (let j = z.j0; j <= z.j1; j++) if ((i === z.i0 || i === z.i1 || j === z.j0 || j === z.j1) && game.combat.cellFree(i, j)) exitM.setMatrixAt(ne++, m4.makeTranslation(i + 0.5, 0.035, j + 0.5)); exitM.count = ne;
      const pathL = new THREE.InstancedMesh(new THREE.CircleGeometry(0.13, 16).rotateX(-Math.PI / 2), mk('#ffe2a8', 0.85), 64); pathL.renderOrder = 4; pathL.count = 0; group.add(pathL);
      const tgt = new THREE.Mesh(new THREE.RingGeometry(0.28, 0.4, 24).rotateX(-Math.PI / 2), mk('#ffe2a8', 0.8)); tgt.renderOrder = 4; group.add(tgt);
      const cost = document.createElement('div'); cost.className = 'wlabel cbt-cost'; labelLayer.appendChild(cost);
      const enemies = c.units.filter(u => !u.joueur).map(u => { const sp = spriteMesh(u.sprite, null, true); sp.material.depthTest = false; sp.material.transparent = true; sp.userData.unit = u.id; world.add(sp); npcSprites.push(sp); return sp; });
      // anneau ennemi toujours visible (haillons couleur sable sur le sable) : liseré sombre + anneau rouge
      const rings = enemies.map(() => { const g2 = new THREE.Group(); const a = new THREE.Mesh(new THREE.RingGeometry(0.34, 0.5, 32).rotateX(-Math.PI / 2), mk('#1a1208', 0.55)); a.renderOrder = 4;
        const b = new THREE.Mesh(new THREE.RingGeometry(0.37, 0.46, 32).rotateX(-Math.PI / 2), mk('#e0503c', 0.9)); b.renderOrder = 5; b.position.y = 0.002; g2.add(a, b); group.add(g2); return g2; });
      cbt = { id: c, group, reach, pathL, tgt, cost, enemies, rings, key: '' }; }
    for (const e of cbt.enemies) { const u = c.units.find(q => q.id === e.userData.unit); e.visible = u.actif; e.position.set(u.x, 0, u.z); const rg = cbt.rings[cbt.enemies.indexOf(e)]; rg.visible = u.actif; rg.position.set(u.x, 0.045, u.z); if (u.heading !== undefined) face(e, u.heading); }
    const pl = c.units.find(u => u.joueur), mine = c.phase === 'joueur' && c.units[c.actif] === pl && !pl.path.length, pv = c.preview;
    const att = pv && pv.type === 'attaque', key = JSON.stringify([mine, pl.i, pl.j, pl.pa, pv && [pv.type, pv.i, pv.j, pv.pa, pv.ok, pv.chance], c.units.map(u => [u.i, u.j, u.actif])]);
    if (key !== cbt.key) { cbt.key = key; const m4 = new THREE.Matrix4(); let n = 0;
      if (mine) for (const q of game.combat.reachable()) if (q.i !== pl.i || q.j !== pl.j) cbt.reach.setMatrixAt(n++, m4.makeTranslation(q.i + 0.5, 0.04, q.j + 0.5));
      cbt.reach.count = n; cbt.reach.instanceMatrix.needsUpdate = true;
      const showPv = mine && pv && pv.cells.length > 1; cbt.pathL.visible = cbt.tgt.visible = !!(mine && pv);
      { let k = 0; if (showPv) for (const [a, b] of pv.cells.slice(1, -1)) if (k < 64) cbt.pathL.setMatrixAt(k++, m4.makeTranslation(a + 0.5, 0.05, b + 0.5)); cbt.pathL.count = k; cbt.pathL.instanceMatrix.needsUpdate = true; }
      if (mine && pv) { cbt.tgt.position.set(pv.i + 0.5, 0.05, pv.j + 0.5); cbt.tgt.material.color.set(pv.ok ? '#ffe2a8' : '#d06050'); cbt.pathL.material.color.set(pv.ok ? '#ffe2a8' : '#d06050'); }
      cbt.cost.textContent = mine && pv ? (att ? (pv.raison === 'pas_de_ligne_de_vue' ? 'pas de vue' : pv.raison === 'hors_portee' ? 'au contact' : `${pv.chance} % \u00b7 ${pv.pa} PA` + (pv.couverture ? ` \u00b7 couvert ${pv.couverture}` : '')) : pv.pa != null ? `${pv.pa} PA` : '\u00d7') : '';
      cbt.cost.hidden = !(mine && pv); cbt.cost.classList.toggle('att', !!att); cbt.cost.classList.toggle('ko', !!(mine && pv && !pv.ok)); }
    if (mine && pv) { const v = new THREE.Vector3(pv.i + 0.5, att ? 2.0 : 0.6, pv.j + 0.5).project(cam), r = canvas.getBoundingClientRect();
      cbt.cost.style.transform = `translate(-50%,-100%) translate(${r.left + (v.x + 1) / 2 * r.width}px,${r.top + (1 - v.y) / 2 * r.height}px)`; }
  }
  function pick(clientX, clientY) {
    render();
    const r = canvas.getBoundingClientRect();
    ray.setFromCamera(new THREE.Vector2(((clientX - r.left) / r.width) * 2 - 1, -((clientY - r.top) / r.height) * 2 + 1), cam);
    if (arguments[2]) { const h = groundMesh && ray.intersectObject(groundMesh, false)[0]; return h ? { kind: 'ground', x: h.point.x, z: h.point.z } : null; } // combat : sol seul
    if (exterior) { // sprites : pixel opaque le plus haut dans l'ordre du peintre ; un bâtiment transparent laisse passer le clic
      const hits = ray.intersectObjects(pickables, false), ring = hits.find(h => h.object.userData.doorId); if (ring) return { kind: 'door', doorId: ring.object.userData.doorId };
      const nh = hits.find(h => h.object.userData.npc); if (nh) return { kind: 'npc', npcId: nh.object.userData.npc }; // v12 : PNJ dehors (Steel)
      const c = scr(ray.ray.origin); let top = null;
      for (const s of bsprites) { if (s.material.opacity < 0.5) continue; const q = uvOf(s, c); if (alphaAt(s.userData.img, q.u, q.v) > 0.5 && (!top || s.renderOrder > top.renderOrder)) top = s; }
      if (top) { const u = top.userData;
        const g = hits.find(h => h.object.userData.ground), b = LOCATIONS[builtFor].buildings.find(b => b.id === u.buildingId);
        if ((!u.visitable || (bman[u.img]?.height_m ?? 0) > 12) && g && (g.point.x < b.x - 1 || g.point.x > b.x + b.w + 1 || g.point.z < b.z - 1 || g.point.z > b.z + b.d + 1)) return { kind: 'ground', x: g.point.x, z: g.point.z };
        if (!u.visitable) { // clic sur un bâtiment fermé : si le sol visé est hors de son emprise (rue cachée derrière), on marche
          // décor praticable (halle, escalier, dalle : `solid` explicite) : le sol visé hors des parties pleines reste cliquable
          if (g && b.solid && !b.solid.some(q => g.point.x >= q.x && g.point.x <= q.x + q.w && g.point.z >= q.z && g.point.z <= q.z + q.d)) return { kind: 'ground', x: g.point.x, z: g.point.z };
          return { kind: 'closed', label: u.label, buildingId: u.buildingId }; }
        const ds = DOORS.filter(d => d.buildingId === u.buildingId).map(d => ({ d, p: scr(new THREE.Vector3(d.opening.x, 1, d.opening.z)) }));
        ds.sort((a, b) => Math.hypot(a.p.x - c.x, a.p.y - c.y) - Math.hypot(b.p.x - c.x, b.p.y - c.y)); return { kind: 'door', doorId: ds[0].d.id }; }
      const g = hits.find(h => h.object.userData.ground); return g ? { kind: 'ground', x: g.point.x, z: g.point.z } : null;
    }
    for (const h of ray.intersectObjects(pickables, false)) {
      const u = h.object.userData, op = [].concat(h.object.material)[0].opacity;
      if (u.npc) return { kind: 'npc', npcId: u.npc };
      if (u.front) continue; // v6 : mur avant bas (coupe) : le clic passe au sol derrière
      if (u.doorId && !(h.object.isMesh && h.object.geometry.type === 'PlaneGeometry' && op < 0.5)) return { kind: 'door', doorId: u.doorId }; // porte estompée : le clic passe
      if (u.doorId) continue;
      if (op < 0.5) continue; // volume devenu transparent : le clic passe au travers
      if (u.buildingId) return u.visitable ? { kind: 'building', buildingId: u.buildingId } : { kind: 'closed', label: u.label, buildingId: u.buildingId };
      if (u.solid) return { kind: 'solid' };
      if (u.ground) return { kind: 'ground', x: h.point.x, z: h.point.z };
    }
    return null;
  }
  function project(x, y, z) { if(!game.world.editorLayers)render(); const v = new THREE.Vector3(x, y, z).project(cam), r = canvas.getBoundingClientRect(); return { x: r.left + (v.x + 1) / 2 * r.width, y: r.top + (1 - v.y) / 2 * r.height }; }
  // joue(id, cle) : planche cle (même taille et même ancre que le sprite de base, _mobile sur petit écran), jouée une fois puis retour au sprite de base
  const joueEtat = { id: null, cle: null, fini: true };
  function joue(id, cle) { const s = bsprites.find(o => o.userData.buildingId === id), m = bman[cle]; if (!s || !m) return false;
    const mob = viewW < 700 && SKIN[cle + '_mobile'], t = new THREE.Texture(SKIN[mob ? cle + '_mobile' : cle]); t.needsUpdate = true; t.colorSpace = THREE.SRGBColorSpace; t.repeat.set(1 / m.frames, 1);
    for (const u of uniques.filter(u => u.s === s)) { s.material.map = u.base; uniques.splice(uniques.indexOf(u), 1); }
    uniques.push({ s, t, base: s.material.map, n: m.frames, fps: m.fps, t0: horloge }); s.material.map = t; s.material.needsUpdate = true; Object.assign(joueEtat, { id, cle, fini: false }); return true; }
  // Update existing sprite transforms during a drag; rebuild terrain only on commit.
  function editorUpdate() {
    ({ LOCATIONS, DOORS, NPCS } = game.world);
    const loc=LOCATIONS[game.state.location];
    if (builtFor!==game.state.location || bsprites.length!==loc.buildings.length) { builtFor=null; return; }
    for(const item of bills) {
      const s=item.obj, id=s.userData.buildingId;
      if(id) {
        const b=loc.buildings.find(b=>b.id===id), m=b && bman[b.sprite];
        if(!m || s.userData.img!==b.sprite) { builtFor=null; return; }
        s.position.set(b.x+b.w+(b.ancre?.[0]||0),b.y||0,b.z+b.d+(b.ancre?.[1]||0));
        s.scale.set(m.px[0]/K*(b.k||1),m.px[1]/K*(b.k||1)*(b.sy||1),1);
        Object.assign(item,{x0:b.x,x1:b.x+b.w,z0:b.z,z1:b.z+b.d});
      } else if(s.userData.editorId) {
        const p=loc.props.find(p=>p.id===s.userData.editorId), m=p && sprites[p.furn||p.sprite];
        if(!m) { builtFor=null;return; }
        if(p.furn){const [fw,fd]=m.footprint_m.map(v=>v*(p.editorScale||1)),sw=fw*Math.abs(screenRight.x)+fd*Math.abs(screenRight.z),sh=sw*m.px[1]/m.px[0],dy=-(fw/2*camUp.x+fd/2*camUp.z);s.center.set(.5,dy/sh);s.scale.set(sw,sh,1);s.position.set(p.x+fw/2,0,p.z+fd/2);const [cw,cd]=p.fp||[fw,fd];Object.assign(item,{x0:p.x,x1:p.x+cw,z0:p.z,z1:p.z+cd});continue;}
        const h=m.height_m*Math.cos(pitch)*(p.editorScale||1), w=h*m.px[0]/m.px[1];
        s.position.set(p.x,p.y||0,p.z);s.scale.set(w,h,1);
        const [fw,fd]=p.fp || (p.solid ? [p.solid,p.solid] : m.footprint_m);
        Object.assign(item,{x0:p.x-fw/2,x1:p.x+fw/2,z0:p.z-fd/2,z1:p.z+fd/2});
      }
    }
    world.traverse(o=>{if(o.userData.propBox){const p=loc.props.find(p=>p.id===o.userData.editorId);if(p){o.geometry.dispose();o.geometry=new THREE.BoxGeometry(p.w,p.h,p.d);o.position.set(p.x+p.w/2,p.h/2,p.z+p.d/2);}}});
    for(const sp of npcSprites){const a=NPCS.find(n=>n.id===sp.userData.npc);if(!a)continue;const m=sprites[a.sprite],h=m.height_m*Math.cos(pitch)*(a.editorScale||1),w=h*m.px[0]/m.px[1];sp.position.set(a.x,0,a.z);sp.userData.w=w;sp.userData.h=h;sp.scale.set(w,h,1);}
    world.traverse(o=>{ if(o.isMesh && o.geometry.type==='RingGeometry' && o.userData.doorId) {const d=DOORS.find(d=>d.id===o.userData.doorId);if(d)o.position.set(d.threshold.x,.03,d.threshold.z);} });
  }
  function editorGround(x,y) {
    const r=canvas.getBoundingClientRect();
    ray.setFromCamera(new THREE.Vector2((x-r.left)/r.width*2-1,1-(y-r.top)/r.height*2),cam);
    const p=ray.ray.intersectPlane(new THREE.Plane(new THREE.Vector3(0,1,0),0),new THREE.Vector3());
    return p && {x:p.x,z:p.z};
  }
  return { refreshGround:()=>{if(groundMesh){groundMesh.material.map?.dispose();groundMesh.material.map=groundTexture(game.world.LOCATIONS[game.state.location],game.world.DOORS);groundMesh.material.needsUpdate=true;}}, editorUpdate, editorGround, invalidate:()=>{builtFor=null;}, editorPick:(x,y,kinds=['building','prop','actor'])=>{
      const r=canvas.getBoundingClientRect();ray.setFromCamera({x:(x-r.left)/r.width*2-1,y:1-(y-r.top)/r.height*2},cam);
      const candidates=[...bsprites,...bills.map(b=>b.obj),...pickables.filter(o=>o.userData.propBox),player,...npcSprites].filter(s=>s.visible&&kinds.includes(s.userData.buildingId?'building':s===player||s.userData.npc?'actor':'prop'));
      const hits=ray.intersectObjects([...new Set(candidates)],false).sort((a,b)=>b.object.renderOrder-a.object.renderOrder);
      for(const h of hits){const s=h.object;const img=s.userData.img|| (s===player?'player':s.userData.npc?NPCS.find(n=>n.id===s.userData.npc)?.sprite:null);if(img&&h.uv&&alphaAt(img,h.uv.x,h.uv.y)<.3)continue;
      return {id:s.userData.buildingId||s.userData.editorId};}return null;
    }, joue, joueEtat, animStats, masqueEn, camCible: () => camCible, codeAnims: () => ({ neons: neons.map(s => +s.material.opacity.toFixed(3)), fenetres: fenetres.map(s => +s.material.opacity.toFixed(3)), beams: beams.map(m => +m.rotation.y.toFixed(3)), sources: beams.map(m => m.position.toArray().map(v => +v.toFixed(2))) }), masques, render, pick, project, zoom: () => userZoom, setZoom, zoomBounds: () => [ZOOM_MIN, ZOOM_MAX], ppm: () => cam.userData.zoom || ppm * userZoom, setCamera: o => { camOverride = o; if (!o) resize(); },
    facingOf: who => { render(); const sp = who === 'player' ? player : who === 'companion' ? companion : npcSprites.find(n => n.userData.npc === who); return sp && sp.userData.facing; },
    // rectangle écran (px CSS) d'un personnage, pour les contrôles au pixel
    actorRect: who => { render(); const sp = who === 'player' ? player : who === 'companion' ? companion : npcSprites.find(n => n.userData.npc === who);
      const c = canvas.getBoundingClientRect(), p = sp.position.clone(), w = sp.userData.w, h = sp.userData.h;
      const a = p.clone().addScaledVector(screenRight, -w / 2).addScaledVector(camUp, h * 1.02), b = p.clone().addScaledVector(screenRight, w / 2).addScaledVector(camUp, -0.05);
      const P = v => { const q = v.clone().project(cam); return { x: c.left + (q.x + 1) / 2 * c.width, y: c.top + (1 - q.y) / 2 * c.height }; }; const A = P(a), B = P(b);
      return { x: Math.min(A.x, B.x), y: Math.min(A.y, B.y), w: Math.abs(B.x - A.x), h: Math.abs(B.y - A.y) }; },
    // rendu isolé d'un personnage sur fond uni (le même pipeline de rendu, rien d'autre visible)
    isolate: who => { const keep = who === 'player' ? player : who === 'companion' ? companion : npcSprites.find(n => n.userData.npc === who);
      const hidden = []; scene.traverse(o => { if ((o.isMesh || o.isSprite) && o !== keep && o.visible) { o.visible = false; hidden.push(o); } });
      const bg = scene.background; scene.background = new THREE.Color('#ff00ff'); renderer.render(scene, cam); const url = canvas.toDataURL('image/png');
      hidden.forEach(o => o.visible = true); scene.background = bg; return url; },
    isolateFurn: i => { const keep = fsprites[i]; const hidden = []; scene.traverse(o => { if ((o.isMesh || o.isSprite) && o !== keep && o.visible) { o.visible = false; hidden.push(o); } });
      const bg = scene.background, op = keep.material.opacity; keep.material.opacity = 1; scene.background = new THREE.Color('#ff00ff'); renderer.render(scene, cam); const url = canvas.toDataURL('image/png');
      hidden.forEach(o => o.visible = true); scene.background = bg; keep.material.opacity = op; return url; },
    // v7 : rendu isolé d'un bâtiment (sprite entier) pour les contrôles au pixel des quartiers
    isolateBuilding: id => { render(); const keep = bsprites.find(s => s.userData.buildingId === id); if (!keep) return null; const hidden = []; scene.traverse(o => { if ((o.isMesh || o.isSprite) && o !== keep && o.visible) { o.visible = false; hidden.push(o); } });
      const bg = scene.background, op = keep.material.opacity; keep.material.opacity = 1; scene.background = new THREE.Color('#ff00ff'); renderer.render(scene, cam); const url = canvas.toDataURL('image/png');
      hidden.forEach(o => o.visible = true); scene.background = bg; keep.material.opacity = op; return url; },
    furnCount: () => { render(); return fsprites.length; },
    leafOpacity: () => { render(); let o = null; world.traverse(m => { if (m.isMesh && m.userData.doorId && m.material.map && !exterior && m.geometry.type === 'PlaneGeometry') o = +m.material.opacity.toFixed(2); }); return o; },
    screenRightOf: (x, z) => x * screenRight.x + z * screenRight.z,
    opacityOf: id => bsprites.find(s => s.userData.buildingId === id)?.material.opacity,
    furnitureOf: () => { render(); return fsprites.map(s => ({ id: s.userData.furn, x: s.position.x, z: s.position.z, opacity: +s.material.opacity.toFixed(2), order: s.renderOrder })); },
    // contrôle au pixel : rectangle écran (px CSS) d'un meuble (index dans l'ordre de la pièce)
    furnRect: i => { render(); const s = fsprites[i], r = rectOf(s), c = canvas.getBoundingClientRect();
      const P = (x, y) => { const v = new THREE.Vector3().addScaledVector(screenRight, x).addScaledVector(camUp, y).addScaledVector(camDir, scr0(s.position)).project(cam); return { x: c.left + (v.x + 1) / 2 * c.width, y: c.top + (1 - v.y) / 2 * c.height }; };
      const A = P(r.x0, r.y1), B = P(r.x1, r.y0); return { x: A.x, y: A.y, w: B.x - A.x, h: B.y - A.y }; },
    // contrôle : alpha du sprite aux coins de l'emprise déclarée (coin avant, coin gauche, coin droit), légèrement à l'intérieur
    baseAlpha: id => { render(); const s = bsprites.find(s => s.userData.buildingId === id), b = LOCATIONS[builtFor].buildings.find(b => b.id === id);
      return [[b.x + b.w - 0.4, b.z + b.d - 0.4], [b.x + 0.4, b.z + b.d - 0.4], [b.x + b.w - 0.4, b.z + 0.4]].map(([x, z]) => { const q = uvOf(s, scr(new THREE.Vector3(x, 0.3, z))); return +alphaAt(s.userData.img, q.u, q.v).toFixed(2); }); },
    // écart (m, plan écran) entre la porte peinte sur le sprite et l'ouverture monde déclarée
    paintedDoorError: doorId => { render(); const d = DOORS.find(d => d.id === doorId), s = bsprites.find(s => s.userData.buildingId === d.buildingId), m = bman[s.userData.img];
      const r = rectOf(s), c = m.crop, u = (d.painted[0] - c[0]) / m.px[0], v = 1 - (d.painted[1] - c[1]) / m.px[1];
      const p = { x: r.x0 + u * (r.x1 - r.x0), y: r.y0 + v * (r.y1 - r.y0) }, o = scr(new THREE.Vector3(d.opening.x, 0, d.opening.z)); return +Math.hypot(p.x - o.x, p.y - o.y).toFixed(2); },
    // v13 : figurants (rôle, position monde) et rendu isolé d'un figurant, pour les contrôles au pixel (comptage à l'écran)
    decor: () => { render(); return decor.concat(drones).map((s, i) => ({ i, role: s.userData.role, x: +s.position.x.toFixed(2), z: +s.position.z.toFixed(2), facing: s.userData.facing, sprite: s.userData.sprite, ratio: +(Math.abs(s.scale.x) / s.scale.y).toFixed(3) })); },
    isolateDecor: i => { render(); const keep = decor.concat(drones)[i]; const hidden = []; scene.traverse(o => { if ((o.isMesh || o.isSprite) && o !== keep && o.visible) { o.visible = false; hidden.push(o); } });
      const bg = scene.background; scene.background = new THREE.Color('#ff00ff'); renderer.render(scene, cam); const url = canvas.toDataURL('image/png');
      hidden.forEach(o => o.visible = true); scene.background = bg; return url; },
    lightOf: () => light,
    // v13 : décor seul (personnages masqués), pour mesurer la palette d'un lieu sans les vêtements des personnages
    envShot: () => { render(); const hid = [player, companion, ...npcSprites, ...decor].filter(o => o.visible); hid.forEach(o => o.visible = false); renderer.render(scene, cam);
      const url = canvas.toDataURL('image/png'); hid.forEach(o => o.visible = true); return url; },
    ghostOf: id => { const n = npcSprites.find(s => s.userData.npc === id); return n?.userData.ghost ? { visible: n.userData.ghost.visible, opacity: n.userData.ghost.material.opacity, order: n.userData.ghost.renderOrder } : null; },
    ostCentre,
    pulses: () => pulses.map(s => ({ ...s.userData.pulse, on: !!s.userData.pulseOn, opacity: +s.material.opacity.toFixed(3) })),
    orderOf: id => id === 'player' ? player.renderOrder : bsprites.find(s => s.userData.buildingId === id)?.renderOrder };
}
