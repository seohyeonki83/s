# c426: 장비 배지 줄 구성 원래대로 (3 · 2 · 2 · 2 …). 위아래 간격 42px는 그대로
src = open('c425.mjs').read()
R = []
a = "      const row = i < 6 ? Math.floor(i / 3) : 2 + Math.floor((i - 6) / 2), col = i < 6 ? i % 3 : (i - 6) % 2;   // c425: 아래 두 줄은 3개씩, 그 위로 2개씩"
assert src.count(a) == 1
R.append((a, "      const row = i < 3 ? 0 : 1 + Math.floor((i - 3) / 2), col = i < 3 ? i : (i - 3) % 2;   // c426: 원래대로 — 첫 줄 3개, 그 위로 2개씩"))
open('c426_patch.py', 'w').write("# c426: 배지 줄 원래대로\nC426_R = " + repr(R) + "\n")
