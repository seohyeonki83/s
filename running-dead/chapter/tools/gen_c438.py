# c438: 드론 — 나에게 못 오고 멀리(시야 2.5배 밖) 25초 넘게 떠 있으면 조용히 사라진다 (다음 출동 주기를 막지 않게) · 불도저는 늘 노랑 (목표 표시가 풀릴 때 초록으로 돌아가던 것)
src = open('c437.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("    for (const d of chDrones.slice()) {\n      if (d.dead) continue;\n", """    for (const d of chDrones.slice()) {
      if (d.dead) continue;
      if (Math.hypot(d.x - me.foot.x, d.z - me.foot.z) > me.sense * 2.5) { if ((d.farT = (d.farT || 0) + dt) > 25) { d.dead = true; scene.remove(d.s); d.s.material.dispose(); scene.remove(d.sh); if (d.tr) { scene.remove(d.tr); d.tr.material.dispose(); } chDrones.splice(chDrones.indexOf(d), 1); continue; } } else d.farT = 0;   // c438: 못 오는 드론은 조용히 사라진다 (경험치 없음)
""")
rep("if (CHAPTER) { car.dozer = true; car.hpK *= 0.8; }", "if (CHAPTER) { car.dozer = true; car.hpK *= 0.8; car.tint0 = 0xd9a21b; }   /* c438: 목표 표시가 풀려도 노랑 */")
open('c438_patch.py', 'w').write("# c438: 못 오는 드론 정리 · 불도저 노랑\nC438_R = " + repr(R) + "\n")
