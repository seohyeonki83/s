# c183: 장갑차 체력 3배 · 돌진 주기 3분의 1 짧게 (10~15초 → 6.7~10초) · 평소(눈에 띈 뒤) 이동 속도 20% 빠르게
C183_R = [
 ("car.hpK = 10 * 0.95;", "car.hpK = 10 * 0.95 * 3;   /* c183: 3배 */"),
 ("rand(10, 15)", "rand(10 * 2 / 3, 15 * 2 / 3)", 2),
 ("car.tkSeen ? CAR_SPEED * CH_TR_SPD.sedan * CH_TR_SLOW / 2 :", "car.tkSeen ? CAR_SPEED * CH_TR_SPD.sedan * CH_TR_SLOW / 2 * 1.2 :   /* c183: 20% 빠르게 */"),
]
