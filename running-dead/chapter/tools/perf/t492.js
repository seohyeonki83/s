// 출동했던 경찰이 내가 다른 단락으로 넘어간 뒤에도 따라오나 — 같은 씨앗으로 버전끼리 비교
// node t492.js <var 파일> <씨앗>
const { chromium } = require('playwright');
const V = process.argv[2], SEED = +(process.argv[3] || 11);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
await ctx.addInitScript((sd) => { let s = sd; Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; let u = 777; globalThis.__uu = () => { u = (u * 1103515245 + 12345) >>> 0; return u / 4294967296; }; window.requestAnimationFrame = () => 0; let t = 1000; performance.now = () => (t += 0.01); Date.now = () => 1700000000000; window.__noReload = true; }, SEED);
const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 2).join(' | ')));
const three = require('fs').readFileSync(__dirname + '/../node_modules/three/build/three.module.min.js', 'utf8').split('4294967295*Math.random()').join('4294967295*globalThis.__uu()');
await p.route('**/three.module.min.js', (r) => r.fulfill({ body: three, contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 }); await p.waitForTimeout(500);
const out = await p.evaluate(() => {
  const R = window.__rd, me = R.me, log = [], Z = R.ch.zones, P = R.ch.passes2;
  const ok = () => document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })));
  ok(); window.__noRender = true; me.hp = me.maxHp = 1e7;
  const step = (n) => { for (let i = 0; i < n; i++) { R.step(1 / 60); if (i % 30 === 0) ok(); } };
  const walkTo = (tx, tz, sp = 0.07) => { for (let k = 0; k < 20000; k++) { const dx = tx - me.foot.x, dz = tz - me.foot.z, d = Math.hypot(dx, dz); if (d < 0.5) break; me.foot.x += dx / d * sp; me.foot.z += dz / d * sp; me.px = me.foot.x; me.pz = me.foot.z; R.step(1 / 60); if (k % 30 === 0) ok(); } };
  const all = () => R.bodies.concat(R.sec ? R.sec().dormB : []);
  const mz = Z.findIndex((q) => me.foot.x >= q[0] - 3 && me.foot.x <= q[2] + 3 && me.foot.z >= q[1] - 3 && me.foot.z <= q[3] + 3);
  const pass = P.find((q) => q.za === mz || q.zb === mz), other = pass.za === mz ? pass.zb : pass.za, fa = pass.za === mz, A = fa ? [pass.ax, pass.az] : [pass.bx, pass.bz], B = fa ? [pass.bx, pass.bz] : [pass.ax, pass.az];
  R.setStars(3);
  step(60 * 90);                                 // 90초 — 출동이 서너 번 온다. 나는 둘레 사람을 알아서 문다
  const duty = all().filter((c) => c.kind === 'citizen' && c.police && c.onDuty && !c.military);
  const mob = all().filter((c) => c.kind === 'citizen' && c.police && !c.post && !c.sleep);
  log.push({ t: '떠나기 직전 (구역 ' + mz + ')', onDuty: duty.length, awakeMobilePolice: mob.length, allies: R.bodies.filter((c) => c.kind === 'ally').length, stars: R.stars ? R.stars() : null });
  // 동료는 데리고 간다 (남겨 두면 그 단락이 계속 깨어 있다) — 나를 따라 순간이동
  const bring = () => { for (const c of R.bodies) if (c.kind === 'ally') { c.foot.x = me.foot.x + (Math.random() - 0.5) * 3; c.foot.z = me.foot.z + (Math.random() - 0.5) * 3; c.px = c.foot.x; c.pz = c.foot.z; c.space = null; } };
  const q = Z[mz], ax = Math.max(q[0] + 2.25, Math.min(q[2] - 2.25, A[0])), az = Math.max(q[1] + 2.25, Math.min(q[3] - 2.25, A[1]));
  walkTo(ax, az); walkTo(A[0], A[1]); bring(); walkTo(B[0], B[1]); bring();
  const q2 = Z[other]; const tx = B[0] < q2[0] + 5 ? q2[2] - 2.25 : B[0] > q2[2] - 5 ? q2[0] + 2.25 : B[0], tz = B[1] < q2[1] + 5 ? q2[3] - 2.25 : B[1] > q2[3] - 5 ? q2[1] + 2.25 : B[1];
  walkTo(Math.max(q2[0] + 2.25, Math.min(q2[2] - 2.25, B[0])), Math.max(q2[1] + 2.25, Math.min(q2[3] - 2.25, B[1]))); bring();
  walkTo(tx, tz); bring();                       // 건너편 단락의 맞은편 변까지
  const rep = (t) => { const S = duty.filter((c) => c.kind === 'citizen'); const nearMe = (c) => Math.hypot(c.foot.x - me.foot.x, c.foot.z - me.foot.z) < 15;
    const inB = (c) => c.foot.x >= q2[0] - 7 && c.foot.x <= q2[2] + 7 && c.foot.z >= q2[1] - 7 && c.foot.z <= q2[3] + 7;
    return { t, live: R.sec ? R.sec().secs.filter((x) => x.live).map((x) => x.i).join('') : 'n/a', dutyAlive: S.length, dutyDormant: S.filter((c) => c.dorm).length, dutyWithCalls: S.filter((c) => c.calls && c.calls.length).length, dutyInMyZone: S.filter(inB).length, dutyNearMe: S.filter(nearMe).length, policeNearMe: all().filter((c) => c.kind === 'citizen' && c.police && !c.dorm && nearMe(c)).length, driveCars: R.cars().filter((c) => c.state === 'drive').length, parkedWithCrew: R.cars().concat(R.sec ? R.sec().dormC : []).filter((c) => c.state === 'parked' && c.crew && c.crew.length).length, deaths: R.bodies.filter((c) => c.kind === 'ally').length }; };
  log.push(rep('건너간 직후'));
  for (let k = 1; k <= 4; k++) { step(60 * 30); log.push(rep(k * 30 + '초 뒤')); }
  return log;
});
console.log('==', V, 'seed', SEED); for (const r of out) console.log(JSON.stringify(r)); if (errs.length) console.log('ERR', JSON.stringify(errs.slice(0, 3)));
await b.close(); })();
