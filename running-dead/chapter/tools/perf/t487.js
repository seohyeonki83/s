// c406: 본 맵 둘러보기 스샷 — 다리(가로·세로) · 돌린 주유소·공원·농구장 · 큰 단락 네거리
const { chromium } = require('playwright');
const V = process.argv[2] || 'c406m', SEED = +(process.argv[3] || 1);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 }); await ctx.addInitScript((s) => { window.__seed = s; window.__noReload = true; }, SEED);
const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 2).join(' | ')));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 }); await p.waitForTimeout(1200);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(400);
const spots = await p.evaluate(() => { const R = window.__rd, C = R.ch, out = [];
  const pv = C.passes2.find((q) => q.axis === 'v'), ph = C.passes2.find((q) => q.axis === 'h'), pl = C.passes2.slice().sort((a, c) => c.len - a.len)[0];
  out.push(['bridge_v', (pv.ax + pv.bx) / 2, pv.az]); out.push(['bridge_h', ph.ax, (ph.az + ph.bz) / 2]); out.push(['bridge_long', (pl.ax + pl.bx) / 2, (pl.az + pl.bz) / 2]);
  for (const [k, cond] of [['gas', (a) => a.rk === 1], ['gas', (a) => a.rf && a.rk === 0], ['park', (a) => a.rk % 2 === 1], ['court', (a) => a.rk === 2], ['site', (a) => a.rk === 3]]) { const a = C.areas.find((q) => q.k === k && cond(q)); if (a) out.push([k + '_k' + a.rk + (a.rf ? 'f' : ''), (a.r[0] + a.r[2]) / 2, a.r[3] + 1.2]); }
  const A = C.ave.find((q) => q.V && q.H); if (A) out.push(['cross_roads', A.V.c, A.H.c]);
  return out; });
const S = __dirname + '/perf/tour_';
for (const [name, x, z] of spots) {
  await p.evaluate(([x, z]) => { const me = window.__rd.me; me.hp = me.maxHp; me.foot.x = x; me.foot.z = z; me.px = x; me.pz = z; window.__camK = 1.5; }, [x, z]);
  await p.waitForTimeout(1300);
  await p.screenshot({ path: S + name + '.png' });
}
console.log(spots.map((s) => s[0]).join(' '), 'errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
