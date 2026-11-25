const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c432z.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1000);
console.log(JSON.stringify(await p.evaluate(() => { const R = window.__rd; const mk = () => { const c = R.bodies.find((b) => b.kind === 'citizen' && b.sleep && !b.space); c.sleep = false; R.zombify(c); return c; };
  const pol = R.bodies.find((b) => b.kind === 'citizen' && b.police);
  const a = mk(), z = mk(); a.hp = a.maxHp * 0.3; z.hp = z.maxHp * 0.3; const h0 = a.hp; R.BC(a, 3); const full = a.hp === a.maxHp;
  const ha = a.hp, hz0 = z.hp = z.maxHp; R.LH(pol, a, 10); R.LH(pol, z, 10);
  return { before: +h0.toFixed(1), afterCharge: +ha.toFixed(1), max: +a.maxHp.toFixed(1), full, dmgBombing: +(ha - a.hp).toFixed(2), dmgNormal: +(hz0 - z.hp).toFixed(2) }; })), errs); await b.close(); })();
