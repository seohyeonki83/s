import pathlib
s = pathlib.Path('c543.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("const CH_SK = CH_RUN ? 1 + 0.2 * (CH_STG - 1) : 1;", "const CH_SK = CH_RUN ? 1 + 0.1 * (CH_STG - 1) : 1;   /* c544: 챕터마다 +10% (복리 아님 — 1.0 · 1.1 · 1.2 · 1.3) */")
pathlib.Path('c544_patch.py').write_text('C544_R = ' + repr(R) + '\n')
print(len(R))
