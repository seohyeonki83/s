// c407: 본 맵 테스트 속도 — 순환도로 위에서 조이스틱을 한쪽으로 밀고 2초 (손으로 걸음을 돌린다)
const { chromium } = require('playwright');
const V = process.argv[2] || 'c407w', SEED = +(process.argv[3] || 1);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const ctx = await b.newContext({ viewport: { width: 390, height: 844 } }); await ctx.addInitScript((s) => { window.__seed = s; window.__noReload = true; window.requestAnimationFrame = () => 0; }, SEED);
const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 }); await p.waitForTimeout(300);
await p.evaluate(() => { document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); const R = window.__rd, me = R.me, Z = R.ch.zones, zi = Z.findIndex((q) => me.foot.x >= q[0] && me.foot.x <= q[2] && me.foot.z >= q[1] && me.foot.z <= q[3]), q = Z[zi]; window.__noRender = true;
  me.foot.x = q[0] + 6; me.foot.z = q[1] + 2.25; me.px = me.foot.x; me.pz = me.foot.z; for (let i = 0; i < 30; i++) R.step(1 / 60); });
await p.mouse.move(195, 600); await p.mouse.down(); await p.mouse.move(315, 600, { steps: 3 });   // 오른쪽으로
const r = await p.evaluate(() => { const R = window.__rd, me = R.me, x0 = me.foot.x, z0 = me.foot.z; for (let i = 0; i < 120; i++) R.step(1 / 60); return { moved: +Math.hypot(me.foot.x - x0, me.foot.z - z0).toFixed(2), vel: +me.vel.length().toFixed(2), speed: +me.speed.toFixed(2), dx: +(me.foot.x - x0).toFixed(2) }; });
await p.mouse.up();
const r2 = await p.evaluate(() => { const R = window.__rd, me = R.me; for (let i = 0; i < 60; i++) R.step(1 / 60); return { stopVel: +me.vel.length().toFixed(2) }; });
console.log(V, JSON.stringify(r), JSON.stringify(r2), 'errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
