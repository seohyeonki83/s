// c406: 본 맵에서 드론 — 길 찾기 격자를 처음 만들 때 멈칫하는지 · 오류 없는지
const { chromium } = require('playwright');
const V = process.argv[2] || 'c406m', SEED = +(process.argv[3] || 1);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const ctx = await b.newContext({ viewport: { width: 390, height: 844 } }); await ctx.addInitScript((s) => { window.__seed = s; window.__noReload = true; window.requestAnimationFrame = () => 0; }, SEED);
const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 3).join(' | ')));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 }); await p.waitForTimeout(300);
const out = await p.evaluate(() => { const R = window.__rd, me = R.me; document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })));
  window.__noRender = true; me.hp = me.maxHp = 1e6; for (let i = 0; i < 60; i++) R.step(1 / 60);
  // 건물 건너편에 드론 3대
  const B = R.buildings.filter((q) => !q.parent && q.type !== 'hill').sort((a, c) => Math.hypot((a.x0 + a.x1) / 2 - me.foot.x, (a.z0 + a.z1) / 2 - me.foot.z) - Math.hypot((c.x0 + c.x1) / 2 - me.foot.x, (c.z0 + c.z1) / 2 - me.foot.z))[0];
  const bx = (B.x0 + B.x1) / 2, bz = (B.z0 + B.z1) / 2, dx = bx - me.foot.x, dz = bz - me.foot.z, l = Math.hypot(dx, dz);
  const ds = []; for (let k = 0; k < 3; k++) ds.push(window.__droneAdd(bx + dx / l * (Math.max(B.x1 - B.x0, B.z1 - B.z0) / 2 + 3 + k), bz + dz / l * (Math.max(B.x1 - B.x0, B.z1 - B.z0) / 2 + 3 + k)));
  const d0 = ds.map((d) => Math.round(Math.hypot(d.x - me.foot.x, d.z - me.foot.z)));
  const ts = []; for (let i = 0; i < 900; i++) { const t = performance.now(); R.step(1 / 60); ts.push(performance.now() - t); }
  const top = ts.slice().sort((a, c) => c - a).slice(0, 4).map((v) => +v.toFixed(1));
  return { d0, d1: ds.map((d) => d.dead ? 'dead' : Math.round(Math.hypot(d.x - me.foot.x, d.z - me.foot.z))), worstSteps: top, avg: +(ts.reduce((a, c) => a + c, 0) / ts.length).toFixed(2), drones: window.__drones().length, meHp: Math.round(me.hp) }; });
console.log(JSON.stringify(out), 'errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
