// c448: 괴물 뿔 · 괴물 히드라 빨간 토사물 화면
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c448z.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(400);
await p.evaluate(() => { const R = window.__rd, me = R.me; me.hp = me.maxHp = 1e9; R.setLv('mutate', 12); R.BR.mutate = 'monster';
  const mk = (type, dx, dz) => { const c = R.bodies.find((b) => b.kind === 'citizen' && b.sleep && !b.space && Math.hypot(b.foot.x - me.foot.x, b.foot.z - me.foot.z) > 30); c.sleep = false; R.zombify(c); let t = 0; do { window.__mut(c); } while (c.mut !== type && t++ < 30); c.mutT = 999; c.foot.x = me.foot.x + dx; c.foot.z = me.foot.z + dz; c.space = null; return c; };
  mk('armor', -2, 0.5); mk('hydra', 2, 0.5);
  const v = R.bodies.find((c) => c.kind === 'citizen' && c.maxHp > 0 && !c.space && !c.police); v.sleep = false; v.met = true; v.foot.x = me.foot.x + 2; v.foot.z = me.foot.z - 5; v.hp = 9999; });
let shot = false; for (let i = 0; i < 40 && !shot; i++) { await p.waitForTimeout(100); shot = await p.evaluate(() => window.__rd.SPITS().some((q) => q.rs)); }
await p.screenshot({ path: __dirname + '/perf/c448_monster.png', clip: { x: 60, y: 280, width: 270, height: 340 } });
console.log('redSpit', shot, JSON.stringify(errs.slice(0, 3))); await b.close(); })();
