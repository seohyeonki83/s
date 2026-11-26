const { chromium } = require('playwright'); const fs = require('fs');
const src = fs.readFileSync(__dirname + '/var/c513.html', 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + '/var/c513_1e.html', src);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c513_1e.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(1500);
for (const [d, sh] of [[0, 0], [3, 0], [20, 1], [60, 2], [100, 2], [250, 3], [900, 6]]) {
  await p.evaluate(([d, sh]) => window.__rd.ev(`deaths = ${d}; shownStars = ${sh}; chSkullMode = ${sh > 5}; drawStars(); chSfHud();`), [d, sh]); await p.waitForTimeout(300);
  await p.screenshot({ path: `shot513_${d}.png`, clip: { x: 60, y: 0, width: 270, height: 110 } });
}
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
