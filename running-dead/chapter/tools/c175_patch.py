# c175: 장갑차가 돌진하려고 후진할 때와 돌진할 때 바퀴(궤도) 둘레에 연기가 피어오른다 — 돌진 때가 더 짙다
C175_R = [
 ("    if (car.tkPh === 'back') {                 // c171 ① 후진 (방향 고정)\n", "    if (car.tkPh) chTankSmoke(car, dt);   // c175\n    if (car.tkPh === 'back') {                 // c171 ① 후진 (방향 고정)\n"),
 ("  function chTankDrive(car, dt) {\n", """  function chTankSmoke(car, dt) {             // c175: 궤도 네 귀퉁이에서 연기 — 가는 반대쪽으로 흩어진다
    const dash = car.tkPh === 'dash';
    if ((car.smT = (car.smT || 0) - dt) > 0) return; car.smT = dash ? 0.035 : 0.06;
    const fx = Math.cos(car.h), fz = Math.sin(car.h), rx = -fz, rz = fx, hl = CAR_L * CH_TK_K / 2, hw = CAR_W * CH_TK_K / 2 * 0.85;
    const mv = dash ? 1 : -1;                  // 차가 가는 쪽 (후진이면 뒤)
    for (const sd of [-1, 1]) for (const e of [-1, 1]) {
      if (Math.random() < (dash ? 0.25 : 0.45)) continue;
      const x = car.x + fx * hl * e * 0.9 + rx * hw * sd, z = car.z + fz * hl * e * 0.9 + rz * hw * sd, sp = rand(0.8, 1.8) * (dash ? 1.6 : 1);
      const f = puff(x + rand(-0.15, 0.15), 0.25, z + rand(-0.15, 0.15), dash ? (Math.random() < 0.5 ? 0x4a4a4a : 0x6a6a6a) : (Math.random() < 0.5 ? 0x8a8a84 : 0xa8a8a0), rand(0.35, 0.55), rand(1.3, 2.0) * (dash ? 1.3 : 1), rand(0.55, 0.9), -fx * mv * sp + rx * sd * rand(0.3, 0.9), rand(0.3, 0.7), -fz * mv * sp + rz * sd * rand(0.3, 0.9), dash ? 0.75 : 0.6);
      f.s.renderOrder = -0.4;
    }
  }
  function chTankDrive(car, dt) {
"""),
]
