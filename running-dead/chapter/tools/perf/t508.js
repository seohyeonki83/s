// c430: 괴물 · 흡수 좀비
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c430z.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1200);
const r = await p.evaluate(() => { const R = window.__rd, me = R.me, o = {}; document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); me.hp = me.maxHp = 1e9;
  const mk = () => { const c = R.bodies.find((b) => b.kind === 'citizen' && b.sleep && !b.space); c.sleep = false; R.zombify(c); return c; };
  // 기본 (갈림길 전)
  const a0 = mk(); window.__mut(a0); o.base = { mut: a0.mut, force: a0.force, hyd: R.HK(a0), spl: R.SK(a0) };
  // 변이 주사 = 괴물 빨간 ★6
  R.setLv('mutate', 12); R.BR.mutate = 'monster';
  const a1 = mk(); let t = 0; do { window.__mut(a1); } while (a1.mut !== 'armor' && ++t < 20); o.monArmor = { mut: a1.mut, force: a1.force, spl: R.SK(a1).toFixed(2) };
  const a2 = mk(); t = 0; do { window.__mut(a2); } while (a2.mut !== 'hydra' && ++t < 20); o.monHyd = { mut: a2.mut, hyd: R.HK(a2).toFixed(2) };
  for (let i = 0; i < 3; i++) R.step(1 / 60); o.halo = { armor: !!a1.brHalo, col: a1.brHalo && a1.brHalo.material.color.getHex().toString(16) };
  // 괴물 덩치가 차를 친다 → 차 넉백 + 스플래시
  const car = R.cars().find((c) => c.state === 'parked' && c.obj && !c.obj.dead && !c.wall); if (car) { a1.foot.x = car.x - 1.6; a1.foot.z = car.z; const cx = car.x, cz = car.z;
    const v = R.bodies.find((b) => b.kind === 'citizen' && b.maxHp > 0 && b !== a1 && !b.space); v.sleep = false; v.foot.x = car.x + 0.9; v.foot.z = car.z; const h0 = v.hp;
    R.LH(a1, car.obj, 10); for (let i = 0; i < 30; i++) R.step(1 / 60); o.carHit = { moved: +Math.hypot(car.x - cx, car.z - cz).toFixed(2), behindDmg: +(h0 - v.hp).toFixed(1) }; }
  // 각성 주사 = 흡수 빨간 ★6, 테이저 흡수
  R.setLv('awaken', 12); R.BR.awaken = 'absorb'; R.own('taser'); R.awaken(10); R.setAbs('taser');
  const v2 = R.bodies.find((b) => b.kind === 'citizen' && b.maxHp > 0 && !b.space && b.hp > 0 && !(b.stunT > 0)); v2.sleep = false; R.LH(me, v2, 1); o.absorbMe = { mb: R.MB(me), stun: +(v2.stunT || 0).toFixed(2), meForce: me.force };
  o.stat = [R.SL('mutate', 12), R.SL('awaken', 7)];
  return o; });
console.log(JSON.stringify(r, null, 1)); console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
