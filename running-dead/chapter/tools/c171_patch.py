# c171: 장갑차 돌진 새로 — 10~15초마다 · 방향이 정해지면(좀비가 가장 많은 쪽) 끝까지 고정
#   ① 2초 동안 그 반대쪽으로 후진 (내 공격 거리의 3배 = 5.1칸) — 보고 피할 틈
#   ② 1.5초 동안 경찰차 최고 속도의 1.2배로 돌진 — 동료가 있어도 그대로 들이민다 · 벽은 평소의 3배로 부순다 (막혀도 돌진은 안 끊긴다)
C171_R = [
 ("dashAt: CH_TK_DASH_EVERY, dashT: 0,", "dashAt: rand(10, 15), dashT: 0, tkPh: null, tkPhT: 0,"),
 ("      car.dashT = 0;\n      if (car.rubBack <= 0 && car.rubCool <= 0) { car.rubBack = 0.3;", "      if (!car.tkPh && car.rubBack <= 0 && car.rubCool <= 0) { car.rubBack = 0.3;   /* c171: 돌진·후진 중엔 비비지 않는다 */"),
 ("if ((sg.tkT = (sg.tkT || 0) + dt) >= CH_TK_WALL_T)", "if ((sg.tkT = (sg.tkT || 0) + dt * (car.tkPh === 'dash' ? 3 : 1)) >= CH_TK_WALL_T)"),
 ("""    if (car.dashT > 0) { car.dashT -= dt; car.tkV = CAR_SPEED * 1.6; return; }
    if (car.dashAt <= 0 && car.rubBack <= 0) {
      const d = chTankDense(car);
      if (d) { const V = CAR_SPEED * 1.6; car.dashAt = CH_TK_DASH_EVERY; car.dashT = CH_TK_DASH_T; car.rev = false; car.vx = d[0] * V; car.vz = d[1] * V; car.h = Math.atan2(d[1], d[0]); car.tkV = V; return; }
    }
""", """    if (car.tkPh === 'back') {                 // c171 ① 후진 (방향 고정)
      const v = MELEE * 3 / 2; car.tkPhT -= dt; car.rev = true; car.h = car.tkDh; car.vx = -car.tkDx * v; car.vz = -car.tkDz * v; car.tkV = v;
      if (car.tkPhT <= 0) { car.tkPh = 'dash'; car.tkPhT = 1.5; }
      return;
    }
    if (car.tkPh === 'dash') {                 // c171 ② 돌진 (방향 고정 · 무리에 안 느려진다 — 걸음마다 속도를 다시 준다)
      const V = CAR_SPEED * 1.2; car.tkPhT -= dt; car.rev = false; car.h = car.tkDh; car.vx = car.tkDx * V; car.vz = car.tkDz * V; car.tkV = V; car.dashT = Math.max(0, car.tkPhT);
      if (car.tkPhT <= 0) { car.tkPh = null; car.dashT = 0; car.dashAt = rand(10, 15); }
      return;
    }
    if (car.dashAt <= 0 && car.rubBack <= 0) {
      const d = chTankDense(car);
      if (d) { car.tkPh = 'back'; car.tkPhT = 2; car.tkDx = d[0]; car.tkDz = d[1]; car.tkDh = Math.atan2(d[1], d[0]); car.rubBack = 0; return; }
    }
"""),
 (": car.tank ? car.tkV : CAR_SPEED * (car.mil ? 2 / 3 : 1), vmax = base * car.loadK;", ": car.tank ? car.tkV : CAR_SPEED * (car.mil ? 2 / 3 : 1), vmax = base * (car.tank && car.tkPh ? 1 : car.loadK);   /* c171: 돌진·후진 중엔 무리에 안 느려진다 */"),
 ("Object.assign(chSf, { on: false,", "if (chTank) chTank.tkPh = null; Object.assign(chSf, { on: false,"),
]
