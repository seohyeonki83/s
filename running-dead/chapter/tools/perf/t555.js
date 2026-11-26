const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c481eM.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(2000);
await p.evaluate(() => { window.__rd.SET('taser', 10, null); return window.__rd.PREP(); }); await p.waitForTimeout(500);
const z = []; for (let i = 0; i < 12; i++) { z.push(await p.evaluate(() => window.__rd.ZAP())); await p.waitForTimeout(250); }
const o = { zaps: z, t0: await p.evaluate(() => window.__rd.ST()) };
await p.waitForTimeout(1000); await p.screenshot({ path: __dirname + '/perf/c481_mad1.png' });
await p.waitForTimeout(2500); o.t3 = await p.evaluate(() => window.__rd.ST()); await p.screenshot({ path: __dirname + '/perf/c481_mad2.png' });
await p.waitForTimeout(6000); o.t9 = await p.evaluate(() => window.__rd.ST());
console.log(JSON.stringify(o)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
