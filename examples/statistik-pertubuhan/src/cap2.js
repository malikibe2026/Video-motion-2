const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
const ROWS = JSON.parse(fs.readFileSync(__dirname + '/data.json'));
(async () => {
  const browser = await chromium.launch({ args: ['--font-render-hinting=none', '--force-color-profile=srgb'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2, reducedMotion: 'reduce' });
  await page.route('https://phrbiposqqclnwclizim.supabase.co/**', async (route) => {
    const u = route.request().url(); let body = [];
    if (u.includes('/rest/v1/muat_naik')) body = [{ id: 'demo-1', nama_fail: 'DATA_REKAAN_DEMO.xlsx', bil_rekod: ROWS.length, status: 'aktif', created_at: '2026-10-21T11:00:00Z' }];
    else if (u.includes('/rest/v1/rekod')) body = u.includes('offset=') && !/offset=0(&|$)/.test(u) ? [] : ROWS;
    await route.fulfill({ status: 200, contentType: 'application/json', headers: { 'access-control-allow-origin': '*' }, body: JSON.stringify(body) });
  });
  await page.goto('http://127.0.0.1:8770/app/index.html'); await page.waitForTimeout(3500);
  fs.mkdirSync('el', { recursive: true });
  await page.locator('header').first().screenshot({ path: 'el/header.png' });
  await page.locator('#kpi').screenshot({ path: 'el/Ring_x_kpi.png' });
  await page.locator('#sektorKad').screenshot({ path: 'el/Ring_x_sektor.png' });
  for (const tab of ['Ringkasan', 'Prestasi Pegawai', 'Peta Parlimen', 'Analisis Nilai', 'Senarai Rekod']) {
    await page.evaluate(t => { const b = [...document.querySelectorAll('button,a')].find(x => x.textContent.trim() === t); if (b) b.click(); }, tab);
    await page.waitForTimeout(3500);
    if (tab === 'Prestasi Pegawai') { for (const [sel, nm] of [['.fe-hero', 'hero'], ['.fe-kpis, .fe-kpi-grid', 'kpis']]) { const l = page.locator(sel).first(); if (await l.count()) await l.screenshot({ path: `el/Pres_x_${nm}.png` }); } }
    if (tab === 'Peta Parlimen') {
      await page.evaluate(() => { const ch = echarts.getInstanceByDom(document.getElementById('cPeta')); ch.setOption({ series: [{ zoom: 5.2, center: [101.70, 3.14] }] }); });
      await page.waitForTimeout(1500);
    }
    const arts = page.locator('article.kad:visible, section.kad:visible, .kad:visible');
    const n = await arts.count(); const seen = new Set();
    for (let i = 0; i < n; i++) {
      const a = arts.nth(i); const box = await a.boundingBox(); if (!box || box.width < 200 || box.height < 120) continue;
      const key = Math.round(box.x) + ',' + Math.round(box.y); if (seen.has(key)) continue; seen.add(key);
      const t = (await a.locator('h2,h3').first().textContent().catch(() => '') || '').trim().slice(0, 30).replace(/[^A-Za-z0-9]+/g, '_');
      const f = `el/${tab.slice(0, 4)}_${String(i).padStart(2, '0')}_${t}.png`;
      await a.screenshot({ path: f }); console.log(f, Math.round(box.width), Math.round(box.height));
    }
  }
  await browser.close();
})();
