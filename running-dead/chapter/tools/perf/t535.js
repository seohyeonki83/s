// c463: 적 테스트 맵
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c463ez.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(1500);
const cnt = (a) => a.reduce((m, k) => (m[k] = (m[k] || 0) + 1, m), {});
const o = {}; o.start = await p.evaluate(() => ({ lv: window.__rd.LV('taser'), it: window.__rd.IT(), ens: window.__rd.ENS() })); o.start.ens = cnt(o.start.ens);
await p.screenshot({ path: __dirname + '/perf/c463_start.png' });
await p.waitForTimeout(12000);
o.after12 = await p.evaluate(() => ({ x: Math.round(window.__rd.me.foot.x), z: Math.round(window.__rd.me.foot.z), hp: window.__rd.me.hp, max: window.__rd.me.maxHp, n: window.__rd.ENS().length }));
await p.screenshot({ path: __dirname + '/perf/c463_fight.png' });
// 테이저건 버튼 → 전기폭탄 빨★6
await p.evaluate(() => document.querySelector('#etbar .b[data-k="taser"]').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); await p.waitForTimeout(300);
await p.screenshot({ path: __dirname + '/perf/c463_pick.png' });
await p.evaluate(() => { const L = [...document.querySelectorAll('#etpick .n')]; L.filter((x) => x.dataset.n === '12')[1].dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); }); await p.waitForTimeout(300);
await p.evaluate(() => document.querySelector('#etbar .b[data-k="bomb"]').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); await p.waitForTimeout(300);
await p.evaluate(() => { const L = [...document.querySelectorAll('#etpick .n')]; L.filter((x) => x.dataset.n === '3')[0].dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); }); await p.waitForTimeout(500);
o.set = await p.evaluate(() => ({ taser: window.__rd.LV('taser'), bomb: window.__rd.LV('bomb'), br: window.__rd.BR(), it: window.__rd.IT(), bar: document.getElementById('etbar').innerText.replace(/\n/g, ' ') }));
await p.evaluate(() => document.querySelector('#etbar .b[data-k="__re"]').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); await p.waitForTimeout(500);
o.re = (await p.evaluate(() => window.__rd.ENS())).length;
await p.screenshot({ path: __dirname + '/perf/c463_bar.png' });
console.log(JSON.stringify(o)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
