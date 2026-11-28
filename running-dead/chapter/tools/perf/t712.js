const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c612_sn.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
console.log(await p.evaluate(() => window.__rd.ev(`(() => { const x = me.foot.x + 25, z = me.foot.z + 18; chNoMix = true; const sn = addCitizen(x, z, square(x, z), 'sniper'); chNoMix = false; const n0 = pickups.length, aw0 = pendingAward.length; makeZombie(sn);
  const pk = pickups[pickups.length - 1], d0 = Math.hypot(pk.x - me.foot.x, pk.z - me.foot.z); let t = 0; while (pickups.includes(pk) && t < 5) { pickupTick(1 / 30); t += 1 / 30; }
  return '떨어진 거리 ' + d0.toFixed(1) + '칸 · 저격수 표시 ' + !!pk.snip + ' · 먹은 시간 ' + (pickups.includes(pk) ? '못 먹음' : t.toFixed(2) + '초') + ' · 획득창 대기 +' + (pendingAward.length - aw0); })()`)));
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
