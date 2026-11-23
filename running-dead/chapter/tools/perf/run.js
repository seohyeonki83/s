// 측정: node perf/run.js <variant file under var/> <scenario: idle|army> [allies]
const { chromium } = require('playwright');
const file = process.argv[2], SC = process.argv[3] || 'idle', NA = +(process.argv[4] || 60);
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } }); await ctx.addInitScript(() => { window.__secOff = true; });   // 동료를 만들 때까지는 재우기를 꺼 둔다
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(0, 3).join(' | ')));
  await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
  const t0 = Date.now();
  await p.goto('file://' + __dirname + '/../var/' + file + '.html');
  await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 });
  const loadMs = Date.now() - t0;
  await p.waitForTimeout(1500);
  await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))));
  await p.waitForTimeout(500);
  const out = await p.evaluate(({ SC, NA }) => {
    const R = window.__rd, me = R.me, bodies = R.bodies;
    me.hp = me.maxHp = 100000;
    if (SC === 'army') {
      const far = bodies.filter((c) => c.kind === 'citizen' && c.sleep && !c.space && Math.hypot(c.foot.x - me.foot.x, c.foot.z - me.foot.z) > 40).slice(0, NA);
      far.forEach((h, i) => { const a = i * 2.399, r = 1.2 + 0.45 * Math.sqrt(i) * 1.6; h.sleep = false; h.met = true; h.space = null; R.zombify(h); h.foot.x = me.foot.x + Math.cos(a) * r; h.foot.z = me.foot.z + Math.sin(a) * r; h.px = h.foot.x; h.pz = h.foot.z; });
    }
    window.__secOff = false;
    window.__noRender = true;
    for (let i = 0; i < 180; i++) R.step(1 / 60);          // 데우기 (3초)
    const run = (n) => { for (const k in window.__ph) delete window.__ph[k]; for (const k in window.__pd) delete window.__pd[k]; const t = performance.now(); for (let i = 0; i < n; i++) R.step(1 / 60); const tot = (performance.now() - t) / n; const ph = {}, pd = {}; for (const k in window.__ph) ph[k] = +(window.__ph[k] / n).toFixed(4); for (const k in window.__pd) pd[k] = +(window.__pd[k] / n).toFixed(4); return { tot: +tot.toFixed(3), ph, pd }; };
    const logic = run(600);
    // 그리기 (작은 화면 = CPU 쪽 비용에 가깝다)
    const ren = window.__ren, sc = window.__scene, cam = window.__cam;
    window.__noRender = false;
    const info = () => ({ calls: window.__ri.render.calls, tris: window.__ri.render.triangles, geos: window.__ri.memory.geometries, tex: window.__ri.memory.textures });
    R.step(1 / 60); const inf = info();
    const full = run(40);
    const cv = ren.domElement, w0 = cv.width, h0 = cv.height;
    ren.setSize(39, 84, false);
    const tiny = run(120);
    ren.setSize(w0, h0, false);
    // 장면 객체 수
    let all = 0, meshes = 0, vis = 0, auto = 0;
    sc.traverse((o) => { all++; if (o.isMesh || o.isSprite || o.isLine) meshes++; if (o.matrixAutoUpdate) auto++; });
    const walk = (o) => { if (!o.visible) return; vis++; for (const c of o.children) walk(c); }; walk(sc);
    const secs = window.__secs ? window.__secs() : null;
    const cnt = { bodies: bodies.length, citizen: 0, asleep: 0, awake: 0, ally: 0, out: 0, fixed: 0, other: 0 };
    for (const c of bodies) { if (c.kind === 'citizen') { cnt.citizen++; if (c.sleep) cnt.asleep++; else cnt.awake++; } else if (c.kind === 'ally') cnt.ally++; else cnt.other++; if (c.out) cnt.out++; if (c.fixed) cnt.fixed++; }
    const kinds = {}; for (const c of bodies) { const k = c.kind + (c.out ? ':out' : '') + (c.prop ? ':prop' : '') + (c.fixed ? ':fixed' : ''); kinds[k] = (kinds[k] || 0) + 1; }
    return { secs, cnt, kinds, buildings: R.buildings.length, zones: R.ch.zones.length, mm: R.ch.mm, scene: { all, meshes, vis, auto }, info: inf, canvas: [w0, h0], logic, renderFull: full.ph['28 화면그리기(render)'], renderTiny: tiny.ph['28 화면그리기(render)'] };
  }, { SC, NA });
  console.log(JSON.stringify({ file, SC, loadMs, ...out }, null, 1));
  if (errs.length) console.log('ERR', errs.slice(0, 5));
  await b.close();
})();
