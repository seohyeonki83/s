const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const v of ['c578', 'c579']) {
const src = fs.readFileSync(__dirname + `/var/${v}.html`, 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "h";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/${v}_sf2.html`, src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/${v}_sf2.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
console.log(v, await p.evaluate(() => window.__rd.ev(`(() => { const out = []; for (const i of [4]) { let S = 0, G = 0; for (let r = 0; r < 400; r++) { teamWait.length = 0; chQueueTeam(i); for (const w of teamWait) for (const t of (w.comp || w.car || [])) { if (t === 'sniper') S++; else if (t === 'soldier') G++; } } out.push((i < 4 ? (i + 1) + '번째' : '보스 뒤') + ' 저' + (S / 400).toFixed(1) + ' 군' + (G / 400).toFixed(1)); } teamWait.length = 0; return out.join(' · '); })()`))); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
