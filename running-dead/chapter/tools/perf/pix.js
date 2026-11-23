// 안 보이는 객체의 위치 계산을 건너뛰어도 화면이 똑같은지 — 난수·시간을 고정하고 손으로 걸음을 돌려 프레임을 비교한다
// node perf/pix.js <variant> <patch:0|1>  → 프레임 해시 출력
const { chromium } = require('playwright'); const crypto = require('crypto');
const file = process.argv[2], PATCH = +process.argv[3];
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
  await ctx.addInitScript(() => { let s = 12345; Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; window.requestAnimationFrame = () => 0; let t = 1000; performance.now = () => (t += 0.01); Date.now = () => 1700000000000; });
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', (e) => errs.push(e.message));
  await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
  await p.goto('file://' + __dirname + '/../var/' + file + '.html');
  await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 });
  await p.waitForTimeout(800);
  const frames = await p.evaluate((PATCH) => {
    const R = window.__rd, me = R.me, bodies = R.bodies, ren = window.__ren, sc = window.__scene, cam = window.__cam;
    document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })));
    me.hp = me.maxHp = 100000;
    const far = bodies.filter((c) => c.kind === 'citizen' && c.sleep && !c.space && Math.hypot(c.foot.x - me.foot.x, c.foot.z - me.foot.z) > 40).slice(0, 40);
    far.forEach((h, i) => { const a = i * 2.399, r = 1.2 + 0.45 * Math.sqrt(i) * 1.6; h.sleep = false; h.met = true; h.space = null; R.zombify(h); h.foot.x = me.foot.x + Math.cos(a) * r; h.foot.z = me.foot.z + Math.sin(a) * r; h.px = h.foot.x; h.pz = h.foot.z; });
    if (PATCH) { const O3 = Object.getPrototypeOf(Object.getPrototypeOf(sc)), umw = O3.updateMatrixWorld; O3.updateMatrixWorld = function (force) { if (this.visible === false) return; umw.call(this, force); }; }
    window.__noRender = false;
    const out = [];
    for (let i = 1; i <= 600; i++) { R.step(1 / 60); if (i % 50 === 0) out.push(ren.domElement.toDataURL('image/png')); }
    return out;
  }, PATCH);
  console.log(file, 'patch', PATCH, frames.map((f) => crypto.createHash('md5').update(f).digest('hex').slice(0, 8)).join(' '), 'len', frames[0].length);
  if (errs.length) console.log('ERR', errs.slice(0, 3));
  await b.close();
})();
