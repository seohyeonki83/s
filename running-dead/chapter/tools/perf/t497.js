// c410: pix2b 걷기 시나리오에서 두 버전이 갈라지는 걸음과 첫 잔해가 생기는 걸음 — 잔해가 생기기 전에는 똑같아야 한다
const { chromium } = require('playwright');
const file = process.argv[2], NA = 40, N = 600;
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
  await ctx.addInitScript(() => { let s = 12345; Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; { let u = 777; globalThis.__uu = () => { u = (u * 1103515245 + 12345) >>> 0; return u / 4294967296; }; } window.__secOff = false; window.requestAnimationFrame = () => 0; let t = 1000; performance.now = () => (t += 0.01); Date.now = () => 1700000000000; });
  const p = await ctx.newPage();
  const three = require('fs').readFileSync(__dirname + '/../node_modules/three/build/three.module.min.js', 'utf8').split('4294967295*Math.random()').join('4294967295*globalThis.__uu()');
  await p.route('**/three.module.min.js', (r) => r.fulfill({ body: three, contentType: 'application/javascript' }));
  await p.goto('file://' + __dirname + '/var/' + file + '.html');
  await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 });
  await p.waitForTimeout(800);
  const res = await p.evaluate(({ NA, N }) => {
    const R = window.__rd, me = R.me, bodies = R.bodies;
    document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })));
    me.hp = me.maxHp = 100000;
    const far = bodies.filter((c) => c.kind === 'citizen' && c.sleep && !c.space && Math.hypot(c.foot.x - me.foot.x, c.foot.z - me.foot.z) > 40).slice(0, NA);
    far.forEach((h, i) => { const a = i * 2.399, r = 1.2 + 0.45 * Math.sqrt(i) * 1.6; h.sleep = false; h.met = true; h.space = null; R.zombify(h); h.foot.x = me.foot.x + Math.cos(a) * r; h.foot.z = me.foot.z + Math.sin(a) * r; h.px = h.foot.x; h.pz = h.foot.z; });
    const Z = R.ch.zones, zc = Z.map((q) => [(q[0] + q[2]) / 2, (q[1] + q[3]) / 2]);
    let ti = 0, firstWreck = -1; const sums = [];
    for (let i = 1; i <= N; i++) {
      const [tx, tz] = zc[ti % zc.length], dx = tx - me.foot.x, dz = tz - me.foot.z, d = Math.hypot(dx, dz);
      if (d < 1) ti++; else { me.foot.x += dx / d * 0.07; me.foot.z += dz / d * 0.07; }
      window.__noRender = i % 50 !== 0;
      R.step(1 / 60);
      if (firstWreck < 0 && R.cars().some((c) => c.wreck)) firstWreck = i;
      let s = 0; for (const q of bodies) s += q.foot.x * 1.37 + q.foot.z * 0.91; for (const c of R.cars()) s += c.x * 0.53 + c.z * 0.77; sums.push(s.toFixed(4));
    }
    return { firstWreck, sums };
  }, { NA, N });
  require('fs').writeFileSync(__dirname + '/out410b/sum_' + file + '.json', JSON.stringify(res));
  console.log(file, 'firstWreck', res.firstWreck);
  await b.close();
})();
