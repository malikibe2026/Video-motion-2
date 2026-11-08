// Guna:
//   node render.js schedule              -> schedule.json (masa peristiwa untuk audio.py)
//   node render.js probe 1,5.5,20 probe  -> gambar pegun pada masa tertentu (saat)
//   node render.js full fr 0 600         -> bingkai 0..599 ke fr/
// Perlu pelayan: python3 -m http.server 8767 --bind 127.0.0.1 (dalam folder ini)
let pw;
try { pw = require('playwright'); } catch { pw = require('/opt/node-tools/node_modules/playwright'); }
const fs = require('fs'), path = require('path');
const [, , mode, a, b, c] = process.argv;
const FPS = 30, FILM = process.env.FILM || 'film.html', URL = 'http://127.0.0.1:8767/' + FILM;
const SCHED = FILM === 'film.html' ? 'schedule.json' : FILM.replace('.html', '_schedule.json');
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
  for (const f of frames) {
    await page.evaluate(t => { seek(t); return new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); }, f / FPS);
    await page.screenshot({ path: path.join(out, 'f' + String(f).padStart(5, '0') + '.png') });
  }
  console.log('siap', frames.length);
  await browser.close();
})();
