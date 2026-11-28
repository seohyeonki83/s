const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
const src = fs.readFileSync(__dirname + '/var/c582.html', 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + '/var/c582_fx.html', src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c582_fx.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
await p.waitForTimeout(1500);
await p.evaluate(() => { const o = document.querySelector('.ok'); if (o) o.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); });
await p.waitForTimeout(1500);
await p.evaluate(() => window.__rd.ev(`(() => { me.hp = me.maxHp = 1e9; chNoMix = true; const x = me.foot.x - 3, z = me.foot.z + 2; const sg = addCitizen(x, z, square(x, z), 'police'); chMakeSg(sg); sg.sight = 7; sg.met = true; window.__sg = sg; chNoMix = false; const P0 = puff; puff = (x, y, z, col, s0, s1, life, vx, vy, vz, op, dl = 0) => P0(x, y, z, col, s0, s1, life * 20, vx / 20, vy / 20, vz / 20, op, dl * 20); const tgt = { foot: { x: me.foot.x + 3, z: me.foot.z + 2 } }; puff = P0; })()`));
for (const [i, t] of [[1, 600]]) { await p.waitForTimeout(t); await p.screenshot({ path: __dirname + `/shots/c582_sg${i}.png`, clip: { x: 40, y: 260, width: 310, height: 200 } }); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
