// Guna (pelayan: python3 -m http.server 8767 --bind 127.0.0.1 dalam folder ini):
//   node render.js schedule              -> jadual peristiwa untuk skrip audio
//   node render.js probe 1,5.5,20 probe  -> gambar pegun pada masa tertentu (saat)
//   node render.js full fr 0 600         -> bingkai 0..599 ke fr/
// Pemboleh ubah: FILM (fail html), VW/VH (saiz), SUB (bilangan subbingkai motion blur).
// Dengan SUB>1, bingkai dalam tetingkap `blur` jadual dirender sebagai SUB subbingkai
// (pengatup 180 darjah) ke <out>_sub/, kemudian digabung oleh blend.py.
let pw;
try { pw = require('playwright'); } catch { pw = require('/opt/node-tools/node_modules/playwright'); }
const fs = require('fs'), path = require('path');
const [, , mode, a, b, c] = process.argv;
const FPS = 30, FILM = process.env.FILM || 'film.html', URL = 'http://127.0.0.1:8767/' + FILM;
const SCHED = FILM === 'film.html' ? 'schedule.json' : FILM.replace('.html', '_schedule.json');
const SUB = +(process.env.SUB || 1);
(async () => {
  const browser = await pw.chromium.launch({ args: ['--font-render-hinting=none', '--force-color-profile=srgb'] });
  const VW = +(process.env.VW || 1920), VH = +(process.env.VH || 1080);
  const page = await browser.newPage({ viewport: { width: VW, height: VH }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.log('PAGEERROR', e.message));
  await page.goto(URL);
  const info = await page.evaluate(() => window.ready);
  if (mode === 'schedule') {
    fs.writeFileSync(SCHED, JSON.stringify(info));
    console.log(SCHED, 'jumlah saat', info.total.toFixed(2), 'halaman', info.pages || info.scenes.length, 'bingkai', Math.ceil(info.total * FPS));
    await browser.close(); return;
  }
  let frames, out;
  if (mode === 'probe') { out = b || 'probe'; frames = a.split(',').map(s => Math.round(parseFloat(s) * FPS)); }
  else { out = a; const n = Math.ceil(info.total * FPS); frames = []; for (let f = +b; f < Math.min(+c, n); f++) frames.push(f); }
  fs.mkdirSync(out, { recursive: true });
  const blur = (mode === 'full' && SUB > 1 && info.blur) || [];
  if (blur.length) fs.mkdirSync(out + '_sub', { recursive: true });
  const shot = async (t, file) => {
    await page.evaluate(t => { seek(t); return new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); }, t);
    await page.screenshot({ path: file });
  };
  let nb = 0;
  for (const f of frames) {
    const t = f / FPS, name = 'f' + String(f).padStart(5, '0');
    if (blur.some(([x, y]) => t >= x && t <= y)) {
      for (let j = 0; j < SUB; j++) await shot(t + ((j + .5) / SUB - .5) * .5 / FPS, path.join(out + '_sub', `${name}_${j}.png`));
      nb++;
    } else await shot(t, path.join(out, name + '.png'));
  }
  console.log('siap', frames.length, 'blur', nb);
  await browser.close();
})();
