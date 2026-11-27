const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const V of ['c528']) {
const src = fs.readFileSync(__dirname + `/var/${V}.html`, 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/${V}_1e.html`, src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(V + ': ' + e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/${V}_1e.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1200);
await p.evaluate(() => { window.__noRender = true; document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); }); await p.waitForTimeout(800);
console.log(V, await p.evaluate(() => window.__rd.ev(`(() => { try {
  const l0 = ilv.taser; ilv.taser = 7; const out = []; for (let k = 0; k < 6; k++) { const r = addCitizen(me.foot.x + 2 + k, me.foot.z, square(me.foot.x + 2 + k, me.foot.z), 'robot'); const g0 = chRunGenes; let ok = false; for (let i = 0; i < 40 && !ok; i++) ok = chMadRoll(r); out.push(ok + ':' + (chRunGenes - g0)); }
  ilv.taser = l0; for (let i = 0; i < 60; i++) { paused = false; me.hp = me.maxHp = 1e6; stepWorld(0.033); }
  return 'rolls ' + out.join(' ') + ' · mad ' + bodies.filter((b) => b.mad).length;
} catch (e) { return 'ERR ' + e.message; } })()`))); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
