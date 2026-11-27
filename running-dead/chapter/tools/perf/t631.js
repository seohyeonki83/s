const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
const src = fs.readFileSync(__dirname + '/var/c541.html', 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + '/var/c541_1e.html', src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c541_1e.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(800);
console.log(await p.evaluate(() => window.__rd.ev(`(() => { const sees = iSee; let seen = 0; iSee = () => true; const out = [];
  const L = bodies.filter((c) => c.kind === 'citizen' && !c.disc && !c.boss && c.hp > 0 && ((c.attacker) || (c.police && !c.military && c.street) || c.guard));
  for (let i = 0; i < 400; i++) { chDiscT = 0; chDiscTick(0.1); }
  iSee = sees; return 'red/cop kept ' + chDiscR + ' · org ' + chDiscO + ' · yel ' + chDiscY + ' · demoted ' + bodies.filter((c) => c.demoted).length; })()`)));
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
