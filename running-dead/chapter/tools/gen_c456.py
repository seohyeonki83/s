import pathlib
s = pathlib.Path('c455.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:60], s.count(a)); R.append((a, b))
rep("const CH_DISC_N = 14;", "const CH_DISC_N = 10;   /* c456: 14 → 10 */")
pathlib.Path('c456_patch.py').write_text('C456_R = ' + repr(R) + '\n')
