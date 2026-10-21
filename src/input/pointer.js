// Pointer Events : souris, toucher et stylet passent par le même chemin.
export function bindPointer(canvas, onTap) {
  let down = null;
  canvas.addEventListener('pointerdown', e => { down = { x: e.clientX, y: e.clientY, t: performance.now() }; });
  canvas.addEventListener('pointerup', e => {
    if (!down) return; const moved = Math.hypot(e.clientX - down.x, e.clientY - down.y);
    if (moved < 12 && performance.now() - down.t < 600) onTap(e.clientX, e.clientY, e.pointerType);
    down = null;
  });
  canvas.addEventListener('contextmenu', e => e.preventDefault());
}
