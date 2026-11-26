const { chromium } = require('playwright'); const fs = require('fs'); const V = process.argv[2];
const src = fs.readFileSync(__dirname + `/var/${V}.html`, 'utf8').replace('window.__map = "b";', 'window.__map = "t";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/${V}_tq.html`, src);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const [sx, sz, mx, mz, lab] of JSON.parse(process.argv[3])) {
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/${V}_tq.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1000);
await p.evaluate(() => { window.__noRender = true; document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); }); await p.waitForTimeout(600);
const r = await p.evaluate(([sx, sz, mx, mz]) => window.__rd.ev(`(() => {
  const C9 = buildings.find((B) => B.local === 913); const sn = bodies.find((b) => b.kind === 'citizen' && b.sniper && b.space === C9);
  sn.foot.set(${sx}, 0, ${sz}); const n0 = pickups.length; makeZombie(sn); const pk = pickups[pickups.length - 1];
  const info = { made: pickups.length - n0, at: pk && [+pk.x.toFixed(2), +pk.z.toFixed(2), pk.space && pk.space.local, pk.kind] };
  me.foot.set(${mx} === 0 ? pk.x : ${mx}, 0, ${mz} === 0 ? pk.z : ${mz}); me.space = spaceOf(me.foot.x, me.foot.z) || null;
  if (${mx} !== 0) { me.foot.x = pk.x + ${mx}; me.foot.z = pk.z + ${mz}; me.space = spaceOf(me.foot.x, me.foot.z) || null; }
  for (let i = 0; i < 10; i++) { paused = false; move.set(0, 0); pickupTick(0.05); }
  info.meSp = me.space && me.space.local; info.left = pickups.includes(pk); return info;
})()`), [sx, sz, mx, mz]);
console.log(lab, JSON.stringify(r)); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
