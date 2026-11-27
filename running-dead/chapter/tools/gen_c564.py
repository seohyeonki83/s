import pathlib
s = pathlib.Path('c563.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("[[0, 3], [1.2, 3], [2.4, 2]]", "[[0, 2], [1.2, 2]]   /* c564: 군인차 3대 → 2대 · 드론 차마다 2 (총 4) · 사각 4 · 군인 6 */")
rep("'드론을 싣고 오는 군인차 3대'", "'드론을 싣고 오는 군인차 2대'")
pathlib.Path('c564_patch.py').write_text('C564_R = ' + repr(R) + '\n')
print(len(R))
