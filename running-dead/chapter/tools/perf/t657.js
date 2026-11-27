const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
const src = fs.readFileSync(__dirname + '/var/c566.html', 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + '/var/c566_xp.html', src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c566_xp.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
console.log(await p.evaluate(() => window.__rd.ev(`(() => { const need = [0, 1, 2, 4, 9, 14, 19, 29].map((L) => 'Lv' + (L + 1) + ':' + needXp(L)).join(' '); let k = 0; while (pendingLv === 0 && k < 50) { gainXp(); k++; } return need + ' | 첫 레벨업까지 ' + k + '명'; })()`)));
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
