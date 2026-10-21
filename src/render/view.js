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
  scene.add(new THREE.HemisphereLight('#ffe9cf', '#4a3a2a', 1.5));
  const sun = new THREE.DirectionalLight('#ffd2a0', 1.6); sun.position.set(-12, 18, 20); scene.add(sun);
  const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 500);
  const yaw = THREE.MathUtils.degToRad(UNITS.camera.yawDeg), pitch = THREE.MathUtils.degToRad(UNITS.camera.pitchDeg);
  const camDir = new THREE.Vector3(-Math.sin(yaw) * Math.cos(pitch), -Math.sin(pitch), -Math.cos(yaw) * Math.cos(pitch)).normalize();
  const loader = new THREE.TextureLoader(), texCache = {};
  const spriteTex = id => texCache[id] ||= Object.assign(loader.load('./assets/' + (sprites[id].file || `reused/${id}.webp`)), { colorSpace: THREE.SRGBColorSpace });
  function spriteMesh(id, heightOverride) {
    const m = sprites[id], h = (heightOverride || m.height_m) * Math.cos(pitch), w = h * m.px[0] / m.px[1]; // hauteur vue par la caméra
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: spriteTex(id), alphaTest: 0.5, transparent: false }));
    s.center.set(0.5, 0.02); s.scale.set(w, h, 1); s.userData.base = sprites[id].faces || 1; s.userData.facing = 1; return s;
  }
  let world = new THREE.Group(); scene.add(world);
  let solids = [], pickables = [], labels = [], npcSprites = [], bsprites = [], bills = [], builtFor = null, exterior = false;
  const player = spriteMesh('player'), companion = spriteMesh(COMPANION.sprite);
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
  function building(b) {
    const m = bman[b.sprite]; const t = new THREE.Texture(SKIN[b.sprite]); t.needsUpdate = true; t.colorSpace = THREE.SRGBColorSpace;
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true, depthTest: false, depthWrite: false }));
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
    if (b.visitable) { addLabel(b.label, 'service', () => new THREE.Vector3(door.opening.x, 3.4, door.opening.z), () => !!game.state.discovered[b.id]); labels[labels.length - 1].el.dataset.building = b.id; }
  }
  function box(p, color) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(p.w, p.h, p.d), mat(null, color));
    m.position.set(p.x + p.w / 2, p.h / 2, p.z + p.d / 2); m.userData.targetOpacity = 1; m.userData.solid = true;
    world.add(m); solids.push(m); pickables.push(m); return m;
  }
  function build(locId) {
    scene.remove(world); world = new THREE.Group(); scene.add(world); solids = []; pickables = []; npcSprites = []; bsprites = []; bills = [];
    labels.forEach(l => l.el.remove()); labels = [];
    const loc = LOCATIONS[locId]; exterior = loc.kind === 'exterior';
    for (const a of [player, companion]) { a.material.depthTest = !exterior; a.material.transparent = exterior; }
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(loc.size.w, loc.size.d), new THREE.MeshStandardMaterial({ map: groundTexture(loc, DOORS), roughness: 1 }));
    ground.rotation.x = -Math.PI / 2; ground.position.set(loc.size.w / 2, 0, loc.size.d / 2); ground.userData.ground = true;
    world.add(ground); pickables.push(ground);
    for (const b of loc.buildings) building(b);
    for (const p of loc.props) {
      if (p.box) box(p, p.color);
      else { const s = spriteMesh(p.sprite); s.position.set(p.x, 0, p.z); world.add(s);
        if (exterior) { s.material.depthTest = false; s.material.transparent = true; const [w, d] = p.fp || sprites[p.sprite].footprint_m || [0.6, 0.6];
          bills.push({ obj: s, x0: p.x - w / 2, x1: p.x + w / 2, z0: p.z - d / 2, z1: p.z + d / 2, extra: [] }); } }
    }
    for (const w of wallsOf(loc, DOORS)) box(w, loc.wall);
    for (const d of DOORS.filter(d => d.location === locId)) {
      const o = d.opening, south = o.side === 'south';
      const g = new THREE.Group(); if (exterior) g.visible = false;
      const frame = new THREE.Mesh(new THREE.BoxGeometry(south ? UNITS.door.width + 0.16 : 0.1, UNITS.door.height + 0.08, south ? 0.1 : UNITS.door.width + 0.16), new THREE.MeshStandardMaterial({ color: '#2e2015' }));
      const leaf = new THREE.Mesh(new THREE.PlaneGeometry(UNITS.door.width, UNITS.door.height), loc.kind === 'interior' ? new THREE.MeshStandardMaterial({ color: '#d8b77a', side: THREE.DoubleSide }) : new THREE.MeshStandardMaterial({ color: '#4a3828', side: THREE.DoubleSide }));
      if (!south) leaf.rotation.y = Math.PI / 2;
      leaf.position.set(south ? 0 : 0.07, 0, south ? 0.07 : 0);
      g.add(frame, leaf); g.position.set(o.x, UNITS.door.height / 2, o.z);
      if (loc.kind === 'interior') { frame.visible = false; leaf.material.transparent = true; leaf.material.opacity = 0.55; }
      frame.userData.doorId = d.id; leaf.userData.doorId = d.id; world.add(g); if (!exterior) pickables.push(frame, leaf);
      const ring = new THREE.Mesh(new THREE.RingGeometry(0.32, 0.4, 28), new THREE.MeshBasicMaterial({ color: '#e0b04a', transparent: true, opacity: 0.7 }));
      ring.rotation.x = -Math.PI / 2; ring.renderOrder = 1; ring.position.set(d.threshold.x, 0.03, d.threshold.z); ring.userData.doorId = d.id; world.add(ring); pickables.push(ring);
      if (loc.kind === 'interior') addLabel('Sortie', 'exit', () => new THREE.Vector3(d.threshold.x, 0.2, d.threshold.z));
    }
    for (const n of NPCS.filter(n => n.location === locId)) {
      const s = spriteMesh(n.sprite); s.position.set(n.x, 0, n.z); s.userData.npc = n.id; world.add(s); pickables.push(s); npcSprites.push(s);
      addLabel(n.name, 'npc', () => new THREE.Vector3(n.x, 2.05, n.z));
    }
    builtFor = locId;
  }
  // Miroir horizontal : l'image regarde à droite de l'écran par défaut (manifest.faces = -1 sinon).
  const screenRight = new THREE.Vector3().crossVectors(camDir, new THREE.Vector3(0, 1, 0)).normalize();
  function face(s, heading) {
    if (heading == null) return; const sx = Math.sin(heading) * screenRight.x + Math.cos(heading) * screenRight.z;
    if (Math.abs(sx) > 0.2) s.userData.facing = sx > 0 ? 1 : -1; // mouvement quasi vertical à l'écran : on garde le sens précédent
    s.scale.x = Math.abs(s.scale.x) * s.userData.facing * s.userData.base;
  }
  const camUp = new THREE.Vector3().crossVectors(screenRight, camDir).normalize();
  const scr = p => ({ x: p.x * screenRight.x + p.y * screenRight.y + p.z * screenRight.z, y: p.x * camUp.x + p.y * camUp.y + p.z * camUp.z });
  function rectOf(o) { const a = scr(o.position), sx = Math.abs(o.scale.x), sy = o.scale.y; return { x0: a.x - o.center.x * sx, x1: a.x + (1 - o.center.x) * sx, y0: a.y - o.center.y * sy, y1: a.y + (1 - o.center.y) * sy }; }
  function uvOf(o, p) { const r = rectOf(o); let u = (p.x - r.x0) / (r.x1 - r.x0); if (o.scale.x < 0) u = 1 - u; return { u, v: (p.y - r.y0) / (r.y1 - r.y0) }; }
  // Ordre de dessin : A avant B si B est devant (séparés sur x ou z, le plus grand est devant, la caméra regardant vers -x et -z).
  function inFront(b, a) { if (b.x0 >= a.x1 - 1e-6 || b.z0 >= a.z1 - 1e-6) return true; if (a.x0 >= b.x1 - 1e-6 || a.z0 >= b.z1 - 1e-6) return false; return b.x0 + b.x1 + b.z0 + b.z1 > a.x0 + a.x1 + a.z0 + a.z1; }
  const actorItem = a => ({ obj: a, actor: true, x0: a.position.x - 0.3, x1: a.position.x + 0.3, z0: a.position.z - 0.3, z1: a.position.z + 0.3, extra: [] });
  function painter() {
    const items = bills.concat([player, companion].filter(a => a.visible).map(actorItem)); const n = items.length;
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
    for (const s of bsprites) { const m = s.material; m.opacity += (s.userData.targetOpacity - m.opacity) * 0.3; for (const b of bills) if (b.obj === s) for (const e of b.extra) e.material.opacity = Math.min(0.9, m.opacity); }
  }
  const ray = new THREE.Raycaster();
  function updateOcclusion() {
    for (const m of solids) m.userData.targetOpacity = 1;
    for (const a of [player, companion]) {
      if (!a.visible) continue;
      for (const hy of [0.5, 1.0, 1.6]) {
        const p = a.position.clone(); p.y = hy; ray.set(p.clone().addScaledVector(camDir, -200), camDir);
        for (const hit of ray.intersectObjects(solids, false)) if (hit.distance < 199.9) hit.object.userData.targetOpacity = 0.22;
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
  let camOverride = null;
  function render() {
    const s = game.state;
    if (builtFor !== s.location) build(s.location);
    player.position.set(s.player.x, 0, s.player.z);
    companion.visible = s.companion.mode === 'follow' && s.companion.location === s.location;
    companion.position.set(s.companion.x, 0, s.companion.z);
    face(player, s.player.heading); face(companion, s.companion.heading);
    for (const n of npcSprites) face(n, s.npcs[n.userData.npc]?.heading);
    const loc = LOCATIONS[s.location];
    const target = camOverride ? new THREE.Vector3(camOverride.x, 0, camOverride.z) : new THREE.Vector3(s.player.x, 0, s.player.z);
    if (loc.kind === 'interior' && !camOverride) target.set(loc.size.w / 2, 0, loc.size.d / 2);
    cam.position.copy(target).addScaledVector(camDir, -80); cam.lookAt(target);
    const zoom = camOverride?.ppm || (loc.kind === 'interior' ? Math.min(ppm * 1.8, innerWidth / (loc.size.w * 1.6)) : ppm);
    if (zoom !== cam.userData.zoom) { cam.userData.zoom = zoom; const w = innerWidth, h = innerHeight; cam.left = -w / 2 / zoom; cam.right = w / 2 / zoom; cam.top = h / 2 / zoom; cam.bottom = -h / 2 / zoom; cam.updateProjectionMatrix(); }
    if (false) { const w = innerWidth, h = innerHeight; cam.left = -w / 2 / camOverride.ppm; cam.right = w / 2 / camOverride.ppm; cam.top = h / 2 / camOverride.ppm; cam.bottom = -h / 2 / camOverride.ppm; cam.updateProjectionMatrix(); }
    if (exterior) { painter(); spriteOcclusion(); } else updateOcclusion();
    renderer.render(scene, cam);
    const r = canvas.getBoundingClientRect();
    for (const l of labels) { const vis = !l.visible || l.visible(); l.el.hidden = !vis; if (!vis) continue; const v = l.getPos().clone().project(cam); l.el.style.transform = `translate(-50%,-100%) translate(${r.left + (v.x + 1) / 2 * r.width}px,${r.top + (1 - v.y) / 2 * r.height}px)`; }
  }
  function pick(clientX, clientY) {
    render();
    const r = canvas.getBoundingClientRect();
    ray.setFromCamera(new THREE.Vector2(((clientX - r.left) / r.width) * 2 - 1, -((clientY - r.top) / r.height) * 2 + 1), cam);
    if (exterior) { // sprites : pixel opaque le plus haut dans l'ordre du peintre ; un bâtiment transparent laisse passer le clic
      const hits = ray.intersectObjects(pickables, false), ring = hits.find(h => h.object.userData.doorId); if (ring) return { kind: 'door', doorId: ring.object.userData.doorId };
      const c = scr(ray.ray.origin); let top = null;
      for (const s of bsprites) { if (s.material.opacity < 0.5) continue; const q = uvOf(s, c); if (alphaAt(s.userData.img, q.u, q.v) > 0.5 && (!top || s.renderOrder > top.renderOrder)) top = s; }
      if (top) { const u = top.userData;
        if (!u.visitable) { // clic sur un bâtiment fermé : si le sol visé est hors de son emprise (rue cachée derrière), on marche
          const g = hits.find(h => h.object.userData.ground), b = LOCATIONS[builtFor].buildings.find(b => b.id === u.buildingId);
          if (g && (g.point.x < b.x - 1 || g.point.x > b.x + b.w + 1 || g.point.z < b.z - 1 || g.point.z > b.z + b.d + 1)) return { kind: 'ground', x: g.point.x, z: g.point.z };
          return { kind: 'closed', label: u.label }; }
        const ds = DOORS.filter(d => d.buildingId === u.buildingId).map(d => ({ d, p: scr(new THREE.Vector3(d.opening.x, 1, d.opening.z)) }));
        ds.sort((a, b) => Math.hypot(a.p.x - c.x, a.p.y - c.y) - Math.hypot(b.p.x - c.x, b.p.y - c.y)); return { kind: 'door', doorId: ds[0].d.id }; }
      const g = hits.find(h => h.object.userData.ground); return g ? { kind: 'ground', x: g.point.x, z: g.point.z } : null;
    }
    for (const h of ray.intersectObjects(pickables, false)) {
      const u = h.object.userData, op = [].concat(h.object.material)[0].opacity;
      if (u.npc) return { kind: 'npc', npcId: u.npc };
      if (u.doorId) return { kind: 'door', doorId: u.doorId };
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
    screenRightOf: (x, z) => x * screenRight.x + z * screenRight.z,
    opacityOf: id => bsprites.find(s => s.userData.buildingId === id)?.material.opacity,
    // contrôle : alpha du sprite aux coins de l'emprise déclarée (coin avant, coin gauche, coin droit), légèrement à l'intérieur
    baseAlpha: id => { render(); const s = bsprites.find(s => s.userData.buildingId === id), b = LOCATIONS[builtFor].buildings.find(b => b.id === id);
      return [[b.x + b.w - 0.4, b.z + b.d - 0.4], [b.x + 0.4, b.z + b.d - 0.4], [b.x + b.w - 0.4, b.z + 0.4]].map(([x, z]) => { const q = uvOf(s, scr(new THREE.Vector3(x, 0.3, z))); return +alphaAt(s.userData.img, q.u, q.v).toFixed(2); }); },
    // écart (m, plan écran) entre la porte peinte sur le sprite et l'ouverture monde déclarée
    paintedDoorError: doorId => { render(); const d = DOORS.find(d => d.id === doorId), s = bsprites.find(s => s.userData.buildingId === d.buildingId), m = bman[s.userData.img];
      const r = rectOf(s), c = m.crop, u = (d.painted[0] - c[0]) / m.px[0], v = 1 - (d.painted[1] - c[1]) / m.px[1];
      const p = { x: r.x0 + u * (r.x1 - r.x0), y: r.y0 + v * (r.y1 - r.y0) }, o = scr(new THREE.Vector3(d.opening.x, 0, d.opening.z)); return +Math.hypot(p.x - o.x, p.y - o.y).toFixed(2); },
    orderOf: id => id === 'player' ? player.renderOrder : bsprites.find(s => s.userData.buildingId === id)?.renderOrder };
}
