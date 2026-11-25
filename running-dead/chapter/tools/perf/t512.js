// c434: ★0 자폭 산성을 뒤집어쓴 드론이 죽나
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + process.argv[2] + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(800);
console.log(process.argv[2], JSON.stringify(await p.evaluate(() => { const R = window.__rd, me = R.me; me.hp = me.maxHp = 1e9; window.__droneAdd(me.foot.x + 6, me.foot.z); const d = window.__drones()[window.__drones().length - 1]; const hp0 = d.hp; d.goo = 4; d.gooT = 0; d.tg = null;
  const tl = []; for (let i = 1; i <= 60 * 5; i++) { R.step(1 / 60); if (i % 60 === 0) tl.push((i / 60) + 's:' + (d.dead ? 'dead' : d.hp)); } return { hp0, tl }; })), errs); await b.close(); })();
