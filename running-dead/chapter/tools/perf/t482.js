// c405: 재운 것이 화면에 영향을 안 주나 — 같은 순간을 '재운 채'와 '전부 깨운 채'로 그려서 픽셀 비교 (여러 자리에서)
const { chromium } = require('playwright'); const crypto = require('crypto'); const fs = require('fs');
const V = process.argv[2] || 'c405';
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
await ctx.addInitScript((sd) => { window.requestAnimationFrame = () => 0; if (sd) window.__seed = sd; window.__noReload = true; }, +(process.argv[3] || 0));
const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 3).join(' | ')));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(500);
const out = await p.evaluate(() => {
  const R = window.__rd, me = R.me, cv = document.getElementById('view'), res = [];
  document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })));
  me.hp = me.maxHp = 100;   // 체력바는 보통 크기
  const Z = R.ch.zones, P = R.ch.passes2;
  const near = R.bodies.filter((c) => c.kind === 'citizen' && !c.space).sort((a, c) => Math.hypot(a.foot.x - me.foot.x, a.foot.z - me.foot.z) - Math.hypot(c.foot.x - me.foot.x, c.foot.z - me.foot.z)).slice(0, 6);
  near.forEach((h, i) => { h.sleep = false; h.met = true; R.zombify(h); h.foot.x = me.foot.x + 1 + i * 0.5; h.foot.z = me.foot.z + 1; h.px = h.foot.x; h.pz = h.foot.z; });
  const put = (x, z) => { me.foot.x = x; me.foot.z = z; me.px = x; me.pz = z; for (const c of R.bodies) if (c.kind === 'ally') { c.foot.x = x + (Math.random() - 0.5) * 3; c.foot.z = z + (Math.random() - 0.5) * 3; c.px = c.foot.x; c.pz = c.foot.z; } };
  const rnd0 = Math.random; const shot = () => { let s = 4242; Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; window.__redraw(); const u = cv.toDataURL('image/png'); Math.random = rnd0; return u; };   // 다시 그리기만 (난수는 두 번 다 같은 순서로)
  const spots = [];
  for (const q of P) { spots.push(['건널목 가운데 ' + q.axis, (q.ax + q.bx) / 2, (q.az + q.bz) / 2]); spots.push(['건널목 a끝', q.ax, q.az]); spots.push(['건널목 b끝', q.bx, q.bz]); }
  Z.forEach((q, i) => { spots.push(['구역 ' + i + ' 모서리', q[0] + 2.25, q[1] + 2.25]); spots.push(['구역 ' + i + ' 맞은편 모서리', q[2] - 2.25, q[3] - 2.25]); spots.push(['구역 ' + i + ' 가운데 길', (q[0] + q[2]) / 2, q[1] + 2.25]); });
  window.__noRender = true;
  const EVERY = spots.length > 60 ? 6 : 1;
  for (const [name, x, z] of spots.filter((q, i) => i % EVERY === 0)) {
    window.__secOff = false; put(x, z);
    for (let i = 0; i < 90; i++) { me.foot.x = x; me.foot.z = z; R.step(1 / 60); }   // 1.5초 — 단락이 깨고 자리를 잡게
    window.__secOff = true;                    // 여기서부터 단락 상태를 얼린다
    const s = R.sec(), live = s.secs.filter((q) => q.live).map((q) => q.i).join(''), dorm = s.dormB.length;
    const a = shot();                          // 재운 채
    s.wakeAll(); const act = R.bodies.length;
    const c = shot();                          // 전부 깨운 채 (같은 순간 — 걸음 0)
    res.push({ name, live, dorm, same: a === c, a: a === c ? null : a, c: a === c ? null : c });
    window.__secOff = false;
  }
  return res;
});
let bad = 0;
for (const r of out) { if (!r.same) { bad++; const k = bad; fs.writeFileSync(__dirname + '/perf/diff_' + k + '_a.png', Buffer.from(r.a.split(',')[1], 'base64')); fs.writeFileSync(__dirname + '/perf/diff_' + k + '_c.png', Buffer.from(r.c.split(',')[1], 'base64')); } console.log((r.same ? 'SAME ' : 'DIFF ') + r.name + '  깨어 있는 단락 ' + r.live + '  재운 몸 ' + r.dorm); }
console.log('diff', bad, 'of', out.length, 'errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
