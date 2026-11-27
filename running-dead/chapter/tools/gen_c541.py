import pathlib
s = pathlib.Path('c540.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  const CH_DISC_N = 10;", "  const CH_DISC_N = 4, CH_DISC_O = 2, CH_DISC_Y = 2;   /* c541: 빨강·경찰 4 · 주황 2 · 노랑 2 */")
rep("if (chDiscR >= CH_DISC_N && chDiscO >= 4 && chDiscY >= 3) return;", "if (chDiscR >= CH_DISC_N && chDiscO >= CH_DISC_O && chDiscY >= CH_DISC_Y) return;")
rep("const org = c.attacker && !c.vig && chDiscO < 4, yel = c.guard && !c.demoted && chDiscY < 3;", "const org = c.attacker && !c.vig && chDiscO < CH_DISC_O, yel = c.guard && !c.demoted && chDiscY < CH_DISC_Y;")
pathlib.Path('c541_patch.py').write_text('C541_R = ' + repr(R) + '\n')
print(len(R))
