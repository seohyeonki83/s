// c440: 변이 주사 갈림길 카드 색 · 이미 변이한 동료 · 각성한 나도 바뀌나
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c440z.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
const tap = (txt) => p.evaluate((txt) => { const bs = [...document.querySelectorAll('.okBtn')].filter((x) => !txt || x.textContent.trim() === txt); bs.forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); return bs.length; }, txt);
await tap(); await p.waitForTimeout(500);
await p.evaluate(() => window.__rd.give('mutate')); await p.waitForTimeout(2500); await tap('획득'); await p.waitForTimeout(900);
// 갈림길 전에 이미 변이한 동료 (덩치)
const pre = await p.evaluate(() => { const R = window.__rd, me = R.me; const c = R.bodies.find((b) => b.kind === 'citizen' && b.sleep && !b.space && Math.hypot(b.foot.x - me.foot.x, b.foot.z - me.foot.z) > 25); c.sleep = false; R.zombify(c); let t = 0; do { window.__mut(c); } while (c.mut !== 'armor' && t++ < 20); c.mutT = 999; window.__pre = c; c.foot.x = me.foot.x + 2.5; c.foot.z = me.foot.z; return { force: c.force, halo: !!c.brHalo }; });
await p.evaluate(() => window.__rd.setLv('mutate', 6)); await p.evaluate(() => window.__rd.give('mutate')); await p.waitForTimeout(2500); await tap('강화'); await p.waitForTimeout(2000);
await p.screenshot({ path: __dirname + '/perf/c440_mutpick.png' });
await p.evaluate(() => { const c = document.querySelector('#pick .card[data-k="monster"]'); c.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); }); await p.waitForTimeout(1500);
await p.evaluate(() => window.__rd.setLv('mutate', 12)); await p.waitForTimeout(600);
const post = await p.evaluate(() => { const c = window.__pre; return { force: c.force, halo: !!c.brHalo, haloCol: c.brHalo && c.brHalo.material.color.getHex().toString(16), btnCol: document.querySelector('.item') && getComputedStyle(document.querySelector('.item')).getPropertyValue('--c') }; });
await p.screenshot({ path: __dirname + '/perf/c440_after.png' });
console.log(JSON.stringify({ pre, post })); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
