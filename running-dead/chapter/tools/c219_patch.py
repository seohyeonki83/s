# c219: 보스 체력바만 따로 — 빨강 한 줄 · 가로 = 내 바의 2배
C219_R = [
 ("    if (!b.hpMat0) b.hpMat0 = b.hpFill.material;",
  "    if (b.oneBar) { b.hpFill.material = chHpMat4; b.hpFill.scale.x = Math.max(0.001, h / (b.maxHp || 1)); if (b.hpFill2) b.hpFill2.visible = b.hpFill3.visible = b.hpFill4.visible = false; return; }   // c219: 보스 = 빨강 한 줄\n"
  "    if (!b.hpMat0) b.hpMat0 = b.hpFill.material;"),
 ("CHAPTER ? (mine ? 1.2 * 1.2 * 1.2 * 2 / 3 * 2 / 3 :", "CHAPTER && b.oneBar ? 2 * 1.2 * 1.2 * 1.2 * 2 / 3 * 2 / 3   /* c219: 보스 = 내 바의 2배 */ : CHAPTER ? (mine ? 1.2 * 1.2 * 1.2 * 2 / 3 * 2 / 3 :"),
]
