const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c613_m.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
console.log(await p.evaluate(() => window.__rd.ev(`(() => { const out = [];
  for (const snip of [false, true]) { const tags = []; for (const d of [2.0, 3.0, 4.5, 5.5]) { chHeartDrop(me.foot.x + d, me.foot.z, me.space); const pk = pickups[pickups.length - 1]; pk.tag = d; pk.snip = snip; }
    const eaten = []; for (let i = 0; i < 60; i++) { const before = new Set(pickups); pickupTick(1 / 30); for (const q of before) if (!pickups.includes(q) && q.tag) eaten.push(q.tag + '칸'); }
    const left = pickups.filter((q) => q.tag).map((q) => q.tag + '칸'); for (const q of pickups.filter((q) => q.tag)) scene.remove(q.s); for (let i = pickups.length - 1; i >= 0; i--) if (pickups[i].tag) pickups.splice(i, 1);
    out.push((snip ? '저격수 장비' : '일반') + ' 먹음 ' + eaten.join(',') + ' · 남음 ' + left.join(',')); }
  return out.join('\\n') + '\\n자석 거리 ' + (CH_MAG_R * MELEE).toFixed(2) + ' / 저격수 ' + (CH_MAG_R * 2 * MELEE).toFixed(2); })()`)));
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
