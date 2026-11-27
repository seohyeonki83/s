const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const v of ['c555', 'c556']) for (const k of [0, 1]) {
const src = fs.readFileSync(__dirname + `/var/${v}.html`, 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },').replace('chOrange10(); }', 'window.__o10 = chOrange10.length; chOrange10(); }');
fs.writeFileSync(__dirname + `/var/${v}_or.html`, src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/${v}_or.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
console.log(v, k, await p.evaluate(() => window.__rd.ev(`(() => { const all = [...bodies, ...(chDormB || []), ...(chDormC || [])].filter((b) => b.kind === 'citizen'); const set = new Set(all); const A = [...set];
  const o = A.filter((b) => b.attacker && !b.vig && !b.police && !b.boss && !b.robot).length, d = A.filter((b) => b.demoted && !b.guard && !b.attacker && !b.police).length, w = A.filter((b) => !b.attacker && !b.guard && !b.police && !b.robot && !b.boss).length, inB = A.filter((b) => b.demoted && b.space).length;
  return '주황 ' + o + ' · 하양 ' + w + ' · 주황→하양 ' + d + ' (건물 안 ' + inB + ')'; })()`))); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
