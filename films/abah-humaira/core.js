// core.js — deterministic storybook engine. Everything is a pure function of time t.
const W = 1080, H = 1920;
let ctx = null;          // current drawing context (switched for offscreen layers)
let BOIL = 0;            // line-boil frame (8 fps), drives the hand-drawn jitter
let SID = 0;             // shape counter, reset per scene draw so jitter is stable

// ---------- math ----------
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, k) => a + (b - a) * k;
const io = k => { k = clamp(k); return k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; };
const out = k => { k = clamp(k); return 1 - Math.pow(1 - k, 3); };
const inn = k => { k = clamp(k); return k * k * k; };
const seg = (t, a, b) => clamp((t - a) / (b - a));
// closed-form damped spring step response (0 -> 1), tau = start time, f = Hz, z = damping ratio
function spring(t, tau, f = 1.2, z = 0.78) {
  const x = t - tau; if (x <= 0) return 0;
  const w = 2 * Math.PI * f;
  if (z >= 1) return 1 - Math.exp(-w * x) * (1 + w * x);
  const wd = w * Math.sqrt(1 - z * z);
  return 1 - Math.exp(-z * w * x) * (Math.cos(wd * x) + (z * w / wd) * Math.sin(wd * x));
}
function hash(n) {
  n = n | 0; n = Math.imul(n ^ (n >>> 16), 0x45d9f3b); n = Math.imul(n ^ (n >>> 16), 0x45d9f3b); n ^= n >>> 16;
  return ((n >>> 0) / 4294967295) * 2 - 1;
}
function noise1(x, seed = 0) {
  const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f);
  return hash(i * 7 + seed * 1013) * (1 - u) + hash((i + 1) * 7 + seed * 1013) * u;
}
function mulberry32(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

// ---------- shapes ----------
const mid = (p, q) => [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2];
function smoothPath(pts, closed = true) {
  const n = pts.length; ctx.beginPath();
  if (closed) {
    const m0 = mid(pts[n - 1], pts[0]); ctx.moveTo(m0[0], m0[1]);
    for (let i = 0; i < n; i++) { const p = pts[i], m = mid(p, pts[(i + 1) % n]); ctx.quadraticCurveTo(p[0], p[1], m[0], m[1]); }
    ctx.closePath();
  } else {
    ctx.moveTo(pts[0][0], pts[0][1]);
    for (let i = 1; i < n - 1; i++) { const m = mid(pts[i], pts[i + 1]); ctx.quadraticCurveTo(pts[i][0], pts[i][1], m[0], m[1]); }
    ctx.lineTo(pts[n - 1][0], pts[n - 1][1]);
  }
}
function ell(cx, cy, rx, ry, rot = 0, n = 30, a0 = 0, a1 = Math.PI * 2) {
  const pts = [], c = Math.cos(rot), s = Math.sin(rot), full = Math.abs(a1 - a0) >= Math.PI * 2 - 1e-6;
  const m = full ? n : n + 1;
  for (let i = 0; i < m; i++) {
    const a = a0 + (a1 - a0) * i / (full ? n : n);
    const x = Math.cos(a) * rx, y = Math.sin(a) * ry;
    pts.push([cx + x * c - y * s, cy + x * s + y * c]);
  }
  return pts;
}
function capsule(x1, y1, x2, y2, r1, r2, n = 10) {
  const a = Math.atan2(y2 - y1, x2 - x1), pts = [];
  for (let i = 0; i <= n; i++) { const b = a + Math.PI / 2 + Math.PI * i / n; pts.push([x1 + Math.cos(b) * r1, y1 + Math.sin(b) * r1]); }
  for (let i = 0; i <= n; i++) { const b = a - Math.PI / 2 + Math.PI * i / n; pts.push([x2 + Math.cos(b) * r2, y2 + Math.sin(b) * r2]); }
  return pts;
}
const INK = '#3b2a22';
function shape(pts, fill, o = {}) {
  const id = ++SID, jit = o.jit ?? 1.3, closed = o.closed ?? true;
  const jp = pts.map((p, k) => [p[0] + jit * hash(k * 31 + id * 977 + BOIL * 7919), p[1] + jit * hash(k * 57 + id * 389 + BOIL * 104729)]);
  if (o.round) { // polygon with rounded corners (clean, not blobby)
    const n = jp.length, rr = Array.isArray(o.round) ? o.round : jp.map(() => o.round);
    ctx.beginPath(); const m0 = mid(jp[n - 1], jp[0]); ctx.moveTo(m0[0], m0[1]);
    for (let i = 0; i < n; i++) ctx.arcTo(jp[i][0], jp[i][1], jp[(i + 1) % n][0], jp[(i + 1) % n][1], rr[i]);
    ctx.closePath();
  } else if (o.sharp) { ctx.beginPath(); ctx.moveTo(jp[0][0], jp[0][1]); for (let i = 1; i < jp.length; i++) ctx.lineTo(jp[i][0], jp[i][1]); if (closed) ctx.closePath(); }
  else smoothPath(jp, closed);
  const a0 = ctx.globalAlpha;
  if (fill) {
    ctx.fillStyle = fill; ctx.fill();
    if (o.wash !== false) { // watercolour edge pooling
      ctx.save(); ctx.clip(); ctx.lineWidth = o.washW ?? 16; ctx.strokeStyle = o.washC ?? 'rgba(110,55,25,0.13)'; ctx.stroke(); ctx.restore();
    }
  }
  if (o.ink !== null) {
    ctx.globalAlpha = a0 * (o.inkA ?? 0.9); ctx.lineWidth = o.lw ?? 3.4; ctx.strokeStyle = o.ink ?? INK;
    ctx.lineJoin = 'round'; ctx.lineCap = 'round'; ctx.stroke(); ctx.globalAlpha = a0;
  }
}
function line(pts, o = {}) { shape(pts, null, Object.assign({ closed: false }, o)); }
function glow(x, y, r, col, a = 1) {
  const g = ctx.createRadialGradient(x, y, 0, x, y, r);
  g.addColorStop(0, col.replace('A', a)); g.addColorStop(1, col.replace('A', 0));
  ctx.fillStyle = g; ctx.fillRect(x - r, y - r, r * 2, r * 2);
}
function vgrad(y0, y1, stops) {
  const g = ctx.createLinearGradient(0, y0, 0, y1); stops.forEach(([k, c]) => g.addColorStop(k, c)); return g;
}
function cam(z, cx, cy, rot = 0) { ctx.translate(W / 2, H / 2); ctx.rotate(rot); ctx.scale(z, z); ctx.translate(-cx, -cy); }
// zoom keyed in log space
function logZoom(a, b, k) { return Math.exp(lerp(Math.log(a), Math.log(b), k)); }

// ---------- offscreen ----------
function mkCanvas(w = W, h = H) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
function withCtx(c, fn) { const prev = ctx, prevSID = SID; ctx = c.getContext('2d'); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, c.width, c.height); fn(); ctx = prev; SID = prevSID; }

// ---------- paper + grain (seeded, built once) ----------
let PAPER = null, GRAIN = [];
function buildTextures() {
  PAPER = mkCanvas(540, 960);
  const p = PAPER.getContext('2d'), img = p.createImageData(540, 960), r = mulberry32(7);
  for (let i = 0; i < img.data.length; i += 4) {
    const x = (i / 4) % 540, y = Math.floor(i / 4 / 540);
    const fib = 0.5 + 0.5 * Math.sin(x * 0.9 + noise1(y * 0.05, 3) * 6) * Math.sin(y * 0.13 + noise1(x * 0.04, 5) * 5);
    const v = 236 + r() * 16 - fib * 8;
    img.data[i] = v; img.data[i + 1] = v - 6; img.data[i + 2] = v - 18; img.data[i + 3] = 255;
  }
  p.putImageData(img, 0, 0);
  for (let g = 0; g < 4; g++) {
    const c = mkCanvas(360, 640), q = c.getContext('2d'), im = q.createImageData(360, 640), rr = mulberry32(100 + g);
    for (let i = 0; i < im.data.length; i += 4) { const v = rr() * 255; im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255; }
    q.putImageData(im, 0, 0); GRAIN.push(c);
  }
}
function paperPass(a = 0.55) {
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = a; ctx.drawImage(PAPER, 0, 0, W, H);
  ctx.globalCompositeOperation = 'overlay'; ctx.globalAlpha = 0.07; ctx.drawImage(GRAIN[BOIL % 4], 0, 0, W, H);
  ctx.restore();
}
function vignette(a = 0.35, col = '40,20,10') {
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  const g = ctx.createRadialGradient(W / 2, H * 0.48, H * 0.28, W / 2, H * 0.5, H * 0.72);
  g.addColorStop(0, `rgba(${col},0)`); g.addColorStop(1, `rgba(${col},${a})`);
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); ctx.restore();
}
