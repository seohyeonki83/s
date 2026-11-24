// c427: 자폭 스위치 모양 · 현금 갈림길 (다이아몬드 싸움 · 차 · 금 드론)
const { chromium } = require('playwright');
const V = process.argv[2], BOMB = process.argv[3] || 'sticky', CASH = process.argv[4] || 'dia';
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
const tap = (txt) => p.evaluate((txt) => { const bs = [...document.querySelectorAll('.okBtn')].filter((x) => !txt || x.textContent.trim() === txt); bs.forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); return bs.length; }, txt);
const pick = (id) => p.evaluate((id) => { const c = document.querySelector(`#pick .card[data-k="${id}"]`); if (c) c.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); return !!c; }, id);
const out = {}; await tap(); await p.waitForTimeout(600);
await p.evaluate(() => window.__rd.give('bag')); await p.waitForTimeout(2500); await tap('획득'); await p.waitForTimeout(900);
for (const [k, id] of [['bomb', BOMB], ['cash', CASH]]) {
  await p.evaluate((k) => window.__rd.give(k), k); await p.waitForTimeout(2500); await tap('획득'); await p.waitForTimeout(900);
  await p.evaluate((k) => window.__rd.setLv(k, 6), k); await p.evaluate((k) => window.__rd.give(k), k); await p.waitForTimeout(2500); await tap('강화'); await p.waitForTimeout(2000);
  out[k] = { picked: await pick(id) }; await p.waitForTimeout(1500);
  out[k].look = await p.evaluate((k) => ({ br: window.__rd.BR[k], name: window.__rd.IT[k].name, btn: !!document.querySelector('.item .ic svg'), goo: window.__rd.gooCol().toString(16) }), k);
}
await p.screenshot({ path: __dirname + '/perf/c427_buttons.png' });
// 현금 쓰기
out.use = await p.evaluate((CASH) => { const R = window.__rd, me = R.me; me.hp = me.maxHp = 1e9;
  const arm = R.bodies.filter((c) => c.kind === 'citizen' && c.maxHp > 0 && !c.space && !c.police).slice(0, 6), wh = R.bodies.filter((c) => c.kind === 'citizen' && c.maxHp === 0 && !c.space).slice(0, 3);
  [...arm, ...wh].forEach((c, i) => { const a = i / 9 * 6.28; c.sleep = false; c.met = true; c.foot.x = me.foot.x + Math.cos(a) * 3.2; c.foot.z = me.foot.z + Math.sin(a) * 3.2; c.px = c.foot.x; c.pz = c.foot.z; c.space = null; });
  const T = R.tr().cars.find((c) => c.tr && c.tr.mode !== 'left' && c.tr.mode !== 'gone'); let tcar = null; if (T) { T.x = me.foot.x + 6; T.z = me.foot.z + 1; tcar = T; }
  let dr = null; if (CASH === 'gold') { window.__droneAdd(me.foot.x + 7, me.foot.z + 4); const ds = window.__drones(); dr = ds[ds.length - 1]; }
  R.step(1 / 60); const hp0 = arm.map((c) => c.hp); const n0 = R.bodies.length;
  R.use('cash'); const o = { thrown: R.cashes().length, lured: [...arm, ...wh].filter((c) => c.state === 'lured').length, carLeft: tcar ? tcar.tr.mode : 'none', newPeople: R.bodies.length - n0, droneLure: dr ? +(dr.lureT || 0).toFixed(2) : null };
  const tl = []; for (let i = 1; i <= 60 * 6; i++) { R.step(1 / 60); if (dr && i % 30 === 0) tl.push([+(i / 60).toFixed(1), +(dr.lureT || 0).toFixed(2), +(dr.stunT || 0).toFixed(2), +Math.hypot(dr.x - (R.cashes()[0] || dr).x, dr.z - (R.cashes()[0] || dr).z).toFixed(1)].join('/')); if (i === 90) { o.mid = { lured: [...arm, ...wh].filter((c) => c.state === 'lured').length, dmgTaken: arm.reduce((s, c, j) => s + Math.max(0, hp0[j] - c.hp), 0).toFixed(1) }; } }
  o.end = { cashes: R.cashes().length, lured: [...arm, ...wh].filter((c) => c.state === 'lured').length, dmgTaken: arm.reduce((s, c, j) => s + Math.max(0, hp0[j] - c.hp), 0).toFixed(1) }; if (dr) o.droneTl = tl;
  return o; }, CASH);
await p.evaluate(() => { window.__rd.use('cash'); }); await p.waitForTimeout(300); await p.screenshot({ path: __dirname + '/perf/c427_' + CASH + '.png' });
console.log(V, BOMB, CASH, JSON.stringify(out)); console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
