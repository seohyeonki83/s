# c451: 덩치 사물 피해 배율 1.4 → 1.5배
src = open('c450.mjs').read()
a = "dmg *= CHAPTER ? 1.4 : 2;   /* c450: 2 → 1.4배 (30% 줄임) */"
assert src.count(a) == 1
R = [(a, "dmg *= CHAPTER ? 1.5 : 2;   /* c451: 1.5배 */   /* c450: 2 → 1.4배 (30% 줄임) */")]
open('c451_patch.py', 'w').write("# c451: 덩치 사물 피해 1.5배\nC451_R = " + repr(R) + "\n")
