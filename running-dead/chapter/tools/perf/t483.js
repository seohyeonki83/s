// c405: 추적하는 출동 병력은 다른 단락에서도 계속 움직이나 · 건널목 수비대가 사라지지 않나
const { chromium } = require('playwright');
const V = process.argv[2] || 'c405';
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
await ctx.addInitScript(() => { window.requestAnimationFrame = () => 0; });
const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 3).join(' | ')));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(500);
const out = await p.evaluate(() => {
  const R = window.__rd, me = R.me, log = [];
  document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })));
  window.__noRender = true; me.hp = me.maxHp = 1e6;
  const step = (n) => { for (let i = 0; i < n; i++) { R.step(1 / 60); document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); } };
  const walkTo = (tx, tz, sp = 0.07) => { for (let k = 0; k < 20000; k++) { const dx = tx - me.foot.x, dz = tz - me.foot.z, d = Math.hypot(dx, dz); if (d < 0.5) break; me.foot.x += dx / d * sp; me.foot.z += dz / d * sp; me.px = me.foot.x; me.pz = me.foot.z; R.step(1 / 60); } };
  const Z = R.ch.zones, P = R.ch.passes2, S = () => R.sec();
  const mz = Z.findIndex((q) => me.foot.x >= q[0] - 3 && me.foot.x <= q[2] + 3 && me.foot.z >= q[1] - 3 && me.foot.z <= q[3] + 3);
  const pass = P.find((q) => q.za === mz || q.zb === mz), other = pass.za === mz ? pass.zb : pass.za, fa = pass.za === mz, A = fa ? [pass.ax, pass.az] : [pass.bx, pass.bz], B = fa ? [pass.bx, pass.bz] : [pass.ax, pass.az];
  step(30);
  const bar0 = R.bar().X.map((X) => X.units.length);
  R.setStars(1); step(60);
  const bar1 = R.bar().X.map((X) => ({ units: X.units.length, dorm: X.units.filter((c) => c.dorm).length, pieces: X.rows.flat().flat().filter(Boolean).length, dormPieces: X.rows.flat().flat().filter((q) => q && q.car.dorm).length }));
  log.push({ tag: '경보 1단계 뒤 수비대', bar0, bar1 });
  R.setStars(3); step(60 * 32);   // 32초 — 출동이 한두 번 온다
  const tr = R.bodies.filter((c) => c.kind === 'citizen' && c.police && ((c.calls && c.calls.length) || c.heading)), trC = R.cars().filter((c) => c.state === 'drive' || c.state === 'brake' || (c.crew && c.crew.length));
  log.push({ tag: '출동 병력 (내 구역 ' + mz + ')', onFoot: tr.length, cars: trC.length, awakePolice: R.bodies.filter((c) => c.kind === 'citizen' && c.police && !c.sleep).length });
  // 다른 구역으로 건너간다
  const q = Z[mz]; const ax = Math.max(q[0] + 2.25, Math.min(q[2] - 2.25, A[0])), az = Math.max(q[1] + 2.25, Math.min(q[3] - 2.25, A[1]));
  walkTo(ax, az); walkTo(A[0], A[1]); walkTo(B[0], B[1]);
  const q2 = Z[other], bx = Math.max(q2[0] + 2.25, Math.min(q2[2] - 2.25, B[0])), bz = Math.max(q2[1] + 2.25, Math.min(q2[3] - 2.25, B[1]));
  walkTo(bx, bz);
  const far = [bx === q2[0] + 2.25 ? q2[2] - 2.25 : bx === q2[2] - 2.25 ? q2[0] + 2.25 : bx, bz === q2[1] + 2.25 ? q2[3] - 2.25 : bz === q2[3] - 2.25 ? q2[1] + 2.25 : bz];   // 맞은편 변
  walkTo(far[0], bz === q2[1] + 2.25 || bz === q2[3] - 2.25 ? bz : far[1]); walkTo(far[0], far[1]);
  const rep = (tag) => { const s = S(), all = R.bodies.concat(s.dormB);
    const pol = all.filter((c) => c.kind === 'citizen' && c.police);
    const chasing = pol.filter((c) => !c.dorm && !c.sleep && (c.state !== 'normal' || (c.calls && c.calls.length) || c.heading));
    const inOther = (c) => c.foot.x >= q2[0] - 7 && c.foot.x <= q2[2] + 7 && c.foot.z >= q2[1] - 7 && c.foot.z <= q2[3] + 7;
    return { tag, live: s.secs.filter((x) => x.live).map((x) => x.i).join(''), police: pol.length, dormPolice: pol.filter((c) => c.dorm).length, chasing: chasing.length, chasingHere: chasing.filter(inOther).length, chasingNear: chasing.filter((c) => Math.hypot(c.foot.x - me.foot.x, c.foot.z - me.foot.z) < 12).length,
      trackersStillTracked: tr.filter((c) => c.kind === 'citizen' && !c.dorm).length + '/' + tr.length, driveCars: R.cars().filter((c) => c.state === 'drive').length, dormDrive: s.dormC.filter((c) => c.state === 'drive' || c.state === 'brake').length, me: [Math.round(me.foot.x), Math.round(me.foot.z)] }; };
  log.push(rep('건너간 직후'));
  for (let k = 0; k < 6; k++) { step(60 * 10); log.push(rep((k + 1) * 10 + '초 뒤')); }
  R.setStars(5); step(120);
  const bar2 = R.bar().X.map((X) => ({ units: X.units.length, dorm: X.units.filter((c) => c.dorm).length, pieces: X.rows.flat().flat().filter(Boolean).length, dormPieces: X.rows.flat().flat().filter((q) => q && q.car.dorm).length, live: X.rows.flat().flat().filter((q) => q && !q.car.wreck && (q.car.dorm || R.cars().includes(q.car))).length }));
  log.push({ tag: '경보 5단계 뒤 수비대', bar2 });
  return log;
});
for (const r of out) console.log(JSON.stringify(r));
console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
