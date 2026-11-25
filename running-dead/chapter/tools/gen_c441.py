# c441: 잔류제가 변이 주사의 변이 시간도 늘린다 (5%씩 · 최대 30%)
src = open('c440.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("  const MUT_T = () => 6 + 3 * chLvB('mutate');", "  const MUT_T = () => (6 + 3 * chLvB('mutate')) * (CHAPTER ? chLingK() : 1);   /* c441: 잔류제 */")
rep("    linger: (n) => `감전·산성·유혹 시간 +${5 * (1 + n)}%`,", "    linger: (n) => `감전·산성·유혹 · 변이 시간 +${5 * (1 + n)}%`,   /* c441 */")
rep("감전, 산성(산성 자폭 스위치 · 산성 폭발), 유혹 시간이 늘어납니다.", "감전, 산성(산성 자폭 스위치 · 산성 폭발), 유혹 시간과 변이 주사의 변이 시간이 늘어납니다.")
open('c441_patch.py', 'w').write("# c441: 잔류제 — 변이 시간\nC441_R = " + repr(R) + "\n")
