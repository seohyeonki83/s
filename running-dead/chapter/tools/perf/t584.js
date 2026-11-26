const { chromium } = require('playwright'); const fs = require('fs');
const src = fs.readFileSync(__dirname + '/var/c508.html', 'utf8').replace('<script>window.__map = "b";</script>\n', '').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + '/var/c508_boot.html', src);
const U = 'file://' + __dirname + '/var/c508_boot.html';
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 }); const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
const ready = () => p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
// 1) 처음 — 저장 없음 + 옛 rd_genes 40
await p.goto(U); await p.evaluate(() => { localStorage.clear(); localStorage.setItem('rd_genes', '4000'); localStorage.setItem('rd_save_v1', JSON.stringify({genes: 5000, clr: {}, sub: {}, up: {hp: 0, ahp: 0, atk: 0}, tut: true, mig: 1})); }); await p.reload(); await ready(); await p.waitForTimeout(1000);
console.log('first', JSON.stringify(await p.evaluate(() => window.__rd.ev('({pick: CH_PICK, tut: CH_TUT, run: CH_RUN, sv: CH_SV, hud: document.getElementById("gene").innerText})'))));
// 튜토리얼 끝 흉내
await p.evaluate(() => window.__rd.ev(`document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); chTutGate.dead = true; me.foot.z = chTutGateZ - 2;`)); await p.waitForTimeout(4000);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(2500);
console.log('tutres', JSON.stringify(await p.evaluate(() => { const o = document.getElementById('rres'); return o && o.innerText.replace(/\n/g, ' | '); })));
await p.screenshot({ path: 'shot505_tutres.png' });
await Promise.all([p.waitForNavigation(), p.evaluate(() => document.querySelector('#rres button').click())]);
await p.waitForSelector('#outg'); await p.waitForTimeout(500);
await p.screenshot({ path: 'shot505_out.png' });
await p.evaluate(() => { const b = document.querySelector('#outg button[data-rst]'); b.scrollIntoView(); b.click(); }); await p.waitForTimeout(300);
await p.screenshot({ path: 'shot507_rst.png' });
console.log('before', await p.evaluate(() => localStorage.getItem('rd_save_v1')));
await Promise.all([p.waitForNavigation(), p.evaluate(() => document.querySelector('#outg button[data-rst]').click())]); await ready(); await p.waitForTimeout(800);
console.log('after', JSON.stringify(await p.evaluate(() => window.__rd.ev('({pick: CH_PICK, sv: CH_SV, old: localStorage.getItem("rd_genes")})'))));
console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
