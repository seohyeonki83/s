// 맵별 무기 실측 비교 (같은 조건: 둘레 적 15 · 동료 6)
const { chromium } = require('playwright');
const f = process.argv[2];
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + f + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 90000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(3000);
const R = {}; const W = (ms) => p.waitForTimeout(ms);
const run = async (name, k, n, br, wait, fn) => { R[name] = {}; R[name].prep = await p.evaluate(() => window.__rd.PREP(15, 6)); await W(300); await p.evaluate(([k, n, br]) => window.__rd.SET(k, n, br), [k, n, br]); await W(200); R[name].pre = await p.evaluate(() => window.__rd.EN()); R[name].used = await p.evaluate((k) => String(window.__rd.USE(k)), k); await W(wait); R[name].post = await p.evaluate(fn ? fn : () => window.__rd.EN()); };
await run('taser6', 'taser', 6, null, 300);
await run('ebomb6', 'taser', 12, 'bomb', 300);
await run('bomb6', 'bomb', 6, null, 5000);
await run('cash6', 'cash', 6, null, 4000);
await run('mutate6', 'mutate', 6, null, 600, () => window.__rd.MUT());
await run('awaken6', 'awaken', 6, null, 600, () => window.__rd.MUT());
R.me = await p.evaluate(() => window.__rd.ME());
console.log(f, JSON.stringify(R)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
