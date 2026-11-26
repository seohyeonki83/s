import pathlib
s = pathlib.Path('c494.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("const cashK = () => CHAPTER ? 1.2 * 1.15   /* c443: 15% 늘림 */", "const cashK = () => CHAPTER ? 1.2 * 1.15 * 1.25   /* c495: 25% 늘림 · c443: 15% 늘림 */")
rep("알아채는 거리 ${(8.64 * 1.15 * chCashStep(Math.min(5, n))).toFixed(1)}칸` + (n > 5", "알아채는 거리 ${(8.64 * 1.15 * 1.25 * chCashStep(Math.min(5, n))).toFixed(1)}칸` + (n > 5")
pathlib.Path('c495_patch.py').write_text('C495_R = ' + repr(R) + '\n')
