const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const dif of ['e', 'n', 'h']) {
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(dif + ' ' + e.message + ' ' + (e.stack || '').split('\n').slice(1, 3).join(' | ')));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
const src = fs.readFileSync(__dirname + '/var/c539.html', 'utf8').replace('window.__map = "b";', `window.__map = "m"; window.__stg = 3; window.__dif = "${dif}";`).replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/c539_3${dif}.html`, src);
await p.goto('file://' + __dirname + `/var/c539_3${dif}.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1200);
await p.evaluate(() => { window.__noRender = true; document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); }); await p.waitForTimeout(600);
console.log(dif, JSON.stringify(await p.evaluate(() => window.__rd.ev(`(() => { me.hp = me.maxHp = 1e8; deaths = 40;
  let waves = 0; const w0 = () => bodies.filter((b) => b.bWave).length;
  for (let i = 0; i < 3000; i++) { paused = false; me.hp = me.maxHp; stepWorld(0.05); if (i % 600 === 599) { const T = CH_MAP.typeB; me.foot.set(i % 1200 === 599 ? T.bx : me.foot.x, 0, i % 1200 === 599 ? T.yz + 3 : me.foot.z); } }
  return { t: Math.round(chRunT), chAL, waves: w0(), yard: chB.yard.length, entered: chB.entered, chk: chB.chkCap, won: chSf.won, cops: bodies.filter((b) => b.police && !b.military).length };
})()`))));
await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 5))); await b.close(); })();
