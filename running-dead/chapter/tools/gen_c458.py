import pathlib
s = pathlib.Path('c457.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:60], s.count(a)); R.append((a, b))
rep("const chSfAt = (n) => { let t = 0; for (let i = 0; i < n; i++) t += 120 - 5 * i; return t; };",
    "const chSfAt = (n) => [0, 120, 265, 405, 550][Math.min(n, 4)] + Math.max(0, n - 4) * 100;   /* c458: 보스 550초 그대로 · 특공대 3차례를 그 안에 — 120 · 265 · 405 (간격 120 · 145 · 140 · 145) */")
pathlib.Path('c458_patch.py').write_text('C458_R = ' + repr(R) + '\n')
