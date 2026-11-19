# c194: 보스 감전 — 내가 건물 안(뚫린 벽 · 열린 문 너머)에 있어도 공격선이 벽에 안 막히면 맞는다 (전엔 내가 건물 안이면 아예 후보에서 빠졌다)
C194_R = [
 ("if (CHAPTER && chTank && !chTank.wreck && !(chTank.stunT > 0) && !me.space) {", "if (CHAPTER && chTank && !chTank.wreck && !(chTank.stunT > 0)) {   /* c194: 건물 안이어도 (공격선만 본다) */"),
]
