// c420: 현금 — 유혹된 하양이 맞아도 안 풀리나 · 돈다발에 닿아도 안 사라지나 · 돈다발 수명
const { chromium } = require('playwright');
const V = process.argv[2];
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
  await ctx.addInitScript(() => { let s = 4242; Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; let u = 777; globalThis.__uu = () => { u = (u * 1103515245 + 12345) >>> 0; return u / 4294967296; }; window.requestAnimationFrame = () => 0; window.__noRender = true; });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
  const three = require('fs').readFileSync(__dirname + '/../node_modules/three/build/three.module.min.js', 'utf8').split('4294967295*Math.random()').join('4294967295*globalThis.__uu()');
  await p.route('**/three.module.min.js', (r) => r.fulfill({ body: three, contentType: 'application/javascript' }));
  await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 }); await p.waitForTimeout(500);
  const r = await p.evaluate(() => { const R = window.__rd, me = R.me; document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })));
    const c = R.bodies.filter((b) => b.kind === 'citizen' && !b.space && !b.guard && !b.attacker && !b.police && !b.vig && b.sleep).sort((a, q) => Math.hypot(a.foot.x - me.foot.x, a.foot.z - me.foot.z) - Math.hypot(q.foot.x - me.foot.x, q.foot.z - me.foot.z))[0];
    c.sleep = false; c.met = true; me.foot.x = c.foot.x + 20; me.foot.z = c.foot.z;
    const k = { x: c.foot.x + 2, z: c.foot.z, space: null, mesh: {}, t: 6, who: new Set([c]) }; R.cashes().push(k); R.EL(c);
    const log = []; let hits = 0;
    for (let i = 1; i <= 60 * 8; i++) { R.step(1 / 60);
      if (i % 20 === 0 && c.state === 'lured') { R.ST(me, c); hits++; c.hp = Math.max(c.hp, 1); }   // 0.33초마다 한 대
      if (i % 60 === 0) log.push(`${i / 60}s ${c.state} cash:${R.cashes().includes(k) ? 'O' : 'X'} d=${Math.hypot(c.foot.x - k.x, c.foot.z - k.z).toFixed(1)} hits=${hits}`); }
    return log; });
  console.log(V, r.join(' | ')); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
