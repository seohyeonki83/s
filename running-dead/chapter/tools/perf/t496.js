// c410: 바리케이트·바리케이트 줄의 경찰차도 부서지면 바로 안 막는다 (부서진 바로 다음 걸음에 그 한가운데 선 몸이 밀려나나)
const { chromium } = require('playwright');
const V = process.argv[2];
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
  await ctx.addInitScript(() => { let s = 7932; Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; let u = 777; globalThis.__uu = () => { u = (u * 1103515245 + 12345) >>> 0; return u / 4294967296; }; window.requestAnimationFrame = () => 0; window.__seed = 108; window.__secOff = true; window.__noReload = true; window.__noRender = true; });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 3).join(' | ')));
  const three = require('fs').readFileSync(__dirname + '/../node_modules/three/build/three.module.min.js', 'utf8').split('4294967295*Math.random()').join('4294967295*globalThis.__uu()');
  await p.route('**/three.module.min.js', (r) => r.fulfill({ body: three, contentType: 'application/javascript' }));
  await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 }); await p.waitForTimeout(500);
  const res = await p.evaluate(() => { const R = window.__rd, me = R.me, cars = R.cars(), out = {};
    document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })));
    me.hp = me.maxHp = 1e7;
    const st = {}; for (const c of cars) { const k = c.state + (c.deco ? ':deco' : '') + (c.wall ? ':wall' : '') + (c.barr ? ':barr' : '') + (c.tutS ? ':tut' : ''); st[k] = (st[k] || 0) + 1; } out.st = st;
    const probe = (c) => { const x0 = c.x, z0 = c.z; me.foot.x = c.x + 0.03; me.foot.z = c.z + 0.02; me.vel.set(0, 0); const bx = me.foot.x, bz = me.foot.z; R.step(1 / 60); return { meMoved: +Math.hypot(me.foot.x - bx, me.foot.z - bz).toFixed(3), carMoved: +Math.hypot(c.x - x0, c.z - z0).toFixed(3) }; };
    for (const [name, f] of [['barr', (c) => c.barr && !c.wreck], ['wallCar', (c) => c.wall && !c.barr && !c.wreck]]) { const c = cars.find(f); if (!c) continue;
      const live = probe(c); me.foot.x = c.x + 40; R.breakObj(c.obj); const w = probe(c); out[name] = { live, wreck: w, isWreck: !!c.wreck }; }
    return out; });
  console.log(V, JSON.stringify(res)); if (errs.length) console.log('ERR', errs.slice(0, 3)); await b.close(); })();
