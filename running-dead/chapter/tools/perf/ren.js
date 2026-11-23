// 그리기 쪽 분해: node perf/ren.js <variant>
const { chromium } = require('playwright');
const file = process.argv[2];
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage();
  const errs = []; p.on('pageerror', (e) => errs.push(e.message));
  await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
  await p.goto('file://' + __dirname + '/../var/' + file + '.html');
  await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 });
  await p.waitForTimeout(1500);
  await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))));
  await p.waitForTimeout(300);
  const shot = async (name) => { await p.evaluate(() => { window.__noRender = false; window.__rd.step(0); }); await p.waitForTimeout(200); return (await p.screenshot()).toString('base64'); };
  const out = await p.evaluate(() => {
    const R = window.__rd, ren = window.__ren, sc = window.__scene, cam = window.__cam;
    window.__noRender = true; for (let i = 0; i < 120; i++) R.step(1 / 60);
    const T = (f, n) => { const t = performance.now(); for (let i = 0; i < n; i++) f(); return +((performance.now() - t) / n).toFixed(3); };
    const r = {};
    r.umw = T(() => sc.updateMatrixWorld(), 60);
    r.render = T(() => ren.render(sc, cam), 60);
    sc.matrixWorldAutoUpdate = false;
    r.renderNoUmw = T(() => ren.render(sc, cam), 60);
    sc.matrixWorldAutoUpdate = true;
    // 종류별 객체 수
    const kinds = {}; let top = sc.children.length;
    sc.traverse((o) => { const k = o.type + (o.visible ? '' : ':hidden'); kinds[k] = (kinds[k] || 0) + 1; });
    r.top = top; r.kinds = kinds;
    // 보이는 최상위 객체 중 무엇이 많은지 (재질 색/기하 종류로 대충)
    const geoN = {}; for (const o of sc.children) { if (!o.visible) continue; const g = o.geometry ? o.geometry.type + (o.geometry.parameters ? ':' + Object.values(o.geometry.parameters).slice(0, 2).map((v) => typeof v === 'number' ? v.toFixed(1) : '').join('x') : '') : o.type; geoN[g] = (geoN[g] || 0) + 1; }
    r.visTop = Object.entries(geoN).sort((a, b) => b[1] - a[1]).slice(0, 14);
    return r;
  });
  console.log(JSON.stringify(out));
  // 안 보이는 객체의 행렬 갱신을 건너뛰는 패치
  const out2 = await p.evaluate(() => {
    const R = window.__rd, ren = window.__ren, sc = window.__scene, cam = window.__cam;
    const O3 = Object.getPrototypeOf(Object.getPrototypeOf(sc)), umw = O3.updateMatrixWorld;
    window.__umw0 = umw; window.__O3 = O3;
    const T = (f, n) => { const t = performance.now(); for (let i = 0; i < n; i++) f(); return +((performance.now() - t) / n).toFixed(3); };
    const before = { calls: 0, tris: 0 }; ren.render(sc, cam); before.calls = window.__ri.render.calls; before.tris = window.__ri.render.triangles;
    O3.updateMatrixWorld = function (force) { if (this.visible === false) return; umw.call(this, force); };
    const r = { umwSkip: T(() => sc.updateMatrixWorld(), 60), renderSkip: T(() => ren.render(sc, cam), 60) };
    ren.render(sc, cam); r.before = before; r.after = { calls: window.__ri.render.calls, tris: window.__ri.render.triangles };
    return r;
  });
  console.log(JSON.stringify(out2));
  if (errs.length) console.log('ERR', errs.slice(0, 5));
  await b.close();
})();
