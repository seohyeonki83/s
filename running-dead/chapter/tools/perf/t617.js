const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const [tag, stg, dif, T, n] of [['sf', 1, 'e', 118.5, 0], ['boss', 2, 'h', 548.5, 3]]) {
const src = fs.readFileSync(__dirname + '/var/c534.html', 'utf8').replace('window.__map = "b";', `window.__map = "m"; window.__stg = ${stg}; window.__dif = "${dif}";`).replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/c534_${tag}.html`, src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/c534_${tag}.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(2500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(2000);
await p.evaluate(([T, n]) => window.__rd.ev(`chSf.on = true; chSf.T = ${T}; chSf.n = ${n}; chSf.hide = false; me.hp = me.maxHp = 1e6;`), [T, n]);
const pz = [];
for (let k = 0; k < 10; k++) { await p.waitForTimeout(400); pz.push(await p.evaluate(() => window.__rd.ev('(paused ? "P" : "-") + (document.querySelector(".sqx") ? "S" : "")'))); await p.screenshot({ path: `shot534_${tag}_${k}.png` }); }
console.log(tag, pz.join(' '));
await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
