// 단계별 흉내: A 그대로 → B 먼 구역의 몸·차·문 재우기 → C 먼 구역의 건물·벽·강도 목록에서 빼기 → D 먼 구역 그림 숨기기 + 안 보이는 것 위치 계산 건너뛰기
const { chromium } = require('playwright');
const file = process.argv[2], SC = process.argv[3] || 'army', NA = +(process.argv[4] || 60), RAD = +(process.argv[5] || 45), PROF = process.argv[6];
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--enable-precise-memory-info'] });
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage();
  const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 3).join(' | ')));
  await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
  await p.goto('file://' + __dirname + '/../var/' + file + '.html');
  await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 });
  await p.waitForTimeout(1500);
  await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))));
  await p.waitForTimeout(300);
  await p.evaluate(({ SC, NA, RAD }) => {
    const R = window.__rd, me = R.me, bodies = R.bodies, ren = window.__ren, sc = window.__scene, cam = window.__cam;
    me.hp = me.maxHp = 100000;
    if (SC === 'army') {
      const far = bodies.filter((c) => c.kind === 'citizen' && c.sleep && !c.space && Math.hypot(c.foot.x - me.foot.x, c.foot.z - me.foot.z) > 40).slice(0, NA);
      far.forEach((h, i) => { const a = i * 2.399, r = 1.2 + 0.45 * Math.sqrt(i) * 1.6; h.sleep = false; h.met = true; h.space = null; R.zombify(h); h.foot.x = me.foot.x + Math.cos(a) * r; h.foot.z = me.foot.z + Math.sin(a) * r; h.px = h.foot.x; h.pz = h.foot.z; });
    }
    window.__noRender = true;
    for (let i = 0; i < 180; i++) R.step(1 / 60);
    const Z = R.ch.zones, act = Z.filter(([x0, z0, x1, z1]) => { const dx = Math.max(x0 - me.foot.x, 0, me.foot.x - x1), dz = Math.max(z0 - me.foot.z, 0, me.foot.z - z1); return Math.hypot(dx, dz) < RAD; });
    const inAct = (x, z) => act.some(([x0, z0, x1, z1]) => x > x0 - 6.5 && x < x1 + 6.5 && z > z0 - 6.5 && z < z1 + 6.5);
    const keepIn = (arr, ok, drop) => { let w = 0; for (const o of arr) { if (ok(o)) arr[w++] = o; else if (drop) drop(o); } arr.length = w; };
    window.__S = {
      run: (n) => { for (const k in window.__ph) delete window.__ph[k]; for (const k in window.__pd) delete window.__pd[k]; const t = performance.now(); for (let i = 0; i < n; i++) R.step(1 / 60); const tot = (performance.now() - t) / n; const ph = {}; for (const k in window.__ph) ph[k] = +(window.__ph[k] / n).toFixed(3); for (const k in window.__pd) ph['  ' + k] = +(window.__pd[k] / n).toFixed(3); return { tot: +tot.toFixed(3), ph }; },
      T: (f, n) => { const t = performance.now(); for (let i = 0; i < n; i++) f(); return +((performance.now() - t) / n).toFixed(3); },
      ren: () => window.__S.T(() => ren.render(sc, cam), 40),
      count: () => { let vis = 0; const walk = (o) => { if (!o.visible) return; vis++; for (const c of o.children) walk(c); }; walk(sc); let all = 0; sc.traverse(() => all++); return { bodies: bodies.length, cars: R.cars().length, objs: R.objsL().length, buildings: R.buildings.length, walls: window.__x.walls.length, rivers: R.ch.rivers.length, sceneAll: all, sceneVisible: vis, heapMB: performance.memory ? Math.round(performance.memory.usedJSHeapSize / 1048576) : 0, actZones: act.length }; },
      B: () => {
        keepIn(bodies, (c) => c === me || c.kind === 'ally' || inAct(c.foot.x, c.foot.z), (c) => { for (const k of ['mesh', 'hpBar', 'icon', 'gauge', 'mark', 'tracer', 'tracer2']) if (c[k]) sc.remove(c[k]); });
        const cars = R.cars(), goneObj = new Set();
        keepIn(cars, (c) => inAct(c.x, c.z), (c) => { sc.remove(c.g); if (c.obj) { goneObj.add(c.obj); if (c.obj.hpBar) sc.remove(c.obj.hpBar); } });
        const tr = R.tr(); if (tr) keepIn(tr.cars, (c) => cars.includes(c));
        keepIn(R.objsL(), (o) => !goneObj.has(o) && (!o.foot || inAct(o.foot.x, o.foot.z)), (o) => { if (o.hpBar) sc.remove(o.hpBar); });
        keepIn(R.outProps(), (o) => bodies.includes(o));
        keepIn(window.__x.deco, (o) => !o.car || inAct(o.car.x, o.car.z), (o) => { if (o.hpBar) sc.remove(o.hpBar); });
        for (let i = 0; i < 60; i++) R.step(1 / 60);
      },
      C: () => {
        const rectIn = (x0, z0, x1, z1) => act.some(([a, b, c, d]) => x1 > a - 6.5 && x0 < c + 6.5 && z1 > b - 6.5 && z0 < d + 6.5);
        keepIn(R.buildings, (B) => rectIn(B.x0, B.z0, B.x1, B.z1));
        keepIn(window.__x.walls, (w) => inAct((w[0] + w[2]) / 2, (w[1] + w[3]) / 2));
        keepIn(window.__walls.bs, (B) => rectIn(B.x0, B.z0, B.x1, B.z1));
        keepIn(R.ch.rivers, (r) => rectIn(r[0], r[1], r[2], r[3]));
        window.__x.reset();
        for (let i = 0; i < 60; i++) R.step(1 / 60);
      },
      D: () => {
        let hid = 0; for (const o of sc.children) { if (!o.visible || o.frustumCulled === false) continue; const x = o.position.x, z = o.position.z; if ((x !== 0 || z !== 0) && !inAct(x, z)) { o.visible = false; hid++; } }
        const O3 = Object.getPrototypeOf(Object.getPrototypeOf(sc)), umw = O3.updateMatrixWorld;
        O3.updateMatrixWorld = function (force) { if (this.visible === false) return; umw.call(this, force); };
        return hid;
      },
    };
  }, { SC, NA, RAD });
  const pr = (t, r, ren) => { console.log(t.padEnd(34), 'calc', String(r.tot).padStart(7), ' render', String(ren).padStart(7), ' sum', (r.tot + ren).toFixed(2)); return r; };
  const all = {};
  const step = async (name, pre) => { if (pre) await p.evaluate(pre); const c = await p.evaluate(() => window.__S.count()); const r = await p.evaluate(() => window.__S.run(400)); const ren = await p.evaluate(() => window.__S.ren()); all[name] = { c, r, ren }; pr(name, r, ren); console.log('   ', JSON.stringify(c)); };
  await step('A 그대로');
  await step('B 먼 구역 몸·차·문 재움', () => window.__S.B());
  await step('C + 먼 건물·벽·강 목록에서 뺌', () => window.__S.C());
  await step('D + 먼 그림 숨김·위치계산 생략', () => { window.__hid = window.__S.D(); });
  require('fs').writeFileSync(__dirname + '/freeze2_' + file + '_' + SC + '.json', JSON.stringify(all));
  const keys = Object.keys(all['A 그대로'].r.ph);
  console.log('\n' + '구간'.padEnd(26) + Object.keys(all).map((k) => k.slice(0, 1).padStart(8)).join(''));
  for (const k of keys) { const v = Object.values(all).map((a) => a.r.ph[k] || 0); if (Math.max(...v) < 0.04) continue; console.log(k.padEnd(26) + v.map((x) => x.toFixed(3).padStart(8)).join('')); }
  if (errs.length) console.log('ERR', errs.slice(0, 5));
  await b.close();
})();
