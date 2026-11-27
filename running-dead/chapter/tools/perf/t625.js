const { chromium } = require('playwright'); const fs = require('fs');
const dif = process.argv[2] || 'h';
const src = fs.readFileSync(__dirname + '/var/c539.html', 'utf8').replace('window.__map = "b";', `window.__map = "m"; window.__stg = 3; window.__dif = "${dif}";`).replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/c539_3${dif}.html`, src);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(1, 3).join(' | ')));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/c539_3${dif}.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(1200);
// 1) 기지 모습
await p.evaluate(() => window.__rd.ev(`me.hp = me.maxHp = 1e8; const T = CH_MAP.typeB; me.foot.set(T.bx, 0, T.yz + 7); me.space = null; for (let i = 0; i < explored.length; i++) explored[i] = 1; for (const B of buildings) if (B.type === 'mbase' || B.type === 'bks') B.everOpen = true; window.__camK = 2.2; for (let i = 0; i < 20; i++) { paused = false; stepWorld(0.02); } me.foot.set(T.bx, 0, T.yz + 7); paused = true;`));
await p.waitForTimeout(500); await p.screenshot({ path: 'shot539_base.png' });
// 2) 출동 · 주기 팀 · 점령 · 클리어
console.log(JSON.stringify(await p.evaluate(() => window.__rd.ev(`(() => { const out = {}; paused = false; window.__camK = 1; const T = CH_MAP.typeB;
  me.foot.set(T.bx, 0, T.yz + 12); me.space = null;
  const y0 = chB.yard.length; const u = chB.yard[0]; u.hp -= chB.thr * 1.2; stepWorld(0.05); out.dispatch1 = chB.yard.length - y0;
  const u2 = chB.yard[1]; u2.hp -= chB.thr * 1.2; stepWorld(0.05); out.dispatchDuringCd = chB.yard.length - y0;
  for (let i = 0; i < 50; i++) stepWorld(0.05); const u3 = chB.yard[2]; u3.hp -= chB.thr * 1.2; stepWorld(0.05); out.dispatch2 = chB.yard.length - y0;
  // 주기 팀: 북쪽에 내가 있으니 북쪽 숨은 자리에서
  chAL = 1; const w0 = bodies.filter((b) => b.bWave).length; chB.waveT = 100; stepWorld(0.05); const W1 = bodies.filter((b) => b.bWave); out.waveN = W1.length - w0; out.waveInNorth = W1.slice(w0).every((c) => chB.inN(c.foot.x, c.foot.z));
  // 내가 남쪽 멀리 → 검문소 앞
  const P = CH_MAP.passes2[0]; me.foot.set(T.bx + 5, 0, CH_MAP.zones[2][3] - 6); for (const z of zombies) if (z !== me) z.foot.set(me.foot.x, 0, me.foot.z + 1);
  chB.waveT = 100; stepWorld(0.05); const W2 = bodies.filter((b) => b.bWave).slice(W1.length); out.wave2N = W2.length; out.wave2Front = W2.length ? [Math.round(W2[0].foot.x - P.c), Math.round(W2[0].foot.z - Math.max(P.az, P.bz))] : null;
  // 검문소 점령 — 터렛 · 수비대 없애기
  for (const t of chB.turrets) makeZombie(t); for (const c of chB.X.units) if (c.kind === 'citizen') makeZombie(c); stepWorld(0.05); stepWorld(0.05); out.chkCap = chB.chkCap; out.mis0 = chMis[0].done; out.runT = Math.round(chRunT);
  // 기지 들어가기 → 출동 멈춤
  const z1 = zombies.find((z) => z !== me) || me; z1.space = chB.base; stepWorld(0.05); out.entered = chB.entered; const y1 = chB.yard.length; chB.yard[0] && (chB.yard[0].hp -= chB.thr * 3); for (let i = 0; i < 60; i++) stepWorld(0.05); out.dispatchAfterEnter = chB.yard.length - y1 + (chB.yard.length < y1 ? 'died' : '');
  out.boss = chB.inside.some((c) => c.bBoss); out.bossHp = Math.round((chB.inside.find((c) => c.bBoss) || {}).maxHp || 0);
  out.objText = chObjText();
  for (const c of chB.inside) if (c.kind === 'citizen') makeZombie(c); stepWorld(0.05); out.won = chSf.won; out.mis1 = chMis[1].done;
  return out; })()`))));
await p.waitForTimeout(3000); console.log(JSON.stringify(await p.evaluate(() => window.__rd.ev('({paused, acqOpen, lvOpen, tutOpen, squadAnim, starAnim, rankAnim, menuOv: !!menuOv, victoryOn, goal: goalShown, fxq: fxQueue.length, tq: tutQueue.length, over: chRunOver, won: chSf.won})'))));
console.log('result', JSON.stringify(await p.evaluate(() => { const o = document.getElementById('rres'); return o ? o.innerText.replace(/\n/g, ' | ') : null; })));
console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
