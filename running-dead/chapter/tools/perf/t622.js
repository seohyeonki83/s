const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const V of ['c537', 'c538']) for (let rep = 0; rep < 2; rep++) {
const src = fs.readFileSync(__dirname + `/var/${V}.html`, 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/${V}_1e.html`, src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); p.on('pageerror', (e) => errs.push(V + ' ' + e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/${V}_1e.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1000);
const cnt = await p.evaluate(() => window.__rd.ev(`(() => { const all = [...bodies, ...chDormB].filter((b) => b.kind === 'citizen'); const w = all.filter((b) => !b.police && !b.attacker && !b.guard && !b.robot).length, y = all.filter((b) => b.guard && !b.police).length; return { white: w, yellow: y, total: all.length }; })()`));
let extra = '';
if (V === 'c538' && rep === 0) {
  await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(1500);
  await p.evaluate(() => window.__rd.ev(`chSf.on = true; chSf.T = 118; me.hp = me.maxHp = 1e6; for (let i = 0; i < 400; i++) { for (const w of teamWait) w.hold = false; paused = false; stepWorld(0.05); } paused = false;`));
  await p.waitForTimeout(1500);
  extra = JSON.stringify(await p.evaluate(() => window.__rd.ev('chObjPts().length')));
  await p.screenshot({ path: 'shot538_mm.png', clip: { x: 270, y: 0, width: 120, height: 120 } });
  await p.evaluate(() => document.getElementById('minimap').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); await p.waitForTimeout(600);
  await p.screenshot({ path: 'shot538_mmbig.png' });
}
console.log(V, rep, JSON.stringify(cnt), extra); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
