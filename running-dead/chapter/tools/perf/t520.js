// c439: 막힌 드론 순간이동 · 괴물 테두리
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c439z.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(400);
const o = await p.evaluate(() => { const R = window.__rd, me = R.me; me.hp = me.maxHp = 1e9;
  const B = R.buildings.filter((q) => !q.parent && q.t !== 'hill' && (q.x1 - q.x0) > 6 && (q.z1 - q.z0) > 6).sort((a, q) => Math.hypot((a.x0 + a.x1) / 2 - me.foot.x, (a.z0 + a.z1) / 2 - me.foot.z) - Math.hypot((q.x0 + q.x1) / 2 - me.foot.x, (q.z0 + q.z1) / 2 - me.foot.z))[0];
  const cx = (B.x0 + B.x1) / 2, cz = (B.z0 + B.z1) / 2; window.__droneAdd(cx, cz); const d = window.__drones()[window.__drones().length - 1]; d.x = cx; d.z = cz;
  return { start: [+(Math.hypot(cx - me.foot.x, cz - me.foot.z)).toFixed(1)], size: [B.x1 - B.x0, B.z1 - B.z0].map((v) => +v.toFixed(1)) }; });
const tl = []; for (let i = 0; i < 10; i++) { await p.waitForTimeout(500); tl.push(await p.evaluate(() => { const R = window.__rd, me = R.me, d = window.__drones()[window.__drones().length - 1]; return d ? [+d.x.toFixed(1), +d.z.toFixed(1), +me.foot.x.toFixed(1), +me.foot.z.toFixed(1), d.tg ? (d.tg === me ? 'me' : 'other') : '-', d.stunT > 0 ? 'stun' : ''].join(',') : 'gone'; })); } o.tl = tl;
o.after = await p.evaluate(() => { const R = window.__rd, me = R.me, d = window.__drones()[window.__drones().length - 1]; return d ? { dist: +Math.hypot(d.x - me.foot.x, d.z - me.foot.z).toFixed(1), warps: d.jn || 0 } : 'gone'; });
// 괴물 덩치 테두리
await p.evaluate(() => { const R = window.__rd, me = R.me; R.setLv('mutate', 12); R.BR.mutate = 'monster'; const c = R.bodies.find((b) => b.kind === 'citizen' && b.sleep && !b.space && Math.hypot(b.foot.x - me.foot.x, b.foot.z - me.foot.z) > 30); c.sleep = false; R.zombify(c); let t = 0; do { window.__mut(c); } while (c.mut !== 'armor' && t++ < 20); c.foot.x = me.foot.x + 2; c.foot.z = me.foot.z; c.fixed = true; });
await p.waitForTimeout(800); await p.screenshot({ path: __dirname + '/perf/c439_halo.png', clip: { x: 120, y: 330, width: 200, height: 180 } });
console.log(JSON.stringify(o)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
