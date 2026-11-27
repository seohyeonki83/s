const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const v of ['c566', 'c567']) {
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
const url = `file:///home/user/s/running-dead/chapter/${v}.html`;
await p.goto(url); await p.evaluate(() => localStorage.setItem('rd_save_v1', JSON.stringify({ genes: 500, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tut: true, mig: 1, v2: 1, v3: 1, v4: 1, u2: 1 })));
await p.goto(url); await p.waitForSelector('#outg .map', { timeout: 30000 }); await p.waitForTimeout(500);
const s0 = await p.evaluate(() => { const m = document.querySelector('#outg .map'); m.scrollLeft = m.scrollLeft + 400; return m.scrollLeft; });
await p.evaluate(() => [...document.querySelectorAll('#outg button')].find((x) => x.textContent.includes('성장')).click()); await p.waitForTimeout(300);
await p.click('[data-up="hp"]'); await p.waitForTimeout(400); await p.click('[data-up="hp"]'); await p.waitForTimeout(400);
const s1 = await p.evaluate(() => document.querySelector('#outg .map').scrollLeft);
console.log(v, '누르기 전', s0, '두 번 누른 뒤', s1, '유전자', await p.textContent('#outg .gp span')); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
