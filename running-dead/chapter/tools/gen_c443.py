# c443: 현금 거리 전부 15% 늘림 (알아채는 거리 · 바로 홀리는 거리 — 모든 단계)
src = open('c442.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("const cashK = () => CHAPTER ? 1.2 * chCashStep(", "const cashK = () => CHAPTER ? 1.2 * 1.15   /* c443: 15% 늘림 */ * chCashStep(")
rep("8.64 * chCashStep", "8.64 * 1.15 * chCashStep", 2)
open('c443_patch.py', 'w').write("# c443: 현금 거리 15%\nC443_R = " + repr(R) + "\n")
