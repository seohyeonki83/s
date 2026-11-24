// c427: 자폭 스위치 모양 · 현금 갈림길 (다이아몬드 싸움 · 차 · 금 드론)
const { chromium } = require('playwright');
const V = process.argv[2], BOMB = process.argv[3] || 'sticky', CASH = process.argv[4] || 'dia';
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
const tap = (txt) => p.evaluate((txt) => { const bs = [...document.querySelectorAll('.okBtn')].filter((x) => !txt || x.textContent.trim() === txt); bs.forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); return bs.length; }, txt);
const pick = (id) => p.evaluate((id) => { const c = document.querySelector(`#pick .card[data-k="${id}"]`); if (c) c.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); return !!c; }, id);
await p.evaluate(() => { window.__noCar = true; }); const out = {}; await tap(); await p.waitForTimeout(600);
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
  const arm = R.bodies.filter((c) => c.kind === 'citizen' && c.maxHp > 0 && !c.space && !c.police && !c.soldier && !c.sniper).slice(0, 5), wh = R.bodies.filter((c) => c.kind === 'citizen' && !(c.maxHp > 0) && !c.space).slice(0, 3), all = [...arm, ...wh];
  all.forEach((c, i) => { const a = i / all.length * 6.28; c.sleep = false; c.met = true; c.foot.x = me.foot.x + Math.cos(a) * 2.2; c.foot.z = me.foot.z + Math.sin(a) * 2.2; c.px = c.foot.x; c.pz = c.foot.z; c.space = null; });
  for (let i = 0; i < 3; i++) R.step(1 / 60);
  const hits = {}; window.__lh = (a, v, dmg) => { if (v.kind !== 'citizen' || !a || a.kind !== 'citizen') return; const k = (a.attacker ? 'att' : a.vig ? 'vig' : a.guard ? 'gd' : '?') + '>' + (v.maxHp > 0 ? 'arm' : 'white'); hits[k] = (hits[k] || 0) + 1; };
  const hp0 = arm.map((c) => c.hp); R.use('cash'); for (const c of all) if (c.state !== 'lured') R.EL(c);
  const tl = []; for (let i = 1; i <= 60 * 4; i++) { R.step(1 / 60); if (i % 40 === 0) tl.push(all.map((c) => c.state.slice(0, 2) + Math.round(c.hp)).join(' ')); }
  return { hits, tl, lost: arm.map((c, j) => Math.round(hp0[j] - c.hp)) }; }, CASH);
await p.evaluate(() => { window.__rd.use('cash'); }); await p.waitForTimeout(300); await p.screenshot({ path: __dirname + '/perf/c427_' + CASH + '.png' });
console.log(V, BOMB, CASH, JSON.stringify(out)); console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
