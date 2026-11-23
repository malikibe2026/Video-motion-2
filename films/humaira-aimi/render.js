// node render.js probe <style> t1 t2 ...   -> probe/<style>/sheet.png
// node render.js chunk <style> k n         -> frames/<style>/f_XXXXX.jpg (resumable)
// node render.js encode <style>            -> out/<style>.mp4 (original audio, no music, -14 LUFS)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const HERE = __dirname, FPS = 30, N = 1089;
async function open(style) {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files', '--force-color-profile=srgb', '--font-render-hinting=none'] });
  const pg = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const errs = []; pg.on('pageerror', e => errs.push(String(e)));
  await pg.goto('file://' + path.join(HERE, 'film.html') + '?s=' + style);
  await pg.waitForFunction('window.ready === true', null, { timeout: 120000 });
  return { b, pg, errs };
}
async function shot(pg, t, file) {
  await pg.evaluate(t => window.seek(t), t);
  await pg.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
  await (await pg.$('#stage')).screenshot({ path: file, type: 'jpeg', quality: 93 });
}
(async () => {
  const [cmd, style, ...rest] = process.argv.slice(2);
  if (cmd === 'probe') {
    const dir = path.join(HERE, 'probe', style); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const { b, pg, errs } = await open(style);
    for (let i = 0; i < rest.length; i++) await shot(pg, +rest[i], path.join(dir, `p_${String(i).padStart(2, '0')}.jpg`));
    await b.close(); if (errs.length) console.log('PAGE ERRORS', errs.slice(0, 5));
    const cols = Math.min(4, rest.length);
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', path.join(dir, 'p_%02d.jpg'), '-vf', `scale=300:-1,tile=${cols}x${Math.ceil(rest.length / cols)}:padding=6:color=white`, '-frames:v', '1', path.join(dir, 'sheet.png')]);
    console.log('probe ->', path.join(dir, 'sheet.png'));
  } else if (cmd === 'chunk') {
    const k = +rest[0], n = +rest[1], a = Math.floor(N * k / n), e = Math.floor(N * (k + 1) / n);
    const dir = path.join(HERE, 'frames', style); fs.mkdirSync(dir, { recursive: true });
    const { b, pg, errs } = await open(style);
    for (let i = a; i < e; i++) {
      const f = path.join(dir, `f_${String(i).padStart(5, '0')}.jpg`);
      if (fs.existsSync(f) && fs.statSync(f).size > 10000) continue;
      await shot(pg, i / FPS, f);
    }
    await b.close(); if (errs.length) console.log('PAGE ERRORS', errs.slice(0, 5));
    console.log(`chunk ${style} ${k} done`);
  } else if (cmd === 'encode') {
    fs.mkdirSync(path.join(HERE, 'out'), { recursive: true });
    const have = fs.readdirSync(path.join(HERE, 'frames', style)).length;
    if (have !== N) { console.log('frame count mismatch', have); process.exit(1); }
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(FPS), '-i', path.join(HERE, 'frames', style, 'f_%05d.jpg'), '-i', path.join(HERE, 'assets/audio.wav'),
      '-map', '0:v', '-map', '1:a', '-vf', 'scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p',
      '-af', 'loudnorm=I=-14:TP=-1.3:LRA=11', '-c:v', 'libx264', '-crf', '17', '-preset', 'slow', '-color_range', 'tv', '-colorspace', 'bt709',
      '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-shortest', '-movflags', '+faststart', path.join(HERE, 'out', style + '.mp4')]);
    console.log('->', path.join(HERE, 'out', style + '.mp4'));
  }
})();
