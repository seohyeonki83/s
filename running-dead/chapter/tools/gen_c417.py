# c417: 본 맵 — 건널목 길이 50% 더 길게
src = open('c416.mjs').read()
GEN = open('world/gen9.js').read()
R = []
i0 = src.index("  // ── c406: 본 맵 — 시작할 때마다 새로 만드는 랜덤 월드 ──"); i1 = src.index("  const CH_BIGMAP = ")
old = src[i0:i1]
assert old.count('function chWorldGen(') == 1 and old.count('function chWorldBuild(') == 1
R.append((old, GEN.rstrip('\n') + '\n'))
open('c417_patch.py', 'w').write("# c417: 건널목 50% 더 길게\nC417_R = " + repr(R) + "\n")
