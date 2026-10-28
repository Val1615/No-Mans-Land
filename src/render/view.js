import * as THREE from 'three';
import { UNITS } from '../data/units.js';
import { wallsOf } from '../core/grid.js';
import { groundTexture, SKIN } from './textures.js';

export function createView(canvas, game, sprites, bman, labelLayer) {
  const { LOCATIONS, DOORS, NPCS, COMPANION } = game.world;
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
  // Personnages : texture propre à chaque sprite, car le miroir se fait par les UV (repeat.x = -1).
  // THREE.Sprite ignore le signe de scale.x (le shader prend la longueur de la colonne de la matrice) : c'était la cause du miroir invisible.
  const actorTex = id => { const t = loader.load('./assets/' + (sprites[id].file || `reused/${id}.webp`)); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = THREE.RepeatWrapping; return t; };
  function spriteMesh(id, heightOverride, actor = false) {
    const m = sprites[id], h = (heightOverride || m.height_m) * Math.cos(pitch), w = h * m.px[0] / m.px[1]; // hauteur vue par la caméra
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: actor ? actorTex(id) : spriteTex(id), alphaTest: 0.5, transparent: false }));
    s.center.set(0.5, 0.02); s.scale.set(w, h, 1); Object.assign(s.userData, { base: sprites[id].faces || 1, facing: 1, shown: 1, w, h, turn: 1, phase: Math.random() * 6.28 }); return s;
  }
  let world = new THREE.Group(); scene.add(world);
  let solids = [], pickables = [], labels = [], npcSprites = [], bsprites = [], fsprites = [], bills = [], builtFor = null, exterior = false;
  let decor = [], walkers = [], drones = [], flick = [], light = null; // v13 : figurants (file, soldats, passants), drones, néons/hologrammes
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
    const m = bman[b.sprite]; const t = new THREE.Texture(SKIN[b.sprite]); t.needsUpdate = true; t.colorSpace = THREE.SRGBColorSpace;
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true, depthTest: false, depthWrite: false, color: b.tint || light?.tint || '#ffffff' }));
    s.center.set(m.anchor[0] / m.px[0], 1 - m.anchor[1] / m.px[1]); s.scale.set(m.px[0] / K, m.px[1] / K, 1);
    s.position.set(b.x + b.w, 0, b.z + b.d);
    Object.assign(s.userData, { buildingId: b.id, visitable: b.visitable, label: b.label, img: b.sprite, targetOpacity: 1 });
    world.add(s); bsprites.push(s);
    const item = { obj: s, x0: b.x, x1: b.x + b.w, z0: b.z, z1: b.z + b.d, extra: [] }; bills.push(item);
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
    const m = sprites[p.furn], [w, d] = m.footprint_m;
    const sw = w * Math.abs(screenRight.x) + d * Math.abs(screenRight.z), sh = sw * m.px[1] / m.px[0];
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: spriteTex(p.furn), transparent: true, alphaTest: 0.3, depthTest: false, depthWrite: false }));
    const dyFront = -(w / 2 * camUp.x + d / 2 * camUp.z); // le coin avant est plus bas à l'écran que le centre
    s.center.set(0.5, dyFront / sh); s.scale.set(sw, sh, 1); s.position.set(p.x + w / 2, 0, p.z + d / 2);
    Object.assign(s.userData, { furn: p.furn, img: p.furn, targetOpacity: 1 });
    world.add(s); fsprites.push(s); bills.push({ obj: s, x0: p.x, x1: p.x + w, z0: p.z, z1: p.z + d, extra: [] });
  }
  function box(p, color, skin) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(p.w, p.h, p.d), (skin && wallMats(p, skin)) || mat(null, color));
    m.position.set(p.x + p.w / 2, p.h / 2, p.z + p.d / 2); m.userData.targetOpacity = 1; m.userData.solid = true;
    world.add(m); solids.push(m); pickables.push(m); return m;
  }
  function build(locId) {
    scene.remove(world); world = new THREE.Group(); scene.add(world); solids = []; pickables = []; npcSprites = []; bsprites = []; phOf.length = 0; fsprites = []; bills = [];
    labels.forEach(l => l.el.remove()); labels = [];
    const loc = LOCATIONS[locId]; exterior = loc.kind === 'exterior'; light = applyLight(loc.light); decor = []; walkers = []; drones = []; flick = [];
    for (const a of [player, companion]) { a.material.depthTest = false; a.material.transparent = true; } // v6 : intérieur aussi trié par l'ordre du peintre
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(loc.size.w, loc.size.d), new THREE.MeshStandardMaterial({ map: groundTexture(loc, DOORS), roughness: 1 }));
    ground.rotation.x = -Math.PI / 2; ground.position.set(loc.size.w / 2, 0, loc.size.d / 2); ground.userData.ground = true; groundMesh = ground;
    world.add(ground); pickables.push(ground);
    for (const b of loc.buildings) building(b);
    for (const p of loc.props) {
      if (p.furn) furniture(p);
      else if (p.box) box(p, p.color);
      else { const s = spriteMesh(p.sprite); s.position.set(p.x, p.y || 0, p.z); world.add(s);
        if (p.tint || light.tint) s.material.color.set(p.tint || light.tint);
        if (p.glow) { s.material.blending = THREE.AdditiveBlending; s.material.opacity = p.glow; flick.push({ m: s.material, base: p.glow, ph: Math.random() * 6 }); } // hologramme : additif, scintille
        if (p.flip) { s.material.map = actorTex(p.sprite); s.material.map.repeat.x = -1; s.material.map.offset.x = 1; }
        if (exterior) { s.material.depthTest = false; s.material.transparent = true; const [w, d] = p.fp || sprites[p.sprite].footprint_m || [0.6, 0.6];
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
        addLabel(d.label, d.junction ? 'junction' : 'edge', () => new THREE.Vector3(d.opening.x - (d.threshold.x - d.opening.x) * 1.6, 0, d.opening.z - (d.threshold.z - d.opening.z) * 1.6)); labels[labels.length - 1].el.dataset.door = d.id; } // étiquette hors carte : ne cache jamais le joueur au seuil
      if (loc.kind === 'interior') addLabel(d.label || 'Sortie', 'exit', () => new THREE.Vector3(d.opening.x, UNITS.door.height + 0.35, d.opening.z)); // v6 : au-dessus de la porte, plus sur le seuil (cachait le joueur à l'arrivée)
    }
    // v13 : lumières au sol (néons reflétés sur la chaussée mouillée, pinceaux des projecteurs) : disques additifs étirés
    for (const g of loc.glows || []) { const m = new THREE.Mesh(new THREE.PlaneGeometry(g.rx * 2, g.rz * 2), new THREE.MeshBasicMaterial({ map: glowTex(), color: g.color, transparent: true, opacity: g.i ?? 0.6, blending: THREE.AdditiveBlending, depthWrite: false, depthTest: false }));
      m.rotation.x = -Math.PI / 2; m.position.set(g.x, 0.02, g.z); m.renderOrder = 2; world.add(m); if (g.flicker) flick.push({ m: m.material, base: g.i ?? 0.6, ph: Math.random() * 6 }); }
    // v13 : figurants immobiles (file d'attente, soldats) et passants qui marchent : mêmes sprites animés que les PNJ, sans dialogue
    for (const e of loc.extras || []) { const s = spriteMesh(e.sprite, e.h || null, true); s.position.set(e.x, 0, e.z); s.material.depthTest = false; s.material.transparent = true;
      if (light.actor) s.material.color.set(light.actor); s.userData.facing = e.face || 1; s.userData.role = e.role; world.add(s); decor.push(s); }
    for (const w of loc.walkers || []) { const s = spriteMesh(w.sprite, null, true); s.material.depthTest = false; s.material.transparent = true; if (light.actor) s.material.color.set(light.actor);
      s.userData.role = 'passant'; s.userData.route = w.path; s.userData.speed = w.speed || 1.1; s.userData.t = w.t0 || 0; world.add(s); decor.push(s); walkers.push(s); }
    for (const d of loc.drones || []) { const s = spriteMesh('st_drone'); s.material.depthTest = false; s.material.transparent = true; s.userData.role = 'drone'; s.userData.orbit = d; world.add(s); drones.push(s); }
    for (const n of NPCS.filter(n => n.location === locId)) {
      const s = spriteMesh(n.sprite, null, true); if (light.actor) s.material.color.set(light.actor); s.position.set(n.x, 0, n.z); s.userData.npc = n.id; s.material.depthTest = false; s.material.transparent = true; world.add(s); pickables.push(s); npcSprites.push(s);
      addLabel(n.name, 'npc', () => new THREE.Vector3(n.x, 2.05, n.z));
    }
    builtFor = locId;
  }
  let glowT = null;
  function glowTex() { if (glowT) return glowT; const c = document.createElement('canvas'); c.width = c.height = 128; const x = c.getContext('2d'), g = x.createRadialGradient(64, 64, 0, 64, 64, 64);
    g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(0.35, 'rgba(255,255,255,.45)'); g.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = g; x.fillRect(0, 0, 128, 128); return glowT = new THREE.CanvasTexture(c); }
  // v13 : passants le long d'une boucle de points (vitesse m/s), drones en orbite au-dessus de la rue, néons qui scintillent
  function ambient(dt, t) {
    for (const s of walkers) { const u = s.userData, P = u.route, seg = []; let L = 0;
      for (let i = 0; i < P.length; i++) { const a = P[i], b = P[(i + 1) % P.length], l = Math.hypot(b[0] - a[0], b[1] - a[1]); seg.push([a, b, l]); L += l; }
      u.t = (u.t + dt * u.speed) % L; let r = u.t;
      for (const [a, b, l] of seg) { if (r <= l) { const k = r / l; s.position.set(a[0] + (b[0] - a[0]) * k, 0, a[1] + (b[1] - a[1]) * k); face(s, Math.atan2(b[0] - a[0], b[1] - a[1])); break; } r -= l; }
      animate(s, true, dt, t); }
    for (const s of decor) if (!walkers.includes(s)) animate(s, false, dt, t);
    for (const s of drones) { const o = s.userData.orbit, a = t * (o.speed || 0.25) + (o.ph || 0); s.position.set(o.x + Math.cos(a) * o.r, (o.y || 5) + Math.sin(t * 2.1 + (o.ph || 0)) * 0.15, o.z + Math.sin(a) * o.r * 0.6); }
    for (const f of flick) f.m.opacity = f.base * (0.82 + 0.18 * Math.sin(t * 7 + f.ph) * Math.sin(t * 2.3 + f.ph * 2)); }
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
  // Ordre de dessin : A avant B si B est devant (séparés sur x ou z, le plus grand est devant, la caméra regardant vers -x et -z).
  function inFront(b, a) { if (b.x0 >= a.x1 - 1e-6 || b.z0 >= a.z1 - 1e-6) return true; if (a.x0 >= b.x1 - 1e-6 || a.z0 >= b.z1 - 1e-6) return false; return b.x0 + b.x1 + b.z0 + b.z1 > a.x0 + a.x1 + a.z0 + a.z1; }
  const actorItem = a => ({ obj: a, actor: true, x0: a.position.x - 0.3, x1: a.position.x + 0.3, z0: a.position.z - 0.3, z1: a.position.z + 0.3, extra: [] });
  function painter() {
    const items = bills.concat([player, companion].filter(a => a.visible).concat(npcSprites, decor, drones).map(actorItem)); const n = items.length;
    const R = items.map(i => rectOf(i.obj)), indeg = new Array(n).fill(0), out = items.map(() => []);
    for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
      const a = R[i], b = R[j]; if (a.x1 < b.x0 || b.x1 < a.x0 || a.y1 < b.y0 || b.y1 < a.y0) continue; // pas de recouvrement à l'écran
      if (inFront(items[j], items[i])) { out[i].push(j); indeg[j]++; } else { out[j].push(i); indeg[i]++; }
    }
    const key = i => items[i].x0 + items[i].x1 + items[i].z0 + items[i].z1, done = new Array(n).fill(false); let ord = 10;
    for (let k = 0; k < n; k++) {
      let best = -1; for (let i = 0; i < n; i++) if (!done[i] && indeg[i] === 0 && (best < 0 || key(i) < key(best))) best = i;
      if (best < 0) for (let i = 0; i < n; i++) if (!done[i] && (best < 0 || key(i) < key(best))) best = i; // cycle : repli sur la clé
      done[best] = true; for (const j of out[best]) indeg[j]--;
      items[best].obj.renderOrder = ord; for (const e of items[best].extra) e.renderOrder = ord + 1; ord += 2;
    }
    return items;
  }
  // Règle d'occultation : un bâtiment passe à 30 % d'opacité quand un acteur est derrière lui (ordre du peintre)
  // et qu'un point du corps de l'acteur (0,3 à 1,5 m) tombe sur un pixel opaque du sprite.
  function spriteOcclusion() {
    for (const s of bsprites) s.userData.targetOpacity = 1;
    for (const a of [player, companion]) { if (!a.visible) continue; const ai = actorItem(a);
      for (const s of bsprites) { const bi = bills.find(b => b.obj === s); if (!inFront(bi, ai)) continue;
        for (const hy of [0.3, 0.9, 1.5]) { const q = uvOf(s, scr(new THREE.Vector3(a.position.x, hy, a.position.z))); if (alphaAt(s.userData.img, q.u, q.v) > 0.3) { s.userData.targetOpacity = 0.3; break; } } } }
    for (const o of phOf) { o.userData.targetOpacity = 1; const bi = bills.find(b => b.obj === o), r = rectOf(o);
      for (const a of [player, companion]) { if (!a.visible || !inFront(bi, actorItem(a))) continue; const q = scr(new THREE.Vector3(a.position.x, 0.9, a.position.z));
        if (q.x > r.x0 && q.x < r.x1 && q.y > r.y0 && q.y < r.y1) o.userData.targetOpacity = 0.3; }
      const m = o.material; m.opacity += (o.userData.targetOpacity - m.opacity) * 0.3; for (const e of bi.extra) e.material.opacity = m.opacity; }
    for (const s of bsprites) { const m = s.material; m.opacity += (s.userData.targetOpacity - m.opacity) * 0.3; for (const b of bills) if (b.obj === s) for (const e of b.extra) e.material.opacity = Math.min(0.9, m.opacity); }
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
  let ppm = 30;
  function resize() {
    const w = innerWidth, h = innerHeight; renderer.setSize(w, h, false);
    ppm = w < 700 ? UNITS.camera.pxPerMeterMobile : UNITS.camera.pxPerMeterDesktop;
    cam.userData.zoom = null;
  }
  addEventListener('resize', resize); resize();
  let camOverride = null, camShift = 0;
  let groundMesh = null, cbt = null; // combat C1 : grille, cases atteignables, chemin, unités ennemies
  function render() {
    const s = game.state;
    if (builtFor !== s.location) build(s.location);
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
    // mobile : quand le dialogue est ouvert, le cadre remonte pour garder joueur et PNJ visibles au-dessus du panneau
    const dlg = document.getElementById('dialogue');
    let wantShift = 0;
    if (!camOverride && innerWidth <= 600 && dlg && !dlg.hidden && dlg.offsetHeight) {
      const top = dlg.getBoundingClientRect().top;
      wantShift = Math.max(0, innerHeight / 2 - top / 2 - 20);
      if (loc.kind === 'interior') target.set((target.x + s.player.x) / 2, 0, (target.z + s.player.z) / 2);
    }
    camShift += (wantShift - camShift) * Math.min(1, dt * 8); if (Math.abs(wantShift - camShift) < 0.5) camShift = wantShift;
    cam.position.copy(target).addScaledVector(camDir, -80); cam.lookAt(target);
    const zoom = camOverride?.ppm || (loc.kind === 'interior' ? Math.min(ppm * 1.8, innerWidth / (loc.size.w * 1.6)) : ppm);
    if (zoom !== cam.userData.zoom || camShift !== cam.userData.shift) { cam.userData.shift = camShift; cam.userData.zoom = zoom; const w = innerWidth, h = innerHeight; cam.left = -w / 2 / zoom; cam.right = w / 2 / zoom; cam.top = (h / 2 - camShift) / zoom; cam.bottom = (-h / 2 - camShift) / zoom; cam.updateProjectionMatrix(); }
    if (false) { const w = innerWidth, h = innerHeight; cam.left = -w / 2 / camOverride.ppm; cam.right = w / 2 / camOverride.ppm; cam.top = h / 2 / camOverride.ppm; cam.bottom = -h / 2 / camOverride.ppm; cam.updateProjectionMatrix(); }
    if (exterior) { painter(); spriteOcclusion(); } else { painter(); furnitureOcclusion(); updateOcclusion(); }
    combatOverlay();
    renderer.render(scene, cam);
    const r = canvas.getBoundingClientRect();
    const placed = []; // étiquettes : bornées à l'écran, puis décalées vers le haut si elles se chevauchent (mobile étroit)
    for (const l of labels) { const vis = !l.visible || l.visible(); l.el.hidden = !vis; if (!vis) continue; const v = l.getPos().clone().project(cam); const lw = l.el.offsetWidth || 0, lh = l.el.offsetHeight || 0; let lx = r.left + (v.x + 1) / 2 * r.width; if (lw && lw + 8 < innerWidth) lx = Math.min(innerWidth - 4 - lw / 2, Math.max(4 + lw / 2, lx)); placed.push({ l, lx, ly: r.top + (1 - v.y) / 2 * r.height, lw, lh }); }
    const hudRects = ['hud', 'locbox', 'obj', 'msg', 'dialogue', 'panel', 'keys', 'act', 'mini'].map(id => document.getElementById(id))
      .filter(e => e && !e.hidden && e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden').flatMap(e => e.id === 'keys' ? [...e.children].filter(c => c.getClientRects().length) : [e])
      .map(e => e.getBoundingClientRect()).filter(q => q.width > 0 && q.height > 0);
    placed.sort((a, b) => b.ly - a.ly);
    for (let i = 0; i < placed.length; i++) { const a = placed[i]; for (let pass = 0; pass < 4; pass++) { let moved = false; for (let j = 0; j < i; j++) { const b = placed[j]; if (Math.abs(a.lx - b.lx) < (a.lw + b.lw) / 2 + 2 && a.ly > b.ly - b.lh - 2 && a.ly - a.lh < b.ly + 2) { a.ly = b.ly - b.lh - 3; moved = true; } } if (!moved) break; } a.l.el.style.transform = `translate(-50%,-100%) translate(${a.lx}px,${a.ly}px)`;
      // un libellé qui passe sous un panneau d'interface (HUD, lieu, OBJECTIF, message, dialogue, panneau, boutons) est masqué, jamais coupé
      const L = a.lx - a.lw / 2, R = a.lx + a.lw / 2, T = a.ly - a.lh, Bt = a.ly, under = hudRects.some(q => L < q.right && R > q.left && T < q.bottom && Bt > q.top);
      a.l.el.style.visibility = under ? 'hidden' : ''; a.l.el.dataset.underHud = under ? '1' : ''; }
  }
  // ---------- Combat C1 : grille de 1 m semi-transparente (seulement en combat), cases atteignables, aperçu du chemin et coût ----------
  function combatOverlay() {
    const c = game.state.combat;
    if (!c) { if (cbt) { scene.remove(cbt.group); for (const e of cbt.enemies) { world.remove(e); npcSprites.splice(npcSprites.indexOf(e), 1); } cbt.cost.remove(); cbt = null; } return; }
    if (!cbt || cbt.id !== c) { if (cbt) { scene.remove(cbt.group); cbt.cost.remove(); }
      const group = new THREE.Group(); scene.add(group); const z = c.zone, pts = [];
      for (let i = z.i0; i <= z.i1; i++) for (let j = z.j0; j <= z.j1; j++) if (game.combat.cellFree(i, j)) pts.push(i, 0.03, j, i + 1, 0.03, j, i, 0.03, j, i, 0.03, j + 1, i + 1, 0.03, j, i + 1, 0.03, j + 1, i, 0.03, j + 1, i + 1, 0.03, j + 1);
      const gg = new THREE.BufferGeometry(); gg.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
      const lines = new THREE.LineSegments(gg, new THREE.LineBasicMaterial({ color: '#f2b44a', transparent: true, opacity: 0.16, depthTest: false, depthWrite: false })); lines.renderOrder = 3; group.add(lines);
      const mk = (col, op) => new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: op, depthTest: false, depthWrite: false });
      const reach = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.92, 0.92).rotateX(-Math.PI / 2), mk('#f2b44a', 0.10), (2 * z.i1 - 2 * z.i0 + 3) ** 2); reach.renderOrder = 3; group.add(reach);
      const exitM = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.92, 0.92).rotateX(-Math.PI / 2), mk('#b8d0a0', 0.10), 4 * (z.i1 - z.i0 + 1)); exitM.renderOrder = 3; group.add(exitM);
      let ne = 0; const m4 = new THREE.Matrix4(); for (let i = z.i0; i <= z.i1; i++) for (let j = z.j0; j <= z.j1; j++) if ((i === z.i0 || i === z.i1 || j === z.j0 || j === z.j1) && game.combat.cellFree(i, j)) exitM.setMatrixAt(ne++, m4.makeTranslation(i + 0.5, 0.035, j + 0.5)); exitM.count = ne;
      const pathL = new THREE.Line(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({ color: '#ffe2a8', transparent: true, opacity: 0.85, depthTest: false, depthWrite: false })); pathL.renderOrder = 4; group.add(pathL);
      const tgt = new THREE.Mesh(new THREE.RingGeometry(0.28, 0.4, 24).rotateX(-Math.PI / 2), mk('#ffe2a8', 0.8)); tgt.renderOrder = 4; group.add(tgt);
      const cost = document.createElement('div'); cost.className = 'wlabel cbt-cost'; labelLayer.appendChild(cost);
      const enemies = c.units.filter(u => !u.joueur).map(u => { const sp = spriteMesh(u.sprite, null, true); sp.material.depthTest = false; sp.material.transparent = true; sp.userData.unit = u.id; world.add(sp); npcSprites.push(sp); return sp; });
      cbt = { id: c, group, reach, pathL, tgt, cost, enemies, key: '' }; }
    for (const e of cbt.enemies) { const u = c.units.find(q => q.id === e.userData.unit); e.visible = u.actif; e.position.set(u.x, 0, u.z); if (u.heading !== undefined) face(e, u.heading); }
    const pl = c.units.find(u => u.joueur), mine = c.phase === 'joueur' && c.units[c.actif] === pl && !pl.path.length, pv = c.preview;
    const key = JSON.stringify([mine, pl.i, pl.j, pl.pa, pv && [pv.i, pv.j, pv.pa, pv.ok], c.units.map(u => [u.i, u.j, u.actif])]);
    if (key !== cbt.key) { cbt.key = key; const m4 = new THREE.Matrix4(); let n = 0;
      if (mine) for (const q of game.combat.reachable()) if (q.i !== pl.i || q.j !== pl.j) cbt.reach.setMatrixAt(n++, m4.makeTranslation(q.i + 0.5, 0.04, q.j + 0.5));
      cbt.reach.count = n; cbt.reach.instanceMatrix.needsUpdate = true;
      const showPv = mine && pv && pv.cells.length > 1; cbt.pathL.visible = cbt.tgt.visible = !!(mine && pv);
      cbt.pathL.geometry.setFromPoints(showPv ? pv.cells.map(([a, b]) => new THREE.Vector3(a + 0.5, 0.05, b + 0.5)) : []);
      if (mine && pv) { cbt.tgt.position.set(pv.i + 0.5, 0.05, pv.j + 0.5); cbt.tgt.material.color.set(pv.ok ? '#ffe2a8' : '#d06050'); cbt.pathL.material.color.set(pv.ok ? '#ffe2a8' : '#d06050'); }
      cbt.cost.textContent = mine && pv ? (pv.pa != null ? `${pv.pa} PA` : '\u00d7') : ''; cbt.cost.hidden = !(mine && pv); }
    if (mine && pv) { const v = new THREE.Vector3(pv.i + 0.5, 0.6, pv.j + 0.5).project(cam), r = canvas.getBoundingClientRect();
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
        if (!u.visitable) { // clic sur un bâtiment fermé : si le sol visé est hors de son emprise (rue cachée derrière), on marche
          const g = hits.find(h => h.object.userData.ground), b = LOCATIONS[builtFor].buildings.find(b => b.id === u.buildingId);
          if (g && (g.point.x < b.x - 1 || g.point.x > b.x + b.w + 1 || g.point.z < b.z - 1 || g.point.z > b.z + b.d + 1)) return { kind: 'ground', x: g.point.x, z: g.point.z };
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
      if (u.buildingId) return u.visitable ? { kind: 'building', buildingId: u.buildingId } : { kind: 'closed', label: u.label };
      if (u.solid) return { kind: 'solid' };
      if (u.ground) return { kind: 'ground', x: h.point.x, z: h.point.z };
    }
    return null;
  }
  function project(x, y, z) { render(); const v = new THREE.Vector3(x, y, z).project(cam), r = canvas.getBoundingClientRect(); return { x: r.left + (v.x + 1) / 2 * r.width, y: r.top + (1 - v.y) / 2 * r.height }; }
  return { render, pick, project, setCamera: o => { camOverride = o; if (!o) resize(); },
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
    decor: () => { render(); return decor.concat(drones).map((s, i) => ({ i, role: s.userData.role, x: +s.position.x.toFixed(2), z: +s.position.z.toFixed(2), facing: s.userData.facing })); },
    isolateDecor: i => { render(); const keep = decor.concat(drones)[i]; const hidden = []; scene.traverse(o => { if ((o.isMesh || o.isSprite) && o !== keep && o.visible) { o.visible = false; hidden.push(o); } });
      const bg = scene.background; scene.background = new THREE.Color('#ff00ff'); renderer.render(scene, cam); const url = canvas.toDataURL('image/png');
      hidden.forEach(o => o.visible = true); scene.background = bg; return url; },
    lightOf: () => light,
    // v13 : décor seul (personnages masqués), pour mesurer la palette d'un lieu sans les vêtements des personnages
    envShot: () => { render(); const hid = [player, companion, ...npcSprites, ...decor].filter(o => o.visible); hid.forEach(o => o.visible = false); renderer.render(scene, cam);
      const url = canvas.toDataURL('image/png'); hid.forEach(o => o.visible = true); return url; },
    orderOf: id => id === 'player' ? player.renderOrder : bsprites.find(s => s.userData.buildingId === id)?.renderOrder };
}
