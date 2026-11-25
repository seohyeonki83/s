// c462: 군인차 1~2대 랜덤 · 나눠 타기
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c462z.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
const o = await p.evaluate(() => { const R = window.__rd, out = {}; for (const i of [0, 1, 2, 3]) { const H = {}; for (let n = 0; n < 200; n++) { R.TW().length = 0; R.QT(i); const k = R.TW().map((w) => (w.car ? 'C' : 'W') + ':' + (w.car || w.comp).map((x) => x === 'sniper' ? 'S' : 'G').join('')).join(' '); H[k] = (H[k] || 0) + 1; } out[i] = H; } R.TW().length = 0; return out; });
console.log(JSON.stringify(o, null, 1)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
