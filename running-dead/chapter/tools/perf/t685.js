const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const v of ['c590', 'c591']) {
const src = fs.readFileSync(__dirname + `/var/${v}.html`, 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 2; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/${v}_veh.html`, src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/${v}_veh.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
console.log(v, await p.evaluate(() => window.__rd.ev(`(() => { CH_UPK.ahp = 1.1;
  const mk = (cvy) => { const x = me.foot.x + 8, z = me.foot.z + (cvy ? 4 : 8); addCar(x, z, 0, null, 0); const c = cars[cars.length - 1]; if (cvy) c.cvy = true; return c; };
  const hit = (c) => { const o = c.obj; if (!o) return 'obj없음'; const h0 = o.hp; landHit(me, o, 100); return (h0 - o.hp).toFixed(1); };
  const fake = (cvy, tank) => ({ kind: 'obj', type: 'car', car: { cvy, tank }, foot: me.foot.clone(), hp: 1e5, maxHp: 1e5, dead: false }); const pc = { obj: fake(false, false) }, cv = { obj: fake(true, false) }, tk = { obj: fake(false, true) };
  chNoMix = true; const x = me.foot.x + 3, z = me.foot.z; const pk = addCitizen(x, z, square(x, z), ''); chNoMix = false; pk.boss = 'armor'; makeZombie(pk);
  return 'CH_SK ' + CH_SK + ' · 경찰차 100 → ' + hit(pc) + ' · 군인차부대 차 100 → ' + hit(cv) + ' · 장갑차 100 → ' + hit(tk) + ' · 분홍 덩치 체력 ' + pk.maxHp.toFixed(1); })()`))); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
