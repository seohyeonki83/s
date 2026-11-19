# c211: 죽은 장갑차가 계속 가던 버그 — 죽는 순간 속도·돌진 상태를 지우고, 잔해는 그 자리에 멈춰 있다
C211_R = [
 ("    car.foot.set(car.x, 0, car.z);\n    const o = car.obj; if (o) o.foot.set(car.x, 0, car.z);\n    if (car.wreck) return;",
  "    car.foot.set(car.x, 0, car.z);\n    const o = car.obj; if (o) o.foot.set(car.x, 0, car.z);\n    if (car.wreck) { car.vx = car.vz = 0; car.tkV = 0; car.tkPh = null; car.dashT = 0; car.spOn = false; return; }   // c211: 잔해는 멈춘다"),
 ("    if (car.tracer) car.tracer.visible = false;\n    for (let i = 0; i < 3; i++) boom(",
  "    if (car.tracer) car.tracer.visible = false;\n    car.vx = car.vz = 0; car.tkV = 0; car.tkPh = null; car.dashT = 0; car.spOn = false;   // c211\n    for (let i = 0; i < 3; i++) boom("),
]
