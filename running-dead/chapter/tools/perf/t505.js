// 장비 배지 14개를 다 가졌을 때 화면 (왼쪽 아래 배지 묶음)
const { chromium } = require('playwright');
const V = process.argv[2];
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(600);
const box = await p.evaluate(() => { const ks = ['book', 'bag', 'rage', 'crowbar', 'vest', 'shoes', 'catalyst', 'blood', 'revive', 'teeth', 'acid', 'acidp', 'parasite', 'linger']; ks.forEach((k, i) => window.__rd.gain(k, i % 6)); const r = [...document.querySelectorAll('.pbadge')].map((e) => e.getBoundingClientRect()); return { n: r.length, top: Math.min(...r.map((q) => q.top)), right: Math.max(...r.map((q) => q.right)), bottom: Math.max(...r.map((q) => q.bottom)) }; });
await p.waitForTimeout(800); await p.screenshot({ path: __dirname + '/perf/badges_' + V + '.png' });
console.log(V, JSON.stringify(box), errs.slice(0, 2)); await b.close(); })();
