const { chromium } = require('playwright'); const fs = require('fs');
const dif = process.argv[2] || 'h';
const src = fs.readFileSync(__dirname + '/var/c540.html', 'utf8').replace('window.__map = "b";', `window.__map = "m"; window.__stg = 3; window.__dif = "${dif}";`).replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + `/var/c540_3${dif}.html`, src);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n').slice(1, 3).join(' | ')));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + `/var/c540_3${dif}.html`); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(1200);
// 1) 기지 모습
await p.evaluate(() => window.__rd.ev(`me.hp = me.maxHp = 1e8; const T = CH_MAP.typeB; const R = CH_MAP.zones[0]; me.foot.set((R[0] + R[2]) / 2, 0, (R[1] + R[3]) / 2 + 4); me.space = null; for (let i = 0; i < explored.length; i++) explored[i] = 1; for (const B of buildings) if (B.type === 'mbase' || B.type === 'bks') B.everOpen = true; window.__camK = 3.6; for (let i = 0; i < 20; i++) { paused = false; stepWorld(0.02); } me.foot.set((R[0] + R[2]) / 2, 0, (R[1] + R[3]) / 2 + 4); paused = true;`));
await p.waitForTimeout(500); await p.screenshot({ path: 'shot540_base.png' });
console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
