// 금 현금에 홀린 로봇이 쏘는지 (사격 횟수 = atkT가 다시 차오른 횟수)
const { chromium } = require('playwright');
const f = process.argv[2];
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + f + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(2500);
await p.evaluate(() => { window.__rd.RB(); window.__rd.SET('cash', 12, 'gold'); });
await p.waitForTimeout(1500);
await p.evaluate(() => window.__rd.USE('cash'));
let prev = null, shots = 0, luredS = 0, maxL = 0;
for (let i = 0; i < 60; i++) { await p.waitForTimeout(100); const S = await p.evaluate(() => window.__rd.SAMP()); const nl = S.filter((x) => x[0] === 'lured').length; maxL = Math.max(maxL, nl); if (prev) S.forEach((x, j) => { if (x[1] > prev[j][1] + 0.05) { shots++; if (x[0] === 'lured') luredS++; } }); prev = S; }
console.log(f, JSON.stringify({ maxLured: maxL, shotsWhileLured: luredS, shotsTotal: shots })); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
