// c436: 경보 10단계 표시 · 샷건 경찰 · 로봇 · 덩치 넉백 · 불도저
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c436z.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(500);
const out = {};
// 경보: 감염 수를 1021(계엄)으로 → 연출이 차례로
await p.evaluate(() => { const R = window.__rd; R.me.hp = R.me.maxHp = 1e9; R.kills(1021); R.incident(R.me.foot.x, R.me.foot.z); });
await p.waitForTimeout(16000);
out.alert = await p.evaluate(() => ({ al: window.__rd.AL(), text: document.getElementById('stars').innerText.replace(/\s+/g, ' ') }));
await p.screenshot({ path: __dirname + '/perf/c436_alert.png', clip: { x: 0, y: 0, width: 390, height: 140 } });
out.units = await p.evaluate(() => { const R = window.__rd, me = R.me, o = {};
  const pol = []; for (let i = 0; i < 5; i++) pol.push(R.AC(me.foot.x + 3 + i * 0.5, me.foot.z + 3, { x0: me.foot.x - 9, z0: me.foot.z - 9, x1: me.foot.x + 9, z1: me.foot.z + 9 }, 'police'));
  const sol = []; for (let i = 0; i < 5; i++) sol.push(R.AC(me.foot.x - 3 - i * 0.5, me.foot.z + 3, { x0: me.foot.x - 9, z0: me.foot.z - 9, x1: me.foot.x + 9, z1: me.foot.z + 9 }, 'soldier'));
  o.sg = pol.map((c) => !!c.sg); o.robot = sol.map((c) => !!c.robot); const sg = pol.find((c) => c.sg), rb = sol.find((c) => c.robot);
  o.sgHp = [Math.round(pol[0].maxHp), Math.round(sg.maxHp)]; o.rbHp = [Math.round(sol[0].maxHp), Math.round(rb.maxHp), rb.r.toFixed(2)];
  // 샷건: 앞쪽 부채꼴 안 좀비 3 · 밖 1
  const mk = () => { const c = R.bodies.find((x) => x.kind === 'citizen' && x.sleep && !x.space && Math.hypot(x.foot.x - me.foot.x, x.foot.z - me.foot.z) > 30); c.sleep = false; R.zombify(c); return c; };
  sg.foot.x = me.foot.x + 10; sg.foot.z = me.foot.z + 10; sg.space = null;
  const zs = [[1.2, 0], [2.4, 0.3], [3.3, -0.4], [0, 2]].map(([dx, dz]) => { const z = mk(); z.foot.x = sg.foot.x + dx; z.foot.z = sg.foot.z + dz; z.space = null; return z; });
  const P = zs.map((z) => [z.foot.x, z.foot.z]); window.__noRender = true; R.step(1 / 60); zs.forEach((z, i) => { z.foot.x = P[i][0]; z.foot.z = P[i][1]; z.knockT = 0; }); const h0 = zs.map((z) => z.hp); R.SG(sg, zs[0]); window.__noRender = false; o.sgHit = zs.map((z, i) => +(h0[i] - z.hp).toFixed(2)); o.sgKnock = zs.map((z) => +(z.knockT || 0).toFixed(3)); o.sgDbg = zs.map((z) => [+(z.foot.x - sg.foot.x).toFixed(2), +(z.foot.z - sg.foot.z).toFixed(2), z.space === sg.space, z.kind, +z.hp.toFixed(1), z.mode]); o.sgR = +(sg.sight * 0.5).toFixed(2);
  // 덩치 넉백 막는 힘 (방탄복 개수 → 값, 저격수 넉백 12 기준)
  const a = mk(); window.__mut(a); let t = 0; while (a.mut !== 'armor' && t++ < 20) window.__mut(a); const u = 0.9245 / 12; o.kbArmor = +(R.KB(a) / u).toFixed(2); R.setLv('mutate', 12); R.BR.mutate = 'monster'; o.kbMonster6 = +(R.KB(a) / u).toFixed(2); o.kbMe = +(R.KB(me) / u).toFixed(2);
  // 로봇 체력 0 → 터짐 + 경험치
  const xp0 = R.lvInfo().xp; rb.hp = 0; R.step(1 / 60); o.robotGone = !R.bodies.includes(rb); o.xp = R.lvInfo().xp - xp0;
  return o; });
// 불도저 — 살아 있을 때 화면
await p.evaluate(() => { const R = window.__rd; R.BS(); const T = R.TK(); T.stunT = 0.05; R.me.foot.x = T.x - 3.5; R.me.foot.z = T.z + 1; });
await p.waitForTimeout(1200); await p.screenshot({ path: __dirname + '/perf/c436_dozer.png' });
out.boss = await p.evaluate(() => { const R = window.__rd, T = R.TK(); const o = { dozer: !!T.dozer, hp: Math.round(T.obj.maxHp) }; const p0 = R.PK().length; T.obj.hp = 0; R.BO(T.obj); o.drop = R.PK().length - p0; o.item = R.PK().slice(-1)[0]; return o; });
console.log(JSON.stringify(out, null, 1)); console.log('errors', JSON.stringify(errs.slice(0, 5))); await b.close(); })();
