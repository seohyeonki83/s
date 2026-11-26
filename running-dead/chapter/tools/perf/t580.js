const { chromium } = require('playwright'); const fs = require('fs');
const src = fs.readFileSync(__dirname + '/var/c505.html', 'utf8').replace('<script>window.__map = "b";</script>\n', '').replace('window.__rd = { get me() { return me; },', 'window.__rd = { ev: (s) => eval(s), get me() { return me; },');
fs.writeFileSync(__dirname + '/var/c505_boot.html', src);
const U = 'file://' + __dirname + '/var/c505_boot.html';
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 }); const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
await p.route('**/three.module.min.js', (r) => r.fulfill({ path: __dirname + '/../node_modules/three/build/three.module.min.js', contentType: 'application/javascript' }));
const ready = () => p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 60000 });
// 1) 처음 — 저장 없음 + 옛 rd_genes 40
await p.goto(U); await p.evaluate(() => { localStorage.clear(); localStorage.setItem('rd_genes', '40'); }); await p.reload(); await ready(); await p.waitForTimeout(1000);
console.log('first', JSON.stringify(await p.evaluate(() => window.__rd.ev('({pick: CH_PICK, tut: CH_TUT, run: CH_RUN, sv: CH_SV})'))));
// 튜토리얼 끝 흉내
await p.evaluate(() => window.__rd.ev(`document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); chTutGate.dead = true; me.foot.z = chTutGateZ - 2;`)); await p.waitForTimeout(4000);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(2500);
console.log('tutres', JSON.stringify(await p.evaluate(() => { const o = document.getElementById('rres'); return o && o.innerText.replace(/\n/g, ' | '); })));
await p.screenshot({ path: 'shot505_tutres.png' });
await Promise.all([p.waitForNavigation(), p.evaluate(() => document.querySelector('#rres button').click())]);
await p.waitForSelector('#outg'); await p.waitForTimeout(500);
await p.screenshot({ path: 'shot505_out.png' });
// 성장 1포인트
await p.evaluate(() => document.querySelector('#outg button[data-up="atk"]').click()); await p.waitForTimeout(200);
console.log('after up', await p.evaluate(() => localStorage.getItem('rd_save_v1')));
console.log('locks', JSON.stringify(await p.evaluate(() => [...document.querySelectorAll('#outg button[data-st]')].map((x) => x.dataset.st + x.dataset.d + (x.disabled ? 'L' : 'O')))));
await p.evaluate(() => document.querySelector('#outg button[data-st="1"][data-d="e"]').click()); await ready(); await p.waitForTimeout(1500);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(1500);
console.log('run', JSON.stringify(await p.evaluate(() => window.__rd.ev('({pick: CH_PICK, run: CH_RUN, stg: CH_STG, dif: CH_DIF, sk: CH_SK, mix: CH_MIXL, upk: CH_UPK, ver: document.getElementById("ver") && document.getElementById("ver").textContent, myMax: me.maxHp, MY_HP})'))));
await p.evaluate(() => window.__rd.ev('deaths = 200; chSf.on = true; stepWorld(0.05);')); await p.waitForTimeout(3000);
await p.evaluate(() => document.querySelectorAll('.okBtn').forEach((x) => x.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })))); await p.waitForTimeout(1500);
await p.screenshot({ path: 'shot505_hud.png' });
await p.evaluate(() => document.getElementById('stars').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }))); await p.waitForTimeout(500);
await p.screenshot({ path: 'shot505_panel.png' });
console.log('errors', JSON.stringify(errs.slice(0, 4))); await b.close(); })();
