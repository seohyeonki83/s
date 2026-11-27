const { chromium } = require('playwright'); const fs = require('fs');
const src = fs.readFileSync(__dirname + '/var/c524.html', 'utf8').replace('<script>window.__map = "b";</script>\n', '').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + '/var/c524_boot.html', src);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c524_boot.html'); await p.evaluate(() => { localStorage.clear(); localStorage.setItem('rd_save_v1', JSON.stringify({ genes: 640, clr: { '1e': 1, '1n': 1 }, sub: { '1e0': 1 }, up: { hp: 2, ahp: 0, atk: 3 }, tut: true, mig: 1, v2: 1, v3: 1 })); }); await p.reload();
await p.waitForSelector('#outg'); await p.evaluate(() => { document.querySelector('#outg .map').scrollLeft = 0; }); await p.waitForTimeout(400); await p.screenshot({ path: 'shot524_map.png' });
console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
