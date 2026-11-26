// c469: 현금 빨간 별 — 기계 유혹 시간 · 비트코인
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c496eR.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(2000);
const o = { max: await p.evaluate(() => window.__rd.MAXL()) };
for (const n of [5, 6, 10]) {
  await p.evaluate((n) => { window.__rd.RB(); window.__rd.SET('cash', n, null); }, n); await p.waitForTimeout(800);
  await p.evaluate(() => window.__rd.USE('cash'));
  const tl = []; let rl = 0, pl = 0; for (let i = 0; i < 50; i++) { await p.waitForTimeout(100); const s = await p.evaluate(() => window.__rd.SAMP()); if (/R1/.test(s)) rl = (i + 1) / 10; if (/P1/.test(s)) pl = (i + 1) / 10; if (i === 3 && n === 10) await p.screenshot({ path: __dirname + '/perf/c496_btc.png' }); }
  o['lv' + n] = { name: await p.evaluate(() => window.__rd.NAME()), robotLuredUntil: rl, policeLuredUntil: pl };
  await p.waitForTimeout(4000);
}
console.log(JSON.stringify(o)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
