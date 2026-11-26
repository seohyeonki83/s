import pathlib
s = pathlib.Path('c489.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("car.hpK *= 0.8 * 0.8", "car.hpK *= 0.8 * 0.8 * 0.75   /* c490: 25% 더 */")
pathlib.Path('c490_patch.py').write_text('C490_R = ' + repr(R) + '\n')
