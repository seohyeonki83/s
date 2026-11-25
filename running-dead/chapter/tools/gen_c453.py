# c453: 승리 없음 (경찰서 · 보스 — 계속 한다, 튜토리얼 탈출은 그대로) · 흡수 좀비도 테두리 얇게 + 뿔 · 동료 감염 시간 15% → 6% 짧게
src = open('c452.mjs').read()
R = []
def rep(a, b, n=1):
    assert src.count(a) == n, (src.count(a), n, a[:90])
    R.append((a, b, n) if n != 1 else (a, b))
rep("if ((stationDown || (CHAPTER && chSf.won) || (CH_TUT", "if ((((stationDown || (CHAPTER && chSf.won)) && !(CHAPTER && !CH_TUT))   /* c453: 챕터는 승리 없음 — 계속 한다 */ || (CH_TUT")
rep("    const horn = !!B && B.id === 'monster';   // c448: 괴물 = 뿔", "    const horn = !!B;   // c448: 괴물 = 뿔 · c453: 흡수도")
rep("z.brHalo.scale.setScalar(B.id === 'monster' ? 1.45 : 1.9);", "z.brHalo.scale.setScalar(1.45);   /* c453: 흡수도 괴물처럼 얇게 */")
rep("(CHAPTER ? (z === me ? 0.9 : 0.85) : 1);   /* c452: 나 10% · 동료 15% 짧게 */", "(CHAPTER ? (z === me ? 0.9 : 0.94) : 1);   /* c453: 동료 6% · c452: 나 10% 짧게 */")
open('c453_patch.py', 'w').write("# c453: 승리 없음 · 흡수 테두리 · 뿔 · 동료 감염 6%\nC453_R = " + repr(R) + "\n")
