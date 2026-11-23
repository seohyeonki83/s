// c406: 새 본 맵 — 뜨는지 · 시작 자리 · 수 · 스샷
const { chromium } = require('playwright');
const V = process.argv[2] || 'c406m', SEED = +(process.argv[3] || 1), TAG = process.argv[4] || 'm';
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--enable-precise-memory-info'] });
const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 }); await ctx.addInitScript((s) => { window.__seed = s; window.__noReload = true; }, SEED);
const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 3).join(' | ')));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
const t0 = Date.now();
await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 }); const load = Date.now() - t0; await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(800);
const info = await p.evaluate(() => { const R = window.__rd, s = R.sec(), me = R.me, Z = R.ch.zones; const zi = Z.findIndex((q) => me.foot.x >= q[0] && me.foot.x <= q[2] && me.foot.z >= q[1] && me.foot.z <= q[3]);
  return { ver: document.getElementById('ver').textContent, zones: Z.length, passes: R.ch.passes2.length, rivers: R.ch.rivers.length, buildings: R.buildings.length, mm: R.ch.mm, me: [Math.round(me.foot.x), Math.round(me.foot.z)], startZone: zi, startZ: R.ch.startZ, live: s.secs.filter((q) => q.live).map((q) => q.i), bodies: R.bodies.length, dormB: s.dormB.length, cars: R.cars().length, dormC: s.dormC.length, scene: s.scene.children.length, heapMB: performance.memory ? Math.round(performance.memory.usedJSHeapSize / 1048576) : 0 }; });
console.log('load ms', load, JSON.stringify(info));
const S = '/home/user/s/running-dead/chapter/shots/';
await p.screenshot({ path: S + 'c406_' + TAG + '_1.png' });
// 다 밝히고 전체 지도
await p.evaluate(() => { const R = window.__rd; R.explored.fill(1); const mm = R.ch.mm, W = Math.ceil((mm.x1 - mm.x0) / 2); R.explored[Math.floor((R.me.foot.z - mm.z0) / 2) * W + Math.floor((R.me.foot.x - mm.x0) / 2)] = 0; }); await p.waitForTimeout(500);
await p.screenshot({ path: S + 'c406_' + TAG + '_2.png' });
await p.evaluate(() => document.getElementById('minimap').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); await p.waitForTimeout(700);
await p.screenshot({ path: S + 'c406_' + TAG + '_3map.png' });
console.log('errors', JSON.stringify(errs.slice(0, 5))); await b.close(); })();
