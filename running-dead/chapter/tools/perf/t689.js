const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
const url = 'file:///home/user/s/running-dead/chapter/c594.html';
await p.goto(url); await p.evaluate(() => localStorage.setItem('rd_save_v1', JSON.stringify({ genes: 500, clr: { '1e': 1, '1n': 1 }, sub: { '1e0': 1, '1e1': 1, '1n0': 1 }, up: { hp: 20, ahp: 0, atk: 0 }, tr: {}, tut: true, mig: 1, v2: 1, v3: 1, v4: 1, u2: 1, u3: 1 })));
await p.goto(url); await p.waitForSelector('#outg .ugb', { timeout: 30000 }); await p.waitForTimeout(300);
console.log('특성 버튼 숫자:', await p.evaluate(() => (document.querySelector('#outg .bd2') || {}).textContent));
await p.click('[data-trs="1"]'); await p.waitForTimeout(300);
for (const k of ['start', 'start', 'start', 'leech']) { await p.click(`[data-tr="${k}"]`); await p.waitForTimeout(150); }
console.log('산 뒤:', await p.evaluate(() => JSON.stringify(JSON.parse(localStorage.getItem('rd_save_v1')).tr) + ' 남은 ' + document.querySelector('#outg .tpn').textContent + ' · 시작동료 다음 비용 ' + document.querySelector('[data-tr="start"]').textContent));
await p.screenshot({ path: __dirname + '/shots/c594_tr.png', clip: { x: 0, y: 150, width: 390, height: 520 } });
await p.click('.sh .x'); await p.waitForTimeout(200);
await p.evaluate(() => document.querySelector('#outg .nd[data-st="1"]').click()); await p.waitForTimeout(400);
await p.screenshot({ path: __dirname + '/shots/c594_stage.png', clip: { x: 0, y: 380, width: 390, height: 464 } });
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
