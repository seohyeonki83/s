const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const v of ['c562', 'c563']) {
const src = fs.readFileSync(__dirname + `/var/${v}.html`, 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/${v}_hp.html`, src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/${v}_hp.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
console.log(v, await p.evaluate(() => window.__rd.ev(`(() => { chNoMix = true; const s = addCitizen(me.foot.x + 20, me.foot.z, square(me.foot.x + 20, me.foot.z), 'soldier'), r = addCitizen(me.foot.x + 22, me.foot.z, square(me.foot.x + 22, me.foot.z), 'robot'); chNoMix = false; const po = addCitizen(me.foot.x + 24, me.foot.z, square(me.foot.x + 24, me.foot.z), 'police'); me.hp = me.maxHp = 1e6; landHit(po, me, 10); const dP = 1e6 - me.hp; me.hp = 1e6; landHit(s, me, 10); const dS = 1e6 - me.hp; const d = chDroneAdd ? (chDroneAdd(me.foot.x + 30, me.foot.z), chDrones[chDrones.length - 1].maxHp) : 0; return '군인HP ' + s.maxHp.toFixed(1) + ' 사각HP ' + r.maxHp.toFixed(1) + ' 경찰HP ' + po.maxHp.toFixed(1) + ' 경찰타격 ' + dP.toFixed(2) + ' 군인타격 ' + dS.toFixed(2) + ' 드론HP ' + d.toFixed(1); })()`))); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
