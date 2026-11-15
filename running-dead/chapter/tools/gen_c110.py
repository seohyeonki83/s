# c110: 주유소 지붕 없앰 · 시작 자리 가까이에 하양 1~2명 (가는 길에 먼저 만난다)
import pprint
S = open('c109.mjs', encoding='utf8').read(); R = []
def rep(a, b, n=1):
    assert S.count(a) == n, (S.count(a), n, a[:90]); R.append((a, b, n) if n != 1 else (a, b))
rep("  function chCanopyDraw(eyes) {                // 주유소 지붕 — 좀비가 밑(이나 바로 옆 1.2칸)에 있으면 사라진다\n",
    "  function chCanopyDraw(eyes) {                // 주유소 지붕 — 좀비가 밑(이나 바로 옆 1.2칸)에 있으면 사라진다\n    if (CHAPTER) { for (const C of chCanopies) { C.open = true; C.m.visible = false; } return; }   // c110: 지붕을 아예 없앤다 (늘 열린 것으로 — 밑에 있는 것도 그대로 보인다)\n")
rep("chDecoPlace(); chTrReset(); return; }", "chDecoPlace(); chStartWhites(); chTrReset(); return; }")
rep("  function showDud() {", r'''  function chStartWhites() {                   // c110: 시작 자리에서 구역 안쪽으로 가는 길에 하양 1~2명 — 시작하자마자 먼저 만난다 (6~9칸 앞, 벽에 안 가린 빈자리)
    const zi = chZoneOf(me.foot.x, me.foot.z), Z = CH_MAP.zones[Math.max(0, zi)], a0 = Math.atan2((Z[1] + Z[3]) / 2 - me.foot.z, (Z[0] + Z[2]) / 2 - me.foot.x), n = 1 + Math.floor(Math.random() * 2);
    const put = [];
    for (let k = 0; k < n; k++) for (let t = 0; t < 60; t++) {
      const a = a0 + rand(-1, 1) * (0.35 + t * 0.03), d = rand(6, 9), x = me.foot.x + Math.cos(a) * d, z = me.foot.z + Math.sin(a) * d;
      if (spaceOf(x, z) || !freeSpot(x, z, null) || chNearRiver(x, z, 0.8) || blocked(me.foot.x, me.foot.z, x, z) || chZoneOf(x, z) !== zi) continue;
      if (put.some((q) => Math.hypot(q[0] - x, q[1] - z) < 1.6) || cars.some((c) => Math.abs(c.x - x) < 1.8 && Math.abs(c.z - z) < 1.8)) continue;
      chExact = true; const c = chPut(x, z, { x0: x - 1.5, z0: z - 1.5, x1: x + 1.5, z1: z + 1.5 }, '', null); chExact = false; c.startW = true; put.push([x, z]); break;
    }
  }
  function showDud() {''')
open('c110_patch.py', 'w', encoding='utf8').write('# c110: 주유소 지붕 없앰 · 시작 자리 가까이 하양 1~2명 (gen_c110.py가 만든다)\nC110_R = ' + pprint.pformat(R, width=100000) + '\n')
print('replacements', len(R))
