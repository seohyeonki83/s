// 테이저건 ★6 인원 · 전기폭탄 발동 확인
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + (process.argv[2] || 'c463t') + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(6000);
const out = [];
for (const [n, br] of [[6, null], [6, null], [12, 'chain'], [7, 'bomb'], [12, 'bomb']]) {
  out.push(await p.evaluate(([n, br]) => { const R = window.__rd; R.SET('taser', n, br); R.CLR(); const pre = R.ST(); R.UI('taser'); const post = R.ST(); return { n, br, near: pre.near, stunned: post.n, ammo: R.IT()[0][1] }; }, [n, br]));
  await p.waitForTimeout(800);
}
console.log(JSON.stringify(out)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
