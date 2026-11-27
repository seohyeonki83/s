import pathlib
s = pathlib.Path('c557.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("const camK = 1 + Math.max(0, n - ARMY_FREE) * 0.004;", "const camK = 1 + Math.max(0, n - ARMY_FREE) * 0.008;   /* c558: 0.4 → 0.8% */")
pathlib.Path('c558_patch.py').write_text('C558_R = ' + repr(R) + '\n')
print(len(R))
