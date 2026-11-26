// c468: 테이저건 10단계 · 정전기
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c468eS.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(2000);
const o = { max: await p.evaluate(() => ['taser', 'bomb', 'cash', 'mutate', 'awaken'].map((k) => window.__rd.MAXL(k))) };
for (const [n, nm] of [[5, 'w5'], [6, 'r1'], [10, 'r5']]) {
  await p.evaluate(() => window.__rd.PACK()); await p.evaluate((n) => window.__rd.SET('taser', n, null), n); await p.waitForTimeout(500);
  const a = await p.evaluate(() => window.__rd.ST()); await p.evaluate(() => window.__rd.USE('taser')); await p.waitForTimeout(300);
  const b0 = await p.evaluate(() => window.__rd.ST()); await p.waitForTimeout(1500); const b1 = await p.evaluate(() => window.__rd.ST());
  const mv = (A, B, w) => { let s = 0, k = 0; A.pos.forEach((q, i) => { const r = B.pos[i]; if (!r) return; if ((w === 'stat' && q[3] && !q[2]) || (w === 'free' && !q[3] && !q[2])) { s += Math.hypot(r[0] - q[0], r[1] - q[1]); k++; } }); return k ? +(s / k).toFixed(2) : null; };
  o[nm] = { lv: n, col: await p.evaluate(() => window.__rd.COL()), btn: await p.evaluate(() => window.__rd.STARS()), stun: b0.stun, stat: b0.stat, moveStat: mv(b0, b1, 'stat'), moveFree: mv(b0, b1, 'free') };
  if (nm === 'r5') await p.screenshot({ path: __dirname + '/perf/c468_static.png' });
  await p.waitForTimeout(4500);
}
console.log(JSON.stringify(o)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
