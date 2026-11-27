const { chromium } = require('playwright'); const fs = require('fs');
const src = fs.readFileSync(__dirname + '/var/c526.html', 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + '/var/c526_1e.html', src);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c526_1e.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1200);
await p.evaluate(() => { window.__noRender = true; document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); }); await p.waitForTimeout(800);
console.log(await p.evaluate(() => window.__rd.ev(`(() => {
  // 도망가는 사람 하나: 나에게서 멀어지게 계속 걷는다
  const c = addCitizen(me.foot.x + 2, me.foot.z, square(me.foot.x + 2, me.foot.z), ''); c.hp = c.maxHp = 1e6; me.hp = me.maxHp = 1e6; paused = false;
  const out = []; let px = c.foot.x, pz = c.foot.z;
  for (let i = 0; i < 16; i++) {
    if (i === 5) landHit(me, c, 1);
    c.vel.set(3, 0); c.knockT = 0; c.state = 'normal';
    const fl = CH_FLINCH(c); stepWorld(0.025);
    out.push((i === 5 ? '맞음 ' : '') + (Math.hypot(c.foot.x - px, c.foot.z - pz) / 0.025).toFixed(2) + '(' + fl.toFixed(2) + ')'); px = c.foot.x; pz = c.foot.z;
  }
  return out.join(' ');
})()`)));
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
