import pathlib
s = pathlib.Path('c598.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep('<div class="pc">${100 + lvN}', '<div class="pc">${lvN}')   # c599: 성장 표시 0부터
pathlib.Path('c599_patch.py').write_text('C599_R = ' + repr(R) + '\n')
print(len(R))
