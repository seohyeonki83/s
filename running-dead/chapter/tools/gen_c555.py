import pathlib
s = pathlib.Path('c554.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); R.append((a, b))
rep("  const CH_SK = CH_RUN ?", "  const CH_E7 = 0.93;   /* c555: 적 캐릭터 기본 체력 · 공격력 7% 낮춤 (드론 · 차량 제외, 튜토리얼 포함) */\n  const CH_SK = CH_RUN ?")
rep("    if (CHAPTER && CH_SK !== 1 && c.maxHp > 0) { c.maxHp *= CH_SK; c.hp *= CH_SK; }   // c505: 스테이지 강화",
    "    if (CHAPTER && c.maxHp > 0) { c.maxHp *= CH_SK * CH_E7; c.hp *= CH_SK * CH_E7; }   // c505: 스테이지 강화   /* c555: × CH_E7 */")
rep("c.hp = c.maxHp = GUARD_HP * (type === 'armor' ? 4 : 2) * 0.95 * 0.9 * 1.1 * 0.95; c.hpDisp = c.hp;",
    "c.hp = c.maxHp = GUARD_HP * (type === 'armor' ? 4 : 2) * 0.95 * 0.9 * 1.1 * 0.95 * CH_E7; c.hpDisp = c.hp;   /* c555 */")
rep("c.hp = c.maxHp = CH_SK * GUARD_HP * 0.95 * 0.9 * 0.95 * 0.9 * 1.1 * 0.95;", "c.hp = c.maxHp = CH_SK * CH_E7 * GUARD_HP * 0.95 * 0.9 * 0.95 * 0.9 * 1.1 * 0.95;   /* c555 */")
rep("    if (CHAPTER && a && (a.kind === 'citizen' || a.kind === 'tank')) dmg *= 1.15 * 1.2 * 0.95 * 0.93 * 0.93;",
    "    if (CHAPTER && a && (a.kind === 'citizen' || a.kind === 'tank')) dmg *= 1.15 * 1.2 * 0.95 * 0.93 * 0.93;\n    if (CHAPTER && a && a.kind === 'citizen') dmg *= CH_E7;   /* c555: 적 캐릭터 공격 7% 낮춤 (드론 · 차량 제외) */")
pathlib.Path('c555_patch.py').write_text('C555_R = ' + repr(R) + '\n')
print(len(R))
