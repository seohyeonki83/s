// 본 맵: 평소 프레임 시간 + 경보 단계가 오를 때 한 걸음이 얼마나 걸리나
const { chromium } = require('playwright');
const file = process.argv[2] || 'perf6m', SEED = +(process.argv[3] || 1);
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--enable-precise-memory-info'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } }); await ctx.addInitScript((s) => { window.__seed = s; window.__noReload = true; window.__secOff = true; window.requestAnimationFrame = () => 0; }, SEED);
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 3).join(' | ')));
  await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
  const t0 = Date.now();
  await p.goto('file://' + __dirname + '/../var/' + file + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 }); const load = Date.now() - t0;
  const out = await p.evaluate(() => {
    const R = window.__rd, me = R.me, bodies = R.bodies, ren = window.__ren, sc = window.__scene, cam = window.__cam, res = {};
    document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })));
    me.hp = me.maxHp = 1e6;
    const near = bodies.filter((c) => c.kind === 'citizen' && !c.space).sort((a, c) => Math.hypot(a.foot.x - me.foot.x, a.foot.z - me.foot.z) - Math.hypot(c.foot.x - me.foot.x, c.foot.z - me.foot.z)).slice(0, 60);
    near.forEach((h, i) => { const a = i * 2.399, r = 1.2 + 0.45 * Math.sqrt(i) * 1.6; h.sleep = false; h.met = true; h.space = null; R.zombify(h); h.foot.x = me.foot.x + Math.cos(a) * r; h.foot.z = me.foot.z + Math.sin(a) * r; h.px = h.foot.x; h.pz = h.foot.z; });
    window.__secOff = false; window.__noRender = true;
    const one = () => { const t = performance.now(); R.step(1 / 60); return performance.now() - t; };
    for (let i = 0; i < 180; i++) one();
    const run = (n) => { for (const k in window.__ph) delete window.__ph[k]; let tot = 0, mx = 0; for (let i = 0; i < n; i++) { const d = one(); tot += d; if (d > mx) mx = d; } const ph = {}; for (const k in window.__ph) ph[k] = +(window.__ph[k] / n).toFixed(3); return { avg: +(tot / n).toFixed(3), max: +mx.toFixed(1), ph }; };
    res.steady = run(600);
    const T = (f, n) => { const t = performance.now(); for (let i = 0; i < n; i++) f(); return +((performance.now() - t) / n).toFixed(3); };
    res.render = T(() => ren.render(sc, cam), 40);
    res.secs = window.__secs();
    res.stage = [];
    for (let s = 1; s <= 5; s++) { const t = performance.now(); R.setStars(s); const t1 = performance.now() - t; const worst = []; for (let i = 0; i < 90; i++) worst.push(one()); worst.sort((a, c) => c - a); const q = window.__secs();
      res.stage.push({ s, setStars: +t1.toFixed(1), worstSteps: worst.slice(0, 3).map((v) => +v.toFixed(1)), bodies: bodies.length, dormB: q.dormB, cars: q.cars, dormC: q.dormC }); for (let i = 0; i < 240; i++) one(); }
    res.after = run(300); res.secs2 = window.__secs(); res.heapMB = performance.memory ? Math.round(performance.memory.usedJSHeapSize / 1048576) : 0;
    return res;
  });
  console.log(file, 'seed', SEED, 'load ms', load);
  console.log('steady avg', out.steady.avg, 'max', out.steady.max, 'render', out.render, JSON.stringify(out.secs));
  console.log('  ' + Object.entries(out.steady.ph).sort((a, c) => c[1] - a[1]).slice(0, 10).map(([k, v]) => k.split(' ', 2)[1] + ' ' + v).join(' | '));
  for (const s of out.stage) console.log('stage', JSON.stringify(s));
  console.log('after stage 5: avg', out.after.avg, 'max', out.after.max, JSON.stringify(out.secs2), 'heapMB', out.heapMB);
  console.log('  ' + Object.entries(out.after.ph).sort((a, c) => c[1] - a[1]).slice(0, 10).map(([k, v]) => k.split(' ', 2)[1] + ' ' + v).join(' | '));
  if (errs.length) console.log('ERR', errs.slice(0, 4));
  await b.close();
})();
