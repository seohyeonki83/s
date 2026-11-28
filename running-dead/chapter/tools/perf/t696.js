const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
const url = 'file:///home/user/s/running-dead/chapter/c601.html';
await p.goto(url); await p.evaluate(() => localStorage.setItem('rd_save_v1', JSON.stringify({ genes: 1000, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tr: {}, tut: true, mig: 1, v2: 1, v3: 1, v4: 1, u2: 1, u3: 1 })));
await p.goto(url); await p.waitForSelector('#outg .ugb', { timeout: 30000 }); await p.waitForTimeout(300);
await p.click('[data-ug="1"]'); await p.waitForTimeout(300);
const st = () => p.evaluate(() => [...document.querySelectorAll('#outg .ug')].map((r) => r.dataset.row + ' ' + r.querySelector('.pc').textContent + ' ' + r.querySelector('.ub').textContent.trim() + (r.querySelector('.ub').disabled ? '(잠김)' : '')).join(' | ') + ' · 유전자 ' + JSON.parse(localStorage.getItem('rd_save_v1')).genes);
for (let i = 0; i < 10; i++) { await p.click('[data-up="hp"]'); await p.waitForTimeout(40); }
await p.waitForTimeout(1100); console.log('체력 10번:', await st());
await p.screenshot({ path: __dirname + '/shots/c601_lock.png', clip: { x: 0, y: 460, width: 390, height: 384 } });
await p.evaluate(() => { const b = document.querySelector('#outg .ug[data-row="hp"] .ub'); b.disabled = false; b.click(); }); await p.waitForTimeout(200); console.log('잠긴 거 억지로 눌러도:', await st());
for (let i = 0; i < 10; i++) { await p.click('[data-up="ahp"]'); await p.waitForTimeout(40); } await p.waitForTimeout(1100);
for (let i = 0; i < 10; i++) { await p.click('[data-up="atk"]'); await p.waitForTimeout(40); }
await p.waitForTimeout(1050); await p.screenshot({ path: __dirname + '/shots/c601_unl.png', clip: { x: 0, y: 460, width: 390, height: 384 } });
await p.waitForTimeout(300); console.log('셋 다 채운 뒤:', await st());
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
