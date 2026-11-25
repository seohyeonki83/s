// c465: 적 테스트 — 동료 10 따라다님 · 서로 공격 안 함 · 내 스킬만
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c465eZ.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(2000);
const o = {}; o.t0 = await p.evaluate(() => window.__rd.S());
await p.waitForTimeout(10000); o.t10 = await p.evaluate(() => window.__rd.S());
// 조이스틱으로 오른쪽 위로 4초 걷기
const J = await p.evaluate(() => { const r = document.getElementById('joy').getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2]; });
await p.mouse.move(J[0], J[1]); await p.mouse.down(); await p.mouse.move(J[0] + 40, J[1] - 40, { steps: 5 }); await p.waitForTimeout(4000); await p.mouse.up();
o.walk = await p.evaluate(() => window.__rd.S()); await p.waitForTimeout(3000); o.after = await p.evaluate(() => window.__rd.S());
await p.screenshot({ path: __dirname + '/perf/c465_allies.png' });
await p.evaluate(() => { window.__rd.SET('bomb', 6, null); window.__rd.USE('bomb'); }); await p.waitForTimeout(5000); o.bomb = await p.evaluate(() => window.__rd.S());
await p.evaluate(() => document.querySelector('#etbar .b[data-k="__re"]').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); await p.waitForTimeout(500); o.re = await p.evaluate(() => window.__rd.S());
console.log(JSON.stringify(o)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
