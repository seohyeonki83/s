import pathlib
s = pathlib.Path('c559.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  const CH_E7 = 0.9;   /* c557: 7% → 10% (원래 값 기준)", "  const CH_E7 = 0.93;   /* c560: 다시 7%로 */   /* c557: 7% → 10% (원래 값 기준)")
pathlib.Path('c560_patch.py').write_text('C560_R = ' + repr(R) + '\n')
print(len(R))
