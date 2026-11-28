const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
const src = fs.readFileSync(__dirname + '/var/c596.html', 'utf8').replace('window.__map = "b";', 'window.__map = "m"; window.__stg = 2; window.__dif = "e";').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + '/var/c596_obj.html', src);
const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
const url = 'file://' + __dirname + '/var/c596_obj.html';
await p.goto(url); await p.evaluate(() => localStorage.setItem('rd_save_v1', JSON.stringify({ genes: 0, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tr: { mut: 20 }, tut: true, mig: 1, v2: 1, v3: 1, v4: 1, u2: 1, u3: 1 })));
await p.goto(url); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
console.log(await p.evaluate(() => window.__rd.ev(`(() => { const out = [];
  chNoMix = true; const al = addCitizen(me.foot.x + 1, me.foot.z, square(me.foot.x + 1, me.foot.z), ''); chNoMix = false; makeZombie(al); mutate(al, 'armor'); if (!zombies.includes(al)) zombies.push(al);
  const near = (o) => { const c = o.foot || (o.car ? { x: o.car.x, z: o.car.z } : o.L ? { x: o.L.cx, z: o.L.cz } : null); if (!c) return false; for (let r = 0.3; r < 4; r += 0.05) for (let a = 0; a < 6.28; a += 0.4) { al.foot.set(c.x + Math.cos(a) * r, 0, c.z + Math.sin(a) * r); al.space = o.space || null; if (objGap(o, al) <= al.r + 0.1 && objGap(o, al) > 0.02) return true; } return false; };
  const kinds = {}; for (const o of [...objs, ...chWallObjs.filter((w) => Math.hypot(w.foot.x - me.foot.x, w.foot.z - me.foot.z) < 40)]) { const t = o.type + (o.car ? (o.car.barr ? '-바리' : '-차') : ''); if (kinds[t] || o.dead || !(o.hp > 0)) continue; if (!near(o)) continue; const h0 = o.hp; for (let i = 0; i < 4; i++) { al.spkT = 0; chSpikeTick(0.5); } kinds[t] = (h0 - o.hp).toFixed(2) + '/' + h0.toFixed(0); }
  const sf = bodies.find((o) => o.kind === 'safe' && o.hp > 0 && !o.dead); if (sf) { al.space = sf.space; al.foot.set(sf.foot.x + (sf.r || BODY) + al.r, 0, sf.foot.z); const h0 = sf.hp; for (let i = 0; i < 4; i++) { al.spkT = 0; chSpikeTick(0.5); } kinds['금고·가구'] = (h0 - sf.hp).toFixed(2) + '/' + h0.toFixed(0); }
  return 'CH_SK ' + CH_SK + ' · 피해(4번) ' + JSON.stringify(kinds); })()`)));
console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
