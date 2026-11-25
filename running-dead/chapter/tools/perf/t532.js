// c460: 자폭 동료 힘 3배 · 방탄복 2개
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c460z.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(400);
const o = await p.evaluate(() => { const R = window.__rd, a = R.NZ(1.5), c = R.NZ(-1.5);
  R.MU(c, 'armor'); const k = (z) => +(R.KB(z) / R.KD * 12).toFixed(2);
  const r = { plain0: [a.force, k(a)], armor0: [+c.force.toFixed(2), k(c)] };
  R.BC(a, 3); R.BC(c, 3); r.plain1 = [a.force, k(a)]; r.armor1 = [+c.force.toFixed(2), k(c)]; return r; });
await p.waitForTimeout(1500); console.log(JSON.stringify(o)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
