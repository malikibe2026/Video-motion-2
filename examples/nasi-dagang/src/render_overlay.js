// Render lapisan grafik telus (PNG) bingkai demi bingkai.
// node render_overlay.js <outDir> <fromFrame> <toFrame>   |  node render_overlay.js probe t1 t2 ...
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
const FPS = 24;
(async () => {
  const [mode, ...rest] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.join(__dirname, 'overlay.html'));
  await page.waitForFunction(() => window.ready === true);
  const shot = async (t, file) => {
    await page.evaluate(async (t) => { await window.seek(t); await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); }, t);
    await page.screenshot({ path: file, omitBackground: true });
  };
  if (mode === 'probe') {
    fs.mkdirSync('probe', { recursive: true });
    for (const t of rest) await shot(parseFloat(t), `probe/ov_${t}.png`);
  } else {
    const [a, b] = rest.map(Number); fs.mkdirSync(mode, { recursive: true });
    for (let f = a; f < b; f++) await shot(f / FPS, path.join(mode, String(f).padStart(5, '0') + '.png'));
  }
  await browser.close();
})();
