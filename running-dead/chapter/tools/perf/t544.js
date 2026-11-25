// 실제 앱: 메뉴에서 적 테스트 → 30초 관찰 (적이 쏘거나 때리는지)
const { chromium } = require('playwright');
const f = process.argv[2];
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + f); await p.waitForTimeout(2500);
await p.screenshot({ path: __dirname + '/perf/menu_c466.png' });
const btns = await p.evaluate(() => [...document.querySelectorAll('button')].map((x) => { const r = x.getBoundingClientRect(); return [x.innerText.split('\n')[0], Math.round(r.top), Math.round(r.bottom)]; }));
console.log(JSON.stringify(btns));
await p.evaluate(() => [...document.querySelectorAll('button')].find((x) => x.innerText.startsWith('적 테스트')).click());
await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); 
for (let i = 0; i < 3; i++) { await p.waitForTimeout(8000); await p.screenshot({ path: __dirname + `/perf/et466_${i}.png` }); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
