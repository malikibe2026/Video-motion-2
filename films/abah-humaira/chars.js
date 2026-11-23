// chars.js — Abah and Humaira, drawn by code so they look the same in every scene.
const C = {
  skin: '#e3b48e', skinL: '#efc6a3', hair: '#2a211d', beard: 'rgba(48,32,24,0.55)',
  shirt: '#f3eadb', shirtD: '#e0d1b6', trouser: '#5d4535',
  pink: '#f5bec7', pinkD: '#e08e9d', ribbon: '#e56c86', blanket: '#fcf7ee', cap: '#f4ebdb',
  blush: 'rgba(236,118,108,0.30)', sil: '#22130e', mouth: '#8a3f38', tear: 'rgba(176,218,242,0.95)'
};
const SIL = { on: false }; // silhouette mode: every fill becomes ink-dark, no features

function F(c) { return SIL.on ? C.sil : c; }
function feat() { return !SIL.on; }

// simple 2-bone IK: returns elbow for shoulder S, hand Hn, lengths a,b; bend = +1/-1
function ik(S, Hn, a, b, bend = 1) {
  const dx = Hn[0] - S[0], dy = Hn[1] - S[1]; let d = Math.hypot(dx, dy);
  d = Math.min(d, a + b - 1e-3);
  const ang = Math.atan2(dy, dx), cosA = clamp((a * a + d * d - b * b) / (2 * a * d), -1, 1);
  const e = ang + bend * Math.acos(cosA);
  return [S[0] + Math.cos(e) * a, S[1] + Math.sin(e) * a];
}
function arm(S, Hn, a, b, bend, o = {}) {
  const E = ik(S, Hn, a, b, bend);
  const r0 = o.r0 ?? 44, r1 = o.r1 ?? 38, r2 = o.r2 ?? 32;
  shape(capsule(S[0], S[1], E[0], E[1], r0, r1), F(o.sleeve ?? C.shirt));
  if (o.rolled) { // rolled sleeve: bare forearm
    shape(capsule(E[0], E[1], Hn[0], Hn[1], r1 * 0.78, r2 * 0.8), F(C.skin));
    shape(ell(E[0], E[1], r1 * 1.02, r1 * 0.62, Math.atan2(Hn[1] - E[1], Hn[0] - E[0]) + Math.PI / 2), F(C.shirtD), { lw: 3 });
  } else shape(capsule(E[0], E[1], Hn[0], Hn[1], r1, r2), F(o.sleeve ?? C.shirt));
  return E;
}
function hand(x, y, s, rot, o = {}) { // round storybook mitten with a thumb
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s * (o.flip ? -1 : 1));
  shape(ell(-4, -16, 11, 9, -0.6), F(o.c ?? C.skin), { lw: 3 });
  shape(ell(0, 0, 25, 21), F(o.c ?? C.skin));
  if (feat()) { line([[14, -6], [22, -4]], { lw: 2, inkA: 0.45 }); line([[14, 5], [22, 6]], { lw: 2, inkA: 0.45 }); }
  ctx.restore();
}

// ---------- Abah ----------
function abahHead(x, y, s, rot, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s * (o.dir ?? 1), s);
  const lx = (o.look?.[0] ?? 0), ly = (o.look?.[1] ?? 0);
  shape(ell(-50, 10, 13, 19), F(C.skin), { lw: 3 });
  if (feat()) line([[-53, 2], [-47, 12], [-52, 20]], { lw: 2.2, inkA: 0.55 });
  shape(ell(0, 0, 66, 80), F(C.skin));
  if (feat()) {
    // beard crescent + moustache
    const outer = ell(3, 6, 66, 77, 0, 22, 0.1, Math.PI - 0.15);
    const inner = ell(16, 20, 44, 34, 0, 16, Math.PI - 0.35, 0.35);
    shape(outer.concat(inner), C.beard, { ink: null, wash: false, jit: 0.6 });
    shape([[12, 26], [28, 22], [46, 24], [50, 30], [30, 30], [14, 32]], 'rgba(48,32,24,0.6)', { ink: null, wash: false, jit: 0.4 });
    shape(ell(36, 20, 13, 7), C.blush, { ink: null, wash: false });
    // eyes
    const e = o.eyes ?? 'open';
    const ex1 = 32 + lx, ey1 = -4 + ly, ex2 = -6 + lx * 0.8, ey2 = -6 + ly;
    if (e === 'open') {
      shape(ell(ex1, ey1, 6.5, 8.5), INK, { ink: null, wash: false, jit: 0.3 });
      shape(ell(ex2, ey2, 5.5, 8), INK, { ink: null, wash: false, jit: 0.3 });
      ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(ex1 + 2, ey1 - 3, 2.2, 0, 7); ctx.arc(ex2 + 2, ey2 - 3, 1.8, 0, 7); ctx.fill();
    } else if (e === 'happy') {
      line(ell(32, 0, 10, 8, 0, 8, Math.PI + 0.25, Math.PI * 2 - 0.25), { lw: 3.6 });
      line(ell(-6, -2, 8, 7, 0, 8, Math.PI + 0.25, Math.PI * 2 - 0.25), { lw: 3.4 });
    } else { // closed, peaceful (looking down)
      line(ell(32, -4, 10, 6, 0, 8, 0.25, Math.PI - 0.25), { lw: 3.6 });
      line(ell(-6, -6, 8, 5, 0, 8, 0.25, Math.PI - 0.25), { lw: 3.4 });
    }
    const br = o.brow ?? 0;
    line([[20, -26 - br], [33, -31 - br], [46, -28 - br]], { lw: 4.4, ink: C.hair });
    line([[-16, -26 - br], [-6, -30 - br], [4, -28 - br]], { lw: 4, ink: C.hair });
    line([[52, 2], [62, 18], [52, 22]], { lw: 3 });
    const m = o.mouth ?? 'smile';
    if (m === 'smile') line(ell(28, 36, 15, 8, 0, 8, 0.35, Math.PI - 0.35), { lw: 3.4 });
    else if (m === 'laugh') shape(ell(28, 36, 16, 13, 0, 12, 0, Math.PI).concat([[12, 36]]), C.mouth, { lw: 3, wash: false });
    else if (m === 'kiss') shape(ell(42, 38, 6, 7), C.mouth, { lw: 2.6, wash: false });
    else line(ell(30, 38, 10, 4, 0, 6, 0.4, Math.PI - 0.4), { lw: 3.2 });
    if (o.tear > 0 && o.tear < 1) {
      const k = o.tear, tx = lerp(40, 48, k), ty = lerp(6, 52, io(k)), r = 6;
      ctx.globalAlpha = Math.min(1, k * 6, (1 - k) * 5);
      shape([[tx, ty - r * 2.2], [tx + r, ty], [tx, ty + r], [tx - r, ty]], C.tear, { lw: 2, ink: '#5b8fb0', wash: false, jit: 0.3 });
      ctx.globalAlpha = 1;
    }
  }
  shape([[-70, 12], [-72, -30], [-58, -66], [-24, -88], [18, -91], [52, -76], [68, -48], [66, -30], [46, -44], [14, -50], [-20, -45], [-44, -30], [-52, -8], [-58, 14]], F(C.hair));
  ctx.restore();
}

// ---------- Humaira (toddler) ----------
function humairaHead(x, y, s, rot, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s * (o.dir ?? 1), s);
  // ponytail + ribbon (behind the head top)
  shape(ell(-26, -66, 15, 22, -0.5), F(C.hair));
  shape(ell(-44, 8, 11, 15), F(C.skin), { lw: 3 });
  shape(ell(0, 0, 58, 55), F(C.skin));
  if (feat()) {
    shape(ell(30, 20, 15, 9), C.blush, { ink: null, wash: false });
    shape(ell(-8, 22, 11, 8), C.blush, { ink: null, wash: false });
    const e = o.eyes ?? 'open', lx = o.look?.[0] ?? 0, ly = o.look?.[1] ?? 0;
    if (e === 'open') {
      shape(ell(24 + lx, -2 + ly, 7.5, 9), INK, { ink: null, wash: false, jit: 0.3 });
      shape(ell(-8 + lx, -2 + ly, 6.5, 8.5), INK, { ink: null, wash: false, jit: 0.3 });
      ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(26 + lx, -6 + ly, 2.6, 0, 7); ctx.arc(-6 + lx, -6 + ly, 2.2, 0, 7); ctx.fill();
    } else if (e === 'happy') {
      line(ell(24, 2, 9, 8, 0, 8, Math.PI + 0.25, Math.PI * 2 - 0.25), { lw: 3.6 });
      line(ell(-8, 2, 8, 7, 0, 8, Math.PI + 0.25, Math.PI * 2 - 0.25), { lw: 3.4 });
    } else {
      line(ell(24, -2, 9, 5, 0, 8, 0.25, Math.PI - 0.25), { lw: 3.4 });
      line(ell(-8, -2, 8, 5, 0, 8, 0.25, Math.PI - 0.25), { lw: 3.2 });
    }
    line([[42, 8], [46, 14], [41, 16]], { lw: 2.6, inkA: 0.7 });
    const m = o.mouth ?? 'smile';
    if (m === 'laugh') shape(ell(24, 26, 12, 11, 0, 10, 0, Math.PI).concat([[12, 26]]), C.mouth, { lw: 2.8, wash: false });
    else if (m === 'smile') line(ell(24, 24, 10, 6, 0, 8, 0.4, Math.PI - 0.4), { lw: 3 });
    else if (m === 'o') shape(ell(26, 28, 5, 6), C.mouth, { lw: 2.4, wash: false });
    else line(ell(24, 27, 6, 3, 0, 6, 0.4, Math.PI - 0.4), { lw: 2.8 });
  }
  shape([[-60, 10], [-62, -24], [-44, -50], [-10, -62], [26, -58], [50, -40], [58, -16], [48, -20], [36, -30], [22, -22], [8, -34], [-12, -28], [-30, -20], [-46, -2], [-52, 18]], F(C.hair));
  // ribbon bow on the ponytail
  shape(ell(-30, -54, 13, 8, 0.6), F(C.ribbon), { lw: 3 });
  shape(ell(-8, -60, 13, 8, -0.4), F(C.ribbon), { lw: 3 });
  shape(ell(-19, -57, 5.5, 5.5), F(C.ribbon), { lw: 2.6 });
  ctx.restore();
}

// ---------- newborn (knitted cap) ----------
function babyHead(x, y, s, rot, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s * (o.dir ?? 1), s);
  shape(ell(0, 6, 44, 42), F(C.skinL));
  if (feat()) {
    shape(ell(18, 20, 10, 6), C.blush, { ink: null, wash: false });
    shape(ell(-14, 20, 9, 6), C.blush, { ink: null, wash: false });
    line(ell(14, 8, 8, 4, 0, 8, 0.25, Math.PI - 0.25), { lw: 3 });
    line(ell(-12, 8, 7, 4, 0, 8, 0.25, Math.PI - 0.25), { lw: 3 });
    line(ell(2, 27, 5, 3, 0, 6, 0.4, Math.PI - 0.4), { lw: 2.6 });
  }
  const capPts = ell(0, 2, 48, 46, 0, 22, Math.PI + 0.12, Math.PI * 2 - 0.12).concat([[44, 0], [-44, 0]]);
  shape(capPts, F(C.cap));
  if (feat()) for (let i = -3; i <= 3; i++) line([[i * 12, -2], [i * 11, -30 + Math.abs(i) * 3]], { lw: 1.8, inkA: 0.35 });
  shape(capsule(-46, -2, 46, -2, 7, 7, 6), F(C.cap), { lw: 3 });
  shape(ell(-4, -50, 13, 12), F(C.cap), { lw: 3 });
  ctx.restore();
}

// ---------- heart (drawn, not emoji) ----------
function heart(x, y, s, col) {
  const pts = [];
  for (let i = 0; i < 40; i++) {
    const t = Math.PI * 2 * i / 40;
    pts.push([x + 16 * Math.pow(Math.sin(t), 3) * s, y - (13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t)) * s]);
  }
  shape(pts, col, { lw: 3.2, washC: 'rgba(150,30,50,0.2)' });
}
