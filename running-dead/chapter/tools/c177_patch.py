# c177: 장갑차 길이 15% 짧게 (폭은 그대로) · 방향을 천천히 튼다 (초당 약 125도) — 몸에 부딪힐 때마다 머리가 팍팍 튀던 것
C177_R = [
 ("CH_TK_K = MIL_K * 2 * 0.8,", "CH_TK_K = MIL_K * 2 * 0.8, CH_TK_KL = MIL_K * 2 * 0.8 * 0.85,   /* c177: 길이만 15% 짧게 */"),
 ("CAR_L * CH_TK_K", "CAR_L * CH_TK_KL", 8),
 ("car.kl = car.kw = CH_TK_K;", "car.kw = CH_TK_K; car.kl = CH_TK_KL;"),
 ("K[0].material.color.setHex(0x3c4a2a);", "K[0].material.color.setHex(0x3c4a2a); K[0].scale.x = 0.85;   /* c177 */"),
 ("const tr = new THREE.Mesh(new THREE.PlaneGeometry(CAR_L * 0.96, 0.13)", "const tr = new THREE.Mesh(new THREE.PlaneGeometry(CAR_L * 0.96 * 0.85, 0.13)"),
 ("      if (!car.rev && Math.hypot(car.vx, car.vz) > 0.3) car.h = Math.atan2(car.vz, car.vx);",
  "      if (!car.rev && Math.hypot(car.vx, car.vz) > 0.3) { const hw = Math.atan2(car.vz, car.vx); if (car.tank && !car.tkPh) { let d = hw - car.h; d = Math.atan2(Math.sin(d), Math.cos(d)); const st = 2.2 * dt; car.h += Math.abs(d) <= st ? d : Math.sign(d) * st; } else car.h = hw; }   /* c177: 장갑차는 천천히 돈다 */"),
]
