// S1 hospital (0-8), S2 little hand (8-13.1)

// ---------- S1: first meeting ----------
const R = (x0, y0, x1, y1) => [[x0, y0], [x1, y0], [x1, y1], [x0, y1]];
function abahTorso(cx, top, w, br = 1, lean = 0) {
  ctx.save(); ctx.translate(cx, 2000); ctx.rotate(lean); ctx.scale(1, br); ctx.translate(-cx, -2000);
  const x0 = cx - w / 2, x1 = cx + w / 2;
  shape([[x0, top + 10], [cx, top - 12], [x1, top + 10], [x1 + 20, 2100], [x0 - 20, 2100]], F(C.shirt), { round: [w * 0.32, 60, w * 0.32, 0, 0] });
  if (feat()) {
    shape([[cx - 60, top - 8], [cx, top + 80], [cx - 34, top + 104], [cx - 82, top + 6]], C.shirtD, { round: 10, lw: 3 });
    shape([[cx + 60, top - 8], [cx, top + 80], [cx + 34, top + 104], [cx + 82, top + 6]], C.shirtD, { round: 10, lw: 3 });
    line([[cx + 2, top + 110], [cx + 6, 2000]], { lw: 2.4, inkA: 0.4 });
    [180, 320, 460].forEach(dy => { ctx.fillStyle = '#d6c4a4'; ctx.beginPath(); ctx.arc(cx + 18, top + dy, 7, 0, 7); ctx.fill(); });
  }
  ctx.restore();
}
function S1(u) {
  ctx.fillStyle = vgrad(0, H, [[0, '#f6dfc6'], [1, '#e9c3a0']]); ctx.fillRect(-500, -500, W + 1000, H + 1000);
  const k0 = io(seg(u, 0.2, 3.4));
  const kiss = spring(u, 5.6, 0.45, 0.95);
  const B = [lerp(590, 600, kiss), lerp(1240, 1010, kiss)], bRot = lerp(0.18, 0.30, kiss);
  const bp = (lx, ly) => [B[0] + lx * Math.cos(bRot) - ly * Math.sin(bRot), B[1] + lx * Math.sin(bRot) + ly * Math.cos(bRot)];
  const BhRest = [590 - 235 * Math.cos(0.18), 1240 - 235 * Math.sin(0.18)];
  const z = logZoom(2.0, 1.0, k0) * (1 + 0.035 * seg(u, 3.4, 8.5));
  ctx.save(); cam(z, lerp(BhRest[0] + 40, 560, k0), lerp(BhRest[1] - 30, 1000, k0));

  // window + light
  shape(R(40, 180, 520, 1120), '#fff4da', { lw: 4, sharp: true });
  ctx.save(); ctx.beginPath(); ctx.rect(40, 180, 480, 940); ctx.clip();
  ctx.fillStyle = vgrad(180, 1120, [[0, '#fff7e2'], [1, '#ffd9a6']]); ctx.fillRect(40, 180, 480, 940);
  glow(300, 600, 420, 'rgba(255,240,200,A)', 0.9);
  ctx.restore();
  line([[280, 182], [280, 1118]], { lw: 12, ink: '#f7ecdc' }); line([[280, 182], [280, 1118]], { lw: 3 });
  line([[42, 650], [518, 650]], { lw: 12, ink: '#f7ecdc' }); line([[42, 650], [518, 650]], { lw: 3 });
  shape([[20, 1120], [550, 1120], [564, 1156], [6, 1156]], '#f1e2cb', { lw: 3.4, sharp: true });
  const sw = Math.sin(u * 0.7) * 10;
  shape([[-20, 150], [120, 150], [100 + sw, 520], [125 + sw * 1.4, 900], [85 + sw, 1210], [-30, 1220]], 'rgba(255,252,244,0.72)', { inkA: 0.35, lw: 2.6 });
  shape([[420, 1055], [500, 1055], [488, 1120], [432, 1120]], '#cf8f6a', { lw: 3, sharp: true });
  for (let i = 0; i < 5; i++) { const a = -2.2 + i * 0.35 + Math.sin(u * 0.8 + i) * 0.04; shape(ell(460 + Math.cos(a) * 38, 1045 + Math.sin(a) * 38, 30, 11, a), '#8fae7c', { lw: 2.6 }); }
  ctx.save(); ctx.globalCompositeOperation = 'screen';
  for (let i = 0; i < 4; i++) {
    const a = 0.10 + 0.06 * Math.sin(u * 0.5 + i * 1.7);
    ctx.fillStyle = `rgba(255,226,170,${a})`;
    ctx.beginPath(); ctx.moveTo(100 + i * 110, 210); ctx.lineTo(220 + i * 110, 210); ctx.lineTo(980 + i * 60, 1900); ctx.lineTo(700 + i * 60, 1900); ctx.fill();
  }
  ctx.restore();
  shape(R(-60, 1600, 200, 2000), '#d7ae86', { lw: 3.6, sharp: true });
  shape([[-60, 1580], [190, 1580], [200, 1610], [-60, 1610]], '#f3b8c1', { lw: 3, round: 8 });

  // ---- Abah (storybook proportions: big head, compact body) ----
  const br = 1 + 0.006 * Math.sin(u * Math.PI * 2 / 3.6);
  const lean = -0.05 * kiss;
  const Hc = [lerp(565, 430, kiss), lerp(700, 785, kiss)], hRot = lerp(0.04, -0.35, kiss);
  shape(capsule(565, 930, lerp(565, 470, kiss), Hc[1] + 120, 58, 56), F(C.skin));
  abahTorso(565, 900, 500, br, lean);
  // cradling arm (screen left): the baby's head rests in the crook
  const crook = bp(-190, 60);
  arm([360, 1010], crook, 200, 190, 1, { r0: 56, r1: 50, r2: 44 });
  shape(ell(crook[0], crook[1], 42, 38), F(C.skin));
  // bundle
  shape(ell(B[0], B[1], 235, 128, bRot), F(C.blanket), { washC: 'rgba(160,120,90,0.18)', washW: 22 });
  shape([bp(-130, -92), bp(40, -108), bp(160, -40), bp(60, 8), bp(-110, -18)], F('#f7efe2'), { lw: 3 });
  line([bp(-90, 30), bp(40, 62), bp(160, 44)], { lw: 2.2, inkA: 0.35 });
  const wig = Math.sin(u * 1.6) * 0.15;
  hand(...bp(-50, -60), 0.7, bRot - 1.3 + wig, { c: C.skinL });
  const Bh = bp(-235, -10);
  babyHead(Bh[0], Bh[1], 1.8, bRot - 1.15, { dir: 1 });
  // holding arm (screen right): forearm across the blanket
  const handO = bp(10, 40);
  arm([770, 1010], handO, 230, 230, -1, { r0: 56, r1: 50, r2: 44 });
  hand(handO[0], handO[1], 1.55, Math.PI + bRot);
  abahHead(Hc[0], Hc[1], 2.25, hRot, { dir: -1, eyes: u < 5.5 ? 'open' : 'closed', look: [4, 7], mouth: kiss > 0.65 ? 'kiss' : 'smile', tear: seg(u, 3.5, 5.6), brow: 2 * seg(u, 2.5, 4) });
  ctx.restore();
  glow(300, 500, 900, 'rgba(255,214,150,A)', 0.28);
}

// ---------- S2: the little hand ----------
let S2bg = null, S2fg = null;
function S2(u) {
  if (!S2bg) { S2bg = mkCanvas(); S2fg = mkCanvas(); }
  const rack = io(seg(u, 3.0, 4.4));
  // background: Abah smiling, out of focus at first
  withCtx(S2bg, () => {
    ctx.fillStyle = vgrad(0, H, [[0, '#f3d3b0'], [1, '#f6e6d2']]); ctx.fillRect(0, 0, W, H);
    glow(820, 300, 700, 'rgba(255,232,190,A)', 0.9);
    ctx.save(); cam(1.0 + 0.04 * seg(u, 0, 5), 540, 900);
    shape([[160, 820], [300, 700], [800, 690], [980, 820], [1040, 1300], [100, 1300]], C.shirt);
    abahHead(560, 470, 2.6, 0.05, { dir: -1, eyes: rack > 0.5 ? 'happy' : 'open', look: [6, 10], mouth: 'smile', brow: 2 });
    ctx.restore();
  });
  // foreground: blanket + baby hand + Abah's finger
  withCtx(S2fg, () => {
    ctx.save(); cam(1.0 + 0.05 * seg(u, 0, 5), 540, 1200);
    shape([[-60, 1180], [300, 1120], [700, 1160], [1140, 1100], [1160, 2000], [-80, 2000]], C.blanket, { washC: 'rgba(160,120,90,0.18)', washW: 30 });
    line([[0, 1420], [320, 1360], [640, 1450], [1100, 1380]], { lw: 2.6, inkA: 0.35 });
    line([[60, 1700], [420, 1600], [900, 1680]], { lw: 2.4, inkA: 0.3 });
    // sleeve + wrist
    shape([[300, 1500], [520, 1470], [560, 1650], [280, 1680]], C.blanket, { lw: 3.4 });
    shape(capsule(420, 1520, 470, 1380, 62, 66), C.skinL);
    // palm
    const px = 480, py = 1290;
    shape(ell(px, py, 105, 92, -0.15), C.skinL);
    // Abah's finger slides in from the right and rests across the palm
    const fin = spring(u, 0.5, 0.75, 0.86);
    const fx = lerp(1250, 470, fin), fy = 1250;
    shape(capsule(fx, fy, fx + 700, fy + 40, 46, 56), C.skin);
    shape(ell(fx + 12, fy - 6, 22, 30, 0.1), '#f1d2bb', { lw: 2.6 });
    line([[fx + 150, fy - 30], [fx + 158, fy + 30]], { lw: 2.2, inkA: 0.5 });
    // thumb
    const cT = spring(u, 2.35, 1.2, 0.8);
    const tA = lerp(-2.3, -0.9, cT);
    shape(capsule(px - 70, py + 20, px - 70 + Math.cos(tA) * 95, py + 20 + Math.sin(tA) * 95, 30, 24), C.skinL);
    // four fingers curl over Abah's finger, staggered
    for (let i = 0; i < 4; i++) {
      const c = spring(u, 2.1 + i * 0.07, 1.25, 0.8);
      const bx = px - 60 + i * 42, by = py - 70 + Math.abs(i - 1.5) * 8;
      const a = lerp(-1.75 + (i - 1.5) * 0.12, 1.35, c), L = lerp(118 - Math.abs(i - 1.5) * 14, 80, c);
      shape(capsule(bx, by, bx + Math.cos(a) * L, by + Math.sin(a) * L, 22, 18), C.skinL);
      if (c > 0.6) line([[bx + Math.cos(a) * L * 0.55 - 8, by + Math.sin(a) * L * 0.55], [bx + Math.cos(a) * L * 0.55 + 10, by + Math.sin(a) * L * 0.55 - 4]], { lw: 1.8, inkA: 0.45 });
    }
    // gentle squeeze pulse after the grip
    ctx.restore();
  });
  ctx.save(); ctx.filter = `blur(${lerp(16, 0, rack)}px)`; ctx.drawImage(S2bg, 0, 0); ctx.restore();
  ctx.save(); ctx.filter = `blur(${lerp(0, 7, rack)}px)`; ctx.globalAlpha = lerp(1, 0.92, rack); ctx.drawImage(S2fg, 0, 0); ctx.restore();
  glow(860, 260, 800, 'rgba(255,220,160,A)', 0.25);
}
