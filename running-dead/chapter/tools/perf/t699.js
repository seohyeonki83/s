const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
const src = fs.readFileSync(__dirname + '/var/c603.html', 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + '/var/c603_st.html', src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
const url = 'file://' + __dirname + '/var/c603_st.html'; const out = [];
for (const L of [1, 2, 3, 4, 5, 6, 20]) {
  await p.goto(url); await p.evaluate((L) => localStorage.setItem('rd_save_v1', JSON.stringify({ genes: 0, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tr: { start: L }, tut: true, mig: 1, v2: 1, v3: 1, v4: 1, u2: 1, u3: 1 })), L);
  await p.goto(url); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
  out.push(L + '단계: ' + await p.evaluate(() => window.__rd.ev(`(() => { const A = bodies.filter((b) => b.kind === 'ally'); return '일반 ' + A.filter((a) => !a.mini).length + ' 새끼 ' + A.filter((a) => a.mini).length + ' · 설명 ' + CH_TRD[0].fx(chTrait('start')); })()`)));
}
console.log(out.join('\n'));
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
