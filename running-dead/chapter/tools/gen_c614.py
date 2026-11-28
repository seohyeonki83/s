import pathlib
s = pathlib.Path('c613.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("const R = c.sight * 0.8, dx", "const R = c.sight * 0.8 * 0.7, dx")   # c614: 샷건 맞는 범위 30% 줄임 (0.8 → 0.56)
pathlib.Path('c614_patch.py').write_text('C614_R = ' + repr(R) + '\n')
print(len(R))
