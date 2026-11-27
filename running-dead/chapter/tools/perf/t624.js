const { chromium } = require('playwright'); const fs = require('fs');
const stg = +process.argv[2] || 3, dif = process.argv[3] || 'e', seed = process.argv[4];
const src = fs.readFileSync(__dirname + '/var/c539.html', 'utf8').replace('window.__map = "b";', `window.__map = "m"; window.__stg = ${stg}; window.__dif = "${dif}";${seed ? ' window.__seed = ' + seed + ';' : ''}`).replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/c539_${stg}${dif}.html`, src);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(1, 3).join(' | ')));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/c539_${stg}${dif}.html`); 
try { await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); } catch (e) { console.log('not ready', errs); await b.close(); return; }
await p.waitForTimeout(2000);
console.log(JSON.stringify(await p.evaluate(() => window.__rd.ev(`(() => ({ typeB: CH_TYPEB, zones: CH_MAP.zones.map((z) => z.map((v) => Math.round(v))), passes: CH_MAP.passes2.length, passW: CH_MAP.passW, half: CH_BAR_HALF, chB: chB ? { inside: chB.inside.length, yard: chB.yard.length, teams: chB.teams.length, turrets: chB.turrets.length, thr: Math.round(chB.thr), base: [chB.base.x0, chB.base.z0, chB.base.x1, chB.base.z1].map(Math.round), locks: chB.base.locks.length } : null, bks: buildings.filter((B) => B.type === 'bks').length, me: [Math.round(me.foot.x), Math.round(me.foot.z)], startZone: chZoneOf(me.foot.x, me.foot.z), safes: buildings.filter((B) => B.type === 'bks' && B.safe).length }))()`))));
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(1500);
await p.evaluate(() => window.__rd.ev(`for (let i = 0; i < explored.length; i++) explored[i] = 1; mmDirty = true;`));
await p.evaluate(() => document.getElementById('minimap').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); await p.waitForTimeout(800);
await p.screenshot({ path: `shot539_map_${stg}${dif}.png` });
console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
