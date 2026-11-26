// c494: 불도저 → 특공대 3번 → 장갑차
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c494S.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(800);
await p.evaluate(() => { const R = window.__rd; R.me.hp = R.me.maxHp = 1e9; const S = R.SF(); S.on = true; S.T = R.AT(4) - 0.05; }); await p.waitForTimeout(400); await p.evaluate(() => window.__rd.REL()); await p.waitForTimeout(2500);
const o = { dozers: await p.evaluate(() => window.__rd.TK()) };
await p.evaluate(() => { const R = window.__rd; for (const t of R.TKS()) { t.obj.hp = 0; R.BO(t.obj); } R.TW().length = 0; }); await p.waitForTimeout(600);
o.c2 = await p.evaluate(() => { const S = window.__rd.SF(); return { c2: S.c2 && { n: S.c2.n, boss: S.c2.boss, dt: Math.round(S.T - S.c2.T0) }, hud: window.__rd.HUD() }; });
const step = async (t) => { await p.evaluate((t) => { const S = window.__rd.SF(); S.T = S.c2.T0 + t - 0.05; window.__rd.TW().length = 0; }, t); await p.waitForTimeout(400); const q = await p.evaluate(() => window.__rd.Q()); await p.evaluate(() => window.__rd.REL()); return q; };
o.w120 = await step(120); o.w265 = await step(265); o.w405 = await step(405); o.hudBoss = await p.evaluate(() => window.__rd.HUD()); o.w550 = await step(550);
await p.waitForTimeout(2500); o.tank = await p.evaluate(() => window.__rd.TK().filter((t) => !t.dozer));
o.after = await p.evaluate(() => { const S = window.__rd.SF(); return { repIn: Math.round(S.repNext - S.T), hud: window.__rd.HUD() }; });
await p.screenshot({ path: __dirname + '/perf/c494_tank.png' });
console.log(JSON.stringify(o)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
