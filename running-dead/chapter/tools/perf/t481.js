// c405: 단락 재우기 동작 검사 — 다리 건너기 · 불변식 · 새 판
const { chromium } = require('playwright');
const V = process.argv[2] || 'c405', MODE = process.argv[3] || 'cross';
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
await ctx.addInitScript(() => { window.requestAnimationFrame = () => 0; });   // 걸음은 손으로 돌린다
const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 3).join(' | ')));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(500);
const out = await p.evaluate((MODE) => {
  const R = window.__rd, me = R.me, log = [];
  document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })));
  window.__noRender = true; me.hp = me.maxHp = 1e6;
  const S = () => R.sec();
  const inv = (tag) => {   // 불변식
    const s = S(), bad = [];
    const setB = new Set(R.bodies);
    for (const d of s.dormB) { if (!d.dorm) bad.push('dormB without flag'); if (setB.has(d)) bad.push('dorm body in bodies'); if (d === me || d.kind === 'ally') bad.push('zombie dormant'); }
    for (const c of R.bodies) if (c.dorm) bad.push('active body with dorm flag ' + c.kind);
    const zs = R.bodies.filter((c) => c.kind === 'ally' || c === me);
    let near = 0; for (const d of s.dormB) for (const z of zs) if (Math.hypot(d.foot.x - z.foot.x, d.foot.z - z.foot.z) < 10) near++;
    if (near) bad.push('dormant body within 10 of a zombie: ' + near);
    let nearC = 0; for (const d of s.dormC) for (const z of zs) if (Math.hypot(d.x - z.foot.x, d.z - z.foot.z) < 10) nearC++;
    if (nearC) bad.push('dormant car within 10 of a zombie: ' + nearC);
    const setP = new Set(s.props); for (const q of s.props) if (!setB.has(q) && !q.dead) bad.push('prop not in bodies');
    const cars = R.cars(), setC = new Set(cars); for (const c of s.dormC) if (setC.has(c)) bad.push('dorm car in cars');
    for (const o of s.objs) { if (o.dorm) bad.push('obj with dorm flag'); if (o.type === 'car' && o.car && o.car.dorm) bad.push('obj of dormant car in objs'); }
    for (const d of s.dormB) for (const k of ['mesh', 'hpBar', 'icon', 'gauge', 'mark', 'tracer']) if (d[k] && d[k].parent) bad.push('dormant body ' + k + ' still in scene');
    for (const c of R.bodies) if (c.mesh && !c.mesh.parent) bad.push('active body mesh not in scene ' + c.kind + (c.prop || ''));
    return { tag, live: s.secs.filter((q) => q.live).map((q) => q.i).join(''), bodies: R.bodies.length, dormB: s.dormB.length, cars: cars.length, dormC: s.dormC.length, objs: s.objs.length, dormO: s.dormO.length, props: s.props.length, scene: s.scene.children.length, awake: R.bodies.filter((c) => c.kind === 'citizen' && !c.sleep).length, bad: [...new Set(bad)].slice(0, 6) };
  };
  const step = (n) => { for (let i = 0; i < n; i++) R.step(1 / 60); };
  const walkTo = (tx, tz, sp = 0.09) => { for (let k = 0; k < 20000; k++) { const dx = tx - me.foot.x, dz = tz - me.foot.z, d = Math.hypot(dx, dz); if (d < 0.5) break; me.foot.x += dx / d * sp; me.foot.z += dz / d * sp; me.px = me.foot.x; me.pz = me.foot.z; R.step(1 / 60); } };
  const Z = R.ch.zones, P = R.ch.passes2;
  step(30); log.push(inv('start'));
  const total0 = R.bodies.length + S().dormB.length, cars0 = R.cars().length + S().dormC.length;
  // 동료 12명
  { const cs = S().dormB.filter((c) => c.kind === 'citizen').slice(0, 12); window.__secOff = true; for (const S2 of S().secs) S2.live = true; }
  if (MODE === 'cross' || MODE === 'soak') {
    const mz = Z.findIndex((q) => me.foot.x >= q[0] - 3 && me.foot.x <= q[2] + 3 && me.foot.z >= q[1] - 3 && me.foot.z <= q[3] + 3);
    const pass = P.find((q) => q.za === mz || q.zb === mz), other = pass.za === mz ? pass.zb : pass.za;
    const A = pass.za === mz ? [pass.ax, pass.az] : [pass.bx, pass.bz], B = pass.za === mz ? [pass.bx, pass.bz] : [pass.ax, pass.az];
    window.__secOff = false;
    // 동료: 가까운 사람 몇을 좀비로
    const near = R.bodies.filter((c) => c.kind === 'citizen' && !c.space).sort((a, c) => Math.hypot(a.foot.x - me.foot.x, a.foot.z - me.foot.z) - Math.hypot(c.foot.x - me.foot.x, c.foot.z - me.foot.z)).slice(0, 10);
    near.forEach((h, i) => { h.sleep = false; h.met = true; R.zombify(h); h.foot.x = me.foot.x + 1 + i * 0.5; h.foot.z = me.foot.z + 1; h.px = h.foot.x; h.pz = h.foot.z; });
    step(60); log.push(inv('allies'));
    walkTo(A[0], A[1]); log.push(inv('at bridge end A z' + mz));
    walkTo((A[0] + B[0]) / 2, (A[1] + B[1]) / 2); log.push(inv('mid bridge'));
    walkTo(B[0], B[1]); log.push(inv('at bridge end B z' + other));
    const q = Z[other]; walkTo((q[0] + q[2]) / 2, (q[1] + q[3]) / 2); step(300); log.push(inv('center of zone ' + other));
    walkTo(B[0], B[1]); walkTo(A[0], A[1]); const q0 = Z[mz]; walkTo((q0[0] + q0[2]) / 2, (q0[1] + q0[3]) / 2); step(300); log.push(inv('back in zone ' + mz));
    const total1 = R.bodies.length + S().dormB.length, cars1 = R.cars().length + S().dormC.length;
    log.push({ tag: 'totals', bodies: [total0, total1], cars: [cars0, cars1] });
    if (MODE === 'soak') {
      let s = 7; const rnd = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
      // 순환도로 위 점만 골라서, 다른 구역으로는 건널목을 거쳐 간다 (건물·산을 뚫고 가지 않게)
      const zoneOf = () => Z.findIndex((q) => me.foot.x >= q[0] - 0.5 && me.foot.x <= q[2] + 0.5 && me.foot.z >= q[1] - 0.5 && me.foot.z <= q[3] + 0.5);
      const ring = (zi) => { const q = Z[zi], t = rnd(); return rnd() < 0.5 ? [q[0] + 2.25 + t * (q[2] - q[0] - 4.5), rnd() < 0.5 ? q[1] + 2.25 : q[3] - 2.25] : [rnd() < 0.5 ? q[0] + 2.25 : q[2] - 2.25, q[1] + 2.25 + t * (q[3] - q[1] - 4.5)]; };
      const ringTo = (zi, tx, tz, sp) => { const q = Z[zi], cs = [[q[0] + 2.25, q[1] + 2.25], [q[2] - 2.25, q[1] + 2.25], [q[2] - 2.25, q[3] - 2.25], [q[0] + 2.25, q[3] - 2.25]];   // 순환도로를 따라 모서리를 돌아서
        const onE = (x, z) => Math.abs(x - (q[0] + 2.25)) < 0.3 ? 3 : Math.abs(z - (q[1] + 2.25)) < 0.3 ? 0 : Math.abs(x - (q[2] - 2.25)) < 0.3 ? 1 : 2;
        let e = onE(me.foot.x, me.foot.z); const te = onE(tx, tz); for (let g = 0; g < 4 && e !== te; g++) { const c = cs[(e + 1) % 4]; walkTo(c[0], c[1], sp); e = (e + 1) % 4; } walkTo(tx, tz, sp); };
      const snap = (zi) => { const q = Z[zi]; const x = Math.max(q[0] + 2.25, Math.min(q[2] - 2.25, me.foot.x)), z = Math.max(q[1] + 2.25, Math.min(q[3] - 2.25, me.foot.z)); const d = [x - (q[0] + 2.25), (q[2] - 2.25) - x, z - (q[1] + 2.25), (q[3] - 2.25) - z], m = Math.min(...d); walkTo(m === d[0] ? q[0] + 2.25 : m === d[1] ? q[2] - 2.25 : x, m === d[2] ? q[1] + 2.25 : m === d[3] ? q[3] - 2.25 : z); };
      for (let leg = 0; leg < 16; leg++) { if (leg === 3) R.setStars(2); if (leg === 6) R.setStars(4); if (leg === 9) R.setStars(5);
        let cz = zoneOf(); if (cz < 0) { log.push({ tag: 'lost zone', at: [me.foot.x, me.foot.z] }); break; }
        snap(cz);
        if (rnd() < 0.6) { const ps = P.filter((q) => q.za === cz || q.zb === cz), pp = ps[Math.floor(rnd() * ps.length)], fa = pp.za === cz, A2 = fa ? [pp.ax, pp.az] : [pp.bx, pp.bz], B2 = fa ? [pp.bx, pp.bz] : [pp.ax, pp.az];
          const q = Z[cz], ax = Math.max(q[0] + 2.25, Math.min(q[2] - 2.25, A2[0])), az = Math.max(q[1] + 2.25, Math.min(q[3] - 2.25, A2[1]));
          ringTo(cz, ax, az, 0.11); walkTo(A2[0], A2[1], 0.11); walkTo(B2[0], B2[1], 0.11); cz = fa ? pp.zb : pp.za; snap(cz); }
        const t = ring(cz); ringTo(cz, t[0], t[1], 0.11); step(150); const r = inv('leg ' + leg + ' z' + cz); if (r.bad.length || leg % 3 === 2) log.push(r); }
    }
    // 새 판
    R.spawn(); const s2 = S(); log.push({ tag: 'after spawn (before step)', bodies: R.bodies.length, dormB: s2.dormB.length, dormC: s2.dormC.length, dormO: s2.dormO.length, scene: s2.scene.children.length });
    step(30); log.push(inv('new game'));
  }
  return log;
}, MODE);
for (const r of out) console.log(JSON.stringify(r));
console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
