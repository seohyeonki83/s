const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
const url = 'file:///home/user/s/running-dead/chapter/c577.html';
await p.goto(url); await p.evaluate(() => localStorage.setItem('rd_save_v1', JSON.stringify({ genes: 0, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tut: false, mig: 1, v2: 1, v3: 1, v4: 1, u2: 1 })));
await p.goto(url); await p.waitForSelector('#ldx .go', { timeout: 90000 }); await p.dispatchEvent('#ldx .go', 'pointerdown');
await p.waitForTimeout(1500); await p.evaluate(() => { const o = document.querySelector('.ok'); if (o) o.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); });
const names = [];
for (let i = 0; i < 12; i++) { await p.waitForTimeout(600); const t = await p.evaluate(() => { const o = document.getElementById('tut'); return o ? (o.querySelector('.nm') || {}).textContent : null; }); if (t) { names.push(t); await p.evaluate(() => document.querySelector('#tut .close').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); } }
console.log('튜토리얼 시작 직후 소개:', names.join(', ') || '없음', '| 저장', await p.evaluate(() => JSON.stringify(JSON.parse(localStorage.getItem('rd_save_v1')).seen)));
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
