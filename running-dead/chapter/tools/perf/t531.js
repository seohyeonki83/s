// c459: 보스 뒤 100초마다 저2군6, 15초 군2는 불도저 살아 있을 때만
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c459z.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(400);
await p.evaluate(() => { window.__rd.me.hp = window.__rd.me.maxHp = 1e9; });
const Q = () => p.evaluate(() => { const R = window.__rd, S = R.SF(); return { wn: S.wn || 0, alive: R.TKS().filter((t) => !t.wreck).length, n: S.n, T: Math.round(S.T), hud: R.HUD(), q: R.TW().map((w) => w.boss ? 'BOSS' : (w.car ? 'C' : 'W') + ':' + (w.car || w.comp).map((x) => x === undefined ? '?' : '').length + (w.tk ? 'tk' : '')) }; });
const out = [];
await p.evaluate(() => { const R = window.__rd, S = R.SF(); S.on = true; R.TW().length = 0; S.T = R.AT(4) - 0.05; }); await p.waitForTimeout(300); await p.evaluate(() => { const R = window.__rd, W = R.TW(); for (let i = W.length - 1; i >= 0; i--) if (!W[i].boss) W.splice(i, 1); else { W[i].hold = false; W[i].t = 0; } }); await p.waitForTimeout(3000); out.push(await Q());
await p.evaluate(() => { const R = window.__rd, S = R.SF(); R.TW().length = 0; S.waveT = 14.9; }); await p.waitForTimeout(500); out.push(await Q());
await p.evaluate(() => { const R = window.__rd, S = R.SF(); R.TW().length = 0; S.T = R.AT(5) - 0.05; S.waveT = 0; }); await p.waitForTimeout(500); out.push(await Q());
await p.evaluate(() => { const R = window.__rd, S = R.SF(); R.TW().length = 0; for (const t of R.TKS()) { t.obj.hp = 0; R.BO(t.obj); } S.waveT = 14.9; }); await p.waitForTimeout(1000); out.push(await Q());
await p.evaluate(() => { const R = window.__rd, S = R.SF(); R.TW().length = 0; S.T = R.AT(6) - 0.05; }); await p.waitForTimeout(500); out.push(await Q());
out.push(await p.evaluate(() => [4, 5, 6, 7].map((n) => window.__rd.AT(n))));
console.log(JSON.stringify(out)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
