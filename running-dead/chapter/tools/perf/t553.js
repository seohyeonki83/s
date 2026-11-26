const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c479eS.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(2000);
const o = {};
for (const n of [5, 6, 10]) {
  await p.evaluate((n) => { window.__rd.SET('bomb', n, null); window.__rd.PREP(); }, n); await p.waitForTimeout(400);
  const a = await p.evaluate(() => window.__rd.POS()); await p.waitForTimeout(2000); const c = await p.evaluate(() => window.__rd.POS());
  let sg = 0, ng = 0, kg = 0, kn = 0; a.forEach((q, i) => { const d = Math.hypot(c[i][0] - q[0], c[i][1] - q[1]); if (q[2]) { sg += d; kg++; } else { ng += d; kn++; } });
  o['lv' + n] = { col: await p.evaluate(() => window.__rd.COL()), gooMove: +(sg / kg).toFixed(2), freeMove: +(ng / kn).toFixed(2), gooHpLost2s: a.filter((q) => q[2]).map((q, i) => q[3]).length ? a[1][3] - c[1][3] : null };
  if (n === 10) await p.screenshot({ path: __dirname + '/perf/c479_purple.png' });
}
o.acidp = await p.evaluate(() => window.__rd.AP());
console.log(JSON.stringify(o)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
