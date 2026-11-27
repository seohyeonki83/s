import pathlib
s = pathlib.Path('c553.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("c.robot = true; c.noLure = true; c.hp = c.maxHp = c.maxHp * 2;", "c.robot = true; c.noLure = true; c.hp = c.maxHp = c.maxHp * 1.6;   /* c554: 사각 로봇 체력 20% 줄임 (2 → 1.6배) */")
pathlib.Path('c554_patch.py').write_text('C554_R = ' + repr(R) + '\n')
print(len(R))
