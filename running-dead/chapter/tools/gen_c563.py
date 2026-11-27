import pathlib
s = pathlib.Path('c562.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  const CH_E7 = 0.93;", "  const CH_E7H = 0.93 * 0.95;   /* c563: 적 체력만 5% 더 (공격력은 0.93 그대로) */\n  const CH_E7 = 0.93;")
rep("c.maxHp *= CH_SK * CH_E7; c.hp *= CH_SK * CH_E7; }", "c.maxHp *= CH_SK * CH_E7H; c.hp *= CH_SK * CH_E7H; }")
rep("* 0.95 * 0.9 * 1.1 * 0.95 * CH_E7; c.hpDisp = c.hp;", "* 0.95 * 0.9 * 1.1 * 0.95 * CH_E7H; c.hpDisp = c.hp;")
rep("c.hp = c.maxHp = CH_SK * CH_E7 * GUARD_HP", "c.hp = c.maxHp = CH_SK * CH_E7H * GUARD_HP")
pathlib.Path('c563_patch.py').write_text('C563_R = ' + repr(R) + '\n')
print(len(R))
