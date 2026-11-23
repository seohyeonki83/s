// 두 버전의 화면이 픽셀까지 같은지 — 난수·시간을 고정하고 손으로 걸음을 돌려 프레임 해시를 뽑는다
// node perf/pix2.js <var/ 아래 파일 이름> <stand|walk> [동료 수] [걸음 수]
const { chromium } = require('playwright'); const crypto = require('crypto');
const file = process.argv[2], SC = process.argv[3] || 'stand', NA = +(process.argv[4] || 40), N = +(process.argv[5] || 600);
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
  await ctx.addInitScript((SECOFF) => { let s = 12345; Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; { let u = 777; globalThis.__uu = () => { u = (u * 1103515245 + 12345) >>> 0; return u / 4294967296; }; } window.__secOff = SECOFF; window.requestAnimationFrame = () => 0; let t = 1000; performance.now = () => (t += 0.01); Date.now = () => 1700000000000; }, process.argv[6] === 'off');
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 2).join(' | ')));
  const three = require('fs').readFileSync(__dirname + '/../../node_modules/three/build/three.module.min.js', 'utf8').split('4294967295*Math.random()').join('4294967295*globalThis.__uu()');   // three.js가 물체 이름표(UUID)를 만들 때 게임 난수를 쓰지 않게 — 그림 물체 수가 달라도 게임 난수 순서는 같다
  await p.route('**/three.module.min.js', (r) => r.fulfill({ body: three, contentType: 'application/javascript' }));
  await p.goto('file://' + __dirname + '/../var/' + file + '.html');
  await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 });
  await p.waitForTimeout(800);
  const res = await p.evaluate(({ SC, NA, N }) => {
    const R = window.__rd, me = R.me, bodies = R.bodies, cv = document.getElementById('view');
    document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })));
    me.hp = me.maxHp = 100000;
    const far = bodies.filter((c) => c.kind === 'citizen' && c.sleep && !c.space && Math.hypot(c.foot.x - me.foot.x, c.foot.z - me.foot.z) > 40).slice(0, NA);
    far.forEach((h, i) => { const a = i * 2.399, r = 1.2 + 0.45 * Math.sqrt(i) * 1.6; h.sleep = false; h.met = true; h.space = null; R.zombify(h); h.foot.x = me.foot.x + Math.cos(a) * r; h.foot.z = me.foot.z + Math.sin(a) * r; h.px = h.foot.x; h.pz = h.foot.z; });
    window.__noRender = false;
    const Z = R.ch.zones, zc = Z.map((q) => [(q[0] + q[2]) / 2, (q[1] + q[3]) / 2]);
    let ti = 0; const out = [], st = [];
    for (let i = 1; i <= N; i++) {
      if (SC === 'walk') {   // 구역 가운데들을 차례로 찾아간다 (걸음마다 0.07칸 = 초당 4.2칸) — 벽·강은 무시하고 곧장
        const [tx, tz] = zc[ti % zc.length], dx = tx - me.foot.x, dz = tz - me.foot.z, d = Math.hypot(dx, dz);
        if (d < 1) ti++; else { me.foot.x += dx / d * 0.07; me.foot.z += dz / d * 0.07; }
      }
      window.__noRender = i % 50 !== 0;   // 찍는 프레임만 그린다 (그리기는 게임 상태를 안 바꾼다)
      R.step(1 / 60);
      if (i % 50 === 0) { out.push(cv.toDataURL('image/png')); st.push([bodies.length, bodies.filter((c) => c.kind === 'ally').length, +me.foot.x.toFixed(3), +me.foot.z.toFixed(3)].join(',')); }
    }
    return { out, st };
  }, { SC, NA, N });
  console.log(file, SC, res.out.map((f) => crypto.createHash('md5').update(f).digest('hex').slice(0, 6)).join(' '));
  console.log('   ', res.st.filter((_, i) => i % 3 === 2).join(' | '));
  if (errs.length) console.log('ERR', errs.slice(0, 3));
  await b.close();
})();
