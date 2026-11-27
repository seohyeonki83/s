const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
const src = fs.readFileSync(__dirname + '/var/c564.html', 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "h";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + '/var/c564_cvy.html', src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c564_cvy.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
await p.evaluate(() => document.querySelectorAll('.okBtn, .ok').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))));
console.log(await p.evaluate(() => window.__rd.ev(`(() => { me.hp = me.maxHp = 1e9; chSf.on = true; chSf.T = chSfAt(4) - 0.1; chSf.n = 3; const d0 = chDrones.length;
  for (let i = 0; i < 400; i++) { paused = false; me.hp = me.maxHp; stepWorld(0.05); }
  const cv = chCvy.filter((c) => !c.wreck); const crew = cv.flatMap((c) => c.crew || c.riders || []);
  const W = teamWait.filter((w) => w.cvy); return '대기열 군인차 ' + W.length + ' 구성 ' + JSON.stringify(W.map((w) => [w.car.join(','), '드론' + w.nd])) + ' · 나간 군인차 ' + chCvy.length + ' · 드론 ' + chDrones.filter((d) => d.cvy).length + ' · 차 안 ' + JSON.stringify(cv.map((c) => Object.keys(c).filter((k) => /crew|ride|pass|seat/i.test(k)))); })()`)));
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
