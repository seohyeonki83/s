import pathlib
s = pathlib.Path('c608.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("const CH_DRONE_HP = 8 * HPK,", "const CH_DRONE_HP = 9,   /* c609: 드론 기본 체력 16 → 9 (화면 숫자 기준) */")
pathlib.Path('c609_patch.py').write_text('C609_R = ' + repr(R) + '\n')
print(len(R))
