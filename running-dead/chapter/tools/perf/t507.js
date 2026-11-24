const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c429z.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
const r = await p.evaluate(() => { const R = window.__rd, o = []; for (const br of [null, 'dia', 'gold']) { if (br) R.BR.cash = br; else delete R.BR.cash; const row = []; for (let n = 0; n <= (br ? 12 : 6); n++) { R.setLv('cash', n); row.push(n + ':' + (R.CK() * 7.2).toFixed(1) + '칸(' + (R.CK() / 1.2).toFixed(2) + ')'); } o.push((br || 'cash') + ' ' + row.join(' ')); if (br) o.push('  ' + R.SL('cash', 7) + ' | ' + R.SL('cash', 12)); } return o; });
console.log(r.join('\n')); console.log('errors', JSON.stringify(errs)); await b.close(); })();
