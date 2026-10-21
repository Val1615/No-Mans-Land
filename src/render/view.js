import * as THREE from 'three';
import { UNITS } from '../data/units.js';
import { wallsOf } from '../core/grid.js';
import { facadeTexture, roofTexture, groundTexture, hiddenDoorTexture } from './textures.js';

export function createView(canvas, game, sprites, labelLayer) {
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
  const spriteTex = id => texCache[id] ||= Object.assign(loader.load(`./assets/reused/${id}.webp`), { colorSpace: THREE.SRGBColorSpace });
  function spriteMesh(id, heightOverride) {
    const m = sprites[id], h = heightOverride || m.height_m, w = h * m.px[0] / m.px[1];
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: spriteTex(id), alphaTest: 0.5, transparent: false }));
    s.center.set(0.5, 0.02); s.scale.set(w, h, 1); return s;
  }
  let world = new THREE.Group(); scene.add(world);
  let solids = [], pickables = [], labels = [], npcSprites = [], builtFor = null;
  const player = spriteMesh('player'), companion = spriteMesh(COMPANION.sprite);
  player.userData.actor = 'player'; scene.add(player, companion);

  function mat(map, color) { return new THREE.MeshStandardMaterial({ map, color: map ? '#ffffff' : color, transparent: true, opacity: 1, roughness: 0.95 }); }
  function addLabel(text, cls, getPos, visible) { const el = document.createElement('div'); el.className = 'wlabel ' + cls; el.textContent = text; labelLayer.appendChild(el); labels.push({ el, getPos, visible }); }
  function building(b) {
    const h = b.height ?? b.storeys * UNITS.storey;
    const door = DOORS.find(d => d.buildingId === b.id);
    const southDoorX = door?.opening.side === 'south' ? door.opening.x - b.x : (!door && b.door && b.door !== 'none' && b.door !== 'garage-east') ? b.w / 2 : null;
    const eastDoorX = door?.opening.side === 'east' ? (b.z + b.d) - door.opening.z : null;
    const paint = b.visitable ? null : (b.door === 'none' ? null : b.door);
    const mats = [
      mat(facadeTexture(b, b.d, h, { face: 'e', doorX: eastDoorX, cue: eastDoorX != null ? b.cue : null })),
      mat(facadeTexture(b, b.d, h, { face: 'w', doorX: null })),
      mat(roofTexture(b, b.w, b.d)), mat(null, '#000'),
      mat(facadeTexture(b, b.w, h, { face: 's', doorX: southDoorX, paintDoor: paint, cue: southDoorX != null && b.visitable ? b.cue : null })),
      mat(facadeTexture(b, b.w, h, { face: 'n', doorX: null }))];
    const m = new THREE.Mesh(new THREE.BoxGeometry(b.w, h, b.d), mats);
    m.position.set(b.x + b.w / 2, h / 2, b.z + b.d / 2);
    Object.assign(m.userData, { buildingId: b.id, visitable: b.visitable, label: b.label, targetOpacity: 1 });
    world.add(m); solids.push(m); pickables.push(m);
    if (b.visitable) { const el = addLabel(b.label, 'service', () => door ? new THREE.Vector3(door.opening.x, Math.min(h, 3) + 0.9, door.opening.z) : m.position, () => !!game.state.discovered[b.id]); labels[labels.length - 1].el.dataset.building = b.id; }
  }
  function box(p, color) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(p.w, p.h, p.d), mat(null, color));
    m.position.set(p.x + p.w / 2, p.h / 2, p.z + p.d / 2); m.userData.targetOpacity = 1; m.userData.solid = true;
    world.add(m); solids.push(m); pickables.push(m); return m;
  }
  function build(locId) {
    scene.remove(world); world = new THREE.Group(); scene.add(world); solids = []; pickables = []; npcSprites = [];
    labels.forEach(l => l.el.remove()); labels = [];
    const loc = LOCATIONS[locId];
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(loc.size.w, loc.size.d), new THREE.MeshStandardMaterial({ map: groundTexture(loc, DOORS), roughness: 1 }));
    ground.rotation.x = -Math.PI / 2; ground.position.set(loc.size.w / 2, 0, loc.size.d / 2); ground.userData.ground = true;
    world.add(ground); pickables.push(ground);
    for (const b of loc.buildings) building(b);
    for (const p of loc.props) {
      if (p.box) box(p, p.color);
      else { const s = spriteMesh(p.sprite); s.position.set(p.x, 0, p.z); world.add(s); }
    }
    for (const w of wallsOf(loc, DOORS)) box(w, loc.wall);
    for (const d of DOORS.filter(d => d.location === locId)) {
      const o = d.opening, south = o.side === 'south';
      const g = new THREE.Group();
      const frame = new THREE.Mesh(new THREE.BoxGeometry(south ? UNITS.door.width + 0.16 : 0.1, UNITS.door.height + 0.08, south ? 0.1 : UNITS.door.width + 0.16), new THREE.MeshStandardMaterial({ color: '#2e2015' }));
      const leaf = new THREE.Mesh(new THREE.PlaneGeometry(UNITS.door.width, UNITS.door.height), loc.kind === 'interior' ? new THREE.MeshStandardMaterial({ color: '#d8b77a', side: THREE.DoubleSide }) : new THREE.MeshStandardMaterial({ map: hiddenDoorTexture(), side: THREE.DoubleSide }));
      if (!south) leaf.rotation.y = Math.PI / 2;
      leaf.position.set(south ? 0 : 0.07, 0, south ? 0.07 : 0);
      g.add(frame, leaf); g.position.set(o.x, UNITS.door.height / 2, o.z);
      if (loc.kind === 'interior') { frame.visible = false; leaf.material.transparent = true; leaf.material.opacity = 0.55; }
      frame.userData.doorId = d.id; leaf.userData.doorId = d.id; world.add(g); pickables.push(frame, leaf);
      const ring = new THREE.Mesh(new THREE.RingGeometry(0.32, 0.4, 28), new THREE.MeshBasicMaterial({ color: '#e0b04a', transparent: true, opacity: 0.7 }));
      ring.rotation.x = -Math.PI / 2; ring.position.set(d.threshold.x, 0.03, d.threshold.z); ring.userData.doorId = d.id; world.add(ring); pickables.push(ring);
      if (loc.kind === 'interior') addLabel('Sortie', 'exit', () => new THREE.Vector3(d.threshold.x, 0.2, d.threshold.z));
    }
    for (const n of NPCS.filter(n => n.location === locId)) {
      const s = spriteMesh(n.sprite); s.position.set(n.x, 0, n.z); s.userData.npc = n.id; world.add(s); pickables.push(s); npcSprites.push(s);
      addLabel(n.name, 'npc', () => new THREE.Vector3(n.x, 2.05, n.z));
    }
    builtFor = locId;
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
    const loc = LOCATIONS[s.location];
    const target = camOverride ? new THREE.Vector3(camOverride.x, 0, camOverride.z) : new THREE.Vector3(s.player.x, 0, s.player.z);
    if (loc.kind === 'interior' && !camOverride) target.set(loc.size.w / 2, 0, loc.size.d / 2);
    cam.position.copy(target).addScaledVector(camDir, -80); cam.lookAt(target);
    const zoom = camOverride?.ppm || (loc.kind === 'interior' ? Math.min(ppm * 1.8, innerWidth / (loc.size.w * 1.6)) : ppm);
    if (zoom !== cam.userData.zoom) { cam.userData.zoom = zoom; const w = innerWidth, h = innerHeight; cam.left = -w / 2 / zoom; cam.right = w / 2 / zoom; cam.top = h / 2 / zoom; cam.bottom = -h / 2 / zoom; cam.updateProjectionMatrix(); }
    if (false) { const w = innerWidth, h = innerHeight; cam.left = -w / 2 / camOverride.ppm; cam.right = w / 2 / camOverride.ppm; cam.top = h / 2 / camOverride.ppm; cam.bottom = -h / 2 / camOverride.ppm; cam.updateProjectionMatrix(); }
    updateOcclusion();
    renderer.render(scene, cam);
    const r = canvas.getBoundingClientRect();
    for (const l of labels) { const vis = !l.visible || l.visible(); l.el.hidden = !vis; if (!vis) continue; const v = l.getPos().clone().project(cam); l.el.style.transform = `translate(-50%,-100%) translate(${r.left + (v.x + 1) / 2 * r.width}px,${r.top + (1 - v.y) / 2 * r.height}px)`; }
  }
  function pick(clientX, clientY) {
    render();
    const r = canvas.getBoundingClientRect();
    ray.setFromCamera(new THREE.Vector2(((clientX - r.left) / r.width) * 2 - 1, -((clientY - r.top) / r.height) * 2 + 1), cam);
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
    opacityOf: id => [].concat(solids.find(m => m.userData.buildingId === id)?.material ?? [])[0]?.opacity };
}
