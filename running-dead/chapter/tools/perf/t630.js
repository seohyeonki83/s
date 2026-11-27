const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const [V, mp] of [['c539', 't'], ['c540', 't'], ['c540', 'm2']]) {
const src = fs.readFileSync(__dirname + `/var/${V}.html`, 'utf8').replace('window.__map = "b";', mp === 't' ? 'window.__map = "t";' : 'window.__map = "m"; window.__stg = 2; window.__dif = "n";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/${V}_${mp}g.html`, src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/${V}_${mp}g.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
if (mp === 't') console.log(V, await p.evaluate(() => window.__rd.ev(`(() => { const [L] = buildings.filter((B) => B.type === 'lab'), C1 = buildings.filter((B) => B.type === 'labc')[0], w = bodies.find((b) => b.kind === 'citizen' && b.home === C1 && !b.guard && !b.police && !b.attacker); const D = L.locks[0];
  let vis = 0, n = 0; for (let x = L.x0 + 0.8; x < L.x1 - 0.8; x += 0.7) for (let z = L.z0 + 0.8; z < L.z1 - 0.8; z += 0.7) { n++; const d = Math.hypot(w.foot.x - x, w.foot.z - z); if (d <= SIGHT && !blocked(x, z, w.foot.x, w.foot.z)) vis++; }
  return 'white dist from door ' + Math.hypot(w.foot.x - D.cx, w.foot.z - D.cz).toFixed(1) + ' · seen from room spots ' + vis + '/' + n; })()`)));
await p.waitForSelector('#goal.on', { timeout: 30000 }).catch(() => {}); await p.waitForTimeout(700);
if (V === 'c540') await p.screenshot({ path: `shot540_goal_${mp}.png` }); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
