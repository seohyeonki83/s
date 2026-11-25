# c446: 내 미는 힘 5 → 4 (덩치가 되면 5 · 덩치는 모두 5 · 괴물 덩치만 세진다)
src = open('c445.mjs').read()
a = "const CH_MY_FORCE = 5;   /* c445: 7 → 5 */"
assert src.count(a) == 1
R = [(a, "const CH_MY_FORCE = 4;   /* c446: 5 → 4 (덩치가 되면 5) */   /* c445: 7 → 5 */")]
open('c446_patch.py', 'w').write("# c446: 내 미는 힘 4\nC446_R = " + repr(R) + "\n")
