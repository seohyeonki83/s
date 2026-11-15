# c113: 시작 하양 1~2명 — 시작하자마자가 아니라, 내가 조금(2.5칸) 움직인 뒤에 내가 가는 방향 앞쪽(시야 바로 밖)에 나타난다
import pprint
S = open('c112.mjs', encoding='utf8').read(); R = []
def rep(a, b, n=1):
    assert S.count(a) == n, (S.count(a), n, a[:90]); R.append((a, b, n) if n != 1 else (a, b))
rep("chDecoPlace(); chStartWhites(); chTrReset(); return; }", "chDecoPlace(); chStartW = { x: me.foot.x, z: me.foot.z, n: 1 + Math.floor(Math.random() * 2), tries: 0 }; chTrReset(); return; }")
rep("    if (CHAPTER) chRespawnTick(dt);", "    if (CHAPTER) { chRespawnTick(dt); if (chStartW) chStartTick(); }")
rep("  function showDud() {", r'''  let chStartW = null;                        // c113: 아직 안 나타난 시작 하양 { 시작 자리, 몇 명 }
  function chStartTick() {                     // 내가 시작 자리에서 2.5칸 넘게 움직이면 — 그 방향 앞쪽, 시야(7.2칸) 바로 밖 8~9.5칸에 하양 1~2명을 세운다 (벽에 안 가린 빈자리. 못 찾으면 다음 걸음에 다시)
    const W = chStartW; if (!isZombie(me)) { chStartW = null; return; }
    const dx = me.foot.x - W.x, dz = me.foot.z - W.z, d = Math.hypot(dx, dz); if (d < 2.5 || me.space) return;
    const a0 = Math.atan2(dz, dx), zi = chZoneOf(me.foot.x, me.foot.z), put = [];
    for (let k = 0; k < W.n; k++) for (let t = 0; t < 40; t++) {
      const a = a0 + rand(-1, 1) * (0.3 + t * 0.03 + W.tries * 0.05), r = rand(8, 9.5), x = me.foot.x + Math.cos(a) * r, z = me.foot.z + Math.sin(a) * r;
      if (spaceOf(x, z) || !freeSpot(x, z, null) || chNearRiver(x, z, 0.8) || blocked(me.foot.x, me.foot.z, x, z) || chZoneOf(x, z) !== zi) continue;
      if (put.some((q) => Math.hypot(q[0] - x, q[1] - z) < 1.6) || cars.some((c) => Math.abs(c.x - x) < 1.8 && Math.abs(c.z - z) < 1.8)) continue;
      if (zombies.some((q) => Math.hypot(q.foot.x - x, q.foot.z - z) < 7.6)) continue;   // 어느 좀비의 시야 안에도 갑자기 생기지 않게
      chExact = true; const c = chPut(x, z, { x0: x - 1.5, z0: z - 1.5, x1: x + 1.5, z1: z + 1.5 }, '', null); chExact = false; c.startW = true; c.sleep = false; c.met = true; put.push([x, z]); break;
    }
    W.n -= put.length; W.tries++;
    if (W.n <= 0 || W.tries > 90) chStartW = null;
  }
  function showDud() {''')
open('c113_patch.py', 'w', encoding='utf8').write('# c113: 시작 하양은 내가 조금 움직인 뒤 가는 방향 앞에 나타난다 (gen_c113.py가 만든다)\nC113_R = ' + pprint.pformat(R, width=100000) + '\n')
print('replacements', len(R))
