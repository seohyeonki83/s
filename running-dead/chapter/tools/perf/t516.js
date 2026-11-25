// c437: 총동원령 — 건널목 터렛 · 샷건 경찰 2명
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c437z.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(400);
await p.evaluate(() => { const R = window.__rd; R.me.hp = R.me.maxHp = 1e9; R.kills(711); R.incident(R.me.foot.x, R.me.foot.z); });
await p.waitForTimeout(14000);
const o = await p.evaluate(() => { const R = window.__rd, X = R.BAR().X; const tur = R.bodies.filter((c) => c.turret), sg = R.bodies.filter((c) => c.sg);
  return { al: R.AL(), crossings: X.length, turrets: tur.length, sgAtCross: sg.filter((c) => c.gar).length, sgAll: sg.length, robots: R.bodies.filter((c) => c.robot && !c.turret).length, turHp: tur[0] && Math.round(tur[0].maxHp), turFixed: tur[0] && tur[0].fixed };
});
// 터렛 앞으로 가서 화면 + 사격 확인
const o2 = await p.evaluate(() => { const R = window.__rd, t = R.bodies.find((c) => c.turret); R.me.foot.x = t.foot.x + 4; R.me.foot.z = t.foot.z + 3; R.me.space = null; return { tx: +t.foot.x.toFixed(1), tz: +t.foot.z.toFixed(1) }; });
await p.waitForTimeout(2500); await p.screenshot({ path: __dirname + '/perf/c437_turret.png' });
const o3 = await p.evaluate(() => { const R = window.__rd, t = R.bodies.find((c) => c.turret); const x0 = t.foot.x; const xp0 = R.lvInfo().xp; const r = { burstMax: t.burstN, moved: +Math.abs(t.foot.x - x0).toFixed(2) }; t.hp = 0; return new Promise((res) => setTimeout(() => res(Object.assign(r, { gone: !R.bodies.includes(t), xp: R.lvInfo().xp - xp0 })), 500)); });
console.log(JSON.stringify({ o, o2, o3 })); console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
