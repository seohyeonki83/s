const { chromium } = require('playwright'); const fs = require('fs'); const V = process.argv[2] || 'c511';
const src = fs.readFileSync(__dirname + `/var/${V}.html`, 'utf8').replace('window.__map = "b";', 'window.__map = "t";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/${V}_tq.html`, src);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
const P = JSON.parse(process.argv[3]);
for (const [sx, sz, mx, mz, lab] of P) {
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/${V}_tq.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1000);
await p.evaluate(() => { window.__noRender = true; document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); }); await p.waitForTimeout(600);
const r = await p.evaluate(([sx, sz, mx, mz]) => window.__rd.ev(`(() => {
  const C9 = buildings.find((B) => B.local === 913), C14 = buildings.find((B) => B.local === 914);
  const sns = bodies.filter((b) => b.kind === 'citizen' && b.sniper && b.space === C9), sn = sns[0];
  for (const b of bodies) if (b !== sn && b.kind === 'citizen' && (b.space === C9)) { b.foot.set(C9.x0 + 3, 0, C9.z1 - 1); b.stunT = 999; }
  for (const s of sns.slice(1)) { s.foot.set(C9.x0 + 3.3, 0, C9.z1 - 1.2); }
  me.foot.set(${mx}, 0, ${mz}); me.space = spaceOf(${mx}, ${mz}) || null; me.hp = me.maxHp = 1e6; if (window.__rd) {}
  sn.hp = sn.maxHp = 1e6; const sp0 = spaceOf(${sx}, ${sz});
  let hits = 0, lunges = 0, minD = 99, log = [];
  for (let i = 0; i < 80; i++) { sn.foot.set(${sx}, 0, ${sz}); sn.space = sp0 || sn.space; sn.vel && sn.vel.set(0, 0); const h0 = sn.hp; me.hp = me.maxHp; paused = false; move.set(0, 0); stepWorld(0.05); if (sn.hp < h0) hits++; if (me.lungeVictim === sn) lunges++; const d = Math.hypot(me.foot.x - ${sx}, me.foot.z - ${sz}); minD = Math.min(minD, d); if (i % 20 === 0) log.push([+me.foot.x.toFixed(2), +me.foot.z.toFixed(2), me.mode || me.state, me.space && me.space.local]); }
  chNbrBuild(); return { nbr: buildings.filter((B) => B.nbr).map((B) => B.local + ">" + [...B.nbr].map((q) => q.local).join("/")).join(" "), snSp: sp0 && sp0.local, meSp: me.space && me.space.local, hits, lunges, minD: +minD.toFixed(2), adj: !!chAdjFoe(me), log };
})()`), [sx, sz, mx, mz]);
console.log(lab, JSON.stringify(r)); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
