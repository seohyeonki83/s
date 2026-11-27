import pathlib
s = pathlib.Path('c570.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("const CH_MIXL = CH_RUN ? { e: 6, n: 5, h: 4 }[CH_DIF] : 5;", "const CH_MIXL = CH_RUN ? { e: 5, n: 4, h: 3 }[CH_DIF] : 5;   /* c571: 쉬움 총동원령 · 보통 팬데믹 · 어려움 비상 */")
rep("const CH_MIX_T = { e: 6, n: 5, h: 4 };", "const CH_MIX_T = { e: 5, n: 4, h: 3 };")
pathlib.Path('c571_patch.py').write_text('C571_R = ' + repr(R) + '\n')
print(len(R))
