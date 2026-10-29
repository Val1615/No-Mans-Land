import * as THREE from 'three';
// Textures peintes procéduralement (faites pour ce projet). Statut : provisoire stylisé.
const PPM = 32;
// Skins issus de la maquette (assets/mockup, voir tools_assets.py). Chargés avant la construction des scènes.
export const SKIN = {};
export async function loadSkins(names, path = n => `./assets/mockup/${n}.webp`) {
  await Promise.all(names.map(n => new Promise((ok, ko) => { const i = new Image(); i.onload = () => { SKIN[n] = i; ok(); }; i.onerror = ko; i.src = path(n); })));
}
function pattern(x, name, metres, P) {
  const img = SKIN[name]; if (!img) return null; const c = document.createElement('canvas'); c.width = c.height = Math.round(metres * P);
  c.getContext('2d').drawImage(img, 0, 0, c.width, c.height); return x.createPattern(c, 'repeat');
}
function cueMark(x, cue, cx, cy) { x.strokeStyle = 'rgba(235,225,200,.85)'; x.lineWidth = 3; x.beginPath();
  if (cue === 'cross') { x.moveTo(cx, cy - 10); x.lineTo(cx, cy + 10); x.moveTo(cx - 10, cy); x.lineTo(cx + 10, cy); }
  if (cue === 'bottle') { x.rect(cx - 4, cy - 2, 8, 14); x.moveTo(cx, cy - 2); x.lineTo(cx, cy - 10); }
  if (cue === 'drop') { x.moveTo(cx, cy - 11); x.quadraticCurveTo(cx + 9, cy + 2, cx, cy + 8); x.quadraticCurveTo(cx - 9, cy + 2, cx, cy - 11); }
  if (cue === 'mirror') { x.arc(cx, cy, 8, 0, Math.PI * 2); x.moveTo(cx - 3, cy - 3); x.lineTo(cx + 2, cy - 5); }
  if (cue === 'key') { x.arc(cx - 5, cy, 5, 0, Math.PI * 2); x.moveTo(cx, cy); x.lineTo(cx + 11, cy); x.moveTo(cx + 8, cy); x.lineTo(cx + 8, cy + 5); }
  if (cue === 'jar') { x.rect(cx - 7, cy - 6, 14, 16); x.moveTo(cx - 9, cy - 8); x.lineTo(cx + 9, cy - 8); }
  x.stroke(); } // pixels par mètre de texture
function rng(seed) { let s = seed >>> 0 || 1; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; }
function hash(str) { let h = 2166136261; for (const c of str) h = Math.imul(h ^ c.charCodeAt(0), 16777619); return h >>> 0; }
const tex = (c) => { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t; };
function shade(hex, f) { const c = new THREE.Color(hex); c.multiplyScalar(f); return '#' + c.getHexString(); }

export function facadeTexture(b, faceW, faceH, opts) {
  const c = document.createElement('canvas'); c.width = Math.max(64, Math.round(faceW * PPM)); c.height = Math.max(64, Math.round(faceH * PPM));
  const x = c.getContext('2d'), r = rng(hash(b.id + opts.face)), W = c.width, H = c.height, m = PPM;
  const skin = b.skin?.[opts.face];
  if (skin && SKIN[skin]) { // la texture s'applique au volume mesuré, elle ne le définit pas
    x.drawImage(SKIN[skin], 0, 0, W, H);
    for (const [fx, fy, fw, fh] of b.skin.cover?.[opts.face] || []) {
      const x0 = fx * W, y0 = fy * H, w = fw * W, h = fh * H; x.fillStyle = '#3a2c1f'; x.fillRect(x0, y0, w, h);
      for (let yy = y0; yy < y0 + h; yy += 0.22 * m) { x.save(); x.translate(x0 + w / 2, yy + 0.1 * m); x.rotate((r() - .5) * 0.08); x.fillStyle = shade('#7a6248', 0.7 + r() * 0.4); x.fillRect(-w / 2 - 3, -0.09 * m, w + 6, 0.18 * m); x.restore(); } }
    x.fillStyle = 'rgba(40,28,18,.18)'; x.fillRect(0, 0, W, H);
    const g = x.createLinearGradient(0, H - 1.2 * m, 0, H); g.addColorStop(0, 'rgba(160,130,90,0)'); g.addColorStop(1, 'rgba(176,146,100,.9)'); x.fillStyle = g; x.fillRect(0, H - 1.2 * m, W, 1.2 * m);
    if (opts.cue && opts.doorX != null) cueMark(x, opts.cue, opts.doorX * m + 0.85 * m, H - 1.7 * m);
    return tex(c);
  }
  x.fillStyle = b.color; x.fillRect(0, 0, W, H);
  for (let i = 0; i < W * H / 60; i++) { x.fillStyle = `rgba(${r() < .5 ? '0,0,0' : '255,240,220'},${r() * 0.06})`; x.fillRect(r() * W, r() * H, 1 + r() * 3, 1 + r() * 3); }
  // enduit écaillé et coulures de sable
  for (let i = 0; i < faceW * 1.5; i++) { x.fillStyle = shade(b.color, 0.82 + r() * 0.1); const w = (0.4 + r()) * m, h = (0.2 + r() * 0.6) * m; x.fillRect(r() * W, r() * H, w, h); }
  for (let i = 0; i < faceW * 0.6; i++) { const px = r() * W, py = r() * H, pw = (0.6 + r() * 1.4) * m, ph = (0.4 + r() * 0.9) * m;
    x.fillStyle = '#7d5a43'; x.fillRect(px, py, pw, ph); x.strokeStyle = 'rgba(40,25,15,.5)'; x.lineWidth = 1;
    for (let yy = py; yy < py + ph; yy += 0.12 * m) { x.beginPath(); x.moveTo(px, yy); x.lineTo(px + pw, yy); x.stroke(); } }
  x.strokeStyle = 'rgba(25,18,12,.55)'; x.lineWidth = 1.5;
  for (let i = 0; i < faceW * 0.8; i++) { let px = r() * W, py = r() * H * 0.6; x.beginPath(); x.moveTo(px, py); for (let k = 0; k < 6; k++) { px += (r() - .5) * 18; py += 6 + r() * 14; x.lineTo(px, py); } x.stroke(); }
  for (let i = 0; i < faceW; i++) { x.fillStyle = 'rgba(40,30,20,.18)'; x.fillRect(r() * W, 0.2 * m, 2 + r() * 5, r() * H * 0.7); }
  const g = x.createLinearGradient(0, H - 1.3 * m, 0, H); g.addColorStop(0, 'rgba(160,130,90,0)'); g.addColorStop(1, 'rgba(170,140,95,.95)'); x.fillStyle = g; x.fillRect(0, H - 1.3 * m, W, 1.3 * m);
  if (b.ruin === true) { x.fillStyle = 'rgba(0,0,0,.25)'; for (let i = 0; i < 6; i++) { x.beginPath(); x.moveTo(r() * W, 0); x.lineTo(r() * W, H * r()); x.lineTo(r() * W, 0); x.fill(); } return tex(c); }
  const storeys = Math.max(1, Math.round(faceH / 3));
  // corniche
  x.fillStyle = b.trim; x.fillRect(0, 0, W, 0.18 * m);
  for (let s = 1; s < storeys; s++) { x.fillStyle = shade(b.color, 0.75); x.fillRect(0, H - s * 3 * m, W, 0.12 * m); }
  const doorX = opts.doorX; // position de la porte en m depuis la gauche de la face, ou null
  const win = b.windows || 'shutters';
  if (win !== 'none') for (let s = 0; s < storeys; s++) {
    const n = Math.max(1, Math.floor(faceW / 2.6));
    for (let k = 0; k < n; k++) {
      const cx = (k + 0.5) * faceW / n; if (doorX != null && s === 0 && Math.abs(cx - doorX) < 1.3) continue;
      const y0 = H - (s * 3 + (win === 'high' ? 2.3 : 1.0)) * m - (win === 'slits' ? 0.9 : 1.1) * m;
      const ww = (win === 'slits' ? 0.25 : win === 'high' ? 1.2 : 0.9) * m, wh = (win === 'slits' ? 0.9 : win === 'high' ? 0.5 : 1.1) * m, x0 = cx * m - ww / 2;
      x.fillStyle = '#16120e'; x.fillRect(x0, y0, ww, wh);
      if (win === 'holes') { x.fillStyle = b.color; for (let q = 0; q < 5; q++) x.fillRect(x0 + r() * ww, y0 + (r() < .5 ? 0 : wh - 4), 3 + r() * 6, 3 + r() * 5); continue; }
      if (win === 'boarded') { for (let l = 0; l < 3; l++) { x.save(); x.translate(x0 + ww / 2, y0 + (0.25 + l * 0.27) * wh); x.rotate((r() - .5) * 0.5); x.fillStyle = shade('#7a6248', 0.8 + r() * 0.35); x.fillRect(-ww * 0.65, -0.08 * m, ww * 1.3, 0.16 * m); x.restore(); } continue; }
      if (win === 'curtains') { x.fillStyle = '#5a3f30'; x.fillRect(x0 + 2, y0 + 2, ww - 4, wh - 4); }
      if (win === 'shutters' || (win !== 'slits' && r() < 0.4)) { x.fillStyle = shade(b.trim, 0.9 + r() * 0.2);
        const half = r() < 0.5; x.fillRect(x0 - 0.3 * m, y0, 0.3 * m, wh); if (half) x.fillRect(x0 + ww, y0, 0.3 * m, wh); else x.fillRect(x0, y0, ww, wh * 0.6);
        x.strokeStyle = 'rgba(0,0,0,.35)'; for (let l = 0; l < 5; l++) { x.beginPath(); x.moveTo(x0, y0 + l * wh / 5); x.lineTo(x0 + ww, y0 + l * wh / 5); x.stroke(); } }
      x.strokeStyle = b.trim; x.lineWidth = 2; x.strokeRect(x0, y0, ww, wh);
    }
  }
  // porte peinte (non visitable) : jamais de marqueur, apparence fermée
  if (opts.paintDoor && doorX != null) {
    const dw = (opts.paintDoor === 'garage' ? 3 : 1) * m, dh = (opts.paintDoor === 'garage' ? 2.8 : 2.1) * m, x0 = doorX * m - dw / 2;
    x.fillStyle = shade(b.trim, 0.8); x.fillRect(x0, H - dh, dw, dh);
    x.strokeStyle = 'rgba(0,0,0,.45)'; x.lineWidth = 2;
    if (opts.paintDoor === 'garage') for (let l = 1; l < 10; l++) { x.beginPath(); x.moveTo(x0, H - dh + l * dh / 10); x.lineTo(x0 + dw, H - dh + l * dh / 10); x.stroke(); }
    else { x.strokeRect(x0 + 4, H - dh + 4, dw - 8, dh - 4); x.fillStyle = '#c9a54a'; x.fillRect(x0 + dw - 8, H - dh / 2, 3, 3); }
    if (opts.paintDoor === 'boarded') { x.fillStyle = '#6b5236'; for (let l = 0; l < 3; l++) x.fillRect(x0 - 4, H - dh + (0.3 + l * 0.6) * m, dw + 8, 0.14 * m); }
  }
  if (opts.cue && doorX != null) { const cx = doorX * m + 0.85 * m, cy = H - 1.7 * m; x.strokeStyle = 'rgba(235,225,200,.75)'; x.lineWidth = 3; x.beginPath();
    if (opts.cue === 'cross') { x.moveTo(cx, cy - 10); x.lineTo(cx, cy + 10); x.moveTo(cx - 10, cy); x.lineTo(cx + 10, cy); }
    if (opts.cue === 'bottle') { x.rect(cx - 4, cy - 2, 8, 14); x.moveTo(cx, cy - 2); x.lineTo(cx, cy - 10); }
    if (opts.cue === 'drop') { x.moveTo(cx, cy - 11); x.quadraticCurveTo(cx + 9, cy + 2, cx, cy + 8); x.quadraticCurveTo(cx - 9, cy + 2, cx, cy - 11); }
    if (opts.cue === 'jar') { x.rect(cx - 7, cy - 6, 14, 16); x.moveTo(cx - 9, cy - 8); x.lineTo(cx + 9, cy - 8); }
    x.stroke(); }
  if (opts.sign) { // enseigne de service
    const sw = Math.min(W * 0.6, opts.sign.length * 0.36 * m + 0.6 * m), sx = (doorX ?? faceW / 2) * m - sw / 2, sy = H - 3.0 * m + 0.25 * m;
    x.fillStyle = '#2a1f17'; x.fillRect(sx, sy, sw, 0.55 * m); x.strokeStyle = b.trim; x.lineWidth = 3; x.strokeRect(sx, sy, sw, 0.55 * m);
    x.fillStyle = '#f0dcae'; x.font = `bold ${0.36 * m}px Georgia, serif`; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(opts.sign, sx + sw / 2, sy + 0.29 * m);
  }
  return tex(c);
}
export function roofTexture(b, w, d) {
  const c = document.createElement('canvas'); c.width = Math.round(w * 16); c.height = Math.round(d * 16);
  const x = c.getContext('2d'), r = rng(hash(b.id + 'roof'));
  x.fillStyle = b.ruin === true ? '#6e6255' : shade(b.trim, 0.55); x.fillRect(0, 0, c.width, c.height);
  const pr = b.roof && SKIN[b.roof]; if (pr) { x.drawImage(pr, 0, 0, c.width, c.height);
    if (b.roofHoles) for (let i = 0; i < 3; i++) { x.fillStyle = 'rgba(18,14,10,.85)'; x.beginPath(); x.ellipse(r() * c.width, r() * c.height, 8 + r() * 20, 6 + r() * 12, r() * 3, 0, 7); x.fill(); }
    x.fillStyle = 'rgba(190,160,110,.22)'; x.fillRect(0, 0, c.width, c.height); return tex(c); }
  if (b.roofHoles) for (let i = 0; i < 4; i++) { x.fillStyle = '#120e0a'; x.beginPath(); const hx = r() * c.width, hy = r() * c.height; x.ellipse(hx, hy, 8 + r() * 26, 6 + r() * 16, r() * 3, 0, 7); x.fill(); }
  if (b.ruin !== true) { for (let i = 0; i < c.width; i += 6) { x.fillStyle = `rgba(0,0,0,${0.08 + r() * 0.1})`; x.fillRect(i, 0, 2, c.height); }
    for (let i = 0; i < 6; i++) { x.fillStyle = `rgba(120,70,30,${0.2 + r() * 0.3})`; x.fillRect(r() * c.width, r() * c.height, 10 + r() * 30, 8 + r() * 20); } }
  x.fillStyle = 'rgba(190,160,110,.35)'; for (let i = 0; i < 12; i++) x.fillRect(r() * c.width, r() * c.height, 6 + r() * 20, 3 + r() * 6);
  return tex(c);
}
export function groundTexture(loc, doors = []) {
  const P = 24, W = Math.round(loc.size.w * P), H = Math.round(loc.size.d * P);
  const c = document.createElement('canvas'); c.width = W; c.height = H; const x = c.getContext('2d'), r = rng(hash(loc.id));
  x.fillStyle = pattern(x, loc.ground.skin, loc.ground.tileM || 4, P) || loc.ground.base; x.fillRect(0, 0, W, H);
  if (loc.kind === 'interior' && loc.ground.skin) return tex(c); // v6 : sol d'intérieur = texture réelle seule, rien de peint par code
  if (!loc.ground.clean) for (let i = 0; i < W * H / 40; i++) { x.fillStyle = `rgba(${r() < .5 ? '60,45,30' : '230,210,170'},${r() * 0.08})`; x.fillRect(r() * W, r() * H, 1 + r() * 2, 1 + r() * 2); }
  if (loc.ground.tiles && !loc.ground.skin) { x.strokeStyle = 'rgba(0,0,0,.15)'; for (let i = 0; i <= loc.size.w; i += 0.5) { x.beginPath(); x.moveTo(i * P, 0); x.lineTo(i * P, H); x.stroke(); } for (let j = 0; j <= loc.size.d; j += 0.5) { x.beginPath(); x.moveTo(0, j * P); x.lineTo(W, j * P); x.stroke(); } }
  if (loc.ground.planks && !loc.ground.skin) { for (let j = 0; j < loc.size.d; j += 0.25) { x.fillStyle = `rgba(0,0,0,${0.05 + r() * 0.12})`; x.fillRect(0, j * P, W, 1.5); } }
  for (const z of loc.ground.zones || []) {
    const zx = z.x * P, zy = z.z * P, zw = z.w * P, zh = z.d * P;
    const zp = pattern(x, z.skin || { asphalt: 'g_asphalt', packed: 'g_dirt', track: 'g_gravel', grass: 'g_grass', wet: 'g_wet', plate: 'g_concrete' }[z.kind], z.tileM || 4, P); // v13 : wet = chaussée mouillée de Steel
    if (zp) { x.fillStyle = zp; x.globalAlpha = z.kind === 'grass' ? 0.75 : 1; x.fillRect(zx, zy, zw, zh); x.globalAlpha = 1;
      if (z.tint) { x.fillStyle = z.tint; x.fillRect(zx, zy, zw, zh); }
      if (z.kind === 'asphalt' && !loc.ground.clean) { x.fillStyle = 'rgba(205,180,130,.5)'; for (let i = 0; i < 26; i++) { const ex = zx + r() * zw, top = r() < .5; x.beginPath(); x.ellipse(ex, top ? zy + 6 : zy + zh - 6, 30 + r() * 70, 6 + r() * 14, 0, 0, Math.PI * 2); x.fill(); } }
    } else if (z.kind === 'asphalt') { x.fillStyle = '#4b4743'; x.fillRect(zx, zy, zw, zh);
      for (let i = 0; i < zw * zh / 30; i++) { x.fillStyle = `rgba(255,255,255,${r() * 0.05})`; x.fillRect(zx + r() * zw, zy + r() * zh, 2, 2); }
      x.strokeStyle = 'rgba(20,18,16,.6)'; x.lineWidth = 1.2; for (let i = 0; i < 40; i++) { let px = zx + r() * zw, py = zy + r() * zh; x.beginPath(); x.moveTo(px, py); for (let k = 0; k < 5; k++) { px += (r() - .5) * 40; py += (r() - .5) * 20; x.lineTo(px, py); } x.stroke(); }
      x.fillStyle = 'rgba(205,180,130,.55)'; for (let i = 0; i < 26; i++) { const ex = zx + r() * zw, top = r() < .5; x.beginPath(); x.ellipse(ex, top ? zy + 6 : zy + zh - 6, 30 + r() * 70, 6 + r() * 14, 0, 0, Math.PI * 2); x.fill(); }
      x.fillStyle = 'rgba(220,200,150,.35)'; for (let i = zx + 40; i < zx + zw; i += 90) x.fillRect(i, zy + zh / 2 - 2, 40, 4);
    } else if (z.kind === 'track') { x.fillStyle = '#9b8463'; x.fillRect(zx, zy, zw, zh); x.fillStyle = 'rgba(80,60,40,.25)'; x.fillRect(zx, zy + zh * 0.3, zw, 6); x.fillRect(zx, zy + zh * 0.65, zw, 6); }
    else if (z.kind === 'packed') { x.fillStyle = 'rgba(120,100,75,.45)'; x.fillRect(zx, zy, zw, zh); }
  }
  if (loc.kind === 'exterior' && !loc.ground.clean) {
    for (const b of loc.buildings) for (let i = 0; i < b.w + b.d; i++) { const side = r(); x.fillStyle = `rgba(200,172,120,${0.35 + r() * 0.3})`; x.beginPath();
      const px = side < .5 ? (b.x + r() * b.w) * P : (b.x + b.w) * P, py = side < .5 ? (b.z + b.d) * P : (b.z + r() * b.d) * P;
      x.ellipse(px, py, (0.6 + r() * 1.4) * P, (0.3 + r() * 0.7) * P, side < .5 ? 0 : Math.PI / 2, 0, 7); x.fill(); }
    for (const d of doors.filter(d => d.location === loc.id && !d.junction && !d.edge)) { x.fillStyle = 'rgba(90,70,50,.35)'; x.beginPath(); x.ellipse(d.threshold.x * P, d.threshold.z * P, 0.9 * P, 0.7 * P, 0, 0, 7); x.fill();
      x.fillStyle = 'rgba(60,45,30,.35)'; for (let k = 0; k < 7; k++) x.fillRect((d.threshold.x + (r() - .5) * 1.4) * P, (d.threshold.z + (r() - .5) * 1.2) * P, 4, 7); }
  }
  for (const w of loc.ground.water || []) paintWater(x, w, loc.ground.waterSkin || 'g_cl_eau', w.tileM || 6, P, r);
  // herbes mortes (Ch. I §71)
  if (loc.ground.tint) { x.fillStyle = loc.ground.tint; x.fillRect(0, 0, W, H); } // v13 : voile de nuit
  if (loc.kind === 'exterior' && !loc.ground.clean) { x.strokeStyle = 'rgba(150,130,70,.8)'; for (let i = 0; i < (loc.ground.skin ? 250 : 700); i++) { const px = r() * W, py = r() * H; for (let k = 0; k < 4; k++) { x.beginPath(); x.moveTo(px, py); x.lineTo(px + (r() - .5) * 8, py - 4 - r() * 6); x.stroke(); } } }
  return tex(c);
}

export function hiddenDoorTexture() {
  const c = document.createElement('canvas'); c.width = 64; c.height = 140; const x = c.getContext('2d');
  x.fillStyle = '#4a3828'; x.fillRect(0, 0, 64, 140);
  for (let i = 0; i < 5; i++) { x.fillStyle = shade('#6e5640', 0.8 + (i % 2) * 0.2); x.fillRect(i * 13, 0, 12, 140); x.fillStyle = 'rgba(0,0,0,.4)'; x.fillRect(i * 13 + 12, 0, 1, 140); }
  x.fillStyle = '#5c4632'; x.save(); x.translate(32, 40); x.rotate(-0.25); x.fillRect(-40, -5, 80, 10); x.restore(); x.save(); x.translate(32, 100); x.rotate(0.2); x.fillRect(-40, -5, 80, 10); x.restore();
  x.fillStyle = 'rgba(255,190,110,.8)'; x.fillRect(4, 134, 56, 3); // filet de lumière sous la porte : indice de vie, lisible de près
  x.fillStyle = 'rgba(200,170,120,.6)'; x.fillRect(0, 120, 64, 20);
  return tex(c);
}

// China Lake : le carreau d'eau (512 px, raccordable) se répète ; on casse la répétition sans toucher au PNG :
// couche de base décalée (UV offset), deuxième couche tournée de 37° et mise à l'échelle 1,7 en fondu, taches basses fréquences,
// reflets de lanternes flottantes peints par code. Les bords restent raccordés (aucune rotation par carreau, donc aucune couture).
function paintWater(x, w, skin, metres, P, r) {
  const img = SKIN[skin], zx = w.x * P, zy = w.z * P, zw = w.w * P, zh = w.d * P;
  if (w.image && SKIN[w.image]) { // retours tour 1 : lac d'Ocre (contour, quai, pilotis peints), image entière sur LAKE, aucune retouche du fichier
    x.drawImage(SKIN[w.image], zx, zy, zw, zh);
    for (const l of w.lanterns || []) { const px = l.x * P, py = l.z * P, g = x.createRadialGradient(px, py, 0, px, py, 1.4 * P);
      g.addColorStop(0, 'rgba(200,50,42,.55)'); g.addColorStop(1, 'rgba(200,50,42,0)'); x.fillStyle = g; x.fillRect(px - 1.4 * P, py - 1.4 * P, 2.8 * P, 2.8 * P);
      x.fillStyle = 'rgba(232,161,58,.9)'; x.beginPath(); x.ellipse(px, py, 0.22 * P, 0.16 * P, 0, 0, 7); x.fill();
      x.fillStyle = 'rgba(200,50,42,.95)'; x.beginPath(); x.ellipse(px, py, 0.16 * P, 0.11 * P, 0, 0, 7); x.fill(); }
    return; }
  x.save(); x.beginPath(); x.rect(zx, zy, zw, zh); x.clip();
  if (img) {
    const c = document.createElement('canvas'); c.width = c.height = Math.round(metres * P); c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
    const pat = x.createPattern(c, 'repeat'); pat.setTransform(new DOMMatrix().translate(zx + c.width * 0.37, zy + c.width * 0.61));
    x.fillStyle = pat; x.fillRect(zx, zy, zw, zh);
    const p2 = x.createPattern(c, 'repeat'); p2.setTransform(new DOMMatrix().translate(zx + zw / 2, zy + zh / 2).rotate(37).scale(1.7));
    x.globalAlpha = 0.38; x.fillStyle = p2; x.fillRect(zx, zy, zw, zh); x.globalAlpha = 1;
  } else { x.fillStyle = '#0b0d0a'; x.fillRect(zx, zy, zw, zh); }
  for (let i = 0; i < Math.round(w.w * w.d / 6); i++) { // taches lentes : pétrole plus sombre, voile plus clair
    const px = zx + r() * zw, py = zy + r() * zh, rad = (1.5 + r() * 3.5) * P, g = x.createRadialGradient(px, py, 0, px, py, rad), dark = r() < 0.6;
    g.addColorStop(0, dark ? 'rgba(4,5,3,.35)' : 'rgba(70,80,50,.12)'); g.addColorStop(1, 'rgba(0,0,0,0)'); x.fillStyle = g; x.fillRect(px - rad, py - rad, rad * 2, rad * 2); }
  for (const l of w.lanterns || []) { // lanternes flottantes : corps rouge, reflet étiré
    const px = l.x * P, py = l.z * P, g = x.createRadialGradient(px, py, 0, px, py, 1.4 * P);
    g.addColorStop(0, 'rgba(200,50,42,.55)'); g.addColorStop(1, 'rgba(200,50,42,0)'); x.fillStyle = g; x.fillRect(px - 1.4 * P, py - 1.4 * P, 2.8 * P, 2.8 * P);
    x.fillStyle = 'rgba(232,161,58,.9)'; x.beginPath(); x.ellipse(px, py, 0.22 * P, 0.16 * P, 0, 0, 7); x.fill();
    x.fillStyle = 'rgba(200,50,42,.95)'; x.beginPath(); x.ellipse(px, py, 0.16 * P, 0.11 * P, 0, 0, 7); x.fill(); }
  x.strokeStyle = 'rgba(20,16,10,.8)'; x.lineWidth = 3; x.strokeRect(zx + 1, zy + 1, zw - 2, zh - 2); // arête du quai
  x.restore();
}
