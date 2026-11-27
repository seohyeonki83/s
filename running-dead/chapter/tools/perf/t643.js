const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const dif of ['e']) {
const src = fs.readFileSync(__dirname + '/var/c550.html', 'utf8').replace('window.__map = "b";', `window.__map = "m"; window.__stg = 1; window.__dif = "${dif}";`).replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/c550_1${dif}.html`, src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(dif + ' ' + e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/c550_1${dif}.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(800);
console.log(dif, await p.evaluate(() => window.__rd.ev(`(() => { const out = []; me.hp = me.maxHp = 1e9; const tur = () => bodies.filter((b) => b.turret).length + chDormB.filter((b) => b.turret).length;
  for (const D of [5, 30, 160, 330, 540, 790]) { deaths = D; stars = Math.min(STAR_MAX, STAR_AT.filter((n) => deaths >= n).length); chAL = CH_AL_AT.filter((n) => deaths >= n).length; for (let i = 0; i < 40; i++) { paused = false; me.hp = me.maxHp; stepWorld(0.05); } out.push('Lv' + chAL + ':' + tur()); }
  const pT = chBar.X.filter((X) => X.pend && X.pend.includes('T')).length; chSecAwake = () => true; chBarCatch(); out.push('pendT ' + pT + ' afterWake ' + tur()); return 'mixL ' + CH_MIXL + ' | ' + out.join(' '); })()`))); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
