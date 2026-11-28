import pathlib
s = pathlib.Path('c610.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  const CH_MAG_R = 1.5;", "  const CH_MAG_R = 3.0;   /* c611: 자석 거리 2배 (공격 거리 × 1.5 → × 3) */")
pathlib.Path('c611_patch.py').write_text('C611_R = ' + repr(R) + '\n')
print(len(R))
