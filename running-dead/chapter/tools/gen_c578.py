import pathlib
s = pathlib.Path('c577.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("{ if (type === 'police' && ++chPolN % 5 === 0) chMakeSg(c);   /* c437 */ else if (type === 'soldier' && chAL >= CH_MIXL && ++chSolN % 5 === 0) chMakeRobot(c); }",
    "{ if (type === 'police' && ++chPolN % 3 === 0) chMakeSg(c);   /* c578: 5명 중 1 → 3명 중 1 */ else if (type === 'soldier' && chAL >= CH_MIXL && ++chSolN % 3 === 0) chMakeRobot(c); }")
pathlib.Path('c578_patch.py').write_text('C578_R = ' + repr(R) + '\n')
print(len(R))
