const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = []; const out = {};
for (const [stg, dif] of [[1, 'h'], [3, 'h']]) {
  const src = fs.readFileSync(__dirname + '/var/c506.html', 'utf8').replace('window.__map = "b";', `window.__map = "m"; window.__stg = ${stg}; window.__dif = "${dif}";`).replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
  fs.writeFileSync(__dirname + `/var/c506_${stg}${dif}.html`, src);
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
  await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
  await p.goto('file://' + __dirname + `/var/c506_${stg}${dif}.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
  out[stg + dif] = await p.evaluate(() => window.__rd.ev(`(() => {
    chBossSpawn(teamSeg(), 'tank'); const T = chTanks[chTanks.length - 1];
    const s = addCitizen(me.foot.x + 3, me.foot.z, null, 'soldier'), so = addCitizen(me.foot.x + 3.5, me.foot.z, null, 'soldier');
    me.hp = me.maxHp = 100000; let h0 = me.hp; landHit(T.gun, me, 100); const tankHit = h0 - me.hp;
    h0 = me.hp; landHit(so, me, 100); const solHit = h0 - me.hp;
    const cz = bodies.find((b) => b.kind === 'citizen' && chCanSleep(b)); const sleepN = !!cz; cz.sfw = 1; const sleepSf = chCanSleep(cz); cz.sfw = 0; cz.cvy = true; const sleepCv = chCanSleep(cz); cz.cvy = false;
    for (let k = 0; k < 8; k++) { const d = chDroneAdd(me.foot.x + 20, me.foot.z); d.cvy = true; }
    const before = chDrones.length; stars = 5; chDroneOn = true; chDroneT = 1e9;
    for (let i = 0; i < 40; i++) chDroneTick(0.1);
    return { sk: CH_SK, tankHit: Math.round(tankHit), solHit: Math.round(solHit), sleepSf, sleepN, sleepCv, dronesBefore: before, dronesAfter: chDrones.length, normal: chDrones.filter((d) => !d.cvy).length };
  })()`)); }
console.log(JSON.stringify(out)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
