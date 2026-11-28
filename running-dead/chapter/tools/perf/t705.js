const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c606_bomb.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
console.log(await p.evaluate(() => window.__rd.ev(`(() => { const log = []; const H0 = chHitPop; chHitPop = (x, z, n, y) => { log.push(clock.toFixed(2) + ':순간' + Math.round(n)); H0(x, z, n, y); }; me.hp = me.maxHp = 1e9; owned.acidp = true; owned.acid = true; ilv.acid = ilv.acid || 0; const P0 = chDotPop; chDotPop = (x, z, n, y) => { log.push(clock.toFixed(2) + ':' + Math.round(n)); P0(x, z, n, y); };
  chNoMix = true; const cs = []; for (let i = 0; i < 6; i++) { const x = me.foot.x + 3 + (i % 3) * 0.9, zz = me.foot.z + Math.floor(i / 3) * 0.9; const c = addCitizen(x, zz, square(x, zz), 'police'); c.hp = c.maxHp = 1e5; c.atkT = 999; cs.push(c); }
  const al = addCitizen(me.foot.x + 3.9, me.foot.z + 0.45, square(me.foot.x + 3.9, me.foot.z + 0.45), ''); chNoMix = false; makeZombie(al); if (!zombies.includes(al)) zombies.push(al);
  chBombCharge(al, 2); al.bombing.t = 99; killZombie(al);
  const t0 = clock; for (let i = 0; i < 200; i++) { paused = false; me.hp = me.maxHp; stepWorld(1 / 30); }
  chDotPop = P0; const byT = {}; for (const e of log) { const [t, n] = e.split(':'); (byT[n] = byT[n] || 0); byT[n]++; }
  return '6.7초 동안 뜬 숫자 개수 ' + JSON.stringify(byT) + ' · 처음 15개 ' + log.slice(0, 15).join(' '); })()`)));
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
