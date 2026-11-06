// Pointer Events : souris, toucher et stylet passent par le même chemin ; molette et pincement à deux doigts pilotent le zoom caméra.
export function bindPointer(canvas, onTap, zoomCtl = null) {
  const pts = new Map();
  let down = null, pinch = null, tPinch = null, pinching = false;
  const canZ = () => !!zoomCtl && (!zoomCtl.canZoom || zoomCtl.canZoom());
  const applyPinch = (st, d) => {
    const raw = st.z * (d / st.d), applied = zoomCtl.set(raw);
    if (Number.isFinite(applied) && Math.abs(applied - raw) > 1e-3) { st.d = d; st.z = applied; }
  };
  canvas.addEventListener('pointerdown', e => {
    pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pts.size === 1 && !pinching) {
      down = { id: e.pointerId, x: e.clientX, y: e.clientY, t: performance.now() };
    } else {
      down = null; pinching = true;
      if (pts.size === 2 && canZ()) {
        const [a, b] = [...pts.values()], d = Math.hypot(a.x - b.x, a.y - b.y);
        if (d > 8) pinch = { d, z: zoomCtl.get() };
      }
    }
  });
  canvas.addEventListener('pointermove', e => {
    if (!pts.has(e.pointerId)) return;
    pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pts.size === 2 && canZ()) {
      const [a, b] = [...pts.values()], d = Math.hypot(a.x - b.x, a.y - b.y);
      if (!pinch && d > 8) pinch = { d, z: zoomCtl.get() };
      if (pinch && d > 8) applyPinch(pinch, d);
    }
  });
  const endPtr = e => {
    pts.delete(e.pointerId);
    if (e.type === 'pointerup' && !pinching && down && down.id === e.pointerId) {
      const moved = Math.hypot(e.clientX - down.x, e.clientY - down.y);
      if (moved < 12 && performance.now() - down.t < 600) onTap(e.clientX, e.clientY, e.pointerType);
    }
    if (pts.size < 2) pinch = null;
    if (pts.size === 0) { down = null; pinching = false; }
  };
  canvas.addEventListener('pointerup', endPtr);
  canvas.addEventListener('pointercancel', endPtr);
  // Repli TouchEvent (gestes synthétiques ou WebKit tactile sans double comptage si PointerEvent actif)
  canvas.addEventListener('touchstart', e => {
    if (e.touches.length < 2) return;
    down = null; pinching = true;
    if (pts.size < 2 && e.touches.length === 2 && canZ()) {
      const d = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
      if (d > 8) tPinch = { d, z: zoomCtl.get() };
    }
  }, { passive: true });
  canvas.addEventListener('touchmove', e => {
    if (e.touches.length >= 2) e.preventDefault();
    if (pts.size < 2 && e.touches.length === 2 && canZ()) {
      const d = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
      if (!tPinch && d > 8) tPinch = { d, z: zoomCtl.get() };
      if (tPinch && d > 8) applyPinch(tPinch, d);
    }
  }, { passive: false });
  const endTouch = e => {
    if (e.touches.length < 2) tPinch = null;
    if (e.touches.length === 0 && pts.size === 0) pinching = false;
  };
  canvas.addEventListener('touchend', endTouch, { passive: true });
  canvas.addEventListener('touchcancel', endTouch, { passive: true });
  canvas.addEventListener('wheel', e => {
    if (!canZ()) return;
    e.preventDefault();
    const raw = e.deltaMode === 1 ? e.deltaY * 32 : e.deltaMode === 2 ? e.deltaY * 300 : e.deltaY;
    const dy = Math.max(-240, Math.min(240, raw));
    if (!dy) return;
    zoomCtl.set(zoomCtl.get() - dy * 0.001);
  }, { passive: false });
  addEventListener('blur', () => { pts.clear(); down = null; pinch = null; tPinch = null; pinching = false; });
  canvas.addEventListener('contextmenu', e => e.preventDefault());
}
