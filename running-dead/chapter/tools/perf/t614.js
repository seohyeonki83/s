const { chromium } = require('playwright'); const fs = require('fs');
const src = fs.readFileSync(__dirname + '/var/c532.html', 'utf8').replace('<script>window.__map = "b";</script>\n', '');
fs.writeFileSync(__dirname + '/var/c532_boot.html', src);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const errs = [];
for (const [tag, save, nm] of [['s1', { genes: 900, clr: { '1e': 1 }, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tut: true, mig: 1, v2: 1, v3: 1 }, 'rd-anim:1:e'], ['tut', { genes: 500, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tut: true, mig: 1, v2: 1, v3: 1 }, 'rd-anim:t']]) {
const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 })).newPage(); p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c532_boot.html'); await p.evaluate(([s, n]) => { localStorage.clear(); localStorage.setItem('rd_save_v1', JSON.stringify(s)); window.name = n; }, [save, nm]); await p.reload();
await p.waitForSelector('#outg'); const t0 = Date.now(); const blk = [];
for (let k = 0; k < 16; k++) { await p.screenshot({ path: `shot532_${tag}_${k}.png` }); blk.push(await p.evaluate(() => !!document.querySelector('#outg .blk'))); await p.waitForTimeout(330); }
console.log(tag, 'blocker', blk.map((x) => x ? 1 : 0).join(''), 'ms', Date.now() - t0, 'cbs', await p.evaluate(() => [...document.querySelectorAll('#outg .cb')].map((c) => c.dataset.cb + (c.classList.contains('on') ? '✓' : '')).join(' ')));
await p.close(); }
console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
