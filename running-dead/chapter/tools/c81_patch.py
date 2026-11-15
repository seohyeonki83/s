# c81: 길거리 차 (출동한 경찰차·군인차는 빼고) — 달리는 차 수 3분의 1 줄임 (구역마다 3~4대 → 2~3대) · 운전 중 미는 힘 3분의 1 줄임 · 속도 20% 줄임
C81_R = [
  # 구역마다 달리는 차: 3대 또는 4대 (평균 3.5) → 2대 또는 3대 (3대는 세 번에 한 번 — 평균 2.33 = 3분의 2)
  ("want: 3 + (Math.random() < 0.5 ? 1 : 0)", "want: chTrWant()"),
  ("Z.want = 3 + (Math.random() < 0.5 ? 1 : 0);", "Z.want = chTrWant();"),
  # 운전 중 미는 힘: 길거리 차만 3분의 2 (경찰차·군인차는 그대로)
  ("  const chCarCap = (car) => CH_PUSH * chCarM(car) * (car.pushK || 1);",
   "  const CH_TR_PUSH = 2 / 3, CH_TR_SLOW = 0.8;   // c81: 길거리 차 — 운전 중 미는 힘 3분의 2 · 속도 80%\n"
   "  const chTrWant = () => 2 + (Math.random() < 1 / 3 ? 1 : 0);   // c81: 구역마다 달리는 차 2~3대 (평균 2.33)\n"
   "  const chCarCap = (car) => CH_PUSH * chCarM(car) * (car.tr ? CH_TR_PUSH : 1);"),
  # 속도: 전부 80%로 (차마다 다른 건 그대로 — 차종 기준 속도의 0.8~1.0배)
  ("spd = CAR_SPEED * CH_TR_SPD[type] * rand(1, CH_TR_FAST), who = [];", "spd = CAR_SPEED * CH_TR_SPD[type] * rand(1, CH_TR_FAST) * CH_TR_SLOW, who = [];"),
]
