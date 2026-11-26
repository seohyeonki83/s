import pathlib
s = pathlib.Path('c488.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("    else z.force = MY_FORCE * 0.5;            // 히드라: 미는 힘 = 나의 50%", "    else { z.force = MY_FORCE * 0.5; if (CHAPTER) { z.baseMaxHp = z.maxHp; z.maxHp *= 2; z.hp = z.maxHp; } }   /* c489: 히드라 최대 체력 2배 (변이 동안) */            // 히드라: 미는 힘 = 나의 50%")
pathlib.Path('c489_patch.py').write_text('C489_R = ' + repr(R) + '\n')
