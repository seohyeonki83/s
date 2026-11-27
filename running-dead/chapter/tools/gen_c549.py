import pathlib
s = pathlib.Path('c548.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  const CH_DISC_N = 2;", "  const CH_DISC_N = 4, CH_DISC_P = 3;   /* c549: 바뀐 빨강 4 · 바뀐 경찰 3 */")
rep("if (chDiscR >= CH_DISC_N && chDiscP >= CH_DISC_N) return;", "if (chDiscR >= CH_DISC_N && chDiscP >= CH_DISC_P) return;")
rep("cop = c.police && !c.military && c.street && chDiscP < CH_DISC_N;", "cop = c.police && !c.military && c.street && chDiscP < CH_DISC_P;")
pathlib.Path('c549_patch.py').write_text('C549_R = ' + repr(R) + '\n')
print(len(R))
