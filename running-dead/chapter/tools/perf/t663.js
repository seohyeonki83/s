const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const dif of ['e', 'n', 'h']) {
const src = fs.readFileSync(__dirname + '/var/c572.html', 'utf8').replace('window.__map = "b";', `window.__map = "m"; window.__stg = 1; window.__dif = "${dif}";`).replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/c572_${dif}.html`, src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/c572_${dif}.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
console.log(dif, await p.evaluate(() => window.__rd.ev(`(() => { const out = []; for (let L = 1; L <= 6; L++) { chAL = L; let sg = 0, rb = 0; for (let i = 0; i < 10; i++) { const x = me.foot.x + 40 + i, z = me.foot.z + 40; const a = addCitizen(x, z, square(x, z), 'police'), s = addCitizen(x, z + 2, square(x, z + 2), 'soldier'); if (a.sg) sg++; if (s.robot) rb++; } out.push(LEVEL_NAME[L - 1] + ' 샷' + sg + '/10 사각' + rb + '/10'); } return 'mixL ' + CH_MIXL + ' | ' + out.join(' · '); })()`))); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
