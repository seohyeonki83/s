const { chromium } = require('playwright'); const fs = require('fs');
const src = fs.readFileSync(__dirname + '/var/c516.html', 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "h";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + '/var/c516_cap.html', src);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const kind of ['convoy', 'dozer', 'tank']) {
const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c516_cap.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(1200);
await p.evaluate((kind) => window.__rd.ev(`(() => {
  // 빈 길 찾기: 나 둘레에서 건물 없는 넓은 곳
  let best = null; for (let t = 0; t < 400 && !best; t++) { const x = me.foot.x + (Math.random() - 0.5) * 60, z = me.foot.z + (Math.random() - 0.5) * 60; let ok = true; for (let dx = -5; dx <= 5 && ok; dx += 1) for (let dz = -6; dz <= 6 && ok; dz += 1) if (spaceOf(x + dx, z + dz) || chNearRiver(x + dx, z + dz, 1)) ok = false; if (ok) best = [x, z]; }
  const [x, z] = best; me.foot.set(x, 0, z); me.space = null; for (const o of [me.mesh, me.gauge, me.hpBar, me.icon]) if (o) o.visible = false;
  for (const c of bodies) if (c.kind === 'citizen' && Math.hypot(c.foot.x - x, c.foot.z - z) < 12) c.foot.set(c.foot.x + 40, 0, c.foot.z);
  for (const c of cars) if (Math.hypot(c.x - x, c.z - z) < 12) { c.x += 40; }
  if ('${kind}' === 'convoy') { [-2.6, 0, 2.6].forEach((dx, i) => { addCar(x + dx, z - 0.5, -Math.PI / 2, null, 0, ['robot', 'robot', 'soldier', 'soldier', 'soldier']); const cc = cars[cars.length - 1]; cc.state = 'parked'; for (let k = 0; k < [3, 3, 2][i]; k++) { const d = chDroneAdd(cc.x, cc.z); d.ride = cc; d.rideK = k; } }); }
  else if ('${kind}' === 'dozer') { chBossSpawn(teamSeg()); chBossSpawn(teamSeg()); chTanks.forEach((t, i) => { t.x = x + (i ? 2.4 : -2.4); t.z = z; t.h = -Math.PI / 2; t.vx = t.vz = 0; }); }
  else { chBossSpawn(teamSeg(), 'tank'); const t = chTanks[0]; t.x = x; t.z = z; t.h = -Math.PI / 2; t.vx = t.vz = 0; }
  window.__camK = 0.75; for (let i = 0; i < 3; i++) { stepWorld(0.016); for (const t of chTanks) { t.x = t.x; } }
  paused = true; for (const o of [me.mesh, me.gauge, me.hpBar, me.icon, me.ring, me.shadow]) if (o) o.visible = false; document.querySelectorAll('#stage > *').forEach((e) => { if (e.tagName !== 'CANVAS') e.style.visibility = 'hidden'; }); return 1; })()`), kind);
await p.waitForTimeout(400);
await p.evaluate(() => window.__rd.ev(`(() => { const hide = () => { for (const k in me) { const o = me[k]; if (o && o.isObject3D) o.visible = false; } for (const t of chTanks) if (t.tracer) t.tracer.visible = false; for (const f of (typeof flashes !== "undefined" ? flashes : [])) if (f.m) f.m.visible = false; }; hide(); const d0 = draw; draw(0); place(); hide(); renderer.render(scene, camera); })()`)); await p.screenshot({ path: `boss_${kind}.png`, clip: { x: 0, y: 190, width: 390, height: 300 } });
}
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
