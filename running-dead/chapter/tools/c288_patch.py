# c288: 틀니 새로 — 감염 속도 100% → 최대 180% · 체력 회복량 +5%씩 (최대 +30%) · 덮치기 기준 기능 없앰 / 자폭은 변이 좀비에 안 걸림
C288_R = [
  ("  const chDown = (b) => b.hp <= 0 || (CHAPTER && owned.teeth && !b.boss && b.hp <= b.maxHp * 0.05 * (1 + lv('teeth')));   // c283: 틀니 — 체력이 이만큼 남으면 덮칠 수 있다",
   "  const chDown = (b) => b.hp <= 0;   // c288: 틀니 덮치기 기준 없앰 — 체력 0일 때만"),
  ("    if (t.hp > 0) t.hp = 0;   // c283: 틀니로 덮친 사람 — 물리는 순간 쓰러진다\n", ""),
  ("(CHAPTER && owned.teeth ? 1 - 0.1 * (1 + lv('teeth')) : 1);   /* c224: 틀니 */", "(CHAPTER && owned.teeth ? 1 / (1 + 0.8 / 6 * (1 + lv('teeth'))) : 1);   /* c288: 틀니 — 감염 속도 113 · 127 · 140 · 153 · 167 · 180% */"),
  ("  const zHeal = (z) => (z === me ? MY_BITE_HEAL : BITE_HEAL) + 0.04 * up.meat;", "  const zHeal = (z) => ((z === me ? MY_BITE_HEAL : BITE_HEAL) + 0.04 * up.meat) * (CHAPTER && owned.teeth ? 1 + 0.05 * (1 + lv('teeth')) : 1);   /* c288: 틀니 — 회복량 +5%씩 (나·동료 전부) */"),
  ("teeth: ['나와 동료들이 인간을 더 빠르게 좀비로 만듭니다', '강화 시 더 빨라집니다.'],", "teeth: ['인간을 덮칠 때 감염시키는 시간이 줄어듭니다. 체력 회복량이 늘어납니다.', '강화 시 더 빨라지고 회복량이 더 늘어납니다.'],"),
  ("teeth: '나와 동료들이 인간을 좀비로 만드는 시간이 줄어들고, 체력이 조금 남은 인간도 바로 덮칠 수 있습니다. 강화하면 더 빨라지고 더 많이 남아도 덮칩니다.',", "teeth: '나와 동료들이 인간을 덮칠 때 감염시키는 시간이 줄어들고, 물어뜯으며 회복하는 체력이 늘어납니다. 강화하면 더 빨라지고 더 많이 회복합니다.',"),
  ("teeth: (n) => `감염 시간 -${10 * (1 + n)}% · 체력 ${5 * (1 + n)}% 이하면 덮침`,", "teeth: (n) => `감염 속도 ${Math.round(100 + 80 / 6 * (1 + n))}% · 체력 회복량 +${5 * (1 + n)}%`,"),
  ("teeth: ['감염', (n) => `-${10 * (1 + n)}%`]", "teeth: ['감염', (n) => `${Math.round(100 + 80 / 6 * (1 + n))}%`]"),
  ("    const plain = all.filter((z) => !z.mut), al = plain.length ? plain : all;", "    const al = all.filter((z) => !z.mut); if (!al.length) return false;   // c288: 변이 좀비는 자폭하지 않는다"),
]
C288_R.append(("teeth: '나와 동료들의 감염 속도 증가'", "teeth: '감염 속도·회복량 증가'"))
