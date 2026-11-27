import pathlib
s = pathlib.Path('c571.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("    if (CHAPTER && chAL >= CH_MIXL && !chNoMix)   /* c505: 난이도별 */ { if (type === 'police' && ++chPolN % 5 === 0) chMakeSg(c);   /* c437: 총동원령부터 */ else if (type === 'soldier' && ++chSolN % 5 === 0) chMakeRobot(c); }",
    "    if (CHAPTER && chAL >= CH_MIXL - 1 && !chNoMix)   /* c572: 경찰 → 샷건 섞임은 한 단계 먼저 (쉬움 팬데믹 · 보통 비상 · 어려움 경계) */ { if (type === 'police' && ++chPolN % 5 === 0) chMakeSg(c);   /* c437 */ else if (type === 'soldier' && chAL >= CH_MIXL && ++chSolN % 5 === 0) chMakeRobot(c); }")
pathlib.Path('c572_patch.py').write_text('C572_R = ' + repr(R) + '\n')
print(len(R))
