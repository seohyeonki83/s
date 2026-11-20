# c218: 체력바 — 늘 최대 4겹(초록·파랑·보라·빨강), 그 이상은 가로를 끝없이 늘려서 4겹에 맞춘다 · 보스도 같다
#   · 기준 = 동료 기본 최대 체력 (나는 내 기본 최대 체력) · 동료(와 같은 적·사물) 바 가로 3분의 1 줄임
C218_R = [
 ("return Math.min(2, Math.max(1, (b.maxHp || 0) / (4 * U0))); };", "return Math.max(1, (b.maxHp || 0) / (4 * U0)); };   /* c218: 끝없이 */"),
 ("    if (b.oneBar) { b.hpFill.scale.x = Math.max(0.001, h / (b.maxHp || 1)); return; }   // 보스는 그대로\n", ""),
 ("CHAPTER && !b.oneBar ? (mine ? 1.2 * 1.2 * 1.2 * 2 / 3 * 2 / 3 : 2 * 0.5 / POLICE_HP * ALLY_HP * 0.9) * chBarK(b)",
  "CHAPTER ? (mine ? 1.2 * 1.2 * 1.2 * 2 / 3 * 2 / 3 : 2 * 0.5 / POLICE_HP * ALLY_HP * 0.9 * 2 / 3) * chBarK(b)"),
]
