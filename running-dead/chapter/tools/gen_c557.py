import pathlib
s = pathlib.Path('c556.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  const CH_E7 = 0.93;", "  const CH_E7 = 0.9;   /* c557: 7% → 10% (원래 값 기준) · 챕터 강화(CH_SK)는 이 값 위에 곱해진다 */")
pathlib.Path('c557_patch.py').write_text('C557_R = ' + repr(R) + '\n')
print(len(R))
