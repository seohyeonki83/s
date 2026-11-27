const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const dif of ['e', 'n', 'h']) {
const src = fs.readFileSync(__dirname + '/var/c551.html', 'utf8').replace('window.__map = "b";', `window.__map = "m"; window.__stg = 1; window.__dif = "${dif}";`).replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/c551_1${dif}.html`, src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(dif + ' ' + e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/c551_1${dif}.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(800);
console.log(dif, await p.evaluate(() => window.__rd.ev(`(() => { const out = []; me.hp = me.maxHp = 1e9; chSecAwake = () => true;
  const X = chBar.X[0]; const comp = () => { const u = X.units.filter((c) => !c.dead); return { 경: u.filter((c) => c.police && !c.sg).length, 샷: u.filter((c) => c.sg).length, 군: u.filter((c) => c.soldier && !c.robot).length, 사: u.filter((c) => c.robot && !c.turret).length }; };
  const tur = () => bodies.filter((b) => b.turret && Math.hypot(b.foot.x - X.cx, b.foot.z - X.cz) < 30).length; const barr = () => X.rows.flat().flat().filter((p) => p && chBarLive(p)).length;
  let prev = comp();
  for (const D of [5, 30, 160, 330, 540, 790, 1080, 1410, 1780, 2190]) { deaths = D; stars = Math.min(STAR_MAX, STAR_AT.filter((n) => deaths >= n).length); chAL = CH_AL_AT.filter((n) => deaths >= n).length; chBar.t = 0; chBarTick(0.01);
    const c = comp(); out.push(chAL + '[' + Object.keys(c).map((k) => c[k] - prev[k] ? k + (c[k] - prev[k]) : '').join('') + ' T' + tur() + ' B' + barr() + ']'); prev = c; }
  return 'mixL ' + CH_MIXL + ' ' + out.join(' '); })()`))); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
