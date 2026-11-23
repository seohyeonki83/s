// c410: 잔해(부서진 차)는 부딪힘이 없다 — 몸 · 차 · 길거리 사물 · 덮치기 가림 · 길 찾기 원. 두 버전을 같은 상황에 놓고 비교한다
// node t495.js <var 이름 (…x)> [씨앗]
const { chromium } = require('playwright');
const V = process.argv[2], SEED = +(process.argv[3] || 1);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
  await ctx.addInitScript((sd0) => { const sd = Math.abs(sd0); let s = sd * 7919 + 13; Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; let u = 777; globalThis.__uu = () => { u = (u * 1103515245 + 12345) >>> 0; return u / 4294967296; }; window.requestAnimationFrame = () => 0; window.__seed = sd * 101 + 7; window.__secOff = true; window.__noReload = true; window.__noRender = true; window.__dbg = sd0 < 0; }, process.argv[4] === 'dbg' ? -SEED : SEED);
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 3).join(' | ')));
  const three = require('fs').readFileSync(__dirname + '/../node_modules/three/build/three.module.min.js', 'utf8').split('4294967295*Math.random()').join('4294967295*globalThis.__uu()');
  await p.route('**/three.module.min.js', (r) => r.fulfill({ body: three, contentType: 'application/javascript' }));
  await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 }); await p.waitForTimeout(500);
  const res = await p.evaluate(() => {
    const R = window.__rd, me = R.me, K = R.K, cars = R.cars(), out = {};
    document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })));
    me.hp = me.maxHp = 1e7;
    const inB = (x, z, m) => R.buildings.some((B) => !B.parent && x > B.x0 - m && x < B.x1 + m && z > B.z0 - m && z < B.z1 + m);
    const lineOk = (c, L) => { const fx = Math.cos(c.h), fz = Math.sin(c.h); for (let t = -L; t <= L; t += 0.25) { const x = c.x + fx * t, z = c.z + fz * t; if (inB(x, z, 1.2) || R.spaceOf(x, z)) return false; } return true; };
    const alone = (c, L, w) => { const fx = Math.cos(c.h), fz = Math.sin(c.h); const near = (x, z) => { const dx = x - c.x, dz = z - c.z, u = dx * fx + dz * fz, v = -dx * fz + dz * fx; return Math.abs(u) < L && Math.abs(v) < w; }; return !cars.some((q) => q !== c && near(q.x, q.z)) && !R.outProps().some((q) => !q.dead && near(q.foot.x, q.foot.z)) && !R.bodies.some((q) => q !== me && q.kind === 'citizen' && !q.space && near(q.foot.x, q.foot.z)); };   // 지나갈 길(앞뒤 5칸 · 옆 1.6칸)에 다른 차·사물·사람이 없다
    const pool = cars.filter((c) => c.state === 'parked' && !c.wreck && !c.wall && !c.barr && !c.tank && c.obj && !c.obj.dead && lineOk(c, 4.5) && alone(c, 5, 1.6)).sort((a, q) => Math.hypot(a.x - me.foot.x, a.z - me.foot.z) - Math.hypot(q.x - me.foot.x, q.z - me.foot.z));
    out.pool = pool.length; if (pool.length < 3) return out;
    const walk = (c, steps) => {   // 차의 긴 쪽을 따라 한가운데를 뚫고 간다 (걸음마다 0.05칸 = 초당 3칸)
      const fx = Math.cos(c.h), fz = Math.sin(c.h), x0 = c.x, z0 = c.z; me.foot.x = c.x - fx * 2.5; me.foot.z = c.z - fz * 2.5; me.vel.set(0, 0); let dev = 0;
      for (let i = 0; i < steps; i++) { me.foot.x += fx * 0.05; me.foot.z += fz * 0.05; R.step(1 / 60); const dx = me.foot.x - x0, dz = me.foot.z - z0; dev = Math.max(dev, Math.abs(-dx * fz + dz * fx)); }
      const dx = me.foot.x - x0, dz = me.foot.z - z0;
      return { along: +(dx * fx + dz * fz).toFixed(2), side: +dev.toFixed(2), carMoved: +Math.hypot(c.x - x0, c.z - z0).toFixed(2) };
    };
    // (가) 멀쩡한 차: 막힌다 (두 버전 같아야 한다)
    const A = pool[0]; out.live = walk(A, 100);
    // (나) 잔해: 뚫고 지나가나
    const W = pool[1], nObs0 = R.carObs().length, nBox0 = R.carBoxes().length; me.foot.x = W.x + 30; R.breakObj(W.obj); for (let i = 0; i < 90; i++) R.step(1 / 60);   // 폭발이 가라앉은 뒤에 본다
    out.wreck = !!W.wreck; out.obsDrop = nObs0 - R.carObs().length; out.boxDrop = nBox0 - R.carBoxes().length;
    const fx = Math.cos(W.h), fz = Math.sin(W.h);
    out.pounce = R.pb(W.x - fx * 3, W.z - fz * 3, W.x + fx * 3, W.z + fz * 3);   // 잔해를 가로지르는 덮치기 선이 막히나
    out.pounceLive = R.pb(A.x - Math.cos(A.h) * 3, A.z - Math.sin(A.h) * 3, A.x + Math.cos(A.h) * 3, A.z + Math.sin(A.h) * 3);   // 멀쩡한 차는 막아야 한다
    out.body = walk(W, 100);
    // (다) 길거리 사물: 잔해 한가운데 놓고 내가 살짝 밀었을 때 잔해 밖으로 튕겨 나가나
    const pr = R.outProps().filter((q) => !q.dead && !q.fixed).sort((a, q) => Math.hypot(a.foot.x - W.x, a.foot.z - W.z) - Math.hypot(q.foot.x - W.x, q.foot.z - W.z))[0];
    if (pr) { const wx = W.x, wz = W.z; pr.sleep = false; pr.foot.x = W.x + fx * 0.02; pr.foot.z = W.z + fz * 0.02; me.foot.x = pr.foot.x - fx * (pr.r + me.r - 0.15); me.foot.z = pr.foot.z - fz * (pr.r + me.r - 0.15); let inside = 0, moved = 0;
      for (let i = 0; i < 12; i++) { me.foot.x += fx * 0.01; me.foot.z += fz * 0.01; const qx = pr.foot.x, qz = pr.foot.z; R.step(1 / 60); const dx = pr.foot.x - W.x, dz = pr.foot.z - W.z, u = Math.abs(dx * fx + dz * fz), v = Math.abs(-dx * fz + dz * fx);
        const hu = K.CAR_L * K.ckl(W) / 2 * 0.16 + pr.r, hv = K.CAR_W * K.ck(W) / 2 * 0.16 + pr.r; if (pr.foot.x === qx && pr.foot.z === qz) continue; moved++; if (u < hu - 1e-6 && v < hv - 1e-6) inside++; }   // 이번 걸음에 밀린 사물만 센다 (안 밀린 사물은 원래도 안 본다)
      out.prop = { r: pr.r, movedInside: inside + '/' + moved, carMoved: +Math.hypot(W.x - wx, W.z - wz).toFixed(3) }; }
    // (라) 차와 차: 돌아다니는 민간 차를 잔해 위에 올려놓으면 서로 밀어내나
    const T = R.tr().cars.find((c) => !c.wreck && c.tr && c.tr.mode !== 'left' && c.tr.mode !== 'gone');
    if (T) { const W2 = pool[2]; me.foot.x = W2.x + 30; R.breakObj(W2.obj); for (let i = 0; i < 30; i++) R.step(1 / 60); const wx = W2.x, wz = W2.z; T.x = W2.x + 0.05; T.z = W2.z + 0.05; T.vx = T.vz = 0; const tx = T.x, tz = T.z; R.step(1 / 60);
      out.carcar = { wreckMoved: +Math.hypot(W2.x - wx, W2.z - wz).toFixed(3), carMoved: +Math.hypot(T.x - tx, T.z - tz).toFixed(3) }; }
    // (마) 잔해는 10초 뒤 사라지나 (그림만 남았다가 없어진다)
    const n0 = cars.includes(W); for (let i = 0; i < 600; i++) R.step(1 / 60); out.gone = [n0, cars.includes(W)];
    return out;
  });
  console.log(V, 'seed', SEED, JSON.stringify(res)); if (errs.length) console.log('ERR', errs.slice(0, 3)); await b.close(); })();
