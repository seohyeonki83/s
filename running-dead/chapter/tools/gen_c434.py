# c434: 드론 체력 9 → 8 (★0 자폭 산성 4초 × 2 = 8로 딱 죽는다)
src = open('c433.mjs').read()
a = "const CH_DRONE_HP = 9,   /* c433: 30 → 9 */"
assert src.count(a) == 1
R = [(a, "const CH_DRONE_HP = 8,   /* c434: 9 → 8 */   /* c433: 30 → 9 */")]
open('c434_patch.py', 'w').write("# c434: 드론 체력 8\nC434_R = " + repr(R) + "\n")
