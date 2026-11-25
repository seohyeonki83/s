// c454: 불도저 2대
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c454z.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(400);
await p.evaluate(() => { const R = window.__rd; R.me.hp = R.me.maxHp = 1e9; R.BS(); });
await p.waitForTimeout(6000);
const o = await p.evaluate(() => { const R = window.__rd, T = R.TKS(); return { n: T.length, hp: T.map((t) => Math.round(t.obj.maxHp)), pos: T.map((t) => [Math.round(t.x), Math.round(t.z)]), dist: T.length > 1 ? +Math.hypot(T[0].x - T[1].x, T[0].z - T[1].z).toFixed(1) : null, alive: T.map((t) => !t.wreck) }; });
await p.evaluate(() => { const R = window.__rd, T = R.TKS()[0]; R.me.foot.x = T.x - 5; R.me.foot.z = T.z; });
await p.waitForTimeout(1500); await p.screenshot({ path: __dirname + '/perf/c454_soak0.png' });
await p.waitForTimeout(25000); o.soak = await p.evaluate(() => window.__rd.TKS().map((t) => [!t.wreck, Math.round(t.obj.hp), Math.round(t.x), Math.round(t.z)]));
await p.waitForTimeout(3000); o.victory = await p.evaluate(() => document.body.innerText.includes('VICTORY'));
console.log(JSON.stringify(o)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
