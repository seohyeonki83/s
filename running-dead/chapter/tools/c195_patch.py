# c195: 장갑차 거리는 가운데 점이 아니라 몸 둘레(반지름 = 몸 길이의 반)부터 잰다 — 테이저가 닿는 거리 · 장갑차 기관포 사거리 둘 다
#       처음 시작할 때 내 체력 = 최대의 80%
C195_R = [
 ("const T = chTank, d = Math.max(0, Math.hypot(T.x - me.foot.x, T.z - me.foot.z) - CAR_W * CH_TK_K / 2);", "const T = chTank, d = Math.max(0, Math.hypot(T.x - me.foot.x, T.z - me.foot.z) - CAR_L * CH_TK_KL / 2);   /* c195: 몸 둘레부터 */"),
 ("    const R = SIGHT; let best = null, bd = R;   /* c168: 사거리 = 경찰 */\n    for (const z of nearIn(zCells, car.x, car.z, R, chTkBuf)) {\n      if (!isZombie(z)) continue;\n      const d = Math.hypot(z.foot.x - car.x, z.foot.z - car.z);",
  "    const rim = CAR_L * CH_TK_KL / 2, R = SIGHT; let best = null, bd = R;   /* c168: 사거리 = 경찰 · c195: 몸 둘레부터 잰다 */\n    for (const z of nearIn(zCells, car.x, car.z, R + rim, chTkBuf)) {\n      if (!isZombie(z)) continue;\n      const d = Math.max(0, Math.hypot(z.foot.x - car.x, z.foot.z - car.z) - rim);"),
 ("    me.hp = MY_HP * MY_START_HP;", "    me.hp = MY_HP * (CHAPTER ? 0.8 : MY_START_HP);   /* c195: 처음 체력 80% */"),
]
