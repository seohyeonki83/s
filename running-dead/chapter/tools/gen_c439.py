# c439: 괴물 좀비 빨간 테두리 두께 반 (후광 1.9 → 1.45) · 드론이 막혀 못 움직이면 차처럼 갈 쪽으로 순간이동 (3초 동안 1칸도 못 가면 8칸 · 또 막히면 16칸 …)
src = open('c438.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("z.brHalo.material.color.setHex(want);", "z.brHalo.material.color.setHex(want); z.brHalo.scale.setScalar(B.id === 'monster' ? 1.45 : 1.9);   /* c439: 괴물 테두리 두께 반 */")
rep("      d.foot.set(d.x, 0, d.z);\n      // 기관총", """      if (!t || dist > CH_DRONE_RANGE * 0.8) {   // c439: 다가가는 중인데 3초 동안 1칸도 못 갔다 → 갈 쪽으로 8칸 순간이동 (그 둘레에서 또 막히면 16칸 …) — 차가 끼었을 때와 같다
        if (d.sx === undefined || Math.hypot(d.x - d.sx, d.z - d.sz) > 1) { d.sx = d.x; d.sz = d.z; d.stT = 0; }
        else if ((d.stT = (d.stT || 0) + dt) >= 3) {
          d.jn = d.jx !== undefined && Math.hypot(d.x - d.jx, d.z - d.jz) < 8 ? (d.jn || 1) + 1 : 1;
          const st = Math.min(8 * d.jn, dist - CH_DRONE_RANGE * 0.6);
          for (let k = st; k > 1; k -= 0.5) { const nx = d.x + (gx - d.x) / dist * k, nz = d.z + (gz - d.z) / dist * k; if (chDroneFree(nx, nz)) { d.x = nx; d.z = nz; break; } }
          d.sx = d.x; d.sz = d.z; d.stT = 0; d.jx = d.x; d.jz = d.z;
        }
      } else d.stT = 0;
      d.foot.set(d.x, 0, d.z);
      // 기관총""")
open('c439_patch.py', 'w').write("# c439: 괴물 테두리 · 드론 끼임\nC439_R = " + repr(R) + "\n")
