const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
const src = fs.readFileSync(__dirname + '/var/c576.html', 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + '/var/c576_tut.html', src);
const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 }); const p = await ctx.newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
const url = 'file://' + __dirname + '/var/c576_tut.html';
await p.goto(url); await p.evaluate(() => localStorage.setItem('rd_save_v1', JSON.stringify({ genes: 0, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tut: true, mig: 1, v2: 1, v3: 1, v4: 1, u2: 1 })));
await p.goto(url); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
await p.waitForTimeout(1500); await p.evaluate(() => { const o = document.querySelector('.ok'); if (o) o.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); });
const seenNames = [];
console.log('보이는 것:', await p.evaluate(() => window.__rd.ev(`(() => { const m = {}; for (const b of bodies) if (b.kind === 'citizen' && (iSee(b) || zSeen(b))) { const k = b.police ? 'police' : b.attacker ? 'attacker' : b.guard ? 'guard' : 'citizen'; m[k] = (m[k] || 0) + 1; } return JSON.stringify(m) + ' sense ' + me.sense.toFixed(1) + ' 근처 시민 ' + bodies.filter((b) => b.kind === 'citizen' && Math.hypot(b.foot.x - me.foot.x, b.foot.z - me.foot.z) < 12).length; })()`)));
for (let i = 0; i < 25; i++) {
  await p.waitForTimeout(700);
  const t = await p.evaluate(() => { const o = document.getElementById('tut'); return o ? (o.querySelector('.nm') || {}).textContent : null; });
  if (t) { seenNames.push(t + ' / ' + await p.evaluate(() => document.querySelector('#tut .say').textContent)); if (seenNames.length === 1) await p.screenshot({ path: __dirname + '/shots/c576_tut1.png' }); await p.evaluate(() => document.querySelector('#tut .close').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); }
  if (i === 12) await p.evaluate(() => window.__rd.ev(`(() => { chNoMix = true; const put = (t, dx, dz) => { const x = me.foot.x + dx, z = me.foot.z + dz; return addCitizen(x, z, square(x, z), t); }; put('', -2.5, 0); put('robot', 0, 3); put('soldier', -2, -2.5); put('attacker', 2, 2.5); put('guard', -1, 2.5); chNoMix = false; chDroneAdd(me.foot.x + 3, me.foot.z - 2); })()`));
  if (i === 8) await p.evaluate(() => window.__rd.ev(`(() => { chNoMix = true; const x = me.foot.x + 2.5, z = me.foot.z + 1; const sg = addCitizen(x, z, square(x, z), 'police'); chMakeSg(sg); chNoMix = false; })()`));
}
console.log('소개된 순서:', seenNames.join(' → '));
console.log('저장:', await p.evaluate(() => JSON.stringify(JSON.parse(localStorage.getItem('rd_save_v1')).seen)));
await p.goto(url); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
await p.waitForTimeout(1500); await p.evaluate(() => { const o = document.querySelector('.ok'); if (o) o.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); });
let again = []; for (let i = 0; i < 6; i++) { await p.waitForTimeout(700); const t = await p.evaluate(() => { const o = document.getElementById('tut'); return o ? (o.querySelector('.nm') || {}).textContent : null; }); if (t) { again.push(t); await p.evaluate(() => document.querySelector('#tut .close').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); } }
console.log('다시 들어갔을 때 소개:', again.join(', ') || '없음');
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
