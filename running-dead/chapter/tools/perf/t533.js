// c457: 특공대 3차례 + 보스
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c461z.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(400);
await p.evaluate(() => { window.__rd.me.hp = window.__rd.me.maxHp = 1e9; });
const out = [];
for (let n = 1; n <= 4; n++) {
  await p.evaluate((n) => { const R = window.__rd, S = R.SF(); S.on = true; R.TW().length = 0; S.T = R.AT(n) - 0.05; }, n);
  await p.waitForTimeout(500);
  out.push(await p.evaluate(() => { const R = window.__rd, S = R.SF(); const L = (c) => c.map((x) => x.sniper ? 'S' : 'G').join(''); return { n: S.n, boss: S.boss, hud: R.HUD(), q: R.TW().map((w) => w.boss ? 'BOSS' : (w.car ? 'C' : 'W') + ':' + (w.car || w.comp).map((x) => x === 'sniper' ? 'S' : 'G').join('')) }; }));
}
console.log(JSON.stringify(out, null, 0)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
