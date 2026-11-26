import pathlib
s = pathlib.Path('c477.mjs').read_text()
R = []
def rep(a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a)); R.append((a, b))
rep("const HP_MAX = 100;", "const HPK = 2;   // c478: 체력 · 공격력 숫자만 2배 (밸런스 그대로)\n  const HP_MAX = 100 * HPK;")
rep("const GUARD_HP = 200;", "const GUARD_HP = 200 * HPK;   /* c478 */")
rep("const DAMAGE = 20 / 2 * 0.7;", "const DAMAGE = 20 / 2 * 0.7 * HPK;   /* c478 */")
for nm, v in [('ORG', 15), ('RED', 18), ('PO', 20), ('SO', 5), ('SN', 70)]:
    rep(f"CH_DMG_{nm} = {v} * CH_EK", f"CH_DMG_{nm} = {v} * HPK * CH_EK")
rep("const POLICE_HP = 300 * 0.7 * 0.8;", "const POLICE_HP = 300 * HPK * 0.7 * 0.8;   /* c478 */")
rep("const POLICE_DAMAGE = 50 / 2 * 0.7 * 0.95 * 0.9;", "const POLICE_DAMAGE = 50 * HPK / 2 * 0.7 * 0.95 * 0.9;   /* c478 */")
rep("const CAR_HIT_DMG = 50;", "const CAR_HIT_DMG = 50 * HPK;   /* c478 */")
rep("const CH_DRONE_HP = 8,", "const CH_DRONE_HP = 8 * HPK,   /* c478 */")
rep("b.maxHp = 380 * 0.9;", "b.maxHp = 380 * HPK * 0.9;   /* c478 */")
rep("b.hp -= Math.max(300, (b.maxHp || 100) / 1.2) * chDt;", "b.hp -= Math.max(300 * HPK, (b.maxHp || 100 * HPK) / 1.2) * chDt;   /* c478 */")
# 산성 — 도트 · 산성 강도 · 산성 폭발 터질 때
rep("e.acidT -= CH_DOT_T; const d = 1 + chAcidB();", "e.acidT -= CH_DOT_T; const d = 1 * HPK + chAcidB();   /* c478 */")
rep("d.acidT -= CH_DOT_T; const n = 1 + chAcidB();", "d.acidT -= CH_DOT_T; const n = 1 * HPK + chAcidB();   /* c478 */")
rep("c.hp = Math.max(0, c.hp - 3 - chAcidB());", "c.hp = Math.max(0, c.hp - 3 * HPK - chAcidB());   /* c478 */")
rep("chDotPop(c.foot.x + 0.6, c.foot.z, 3 + chAcidB());", "chDotPop(c.foot.x + 0.6, c.foot.z, 3 * HPK + chAcidB());")
rep("d.gooT -= CH_DOT_T; const n = 3 + chAcidB();", "d.gooT -= CH_DOT_T; const n = 3 * HPK + chAcidB();")
rep("car.gooT -= CH_DOT_T; const gd = 3 + chAcidB();", "car.gooT -= CH_DOT_T; const gd = 3 * HPK + chAcidB();")
rep("  const chAcidB = () => owned.acidp ? chAcidPB(lv('acidp')) : 0;", "  const chAcidB = () => owned.acidp ? chAcidPB(lv('acidp')) * HPK : 0;   /* c478 */")
rep("  const chAcidHit = () => Math.round(3 + 7 * lv('acid') / 5);", "  const chAcidHit = () => Math.round(3 + 7 * lv('acid') / 5) * HPK;   /* c478 */")
# 설명 숫자
rep("    acidp: (n) => `산성 도트 +${chAcidPB(n)} (1초마다)`,", "    acidp: (n) => `산성 도트 +${chAcidPB(n) * HPK} (1초마다)`,")
rep("acidp: ['도트', (n) => `+${chAcidPB(n)}`]", "acidp: ['도트', (n) => `+${chAcidPB(n) * HPK}`]")
rep("    acid: (n) => `터질 확률 ${30 + 10 * n}% · 터질 때 ${Math.round(3 + 7 * n / 5)} · 3초 · 1초마다 1 ·", "    acid: (n) => `터질 확률 ${30 + 10 * n}% · 터질 때 ${Math.round(3 + 7 * n / 5) * HPK} · 3초 · 1초마다 ${HPK} ·")
pathlib.Path('c478_patch.py').write_text('C478_R = ' + repr(R) + '\n')
print(len(R))
