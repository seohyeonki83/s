// c435: 자폭 목표 고르기 — 하양 · 저격수 · 드론
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } }); await ctx.addInitScript(() => { window.requestAnimationFrame = () => 0; window.__noRender = true; });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
  await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
  await p.goto('file://' + __dirname + '/var/c435z.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(500);
  const r = await p.evaluate(() => { const R = window.__rd, me = R.me, o = {}; me.hp = me.maxHp = 1e9;
    // 내 둘레 비우기: 근처 사람을 멀리
    for (const c of R.bodies) if (c !== me && c.kind === 'citizen' && Math.hypot(c.foot.x - me.foot.x, c.foot.z - me.foot.z) < 15) { c.foot.x += 60; c.px = c.foot.x; }
    const put = (c, dx, dz) => { c.sleep = false; c.met = true; c.disc = true; c.space = null; c.foot.x = me.foot.x + dx; c.foot.z = me.foot.z + dz; c.px = c.foot.x; c.pz = c.foot.z; };
    const fresh = () => R.bodies.find((b) => b.kind === 'citizen' && b.sleep && !b.space && Math.hypot(b.foot.x - me.foot.x, b.foot.z - me.foot.z) > 30);
    const A = fresh(); R.zombify(A); put(A, -4, 0); const B = fresh(); R.zombify(B); put(B, 4, 0);
    const w = R.bodies.find((c) => c.kind === 'citizen' && !c.maxHp && !c.space && c.sleep); put(w, -5, 0.5);
    const sn = R.bodies.find((c) => c.kind === 'citizen' && (c.sniper || c.soldier || c.police) && !c.space); put(sn, 5, 0.5); o.snKind = sn.sniper ? 'sniper' : sn.soldier ? 'soldier' : 'police';
    const fix = () => { for (const [c, x, z] of pos) { c.foot.x = x; c.foot.z = z; c.vel.set(0, 0); } };
    const pos = [[A, A.foot.x, A.foot.z], [B, B.foot.x, B.foot.z], [w, w.foot.x, w.foot.z], [sn, sn.foot.x, sn.foot.z]];
    R.step(1 / 60); fix(); R.step(1 / 60); fix();
    R.UB(); o.case1 = { A: !!A.bombing, B: !!B.bombing, Btg: B.bombing && B.bombing.tg === sn };
    A.bombing = null; B.bombing = null; for (const z of [A, B]) if (z.bombS) { z.bombS.visible = false; z.bombS = null; }
    window.__droneAdd(me.foot.x - 4.5, me.foot.z + 1.5); const d = window.__drones()[window.__drones().length - 1];
    R.step(1 / 60); fix(); d.x = me.foot.x - 4.5; d.z = me.foot.z + 1.5;
    R.UB(); o.case2 = { A: !!A.bombing, B: !!B.bombing, Adrone: !!(A.bombing && A.bombing.drone === d) };
    return o; });
  console.log(JSON.stringify(r)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
