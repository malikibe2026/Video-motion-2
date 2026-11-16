// node render.js probe out.png 1,5,9      -> lembaran kontak
// node render.js chunk out.mp4 f0 f1      -> segmen video (bingkai f0..f1-1)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');
const [, , mode, out, a, b] = process.argv;
const FPS = 30, URL = "http://127.0.0.1:8777/" + (process.env.PAGE || "humaira.html");
(async () => {
  const browser = await chromium.launch({ args: ['--font-render-hinting=none', '--force-color-profile=srgb', '--disable-gpu-vsync'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.log('PAGEERROR', e.message));
  page.on('console', m => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
  await page.goto(URL); await page.waitForFunction(() => window.ready === true);
  const grab = async t => {
    const d = await page.evaluate(t => { seek(t); return document.getElementById('c').toDataURL('image/jpeg', 0.95); }, t);
    return Buffer.from(d.split(',')[1], 'base64');
  };
  if (mode === 'probe') {
    const ts = a.split(',').map(Number); const dir = out + '_f'; fs.mkdirSync(dir, { recursive: true });
    for (let i = 0; i < ts.length; i++) fs.writeFileSync(path.join(dir, String(i).padStart(3, '0') + '.jpg'), await grab(ts[i]));
    const cols = Math.min(ts.length, 5);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-i', path.join(dir, '%03d.jpg'), '-vf', `scale=360:-1,tile=${cols}x${Math.ceil(ts.length / cols)}:padding=6:color=white`, '-frames:v', '1', out]);
    await new Promise(r => ff.on('close', r));
  } else {
    const f0 = +a, f1 = +b;
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
      '-vf', 'scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
      '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    const t0 = Date.now();
    for (let f = f0; f < f1; f++) {
      const buf = await grab(f / FPS);
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if ((f - f0) % 150 === 0) console.log(out, f, ((Date.now() - t0) / 1000).toFixed(0) + 's');
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
