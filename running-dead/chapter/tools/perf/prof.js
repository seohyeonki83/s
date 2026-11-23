// 함수별 시간 (크롬 프로파일러): node perf/prof.js <variant> <idle|army> [allies] [freezeRadius] [render:0|1]
const { chromium } = require('playwright');
const file = process.argv[2], SC = process.argv[3] || 'army', NA = +(process.argv[4] || 60), RAD = +(process.argv[5] || 0), REN = +(process.argv[6] || 0);
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage();
  const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 3).join(' | ')));
  await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
  await p.goto('file://' + __dirname + '/../var/' + file + '.html');
  await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 });
  await p.waitForTimeout(1500);
  await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))));
  await p.waitForTimeout(300);
  await p.evaluate(({ SC, NA, RAD }) => {
    const R = window.__rd, me = R.me, bodies = R.bodies, sc = window.__scene;
    me.hp = me.maxHp = 100000;
    if (SC === 'army') {
      const far = bodies.filter((c) => c.kind === 'citizen' && c.sleep && !c.space && Math.hypot(c.foot.x - me.foot.x, c.foot.z - me.foot.z) > 40).slice(0, NA);
      far.forEach((h, i) => { const a = i * 2.399, r = 1.2 + 0.45 * Math.sqrt(i) * 1.6; h.sleep = false; h.met = true; h.space = null; R.zombify(h); h.foot.x = me.foot.x + Math.cos(a) * r; h.foot.z = me.foot.z + Math.sin(a) * r; h.px = h.foot.x; h.pz = h.foot.z; });
    }
    window.__noRender = true;
    for (let i = 0; i < 180; i++) R.step(1 / 60);
    if (RAD > 0) {
      const Z = R.ch.zones, act = Z.filter(([x0, z0, x1, z1]) => { const dx = Math.max(x0 - me.foot.x, 0, me.foot.x - x1), dz = Math.max(z0 - me.foot.z, 0, me.foot.z - z1); return Math.hypot(dx, dz) < RAD; });
      const inAct = (x, z) => act.some(([x0, z0, x1, z1]) => x > x0 - 6.5 && x < x1 + 6.5 && z > z0 - 6.5 && z < z1 + 6.5);
      let w = 0; for (const c of bodies) { if (c === me || c.kind === 'ally' || inAct(c.foot.x, c.foot.z)) { bodies[w++] = c; continue; } for (const k of ['mesh', 'hpBar', 'icon', 'gauge', 'mark', 'tracer', 'tracer2']) if (c[k]) sc.remove(c[k]); }
      bodies.length = w;
      const cars = R.cars(); w = 0; const goneObj = new Set();
      for (const c of cars) { if (inAct(c.x, c.z)) { cars[w++] = c; continue; } sc.remove(c.g); if (c.obj) { goneObj.add(c.obj); if (c.obj.hpBar) sc.remove(c.obj.hpBar); } }
      cars.length = w;
      const tr = R.tr(); if (tr) { const keep = tr.cars.filter((c) => cars.includes(c)); tr.cars.length = 0; for (const c of keep) tr.cars.push(c); }
      const objs = R.objsL(); w = 0; for (const o of objs) { if (!goneObj.has(o) && (!o.foot || inAct(o.foot.x, o.foot.z))) { objs[w++] = o; continue; } if (o.hpBar) sc.remove(o.hpBar); if (o.mesh) sc.remove(o.mesh); } objs.length = w;
      const op = R.outProps(); w = 0; for (const o of op) if (bodies.includes(o)) op[w++] = o; op.length = w;
      for (let i = 0; i < 60; i++) R.step(1 / 60);
    }
  }, { SC, NA, RAD });
  const cdp = await p.context().newCDPSession(p);
  await cdp.send('Profiler.enable'); await cdp.send('Profiler.setSamplingInterval', { interval: 100 });
  await cdp.send('Profiler.start');
  const N = 600;
  const tot = await p.evaluate(({ N, REN }) => { window.__noRender = !REN; const t = performance.now(); for (let i = 0; i < N; i++) window.__rd.step(1 / 60); return (performance.now() - t) / N; }, { N, REN });
  const { profile } = await cdp.send('Profiler.stop');
  const dt = profile.timeDeltas, ids = profile.samples, self = new Map(), byId = new Map();
  for (const n of profile.nodes) byId.set(n.id, n);
  for (let i = 0; i < ids.length; i++) self.set(ids[i], (self.get(ids[i]) || 0) + dt[i]);
  // 포함 시간: 자식 합
  const parent = new Map(); for (const n of profile.nodes) for (const c of n.children || []) parent.set(c, n.id);
  const selfF = {}, inclF = {};
  for (const [id, us] of self) {
    const n = byId.get(id), name = (n.callFrame.functionName || '(anon)') + ':' + (n.callFrame.lineNumber + 1);
    selfF[name] = (selfF[name] || 0) + us;
    const seen = new Set(); let cur = id;
    while (cur !== undefined) { const m = byId.get(cur), nm = (m.callFrame.functionName || '(anon)') + ':' + (m.callFrame.lineNumber + 1); if (!seen.has(nm)) { seen.add(nm); inclF[nm] = (inclF[nm] || 0) + us; } cur = parent.get(cur); }
  }
  const top = (o, k) => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, k).map(([n, us]) => (us / 1000 / N).toFixed(3).padStart(7) + '  ' + n).join('\n');
  console.log(file, SC, 'freeze', RAD, 'render', REN, 'ms/step', tot.toFixed(3));
  { const o = {}; for (const [n, us] of Object.entries(selfF)) o[n.split(':')[0]] = (o[n.split(':')[0]] || 0) + us / 1000 / N; const oi = {}; for (const [n, us] of Object.entries(inclF)) oi[n.split(':')[0]] = Math.max(oi[n.split(':')[0]] || 0, us / 1000 / N); require('fs').writeFileSync(__dirname + '/prof_' + file + '_' + SC + '_' + RAD + '_' + REN + '.json', JSON.stringify({ tot, self: o, incl: oi })); if (process.argv[7] === 'q') { await b.close(); return; } }
  console.log('--- self (ms/step)'); console.log(top(selfF, 42));
  console.log('--- inclusive (ms/step)'); console.log(top(inclF, 45));
  if (errs.length) console.log('ERR', errs.slice(0, 5));
  await b.close();
})();
