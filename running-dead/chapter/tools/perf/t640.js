const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage();
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c548_boot.html'); await p.evaluate(() => { localStorage.setItem('rd_save_v1', JSON.stringify({ genes: 0, clr: {}, sub: {}, up: { hp: 0, ahp: 0, atk: 0 }, tut: true, mig: 1, v2: 1, v3: 1, v4: 1 })); }); await p.reload(); await p.waitForSelector('#outg'); await p.click('#outg .nd[data-st="1"]'); await p.waitForTimeout(300);
await p.evaluate(() => { window.__paints = 0; const f = () => { window.__paints++; if (window.__paints < 400) requestAnimationFrame(f); }; new MutationObserver(() => { if (document.getElementById('ldx') && !window.__ldxT) { window.__ldxT = performance.now(); window.__p0 = window.__paints; } }).observe(document.body, { childList: true }); requestAnimationFrame(f); });
await p.click('#outg .go'); await p.waitForFunction(() => window.__rdReady, null, { timeout: 60000 });
console.log(await p.evaluate(() => 'frames drawn while loading screen up (before map work blocks): ' + (window.__paints - window.__p0)));
await b.close(); })();
