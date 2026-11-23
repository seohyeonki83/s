// c413: 가방을 가진 채 가방을 또 얻으면 [강화] [분해] 두 버튼이 뜨나 (강화할 무기가 있을 때만), 분해를 누르면 무기 강화 창으로 가나
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
await p.goto('file://' + __dirname + '/var/' + process.argv[2] + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 }); await p.waitForTimeout(1500);
const tap = async (sel, txt) => p.evaluate(({ sel, txt }) => { const bs = [...document.querySelectorAll(sel)].filter((x) => !txt || x.textContent.trim() === txt); bs.forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); return bs.length; }, { sel, txt });
const btns = () => p.evaluate(() => { const a = document.getElementById('acq'); return a ? [...a.querySelectorAll('.okBtn')].map((x) => x.textContent.trim()) : null; });
const out = {}; await tap('.okBtn'); await p.waitForTimeout(600);
const give = async (k) => { await p.evaluate((k) => window.__rd.give(k), k); await p.waitForTimeout(2500); };
await give('bag'); out.bag1 = await btns(); await tap('#acq .okBtn', '획득'); await p.waitForTimeout(900);          // 무기 없음: 획득만
await give('bag'); out.bag2_noWeapon = await btns(); await tap('#acq .okBtn', '강화'); await p.waitForTimeout(900);   // 무기 없음: 강화만
await give('bomb'); out.bomb = await btns(); await tap('#acq .okBtn', '획득'); await p.waitForTimeout(900);
await give('bag'); out.bag3_withWeapon = await btns(); out.inv0 = await p.evaluate(() => window.__rd.inv().lv);
await tap('#acq .okBtn', '분해'); await p.waitForTimeout(1500); out.pick = await p.evaluate(() => { const q = document.getElementById('pick'); return q ? q.querySelector('.hd').textContent : null; });
await p.evaluate(() => { const c = document.querySelector('#pick .card'); if (c) c.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); }); await p.waitForTimeout(600); await tap('.okBtn'); await p.waitForTimeout(1500); await tap('.okBtn'); await p.waitForTimeout(800);
out.inv1 = await p.evaluate(() => ({ lv: window.__rd.inv().lv, cap: window.__rd.inv().cap, open: !!document.getElementById('pick') || !!document.getElementById('acq') }));
console.log(JSON.stringify(out)); console.log('errors', JSON.stringify(errs.slice(0, 3))); await b.close(); })();
