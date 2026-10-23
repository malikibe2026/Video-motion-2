const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const [,, mode, outDir, a, b] = process.argv;
const FPS = 30;
(async () => {
  const browser = await chromium.launch({ args: ['--font-render-hinting=none', '--force-color-profile=srgb'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.log('PAGEERROR', e.message));
  await page.goto('http://127.0.0.1:8767/khutbah.html');
  await page.evaluate(() => window.ready);
  fs.mkdirSync(outDir, { recursive: true });
  const frames = mode === 'probe' ? a.split(',').map(s => Math.round(parseFloat(s) * FPS)) : Array.from({ length: +b - +a }, (_, i) => +a + i);
  for (const f of frames) { await page.evaluate(t => seek(t), f / FPS); await page.screenshot({ path: path.join(outDir, 'f' + String(f).padStart(4, '0') + '.png') }); }
  console.log('done', frames.length); await browser.close();
})();
