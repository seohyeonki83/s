const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const v of ['c572', 'c573']) {
const src = fs.readFileSync(__dirname + `/var/${v}.html`, 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 1; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/${v}_sg.html`, src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/${v}_sg.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
console.log(v, await p.evaluate(() => window.__rd.ev(`(() => { chNoMix = true; const x = me.foot.x + 30, z = me.foot.z + 30; const po = addCitizen(x, z, square(x, z), 'police'), sg = addCitizen(x + 1, z, square(x + 1, z), 'police'); chMakeSg(sg); const rb = addCitizen(x + 2, z, square(x + 2, z), 'robot'); chNoMix = false;
  sg.atkT = 0; let iv = null; { const t0 = sg.atkT; }
  // 감전 후 색 복구
  for (const c of [sg, rb]) { c.stunT = 0.01; c.stunShown = true; }
  let col = ''; { const f = () => { for (const c of [sg, rb]) { c.stunT = 0; } }; f(); }
  return JSON.stringify({ sgHP: sg.maxHp.toFixed(1), sgCol: sg.mesh.material.color.getHexString(), poCol: po.mesh.material.color.getHexString(), approach: (sg.sight * (typeof CH_SG_HPK !== 'undefined' ? 0.5 : 0.4)).toFixed(2), poSight: po.sight.toFixed(2), every: (HIT_EVERY * (typeof CH_SG_HPK !== 'undefined' ? 1 / HIT_EVERY : 1.6)).toFixed(2) }); })()`)));
await p.evaluate(() => window.__rd.ev(`(() => { window.__t = []; })()`));
console.log(' 감전 뒤 색', await p.evaluate(() => window.__rd.ev(`(() => { chNoMix = true; const x = me.foot.x + 30, z = me.foot.z + 34; const sg = addCitizen(x, z, square(x, z), 'police'); chMakeSg(sg); const rb = addCitizen(x + 2, z, square(x + 2, z), 'robot'); chNoMix = false; for (const c of [sg, rb]) { c.stunT = 0.05; } for (let i = 0; i < 20; i++) { paused = false; stepWorld(0.02); } return 'sg #' + sg.mesh.material.color.getHexString() + ' 사각 #' + rb.mesh.material.color.getHexString(); })()`)));
console.log(' 샷 한 번', await p.evaluate(() => window.__rd.ev(`(() => { me.hp = me.maxHp = 1e6; chNoMix = true; const out = []; for (const d of [1.0, 2.5, 4.0, 5.0, 5.6]) { const x = me.foot.x + d, z = me.foot.z; const sg = addCitizen(x, z, square(x, z), 'police'); chMakeSg(sg); sg.sleep = true; const hp0 = me.hp; me.kbV = 0; chShotgun(sg, me); const kb = me.kb ? Math.hypot(me.kb.x, me.kb.y || me.kb.z) : (me.knockV || 0); out.push(d + '칸:' + (hp0 - me.hp > 0 ? '맞음' : '빗나감')); sg.kind = 'gone'; scene.remove(sg.mesh); } chNoMix = false; return out.join(' ') + ' | 경찰 사거리 ' + me.sight; })()`)));
await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
