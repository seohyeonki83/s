// c405: 평소 실행 (손으로 조이스틱) — 오류 없이 도는지 + 성능 글자
const { chromium } = require('playwright');
const V = process.argv[2] || 'c405', TAG = process.argv[3] || 'b';
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: false })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 3).join(' | ')));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1200);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(400);
await p.evaluate(() => document.getElementById('ver').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })));   // 성능 글자 켜기
const dirs = [[0, -120], [120, 0], [0, 120], [-120, 0], [90, -90], [-90, 90]];
for (let k = 0; k < 6; k++) { await p.mouse.move(195, 600); await p.mouse.down(); await p.mouse.move(195 + dirs[k][0], 600 + dirs[k][1], { steps: 4 }); await p.waitForTimeout(3500); await p.mouse.up(); await p.waitForTimeout(200);
  await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); }
const info = await p.evaluate(() => { const s = window.__rd.sec(); return { ver: document.getElementById('ver').textContent, live: s.secs.filter((q) => q.live).length, bodies: window.__rd.bodies.length, dorm: s.dormB.length, me: [Math.round(window.__rd.me.foot.x), Math.round(window.__rd.me.foot.z)] }; });
console.log(JSON.stringify(info));
await p.screenshot({ path: '/home/user/s/running-dead/chapter/shots/c405_' + TAG + '_run.png' });
console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
