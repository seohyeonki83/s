// 전기폭탄 고리 이펙트
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c464eR.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(2500);
for (const [n, nm] of [[12, 'r6'], [9, 'r3']]) {
  await p.evaluate((n) => window.__rd.SET('taser', n, 'bomb'), n); await p.waitForTimeout(400);
  await p.evaluate(() => window.__rd.USE('taser'));
  for (const ms of [120, 140, 200]) { await p.waitForTimeout(ms); await p.screenshot({ path: __dirname + `/perf/c464_eb_${nm}_${ms}.png` }); }
  await p.waitForTimeout(1500);
}
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
