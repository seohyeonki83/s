# c235: 적 한 번 피해를 숫자로 정한다 (적 배율 적용 뒤 값) — 주황 15 · 빨강 18 (분홍도 빨강 기준) · 경찰 20 · 군인 한 발 5 · 저격수 70
C235_R = [
 ("isZombie(b) ? zDamage(b) : DAMAGE * (CHAPTER && b.attacker ? (b.vig || b.boss ? 2 : 1.5) : 1) * (b.dmgK || 1)",
  "isZombie(b) ? zDamage(b) : (CHAPTER && b.attacker ? (b.vig || b.boss ? CH_DMG_RED : CH_DMG_ORG) : DAMAGE) * (b.dmgK || 1)   /* c235 */"),
 ("    const base = POLICE_DAMAGE * (c.sniper ?", "    const base = CHAPTER ? (c.sniper ? CH_DMG_SN : c.soldier ? CH_DMG_SO : CH_DMG_PO) : POLICE_DAMAGE * (c.sniper ?"),
 ("  const HIT_EVERY = 1 / 1.3;", "  const CH_EMUL = 1.15 * 1.2 * 0.95 * 0.93 * 0.93;   // c235: 챕터 적 공격 배율 (landHit에서 곱한다) — 아래 값은 이걸 곱한 뒤 정확히 그 숫자가 되게\n"
  "  const CH_DMG_ORG = 15 / CH_EMUL, CH_DMG_RED = 18 / CH_EMUL, CH_DMG_PO = 20 / CH_EMUL, CH_DMG_SO = 5 / CH_EMUL, CH_DMG_SN = 70 / CH_EMUL;   // 주황 · 빨강 · 경찰 · 군인 한 발 · 저격수\n"
  "  const HIT_EVERY = 1 / 1.3;"),
]
