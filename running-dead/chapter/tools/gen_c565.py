import pathlib
s = pathlib.Path('c564.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  const SAFE_HP = MY_DAMAGE * 7.5;", "  const SAFE_HP = MY_DAMAGE * 7.5 * 0.5;   /* c565: 보물상자 체력 반 */")
pathlib.Path('c565_patch.py').write_text('C565_R = ' + repr(R) + '\n')
print(len(R))
