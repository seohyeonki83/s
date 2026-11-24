// c422: 갈림길 — 자폭 스위치 ★6 → 7번째 강화에서 카드 2장 → 고르면 빨간 별 · 끈적(둔화) · 분열(새끼 2마리 + 경험치 1) · 드론 경험치
const { chromium } = require('playwright');
const V = process.argv[2], PICK = process.argv[3] || 'split';
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
const tap = (txt) => p.evaluate((txt) => { const bs = [...document.querySelectorAll('.okBtn')].filter((x) => !txt || x.textContent.trim() === txt); bs.forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); return bs.length; }, txt);
const out = {}; await tap(); await p.waitForTimeout(600);
await p.evaluate(() => window.__rd.give('bomb')); await p.waitForTimeout(2500); await tap('획득'); await p.waitForTimeout(900);
await p.evaluate(() => window.__rd.setLv('bomb', 6)); out.at6 = await p.evaluate(() => [window.__rd.SK('bomb', 6), window.__rd.SL('bomb', 6)]);
await p.evaluate(() => window.__rd.give('bomb')); await p.waitForTimeout(2500); out.upBtns = await p.evaluate(() => [...document.querySelectorAll('#acq .okBtn')].map((x) => x.textContent.trim())); out.upStars = await p.evaluate(() => { const a = document.getElementById('acq'); return a ? a.innerText.replace(/\s+/g, ' ').slice(0, 200) : null; });
await tap('강화'); await p.waitForTimeout(2000);
out.pick = await p.evaluate(() => { const q = document.getElementById('pick'); return q ? q.innerText.replace(/\s+/g, ' ') : null; });
await p.screenshot({ path: __dirname + '/perf/c422_branch.png' });
await p.evaluate((id) => { const c = document.querySelector(`#pick .card[data-k="${id}"]`); if (c) c.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); }, PICK); await p.waitForTimeout(1500);
out.after = await p.evaluate(() => ({ br: Object.assign({}, window.__rd.BR), lv: window.__rd.inv().lv.bomb, stat: window.__rd.SL('bomb', window.__rd.inv().lv.bomb), stars: window.__rd.SK('bomb', window.__rd.inv().lv.bomb), open: !!document.getElementById('pick') }));
// 빨간 ★6까지
await p.evaluate(() => window.__rd.setLv('bomb', 12)); out.max = await p.evaluate(() => [window.__rd.SK('bomb', 12), window.__rd.SL('bomb', 12)]);
// 효과 시험
out.fx = await p.evaluate((PICK) => { const R = window.__rd, me = R.me; me.hp = me.maxHp = 1e9; const o = {};
  const cs = R.bodies.filter((c) => c.kind === 'citizen' && c.maxHp > 0 && !c.space && !c.police).slice(0, 20);
  if (PICK === 'split') { const xp0 = R.lvInfo(); const al0 = R.bodies.filter((b) => b.kind === 'ally').length; let n = 0;
    for (const c of cs) { c.sleep = false; window.__goo(c); c.hp = 0; } for (let i = 0; i < 3; i++) R.step(1 / 60);
    const al1 = R.bodies.filter((b) => b.kind === 'ally'); const minis = al1.filter((b) => b.mini).length; const xp1 = R.lvInfo();
    o.split = { tried: cs.length, newAllies: al1.length - al0, minis, xpGain: (xp1.level - xp0.level) * 1000 + (xp1.xp - xp0.xp) }; }
  else { const c = cs[0]; c.sleep = false; c.met = true; window.__goo(c); const P = [c.foot.x, c.foot.z]; let L = 0; for (let i = 0; i < 120; i++) { const q = [c.foot.x, c.foot.z]; R.step(1 / 60); L += Math.hypot(c.foot.x - q[0], c.foot.z - q[1]); } o.stickyDist = +L.toFixed(2); }
  const xa = R.lvInfo(); window.__droneAdd(me.foot.x + 3, me.foot.z); const d = window.__drones()[window.__drones().length - 1]; d.hp = 1; d.hp -= 5; window.__drones; R.step(1 / 60);
  return o; }, PICK);
out.droneXp = await p.evaluate(() => { const R = window.__rd, x0 = R.lvInfo().xp; window.__droneAdd(R.me.foot.x + 2, R.me.foot.z); const ds = window.__drones(); const d = ds[ds.length - 1]; R.DD(d, 999); return { before: x0, after: R.lvInfo().xp, dead: d.dead }; });
console.log(V, PICK, JSON.stringify(out, null, 1)); console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
