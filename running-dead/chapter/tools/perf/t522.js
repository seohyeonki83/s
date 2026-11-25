// c444: 주차된 차에 몸을 붙였을 때 밀려나는 거리 (차 중심에서 몸 중심까지)
const { chromium } = require('playwright');
const V = process.argv[2];
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader'] }); const ctx = await b.newContext(); await ctx.addInitScript(() => { window.requestAnimationFrame = () => 0; window.__noRender = true; let s = 7; Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; });
const p = await ctx.newPage(); await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
console.log(V, JSON.stringify(await p.evaluate(() => { const R = window.__rd, me = R.me; const car = R.cars().find((c) => c.state === 'parked' && !c.wall && !c.barr && !c.tank); const fx = Math.cos(car.h), fz = Math.sin(car.h), x0 = car.x, z0 = car.z; const o = [];
  for (const [u, v] of [[0.3, 0], [0, 0.2]]) { me.foot.x = car.x + fx * u - fz * v; me.foot.z = car.z + fz * u + fx * v; me.vel.set(0, 0); for (let i = 0; i < 5; i++) R.step(1 / 60); const dx = me.foot.x - car.x, dz = me.foot.z - car.z; o.push([+(dx * fx + dz * fz).toFixed(2), +(-dx * fz + dz * fx).toFixed(2)]); car.x = x0; car.z = z0; }
  return o; }))); await b.close(); })();
