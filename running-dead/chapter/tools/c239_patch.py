# c239: 적 공격력 전체 10% 줄임 (보스 제외) — 주황 13.5 · 빨강 16.2 · 경찰 18 · 군인 한 발 4.5 · 저격수 63 · 노랑도 10% (분홍은 빨강 기준이라 같이)
C239_R = [
 ("const CH_DMG_ORG = 15 / CH_EMUL, CH_DMG_RED = 18 / CH_EMUL, CH_DMG_PO = 20 / CH_EMUL, CH_DMG_SO = 5 / CH_EMUL, CH_DMG_SN = 70 / CH_EMUL;",
  "const CH_EK = 0.9, CH_DMG_ORG = 15 * CH_EK / CH_EMUL, CH_DMG_RED = 18 * CH_EK / CH_EMUL, CH_DMG_PO = 20 * CH_EK / CH_EMUL, CH_DMG_SO = 5 * CH_EK / CH_EMUL, CH_DMG_SN = 70 * CH_EK / CH_EMUL, CH_DMG_YEL = DAMAGE * CH_EK;   /* c239: 보스 빼고 적 공격력 10% 줄임 */"),
 ("(b.vig || b.boss ? CH_DMG_RED : CH_DMG_ORG) : DAMAGE) * (b.dmgK || 1)", "(b.vig || b.boss ? CH_DMG_RED : CH_DMG_ORG) : CHAPTER ? CH_DMG_YEL : DAMAGE) * (b.dmgK || 1)"),
]
