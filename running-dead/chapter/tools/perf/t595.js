const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const V of ['c515', 'c516']) {
const src = fs.readFileSync(__dirname + `/var/${V}.html`, 'utf8').replace('window.__map = "b";', 'window.__map = "t";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/${V}_tq.html`, src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/${V}_tq.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
console.log(V, await p.evaluate(() => window.__rd.ev(`(() => { const cnt = (B) => { const o = {}; for (const c of bodies) if (c.kind === 'citizen' && c.home === B) { const k = c.sniper ? 'sniper' : c.soldier ? 'soldier' : c.police ? 'police' : c.attacker ? 'attacker' : c.guard ? 'guard' : 'white'; o[k] = (o[k] || 0) + 1; } return JSON.stringify(o); };
  const L2 = buildings.filter((B) => B.type === 'lab')[1], P = buildings.find((B) => B.local === 941); return 'room1 ' + cnt(L2) + ' | parking ' + cnt(P); })()`))); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
