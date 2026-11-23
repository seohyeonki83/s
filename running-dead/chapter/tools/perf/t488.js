// c406: 본 맵 '다시 하기' = 새 월드 (화면을 다시 불러 본 맵을 바로 고른다)
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file:///home/user/s/running-dead/chapter/c406.html'); await p.waitForTimeout(800);
const menu = await p.evaluate(() => [...document.querySelectorAll('button')].map((x) => x.textContent.trim().slice(0, 40)));
console.log('menu', JSON.stringify(menu));
await p.getByText('본 맵', { exact: true }).click(); 
await p.waitForFunction(() => document.getElementById('ver') && /본 맵 c406 #\d+/.test(document.getElementById('ver').textContent), null, { timeout: 60000 }); await p.waitForTimeout(2500);
const v1 = await p.evaluate(() => document.getElementById('ver').textContent);
await p.evaluate(() => { const r = document.getElementById('retry'); r.hidden = false; r.click(); });
await p.waitForTimeout(600);
await p.waitForFunction(() => document.getElementById('ver') && /본 맵 c406 #\d+/.test(document.getElementById('ver').textContent), null, { timeout: 60000 }); await p.waitForTimeout(2500);
const v2 = await p.evaluate(() => ({ ver: document.getElementById('ver').textContent, name: window.name, pickShown: [...document.querySelectorAll('div')].some((d) => d.textContent === '맵 선택') }));
console.log('first', v1, '| after retry', JSON.stringify(v2), 'errors', JSON.stringify(errs.slice(0, 3)));
// 다른 맵의 다시 하기는 전처럼 (다시 불러오지 않는다)
await b.close(); })();
