# c172: 장갑차 돌진에 '기세'(1 → 0) — 속도 · 벽 부수는 힘 · 차 부수는 힘 · 치는 데미지가 기세에 비례하고, 막는 것마다 기세가 깎인다
#   · 돌진 거리 11.3칸 (막혀 있던 시간은 안 센다 · 최대 3초) · 기세 0.08 아래면 끝
#   · 벽: 부수는 힘 = 평소의 6배 × 기세 (최소 1배) · 미는 동안 초당 0.3 · 하나 뚫을 때마다 0.15 → 벽 3장쯤 뚫고 네 번째에서 멈춘다
#   · 몸: 앞을 막은 몸 무게 / 장갑차 미는 힘(32) × 초당 0.5 + 처음 칠 때 몸 무게 / 장갑차 무게(40) × 0.25
#   · 차: 닿아 있는 동안 초당 0.6 · 차는 평소의 (1 + 2 × 기세)배로 부서진다
#   · 치는 데미지 = 보통 차에 치이는 데미지 × (0.5 + 기세)
C172_R = [
 ("if (d) { car.tkPh = 'back'; car.tkPhT = 2;", "if (d) { car.tkM = 1; car.tkLeft = CAR_SPEED * 1.2 * 1.5; car.tkLX = undefined; car.tkPh = 'back'; car.tkPhT = 2;"),
 ("      const V = CAR_SPEED * 1.2; car.tkPhT -= dt; car.rev = false; car.h = car.tkDh; car.vx = car.tkDx * V; car.vz = car.tkDz * V; car.tkV = V; car.dashT = Math.max(0, car.tkPhT);\n      if (car.tkPhT <= 0) {",
  "      car.tkM -= dt * (car.load || 0) / (CH_PUSH * chCarM(car)) * 0.5;   // c172: 앞을 막은 몸 무게만큼 기세가 깎인다\n"
  "      const V = CAR_SPEED * 1.2 * Math.max(0, car.tkM); car.tkPhT -= dt; if (car.tkLX !== undefined) car.tkLeft -= Math.hypot(car.x - car.tkLX, car.z - car.tkLZ); car.tkLX = car.x; car.tkLZ = car.z; car.rev = false; car.h = car.tkDh; car.vx = car.tkDx * V; car.vz = car.tkDz * V; car.tkV = V; car.dashT = Math.max(0, car.tkPhT);\n"
  "      if (car.tkLeft <= 0 || car.tkPhT <= -1.5 || car.tkM < 0.08) {   /* c172: 정한 거리(11.3칸)를 다 가거나 기세가 다하면 끝 (막혀 있던 시간은 안 센다 · 최대 3초) */"),
 ("if ((sg.tkT = (sg.tkT || 0) + dt * (car.tkPh === 'dash' ? 3 : 1)) >= CH_TK_WALL_T)", "if ((sg.tkT = (sg.tkT || 0) + dt * (car.tkPh === 'dash' ? Math.max(1, 6 * car.tkM) : 1)) >= CH_TK_WALL_T)"),
 ("      if (car.tkPX !== undefined) { car.x = car.tkPX; car.z = car.tkPZ; car.h = car.tkPH; car.foot.set(car.x, 0, car.z); if (o) o.foot.set(car.x, 0, car.z); }\n",
  "      if (car.tkPX !== undefined) { car.x = car.tkPX; car.z = car.tkPZ; car.h = car.tkPH; car.foot.set(car.x, 0, car.z); if (o) o.foot.set(car.x, 0, car.z); }\n"
  "      if (car.tkPh === 'dash') car.tkM -= 0.3 * dt;   // c172: 벽을 미는 동안 기세가 깎인다\n"),
 ("    B.tkCut = true;\n", "    B.tkCut = true;\n    if (car && car.tkPh === 'dash') car.tkM -= 0.15;   // c172: 벽 하나 뚫을 때마다\n"),
 ("    o.obj.hp -= MY_DAMAGE * 9.5 / 1.5 * chDt;\n", "    const T = chTank, ds = T && T.tkPh === 'dash';\n    o.obj.hp -= MY_DAMAGE * 9.5 / 1.5 * chDt * (ds ? 1 + 2 * T.tkM : 1);   // c172: 돌진 중엔 기세만큼 더 세게\n    if (ds) T.tkM -= 0.6 * chDt;   // c172: 차에 막히면 기세가 깎인다\n"),
 ("    const dmg = CAR_HIT_DMG * ve / CAR_SPEED;\n    if (isZombie(b))", "    const tkD = car.tank && car.tkPh === 'dash';\n    const dmg = CAR_HIT_DMG * ve / CAR_SPEED * (tkD ? 0.5 + Math.max(0, car.tkM) : 1);   // c172: 장갑차 돌진 = 기세만큼\n    if (tkD) car.tkM -= m / (CAR_MASS * chCarM(car)) * 0.25;\n    if (isZombie(b))"),
]
