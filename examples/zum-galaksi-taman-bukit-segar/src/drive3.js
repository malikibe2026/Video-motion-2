const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const [,, mode, outDir, a, b] = process.argv;
const FPS = 30, T = 51.4, URL = 'http://127.0.0.1:8766/zoom3.html?p=1';
(async () => {
  const browser = await chromium.launch({ args: ['--font-render-hinting=none', '--force-color-profile=srgb'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.log('PAGEERROR', e.message));
  page.on('console', m => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
  await page.goto(URL);
  if (mode === 'collect') {
    await page.evaluate(() => loadAll(null));
    const list = await page.evaluate(([n, f]) => collect(n, f), [T * FPS, FPS]);
    fs.writeFileSync('needed3.json', JSON.stringify(list)); console.log('tiles', list.length);
    const t = await page.evaluate(() => LV.map(l => [l.key, +l.t0.toFixed(2)]));
    console.log(JSON.stringify(t)); await browser.close(); return;
  }
  const need = JSON.parse(fs.readFileSync('needed3.json'));
  console.log('loaded', await page.evaluate(l => loadAll(l), need));
  fs.mkdirSync(outDir, { recursive: true });
  const frames = mode === 'probe' ? a.split(',').map(s => Math.round(parseFloat(s) * FPS)) : Array.from({ length: +b - +a }, (_, i) => +a + i);
  for (const f of frames) {
    await page.evaluate(t => seek(t), f / FPS);
    await page.screenshot({ path: path.join(outDir, 'f' + String(f).padStart(4, '0') + '.png') });
  }
  console.log('done', frames.length);
  await browser.close();
})();
