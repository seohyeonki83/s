# c117: 물음표 수송차는 일반 차(승용차 속도 0.62)보다 10% 빠르다 — 세 종류 모두 같은 속도 (전엔 현금 0.55 · 구급 0.72 · 택배 0.48)
C117_R = [
 ("spd = CAR_SPEED * CH_TR_SPD[type] * rand(1, CH_TR_FAST) * CH_TR_SLOW,", "spd = CAR_SPEED * (loot ? CH_TR_SPD.sedan * 1.1 : CH_TR_SPD[type]) * rand(1, CH_TR_FAST) * CH_TR_SLOW,   /* c117: 수송차 = 승용차 속도의 1.1배 */"),
]
