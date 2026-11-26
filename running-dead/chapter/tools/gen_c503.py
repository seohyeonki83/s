import pathlib
s = pathlib.Path('c502.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("if (z.mut || z.brHalo) chMutLook(z);", "if (z.mut || z.brHalo || z.brHorn) chMutLook(z);   /* c503: 변이가 풀리면 뿔도 지운다 */")
pathlib.Path('c503_patch.py').write_text('C503_R = ' + repr(R) + '\n')
