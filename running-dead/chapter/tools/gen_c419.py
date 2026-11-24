# c419: 드론 — 나오는 주기 2배 (40 → 80초), 한 번에 나오는 수 2배 (1·2·3 → 2·4·6). 첫 출동(개판 1분 뒤)은 그대로
src = open('c418.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("CH_DRONE_EVERY = 40,", "CH_DRONE_EVERY = 80,   /* c419: 40 → 80초 (주기 2배) */")
rep("N = stars <= 3 ? 1 : stars === 4 ? 2 : 3; i < N", "N = (stars <= 3 ? 1 : stars === 4 ? 2 : 3) * 2   /* c419: 한 번에 2배 */; i < N")
open('c419_patch.py', 'w').write("# c419: 드론 주기 2배 · 한 번에 2배\nC419_R = " + repr(R) + "\n")
