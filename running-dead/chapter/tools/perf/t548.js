const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c475eT.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(2000);
await p.evaluate(() => window.__rd.GOO()); await p.waitForTimeout(3300); const g = await p.evaluate(() => window.__rd.GH());
const n = await p.evaluate(() => window.__rd.BURST(false)); const m = await p.evaluate(() => window.__rd.BURST(true));
console.log(JSON.stringify({ gooHpAfter3s: g, burstNormal: n, burstMini: m })); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
