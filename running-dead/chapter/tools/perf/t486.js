// c406: 본 맵을 씨앗 여러 개로 — 뜨는지 · 시작이 가운데 그룹인지 · 오류 없는지 · 30초 돌려 보기
const { chromium } = require('playwright');
const V = process.argv[2] || 'c406m', S0 = +(process.argv[3] || 1), N = +(process.argv[4] || 10);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
for (let seed = S0; seed < S0 + N; seed++) {
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } }); await ctx.addInitScript((s) => { window.__seed = s; window.__noReload = true; window.requestAnimationFrame = () => 0; }, seed);
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 2).join(' | ')));
  await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
  const t0 = Date.now();
  await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 }); const load = Date.now() - t0;
  const r = await p.evaluate(() => { const R = window.__rd, me = R.me, Z = R.ch.zones; document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })));
    window.__noRender = true; const zi = Z.findIndex((q) => me.foot.x >= q[0] && me.foot.x <= q[2] && me.foot.z >= q[1] && me.foot.z <= q[3]);
    const t = performance.now(); for (let i = 0; i < 1800; i++) R.step(1 / 60); const ms = (performance.now() - t) / 1800;
    const s = R.sec(); const tr = R.tr(); let offRoad = 0; for (const c of R.cars()) if (c.tr && c.state === 'civ' && !R.onRoad(c.x, c.z, 1.5)) offRoad++;
    return { ver: document.getElementById('ver').textContent, passes: R.ch.passes2.length, startOk: R.ch.startZ.includes(zi), bodies: R.bodies.length, dorm: s.dormB.length, cars: R.cars().length, trCars: tr.cars.length, offRoad, ms: +ms.toFixed(2), size: [Math.round(R.ch.mm.x1 - R.ch.mm.x0), Math.round(R.ch.mm.z1 - R.ch.mm.z0)] }; });
  console.log(seed, 'load', load, JSON.stringify(r), errs.length ? 'ERR ' + JSON.stringify(errs.slice(0, 2)) : '');
  await ctx.close();
}
await b.close(); })();
