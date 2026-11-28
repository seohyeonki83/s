const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const v of ['c610', 'c611']) {
const src = fs.readFileSync(__dirname + `/var/${v}.html`, 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/${v}_mag.html`, src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/${v}_mag.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
console.log(v, await p.evaluate(() => window.__rd.ev(`(() => { const out = []; for (const d of [2.4, 3.5, 4.5, 5.0, 5.5]) { const x = me.foot.x + d, z = me.foot.z; chHeartDrop(x, z, me.space); const pk = pickups[pickups.length - 1]; pk.tag = d; }
  const eaten = []; for (let i = 0; i < 60; i++) { const before = new Set(pickups); pickupTick(1 / 30); for (const q of before) if (!pickups.includes(q)) eaten.push(q.tag + '칸(' + (i / 30).toFixed(2) + '초)'); }
  const left = pickups.filter((q) => q.tag).map((q) => q.tag + '칸'); for (const q of pickups.filter((q) => q.tag)) { scene.remove(q.s); } for (let i = pickups.length - 1; i >= 0; i--) if (pickups[i].tag) pickups.splice(i, 1);
  return '먹음: ' + eaten.join(', ') + ' | 남음: ' + left.join(', ') + ' | 자석 거리 ' + (typeof CH_MAG_R !== 'undefined' ? (CH_MAG_R * MELEE).toFixed(2) : '-') + ' · 줍는 거리 ' + PICK_R.toFixed(2); })()`))); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
