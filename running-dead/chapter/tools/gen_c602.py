import pathlib
s = pathlib.Path('c601.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("      makeZombie(c); if (i >= n) { chMini(c);", "      c.sleep = false; c.met = true; makeZombie(c); c.sleep = false;   /* c602: 잠든 채로 만들어져 안 따라오던 것 */ if (i >= n) { chMini(c);")
pathlib.Path('c602_patch.py').write_text('C602_R = ' + repr(R) + '\n')
print(len(R))
