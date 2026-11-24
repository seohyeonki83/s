# c415: 본 맵 — 마주 보는 두 면마다 건널목 딱 하나 (같은 두 단락 사이 두 개는 하나로, 빠졌던 면은 다시)
src = open('c414.mjs').read()
GEN = open('world/gen9.js').read()
R = []
i0 = src.index("  // ── c406: 본 맵 — 시작할 때마다 새로 만드는 랜덤 월드 ──"); i1 = src.index("  const CH_BIGMAP = ")
old = src[i0:i1]
assert old.count('function chWorldGen(') == 1 and old.count('function chWorldBuild(') == 1
R.append((old, GEN.rstrip('\n') + '\n'))
open('c415_patch.py', 'w').write("# c415: 마주 보는 면마다 건널목 하나\nC415_R = " + repr(R) + "\n")
