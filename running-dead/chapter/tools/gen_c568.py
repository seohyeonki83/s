import pathlib
s = pathlib.Path('c567.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  const chSfAt = (n) => n * 100;", "  const chSfAt = (n) => 80 + (n - 1) * 100;   /* c568: 첫 특공대 80초, 그 뒤 100초마다 (80 · 180 · 280 · 380) */")
pathlib.Path('c568_patch.py').write_text('C568_R = ' + repr(R) + '\n')
print(len(R))
