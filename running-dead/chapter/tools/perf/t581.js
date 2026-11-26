const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = []; const out = {};
for (const v of ['c505_1e', 'c505_3h']) { const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + v + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
out[v] = await p.evaluate(() => window.__rd.ev(`(() => { const s = addCitizen(me.foot.x + 3, me.foot.z, null, 'soldier'), r = addCitizen(me.foot.x + 4, me.foot.z, null, 'robot'), d = chDroneAdd(me.foot.x, me.foot.z + 3);
  const sn = bodies.filter((b) => b.kind === 'citizen' && b.sniper).length;
  return { sk: CH_SK, mix: CH_MIXL, soldier: Math.round(s.maxHp), robot: [r.robot, Math.round(r.maxHp)], drone: Math.round(d.maxHp), snipersOnMap: sn, robotsOnMap: bodies.filter((b) => b.robot).length, mutMax: itemMax('mutate') }; })()`)); }
console.log(JSON.stringify(out)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
