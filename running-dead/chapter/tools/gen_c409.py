# c409: 본 맵 — 단락 사이를 물과 산 반반으로 (물 위 건널목 = 다리, 산 사이 건널목 = 산길)
src = open('c408.mjs').read()
GEN = open('world/gen9.js').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
# 생성기 통째로 바꾼다
i0 = src.index("  // ── c406: 본 맵 — 시작할 때마다 새로 만드는 랜덤 월드 ──"); i1 = src.index("  const CH_BIGMAP = ")
old = src[i0:i1]
assert old.count('function chWorldGen(') == 1 and old.count('function chWorldBuild(') == 1
R.append((old, GEN.rstrip('\n') + '\n'))
# 산 그림: 단락 묶음에 (산 덩어리가 100개쯤 된다)
rep("B.roof.renderOrder = -0.46; scene.add(B.roof);   // c13: 산 그림자(-0.47) 위 — 산 자체는 늘 보인다", "B.roof.renderOrder = -0.46; chStat(B.roof, Math.hypot(w, d) / 2);   /* c409: 단락 묶음에 */   // c13: 산 그림자(-0.47) 위 — 산 자체는 늘 보인다")
# 산 그림자: 화면에 걸친 산만 (화면 밖 산의 그림자는 나에게서 더 먼 쪽으로 뻗어서 화면에 안 들어온다 — 그림은 같다)
rep("        for (const B of hs) {\n          const cs = [[B.x0, B.z0], [B.x1, B.z0], [B.x1, B.z1], [B.x0, B.z1]];", "        for (const B of hs) {\n          if (B.x1 < viewR.x0 || B.x0 > viewR.x1 || B.z1 < viewR.z0 || B.z0 > viewR.z1) continue;   // c409: 화면 밖 산은 건너뛴다\n          const cs = [[B.x0, B.z0], [B.x1, B.z0], [B.x1, B.z1], [B.x0, B.z1]];")
rep("          pos.set([ax, 0.05, az, bx, 0.05, bz, bx2, 0.05, bz2, ax, 0.05, az, bx2, 0.05, bz2, ax2, 0.05, az2], o); o += 18;\n        }\n        geo.attributes.position.needsUpdate = true;", "          pos.set([ax, 0.05, az, bx, 0.05, bz, bx2, 0.05, bz2, ax, 0.05, az, bx2, 0.05, bz2, ax2, 0.05, az2], o); o += 18;\n        }\n        geo.setDrawRange(0, o / 3);   /* c409: 이번에 쓴 만큼만 그린다 */\n        geo.attributes.position.needsUpdate = true;")
open('c409_patch.py', 'w').write("# c409: 본 맵 — 물과 산 반반\nC409_R = " + repr(R) + "\n")
print(len(R), 'entries')
