// c419: 드론 출동 — 별 단계마다 언제 몇 대 나오나 (드론 수만 센다)
const { chromium } = require('playwright');
const V = process.argv[2];
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
  await ctx.addInitScript(() => { let s = 99; Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; let u = 777; globalThis.__uu = () => { u = (u * 1103515245 + 12345) >>> 0; return u / 4294967296; }; window.requestAnimationFrame = () => 0; window.__noRender = true; });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
  const three = require('fs').readFileSync(__dirname + '/../node_modules/three/build/three.module.min.js', 'utf8').split('4294967295*Math.random()').join('4294967295*globalThis.__uu()');
  await p.route('**/three.module.min.js', (r) => r.fulfill({ body: three, contentType: 'application/javascript' }));
  await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 }); await p.waitForTimeout(500);
  const r = await p.evaluate(() => { const R = window.__rd, me = R.me, ev = []; document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); me.hp = me.maxHp = 1e9;
    for (const st of [3, 5]) { R.setStars(st, me.foot.x, me.foot.z); for (const d of window.__drones()) d.dead = true; let prev = window.__drones().filter((d) => !d.dead).length;
      for (let i = 0; i < 60 * 200; i++) { R.step(1 / 30); me.hp = me.maxHp; const n = window.__drones().filter((d) => !d.dead).length; if (n > prev) ev.push('별' + st + ' t=' + (i / 30).toFixed(0) + 's +' + (n - prev)); prev = n; if (ev.length > 8) break; }
      for (const d of window.__drones()) d.dead = true; }
    return ev; });
  console.log(V, JSON.stringify(r), errs.slice(0, 2)); await b.close(); })();
