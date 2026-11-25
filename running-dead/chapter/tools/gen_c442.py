# c442: c441 되돌림 — 잔류제는 변이 주사 · 각성 주사에 안 걸린다
src = open('c441.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("  const MUT_T = () => (6 + 3 * chLvB('mutate')) * (CHAPTER ? chLingK() : 1);   /* c441: 잔류제 */", "  const MUT_T = () => 6 + 3 * chLvB('mutate');   /* c442: 잔류제 안 걸림 (c441 되돌림) */")
rep("    linger: (n) => `감전·산성·유혹 · 변이 시간 +${5 * (1 + n)}%`,   /* c441 */", "    linger: (n) => `감전·산성·유혹 시간 +${5 * (1 + n)}%`,")
rep("감전, 산성(산성 자폭 스위치 · 산성 폭발), 유혹 시간과 변이 주사의 변이 시간이 늘어납니다.", "감전, 산성(산성 자폭 스위치 · 산성 폭발), 유혹 시간이 늘어납니다.")
open('c442_patch.py', 'w').write("# c442: c441 되돌림\nC442_R = " + repr(R) + "\n")
