// c407: 본 맵 테스트 — 속도 3배 · 이동만 · 적이 나를 못 본다 · 원형 미니맵
const { chromium } = require('playwright');
const V = process.argv[2] || 'c407w', SEED = +(process.argv[3] || 1);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 }); await ctx.addInitScript((s) => { window.__seed = s; window.__noReload = true; }, SEED);
const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 3).join(' | ')));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 }); await p.waitForTimeout(1200);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(400);
const S = '/home/user/s/running-dead/chapter/shots/';
const info0 = await p.evaluate(() => { const R = window.__rd, me = R.me, e = document.getElementById('minimap'), cs = getComputedStyle(e); return { ver: document.getElementById('ver').textContent, speed: +me.speed.toFixed(2), hp: [Math.round(me.hp), Math.round(me.maxHp)], mm: [cs.width, cs.height, cs.borderRadius, cs.outlineStyle, cs.boxShadow.slice(0, 40)], items: document.querySelectorAll('.item').length, at: [me.foot.x, me.foot.z] }; });
console.log('start', JSON.stringify(info0));
// 조이스틱으로 2초 — 순환도로를 따라 (시작 자리는 순환도로 안쪽) 오른쪽으로
await p.mouse.move(195, 600); await p.mouse.down(); await p.mouse.move(315, 600, { steps: 3 }); await p.waitForTimeout(300);
const a = await p.evaluate(() => [window.__rd.me.foot.x, window.__rd.me.foot.z, performance.now()]); await p.waitForTimeout(1500);
const c = await p.evaluate(() => [window.__rd.me.foot.x, window.__rd.me.foot.z, performance.now(), window.__rd.me.vel.length()]); await p.mouse.up();
console.log('moved', Math.hypot(c[0] - a[0], c[1] - a[1]).toFixed(1), 'in', ((c[2] - a[2]) / 1000).toFixed(2), 's  vel', c[3].toFixed(2));
// 사람들 한가운데로: 농구장·주유소·공사장 자리, 그리고 경찰서·군사시설 문 앞
const spots = await p.evaluate(() => { const R = window.__rd, C = R.ch, out = []; const z0 = C.startZ;
  for (const s of C.spots) if (s.at && out.length < 3) out.push(['spot ' + s.k, s.at[0], s.at[1]]);
  for (const t of ['police', 'army']) { const B = R.buildings.find((q) => q.type === t); if (B) out.push([t, B.front ? B.front.cx + B.front.nx * 2.5 : B.x0 - 2, B.front ? B.front.cz + B.front.nz * 2.5 : B.z0 - 2]); }
  return out; });
for (const [name, x, z] of spots) {
  await p.evaluate(([x, z]) => { const me = window.__rd.me; me.foot.x = x; me.foot.z = z; me.px = x; me.pz = z; }, [x, z]);
  await p.waitForTimeout(6000);
  const r = await p.evaluate(() => { const R = window.__rd, me = R.me; const near = R.bodies.filter((c) => c.kind === 'citizen' && Math.hypot(c.foot.x - me.foot.x, c.foot.z - me.foot.z) < 7);
    return { near: near.length, awake: near.filter((c) => !c.sleep).length, states: [...new Set(near.map((c) => c.state))], noticed: near.filter((c) => c.notice > 0 || c.iconKind).length, hurt: near.filter((c) => c.maxHp > 0 && c.hp < c.maxHp).length, infect: near.filter((c) => c.infect > 0).length, shots: near.filter((c) => c.shotT >= 0).length, police: near.filter((c) => c.police).length, meHp: Math.round(me.hp) + '/' + Math.round(me.maxHp), meMode: me.mode, allies: R.bodies.filter((c) => c.kind === 'ally').length }; });
  console.log(name, JSON.stringify(r));
  if (name === 'spot court' || name.startsWith('spot')) await p.screenshot({ path: S + 'c407_w_' + name.replace(' ', '_') + '.png' });
}
// 다 밝히고 전체 지도도
await p.evaluate(() => document.getElementById('minimap').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); await p.waitForTimeout(500);
const big = await p.evaluate(() => { const e = document.getElementById('minimap'), cs = getComputedStyle(e); return [cs.width, cs.height, cs.borderRadius]; });
await p.evaluate(() => document.getElementById('minimap').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); await p.waitForTimeout(300);
console.log('big map style', JSON.stringify(big), 'errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
