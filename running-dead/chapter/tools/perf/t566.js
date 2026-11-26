// 보스 테스트: 동료 70 + 덩치 2 vs 불도저 2대 — 120초 관찰
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c493kS.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))));
const t0 = Date.now(); for (let i = 0; i < 12; i++) { await p.waitForTimeout(8000); const s = await p.evaluate(() => window.__rd.S()); console.log(Math.round((Date.now() - t0) / 1000) + 's', JSON.stringify(s)); if (i === 3) await p.screenshot({ path: __dirname + '/perf/c493_boss.png' }); if (s.dozers.length && s.dozers.every((d) => d === 'X')) break; }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
