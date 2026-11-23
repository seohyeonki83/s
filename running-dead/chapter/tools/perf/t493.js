// 극초반 난이도 재료: 시작 자리 둘레(30칸 · 내 단락)에 누가 얼마나 있나 — 큰 맵과 본 맵을 씨앗 여러 개로
const { chromium } = require('playwright');
const V = process.argv[2], N = +(process.argv[3] || 8);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const rows = [];
for (let seed = 1; seed <= N; seed++) {
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
  await ctx.addInitScript((sd) => { let s = sd * 7919 + 13; Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; let u = 777; globalThis.__uu = () => { u = (u * 1103515245 + 12345) >>> 0; return u / 4294967296; }; window.requestAnimationFrame = () => 0; window.__seed = sd * 101 + 7; window.__secOff = true; window.__noReload = true; }, seed);
  const p = await ctx.newPage(); const three = require('fs').readFileSync(__dirname + '/../node_modules/three/build/three.module.min.js', 'utf8').split('4294967295*Math.random()').join('4294967295*globalThis.__uu()');
  await p.route('**/three.module.min.js', (r) => r.fulfill({ body: three, contentType: 'application/javascript' }));
  await p.goto('file://' + __dirname + '/var/' + V + '.html'); await p.waitForFunction(() => window.__rdReady && window.__rd && window.__rd.me, null, { timeout: 120000 });
  rows.push(await p.evaluate(() => { const R = window.__rd, me = R.me, Z = R.ch.zones; const zi = Z.findIndex((q) => me.foot.x >= q[0] && me.foot.x <= q[2] && me.foot.z >= q[1] && me.foot.z <= q[3]), q = Z[zi];
    const kind = (c) => c.police ? 'police' : c.vig ? 'red' : c.attacker ? 'orange' : c.guard ? 'yellow' : 'white';
    const cs = R.bodies.filter((c) => c.kind === 'citizen'), near = { white: 0, yellow: 0, orange: 0, red: 0, police: 0 }, zone = { white: 0, yellow: 0, orange: 0, red: 0, police: 0 };
    for (const c of cs) { const k = kind(c), out = !c.space; if (out && Math.hypot(c.foot.x - me.foot.x, c.foot.z - me.foot.z) < 30) near[k]++; if (out && c.foot.x >= q[0] && c.foot.x <= q[2] && c.foot.z >= q[1] && c.foot.z <= q[3]) zone[k]++; }
    return { big: q[3] - q[1] > 60 || q[2] - q[0] > 60, area: Math.round((q[2] - q[0]) * (q[3] - q[1])), near, zone }; }));
  await ctx.close();
}
const f = (a) => { const m = a.reduce((x, y) => x + y, 0) / a.length; return m.toFixed(1) + ' (' + Math.min(...a) + '~' + Math.max(...a) + ')'; };
console.log('==', V, N, 'seeds');
console.log(' 시작 30칸 안 길거리: 쉬운 적(하양+노랑)', f(rows.map((r) => r.near.white + r.near.yellow)), ' 센 적(주황+빨강+경찰)', f(rows.map((r) => r.near.orange + r.near.red + r.near.police)));
console.log(' 내 단락 길거리, 넓이 1000칸당: 쉬운 적', f(rows.map((r) => +(((r.zone.white + r.zone.yellow) / r.area) * 1000).toFixed(1))), ' 센 적', f(rows.map((r) => +(((r.zone.orange + r.zone.red + r.zone.police) / r.area) * 1000).toFixed(1))));
console.log(' 씨앗별 [쉬운, 센] (30칸 안):', rows.map((r) => '[' + (r.near.white + r.near.yellow) + ',' + (r.near.orange + r.near.red + r.near.police) + ']').join(' '));
await b.close(); })();
