// c433: 드론 — 체력 · 살아 있는 동안 주기 멈춤 · 다 죽은 뒤 144초
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
  await ctx.addInitScript(() => { let s = 99; Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; window.requestAnimationFrame = () => 0; window.__noRender = true; });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
  await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
  await p.goto('file://' + __dirname + '/var/c433.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 }); await p.waitForTimeout(500);
  const r = await p.evaluate(() => { const R = window.__rd, me = R.me, ev = []; document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); me.hp = me.maxHp = 1e9;
    R.setStars(3, me.foot.x, me.foot.z); const alive = () => window.__drones().filter((d) => !d.dead); let prev = 0, killAt = null;
    for (let i = 0; i < 30 * 420; i++) { R.step(1 / 30); me.hp = me.maxHp; const n = alive().length; const t = +(i / 30).toFixed(0);
      if (n > prev) ev.push(`t=${t}s +${n - prev} (hp ${alive()[0].hp})`); prev = n;
      if (n && killAt === null && ev.length === 1) killAt = t + 90;   // 첫 출동 뒤 90초 동안 살려 둔다
      if (n && killAt !== null && t >= killAt) { for (const d of alive()) d.dead = true; ev.push(`t=${t}s 모두 죽임`); killAt = Infinity; prev = 0; }
      if (ev.length > 5) break; }
    return ev; });
  console.log(JSON.stringify(r), errs.slice(0, 2)); await b.close(); })();
