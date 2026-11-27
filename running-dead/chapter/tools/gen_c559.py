import pathlib
s = pathlib.Path('c558.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("const camK = 1 + Math.max(0, n - ARMY_FREE) * 0.008;   /* c558: 0.4 → 0.8% */", "const camK = 1 + Math.max(0, n - ARMY_FREE) * 0.0035;   /* c559: 0.4 → 0.35% (c558의 0.8%는 잘못 알아들음) */")
pathlib.Path('c559_patch.py').write_text('C559_R = ' + repr(R) + '\n')
print(len(R))
