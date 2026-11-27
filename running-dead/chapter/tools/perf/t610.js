const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const V of process.argv.slice(2)) for (const kind of ['ally', 'armor']) {
const src = fs.readFileSync(__dirname + `/var/${V}.html`, 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/${V}_1e.html`, src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/${V}_1e.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1200);
await p.evaluate(() => { window.__noRender = true; document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); }); await p.waitForTimeout(800);
console.log(V, kind, await p.evaluate((kind) => window.__rd.ev(`(() => {
  Math.random = (() => { let s = 7; return () => (s = (s * 16807) % 2147483647) / 2147483647; })();
  let best = null; for (let t = 0; t < 900 && !best; t++) { const x = me.foot.x + (Math.random() - 0.5) * 90, z = me.foot.z + (Math.random() - 0.5) * 90; let ok = true; for (let dx = -8; dx <= 8 && ok; dx++) for (let dz = -6; dz <= 6 && ok; dz++) if (spaceOf(x + dx, z + dz) || chNearRiver(x + dx, z + dz, 1)) ok = false; if (ok) best = [x, z]; }
  const [x, z] = best; for (const c of bodies) if (c.kind === 'citizen' && Math.hypot(c.foot.x - x, c.foot.z - z) < 20) c.foot.set(c.foot.x + 80, 0, c.foot.z);
  for (const c of cars) if (Math.hypot(c.x - x, c.z - z) < 12) c.x += 60;
  me.foot.set(x, 0, z + 6); me.space = null; me.hp = me.maxHp = 1e6;
  const bars = [-4.1, -2.05, 0, 2.05, 4.1].map((dx) => chParked(x + dx, z, 0, true));
  const h = addCitizen(x, z - 1.9, square(x, z - 1.9), 'soldier'); h.hp = h.maxHp = 1e7;
  const q = addCitizen(x, z + 1.3, square(x, z + 1.3), ''); makeZombie(q); const a = q; if ('${kind}' === 'armor') mutate(a, 'armor'); a.foot.set(x, 0, z + 1.2); a.hp = a.maxHp = 1e6;
  const tg = {}; const s0 = strike; strike = (zz, tt) => { if (zz === a) { const k = tt.kind === 'obj' ? (tt.car && tt.car.barr ? 'barricade' : tt.type) : tt.kind; tg[k] = (tg[k] || 0) + 1; } return s0(zz, tt); };
  const hp0 = bars.reduce((s, c) => s + c.obj.hp, 0); let slow = 0;
  for (let i = 0; i < 150; i++) { paused = false; me.hp = me.maxHp; h.hp = 1e7; h.stunT = 9; h.foot.set(x, 0, z - 1.9); stepWorld(0.033); if ((a.realSp || 0) < 0.3 * a.speed) slow++; }
  strike = s0;
  return 'strikes ' + JSON.stringify(tg) + ' · bar hp -' + Math.round(hp0 - bars.reduce((s, c) => s + c.obj.hp, 0)) + ' · slow frames ' + slow + '/150 · eng ' + (a.engaging ? a.engaging.kind : '-') + ' · pos ' + (a.foot.x - x).toFixed(1) + ',' + (a.foot.z - z).toFixed(1);
})()`), kind)); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
