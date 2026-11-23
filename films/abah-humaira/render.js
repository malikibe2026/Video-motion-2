// render.js — Playwright frame renderer for film.html (port of the motion-design render_template to Node).
// node render.js probe t1 t2 ...        -> probe/p_XX.png + probe/sheet.png
// node render.js chunk k n             -> frames for chunk k of n into frames/ (SUB subframes blended later)
// node render.js encode                -> out/video.mp4 from frames/ (tmix subframes, TV-range BT.709)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const HERE = __dirname, URL = 'file://' + path.join(HERE, 'film.html');
const FPS = 30, T = 55, SUB = 2, SHUTTER = 0.5;
const CUTS = []; // the film has no hard cuts (all watercolour reveals)

async function open() {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files', '--force-color-profile=srgb', '--font-render-hinting=none'] });
  const pg = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const errs = [];
  pg.on('pageerror', e => errs.push(String(e)));
  pg.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push('console: ' + m.text()); });
  await pg.goto(URL);
  await pg.waitForFunction('window.ready === true', null, { timeout: 120000 });
  return { b, pg, errs };
}
async function shot(pg, t, file, type = 'png') {
  await pg.evaluate(t => window.seek(t), t);
  await pg.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
  const el = await pg.$('#stage');
  await el.screenshot({ path: file, type, ...(type === 'jpeg' ? { quality: 94 } : {}) });
}
(async () => {
  const [cmd, ...rest] = process.argv.slice(2);
  if (cmd === 'probe') {
    const dir = path.join(HERE, 'probe', process.env.P || 'a'); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const { b, pg, errs } = await open();
    const times = rest.map(Number);
    for (let i = 0; i < times.length; i++) await shot(pg, times[i], path.join(dir, `p_${String(i).padStart(2, '0')}.png`));
    await b.close();
    if (errs.length) console.log('PAGE ERRORS:', errs.slice(0, 8));
    const cols = Math.min(4, times.length), rows = Math.ceil(times.length / cols);
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', path.join(dir, 'p_%02d.png'), '-vf', `scale=300:-1,tile=${cols}x${rows}:padding=6:color=white`, '-frames:v', '1', path.join(dir, 'sheet.png')]);
    console.log('probe ->', path.join(dir, 'sheet.png'));
  } else if (cmd === 'chunk') {
    const k = +rest[0], n = +rest[1], N = Math.round(T * FPS);
    const a = Math.floor(N * k / n), e = Math.floor(N * (k + 1) / n);
    const dir = path.join(HERE, 'frames'); fs.mkdirSync(dir, { recursive: true });
    const offs = [...Array(SUB).keys()].map(j => (j - (SUB - 1) / 2) * SHUTTER / (FPS * SUB));
    const { b, pg, errs } = await open();
    for (let i = a; i < e; i++) {
      for (let j = 0; j < SUB; j++) {
        const t = Math.min(T - 1e-3, Math.max(0, i / FPS + offs[j]));
        await shot(pg, t, path.join(dir, `s_${String(i * SUB + j).padStart(6, '0')}.jpg`), 'jpeg');
      }
      if ((i - a) % 60 === 0) console.log(`chunk ${k}: frame ${i - a}/${e - a}`);
    }
    await b.close();
    if (errs.length) console.log('PAGE ERRORS:', errs.slice(0, 8));
    console.log(`chunk ${k} done`);
  } else if (cmd === 'encode') {
    fs.mkdirSync(path.join(HERE, 'out'), { recursive: true });
    const N = Math.round(T * FPS), have = fs.readdirSync(path.join(HERE, 'frames')).length;
    if (have !== N * SUB) { console.log(`frame count mismatch: ${have} vs ${N * SUB}`); process.exit(1); }
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(FPS * SUB), '-i', path.join(HERE, 'frames/s_%06d.jpg'),
      '-vf', `tmix=frames=${SUB},select='eq(mod(n\\,${SUB})\\,${SUB - 1})',setpts=N/${FPS}/TB,scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p`,
      '-r', String(FPS), '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-color_range', 'tv', '-colorspace', 'bt709', path.join(HERE, 'out/video.mp4')]);
    console.log('video ->', path.join(HERE, 'out/video.mp4'));
  }
})();
