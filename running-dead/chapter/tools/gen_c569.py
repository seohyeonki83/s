import pathlib
s = pathlib.Path('c568.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("g.strokeText('-' + n, 64, 34); g.fillStyle = '#ff4a3d'", "g.strokeText('-' + n, 64, 34); g.fillStyle = '#7ed321'   /* c569: 도트 숫자 = 산성 녹색 */")
pathlib.Path('c569_patch.py').write_text('C569_R = ' + repr(R) + '\n')
print(len(R))
