// S3 tickle (13.1), S4 lap + bunny (20.9), S5 sunset walk (27.9), S6 hug + kiss (34.5), S7 silhouette (39.0) + text

// ---------- living room set (shared by S3 and S4) ----------
function room(u) {
  ctx.fillStyle = vgrad(0, 1200, [[0, '#f3dec7'], [1, '#e9ccb0']]); ctx.fillRect(-400, -400, W + 800, 1700);
  // window top right
  shape([[660, 220], [1010, 220], [1010, 860], [660, 860]], '#fff2d6', { lw: 4 });
  ctx.save(); smoothPath([[660, 220], [1010, 220], [1010, 860], [660, 860]]); ctx.clip();
  ctx.fillStyle = vgrad(220, 860, [[0, '#fff6df'], [1, '#ffd8a3']]); ctx.fillRect(660, 220, 350, 640);
  glow(840, 520, 360, 'rgba(255,244,210,A)', 0.9); ctx.restore();
  line([[835, 222], [835, 858]], { lw: 9, ink: '#f7ecdc' }); line([[835, 222], [835, 858]], { lw: 3 });
  const sw = Math.sin(u * 0.6) * 8;
  shape([[1000, 190], [1120, 190], [1120, 960], [990 + sw, 960], [1010 + sw, 560]], 'rgba(255,251,243,0.7)', { inkA: 0.3, lw: 2.4 });
  // plant
  shape([[90, 980], [230, 980], [212, 1150], [108, 1150]], '#cd8a64', { lw: 3.4 });
  for (let i = 0; i < 7; i++) { const a = -2.6 + i * 0.32 + Math.sin(u * 0.7 + i) * 0.04; shape(ell(160 + Math.cos(a) * 80, 960 + Math.sin(a) * 90, 62, 20, a), i % 2 ? '#8eae7b' : '#7c9c6c', { lw: 2.8 }); }
  // sofa
  shape([[40, 760], [1040, 760], [1060, 1060], [20, 1060]], '#bdb6ad', { lw: 3.6, washC: 'rgba(60,50,40,0.14)' });
  shape([[0, 900], [140, 880], [150, 1180], [0, 1190]], '#b0a99f', { lw: 3.4 });
  shape([[940, 880], [1080, 900], [1080, 1190], [930, 1180]], '#b0a99f', { lw: 3.4 });
  shape(ell(330, 860, 170, 85, -0.05), '#c9c2b8', { lw: 3 }); shape(ell(720, 860, 170, 85, 0.05), '#c9c2b8', { lw: 3 });
  shape([[120, 1040], [960, 1040], [960, 1180], [120, 1180]], '#c4bdb3', { lw: 3.4 });
  // floor + rug
  ctx.fillStyle = vgrad(1170, H, [[0, '#d8b18a'], [1, '#c99d74']]); ctx.fillRect(-400, 1170, W + 800, H);
  line([[-100, 1300], [1200, 1290]], { lw: 2, inkA: 0.25 }); line([[-100, 1520], [1200, 1530]], { lw: 2, inkA: 0.25 });
  shape(ell(540, 1480, 600, 300), '#f0e5d3', { lw: 3.4, washC: 'rgba(150,110,70,0.16)' });
  for (let i = -3; i <= 3; i++) line([[540 + i * 150 - 60, 1480], [540 + i * 150, 1400], [540 + i * 150 + 60, 1480], [540 + i * 150, 1560], [540 + i * 150 - 60, 1480]], { lw: 2, inkA: 0.25, ink: '#a5704f' });
  glow(840, 520, 1000, 'rgba(255,226,170,A)', 0.22);
}

// ---------- S3: tickles ----------
function sleeveArm(S, Hn, a, b, bend, r = 50) { const E = arm(S, Hn, a, b, bend, { r0: r, r1: r * 0.9, r2: r * 0.8 }); return E; }
function kidLimb(S, Hn, a, b, bend, r, end) { // short chubby limb with a hand or a sock
  const E = ik(S, Hn, a, b, bend);
  shape(capsule(S[0], S[1], E[0], E[1], r, r * 0.92), F(C.skin)); shape(capsule(E[0], E[1], Hn[0], Hn[1], r * 0.92, r * 0.85), F(C.skin));
  if (end === 'sock') shape(ell(Hn[0], Hn[1], r * 1.15, r * 0.85, Math.atan2(Hn[1] - E[1], Hn[0] - E[0])), F('#fbf4ea'), { lw: 3 });
  else shape(ell(Hn[0], Hn[1], r * 0.95, r * 0.85), F(C.skin), { lw: 3 });
}
function S3(u) {
  const z = logZoom(1.42, 1.32, io(u / 8.3));
  ctx.save(); cam(z, 560 + 30 * io(u / 8.3), 1150);
  room(u);
  const bursts = [0.5, 2.6, 4.7, 6.6];
  let L = 0; for (const s of bursts) L = Math.max(L, Math.sin(Math.PI * clamp((u - s) / 1.4)));
  const laugh = L, bob = -5 * laugh * Math.abs(Math.sin(u * 10)), hb = -6 * laugh * Math.abs(Math.sin(u * 12));
  // Abah kneeling behind her (legs folded under him)
  shape(capsule(700, 1330, 930, 1350, 78, 70), C.trouser);
  shape(capsule(930, 1350, 1010, 1420, 66, 56), C.trouser);
  ctx.save(); ctx.translate(780, 1340); ctx.rotate(-0.16); ctx.translate(-780, -1340 - bob);
  shape([[600, 980], [940, 980], [955, 1345], [600, 1345]], C.shirt, { round: [140, 140, 40, 40] });
  shape([[730, 984], [770, 1060], [748, 1078], [712, 990]], C.shirtD, { round: 8, lw: 3 }); shape([[810, 984], [770, 1060], [792, 1078], [828, 990]], C.shirtD, { round: 8, lw: 3 });
  ctx.restore();
  // Humaira lying on her back, head left
  const kick = 0.3 + laugh;
  for (let i = 0; i < 2; i++) {
    const a = -0.5 + i * 0.35 + Math.sin(u * 8 + i * Math.PI) * 0.45 * kick;
    kidLimb([600, 1330 + i * 22 + hb], [600 + Math.cos(a) * 125, 1330 + i * 22 + hb + Math.sin(a) * 125], 70, 66, 1, 29, 'sock');
  }
  shape([[390, 1250 + hb], [600, 1250 + hb], [630, 1400 + hb], [390, 1400 + hb]], C.pink, { round: [70, 60, 60, 70] });
  line([[430, 1270 + hb], [430, 1380 + hb]], { lw: 2.2, inkA: 0.35 });
  for (let i = 0; i < 2; i++) {
    const a = -1.75 + i * 0.55 + Math.sin(u * 7 + i * 2) * 0.4 * laugh;
    kidLimb([440 + i * 50, 1275 + hb + i * 10], [440 + i * 50 + Math.cos(a) * 105, 1275 + hb + i * 10 + Math.sin(a) * 105], 58, 56, i ? 1 : -1, 25, 'hand');
  }
  humairaHead(320, 1325 + hb, 1.6, -Math.PI / 2 + 0.22, { dir: 1, eyes: laugh > 0.3 ? 'happy' : 'open', look: [6, -2], mouth: laugh > 0.25 ? 'laugh' : 'smile' });
  // Abah's arms, hands tickling her tummy
  const wx = Math.sin(u * 28) * 7 * laugh, wy = Math.cos(u * 23) * 6 * laugh;
  sleeveArm([640, 1060 + bob], [505 + wx, 1300 + wy + hb], 170, 170, -1, 50);
  hand(505 + wx, 1300 + wy + hb, 1.55, 2.7);
  sleeveArm([900, 1080 + bob], [585 - wx, 1318 - wy + hb], 220, 220, 1, 50);
  hand(585 - wx, 1318 - wy + hb, 1.55, 2.5);
  abahHead(715, 830 + bob, 2.05, 0.34, { dir: -1, eyes: laugh > 0.35 ? 'happy' : 'open', look: [4, 9], mouth: laugh > 0.4 ? 'laugh' : 'smile' });
  ctx.restore();
}

// ---------- S4: in Abah's lap, the knitted bunny ----------
function bunny(x, y, s, rot) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s);
  shape(ell(-14, -78, 11, 34, -0.2), '#f6efe3', { lw: 3 }); shape(ell(14, -78, 11, 34, 0.2), '#f6efe3', { lw: 3 });
  shape(ell(-14, -78, 4, 22, -0.2), '#f3c3c8', { ink: null, wash: false }); shape(ell(14, -78, 4, 22, 0.2), '#f3c3c8', { ink: null, wash: false });
  shape(ell(0, 30, 40, 46), '#f6efe3', { lw: 3 });
  shape(ell(0, -28, 34, 30), '#f6efe3', { lw: 3 });
  for (let i = -2; i <= 2; i++) line([[i * 12, 6], [i * 11, 64]], { lw: 1.4, inkA: 0.25 });
  ctx.fillStyle = INK; ctx.beginPath(); ctx.arc(-11, -32, 3.5, 0, 7); ctx.arc(11, -32, 3.5, 0, 7); ctx.fill();
  shape(ell(0, -22, 5, 4), '#e98c99', { lw: 2 });
  ctx.restore();
}
function S4(u) {
  const z = logZoom(1.22, 1.34, io(u / 7.4));
  ctx.save(); cam(z, 540, 1230);
  room(u + 8);
  const grab = spring(u, 4.2, 0.9, 0.85);
  const bob = Math.sin(u * 3.0) * 26 * (1 - grab);
  const bH = [lerp(300, 540, grab), lerp(1180 + bob, 1350, grab)];
  // Abah sitting cross-legged, leaning on the sofa
  shape([[300, 990], [780, 990], [800, 1500], [280, 1500]], C.shirt, { round: [150, 150, 40, 40] });
  shape([[500, 994], [540, 1070], [518, 1088], [482, 1000]], C.shirtD, { round: 8, lw: 3 }); shape([[580, 994], [540, 1070], [562, 1088], [598, 1000]], C.shirtD, { round: 8, lw: 3 });
  shape(capsule(300, 1500, 770, 1545, 82, 78), C.trouser);
  shape(capsule(780, 1500, 310, 1545, 82, 78), '#6a4f3e');
  shape(ell(240, 1555, 58, 34, -0.2), '#3d2c22', { lw: 3 }); shape(ell(840, 1555, 58, 34, 0.2), '#3d2c22', { lw: 3 });
  // Humaira on his lap
  const reach = 1 - grab, laugh = reach * (0.5 + 0.5 * Math.sin(u * 5));
  for (let i = 0; i < 2; i++) kidLimb([490 + i * 100, 1450], [470 + i * 140, 1540], 50, 48, i ? -1 : 1, 28, 'sock');
  shape([[420, 1265], [660, 1265], [690, 1470], [390, 1470]], C.pink, { round: [80, 80, 50, 50] });
  // Abah's right arm (screen left) holds the bunny, then rests on his knee
  const aH = [lerp(bH[0] - 6, 330, grab), lerp(bH[1] + 40, 1480, grab)];
  sleeveArm([350, 1060], aH, 200, 200, -1, 52);
  bunny(bH[0], bH[1], 1.25 + 0.1 * grab, lerp(-0.25 + Math.sin(u * 3) * 0.12, 0.05, grab));
  hand(aH[0], aH[1], 1.55, lerp(-0.5, 0.4, grab));
  // her arms reach for it, then hug it
  kidLimb([450, 1300], [lerp(bH[0] + 50, 480, grab), lerp(bH[1] + 20, 1330, grab)], 60, 56, -1, 25, 'hand');
  kidLimb([630, 1300], [lerp(bH[0] + 70, 600, grab), lerp(bH[1] + 50, 1345, grab)], 70, 66, 1, 25, 'hand');
  // his left arm (screen right) around her waist
  sleeveArm([740, 1070], [650, 1420], 200, 200, 1, 52);
  hand(650, 1420, 1.55, 3.1);
  humairaHead(545, 1170, 1.55, -0.08 + 0.04 * Math.sin(u * 2.2), { dir: -1, eyes: grab > 0.6 ? 'closed' : (laugh > 0.4 ? 'happy' : 'open'), look: [8, 2], mouth: grab > 0.6 ? 'smile' : (laugh > 0.3 ? 'laugh' : 'smile') });
  abahHead(545, 840, 2.1, 0.18, { dir: -1, eyes: grab > 0.5 ? 'happy' : 'open', look: [2, 10], mouth: 'smile', brow: 2 * grab });
  ctx.restore();
}

// ---------- outdoor sunset set ----------
function palm(x, y, h, lean, u, col) {
  const top = [x + lean, y - h];
  line([[x, y], [x + lean * 0.4, y - h * 0.5], top], { lw: 16, ink: col, inkA: 1 });
  for (let i = 0; i < 7; i++) {
    const a = -Math.PI + i * (Math.PI / 6) + Math.sin(u * 0.8 + i) * 0.05;
    const L = 120 + (i % 2) * 30;
    const p1 = [top[0] + Math.cos(a) * L * 0.5, top[1] + Math.sin(a) * L * 0.3 - 20], p2 = [top[0] + Math.cos(a) * L, top[1] + Math.sin(a) * L * 0.5 + 30];
    shape([top, [p1[0], p1[1] - 18], p2, [p1[0] + 4, p1[1] + 22]], col, { ink: null, wash: false, jit: 0.8 });
  }
}
function sunsetSky(sunY, u, dusk = 0) {
  ctx.fillStyle = vgrad(-300, 1400, [[0, dusk ? '#6d4b6c' : '#f2a07b'], [0.45, dusk ? '#de7c62' : '#f9be8c'], [0.9, '#ffdca3'], [1, '#ffe7b8']]);
  ctx.fillRect(-600, -600, W + 1200, 2200);
  glow(W / 2 + 220 * (1 - dusk) * 0, sunY, 1100, 'rgba(255,214,150,A)', 0.8);
  ctx.fillStyle = '#fff3cf'; ctx.beginPath(); ctx.arc(540, sunY, 118, 0, 7); ctx.fill();
  glow(540, sunY, 330, 'rgba(255,250,225,A)', 0.9);
  // thin clouds
  for (let i = 0; i < 5; i++) {
    const cy = 300 + i * 150, cx = (i * 260 + u * (6 + i * 2)) % 1500 - 200;
    shape(ell(cx, cy, 220 - i * 18, 14, -0.02), dusk ? 'rgba(250,170,150,0.55)' : 'rgba(255,214,196,0.6)', { ink: null, wash: false, jit: 2 });
  }
}

// ---------- S5: walking home at sunset ----------
function S5(u) {
  ctx.save(); cam(1.0, 540, 960);
  ctx.save(); ctx.translate(220, 0); sunsetSky(1060, u); ctx.restore();
  const par = (k) => -u * k;
  // hills
  ctx.save(); ctx.translate(par(6), 0);
  shape([[-300, 1180], [100, 1110], [420, 1150], [760, 1090], [1100, 1140], [1500, 1100], [1500, 1400], [-300, 1400]], '#e3a083', { ink: null, wash: false });
  ctx.restore();
  ctx.save(); ctx.translate(par(16), 0);
  shape([[-300, 1250], [200, 1200], [600, 1240], [1000, 1190], [1500, 1230], [1500, 1500], [-300, 1500]], '#c7866b', { ink: null, wash: false });
  palm(140, 1230, 330, -30, u, '#8a5643'); palm(980, 1210, 380, 40, u, '#8a5643');
  ctx.restore();
  ctx.save(); ctx.translate(par(40), 0);
  ctx.fillStyle = vgrad(1300, H, [[0, '#b89058'], [1, '#8f6a3c']]); ctx.fillRect(-400, 1300, W + 1600, H);
  shape([[-300, 1440], [1500, 1420], [1500, 1520], [-300, 1540]], '#d4b07a', { ink: null, wash: false });
  ctx.restore();
  // Abah walking with Humaira asleep on his shoulder
  const ph = u * Math.PI * 2 / 1.2, bob = 6 * Math.cos(ph * 2);
  ctx.save(); ctx.translate(520, 1680); ctx.scale(1.18, 1.18); ctx.translate(-540, -1680 + bob);
  for (let i = 0; i < 2; i++) { // legs
    const a = Math.PI / 2 + Math.sin(ph + i * Math.PI) * 0.38;
    const hip = [520, 1240], kn = [hip[0] + Math.cos(a) * 220, hip[1] + Math.sin(a) * 220];
    const a2 = a + Math.max(0, Math.sin(ph + i * Math.PI + 1.2)) * 0.5;
    const ft = [kn[0] + Math.cos(a2) * 210, kn[1] + Math.sin(a2) * 210];
    const col = i ? C.trouser : '#6a4f3d';
    shape(capsule(hip[0], hip[1], kn[0], kn[1], 52, 44), col); shape(capsule(kn[0], kn[1], ft[0], ft[1], 44, 36), col);
    shape(ell(ft[0] + 28, ft[1] + 10, 50, 22), '#3a2a20', { lw: 3 });
  }
  shape([[410, 850], [630, 850], [640, 1270], [420, 1270]], C.shirt, { round: [120, 120, 30, 30] });
  // Humaira against his chest, head on his shoulder
  const sway = Math.sin(ph) * 6;
  shape(ell(660, 1010, 85, 135, -0.12), C.pink);
  for (let i = 0; i < 2; i++) kidLimb([650 + i * 34, 1100], [645 + i * 44 + sway, 1200], 52, 50, 1, 26, 'sock');
  humairaHead(615, 860, 1.25, -0.25, { dir: -1, eyes: 'closed', mouth: 'soft' });
  // his arm under her, other hand on her back
  sleeveArm([510, 920], [655, 1110], 160, 150, -1, 46);
  hand(655, 1110, 1.45, -0.2);
  hand(722, 965, 1.35, 1.9);
  abahHead(535, 700, 1.85, 0.12, { dir: 1, eyes: 'closed', mouth: 'smile' });
  ctx.restore();
  // foreground grass
  ctx.save(); ctx.translate(par(90) % 60, 0);
  for (let i = -2; i < 26; i++) {
    const gx = i * 48, s = Math.sin(u * 1.4 + i * 0.7) * 14;
    line([[gx, 1990], [gx + s * 0.5, 1800], [gx + s, 1640 + (i % 3) * 40]], { lw: 7, ink: '#6f5230', inkA: 1 });
  }
  ctx.restore();
  ctx.restore();
  glow(760, 1060, 900, 'rgba(255,196,130,A)', 0.25);
}

// ---------- S6: the hug and the forehead kiss ----------
function S6(u) {
  const z = logZoom(1.0, 1.08, io(u / 5));
  ctx.save(); cam(z, 540, 940);
  ctx.fillStyle = vgrad(0, H, [[0, '#f0a27f'], [0.5, '#fbc98e'], [1, '#f2a780']]); ctx.fillRect(-300, -300, W + 600, H + 600);
  const peak = Math.exp(-Math.pow((u - 4.5) / 0.6, 2));
  glow(570, 760, 900, 'rgba(255,240,200,A)', 0.75 + 0.25 * peak);
  const r = mulberry32(42);
  for (let i = 0; i < 14; i++) { // soft bokeh
    const bx = r() * W, by = r() * H, br = 30 + r() * 70;
    ctx.fillStyle = `rgba(255,236,200,${0.10 + 0.08 * Math.sin(u * 0.8 + i)})`; ctx.beginPath(); ctx.arc(bx + u * 4 * (r() - 0.5), by, br, 0, 7); ctx.fill();
  }
  const come = spring(u, 0.15, 0.6, 0.9), kiss = spring(u, 2.0, 0.55, 0.95);
  // his shoulders
  shape([[-80, 1220], [180, 1120], [520, 1150], [680, 1400], [720, 2000], [-80, 2000]], C.shirt);
  shape(capsule(380, 1150, 400, 1000, 70, 66), C.skin);
  // her body + arm around his neck
  const hx = lerp(800, 620, come), hy = lerp(960, 990, come);
  shape([[hx - 170, 1180], [hx + 190, 1180], [hx + 230, 2000], [hx - 210, 2000]], C.pink, { round: [150, 150, 0, 0] });
  const hug = lerp(0.7, 1, come);
  const hand2 = [lerp(hx - 150, 300, hug), lerp(1200, 1095, hug)];
  shape(capsule(hx - 90, 1240, hand2[0], hand2[1], 46, 40), C.skin);
  shape(ell(hx - 110, 1236, 70, 52, -0.3), C.pink, { lw: 3 });
  shape(ell(hand2[0], hand2[1], 40, 34, -0.4), C.skin, { lw: 3 });
  humairaHead(hx, hy, 2.0, 0.12, { dir: -1, eyes: come > 0.7 ? 'closed' : 'open', look: [6, 4], mouth: 'smile' });
  abahHead(lerp(390, 465, kiss), lerp(850, 840, kiss), 2.25, lerp(0.02, 0.22, kiss), { dir: 1, eyes: u > 1.4 ? 'closed' : 'open', look: [6, 4], mouth: kiss > 0.7 ? 'kiss' : 'smile' });
  ctx.restore();
  // lens bloom at the musical peak
  glow(570, 760, 600, 'rgba(255,250,230,A)', 0.35 * peak);
}

// ---------- S7: silhouette at sunset ----------
function S7(u) {
  const z = logZoom(1.08, 1.0, io(seg(u, 0, 11)));
  const sunY = 1150 + 80 * seg(u, 0, 16);
  ctx.save(); cam(z, 540, lerp(1060, 990, io(seg(u, 0, 11))));
  sunsetSky(sunY, u, 1);
  shape([[-300, 1250], [150, 1210], [500, 1245], [850, 1200], [1400, 1240], [1400, 1500], [-300, 1500]], '#8a5150', { ink: null, wash: false });
  shape([[-300, 1440], [200, 1380], [540, 1360], [880, 1385], [1400, 1450], [1400, 2600], [-300, 2600]], '#2a1712', { ink: null, wash: false });
  SIL.on = true;
  ctx.shadowColor = 'rgba(255,186,110,0.85)'; ctx.shadowBlur = 22;
  ctx.save(); ctx.translate(540, 1470); ctx.scale(1.22, 1.22); ctx.translate(-540, -1420);
  // Abah sitting, seen from behind, Humaira on his lap leaning back
  const br = Math.sin(u * Math.PI * 2 / 4) * 3;
  shape([[420, 1250 + br], [660, 1250 + br], [700, 1420], [380, 1420]], C.sil, { ink: null, wash: false });
  shape(capsule(540, 1250, 540, 1180, 38, 36), C.sil, { ink: null, wash: false });
  abahHead(540, 1110 + br * 0.5, 1.15, 0.03, { dir: 1 });
  humairaHead(668, 1232 + br, 0.92, -0.18 + 0.02 * Math.sin(u * 0.9), { dir: 1 });
  ctx.restore();
  ctx.shadowBlur = 0; ctx.shadowColor = 'transparent';
  SIL.on = false;
  // grass silhouette
  for (let i = 0; i < 26; i++) {
    const gx = i * 46 - 40, s = Math.sin(u * 1.1 + i * 0.6) * 10;
    line([[gx, 1700], [gx + s * 0.5, 1520], [gx + s, 1420 + (i % 4) * 22]], { lw: 6, ink: '#1e100c', inkA: 1 });
  }
  ctx.restore();
}

// ---------- screen-space overlays: the three lines + heart ----------
const CARDS = [
  { a: 39.6, b: 44.6, text: 'Humaira, mungkin suatu hari nanti kamu akan membesar dan tidak lagi mahu Abah mendukungmu…', font: 'italic 500 62px CG' },
  { a: 44.9, b: 50.0, text: 'Tetapi bagi Abah, kamu akan sentiasa menjadi anak kecil yang pertama mengajar Abah erti sebuah cinta.', font: 'italic 500 62px CG' },
  { a: 50.3, b: 99, text: 'Abah akan sentiasa ada untuk Humaira.', font: '600 72px CG', heart: true },
];
function wrapWords(words, font, maxW) {
  ctx.font = font; const lines = []; let cur = [];
  for (const w of words) { const test = cur.concat(w).join(' '); if (ctx.measureText(test).width > maxW && cur.length) { lines.push(cur); cur = [w]; } else cur.push(w); }
  if (cur.length) lines.push(cur); return lines;
}
function overlays(t) {
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  for (const c of CARDS) {
    if (t < c.a - 0.6 || t > c.b + 0.1) continue;
    const fin = seg(t, c.a - 0.5, c.a + 0.4), fout = 1 - seg(t, c.b - 0.6, c.b);
    // warm scrim behind the text
    const sa = 0.5 * Math.min(fin, fout);
    const g = ctx.createRadialGradient(540, 480, 40, 540, 480, 560);
    g.addColorStop(0, `rgba(48,22,14,${sa})`); g.addColorStop(1, 'rgba(48,22,14,0)');
    ctx.save(); ctx.translate(540, 480); ctx.scale(1, 0.5); ctx.translate(-540, -480); ctx.fillStyle = g; ctx.fillRect(-100, 0, W + 200, 1200); ctx.restore();
    const words = c.text.split(' '), lines = wrapWords(words, c.font, 800);
    const lh = parseInt(c.font.match(/(\d+)px/)[1]) * 1.32, y0 = 480 - (lines.length - 1) * lh / 2 - (c.heart ? 40 : 0);
    ctx.font = c.font; ctx.textBaseline = 'middle';
    let wi = 0;
    lines.forEach((ln, li) => {
      const y = y0 + li * lh, full = ln.join(' '), wFull = ctx.measureText(full).width;
      let x = 540 - wFull / 2;
      ctx.save(); ctx.beginPath(); ctx.rect(0, y - lh * 0.62, W, lh * 1.24); ctx.clip();
      for (const w of ln) {
        const k = out(seg(t, c.a + wi * 0.05, c.a + wi * 0.05 + 0.75));
        const dy = (1 - k) * lh * 0.8 - (1 - fout) * 10;
        ctx.globalAlpha = k * fout;
        ctx.fillStyle = 'rgba(30,12,8,0.55)'; ctx.fillText(w, x + 2, y + dy + 3);
        ctx.fillStyle = '#fff4e6'; ctx.fillText(w, x, y + dy);
        x += ctx.measureText(w + ' ').width; wi++;
      }
      ctx.restore();
    });
    ctx.globalAlpha = 1;
    if (c.heart) {
      const hk = spring(t, c.a + 0.9, 1.1, 0.75), pulse = 1 + 0.035 * Math.sin((t - c.a) * 3.2);
      if (hk > 0) { ctx.globalAlpha = clamp(hk) * fout; heart(540, y0 + lines.length * lh + 40, 3.4 * hk * pulse, '#e8546c'); ctx.globalAlpha = 1; }
    }
  }
  ctx.restore();
}
