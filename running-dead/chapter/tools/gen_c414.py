# c414: 본 맵 — 건널목 3분의 1 덜기 (평균 60 → 40) · 작은 단락 3분의 1로 (18 → 6), 빠진 자리는 큰 단락
src = open('c413.mjs').read()
GEN = open('world/gen9.js').read()
R = []
i0 = src.index("  // ── c406: 본 맵 — 시작할 때마다 새로 만드는 랜덤 월드 ──"); i1 = src.index("  const CH_BIGMAP = ")
old = src[i0:i1]
assert old.count('function chWorldGen(') == 1 and old.count('function chWorldBuild(') == 1
R.append((old, GEN.rstrip('\n') + '\n'))
open('c414_patch.py', 'w').write("# c414: 본 맵 건널목·작은 단락 줄이기\nC414_R = " + repr(R) + "\n")
