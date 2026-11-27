const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
const src = fs.readFileSync(__dirname + '/var/c568.html', 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "n";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + '/var/c568_sf.html', src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c568_sf.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
console.log(await p.evaluate(() => window.__rd.ev(`(() => { const out = []; let last = 0; chSf.on = true; chSf.T = 0; for (let i = 0; i < 4200 && out.length < 4; i++) { chSf.T += 0.1; while (!chSf.boss && chSf.T >= chSfAt(chSf.n + 1)) { chSf.n++; out.push(chSf.n + '번째 ' + chSf.T.toFixed(1) + '초'); if (chSf.n >= 4) chSf.boss = true; } } return out.join(' · '); })()`)));
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
