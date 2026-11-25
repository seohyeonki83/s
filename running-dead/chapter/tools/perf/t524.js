// c449: 변이 동료 획득 — 카메라 이동 · 비춤 · 획득창 · 확인 후 복귀
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message + ' ' + (e.stack || '').split('\n')[1]));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/c449z.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
const tap = (txt) => p.evaluate((txt) => { const bs = [...document.querySelectorAll('.okBtn')].filter((x) => !txt || x.textContent.trim() === txt); bs.forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); return bs.length; }, txt);
await tap(); await p.waitForTimeout(500);
await p.evaluate(() => { const R = window.__rd, me = R.me; const c = R.bodies.find((x) => x.kind === "citizen" && !x.space && !x.police); c.foot.x = me.foot.x + 6; c.foot.z = me.foot.z - 4; c.space = null; c.sleep = false; R.zombify(c); c.boss = 'armor'; R.BT(c); });
const tl = []; for (let i = 0; i < 8; i++) { await p.waitForTimeout(250); tl.push(await p.evaluate(() => [window.__rd.CO().join(','), !!document.getElementById('acq')].join(' '))); if (i === 3) await p.screenshot({ path: __dirname + '/perf/c449_pan.png' }); }
await p.screenshot({ path: __dirname + '/perf/c449_acq.png' });
await tap('확인'); await p.waitForTimeout(1500); tl.push('after ' + await p.evaluate(() => [window.__rd.CO().join(','), !!document.getElementById('acq')].join(' ')));
console.log(tl.join(' | ')); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
