import pathlib
s = pathlib.Path('c545.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("const chSfAt = (n) => [0, 120, 265, 405, 550][Math.min(n, 4)] + Math.max(0, n - 4) * 100;", "const chSfAt = (n) => n * 100;   /* c546: 특공대 · 보스 출동 100초마다로 통일 (100 · 200 · 300 · 400) */")
pathlib.Path('c546_patch.py').write_text('C546_R = ' + repr(R) + '\n')
print(len(R))
