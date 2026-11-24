// c420: 장비 개편 확인 — 수치 줄 · 테이저 장탄 · 촉매제(변이 공격력·체력) · 잔류제 배율 · 현금(맞아도 안 풀림 · 닿아도 안 사라짐 · 수명) · 분노 이동 속도 · 덩치 미는 힘
const { chromium } = require('playwright');
const V = process.argv[2];
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
  await ctx.addInitScript(() => { let s = 4242; Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; let u = 777; globalThis.__uu = () => { u = (u * 1103515245 + 12345) >>> 0; return u / 4294967296; }; window.requestAnimationFrame = () => 0; window.__noRender = true; });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
  const three = require('fs').readFileSync(__dirname + '/../node_modules/three/build/three.module.min.js', 'utf8').split('4294967295*Math.random()').join('4294967295*globalThis.__uu()');
  await p.route('**/three.module.min.js', (r) => r.fulfill({ body: three, contentType: 'application/javascript' }));
  await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 }); await p.waitForTimeout(500);
  const ok = async () => { for (let i = 0; i < 12; i++) { await p.evaluate(() => { document.querySelectorAll('.okBtn').forEach((b) => b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); const c = document.querySelector('#pick .card'); if (c) c.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); window.__rd.step(1 / 60); }); await p.waitForTimeout(300); } };
  await ok();
  const out = {};
  out.lines = await p.evaluate(() => { const R = window.__rd, o = {}; for (const k of ['rage', 'crowbar', 'catalyst', 'linger', 'cash', 'taser']) { if (!R.IT[k]) { o[k] = 'none'; continue; } o[k] = [0, R.LM(k)].map((n) => R.SL(k, n).replace(/<[^>]+>/g, '')).join(' … ') + ' | ' + R.TX[k][0]; } return o; });
  await p.evaluate(() => { const R = window.__rd; for (const k of ['catalyst', 'linger']) if (R.IT[k]) R.own(k, 5); });
  out.after = await p.evaluate(() => { const R = window.__rd, me = R.me; const ally = R.bodies.find((b) => b.kind === 'ally') ; const o = { inv: R.inv(), taserMax: R.IM('taser'), LK: R.LK ? R.LK() : null, CB: R.CB ? R.CB() : null };
    // 촉매제: 동료 하나 만들어 변이
    const c = R.bodies.find((b) => b.kind === 'citizen' && !b.space && b.sleep); if (c) { c.sleep = false; R.zombify(c); const hp0 = c.maxHp, d0 = window.__zd(c); window.__mut(c); o.mut = { type: c.mut, hp0, hp1: c.maxHp, d0: +d0.toFixed(2), d1: +window.__zd(c).toFixed(2), force: c.force }; window.__unmut(c); o.mut.hpBack = c.maxHp; }
    const mh = me.maxHp, md = window.__zd(me); R.awaken(5); o.me = { type: me.mut, hp0: Math.round(mh), hp1: Math.round(me.maxHp), d0: +md.toFixed(2), d1: +window.__zd(me).toFixed(2), force: me.force }; window.__unmut(me); o.me.hpBack = Math.round(me.maxHp);
    return o; });
  console.log(V, JSON.stringify(out, null, 1)); console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
