// c418: 체력이 다한 적이 반 속도로 움직이나 — 같은 상황에서 두 버전의 이동 거리 비교
const { chromium } = require('playwright');
const V = process.argv[2];
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
  await ctx.addInitScript(() => { let s = 4242; Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; let u = 777; globalThis.__uu = () => { u = (u * 1103515245 + 12345) >>> 0; return u / 4294967296; }; window.requestAnimationFrame = () => 0; window.__noRender = true; });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
  const three = require('fs').readFileSync(__dirname + '/../node_modules/three/build/three.module.min.js', 'utf8').split('4294967295*Math.random()').join('4294967295*globalThis.__uu()');
  await p.route('**/three.module.min.js', (r) => r.fulfill({ body: three, contentType: 'application/javascript' }));
  await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 }); await p.waitForTimeout(500);
  const r = await p.evaluate(() => { const R = window.__rd, me = R.me; document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); me.hp = me.maxHp = 1e7;
    const cs = R.bodies.filter((c) => c.kind === 'citizen' && c.maxHp > 0 && !c.space && !c.police).sort((a, q) => Math.hypot(a.foot.x - me.foot.x, a.foot.z - me.foot.z) - Math.hypot(q.foot.x - me.foot.x, q.foot.z - me.foot.z)).slice(0, 6);
    cs.forEach((c) => { c.sleep = false; c.met = true; window.__goo(c); }); const L = cs.map(() => 0), P = cs.map((c) => [c.foot.x, c.foot.z]);
    for (let i = 0; i < 180; i++) { R.step(1 / 60); cs.forEach((c, k) => { L[k] += Math.hypot(c.foot.x - P[k][0], c.foot.z - P[k][1]); P[k] = [c.foot.x, c.foot.z]; }); }
    return { n: cs.length, dist: L.map((x) => +x.toFixed(2)), st: cs.map((c) => c.state) }; });
  console.log(V, JSON.stringify(r), errs.slice(0, 2)); await b.close(); })();
