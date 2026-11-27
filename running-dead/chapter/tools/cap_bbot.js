const { chromium } = require('playwright'); const fs = require('fs');
const src = fs.readFileSync(__dirname + '/var/c539.html', 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 3; window.__dif = "h";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + '/var/c539_cap.html', src);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c539_cap.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(1200);
await p.evaluate(() => window.__rd.ev(`(() => {
  let best = null; for (let t = 0; t < 900 && !best; t++) { const x = me.foot.x + (Math.random() - 0.5) * 60, z = me.foot.z + (Math.random() - 0.5) * 60; let ok = true; for (let dx = -5; dx <= 5 && ok; dx++) for (let dz = -6; dz <= 6 && ok; dz++) if (spaceOf(x + dx, z + dz) || chNearRiver(x + dx, z + dz, 3) || buildings.some((B) => B.type === 'hill' && x + dx > B.x0 - 2 && x + dx < B.x1 + 2 && z + dz > B.z0 - 2 && z + dz < B.z1 + 2)) ok = false; if (ok && bodies.every((b) => b === me || Math.hypot(b.foot.x - x, b.foot.z - z) > 14)) best = [x, z]; }
  const [x, z] = best; me.foot.set(x, 0, z + 30); me.space = null;
  const mk = (dx, boss) => { const c = addCitizen(x + dx, z, square(x + dx, z), 'robot'); if (boss) chBossLook(c); c.sleep = true; return c; };
  const L = [mk(0, true), mk(-2.6, false), mk(2.6, false)];
  me.foot.set(x, 0, z + 0.5); for (const c of L) bodies.splice(bodies.indexOf(c), 1); paused = false; for (let i = 0; i < 4; i++) { stepWorld(0.016); me.foot.set(x, 0, z + 0.5); } for (const c of L) bodies.push(c); paused = true; window.__camK = 0.55; document.querySelectorAll('#stage > *').forEach((e) => { if (e.tagName !== 'CANVAS') e.style.visibility = 'hidden'; });
  const hide = () => { for (const k in me) { const o = me[k]; if (o && o.isObject3D) o.visible = false; } for (const c of L) { for (const k in c) { const o = c[k]; if (o && o.isObject3D && o !== c.mesh) o.visible = false; } for (const ch of c.mesh.children) if (ch.isSprite) ch.visible = false; } }; hide(); draw(0); place(); hide(); window.__noRender = true; renderer.render(scene, camera); })()`));
await p.waitForTimeout(300);
await p.screenshot({ path: 'boss_bbot.png', clip: { x: 0, y: 190, width: 390, height: 300 } });
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
