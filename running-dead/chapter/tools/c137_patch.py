# c137: 보스(장갑차)는 나나 동료 눈에 띄기 전까지 보통 차 속도로 온다 — 한 번 보이면 그때부터 원래 속도(4분의 1)
C137_R = [
 ("const spd = CAR_SPEED * CH_TR_SPD.sedan * CH_TR_SLOW / 4 * (car.goo ? 0.8 : 1);", "const spd = CAR_SPEED * CH_TR_SPD.sedan * CH_TR_SLOW / (car.tkSeen ? 4 : 1) * (car.goo ? 0.8 : 1);   /* c137: 눈에 띄기 전엔 보통 차 속도 */"),
 ("if ((car.scanT -= dt) <= 0) { car.scanT = 0.2; car.foe = chTankFoe(car); }", "if ((car.scanT -= dt) <= 0) { car.scanT = 0.2; car.foe = chTankFoe(car); if (!car.tkSeen) chTankSeen(car); }"),
 ("  function chTankDrive(car, dt) {\n", "  function chTankSeen(car) {                   // c137: 나나 동료가 봤나 (인지거리 안 · 벽에 안 가림) — 한 번 보이면 끝까지 느리다\n    for (const z of nearIn(zCells, car.x, car.z, 16, chTkBuf2)) if (isZombie(z) && Math.hypot(z.foot.x - car.x, z.foot.z - car.z) <= z.sense + CAR_L * CH_TK_K / 2 && !blocked(z.foot.x, z.foot.z, car.x, car.z)) { car.tkSeen = true; return; }\n  }\n  function chTankDrive(car, dt) {\n"),
]
