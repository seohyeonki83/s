const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
const src = fs.readFileSync(__dirname + '/var/c595.html', 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + '/var/c595_mut.html', src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
const url = 'file://' + __dirname + '/var/c595_mut.html';
for (const L of [1, 20]) {
await p.goto(url); await p.evaluate((L) => localStorage.setItem('rd_save_v1', JSON.stringify({ genes: 0, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tr: { mut: L }, tut: true, mig: 1, v2: 1, v3: 1, v4: 1, u2: 1, u3: 1 })), L);
await p.goto(url); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
console.log('단계', L, await p.evaluate(() => window.__rd.ev(`(() => { const o = {};
  chNoMix = true; const put = (t, dx, dz) => { const x = me.foot.x + dx, z = me.foot.z + dz; return addCitizen(x, z, square(x, z), t); };
  const al = put('', 20, 20); makeZombie(al); mutate(al, 'armor'); const po = put('police', 20 + (al.r + po0r()) , 20); function po0r() { return BODY; }
  chNoMix = false; if (!zombies.includes(al)) zombies.push(al); po.fixed = true; po.sleep = true; const h0 = po.hp; let t = 0, hits = 0, last = h0; for (let i = 0; i < 60; i++) { po.foot.set(al.foot.x + al.r + BODY, 0, al.foot.z); chSpikeTick(0.1); if (po.hp < last) { hits++; last = po.hp; } }
  o.dbg = [zombies.includes(al), isZombie(al), al.mut, al.dead, al.space === po.space, po.kind, po.hp > 0, al.r, Math.hypot(po.foot.x - al.foot.x, po.foot.z - al.foot.z).toFixed(2)].join(','); o.가시몸 = '6초 동안 ' + hits + '번 · 피해 ' + (h0 - po.hp).toFixed(1) + ' (간격 ' + chSpkIv().toFixed(2) + '초)';
  const hy = put('', 24, 24); makeZombie(hy); mutate(hy, 'hydra'); const sh = put('police', 30, 30); let miss = 0, kb = 0; for (let i = 0; i < 2000; i++) { hy.hp = hy.maxHp; const before = hy.hp; landHit(sh, hy, 1); if (hy.missAt === clock) { miss++; if (giveKnock(hy, 1, 0, 3, 0.2)) kb++; hy.missAt = -1; } }
  o.히드라회피 = (miss / 20).toFixed(1) + '% (넉백 들어간 회피 ' + kb + ')';
  mutate(me, 'hydra'); let mm = 0; for (let i = 0; i < 2000; i++) { me.hp = me.maxHp; landHit(sh, me, 1); if (me.missAt === clock) { mm++; me.missAt = -1; } } o.나_히드라회피 = (mm / 20).toFixed(1) + '%';
  return JSON.stringify(o); })()`)));
}
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
