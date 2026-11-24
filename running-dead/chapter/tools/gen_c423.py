# c423: 드론 나오는 주기 1.5배 (80 → 120초). 한 번에 나오는 수 · 첫 출동(개판 1분 뒤)은 그대로
src = open('c422.mjs').read()
R = []
a = "CH_DRONE_EVERY = 80,   /* c419: 40 → 80초 (주기 2배) */"
assert src.count(a) == 1
R.append((a, "CH_DRONE_EVERY = 120,   /* c423: 80 → 120초 (1.5배) */   /* c419: 40 → 80초 (주기 2배) */"))
open('c423_patch.py', 'w').write("# c423: 드론 주기 1.5배\nC423_R = " + repr(R) + "\n")
