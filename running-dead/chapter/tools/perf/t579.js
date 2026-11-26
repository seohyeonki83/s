const { chromium } = require('playwright'); const fs = require('fs');
const [stg, dif] = [process.argv[2], process.argv[3]];
const src = fs.readFileSync(__dirname + '/var/c505.html', 'utf8').replace('window.__map = "b";', `window.__map = "m"; window.__stg = ${stg}; window.__dif = "${dif}";`).replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/c505_${stg}${dif}.html`, src);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack||'').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/c505_${stg}${dif}.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => { window.__noRender = true; document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); }); await p.waitForTimeout(800);
const log = [];
for (let chunk = 0; chunk < 80; chunk++) {
  const r = await p.evaluate(() => window.__rd.ev(`(() => {
    const out = [];
    if (!chSf.on) { chSf.on = true; chSf.T = 115; }
    for (let i = 0; i < 100; i++) {
      for (const w of teamWait) if (w.hold) { w.hold = false; }
      me.hp = me.maxHp; paused = false;
      stepWorld(0.1);
      if (i % 10 === 0) {
        for (const b of bodies.slice()) if (b.kind === 'citizen' && (b.sfw || b.cvy || b.tkU) && b.hp > 0 && (b.kAge = (b.kAge || 0) + 1) > 3) makeZombie(b);
        for (const d of chDrones.slice()) if (d.cvy && !d.ride && !d.dead && (d.kAge = (d.kAge || 0) + 1) > 3) chDroneDie(d);
        for (const t of chTanks) if (!t.wreck && (t.kAge = (t.kAge || 0) + 1) > 20) { t.hp = 0; t.wreck = true; chTankDead(t); }
      }
    }
    return { T: Math.round(chSf.T), n: chSf.n, boss: chSf.boss, bossOut: chSf.bossOut, won: chSf.won, obj: chObjText(), cvy: chCvy.length, rideD: chDrones.filter((d) => d.ride).length, cvyD: chDrones.filter((d) => d.cvy && !d.dead).length, tanks: chTanks.map((t) => [t.dozer ? 'D' : 'T', Math.round(t.maxHp || 0), t.wreck ? 1 : 0]), wn: chSf.wn, tw: teamWait.length, sf: bodies.filter((b) => b.kind === 'citizen' && b.sfw).length, over: chRunOver, robotsCvy: bodies.filter((b) => b.cvy && b.robot).length };
  })()`));
  log.push(r);
  if (r.won) { await p.waitForTimeout(3000); console.log(JSON.stringify(await p.evaluate(() => window.__rd.ev("({acqOpen, starAnim, lvOpen, rankAnim, squadAnim, tutOpen, victoryOn, menuOv: !!menuOv, goalShown, tq: tutQueue.length, paused, fx: fxQueue.length})")))); break; }
}
console.log(JSON.stringify(await p.evaluate(() => window.__rd.ev('({acqOpen, starAnim, lvOpen, rankAnim, squadAnim, tutOpen, victoryOn, menuOv: !!menuOv, goalShown, tq: tutQueue.length, paused, fx: fxQueue.length, cur: !!curFx, over: chRunOver})'))));
const fin = await p.evaluate(() => { const o = document.getElementById('rres'); return { res: o ? o.innerText.replace(/\n/g, ' | ') : null, sv: localStorage.getItem('rd_save_v1') }; });
let prev = ''; for (const r of log) { const s = JSON.stringify(r); const k = JSON.stringify([r.n, r.boss, r.bossOut, r.won, r.obj, r.cvy, r.rideD, r.cvyD, r.tanks.length]); if (k !== prev) console.log(s); prev = k; }
console.log(JSON.stringify(log[log.length - 1]));
console.log(JSON.stringify(fin)); console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
