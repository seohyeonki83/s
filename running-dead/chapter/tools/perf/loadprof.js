// 시작(맵 만들기 + 깔기) 시간을 함수별로: node perf/loadprof.js <variant> [seed]
const { chromium } = require('playwright');
const file = process.argv[2], SEED = +(process.argv[3] || 1);
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } }); await ctx.addInitScript((s) => { window.__seed = s; window.requestAnimationFrame = () => 0; }, SEED);
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
  await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
  const cdp = await p.context().newCDPSession(p);
  await cdp.send('Profiler.enable'); await cdp.send('Profiler.setSamplingInterval', { interval: 200 }); await cdp.send('Profiler.start');
  const t0 = Date.now();
  await p.goto('file://' + __dirname + '/../var/' + file + '.html');
  await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 });
  const load = Date.now() - t0;
  const { profile } = await cdp.send('Profiler.stop');
  const dt = profile.timeDeltas, ids = profile.samples, self = new Map(), byId = new Map(), parent = new Map();
  for (const n of profile.nodes) { byId.set(n.id, n); for (const c of n.children || []) parent.set(c, n.id); }
  for (let i = 0; i < ids.length; i++) self.set(ids[i], (self.get(ids[i]) || 0) + dt[i]);
  const selfF = {}, inclF = {};
  for (const [id, us] of self) { const n = byId.get(id), name = (n.callFrame.functionName || '(anon)') + ':' + (n.callFrame.lineNumber + 1); selfF[name] = (selfF[name] || 0) + us;
    const seen = new Set(); let cur = id; while (cur !== undefined) { const m = byId.get(cur), nm = (m.callFrame.functionName || '(anon)') + ':' + (m.callFrame.lineNumber + 1); if (!seen.has(nm)) { seen.add(nm); inclF[nm] = (inclF[nm] || 0) + us; } cur = parent.get(cur); } }
  const top = (o, k) => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, k).map(([n, us]) => (us / 1000).toFixed(0).padStart(6) + '  ' + n).join('\n');
  console.log(file, 'load ms', load); console.log('--- self ms'); console.log(top(selfF, 22)); console.log('--- inclusive ms'); console.log(top(inclF, 34));
  if (errs.length) console.log('ERR', errs.slice(0, 3));
  await b.close();
})();
