const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const v of ['c553', 'c554']) {
const src = fs.readFileSync(__dirname + `/var/${v}.html`, 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/${v}_hp.html`, src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/${v}_hp.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
console.log(v, await p.evaluate(() => window.__rd.ev(`(() => { chNoMix = true; const s = addCitizen(me.foot.x + 20, me.foot.z, square(me.foot.x + 20, me.foot.z), 'soldier'), r = addCitizen(me.foot.x + 22, me.foot.z, square(me.foot.x + 22, me.foot.z), 'robot'); chNoMix = false; return '군인 ' + s.maxHp.toFixed(1) + ' 사각 ' + r.maxHp.toFixed(1) + ' 배율 ' + (r.maxHp / s.maxHp).toFixed(2); })()`))); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
