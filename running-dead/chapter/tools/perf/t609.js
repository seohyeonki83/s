const { chromium } = require('playwright'); const fs = require('fs');
const V = process.argv[2];
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const kind of ['ally', 'armor']) {
const src = fs.readFileSync(__dirname + `/var/${V}.html`, 'utf8').replace('window.__map = "b";', 'window.__map = "t";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/${V}_tq.html`, src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/${V}_tq.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1200);
await p.evaluate(() => { window.__noRender = true; document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); }); await p.waitForTimeout(800);
console.log(V, kind, await p.evaluate((kind) => window.__rd.ev(`(() => {
  const C7 = buildings.find((B) => B.local === 911), bars = cars.filter((c) => c.barr && c.tutS === C7), zc = (C7.z0 + C7.z1) / 2, bx = Math.min(...bars.map((c) => c.x));
  for (const c of bodies) if (c.kind === 'citizen' && c.space === C7 && !c.post) { c.foot.set(c.foot.x + 300, 0, c.foot.z); c.space = null; }   // 앞의 빨강 · 주황은 치우고 바리케이트 뒤 경찰 4만
  const pol = bodies.filter((c) => c.kind === 'citizen' && c.space === C7); for (const c of pol) { c.hp = c.maxHp = 1e7; } for (const c of bodies) if (c.kind === 'citizen' && c.hp <= 0) c.foot.set(c.foot.x + 300, 0, c.foot.z);
  me.foot.set(bx - 6, 0, zc); me.space = C7; me.hp = me.maxHp = 1e6;
  const A = []; for (const dz of [-1.2, 0, 1.2]) { const q = addCitizen(bx - 2.2, zc + dz, C7, ''); q.space = C7; makeZombie(q); const a = q; if ('${kind}' === 'armor') mutate(a, 'armor'); a.foot.set(bx - 1.6, 0, zc + dz); a.space = C7; a.hp = a.maxHp = 1e6; A.push(a); }
  const tg = {}; const s0 = strike; strike = (zz, tt) => { if (A.includes(zz)) { const k = tt.kind === 'obj' ? (tt.car && tt.car.barr ? 'barricade' : tt.type) : tt.kind; tg[k] = (tg[k] || 0) + 1; } return s0(zz, tt); };
  const st = { calls: 0, atk: 0, mh: 0, none: 0, hit: 0, other: {} }; const m0 = chMoveHit; chMoveHit = (z, dt) => { if (A.includes(z)) { st.calls++; if (z.atkT > 0) st.atk++; else if ((z.mhT || 0) - dt > 0) st.mh++; else { const th = chTouch(z); if (!th) { st.none++; const no = nearObj(z); const k = no ? 'gap' + objGap(no, z).toFixed(1) + '>' + chReach(z).toFixed(1) : 'noObj'; st.other[k] = (st.other[k] || 0) + 1; } else st.hit++; } } return m0(z, dt); };
  const uz = { n: 0, knock: 0, mut: 0, bite: 0, pounce: 0, mode: {} }; const u0 = updateZombie; updateZombie = (z, dt) => { if (A.includes(z)) { uz.n++; if (z.knockT > 0) uz.knock++; uz.mode[z.mode] = (uz.mode[z.mode] || 0) + 1; } return u0(z, dt); };
  const hp0 = bars.reduce((s, c) => s + c.obj.hp, 0), x0 = bars.map((c) => c.x); const sp = [];
  for (let i = 0; i < 150; i++) { paused = false; me.hp = me.maxHp; for (const c of pol) c.hp = 1e7; stepWorld(0.033); if (i % 30 === 29) sp.push(A.map((a) => (a.realSp || 0).toFixed(1)).join('/')); }
  strike = s0; chMoveHit = m0; updateZombie = u0;
  return 'upd ' + JSON.stringify(uz) + ' · moveHit ' + JSON.stringify(st).slice(0, 300) + ' · targets ' + JSON.stringify(tg) + ' · bar hp ' + Math.round(hp0) + '→' + Math.round(bars.reduce((s, c) => s + c.obj.hp, 0)) + ' · pushed ' + Math.max(...bars.map((c, i) => Math.abs(c.x - x0[i]))).toFixed(2) + ' · realSp ' + sp.join(' ') + ' · eng ' + A.map((a) => a.engaging ? a.engaging.kind : '-').join(',');
})()`), kind)); await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
