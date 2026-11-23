// c409: 물·산 반반 본 맵 — 산길·다리·산가 스샷 + 전체 지도
const { chromium } = require('playwright');
const V = process.argv[2] || 'c409m', SEED = +(process.argv[3] || 1);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 }); await ctx.addInitScript((s) => { window.__seed = s; window.__noReload = true; }, SEED);
const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 2).join(' | ')));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 }); await p.waitForTimeout(1200);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(400);
const spots = await p.evaluate(() => { const R = window.__rd, C = R.ch, out = [];
  const hv = C.passes2.find((q) => q.hill && q.axis === 'v'), hh = C.passes2.find((q) => q.hill && q.axis === 'h'), wv = C.passes2.find((q) => !q.hill && q.axis === 'v');
  if (hh) out.push(['1_pass_h', hh.ax, (hh.az + hh.bz) / 2]); if (hv) out.push(['2_pass_v', (hv.ax + hv.bx) / 2, hv.az]); if (wv) out.push(['3_bridge_v', (wv.ax + wv.bx) / 2, wv.az]);
  // 물과 산이 맞닿는 단락 가장자리: 산 덩어리 하나의 구석에서 가장 가까운 구역 순환도로
  const Z = C.zones; let best = null; for (const B of R.buildings) { if (B.type !== 'hill') continue; for (const q of Z) { for (const [x, z] of [[q[0] + 2.25, (q[1] + q[3]) / 2], [q[2] - 2.25, (q[1] + q[3]) / 2], [(q[0] + q[2]) / 2, q[1] + 2.25], [(q[0] + q[2]) / 2, q[3] - 2.25]]) { const d = Math.max(B.x0 - x, x - B.x1, 0) + Math.max(B.z0 - z, z - B.z1, 0); if (d < 3 && !best) best = [x, z]; } } }
  if (best) out.push(['4_hill_edge', best[0], best[1]]);
  return { out, hills: R.buildings.filter((B) => B.type === 'hill').length, rivers: C.rivers.length, bridges: C.bridges.length, share: C.hillShare }; });
console.log(JSON.stringify({ hills: spots.hills, rivers: spots.rivers, bridges: spots.bridges, share: +spots.share.toFixed(2) }));
const S = __dirname + '/perf/t9_';
for (const [name, x, z] of spots.out) { await p.evaluate(([x, z]) => { const me = window.__rd.me; me.hp = me.maxHp; me.foot.x = x; me.foot.z = z; me.px = x; me.pz = z; window.__camK = 1.5; }, [x, z]); await p.waitForTimeout(1300); await p.screenshot({ path: S + name + '.png' }); }
await p.evaluate(() => { const R = window.__rd; window.__camK = 1; R.explored.fill(1); const mm = R.ch.mm, W = Math.ceil((mm.x1 - mm.x0) / 2); R.explored[Math.floor((R.me.foot.z - mm.z0) / 2) * W + Math.floor((R.me.foot.x - mm.x0) / 2)] = 0; }); await p.waitForTimeout(500);
await p.evaluate(() => document.getElementById('minimap').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); await p.waitForTimeout(700);
await p.screenshot({ path: S + '5_map.png' });
console.log(spots.out.map((s) => s[0]).join(' '), 'errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
