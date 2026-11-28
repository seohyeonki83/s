const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
const url = 'file:///home/user/s/running-dead/chapter/c600.html';
await p.goto(url); await p.evaluate(() => localStorage.setItem('rd_save_v1', JSON.stringify({ genes: 1000, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tr: {}, tut: true, mig: 1, v2: 1, v3: 1, v4: 1, u2: 1, u3: 1 })));
await p.goto(url); await p.waitForSelector('#outg .ugb', { timeout: 30000 }); await p.waitForTimeout(300);
await p.click('[data-ug="1"]'); await p.waitForTimeout(300);
const log = [];
for (let i = 0; i < 25; i++) { const g0 = await p.evaluate(() => JSON.parse(localStorage.getItem('rd_save_v1')).genes); await p.click('[data-up="hp"]'); await p.waitForTimeout(40); const g1 = await p.evaluate(() => JSON.parse(localStorage.getItem('rd_save_v1')).genes); log.push(g0 - g1); }
console.log('클릭마다 든 유전자:', log.join(','));
await p.waitForTimeout(1100);
console.log('버튼:', await p.evaluate(() => [...document.querySelectorAll('#outg .ug')].map((r) => r.dataset.row + ' ' + r.querySelector('.pc').textContent + ' 다음 ' + r.querySelector('.ub').textContent.trim()).join(' | ')));
await p.screenshot({ path: __dirname + '/shots/c600_up.png', clip: { x: 0, y: 460, width: 390, height: 384 } });
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
