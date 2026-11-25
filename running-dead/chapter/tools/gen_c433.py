# c433: 드론 체력 30 → 9 · 주기 1.2배 (120 → 144초) · 나온 드론이 전부 죽어야 다음 주기가 흐른다 (첫 출동은 그대로 개판 1분 뒤)
src = open('c432.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("const CH_DRONE_HP = 30,", "const CH_DRONE_HP = 9,   /* c433: 30 → 9 */")
rep("CH_DRONE_EVERY = 120,   /* c423: 80 → 120초 (1.5배) */", "CH_DRONE_EVERY = 144,   /* c433: 120 → 144초 (1.2배) */   /* c423: 80 → 120초 (1.5배) */")
rep("    if (chDroneOn && (chDroneT += dt) >= CH_DRONE_EVERY) {", "    if (chDroneOn && !chDrones.some((d) => !d.dead) && (chDroneT += dt) >= CH_DRONE_EVERY) {   // c433: 살아 있는 드론이 있으면 주기가 안 흐른다 (다 죽어야 다음 주기 시작)")
open('c433_patch.py', 'w').write("# c433: 드론 체력 9 · 주기 144초 · 다 죽어야 다음 주기\nC433_R = " + repr(R) + "\n")
