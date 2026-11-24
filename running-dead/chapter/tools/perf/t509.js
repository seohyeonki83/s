// c431: 전이 감전 · 전기폭탄
const { chromium } = require('playwright');
const BR = process.argv[2];
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c431z.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1200);
const r = await p.evaluate((BR) => { const R = window.__rd, me = R.me, o = {}; document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); me.hp = me.maxHp = 1e9;
  R.addTool('taser'); R.setLv('taser', 12); R.BR.taser = BR;
  const cs = R.bodies.filter((c) => c.kind === 'citizen' && c.maxHp > 0 && !c.space).slice(0, 6);
  cs.forEach((c, i) => { c.sleep = false; c.met = true; c.disc = true; const a = i * 1.05; const d = i === 0 ? 4 : i < 3 ? 4 + 1.2 : 6.5; c.foot.x = me.foot.x + Math.cos(a) * d; c.foot.z = me.foot.z + Math.sin(a) * d; if (i === 1 || i === 2) { c.foot.x = cs[0].foot.x + (i === 1 ? 1.0 : -2.6); c.foot.z = cs[0].foot.z; } c.space = null; });
  window.__droneAdd(me.foot.x + 5, me.foot.z - 2); const dr = window.__drones()[window.__drones().length - 1];
  R.step(1 / 60); R.use('taser'); o.after = cs.map((c) => +(c.stunT || 0).toFixed(2)); o.drone = +(dr.stunT || 0).toFixed(2);
  const st = []; for (let i = 1; i <= 120; i++) { R.step(1 / 60); if (i % 12 === 0) st.push(cs.slice(0, 3).map((c) => +(c.stunT || 0).toFixed(2)).join('/')); } o.timeline = st; o.stat = R.SL('taser', 12);
  return o; }, BR);
console.log(BR, JSON.stringify(r)); console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
